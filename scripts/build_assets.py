"""
BUILD STEP — Minifica CSS y JS a ficheros .min junto al original.

Por que existe: Cloudflare ya sirve todo con Brotli, pero comprimir no
sustituye a minificar. Medido sobre este sitio, quitar espacios y comentarios
recorta otro ~33 % del peso ya comprimido de CSS y JS.

Como funciona: los ficheros que se editan siguen siendo los de siempre
(assets/css/main.css, assets/js/*.js). Este script genera al lado su version
.min y es esa la que enlazan las paginas. Asi el codigo legible no se pierde
y en el repo se sigue viendo el diff de verdad.

    python scripts/build_assets.py

Hay que correrlo despues de tocar cualquier CSS o JS. Si se olvida, el sitio
sigue funcionando: servira la version .min anterior, que es justo el fallo
silencioso a vigilar. Por eso el script avisa cuando el original es mas
reciente que su .min.

No se tocan los ficheros de assets/js/vendor/: ya vienen minificados.
"""
import os
import subprocess
import sys
import gzip

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OBJETIVOS = [
    ("assets/css/main.css", "css"),
    ("assets/css/animations.css", "css"),
    ("assets/js/main.js", "js"),
    ("assets/js/i18n.js", "js"),
    ("assets/js/animations.js", "js"),
    ("assets/js/modal.js", "js"),
    ("assets/js/consent.js", "js"),
    ("assets/js/analytics-events.js", "js"),
    ("assets/js/components-loader.js", "js"),
]

NPX = "npx.cmd" if os.name == "nt" else "npx"


def destino(rel):
    base, ext = os.path.splitext(rel)
    return f"{base}.min{ext}"


def comprimido(ruta):
    """Peso aproximado tal como viaja por la red."""
    with open(ruta, "rb") as f:
        return len(gzip.compress(f.read(), 9))


def main():
    total_antes = total_despues = 0
    fallos = []

    for rel, tipo in OBJETIVOS:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            print(f"  SALTADO  {rel} (no existe)")
            continue
        out = os.path.join(ROOT, destino(rel))

        # Sin --loader: leyendo de un fichero, esbuild deduce el tipo por la
        # extension, y pasarlo explicito da error.
        cmd = [NPX, "--yes", "esbuild@0.24", src, "--minify", f"--outfile={out}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            fallos.append(rel)
            print(f"  ERROR    {rel}: {r.stderr.strip()[:120]}")
            continue

        a, d = comprimido(src), comprimido(out)
        total_antes += a
        total_despues += d
        print(f"  {destino(rel):34s} {a:6d} -> {d:6d} B comprimido  (-{100*(a-d)/a:.0f} %)")

    if fallos:
        print(f"\nFallaron {len(fallos)}: {', '.join(fallos)}")
        return 1

    ahorro = total_antes - total_despues
    print(f"\nTotal comprimido: {total_antes} -> {total_despues} B   "
          f"(-{ahorro} B, {100*ahorro/total_antes:.0f} %)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
