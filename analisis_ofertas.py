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

# Palabras clave para filtrar accesorios, fundas, piezas y cosas irrelevantes
PALABRAS_ACCESORIOS = [
    "funda", "cover", "cubierta", "protector", "estuche",
    "carcasa", "case", "batería", "soporte", "pen",
    "stylus", "cable", "cargador", "coque", "vidrio templado",
    "pantalla", "alimentador", "fuente", "reproductor", "caja",
    "box", "vacía", "teclado", "placa base", "support",
    "ps2", "ps5", "docomo", "auriculares", "slim rgb",
    "final fantasy", "nintendo ds", "ds lite", "3ds"
]

# Palabras que indican posibles problemas o riesgos
PALABRAS_RIESGO = [
    "roto", "leer", "no funciona", "pantalla rota",
    "defectuoso", "averiado", "no carga", "problema"
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

    # Calcular descuento en porcentaje
    df["Diferencia (%)"] = (1 - df["Precio limpio"] / df["Precio objetivo"]) * 100

    # Filtrar por palabras no deseadas
    mask_dispositivo = ~df["Título"].str.lower().str.contains(
        "|".join(PALABRAS_ACCESORIOS), na=False
    )

    # Filtrar por umbral
    df_filtrado = df[mask_dispositivo & (df["Diferencia (%)"] > umbral_descuento)].copy()

    # Marcar riesgo
    df_filtrado["Riesgo"] = df_filtrado["Título"].str.lower().str.contains(
        "|".join(PALABRAS_RIESGO), na=False
    )
    df_filtrado["Riesgo detectado"] = df_filtrado["Riesgo"].map({True: "⚠️ Sí", False: "✅ No"})

    # Ordenar por mejor descuento
    df_ordenado = df_filtrado.sort_values(by="Diferencia (%)", ascending=False)

    return df_ordenado


if __name__ == "__main__":
    resultado = analizar_ofertas()
    print(resultado[[
        "Producto objetivo", "Título", "Precio limpio",
        "Precio objetivo", "Diferencia (%)", "Riesgo detectado", "Enlace"
    ]].head(10))
