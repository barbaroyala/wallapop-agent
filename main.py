import pandas as pd
import time
from Busqueda_de_Productos import buscar_productos
from analisis_ofertas import PALABRAS_RIESGO

def ejecutar_agente(productos_personalizados=None):
    dfs = []

    if productos_personalizados:
        productos = productos_personalizados
    else:
        print("⚠️ No se ingresó ningún producto.")
        return

    for producto in productos:
        print(f"\n🔍 Buscando: {producto}")
        t0 = time.time()
        df = buscar_productos(producto)
        t1 = time.time()

        print(f"📦 {len(df)} productos detectados para: {producto}")
        print(f"⏱️ Duración: {round(t1 - t0, 2)} segundos")

        if not df.empty:
            dfs.append(df)
        else:
            print(f"❌ No se obtuvieron datos para: {producto}")

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv("resultados_wallapop.csv", index=False, encoding="utf-8-sig")
        print("✅ Guardado resultados_wallapop.csv")

        analizar_con_estrategia_dinamica("resultados_wallapop.csv")
    else:
        print("⚠️ No se guardó ningún resultado.")

def analizar_con_estrategia_dinamica(path_csv):
    df = pd.read_csv(path_csv)

    # Precio limpio
    df["Precio limpio"] = (
        df["Precio"].str.replace("€", "").str.replace(",", ".").str.strip()
    )
    df["Precio limpio"] = pd.to_numeric(df["Precio limpio"], errors="coerce")

    # Precio objetivo dinámico
    precio_promedio = df["Precio limpio"].mean()
    df["Precio objetivo"] = precio_promedio
    df["Diferencia (%)"] = (1 - df["Precio limpio"] / precio_promedio) * 100

    # Riesgo
    df["Riesgo"] = df["Título"].str.lower().str.contains("|".join(PALABRAS_RIESGO), na=False)
    df["Riesgo detectado"] = df["Riesgo"].map({True: "⚠️ Sí", False: "✅ No"})

    # Guardar resultados
    df.to_csv("ofertas_filtradas.csv", index=False, encoding="utf-8-sig")
    print("✅ Guardado ofertas_filtradas.csv con estrategia dinámica")

if __name__ == "__main__":
    ejecutar_agente(["iPhone XR"])
