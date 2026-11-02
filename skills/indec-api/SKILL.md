---
name: indec-api
description: Consultar datos oficiales del INDEC (Instituto Nacional de Estadística y Censos de Argentina) a través del Catálogo API-INDEC (api.indec.gob.ar, PostgREST + JWT). Usalo cuando haya que obtener, analizar, graficar o integrar en código estadísticas argentinas — inflación / IPC, canasta básica alimentaria y total (CBA/CBT), canasta de crianza, pobreza e indigencia, desocupación y mercado de trabajo (EPH), EMAE / actividad económica, IPI manufacturero y minero, índice de salarios, costo de la construcción (ICC), precios mayoristas (IPIM/IPIB/IPP), redeterminación de obra pública, proyecciones de población, exportaciones e importaciones por país. También para "Argentina inflation / poverty / unemployment / trade data", y siempre que alguien quiera reemplazar el scraping de los Excel del INDEC por la API.
license: MIT
---

# API INDEC

Catálogo API-INDEC: datos oficiales del INDEC servidos con PostgREST.

- Base: `https://api.indec.gob.ar/v1/<tabla>` — solo `GET` (y `HEAD`/`OPTIONS`)
- Auth: `Authorization: Bearer $INDEC_TOKEN` en **todas** las tablas. Sin token → `401 {"code":"42501"}`
- Spec viva (sin auth): `https://api.indec.gob.ar/api/openapi?v=2` (viene envuelta en `{"spec": …}`)
- Docs humanas: https://api.indec.gob.ar/docs

## 0. Token

Si `INDEC_TOKEN` no está definido, no inventes uno ni intentes saltear la auth: pedile a la persona que
se registre en https://api.indec.gob.ar (mail → código OTP → perfil → "generar token"; el token se muestra
**una sola vez** y generar otro revoca el anterior) y lo exporte. No lo escribas en archivos versionados.

## 1. Elegí la tabla

Mirá el índice en `references/endpoints.md` (19 tablas, columnas, tipos, clave primaria) o corré
`scripts/indec.py tables`. Atajos:

| Pregunta | Tabla |
|---|---|
| Inflación, IPC por región/división | `ipc_nacional` |
| Línea de pobreza/indigencia (CBA, CBT) | `valorizacion_canastas_cba_cbt` |
| % pobreza / indigencia (semestral) | `pobreza_eph` |
| Desocupación, actividad, informalidad (trimestral) | `mercado_trabajo_eph` |
| Actividad económica mensual | `estimador-mensual-de-actividad-economica-nivel-general`, `…-sectores` |
| Industria / minería | `ipi_manufacturero`, `ipi_minero` |
| Salarios | `indice_salarios` |
| Construcción / mayoristas / obra pública | `icc_precios_construccion`, `sipm_precios_mayoristas`, `redeterminacion_precios_contratos_obras_publicas` |
| Crianza de chicos | `canasta-crianza` |
| Población | `proyecciones_poblacion_nacional_2022_2040`, `proyecciones_poblacion_jurisdiccion_2022_2040`, `estimaciones_poblacion_departamento_2022_2035` |
| Comercio exterior | `comercio_exterior_exportacion_bienes`, `comercio_exterior_importacion_bienes` + diccionario `comercio_exterior_nomenclaturas` |

## 2. Descubrí los valores antes de filtrar

Las tablas de índices son **largas**: una fila por combinación de `region` × `clasificador` × `nivel` ×
`codigo`/`descripcion` × `indicador` × `tipo_de_indicador` × `periodo`, con un único `valor`. Los textos
exactos de esas columnas (p. ej. cómo se llama "Nacional" o "variación mensual") **no están en la spec**.
Nunca los adivines: listalos primero.

```bash
S=skills/indec-api/scripts/indec.py   # o la ruta donde esté instalada la skill
python3 $S distinct ipc_nacional region,clasificador,nivel
python3 $S distinct ipc_nacional indicador,tipo_de_indicador,tipo_de_indicador_descripcion,unidad_de_medida
```

`distinct` recorre toda la tabla (PostgREST no tiene `DISTINCT`); en tablas grandes acotalo con un filtro,
por ejemplo `periodo=eq.202501`. Recetas completas en `references/recipes.md`.

## 3. Consultá

