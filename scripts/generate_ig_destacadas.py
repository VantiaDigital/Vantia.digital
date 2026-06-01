"""
Genera 6 portadas de Historias Destacadas (highlight covers) para Instagram.
Formato 1080x1920 (story vertical). El cover se recorta en CIRCULO centrado,
asi que TODO el contenido (icono + label) va centrado dentro de un circulo
seguro de ~720px de diametro centrado en (540, 960).

Sistema consistente en las 6:
  - icono centrado arriba, caja ~360px, grosor de trazo ~10px
  - label de UNA palabra debajo, Inter ~66px, centrado
  - en cada icono UN solo elemento en COPPER, el resto del trazo en
    CREAM (fondo oscuro) o DEEP (fondo claro)

Estetica Vantia: cream + cobre + Fraunces/Inter. Sin emojis. Tuteo Espana.
Reutiliza paleta, fuentes, V_PATH/A_PATH y draw_logo de generate_ig_feed.

Outputs en assets/downloads/instagram/destacadas/:
  destacada-1-servicios.png
  destacada-2-proceso.png
  destacada-3-medicion.png
  destacada-4-casos.png
  destacada-5-nosotros.png
  destacada-6-contacto.png
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/instagram/destacadas"

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

W, H = 1080, 1920
CX, CY = 540, 960          # centro del canvas / del circulo seguro
BOX = 360                  # caja del icono
STROKE = 10                # grosor de trazo
ICON_CY = CY - 70          # centro vertical del icono (deja sitio para el label debajo)
LABEL_Y = CY + 175         # baseline-ish del label


def measure(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2]-b[0], b[3]-b[1], b


def draw_logo(draw, x, y, height, v=DEEP, a=COPPER):
    s = height / VBOX_H
    draw.polygon([(x+px*s, y+py*s) for px, py in V_PATH], fill=v)
    draw.polygon([(x+px*s, y+py*s) for px, py in A_PATH], fill=a)


def canvas(bg):
    img = Image.new("RGBA", (W, H), bg)
    return img, ImageDraw.Draw(img)


def label(draw, text, fg):
    f = ImageFont.truetype(INTER, 66)
    tw, th, b = measure(draw, text, f)
    draw.text((CX - tw/2, LABEL_Y - b[1]), text, font=f, fill=fg)


def finish(img, out):
    img.save(out, "PNG", optimize=True)


def base(dark):
    bg = DEEP if dark else CREAM
    fg = CREAM if dark else DEEP   # color de label y trazo neutro del icono
    return canvas(bg) + (fg,)


# ---------------------------------------------------------------------------
# 1 · SERVICIOS — 3 barras verticales de altura creciente; la mas alta en cobre
# ---------------------------------------------------------------------------
def icon_servicios(draw, fg):
    bar_w = 78
    gap = 34
    total_w = bar_w*3 + gap*2
    x0 = CX - total_w/2
    base_y = ICON_CY + BOX/2          # base comun
    heights = [BOX*0.42, BOX*0.68, BOX*0.95]
    for i, h in enumerate(heights):
        x = x0 + i*(bar_w+gap)
        col = COPPER if i == 2 else fg
        draw.rounded_rectangle([x, base_y - h, x + bar_w, base_y],
                               radius=10, outline=col, width=STROKE)


# ---------------------------------------------------------------------------
# 2 · PROCESO — 3 circulos en linea unidos por 2 flechas; una flecha en cobre
# ---------------------------------------------------------------------------
def icon_proceso(draw, fg):
    r = 40
    seg = BOX/2                       # separacion entre centros de circulos
    xs = [CX - seg, CX, CX + seg]
    y = ICON_CY
    # circulos
    for x in xs:
        draw.ellipse([x-r, y-r, x+r, y+r], outline=fg, width=STROKE)
    # flechas entre circulos (la primera en cobre)
    arrow_cols = [COPPER, fg]
    for i in range(2):
        x_start = xs[i] + r + 14
        x_end = xs[i+1] - r - 14
        col = arrow_cols[i]
        draw.line([(x_start, y), (x_end, y)], fill=col, width=STROKE)
        # punta de flecha
        head = 18
        draw.line([(x_end, y), (x_end - head, y - head)], fill=col, width=STROKE)
        draw.line([(x_end, y), (x_end - head, y + head)], fill=col, width=STROKE)


# ---------------------------------------------------------------------------
# 3 · MEDICION — eje en L + linea quebrada ascendente (la ascendente en cobre)
# ---------------------------------------------------------------------------
def icon_medicion(draw, fg):
    half = BOX/2
    left = CX - half
    right = CX + half
    top = ICON_CY - half
    bottom = ICON_CY + half
    # eje en L (vertical + horizontal) en color neutro
    draw.line([(left, top), (left, bottom)], fill=fg, width=STROKE)
    draw.line([(left, bottom), (right, bottom)], fill=fg, width=STROKE)
    # linea quebrada ascendente de 3 tramos, en cobre
    pts = [
        (left + 38, bottom - 60),
        (left + 130, bottom - 150),
        (left + 215, bottom - 95),
        (right - 28, bottom - 250),
    ]
    draw.line(pts, fill=COPPER, width=STROKE, joint="curve")
    # punto final destacado
    ex, ey = pts[-1]
    draw.ellipse([ex-15, ey-15, ex+15, ey+15], fill=COPPER)


# ---------------------------------------------------------------------------
# 4 · CASOS — carpeta (rectangulo con pestana arriba-izq); pestana en cobre
# ---------------------------------------------------------------------------
def icon_casos(draw, fg):
    half = BOX/2
    left = CX - half
    right = CX + half
    body_top = ICON_CY - half*0.55
    bottom = ICON_CY + half*0.75
    tab_w = BOX*0.46
    tab_h = 48
    tab_slant = 34
    # cuerpo de la carpeta (neutro): lado izquierdo arranca arriba (en la pestana)
    draw.line([(left, body_top - tab_h), (left, bottom)], fill=fg, width=STROKE)   # izquierda
    draw.line([(left, bottom), (right, bottom)], fill=fg, width=STROKE)            # base
    draw.line([(right, bottom), (right, body_top)], fill=fg, width=STROKE)         # derecha
    # tramo superior del cuerpo a la derecha de la pestana (neutro)
    draw.line([(left + tab_w, body_top), (right, body_top)], fill=fg, width=STROKE)
    # pestana (cobre): horizontal arriba + diagonal que baja a body_top
    draw.line([(left, body_top - tab_h), (left + tab_w - tab_slant, body_top - tab_h)],
              fill=COPPER, width=STROKE)
    draw.line([(left + tab_w - tab_slant, body_top - tab_h), (left + tab_w, body_top)],
              fill=COPPER, width=STROKE, joint="curve")


# ---------------------------------------------------------------------------
# 5 · NOSOTROS — isotipo Vantia (V cream/dark + A cobre), ~360px de alto
# ---------------------------------------------------------------------------
def icon_nosotros(draw, fg):
    h = 360
    s = h / VBOX_H
    w = VBOX_W * s
    x = CX - w/2
    y = ICON_CY - h/2
    draw_logo(draw, x, y, h, v=fg, a=COPPER)


# ---------------------------------------------------------------------------
# 6 · CONTACTO — sobre (rectangulo + 2 diagonales = solapa); solapa en cobre
# ---------------------------------------------------------------------------
def icon_contacto(draw, fg):
    w = BOX
    h = BOX*0.66
    left = CX - w/2
    right = CX + w/2
    top = ICON_CY - h/2
    bottom = ICON_CY + h/2
    # cuerpo del sobre (neutro)
    draw.rounded_rectangle([left, top, right, bottom], radius=14,
                           outline=fg, width=STROKE)
    # solapa: 2 diagonales desde esquinas superiores al centro (cobre)
    draw.line([(left + STROKE/2, top + STROKE/2), (CX, ICON_CY + 18)],
              fill=COPPER, width=STROKE, joint="curve")
    draw.line([(right - STROKE/2, top + STROKE/2), (CX, ICON_CY + 18)],
              fill=COPPER, width=STROKE, joint="curve")


def render(out, lbl, icon_fn, dark):
    img, draw, fg = base(dark)
    icon_fn(draw, fg)
    label(draw, lbl, fg)
    finish(img, out)


os.makedirs(OUT, exist_ok=True)

render(f"{OUT}/destacada-1-servicios.png", "Servicios", icon_servicios, dark=True)
render(f"{OUT}/destacada-2-proceso.png",   "Proceso",   icon_proceso,   dark=False)
render(f"{OUT}/destacada-3-medicion.png",  "Medición",  icon_medicion,  dark=True)
render(f"{OUT}/destacada-4-casos.png",     "Casos",     icon_casos,     dark=False)
render(f"{OUT}/destacada-5-nosotros.png",  "Nosotros",  icon_nosotros,  dark=True)
render(f"{OUT}/destacada-6-contacto.png",  "Contacto",  icon_contacto,  dark=False)

print("Destacadas IG generadas:")
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p) and f.endswith(".png"):
        print(f"  {f}  ({os.path.getsize(p)} bytes)")
