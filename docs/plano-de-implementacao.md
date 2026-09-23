---
id: plano-de-implementacao
tipo: plano
titulo: "Plano de Implementação"
resumo: "Stack FastAPI, estrutura hexagonal por contexto, rascunho da API e marcos."
relacionados: [modelo-domain-studio, aula-06-do-modelo-ao-codigo, aula-07-artefatos-para-ia]
---
# Plano de Implementação — DomainStudio

> O código segue o modelo definido em [modelo-domain-studio.md](modelo-domain-studio.md):
> cada contexto delimitado vira um módulo, e cada módulo segue arquitetura hexagonal.
> Quando o DomainStudio gerar código (M5), o alvo `python-fastapi` deve produzir
> exatamente esta estrutura — o sistema tem que conseguir gerar a si mesmo.

---

## 1. Decisões de stack

| Tema | Decisão | Motivo |
|------|---------|--------|
| Linguagem | Python ≥ 3.11 | Tipagem moderna, ecossistema de LLM. |
| API | **FastAPI** | Definido pelo projeto; OpenAPI automático. |
| Domínio | `dataclasses` puras, sem dependência de framework | Domínio isolado de tecnologia (hexagonal). |
| DTOs da API | Pydantic v2 (só na camada `api/`) | Validação na borda, domínio limpo. |
| Persistência | Repositórios em memória (M1–M4) → SQLAlchemy 2 + SQLite/PostgreSQL (M6) | Adiar infraestrutura até o modelo estabilizar. |
| Eventos | Publicador in-process síncrono | Suficiente para monólito modular; troca por broker depois. |
| LLM | Porta `Decompositor` + adaptador (ACL) | Provedor substituível; testes com adaptador falso. |
| Diagramas | Gerados como **texto** (CML, PlantUML, C4-PlantUML) | Renderização fica com o front/ferramenta externa. |
| Testes | pytest + httpx (`TestClient`) | Padrão FastAPI. |
| Qualidade | ruff (lint + format) | Uma ferramenta só. |
| Deploy | Monólito modular, um processo | Contextos separados em módulos; extração para serviços só se necessário. |

Frontend fica fora deste plano; a API é o produto inicial (Swagger em `/docs`).

---

## 2. Estrutura do backend

```
backend/
 ├── pyproject.toml
 ├── src/domain_studio/
 │    ├── main.py                    ← app factory, registra routers dos contextos
 │    ├── shared/                    ← Shared Kernel técnico
 │    │    └── domain.py             ← Entity, DomainEvent, erros de domínio
 │    ├── especificacao/             ← um pacote por Contexto Delimitado
 │    │    ├── domain/               ← agregados, VOs, eventos, portas de repositório
 │    │    ├── application/          ← serviços de aplicação (casos de uso)
 │    │    ├── infrastructure/       ← adaptadores (repositórios, LLM, …)
 │    │    └── api/                  ← router FastAPI + schemas Pydantic
 │    ├── decomposicao/
 │    ├── modelagem/
 │    ├── visualizacao/
 │    ├── geracao_codigo/
 │    └── conhecimento/
 └── tests/                          ← espelha a estrutura de src/
```

**Regra de dependência:** `api → application → domain ← infrastructure`.
Um contexto só conversa com outro pela camada `application` pública dele
(ou por eventos) — nunca importando o `domain` do outro. Um teste de arquitetura
vai garantir isso.

---

## 3. API (v1, rascunho)

| Método | Rota | Contexto |
|--------|------|----------|
| `POST` | `/projetos` | Especificação |
| `GET` | `/projetos/{id}` | Especificação |
| `POST` | `/projetos/{id}/especificacao/versoes` | Especificação |
| `GET` | `/projetos/{id}/especificacao` | Especificação |
| `POST` | `/projetos/{id}/decomposicoes` | Decomposição |
| `GET` | `/decomposicoes/{id}` | Decomposição |
| `POST` | `/decomposicoes/{id}/sugestoes/{sid}/revisao` | Decomposição |
| `GET` | `/projetos/{id}/modelo` | Modelagem |
| `POST/PATCH/DELETE` | `/projetos/{id}/modelo/subdominios…`, `/contextos…`, `/relacoes…` | Modelagem |
| `GET/POST…` | `/projetos/{id}/contextos/{cid}/modelo-tatico…` | Modelagem |
| `GET` | `/projetos/{id}/modelo/validacao` | Modelagem |
| `GET` | `/projetos/{id}/diagramas/{tipo}` (`context-map`, `c4-contexto`, `classes`) | Visualização |
| `POST` | `/projetos/{id}/geracoes-codigo` | Geração de Código |
| `GET` | `/conhecimento/conceitos`, `/conhecimento/regras` | Conhecimento DDD |
| `GET` | `/health` | — |

