---
id: aula-04-agregados-e-invariantes
tipo: aula
titulo: "Aula 04 — Agregados e invariantes"
etapa: 4
resumo: "Como desenhar agregados pequenos a partir das invariantes do negócio, tratando cada agregado como uma fronteira de consistência e de transação."
relacionados: [aula-03-contextos-delimitados-e-mapa, aula-05-blocos-taticos, dicionario-ddd, modelo-domain-studio]
termos: [projeto, especificacao, versao-especificacao, decomposicao, sugestao, revisao, modelo-estrategico, modelo-tatico, regra-de-conformidade]
---

# Aula 04 — Agregados e invariantes

> Em Domain-Driven Design (DDD), um agregado não é "um grupo de classes relacionadas": ele existe **para proteger uma regra que
> precisa ser verdadeira ao fim de cada operação**. Sem invariante, não há motivo para agrupar.
> Com invariante, o agregado é a fronteira da transação — e deve ser o menor possível.

## 1. Objetivos

Ao fim desta aula você será capaz de:

1. **Explicar** o que é uma invariante e por que ela é a razão de existir de um agregado.
2. **Identificar** a raiz de agregado e o que pode (e não pode) ser acessado de fora.
3. **Aplicar** as quatro regras de Vernon para desenhar agregados pequenos.
4. **Distinguir** consistência imediata (dentro do agregado) de consistência eventual (entre agregados).

## 2. O problema

Sem esta etapa aparecem dois extremos, ambos ruins:

- **O agregado-mundo.** `Projeto` contém especificação, todas as versões, todas as decomposições,
  todas as sugestões e o modelo inteiro. Qualquer alteração carrega e trava tudo; dois usuários
  revisando sugestões diferentes entram em conflito; a memória cresce sem limite.
- **O modelo anêmico.** Não há agregados, só tabelas e um serviço que altera qualquer objeto de
  qualquer lugar. A regra "versões publicadas nunca mudam" fica num comentário e alguém, um dia,
  faz `versao.texto = "..."`.

## 3. A ideia central

> **Uma invariante, uma fronteira de consistência, uma transação: modifique um agregado por vez e referencie os outros por identidade.**

Invariante é uma regra de negócio que deve valer **sempre**, não "em algum momento". Tudo que
precisa estar consistente com ela no mesmo instante fica dentro do mesmo agregado, atrás de uma
única porta de entrada — a raiz. Tudo o mais pode ficar em outro agregado e ser atualizado depois,
por eventos.

## 4. Passo a passo

1. **Liste as regras de negócio** de cada contexto delimitado da [Aula 03](03-contextos-delimitados-e-mapa.md),
   escritas como frases que "devem ser sempre verdadeiras".
2. **Separe invariantes verdadeiras de desejos.** Pergunte ao especialista: *se esta regra ficar
   falsa por um segundo, alguém perde algo?* Se não, é consistência eventual, não invariante.
3. **Para cada invariante, liste os dados que ela lê.** Esse conjunto é o candidato a agregado.
4. **Escolha a raiz:** a entidade cuja identidade faz sentido fora do agregado e que consegue
   verificar a regra inteira.
5. **Encolha.** Retire do agregado tudo que a invariante não precisa. O que sobrar de fora vira
   outro agregado, referenciado pelo identificador (ID).
6. **Exponha comportamento, não estado.** A raiz oferece métodos com nomes da linguagem ubíqua
   (`publicar`, `aceitar`, `rejeitar`) que validam a invariante antes de mudar qualquer coisa.
7. **Defina o que acontece entre agregados** com eventos de domínio e políticas (tema da
   [Aula 05](05-blocos-taticos.md)): uma transação altera um agregado; os demais reagem depois.
8. **Registre no Modelo Tático** cada agregado com sua raiz, seus elementos internos e suas invariantes escritas.

## 5. Fundamentos

