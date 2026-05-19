"""
Tarjeta de contacto empresarial — Vantia · Marketing Digital.
Estilo: corporativo clásico, sobrio, sin extras forzados.

FRENTE  → logo + nombre, centrado vertical y horizontal
REVERSO → datos de contacto + QR a vantia.digital

Output (4 archivos):
  assets/downloads/vantia-tarjeta-frente.pdf  + .png
  assets/downloads/vantia-tarjeta-reverso.pdf + .png
"""

import io, os
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import qrcode
import fitz

# ────────────────────────────────────────────
# Setup
# ────────────────────────────────────────────
ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FONTS_DIR = f"{ROOT}/assets/fonts"
OUT_DIR = f"{ROOT}/assets/downloads"
os.makedirs(OUT_DIR, exist_ok=True)

# Fraunces para títulos (serif), Inter Variable (TTF completo) para texto/datos
pdfmetrics.registerFont(TTFont('Fraunces', f'{FONTS_DIR}/Fraunces-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inter', f'{FONTS_DIR}/Inter-Variable.ttf'))

# Paleta oficial Vantia
DARK   = HexColor('#1A1813')
OLIVE  = HexColor('#3C3A2F')
COPPER = HexColor('#C1834B')
CREAM  = HexColor('#ECE8D8')
MUTED  = HexColor('#A99B80')

CARD_W, CARD_H = 85*mm, 55*mm

# Logo SVG paths (viewBox 1269 x 1012)
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012


# ────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────
def draw_logo(c, x, y, width):
    """V+A logo. (x, y) = top-left esquina, width en pts."""
    scale = width / VBOX_W
    height = VBOX_H * scale
    c.saveState()
    c.translate(x, y - height)
    c.scale(scale, scale)
    c.translate(0, VBOX_H)
    c.scale(1, -1)
    # V cream
    p = c.beginPath()
    p.moveTo(*V_PATH[0])
    for pt in V_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(CREAM)
    c.drawPath(p, fill=1, stroke=0)
    # A cobre
    p = c.beginPath()
    p.moveTo(*A_PATH[0])
    for pt in A_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(COPPER)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def make_qr(data):
    qr = qrcode.QRCode(
        version=None, box_size=20, border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1A1813", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return ImageReader(buf)


def setup_canvas(filepath, title_suffix):
    c = canvas.Canvas(filepath, pagesize=(CARD_W, CARD_H))
    c.setTitle(f"Vantia · Marketing Digital — {title_suffix}")
    c.setAuthor("Vantia · Marketing Digital")
    return c


def draw_bg(c):
    c.setFillColor(DARK)
    c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)


# ────────────────────────────────────────────
# FRENTE — Logo + nombre, centrado
# ────────────────────────────────────────────
def render_front(filepath):
    c = setup_canvas(filepath, "frente")
    draw_bg(c)

    # Logo grande centrado horizontal y vertical
    LOGO_W = 26*mm
    LOGO_H = LOGO_W * (VBOX_H / VBOX_W)  # 20.7mm

    # Composición vertical: logo + gap + nombre. Centrado en el card.
    GAP = 5*mm
    NAME_H = 6*mm  # altura aprox del texto
    TOTAL_H = LOGO_H + GAP + NAME_H

    # Top y del bloque centrado verticalmente
    block_top = (CARD_H + TOTAL_H) / 2

    logo_x = (CARD_W - LOGO_W) / 2
    logo_y = block_top  # top-left
    draw_logo(c, x=logo_x, y=logo_y, width=LOGO_W)

    # Nombre debajo del logo
    name_baseline_y = block_top - LOGO_H - GAP - 4.2*mm  # ajuste por baseline
    c.setFont('Fraunces', 13)

    # Componer "Vantia · Marketing Digital" centrado, con "·" cobre
    left = "Vantia "
    mid = "·"
    right = " Marketing Digital"
    w_left  = c.stringWidth(left,  'Fraunces', 13)
    w_mid   = c.stringWidth(mid,   'Fraunces', 13)
    w_right = c.stringWidth(right, 'Fraunces', 13)
    total_w = w_left + w_mid + w_right
    start_x = (CARD_W - total_w) / 2

    c.setFillColor(CREAM)
    c.drawString(start_x, name_baseline_y, left)
    c.setFillColor(COPPER)
    c.drawString(start_x + w_left, name_baseline_y, mid)
    c.setFillColor(CREAM)
    c.drawString(start_x + w_left + w_mid, name_baseline_y, right)

    c.showPage()
    c.save()


# ────────────────────────────────────────────
# REVERSO — Datos + QR
# ────────────────────────────────────────────
def render_back(filepath):
    c = setup_canvas(filepath, "reverso")
    draw_bg(c)

    MARGIN = 7*mm

    # Columna izquierda: datos
    label_y = CARD_H - 10*mm
    c.setFillColor(COPPER)
    c.setFont('Inter', 6.5)
    c.drawString(MARGIN, label_y, "CONTACTO")

    # Hairline cobre debajo del label
    c.setStrokeColor(COPPER)
    c.setLineWidth(0.4)
    c.line(MARGIN, label_y - 1.8*mm, MARGIN + 12*mm, label_y - 1.8*mm)

    # Datos en stack vertical
    c.setFillColor(CREAM)
    c.setFont('Inter', 8.5)
    y = label_y - 7*mm
    line_h = 4.5*mm
    for line in ["admin@vantia.digital", "+34 645 720 420", "vantia.digital"]:
        c.drawString(MARGIN, y, line)
        y -= line_h

    # Ubicación más muted
    c.setFillColor(MUTED)
    c.setFont('Inter', 7)
    c.drawString(MARGIN, y - 0.5*mm, "Barcelona, España")

    # QR a la derecha, vertical center
    QR_SIZE = 22*mm
    qr_x = CARD_W - MARGIN - QR_SIZE
    qr_y = (CARD_H - QR_SIZE) / 2

    c.drawImage(make_qr("https://www.vantia.digital/"),
                qr_x, qr_y, width=QR_SIZE, height=QR_SIZE, mask='auto')

    c.showPage()
    c.save()


# ────────────────────────────────────────────
# PDF → PNG 300 DPI
# ────────────────────────────────────────────
def pdf_to_png(pdf_path, png_path, dpi=300):
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom = dpi / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    pix.save(png_path)
    doc.close()


# ────────────────────────────────────────────
# Ejecución
# ────────────────────────────────────────────
files = {
    "frente":  f"{OUT_DIR}/vantia-tarjeta-frente",
    "reverso": f"{OUT_DIR}/vantia-tarjeta-reverso",
}

render_front(f"{files['frente']}.pdf")
render_back(f"{files['reverso']}.pdf")

for side, base in files.items():
    pdf_to_png(f"{base}.pdf", f"{base}.png", dpi=300)

print("Generados:")
for side, base in files.items():
    for ext in ("pdf", "png"):
        path = f"{base}.{ext}"
        size = os.path.getsize(path)
        print(f"  {path}  ({size} bytes)")
