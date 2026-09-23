---
id: aula-01-linguagem-ubiqua-e-fluxo
tipo: aula
titulo: "Aula 01 — Linguagem ubíqua e fluxo"
etapa: 1
resumo: "Primeira etapa do método: descrever o que acontece no negócio e validar, com o especialista, o fluxo e o vocabulário antes de modelar."
relacionados: [aula-00-como-usar, aula-02-subdominios-e-destilacao, dicionario-ddd, modelo-domain-studio, linguagem-ubiqua]
termos: [especificacao, versao-especificacao, projeto]
---
# Aula 01 — Linguagem ubíqua e fluxo

> Antes de desenhar qualquer caixa, confirme duas coisas com quem conhece o negócio:
> **o que acontece** (o fluxo) e **como as coisas se chamam** (o vocabulário). Todo o
> resto do modelo é construído com essas palavras — se elas estiverem erradas, o modelo
> inteiro estará certo sobre a coisa errada.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** por que o vocabulário vem antes das classes em Domain-Driven Design (DDD);
2. **Escrever** uma especificação de domínio em texto livre que sirva de entrada ao método;
3. **Extrair** dela um fluxo (passos, atores, eventos) e um vocabulário (termos, definições,
   sinônimos a evitar);
4. **Conduzir** a validação de ambos com o especialista de domínio;
5. **Registrar** o resultado como artefato que humanos e agentes de IA consomem.

## 2. O problema

Um time — ou um agente de IA — recebe "o sistema gerencia pedidos" e começa a modelar.
Semanas depois descobre que, para o negócio, "pedido" é a intenção do cliente, e o que o
time modelou como pedido é, na verdade, a "ordem de separação" do estoque. As classes estão
corretas, os testes passam, e o software resolve o problema errado.

O defeito não estava no código: estava numa palavra que ninguém confirmou. Com agentes de
IA o risco cresce, porque o agente preenche lacunas com o significado **mais comum** da
palavra, não com o significado **deste** negócio — e faz isso com total confiança.

## 3. A ideia central

> **O modelo é feito de palavras. Valide as palavras primeiro.**

Evans chama isso de **Linguagem Ubíqua**: um vocabulário único, usado igual na conversa,
nos documentos e no código. "Ubíqua" porque aparece em todo lugar; se um termo muda na
conversa, muda no código também.

## 4. Passo a passo

1. **Escreva a especificação em texto livre.** Conte o que acontece no negócio, na voz de
   quem o conhece. Não use jargão técnico (tabela, endpoint, tela). Marque em **negrito**
   os substantivos e verbos que parecem importantes.
2. **Extraia o fluxo.** Transforme o texto numa sequência de passos. Para cada passo:
   - **ator** — quem faz (pessoa, papel ou sistema);
   - **ação** — o que faz, numa frase;
   - **evento** — o fato que fica registrado quando o passo termina, no passado
     (`ProjetoCriado`, `VersaoEspecificacaoPublicada`). Evento no passado força precisão:
     "o que *aconteceu*?" é mais fácil de validar do que "o que o sistema *faz*?".
3. **Extraia o vocabulário.** Para cada termo em negrito:
   - **definição** em uma frase, sem usar o próprio termo;
   - **nome em código** — como vai aparecer em classes e rotas;
   - **sinônimos a evitar** — as outras palavras que as pessoas usam para a mesma coisa;
   - **contexto** — onde o termo vale (na primeira rodada, pode ficar provisório).
4. **Ligue os dois.** Cada passo do fluxo cita os termos que usa. Termo que nenhum passo
   usa é suspeito (é necessário?). Passo que usa palavra fora do vocabulário revela lacuna.
5. **Escreva as dúvidas.** Tudo o que você supôs vira pergunta explícita. Uma suposição não
   escrita é decidida pelo agente, em silêncio.
6. **Valide com o especialista.** Para cada passo: *confere*, *ajustar* ou *não é assim*.
   Para cada termo: *confirmar*, *renomear/redefinir* ou *rejeitar*. Responder às dúvidas.
7. **Registre as decisões num arquivo versionado.** A validação só existe se sobreviver à
   conversa: ela vai para o repositório, não para a memória de ninguém.
8. **Só avance quando** todo passo e todo termo tiver decisão, e toda dúvida, resposta.

## 5. Fundamentos

