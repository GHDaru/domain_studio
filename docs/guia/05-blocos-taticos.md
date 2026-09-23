---
id: aula-05-blocos-taticos
tipo: aula
titulo: "Aula 05 — Blocos táticos"
etapa: 5
resumo: "Como preencher cada agregado com os blocos de construção certos: entidades, objetos de valor, serviços, eventos, políticas, repositórios, fábricas e especificações."
relacionados: [aula-04-agregados-e-invariantes, aula-06-do-modelo-ao-codigo, dicionario-ddd, modelo-domain-studio]
termos: [projeto, especificacao, versao-especificacao, decomposicao, sugestao, revisao, modelo-tatico, elemento-de-modelo, regra-de-conformidade, violacao, diagrama, artefato-de-codigo]
---

# Aula 05 — Blocos táticos

> Os blocos táticos do Domain-Driven Design (DDD) são um vocabulário de **intenção**: chamar algo
> de Objeto de Valor diz "é imutável e comparado pelo conteúdo"; chamar de Evento diz "já aconteceu".
> Escolher o bloco certo é decidir onde cada regra mora — e o código passa a contar a história do negócio.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Distinguir** Entidade de Objeto de Valor com uma heurística simples.
2. **Distinguir** Serviço de Domínio de Serviço de Aplicação.
3. **Identificar** eventos de domínio e escrever políticas no formato "quando X então Y".
4. **Explicar** o papel de Repositórios, Fábricas e do padrão Especificação.
5. **Classificar** cada elemento de um agregado no bloco tático adequado.

## 2. O problema

Sem esta etapa, todo conceito vira "uma classe com `id`" e toda regra vai para um `Service`
genérico. Consequências:

- `Dinheiro`, `Endereco`, `VersaoEspecificacao` ganham identidade e setters; duas cópias iguais são tratadas como diferentes, e alguém altera a que não devia.
- Regras de negócio moram no controller ou no serviço de aplicação, misturadas com transação e serialização.
- Efeitos colaterais ("quando aceitar, aplique ao modelo") ficam escondidos dentro do método que aceita, acoplando agregados e contextos.
- Regras de validação viram `if`s duplicados em vários lugares, sem nome.

## 3. A ideia central

> **Cada regra de negócio tem um endereço: no objeto de valor, na raiz do agregado, num serviço de domínio, numa especificação ou numa política — nunca no serviço de aplicação.**

## 4. Passo a passo

Para cada agregado da [Aula 04](04-agregados-e-invariantes.md):

1. **Para cada conceito, pergunte:** *importa qual é, ou só o que contém?* Qual → **Entidade**.
   O que contém → **Objeto de Valor** (padrão; prefira-o).
2. **Mova comportamento para os objetos de valor** (validação, formatação, cálculo). Eles são imutáveis e fáceis de testar.
3. **Liste os fatos relevantes** no passado ("versão publicada", "sugestão aceita") → **Eventos de Domínio**, publicados pela raiz.
4. **Escreva as reações** como "quando `<Evento>` então `<ação>`" → **Políticas**. Cada política vira um *handler*.
5. **Operações que não pertencem a nenhum objeto** (envolvem vários agregados, ou dependem de algo externo) → **Serviço de Domínio**, com nome da linguagem ubíqua e interface no domínio.
6. **Regras de validação ou seleção reutilizáveis** → **Especificação** (objeto predicado com nome).
7. **Criação complexa** (várias invariantes, vários objetos) → **Fábrica** (método de classe ou serviço).
8. **Um Repositório por raiz de agregado**, com interface no domínio.
9. **O caso de uso** (carregar, chamar a raiz, salvar, publicar eventos) → **Serviço de Aplicação**, sem regra de negócio.

## 5. Fundamentos

Evans (*Blue Book*, cap. 5 e 6) apresenta os blocos; Vernon (*Implementing DDD*, cap. 5–8, 12) detalha a implementação.

