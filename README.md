# 🛒 Mercado Libre Scraper

Script en Python que extrae productos de Mercado Libre Chile y los exporta a Excel.

## ¿Qué hace?
- Busca cualquier producto en Mercado Libre Chile
- Extrae título, precio, descuento y link
- Guarda los resultados en un archivo Excel

## Requisitos
- Python 3.12+
- Google Chrome

## Instalación
```bash
pip install -r requirements.txt
playwright install chromium
```

## Uso
```bash
python scraper.py
```
Ingresa el producto que quieres buscar y el script generará un archivo Excel con los resultados.

## Tecnologías
- Playwright
- BeautifulSoup
- OpenPyXL