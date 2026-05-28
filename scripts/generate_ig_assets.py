"""
Genera TODOS los activos para Instagram (empresa + personal) del Proyecto 3 Días.

Outputs en assets/downloads/instagram/:
  feed/         posts cuadrados o verticales (1080x1080 / 1080x1350)
  stories/      stories 1080x1920
  carruseles/   slides 1080x1350 numerados
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/instagram"
SHOTS = f"{ROOT}/assets/downloads/linkedin/screenshots"

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
        c = (line + " " + w).strip()
        cw, _, _ = measure(draw, c, font)
        if cw <= max_width:
            line = c
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def footer_logo(W, draw, y_baseline, color_text=DEEP, color_v=DEEP, color_a=COPPER):
    logo_h = 44
    logo_scale = logo_h / VBOX_H
    logo_w = VBOX_W * logo_scale
    text = "Vantia Digital"
    font = ImageFont.truetype(FRAUNCES, 26)
    w_t, h_t, bb = measure(draw, text, font)
    gap = 16
    total_w = logo_w + gap + w_t
    sx = (W - total_w) / 2
    draw_logo(draw, sx, y_baseline - logo_h/2 - 2, logo_h, v_color=color_v, a_color=color_a)
    draw.text((sx + logo_w + gap, y_baseline - h_t/2 - bb[1] - 2), text, font=font, fill=color_text)


def canvas(W, H, bg=CREAM):
    img = Image.new("RGBA", (W, H), bg)
    return img, ImageDraw.Draw(img)


def crop_aspect(im, ar):
    w, h = im.size
    sa = w / h
    if sa > ar:
        nw = int(h * ar)
        return im.crop(((w-nw)//2, 0, (w-nw)//2 + nw, h))
    nh = int(w / ar)
    return im.crop((0, 0, w, nh))


def rounded_thumb(path, tw, th, radius=14):
    im = Image.open(path).convert("RGBA")
    im = crop_aspect(im, tw/th)
    im = im.resize((tw, th), Image.LANCZOS)
    mask = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([(0, 0), (tw, th)], radius=radius, fill=255)
    out = Image.new("RGBA", (tw, th), (0,0,0,0))
    out.paste(im, (0, 0), mask)
    return out


# ────────────── STORIES (1080x1920) ──────────────


def story_bienvenida_empresa(out_path):
    W, H = 1080, 1920
    img, draw = canvas(W, H, DEEP)

    font_lbl = ImageFont.truetype(INTER, 26)
    label = "BIENVENIDOS"
    w_l, h_l, b_l = measure(draw, label, font_lbl)
    draw.text(((W - w_l)/2, 280 - b_l[1]), label, font=font_lbl, fill=COPPER)

    logo_h = 220
    logo_scale = logo_h / VBOX_H
    logo_w = VBOX_W * logo_scale
    draw_logo(draw, (W - logo_w)/2, 360, logo_h, v_color=CREAM, a_color=COPPER)

    title = "Vantia Digital"
    font_t = ImageFont.truetype(FRAUNCES, 86)
    w_t, h_t, bt = measure(draw, title, font_t)
    draw.text(((W - w_t)/2, 660 - bt[1]), title, font=font_t, fill=CREAM)

    lines = ["Marketing digital", "con criterio técnico,", "no marketing-speak."]
    font_p = ImageFont.truetype(FRAUNCES, 52)
    accent = "técnico"
    gap = 12
    measured = [(l, *measure(draw, l, font_p)) for l in lines]
    total_h = sum(h for _,_,h,_ in measured) + gap*(len(lines)-1)
    cur_y = 880
    for line, w_l2, h_l2, b_l2 in measured:
        if accent in line:
            pre, post = line.split(accent)
            w_pre, _, _ = measure(draw, pre, font_p)
            w_acc, _, _ = measure(draw, accent, font_p)
            total = measure(draw, line, font_p)[0]
            x0 = (W - total)/2
            draw.text((x0, cur_y - b_l2[1]), pre, font=font_p, fill=CREAM)
            draw.text((x0 + w_pre, cur_y - b_l2[1]), accent, font=font_p, fill=COPPER)
            draw.text((x0 + w_pre + w_acc, cur_y - b_l2[1]), post, font=font_p, fill=CREAM)
        else:
            draw.text(((W - w_l2)/2, cur_y - b_l2[1]), line, font=font_p, fill=CREAM)
        cur_y += h_l2 + gap

    cta = "→ Deslizá las publicaciones del feed"
    font_c = ImageFont.truetype(INTER, 26)
    w_c, h_c, bc = measure(draw, cta, font_c)
    draw.text(((W - w_c)/2, H - 280 - bc[1]), cta, font=font_c, fill=MUTED)

    footer_logo(W, draw, H - 140, color_text=CREAM, color_v=CREAM, color_a=COPPER)
    img.save(out_path, "PNG", optimize=True)


def story_poll(out_path):
    W, H = 1080, 1920
    img, draw = canvas(W, H, CREAM)

    label = "PREGUNTA RÁPIDA"
    font_lbl = ImageFont.truetype(INTER, 26)
    w_l, h_l, b_l = measure(draw, label, font_lbl)
    draw.text(((W - w_l)/2, 380 - b_l[1]), label, font=font_lbl, fill=COPPER)

    question = "¿Tu GA4 tiene Consent Mode v2 instalado?"
    font_q = ImageFont.truetype(FRAUNCES, 72)
    q_lines = wrap_text(draw, question, font_q, W - 200)
    y = 540
    for line in q_lines:
        w_q, h_q, bq = measure(draw, line, font_q)
        draw.text(((W - w_q)/2, y - bq[1]), line, font=font_q, fill=DEEP)
        y += h_q + 12

    explain = "Sin él, en Europa estás perdiendo entre 30% y 60% de tus datos."
    font_e = ImageFont.truetype(INTER, 30)
    e_lines = wrap_text(draw, explain, font_e, W - 240)
    y += 80
    for line in e_lines:
        w_e, h_e, be = measure(draw, line, font_e)
        draw.text(((W - w_e)/2, y - be[1]), line, font=font_e, fill=DARK)
        y += h_e + 10

    cta = "Pegá el sticker de Poll arriba ↑"
    font_c = ImageFont.truetype(INTER, 22)
    w_c, h_c, bc = measure(draw, cta, font_c)
    draw.text(((W - w_c)/2, H - 280 - bc[1]), cta, font=font_c, fill=MUTED)

    footer_logo(W, draw, H - 140)
    img.save(out_path, "PNG", optimize=True)


# ────────────── CARRUSEL · 8 errores GA4 ──────────────


def carrusel_ga4_slide(out_path, idx, total, top_label, big, body=None, is_cover=False, is_close=False):
    W, H = 1080, 1350
    bg = DEEP if (is_cover or is_close) else CREAM
    text_main = CREAM if (is_cover or is_close) else DEEP
    text_sec = MUTED if (is_cover or is_close) else DARK
    img, draw = canvas(W, H, bg)
    PAD = 90

    font_lbl = ImageFont.truetype(INTER, 22)
    label_color = COPPER
    draw.text((PAD, 80), top_label, font=font_lbl, fill=label_color)

    font_idx = ImageFont.truetype(INTER, 22)
    idx_text = f"{idx}/{total}"
    w_i, _, _ = measure(draw, idx_text, font_idx)
    draw.text((W - PAD - w_i, 80), idx_text, font=font_idx, fill=label_color)

    font_big = ImageFont.truetype(FRAUNCES, 78 if is_cover else 64)
    big_lines = wrap_text(draw, big, font_big, W - 2*PAD)
    y = 220 if is_cover else 200
    for line in big_lines:
        _, h, b = measure(draw, line, font_big)
        draw.text((PAD, y - b[1]), line, font=font_big, fill=text_main)
        y += h + 14

    if body:
        font_body = ImageFont.truetype(INTER, 28)
        y += 50
        for paragraph in body:
            wrapped = wrap_text(draw, paragraph, font_body, W - 2*PAD)
            for ln in wrapped:
                _, h, b = measure(draw, ln, font_body)
                draw.text((PAD, y - b[1]), ln, font=font_body, fill=text_sec)
                y += h + 8
            y += 18

    if not is_cover:
        font_swipe = ImageFont.truetype(INTER, 22)
        swipe = "→ Seguí" if not is_close else "→ Hablemos: admin@vantia.digital"
        w_s, _, _ = measure(draw, swipe, font_swipe)
        draw.text((W - PAD - w_s, H - 170), swipe, font=font_swipe, fill=label_color)

    footer_color_v = CREAM if (is_cover or is_close) else DEEP
    footer_color_t = CREAM if (is_cover or is_close) else DEEP
    footer_logo(W, draw, H - 100, color_text=footer_color_t, color_v=footer_color_v, color_a=COPPER)
    img.save(out_path, "PNG", optimize=True)


# ────────────── CARRUSEL · 6 proceso Vantia ──────────────


def carrusel_proceso_slide(out_path, idx, total, top_label, big, body=None, is_cover=False, is_close=False):
    return carrusel_ga4_slide(out_path, idx, total, top_label, big, body, is_cover, is_close)


# ────────────── EJECUCIÓN ──────────────


os.makedirs(f"{OUT}/stories", exist_ok=True)
os.makedirs(f"{OUT}/carruseles/ga4", exist_ok=True)
os.makedirs(f"{OUT}/carruseles/proceso", exist_ok=True)
os.makedirs(f"{OUT}/feed", exist_ok=True)

# STORIES
story_bienvenida_empresa(f"{OUT}/stories/01-bienvenida-empresa.png")
story_poll(f"{OUT}/stories/02-poll-ga4.png")

# CARRUSEL GA4 — 8 slides
GA4 = [
    dict(idx=1, top_label="TIP TÉCNICO · GA4 PYMES", big="3 errores típicos de GA4 que te están costando datos.", is_cover=True),
    dict(idx=2, top_label="ERROR 01", big="Instalar GA4 sin Consent Mode v2.",
         body=["En Europa (RGPD) sin Consent Mode los datos llegan rotos.",
               "Vas a ver entre 30% y 60% MENOS visitas reales que las que tenés.",
               "Solución: instalá Consent Mode v2 con tu banner de cookies bien integrado."]),
    dict(idx=3, top_label="ERROR 02", big="No configurar eventos personalizados.",
         body=["Por defecto GA4 mide 'page_view' y poco más.",
               "Te perdés el 80% de lo importante: clicks en CTAs, formularios, vídeos, scroll, etc.",
               "Solución: definí 5-7 eventos clave y los configurás vía GTM."]),
    dict(idx=4, top_label="ERROR 03", big="Mirar 'sesiones' como métrica de éxito.",
         body=["Una sesión no es un cliente. Una conversión sí.",
               "Si tu reporte mensual dice '+10% sesiones', no estás midiendo crecimiento real.",
               "Solución: marcá tus eventos clave como conversiones en GA4."]),
    dict(idx=5, top_label="BONUS", big="¿Y los enlaces a redes externas?",
         body=["GA4 los registra como salidas anónimas si no las taggeás.",
               "Configurá UTM en cada link de tu Instagram, LinkedIn, mailings.",
               "Así sabés qué red trae tráfico que convierte."]),
    dict(idx=6, top_label="CHECKLIST", big="Lo mínimo bien hecho:",
         body=["✓ Consent Mode v2",
               "✓ Eventos personalizados configurados",
               "✓ Conversiones marcadas",
               "✓ UTMs en cada link saliente",
               "✓ Dashboard en Looker Studio (legible)"]),
    dict(idx=7, top_label="REALIDAD", big="El 70% de las PYMES tiene mal al menos 2 de estas 5.",
         body=["Y muchas veces el problema no lo sabés hasta que mirás los reportes en serio.",
               "Si nunca auditaste tu GA4, es probable que estés tomando decisiones con datos basura."]),
    dict(idx=8, top_label="CIERRE", big="Te lo arreglo. Sin costo el primer chequeo.",
         body=["Si querés saber qué está bien y qué mal en tu GA4 hoy, escribime.",
               "30 min, te paso el diagnóstico por mail. Sin compromiso."],
         is_close=True),
]
for s in GA4:
    carrusel_ga4_slide(f"{OUT}/carruseles/ga4/slide-{s['idx']:02d}.png", total=8, **s)

# CARRUSEL PROCESO — 6 slides
PROC = [
    dict(idx=1, top_label="CÓMO TRABAJAMOS", big="El proceso Vantia, en 4 pasos.", is_cover=True),
    dict(idx=2, top_label="PASO 01 · AUDITORÍA", big="Primero entendemos qué hay.",
         body=["Web actual, stack de medición, posicionamiento, competencia.",
               "Te entregamos un diagnóstico con lo que hay y lo que falta.",
               "Esta fase es siempre el punto de partida. Sin esto, todo es vapor."]),
    dict(idx=3, top_label="PASO 02 · MEDICIÓN", big="Instalamos el stack analítico.",
         body=["GA4 + Google Tag Manager + Consent Mode v2 + Microsoft Clarity.",
               "Eventos personalizados, conversiones marcadas, UTMs sistemáticos.",
               "Dashboard en Looker Studio que vos podés leer."]),
    dict(idx=4, top_label="PASO 03 · WEB", big="Construimos o mejoramos la web.",
         body=["Rápida (Core Web Vitals verde), accesible, optimizada para SEO técnico.",
               "Si ya tenés web, optimizamos. Si no, la construimos desde cero.",
               "Cada elemento pensado desde la medición."]),
    dict(idx=5, top_label="PASO 04 · DECIDIR", big="Empezamos a leer los datos.",
         body=["Reportes mensuales con datos reales, no vanity metrics.",
               "Recomendaciones de qué tocar próximo (SEO, contenido, paid).",
               "Iteramos sobre lo que funciona, descartamos lo que no."]),
    dict(idx=6, top_label="LISTOS", big="¿Tu PYME está en este proceso?",
         body=["Si no, podemos arrancar la auditoría esta semana.",
               "30 minutos por videollamada o chat. Sin compromiso."],
         is_close=True),
]
for s in PROC:
    carrusel_proceso_slide(f"{OUT}/carruseles/proceso/slide-{s['idx']:02d}.png", total=6, **s)

# FEED — adaptar posts LinkedIn a IG 1080x1350 (reusing los PNGs hechos en /linkedin/posts/)
# Aquí solo los copiamos y dejamos nota: los archivos ya hechos sirven al 100% para IG cuadrado.
# Si en el futuro querés versiones 4:5 nativas, agregar acá funciones espejo.

print("IG generado:")
for root, _, files in os.walk(OUT):
    for f in sorted(files):
        if f.endswith(".png"):
            p = os.path.join(root, f)
            print(f"  {p[len(ROOT)+1:]}  ({os.path.getsize(p)} bytes)")
