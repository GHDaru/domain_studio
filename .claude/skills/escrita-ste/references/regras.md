# Regras de escrita STE adaptadas ao português

Catálogo das regras usadas pela skill. A coluna "Linter" indica o código que
`scripts/validar_ste.py` emite. Regras sem código dependem de leitura humana.

## Índice

1. Frases
2. Verbos
3. Vocabulário
4. Estrutura
5. Avisos
6. Casos de classificação difíceis
7. O que a norma original tem e esta adaptação não tem

## 1. Frases

| Regra | Linter | Antes | Depois |
|---|---|---|---|
| Até 20 palavras em procedimento, regra e aviso | STE-01 | "Depois de confirmar com o cliente o número do pedido e o e-mail de cadastro, localize o pedido no sistema e informe a situação atual." | "Confirme com o cliente o número do pedido e o e-mail de cadastro. Localize o pedido no sistema. Informe a situação do pedido." |
| Até 25 palavras em texto descritivo | STE-01 | — | — |
| Uma instrução por frase | STE-05 | "Abra o chamado e depois avise o gestor." | "Abra o chamado. Avise o gestor." |
| Condição antes do comando | STE-06 | "Encaminhe ao fiscal, se a dúvida for sobre imposto." | "Se a dúvida for sobre imposto, encaminhe ao fiscal." |
| Sem oração intercalada longa | — | "O atendente, que já deve ter lido o histórico, responde." | "Leia o histórico. Depois responda." |
| Frase completa, sem estilo telegráfico | — | "Verificar cadastro. Pendência: avisar." | "Verifique o cadastro. Se o cadastro tem pendência, avise o cliente." |

Duas ações podem ficar na mesma frase só quando são simultâneas: "Segure o
botão e gire a chave".

## 2. Verbos

| Regra | Linter | Antes | Depois |
|---|---|---|---|
| Imperativo nos comandos | STE-07 | "Você deve informar o prazo." / "Informar o prazo." | "Informe o prazo." |
| Voz ativa | STE-03 | "O prazo deve ser informado ao cliente." | "Informe o prazo ao cliente." |
| Sujeito explícito | STE-03 | "Recomenda-se revisar o texto." | "Revise o texto." |
| Sem gerúndio encadeado | STE-04 | "Responda ao cliente, informando o prazo." | "Responda ao cliente. Informe o prazo." |
| Tempos simples | — | "Caso o cliente venha a ter solicitado" | "Se o cliente solicitou" |
| Um verbo por ação | — | "verifique", "confira", "cheque", "valide" para a mesma ação | "verifique" em todas |

Em texto descritivo a voz passiva é aceita quando o agente é desconhecido ou
irrelevante ("O arquivo é gerado todo dia às 6h"). Por isso o linter marca
passiva como erro em procedimento e como aviso em texto descritivo.

## 3. Vocabulário

| Regra | Linter | Antes | Depois |
|---|---|---|---|
| Um termo por conceito | STE-09 (com glossário) | "cliente", "contribuinte" e "empresa" para a mesma coisa | "cliente" em todo o texto |
| Sem termos vagos | STE-08 | "Encaminhe se necessário." | "Se o cliente pedir um prazo maior que 5 dias, encaminhe ao gestor." |
| Sem "etc." e "entre outros" | STE-08 | "Peça CPF, RG, etc." | "Peça CPF e RG." (ou liste todos) |
| Sem "e/ou" | STE-08 | "Envie por e-mail e/ou WhatsApp." | "Envie por e-mail, por WhatsApp, ou pelos dois." |
| Repita o substantivo em vez de pronome ambíguo | — | "Compare o boleto com a nota e envie-a." | "Compare o boleto com a nota. Envie a nota." |
| Números em algarismos, com unidade | — | "em alguns dias" | "em até 3 dias úteis" |
| Negação simples | — | "Não deixe de não enviar sem confirmar." | "Confirme antes de enviar." |

Quando o original é vago e você não sabe o valor exato ("prazo razoável"),
não invente o valor. Mantenha o termo e registre em "Pendências".

Formato do glossário para o linter, uma linha por conceito:

```
# preferido: proibidos
cliente: contribuinte, empresa, usuário
atendimento: chamado, ticket, protocolo
verifique: confira, cheque, valide
```

Um glossário de domínio do projeto (por exemplo, um dicionário de linguagem
ubíqua) é a melhor fonte para os termos preferidos.

## 4. Estrutura

| Regra | Linter | Como aplicar |
|---|---|---|
| Parágrafo de até 6 frases | STE-02 | Divida por assunto. |
| Um assunto por parágrafo | — | A primeira frase diz o assunto. |
| Passos numerados quando a ordem importa | — | Um passo, uma ação. |
| Lista com marcador para regras sem ordem | — | Cada item é uma frase completa. |
| Motivo logo depois da regra | — | "Não informe valores por telefone. O canal não tem registro." |

## 5. Avisos

Um aviso tem três partes, nesta ordem:

1. Rótulo: `Cuidado:` (pode causar dano) ou `Atenção:` (pode causar erro).
2. Comando: o que fazer ou não fazer.
3. Risco: o que acontece se o comando não for seguido.

Antes: "Vale lembrar que dados bancários não devem ser pedidos pelo chat, já
que isso pode expor o cliente a golpes."

Depois: "**Cuidado:** Não peça dados bancários pelo chat. O cliente pode ser
vítima de golpe."

O aviso fica antes do passo a que se refere, nunca depois.

## 6. Casos de classificação difíceis

**Regra com exceção subjetiva.** "Seja breve, a não ser que o cliente esteja
confuso." A parte "seja breve" é regra; "esteja confuso" é julgamento.
Converta a estrutura ("Se o cliente está confuso, explique com mais
detalhes. Nos outros casos, responda em até 3 frases.") só se o limite
numérico já estiver no original. Se não estiver, mantenha a frase e registre
a pendência.

**Critério de avaliação com rubrica.** A lista de critérios é estrutura e pode
ser convertida em itens. A descrição de cada nível ("nota 3: resposta correta
mas fria") é julgamento e fica como está.

**Persona com regras embutidas.** "Você é um assistente contábil experiente
que nunca dá conselho jurídico." Separe: a persona fica em prosa; "Não dê
conselho jurídico" vira regra.

**Exemplo com comentário.** O exemplo é literal. O comentário que explica o
exemplo é contexto (parcial).

**Texto que o modelo deve reproduzir.** Mensagens prontas, saudações e
modelos de resposta são literais, mesmo que estejam fora de aspas.

**Formato de saída.** A descrição em prosa converte bem ("Responda em JSON.
Use as chaves `nota` e `motivo`."). O esquema ou o exemplo de saída é literal.

**Prompt já estruturado em XML ou seções.** Classifique o conteúdo de cada
tag ou seção. Não renomeie tags nem mude a ordem das seções.

## 7. O que a norma original tem e esta adaptação não tem

- **Dicionário controlado.** O ASD-STE100 traz cerca de 900 palavras
  aprovadas, cada uma com um só significado e uma só classe gramatical. Não
  existe versão em português. O glossário do projeto cobre o mesmo objetivo
  para os termos do domínio.
- **Regras próprias do inglês.** Limite de três substantivos em sequência,
  restrição da forma em *-ing*, uso obrigatório de artigos. Em português, a
  regra do gerúndio cobre parte disso; as outras não se aplicam.
- **Certificação.** Um texto que passa por esta skill segue o estilo STE. Ele
  não está "em conformidade com o ASD-STE100" no sentido formal.
