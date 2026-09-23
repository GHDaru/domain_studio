---
id: aula-03-contextos-delimitados-e-mapa
tipo: aula
titulo: "Aula 03 — Contextos delimitados e mapa de contexto"
etapa: 3
resumo: "Como traçar fronteiras linguísticas entre modelos, nomear as relações entre elas com os padrões de integração e registrar tudo num mapa de contexto em Context Mapper."
relacionados: [aula-02-subdominios-e-destilacao, aula-04-agregados-e-invariantes, dicionario-ddd, modelo-domain-studio]
termos: [especificacao, versao-especificacao, decomposicao, sugestao, modelo-estrategico, modelo-tatico, elemento-de-modelo, regra-de-conformidade, diagrama]
---

# Aula 03 — Contextos delimitados e mapa de contexto

> Em Domain-Driven Design (DDD), um contexto delimitado é a fronteira dentro da qual cada palavra tem **um único significado**.
> Quando a mesma palavra muda de sentido, você cruzou uma fronteira — e precisa dizer, no
> mapa de contexto, quem manda em quem e como os dois modelos conversam.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** por que o contexto delimitado é uma fronteira *linguística* antes de ser técnica.
2. **Aplicar** a heurística "mesma palavra, significado diferente" para achar fronteiras.
3. **Distinguir** os padrões de integração: Customer–Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language, Shared Kernel e Separate Ways.
4. **Ler e escrever** um mapa de contexto em Context Mapper Language (CML).

## 2. O problema

Sem fronteiras explícitas, nasce o **modelo único corporativo**: uma classe `Produto` com 60
atributos que serve a Vendas, Logística e Fiscal ao mesmo tempo. Cada mudança quebra alguém; cada
time tem medo de mexer; as palavras perdem precisão porque precisam agradar a todos.

E quando as fronteiras existem mas as **relações** não são nomeadas, as integrações acontecem por
acidente: um módulo importa as classes internas do outro, um formato externo vaza para dentro do
domínio, e ninguém sabe quem precisa ser consultado antes de mudar um contrato.

## 3. A ideia central

> **Um modelo, uma linguagem, uma fronteira; entre fronteiras, relações com nome e dono.**

Dentro do contexto, o modelo é coeso e a linguagem ubíqua é rigorosa. Fora dele, o mesmo termo
pode significar outra coisa — e tudo bem, desde que a tradução seja explícita. O mapa de contexto
é o documento que torna essas traduções e dependências visíveis.

## 4. Passo a passo

1. **Comece 1:1 com os subdomínios** da [Aula 02](02-subdominios-e-destilacao.md): cada subdomínio
   Núcleo ou Suporte vira um contexto candidato. Genéricos viram sistemas externos.
2. **Liste os termos de cada candidato** a partir da linguagem ubíqua.
3. **Procure palavras repetidas** entre candidatos. Para cada uma, pergunte: *significa a mesma
   coisa aqui e ali?* Se não, a fronteira está certa e cada lado mantém seu significado. Se o
   mesmo termo tem dois sentidos *dentro* de um candidato, divida-o.
4. **Escreva a declaração de visão de cada contexto** (uma frase: o que ele faz e para quem).
5. **Para cada par que troca informação, decida a direção:** quem é *upstream* (U, influencia) e
   quem é *downstream* (D, é influenciado)? A seta vai de U para D.
6. **Escolha o padrão da relação** com a tabela da seção 5. Pergunte: o downstream tem poder de
   negociação? O modelo do upstream é bom o bastante para ser adotado? Há vários consumidores?
7. **Proteja o Núcleo.** Todo sistema externo ou legado que alimenta um contexto Núcleo passa por
   uma Anticorruption Layer (ACL).
