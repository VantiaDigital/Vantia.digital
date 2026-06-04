# -*- coding: utf-8 -*-
"""
3 posts long-form de LinkedIn, uno por servicio, LISTOS PARA SUBIR.
Por cada servicio crea assets/downloads/linkedin/posts-servicios/NN-slug/ con:
  - texto.txt   -> caption para copiar/pegar
  - imagen.png  -> foto simple de respaldo (1080x1350): ícono del servicio (línea, cobre)
                   sobre fondo de marca + nombre del servicio. Poco texto, algo que sustente.
Sistema visual: paleta Vantia + Fraunces/Inter. Tuteo España, cero emojis.
Correr: python scripts/generate_linkedin_servicios.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/linkedin/posts-servicios"

DEEP = (26, 24, 19, 255)
OLIVE = (60, 58, 47, 255)
CREAM = (236, 232, 216, 255)
COPPER = (193, 131, 75, 255)
MUTED = (169, 155, 128, 255)
BG = {"dark": DEEP, "crema": CREAM, "olive": OLIVE}

W, H, PAD = 1080, 1350, 100
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012
_F = {}


def font(fam, size):
    k = (fam, size)
    if k not in _F:
        _F[k] = ImageFont.truetype(FRAUNCES if fam == "fraunces" else INTER, size)
    return _F[k]


def measure(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1], b


def draw_logo(d, x, y, h, v, a):
    s = h / VBOX_H
    d.polygon([(x + px * s, y + py * s) for px, py in V_PATH], fill=v)
    d.polygon([(x + px * s, y + py * s) for px, py in A_PATH], fill=a)


def footer(d, dark):
    logo_h = 46
    logo_w = VBOX_W * (logo_h / VBOX_H)
    text = "Vantia Digital"
    f = font("fraunces", 30)
    tw, th, b = measure(d, text, f)
    sx = (W - (logo_w + 18 + tw)) / 2
    y = H - 95
    col = CREAM if dark else DEEP
    draw_logo(d, sx, y - logo_h / 2, logo_h, col, COPPER)
    d.text((sx + logo_w + 18, y - th / 2 - b[1]), text, font=f, fill=col)


# ── Íconos de línea (mismos conceptos que la web), dibujados con primitivas ──
def icon_web(d, cx, cy, col, w=11):
    # capas / stack: rombo superior + dos chevrons
    top = [(cx, cy - 130), (cx + 155, cy - 45), (cx, cy + 40), (cx - 155, cy - 45), (cx, cy - 130)]
    d.line(top, fill=col, width=w, joint="curve")
    d.line([(cx - 155, cy + 5), (cx, cy + 90), (cx + 155, cy + 5)], fill=col, width=w, joint="curve")
    d.line([(cx - 155, cy + 60), (cx, cy + 145), (cx + 155, cy + 60)], fill=col, width=w, joint="curve")


def icon_seo(d, cx, cy, col, w=12):
    # lupa
    r = 120
    oy = -40
    d.ellipse([cx - r, cy - r + oy, cx + r, cy + r + oy], outline=col, width=w)
    hx, hy = cx + r * 0.72, cy + r * 0.72 + oy
    d.line([(hx, hy), (hx + 95, hy + 95)], fill=col, width=w + 3)


def icon_ads(d, cx, cy, col, w=12):
    # flecha de crecimiento (línea ascendente + esquina-flecha arriba a la derecha)
    pts = [(cx - 165, cy + 95), (cx - 55, cy - 15), (cx + 25, cy + 65), (cx + 165, cy - 100)]
    d.line(pts, fill=col, width=w, joint="curve")
    ax, ay = cx + 165, cy - 100
    d.line([(ax - 78, ay), (ax, ay)], fill=col, width=w, joint="curve")
    d.line([(ax, ay), (ax, ay + 78)], fill=col, width=w, joint="curve")


ICONS = {"web": icon_web, "seo": icon_seo, "ads": icon_ads}


def render_card(p, path):
    dark = p["bg"] in ("dark", "olive")
    fg = CREAM if dark else DEEP
    img = Image.new("RGBA", (W, H), BG[p["bg"]])
    d = ImageDraw.Draw(img)

    # eyebrow
    ey = font("inter", 24)
    label = " ".join(list(p["eyebrow"]))
    lw, lh, lb = measure(d, label, ey)
    d.text(((W - lw) / 2, 235 - lb[1]), label, font=ey, fill=COPPER)
    d.rectangle([(W / 2 - 35, 235 + lh + 18), (W / 2 + 35, 235 + lh + 22)], fill=COPPER)

    # ícono
    ICONS[p["icon"]](d, W / 2, 600, COPPER)

    # nombre del servicio (auto-fit a una línea), acento cobre
    name, accent = p["name"], p.get("accent")
    size = 64
    while size > 38:
        f = font("fraunces", size)
        if measure(d, name, f)[0] <= W - 2 * PAD:
            break
        size -= 3
    f = font("fraunces", size)
    nw, nh, nb = measure(d, name, f)
    x0, ny = (W - nw) / 2, 880
    if accent and accent in name:
        pre, post_ = name.split(accent, 1)
        wpre = measure(d, pre, f)[0]
        wacc = measure(d, accent, f)[0]
        d.text((x0, ny - nb[1]), pre, font=f, fill=fg)
        d.text((x0 + wpre, ny - nb[1]), accent, font=f, fill=COPPER)
        d.text((x0 + wpre + wacc, ny - nb[1]), post_, font=f, fill=fg)
    else:
        d.text((x0, ny - nb[1]), name, font=f, fill=fg)

    footer(d, dark)
    img.save(path, "PNG", optimize=True)


# ─────────────────────────── DATA: 3 SERVICIOS ───────────────────────────
POSTS = [
    dict(n=1, slug="optimizacion-web", bg="dark", icon="web",
         eyebrow="SERVICIO 01", name="Optimización Web + CRO", accent="CRO",
         photo="Imagen lista: ícono de marca. Mejor aún (swap): una captura real de PageSpeed Insights en verde.",
         caption="""Tu web puede cargar en un segundo y, aun así, no venderte nada.

