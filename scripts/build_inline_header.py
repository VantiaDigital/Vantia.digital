"""
BUILD STEP — Inlinea el header directamente en cada HTML.

Por qué: el header se cargaba vía fetch JS (components-loader.js), lo que
causaba que apareciera tarde ("el header tarda en cargar"). Al inlinearlo
en el HTML estático, el header está presente desde el primer byte: instantáneo.

Fuente única de verdad: components/header.html
Cuando edites el header, cambiá components/header.html y re-corré este script:
    python scripts/build_inline_header.py

Idempotente: si ya está inlineado, lo reemplaza por la versión actual.
"""
import re, os

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
HEADER_SRC = os.path.join(ROOT, "components", "header.html")

# Marcadores para encontrar/reemplazar el bloque inlineado en sucesivas corridas
START = "<!-- BUILD:header:start (inlineado por build_inline_header.py — no editar a mano) -->"
END = "<!-- BUILD:header:end -->"

with open(HEADER_SRC, "r", encoding="utf-8") as f:
    header_html = f.read().strip()

INLINE_BLOCK = f"  {START}\n{header_html}\n  {END}"

# Patrón 1: placeholder original
PLACEHOLDER = re.compile(r'[ \t]*<div data-component="header"></div>')
# Patrón 2: bloque ya inlineado (para re-builds)
INLINED = re.compile(re.escape(START) + r'.*?' + re.escape(END), re.DOTALL)
# Preload del header que ya no hace falta (ahora es inline)
PRELOAD = re.compile(r'[ \t]*<link rel="preload" href="/components/header\.html"[^>]*>\s*\n?', re.IGNORECASE)


def html_files(root):
    for dp, _, fns in os.walk(root):
        p = dp.replace(os.sep, '/')
        if any(s in p for s in ('.git', 'node_modules', 'assets', '.claude', 'components')):
            continue
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.join(dp, fn)


changed = 0
for path in html_files(ROOT):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c
    # Quitar preload del header (ya no se fetchea)
    c = PRELOAD.sub("", c)
    # Reemplazar bloque ya inlineado (re-build) o el placeholder original
    if INLINED.search(c):
        c = INLINED.sub(INLINE_BLOCK.replace("\\", "\\\\"), c)
    elif PLACEHOLDER.search(c):
        c = PLACEHOLDER.sub(lambda m: INLINE_BLOCK.replace("\\", "\\\\"), c, count=1)
    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        changed += 1
        print("  inlined header:", path[len(ROOT)+1:])

print(f"\nTotal: {changed} archivos actualizados")
