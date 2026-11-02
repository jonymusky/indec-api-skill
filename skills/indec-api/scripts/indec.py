#!/usr/bin/env python3
"""Cliente mínimo (solo stdlib) para el Catálogo API-INDEC — https://api.indec.gob.ar/docs

Autenticación: exportá INDEC_TOKEN con el JWT generado en tu perfil del portal.

Comandos:
  tables                                  Lista endpoints y su clave primaria (no requiere token)
  columns  <tabla>                        Columnas, tipos y descripción de una tabla (no requiere token)
  get      <tabla> [filtros] [opciones]   Consulta filas
  count    <tabla> [filtros]              Total de filas que cumplen los filtros
  distinct <tabla> <col1,col2> [filtros]  Combinaciones únicas de columnas (recorre toda la tabla)
  latest   <tabla> [filtros] [--periods N] Filas de los últimos N períodos (detecta periodo/Periodo/fecha)

Filtros: argumentos posicionales estilo PostgREST, columna=operador.valor
  periodo=gte.202401   region=eq.Nacional   descripcion=ilike.*alimentos*   pais_cod=in.(200,203)

Opciones de get:
  --select a,b   --order col.desc   --limit N   --offset N
  --all          Pagina hasta traer todo (ordena por la clave primaria si no pasás --order)
  --format json|csv|ndjson   (default json)
  --labels       En comercio exterior agrega <col>_desc para cada *_cod usando comercio_exterior_nomenclaturas
  --no-validate  No validar nombres de columna contra la spec

Antes de enviar, filtros/select/order se validan contra la spec: si escribís `anio` donde la
columna es `Anio`, el CLI te lo dice en vez de dejar que la API devuelva 400.

Ejemplos:
  indec.py get ipc_nacional periodo=gte.202501 --select periodo,descripcion,valor --limit 20
  indec.py distinct ipc_nacional region,clasificador,nivel
  indec.py count comercio_exterior_exportacion_bienes Anio=eq.2024
  indec.py latest pobreza_eph --periods 4
  indec.py latest comercio_exterior_exportacion_bienes --labels --format csv
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = os.environ.get("INDEC_BASE_URL", "https://api.indec.gob.ar/v1").rstrip("/")
SPEC_URL = "https://api.indec.gob.ar/api/openapi?v=2"
PAGE = 1000  # tope duro del servidor por respuesta
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "indec-api" / "openapi.json"
UA = "indec-api-skill/1.0 (+https://github.com/jonymusky/indec-api-skill)"


class ApiError(Exception):
    pass


# ---------------------------------------------------------------- spec / metadatos

def load_spec(max_age=86400):
    if CACHE.exists() and time.time() - CACHE.stat().st_mtime < max_age:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    req = urllib.request.Request(SPEC_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    spec = data.get("spec", data)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return spec


def _res(spec, node):
    while isinstance(node, dict) and "$ref" in node:
        cur = spec
        for part in node["$ref"].lstrip("#/").split("/"):
            cur = cur[part]
        node = cur
    return node


def table_meta(spec, table):
    op = spec["paths"].get("/" + table.strip("/"), {}).get("get")
    if not op:
        names = ", ".join(p.strip("/") for p in spec["paths"])
        raise ApiError(f"Tabla desconocida: {table!r}. Disponibles: {names}")
    desc = op.get("description", "")
    m = re.search(r"### Clave primaria.*?:\s*(.+)", desc, re.S)
    pk = re.findall(r"`([^`]+)`", m.group(1).splitlines()[0]) if m else []
    schema = _res(spec, op["responses"]["200"]["content"]["application/json"]["schema"])
    if schema.get("type") == "array":
        schema = _res(spec, schema["items"])
    cols = {}
    for name, cs in schema.get("properties", {}).items():
        cs = _res(spec, cs)
        types = [s.get("type") for s in cs.get("anyOf", [cs])]
        cols[name] = {
            "type": "/".join(t for t in types if t != "null") or "null",
            "nullable": "null" in types,
            "description": re.sub(r"\s+", " ", cs.get("description") or "").strip(),
        }
    return {"summary": op.get("summary", ""), "pk": pk, "columns": cols}


# ---------------------------------------------------------------- HTTP

def request(table, params, count=False):
    token = os.environ.get("INDEC_TOKEN")
    if not token:
        raise ApiError("Falta INDEC_TOKEN. Generá el JWT en tu perfil de https://api.indec.gob.ar y exportalo: export INDEC_TOKEN=...")
    url = f"{BASE}/{table.strip('/')}"
    if params:
        # safe= deja legibles los operadores PostgREST ( . , ( ) * ) sin romper la URL
        url += "?" + urllib.parse.urlencode(params, safe=".,()*:")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": UA}
    if count:
        headers["Prefer"] = "count=exact"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:  # 200 y 206 son éxito
                return json.load(r), r.headers.get("Content-Range")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code in (429, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ApiError(f"HTTP {e.code} en {url}\n{body}")
        except urllib.error.URLError as e:
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise ApiError(f"Error de red en {url}: {e.reason}")


def parse_filters(items):
    out = []
    for it in items:
        if "=" not in it:
            raise ApiError(f"Filtro inválido {it!r}: usá columna=operador.valor (ej. periodo=gte.202401)")
        k, v = it.split("=", 1)
        out.append((k, v))
    return out


def total_from(content_range):
    if content_range and "/" in content_range:
        tail = content_range.rsplit("/", 1)[1]
        return int(tail) if tail.isdigit() else None
    return None


def fetch_all(table, filters, select=None, order=None):
    rows, offset = [], 0
    while True:
        params = list(filters) + [("order", order), ("limit", PAGE), ("offset", offset)]
        if select:
            params.append(("select", select))
        page, _ = request(table, params)
        rows.extend(page)
        if len(page) < PAGE:
            return rows
        offset += PAGE



LOGICAL = {"or", "and", "not.or", "not.and"}
PERIOD_COLS = ("periodo", "Periodo", "fecha")


def check_columns(meta, table, names):
    cols = meta["columns"]
    lower = {c.lower(): c for c in cols}
    bad = []
    for n in names:
        if n in cols or n in LOGICAL:
            continue
        hint = lower.get(n.lower())
        bad.append(f"{n!r}" + (f" (¿quisiste decir {hint!r}? las columnas son sensibles a mayúsculas)" if hint else ""))
    if bad:
        raise ApiError(f"Columnas inexistentes en {table}: {', '.join(bad)}.\nVálidas: {', '.join(cols)}")


def validate(table, filters, select=None, order=None):
    meta = table_meta(load_spec(), table)
    names = [k for k, _ in filters]
    for part in (select or "").split(","):
        part = part.strip()
        if part and part != "*":
            names.append(part.split("::")[0].split(":")[-1])  # alias:col y col::cast
    for part in (order or "").split(","):
        part = part.strip()
        if part:
            names.append(part.split(".")[0])
    check_columns(meta, table, names)
    return meta


def period_col(meta):
    for c in PERIOD_COLS:
        if c in meta["columns"]:
            return c
    raise ApiError("La tabla no tiene columna de período (periodo/Periodo/fecha)")


def add_labels(rows, table):
    if not table.startswith("comercio_exterior_"):
        print("# Aviso: --labels solo aplica a tablas comercio_exterior_*; se ignora.", file=sys.stderr)
        return rows
    code_cols = {k for r in rows[:1] for k in r if k.lower().endswith("_cod")}
    if not code_cols:
        return rows
    dic = fetch_all("comercio_exterior_nomenclaturas", [], "nombre_columna,codigo,codigo_descripcion", "nombre_columna,codigo")
    lookup = {}
    for d in dic:
        lookup.setdefault(str(d["nombre_columna"]).lower(), {})[str(d["codigo"])] = d["codigo_descripcion"]
    missing = sorted(c for c in code_cols if c.lower() not in lookup)
    if missing:
        print(f"# Aviso: sin nomenclatura para {missing}. nombre_columna disponibles: {sorted(lookup)}", file=sys.stderr)
    out = []
    for r in rows:
        r = dict(r)
        for c in sorted(code_cols):
            m = lookup.get(c.lower())
            if m is not None:
                r[c[:-4] + "_desc"] = m.get(str(r.get(c)))
        out.append(r)
    return out

# ---------------------------------------------------------------- salida

def emit(rows, fmt):
    if fmt == "json":
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    elif fmt == "ndjson":
        for r in rows:
            sys.stdout.write(json.dumps(r, ensure_ascii=False) + "\n")
    elif fmt == "csv":
        if not rows:
            return
        fields = list(rows[0].keys())
        w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- comandos

def cmd_tables(_a):
    spec = load_spec()
    for path in spec["paths"]:
        m = table_meta(spec, path)
        print(f"{path.strip('/')}\t{m['summary']}\tPK={','.join(m['pk'])}")


def cmd_columns(a):
    m = table_meta(load_spec(), a.table)
    print(f"# {a.table} — {m['summary']}\nPK: {','.join(m['pk'])}")
    for name, c in m["columns"].items():
        flag = " PK" if name in m["pk"] else ""
        null = " null" if c["nullable"] else ""
        print(f"{name}\t{c['type']}{null}{flag}\t{c['description']}")


def cmd_get(a):
    filters = parse_filters(a.filters)
    if not a.no_validate:
        validate(a.table, filters, a.select, a.order)
    if a.all:
        order = a.order or ",".join(table_meta(load_spec(), a.table)["pk"])
        rows = fetch_all(a.table, filters, a.select, order)
    else:
        params = list(filters)
        for k in ("select", "order", "limit", "offset"):
            v = getattr(a, k)
            if v is not None:
                params.append((k, v))
        rows, cr = request(a.table, params, count=a.count)
        if a.count:
            print(f"# Content-Range: {cr} (total={total_from(cr)})", file=sys.stderr)
        if a.limit is None and len(rows) == PAGE:
            print(f"# Aviso: llegaron {PAGE} filas (tope del servidor). Puede haber más: usá --all o paginá con --offset.", file=sys.stderr)
    if a.labels:
        rows = add_labels(rows, a.table)
    emit(rows, a.format)


def cmd_count(a):
    if not a.no_validate:
        validate(a.table, parse_filters(a.filters))
    _, cr = request(a.table, parse_filters(a.filters) + [("limit", 1)], count=True)
    print(total_from(cr))


def cmd_distinct(a):
    meta = table_meta(load_spec(), a.table)
    cols = [c.strip() for c in a.columns.split(",") if c.strip()]
    if not a.no_validate:
        check_columns(meta, a.table, cols + [k for k, _ in parse_filters(a.filters)])
    # PostgREST no tiene DISTINCT: traemos solo esas columnas ordenando por la PK completa y deduplicamos.
    rows = fetch_all(a.table, parse_filters(a.filters), ",".join(cols), ",".join(meta["pk"]))
    seen, out = set(), []
    for r in rows:
        key = tuple(r.get(c) for c in cols)
        if key not in seen:
            seen.add(key)
            out.append(r)
    out.sort(key=lambda r: tuple("" if r.get(c) is None else str(r.get(c)) for c in cols))
    emit(out, a.format)


def cmd_latest(a):
    filters = parse_filters(a.filters)
    meta = table_meta(load_spec(), a.table) if a.no_validate else validate(a.table, filters, a.select)
    pc = period_col(meta)
    rest = [c for c in meta["pk"] if c != pc]
    # Recorre de más reciente a más antiguo hasta juntar N períodos distintos.
    periods, offset = [], 0
    while len(periods) < a.periods:
        params = filters + [("select", pc), ("order", ",".join([pc + ".desc"] + rest)), ("limit", PAGE), ("offset", offset)]
        page, _ = request(a.table, params)
        for r in page:
            v = r[pc]
            if v not in periods:
                periods.append(v)
                if len(periods) == a.periods:
                    break
        if len(page) < PAGE:
            break
        offset += PAGE
    if not periods:
        emit([], a.format)
        return
    print(f"# {pc} en {', '.join(map(str, periods))}", file=sys.stderr)
    in_list = "in.(" + ",".join(f'"{p}"' if isinstance(p, str) else str(p) for p in periods) + ")"
    rows = fetch_all(a.table, filters + [(pc, in_list)], a.select, ",".join(meta["pk"]))
    if a.labels:
        rows = add_labels(rows, a.table)
    emit(rows, a.format)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tables").set_defaults(fn=cmd_tables)

    c = sub.add_parser("columns")
    c.add_argument("table")
    c.set_defaults(fn=cmd_columns)

    g = sub.add_parser("get")
    g.add_argument("table")
    g.add_argument("filters", nargs="*")
    g.add_argument("--select")
    g.add_argument("--order")
    g.add_argument("--limit", type=int)
    g.add_argument("--offset", type=int)
    g.add_argument("--all", action="store_true")
    g.add_argument("--count", action="store_true", help="Pide Prefer: count=exact e informa el total por stderr")
    g.add_argument("--format", choices=["json", "csv", "ndjson"], default="json")
    g.add_argument("--labels", action="store_true")
    g.add_argument("--no-validate", action="store_true")
    g.set_defaults(fn=cmd_get)

    n = sub.add_parser("count")
    n.add_argument("table")
    n.add_argument("filters", nargs="*")
    n.add_argument("--no-validate", action="store_true")
    n.set_defaults(fn=cmd_count)

    l = sub.add_parser("latest")
    l.add_argument("table")
    l.add_argument("filters", nargs="*")
    l.add_argument("--periods", type=int, default=1)
    l.add_argument("--select")
    l.add_argument("--labels", action="store_true")
    l.add_argument("--no-validate", action="store_true")
    l.add_argument("--format", choices=["json", "csv", "ndjson"], default="json")
    l.set_defaults(fn=cmd_latest)

    d = sub.add_parser("distinct")
    d.add_argument("table")
    d.add_argument("columns")
    d.add_argument("filters", nargs="*")
    d.add_argument("--format", choices=["json", "csv", "ndjson"], default="csv", help="default csv (más legible para explorar)")
    d.add_argument("--no-validate", action="store_true")
    d.set_defaults(fn=cmd_distinct)

    a = p.parse_args()
    try:
        a.fn(a)
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
