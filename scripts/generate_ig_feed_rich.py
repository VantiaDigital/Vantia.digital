"""
Genera los 9 posts de feed IG (1080x1350) en DOS variantes desde una sola fuente
de copy (copy mejorado por el Copywriter):
  - RICA (publicable)  -> assets/downloads/instagram/feed/
      isotipo marca de agua sutil + indice 01/09 + hairline cobre bajo eyebrow.
  - FLAT (componentes) -> assets/downloads/instagram/feed-componentes/
      version minimal (sin marca de agua/indice/hairline), util como base en Canva.
Sistema visual: paleta Vantia + Fraunces/Inter. Tuteo Espana, sin emojis.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT_RICH = f"{ROOT}/assets/downloads/instagram/feed"
OUT_FLAT = f"{ROOT}/assets/downloads/instagram/feed-componentes"

DEEP   = (26, 24, 19, 255)
DARK   = (60, 58, 47, 255)
COPPER = (193, 131, 75, 255)
CREAM  = (236, 232, 216, 255)
MUTED  = (169, 155, 128, 255)
WM_DARK  = (43, 41, 34, 255)
WM_LIGHT = (224, 219, 201, 255)

V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012
W, H = 1080, 1350
PAD = 100


def measure(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2]-b[0], b[3]-b[1], b


def wrap(draw, text, font, maxw):
    words, lines, line = text.split(), [], ""
    for w in words:
        c = (line + " " + w).strip()
        if measure(draw, c, font)[0] <= maxw:
            line = c
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def canvas(bg):
    img = Image.new("RGBA", (W, H), bg)
    return img, ImageDraw.Draw(img)


def draw_logo(draw, x, y, height, v, a):
    s = height / VBOX_H
    draw.polygon([(x+px*s, y+py*s) for px, py in V_PATH], fill=v)
    draw.polygon([(x+px*s, y+py*s) for px, py in A_PATH], fill=a)


def watermark(img, dark):
    wm = WM_DARK if dark else WM_LIGHT
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    h = 1080
    s = h / VBOX_H
    logo_w = VBOX_W * s
    x = W - logo_w * 0.62
    y = H - h * 0.78
    draw_logo(d, x, y, h, v=wm, a=wm)
    img.alpha_composite(layer)


def index_tag(draw, n):
    f = ImageFont.truetype(INTER, 26)
    txt = f"{n:02d} / 09"
    tw, th, b = measure(draw, txt, f)
    draw.text((W - PAD - tw, 150 - b[1]), txt, font=f, fill=MUTED)


def eyebrow(draw, label, y, centered, rich):
    f = ImageFont.truetype(INTER, 24)
    tw, th, b = measure(draw, label, f)
    lx = (W - tw) / 2 if centered else PAD
    draw.text((lx, y - b[1]), label, font=f, fill=COPPER)
    if rich:
        ry = y + th + 18
        if centered:
            draw.rectangle([(W/2 - 35, ry), (W/2 + 35, ry + 4)], fill=COPPER)
        else:
            draw.rectangle([(PAD, ry), (PAD + 70, ry + 4)], fill=COPPER)


def footer(draw, dark):
    logo_h = 46
    s = logo_h / VBOX_H
    logo_w = VBOX_W * s
    text = "Vantia Digital"
    f = ImageFont.truetype(FRAUNCES, 30)
    tw, th, b = measure(draw, text, f)
    gap = 18
    total = logo_w + gap + tw
    sx = (W - total) / 2
    y = H - 95
    col = CREAM if dark else DEEP
    draw_logo(draw, sx, y - logo_h/2, logo_h, v=col, a=COPPER)
    draw.text((sx + logo_w + gap, y - th/2 - b[1]), text, font=f, fill=col)


def base(n, dark, rich):
    img, draw = canvas(DEEP if dark else CREAM)
    if rich:
        watermark(img, dark)
        draw = ImageDraw.Draw(img)
        index_tag(draw, n)
    return img, draw


def render_quote(n, out, label, lines, accent_word, dark, rich):
    fg = CREAM if dark else DEEP
    img, draw = base(n, dark, rich)
    eyebrow(draw, label, 210, centered=True, rich=rich)
    font = ImageFont.truetype(FRAUNCES, 86)
    gap = 22
    measured = [(l, *measure(draw, l, font)) for l in lines]
    total = sum(h for _, _, h, _ in measured) + gap*(len(lines)-1)
    cy = (H - total)/2 - 30
    for line, lw, lh, lb in measured:
        if accent_word and accent_word in line:
            pre, post = line.split(accent_word, 1)
            wpre = measure(draw, pre, font)[0]
            wacc = measure(draw, accent_word, font)[0]
            x0 = (W - lw)/2
            draw.text((x0, cy - lb[1]), pre, font=font, fill=fg)
            draw.text((x0+wpre, cy - lb[1]), accent_word, font=font, fill=COPPER)
            draw.text((x0+wpre+wacc, cy - lb[1]), post, font=font, fill=fg)
        else:
            draw.text(((W-lw)/2, cy - lb[1]), line, font=font, fill=fg)
        cy += lh + gap
    footer(draw, dark)
    img.save(out, "PNG", optimize=True)


def render_title_body(n, out, label, title, body_lines, dark, rich):
    fg = CREAM if dark else DEEP
    sec = MUTED if dark else DARK
    img, draw = base(n, dark, rich)
    eyebrow(draw, label, 150, centered=False, rich=rich)
    f_title = ImageFont.truetype(FRAUNCES, 72)
    y = 268
    for line in wrap(draw, title, f_title, W-2*PAD):
        _, h, b = measure(draw, line, f_title)
        draw.text((PAD, y - b[1]), line, font=f_title, fill=fg)
        y += h + 12
    y += 46
    f_body = ImageFont.truetype(INTER, 34)
    for para in body_lines:
        for wl in wrap(draw, para, f_body, W-2*PAD):
            _, h, b = measure(draw, wl, f_body)
            draw.text((PAD, y - b[1]), wl, font=f_body, fill=sec)
            y += h + 10
        y += 20
    footer(draw, dark)
    img.save(out, "PNG", optimize=True)


def render_checklist(n, out, label, title, items, dark, rich):
    fg = CREAM if dark else DEEP
    sec = DARK if not dark else MUTED
    img, draw = base(n, dark, rich)
    eyebrow(draw, label, 150, centered=False, rich=rich)
    f_title = ImageFont.truetype(FRAUNCES, 66)
    y = 268
    for line in wrap(draw, title, f_title, W-2*PAD):
        _, h, b = measure(draw, line, f_title)
        draw.text((PAD, y - b[1]), line, font=f_title, fill=fg)
        y += h + 12
    y += 46
    f_item = ImageFont.truetype(INTER, 34)
    for it in items:
        dash = "—"
        _, hd, bd = measure(draw, dash, f_item)
        draw.text((PAD, y - bd[1]), dash, font=f_item, fill=COPPER)
        wd = measure(draw, dash + " ", f_item)[0]
        for wl in wrap(draw, it, f_item, W-2*PAD-wd):
            _, h, b = measure(draw, wl, f_item)
            draw.text((PAD + wd, y - b[1]), wl, font=f_item, fill=sec)
            y += h + 8
        y += 18
    footer(draw, dark)
    img.save(out, "PNG", optimize=True)


# Carta de presentacion de marca (Estratega + Copywriter). Damero: impares oscuro.
PIECES = [
    dict(n=1, slug="feed-01-no-somos-otra-agencia", kind="quote", dark=True, eyebrow="QUIÉNES SOMOS",
         lines=["No somos", "otra agencia", "creativa.", "Somos", "técnica."], accent="técnica"),
    dict(n=2, slug="feed-02-hablamos-al-dueno", kind="title", dark=False, eyebrow="A QUIÉN LE HABLAMOS",
         title="Le hablamos al dueño, no a su departamento de marketing.",
         body=["No necesitas saber marketing-speak para entender qué hace tu dinero. Eso es trabajo nuestro, no tuyo.",
               "Traducimos lo técnico a decisiones de negocio. Pensado para PYMES, no para corporaciones con un equipo de diez personas."]),
    dict(n=3, slug="feed-03-tu-web-no-es-folleto", kind="quote", dark=True, eyebrow="EL PROBLEMA",
         lines=["Tu web", "no es un", "folleto.", "Es tu mejor", "comercial."], accent="comercial"),
    dict(n=4, slug="feed-04-que-hacemos", kind="check", dark=False, eyebrow="QUÉ HACEMOS",
         title="Cuatro cosas, bien hechas.",
         items=["Optimizar tu web para que venda", "Que te encuentren: SEO técnico y GEO",
                "Campañas de anuncios que rinden", "Medición clara de cada resultado"]),
    dict(n=5, slug="feed-05-primero-medir", kind="quote", dark=True, eyebrow="NUESTRO PRINCIPIO",
         lines=["Primero", "medir.", "Después", "invertir."], accent="medir"),
    dict(n=6, slug="feed-06-como-trabajamos", kind="title", dark=False, eyebrow="CÓMO TRABAJAMOS",
         title="Montamos la medición antes de gastar un euro en tráfico.",
         body=["Primero instrumentamos: dejamos listo el sistema que registra qué pasa en tu web. Después invertimos, sobre datos.",
               "Y si algo no se puede medir bien, te lo decimos. Preferimos ser claros a venderte una cifra que no podemos sostener."]),
    dict(n=7, slug="feed-07-nuestros-valores", kind="check", dark=True, eyebrow="EN QUÉ CREEMOS",
         title="Lo que no negociamos.",
         items=["Decirte lo que no está funcionando", "Hablar claro, sin jerga",
                "Datos antes que promesas", "Tu negocio por delante de todo"]),
    dict(n=8, slug="feed-08-nuestra-metodologia", kind="check", dark=False, eyebrow="PASO A PASO",
         title="Cuatro pasos, en orden.",
         items=["Entender tu negocio", "Medir el punto de partida",
                "Construir y optimizar", "Revisar con datos en la mano"]),
    dict(n=9, slug="feed-09-da-el-paso", kind="quote", dark=True, eyebrow="PARA QUÉ",
         lines=["Por fin", "saber qué", "funciona.", "Y decidir", "con claridad."], accent="claridad"),
]


def run(rich, outdir):
    os.makedirs(outdir, exist_ok=True)
    for p in PIECES:
        out = f"{outdir}/{p['slug']}.png"
        if p["kind"] == "quote":
            render_quote(p["n"], out, p["eyebrow"], p["lines"], p["accent"], p["dark"], rich)
        elif p["kind"] == "title":
            render_title_body(p["n"], out, p["eyebrow"], p["title"], p["body"], p["dark"], rich)
        else:
            render_checklist(p["n"], out, p["eyebrow"], p["title"], p["items"], p["dark"], rich)
    # limpiar PNG huerfanos (slugs viejos)
    keep = {f"{p['slug']}.png" for p in PIECES}
    for f in os.listdir(outdir):
        if f.endswith(".png") and f not in keep:
            os.remove(os.path.join(outdir, f))


run(rich=True, outdir=OUT_RICH)
run(rich=False, outdir=OUT_FLAT)

print("Feed generado (rico + componentes):")
for d, tag in [(OUT_RICH, "RICO"), (OUT_FLAT, "FLAT")]:
    files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    print(f"  [{tag}] {len(files)} archivos")
    for f in files:
        print(f"    {f}  ({os.path.getsize(os.path.join(d, f))} bytes)")
