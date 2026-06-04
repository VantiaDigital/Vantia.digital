# -*- coding: utf-8 -*-
"""
Portada (cover) para la página de Facebook de Vantia Digital.
Tamaño: 1702x630 (= 851x315 a 2x, ratio oficial de portada FB). Contenido centrado
dentro de la zona segura (el móvil recorta los lados).
Marca: fondo profundo #1A1813 + glow cobre + cristal sutil (eco del hero) + isotipo V+A
+ wordmark + tesis. Fraunces/Inter. Sin emojis.
Salida: assets/downloads/facebook/portada-facebook.png
Correr: python scripts/generate_facebook_cover.py
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/facebook"

DEEP = (26, 24, 19, 255)
COPPER = (193, 131, 75, 255)
CREAM = (236, 232, 216, 255)
MUTED = (169, 155, 128, 255)

V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012
W, H = 1702, 630


def measure(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1], b


def draw_logo(d, x, y, h, v, a):
    s = h / VBOX_H
    d.polygon([(x + px * s, y + py * s) for px, py in V_PATH], fill=v)
    d.polygon([(x + px * s, y + py * s) for px, py in A_PATH], fill=a)


def run():
    os.makedirs(OUT, exist_ok=True)
    img = Image.new("RGBA", (W, H), DEEP)

    # glow cobre difuso, detrás del logo
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, 250
    gd.ellipse([cx - 470, cy - 290, cx + 470, cy + 290], fill=(193, 131, 75, 65))
    glow = glow.filter(ImageFilter.GaussianBlur(175))
    img.alpha_composite(glow)

    # cristal hexagonal sutil (eco del hero), centrado
    cr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cr)
    R, hx, hy = 250, W / 2, 250
    pts = [(hx + R * math.cos(math.radians(60 * i - 90)),
            hy + R * math.sin(math.radians(60 * i - 90))) for i in range(6)]
    cd.line(pts + [pts[0]], fill=(193, 131, 75, 40), width=2)
    for i in range(3):
        cd.line([pts[i], pts[i + 3]], fill=(193, 131, 75, 26), width=1)
    img.alpha_composite(cr)

    d = ImageDraw.Draw(img)

    # ---- lockup: isotipo + "Vantia Digital" ----
    logo_h = 124
    logo_w = VBOX_W * (logo_h / VBOX_H)
    fword = ImageFont.truetype(FRAUNCES, 78)
    w1, h1, b1 = measure(d, "Vantia", fword)
    sp = measure(d, " ", fword)[0]
    w2, h2, b2 = measure(d, "Digital", fword)
    gap = 36
    total = logo_w + gap + w1 + sp + w2
    sx = (W - total) / 2
    ly = 232
    draw_logo(d, sx, ly - logo_h / 2, logo_h, CREAM, COPPER)
    tx = sx + logo_w + gap
    wy = ly - h1 / 2 - b1[1]
    d.text((tx, wy), "Vantia", font=fword, fill=CREAM)
    d.text((tx + w1 + sp, wy), "Digital", font=fword, fill=COPPER)

    # hairline cobre
    d.rectangle([(W / 2 - 60, 360), (W / 2 + 60, 363)], fill=COPPER)

    # tesis
    ftag = ImageFont.truetype(FRAUNCES, 48)
    tag = "Datos antes que promesas."
    wt, ht, bt = measure(d, tag, ftag)
    d.text(((W - wt) / 2, 400 - bt[1]), tag, font=ftag, fill=CREAM)

    # descriptor
    fsub = ImageFont.truetype(INTER, 25)
    sub = "Agencia técnica de marketing digital  ·  Barcelona"
    ws, hs, bs = measure(d, sub, fsub)
    d.text(((W - ws) / 2, 478 - bs[1]), sub, font=fsub, fill=MUTED)

    out = f"{OUT}/portada-facebook.png"
    img.save(out, "PNG", optimize=True)
    print("Portada generada:", out, img.size)


run()
