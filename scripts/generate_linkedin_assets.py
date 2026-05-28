"""
Genera los activos para LinkedIn (empresa Vantia + personal Facundo).

Outputs en assets/downloads/linkedin/:
  - empresa-foto-perfil.png   (400x400 — cuadrado redondeado dark con V+A)
  - empresa-banner.png        (1128x191 — banner empresa)
  - personal-banner.png       (1584x396 — banner personal)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT_DIR = f"{ROOT}/assets/downloads/linkedin"

DEEP   = (26, 24, 19, 255)        # #1A1813
DARK   = (60, 58, 47, 255)        # #3C3A2F
COPPER = (193, 131, 75, 255)      # #C1834B
CREAM  = (236, 232, 216, 255)     # #ECE8D8
MUTED  = (169, 155, 128, 255)     # #A99B80

V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012


def draw_logo(draw, x, y, height, v_color, a_color):
    scale = height / VBOX_H
    v_pts = [(x + px*scale, y + py*scale) for (px, py) in V_PATH]
    a_pts = [(x + px*scale, y + py*scale) for (px, py) in A_PATH]
    draw.polygon(v_pts, fill=v_color)
    draw.polygon(a_pts, fill=a_color)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox


def render_foto_perfil_empresa(out_path):
    """400x400 cuadrado redondeado cream con isotipo V+A centrado."""
    W = H = 400
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = 70
    draw.rounded_rectangle([(0, 0), (W, H)], radius=radius, fill=CREAM)

    logo_h = 230
    logo_scale = logo_h / VBOX_H
    logo_w = VBOX_W * logo_scale
    logo_x = (W - logo_w) / 2
    logo_y = (H - logo_h) / 2
    draw_logo(draw, logo_x, logo_y, logo_h, v_color=DEEP, a_color=COPPER)

    img.save(out_path, "PNG", optimize=True)


def render_banner_empresa(out_path, W=1584, H=268):
    """Banner empresa LinkedIn — solo tipografía (la foto de perfil ya tiene el logo).
    Ratio ~5.9:1 (igual al spec original 1128x191, escalado para mejor calidad)."""
    img = Image.new("RGBA", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    PAD_X = 80

    tagline_pre = "Marketing digital con criterio "
    tagline_accent = "técnico"
    tagline_end = "."

    font_main = ImageFont.truetype(FRAUNCES, 52)
    w_pre, h_pre, b_pre = measure(draw, tagline_pre, font_main)
    w_acc, _, _ = measure(draw, tagline_accent, font_main)
    w_end, _, _ = measure(draw, tagline_end, font_main)
    w_total = w_pre + w_acc + w_end

    text_x = (W - w_total) / 2
    text_y = (H - h_pre) / 2 - b_pre[1] - 10

    draw.text((text_x, text_y), tagline_pre, font=font_main, fill=DEEP)
    draw.text((text_x + w_pre, text_y), tagline_accent, font=font_main, fill=COPPER)
    draw.text((text_x + w_pre + w_acc, text_y), tagline_end, font=font_main, fill=DEEP)

    url = "vantia.digital"
    font_url = ImageFont.truetype(INTER, 20)
    w_url, h_url, bbox_url = measure(draw, url, font_url)
    url_x = (W - w_url) / 2 + 8
    url_y = text_y + h_pre + 18 - bbox_url[1]

    dot_r = 4
    dot_x = url_x - 14
    dot_y = url_y + bbox_url[1] + h_url / 2
    draw.ellipse([(dot_x - dot_r, dot_y - dot_r), (dot_x + dot_r, dot_y + dot_r)], fill=COPPER)
    draw.text((url_x, url_y), url, font=font_url, fill=DARK)

    img.save(out_path, "PNG", optimize=True)


def render_banner_personal(out_path):
    """1584x396 banner personal Facundo. Frase grande izq, logo+rol der.
    LinkedIn corta los bordes en móvil — contenido importante en el 60% central."""
    W, H = 1584, 396
    img = Image.new("RGBA", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    safe_left = W * 0.20
    logo_block_x = W * 0.74

    PHRASE_1 = "Medición seria para PYMES"
    PHRASE_2 = "que prefieren"
    PHRASE_3 = " datos"
    PHRASE_4 = "."

    font_phrase = ImageFont.truetype(FRAUNCES, 44)

    w1, h1, b1 = measure(draw, PHRASE_1, font_phrase)
    w2, h2, b2 = measure(draw, PHRASE_2, font_phrase)
    w3, h3, b3 = measure(draw, PHRASE_3, font_phrase)

    line_gap = 12
    total_h = h1 + line_gap + h2
    start_y = (H - total_h) / 2 - b1[1]

    draw.text((safe_left, start_y), PHRASE_1, font=font_phrase, fill=DEEP)

    second_line_y = start_y + h1 + line_gap + (b1[1] - b2[1])
    draw.text((safe_left, second_line_y), PHRASE_2, font=font_phrase, fill=DEEP)
    draw.text((safe_left + w2, second_line_y), PHRASE_3, font=font_phrase, fill=COPPER)
    draw.text((safe_left + w2 + w3, second_line_y), PHRASE_4, font=font_phrase, fill=DEEP)

    logo_h = 96
    logo_scale = logo_h / VBOX_H
    logo_w = VBOX_W * logo_scale
    logo_x = logo_block_x
    logo_y = H / 2 - logo_h - 12
    draw_logo(draw, logo_x, logo_y, logo_h, v_color=DEEP, a_color=COPPER)

    role_text = "Fundador · Vantia Digital"
    font_role = ImageFont.truetype(INTER, 18)
    role_w, role_h, role_bbox = measure(draw, role_text, font_role)
    role_y = H / 2 + 18 - role_bbox[1]
    draw.text((logo_x, role_y), role_text, font=font_role, fill=DARK)

    img.save(out_path, "PNG", optimize=True)


os.makedirs(OUT_DIR, exist_ok=True)

print("Generando...")
render_foto_perfil_empresa(f"{OUT_DIR}/empresa-foto-perfil.png")
render_banner_empresa(f"{OUT_DIR}/empresa-banner.png")
render_banner_personal(f"{OUT_DIR}/personal-banner.png")

print("Listo:")
for f in sorted(os.listdir(OUT_DIR)):
    path = os.path.join(OUT_DIR, f)
    if os.path.isfile(path):
        print(f"  {f}  ({os.path.getsize(path)} bytes)")
