#!/usr/bin/env python3
"""Regenera skills/indec-api/references/endpoints.md a partir de la spec OpenAPI.

Uso:
    python3 scripts/gen_endpoints.py            # usa spec/openapi.json
    python3 scripts/gen_endpoints.py --fetch    # baja la spec actual y la guarda primero

La spec oficial se sirve en https://api.indec.gob.ar/api/openapi?v=2 envuelta en
{"spec": {...}, "uiConfig": {...}}; acá se guarda solo "spec".
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.json"
OUT = ROOT / "skills" / "indec-api" / "references" / "endpoints.md"
SPEC_URL = "https://api.indec.gob.ar/api/openapi?v=2"

PAGING_PARAMS = {"select", "order", "limit", "offset", "Prefer"}


def fetch_spec():
    req = urllib.request.Request(SPEC_URL, headers={"User-Agent": "indec-api-skill"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    spec = data.get("spec", data)
    SPEC.parent.mkdir(parents=True, exist_ok=True)
    SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolver(spec):
    def res(node):
        while isinstance(node, dict) and "$ref" in node:
            cur = spec
            for part in node["$ref"].lstrip("#/").split("/"):
                cur = cur[part]
            node = cur
        return node
    return res


def col_type(schema):
    if "anyOf" in schema:
        types = [s.get("type") for s in schema["anyOf"]]
        base = [t for t in types if t != "null"]
        return "/".join(base) or "null", "null" in types
    return schema.get("type", "?"), False


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def intro(desc):
    body = desc.split("### Ejemplos")[0]
    return clean(body)


def primary_key(desc):
    m = re.search(r"### Clave primaria.*?:\s*(.+)", desc, re.S)
    if not m:
        return []
    return re.findall(r"`([^`]+)`", m.group(1).splitlines()[0])


def param_desc(p):
    text = clean(p.get("description"))
    text = re.sub(r"^Filtro para\s+", "", text)
    text = re.sub(r"\s*Use operadores como eq, gt, ilike\.?$", "", text)
    return text.rstrip(".") + ("." if text else "")


def main():
    if "--fetch" in sys.argv:
        fetch_spec()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    res = resolver(spec)
    base = spec["servers"][0]["url"].rstrip("/")

    lines = [
        "# Catálogo de endpoints — API INDEC",
        "",
        "<!-- Generado por scripts/gen_endpoints.py desde spec/openapi.json. No editar a mano. -->",
        "",
        f"Base URL: `{base}/` · Spec: `{SPEC_URL}` · Versión de spec: {spec['info'].get('version')}",
        "",
        "Los nombres de columna son **sensibles a mayúsculas**: copialos tal cual de esta tabla.",
        "",
        "## Índice",
        "",
        "| Endpoint | Qué es | Dirección INDEC |",
        "|---|---|---|",
    ]
    sections = []
    for path, item in spec["paths"].items():
        op = item["get"]
        name = path.strip("/")
        anchor = re.sub(r"[^a-z0-9_-]", "", name.lower())
        tag = (op.get("tags") or [""])[0]
        lines.append(f"| [`{path}`](#{anchor}) | {op.get('summary', '')} | {tag} |")

        desc = op.get("description", "")
        pk = primary_key(desc)
        params = {p["name"]: p for p in map(res, op.get("parameters", []))}
        schema = res(op["responses"]["200"]["content"]["application/json"]["schema"])
        if schema.get("type") == "array":
            schema = res(schema["items"])

        sec = [f"## {name}", "", f"**{op.get('summary', '')}** — {tag}", "", intro(desc), ""]
        sec.append(f"- Clave primaria (usala completa en `order` para paginar): `{','.join(pk)}`")
        sec.append(f"- Traer todo: `GET {path}?order={','.join(pk)}&limit=1000&offset=0`")
        sec += ["", "| Columna | Tipo | Nulo | Descripción |", "|---|---|---|---|"]
        for col, cs in schema.get("properties", {}).items():
            cs = res(cs)
            t, nullable = col_type(cs)
            d = clean(cs.get("description")) or (param_desc(params[col]) if col in params else "")
            mark = "**PK** " if col in pk else ""
            sec.append(f"| `{col}` | {t} | {'sí' if nullable else ''} | {mark}{d.replace('|', '/')} |")
        sections.append("\n".join(sec))

    lines += ["", *[s + "\n" for s in sections]]
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"OK: {len(sections)} endpoints -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
