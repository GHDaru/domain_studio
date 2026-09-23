---
id: linguagem-ubiqua
tipo: glossario
titulo: "Linguagem Ubíqua do DomainStudio"
resumo: "Vocabulário do produto, por contexto delimitado, com status de validação."
relacionados: [modelo-domain-studio, aula-01-linguagem-ubiqua-e-fluxo]
---
<!-- GERADO por scripts/gerar_docs.py — não edite; edite a fonte e regenere. -->

# Linguagem Ubíqua do DomainStudio

> Fonte: [`linguagem-ubiqua.yaml`](linguagem-ubiqua.yaml) + decisões de validação.
> Status **proposto** = hipótese ainda não confirmada pelo especialista de domínio.

## Especificação

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="projeto"></a>**Projeto** | `Projeto` | agregado | Espaço de trabalho de um domínio de negócio. Agrupa especificação, modelo e artefatos gerados. | workspace, área de trabalho | P1 | proposto |
| <a id="especificacao"></a>**Especificação** | `Especificacao` | agregado | Texto livre que descreve o domínio do negócio. Evolui por versões imutáveis. | requisitos, documento | P2, P3 | proposto |
| <a id="versao-especificacao"></a>**Versão da Especificação** | `VersaoEspecificacao` | objeto-de-valor | Retrato imutável do texto num momento. Toda decomposição aponta para exatamente uma versão. | revisão, rascunho | P2, P4 | proposto |

## Decomposição

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="decomposicao"></a>**Decomposição** | `Decomposicao` | agregado | Execução que transforma uma versão da especificação em sugestões de modelo. | análise, processamento | P4 | proposto |
| <a id="sugestao"></a>**Sugestão** | `Sugestao` | entidade | Elemento de modelo proposto pela decomposição, aguardando revisão humana. | proposta, recomendação | P4, P5 | proposto |
| <a id="revisao"></a>**Revisão** | `Revisao` | objeto-de-valor | Decisão do usuário sobre uma sugestão — aceitar, editar e aceitar, ou rejeitar. | aprovação | P5 | proposto |

## Modelagem

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="modelo-estrategico"></a>**Modelo Estratégico** | `ModeloEstrategico` | agregado | Subdomínios, contextos delimitados e o mapa de contexto de um projeto. | arquitetura | P6, P7 | proposto |
| <a id="modelo-tatico"></a>**Modelo Tático** | `ModeloTatico` | agregado | Blocos de construção (agregados, entidades, objetos de valor, serviços, eventos) de UM contexto delimitado. | modelo de dados, schema | P6, P8 | proposto |
| <a id="elemento-de-modelo"></a>**Elemento de Modelo** | `ElementoDeModelo` | conceito | Qualquer item de um modelo — um subdomínio, um agregado, um objeto de valor. | nó, item | P5 | proposto |
| <a id="violacao"></a>**Violação** | `Violacao` | objeto-de-valor | Resultado de uma regra de conformidade não atendida por um elemento de modelo. | erro, warning | P6 | proposto |

## Visualização

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="diagrama"></a>**Diagrama** | `Diagrama` | objeto-de-valor | Representação textual gerada a partir do modelo (Context Mapper DSL, PlantUML, C4). | imagem, desenho | P7 | proposto |

## Geração de Código

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="artefato-de-codigo"></a>**Artefato de Código** | `ArtefatoDeCodigo` | objeto-de-valor | Arquivo gerado a partir do modelo tático para um alvo (ex. python-fastapi). | template, boilerplate | P8 | proposto |
| <a id="artefato-para-ia"></a>**Artefato para IA** | `ArtefatoParaIA` | objeto-de-valor | Arquivo gerado para ser carregado por agentes de IA (instrução por contexto, glossário, grafo, índice de decisões). | prompt, memória | P8 | proposto |

## Conhecimento DDD

| Termo | Código | Tipo | Definição | Evitar | Passos | Status |
|---|---|---|---|---|---|---|
| <a id="regra-de-conformidade"></a>**Regra de Conformidade** | `RegraDeConformidade` | especificacao | Regra do DDD verificável automaticamente sobre um modelo (ex. todo agregado tem exatamente uma raiz). | lint, validação | P6 | proposto |