La velocidad es la mitad del trabajo. La otra mitad es la conversión.

Una web rápida que no convierte sigue siendo dinero perdido: pagaste por traer a esa persona y se fue sin hacer nada.

Por eso, cuando optimizamos una web, trabajamos las dos capas.

La técnica: que cargue rápido, que se vea bien en el móvil, que Google la entienda. Son los Core Web Vitals, las métricas con las que Google decide si tu web sirve.

Y la de conversión, el CRO: qué pasa una vez que la página carga. Dónde se frena la gente, dónde abandona, qué versión de un titular o un formulario hace que más visitas terminen en clientes.

Cómo lo hacemos:

— Auditoría técnica real (Lighthouse, PageSpeed): el diagnóstico de cómo está hoy.
— Optimización de velocidad: imágenes, código, carga. Rápida de verdad, no en teoría.
— CRO: mapas de calor y grabaciones de sesión, y tests A/B sobre lo que importa. No asumimos qué convierte; lo medimos.

El resultado no es "una web más bonita". Es una web que trabaja: que convierte más de la gente que ya estás trayendo.

Antes de gastar otro euro en traer tráfico, pregúntate qué hace tu web con el que ya recibe.

¿Sabes qué porcentaje de tus visitas termina en contacto? Te lo miramos gratis.

