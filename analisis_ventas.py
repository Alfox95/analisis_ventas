import pandas as pd
import matplotlib.pyplot as plt

# Colores fijos por producto para que sean coherentes en todos los gráficos
PRODUCT_COLORS = {
    "A": "tab:blue",
    "B": "tab:orange",
    "C": "tab:green",
    "D": "tab:red",
    "E": "tab:purple",
    "F": "tab:brown",
    "G": "tab:pink",
}


def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """
    Carga los datos de ventas desde un archivo CSV.

    Parámetros
    ----------
    ruta_csv : str
        Ruta al archivo CSV con las columnas:
        fecha, producto, cantidad, precio

    Devuelve
    --------
    pd.DataFrame
        DataFrame con los datos cargados.
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

    # Para cada mes, nos quedamos con la fila de mayor cantidad_total
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
    
def graficar_dashboard(
    resumen_mensual: pd.DataFrame,
    top_mes_cantidad: pd.DataFrame,
    top_mes_ingresos: pd.DataFrame,
    ruta_png: str,
) -> None:
    """
    Genera un único PNG tipo dashboard (2x2):
    - (1,1) Ingresos por mes + línea de tendencia.
    - (1,2) Producto más vendido por mes (cantidad) con color por producto.
    - (2,1) Torta de ingresos por mes (con totales).
    - (2,2) Torta de unidades vendidas por mes (con totales).
    """
    resumen_mensual = resumen_mensual.copy()
    top_mes_cantidad = top_mes_cantidad.copy()
    top_mes_ingresos = top_mes_ingresos.copy()

    resumen_mensual["mes_str"] = resumen_mensual["mes"].dt.strftime("%Y-%m")
    top_mes_cantidad["mes_str"] = top_mes_cantidad["mes"].dt.strftime("%Y-%m")
    top_mes_ingresos["mes_str"] = top_mes_ingresos["mes"].dt.strftime("%Y-%m")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ax1, ax2, ax3, ax4 = axes.flat

    # 1) Ingresos por mes + línea de tendencia
    ax1.bar(
        resumen_mensual["mes_str"],
        resumen_mensual["ingresos_totales"],
        color="lightgray",
        label="Ingresos",
    )
    ax1.plot(
        resumen_mensual["mes_str"],
        resumen_mensual["ingresos_totales"],
        color="black",
        marker="o",
        label="Tendencia",
    )
    ax1.set_title("Ingresos totales por mes")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Ingresos")
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend()

    # 2) Producto más vendido por mes (cantidad), coloreado por producto
    colors_cant = [
        PRODUCT_COLORS.get(prod, "gray") for prod in top_mes_cantidad["producto"]
    ]
    ax2.bar(
        top_mes_cantidad["mes_str"],
        top_mes_cantidad["cantidad_total"],
        color=colors_cant,
    )
    ax2.set_title("Producto más vendido por mes (cantidad)")
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("Unidades")
    ax2.tick_params(axis="x", rotation=45)
    for x, y, prod in zip(
        top_mes_cantidad["mes_str"],
        top_mes_cantidad["cantidad_total"],
        top_mes_cantidad["producto"],
    ):
        ax2.text(x, y, prod, ha="center", va="bottom")

    # 3) Torta de ingresos por mes
    total_ingresos = resumen_mensual["ingresos_totales"].sum()

    def autopct_ingresos(pct):
        valor = pct * total_ingresos / 100.0
        return f"{pct:0.1f}%\n${valor:0.0f}"

    wedges1, texts1, autotexts1 = ax3.pie(
        resumen_mensual["ingresos_totales"],
        labels=resumen_mensual["mes_str"],
        autopct=autopct_ingresos,
        startangle=90,
    )
    ax3.set_title("Distribución de ingresos por mes")
    ax3.axis("equal")
    fig.text(
        0.25,
        0.02,
        f"Ingresos totales: ${total_ingresos:0.2f}",
        ha="center",
        va="bottom",
    )

    # 4) Torta de unidades vendidas por mes
    total_cantidades = resumen_mensual["cantidad_total"].sum()

    def autopct_cantidades(pct):
        valor = pct * total_cantidades / 100.0
        return f"{pct:0.1f}%\n{valor:0.0f} uds"

    wedges2, texts2, autotexts2 = ax4.pie(
        resumen_mensual["cantidad_total"],
        labels=resumen_mensual["mes_str"],
        autopct=autopct_cantidades,
        startangle=90,
    )
    ax4.set_title("Distribución de unidades vendidas por mes")
    ax4.axis("equal")
    fig.text(
        0.75,
        0.02,
        f"Unidades totales: {total_cantidades:0.0f}",
        ha="center",
        va="bottom",
    )

    fig.suptitle("Dashboard de ventas mensuales", fontsize=16)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(ruta_png, dpi=150)
    plt.close(fig)


def main() -> None:
    # 1. Cargar datos
    ruta = "ventas.csv"
    df = cargar_datos(ruta)

    # 2. Preparar fechas y mostrar información básica
    df = preparar_fechas(df)

    print("Primeras filas del dataset con fechas preparadas:")
    print(df.head(), "\n")

    print("Información del DataFrame:")
    print(df.info(), "\n")

    print("Descriptivo numérico:")
    print(df.describe(), "\n")

    # 3. Calcular ventas totales por mes
    resumen_mensual = ventas_totales_por_mes(df)
    print("Ventas totales por mes (cantidad e ingresos):")
    print(resumen_mensual, "\n")

    # 4. Producto más vendido por mes (por cantidad)
    top_mes_cantidad = producto_top_por_mes(df)
    print("Producto más vendido POR MES (cantidad e ingresos en ese mes):")
    print(top_mes_cantidad, "\n")

    # 5. Producto más vendido en todo el periodo (por cantidad)
    top_periodo_cantidad = producto_top_periodo(df)
    print("Producto más vendido en TODO el periodo (por cantidad):")
    print(top_periodo_cantidad, "\n")

    # 6. Producto con más ingresos en todo el periodo
    top_periodo_ingresos = producto_mas_ingresos_periodo(df)
    print("Producto con MÁS INGRESOS en TODO el periodo:")
    print(top_periodo_ingresos, "\n")

    # 7. Producto con más ingresos por mes
    top_mes_ingresos = producto_mas_ingresos_por_mes(df)
    print("Producto con más ingresos POR MES:")
    print(top_mes_ingresos, "\n")

    # 8. Gráfico único tipo dashboard
    graficar_dashboard(
        resumen_mensual=resumen_mensual,
        top_mes_cantidad=top_mes_cantidad,
        top_mes_ingresos=top_mes_ingresos,
        ruta_png="dashboard_ventas.png",
    )


if __name__ == "__main__":
    main()

