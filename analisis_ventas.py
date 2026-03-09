from analisis import (
    cargar_datos,
    preparar_fechas,
    ventas_totales_por_mes,
    producto_top_por_mes,
    producto_top_periodo,
    producto_mas_ingresos_periodo,
    producto_mas_ingresos_por_mes,
)
from graficos import graficar_dashboard


def generar_informe_texto(
    resumen_mensual,
    top_mes_cantidad,
    top_periodo_cantidad,
    top_periodo_ingresos,
    ruta_informe: str,
) -> None:
    """
    Genera un informe de texto con los resultados principales del análisis.
    """
    lineas: list[str] = []

    lineas.append("INFORME DE ANALISIS DE VENTAS")
    lineas.append("=" * 40)
    lineas.append("")

    lineas.append("Ventas totales por mes:")
    for _, fila in resumen_mensual.iterrows():
        mes_str = fila["mes"].strftime("%Y-%m")
        lineas.append(
            f"- {mes_str}: {fila['cantidad_total']} uds, "
            f"ingresos ${fila['ingresos_totales']:.2f}"
        )

    lineas.append("")
    lineas.append("Producto mas vendido por mes (por cantidad):")
    for _, fila in top_mes_cantidad.iterrows():
        mes_str = fila["mes"].strftime("%Y-%m")
        lineas.append(
            f"- {mes_str}: producto {fila['producto']} "
            f"({fila['cantidad_total']} uds, "
            f"ingresos ${fila['ingresos_totales']:.2f})"
        )

    lineas.append("")
    lineas.append("Resumen del periodo completo:")
    prod_cant = top_periodo_cantidad.iloc[0]
    lineas.append(
        f"- Producto mas vendido en el periodo: {prod_cant['producto']} "
        f"({prod_cant['cantidad_total']} uds, "
        f"ingresos ${prod_cant['ingresos_totales']:.2f})"
    )

    prod_ing = top_periodo_ingresos.iloc[0]
    lineas.append(
        f"- Producto con mayores ingresos en el periodo: {prod_ing['producto']} "
        f"({prod_ing['cantidad_total']} uds, "
        f"ingresos ${prod_ing['ingresos_totales']:.2f})"
    )

    lineas.append("")
    lineas.append("Grafico generado: dashboard_ventas.png")

    with open(ruta_informe, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))


def generar_informe_html(
    resumen_mensual,
    top_mes_cantidad,
    top_periodo_cantidad,
    top_periodo_ingresos,
    ruta_html: str,
) -> None:
    """
    Genera un informe HTML sencillo con tablas y el dashboard embebido.
    """
    partes: list[str] = []

    partes.append("<!DOCTYPE html>")
    partes.append("<html lang='es'>")
    partes.append("<head>")
    partes.append("<meta charset='utf-8' />")
    partes.append("<title>Informe de análisis de ventas</title>")
    partes.append("</head>")
    partes.append("<body>")
    partes.append("<h1>Informe de análisis de ventas</h1>")

    # Ventas totales por mes
    partes.append("<h2>Ventas totales por mes</h2>")
    partes.append("<table border='1' cellspacing='0' cellpadding='4'>")
    partes.append("<tr><th>Mes</th><th>Cantidad total</th><th>Ingresos totales</th></tr>")
    for _, fila in resumen_mensual.iterrows():
        mes_str = fila["mes"].strftime("%Y-%m")
        partes.append(
            f"<tr><td>{mes_str}</td>"
            f"<td>{fila['cantidad_total']}</td>"
            f"<td>${fila['ingresos_totales']:.2f}</td></tr>"
        )
    partes.append("</table>")

    # Producto más vendido por mes
    partes.append("<h2>Producto más vendido por mes (por cantidad)</h2>")
    partes.append("<table border='1' cellspacing='0' cellpadding='4'>")
    partes.append(
        "<tr><th>Mes</th><th>Producto</th><th>Cantidad</th><th>Ingresos</th></tr>"
    )
    for _, fila in top_mes_cantidad.iterrows():
        mes_str = fila["mes"].strftime("%Y-%m")
        partes.append(
            f"<tr><td>{mes_str}</td>"
            f"<td>{fila['producto']}</td>"
            f"<td>{fila['cantidad_total']}</td>"
            f"<td>${fila['ingresos_totales']:.2f}</td></tr>"
        )
    partes.append("</table>")

    # Resumen del periodo
    partes.append("<h2>Resumen del periodo completo</h2>")
    prod_cant = top_periodo_cantidad.iloc[0]
    prod_ing = top_periodo_ingresos.iloc[0]
    partes.append("<ul>")
    partes.append(
        "<li>"
        f"Producto más vendido en el periodo: <strong>{prod_cant['producto']}</strong> "
        f"({prod_cant['cantidad_total']} uds, "
        f"ingresos ${prod_cant['ingresos_totales']:.2f})"
        "</li>"
    )
    partes.append(
        "<li>"
        f"Producto con mayores ingresos en el periodo: <strong>{prod_ing['producto']}</strong> "
        f"({prod_ing['cantidad_total']} uds, "
        f"ingresos ${prod_ing['ingresos_totales']:.2f})"
        "</li>"
    )
    partes.append("</ul>")

    # Imagen del dashboard
    partes.append("<h2>Dashboard de ventas</h2>")
    partes.append("<p>Gráfico generado desde el script Python:</p>")
    partes.append("<img src='dashboard_ventas.png' alt='Dashboard de ventas' />")

    partes.append("</body></html>")

    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))


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

    # 9. Informe en texto plano
    generar_informe_texto(
        resumen_mensual=resumen_mensual,
        top_mes_cantidad=top_mes_cantidad,
        top_periodo_cantidad=top_periodo_cantidad,
        top_periodo_ingresos=top_periodo_ingresos,
        ruta_informe="informe_ventas.txt",
    )

    # 10. Informe HTML
    generar_informe_html(
        resumen_mensual=resumen_mensual,
        top_mes_cantidad=top_mes_cantidad,
        top_periodo_cantidad=top_periodo_cantidad,
        top_periodo_ingresos=top_periodo_ingresos,
        ruta_html="informe_ventas.html",
    )


if __name__ == "__main__":
    main()

