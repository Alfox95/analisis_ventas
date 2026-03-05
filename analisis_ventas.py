import pandas as pd


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


def main() -> None:
    # 1. Cargar datos
    ruta = "ventas.csv"
    df = cargar_datos(ruta)

    # 2. Mostrar información básica para entender el dataset
    print("Primeras filas del dataset:")
    print(df.head(), "\n")

    print("Información del DataFrame:")
    print(df.info(), "\n")

    print("Descriptivo numérico:")
    print(df.describe(), "\n")


if __name__ == "__main__":
    main()