**Definições.** Evans (*Blue Book*, cap. 6) define o [Agregado](../ddd-dicionario.md#agregado-aggregate)
como um cluster de objetos tratado como unidade para mudanças de dados, com uma
[Raiz de Agregado](../ddd-dicionario.md#raiz-de-agregado-aggregate-root) como único ponto de acesso.
Objetos internos podem ter identidade local, mas ninguém de fora guarda referência a eles.

**Fronteira de consistência = transação.** Toda transação deve criar ou alterar **um** agregado.
Se um caso de uso precisa alterar dois agregados de forma atômica, ou a fronteira está errada, ou a
regra não é uma invariante de verdade.

**As quatro regras de Vernon** (*Implementing DDD*, cap. 10):

| Regra | O que diz | Por quê |
|-------|-----------|---------|
| 1. Modele invariantes verdadeiras em fronteiras de consistência | O agregado existe para proteger regras que valem a cada transação. | Sem invariante, o agrupamento é arbitrário. |
| 2. Desenhe agregados pequenos | Raiz + o mínimo de valores e entidades que a invariante exige. | Menos conflito de concorrência, carga rápida, testes simples. |
| 3. Referencie outros agregados por identidade | Guarde `projeto_id`, não o objeto `Projeto`. | Impede alterar dois agregados na mesma transação e desacopla o carregamento. |
| 4. Use consistência eventual fora da fronteira | Outros agregados reagem a eventos de domínio. | Escala e mantém cada agregado autônomo. |

Vernon admite exceções à regra 4 (conveniência de interface, falta de infraestrutura de mensagens),
mas elas devem ser decisões conscientes, não o padrão.

**Referências entre agregados.** A [regra de ouro do dicionário](../ddd-dicionario.md#raiz-de-agregado-aggregate-root):
entre agregados, só **ID**. O [Repositório](../ddd-dicionario.md#repositório-repository) existe
por agregado, e só para a raiz.

## 6. Na prática — o DomainStudio aplicado a si mesmo

Invariantes do [modelo do DomainStudio](../modelo-domain-studio.md#4-contextos-delimitados) e os
agregados que elas justificam (todos `proposto`):

| Agregado (raiz) | Invariantes | Referências por ID |
|-----------------|-------------|--------------------|
| `Especificacao` | Versões numeradas em sequência; versão publicada nunca muda. | `ProjetoId` |
| `Projeto` | (Nenhuma forte além de nome válido.) | — |
| `Decomposicao` | Só uma decomposição concluída aceita revisões; sugestão revisada não volta a pendente. | `ProjetoId`, número da versão |
| `ModeloEstrategico` | Nomes únicos; relação não liga um contexto a si mesmo; todo contexto pertence a um subdomínio. | `ProjetoId` |
| `ModeloTatico` | Cada agregado tem exatamente uma raiz; cada entidade pertence a um só agregado; referências entre agregados por identidade. | `ContextoId` |

**Por que `Especificacao` não está dentro de `Projeto`?** A invariante das versões não precisa do
nome nem da descrição do projeto. Separar permite renomear o projeto e publicar uma versão ao mesmo
tempo sem conflito. `Projeto` quase não tem invariante — um sinal de que ele é pequeno e simples, o que é bom.

**Por que `Sugestao` é entidade interna de `Decomposicao`?** Porque a regra "só decomposição
concluída aceita revisões" precisa ver o estado da decomposição *e* o da sugestão juntos. Esboço
(proposta; ainda não existe no repositório):

```python
from dataclasses import dataclass, field
from enum import Enum

from domain_studio.shared.domain import AggregateRoot, DomainError, DomainEvent, Entity


class EstadoDecomposicao(Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    FALHOU = "falhou"


class EstadoRevisao(Enum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    REJEITADA = "rejeitada"


@dataclass(frozen=True, kw_only=True)
class SugestaoAceita(DomainEvent):
    decomposicao_id: str
    sugestao_id: str


@dataclass(eq=False, kw_only=True)
class Sugestao(Entity):  # entidade interna: só a raiz a altera
    conteudo: str
    estado: EstadoRevisao = EstadoRevisao.PENDENTE


@dataclass(eq=False, kw_only=True)
class Decomposicao(AggregateRoot):
    projeto_id: str  # referência por identidade, não pelo objeto Projeto
    numero_versao: int
    estado: EstadoDecomposicao = EstadoDecomposicao.PENDENTE
    sugestoes: list[Sugestao] = field(default_factory=list)

    def aceitar(self, sugestao_id: str) -> None:
        if self.estado is not EstadoDecomposicao.CONCLUIDA:
            raise DomainError("Só uma decomposição concluída aceita revisões.")
        sugestao = self._sugestao(sugestao_id)
        if sugestao.estado is not EstadoRevisao.PENDENTE:
            raise DomainError("Sugestão já revisada não pode ser revisada de novo.")
        sugestao.estado = EstadoRevisao.ACEITA
        self.record(SugestaoAceita(decomposicao_id=self.id, sugestao_id=sugestao_id))

    def _sugestao(self, sugestao_id: str) -> Sugestao:
        for sugestao in self.sugestoes:
            if sugestao.id == sugestao_id:
                return sugestao
        raise DomainError(f"Sugestão {sugestao_id} não pertence a esta decomposição.")
```

**Consistência eventual entre contextos.** Aceitar uma sugestão *não* altera o `ModeloTatico` na
mesma transação: a `Decomposicao` registra `SugestaoAceita`, e uma política aplica o elemento ao
modelo depois. Se a aplicação falhar (por exemplo, nome duplicado), a sugestão continua aceita e o
usuário vê a violação — um trade-off aceito para manter os agregados independentes.

**Ponto de atenção.** `ModeloEstrategico` é um por projeto e guarda todos os subdomínios, contextos
e relações. A invariante "nomes únicos" justifica isso, mas se projetos crescerem muito ele pode
virar um agregado-mundo. Hoje é uma aposta, não um fato medido.

## 7. Erros comuns

- **Agrupar pelo diagrama de classes.** "Estão ligados por associação, então são um agregado." Associação não é invariante.
- **Referência a objeto entre agregados.** `decomposicao.projeto.nome` permite alterar dois agregados juntos e força carregar os dois.
- **Alterar dois agregados numa transação.** Sintoma de fronteira errada ou de regra que deveria ser eventual.
- **Setters públicos na raiz.** A invariante fica dependente da disciplina de quem chama.
- **Repositório para entidade interna.** `SugestaoRepository` quebra a fronteira: sugestões só se alteram via `Decomposicao`.
- **Invariante que depende de consulta global.** "Nome único entre *todos* os projetos" não cabe num agregado; é regra de serviço ou de banco, com consistência eventual.

## 8. Verificação

- [ ] Todo agregado tem pelo menos uma invariante escrita — ou uma justificativa para existir sem ela.
- [ ] Cada agregado tem exatamente uma raiz, e só ela tem repositório.
- [ ] Nenhum atributo guarda outro agregado inteiro; só IDs.
- [ ] Cada caso de uso altera no máximo um agregado por transação.
- [ ] A raiz expõe métodos com verbos da linguagem ubíqua, e eles validam a invariante antes de mudar o estado.
- [ ] Toda regra entre agregados está descrita como evento + reação.

Perguntas de autoavaliação:

1. Por que "versão publicada nunca muda" é uma invariante do agregado `Especificacao`, e não do `Projeto`?
2. O que você faria se a regra "nomes de contexto únicos no projeto" começasse a gerar conflitos de concorrência no `ModeloEstrategico`?
3. Qual das quatro regras de Vernon o esboço de `Decomposicao` acima aplica ao guardar `projeto_id`?

## 9. Para saber mais

- Anterior: [Aula 03 — Contextos delimitados e mapa](03-contextos-delimitados-e-mapa.md)
- Próxima: [Aula 05 — Blocos táticos](05-blocos-taticos.md)
- [Dicionário de DDD](../ddd-dicionario.md) — seção 3.
- [Modelo do DomainStudio](../modelo-domain-studio.md) — seção 4.
- Eric Evans, *Domain-Driven Design* (2003), cap. 6 "The Life Cycle of a Domain Object".
- Vaughn Vernon, *Implementing Domain-Driven Design* (2013), cap. 10 "Aggregates".
- Vaughn Vernon, "Effective Aggregate Design", partes I–III (2011), dddcommunity.org.
