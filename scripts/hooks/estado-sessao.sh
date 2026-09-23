#!/usr/bin/env bash
# Hook SessionStart: carrega o ESTADO MEDIDO do método em vez de deixar a IA lembrar.
# A saída deste script entra no contexto do agente. Nunca falha a sessão (sempre exit 0).
# Inspirado em GHDaru/maestro scripts/hooks/session-state.sh (memória relata intenção, não fato).
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" 2>/dev/null || exit 0

echo "── DomainStudio: estado medido no início da sessão ──"
branch="$(git symbolic-ref --short -q HEAD 2>/dev/null || echo '(sem branch)')"
dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
echo "  branch: ${branch} · arquivos não commitados: ${dirty}"

python3 - <<'PY' 2>/dev/null || echo "  (não foi possível ler docs/modelo/*.yaml — PyYAML instalado?)"
import yaml, pathlib
m = pathlib.Path("docs/modelo")
g = yaml.safe_load((m / "linguagem-ubiqua.yaml").read_text())
f = yaml.safe_load((m / "fluxo.yaml").read_text())
dec_path = m / "decisoes-validacao.yaml"
dec = yaml.safe_load(dec_path.read_text()) if dec_path.exists() else {}
dec = dec or {}
def status(item, kind):
    return ((dec.get(kind) or {}).get(item["id"]) or {}).get("status", item.get("status", "proposto"))
termos = g.get("termos", [])
passos = f.get("passos", [])
tp = [t["codigo"] for t in termos if status(t, "termos") == "proposto"]
pp = [p["id"] for p in passos if status(p, "passos") == "proposto"]
respondidas = set((dec.get("duvidas") or {}).keys())
abertas = [d["id"] for d in f.get("duvidas", []) if d["id"] not in respondidas]
print(f"  linguagem: {len(termos) - len(tp)}/{len(termos)} termos decididos · proposto: {', '.join(tp) or 'nenhum'}")
print(f"  fluxo: {len(passos) - len(pp)}/{len(passos)} passos decididos · dúvidas abertas: {', '.join(abertas) or 'nenhuma'}")
if tp or pp or abertas:
    print("  → etapa 1 (validação) em aberto: prototipos/validacao-linguagem.html · docs/guia/01-linguagem-ubiqua-e-fluxo.md")
PY

if out="$(python3 scripts/gerar_docs.py --check 2>&1)"; then
  echo "  documentação: coerente (gerar_docs --check verde)"
else
  echo "  documentação: VERMELHA — $(grep -m1 '✗' <<<"$out")"
fi
exit 0
