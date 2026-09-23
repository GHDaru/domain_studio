---
id: aula-06-do-modelo-ao-codigo
tipo: aula
titulo: "Aula 06 — Do modelo ao código"
etapa: 6
resumo: "Como transformar cada contexto delimitado num módulo Python com arquitetura hexagonal — domínio puro em dataclasses, casos de uso na aplicação, adaptadores na infraestrutura e FastAPI na borda."
relacionados: [aula-05-blocos-taticos, aula-07-artefatos-para-ia, dicionario-ddd, modelo-domain-studio, plano-de-implementacao]
termos: [projeto, especificacao, versao-especificacao, modelo-tatico, artefato-de-codigo]
---

# Aula 06 — Do modelo ao código

> Em Domain-Driven Design (DDD) com arquitetura hexagonal, cada contexto delimitado vira um módulo
> em que **o domínio não importa nada de fora** — nem FastAPI, nem Pydantic, nem banco. A tecnologia
> fica na borda e depende do domínio, nunca o contrário.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** a arquitetura hexagonal (portas e adaptadores) e a regra de dependência.
2. **Organizar** um contexto delimitado em `domain/`, `application/`, `infrastructure/` e `api/`.
3. **Distinguir** dataclasses puras no domínio de modelos Pydantic na borda.
4. **Implementar** um agregado, uma porta de repositório, um repositório em memória, um serviço de aplicação e um router FastAPI.

## 2. O problema

Um modelo bem desenhado se perde no código quando:
- a entidade de domínio **é** o modelo do Object-Relational Mapper (ORM) ou o schema Pydantic, e mudar tabela ou Application Programming Interface (API) mexe na regra;
- o router chama o banco diretamente e as invariantes ficam espalhadas por endpoints;
- um contexto importa as classes de domínio de outro, e as fronteiras do mapa de contexto viram ficção.

## 3. A ideia central

> **As dependências apontam para dentro: `api → application → domain ← infrastructure`.**

O domínio define **portas** (como `EspecificacaoRepository`); a infraestrutura fornece **adaptadores**;
a aplicação orquestra; a API traduz HyperText Transfer Protocol (HTTP) em casos de uso. Trocar memória
por banco, ou um provedor de Large Language Model (LLM) por outro, não toca o domínio.

## 4. Passo a passo

1. **Crie um pacote por contexto delimitado** em `backend/src/domain_studio/<contexto>/` (seção 5).
2. **Escreva o domínio primeiro**, com `dataclasses` e as bases de `shared/domain.py`:
   objeto de valor (Value Object — VO) → `@dataclass(frozen=True)`; entidade → `Entity`; raiz → `AggregateRoot`; evento → `DomainEvent`.
3. **Implemente as invariantes nos métodos da raiz**, lançando `DomainError`.
4. **Declare a porta do repositório** no domínio como `typing.Protocol`.
5. **Implemente o repositório em memória** na infraestrutura. Banco só quando o modelo estabilizar.
6. **Escreva o serviço de aplicação**: carrega, chama a raiz, salva, publica `pull_events()`.
7. **Exponha pela API** com schemas Pydantic; converta `DomainError` em resposta HTTP; registre o
   router em `main.py`. Teste o domínio sem FastAPI e a API com `TestClient`.

## 5. Fundamentos

