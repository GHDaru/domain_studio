# DomainStudio — Documentação

Projeto: aplicação onde o usuário define a especificação do domínio e o sistema
decompõe progressivamente em modelos DDD, visualizações (C4, PlantUML, Context
Mapper) e, por fim, código.

## Estrutura atual

```
docs/
 ├── README.md            ← este índice
 └── ddd-dicionario.md    ← dicionário de definições (base de conhecimento)
```

## Roadmap conceitual

1. **Dicionário de DDD** ✅ — termos e padrões de referência.
2. **Especificação de entrada** — formato/DSL para o usuário descrever o domínio.
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
