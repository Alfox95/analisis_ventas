import pandas as pd


def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """
    Carga los datos de ventas desde un archivo CSV.
    """
    df = pd.read_csv(ruta_csv)
    return df


def preparar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte la columna 'fecha' a tipo datetime y añade una columna 'mes'
    con el primer día del mes (útil para agrupar).
    """
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["mes"] = df["fecha"].dt.to_period("M").dt.to_timestamp()
    return df


def agregar_ingresos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna 'ingresos' = cantidad * precio.
    """
    df = df.copy()
    df["ingresos"] = df["cantidad"] * df["precio"]
    return df


def ventas_totales_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula las ventas totales por mes
    (cantidad_total e ingresos_totales).
    """
    df = agregar_ingresos(df)
    resumen = (
        df.groupby("mes", as_index=False)
        .agg(
            cantidad_total=("cantidad", "sum"),
            ingresos_totales=("ingresos", "sum"),
        )
        .sort_values("mes")
    )
    return resumen


def producto_top_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve, para cada mes, el producto más vendido (por cantidad)
    y el ingreso total que generó ese producto en ese mes.
    """
    df = agregar_ingresos(df)
    resumen = (
        df.groupby(["mes", "producto"], as_index=False)
        .agg(
            cantidad_total=("cantidad", "sum"),
            ingresos_totales=("ingresos", "sum"),
        )
    )

    idx_max = resumen.groupby("mes")["cantidad_total"].idxmax()
    top_mes = resumen.loc[idx_max].sort_values("mes")
    return top_mes


def producto_top_periodo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve el producto más vendido en todo el periodo (por cantidad)
    y el ingreso total asociado a ese producto.
    """
    df = agregar_ingresos(df)

    resumen = (
        df.groupby("producto", as_index=False)
        .agg(
            cantidad_total=("cantidad", "sum"),
            ingresos_totales=("ingresos", "sum"),
        )
    )

    idx_max = resumen["cantidad_total"].idxmax()
    top = resumen.loc[[idx_max]]
    return top


def producto_mas_ingresos_periodo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve el producto que más ingresos generó en todo el periodo.
    """
    df = agregar_ingresos(df)

    resumen = (
        df.groupby("producto", as_index=False)
        .agg(
            cantidad_total=("cantidad", "sum"),
            ingresos_totales=("ingresos", "sum"),
        )
    )

    idx_max = resumen["ingresos_totales"].idxmax()
    top = resumen.loc[[idx_max]]
    return top


def producto_mas_ingresos_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve, para cada mes, el producto que más ingresos generó.
    """
    df = agregar_ingresos(df)

    resumen = (
        df.groupby(["mes", "producto"], as_index=False)
        .agg(
            cantidad_total=("cantidad", "sum"),
            ingresos_totales=("ingresos", "sum"),
        )
    )

    idx_max = resumen.groupby("mes")["ingresos_totales"].idxmax()
    top_mes = resumen.loc[idx_max].sort_values("mes")
    return top_mes

