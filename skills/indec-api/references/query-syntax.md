# Sintaxis de consulta (PostgREST)

La API es PostgREST detrás de nginx. Todo lo de abajo funciona con `curl` o cualquier cliente HTTP.

```bash
curl -s -H "Authorization: Bearer $INDEC_TOKEN" \
  "https://api.indec.gob.ar/v1/pobreza_eph?select=periodo,tasa_pobreza_personas&order=periodo.desc&limit=4"
```

## Parámetros

| Parámetro | Ejemplo | Notas |
|---|---|---|
| `select` | `select=periodo,valor` | Columnas. Alias: `select=p:periodo`. Cast: `select=valor::numeric` |
| `order` | `order=periodo.desc,codigo` | `.asc` (default) / `.desc`, `.nullsfirst`/`.nullslast` |
| `limit` | `limit=100` | Máximo efectivo **1000** |
| `offset` | `offset=1000` | Paginación |
| `<columna>` | `periodo=gte.202401` | Filtro, ver operadores |
| `or` | `or=(region.eq.GBA,region.eq.Noreste)` | Disyunción; dentro se usa `col.op.valor` |
| `not.` | `region=not.eq.GBA` | Niega cualquier operador |

Varios filtros sobre columnas distintas se combinan con AND. Para un rango sobre la misma columna:
`and=(periodo.gte.202401,periodo.lte.202412)` o `periodo=gte.202401&periodo=lte.202412`.

## Operadores

| Operador | Significado | Ejemplo |
|---|---|---|
| `eq` / `neq` | igual / distinto | `region=eq.GBA` |
| `gt` `gte` `lt` `lte` | comparaciones | `Anio=gte.2020` |
| `like` / `ilike` | patrón (sensible / insensible a mayúsculas); comodín `*`, no `%` | `descripcion=ilike.*alimentos*` |
| `in` | en lista; comillas dobles si el valor tiene comas o espacios | `pais_cod=in.(200,203)` · `descripcion=in.("Nivel general","Alimentos y bebidas no alcohólicas")` |
| `is` | null / true / false | `valor=is.null` |

URL-encodeá los valores (espacios, acentos, comillas). En `curl` usá `--get --data-urlencode 'descripcion=eq.Nivel general'`.

## Paginación y totales

- Cada respuesta trae **como máximo 1000 filas**.
- Ordená por la **clave primaria completa** (ver `endpoints.md`) y avanzá `offset` de a 1000 hasta recibir < 1000.
- `Prefer: count=exact` → header `Content-Range: inicio-fin/total`; si la respuesta es parcial, el status es `206`.
- Para contar sin traer datos: `limit=1` + `Prefer: count=exact`, o `HEAD`.

## Errores

Cuerpo: `{"code": "...", "message": "...", "details": ..., "hint": ...}`

| Status | Código típico | Causa |
|---|---|---|
| 400 | `PGRST100` | filtro mal formado (`periodo=2024` sin operador). Se valida **antes** que el token |
| 400 | `42703` (Postgres) | columna inexistente — casi siempre mayúsculas (`anio` vs `Anio`) |
| 401 | `42501` | sin header `Authorization` ("permission denied for schema api") |
| 401 | `PGRST301` | JWT mal formado, vencido o revocado |
| 403 | | sin permiso sobre la tabla |
| 404 | `PGRST205` | tabla inexistente; el `hint` sugiere la correcta (`canasta_crianza` → `canasta-crianza`) |

## Snippets

### Python (requests)

```python
import os, requests

BASE = "https://api.indec.gob.ar/v1"
H = {"Authorization": f"Bearer {os.environ['INDEC_TOKEN']}"}

def fetch_all(table, pk, **filters):
    rows, offset = [], 0
    while True:
        params = {**filters, "order": pk, "limit": 1000, "offset": offset}
        r = requests.get(f"{BASE}/{table}", headers=H, params=params, timeout=60)
        r.raise_for_status()           # 200 y 206 son OK
        page = r.json()
        rows += page
        if len(page) < 1000:
            return rows
        offset += 1000

rows = fetch_all("pobreza_eph", "area_geografica_nom,periodo", periodo="gte.20201")
```

### pandas

```python
import pandas as pd
df = pd.DataFrame(rows)
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")  # por las dudas: indice_salarios lo devolvía como texto
```

### TypeScript (fetch)

```ts
const BASE = "https://api.indec.gob.ar/v1";

export async function indec<T>(table: string, params: Record<string, string | number>): Promise<T[]> {
  const qs = new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)]));
  const res = await fetch(`${BASE}/${table}?${qs}`, {
    headers: { Authorization: `Bearer ${process.env.INDEC_TOKEN}` },
  });
  if (!res.ok) throw new Error(`INDEC ${res.status}: ${await res.text()}`); // 206 es ok
  return res.json();
}
```

El token es personal: en apps web llamá a la API desde el servidor, no lo expongas en el navegador.