---

## 4. Marcos

Ordem ditada pelo próprio método: **primeiro a linguagem validada** (etapa 1), depois o
**núcleo** (Modelagem), e só então o que depende dele. A Especificação — subdomínio de
suporte — entra só no mínimo necessário junto com a Modelagem.

| Marco | Entrega | Critério de pronto |
|-------|---------|--------------------|
| **M0 — Fundação** ✅ | Estrutura do backend, Shared Kernel, `/health`, testes, ruff. | `pytest` verde; `uvicorn` sobe. |
| **M1 — Linguagem e fluxo validados** 🔶 | Fontes únicas (`linguagem-ubiqua.yaml`, `fluxo.yaml`) ✅, interface de validação ([protótipo](../prototipos/validacao-linguagem.html)) ✅, gerador + verificação (`scripts/gerar_docs.py`) ✅, **validação pelo especialista** ⏳. | Todo termo e passo com decisão; toda dúvida respondida; `gerar_docs.py --check` verde. |
| **M2 — Modelagem (núcleo)** | `ModeloEstrategico` e `ModeloTatico` com invariantes; edição via API; `ValidadorDeConformidade`. Especificação mínima (`Projeto`, `Especificacao` versionada) como insumo. | Modelar o próprio DomainStudio pela API e validar sem violações. |
| **M3 — Visualização** | Geradores CML, PlantUML de classes e C4 de contexto. | CML gerado do modelo do DomainStudio equivale a `docs/modelo/domain_studio.cml`. |
| **M4 — Decomposição (núcleo)** | Agregado `Decomposicao`, porta `Decompositor`, adaptador LLM, revisão, política que aplica sugestões aceitas. | Decompor a §1 do modelo e obter sugestões próximas do modelo manual. |
| **M5 — Código e artefatos para IA** | Alvo `python-fastapi` + artefatos para IA por contexto ([Aula 07](guia/07-artefatos-para-ia.md)). | Código gerado para o DomainStudio tem a estrutura da seção 2, passa no lint e traz `CLAUDE.md` por contexto. |
| **M6 — Persistência e acesso** | SQLAlchemy + migrações (Alembic); autenticação. | Dados sobrevivem a restart; multiusuário. |

### Critério de dogfooding
Cada marco é validado usando o **próprio DomainStudio como caso de teste**: o
modelo em `docs/modelo-domain-studio.md` vira uma fixture de teste que
atravessa todos os contextos.

---

## 5. Backlog do roadmap (depois de M6, em ordem de valor)

1. **Rastreabilidade** — cada elemento do modelo aponta o trecho da especificação que o originou.
2. **Detecção de ambiguidade** — mesmo termo com sentidos diferentes sugere novo contexto delimitado.
3. **Event Storming** como etapa intermediária da decomposição (eventos, comandos, atores, políticas).
4. **Evolução do modelo** — diff entre versões e impacto de uma mudança na especificação.
5. **Métricas de qualidade** — tamanho de agregado, acoplamento entre contextos.
6. **Round-trip** — importar/exportar CML; engenharia reversa de código existente.
7. **Registro de decisões** — Architecture Decision Records (ADRs) + índice JSONL, só por acréscimo.
8. **Mais alvos de geração** — Java/Spring, TypeScript/NestJS; testes gerados das invariantes.
9. **Colaboração e interface** — editor visual do mapa de contexto, papéis, comentários.
10. **Acesso por agentes** — servidor Model Context Protocol (MCP) / CLI.

---

## 6. Próximo passo

**Você valida a linguagem e o fluxo** no protótipo, cola o YAML de decisões em
`docs/modelo/decisoes-validacao.yaml` e roda `python3 scripts/gerar_docs.py`. Com a
linguagem validada, começa o M2.
