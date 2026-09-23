# DomainStudio — instruções para agentes

> Lido no início de toda sessão. `AGENTS.md` é link simbólico para este arquivo (fonte única).
> Mantido curto de propósito: aponta para as fontes, não as copia (Aula 07).

## O que é
Aplicação que decompõe a especificação de um domínio em modelo DDD, diagramas e código.
O projeto é construído **pelo próprio método**: `docs/modelo-domain-studio.md` é o modelo dele.

## Regras inegociáveis
- **Use a linguagem ubíqua.** Nomes de classes, rotas, eventos e textos vêm de
  `docs/modelo/linguagem-ubiqua.yaml` (campo `codigo`). Nunca use os sinônimos em `evitar`.
  Termo novo? Proponha no YAML com `status: proposto` — não invente no código.
- **Termo `proposto` é hipótese.** Não trate como decidido; se a tarefa depende dele, diga.
- **Fontes únicas; derivados são gerados.** Edite `docs/modelo/*.yaml` e o frontmatter dos
  docs; nunca edite `docs/modelo/linguagem-ubiqua.md`, `docs/grafo.md`, `docs/indice.jsonl`
  nem o bloco de dados de `prototipos/validacao-linguagem.html`. Depois rode
  `python3 scripts/gerar_docs.py`.
- **Todo documento em `docs/` tem frontmatter** (`id`, `tipo`, `titulo`, `resumo`,
  `relacionados`, `termos`). `python3 scripts/gerar_docs.py --check` tem que passar.
- **Estado do projeto: não responda de memória.** Rode `scripts/hooks/estado-sessao.sh`.
- **Sigla nasce por extenso** na primeira ocorrência de cada documento.

## Fluxo do método (uma aula por etapa em `docs/guia/`)
1 linguagem e fluxo validados → 2 subdomínios → 3 contextos e mapa → 4 agregados →
5 blocos táticos → 6 código (hexagonal) → 7 artefatos para IA.
Não pule etapas: código só para elementos cujo vocabulário foi validado.

## Código (`backend/`)
- FastAPI; um pacote por contexto delimitado com `domain/ application/ infrastructure/ api/`.
- Regra de dependência: `api → application → domain ← infrastructure`. Domínio sem framework.
- Antes de concluir: `cd backend && pytest && ruff check . && ruff format --check .`

## Onde está o quê
- Consulta rápida de documentos: `docs/indice.jsonl` (um por linha) · mapa: `docs/grafo.md`
- Vocabulário e fluxo: `docs/modelo/linguagem-ubiqua.yaml`, `docs/modelo/fluxo.yaml`
- Modelo: `docs/modelo-domain-studio.md` · mapa de contexto: `docs/modelo/domain_studio.cml`
- Plano e marcos: `docs/plano-de-implementacao.md` · teoria: `docs/guia/`, `docs/ddd-dicionario.md`
