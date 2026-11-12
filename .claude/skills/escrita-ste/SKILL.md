---
name: escrita-ste
description: Aplica e valida a escrita no estilo STE (ASD-STE100, Simplified Technical English, adaptado ao português) em prompts, instruções, procedimentos, runbooks e documentação. Identifica quais partes de um texto devem ser convertidas (regras, passos, avisos, definições), converte só essas partes para frases curtas, diretas e sem ambiguidade, preserva o resto, e valida o resultado com um linter. Use sempre que o usuário pedir para "aplicar STE", "passar para STE", "validar STE", "frases diretas", "escrita da aviação", "inglês técnico simplificado", "linguagem controlada", ou pedir para deixar um prompt ou uma instrução mais claro, auditável, explicável ou sem ambiguidade, mesmo que não cite a norma. Use também para revisar se um prompt de sistema mistura termos para o mesmo conceito.
---

# Escrita STE

O STE (ASD-STE100) é a norma de escrita dos manuais de manutenção da aviação.
O objetivo dela é que cada frase tenha uma só leitura possível. Esta skill
aplica as regras de escrita da norma a textos em português ou inglês, com foco
em prompts e instruções.

A norma oficial só existe para o inglês e inclui um dicionário de palavras
aprovadas. Aqui usamos as regras de escrita. O papel do dicionário é feito por
um glossário do projeto, quando existe.

## O princípio que orienta tudo

O STE serve para texto que alguém **executa**. Ele prejudica texto que alguém
precisa **entender ou imitar**. Uma regra convertida fica mais clara e mais
fácil de auditar. Um exemplo, um critério subjetivo ou a explicação de um
motivo perdem informação quando viram comandos secos, e o modelo que lê o
prompt decide pior nos casos que o texto não previu.

Por isso o trabalho tem três partes, nesta ordem: classificar, converter só o
que se aplica, validar. Converter o texto inteiro é o erro mais comum.

A conversão nunca pode mudar o que o texto pede. Se uma frase é ambígua e você
não sabe qual leitura o autor quis, não escolha por ele: registre a dúvida em
"Pendências".

## Modos

- **Converter** (padrão): classificar, converter, validar e entregar o relatório.
- **Validar**: o usuário só quer saber se o texto está conforme. Classifique,
  rode o linter nos trechos que se aplicam e entregue o relatório, sem reescrever.

## Passo 1: classificar os segmentos

Divida o texto em segmentos. Um segmento é um trecho com uma só função: um
parágrafo, uma lista, um bloco. Dê a cada segmento um dos tipos abaixo.

| Tipo | Como reconhecer | Aplica STE? |
|---|---|---|
| Procedimento | Passos em sequência, que alguém executa | Sim |
| Regra | Obrigação, proibição ou restrição ("sempre", "nunca", "deve") | Sim |
| Aviso | Risco ou consequência grave se algo for feito errado | Sim |
| Definição | Diz o que um termo significa | Sim |
| Formato de saída descrito em prosa | Diz como a resposta deve ser organizada | Sim |
| Motivo | Explica por que uma regra existe | Parcial |
| Contexto | Situação, público, objetivo, histórico | Parcial |
| Critério de julgamento | Pede avaliação com nuance ("tom cordial", "resposta completa") | Não |
| Exemplo | Entrada ou saída de amostra, few-shot, diálogo | Não |
| Persona e tom | Como o modelo deve soar | Não |
| Literal | Código, JSON, esquema, texto citado, nome de campo, placeholder, tag | Não |

"Parcial" quer dizer: frases curtas, voz ativa e um termo por conceito, mas em
prosa. Não transforme em lista de comandos e não corte informação.

Um parágrafo real costuma misturar tipos. Quando uma regra vem junto com o
motivo, separe os dois: a regra vira frase STE, e o motivo fica logo depois,
em uma frase curta. Não apague o motivo.

Em caso de dúvida entre "Sim" e "Não", pergunte: se eu trocar as palavras
deste trecho, o resultado esperado muda? Se muda (exemplos, tom, literais),
não converta.

## Passo 2: converter os segmentos que se aplicam

Regras principais. A lista completa, com antes e depois, está em
`references/regras.md`. Leia esse arquivo antes da primeira conversão.

1. **Uma instrução por frase.** Duas ações viram duas frases ou dois passos.
2. **Frases curtas.** Até 20 palavras em procedimento, regra e aviso. Até 25
   em texto descritivo.
3. **Imperativo nos comandos.** "Informe o prazo", e não "o prazo deve ser
   informado" nem "é importante informar o prazo".
4. **Voz ativa, com sujeito explícito.** Diga quem faz a ação.
5. **Condição primeiro.** "Se o cliente pedir o cancelamento, registre o
   motivo", e não "registre o motivo, se o cliente pedir o cancelamento".
