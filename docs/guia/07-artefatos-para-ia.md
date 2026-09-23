---
id: aula-07-artefatos-para-ia
tipo: aula
titulo: "Aula 07 — Artefatos para a IA"
etapa: 7
resumo: "Como o método gera o que agentes de IA carregam: instrução por contexto, memória medida no início da sessão, documentação em grafo e índice consultável."
relacionados: [aula-06-do-modelo-ao-codigo, aula-01-linguagem-ubiqua-e-fluxo, aula-03-contextos-delimitados-e-mapa, plano-de-implementacao, grafo, linguagem-ubiqua]
termos: [artefato-para-ia, artefato-de-codigo]
---
# Aula 07 — Artefatos para a IA

> Um agente de Inteligência Artificial (IA) começa toda sessão sem memória. Ele sabe
> apenas o que o ambiente carrega para ele. Por isso o método não termina no código: ele
> gera também **o que a IA deve ler** para trabalhar dentro do modelo — e gera a partir das
> mesmas fontes, para que isso nunca envelheça em silêncio.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** como um harness de agente (como o Claude Code) monta a memória de uma sessão;
2. **Distinguir** o que deve ser carregado sempre, o que deve ser carregado sob demanda e o
   que deve ser consultado sem carregar;
3. **Usar** o contexto delimitado como fronteira de contexto da IA;
4. **Estruturar** a documentação como grafo (identificadores, relações, índice) verificável;
5. **Listar** os artefatos para IA que o DomainStudio vai gerar para cada projeto.

## 2. O problema

Três falhas se repetem quando agentes de IA trabalham num projeto:

1. **Amnésia.** A decisão tomada ontem, na conversa, não existe hoje. O agente decide de
   novo — muitas vezes diferente.
2. **Resposta de memória.** Perguntado "estamos seguindo o método?", o agente responde o que
   *pretendia* fazer, não o que o repositório mostra. Memória relata intenção, não fato.
3. **Instrução que apodrece.** Alguém escreveu à mão, no arquivo de instruções, a lista de
   regras e skills. Uma skill nova foi criada depois; a lista não foi atualizada; a skill
   ficou invisível para a IA por semanas.

As três foram observadas e documentadas no método Maestro (corolários C12 e C13, ADR 0013 do
repositório `GHDaru/maestro`).

## 3. A ideia central

> **A memória da IA é o que o repositório carrega para ela. Então o repositório deve
> carregar fatos medidos, gerados das fontes, cortados pela fronteira do contexto.**

Três regras decorrem disso:

- **O que sobrevive é o que está num artefato consumido** — o resto é apagado, não degradado.
- **Instrução para IA é gerada do disco**, nunca mantida à mão em paralelo.
- **Carregue pouco e certo**: o contexto da IA é finito e piora à medida que enche.

## 4. Passo a passo

1. **Separe três camadas de memória:**

   | Camada | Quando entra no contexto | Exemplo neste repositório |
   |---|---|---|
   | Sempre carregada | início de toda sessão | `CLAUDE.md` da raiz, saída do hook de início de sessão |
   | Sob demanda | quando a IA toca aquela área | `CLAUDE.md` dentro de um contexto delimitado (planejado) |
   | Consultada, não carregada | quando a IA pergunta | `docs/indice.jsonl`, `linguagem-ubiqua.yaml`, o grafo |

2. **Mantenha o arquivo sempre carregado curto.** Ele diz *onde* estão as coisas e *quais
   regras são inegociáveis*; não repete o conteúdo delas.
3. **Carregue fatos medidos no início da sessão.** Um hook `SessionStart` roda comandos e
   imprime o resultado; a saída entra no contexto. Assim a IA começa sabendo o estado
   **medido agora** (quantos termos ainda são hipótese, se a documentação está coerente),
   em vez de lembrar.
4. **Corte a instrução pela fronteira do contexto delimitado.** Quem trabalha no contexto
   Decomposição precisa da linguagem da Decomposição, não da de todos os contextos.
