# Análisis de ventas con Python

Proyecto de práctica para aprender análisis de datos con **Python**, usando **pandas** para manipular datos y **matplotlib / seaborn** para visualizaciones.

Trabajamos con un archivo CSV de ejemplo (`ventas.csv`) que contiene:

- `fecha`: fecha de la venta (YYYY-MM-DD)
- `producto`: identificador del producto (A, B, C, D, E)
- `cantidad`: unidades vendidas
- `precio`: precio unitario

## Objetivos del análisis

- Calcular **ventas totales por mes**.
- Encontrar:
  - **Producto más vendido** (en cantidad).
  - **Producto con mayores ingresos** (cantidad × precio).
- Generar visualizaciones:
  - Gráfico de ventas por mes.
  - Gráfico de ventas por producto (top 5).

## Requisitos

- Python 3.10+ (recomendado)
- Dependencias (incluidas en `requirements.txt`):
  - `pandas`
  - `matplotlib`
  - `seaborn`

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el análisis

Desde la carpeta del proyecto:

```bash
python analisis_ventas.py
```

El script:

1. Carga los datos desde `ventas.csv` usando `pandas`.
2. Muestra información básica del DataFrame (primeras filas, tipos de datos, estadísticas).
3. (Próximos pasos) Calculará métricas de ventas y generará gráficos.

## Notas de aprendizaje

Este proyecto está pensado como ejercicio introductorio para:

- Practicar lectura de CSVs con `pandas`.
- Aprender a agrupar y resumir datos (groupby).
- Crear gráficos simples con `matplotlib` / `seaborn`.
- Practicar un flujo de trabajo básico con Git y GitHub.

