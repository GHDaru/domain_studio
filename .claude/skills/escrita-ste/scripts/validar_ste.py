#!/usr/bin/env python3
"""Validador heurístico de escrita no estilo STE (ASD-STE100 adaptado ao português).

Lê um arquivo Markdown ou texto puro e aponta frases que violam as regras
mecânicas do estilo: tamanho de frase, voz passiva, gerúndio, passos que não
começam com um comando, termos vagos e termos proibidos pelo glossário.

O script só vê a forma do texto. Ele não sabe se o sentido foi preservado nem
se um trecho deveria ou não estar em STE: essa parte é do revisor.

Uso:
    validar_ste.py ARQUIVO [--linhas 3-20,31-40] [--glossario GLOSSARIO]
                           [--json] [--estrito]

Código de saída: 0 sem erros, 1 com erros (ou com avisos, se --estrito), 2 uso inválido.
Sem dependências além da biblioteca padrão.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

LIMITE_PROCEDIMENTO = 20
LIMITE_DESCRITIVO = 25
LIMITE_PARAGRAFO = 6

PONTO = "․"  # substitui pontos que não encerram frase

ABREVIATURAS = [
    "p. ex.", "p.ex.", "ex.", "etc.", "sr.", "sra.", "dr.", "dra.", "art.",
    "obs.", "i.e.", "e.g.", "n.", "nº.", "pág.", "cap.", "vs.",
]

AUX_PASSIVA = (
    r"(?:é|são|foi|foram|era|eram|será|serão|seja|sejam|fosse|fossem|"
    r"ser|sendo|sido)"
)
ADVERBIOS = r"(?:não|sempre|também|já|apenas|só|nunca|ainda)"
PARTICIPIO = (
    r"(?:\w+(?:ad|id)[oa]s?|feit[oa]s?|dit[oa]s?|escrit[oa]s?|vist[oa]s?|"
    r"post[oa]s?|abert[oa]s?|cobert[oa]s?|entregues?|aceit[oa]s?|pag[oa]s?|"
    r"salv[oa]s?|gast[oa]s?)"
)
RE_PASSIVA = re.compile(
    rf"\b{AUX_PASSIVA}\s+(?:{ADVERBIOS}\s+)?({PARTICIPIO})\b", re.IGNORECASE
)
# Substantivos e adjetivos que terminam como particípio.
NAO_PARTICIPIO = {
    "resultado", "resultados", "estado", "estados", "significado", "mercado",
    "lado", "passado", "cuidado", "pedido", "pedidos", "sentido", "partido",
    "advogado", "empregado", "feriado", "sábado", "dado", "dados", "obrigado",
    "obrigada", "rápido", "rápida", "válido", "válida", "inválido", "inválida",
    "sólido", "líquido", "tecido", "ouvido", "marido", "vestido", "ruído",
    "conteúdo", "delegado", "privado", "privada", "adequado", "adequada",
    "complicado", "complicada", "limitado", "limitada",
}

RE_PASSIVA_SE = re.compile(r"\b\w{3,}(?:a|e|am|em)-se\b", re.IGNORECASE)

RE_GERUNDIO = re.compile(r"\b\w{2,}(?:ando|endo|indo)\b", re.IGNORECASE)
NAO_GERUNDIO = {
    "quando", "comando", "comandos", "bando", "brando", "memorando",
    "contrabando", "doutorando", "mestrando", "graduando", "dividendo",
    "dividendos", "adendo", "horrendo", "tremendo", "estupendo", "reverendo",
    "remendo", "lindo", "infindo", "bem-vindo", "vindo", "segundo",
}

RE_SEQUENCIA = re.compile(
    r"\b(?:e depois|e então|e em seguida|em seguida|depois disso|"
    r"logo após|e por fim|e, por fim|e finalmente)\b",
    re.IGNORECASE,
)

RE_CONDICAO_NO_FIM = re.compile(
    r",\s*(?:se|caso|quando|desde que|a menos que)\s", re.IGNORECASE
)
RE_COMECA_COM_CONDICAO = re.compile(
    r"^\W*(?:se|caso|quando|antes|depois|após|para|ao|enquanto|durante)\b",
    re.IGNORECASE,
)

TERMOS_VAGOS = [
    "basta", "simplesmente", "obviamente", "claramente", "etc", "e/ou",
    "se necessário", "se for o caso", "quando possível", "se possível",
    "em geral", "normalmente", "eventualmente", "de alguma forma",
    "adequadamente", "apropriadamente", "devidamente", "entre outros",
    "e assim por diante", "na medida do possível",
]
RE_VAGOS = re.compile(
    r"(?<![\w/])(" + "|".join(re.escape(t) for t in TERMOS_VAGOS) + r")(?![\w/])",
    re.IGNORECASE,
)

RE_ABERTURA_INDIRETA = re.compile(
    r"^\W*(?:você deve|você precisa|você pode|deve-se|devem-se|é necessário|"
    r"é preciso|é importante|é recomendável|recomenda-se|deve|devem|precisa)\b",
    re.IGNORECASE,
)
RE_INFINITIVO = re.compile(r"^\W*(\w{4,}(?:ar|er|ir|por|pôr))\b", re.IGNORECASE)
NAO_INFINITIVO = {
    "qualquer", "quaisquer", "maior", "menor", "melhor", "pior", "valor",
    "favor", "anterior", "posterior", "superior", "inferior", "interior",
    "exterior", "servidor", "usuário", "lugar", "apesar", "mulher", "talher",
    "caráter", "líder", "poder", "dever", "prazer",
}

RE_ITEM_NUMERADO = re.compile(r"^(\s*)(\d+[.)])\s+")
RE_ITEM_MARCADOR = re.compile(r"^(\s*)([-*+])\s+")
RE_AVISO = re.compile(
    r"^\W*(?:atenção|cuidado|aviso|importante|perigo|nota)\b\W*", re.IGNORECASE
)
RE_CODIGO_INLINE = re.compile(r"`[^`\n]+`")
RE_URL = re.compile(r"https?://\S+")
RE_LINK_MD = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")
RE_PLACEHOLDER = re.compile(r"\{\{[^}\n]+\}\}|\{[A-Za-z_][\w.]*\}|<[A-Za-z_/][^>\n]*>")
RE_FIM_DE_FRASE = re.compile(r"(?<=[.!?])[\"”')\]*_]*\s+")


@dataclass
class Achado:
    linha: int
    regra: str
    nivel: str  # "erro" ou "aviso"
    mensagem: str
    trecho: str


@dataclass
class Bloco:
    linha: int
    texto: str
    tipo: str  # "procedimento" ou "descritivo"
    lista: bool


def ler_blocos(linhas: list[str]) -> list[Bloco]:
    """Agrupa o arquivo em parágrafos e itens de lista, pulando o que não é prosa."""
    blocos: list[Bloco] = []
    atual: list[str] = []
    inicio = 0
    tipo = "descritivo"
    lista = False
    em_cerca = False
    em_comentario = False

    def fechar() -> None:
        nonlocal atual
        if atual:
            blocos.append(Bloco(inicio, "\n".join(atual), tipo, lista))
            atual = []

    for numero, bruta in enumerate(linhas, start=1):
        linha = bruta.rstrip("\n")
        limpa = linha.strip()

        if em_cerca:
            if limpa.startswith("```") or limpa.startswith("~~~"):
                em_cerca = False
            continue
        if limpa.startswith("```") or limpa.startswith("~~~"):
            fechar()
            em_cerca = True
            continue
        if em_comentario:
            if "-->" in limpa:
                em_comentario = False
            continue
        if limpa.startswith("<!--"):
            fechar()
            em_comentario = "-->" not in limpa
            continue
        # Linhas que não são prosa: vazias, títulos, tabelas, réguas, tags soltas.
        if (
            not limpa
            or limpa.startswith("#")
            or limpa.startswith("|")
            or re.fullmatch(r"[-*_=]{3,}", limpa)
            or re.fullmatch(r"</?[A-Za-z_][^>]*>", limpa)
        ):
            fechar()
            continue

        numerado = RE_ITEM_NUMERADO.match(linha)
        marcador = RE_ITEM_MARCADOR.match(linha)
        if numerado or marcador:
            fechar()
            achado = numerado or marcador
            inicio = numero
            lista = True
            tipo = "procedimento" if numerado else "descritivo"
            atual = [" " * achado.end() + linha[achado.end():]]
            continue

        if limpa.startswith(">"):
            linha = re.sub(r"^\s*>+\s?", "", linha)
            limpa = linha.strip()

        if not atual:
            inicio = numero
            lista = False
            tipo = "procedimento" if RE_AVISO.match(re.sub(r"[*_]", "", limpa)) else "descritivo"
        atual.append(linha)

    fechar()
    return blocos


def proteger(texto: str) -> str:
    """Troca por marcadores o que não deve ser contado nem quebrado como frase."""
    texto = RE_CODIGO_INLINE.sub("CODIGO", texto)
    texto = RE_LINK_MD.sub(lambda m: m.group(1), texto)
    texto = RE_URL.sub("URL", texto)
    texto = RE_PLACEHOLDER.sub("VARIAVEL", texto)
    for abreviatura in ABREVIATURAS:
        texto = re.sub(
            r"(?<!\w)" + re.escape(abreviatura),
            lambda m: m.group(0).replace(".", PONTO),
            texto,
            flags=re.IGNORECASE,
        )
    texto = re.sub(r"(?<=\d)\.(?=\d)", PONTO, texto)
    return texto


def frases_do_bloco(bloco: Bloco) -> list[tuple[int, str]]:
    texto = proteger(bloco.texto)
    frases: list[tuple[int, str]] = []
    posicao = 0
    cortes = [m.end() for m in RE_FIM_DE_FRASE.finditer(texto)] + [len(texto)]
    for corte in cortes:
        pedaco = texto[posicao:corte]
        if pedaco.strip():
            recuo = len(pedaco) - len(pedaco.lstrip())
            linha = bloco.linha + texto[: posicao + recuo].count("\n")
            frases.append((linha, " ".join(pedaco.split()).replace(PONTO, ".")))
        posicao = corte
    return frases


def contar_palavras(frase: str) -> int:
    return sum(1 for token in frase.split() if re.search(r"\w", token))


def sem_enfase(frase: str) -> str:
    return re.sub(r"[*_]{1,3}", "", frase)


def resumir(frase: str, limite: int = 90) -> str:
    return frase if len(frase) <= limite else frase[: limite - 1].rstrip() + "…"


def carregar_glossario(caminho: str) -> list[tuple[str, re.Pattern[str]]]:
    """Formato por linha: `termo preferido: sinônimo proibido, outro sinônimo`."""
    regras: list[tuple[str, re.Pattern[str]]] = []
    with open(caminho, encoding="utf-8") as arquivo:
        for bruta in arquivo:
            linha = bruta.split("#", 1)[0].strip()
            if not linha or ":" not in linha:
                continue
            preferido, proibidos = linha.split(":", 1)
            termos = [t.strip() for t in proibidos.split(",") if t.strip()]
            if not termos:
                continue
            padrao = re.compile(
                r"(?<!\w)(" + "|".join(re.escape(t) for t in termos) + r")(?!\w)",
                re.IGNORECASE,
            )
            regras.append((preferido.strip(), padrao))
    return regras


def analisar(blocos: list[Bloco], glossario) -> tuple[list[Achado], int]:
    achados: list[Achado] = []
    total = 0

    for bloco in blocos:
        frases = frases_do_bloco(bloco)
        total += len(frases)
        limite = LIMITE_PROCEDIMENTO if bloco.tipo == "procedimento" else LIMITE_DESCRITIVO

        if not bloco.lista and len(frases) > LIMITE_PARAGRAFO:
            achados.append(Achado(
                bloco.linha, "STE-02", "aviso",
                f"parágrafo com {len(frases)} frases (máximo {LIMITE_PARAGRAFO}); divida por assunto",
                resumir(frases[0][1]),
            ))

        for indice, (linha, bruta) in enumerate(frases):
            frase = sem_enfase(bruta)
            trecho = resumir(frase)

            palavras = contar_palavras(frase)
            if palavras > limite:
                achados.append(Achado(
                    linha, "STE-01", "erro",
                    f"frase com {palavras} palavras (máximo {limite} em trecho {bloco.tipo})",
                    trecho,
                ))

            for passiva in RE_PASSIVA.finditer(frase):
                if passiva.group(1).lower() in NAO_PARTICIPIO:
                    continue
                achados.append(Achado(
                    linha, "STE-03",
                    "erro" if bloco.tipo == "procedimento" else "aviso",
                    f"voz passiva em \"{passiva.group(0)}\"; diga quem faz a ação",
                    trecho,
                ))
            for passiva in RE_PASSIVA_SE.finditer(frase):
                achados.append(Achado(
                    linha, "STE-03", "aviso",
                    f"sujeito indeterminado em \"{passiva.group(0)}\"; diga quem faz a ação",
                    trecho,
                ))

            for gerundio in RE_GERUNDIO.finditer(frase):
                if gerundio.group(0).lower() in NAO_GERUNDIO:
                    continue
                achados.append(Achado(
                    linha, "STE-04", "aviso",
                    f"gerúndio \"{gerundio.group(0)}\"; use verbo conjugado em frase própria",
                    trecho,
                ))

            if bloco.tipo == "procedimento":
                sequencia = RE_SEQUENCIA.search(frase)
                if sequencia:
                    achados.append(Achado(
                        linha, "STE-05", "erro",
                        f"mais de uma ação na frase (\"{sequencia.group(0)}\"); use uma frase por ação",
                        trecho,
                    ))
                if RE_CONDICAO_NO_FIM.search(frase) and not RE_COMECA_COM_CONDICAO.match(frase):
                    achados.append(Achado(
                        linha, "STE-06", "aviso",
                        "condição depois do comando; escreva a condição primeiro",
                        trecho,
                    ))

            if bloco.tipo == "procedimento" and bloco.lista and indice == 0:
                indireta = RE_ABERTURA_INDIRETA.match(frase)
                infinitivo = RE_INFINITIVO.match(frase)
                if indireta:
                    achados.append(Achado(
                        linha, "STE-07", "erro",
                        f"passo começa com \"{indireta.group(0).strip()}\"; comece com o verbo no imperativo",
                        trecho,
                    ))
                elif infinitivo and infinitivo.group(1).lower() not in NAO_INFINITIVO:
                    achados.append(Achado(
                        linha, "STE-07", "aviso",
                        f"passo começa com infinitivo \"{infinitivo.group(1)}\"; use o imperativo",
                        trecho,
                    ))

            for vago in RE_VAGOS.finditer(frase):
                achados.append(Achado(
                    linha, "STE-08", "aviso",
                    f"termo vago \"{vago.group(0)}\"; diga a condição ou o valor exato",
                    trecho,
                ))

            for preferido, padrao in glossario:
                for proibido in padrao.finditer(frase):
                    achados.append(Achado(
                        linha, "STE-09", "erro",
                        f"termo \"{proibido.group(0)}\" fora do glossário; use \"{preferido}\"",
                        trecho,
                    ))

    return achados, total


def ler_faixas(texto: str) -> list[tuple[int, int]]:
    faixas = []
    for parte in texto.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            inicio, fim = parte.split("-", 1)
            faixas.append((int(inicio), int(fim)))
        else:
            faixas.append((int(parte), int(parte)))
    return faixas


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida escrita no estilo STE (ASD-STE100 adaptado ao português)."
    )
    parser.add_argument("arquivo", help="arquivo Markdown ou texto; use - para a entrada padrão")
    parser.add_argument("--linhas", help="faixas a validar, por exemplo 3-20,31-40")
    parser.add_argument("--glossario", help="arquivo com linhas `preferido: proibido, proibido`")
    parser.add_argument("--json", action="store_true", help="saída em JSON")
    parser.add_argument("--estrito", action="store_true", help="avisos também reprovam")
    args = parser.parse_args()

    try:
        if args.arquivo == "-":
            linhas = sys.stdin.read().splitlines()
        else:
            with open(args.arquivo, encoding="utf-8") as arquivo:
                linhas = arquivo.read().splitlines()
        glossario = carregar_glossario(args.glossario) if args.glossario else []
        faixas = ler_faixas(args.linhas) if args.linhas else []
    except (OSError, ValueError) as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2

    blocos = ler_blocos(linhas)
    if faixas:
        blocos = [
            b for b in blocos
            if any(inicio <= b.linha + b.texto.count("\n") and b.linha <= fim
                   for inicio, fim in faixas)
        ]
    achados, total = analisar(blocos, glossario)
    if faixas:
        achados = [
            a for a in achados
            if any(inicio <= a.linha <= fim for inicio, fim in faixas)
        ]
    achados.sort(key=lambda a: (a.linha, a.regra))

    erros = sum(1 for a in achados if a.nivel == "erro")
    avisos = len(achados) - erros
    reprovado = erros > 0 or (args.estrito and avisos > 0)

    if args.json:
        print(json.dumps({
            "arquivo": args.arquivo,
            "frases": total,
            "erros": erros,
            "avisos": avisos,
            "aprovado": not reprovado,
            "achados": [asdict(a) for a in achados],
        }, ensure_ascii=False, indent=2))
    else:
        for a in achados:
            print(f"{args.arquivo}:{a.linha}: [{a.regra}] {a.nivel}: {a.mensagem}")
            print(f"    {a.trecho}")
        print(
            f"\n{total} frases analisadas, {erros} erro(s), {avisos} aviso(s): "
            + ("REPROVADO" if reprovado else "APROVADO")
        )
    return 1 if reprovado else 0


if __name__ == "__main__":
    sys.exit(main())
