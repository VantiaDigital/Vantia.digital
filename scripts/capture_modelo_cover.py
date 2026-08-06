# -*- coding: utf-8 -*-
"""
Genera la portada WebP de un modelo para la rejilla de "Tu web a medida".

Levanta el modelo en un puerto, lo captura con Chrome sin ventana a 1200x800
y lo guarda en assets/images/modelos/<slug>.webp.

    python scripts/capture_modelo_cover.py despacho "Despacho Web" 8215

Si el puerto ya tiene el modelo servido, se reutiliza.
"""
import io
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELOS = os.path.abspath(os.path.join(ROOT, "..", "Modelos"))
DESTINO = os.path.join(ROOT, "assets", "images", "modelos")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def vivo(puerto):
    try:
        urllib.request.urlopen("http://localhost:%d/" % puerto, timeout=1.5)
        return True
    except (urllib.error.URLError, OSError):
        return False


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    slug, carpeta, puerto = sys.argv[1], sys.argv[2], int(sys.argv[3])

    ruta = os.path.join(MODELOS, carpeta)
    if not os.path.isdir(ruta):
        print("no existe:", ruta)
        return 1

    servidor = None
    if not vivo(puerto):
        servidor = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(puerto),
             "--bind", "127.0.0.1", "--directory", ruta],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(20):
            time.sleep(0.4)
            if vivo(puerto):
                break
        else:
            print("el servidor no arranco")
            return 1

    os.makedirs(DESTINO, exist_ok=True)
    png = os.path.join(DESTINO, slug + ".png")
    webp = os.path.join(DESTINO, slug + ".webp")

    try:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--window-size=1500,1000", "--screenshot=" + png,
             "--virtual-time-budget=5000", "http://localhost:%d/" % puerto],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        if servidor:
            servidor.terminate()

    if not os.path.exists(png):
        print("no se pudo capturar")
        return 1

    from PIL import Image
    im = Image.open(png).convert("RGB")
    # Recorte a 3:2 desde arriba: interesa la parte alta, que es lo que
    # identifica al modelo, no el pie.
    ancho, alto = im.size
    alto_util = min(alto, int(ancho * 2 / 3))
    im = im.crop((0, 0, ancho, alto_util)).resize((1200, 800), Image.LANCZOS)
    im.save(webp, "WEBP", quality=82, method=6)
    os.remove(png)
    print("%s  %.0f KB" % (os.path.relpath(webp, ROOT), os.path.getsize(webp) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
