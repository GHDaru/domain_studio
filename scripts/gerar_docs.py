#!/usr/bin/env python3
"""Gera a documentação derivada a partir das fontes únicas e verifica a coerência do grafo.

Fontes (editadas à mão):
  docs/modelo/linguagem-ubiqua.yaml   vocabulário
  docs/modelo/fluxo.yaml              fluxo e dúvidas
  docs/modelo/decisoes-validacao.yaml decisões do especialista (opcional, colado da interface)
  docs/**/*.md com frontmatter        documentos (nós do grafo)

Gerados (nunca editar à mão):
  docs/modelo/linguagem-ubiqua.md     vocabulário legível, já com as decisões aplicadas
  docs/grafo.md                       grafo navegável (Mermaid) de documentos e do domínio
  docs/indice.jsonl                   um documento por linha — o que a IA consulta sem ler tudo
  prototipos/validacao-linguagem.html bloco de dados embutido

Uso:
  python3 scripts/gerar_docs.py          # regenera
  python3 scripts/gerar_docs.py --check  # falha se algo gerado estiver desatualizado ou quebrado
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MODELO = DOCS / "modelo"
PROTOTIPO = ROOT / "prototipos" / "validacao-linguagem.html"

GERADO = "<!-- GERADO por scripts/gerar_docs.py — não edite; edite a fonte e regenere. -->"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)\s]*)?\)")
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def carregar_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}


def aplicar_decisoes(itens: list[dict], decisoes: dict) -> None:
    for item in itens:
        d = (decisoes or {}).get(item["id"])
        if d:
            item["status"] = d.get("status", item.get("status"))
            if d.get("nota"):
                item["nota"] = d["nota"]


def ler_documentos() -> list[dict]:
    docs = []
    for path in sorted(DOCS.rglob("*.md")):
        texto = path.read_text(encoding="utf-8")
        m = FRONT_RE.match(texto)
        meta = yaml.safe_load(m.group(1)) if m else None
        docs.append({"path": path, "meta": meta or {}, "corpo": texto[m.end():] if m else texto})
    return docs


def gerar_glossario(glossario: dict, fluxo: dict) -> str:
    contextos = glossario.get("contextos", {})
    usos: dict[str, list[str]] = {}
    for p in fluxo.get("passos", []):
        for t in p.get("termos", []):
            usos.setdefault(t, []).append(p["id"])
    marca = {"validado": "✅ validado", "ajustar": "✏️ ajustar", "rejeitado": "❌ rejeitado"}
    linhas = [
        "---",
        "id: linguagem-ubiqua",
        "tipo: glossario",
        'titulo: "Linguagem Ubíqua do DomainStudio"',
        'resumo: "Vocabulário do produto, por contexto delimitado, com status de validação."',
        "relacionados: [modelo-domain-studio, aula-01-linguagem-ubiqua-e-fluxo]",
        "---",
        GERADO,
        "",
        "# Linguagem Ubíqua do DomainStudio",
        "",
        "> Fonte: [`linguagem-ubiqua.yaml`](linguagem-ubiqua.yaml) + decisões de validação.",
        "> Status **proposto** = hipótese ainda não confirmada pelo especialista de domínio.",
        "",
    ]
    for ctx_id, ctx_nome in contextos.items():
        termos = [t for t in glossario.get("termos", []) if t["contexto"] == ctx_id]
        if not termos:
            continue
        linhas += [f"## {ctx_nome}", "", "| Termo | Código | Tipo | Definição | Evitar | Passos | Status |",
                   "|---|---|---|---|---|---|---|"]
        for t in termos:
            evitar = ", ".join(t.get("evitar", [])) or "—"
            passos = ", ".join(usos.get(t["id"], [])) or "—"
            status = marca.get(t.get("status"), "proposto")
            if t.get("nota"):
                status += f" — {t['nota']}"
            linhas.append(
                f"| <a id=\"{t['id']}\"></a>**{t['termo']}** | `{t['codigo']}` | {t['tipo']} | "
                f"{t['definicao']} | {evitar} | {passos} | {status} |"
            )
        linhas.append("")
    return "\n".join(linhas)


def mermaid_id(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", s)


def gerar_grafo(docs: list[dict], glossario: dict, fluxo: dict) -> str:
    com_id = [d for d in docs if d["meta"].get("id")]
    ids = {d["meta"]["id"] for d in com_id}
    arestas = set()
    for d in com_id:
        for r in d["meta"].get("relacionados", []) or []:
            if r in ids:
                arestas.add(tuple(sorted((d["meta"]["id"], r))))
    doc_linhas = ["flowchart LR"]
    por_tipo: dict[str, list[dict]] = {}
    for d in com_id:
        por_tipo.setdefault(d["meta"].get("tipo", "doc"), []).append(d)
    for tipo, lista in sorted(por_tipo.items()):
        doc_linhas.append(f"  subgraph {mermaid_id(tipo)}[{tipo}]")
        for d in lista:
            titulo = str(d["meta"].get("titulo", d["meta"]["id"])).replace('"', "'")
            doc_linhas.append(f'    {mermaid_id(d["meta"]["id"])}["{titulo}"]')
        doc_linhas.append("  end")
    for a, b in sorted(arestas):
        doc_linhas.append(f"  {mermaid_id(a)} --- {mermaid_id(b)}")
    for d in com_id:
        rel = d["path"].relative_to(DOCS).as_posix()
        doc_linhas.append(f'  click {mermaid_id(d["meta"]["id"])} "{rel}"')

    dom = ["flowchart LR"]
    contextos = glossario.get("contextos", {})
    for ctx_id, nome in contextos.items():
        dom.append(f'  subgraph ctx_{mermaid_id(ctx_id)}["{nome}"]')
        for t in glossario.get("termos", []):
            if t["contexto"] == ctx_id:
                dom.append(f'    t_{mermaid_id(t["id"])}(["{t["termo"]}"])')
        dom.append("  end")
    anterior = None
    for p in fluxo.get("passos", []):
        dom.append(f'  {p["id"]}["{p["id"]} · {p["nome"]}"]')
        if anterior:
            dom.append(f"  {anterior} ==> {p['id']}")
        anterior = p["id"]
        for t in p.get("termos", []):
            dom.append(f"  {p['id']} -.-> t_{mermaid_id(t)}")

    return "\n".join([
        "---",
        "id: grafo",
        "tipo: indice",
        'titulo: "Grafo da documentação"',
        'resumo: "Mapa navegável dos documentos e do domínio (termos × contextos × fluxo)."',
        "relacionados: [docs-readme]",
        "---",
        GERADO,
        "",
        "# Grafo da documentação",
        "",
        "Gerado a partir do frontmatter de cada documento (`relacionados`) e das fontes em "
        "`docs/modelo/`. Clique num nó para abrir o documento.",
        "",
        "## Documentos",
        "",
        "```mermaid",
        *doc_linhas,
        "```",
        "",
        "## Domínio — termos por contexto e o fluxo que os usa",
        "",
        "```mermaid",
        *dom,
        "```",
        "",
    ])


def gerar_indice(docs: list[dict]) -> str:
    linhas = []
    for d in docs:
        m = d["meta"]
        if not m.get("id"):
            continue
        linhas.append(json.dumps({
            "id": m["id"],
            "tipo": m.get("tipo"),
            "titulo": m.get("titulo"),
            "resumo": m.get("resumo"),
            "caminho": d["path"].relative_to(ROOT).as_posix(),
            "relacionados": m.get("relacionados", []) or [],
            "termos": m.get("termos", []) or [],
        }, ensure_ascii=False))
    return "\n".join(linhas) + "\n"


def extrair_especificacao() -> str:
    texto = (DOCS / "modelo-domain-studio.md").read_text(encoding="utf-8")
    m = re.search(r"^## 1\..*?\n(.*?)\n---", texto, re.S | re.M)
    bloco = m.group(1) if m else ""
    linhas = [ln[1:].lstrip() if ln.startswith(">") else ln for ln in bloco.strip().splitlines()]
    return re.sub(r"\*\*(.+?)\*\*", r"\1", "\n".join(linhas)).strip()


def gerar_prototipo(glossario: dict, fluxo: dict) -> str:
    html = PROTOTIPO.read_text(encoding="utf-8")
    dados = {
        "projeto": "DomainStudio",
        "versao": fluxo.get("versao", 1),
        "contextos": glossario.get("contextos", {}),
        "termos": glossario.get("termos", []),
        "passos": fluxo.get("passos", []),
        "duvidas": fluxo.get("duvidas", []),
        "especificacao": extrair_especificacao(),
    }
    blob = json.dumps(dados, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return re.sub(
        r'(<script type="application/json" id="dados">).*?(</script>)',
        lambda m: m.group(1) + blob + m.group(2),
        html,
        flags=re.S,
    )


def verificar(docs: list[dict], glossario: dict, fluxo: dict) -> list[str]:
    erros = []
    ids: dict[str, Path] = {}
    termos = {t["id"] for t in glossario.get("termos", [])}
    for d in docs:
        m = d["meta"]
        rel = d["path"].relative_to(ROOT)
        if not m.get("id"):
            erros.append(f"{rel}: sem frontmatter com `id`")
            continue
        if m["id"] in ids:
            erros.append(f"{rel}: id duplicado `{m['id']}` (também em {ids[m['id']]})")
        ids[m["id"]] = rel
    for d in docs:
        m = d["meta"]
        rel = d["path"].relative_to(ROOT)
        for r in m.get("relacionados", []) or []:
            if r not in ids:
                erros.append(f"{rel}: relacionado inexistente `{r}`")
        for t in m.get("termos", []) or []:
            if t not in termos:
                erros.append(f"{rel}: termo inexistente `{t}`")
        for alvo, _ancora in LINK_RE.findall(d["corpo"]):
            if re.match(r"^[a-z]+:", alvo):
                continue
            if not (d["path"].parent / alvo).resolve().exists():
                erros.append(f"{rel}: link quebrado `{alvo}`")
    for p in fluxo.get("passos", []):
        for t in p.get("termos", []):
            if t not in termos:
                erros.append(f"fluxo.yaml {p['id']}: termo inexistente `{t}`")
    return erros


def main() -> int:
    check = "--check" in sys.argv
    glossario = carregar_yaml(MODELO / "linguagem-ubiqua.yaml")
    fluxo = carregar_yaml(MODELO / "fluxo.yaml")
    decisoes = carregar_yaml(MODELO / "decisoes-validacao.yaml")
    aplicar_decisoes(glossario.get("termos", []), decisoes.get("termos"))
    aplicar_decisoes(fluxo.get("passos", []), decisoes.get("passos"))

    saidas = {MODELO / "linguagem-ubiqua.md": gerar_glossario(glossario, fluxo)}
    # o glossário gerado também é nó do grafo: escreva-o antes de ler os documentos
    if not check:
        for path, conteudo in saidas.items():
            path.write_text(conteudo, encoding="utf-8")
    docs = ler_documentos()
    saidas[DOCS / "grafo.md"] = gerar_grafo(docs, glossario, fluxo)
    saidas[DOCS / "indice.jsonl"] = gerar_indice(docs)
    saidas[PROTOTIPO] = gerar_prototipo(glossario, fluxo)

    erros = verificar(docs, glossario, fluxo)
    for path, conteudo in saidas.items():
        atual = path.read_text(encoding="utf-8") if path.exists() else None
        if check and atual != conteudo:
            erros.append(f"{path.relative_to(ROOT)}: desatualizado — rode scripts/gerar_docs.py")
        elif not check and atual != conteudo:
            path.write_text(conteudo, encoding="utf-8")
            print(f"gerado: {path.relative_to(ROOT)}")

    for e in erros:
        print(f"✗ {e}", file=sys.stderr)
    if erros:
        return 1
    print(f"✓ {len(docs)} documentos, {len(glossario.get('termos', []))} termos, "
          f"{len(fluxo.get('passos', []))} passos — grafo coerente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