**[Arquitetura Hexagonal](../ddd-dicionario.md#arquitetura-hexagonal-ports-and-adapters)**
(Alistair Cockburn, 2005) coloca o domínio no centro e o isola por portas. Vernon
(*Implementing DDD*, cap. 4) a recomenda como arquitetura padrão para DDD; as variantes
[Cebola](../ddd-dicionario.md#arquitetura-cebola-onion-architecture) e
[Clean Architecture](../ddd-dicionario.md#clean-architecture) compartilham a mesma regra de dependência.

Estrutura do [plano de implementação](../plano-de-implementacao.md#2-estrutura-do-backend):
| Camada | Contém | Pode importar |
|--------|--------|---------------|
| `domain/` | Agregados, VOs, eventos, portas (Protocol), serviços de domínio | Só `shared/` e biblioteca padrão |
| `application/` | Serviços de aplicação (casos de uso) | `domain/` |
| `infrastructure/` | Repositórios, adaptador do LLM, publicador de eventos | `domain/` |
| `api/` | Router FastAPI, schemas Pydantic (Data Transfer Objects — DTOs) | `application/`, `domain/` (tipos e erros); `infrastructure/` só para montar dependências |

**Dataclasses no domínio, Pydantic na borda:** Pydantic valida o *formato* do que chega de fora; o
domínio valida *regras de negócio*. Separados, os DTOs mudam (nova versão da API) sem tocar o agregado.

**Entre contextos:** um contexto só usa a camada `application` pública de outro, ou reage a eventos.
Nunca importa o `domain` alheio — é o que mantém o [mapa de contexto](03-contextos-delimitados-e-mapa.md) verdadeiro.

## 6. Na prática — o DomainStudio aplicado a si mesmo

Hoje o repositório tem só a fundação (marco M0): `main.py` com `/health` e `shared/domain.py`. Os
trechos abaixo são uma **proposta** do contexto Especificação (marco M1); ainda não existem no repositório.

**`especificacao/domain/especificacao.py`** — objeto de valor, evento e agregado:

```python
from dataclasses import dataclass, field
from datetime import UTC, datetime

from domain_studio.shared.domain import AggregateRoot, DomainError, DomainEvent


@dataclass(frozen=True)
class VersaoEspecificacao:
    numero: int
    texto: str
    criada_em: datetime


@dataclass(frozen=True, kw_only=True)
class VersaoEspecificacaoPublicada(DomainEvent):
    projeto_id: str
    numero: int


@dataclass(eq=False, kw_only=True)
class Especificacao(AggregateRoot):
    projeto_id: str  # referência por identidade ao agregado Projeto
    versoes: list[VersaoEspecificacao] = field(default_factory=list)

    def publicar(self, texto: str) -> VersaoEspecificacao:
        if not texto.strip():
            raise DomainError("A especificação não pode ser publicada vazia.")
        # invariante: numeração sequencial
        versao = VersaoEspecificacao(len(self.versoes) + 1, texto, datetime.now(UTC))
        self.versoes.append(versao)  # versões anteriores nunca são alteradas
        self.record(VersaoEspecificacaoPublicada(projeto_id=self.projeto_id, numero=versao.numero))
        return versao
```

A porta (`domain/repositorio.py`) e o adaptador (`infrastructure/em_memoria.py`), que a satisfaz só por ter os mesmos métodos:

```python
from typing import Protocol

from domain_studio.especificacao.domain.especificacao import Especificacao


class EspecificacaoRepository(Protocol):  # domain/repositorio.py
    def por_projeto(self, projeto_id: str) -> Especificacao | None: ...
    def salvar(self, especificacao: Especificacao) -> None: ...


class EspecificacaoRepositoryEmMemoria:  # infrastructure/em_memoria.py
    def __init__(self) -> None:
        self._por_projeto: dict[str, Especificacao] = {}

    def por_projeto(self, projeto_id: str) -> Especificacao | None:
        return self._por_projeto.get(projeto_id)

    def salvar(self, especificacao: Especificacao) -> None:
        self._por_projeto[especificacao.projeto_id] = especificacao
```

**`especificacao/application/publicar_versao.py`** — o caso de uso, sem regra de negócio:

```python
from collections.abc import Callable

from domain_studio.especificacao.domain.especificacao import Especificacao, VersaoEspecificacao
from domain_studio.especificacao.domain.repositorio import EspecificacaoRepository
from domain_studio.shared.domain import DomainEvent

PublicarEventos = Callable[[list[DomainEvent]], None]


class PublicarVersao:
    def __init__(self, repositorio: EspecificacaoRepository, publicar: PublicarEventos) -> None:
        self._repositorio = repositorio
        self._publicar = publicar

    def executar(self, projeto_id: str, texto: str) -> VersaoEspecificacao:
        especificacao = self._repositorio.por_projeto(projeto_id) or Especificacao(
            projeto_id=projeto_id
        )
        versao = especificacao.publicar(texto)
        self._repositorio.salvar(especificacao)
        self._publicar(especificacao.pull_events())
        return versao
```

**`especificacao/api/router.py`** — Pydantic só aqui:

```python
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from domain_studio.especificacao.application.publicar_versao import PublicarVersao
from domain_studio.especificacao.infrastructure import em_memoria
from domain_studio.shared.domain import DomainError

# montagem das dependências; o publicador real de eventos chega no M1
_caso_de_uso = PublicarVersao(em_memoria.EspecificacaoRepositoryEmMemoria(), lambda _: None)


class PublicarVersaoIn(BaseModel):
    texto: str = Field(min_length=1)


class VersaoOut(BaseModel):
    numero: int
    texto: str
    criada_em: datetime


router = APIRouter(prefix="/projetos", tags=["especificacao"])


@router.post("/{projeto_id}/especificacao/versoes", status_code=201)
def publicar_versao(
    projeto_id: str,
    dados: PublicarVersaoIn,
    caso_de_uso: Annotated[PublicarVersao, Depends(lambda: _caso_de_uso)],
) -> VersaoOut:
    try:
        versao = caso_de_uso.executar(projeto_id, dados.texto)
    except DomainError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro
    return VersaoOut(numero=versao.numero, texto=versao.texto, criada_em=versao.criada_em)
```

Em `main.py`, dentro de `create_app()`: `app.include_router(router)`.

**Trade-offs assumidos:** `versoes` é lista pública por simplicidade; o caso de uso ainda não verifica se o `Projeto` existe; a ligação (*wiring*) é manual; o publicador é síncrono e in-process, como no [plano](../plano-de-implementacao.md#1-decisões-de-stack).
No marco M5, o alvo `python-fastapi` da Geração de Código deve produzir exatamente esta estrutura como Artefato de Código — o sistema precisa conseguir gerar a si mesmo.

## 7. Erros comuns

- **Pydantic no domínio.** O agregado vira schema de API; mudar o contrato HTTP mexe na regra.
- **Domínio importando infraestrutura.** `from sqlalchemy import …` em `domain/` inverte a regra de dependência.
- **Publicar eventos antes de salvar.** Quem reage pode ler um estado que ainda não existe.
- **Importar o `domain` de outro contexto.** Acoplamento que o mapa de contexto não declara.

## 8. Verificação

- [ ] Nenhum arquivo em `domain/` importa `fastapi`, `pydantic` ou bibliotecas de banco.
- [ ] Cada raiz de agregado herda de `AggregateRoot` e cada VO é `frozen=True`.
- [ ] Cada repositório é um `Protocol` no domínio e tem ao menos uma implementação em memória.
- [ ] Serviços de aplicação salvam antes de publicar eventos e não contêm `if` de regra de negócio.
- [ ] Existem testes de domínio que não sobem a aplicação.

Perguntas de autoavaliação:

1. Por que `Especificacao` usa `eq=False` no `@dataclass`? (Dica: veja `Entity.__eq__` em `shared/domain.py`.)
2. O que muda, e o que não muda, quando o repositório em memória for trocado por SQLAlchemy no M6?
3. Onde você colocaria o adaptador do LLM que implementa a porta `Decompositor`?

## 9. Para saber mais

- Anterior: [Aula 05 — Blocos táticos](05-blocos-taticos.md)
- Próxima: [Aula 07 — Artefatos para Inteligência Artificial (IA)](07-artefatos-para-ia.md)
- [Dicionário de DDD](../ddd-dicionario.md) — seção 4.
- [Modelo do DomainStudio](../modelo-domain-studio.md) — seção 4.1; [Plano](../plano-de-implementacao.md) — seções 1, 2 e 4.
- Alistair Cockburn, "Hexagonal Architecture" (2005), alistair.cockburn.us.
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013), cap. 4 "Architecture" e cap. 14 "Application".
- Harry Percival e Bob Gregory, *Architecture Patterns with Python* (O'Reilly, 2020) — repositório, unidade de trabalho e eventos em Python.
