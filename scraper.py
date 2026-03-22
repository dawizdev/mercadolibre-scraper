import asyncio
from playwright.async_api import async_playwright
import openpyxl

async def scraper_mercadolibre(producto, cantidad=20):
    async with async_playwright() as p:
        # Abrir navegador (False = visible, True = invisible)
        navegador = await p.chromium.launch(headless=False)
        pagina = await navegador.new_page()

        print(f"🔍 Buscando: {producto}")
        
        # Ir a Mercado Libre
        await pagina.goto(f"https://listado.mercadolibre.cl/{producto}")
        
        # Esperar que carguen los productos
        try:
            await pagina.wait_for_selector("li.ui-search-layout__item", timeout=30000)
        except asyncio.TimeoutError:
            print("⚠️ La página tardó mucho en cargar, intentando de todas formas...")
        
        # Extraer datos
        items = await pagina.query_selector_all("li.ui-search-layout__item")
        print(f"✅ Se encontraron {len(items)} productos")

        resultados = []
        for item in items[:cantidad]:
            # Título
            titulo_tag = await item.query_selector("a.poly-component__title")
            titulo = await titulo_tag.inner_text() if titulo_tag else "Sin título"

            # Precio
            precio_tag = await item.query_selector("span.andes-money-amount__fraction")
            precio = await precio_tag.inner_text() if precio_tag else "Sin precio"

            # Link
            link = await titulo_tag.get_attribute("href") if titulo_tag else "Sin link"

            # Descuento
            descuento_tag = await item.query_selector("span.poly-price__disc_label")
            descuento = await descuento_tag.inner_text() if descuento_tag else "Sin descuento"

            resultados.append([titulo, precio, descuento, link])
            print(f"📦 {titulo[:50]} | ${precio} | {descuento}")

        await navegador.close()
        return resultados

def guardar_excel(resultados, nombre_archivo="resultados.xlsx"):
    # Crear archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Encabezados
    ws.append(["Título", "Precio (CLP)", "Descuento", "Link"])

    # Datos
    for fila in resultados:
        ws.append(fila)

    wb.save(nombre_archivo)
    print(f"✅ Excel guardado como: {nombre_archivo}")

# --- PROGRAMA PRINCIPAL ---
async def main():
    producto = input("¿Qué producto quieres buscar? ")
    resultados = await scraper_mercadolibre(producto, cantidad=20)
    guardar_excel(resultados, f"mercadolibre_{producto}.xlsx")
    print(f"\n✅ Listo! Se guardaron {len(resultados)} productos en el Excel.")

asyncio.run(main())
