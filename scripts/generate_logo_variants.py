"""
Genera variantes del logotipo de Vantia (V+A + texto "Vantia Digital").

Outputs (assets/images/):
  - logo-horizontal-claro.png    (V dark + A cobre + texto dark, fondo transparente)
  - logo-horizontal-oscuro.png   (V cream + A cobre + texto cream, fondo transparente)
  - logo-vertical-claro.png      (apilado, fondo transparente)
  - logo-vertical-oscuro.png     (apilado, fondo transparente)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FONT_PATH = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
OUT_DIR = f"{ROOT}/assets/images"

# Colores (RGBA)
DARK   = (26, 24, 19, 255)
COPPER = (193, 131, 75, 255)
CREAM  = (236, 232, 216, 255)

# Logo V+A — coordenadas de paths (viewBox 1269x1012)
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012

TEXT = "Vantia Digital"


def draw_logo(draw, x, y, height, v_color, a_color):
    """Dibuja V+A con top-left en (x, y), altura en píxeles."""
    scale = height / VBOX_H
    v_pts = [(x + px*scale, y + py*scale) for (px, py) in V_PATH]
    a_pts = [(x + px*scale, y + py*scale) for (px, py) in A_PATH]
    draw.polygon(v_pts, fill=v_color)
    draw.polygon(a_pts, fill=a_color)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox


def render_horizontal(out_path, v_color, a_color, text_color):
    """Auto-sized: el canvas se calcula para que el texto + logo entren con padding."""
    FONT_SIZE = 165
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w_full, _, bbox_full = measure(tmp, TEXT, font)
    text_h = bbox_full[3] - bbox_full[1]

    LOGO_H = int(text_h * 2.0)
    logo_scale = LOGO_H / VBOX_H
    LOGO_W = int(VBOX_W * logo_scale)

    PAD = 100
    GAP = 110
    H = max(LOGO_H, text_h) + 2 * PAD
    W = PAD + LOGO_W + GAP + w_full + PAD

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    logo_x = PAD
    logo_y = (H - LOGO_H) // 2
    draw_logo(draw, logo_x, logo_y, LOGO_H, v_color, a_color)

    text_x = logo_x + LOGO_W + GAP - bbox_full[0]
    text_y = (H - text_h) // 2 - bbox_full[1]
    draw.text((text_x, text_y), TEXT, font=font, fill=text_color)

    img.save(out_path, "PNG", optimize=True)


def render_vertical(out_path, v_color, a_color, text_color):
    """Auto-sized vertical: logo arriba, texto debajo, canvas se ajusta al contenido."""
    FONT_SIZE = 130
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w_full, _, bbox_full = measure(tmp, TEXT, font)
    text_h = bbox_full[3] - bbox_full[1]

    LOGO_H = 700
    logo_scale = LOGO_H / VBOX_H
    LOGO_W = int(VBOX_W * logo_scale)

    PAD = 150
    GAP = 90
    W = max(LOGO_W, w_full) + 2 * PAD
    H = PAD + LOGO_H + GAP + text_h + PAD

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    logo_x = (W - LOGO_W) // 2
    logo_y = PAD
    draw_logo(draw, logo_x, logo_y, LOGO_H, v_color, a_color)

    text_x = (W - w_full) // 2 - bbox_full[0]
    text_y = logo_y + LOGO_H + GAP - bbox_full[1]
    draw.text((text_x, text_y), TEXT, font=font, fill=text_color)

    img.save(out_path, "PNG", optimize=True)


os.makedirs(OUT_DIR, exist_ok=True)

print("Rendering...")
render_horizontal(f"{OUT_DIR}/logo-horizontal-claro.png",
                  v_color=DARK, a_color=COPPER, text_color=DARK)
render_horizontal(f"{OUT_DIR}/logo-horizontal-oscuro.png",
                  v_color=CREAM, a_color=COPPER, text_color=CREAM)
render_vertical(f"{OUT_DIR}/logo-vertical-claro.png",
                v_color=DARK, a_color=COPPER, text_color=DARK)
render_vertical(f"{OUT_DIR}/logo-vertical-oscuro.png",
                v_color=CREAM, a_color=COPPER, text_color=CREAM)

print("Generados:")
for f in sorted(os.listdir(OUT_DIR)):
    if "horizontal" in f or "vertical" in f:
        path = os.path.join(OUT_DIR, f)
        print(f"  {f}  ({os.path.getsize(path)} bytes)")
