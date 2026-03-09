from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


PRODUCT_COLORS: Dict[str, str] = {
    "A": "tab:blue",
    "B": "tab:orange",
    "C": "tab:green",
    "D": "tab:red",
    "E": "tab:purple",
    "F": "tab:brown",
    "G": "tab:pink",
}


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

    def autopct_ingresos(pct: float) -> str:
        valor = pct * total_ingresos / 100.0
        return f"{pct:0.1f}%\n${valor:0.0f}"

    ax3.pie(
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

    def autopct_cantidades(pct: float) -> str:
        valor = pct * total_cantidades / 100.0
        return f"{pct:0.1f}%\n{valor:0.0f} uds"

    ax4.pie(
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

