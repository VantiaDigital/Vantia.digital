"""
Descarga capturas de los sitios de cliente vía Microlink API (gratis, 50 req/día).
Outputs en assets/downloads/linkedin/screenshots/.
"""
import os
import urllib.request

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
OUT_DIR = f"{ROOT}/assets/downloads/linkedin/screenshots"

CLIENTS = {
    "gett":         "https://gett.pages.dev/",
    "parrilleros":  "https://loshermanosparrilleros.pages.dev/",
    "estanteria":   "https://la-estanteria.pages.dev/",
}

os.makedirs(OUT_DIR, exist_ok=True)

for name, url in CLIENTS.items():
    print(f"Captura {name}: {url}")
    screenshot_url = (
        "https://api.microlink.io/"
        f"?url={url}"
        "&screenshot=true"
        "&meta=false"
        "&embed=screenshot.url"
        "&viewport.width=1440"
        "&viewport.height=900"
        "&waitForTimeout=3000"
    )
    out_path = f"{OUT_DIR}/{name}.png"
    try:
        urllib.request.urlretrieve(screenshot_url, out_path)
        size = os.path.getsize(out_path)
        print(f"  OK ({size} bytes) -> {out_path}")
    except Exception as e:
        print(f"  ERROR: {e}")