**[Entidade](../ddd-dicionario.md#entidade-entity) × [Objeto de Valor](../ddd-dicionario.md#objeto-de-valor-value-object).**

| Critério | Entidade | Objeto de Valor (Value Object — VO) |
|----------|----------|-------------------------------------|
| Igualdade | Por identidade (`id`) | Por todos os atributos |
| Mutabilidade | Muda de estado ao longo do tempo | Imutável; "mudar" é substituir |
| Ciclo de vida | Tem história (criado, alterado, encerrado) | Descartável |
| No código deste projeto | Herda de `Entity` | `@dataclass(frozen=True)` |

**[Serviço de Domínio](../ddd-dicionario.md#serviço-de-domínio-domain-service) × [Serviço de Aplicação](../ddd-dicionario.md#serviço-de-aplicação-application-service).**
O de domínio *é* regra de negócio sem estado e fala a linguagem ubíqua. O de aplicação *orquestra*:
traduz entrada, carrega, delega, salva, publica. Teste rápido: se o método tem um `if` sobre uma
regra do negócio, ele não pertence à aplicação.

**[Evento de Domínio](../ddd-dicionario.md#evento-de-domínio-domain-event).** Nome no passado,
imutável, carrega IDs e os dados mínimos para quem reage. Registrado pela raiz; publicado após salvar.

**[Política](../ddd-dicionario.md#política-policy).** O dicionário segue Evans: uma regra variável
encapsulada em objeto (padrão *Strategy*, ex. `PoliticaDeDesconto`). O DomainStudio usa também o
sentido popularizado pelo *Event Storming*: uma reação "quando evento → comando". Os dois convivem;
no Modelo Tático, deixe claro qual dos dois é.

**[Repositório](../ddd-dicionario.md#repositório-repository).** Ilusão de coleção em memória, só
para raízes. Interface no domínio, implementação na infraestrutura.

**[Fábrica](../ddd-dicionario.md#fábrica-factory).** Use quando o construtor não expressa a
intenção ou quando criar exige verificar invariantes entre vários objetos.

**[Especificação](../ddd-dicionario.md#especificação-specification).** Predicado nomeado
(`is_satisfied_by`), combinável com e/ou/não. Serve para validar, selecionar e construir.
Atenção à colisão de nomes: no DomainStudio o padrão se chama `RegraDeConformidade`, porque
"Especificação" já é o texto do usuário (ver [Aula 03](03-contextos-delimitados-e-mapa.md)).

## 6. Na prática — o DomainStudio aplicado a si mesmo

Classificação proposta no [modelo](../modelo-domain-studio.md#4-contextos-delimitados):

| Bloco | Elementos no DomainStudio |
|-------|---------------------------|
| Entidade | `Sugestao` (interna a `Decomposicao`), `Subdominio`, `ContextoDelimitado`, `Agregado`, `ElementoTatico` |
| Objeto de Valor | `VersaoEspecificacao`, `Nome`, `EstadoDecomposicao`, `Revisao`, `RelacaoEntreContextos`, `Violacao`, `Diagrama`, `AlvoDeGeracao`, `ArtefatoDeCodigo` |
| Serviço de Domínio | `Decompositor` (porta para o LLM), `ValidadorDeConformidade`, `GeradorContextMap`, `GeradorC4`, `GeradorDiagramaClasses`, `GeradorDeCodigo` |
| Evento de Domínio | `ProjetoCriado`, `VersaoEspecificacaoPublicada`, `DecomposicaoConcluida`, `SugestaoAceita`, `SugestaoRejeitada`, `ModeloAlterado` |
| Política | "quando `SugestaoAceita` → aplicar elemento ao Modelo de Domínio" |
| Repositório | `ProjetoRepository`, `EspecificacaoRepository` (e um por raiz nos demais contextos) |
| Especificação | `RegraDeConformidade` (catálogo no contexto Conhecimento DDD) |

Observações:

- `Decompositor` é um serviço de domínio *cuja implementação* chama um Large Language Model (LLM).
  O domínio conhece só a interface; o adaptador é a Anticorruption Layer (ACL) da [Aula 03](03-contextos-delimitados-e-mapa.md).
- `Diagrama` é VO porque dois diagramas com o mesmo conteúdo são o mesmo diagrama: basta regerar.
- Nenhuma Fábrica foi proposta ainda; `Especificacao` é criada vazia, e a primeira candidata real
  seria a montagem de `Decomposicao` a partir da resposta do LLM.

Esboço do padrão Especificação para a regra "todo agregado tem exatamente uma raiz" (proposta):

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Violacao:
    regra: str
    elemento: str
    mensagem: str


@dataclass(frozen=True)
class AgregadoModelado:  # visão mínima de um agregado dentro do ModeloTatico
    nome: str
    raizes: tuple[str, ...]


class TodoAgregadoTemUmaRaiz:
    codigo = "agregado-uma-raiz"

    def is_satisfied_by(self, agregado: AgregadoModelado) -> bool:
        return len(agregado.raizes) == 1


def validar(agregados: list[AgregadoModelado]) -> list[Violacao]:
    regra = TodoAgregadoTemUmaRaiz()
    return [
        Violacao(regra.codigo, a.nome, f"{a.nome} tem {len(a.raizes)} raízes; esperado 1.")
        for a in agregados
        if not regra.is_satisfied_by(a)
    ]
```

A política "quando `SugestaoAceita` → aplicar ao modelo" vira um *handler* registrado no publicador
de eventos (ver [Aula 06](06-do-modelo-ao-codigo.md)). Ele cruza contextos, então chama a camada de
aplicação pública da Modelagem — nunca o domínio dela diretamente.

## 7. Erros comuns

- **Entidade por padrão.** Tudo ganha `id` "por via das dúvidas". Comece por VO; promova a Entidade quando a identidade importar.
- **VO mutável.** Um `dataclass` sem `frozen=True` convida a alterações que quebram invariantes silenciosamente.
- **Serviço de aplicação gordo.** Regras de negócio no caso de uso deixam o domínio anêmico.
- **Serviço de domínio como depósito.** `ModeloService` com 30 métodos é modelo anêmico com outro nome.
- **Evento no imperativo ou técnico.** `AtualizarModelo` e `RegistroInserido` não são fatos do negócio.
- **Política escondida no agregado.** A raiz que aceita a sugestão e já altera o modelo acopla dois contextos.
- **Repositório genérico.** `Repository[T]` com `find_by_any_field` expõe detalhes de persistência ao domínio.

## 8. Verificação

- [ ] Cada conceito do agregado tem um bloco tático atribuído e justificado pela heurística.
- [ ] Todo Objeto de Valor é imutável e comparado por atributos.
- [ ] Todo evento tem nome no passado e carrega IDs, não objetos.
- [ ] Toda reação entre agregados está escrita como "quando X então Y".
- [ ] Serviços de aplicação não contêm regra de negócio.
- [ ] Regras de validação reutilizáveis têm nome próprio (Especificação).
- [ ] Só raízes têm repositório.

Perguntas de autoavaliação:

1. `Revisao` é VO, mas `Sugestao` é Entidade. Qual pergunta da heurística separa os dois?
2. Por que `ValidadorDeConformidade` é serviço de domínio e não método de `ModeloTatico`?
3. Em que situação `Diagrama` precisaria virar Entidade?

## 9. Para saber mais

- Anterior: [Aula 04 — Agregados e invariantes](04-agregados-e-invariantes.md)
- Próxima: [Aula 06 — Do modelo ao código](06-do-modelo-ao-codigo.md)
- [Dicionário de DDD](../ddd-dicionario.md) — seções 3 e 6.
- [Modelo do DomainStudio](../modelo-domain-studio.md) — seção 4.
- Eric Evans, *Domain-Driven Design* (2003), cap. 5, 6, 9 e 10 (Specification, Supple Design).
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013), cap. 5–8 e 12.
- Alberto Brandolini, *Introducing EventStorming* (Leanpub) — políticas "quando… então…".
