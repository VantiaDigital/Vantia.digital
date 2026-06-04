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
         caption="""El 70% de las PYMES tiene su web en rojo para Google. Y casi ninguna lo sabe.

La web es la base donde todo lo demás se mide. Si carga lento, si no se ve en el móvil, si Google la marca como insegura, ningún otro esfuerzo de marketing rinde.

Optimizar una web es trabajar dos capas a la vez: la técnica y la de conversión.

La capa técnica son los Core Web Vitals, las tres métricas con las que Google decide si tu web sirve:

— LCP: cuánto tarda en aparecer el contenido principal.
— INP: cuán rápido reacciona a un clic.
— CLS: si los elementos se mueven mientras carga.

La capa de conversión es el CRO: qué pasa una vez que la página carga. Dónde se frena la gente, dónde abandona, qué versión de un titular o un formulario hace que más visitas terminen en clientes.

Por qué importa, con números:

— Cada 100 ms extra de carga, pierdes entre 1% y 2% de conversiones.
— Una web que tarda 4 segundos pierde la mitad de las visitas antes de mostrar nada.
— Y como esa visita la pagaste (en anuncios o en SEO), es dinero real desperdiciado.

Cómo lo hacemos:

— Auditoría técnica con Lighthouse y PageSpeed: el diagnóstico real de hoy.
— Performance budget: cuánto puede pesar cada página. Sin esto, las webs se hinchan con cada cambio.
— Refactor: imágenes (WebP/AVIF), lazy loading, CSS crítico, JavaScript no bloqueante.
— CRO: mapas de calor y grabaciones de sesión (Microsoft Clarity) + tests A/B. No asumimos qué convierte; lo medimos.
— Accesibilidad (WCAG 2.2) y SEO técnico de base.

Qué te llevas: PageSpeed 95+, Core Web Vitals en verde (LCP < 2,5s, INP < 200ms, CLS < 0,1), un roadmap de CRO con tests documentados y un dashboard que lees tú mismo.

El resultado no es "una web más bonita". Es una web que convierte más de la gente que ya estás trayendo.

¿Sabes en qué color está tu web para Google? Te lo miramos gratis.

#OptimizacionWeb #CRO #CoreWebVitals #PYMES #MarketingDeResultados"""),

    dict(n=2, slug="seo-geo", bg="crema", icon="seo",
         eyebrow="SERVICIO 02", name="SEO Técnico + GEO", accent="GEO",
         photo="Imagen lista: ícono de marca. Mejor aún (swap): captura real de una respuesta de ChatGPT/Perplexity citando a un cliente, o de Search Console.",
         caption="""Gartner estima que para 2026 el tráfico orgánico tradicional cae un 25%. ¿Tu SEO está preparado para eso?

El SEO ya no es solo "aparecer primero en Google". Es aparecer también en las respuestas de ChatGPT, Perplexity y Gemini.

Por eso combinamos dos disciplinas:

SEO técnico: cómo Google entiende tu web. Estructura, código limpio, schema markup, velocidad, indexación, sitemap. Es la base sobre la que se construye todo el SEO de contenido.

GEO (Generative Engine Optimization): la disciplina nueva, surgida en 2024-2025. Cómo los motores de IA citan e incorporan tu contenido en sus respuestas. Cuando alguien le pregunta a ChatGPT "cuál es la mejor agencia de mi zona", el modelo elige fuentes con señales muy distintas a las de Google.

Las dos se solapan en la base técnica, pero divergen en táctica: el SEO clásico mira backlinks y autoridad de dominio; el GEO mira la "citabilidad" del contenido (claridad, datos verificables, autoridad temática).

Por qué importa ahora:

Si tu estrategia solo apunta a Google, vas a perder relevancia sin darte cuenta. Y GEO está en sus primeros años: quien se posiciona hoy como fuente citable captura una ventaja difícil de revertir.

Cómo lo hacemos:

— Auditoría técnica completa (Screaming Frog + Search Console + Ahrefs): indexación, contenido duplicado, schema, URLs canónicas, redirects.
— Schema markup avanzado (Organization, LocalBusiness, FAQPage, Article…) para que Google y la IA entiendan exactamente qué haces.
— Estrategia de contenido dual: pensada para rankear en Google y para ser citada por IA. No son ejercicios separados.
— Citation engineering: perfiles consistentes, menciones en medios, presencia donde los modelos aprenden.
— Monitorización mensual, también en ChatGPT y Perplexity, no solo en Google.

Qué te llevas: auditoría con issues priorizados (P0-P3), schema implementado, un calendario editorial trimestral y un dashboard mensual de keywords + visibilidad en IA. Recomendaciones accionables, no reportes pasivos.

¿Apareces cuando le preguntan a una IA por tu sector? Te lo comprobamos gratis.

#SEO #GEO #SEOtecnico #InteligenciaArtificial #PYMES"""),

    dict(n=3, slug="campanas", bg="olive", icon="ads",
         eyebrow="SERVICIO 03", name="Campañas de anuncios", accent="anuncios",
         photo="Imagen lista: ícono de marca. Mejor aún (swap): captura real de un panel de campañas (ROAS/CAC) en Looker Studio.",
         caption="""La mayoría de las PYMES no pierde dinero en anuncios por la creatividad. Lo pierde por el tracking.

Una campaña no es "subir un anuncio a Google o Meta". Son cinco capas que tienen que estar coordinadas:

— Tracking: medir qué pasa.
— Audiencia: a quién le hablas.
— Creatividad: qué le muestras.
— Landing: a dónde lo envías.
— Optimización: qué haces con los datos que llegan.

El problema casi siempre está en la primera. Si el tracking está mal configurado, los algoritmos de Google y Meta no aprenden qué clics se convierten en clientes. Entonces optimizan hacia clics baratos, no hacia ventas. Dinero gastado en visitas que nunca compran.

Por qué importa:

Bien hechas, las campañas son el canal más medible y predecible que existe: sabes cuánto te cuesta un cliente, tu ROAS por canal, qué creatividades funcionan. Mal hechas, son el agujero negro más rápido del marketing.

Por eso nunca empezamos por el anuncio. Empezamos por la medición.

Cómo lo hacemos:

— Setup técnico antes que creativo: GA4 con eventos, Conversions API (Meta), Enhanced Conversions (Google). Validamos cada conversión antes de lanzar.
— Investigación de tu cliente real, no del avatar genérico.
— Estructura por intención ("ABC"): audiencias frías y remarketing no se mezclan. Cada nivel del embudo, su campaña y su KPI.
— Creatividades con A/B testing sistemático.
— Optimización semanal: cada lunes cortamos lo que no funciona y escalamos lo que sí. Nada de "set and forget".
— Reporte mensual con números útiles: CPL, CAC, ROAS, LTV proyectado. No "impresiones".

Qué te llevas: tracking validado end-to-end (web → GA4 → algoritmo → reporte), campañas en Google Ads (Search, PMax, YouTube) y Meta Ads, un banco de creatividades testeadas y un dashboard con CAC, ROAS y atribución.

Hecho así, dejas de apostar.

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
