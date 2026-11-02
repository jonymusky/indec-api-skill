# INDEC API — Agent Skill

[![skills.sh](https://img.shields.io/badge/skills.sh-indec--api-black)](https://skills.sh/jonymusky/indec-api-skill)
[![ci](https://github.com/jonymusky/indec-api-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/jonymusky/indec-api-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Skill para agentes de IA que consultan los **datos oficiales del INDEC** (Argentina) a través del
[Catálogo API-INDEC](https://api.indec.gob.ar/docs): inflación, canastas básicas, pobreza, empleo, EMAE,
industria, salarios, construcción, precios mayoristas, población y comercio exterior.

```bash
npx skills add jonymusky/indec-api-skill
```

Funciona con Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot y
[el resto de agentes compatibles con skills.sh](https://skills.sh). El CLI incluido también se usa solo,
sin agente.

---

## Por qué

La API es buena —PostgREST, OpenAPI, 19 tablas oficiales— pero tiene detalles que hacen que un agente
falle en el primer intento y no sepa por qué:

| Lo que el agente hace | Lo que pasa | Lo que hace la skill |
|---|---|---|
| Filtra `anio=eq.2024` en exportaciones | `400`: la columna se llama `Anio` | El CLI valida contra la spec y sugiere `Anio` |
| Pide `/canasta_crianza` | `404`: la ruta es `canasta-crianza` | Catálogo con los nombres exactos |
| Usa `limit=10000` para traer todo | Llegan 1000 filas, sin aviso | `--all` pagina por la clave primaria completa |
| Pagina con `order=periodo` | Filas duplicadas o perdidas entre páginas | Ordena siempre por la PK de cada tabla |
| Adivina `region=eq.Nacional` | `[]` vacío, sin error | Flujo "descubrir con `distinct` → filtrar" |
| Ve `valor: null` y lo ignora | Era `s` (secreto estadístico) o `*` (provisorio) | Lee `observaciones` y los signos convencionales |
| Suma `valor` en `indice_salarios` | Concatena strings | Avisa que ahí `valor` es texto |
| Recibe `206` y lo trata como error | Era una respuesta parcial válida | Documenta `Prefer: count=exact` / `Content-Range` |

## Token

Todos los endpoints de datos requieren un JWT personal (es gratis):

1. Registrate en <https://api.indec.gob.ar> con mail, nombre y organización.
2. Verificá el mail con el código OTP.
3. Generá el token desde tu perfil. **Se muestra una sola vez**; generar otro revoca el anterior.
4. Exportalo:

```bash
export INDEC_TOKEN="eyJ..."
```

No lo commitees. En apps web, llamá a la API desde el servidor.

## Usarlo con un agente

Una vez instalada, pedile cosas en lenguaje natural:

> ¿Cuál fue la inflación mensual de los últimos 6 meses por región?
>
> Graficá la tasa de desocupación desde 2017.
>
> ¿Cuánto exportó Argentina a Brasil en 2024 por rubro?
>
> Armame un script que actualice todos los meses la CBA y la CBT en un CSV.

La skill le enseña al agente qué tabla usar, cómo descubrir los valores exactos de las dimensiones antes de
filtrar, cómo paginar sin perder filas y cómo citar la fuente y el último período disponible.

## Usarlo sin agente: el CLI

`skills/indec-api/scripts/indec.py` — Python ≥ 3.8, solo stdlib, sin instalar nada.

```bash
S=skills/indec-api/scripts/indec.py

python3 $S tables                                    # 19 tablas + clave primaria (sin token)
python3 $S columns mercado_trabajo_eph               # columnas, tipos, descripción (sin token)

python3 $S distinct ipc_nacional region,clasificador,nivel        # qué valores existen
python3 $S latest pobreza_eph --periods 4 --format csv            # últimos 4 semestres
python3 $S get mercado_trabajo_eph anio=gte.2023 \
  --select periodo,anio,trimestre,tasa_de_desocupacion --order periodo
python3 $S count comercio_exterior_exportacion_bienes Anio=eq.2024
python3 $S get comercio_exterior_exportacion_bienes Anio=eq.2024 --all --labels --format csv > expo_2024.csv
```

| Comando | Qué hace |
|---|---|
| `tables` / `columns <tabla>` | Metadatos desde la spec pública (cacheada 24 h en `~/.cache/indec-api`) |
| `get <tabla> [filtros]` | Consulta. `--select --order --limit --offset --all --count --format json\|csv\|ndjson` |
| `latest <tabla> --periods N` | Filas de los últimos N períodos; detecta `periodo` / `Periodo` / `fecha` |
| `distinct <tabla> <cols>` | Combinaciones únicas (PostgREST no tiene `DISTINCT`); sale en CSV por defecto |
| `count <tabla> [filtros]` | Total con `Prefer: count=exact` |
| `--labels` | Traduce `pais_cod`, `rubro_cod`, etc. con `comercio_exterior_nomenclaturas` |

Los filtros son estilo PostgREST: `col=op.valor` con `eq neq gt gte lt lte like ilike in is`, más
`or=(…)` y `not.`. Reintenta 429/5xx con backoff. `--no-validate` saltea la validación de columnas.

## Qué trae

| Archivo | Contenido |
|---|---|
| [`SKILL.md`](skills/indec-api/SKILL.md) | Entrada de la skill: cuándo usarla, flujo, tabla → pregunta, 11 trampas |
| [`references/endpoints.md`](skills/indec-api/references/endpoints.md) | Las 19 tablas: descripción, PK, columnas, tipos, nulos (generado de la spec) |
| [`references/query-syntax.md`](skills/indec-api/references/query-syntax.md) | PostgREST, paginación, errores verificados, snippets Python / pandas / TypeScript |
| [`references/recipes.md`](skills/indec-api/references/recipes.md) | IPC, CBA/CBT, pobreza, empleo, EMAE, exportaciones, población, ajuste por inflación |
| [`scripts/indec.py`](skills/indec-api/scripts/indec.py) | CLI |
| [`AGENTS.md`](AGENTS.md) | Guía para agentes que usan o mantienen el repo |

### Tablas cubiertas

| Tema | Tablas |
|---|---|
| Precios | `ipc_nacional`, `valorizacion_canastas_cba_cbt`, `sipm_precios_mayoristas`, `icc_precios_construccion`, `redeterminacion_precios_contratos_obras_publicas` |
| Actividad | `estimador-mensual-de-actividad-economica-nivel-general`, `estimador-mensual-de-actividad-economica-sectores`, `ipi_manufacturero`, `ipi_minero` |
| Trabajo e ingresos | `mercado_trabajo_eph`, `pobreza_eph`, `indice_salarios`, `canasta-crianza` |
| Población | `proyecciones_poblacion_nacional_2022_2040`, `proyecciones_poblacion_jurisdiccion_2022_2040`, `estimaciones_poblacion_departamento_2022_2035` |
| Comercio exterior | `comercio_exterior_exportacion_bienes`, `comercio_exterior_importacion_bienes`, `comercio_exterior_nomenclaturas` |

## Se mantiene solo

- `spec/openapi.json` es un snapshot de la [spec oficial](https://api.indec.gob.ar/api/openapi?v=2).
- `scripts/gen_endpoints.py` regenera el catálogo; `scripts/check_docs.py` falla si algún ejemplo de la
  documentación cita una tabla o columna que no existe.
- El [CI](.github/workflows/ci.yml) corre ambos en cada push y, todos los lunes, baja la spec y abre un PR
  si el INDEC agregó o cambió tablas. Si configurás el secret `INDEC_TOKEN`, además hace un smoke test real.

```bash
python3 scripts/gen_endpoints.py --fetch && python3 scripts/check_docs.py
```

## Estado y límites

- Metadatos, rutas, columnas, errores sin token y armado de URLs están verificados contra la API.
  Las recetas usan `<placeholders>` para los valores de dimensiones (región, nivel, tipo de indicador)
  porque esos textos no figuran en la spec: la skill los descubre en vivo con `distinct`.
- Proyecto independiente, **no oficial** ni afiliado al INDEC. Los datos y sus condiciones de uso son del
  INDEC: <https://api.indec.gob.ar/ayuda/terminos>.

## In English

Agent skill for Argentina's official statistics API (INDEC). Covers all 19 tables (CPI/inflation,
poverty lines, poverty rate, labour market, monthly economic activity, industrial production, wages,
construction and wholesale prices, population projections, exports/imports by country), the PostgREST
query syntax, and the traps that make agents fail (case-sensitive mixed-case columns, 1000-row cap,
stable pagination, undocumented dimension values, meaningful nulls). Ships a zero-dependency Python CLI.
Requires a free personal JWT from <https://api.indec.gob.ar>. Install with
`npx skills add jonymusky/indec-api-skill`.

## Licencia

[MIT](LICENSE)
