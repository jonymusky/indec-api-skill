# Recetas

`S` = ruta a `scripts/indec.py`. Los valores entre `<…>` salen del paso de descubrimiento (`distinct`):
**no los completes de memoria**, el texto exacto importa (`eq.` compara literal).

## Inflación mensual (IPC)

```bash
# 1. Qué regiones, clasificadores y niveles hay
python3 $S distinct ipc_nacional region,clasificador,nivel periodo=eq.<ultimo_periodo>
# 2. Qué tipos de indicador hay (índice, variación mensual, interanual, …)
python3 $S distinct ipc_nacional indicador,tipo_de_indicador,tipo_de_indicador_descripcion periodo=eq.<ultimo_periodo>
# 3. Serie del nivel general
python3 $S get ipc_nacional region=eq.<region> nivel=eq.<nivel_general> \
  tipo_de_indicador=eq.<variacion_mensual> periodo=gte.202401 \
  --select periodo,descripcion,valor,observaciones --order periodo --all --format csv
```

Truco para obtener `<ultimo_periodo>`: `python3 $S get ipc_nacional --select periodo --order periodo.desc --limit 1`.
O directamente `python3 $S latest ipc_nacional` y mirá qué combinaciones vinieron.

Inflación acumulada de N meses: usá el `tipo_de_indicador` de variación acumulada si existe; si la calculás
vos, encadená `Π(1 + v/100) − 1` sobre variaciones mensuales, nunca sumes porcentajes.

## Canasta básica (línea de pobreza / indigencia)

```bash
python3 $S distinct valorizacion_canastas_cba_cbt descripcion,tipo_de_indicador,unidad_de_medida,region
python3 $S latest valorizacion_canastas_cba_cbt --periods 2 --format csv
```

La tabla es de Gran Buenos Aires. Mirá `descripcion` y `unidad_de_medida` para saber si el valor es por
adulto equivalente o por hogar tipo. Para un hogar propio, multiplicá el valor por adulto equivalente
por la suma de unidades de sus miembros (tabla de equivalencias en la metodología INDEC N° 22).

## Pobreza e indigencia (semestral, tabla ancha)

```bash
python3 $S distinct pobreza_eph area_geografica_nom
python3 $S get pobreza_eph --select periodo,tasa_pobreza_personas,tasa_indigencia_personas,observaciones \
  --order periodo.desc --limit 6
```

`periodo` = `AAAAS`: `20242` es el segundo semestre de 2024.

## Mercado de trabajo (trimestral, tabla ancha)

```bash
python3 $S latest mercado_trabajo_eph --periods 4 \
  --select periodo,area_geografica_nom,tasa_de_actividad,tasa_de_empleo,tasa_de_desocupacion,tasa_de_empleo_informal
```

## EMAE (actividad económica)

```bash
python3 $S distinct estimador-mensual-de-actividad-economica-nivel-general tipo_de_indicador,tipo_de_indicador_descripcion
python3 $S get estimador-mensual-de-actividad-economica-nivel-general \
  tipo_de_indicador_descripcion=eq.<desestacionalizada_indice> --order periodo.desc --limit 24
python3 $S distinct estimador-mensual-de-actividad-economica-sectores codigo,descripcion
```

## Exportaciones por país

```bash
# Códigos de país (y de rubro, subrubro, uso económico, gce)
python3 $S distinct comercio_exterior_nomenclaturas nombre_columna
python3 $S get comercio_exterior_nomenclaturas nombre_columna=eq.pais_cod codigo_descripcion=ilike.*brasil* 
# Exportaciones 2024 a ese país, con nombres
python3 $S get comercio_exterior_exportacion_bienes Anio=eq.2024 pais_cod=eq.<codigo> --all --labels --format csv
```

Ojo: columnas con mayúscula (`Anio`, `Mes`, `Periodo`, `valor_FOB`, `Peso_Neto`); `valor_FOB` en USD,
`Peso_Neto` en kg. Muchas celdas por país/subrubro vienen nulas con `s` (secreto estadístico): al sumar,
aclará que el total es un piso.

## Población

```bash
python3 $S get proyecciones_poblacion_nacional_2022_2040 fecha=eq.2026 --select edad,sexo_nom,poblacion --all
python3 $S distinct proyecciones_poblacion_jurisdiccion_2022_2040 jurisdiccion_cod,jurisdiccion_nom
python3 $S get estimaciones_poblacion_departamento_2022_2035 jurisdiccion_cod=eq.<cod> fecha=eq.2025 --all
```

## Ajustar un monto por inflación

1. Traé el índice (no la variación) del IPC nivel general para el período origen y destino.
2. `monto_ajustado = monto × índice_destino / índice_origen`.
3. Si el período destino no está publicado, decilo; no extrapoles sin avisar.

## Llevar una tabla entera a disco

```bash
python3 $S count ipc_nacional
python3 $S get ipc_nacional --all --format ndjson > ipc_nacional.ndjson
```

Con más de ~100 mil filas, filtrá por período: cada página son 1000 filas y una request.