6. **Um termo por conceito.** Escolha um termo e repita. Não alterne
   sinônimos. Se o projeto tem glossário, o termo do glossário vence.
7. **Um verbo por ação.** Se "verifique", "confira" e "valide" significam a
   mesma coisa no texto, use um só.
8. **Sem gerúndio encadeado.** "Abra o arquivo. Leia o cabeçalho", e não
   "abrindo o arquivo, leia o cabeçalho".
9. **Sem termos vagos.** Troque "se necessário", "adequado", "etc." pela
   condição ou pelo valor exato. Se o texto original não diz qual é, registre
   em "Pendências".
10. **Aviso em bloco próprio.** Primeiro o comando, depois o risco:
    "**Cuidado:** Não envie o CPF por e-mail. O e-mail não é criptografado."
11. **Passos numerados só quando a ordem importa.** Regras sem ordem ficam em
    lista com marcador.
12. **Parágrafos de até 6 frases**, um assunto por parágrafo.

O que não muda em nenhuma hipótese: nomes de campos, variáveis e placeholders
(`{{nome}}`, `<tag>`), código, valores, limites numéricos, texto entre aspas
que o modelo deve reproduzir, e a ordem dos passos.

Mantenha a língua do texto original. Não traduza.

### Numeração das regras (opcional)

Regras atômicas podem receber identificador (`R1`, `R2`...). Isso permite que
o modelo cite na resposta qual regra aplicou, e é o que mais contribui para a
explicabilidade. Numerar altera a estrutura do prompt, então só numere se o
usuário pediu ou concordou. Se não pediu, ofereça no fim do relatório.

## Passo 3: validar

Salve o texto convertido em um arquivo e rode o linter nas linhas dos
segmentos convertidos:

```bash
python3 scripts/validar_ste.py CAMINHO --linhas 3-20,31-40
```

- `--linhas` restringe a validação aos segmentos que receberam STE. Sem essa
  opção o linter analisa o arquivo todo, e os trechos que você preservou de
  propósito vão gerar achados falsos.
- `--glossario ARQUIVO` ativa a checagem de termos. Formato, uma linha por
  termo: `cliente: contribuinte, empresa, usuário`. O primeiro termo é o
  preferido; os outros são proibidos.
- `--json` devolve os achados em JSON. `--estrito` faz avisos reprovarem.

O linter ignora blocos de código, tabelas, títulos e comentários HTML. Ele
trata item numerado e parágrafo de aviso como procedimento (limite 20), e o
resto como descritivo (limite 25).

Corrija todos os **erros** e rode de novo até passar. Para cada **aviso**,
decida: corrija, ou mantenha e explique no relatório. O linter usa heurísticas
de forma, pensadas para o português, e gera falsos positivos (por exemplo, um
substantivo terminado em "-ado" lido como particípio). Em texto em inglês só a
contagem de palavras e o glossário são confiáveis.

O linter não vê o sentido. Depois que ele passar, confira você mesmo, segmento
por segmento:

- A versão convertida pede exatamente o mesmo que a original? Nada foi
  perdido, nada foi acrescentado?
- Todo motivo que existia no original continua no texto?
- Cada conceito tem um só termo no texto inteiro, inclusive nos trechos em prosa?
- Os literais e os exemplos estão idênticos ao original?

## Formato da entrega

Use esta estrutura:

```markdown
## Mapa de segmentos
| # | Linhas | Tipo | STE | Observação |
|---|--------|------|-----|------------|

## Texto convertido
(texto completo, pronto para uso; segmentos não convertidos ficam idênticos ao original)

## Validação
- Linter: N frases, N erros, N avisos (comando usado)
- Avisos mantidos: qual e por quê
- Conferência de sentido: o que foi checado

## Pendências
(ambiguidades do original que só o autor resolve; termos concorrentes para o mesmo conceito)
```

Se o usuário pediu a alteração em um arquivo, grave o texto convertido no
arquivo e deixe no relatório só o mapa, a validação e as pendências.

No modo Validar, troque "Texto convertido" por "Achados", com linha, regra,
trecho e correção sugerida.

## Exemplo curto

Original:

> Ao receber uma mensagem, é importante que seja verificado se o cliente já
> tem um atendimento aberto, criando um novo caso ele não tenha, e sempre
> respondendo de forma acolhedora, pois muitos clientes chegam frustrados
> depois de tentar outros canais.

Classificação: procedimento (verificar e criar), critério de tom (acolhedora),
motivo (clientes frustrados).

Convertido:

> 1. Verifique se o cliente tem um atendimento aberto.
> 2. Se o cliente não tem um atendimento aberto, crie um atendimento.
>
> Responda de forma acolhedora. Muitos clientes chegam frustrados depois de
> tentar outros canais.

O passo 2 repete "atendimento aberto" de propósito: repetir o termo é melhor
do que usar um pronome ambíguo. O critério de tom e o motivo ficaram em prosa,
só com frases mais curtas.
