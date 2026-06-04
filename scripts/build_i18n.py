"""
BUILD STEP — Cablea el sistema i18n (ES/EN) en cada HTML.

Hace, de forma idempotente, en todas las páginas .html del sitio:
  1. Inserta un snippet temprano en <head> que fija el idioma guardado
     (localStorage 'vantia-lang') antes del primer paint.
  2. Inserta el <script src="/assets/js/i18n.js"> junto al resto de scripts.
  3. Sube la versión de assets ?v=6 -> ?v=7 (cache-bust de css/js editados).
  4. Marca el skip-link con data-i18n="a11y.skip".

El contenido traducible del <body> se marca aparte (a mano / por página).
El header se inlinea con scripts/build_inline_header.py (correr ANTES o DESPUÉS,
da igual: tocan regiones distintas).

Correr:  python scripts/build_i18n.py
"""
import os, re

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"

EARLY_MARKER = "<!-- i18n:early"
EARLY_SNIPPET = (
    '  <!-- i18n:early — fija el idioma guardado antes del primer paint -->\n'
    "  <script>try{var l=localStorage.getItem('vantia-lang');"
    "if(l==='en')document.documentElement.lang='en';}catch(e){}</script>\n"
)

CHARSET_RE = re.compile(r'(<meta charset="UTF-8"\s*/?>\s*\n)', re.IGNORECASE)
SKIP_RE = re.compile(r'(<a class="skip-link" href="#main")(>)')
LOADER_RE = re.compile(r'([ \t]*)(<script src="/assets/js/components-loader\.js\?v=\d+" defer></script>)')
I18N_LINE = '<script src="/assets/js/i18n.js?v=7" defer></script>'


def html_files(root):
    for dp, _, fns in os.walk(root):
        p = dp.replace(os.sep, '/')
        if any(s in p for s in ('/.git', '/.claude', '/assets', '/components', '/scripts', '/node_modules')):
            continue
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.join(dp, fn)


changed = 0
for path in html_files(ROOT):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    # 3. Cache-bust ?v=6 -> ?v=7 (css/js)
    c = c.replace('?v=6"', '?v=7"')

    # 1. Snippet temprano de idioma (idempotente)
    if EARLY_MARKER not in c:
        c = CHARSET_RE.sub(lambda m: m.group(1) + EARLY_SNIPPET, c, count=1)

    # 2. Include de i18n.js junto a components-loader (idempotente)
    if '/assets/js/i18n.js' not in c:
        c = LOADER_RE.sub(lambda m: m.group(1) + I18N_LINE + '\n' + m.group(1) + m.group(2), c, count=1)

    # 4. skip-link traducible (idempotente)
    if 'class="skip-link"' in c and 'skip-link" href="#main" data-i18n' not in c:
        c = SKIP_RE.sub(r'\1 data-i18n="a11y.skip"\2', c, count=1)

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        changed += 1
        print("  i18n wired:", path[len(ROOT) + 1:])

print(f"\nTotal: {changed} archivos actualizados")
