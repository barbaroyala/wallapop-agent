# Lista de nombres de archivo
archivos = [
    ".gitignore",
    "analisis_ofertas.py",
    "app.py",
    "Busqueda_de_Productos.py",
    "Chrome_Driver.py",
    "Eficiencia_del_Scraping.py",
    "Extraccion_de_Datos.py",
    "guardar_resultados.py",
    "main.py",
    "packages.txt",
    "Procfile",
    "render.yaml",
    "requirements.txt"
]

# Función para leer cada archivo y guardar su contenido en un archivo .txt
def extraer_contenido(archivos):
    with open('contenido_archivos.txt', 'w', encoding='utf-8') as outfile:
        for archivo in archivos:
            try:
                with open(archivo, 'r', encoding='utf-8') as infile:
                    contenido = infile.read()
                    outfile.write(f"=== Contenido de '{archivo}' ===\n")
                    outfile.write(contenido + '\n\n')
            except FileNotFoundError:
                outfile.write(f"=== Archivo '{archivo}' no encontrado ===\n\n")
            except Exception as e:
                outfile.write(f"=== Error al leer '{archivo}': {str(e)} ===\n\n")

# Llamar a la función para extraer el contenido y guardar en un archivo .txt
extraer_contenido(archivos)

print("Contenido extraído y guardado en 'contenido_archivos.txt'")
