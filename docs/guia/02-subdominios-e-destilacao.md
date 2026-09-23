---
id: aula-02-subdominios-e-destilacao
tipo: aula
titulo: "Aula 02 — Subdomínios e destilação"
etapa: 2
resumo: "Como partir o domínio em subdomínios, classificá-los em Núcleo, Suporte e Genérico e decidir onde investir o esforço de modelagem."
relacionados: [aula-01-linguagem-ubiqua-e-fluxo, aula-03-contextos-delimitados-e-mapa, dicionario-ddd, modelo-domain-studio]
termos: [projeto, especificacao, decomposicao, sugestao, modelo-estrategico, regra-de-conformidade, diagrama, artefato-de-codigo]
---

# Aula 02 — Subdomínios e destilação

> Nem toda parte do sistema merece o mesmo cuidado. Domain-Driven Design (DDD) começa a
> economizar esforço quando você separa o domínio em **subdomínios** e pergunta, para cada um:
> "é isto que nos diferencia?". Só o **Núcleo** recebe modelagem rica; o resto é resolvido
> da forma mais simples que funcione — inclusive comprando pronto.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** o que é um subdomínio e por que ele pertence ao espaço do *problema*, não da solução.
2. **Identificar** subdomínios a partir do fluxo e da linguagem ubíqua validados na aula anterior.
3. **Classificar** cada subdomínio como Núcleo (Core), Suporte (Supporting) ou Genérico (Generic), com justificativa.
4. **Aplicar** a destilação: escrever a declaração do Núcleo e decidir onde investir (modelar, simplificar ou comprar).

## 2. O problema

Sem esta etapa, o time trata o sistema inteiro com a mesma intensidade. Os sintomas são conhecidos:

- **Esforço mal distribuído.** Semanas modelando cadastro de usuários com agregados e eventos, enquanto a regra que realmente dá dinheiro fica num `if` escondido num controller.
- **Reinvenção do genérico.** Autenticação, envio de e-mail, faturamento — problemas resolvidos por qualquer fornecedor — viram código próprio para manter.
- **Núcleo diluído.** O conceito que diferencia o produto se espalha por vários módulos e ninguém consegue apontar "é aqui que está o nosso valor".
- **Prioridade sem critério.** Sem saber o que é Núcleo, o backlog é ordenado por quem pede mais alto.

## 3. A ideia central

> **Classifique antes de modelar: invista profundidade onde está a vantagem competitiva, e simplicidade em todo o resto.**

Um subdomínio é uma *área de conhecimento* do negócio. Ele existe antes do software e continuaria
existindo se o sistema fosse escrito em papel. A classificação diz **quanto** cada área merece:
o Núcleo recebe os melhores modeladores e o DDD completo; o Suporte recebe um modelo simples;
o Genérico recebe uma solução pronta. Destilar é o movimento de tornar esse Núcleo pequeno,
nítido e explícito.

## 4. Passo a passo

1. **Parta do fluxo validado.** Use os passos do fluxo e os termos da linguagem ubíqua da
   [Aula 01](01-linguagem-ubiqua-e-fluxo.md). Não parta de telas nem de tabelas.
2. **Agrupe por capacidade de negócio.** Junte passos e termos que respondem à mesma pergunta
   do negócio ("capturar o texto", "transformar texto em modelo", "desenhar o modelo"…).
   Dê a cada grupo um nome em linguagem ubíqua.
3. **Teste cada grupo com três perguntas:**
   - *Se fizermos isto melhor que os concorrentes, ganhamos clientes?* → candidato a **Núcleo**.
   - *É necessário e específico nosso, mas ninguém escolhe o produto por causa disto?* → **Suporte**.
   - *Qualquer empresa tem este problema e existe solução pronta?* → **Genérico**.
4. **Escreva uma justificativa de uma linha** por subdomínio. Se não consegue justificar, a
   classificação ainda é palpite — marque como `proposto`.
