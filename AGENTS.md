# AGENTS.md

Guía para agentes de IA (Claude Code, Codex, Cursor, OpenCode, Copilot, etc.) que **usan** la API del INDEC
o **mantienen** este repo.

## Si tenés que consultar datos del INDEC

Usá la skill: `skills/indec-api/SKILL.md`. Resumen de lo indispensable:

- `GET https://api.indec.gob.ar/v1/<tabla>` con `Authorization: Bearer $INDEC_TOKEN`. Sin token no hay datos.
- Sintaxis PostgREST: `?col=op.valor&select=a,b&order=c.desc&limit=N&offset=M`.
- Máximo 1000 filas por respuesta. Paginá ordenando por la **clave primaria completa** de la tabla.
- Nombres de columna sensibles a mayúsculas e inconsistentes entre tablas (`Anio` vs `anio`). Copialos de
  `skills/indec-api/references/endpoints.md`.
- Los valores de texto de las dimensiones (región, nivel, tipo de indicador) no están documentados:
  descubrilos con `python3 skills/indec-api/scripts/indec.py distinct <tabla> <columnas>` antes de filtrar.
- `null` en un valor puede tener significado (signo convencional en `observaciones`, p. ej. `s` = secreto
  estadístico).
- Nunca imprimas, commitees ni loguees el token.

## Estructura del repo

```
skills/indec-api/              # la skill (lo que instala `npx skills add`); debe ser autocontenida
  SKILL.md                     # entrada: frontmatter name/description + flujo + trampas
  references/endpoints.md      # GENERADO desde la spec — no editar a mano
  references/query-syntax.md   # PostgREST, paginación, errores, snippets Python/TS
  references/recipes.md        # recetas por pregunta (IPC, CBA, pobreza, EMAE, comercio, población)
  scripts/indec.py             # CLI solo stdlib: tables, columns, get, count, distinct, latest
spec/openapi.json              # snapshot de https://api.indec.gob.ar/api/openapi?v=2 (campo "spec")
scripts/gen_endpoints.py       # spec → references/endpoints.md   (--fetch baja la spec actual)
scripts/check_docs.py          # falla si un .md cita tablas/columnas que no existen en la spec
.github/workflows/             # CI: compila, verifica docs y sincroniza la spec semanalmente
```

## Reglas para cambios

1. Todo lo que la skill necesita en runtime vive dentro de `skills/indec-api/` (los instaladores copian solo
   esa carpeta). Nada de imports desde `scripts/` del repo.
2. `scripts/indec.py` es **solo stdlib**, Python ≥ 3.8. Sin `requests`, sin dependencias.
3. Si la spec cambia: `python3 scripts/gen_endpoints.py --fetch && python3 scripts/check_docs.py`.
4. No inventes valores de dimensiones (`region=eq.Nacional`) en la documentación: usá `<placeholder>` y el
   paso de `distinct`, salvo que lo hayas verificado contra la API con un token real.
5. Prosa en español rioplatense neutro (voseo), nombres de columnas y tablas tal cual vienen de la API.
6. Antes de commitear:
   ```bash
   python3 -m py_compile skills/indec-api/scripts/indec.py
   python3 scripts/check_docs.py
   python3 skills/indec-api/scripts/indec.py tables   # no requiere token
   ```
