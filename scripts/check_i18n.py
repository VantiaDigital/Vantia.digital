"""
CHECK — Cruza las claves data-i18n* usadas en el HTML contra el diccionario EN
de assets/js/i18n.js. Reporta:
  - MISSING: claves usadas en HTML que NO están en el diccionario (caerían a ES).
  - ORPHAN: claves del diccionario que no se usan en ningún HTML (informativo).

Correr:  python scripts/check_i18n.py
"""
import os, re

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
I18N = os.path.join(ROOT, "assets", "js", "i18n.js")

# 1) Claves del diccionario (líneas tipo  "clave": "valor"  o  'clave': '...')
with open(I18N, "r", encoding="utf-8") as f:
    js = f.read()
dict_keys = set(re.findall(r'^\s*["\']([A-Za-z0-9_.]+)["\']\s*:', js, re.M))
# quitar claves que no son de traducción (ninguna esperada, pero por si acaso)

# 2) Claves usadas en HTML
ATTR_RE = re.compile(r'data-i18n(?:-content|-placeholder|-aria-label|-title)?="([^"]+)"')

def html_files(root):
    for dp, _, fns in os.walk(root):
        p = dp.replace(os.sep, '/')
        if any(s in p for s in ('/.git', '/.claude', '/node_modules', '/scripts')):
            continue
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.join(dp, fn)

used = {}  # key -> [files]
for path in html_files(ROOT):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    rel = path[len(ROOT) + 1:].replace(os.sep, '/')
    for key in ATTR_RE.findall(c):
        used.setdefault(key, set()).add(rel)

used_keys = set(used.keys())

missing = sorted(k for k in used_keys if k not in dict_keys)
orphan = sorted(k for k in dict_keys if k not in used_keys)

print(f"Dict keys (EN):      {len(dict_keys)}")
print(f"Keys used in HTML:   {len(used_keys)}")
print()
if missing:
    print(f"!! MISSING ({len(missing)}) — usadas en HTML, faltan en el diccionario:")
    for k in missing:
        print(f"   - {k}   ({', '.join(sorted(used[k]))})")
else:
    print("OK — todas las claves usadas en HTML existen en el diccionario.")
print()
if orphan:
    print(f"~ ORPHAN ({len(orphan)}) — en el diccionario, no usadas en HTML (informativo):")
    for k in orphan:
        print(f"   - {k}")
else:
    print("OK — sin claves huérfanas.")