5. **Dê a cada documento um identificador e relações.** Frontmatter com `id`, `tipo`,
   `resumo`, `relacionados` e `termos`. Isso transforma a pasta `docs/` num grafo.
6. **Gere as visões derivadas por script**: a versão legível do vocabulário, o grafo
   navegável e um índice de uma linha por documento, que a IA consulta sem abrir tudo.
7. **Transforme a coerência em verificação.** `gerar_docs.py --check` falha se um link
   quebrou, se um documento cita um termo que não existe, ou se algo gerado está
   desatualizado. Regra sem comando é regra sem efeito.
8. **Nunca reescreva a história.** Decisões são acrescentadas (um registro novo que
   substitui o anterior), não editadas. Mudar de ideia é legítimo; apagar o registro de que
   se pensava diferente não é.

## 5. Fundamentos

### 5.1 Como o harness monta a memória (Claude Code)

- **`CLAUDE.md`** na raiz do projeto é lido no início de toda sessão. Arquivos `CLAUDE.md`
  em **subpastas** são lidos quando o agente passa a trabalhar em arquivos daquela subpasta —
  memória sob demanda, por diretório.
- **`@caminho`** dentro do `CLAUDE.md` importa outro arquivo inteiro para o contexto. É
  poderoso e caro: tudo que é importado ocupa contexto em toda sessão. O Maestro mede esse
  custo (a constituição importada custa cerca de 1.500 tokens por sessão).
- **Hooks** são comandos que o harness executa em eventos. A saída do `SessionStart` vira
  contexto visível para o agente — é o ponto certo para **fatos medidos**.
- **Skills** carregam só a descrição de uma linha; o corpo entra quando a skill se aplica.
  É o mesmo princípio de "sob demanda".
- **`AGENTS.md`** é o nome que outros assistentes leem. Um link simbólico para o `CLAUDE.md`
  evita duas cópias que divergem (lição do ADR 0013 do Maestro).

### 5.2 Por que o contexto delimitado é a fronteira certa

No DDD, dentro de um contexto delimitado cada palavra tem um único significado
([aula 03](03-contextos-delimitados-e-mapa.md)). Para a IA isso é exatamente o que se quer:
um recorte em que não há ambiguidade. Carregar a linguagem de **um** contexto é carregar
menos **e** carregar sem contradição. O Maestro chega à mesma conclusão pelo outro lado:
"paralelize por contexto delimitado — bons cortes tornam a orquestração segura".

### 5.3 Documentação como grafo

Uma pasta de Markdown é uma árvore; o conhecimento é um grafo. O frontmatter explicita as
arestas:

```yaml
---
id: aula-07-artefatos-para-ia
tipo: aula
resumo: "Como o método gera o que agentes de IA carregam…"
relacionados: [aula-06-do-modelo-ao-codigo, grafo, linguagem-ubiqua]
termos: [artefato-para-ia]
---
```

Com isso, um script gera:

- [`docs/grafo.md`](../grafo.md) — o grafo em Mermaid, com nós clicáveis (documentos) e o
  grafo do domínio (termos × contextos × passos do fluxo);
- [`docs/indice.jsonl`](../indice.jsonl) — uma linha JSON por documento. A IA procura ali
  ("qual documento fala de agregados?") e abre só o que precisa. É o mesmo padrão do
  `decisoes.jsonl` do Maestro: prosa para quem lê, índice para quem consulta.

### 5.4 Gerado do disco, verificado no disco

Uma lista escrita à mão compara com a memória de quem escreveu; uma lista gerada compara
com o que existe. Por isso a versão legível do vocabulário
([`linguagem-ubiqua.md`](../modelo/linguagem-ubiqua.md)) é **gerada** do YAML, e o `--check`
falha se alguém editar uma sem a outra.

## 6. Na prática — o DomainStudio aplicado a si mesmo

O que já existe neste repositório:

