"""
Genera plantillas PNG de posts iniciales para LinkedIn (1080x1080 cuadrado o 1080x1350 vertical 4:5).
Fondo cream + logo principal V dark + A cobre.

Outputs en assets/downloads/linkedin/posts/:
EMPRESA (3 nuevos, enfoque portfolio + tesis):
  - empresa-01-bienvenida-corta.png   (1080x1080) — presentación mínima
  - empresa-02-portfolio.png          (1080x1350) — 3 capturas de clientes reales
  - empresa-03-tesis-hubspot.png      (1080x1080) — opinión técnica fuerte

PERSONAL (no se tocan, regenerados con misma lógica que antes):
  - personal-01-anuncio.png
  - personal-02-tecnico.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT_DIR = f"{ROOT}/assets/downloads/linkedin/posts"
SHOTS_DIR = f"{ROOT}/assets/downloads/linkedin/screenshots"

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


def draw_logo(draw, x, y, height, v_color=DEEP, a_color=COPPER):
    scale = height / VBOX_H
    v_pts = [(x + px*scale, y + py*scale) for (px, py) in V_PATH]
    a_pts = [(x + px*scale, y + py*scale) for (px, py) in A_PATH]
    draw.polygon(v_pts, fill=v_color)
    draw.polygon(a_pts, fill=a_color)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for w in words:
        candidate = (line + " " + w).strip()
        cw, _, _ = measure(draw, candidate, font)
        if cw <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def add_footer_logo(W, draw, y_baseline):
    logo_h = 48
    logo_scale = logo_h / VBOX_H
    logo_w = VBOX_W * logo_scale
    text = "Vantia Digital"
    font = ImageFont.truetype(FRAUNCES, 28)
    w_t, h_t, bbox_t = measure(draw, text, font)
    gap = 18
    total_w = logo_w + gap + w_t
    start_x = (W - total_w) / 2
    logo_y = y_baseline - logo_h / 2 - 4
    draw_logo(draw, start_x, logo_y, logo_h, v_color=DEEP, a_color=COPPER)
    text_x = start_x + logo_w + gap
    text_y = y_baseline - h_t / 2 - bbox_t[1] - 4
    draw.text((text_x, text_y), text, font=font, fill=DEEP)


def new_canvas(W=1080, H=1080):
    img = Image.new("RGBA", (W, H), CREAM)
    return img, ImageDraw.Draw(img)


def crop_to_aspect(im, target_aspect):
    """Recorta imagen al aspect ratio target (w/h). Foco en parte superior (hero)."""
    w, h = im.size
    src_aspect = w / h
    if src_aspect > target_aspect:
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_aspect)
        return im.crop((0, 0, w, new_h))


def rounded_thumb(path, target_w, target_h, radius=14):
    """Devuelve un thumbnail con bordes redondeados, recortado a target aspect."""
    im = Image.open(path).convert("RGBA")
    im = crop_to_aspect(im, target_w / target_h)
    im = im.resize((target_w, target_h), Image.LANCZOS)
    mask = Image.new("L", (target_w, target_h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([(0, 0), (target_w, target_h)], radius=radius, fill=255)
    rounded = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    rounded.paste(im, (0, 0), mask)
    return rounded


# ──────────────────────────── EMPRESA · POSTS ────────────────────────────


def render_empresa_01_bienvenida_corta(out_path):
    """1080x1080 — bienvenida cortita, 3 líneas."""
    W = H = 1080
    img, draw = new_canvas(W, H)

    top_label = "VANTIA DIGITAL · BARCELONA"
    font_lbl = ImageFont.truetype(INTER, 22)
    w_lbl, h_lbl, b_lbl = measure(draw, top_label, font_lbl)
    draw.text(((W - w_lbl) / 2, 200 - b_lbl[1]), top_label, font=font_lbl, fill=COPPER)

    lines = ["Acá estamos.", "Ingeniería web + analítica seria", "para PYMES."]
    font_main = ImageFont.truetype(FRAUNCES, 64)
    gap = 18

    measured = [(line, *measure(draw, line, font_main)) for line in lines]
    total_h = sum(h for _, _, h, _ in measured) + gap * (len(lines) - 1)
    start_y = (H - total_h) / 2 - 30

    cur_y = start_y
    for line, w_l, h_l, b_l in measured:
        draw.text(((W - w_l) / 2, cur_y - b_l[1]), line, font=font_main, fill=DEEP)
        cur_y += h_l + gap

    email = "admin@vantia.digital"
    font_em = ImageFont.truetype(INTER, 28)
    w_em, h_em, b_em = measure(draw, email, font_em)
    draw.text(((W - w_em) / 2, H - 200 - b_em[1]), email, font=font_em, fill=DARK)

    add_footer_logo(W, draw, y_baseline=970)
    img.save(out_path, "PNG", optimize=True)


def render_empresa_02_portfolio(out_path):
    """1080x1350 — 3 capturas de clientes apiladas. Honesto: arrancamos, datos a 90 días."""
    W, H = 1080, 1350
    img, draw = new_canvas(W, H)

    PAD = 90
    top_label = "PRIMEROS SITIOS · BARCELONA"
    font_lbl = ImageFont.truetype(INTER, 22)
    w_lbl, h_lbl, b_lbl = measure(draw, top_label, font_lbl)
    draw.text((PAD, 80 - b_lbl[1]), top_label, font=font_lbl, fill=COPPER)

    title = "Construimos. Medimos desde día 1."
    font_title = ImageFont.truetype(FRAUNCES, 54)
    title_lines = wrap_text(draw, title, font_title, W - 2 * PAD)
    y = 130
    for line in title_lines:
        w_l, h_l, b_l = measure(draw, line, font_title)
        draw.text((PAD, y - b_l[1]), line, font=font_title, fill=DEEP)
        y += h_l + 8

    y += 40

    thumbs = [
        ("gett.png",        "GeTT Studio",          "Estudio de diseño · Barcelona"),
        ("parrilleros.png", "Los Hermanos Parrilleros", "Asado argentino · Barcelona"),
        ("estanteria.png",  "La Estantería",        "Editorial de cuentos · Barcelona"),
    ]

    thumb_w = W - 2 * PAD
    thumb_h = 220
    font_name = ImageFont.truetype(FRAUNCES, 28)
    font_meta = ImageFont.truetype(INTER, 20)
    block_gap = 18

    for fname, name, meta in thumbs:
        path = os.path.join(SHOTS_DIR, fname)
        if os.path.exists(path):
            thumb = rounded_thumb(path, thumb_w, thumb_h, radius=12)
            img.paste(thumb, (PAD, int(y)), thumb)
        else:
            draw.rounded_rectangle([(PAD, y), (PAD + thumb_w, y + thumb_h)], radius=12, fill=DARK)

        y += thumb_h + 14
        w_n, h_n, b_n = measure(draw, name, font_name)
        draw.text((PAD, y - b_n[1]), name, font=font_name, fill=DEEP)
        y += h_n + 4
        w_m, h_m, b_m = measure(draw, meta, font_meta)
        draw.text((PAD, y - b_m[1]), meta, font=font_meta, fill=MUTED)
        y += h_m + block_gap

    footer_note = "Primeros números a 90 días."
    font_note = ImageFont.truetype(INTER, 22)
    w_fn, h_fn, b_fn = measure(draw, footer_note, font_note)
    draw.text(((W - w_fn) / 2, H - 130 - b_fn[1]), footer_note, font=font_note, fill=DARK)

    add_footer_logo(W, draw, y_baseline=H - 70)
    img.save(out_path, "PNG", optimize=True)


def render_empresa_03_tesis_hubspot(out_path):
    """1080x1080 — tesis fuerte: PYMES no necesitan HubSpot todavía."""
    W = H = 1080
    img, draw = new_canvas(W, H)

    top_label = "OPINIÓN · TESIS TÉCNICA"
    font_lbl = ImageFont.truetype(INTER, 22)
    w_lbl, h_lbl, b_lbl = measure(draw, top_label, font_lbl)
    draw.text(((W - w_lbl) / 2, 160 - b_lbl[1]), top_label, font=font_lbl, fill=COPPER)

    lines = ["PYMES no necesitan", "HubSpot", "todavía."]
    accents = {"HubSpot": COPPER}
    font_main = ImageFont.truetype(FRAUNCES, 88)
    gap = 22

    measured = [(line, *measure(draw, line, font_main)) for line in lines]
    total_h = sum(h for _, _, h, _ in measured) + gap * (len(lines) - 1)
    start_y = (H - total_h) / 2 - 80

    cur_y = start_y
    for line, w_l, h_l, b_l in measured:
        color = accents.get(line, DEEP)
        draw.text(((W - w_l) / 2, cur_y - b_l[1]), line, font=font_main, fill=color)
        cur_y += h_l + gap

    subtitle = "Primero medí bien GA4. Después invertí en CRM caro."
    font_sub = ImageFont.truetype(INTER, 26)
    sub_lines = wrap_text(draw, subtitle, font_sub, W - 200)
    sy = cur_y + 50
    for sline in sub_lines:
        w_s, h_s, b_s = measure(draw, sline, font_sub)
        draw.text(((W - w_s) / 2, sy - b_s[1]), sline, font=font_sub, fill=DARK)
        sy += h_s + 6

    add_footer_logo(W, draw, y_baseline=970)
    img.save(out_path, "PNG", optimize=True)


# ──────────────────────────── PERSONAL · POSTS (sin cambios) ────────────────────────────


def render_personal_01_anuncio(out_path):
    """1080x1080 — anuncio personal Facundo presenta Vantia."""
    W = H = 1080
    img, draw = new_canvas(W, H)
    PAD = 100

    top_label = "FACUNDO GOETTE · ANUNCIO"
    font_lbl = ImageFont.truetype(INTER, 22)
    draw.text((PAD, 130), top_label, font=font_lbl, fill=COPPER)

    title = "Fundé Vantia porque vi un patrón."
    font_title = ImageFont.truetype(FRAUNCES, 56)
    title_lines = wrap_text(draw, title, font_title, W - 2 * PAD)
    y = 210
    for line in title_lines:
        _, h, b = measure(draw, line, font_title)
        draw.text((PAD, y - b[1]), line, font=font_title, fill=DEEP)
        y += h + 12

    y += 50
    font_b = ImageFont.truetype(INTER, 30)
    bullets = [
        "Las PYMES contratan agencias que venden estrategia.",
        "Pero a los 6 meses nadie sabe qué funcionó.",
        "Vantia nace de medir todo desde el día uno.",
        "Si tenés una PYME, hablemos.",
    ]
    for b_text in bullets:
        dash = "—"
        _, h_d, bd = measure(draw, dash, font_b)
        draw.text((PAD, y - bd[1]), dash, font=font_b, fill=COPPER)
        w_d, _, _ = measure(draw, dash + " ", font_b)
        wrapped = wrap_text(draw, b_text, font_b, W - 2 * PAD - w_d)
        for wl in wrapped:
            _, hh, bb = measure(draw, wl, font_b)
            draw.text((PAD + w_d, y - bb[1]), wl, font=font_b, fill=DARK)
            y += hh + 8
        y += 14

    add_footer_logo(W, draw, y_baseline=970)
    img.save(out_path, "PNG", optimize=True)


def render_personal_02_tecnico(out_path):
    """1080x1080 — tip técnico: 3 errores GA4 en PYMES."""
    W = H = 1080
    img, draw = new_canvas(W, H)
    PAD = 100

    top_label = "MEDICIÓN · TIP TÉCNICO"
    font_lbl = ImageFont.truetype(INTER, 22)
    draw.text((PAD, 130), top_label, font=font_lbl, fill=COPPER)

    title = "3 errores típicos de GA4 en PYMES."
    font_title = ImageFont.truetype(FRAUNCES, 56)
    title_lines = wrap_text(draw, title, font_title, W - 2 * PAD)
    y = 210
    for line in title_lines:
        _, h, b = measure(draw, line, font_title)
        draw.text((PAD, y - b[1]), line, font=font_title, fill=DEEP)
        y += h + 12

    y += 50
    font_b = ImageFont.truetype(INTER, 30)
    bullets = [
        "Instalar GA4 sin Consent Mode v2 (datos rotos en Europa).",
        "No configurar eventos personalizados (te perdés el 80%).",
        "Mirar 'sesiones' en vez de 'eventos clave' como conversión.",
        "Si tenés alguno, te lo arreglo. Sin costo el primer chequeo.",
    ]
    for b_text in bullets:
        dash = "—"
        _, h_d, bd = measure(draw, dash, font_b)
        draw.text((PAD, y - bd[1]), dash, font=font_b, fill=COPPER)
        w_d, _, _ = measure(draw, dash + " ", font_b)
        wrapped = wrap_text(draw, b_text, font_b, W - 2 * PAD - w_d)
        for wl in wrapped:
            _, hh, bb = measure(draw, wl, font_b)
            draw.text((PAD + w_d, y - bb[1]), wl, font=font_b, fill=DARK)
            y += hh + 8
        y += 14

    add_footer_logo(W, draw, y_baseline=970)
    img.save(out_path, "PNG", optimize=True)


# ──────────────────────────── EJECUCIÓN ────────────────────────────


os.makedirs(OUT_DIR, exist_ok=True)

# Limpiar viejos posts empresa que ya no se usan
for old in ["empresa-01-bienvenida.png", "empresa-02-servicio.png", "empresa-03-manifiesto.png"]:
    old_path = os.path.join(OUT_DIR, old)
    if os.path.exists(old_path):
        os.remove(old_path)

render_empresa_01_bienvenida_corta(f"{OUT_DIR}/empresa-01-bienvenida-corta.png")
render_empresa_02_portfolio(f"{OUT_DIR}/empresa-02-portfolio.png")
render_empresa_03_tesis_hubspot(f"{OUT_DIR}/empresa-03-tesis-hubspot.png")
render_personal_01_anuncio(f"{OUT_DIR}/personal-01-anuncio.png")
render_personal_02_tecnico(f"{OUT_DIR}/personal-02-tecnico.png")

print("Posts generados:")
for f in sorted(os.listdir(OUT_DIR)):
    path = os.path.join(OUT_DIR, f)
    if os.path.isfile(path):
        print(f"  {f}  ({os.path.getsize(path)} bytes)")
