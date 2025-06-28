import pandas as pd

# Estrategia de reventa
ESTRATEGIA = {
    "iPhone 11": 200,
    "Galaxy S8": 110,
    "Nintendo DSi XL": 60,
    "Galaxy Tab S6 Lite": 150,
    "Lenovo Tab M10": 100,
    "PS3 Slim": 67
}

# Palabras clave para filtrar accesorios, partes, versiones incorrectas y juegos
PALABRAS_ACCESORIOS = [
    "funda", "cover", "cubierta", "protector", "estuche", "carcasa", "case",
    "batería", "soporte", "pen", "stylus", "cable", "cargador", "coque",
    "vidrio templado", "pantalla", "alimentador", "fuente", "reproductor",
    "caja", "box", "vacía", "teclado", "placa base", "support", "blu-ray",
    "conector", "custodia", "auriculares",
    "ps2", "ps4", "ps5", "s8 plus", "s9", "s4", "docomo",
    "final fantasy", "nintendo ds", "ds lite", "3ds",
    "layton", "basketball", "fifa", "lotería", "mario",
    "tab lenovo", "tablet lenovo", "tableta lenovo", "tablet samsung",
    "tablet pc", "tab s6 lite", "samsung tab", "tab m10",
    "pro max", "pro max", "pro", "plus"
]

# Palabras clave que indican posible riesgo de estado defectuoso
PALABRAS_RIESGO = [
    "roto", "leer", "no funciona", "pantalla rota", "defectuoso",
    "averiado", "no carga", "problema", "sin funcionar",
    "no enciende", "no da señales de vida"
]

def analizar_ofertas(path_csv="resultados_wallapop.csv", umbral_descuento=20.0):
    df = pd.read_csv(path_csv)

    # Limpieza de precios
    df["Precio limpio"] = (
        df["Precio"].str.replace("€", "")
        .str.replace(",", ".")
        .str.strip()
    )
    df["Precio limpio"] = pd.to_numeric(df["Precio limpio"], errors="coerce")

    # Asignar precio objetivo
    df["Precio objetivo"] = df["Producto objetivo"].map(ESTRATEGIA)
    df.dropna(subset=["Precio limpio", "Precio objetivo"], inplace=True)

    # Calcular descuento
    df["Diferencia (%)"] = (1 - df["Precio limpio"] / df["Precio objetivo"]) * 100

    # Filtrar por palabras no deseadas
    mask_dispositivo = ~df["Título"].str.lower().str.contains(
        "|".join(PALABRAS_ACCESORIOS), na=False
    )

    # Aplicar umbral de descuento y limpiar
    df_filtrado = df[mask_dispositivo & (df["Diferencia (%)"] > umbral_descuento)].copy()

    # Marcar riesgo
    df_filtrado["Riesgo"] = df_filtrado["Título"].str.lower().str.contains(
        "|".join(PALABRAS_RIESGO), na=False
    )
    df_filtrado["Riesgo detectado"] = df_filtrado["Riesgo"].map({True: "⚠️ Sí", False: "✅ No"})

    # Ordenar
    df_ordenado = df_filtrado.sort_values(by="Diferencia (%)", ascending=False)

    return df_ordenado


if __name__ == "__main__":
    resultado = analizar_ofertas()
    print(resultado[[
        "Producto objetivo", "Título", "Precio limpio",
        "Precio objetivo", "Diferencia (%)", "Riesgo detectado", "Enlace"
    ]].head(10))