5. **Limite o Núcleo.** Se mais da metade dos subdomínios virou Núcleo, você não classificou,
   só listou. Normalmente são um ou dois.
6. **Escreva a declaração de visão do domínio** (*Domain Vision Statement*): um parágrafo curto
   dizendo o que o Núcleo faz e por que ele vale. É a primeira peça da destilação.
7. **Decida a estratégia de investimento** para cada subdomínio (tabela da seção 5).
8. **Registre no Modelo Estratégico** e leve os subdomínios para a
   [Aula 03](03-contextos-delimitados-e-mapa.md), onde eles recebem contextos delimitados.

## 5. Fundamentos

**Espaço do problema × espaço da solução.** Evans separa o que o negócio *é* do que o software
*faz*. [Subdomínios](../ddd-dicionario.md#subdomínio-subdomain) vivem no espaço do problema;
[Contextos Delimitados](../ddd-dicionario.md#contexto-delimitado-bounded-context) vivem no
espaço da solução. Vernon (*DDD Distilled*, cap. 2 e 3) insiste que o alinhamento ideal é 1:1,
mas que isso é uma meta, não uma regra.

**Os três tipos.**

| Tipo | Pergunta que o define | Estratégia de investimento | Quem trabalha nele |
|------|-----------------------|----------------------------|--------------------|
| **Núcleo** | Diferencia o produto? | DDD completo: agregados, invariantes, eventos, testes de domínio. Desenvolver em casa. | Os melhores desenvolvedores + especialista de domínio. |
| **Suporte** | Necessário e específico, mas não diferenciador? | Modelo simples; às vezes um Create, Read, Update, Delete (CRUD) bem feito basta. Pode ser terceirizado. | Time com menos senioridade, sem culpa. |
| **Genérico** | Problema comum a qualquer organização? | Comprar, usar biblioteca ou serviço externo; isolar atrás de uma porta. | Quase ninguém — integração, não modelagem. |

**Destilação.** Na parte IV do *Blue Book*, Evans descreve a
[Destilação](../ddd-dicionario.md#destilação-distillation) como separar o essencial do acessório
para que o [Modelo de Núcleo](../ddd-dicionario.md#modelo-de-núcleo-core-domain--distilled-core)
fique visível. Ferramentas que ele propõe:

- **Declaração de visão do domínio** — um parágrafo que qualquer pessoa do time consegue repetir.
- **Núcleo destacado** (*Highlighted Core*) — marcar, no documento de modelo, quais elementos são o Núcleo.
- **Subdomínios genéricos segregados** — tirar do caminho o que é genérico, para que não contamine o Núcleo.
- **Mecanismos coesos** — extrair algoritmos complexos mas não diferenciadores para módulos próprios.

**A classificação muda.** O que hoje é Núcleo pode virar commodity amanhã (e vice-versa). Por isso
ela é revisada sempre que a especificação ganha uma nova versão.

## 6. Na prática — o DomainStudio aplicado a si mesmo

O [modelo do DomainStudio](../modelo-domain-studio.md#3-subdomínios) propõe oito subdomínios:

| Subdomínio | Tipo | Por quê (resumo) |
|------------|------|------------------|
| Decomposição de Domínio | Núcleo | Transformar texto em modelo DDD coerente é o diferencial. |
| Modelagem de Domínio | Núcleo | O modelo validado contra regras do DDD é o ativo central. |
| Especificação | Suporte | Captura e versionamento de texto. |
| Visualização | Suporte | Tradução determinística do modelo para notações existentes. |
| Geração de Código | Suporte | Derivada do modelo, baseada em templates. |
| Conhecimento DDD | Suporte | Catálogo de conceitos e regras de conformidade. |
| Identidade e Acesso | Genérico | Autenticação — solução pronta; fora do escopo inicial (usuário único). |
| Modelo de Linguagem | Genérico | Serviço externo de Large Language Model (LLM), isolado por uma camada anticorrupção. |

Como isso vira investimento, segundo o [plano de implementação](../plano-de-implementacao.md):

- **Modelagem** recebe primeiro o tratamento completo (marco M2): agregados `ModeloEstrategico` e
  `ModeloTatico` com invariantes e um `ValidadorDeConformidade`.
- **Decomposição** vem depois (M4), de propósito: ela precisa de um modelo onde "cair".
- **Visualização** e **Geração de Código** são tratadas como tradução por templates — modelo simples.
- **Modelo de Linguagem** nunca é modelado: fica atrás da porta `Decompositor`.

**Declaração de visão (proposta):** *"O DomainStudio transforma a especificação textual de um
domínio em um modelo DDD revisado por um humano e validado contra regras explícitas; diagramas e
código são consequências desse modelo."*

**Trade-offs honestos.**

- Ter **dois** Núcleos é uma escolha discutível. Um argumento é que Decomposição sem Modelagem
  não tem valor, e Modelagem sem Decomposição é "só mais um editor". Outro é que só a Decomposição
  diferencia de verdade. A proposta atual prefere dois Núcleos pequenos a um grande.
- **Conhecimento DDD** poderia ser Genérico (é um catálogo estático), mas as regras de conformidade
  são específicas deste produto; por isso ficou em Suporte.
- Tudo aqui é `proposto`: nenhum termo de [linguagem-ubiqua.yaml](../modelo/linguagem-ubiqua.yaml)
  está `validado` ainda, e a classificação herda essa incerteza.

## 7. Erros comuns

- **Classificar pela dificuldade técnica.** "É difícil, logo é Núcleo." Dificuldade não é diferencial; um algoritmo complexo e genérico é um *mecanismo coeso*, não o Núcleo.
- **Tudo é Núcleo.** Sinal de que ninguém teve coragem de dizer o que é secundário. O Núcleo perde foco.
- **Confundir subdomínio com módulo de código.** Subdomínio é problema; módulo e contexto são solução.
- **Modelar o Genérico "porque é DDD".** Agregados para login são desperdício; use uma biblioteca e uma porta.
- **Classificar uma vez e esquecer.** O mercado muda; revise a cada nova versão da especificação.
- **Deixar o LLM decidir sozinho.** A decomposição pode sugerir a classificação, mas quem valida é o especialista de domínio.

## 8. Verificação

Rode no seu próprio modelo:

- [ ] Cada subdomínio tem nome em linguagem ubíqua e uma justificativa de uma linha.
- [ ] Há no máximo um ou dois subdomínios Núcleo.
- [ ] Cada subdomínio Genérico tem uma solução pronta candidata (biblioteca, serviço, produto).
- [ ] Existe uma declaração de visão do domínio de um parágrafo.
- [ ] Todo passo do fluxo validado cai em algum subdomínio.
- [ ] Nenhum subdomínio foi nomeado por tecnologia ("Banco", "Front", "Application Programming Interface (API)").

Perguntas de autoavaliação:

1. Por que o subdomínio "Modelo de Linguagem" é Genérico se o produto depende tanto dele?
2. Que evidência faria você rebaixar Modelagem de Núcleo para Suporte?
3. Qual a diferença entre um subdomínio Genérico e um mecanismo coeso?

## 9. Para saber mais

- Anterior: [Aula 01 — Linguagem ubíqua e fluxo](01-linguagem-ubiqua-e-fluxo.md)
- Próxima: [Aula 03 — Contextos delimitados e mapa](03-contextos-delimitados-e-mapa.md)
- [Dicionário de DDD](../ddd-dicionario.md) — seções 1 e 5.
- [Modelo do DomainStudio](../modelo-domain-studio.md) — seção 3.
- [Plano de implementação](../plano-de-implementacao.md) — ordem dos marcos.
- Eric Evans, *Domain-Driven Design* (2003), parte IV, cap. 15 "Distillation".
- Vaughn Vernon, *Domain-Driven Design Distilled* (2016), cap. 3 "Strategic Design with Subdomains".
