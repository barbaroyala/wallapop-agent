import requests
from bs4 import BeautifulSoup

def buscar_productos_sin_driver(producto_objetivo):
    url = f"https://es.wallapop.com/app/search?keywords={producto_objetivo}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Error al obtener resultados")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    productos = []
    for link in soup.select('a[href^="/item/"]'):
        titulo = link.find("img").get("alt") if link.find("img") else "Sin título"
        precio_tag = link.find("strong", {"aria-label": "Item price"})
        precio = precio_tag.text.strip() if precio_tag else "N/A"
        href = link.get("href")
        enlace = f"https://es.wallapop.com{href}" if href else "N/A"

        productos.append({
            "Título": titulo,
            "Precio": precio,
            "Enlace": enlace,
            "Producto objetivo": producto_objetivo
        })

    return productos
