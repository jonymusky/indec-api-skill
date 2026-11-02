#!/usr/bin/env python3
"""Verifica que la documentación no cite tablas ni columnas que no existen en spec/openapi.json.

Revisa todos los .md del repo:
  - comandos `indec.py <cmd> <tabla> col=op.valor --select a,b --order c.desc`
  - URLs `/v1/<tabla>?col=...` y `/<tabla>?col=...`
Sale con código 1 si encuentra algo inválido. Pensado para CI.
"""
import json
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "spec" / "openapi.json").read_text(encoding="utf-8"))


def columns(path):
    schema = spec["paths"][path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    ref = schema["items"]["$ref"].split("/")[-1]
    return set(spec["components"]["schemas"][ref]["properties"])


TABLES = {p.strip("/"): columns(p) for p in spec["paths"]}
# Nombres mal escritos a propósito (ejemplos de errores en la doc)
INTENTIONAL = {"canasta_crianza"}
SPECIAL = {"or", "and", "not.or", "not.and", "select", "order", "limit", "offset"}
errors = []


def check_cols(where, table, cols):
    for c in cols:
        c = c.strip()
        if not c or c in SPECIAL or c == "*" or c.startswith("<"):
            continue
        if c not in TABLES[table]:
            errors.append(f"{where}: columna {c!r} no existe en {table}")


def names_from_list(value, kind):
    out = []
    for part in value.split(","):
        part = part.strip()
        if kind == "select":
            part = part.split(":")[-1].split("::")[0]
        else:
            part = part.split(".")[0]
        out.append(part)
    return out


def check_cli(where, line):
    line = line.split("#")[0].replace("\\", " ")
    m = re.search(r"(?:indec\.py|\$S)\s+(get|count|distinct|latest|columns)\s+([^`]*)", line)
    if not m:
        return
    try:
        args = shlex.split(m.group(2))
    except ValueError:
        args = m.group(2).split()
    if not args:
        return
    table, rest = args[0], args[1:]
    if table.startswith("<"):
        return
    if table not in TABLES:
        errors.append(f"{where}: tabla {table!r} no existe")
        return
    cols = []
    if m.group(1) == "distinct" and rest:
        cols += names_from_list(rest.pop(0), "select")
    it = iter(rest)
    for a in it:
        if a in ("--select", "--order"):
            cols += names_from_list(next(it, ""), a[2:])
        elif a.startswith("--"):
            continue
        elif "=" in a:
            cols.append(a.split("=", 1)[0])
    check_cols(where, table, cols)


def check_url(where, line):
    for m in re.finditer(r"/(?:v1/)?([a-z0-9_-]+)\?([^\s`\"')]+)", line):
        table, qs = m.group(1), m.group(2)
        if table not in TABLES:
            continue
        cols = []
        for kv in qs.split("&"):
            k, _, v = kv.partition("=")
            if k in ("select", "order"):
                cols += names_from_list(v, k)
            else:
                cols.append(k)
        check_cols(where, table, cols)


for md in sorted(ROOT.rglob("*.md")):
    if "node_modules" in md.parts or md.name == "endpoints.md":
        continue
    for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{md.relative_to(ROOT)}:{i}"
        check_cli(where, line)
        check_url(where, line)
        for t in re.findall(r"`([a-z0-9_-]{6,})`", line):
            if ("_" in t or "-" in t) and t not in TABLES and t not in INTENTIONAL and re.fullmatch(r"(ipc|ipi|icc|sipm|comercio|pobreza|mercado|canasta|valorizacion|estimador|proyecciones|estimaciones|indice|redeterminacion)[a-z0-9_-]*", t):
                if not t.endswith("-*") and not any(x.startswith(t) for x in TABLES):
                    errors.append(f"{where}: posible tabla inexistente {t!r}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: docs consistentes con la spec ({len(TABLES)} tablas)")
