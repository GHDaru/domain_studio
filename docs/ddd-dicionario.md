# Dicionário de Definições — Domain-Driven Design (DDD)

> Fonte principal: Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003 — "Blue Book").
> Complementos: Vaughn Vernon, *DDD Distilled* (2016); Vernon, *Implementing DDD* (2013).

---

## 1. Estratégia — Linguagem e Contexto

### Linguagem Ubíqua (Ubiquitous Language)
Linguagem compartilhada entre desenvolvedores e especialistas de domínio, usada de forma consistente em conversas, diagramas, documentos e **código**. Cada termo do vocabulário corresponde a uma construção de software. É o pilar que mantém o modelo alinhado ao negócio. Vive dentro de um único **Contexto Delimitado**.

### Domínio (Domain)
O universo de atividade ou conhecimento sobre o qual o software opera — o "coração" do problema. O modelo de domínio é uma abstração seletiva desse universo.

### Subdomínio (Subdomain)
Partição funcional dentro do domínio. Classifica-se em três tipos:

| Tipo | Descrição | Estratégia típica |
|------|-----------|-------------------|
| **Núcleo (Core)** | O que diferencia o negócio — a maior fonte de valor. | DDD completo, modelagem rica. |
| **Suporte (Supporting)** | Necessário, mas não diferenciador. Pode ser customizado. | DDD leve ou modelagem simplificada. |
| **Genérico (Generic)** | Comum a qualquer organização (ex.: autenticação, faturamento). | Comprar/usar solução pronta; não merece DDD. |

### Contexto Delimitado (Bounded Context)
Fronteira explícita dentro da qual um modelo de domínio e uma **linguagem ubíqua** são válidos e consistentes. Fora da fronteira, os mesmos termos podem ter significados diferentes. Cada Contexto Delimitado corresponde idealmente a um único time, um modelo coeso e, frequentemente, um microsserviço ou módulo deployável.

> **Exemplo clássico:** "Produto" significa algo diferente em Vendas (catálogo, preço), em Logística (peso, dimensões) e em Fiscal (NCM, alíquota). Três Contextos Delimitados, três modelos.

### Mapa de Contexto (Context Map)
Diagrama ou descrição que mostra as relações entre múltiplos **Contextos Delimitados** e os padrões de integração entre eles. É a visão arquitetural de alto nível do sistema.

---

## 2. Padrões de Integração entre Contextos (Context Map Patterns)

| Padrão | Descrição |
|--------|-----------|
| **Shared Kernel (Kernel Compartilhado)** | Dois contextos compartilham um pequeno modelo comum (código + modelo). Mudanças exigem coordenação entre times. Use com moderação. |
| **Customer–Supplier** | Contexto *Supplier* produz dados/modelo que o *Customer* consome. Supplier tem poder de decisão; Customer negocia necessidades. |
| **Conformist** | Customer depende do modelo do Supplier sem influência sobre ele — apenas se conforma. Risco de acoplamento rígido. |
| **Anticorruption Layer (ACL)** | Camada tradutora que isola um contexto de modelos externos legados/incompatíveis, convertendo entradas/saídas para o modelo local. Protege a integridade do modelo. |
| **Open Host Service** | Um contexto expõe um protocolo/abertura padronizada (ex.: API REST, gRPC) para múltiplos consumidores. |
| **Published Language** | Linguagem de intercâmbio bem documentada e padronizada (ex.: schema JSON, XSD, EDI) usada na integração entre contextos. Frequentemente combinada com Open Host Service. |
| **Separate Ways** | Contextos não integrados — declara explicitamente que não há relacionamento. |
| **Big Ball of Mud** | Contexto sem estrutura clara, com acoplamento caótico. Modelado como *Conformist* ou isolado por *ACL* ao se integrar. |

---

## 3. Blocos de Construção do Modelo (Building Blocks)

### Entidade (Entity)
Objeto definido primariamente por sua **identidade** (continuidade ao longo do tempo), não por seus atributos. Dois clientes com os mesmos dados, mas IDs diferentes, são entidades distintas. Pode mudar de estado; é mutável. Ex.: `Cliente`, `Pedido`, `ContaCorrente`.