**Linguagem ubíqua** ([dicionário](../ddd-dicionario.md#linguagem-ubíqua-ubiquitous-language)).
Evans (2003) a coloca como pilar do DDD: especialistas e desenvolvedores usam a mesma
linguagem, e ela aparece no código. Quando o código diz `Pedido` e o negócio diz
"solicitação", cada conversa exige tradução — e toda tradução perde algo.

**A linguagem vive dentro de um contexto.** O mesmo termo pode significar coisas diferentes
em partes diferentes do negócio. Na etapa 1 isso aparece como **ambiguidade**; na
[etapa 3](03-contextos-delimitados-e-mapa.md) ela vira fronteira entre contextos delimitados.
Por isso, uma ambiguidade encontrada aqui não é defeito: é informação.

**Por que eventos no passado.** A técnica de Event Storming (Brandolini) começa exatamente
por eventos de domínio: fatos que o negócio reconhece como tendo acontecido. Especialistas
lembram de fatos com mais precisão do que de funcionalidades.

**Por que validar antes de modelar.** O custo de corrigir um termo cresce a cada etapa: na
etapa 1 é editar uma linha; na etapa 6 é renomear classes, rotas, eventos e migrações. Com
agentes de IA, que geram muito rápido, o erro também se propaga muito rápido.

**Hipótese não é conhecimento.** Todo termo começa com status `proposto`. Só o especialista
de domínio pode mudá-lo para `validado`. Um modelo construído sobre termos `proposto` pode
estar certo — mas ninguém sabe ainda.

## 6. Na prática — o DomainStudio aplicado a si mesmo

A especificação do DomainStudio está na seção 1 do [modelo](../modelo-domain-studio.md). Dela
saíram dois arquivos, que são a **fonte única** do fluxo e do vocabulário:

- [`modelo/fluxo.yaml`](../modelo/fluxo.yaml) — 8 passos (P1 Criar projeto … P8 Gerar código
  e artefatos para IA) e 4 dúvidas em aberto;
- [`modelo/linguagem-ubiqua.yaml`](../modelo/linguagem-ubiqua.yaml) — 14 termos em 6 contextos.

Trecho real do vocabulário:

```yaml
- id: versao-especificacao
  termo: Versão da Especificação
  codigo: VersaoEspecificacao
  contexto: especificacao
  tipo: objeto-de-valor
  definicao: Retrato imutável do texto num momento. Toda decomposição aponta para exatamente uma versão.
  evitar: [revisão, rascunho]
  status: proposto
```

O passo 4 do procedimento (ligar fluxo e vocabulário) já revelou ambiguidades, registradas
como dúvidas:

| Dúvida | Por que importa |
|---|---|
| D2 — "Modelo" = modelo de domínio **ou** modelo de linguagem? | Mesmo termo, dois significados: se não for resolvido, a IA vai confundir `Modelo` com LLM no código. |
| D3 — "Especificação" nomeia um contexto **e** um agregado | Pode ser aceitável, ou sinal de que o contexto tem outro nome ("Captura"). |
| D1 — Revisão sugestão por sugestão ou do modelo inteiro? | Muda o agregado `Decomposicao` inteiro. |

**A interface de validação.** O protótipo
[`prototipos/validacao-linguagem.html`](../../prototipos/validacao-linguagem.html) executa os
passos 6 e 7: mostra o fluxo como linha do tempo, o vocabulário por contexto, a especificação
com os termos marcados, e as dúvidas ao lado. Cada decisão vira YAML, que é colado em
`docs/modelo/decisoes-validacao.yaml`. O script `scripts/gerar_docs.py` aplica as decisões e
regenera o vocabulário legível e o grafo.

**Estado honesto:** até esta aula ser escrita, nenhum termo foi validado. Tudo é `proposto`.

## 7. Erros comuns

- **Pular para as classes.** "Já sei o que é um Pedido." Você sabe o que *você* acha que é.
- **Vocabulário técnico.** "Usuário cadastra registro na tabela de projetos." O negócio não
  tem tabelas; se a linguagem é técnica, o especialista não consegue validá-la.
- **Definição circular.** "Projeto: um projeto do usuário." A definição tem que dizer algo
  que o nome não diz.
- **Sinônimos tolerados.** Deixar "workspace" e "projeto" conviverem. Em seis meses serão
  duas classes diferentes para a mesma coisa.
- **Validação na conversa.** O especialista confirmou numa reunião, ninguém registrou, e o
  agente de IA da semana seguinte não estava na reunião.
- **Suposição silenciosa.** Toda escolha que você fez sem perguntar deveria estar em
  `duvidas`. Se não está, alguém — ou algum agente — vai decidir de novo, diferente.

## 8. Verificação

- [ ] Existe uma especificação em texto livre, sem jargão técnico.
- [ ] Todo passo do fluxo tem ator, ação e (quando cabe) evento no passado.
- [ ] Todo termo tem definição não circular, nome em código e sinônimos a evitar.
- [ ] Todo passo cita os termos que usa; todo termo é usado por pelo menos um passo.
- [ ] Toda suposição está escrita como dúvida.
- [ ] Todo passo e todo termo tem decisão do especialista, registrada em arquivo versionado.
- [ ] `python3 scripts/gerar_docs.py --check` passa.

Perguntas para você:

1. Na sua área, qual palavra significa coisas diferentes para dois departamentos?
2. Por que um evento no passado (`PedidoConfirmado`) é mais fácil de validar do que uma
   funcionalidade ("confirmar pedido")?
3. O que acontece com uma decisão tomada numa conversa com um agente de IA quando a
   conversa acaba?

## 9. Para saber mais

- Anterior: [Aula 00 — Como usar este guia](00-como-usar.md)
- Próxima: [Aula 02 — Subdomínios e destilação](02-subdominios-e-destilacao.md)
- [Linguagem ubíqua do DomainStudio](../modelo/linguagem-ubiqua.md) (gerada)
- Evans, Eric. *Domain-Driven Design* (2003), cap. 2 "Communication and the Use of Language".
- Brandolini, Alberto. *Introducing EventStorming* (2021).