| Artefato | Camada | Função |
|---|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) (+ `AGENTS.md` → link) | sempre | Mapa, regras inegociáveis, fluxo do método |
| [`.claude/settings.json`](../../.claude/settings.json) + [`scripts/hooks/estado-sessao.sh`](../../scripts/hooks/estado-sessao.sh) | sempre | Imprime no início da sessão: branch, termos ainda `proposto`, dúvidas abertas, coerência do grafo |
| [`linguagem-ubiqua.yaml`](../modelo/linguagem-ubiqua.yaml), [`fluxo.yaml`](../modelo/fluxo.yaml) | consulta | Fonte única do vocabulário e do fluxo |
| [`grafo.md`](../grafo.md), [`indice.jsonl`](../indice.jsonl) | consulta | Visões geradas |
| [`scripts/gerar_docs.py`](../../scripts/gerar_docs.py) | — | Gera as visões e verifica (`--check`) |

O que o DomainStudio vai **gerar para cada projeto do usuário** (marco de geração de código):

| Artefato gerado | Conteúdo |
|---|---|
| `CLAUDE.md` raiz + `AGENTS.md` | Mapa de contextos, regra de dependência, onde estão vocabulário, grafo e decisões |
| `src/<contexto>/CLAUDE.md` | Só a linguagem **daquele** contexto, seus agregados e invariantes, e o que ele pode importar |
| `docs/modelo/linguagem-ubiqua.yaml` | Vocabulário validado |
| `docs/modelo/mapa.cml` | Mapa de contexto |
| `docs/indice.jsonl`, `docs/grafo.md` | Índice e grafo |
| Hook `SessionStart` | Estado medido: termos não validados, violações de conformidade abertas |
| `docs/adr/` + `docs/registros/decisoes.jsonl` | Decisões, só por acréscimo |

Isso fecha o ciclo do produto: o mesmo modelo gera o código **e** o contexto que a IA
precisa para mexer nele sem sair do modelo.

## 7. Erros comuns

- **Um `CLAUDE.md` enciclopédico.** Tudo importado em toda sessão: caro, e a IA passa a
  ignorar partes. Carregue o mapa; deixe o território para consulta.
- **Memória por resumo de conversa.** Um "banco de memória" escrito pelo próprio agente
  duplica o que os artefatos já guardam e reintroduz a memória-intenção.
- **Lista mantida à mão.** Skills, termos, contextos listados manualmente no arquivo de
  instruções. Vai divergir.
- **Glossário só em prosa.** A IA consegue ler, mas não consegue verificar. Mantenha a fonte
  estruturada (YAML) e gere a prosa.
- **Grafo desenhado à mão.** Um diagrama bonito que ninguém atualiza mente com o tempo.
  Gere-o das relações declaradas.

## 8. Verificação

- [ ] O arquivo sempre carregado cabe em uma tela e aponta para as fontes, sem copiá-las.
- [ ] O hook de início de sessão imprime fatos medidos, e nunca falha a sessão.
- [ ] Todo documento em `docs/` tem `id`, `tipo`, `resumo` e `relacionados`.
- [ ] Toda visão derivada é gerada por script e o `--check` passa.
- [ ] Nenhuma lista na instrução da IA é mantida à mão em paralelo a uma fonte.
- [ ] Cada contexto delimitado terá instrução própria, com só a sua linguagem.

Perguntas para você:

1. Qual a diferença entre a IA *lembrar* uma regra e o ambiente *verificar* a regra?
2. Por que a linguagem de um contexto delimitado é um bom recorte de contexto para a IA?
3. O que acontece com uma lista de skills escrita à mão quando uma skill nova é criada?

## 9. Para saber mais

- Anterior: [Aula 06 — Do modelo ao código](06-do-modelo-ao-codigo.md)
- Início: [Aula 00 — Como usar este guia](00-como-usar.md)
- Repositório `GHDaru/maestro`: `docs/handbook/04-fluxo-agentic-contexto.md`,
  `docs/handbook/11-rastreabilidade.md`, `docs/governance/axioms.md` (C12, C13),
  `docs/adr/0013-instrucao-para-ia-gerada-e-fonte-unica.md`,
  `scripts/hooks/session-state.sh`.
- Documentação do Claude Code: memória (`CLAUDE.md`), hooks e skills —
  <https://code.claude.com/docs>.