#OptimizacionWeb #CRO #CoreWebVitals #PYMES #MarketingDeResultados"""),

    dict(n=2, slug="seo-geo", bg="crema", icon="seo",
         eyebrow="SERVICIO 02", name="SEO Técnico + GEO", accent="GEO",
         photo="Imagen lista: ícono de marca. Mejor aún (swap): captura real de una respuesta de ChatGPT/Perplexity citando a un cliente, o de Search Console.",
         caption="""Que te encuentren ya no es solo salir en Google. Es salir cuando alguien le pregunta a una IA.

Durante años, que te encontraran significaba aparecer en Google.

Hoy hay un segundo frente: cada vez más gente le pregunta directamente a ChatGPT, Perplexity o Gemini "¿qué [tu sector] me recomiendas?".

Y la IA responde con tres o cuatro nombres. Si no estás, para ese cliente no existes.

Por eso trabajamos los dos a la vez: SEO técnico y GEO.

SEO técnico es cómo Google entiende tu web: estructura, código limpio, schema, velocidad, indexación. La base sobre la que se construye todo lo demás.

GEO (Generative Engine Optimization) es la disciplina nueva: cómo las IA citan e incorporan tu contenido en sus respuestas. Las señales son distintas a las de Google, y casi nadie las trabaja todavía.

Cómo lo hacemos:

— Auditoría SEO técnica: indexación, schema, URLs, lo que frena tu posicionamiento.
— Datos estructurados para que Google y las IA entiendan exactamente qué haces.
— Contenido pensado para rankear en Google y para ser citable por IA. No son ejercicios separados.
— Seguimiento mensual, también en ChatGPT y Perplexity, no solo en Google.

El comportamiento de búsqueda está cambiando rápido. Quien se posicione ahora, en los dos frentes, captura una ventaja difícil de revertir.

¿Apareces cuando le preguntan a una IA por tu sector? Te lo comprobamos gratis.

#SEO #GEO #SEOtecnico #InteligenciaArtificial #PYMES"""),

    dict(n=3, slug="campanas", bg="olive", icon="ads",
         eyebrow="SERVICIO 03", name="Campañas de anuncios", accent="anuncios",
         photo="Imagen lista: ícono de marca. Mejor aún (swap): captura real de un panel de campañas (ROAS/CAC) en Looker Studio.",
         caption="""Los anuncios son el atajo más rápido para conseguir clientes. Y el agujero negro más rápido si no mides bien.

Una campaña bien hecha es el canal más predecible que existe: pones un euro, sabes cuánto vuelve.

Mal hecha, es dinero que se va sin saber a dónde.

¿La diferencia? Casi nunca es la creatividad. Es el tracking.

Cuando la medición está mal montada, los algoritmos de Google y Meta no aprenden qué clics se convierten en clientes. Entonces optimizan hacia clics baratos, no hacia ventas. Pagas visitas que no compran.

Por eso nunca empezamos por el anuncio. Empezamos por la medición.

Cómo lo hacemos:

— Primero, tracking limpio: GA4, Google Tag Manager, Conversions API en Meta, Enhanced Conversions en Google. Validamos que cada conversión se mida bien antes de gastar.
— Estructura por intención: audiencias frías y remarketing no se mezclan. Cada nivel del embudo, su campaña y su KPI.
— Creatividades testeadas con A/B, no a ojo.
— Optimización semanal y un informe con números útiles: CPL, CAC, ROAS. No "impresiones".

Hecho así, dejas de apostar. Sabes cuánto te cuesta un cliente y cuánto te devuelve cada canal.

Antes de subir el presupuesto, asegúrate de que estás midiendo lo que de verdad importa.

¿Sabes cuánto te cuesta conseguir un cliente por anuncios? Si dudas, hablemos.

#GoogleAds #MetaAds #ROAS #PYMES #MarketingDeResultados"""),
]


def run():
    os.makedirs(OUT, exist_ok=True)
    readme = ["# LinkedIn · 3 posts por servicio (long-form) — Vantia Digital", "",
              "Una publicación por servicio, formato long-form + imagen simple de respaldo.",
              "Cada carpeta NN-slug: `texto.txt` (copiar/pegar) + `imagen.png` (adjuntar).",
              "Tuteo España, cero emojis. La subida la hace Facu.", ""]
    for p in POSTS:
        folder = f"{OUT}/{p['n']:02d}-{p['slug']}"
        os.makedirs(folder, exist_ok=True)
        render_card(p, f"{folder}/imagen.png")
        with open(f"{folder}/texto.txt", "w", encoding="utf-8") as f:
            f.write(p["caption"].strip() + "\n")
        readme.append(f"- **{p['n']:02d} · {p['name']}** — `{p['n']:02d}-{p['slug']}/` · {p['photo']}")
    with open(f"{OUT}/README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme) + "\n")
    print(f"Paquete de servicios generado en {OUT}")
    for p in POSTS:
        print(f"  {p['n']:02d}-{p['slug']}/  (texto.txt + imagen.png)")


run()
