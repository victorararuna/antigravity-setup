#!/usr/bin/env python3
"""Consulta o acervo de legislação brasileira em Markdown (repositório ctresb/leis).

Sem dependências externas: só stdlib (sqlite3 com FTS5).

    python consultar.py status
    python consultar.py indexar [--forcar]
    python consultar.py buscar --numero 10406 --ano 2002 [--json]
    python consultar.py buscar --texto "guarda compartilhada"
    python consultar.py buscar --conteudo "alienação parental" --tipo lei
    python consultar.py abrir --numero 10406 --ano 2002 [--trecho N | --termo T --contexto K]
    python consultar.py citar --numero 10406 --ano 2002

O acervo é resolvido nesta ordem: --acervo, $DSH_LEIS_ACERVO, ./leis.
O índice fica em <acervo>/.consultar-leis/indice.sqlite3 (ou $DSH_LEIS_INDICE).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

ESFERAS = ("federal", "estaduais", "reguladores", "jurisprudencia", "tratados", "municipais")
ARQUIVO_RAIZ = "constituicao.md"
IGNORAR_DIR = {
    ".git", ".consultar-leis", "_fonte", "_indice", "scripts", "assets", "fonte",
    "node_modules", "__pycache__",
}

CAMPOS = (
    "titulo", "tipo", "numero", "data", "ano", "uf", "ementa", "situacao",
    "revogada", "versao_texto", "publicacao", "data_publicacao", "urn", "fonte",
)

MESES = (
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
)


# --------------------------------------------------------------------------- #
# frontmatter
# --------------------------------------------------------------------------- #

def _limpar(valor: str) -> str:
    v = valor.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def ler_frontmatter(texto: str) -> tuple[dict[str, str], str]:
    """Parser do YAML plano usado pelo acervo: `chave: valor`, sem listas aninhadas."""
    if not texto.startswith("---"):
        return {}, texto
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}, texto
    bloco = texto[texto.find("\n", 3) + 1 : fim]
    corpo = texto[fim + 4 :].lstrip("\r\n")
    meta: dict[str, str] = {}
    for linha in bloco.splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        chave, sep, valor = linha.partition(":")
        if not sep:
            continue
        meta[chave.strip()] = _limpar(valor.split(" #")[0] if " #" in valor else valor)
    return meta, corpo


def sem_acento(valor: str) -> str:
    n = unicodedata.normalize("NFKD", valor or "")
    return "".join(c for c in n if not unicodedata.combining(c))


def norm_tipo(valor: str) -> str:
    v = sem_acento(valor or "").lower()
    v = re.sub(r"[^a-z0-9]+", "-", v).strip("-")
    return v


ALIASES = {
    "lei": "lei-ordinaria",
    "lo": "lei-ordinaria",
    "lc": "lei-complementar",
    "lcp": "lei-complementar",
    "dec": "decreto",
    "dl": "decreto-lei",
    "cf": "constituicao",
    "constituicao-federal": "constituicao",
    "ec": "emenda-constitucional",
    "mp": "medida-provisoria",
    "sv": "sumula-vinculante",
    "sumula": "sumula",
}


def canon_tipo(valor: str) -> str:
    v = norm_tipo(valor)
    return ALIASES.get(v, v)


def esfera_de(rel: str) -> str:
    topo = rel.split("/", 1)[0]
    if topo == ARQUIVO_RAIZ:
        return "constituicao"
    return topo if topo in ESFERAS else "fora-do-plano"


def bool_meta(valor: str) -> int | None:
    v = (valor or "").strip().lower()
    if v in ("true", "sim", "1", "yes"):
        return 1
    if v in ("false", "nao", "não", "0", "no"):
        return 0
    return None


def ano_de(meta: dict[str, str], rel: str) -> str:
    if meta.get("ano"):
        return meta["ano"]
    data = meta.get("data", "")
    if re.match(r"^\d{4}-\d{2}-\d{2}$", data):
        return data[:4]
    m = re.search(r"/(\d{4})/", "/" + rel)
    return m.group(1) if m else ""


# --------------------------------------------------------------------------- #
# acervo e índice
# --------------------------------------------------------------------------- #

def resolver_acervo(explicito: str | None) -> Path:
    candidatos = []
    if explicito:
        candidatos.append(Path(explicito))
    if os.environ.get("DSH_LEIS_ACERVO"):
        candidatos.append(Path(os.environ["DSH_LEIS_ACERVO"]))
    candidatos.append(Path("leis"))
    for c in candidatos:
        if c.is_dir():
            return c.resolve()
    raise SystemExit(
        "acervo não encontrado. Passe --acervo <pasta> ou defina DSH_LEIS_ACERVO.\n"
        "Clone parcial sugerido:\n"
        "  git clone --filter=blob:none --sparse https://github.com/ctresb/leis.git leis\n"
        "  cd leis && git sparse-checkout set federal estaduais"
    )


def caminho_indice(acervo: Path, explicito: str | None) -> Path:
    if explicito:
        p = Path(explicito)
    elif os.environ.get("DSH_LEIS_INDICE"):
        p = Path(os.environ["DSH_LEIS_INDICE"])
    else:
        p = acervo / ".consultar-leis" / "indice.sqlite3"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


SCHEMA = """
CREATE TABLE IF NOT EXISTS normas (
    id           INTEGER PRIMARY KEY,
    caminho      TEXT NOT NULL UNIQUE,
    esfera       TEXT,
    uf           TEXT,
    tipo         TEXT,
    tipo_norm    TEXT,
    numero       TEXT,
    ano          TEXT,
    data         TEXT,
    titulo       TEXT,
    ementa       TEXT,
    situacao     TEXT,
    revogada     INTEGER,
    versao_texto TEXT,
    urn          TEXT,
    fonte        TEXT,
    mtime        REAL,
    tamanho      INTEGER,
    publicacao   TEXT,
    data_publicacao TEXT
);
CREATE INDEX IF NOT EXISTS ix_normas_numero ON normas(numero, ano);
CREATE INDEX IF NOT EXISTS ix_normas_tipo   ON normas(tipo_norm, ano);
CREATE INDEX IF NOT EXISTS ix_normas_uf     ON normas(uf, ano);
CREATE INDEX IF NOT EXISTS ix_normas_urn    ON normas(urn);
CREATE VIRTUAL TABLE IF NOT EXISTS normas_fts USING fts5(titulo, ementa, numero);
"""


def conectar(db: Path) -> sqlite3.Connection:
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    return con


def iter_md(acervo: Path):
    raiz_constituicao = acervo / ARQUIVO_RAIZ
    if raiz_constituicao.is_file():
        yield raiz_constituicao
    for esfera in ESFERAS:
        base = acervo / esfera
        if not base.is_dir():
            continue
        pilha = [base]
        while pilha:
            atual = pilha.pop()
            try:
                with os.scandir(atual) as it:
                    for e in it:
                        if e.is_dir(follow_symlinks=False):
                            if e.name not in IGNORAR_DIR and not e.name.startswith("."):
                                pilha.append(Path(e.path))
                        elif e.name.endswith(".md"):
                            yield Path(e.path)
            except OSError:
                continue


def cmd_indexar(args) -> int:
    acervo = resolver_acervo(args.acervo)
    db = caminho_indice(acervo, args.db)
    if args.forcar and db.exists():
        db.unlink()
    con = conectar(db)
    existentes = {
        r["caminho"]: (r["mtime"], r["tamanho"])
        for r in con.execute("SELECT caminho, mtime, tamanho FROM normas")
    }
    novos = atualizados = inalterados = ilegiveis = 0
    lote = []
    vistos = 0

    for arquivo in iter_md(acervo):
        vistos += 1
        if vistos % 20000 == 0:
            print(f"  ... {vistos} arquivos varridos, {novos + atualizados} gravados", file=sys.stderr)
        try:
            st = arquivo.stat()
            rel = arquivo.relative_to(acervo).as_posix()
            anterior = existentes.get(rel)
            if anterior and abs(anterior[0] - st.st_mtime) < 1e-6 and anterior[1] == st.st_size:
                inalterados += 1
                continue
            texto = arquivo.read_text(encoding="utf-8", errors="replace")
        except OSError:
            ilegiveis += 1
            continue
        meta, _ = ler_frontmatter(texto)
        tipo = meta.get("tipo", "")
        lote.append((
            rel, esfera_de(rel), (meta.get("uf") or "").upper(), tipo, canon_tipo(tipo),
            meta.get("numero", ""), ano_de(meta, rel), meta.get("data", ""),
            meta.get("titulo", ""), meta.get("ementa", ""), meta.get("situacao", ""),
            bool_meta(meta.get("revogada", "")), meta.get("versao_texto", ""),
            meta.get("urn", ""), meta.get("fonte", ""), st.st_mtime, st.st_size,
            meta.get("publicacao", ""), meta.get("data_publicacao", ""),
        ))
        if len(lote) >= 2000:
            novos, atualizados = _gravar(con, lote, existentes, novos, atualizados)
            lote.clear()
    novos, atualizados = _gravar(con, lote, existentes, novos, atualizados)
    con.commit()
    _reconstruir_fts(con)

    total = con.execute("SELECT count(*) FROM normas").fetchone()[0]
    print(
        f"índice: {total} normas ({novos} novas, {atualizados} atualizadas, "
        f"{inalterados} inalteradas, {ilegiveis} ilegíveis)"
    )
    print(f"acervo: {acervo}")
    print(f"banco:  {db}  ({db.stat().st_size / 1e6:.1f} MB)")
    con.close()
    return 0


def _gravar(con, lote, existentes, novos, atualizados):
    for row in lote:
        cur = con.execute(
            """INSERT INTO normas
               (caminho, esfera, uf, tipo, tipo_norm, numero, ano, data, titulo, ementa,
                situacao, revogada, versao_texto, urn, fonte, mtime, tamanho,
                publicacao, data_publicacao)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(caminho) DO UPDATE SET
                 esfera=excluded.esfera, uf=excluded.uf, tipo=excluded.tipo,
                 tipo_norm=excluded.tipo_norm, numero=excluded.numero, ano=excluded.ano,
                 data=excluded.data, titulo=excluded.titulo, ementa=excluded.ementa,
                 situacao=excluded.situacao, revogada=excluded.revogada,
                 versao_texto=excluded.versao_texto, urn=excluded.urn, fonte=excluded.fonte,
                 mtime=excluded.mtime, tamanho=excluded.tamanho,
                 publicacao=excluded.publicacao, data_publicacao=excluded.data_publicacao""",
            row,
        )
        if row[0] in existentes:
            atualizados += 1
        else:
            novos += 1
    return novos, atualizados


def _reconstruir_fts(con) -> int:
    """Reconstrói o índice textual em duas instruções, em vez de manter por arquivo.

    Manter o FTS linha a linha (DELETE + INSERT por norma) dominava o custo da indexação:
    ~50 arquivos/s. Em bloco, os mesmos 264 mil arquivos indexam em minutos.
    """
    con.execute("DELETE FROM normas_fts")
    con.execute(
        "INSERT INTO normas_fts(rowid, titulo, ementa, numero) "
        "SELECT id, titulo, ementa, numero FROM normas"
    )
    con.commit()
    return con.execute("SELECT count(*) FROM normas_fts").fetchone()[0]


# --------------------------------------------------------------------------- #
# busca
# --------------------------------------------------------------------------- #

def filtros(args) -> tuple[str, list]:
    where, params = [], []
    if getattr(args, "numero", None):
        where.append("numero = ?")
        params.append(re.sub(r"\D", "", args.numero))
    if getattr(args, "ano", None):
        where.append("ano = ?")
        params.append(str(args.ano))
    if getattr(args, "tipo", None):
        where.append("tipo_norm = ?")
        params.append(canon_tipo(args.tipo))
    if getattr(args, "uf", None):
        where.append("uf = ?")
        params.append(args.uf.upper())
    if getattr(args, "esfera", None):
        where.append("esfera = ?")
        params.append(args.esfera)
    if getattr(args, "vigente", False):
        where.append("(revogada IS NULL OR revogada = 0)")
    if getattr(args, "revogada", False):
        where.append("revogada = 1")
    return (" AND ".join(where) if where else "1=1"), params


def select(args) -> list[sqlite3.Row]:
    acervo = resolver_acervo(args.acervo)
    db = caminho_indice(acervo, args.db)
    if not db.exists():
        raise SystemExit("índice ausente. Rode: python scripts/consultar.py indexar")
    con = conectar(db)
    cond, params = filtros(args)
    limite = args.limite or 20

    if getattr(args, "texto", None):
        termo = '"' + args.texto.replace('"', '""') + '"'
        sql = (
            "SELECT n.* FROM normas_fts f JOIN normas n ON n.id = f.rowid "
            f"WHERE normas_fts MATCH ? AND ({cond}) ORDER BY rank LIMIT ?"
        )
        rows = con.execute(sql, [termo, *params, limite]).fetchall()
    else:
        sql = f"SELECT * FROM normas WHERE {cond} ORDER BY ano, numero LIMIT ?"
        rows = con.execute(sql, [*params, limite]).fetchall()
    con.close()
    return rows


def resumo(r: sqlite3.Row) -> str:
    situacao = r["situacao"] or ("revogada" if r["revogada"] == 1 else "")
    partes = " | ".join(x for x in (r["tipo"], f"nº {r['numero']}" if r["numero"] else "",
                                    r["data"], r["uf"], situacao) if x)
    linhas = [f"{r['titulo'] or '(sem título)'}", f"  {partes}", f"  {r['caminho']}"]
    if r["ementa"]:
        linhas.append(f"  ementa: {r['ementa'][:300]}")
    if r["urn"]:
        linhas.append(f"  urn: {r['urn']}")
    return "\n".join(linhas)


def cmd_buscar(args) -> int:
    rows = select(args)
    if args.json:
        print(json.dumps([{k: r[k] for k in r.keys()} for r in rows], ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("nada encontrado com esses filtros.", file=sys.stderr)
        return 1
    for r in rows:
        print(resumo(r))
        if args.conteudo:
            trecho = _buscar_no_corpo(resolver_acervo(args.acervo) / r["caminho"], args.conteudo, 1)
            if trecho:
                print(trecho)
        print()
    if len(rows) == (args.limite or 20):
        print(f"(limite de {len(rows)} atingido; use --limite para ver mais)", file=sys.stderr)
    return 0


def _buscar_no_corpo(arquivo: Path, termo: str, contexto: int) -> str:
    try:
        linhas = arquivo.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    alvo = sem_acento(termo).lower()
    saida = []
    for i, linha in enumerate(linhas):
        if alvo in sem_acento(linha).lower():
            ini, fim = max(0, i - contexto), min(len(linhas), i + contexto + 1)
            saida.append("    " + "\n    ".join(f"{n+1}: {linhas[n]}" for n in range(ini, fim)))
            if len(saida) >= 3:
                break
    return "\n".join(saida)


def cmd_buscar_conteudo(args) -> int:
    """Varre o corpo apenas dos candidatos que passam nos filtros estruturais."""
    acervo = resolver_acervo(args.acervo)
    rows = select(argparse.Namespace(**{**vars(args), "texto": None, "limite": args.limite or 100000}))
    achados = 0
    for r in rows:
        trecho = _buscar_no_corpo(acervo / r["caminho"], args.conteudo, args.contexto)
        if trecho:
            print(resumo(r))
            print(trecho)
            print()
            achados += 1
            if achados >= (args.limite or 20):
                break
    if not achados:
        print("nenhuma ocorrência no corpo dos candidatos filtrados.", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- #
# abrir / citar
# --------------------------------------------------------------------------- #

def resolver_uma(args) -> sqlite3.Row:
    rows = select(argparse.Namespace(**{**vars(args), "texto": getattr(args, "texto", None),
                                       "limite": 5}))
    if not rows:
        raise SystemExit("norma não encontrada com esses filtros.")
    if len(rows) > 1:
        print("mais de uma norma corresponde; refine os filtros:", file=sys.stderr)
        for r in rows:
            print(resumo(r), file=sys.stderr)
        raise SystemExit(2)
    return rows[0]


def cmd_abrir(args) -> int:
    acervo = resolver_acervo(args.acervo)
    r = resolver_uma(args)
    texto = (acervo / r["caminho"]).read_text(encoding="utf-8", errors="replace")
    meta, corpo = ler_frontmatter(texto)

    if args.json:
        print(json.dumps({"meta": meta, "corpo": corpo}, ensure_ascii=False, indent=2))
        return 0

    print(f"# {meta.get('titulo') or r['titulo']}")
    for campo in ("tipo", "numero", "data", "uf", "ementa", "situacao", "versao_texto",
                  "publicacao", "urn", "fonte"):
        if meta.get(campo):
            print(f"{campo:14} {meta[campo]}")
    print(f"{'caminho':14} {r['caminho']}")
    print()

    linhas = corpo.splitlines()
    if args.termo:
        alvo = sem_acento(args.termo).lower()
        for i, linha in enumerate(linhas):
            if alvo in sem_acento(linha).lower():
                ini, fim = max(0, i - args.contexto), min(len(linhas), i + args.contexto + 1)
                print("---")
                for n in range(ini, fim):
                    print(linhas[n])
        return 0
    print("\n".join(linhas[: args.trecho or 120]))
    if args.trecho is None and len(linhas) > 120:
        print(f"\n[... {len(linhas) - 120} linhas; use --trecho 0 para o texto integral]")
    return 0


def _fmt_numero(numero: str) -> str:
    """10406 -> 10.406; 123 -> 123. Só age em números puramente numéricos."""
    if numero.isdigit() and len(numero) >= 4:
        return f"{int(numero):,}".replace(",", ".")
    return numero


def _data_longa(iso: str) -> str:
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except (ValueError, TypeError):
        return iso or ""
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def cmd_citar(args) -> int:
    r = resolver_uma(args)
    uf = r["uf"] or ""
    tipo = r["tipo"] or "Norma"
    numero = _fmt_numero(r["numero"] or "")
    data = _data_longa(r["data"])
    orgao = "Diário Oficial da União: seção 1, Brasília, DF" if not uf else f"Diário Oficial do Estado de {uf}"
    if r["esfera"] == "municipais":
        partes = r["caminho"].split("/")
        if len(partes) > 2:
            orgao = f"Diário Oficial do Município de {partes[2].replace('-', ' ').title()}"

    ref = f"{'BRASIL' if not uf else uf}. {tipo} nº {numero}, de {data}."
    if r["ementa"]:
        ref += f" {r['ementa'].rstrip('.')}."
    if r["publicacao"]:
        ref += f" {r['publicacao']}."
    else:
        ref += f" {orgao}."

    dados = {
        "referencia": ref,
        "urn": r["urn"],
        "fonte": r["fonte"],
        "versao_texto": r["versao_texto"],
        "situacao": r["situacao"],
        "revogada": bool(r["revogada"]) if r["revogada"] is not None else None,
        "data": r["data"],
        "caminho": r["caminho"],
    }
    if args.json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
        return 0
    print(ref)
    for campo in ("urn", "fonte", "versao_texto", "situacao", "caminho"):
        if dados[campo]:
            print(f"{campo:12} {dados[campo]}")
    if dados["revogada"]:
        print(f"{'ATENÇÃO':12} norma marcada como revogada no acervo")
    return 0


def cmd_status(args) -> int:
    acervo = resolver_acervo(args.acervo)
    db = caminho_indice(acervo, args.db)
    print(f"acervo  {acervo}")
    if not db.exists():
        print("índice  ausente (rode: python consultar.py indexar)")
        return 0
    con = conectar(db)
    total = con.execute("SELECT count(*) FROM normas").fetchone()[0]
    tamanho = db.stat().st_size / 1e6
    print(f"índice  {db}  ({tamanho:.1f} MB, {total} normas)")
    print("\npor esfera:")
    for row in con.execute(
        "SELECT esfera, count(*) c, min(ano) de, max(ano) ate FROM normas GROUP BY esfera ORDER BY c DESC"
    ):
        print(f"  {row['esfera'] or '?':16} {row['c']:>8}  {row['de'] or '?'}–{row['ate'] or '?'}")
    print("\npor tipo (top 12):")
    for row in con.execute(
        "SELECT tipo, count(*) c FROM normas GROUP BY tipo ORDER BY c DESC LIMIT 12"
    ):
        print(f"  {(row['tipo'] or '?'):32} {row['c']:>8}")
    n_uf = con.execute("SELECT count(DISTINCT uf) FROM normas WHERE uf <> ''").fetchone()[0]
    print(f"\nUFs distintas: {n_uf}")
    con.close()
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _comuns(p: argparse.ArgumentParser) -> None:
    """Aceita as opções globais também depois do subcomando, sem sobrescrever o valor global."""
    p.add_argument("--acervo", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    p.add_argument("--db", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    p.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help=argparse.SUPPRESS)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Consulta o acervo ctresb/leis.")
    p.add_argument("--acervo", help="pasta do clone (default: $DSH_LEIS_ACERVO ou ./leis)")
    p.add_argument("--db", help="caminho do índice SQLite")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    sub = p.add_subparsers(dest="comando", required=True)

    i = sub.add_parser("indexar", help="constrói/atualiza o índice")
    i.add_argument("--forcar", action="store_true", help="reconstrói do zero")
    _comuns(i)

    s = sub.add_parser("buscar", help="busca por identificação, título/ementa ou corpo")
    _comuns(s)
    s.add_argument("--numero")
    s.add_argument("--ano")
    s.add_argument("--tipo")
    s.add_argument("--uf")
    s.add_argument("--esfera")
    s.add_argument("--texto", help="busca textual em título/ementa/número")
    s.add_argument("--conteudo", help="busca no corpo das normas candidatas")
    s.add_argument("--contexto", type=int, default=1)
    s.add_argument("--vigente", action="store_true")
    s.add_argument("--revogada", action="store_true")
    s.add_argument("--limite", type=int, default=20)

    for nome, ajuda in (("abrir", "abre a norma"), ("citar", "monta a referência")):
        c = sub.add_parser(nome, help=ajuda)
        _comuns(c)
        c.add_argument("--numero")
        c.add_argument("--ano")
        c.add_argument("--tipo")
        c.add_argument("--uf")
        c.add_argument("--esfera")
        c.add_argument("--texto")
        c.add_argument("--vigente", action="store_true")
        c.add_argument("--revogada", action="store_true")
        c.add_argument("--limite", type=int, default=20)
        if nome == "abrir":
            c.add_argument("--trecho", type=int, help="linhas do corpo (0 = tudo)")
            c.add_argument("--termo", help="mostra só as ocorrências do termo")
            c.add_argument("--contexto", type=int, default=3)

    st = sub.add_parser("status", help="resumo do acervo e do índice")
    _comuns(st)

    args = p.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    if args.comando == "indexar":
        return cmd_indexar(args)
    if args.comando == "buscar":
        return cmd_buscar_conteudo(args) if args.conteudo else cmd_buscar(args)
    if args.comando == "abrir":
        return cmd_abrir(args)
    if args.comando == "citar":
        return cmd_citar(args)
    if args.comando == "status":
        return cmd_status(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
