---
id: docs-readme
tipo: indice
titulo: "DomainStudio — Documentação"
resumo: "Ponto de entrada: estrutura da documentação, roadmap e referências."
relacionados: [aula-00-como-usar, dicionario-ddd, modelo-domain-studio, plano-de-implementacao, grafo]
---
# DomainStudio — Documentação

Projeto: aplicação onde o usuário define a especificação do domínio e o sistema
decompõe progressivamente em modelos DDD, visualizações (C4, PlantUML, Context
Mapper) e, por fim, código.

## Estrutura atual

```
CLAUDE.md / AGENTS.md            ← instruções para agentes de IA (AGENTS.md é link)
docs/
 ├── README.md                   ← este índice
 ├── guia/                       ← aulas 00–07: o método passo a passo (vira a ajuda do produto)
 ├── ddd-dicionario.md           ← dicionário de definições (base de conhecimento)
 ├── modelo-domain-studio.md     ← o DomainStudio modelado pelo próprio método
 ├── modelo/
 │    ├── linguagem-ubiqua.yaml  ← FONTE do vocabulário (→ linguagem-ubiqua.md gerado)
 │    ├── fluxo.yaml             ← FONTE do fluxo e das dúvidas
 │    └── domain_studio.cml      ← mapa de contexto em Context Mapper DSL
 ├── plano-de-implementacao.md   ← stack, estrutura, API, marcos e backlog
 ├── grafo.md                    ← grafo navegável (gerado)
 └── indice.jsonl                ← um documento por linha, para consulta da IA (gerado)
prototipos/validacao-linguagem.html ← interface de validação do fluxo e do vocabulário
scripts/gerar_docs.py            ← gera as visões derivadas; `--check` verifica o grafo
backend/                         ← API FastAPI (ver backend/README.md)
```

Comece pela [Aula 00](guia/00-como-usar.md). Visão geral: [grafo](grafo.md).

## Roadmap conceitual

1. **Dicionário de DDD** ✅ — termos e padrões de referência.
   - **Modelo do próprio DomainStudio** ✅, **plano** ✅, **guia em aulas** ✅, **artefatos para IA** ✅.
2. **Especificação de entrada e validação** 🔶 — texto livre → `fluxo.yaml` + `linguagem-ubiqua.yaml`, validados na interface.
3. **Decomposição** — do texto → Subdomínios → Contextos Delimitados → Agregados → Entidades/VOs.
4. **Visualização** — geração de diagramas C4, PlantUML e Context Map.
5. **Geração de código** — scaffolding a partir do modelo decomposto.

## Referências

- Evans, Eric. *Domain-Driven Design* (2003) — "Blue Book".
- Vernon, Vaughn. *DDD Distilled* (2016).
- Vernon, Vaughn. *Implementing Domain-Driven Design* (2013).
- [Context Mapper](https://contextmapper.org/) — DSL para Context Maps.
- [C4 Model](https://c4model.com/) — Simon Brown.
- [PlantUML](https://plantuml.com/).
