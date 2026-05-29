"""
Genera 7 posts de feed para Instagram (1080x1350, formato 4:5 vertical).
Estética Vantia: cream + cobre + Fraunces/Inter. Tuteo España. Sin emojis.
Para completar el grid de lanzamiento + colchón de varias semanas.

Outputs en assets/downloads/instagram/feed/:
  feed-01-principio.png        (cita)
  feed-02-sesion-cliente.png   (tip GA4)
  feed-03-manifiesto.png       (cita)
  feed-04-web-checklist.png    (checklist)
  feed-05-comercial.png        (cita)
  feed-06-geo.png              (tip GEO)
  feed-07-posicionamiento.png  (cita)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/instagram/feed"

DEEP   = (26, 24, 19, 255)
DARK   = (60, 58, 47, 255)
COPPER = (193, 131, 75, 255)
CREAM  = (236, 232, 216, 255)
MUTED  = (169, 155, 128, 255)

V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012

W, H = 1080, 1350


def draw_logo(draw, x, y, height, v=DEEP, a=COPPER):
    s = height / VBOX_H
    draw.polygon([(x+px*s, y+py*s) for px, py in V_PATH], fill=v)
    draw.polygon([(x+px*s, y+py*s) for px, py in A_PATH], fill=a)


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


def canvas(bg=CREAM):
    img = Image.new("RGBA", (W, H), bg)
    return img, ImageDraw.Draw(img)


def footer(draw, dark_bg=False):
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
    vcol = CREAM if dark_bg else DEEP
    tcol = CREAM if dark_bg else DEEP
    draw_logo(draw, sx, y - logo_h/2, logo_h, v=vcol, a=COPPER)
    draw.text((sx + logo_w + gap, y - th/2 - b[1]), text, font=f, fill=tcol)


def eyebrow(draw, text, dark_bg=False, y=150):
    f = ImageFont.truetype(INTER, 24)
    tw, th, b = measure(draw, text, f)
    draw.text(((W - tw)/2, y - b[1]), text, font=f, fill=COPPER)


def render_quote(out, label, lines, accent_word=None, dark=False):
    bg = DEEP if dark else CREAM
    fg = CREAM if dark else DEEP
    img, draw = canvas(bg)
    eyebrow(draw, label, dark, y=210)
    font = ImageFont.truetype(FRAUNCES, 86)
    gap = 22
    measured = [(l, *measure(draw, l, font)) for l in lines]
    total = sum(h for _, _, h, _ in measured) + gap*(len(lines)-1)
    cy = (H - total)/2 - 40
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


def render_title_body(out, label, title, body_lines, dark=False):
    bg = DEEP if dark else CREAM
    fg = CREAM if dark else DEEP
    sec = MUTED if dark else DARK
    img, draw = canvas(bg)
    PAD = 100
    f_lbl = ImageFont.truetype(INTER, 24)
    draw.text((PAD, 150), label, font=f_lbl, fill=COPPER)
    f_title = ImageFont.truetype(FRAUNCES, 72)
    y = 250
    for line in wrap(draw, title, f_title, W-2*PAD):
        _, h, b = measure(draw, line, f_title)
        draw.text((PAD, y - b[1]), line, font=f_title, fill=fg)
        y += h + 12
    y += 50
    f_body = ImageFont.truetype(INTER, 34)
    for para in body_lines:
        for wl in wrap(draw, para, f_body, W-2*PAD):
            _, h, b = measure(draw, wl, f_body)
            draw.text((PAD, y - b[1]), wl, font=f_body, fill=sec)
            y += h + 10
        y += 20
    footer(draw, dark)
    img.save(out, "PNG", optimize=True)


def render_checklist(out, label, title, items, dark=False):
    bg = DEEP if dark else CREAM
    fg = CREAM if dark else DEEP
    sec = DARK if not dark else MUTED
    img, draw = canvas(bg)
    PAD = 100
    f_lbl = ImageFont.truetype(INTER, 24)
    draw.text((PAD, 150), label, font=f_lbl, fill=COPPER)
    f_title = ImageFont.truetype(FRAUNCES, 66)
    y = 250
    for line in wrap(draw, title, f_title, W-2*PAD):
        _, h, b = measure(draw, line, f_title)
        draw.text((PAD, y - b[1]), line, font=f_title, fill=fg)
        y += h + 12
    y += 50
    f_item = ImageFont.truetype(INTER, 34)
    for it in items:
        dash = "—"
        _, hd, bd = measure(draw, dash, f_item)
        draw.text((PAD, y - bd[1]), dash, font=f_item, fill=COPPER)
        wd = measure(draw, dash + " ", f_item)[0]
        for i, wl in enumerate(wrap(draw, it, f_item, W-2*PAD-wd)):
            _, h, b = measure(draw, wl, f_item)
            draw.text((PAD + (wd if i == 0 else wd), y - b[1]), wl, font=f_item, fill=sec)
            y += h + 8
        y += 18
    footer(draw, dark)
    img.save(out, "PNG", optimize=True)


os.makedirs(OUT, exist_ok=True)

render_quote(f"{OUT}/feed-01-principio.png", "PRINCIPIO",
             ["Si no se mide,", "no se mejora."], accent_word="mide")

render_title_body(f"{OUT}/feed-02-sesion-cliente.png", "TIP · GA4",
                  "Una sesión no es un cliente.",
                  ["La mayoría de las PYMES mira 'sesiones' como métrica de éxito.",
                   "Pero una visita no paga las cuentas. Una conversión sí.",
                   "Marca tus eventos clave como conversiones, no la visita."])

render_quote(f"{OUT}/feed-03-manifiesto.png", "CÓMO TRABAJAMOS",
             ["Medimos antes", "de ejecutar.", "Siempre."], accent_word="antes", dark=True)

render_checklist(f"{OUT}/feed-04-web-checklist.png", "CHECKLIST",
                 "Una web bien hecha tiene:",
                 ["Core Web Vitals en verde (carga rápida).",
                  "GA4 + medición desde el día 1.",
                  "Accesibilidad y SEO técnico de base.",
                  "Un dashboard que el dueño puede leer."])

render_quote(f"{OUT}/feed-05-comercial.png", "OPINIÓN",
             ["Tu web no es", "un folleto.", "Es tu mejor", "comercial."], accent_word="comercial")

render_title_body(f"{OUT}/feed-06-geo.png", "TENDENCIA · GEO",
                  "Ya no alcanza con Google.",
                  ["Cada vez más gente busca en ChatGPT, Perplexity y Gemini.",
                   "Si tu marca no aparece ahí, no existe para ese público.",
                   "GEO es optimizar para ser citado por la IA, no solo por Google."],
                  dark=True)

render_quote(f"{OUT}/feed-07-posicionamiento.png", "VANTIA DIGITAL",
             ["Datos antes", "que promesas."], accent_word="Datos")

print("Feed IG generado:")
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p):
        print(f"  {f}  ({os.path.getsize(p)} bytes)")
