---
id: aula-00-como-usar
tipo: aula
titulo: "Aula 00 — Como usar este guia"
etapa: 0
resumo: "Mapa da trilha: as etapas do método, a ordem das aulas e como cada uma vira ajuda dentro do produto."
relacionados: [aula-01-linguagem-ubiqua-e-fluxo, dicionario-ddd, modelo-domain-studio, grafo]
termos: []
---
# Aula 00 — Como usar este guia

> Este guia ensina o método que o DomainStudio executa — e o DomainStudio é construído
> seguindo este guia. Cada aula é uma etapa do método, aplicada ao próprio produto.

## A trilha

O método transforma um texto sobre um negócio em software, em etapas. Cada etapa produz um
artefato que a seguinte consome — nenhuma etapa trabalha "de memória".

| Etapa | Aula | Pergunta que responde | Artefato que produz |
|---|---|---|---|
| 1 | [Linguagem ubíqua e fluxo](01-linguagem-ubiqua-e-fluxo.md) | O que acontece no negócio, e como as coisas se chamam? | `fluxo.yaml`, `linguagem-ubiqua.yaml` validados |
| 2 | [Subdomínios e destilação](02-subdominios-e-destilacao.md) | Onde está o valor? Onde investir? | Tabela de subdomínios (núcleo / suporte / genérico) |
| 3 | [Contextos delimitados e mapa](03-contextos-delimitados-e-mapa.md) | Onde cada palavra tem um só significado? Como as partes conversam? | Contextos + mapa de contexto (`.cml`) |
| 4 | [Agregados e invariantes](04-agregados-e-invariantes.md) | Que regras nunca podem ser quebradas, e quem as protege? | Agregados com invariantes |
| 5 | [Blocos táticos](05-blocos-taticos.md) | Entidade ou valor? Serviço, evento, política? | Modelo tático por contexto |
| 6 | [Do modelo ao código](06-do-modelo-ao-codigo.md) | Como o modelo vira código sem se perder? | Esqueleto hexagonal (FastAPI) |
| 7 | [Artefatos para a IA](07-artefatos-para-ia.md) | O que a IA precisa carregar para trabalhar dentro do modelo? | Instruções, glossário, grafo e índice |

A etapa 7 atravessa todas as outras: a partir da etapa 1, cada artefato já nasce legível
por pessoas **e** por agentes de IA.

## Como cada aula é organizada

Todas têm as mesmas nove seções, para que você saiba onde procurar:

1. **Objetivos** — o que você saberá fazer ao terminar.
2. **O problema** — o que dá errado quando se pula esta etapa.
3. **A ideia central** — a frase para lembrar.
4. **Passo a passo** — o procedimento. É esta seção que vira a ajuda contextual do produto.
5. **Fundamentos** — a teoria, com referência ao [dicionário](../ddd-dicionario.md).
6. **Na prática** — a etapa aplicada ao próprio DomainStudio.
7. **Erros comuns** — o que evitar e por quê.
8. **Verificação** — checklist para conferir o seu próprio modelo.
9. **Para saber mais** — próximos passos e referências.

## Como ler

- **Primeira vez**: siga a ordem 00 → 07. Cada aula assume a anterior.
- **Consulta**: vá direto à seção 4 (passo a passo) ou 8 (verificação) da etapa em que está.
- **Termo desconhecido**: o [dicionário de DDD](../ddd-dicionario.md) define todos os termos
  do método; a [linguagem ubíqua](../modelo/linguagem-ubiqua.md) define os termos do produto.
- **Visão geral**: o [grafo da documentação](../grafo.md) mostra como tudo se liga.

## De onde vem a forma deste guia

A estrutura de nove seções, a regra de escrever toda sigla por extenso na primeira vez e a
ideia de que *o que não está num artefato consumido se perde* vêm do método Maestro
(repositório `GHDaru/maestro`), que trata de um humano conduzindo muitos agentes de IA. O
DomainStudio aplica essas regras ao problema específico de modelagem de domínio.

## Para saber mais

- Próxima: [Aula 01 — Linguagem ubíqua e fluxo](01-linguagem-ubiqua-e-fluxo.md)
- [Modelo do DomainStudio](../modelo-domain-studio.md) — o exemplo que percorre todas as aulas
