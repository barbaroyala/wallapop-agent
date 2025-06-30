import pandas as pd
import time
from Busqueda_de_Productos import buscar_productos
from analisis_ofertas import analizar_ofertas

# Productos definidos en la estrategia
productos = [
    "iPhone 11",
    "Galaxy S8",
    "Nintendo DSi XL",
    "Galaxy Tab S6 Lite",
    "Lenovo Tab M10",
    "PS3 Slim"
]

def ejecutar_agente():
    dfs = []

    for producto in productos:
        print(f"\n🔍 Buscando: {producto}")
        t0 = time.time()
        df = buscar_productos(producto)
        t1 = time.time()

        if not df.empty:
            dfs.append(df)
            print(f"📦 {len(df)} productos detectados para: {producto}")
        else:
            print(f"⚠️ Sin resultados para: {producto}")

        print(f"⏱️ Duración: {round(t1 - t0, 2)} segundos")

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv("resultados_wallapop.csv", index=False, encoding="utf-8-sig")
        print("✅ Guardado resultados_wallapop.csv")

        ofertas = analizar_ofertas("resultados_wallapop.csv")
        ofertas.to_csv("ofertas_filtradas.csv", index=False, encoding="utf-8-sig")
        print("✅ Guardado ofertas_filtradas.csv")
    else:
        print("⚠️ No se guardó ningún resultado.")

if __name__ == "__main__":
    ejecutar_agente()
