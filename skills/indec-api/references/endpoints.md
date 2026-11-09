# Catálogo de endpoints — API INDEC

<!-- Generado por scripts/gen_endpoints.py desde spec/openapi.json. No editar a mano. -->

Base URL: `https://api.indec.gob.ar/v1/` · Spec: `https://api.indec.gob.ar/api/openapi?v=2` · Versión de spec: 1.0.0

Los nombres de columna son **sensibles a mayúsculas**: copialos tal cual de esta tabla.

## Índice

| Endpoint | Qué es | Dirección INDEC |
|---|---|---|
| [`/ipi_manufacturero`](#ipi_manufacturero) | Índice de producción industrial manufacturero | Dirección de Estadísticas Mineras, Manufactureras, Energéticas y de la Construcción |
| [`/ipi_minero`](#ipi_minero) | Índice de producción industrial minero | Dirección de Estadísticas Mineras, Manufactureras, Energéticas y de la Construcción |
| [`/estimaciones_poblacion_departamento_2022_2035`](#estimaciones_poblacion_departamento_2022_2035) | Estimaciones de población por departamento y sexo | Dirección de Estadísticas Poblacionales |
| [`/proyecciones_poblacion_jurisdiccion_2022_2040`](#proyecciones_poblacion_jurisdiccion_2022_2040) | Proyecciones de población por jurisdicción, sexo y edad | Dirección de Estadísticas Poblacionales |
| [`/proyecciones_poblacion_nacional_2022_2040`](#proyecciones_poblacion_nacional_2022_2040) | Proyecciones nacionales de población por sexo y edad | Dirección de Estadísticas Poblacionales |
| [`/ipc_nacional`](#ipc_nacional) | Índice de Precios al Consumidor (IPC) | Dirección de Índices de Precios de Consumo |
| [`/valorizacion_canastas_cba_cbt`](#valorizacion_canastas_cba_cbt) | Valorización de las canastas básicas (CBA y CBT) | Dirección de Índices de Precios de Consumo |
| [`/indice_salarios`](#indice_salarios) | Índice de salarios | Dirección de Índices de Precios de la Producción |
| [`/icc_precios_construccion`](#icc_precios_construccion) | Índice del costo de la construcción | Dirección de Índices de Precios de la Producción |
| [`/redeterminacion_precios_contratos_obras_publicas`](#redeterminacion_precios_contratos_obras_publicas) | Redeterminación de precios de obras públicas | Dirección de Índices de Precios de la Producción |
| [`/sipm_precios_mayoristas`](#sipm_precios_mayoristas) | Sistema de índices de precios mayoristas | Dirección de Índices de Precios de la Producción |
| [`/estimador-mensual-de-actividad-economica-nivel-general`](#estimador-mensual-de-actividad-economica-nivel-general) | Estimador mensual de actividad económica. Nivel general | Dirección Nacional de Cuentas Nacionales |
| [`/estimador-mensual-de-actividad-economica-sectores`](#estimador-mensual-de-actividad-economica-sectores) | Estimador mensual de actividad económica. Sectores | Dirección Nacional de Cuentas Nacionales |
| [`/pobreza_eph`](#pobreza_eph) | Incidencia de la pobreza y la indigencia (EPH) | Dirección Nacional de Estadísticas de Condiciones de Vida |
| [`/mercado_trabajo_eph`](#mercado_trabajo_eph) | Principales tasas del mercado de trabajo (EPH) | Dirección Nacional de Estadísticas de Condiciones de Vida |
| [`/canasta-crianza`](#canasta-crianza) | Valorización de la canasta de crianza | Dirección Nacional de Estadísticas de Condiciones de Vida |
| [`/comercio_exterior_nomenclaturas`](#comercio_exterior_nomenclaturas) | Códigos y denominaciones de comercio exterior | Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales |
| [`/comercio_exterior_exportacion_bienes`](#comercio_exterior_exportacion_bienes) | Exportaciones de bienes por rubros y países de destino | Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales |
| [`/comercio_exterior_importacion_bienes`](#comercio_exterior_importacion_bienes) | Importaciones de bienes por uso económico y país de origen | Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales |

## ipi_manufacturero

**Índice de producción industrial manufacturero** — Dirección de Estadísticas Mineras, Manufactureras, Energéticas y de la Construcción

Índice de producción industrial manufacturero (IPI manufacturero), nivel general y aperturas por actividad económica, base 2004=100. Incluye las series original, desestacionalizada y tendencia-ciclo, expresadas como números índice y variaciones porcentuales. Este endpoint contiene información desde enero de 2016. Para más información, se puede consultar la metodología INDEC N° 31, Metodología del índice de producción industrial manufacturero, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_ipi_manufacturero_2019.pdf

- Clave primaria (usala completa en `order` para paginar): `periodo,indicador,cuadro_web,codigo_CLaNAE_2004,descripcion,serie,tipo_de_indicador`
- Traer todo: `GET /ipi_manufacturero?order=periodo,indicador,cuadro_web,codigo_CLaNAE_2004,descripcion,serie,tipo_de_indicador&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM para meses |
| `anio` | number |  | Año correspondiente al período de referencia del dato |
| `mes` | number |  | Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `cuadro_web` | string |  | **PK** Número del cuadro estadístico publicado en el sitio web del INDEC al que corresponde el dato |
| `codigo_CLaNAE_2004` | string |  | **PK** Código de Clasificación Nacional de Actividades Económicas 2004 |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `serie` | string |  | **PK** Tipo de serie estadística: original, desestacionalizada o tendencia-ciclo |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o peso promedio |
| `unidad_de_medida` | string |  | Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas. |

## ipi_minero

**Índice de producción industrial minero** — Dirección de Estadísticas Mineras, Manufactureras, Energéticas y de la Construcción

IPI minero nivel general. Series original, desestacionalizada y tendencia-ciclo, base 2016=100. Este endpoint contiene información desde enero de 2017. Para más información, se puede consultar la metodología INDEC N° 41, Índice de producción industrial minero, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_ipi_minero.pdf

- Clave primaria (usala completa en `order` para paginar): `periodo,anio,mes,indicador,cuadro_web,codigo_ClaNAE_2010,codigo_CPC_2_1,serie,descripcion,tipo_de_indicador,unidad_de_medida`
- Traer todo: `GET /ipi_minero?order=periodo,anio,mes,indicador,cuadro_web,codigo_ClaNAE_2010,codigo_CPC_2_1,serie,descripcion,tipo_de_indicador,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM para meses |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `cuadro_web` | string |  | **PK** Número del cuadro estadístico publicado en el sitio web del INDEC al que corresponde el dato |
| `codigo_ClaNAE_2010` | string |  | **PK** Código ClaNAE 2010 |
| `codigo_CPC_2_1` | string |  | **PK** Código CPC 2.1 |
| `serie` | string |  | **PK** Tipo de serie estadística: original, desestacionalizada o tendencia-ciclo |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |

## estimaciones_poblacion_departamento_2022_2035

**Estimaciones de población por departamento y sexo** — Dirección de Estadísticas Poblacionales

Estimaciones de población al 1° de julio de cada año calendario, por sexo y departamento, con base en el Censo Nacional de Población, Hogares y Viviendas 2022. Años 2022-2035. Para más información, se pueden consultar la siguiente documentación metodológica: https://www.indec.gob.ar/ftp/cuadros/publicaciones/estimaciones_departamentos_2022_2035.pdf

- Clave primaria (usala completa en `order` para paginar): `departamento_cod,sexo_cod,fecha`
- Traer todo: `GET /estimaciones_poblacion_departamento_2022_2035?order=departamento_cod,sexo_cod,fecha&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `jurisdiccion_cod` | string |  | Código de dos posiciones que identifica a la jurisdicción de la República Argentina |
| `jurisdiccion_nom` | string |  | Nombre de la jurisdicción de la República Argentina |
| `departamento_cod` | string |  | **PK** Código de cinco posiciones que identifica al departamento, partido o comuna. Las dos primeras corresponden a la jurisdicción y las tres restantes al departamento, partido o comuna |
| `departamento_nom` | string |  | Nombre del departamento, partido o comuna |
| `rmba` | string |  | Indica si la jurisdicción, el departamento o el partido pertenece a la Región Metropolitana de Buenos Aires (RMBA) |
| `sexo_cod` | string |  | **PK** Código que identifica el sexo registrado al nacer |
| `sexo_nom` | string |  | Categoría de sexo registrado al nacer |
| `poblacion` | number | sí | Cantidad de habitantes estimada (2022) o proyectada (2023-2040) para la fecha de referencia |
| `fecha` | string |  | **PK** Año correspondiente a la estimación o proyección de población, referida al 1 de julio |

## proyecciones_poblacion_jurisdiccion_2022_2040

**Proyecciones de población por jurisdicción, sexo y edad** — Dirección de Estadísticas Poblacionales

Estimaciones y proyecciones de población al 1° de julio de cada año calendario, por sexo y grupos de edad, con base en el Censo Nacional de Población, Hogares y Viviendas 2022. Jurisdicciones. Años 2022-2040. Para más información, se pueden consultar la siguiente documentación metodológica: https://www.indec.gob.ar/ftp/cuadros/publicaciones/proyecciones_jurisdicciones_2022_2040.pdf

- Clave primaria (usala completa en `order` para paginar): `jurisdiccion_cod,sexo_cod,edad_cod,fecha`
- Traer todo: `GET /proyecciones_poblacion_jurisdiccion_2022_2040?order=jurisdiccion_cod,sexo_cod,edad_cod,fecha&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `jurisdiccion_cod` | string |  | **PK** Código de dos posiciones que identifica a la jurisdicción de la República Argentina |
| `jurisdiccion_nom` | string |  | Nombre de la jurisdicción de la República Argentina |
| `sexo_cod` | string |  | **PK** Código que identifica el sexo registrado al nacer |
| `sexo_nom` | string |  | Categoría de sexo registrado al nacer |
| `edad_cod` | string |  | **PK** Código que identifica al grupo quinquenal de edad |
| `edad_nom` | string |  | Intervalo de edad de cinco años correspondiente al código informado |
| `poblacion` | number | sí | Cantidad de habitantes estimada (2022) o proyectada (2023-2040) para la fecha de referencia |
| `fecha` | string |  | **PK** Año correspondiente a la estimación o proyección de población, referida al 1 de julio |

## proyecciones_poblacion_nacional_2022_2040

**Proyecciones nacionales de población por sexo y edad** — Dirección de Estadísticas Poblacionales

Estimaciones y proyecciones de población al 1° de julio de cada año calendario, por sexo y edad, con base en el Censo Nacional de Población, Hogares y Viviendas 2022. Total del país. Años 2022-2040. Para más información, se pueden consultar la siguiente documentación metodológica: https://www.indec.gob.ar/ftp/cuadros/publicaciones/proyecciones_nacionales_2022_2040.pdf

- Clave primaria (usala completa en `order` para paginar): `edad,sexo_cod,fecha`
- Traer todo: `GET /proyecciones_poblacion_nacional_2022_2040?order=edad,sexo_cod,fecha&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `edad` | number |  | **PK** Edad de las personas, expresada en años cumplidos |
| `sexo_cod` | string |  | **PK** Código que identifica al sexo registrado al nacer |
| `sexo_nom` | string |  | Categoría de sexo registrado al nacer |
| `poblacion` | number | sí | Cantidad de habitantes estimada (2022) o proyectada (2023-2040) para la fecha de referencia |
| `fecha` | number |  | **PK** Año correspondiente a la estimación o proyección de población, referida al 1 de julio |

## ipc_nacional

**Índice de Precios al Consumidor (IPC)** — Dirección de Índices de Precios de Consumo

Índice de precios al consumidor (IPC) de la República Argentina, con aperturas por región, división, grupo, clase y subclase, desde diciembre de 2016. Para más información, se puede consultar la metodología INDEC N° 32, Índice de precios al consumidor (IPC). Base diciembre 2016=100, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_ipc_nacional_2019.pdf

- Clave primaria (usala completa en `order` para paginar): `clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida`
- Traer todo: `GET /ipc_nacional?order=clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `codigo` | string |  | **PK** Código asignado a la categoría de acuerdo con el clasificador utilizado |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `region` | string |  | **PK** Región estadística a la que corresponde el dato |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## valorizacion_canastas_cba_cbt

**Valorización de las canastas básicas (CBA y CBT)** — Dirección de Índices de Precios de Consumo

Valorización mensual de la canasta básica alimentaria (CBA) y de la canasta básica total (CBT) desde abril de 2016. Gran Buenos Aires. Para más información, se puede consultar la metodología INDEC N° 22, La medición de la pobreza y la indigencia en la Argentina, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/sociedad/EPH_metodologia_22_pobreza.pdf

- Clave primaria (usala completa en `order` para paginar): `clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida`
- Traer todo: `GET /valorizacion_canastas_cba_cbt?order=clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `codigo` | string |  | **PK** Código asignado a la categoría de acuerdo con el clasificador utilizado |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `region` | string |  | **PK** Región estadística a la que corresponde el dato |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## indice_salarios

**Índice de salarios** — Dirección de Índices de Precios de la Producción

El índice de salarios estima la evolución de los salarios pagados en la economía aislando el indicador de variaciones relacionadas con conceptos tales como la cantidad de horas trabajadas, descuentos por ausentismo, premios por productividad y todo otro concepto asociado al desempeño o a las características de los individuos concretos. La serie muestra la evolución de los salarios pagados en los sectores privado registrado y público desde noviembre de 2015. A partir de octubre de 2016 se incorporó la serie del sector privado no registrado y el cálculo del índice de salarios total, que resulta de la agregación de los índices de salarios de los componentes mencionados. Para más información, se puede consultar la metodología INDEC N° 16, Índice de salarios y coeficiente de variación salarial, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/sociedad/cvs_metodologia.pdf

- Clave primaria (usala completa en `order` para paginar): `clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,unidad_de_medida`
- Traer todo: `GET /indice_salarios?order=clasificador,nivel,codigo,descripcion,periodo,anio,mes,indicador,tipo_de_indicador,tipo_de_indicador_descripcion,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `codigo` | string |  | **PK** Código asignado a la categoría de acuerdo con el clasificador utilizado |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## icc_precios_construccion

**Índice del costo de la construcción** — Dirección de Índices de Precios de la Producción

Índice del costo de la construcción (ICC) en el Gran Buenos Aires, base 1993. Este endpoint contiene información desde noviembre de 2015. Para más información, se puede consultar la metodología INDEC N° 9, Índice del Costo de la Construcción en el Gran Buenos Aires, base 1993, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_icc.pdf

- Clave primaria (usala completa en `order` para paginar): `indicador,codigo_apertura,codigo_CPC_1,clasificador,nivel,descripcion,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida`
- Traer todo: `GET /icc_precios_construccion?order=indicador,codigo_apertura,codigo_CPC_1,clasificador,nivel,descripcion,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `codigo_apertura` | string |  | **PK** Código que identifica el nivel de apertura o desagregación del dato |
| `codigo_CPC_1` | string |  | **PK** Código de la Clasificación Central Provisional de Productos (CPC) elaborada por la Organización de las Naciones Unidas. |
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `region` | string |  | **PK** Región estadística a la que corresponde el dato |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## redeterminacion_precios_contratos_obras_publicas

**Redeterminación de precios de obras públicas** — Dirección de Índices de Precios de la Producción

Aperturas del índice del costo de la construcción (ICC) y del índice de precios internos básicos al por mayor (IPIB) utilizadas para la redeterminación periódica de precios de contratos de obra pública, según el Decreto 1295/2002. También incluye indicadores requeridos por el Decreto 634/2003, relativo a las Ampliaciones de Transporte de Energía Eléctrica en Alta Tensión y por Distribución Troncal. Este endpoint contiene información desde diciembre de 2015. Para más información, se puede consultar la información disponible en el sitio web del INDEC :https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-112

- Clave primaria (usala completa en `order` para paginar): `indicador,operativo,inciso,descripcion_inciso,codigo_apertura,clasificador,nivel,descripcion,origen,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida`
- Traer todo: `GET /redeterminacion_precios_contratos_obras_publicas?order=indicador,operativo,inciso,descripcion_inciso,codigo_apertura,clasificador,nivel,descripcion,origen,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `operativo` | string |  | **PK** Operativo estadístico del que proviene el dato |
| `inciso` | string |  | **PK** Código o denominación abreviada del inciso correspondiente al artículo 15 del Decreto 1295/2002 |
| `descripcion_inciso` | string |  | **PK** Denominación del inciso correspondiente al artículo 15 del Decreto 1295/2002 |
| `codigo_apertura` | string |  | **PK** Código que identifica el nivel de apertura o desagregación del dato |
| `codigo_CPC_1` | string | sí | Código de la Clasificación Central Provisional de Productos (CPC) elaborada por la Organización de las Naciones Unidas. |
| `codigo_CIUU_3` | string | sí | Código de la Clasificación Industrial Internacional Uniforme (CIIU), revisión 3 |
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `origen` | string |  | **PK** Origen nacional o importado del producto de referencia |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `region` | string |  | **PK** Región estadística a la que corresponde el dato |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## sipm_precios_mayoristas

**Sistema de índices de precios mayoristas** — Dirección de Índices de Precios de la Producción

El Sistema de índices de precios mayoristas (SIPM) está compuesto por el índice de precios internos al por mayor (IPIM), el índice de precios internos básicos al por mayor (IPIB) y el índice de precios básicos del productor (IPP). Este endpoint contiene información desde diciembre de 2015. Para más información, se puede consultar la metodología INDEC N° 8, Sistema de Índices de Precios Mayoristas, base 1993, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia1_8_sipm.pdf

- Clave primaria (usala completa en `order` para paginar): `operativo,indicador,clasificador,nivel,codigo_apertura,descripcion,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida`
- Traer todo: `GET /sipm_precios_mayoristas?order=operativo,indicador,clasificador,nivel,codigo_apertura,descripcion,periodo,anio,mes,tipo_de_indicador,tipo_de_indicador_descripcion,region,unidad_de_medida&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `operativo` | string |  | **PK** Operativo estadístico del que proviene el dato |
| `indicador` | string |  | **PK** Nombre del indicador estadístico |
| `clasificador` | string |  | **PK** Clasificador utilizado para organizar y codificar las categorías del dato |
| `nivel` | string |  | **PK** Nivel de desagregación de la categoría dentro de la estructura del clasificador |
| `codigo_apertura` | string |  | **PK** Código que identifica el nivel de apertura o desagregación del dato |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o precio promedio |
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `region` | string |  | **PK** Región estadística a la que corresponde el dato |
| `unidad_de_medida` | string |  | **PK** Unidad en la que se expresa el valor del indicador |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## estimador-mensual-de-actividad-economica-nivel-general

**Estimador mensual de actividad económica. Nivel general** — Dirección Nacional de Cuentas Nacionales

Estimador mensual de actividad económica (EMAE), nivel general, base 2004=100. Incluye la serie original, desestacionalizada y tendencia-ciclo, expresadas como números índice y variaciones porcentuales. Este endpoint contiene información desde enero de 2004. Para más información, se puede consultar la metodología INDEC N° 20, Estimador Mensual de Actividad Económica (EMAE), Base año 2004, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_emae_ago_16.pdf

- Clave primaria (usala completa en `order` para paginar): `tipo_de_indicador_descripcion,anio,mes,periodo,tipo_de_indicador`
- Traer todo: `GET /estimador-mensual-de-actividad-economica-nivel-general?order=tipo_de_indicador_descripcion,anio,mes,periodo,tipo_de_indicador&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `tipo_de_indicador_descripcion` | string |  | **PK** Descripción del tipo de indicador |
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o peso promedio |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## estimador-mensual-de-actividad-economica-sectores

**Estimador mensual de actividad económica. Sectores** — Dirección Nacional de Cuentas Nacionales

Estimador mensual de actividad económica (EMAE) por sector de actividad económica, base 2004=100 (serie original). Incluye números índice y variaciones porcentuales interanuales para cada sector desde enero de 2004. Para más información, se puede consultar la metodología INDEC N° 20, Estimador Mensual de Actividad Económica (EMAE), Base año 2004, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_emae_ago_16.pdf

- Clave primaria (usala completa en `order` para paginar): `anio,mes,codigo,descripcion,periodo,tipo_de_indicador`
- Traer todo: `GET /estimador-mensual-de-actividad-economica-sectores?order=anio,mes,codigo,descripcion,periodo,tipo_de_indicador&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `codigo` | string |  | **PK** Código letra de la Clasificación nacional de actividades económicas 2004 (ClaNAE04) |
| `descripcion` | string |  | **PK** Denominación de la categoría correspondiente al código informado |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `tipo_de_indicador` | string |  | **PK** Tipo de cálculo o presentación del indicador, como índice, variación intermensual, variación interanual, variación acumulada, incidencia o peso promedio |
| `valor` | number | sí | Valor del indicador para el período y las categorías informadas |
| `observaciones` | string | sí | Notas necesarias para el valor informado |

## pobreza_eph

**Incidencia de la pobreza y la indigencia (EPH)** — Dirección Nacional de Estadísticas de Condiciones de Vida

Incidencia de la pobreza y la indigencia en hogares y personas a partir de la Encuesta Permanente de Hogares (EPH) para el total de 31 aglomerados urbanos. La información se presenta con frecuencia semestral desde el segundo semestre de 2016. Para más información, se puede consultar la metodología INDEC N° 22, la medición de la pobreza y la indigencia en la Argentina, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/sociedad/metodologia_eph_continua.pdf . Y se puede acceder a los informes técnicos y datos complementarios en: https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-31-58

- Clave primaria (usala completa en `order` para paginar): `area_geografica_nom,periodo`
- Traer todo: `GET /pobreza_eph?order=area_geografica_nom,periodo&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `area_geografica_nom` | string |  | **PK** Denominación del área geográfica a la que corresponde el dato. |
| `area_geografica_cod` | number | sí | Código que identifica el área geográfica a la que corresponde el dato. Ver diseño de registros y estructura para las bases preliminares (hogares y personas) de EPH en https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos . |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAANS (número de semestre) |
| `anio` | number |  | Año correspondiente al período de referencia del dato. |
| `semestre` | number |  | Número del semestre correspondiente al año de referencia. Utiliza los valores 1 (primer semestre) y 2 (segundo semestre). |
| `tasa_pobreza_hogares` | number | sí | Porcentaje de hogares cuyos ingresos se encuentran por debajo de su respectiva línea de pobreza en relación con el total de hogares. |
| `tasa_pobreza_personas` | number | sí | Porcentaje de personas que habitan en hogares cuyos ingresos se encuentran por debajo de su respectiva línea de pobreza en relación con el total de personas. |
| `tasa_indigencia_hogares` | number | sí | Porcentaje de hogares cuyos ingresos se encuentran por debajo de su respectiva línea de indigencia en relación con el total de hogares. |
| `tasa_indigencia_personas` | number | sí | Porcentaje de personas que habitan en hogares cuyos ingresos se encuentran por debajo de su respectiva línea de indigencia en relación con el total de personas. |
| `observaciones` | string | sí | Notas vinculadas a los valores informados. |

## mercado_trabajo_eph

**Principales tasas del mercado de trabajo (EPH)** — Dirección Nacional de Estadísticas de Condiciones de Vida

Principales tasas del mercado de trabajo estimadas a partir de la Encuesta Permanente de Hogares (EPH), correspondientes al total de 31 aglomerados urbanos. Incluye las tasas de actividad, empleo, empleo formal e informal, desocupación, ocupación demandante de empleo y subocupación. La información se presenta con frecuencia trimestral desde el segundo trimestre de 2016. Para más información, se puede consultar la metodología INDEC de la EPH a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/sociedad/metodologia_eph_continua.pdf Y acceder a informes técnicos y datos complementarios en: https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-31-58

- Clave primaria (usala completa en `order` para paginar): `area_geografica_nom,periodo`
- Traer todo: `GET /mercado_trabajo_eph?order=area_geografica_nom,periodo&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `area_geografica_nom` | string |  | **PK** Denominación del área geográfica a la que corresponde el dato. |
| `area_geografica_cod` | number | sí | Código que identifica el área geográfica a la que corresponde el dato. Ver diseño de registros y estructura para las bases preliminares (hogares y personas) de EPH en https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos . |
| `periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAANT (número de trimestre que utiliza valores comprendidos entre 1 Y 4). |
| `anio` | number |  | Año correspondiente al período de referencia del dato. |
| `trimestre` | number |  | Número del trimestre correspondiente al año de referencia. Utiliza valores comprendidos entre 1 (primer trimestre) y 4 (cuarto trimestre). |
| `tasa_de_actividad` | number | sí | Porcentaje de la población económicamente activa con respecto a la población total de referencia. |
| `tasa_de_empleo` | number | sí | Porcentaje de la población ocupada con respecto a la población total de referencia. |
| `tasa_de_empleo_formal` | number | sí | Porcentaje de la población ocupada con empleo formal con respecto a la población total de referencia. |
| `tasa_de_empleo_informal` | number | sí | Porcentaje de la población ocupada con empleo informal con respecto a la población total de referencia. |
| `tasa_de_desocupacion` | number | sí | Porcentaje de la población desocupada con respecto a la población económicamente activa. |
| `tasa_de_ocupacion_demandante` | number | sí | Porcentaje de la población ocupada que busca activamente otra ocupación con respecto a la población económicamente activa. |
| `tasa_de_subocupacion` | number | sí | Porcentaje de la población subocupada con respecto a la población económicamente activa. |
| `tasa_de_subocupacion_demandante` | number | sí | Porcentaje de la población subocupada que busca activamente otra ocupación con respecto a la población económicamente activa. |
| `tasa_de_subocupacion_no_demandante` | number | sí | Porcentaje de la población subocupada que busca activamente otra ocupación con respecto a la población económicamente activa. |
| `observaciones` | string | sí | Notas vinculadas a los valores informados. |

## canasta-crianza

**Valorización de la canasta de crianza** — Dirección Nacional de Estadísticas de Condiciones de Vida

Valorización mensual de la canasta de crianza de la primera infancia, la niñez y la adolescencia. Está conformada por el costo de los bienes y servicios, y la valorización del tiempo de cuidado. La estimación se realiza para cuatro tramos de edad: menores de 1 año, de 1 a 3 años, de 4 a 5 años y de 6 a 12 años. Gran Buenos Aires. Este endpoint contiene información desde enero de 2020. Para más información sobre la canasta de crianza, se puede consultar el siguiente enlace: https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-43-173

- Clave primaria (usala completa en `order` para paginar): `Periodo`
- Traer todo: `GET /canasta-crianza?order=Periodo&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `anio` | number |  | Año correspondiente al período de referencia del dato |
| `Mes` | number |  | Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `Periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `bys_men1` | number | sí | Costo mensual de los bienes y servicios incluidos en la canasta de crianza para menores de 1 año, expresado en pesos argentinos |
| `cuid_men1` | number | sí | Valorización mensual del tiempo de cuidado requerido para menores de 1 año, expresado en pesos argentinos |
| `tot_men1` | number | sí | Valor mensual total de la canasta de crianza para menores de 1 año, expresado en pesos argentinos |
| `bys_1a3` | number | sí | Costo mensual de los bienes y servicios incluidos en la canasta de crianza para niñas y niños de 1 a 3 años, expresado en pesos argentinos |
| `cuid_1a3` | number | sí | Valorización mensual del tiempo de cuidado requerido para niñas y niños de 1 a 3 años, expresado en pesos argentinos |
| `tot_1a3` | number | sí | Valor mensual total de la canasta de crianza para niñas y niños de 1 a 3 años, expresado en pesos argentinos |
| `bys_4a5` | number | sí | Costo mensual de los bienes y servicios incluidos en la canasta de crianza para niñas y niños de 4 a 5 años, expresado en pesos argentinos |
| `cuid_4a5` | number | sí | Valorización mensual del tiempo de cuidado requerido para niñas y niños de 4 a 5 años, expresado en pesos argentinos |
| `tot_4a5` | number | sí | Valor mensual total de la canasta de crianza para niñas y niños de 4 a 5 años, expresado en pesos argentinos |
| `bys_6a12` | number | sí | Costo mensual de los bienes y servicios incluidos en la canasta de crianza para niñas, niños y adolescentes de 6 a 12 años, expresado en pesos argentinos |
| `cuid_6a12` | number | sí | Valorización mensual del tiempo de cuidado requerido para niñas, niños y adolescentes de 6 a 12 años, expresado en pesos argentinos |
| `tot_6a12` | number | sí | Valor mensual total de la canasta de crianza para niñas, niños y adolescentes de 6 a 12 años, expresado en pesos argentinos |

## comercio_exterior_nomenclaturas

**Códigos y denominaciones de comercio exterior** — Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales

Diccionario de códigos y nomenclaturas utilizados en los servicios de datos de comercio exterior de la Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales. Incluye los códigos de país, grandes rubros y subrubros de las exportaciones, y los usos económicos y grandes categorías económicas de las importaciones.

- Clave primaria (usala completa en `order` para paginar): `nombre_columna,codigo`
- Traer todo: `GET /comercio_exterior_nomenclaturas?order=nombre_columna,codigo&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `nombre_columna` | string |  | **PK** Nombre de la columna de los servicios de datos de comercio exterior en la que se utiliza el código |
| `codigo` | string |  | **PK** Código utilizado en la columna indicada de los servicios de datos de comercio exterior |
| `codigo_descripcion` | string |  | Denominación correspondiente al código informado |

## comercio_exterior_exportacion_bienes

**Exportaciones de bienes por rubros y países de destino** — Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales

Exportaciones argentinas de bienes por grandes rubros, subrubros y país de destino desde enero de 1986. Incluye el valor FOB expresado en dólares estadounidenses y el peso neto de las mercaderías expresado en kilogramos. La información se presenta con frecuencia mensual. Se aplican criterios de supresión para resguardar el secreto estadístico y la confidencialidad de la información aduanera. El signo convencional “s” indica que se registraron operaciones, pero el número de operadores fue insuficiente para publicar el valor. Para conocer los códigos de país, rubro y subrubro, se encuentra disponible el servicio de datos llamado “Códigos y nomencladores de comercio exterior” (https://api.indec.gob.ar/v1/comercio_exterior_nomenclaturas). Para más información, se puede consultar la metodología INDEC N° 26, Metodología de comercio exterior, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_comex.pdf

- Clave primaria (usala completa en `order` para paginar): `Anio,Mes,Periodo,rubro_cod,subrubro_cod,pais_cod`
- Traer todo: `GET /comercio_exterior_exportacion_bienes?order=Anio,Mes,Periodo,rubro_cod,subrubro_cod,pais_cod&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `Anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `Mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `Periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `rubro_cod` | string |  | **PK** Código que identifica el rubro al que pertenece la exportación |
| `subrubro_cod` | string |  | **PK** Código de tres posiciones que identifica el subrubro de exportación dentro del rubro correspondiente |
| `pais_cod` | string |  | **PK** Código que identifica el país de origen de las importaciones o de destino de las exportaciones |
| `valor_FOB` | number | sí | Valor de las exportaciones a precios FOB, expresado en dólares estadounidenses |
| `Peso_Neto` | number | sí | Peso neto de los bienes que componen el rubro o subrubro informado, expresado en kilogramos |

## comercio_exterior_importacion_bienes

**Importaciones de bienes por uso económico y país de origen** — Dirección Nacional de Estadísticas del Sector Externo y Cuentas Internacionales

Importaciones argentinas de bienes por uso económico, grandes categorías económica y país de origen. Incluye el valor CIF expresado en dólares estadounidenses y el peso neto de las mercaderías expresado en kilogramos. La información se presenta con frecuencia mensual. Este endpoint contiene información desde enero de 1986. Para conocer los códigos de país, uso económico y gran categoría económica, se encuentra disponible el servicio de datos llamado “Códigos y nomencladores de comercio exterior” (https://api.indec.gob.ar/v1/comercio_exterior_nomenclaturas). Para más información, se puede consultar la metodología INDEC N° 26, Metodología de comercio exterior, a través del siguiente enlace: https://www.indec.gob.ar/ftp/cuadros/economia/metodologia_comex.pdf

- Clave primaria (usala completa en `order` para paginar): `Anio,Mes,Periodo,uso_economico_cod,gce_cod,pais_cod`
- Traer todo: `GET /comercio_exterior_importacion_bienes?order=Anio,Mes,Periodo,uso_economico_cod,gce_cod,pais_cod&limit=1000&offset=0`

| Columna | Tipo | Nulo | Descripción |
|---|---|---|---|
| `Anio` | number |  | **PK** Año correspondiente al período de referencia del dato |
| `Mes` | number |  | **PK** Número del mes correspondiente al período de referencia. Utiliza valores comprendidos entre 1 (enero) y 12 (diciembre) |
| `Periodo` | string |  | **PK** Período de referencia del dato, expresado en formato AAAAMM (meses) |
| `uso_economico_cod` | string |  | **PK** Código que identifica el uso económico de las importaciones |
| `gce_cod` | string |  | **PK** Código que identifica la gran categoría económica dentro del uso económico de importación correspondiente |
| `pais_cod` | string |  | **PK** Código que identifica el país de origen de las importaciones o de destino de las exportaciones |
| `valor_CIF` | number | sí | Valor de las importaciones a precios CIF, expresado en dólares estadounidenses |
| `peso_neto` | number | sí | Peso neto de los bienes que componen el uso económico o categoría económica informada, expresado en kilogramos |