```bash
python3 $S get <tabla> col=op.valor … --select a,b --order periodo.desc --limit 12
python3 $S latest <tabla> [filtros] --periods 3     # últimos N períodos, sin saber cómo se llama la columna
python3 $S get <tabla> [filtros] --all --format csv  # pagina sola por la clave primaria
python3 $S count <tabla> [filtros]
python3 $S get comercio_exterior_exportacion_bienes Anio=eq.2024 --all --labels   # agrega *_desc
```

El CLI es solo stdlib (Python 3.8+), valida columnas contra la spec antes de enviar y reintenta 429/5xx.
Si trabajás en otro lenguaje, la API es HTTP plano: ver `references/query-syntax.md`.

## Trampas (leer antes de escribir código)

1. **Mayúsculas en columnas**. PostgREST distingue mayúsculas y la API no es consistente:
   `Anio`, `Mes`, `Periodo` en ambas tablas de comercio exterior; en `canasta-crianza` es `anio` pero
   `Mes` y `Periodo`; `valor_FOB`/`Peso_Neto` (expo) vs `valor_CIF`/`peso_neto` (impo);
   `codigo_CLaNAE_2004` (IPI manufacturero) vs `codigo_ClaNAE_2010` (IPI minero); `codigo_CPC_1`,
   `codigo_CIUU_3`, `codigo_CPC_2_1`. Copiá los nombres de `references/endpoints.md`, nunca los normalices.
2. **Guiones vs guiones bajos en rutas**: `estimador-mensual-de-actividad-economica-*` y `canasta-crianza`
   usan guiones; el resto, guiones bajos.
3. **Tope de 1000 filas por respuesta**, aunque pidas `limit=5000`. Si recibís exactamente 1000, hay más.
   Para paginar, `order` tiene que incluir **la clave primaria completa** o se duplican/pierden filas entre
   páginas. La PK de cada tabla está en `references/endpoints.md`.
4. **`206 Partial Content` es éxito**: pasa cuando mandás `Prefer: count=exact` y la respuesta es parcial;
   el total viene en `Content-Range: 0-999/103545`.
5. **Período como texto de ancho fijo**: `AAAAMM` mensual; `AAAAN` con N = semestre en `pobreza_eph`
   (`20242` = 2.º semestre 2024) y N = trimestre en `mercado_trabajo_eph`. Comparar con `gte.`/`lte.`
   funciona por ser ancho fijo. En población, `fecha` es el año: texto en las tablas de jurisdicción y
   departamento, número en la nacional.
6. **`valor` es texto en `indice_salarios`** (número en el resto). Convertí antes de operar.
7. **Nulos con significado**: cuando `valor` es `null`, `observaciones` puede traer un signo convencional
   (`*` provisorio, `**` preliminar, `e`/`i` estimado, `-` cero absoluto, `...` no disponible, `///` no
   corresponde, `s` secreto estadístico — muy común en comercio exterior por país). No lo trates como
   "dato faltante" sin mirar `observaciones`, y avisale a la persona si un número es provisorio.
8. **Formatos distintos**: las tablas EPH (`pobreza_eph`, `mercado_trabajo_eph`) y `canasta-crianza` son
   **anchas** (una columna por tasa o tramo de edad); las de índices son **largas** (`valor` + dimensiones).
9. **Series con variaciones ya calculadas**: no recalcules la inflación mensual dividiendo índices si la
   tabla trae `tipo_de_indicador` de variación — usá el publicado. Las variaciones calculadas por vos
   pueden diferir de los informes técnicos por redondeo (lo aclara el propio INDEC).
10. **Los "Ejemplos de uso" de la spec oficial son autogenerados** (`anio=gt.100`, `periodo=ilike.*valor*`):
    no los copies como si fueran consultas útiles.
11. **Comercio exterior usa códigos**: `pais_cod`, `rubro_cod`, `subrubro_cod`, `uso_economico_cod`,
    `gce_cod`. Traducilos con `comercio_exterior_nomenclaturas` (`nombre_columna`, `codigo`,
    `codigo_descripcion`) — `--labels` lo hace solo.

## Al responder

- Citá la fuente: "INDEC, Catálogo API-INDEC, tabla `<tabla>`, período `<periodo>`".
- Indicá el último período disponible y si el dato es provisorio.
- Para series largas, devolvé CSV o un gráfico, no 500 filas pegadas en el chat.