### Objeto de Valor (Value Object)
Objeto definido inteiramente por seus **atributos** — sem identidade própria. Imutável por convenção. Dois objetos de valor com os mesmos atributos são considerados iguais. Substituíveis, descartáveis. Ex.: `Endereco`, `Dinheiro`, `Periodo`, `Coordenada`.

> **Heurística:** se você se importa *qual* é o objeto → Entidade. Se você se importa apenas *o que* ele contém → Objeto de Valor.

### Agregado (Aggregate)
Cluster de **Entidades** e **Objetos de Valor** tratados como uma unidade transacional e de consistência. Possui uma **Raiz de Agregado** que é a única entidade acessível externamente. Referências externas apontam sempre para a raiz, nunca para objetos internos. Garante invariantes do negócio em toda operação.

### Raiz de Agregado (Aggregate Root)
Entidade de entrada do Agregado. Centraliza a aplicação das regras de invariantes. Objetos internos só podem ser modificados através dela. Ex.: `Pedido` é raiz; `ItemPedido` só é manipulado via `Pedido.adicionarItem(...)`.

> **Regra de ouro:** referências entre agregados devem ser por **ID**, não por referência de objeto direta. Mantém agregados pequenos e consistentes.

### Repositório (Repository)
Mecanismo que abstrai a persistência e recuperação de **Agregados**, oferecendo a ilusão de uma coleção em memória. Acesso apenas a raízes de agregado. Interface pertence ao domínio; implementação à infraestrutura. Ex.: `PedidoRepository.buscarPorId(id)`, `salvar(pedido)`.

### Fábrica (Factory)
Encapsula a criação de objetos complexos (Agregados/Entidades) quando o construtor simples não basta — quando há invariantes a validar ou múltiplos objetos a coordenar. Restaura a intenção de domínio. Pode ser um método estático, um serviço de domínio ou um builder.

### Serviço de Domínio (Domain Service)
Operação de domínio que não pertence naturalmente a nenhuma Entidade ou Objeto de Valor — representa um conceito do negócio como uma *ação* ou *processo* stateless. Ex.: `CalculadorDeFrete`, `TransferenciaEntreContas`. Nome em linguagem ubíqua, interface no domínio.

### Serviço de Aplicação (Application Service)
Camada fina que **orquestra** casos de uso: traduz DTOs/entradas externas em chamadas de domínio, coordena transações e segurança, mas **não contém regras de negócio**. É o ponto de entrada da aplicação (ex.: controller, handler de caso de uso). Mantém o domínio puro e desacoplado de tecnologia.

### Evento de Domínio (Domain Event)
Representa algo significativo que ocorreu no domínio (passado: `PedidoCriado`, `PagamentoConfirmado`). Permite comunicação **desacoplada** entre agregados e contextos. Publicado pelo agregado; consumido por handlers interessados. Base para *event sourcing* e integração assíncrona.

### Módulo (Module / Package)
Agrupamento nomeado de elementos do modelo que formam um conceito coeso — a "namespace" do domínio. Reduz complexidade cognitiva. Deve contar uma *história* (ex.: `pedidos`, `faturamento`, `catalogo`) e seguir a linguagem ubíqua.

### Política (Policy)
Encapsulamento de uma regra ou algoritmo de negócio como um objeto de valor ou serviço, permitindo variar comportamento por composição. Ex.: `PoliticaDeDesconto`, `PoliticaDeAprovacao`.

### Especificação (Specification)
Padrão que expressa uma regra de negócio como um objeto predicado (`isSatisfiedBy(candidate)`), permitindo combinar, reutilizar e validar regras declarativamente. Útil para validação, seleção e queries. Ex.: `ClientePremiumSpec`, `PedidoElegivelParaFreteGratisSpec`.

---

## 4. Arquitetura

### Arquitetura em Camadas (Layered Architecture)
Separação de responsabilidades em camadas verticais, com dependências apontando para baixo:

```
┌─────────────────────────┐
│   Interface / UI        │  ← Apresentação
├─────────────────────────┤
│   Application Service   │  ← Orquestração, casos de uso
├─────────────────────────┤
│   Domain Model          │  ← Entidades, Agregados, Regras (núcleo)
├─────────────────────────┤
│   Infrastructure        │  ← Persistência, mensageria, APIs externas
└─────────────────────────┘
```