8. **Registre o mapa em CML** (seção 6) e gere o [diagrama](../ddd-dicionario.md#7-diagramas-e-notação-para-a-ferramenta)
   a partir dele. O texto é a fonte; a imagem é derivada.

## 5. Fundamentos

**Contexto delimitado.** Evans (*Blue Book*, cap. 14) define o
[Contexto Delimitado](../ddd-dicionario.md#contexto-delimitado-bounded-context) como a fronteira
de aplicabilidade de um modelo. Vernon (*DDD Distilled*, cap. 2) acrescenta: ele é também uma
fronteira de **time** e de **linguagem** — idealmente um time por contexto.

**Mapa de contexto.** O [Mapa de Contexto](../ddd-dicionario.md#mapa-de-contexto-context-map)
descreve a realidade *como ela é* (ou como se quer que seja), não um desenho ideal.
Os [padrões de integração](../ddd-dicionario.md#2-padrões-de-integração-entre-contextos-context-map-patterns):

| Padrão | Quando usar | Custo / risco |
|--------|-------------|---------------|
| **Customer–Supplier** | O downstream tem voz: o upstream planeja entregas pensando nele. | Exige negociação contínua entre times. |
| **Conformist** | O downstream adota o modelo do upstream como está, sem traduzir. | Acoplamento; aceitável se o modelo do upstream é bom. |
| **Anticorruption Layer (ACL)** | O modelo externo é ruim, legado ou alheio; o downstream traduz na borda. | Código de tradução para manter; protege o modelo local. |
| **Open Host Service (OHS)** | O upstream serve vários consumidores com um protocolo público estável. | Versionar e manter o contrato. |
| **Published Language (PL)** | Formato de troca documentado (esquema JavaScript Object Notation — JSON, por exemplo). Anda junto com OHS. | Evoluir sem quebrar consumidores. |
| **Shared Kernel (SK)** | Dois contextos compartilham um pedaço pequeno do modelo. | Toda mudança exige acordo; mantenha mínimo. |
| **Separate Ways** | Integrar custa mais do que duplicar. | Duplicação consciente. |

Relações *upstream/downstream* descrevem **fluxo de influência**, não fluxo de dados: o
downstream pode até enviar comandos ao upstream e continuar downstream, porque é ele quem se adapta.

## 6. Na prática — o DomainStudio aplicado a si mesmo

**Fronteiras.** A [seção 4 do modelo](../modelo-domain-studio.md#4-contextos-delimitados) mantém
1:1 com os subdomínios: Especificação, Decomposição, Modelagem, Visualização, Geração de Código e
Conhecimento DDD; o provedor de Large Language Model (LLM) é um sistema externo.

**A heurística funcionando no próprio projeto:**

| Palavra | Sentido 1 | Sentido 2 | Consequência |
|---------|-----------|-----------|--------------|
| "Especificação" | Texto versionado do usuário (contexto Especificação) | Padrão *Specification* do DDD, que implementa uma Regra de Conformidade (Conhecimento/Modelagem) | Em código, o padrão aparece como `RegraDeConformidade`, nunca como `Especificacao`. |
| "Modelo" | Modelo de domínio (Modelagem) | Modelo de linguagem (provedor LLM) | Dúvida D2 em [fluxo.yaml](../modelo/fluxo.yaml): usar sempre "LLM" para o segundo. |
| "Sugestão" × "Elemento de Modelo" | Proposta ainda não revisada (Decomposição) | Item aceito no modelo (Modelagem) | A fronteira fica exatamente onde a revisão humana acontece. |

**O mapa em CML.** Arquivo: [domain_studio.cml](../modelo/domain_studio.cml). Trecho:

```
ContextMap DomainStudioMap {
	type = SYSTEM_LANDSCAPE
	state = TO_BE
	contains Especificacao, Decomposicao, Modelagem, Visualizacao, GeracaoDeCodigo, ConhecimentoDDD, ProvedorLLM

	Especificacao [S]->[C] Decomposicao
	Modelagem [U,OHS,PL]->[D,CF] Visualizacao
	ConhecimentoDDD [SK]<->[SK] Modelagem
	ProvedorLLM [U]->[D,ACL] Decomposicao
}
```

Como ler cada linha:

| Sintaxe | Significado |
|---------|-------------|
| `A [S]->[C] B` | A é *Supplier*, B é *Customer* (Customer–Supplier). |
| `A [U,OHS,PL]->[D,CF] B` | A é upstream com Open Host Service e Published Language; B é downstream Conformist. |
| `A [SK]<->[SK] B` | Relação simétrica: Shared Kernel (seta dupla, sem upstream). |
| `A [U]->[D,ACL] B` | B é downstream e se protege de A com uma ACL. |
| `BoundedContext X implements XSD` | O contexto X realiza o subdomínio `XSD`, declarado em `Domain { Subdomain … }` com `type = CORE_DOMAIN` ou `SUPPORTING_DOMAIN`. |

Para **escrever** uma relação nova: declare o contexto em `contains`, crie o bloco
`BoundedContext` com `domainVisionStatement`, e acrescente uma linha de relação com os papéis de
cada lado entre colchetes.

**Trade-offs e pontos em aberto:**

- `Modelagem [U,OHS]->[D] Decomposicao`: a Decomposição *envia* sugestões aceitas para a Modelagem,
  mas é downstream, porque usa os comandos públicos que a Modelagem define. Contraintuitivo, porém
  coerente com "fluxo de influência".
- O **Shared Kernel** com Conhecimento DDD é só de enumerações (`TipoElemento`, `TipoSubdominio`,
  `PadraoDeIntegracao`). Se crescer, vira dor de coordenação.
- A dúvida D3 pergunta se o contexto Especificação deveria se chamar "Captura", para não colidir
  com o agregado de mesmo nome. Ainda `proposto`.
- O marco M3 do [plano](../plano-de-implementacao.md) exige que o CML gerado pelo próprio sistema
  seja equivalente a este arquivo — hoje ele é escrito à mão.

## 7. Erros comuns

- **Um contexto por entidade.** "Contexto Cliente", "Contexto Pedido" — são agregados, não fronteiras linguísticas.
- **Fronteira por camada técnica.** "Contexto Backend" e "Contexto Frontend" não têm linguagem própria.
- **Shared Kernel como atalho.** Compartilhar muito para evitar tradução recria o modelo único.
- **Conformist sem perceber.** Importar classes do outro contexto é Conformist implícito — e sem decisão registrada.
- **Setas no sentido dos dados.** A seta indica influência (quem se adapta a quem), não para onde vai o *payload*.
- **Esquecer a ACL diante de serviços externos.** O formato do provedor passa a ditar o seu Núcleo.
- **Mapa desenhado e nunca atualizado.** Se o mapa é texto (CML) versionado junto ao código, ele envelhece menos.

## 8. Verificação

- [ ] Cada contexto tem declaração de visão de uma frase.
- [ ] Nenhum termo tem dois significados dentro do mesmo contexto.
- [ ] Toda palavra repetida entre contextos tem o significado de cada lado documentado.
- [ ] Toda relação tem direção (U/D ou simétrica) e um padrão nomeado.
- [ ] Todo sistema externo que alimenta um contexto Núcleo passa por ACL.
- [ ] O mapa existe em CML, versionado, e o diagrama é gerado dele.

Perguntas de autoavaliação:

1. Por que Visualização pode ser Conformist em relação à Modelagem, mas a Decomposição não pode ser Conformist ao provedor LLM?
2. Qual a diferença entre Open Host Service e Published Language? Por que costumam andar juntos?
3. Dê um exemplo, no seu domínio, de uma palavra que muda de significado entre duas áreas.

## 9. Para saber mais

- Anterior: [Aula 02 — Subdomínios e destilação](02-subdominios-e-destilacao.md)
- Próxima: [Aula 04 — Agregados e invariantes](04-agregados-e-invariantes.md)
- [Dicionário de DDD](../ddd-dicionario.md) — seções 1 e 2.
- [Modelo do DomainStudio](../modelo-domain-studio.md) — seções 4 e 5; [mapa em CML](../modelo/domain_studio.cml).
- Eric Evans, *Domain-Driven Design* (2003), cap. 14 "Maintaining Model Integrity".
- Vaughn Vernon, *Domain-Driven Design Distilled* (2016), cap. 2 e 4.
- Documentação do Context Mapper: contextmapper.org (seção "Context Map").
