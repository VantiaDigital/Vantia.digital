"""
Genera los 4 carruseles de LinkedIn (carrusel-documento 1080x1350, 4:5) como PNGs.
Sigue el brief de assets/downloads/linkedin/programa-carruseles.md:
  - Fondos: dark espresso #1A1813 / olive #3C3A2F / crema #ECE8D8
  - Fraunces (display) + Inter (cuerpo). Cobre #C1834B solo como acento.
  - Numeracion "03 / 08" e isotipo V+A en cierres.

Salida: assets/downloads/linkedin/carruseles/<slug>/slide-XX.png
Correr: python scripts/generate_linkedin_carruseles.py

Data-driven: cada slide es un dict; el renderer generico lo compone.
Tipos de elemento: ("h", texto, size, color)  heading Fraunces (admite \n)
                   ("p", texto, size, color)  parrafo Inter (wrap)
                   ("hero", texto, size, color) numero/palabra grande Fraunces
                   ("list", [items], size, marker_color, text_color, marker)
                   ("gap", px)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT_ROOT = f"{ROOT}/assets/downloads/linkedin/carruseles"

DEEP = (26, 24, 19, 255)     # dark espresso
OLIVE = (60, 58, 47, 255)    # #3C3A2F
CREAM = (236, 232, 216, 255)
COPPER = (193, 131, 75, 255)
MUTED = (169, 155, 128, 255)

BG = {"dark": DEEP, "olive": OLIVE, "crema": CREAM}

W, H, M = 1080, 1350, 96
CW = W - 2 * M

# Isotipo V+A (paths del logo oficial)
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012

_FONTS = {}


def font(family, size):
    key = (family, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(FRAUNCES if family == "fraunces" else INTER, size)
    return _FONTS[key]


def measure(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1], b


def wrap(draw, text, f, max_w):
    out, line = [], ""
    for word in text.split():
        cand = (line + " " + word).strip()
        if measure(draw, cand, f)[0] <= max_w:
            line = cand
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def spaced(text):
    return " ".join(list(text))  # tracking ligero para labels


def draw_logo(draw, x, y, height, v_color, a_color):
    s = height / VBOX_H
    draw.polygon([(x + px * s, y + py * s) for px, py in V_PATH], fill=v_color)
    draw.polygon([(x + px * s, y + py * s) for px, py in A_PATH], fill=a_color)


def footer_logo(draw, bg):
    v_color = CREAM if bg in ("dark", "olive") else DEEP
    logo_h = 46
    logo_w = VBOX_W * (logo_h / VBOX_H)
    text = "Vantia Digital"
    f = font("fraunces", 30)
    wt, ht, bt = measure(draw, text, f)
    gap = 18
    total = logo_w + gap + wt
    sx = (W - total) / 2
    y_base = H - 96
    draw_logo(draw, sx, y_base - logo_h, logo_h, v_color, COPPER)
    draw.text((sx + logo_w + gap, y_base - logo_h / 2 - ht / 2 - bt[1]), text, font=f, fill=v_color)


def build_lines(draw, elements):
    """Lineas renderizables: (text, font, color, marker, marker_color, gap_before, indent)."""
    lines = []
    for el in elements:
        kind = el[0]
        if kind == "gap":
            lines.append(("__gap__", None, None, None, None, el[1], 0))
        elif kind in ("h", "hero"):
            text, size, color = el[1], el[2], el[3]
            f = font("fraunces", size)
            segs = text.split("\n")
            for i, seg in enumerate(segs):
                for j, wl in enumerate(wrap(draw, seg, f, CW)):
                    lines.append((wl, f, color, None, None, 14 if (i == 0 and j == 0) else 8, 0))
        elif kind == "p":
            text, size, color = el[1], el[2], el[3]
            f = font("inter", size)
            for k, wl in enumerate(wrap(draw, text, f, CW)):
                lines.append((wl, f, color, None, None, 12 if k == 0 else 6, 0))
        elif kind == "list":
            items, size, mcolor, tcolor = el[1], el[2], el[3], el[4]
            marker = el[5] if len(el) > 5 else "—"
            f = font("inter", size)
            mw = measure(draw, marker + " ", f)[0]
            for it in items:
                wls = wrap(draw, it, f, CW - mw)
                for j, wl in enumerate(wls):
                    # sangria francesa: la marca solo en la 1a linea; el texto siempre a M+mw
                    lines.append((wl, f, tcolor, marker if j == 0 else None, mcolor, 18 if j == 0 else 6, mw))
    return lines, [None]  # second val unused


def line_h(line, draw):
    if line[0] == "__gap__":
        return line[5]
    f = line[1]
    asc, desc = f.getmetrics()
    return asc + desc


def render(spec, path, idx, total):
    bg = spec["bg"]
    img = Image.new("RGBA", (W, H), BG[bg])
    d = ImageDraw.Draw(img)
    align = spec.get("align", "left")
    has_footer = spec.get("footer", False)

    # Label superior
    top = M
    if spec.get("label"):
        ltext, lcolor = spec["label"]
        lf = font("inter", 24)
        lt = spaced(ltext.upper())
        lw, lh, lb = measure(d, lt, lf)
        lx = M if spec.get("label_align", "left") == "left" else (W - lw) / 2
        d.text((lx, M - lb[1]), lt, font=lf, fill=lcolor)
        top = M + lh + 46

    lines, _ = build_lines(d, spec["elements"])
    total_h = 0
    for ln in lines:
        total_h += line_h(ln, d) + (ln[5] if ln[0] != "__gap__" else 0)

    bottom_limit = H - (170 if has_footer else 110)
    if spec.get("valign", "top") == "center":
        y = top + max(0, (bottom_limit - top - total_h) / 2)
    else:
        y = top + 14

    for ln in lines:
        if ln[0] == "__gap__":
            y += ln[5]
            continue
        text, f, color, marker, mcolor, gap_before, indent = ln
        y += gap_before
        b = d.textbbox((0, 0), text, font=f)
        if align == "center":
            x = (W - (b[2] - b[0])) / 2
        else:
            x = M + indent
            if marker is not None:
                d.text((M, y - b[1]), marker, font=f, fill=mcolor)
        d.text((x, y - b[1]), text, font=f, fill=color)
        y += line_h(ln, d)

    # Numeracion de slide
    nf = font("inter", 24)
    ntxt = f"{idx:02d} / {total:02d}"
    nw, nh, nb = measure(d, ntxt, nf)
    ncolor = MUTED
    d.text((W - M - nw, H - 70 - nb[1]), ntxt, font=nf, fill=ncolor)

    if has_footer:
        footer_logo(d, bg)

    img.save(path, "PNG", optimize=True)


# ──────────────────────────── DATA: 4 CARRUSELES ────────────────────────────

def C_A():
    return [
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "4.000 visitas\neste mes.", 84, CREAM),
            ("gap", 18),
            ("h", "¿Y cuántos\nclientes?", 84, COPPER),
            ("gap", 44),
            ("p", "Las métricas que enseñan no son las que pagan.", 30, MUTED),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "Hay dos tipos de números\nen tu informe.", 56, DEEP),
            ("gap", 30),
            ("p", "Unos te hacen sentir bien.", 38, OLIVE),
            ("p", "Otros te dicen si ganas dinero.", 38, OLIVE),
            ("p", "Casi nunca son los mismos.", 38, COPPER),
        ]},
        {"bg": "olive", "valign": "top", "label": ("Vanidad", MUTED), "elements": [
            ("h", "Métrica de vanidad", 60, CREAM),
            ("gap", 20),
            ("p", "Mide actividad, no resultado. Sube, da subidón, no cambia tu cuenta.", 34, CREAM),
            ("gap", 36),
            ("list", ["Visitas", "Impresiones", "Me gusta", "Seguidores"], 38, MUTED, MUTED, "·"),
        ]},
        {"bg": "olive", "valign": "top", "label": ("Paga facturas", COPPER), "elements": [
            ("h", "Métrica que paga facturas", 56, CREAM),
            ("gap", 20),
            ("p", "Mide decisiones y dinero. No siempre es vistosa. Siempre es útil.", 34, CREAM),
            ("gap", 36),
            ("list", ["Leads", "Coste por lead", "Clientes cerrados", "Retorno por euro"], 38, COPPER, CREAM, "·"),
        ]},
        {"bg": "olive", "valign": "center", "align": "center", "elements": [
            ("h", "La trampa:\nlas de vanidad son\nfáciles de enseñar.", 60, CREAM),
            ("gap", 30),
            ("p", "Por eso llenan los informes bonitos.", 32, MUTED),
        ]},
        {"bg": "dark", "valign": "center", "elements": [
            ("p", "Pregúntale a tu informe una cosa:", 34, MUTED),
            ("gap", 30),
            ("h", "“¿Esta cifra me ayuda\na tomar una decisión?”", 58, COPPER),
            ("gap", 30),
            ("p", "Si la respuesta es no, sobra.", 36, CREAM),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "Nuestra regla,\nsin excepciones:", 56, DEEP),
            ("gap", 28),
            ("h", "si un número no cambia lo que\nvas a hacer mañana,\nno entra en el informe.", 48, OLIVE),
        ]},
        {"bg": "dark", "valign": "center", "footer": True, "elements": [
            ("p", "Tu informe debería decirte una cosa por encima de todo:", 32, MUTED),
            ("gap", 24),
            ("h", "qué euro trabajó\ny cuál se perdió.", 58, CREAM),
            ("gap", 40),
            ("p", "¿El tuyo lo hace? Cuéntanoslo en comentarios.", 32, COPPER),
        ]},
    ]


def C_B():
    return [
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "Tu web\ncarga rápido.", 80, CREAM),
            ("gap", 20),
            ("h", "Y aun así\nno vende.", 80, COPPER),
            ("gap", 44),
            ("p", "Velocidad y conversión no son lo mismo.", 30, MUTED),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("p", "Arreglaste la velocidad. Bien. Una web lenta espanta antes de empezar.", 40, DEEP),
            ("gap", 28),
            ("h", "Pero rápido solo significa\nque la gente se queda.\nNo que actúa.", 50, COPPER),
        ]},
        {"bg": "olive", "valign": "center", "elements": [
            ("p", "CRO es lo que pasa después de que carga:", 34, MUTED),
            ("gap", 30),
            ("list", ["¿entiende la persona qué ofreces?",
                      "¿sabe qué hacer a continuación?",
                      "¿confía lo suficiente para dejarte sus datos?"], 40, COPPER, CREAM, "·"),
        ]},
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "Síntoma típico:\nmucho tráfico,\npocos contactos.", 60, CREAM),
            ("gap", 30),
            ("p", "No es un problema de visitas. Es un problema de qué hacen al llegar.", 32, MUTED),
        ]},
        {"bg": "crema", "valign": "top", "label": ("Dónde se pierde casi siempre", COPPER), "elements": [
            ("list", ["Mensaje confuso en los primeros 3 segundos",
                      "Llamada a la acción escondida o débil",
                      "Formularios que piden de más",
                      "Cero señales de confianza"], 40, COPPER, DEEP, "—"),
        ]},
        {"bg": "dark", "valign": "center", "elements": [
            ("h", "Lo que no se mide aquí,\nno se arregla.", 56, CREAM),
            ("gap", 28),
            ("p", "Mapas de calor, grabaciones de sesión, embudos. Primero ves dónde abandona la gente. Después corriges.", 32, MUTED),
        ]},
        {"bg": "olive", "valign": "center", "align": "center", "elements": [
            ("h", "Optimizar la conversión\ncasi siempre rinde más\nque traer más tráfico.", 52, CREAM),
            ("gap", 34),
            ("p", "El tráfico lo pagas cada mes.", 34, MUTED),
            ("p", "La conversión la arreglas una vez.", 34, COPPER),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "Antes de gastar un euro\nmás en anuncios,\npregúntate qué pasa cuando\nesa gente ya está en tu web.", 52, DEEP),
        ]},
        {"bg": "dark", "valign": "center", "footer": True, "elements": [
            ("h", "Te miramos gratis\nqué frena tu conversión:", 56, CREAM),
            ("gap", 24),
            ("p", "dónde abandona la gente y por qué.", 32, MUTED),
            ("gap", 36),
            ("p", "Escríbenos “CRO” en comentarios o por mensaje.", 32, COPPER),
        ]},
    ]


def C_C():
    # 7 slides: se omite la slide del numero [PENDIENTE] hasta tener el dato real.
    return [
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "Mendieta cerraba\nclientes por", 64, CREAM),
            ("h", "WhatsApp.", 80, COPPER),
            ("gap", 30),
            ("h", "Su informe\nno lo sabía.", 56, CREAM),
            ("gap", 36),
            ("p", "El canal invisible que casi todas las PYMES tienen.", 28, MUTED),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "El problema no era vender.\nVendían.", 56, DEEP),
            ("gap", 30),
            ("p", "El problema era no saber de dónde salía cada venta.", 40, OLIVE),
        ]},
        {"bg": "olive", "valign": "center", "elements": [
            ("h", "Una conversión que no se\natribuye es una conversión\nque no puedes repetir.", 52, CREAM),
            ("gap", 30),
            ("p", "Si no sabes qué la trajo, no sabes qué financiar.", 34, MUTED),
        ]},
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "En el informe,\nel WhatsApp no existía.", 56, CREAM),
            ("gap", 34),
            ("p", "Para los datos: cero.", 34, MUTED),
            ("p", "Para el negocio: una parte enorme de los cierres.", 34, COPPER),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("p", "Qué montamos:", 34, COPPER),
            ("gap", 26),
            ("h", "seguimiento para que cada\nconversación de WhatsApp\nque terminara en contacto\nquedara registrada y atribuida.", 46, DEEP),
        ]},
        {"bg": "dark", "valign": "center", "elements": [
            ("h", "De repente,\nel dato existía.", 60, COPPER),
            ("gap", 30),
            ("p", "Y con el dato, la decisión: dónde invertir más, dónde dejar de tirar dinero.", 34, CREAM),
        ]},
        {"bg": "dark", "valign": "center", "align": "center", "footer": True, "elements": [
            ("h", "¿Sabes qué canal\nte trae más clientes?\n¿O lo intuyes?", 56, CREAM),
            ("gap", 36),
            ("p", "Te ayudamos a que deje de ser una intuición. Hablemos.", 32, COPPER),
        ]},
    ]


def C_D():
    return [
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("h", "Tu próximo cliente\nno buscó en Google.", 58, CREAM),
            ("gap", 26),
            ("h", "Le preguntó\na una IA.", 76, COPPER),
            ("gap", 40),
            ("p", "Y la IA recomendó a otro.", 30, MUTED),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("p", "Cada vez más gente abre ChatGPT, Gemini o Perplexity y pregunta:", 36, DEEP),
            ("gap", 34),
            ("h", "“¿qué [tu sector] me\nrecomiendas por mi zona?”", 50, COPPER),
        ]},
        {"bg": "olive", "valign": "center", "elements": [
            ("h", "La IA no devuelve\ndiez enlaces azules.", 54, CREAM),
            ("gap", 22),
            ("h", "Devuelve tres\no cuatro nombres.", 54, COPPER),
            ("gap", 34),
            ("p", "Si no estás, para ese cliente no existes.", 34, MUTED),
        ]},
        {"bg": "dark", "valign": "center", "align": "center", "elements": [
            ("p", "A esto se le llama", 34, MUTED),
            ("gap", 16),
            ("hero", "GEO", 150, COPPER),
            ("gap", 24),
            ("p", "Generative Engine Optimization.", 34, CREAM),
            ("gap", 14),
            ("p", "Optimizar para que las IA te elijan al responder.", 30, MUTED),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "No sustituye al SEO\nde siempre. Se suma.", 54, DEEP),
            ("gap", 28),
            ("p", "Google sigue importando. Las IA, cada vez más.", 36, OLIVE),
        ]},
        {"bg": "dark", "valign": "top", "label": ("Qué mira una IA para recomendarte", COPPER), "elements": [
            ("list", ["Que tu información sea clara y estructurada",
                      "Que otras fuentes te mencionen",
                      "Que lo que dices encaje con lo que la gente pregunta"], 38, COPPER, CREAM, "—"),
        ]},
        {"bg": "olive", "valign": "center", "elements": [
            ("p", "Lo trabajamos con", 34, MUTED),
            ("gap", 14),
            ("h", "La Estantería:", 60, COPPER),
            ("gap", 24),
            ("p", "SEO técnico y GEO juntos, para aparecer en Google y en las respuestas de IA.", 36, CREAM),
        ]},
        {"bg": "crema", "valign": "center", "elements": [
            ("h", "Es pronto en este terreno.", 52, DEEP),
            ("gap", 24),
            ("h", "Justo por eso conviene\nmoverse ahora,\nno cuando lleguen todos.", 50, COPPER),
        ]},
        {"bg": "dark", "valign": "center", "align": "center", "footer": True, "elements": [
            ("h", "¿Apareces cuando\nle preguntan a una IA\npor tu sector?", 56, CREAM),
            ("gap", 36),
            ("p", "Te lo comprobamos gratis. Escríbenos.", 32, COPPER),
        ]},
    ]


CARRUSELES = {
    "a-vanidad": C_A(),
    "b-cro": C_B(),
    "c-mendieta": C_C(),
    "d-geo": C_D(),
}


def run():
    for slug, slides in CARRUSELES.items():
        d = os.path.join(OUT_ROOT, slug)
        os.makedirs(d, exist_ok=True)
        total = len(slides)
        for i, spec in enumerate(slides, 1):
            render(spec, os.path.join(d, f"slide-{i:02d}.png"), i, total)
        print(f"  {slug}: {total} slides")
    print("Carruseles generados en", OUT_ROOT)


run()