O **modelo de domínio** é isolado e independente de tecnologia. Toda lógica de negócio vive ali.

### Arquitetura Hexagonal (Ports and Adapters)
O domínio no centro, cercado por **portas** (interfaces) e **adaptadores** (implementações de UI, DB, mensageria). Permite trocar a infraestrutura sem tocar o domínio. Alinhada com DDD.

### Arquitetura Cebola (Onion Architecture)
Similar à hexagonal, com camadas concêntricas: domínio no centro, serviços ao redor, infraestrutura na borda. Dependências sempre apontam para dentro.

### Clean Architecture
Generalização das anteriores: a regra de dependência é que dependências apontam sempre para as políticas/regras de domínio (centro), nunca para detalhes (borda).

---

## 5. Conceitos de Modelagem Estratégica

### Refatoração de Modelo (Model Refactoring)
Processo contínuo de aprofundar e corrigir o modelo à medida que a compreensão do domínio evolui. O modelo nunca está "pronto" — é uma destilação viva.

### Design Maleável (Supple Design)
Design que permite expressar o modelo de forma fluida e declarativa no código, com combinações poderosas de pequenos conceitos. Objetos de valor, especificações e políticas são ferramentas para alcançá-lo. O objetivo é que o código "leia" como a linguagem ubíqua.

### Destilação (Distillation)
Processo de reduzir o modelo ao essencial, removendo ruído para revelar o núcleo de valor. Pode resultar em um **Modelo de Núcleo (Core Domain)** documentado separadamente.

### Modelo de Núcleo (Core Domain / Distilled Core)
Versão reduzida e destacada do modelo que contém apenas os conceitos essenciais do subdomínio núcleo — frequentemente documentado com um diagrama simplificado para guiar o time.

---

## 6. Eventos e Comunicação

### Publicador de Eventos (Event Publisher / Dispatcher)
Mecanismo pelo qual o domínio publica **Eventos de Domínio** sem conhecer seus consumidores. Implementação pode ser síncrona (in-process) ou assíncrona (message broker).

### Event Sourcing
Padrão em que o estado de um agregado é reconstruído a partir da **sequência de eventos** que o afetaram, em vez de persistir apenas o estado atual. O estado é uma projeção dos eventos. Permite auditoria total e reconstrução temporal.

### CQRS (Command Query Responsibility Segregation)
Separação do modelo de escrita (Commands) do modelo de leitura (Queries). Frequentemente combinado com Event Sourcing. O modelo de leitura pode ser otimizado independentemente (projeções, read models).

---

## 7. Diagramas e Notação (para a ferramenta)

| Notação | Uso no projeto |
|---------|----------------|
| **C4 Model** (Context, Container, Component, Code) | Visualização em níveis de arquitetura — do sistema no mundo até classes. |
| **PlantUML** | Diagramas UML textuais (classes, sequência, contexto). Geração declarativa. |
| **Context Mapper DSL** | Linguagem DSL para modelar **Context Maps** e Bounded Contexts com padrões de integração — gera PlantUML/Mermaid. |
| **Mermaid** | Diagrams-as-code, suportado nativamente em Markdown/GitHub. |

---

## Mapa de Relações (resumo)

```
Domínio
 └── Subdomínio (Core / Supporting / Generic)
      └── Contexto Delimitado
           ├── Linguagem Ubíqua
           ├── Modelo de Domínio
           │    ├── Entidade (Raiz de Agregado)
           │    ├── Objeto de Valor
           │    ├── Agregado
           │    ├── Serviço de Domínio
           │    ├── Evento de Domínio
           │    ├── Repositório (interface)
           │    ├── Fábrica
           │    ├── Política
           │    ├── Especificação
           │    └── Módulo
           └── [integra com outros Contextos via padrões do Mapa de Contexto]
```

---

*Este dicionário é a base de referência para o DomainStudio — a aplicação que decomporá especificações em modelos DDD, visualizações C4/PlantUML e, por fim, código.*
