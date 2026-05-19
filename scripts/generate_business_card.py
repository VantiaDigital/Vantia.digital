"""
Generador de tarjeta de contacto de Vantia · Marketing Digital.
Genera 4 archivos: frente y reverso, en PDF (vector) y PNG (300 DPI).

Output:
  assets/downloads/vantia-tarjeta-frente.pdf
  assets/downloads/vantia-tarjeta-frente.png
  assets/downloads/vantia-tarjeta-reverso.pdf
  assets/downloads/vantia-tarjeta-reverso.png
"""

import io, os
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import qrcode
import fitz  # PyMuPDF — para convertir PDF a PNG

# ────────────────────────────────────────────
# Setup
# ────────────────────────────────────────────
ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FONTS_DIR = f"{ROOT}/assets/fonts"
OUT_DIR = f"{ROOT}/assets/downloads"
os.makedirs(OUT_DIR, exist_ok=True)

pdfmetrics.registerFont(TTFont('Fraunces', f'{FONTS_DIR}/Fraunces-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inter', f'{FONTS_DIR}/Inter-Regular.ttf'))

# Brand palette
DARK   = HexColor('#1A1813')
OLIVE  = HexColor('#3C3A2F')
COPPER = HexColor('#C1834B')
CREAM  = HexColor('#ECE8D8')
MUTED  = HexColor('#A99B80')

# Card dimensions: 85 x 55 mm landscape
CARD_W, CARD_H = 85*mm, 55*mm

# Logo SVG paths (V + A interlocking, viewBox 1269 x 1012)
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
    """V+A logo. (x, y) = top-left esquina, width en pts. Eje y de reportlab: arriba."""
    scale = width / VBOX_W
    height = VBOX_H * scale
    c.saveState()
    c.translate(x, y - height)
    c.scale(scale, scale)
    c.translate(0, VBOX_H)
    c.scale(1, -1)  # SVG y va para abajo, PDF y va para arriba

    # V — cream
    p = c.beginPath()
    p.moveTo(*V_PATH[0])
    for pt in V_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(CREAM)
    c.drawPath(p, fill=1, stroke=0)

    # A — copper
    p = c.beginPath()
    p.moveTo(*A_PATH[0])
    for pt in A_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(COPPER)
    c.drawPath(p, fill=1, stroke=0)

    c.restoreState()


def make_qr(data):
    """QR negro sobre blanco, ImageReader para reportlab."""
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


def setup_canvas(filepath):
    c = canvas.Canvas(filepath, pagesize=(CARD_W, CARD_H))
    c.setTitle("Vantia · Marketing Digital — Tarjeta de contacto")
    c.setAuthor("Vantia · Marketing Digital")
    return c


def draw_bg(c):
    """Fondo dark + accent cobre superior."""
    c.setFillColor(DARK)
    c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)
    c.setFillColor(COPPER)
    c.rect(0, CARD_H - 0.6*mm, CARD_W, 0.6*mm, fill=1, stroke=0)


# ────────────────────────────────────────────
# FRENTE — Brand showcase, centrado y minimal
# ────────────────────────────────────────────
def render_front(filepath):
    c = setup_canvas(filepath)
    draw_bg(c)

    # Logo grande centrado horizontalmente
    LOGO_W = 22*mm
    logo_x = (CARD_W - LOGO_W) / 2
    logo_y = CARD_H - 11*mm  # top-left y
    draw_logo(c, x=logo_x, y=logo_y, width=LOGO_W)

    # "Vantia" — serif grande, debajo del logo, centrado
    c.setFillColor(CREAM)
    c.setFont('Fraunces', 18)
    title_y = CARD_H - 32*mm
    c.drawCentredString(CARD_W/2, title_y, "Vantia")

    # "· Marketing Digital" — debajo, más chico, con punto medio cobre
    c.setFont('Fraunces', 11)
    sub = "· Marketing Digital"
    # Medir width de cada parte para centrar y colorear el "·"
    dot_w = c.stringWidth("·", 'Fraunces', 11)
    rest_w = c.stringWidth(" Marketing Digital", 'Fraunces', 11)
    total_w = dot_w + rest_w
    start_x = (CARD_W - total_w) / 2
    sub_y = title_y - 6*mm
    c.setFillColor(COPPER)
    c.drawString(start_x, sub_y, "·")
    c.setFillColor(CREAM)
    c.drawString(start_x + dot_w, sub_y, " Marketing Digital")

    # Tagline
    c.setFillColor(MUTED)
    c.setFont('Inter', 6.5)
    c.drawCentredString(CARD_W/2, sub_y - 7*mm,
                        "Agencia técnica  ·  Ingeniería Web  ·  SEO + GEO  ·  Paid Media")

    c.showPage()
    c.save()


# ────────────────────────────────────────────
# REVERSO — Datos de contacto + QRs
# ────────────────────────────────────────────
def render_back(filepath):
    c = setup_canvas(filepath)
    draw_bg(c)

    # Eyebrow "CONTACTO"
    c.setFillColor(COPPER)
    c.setFont('Inter', 6)
    eyebrow_y = CARD_H - 8*mm
    c.drawString(6*mm, eyebrow_y, "CONTACTO")

    # Línea hairline debajo del eyebrow
    c.setStrokeColor(COPPER)
    c.setLineWidth(0.4)
    c.line(6*mm, eyebrow_y - 1.5*mm, 22*mm, eyebrow_y - 1.5*mm)

    # Datos de contacto — columna izquierda
    c.setFillColor(CREAM)
    c.setFont('Inter', 9)
    y = CARD_H - 16*mm
    line_h = 5*mm
    c.drawString(6*mm, y, "admin@vantia.digital")
    c.drawString(6*mm, y - line_h, "+34 645 720 420")
    c.drawString(6*mm, y - 2*line_h, "vantia.digital")

    c.setFillColor(MUTED)
    c.setFont('Inter', 7)
    c.drawString(6*mm, y - 3*line_h - 0.5*mm, "Barcelona, España")

    # QRs — columna derecha, mismo nivel
    QR_SIZE = 17*mm
    qr_y = (CARD_H - QR_SIZE) / 2 - 1*mm  # vertical center, ligeramente bajo
    qr_x_wa = CARD_W - 6*mm - QR_SIZE
    qr_x_web = qr_x_wa - QR_SIZE - 3*mm

    # QR Web
    c.drawImage(make_qr("https://vantia.digital"),
                qr_x_web, qr_y, width=QR_SIZE, height=QR_SIZE, mask='auto')
    c.setFillColor(MUTED)
    c.setFont('Inter', 5.5)
    c.drawCentredString(qr_x_web + QR_SIZE/2, qr_y - 2*mm, "SITIO WEB")

    # QR WhatsApp
    wa_url = ("https://wa.me/34645720420"
              "?text=Hola%20Vantia%20Digital%2C%20me%20gustar%C3%ADa%20agendar%20una%20sesi%C3%B3n%20gratuita.")
    c.drawImage(make_qr(wa_url),
                qr_x_wa, qr_y, width=QR_SIZE, height=QR_SIZE, mask='auto')
    c.drawCentredString(qr_x_wa + QR_SIZE/2, qr_y - 2*mm, "WHATSAPP")

    c.showPage()
    c.save()


# ────────────────────────────────────────────
# PDF → PNG (300 DPI)
# ────────────────────────────────────────────
def pdf_to_png(pdf_path, png_path, dpi=300):
    """Renderiza la primera página de PDF a PNG a la DPI indicada."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    # PyMuPDF usa zoom factor (1.0 = 72 DPI)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(png_path)
    doc.close()


# ────────────────────────────────────────────
# Ejecución
# ────────────────────────────────────────────
files = {
    "frente": f"{OUT_DIR}/vantia-tarjeta-frente",
    "reverso": f"{OUT_DIR}/vantia-tarjeta-reverso",
}

# Render PDFs (vector)
render_front(f"{files['frente']}.pdf")
render_back(f"{files['reverso']}.pdf")

# Convert each PDF → PNG (raster 300 DPI)
for side, base in files.items():
    pdf_to_png(f"{base}.pdf", f"{base}.png", dpi=300)

# Limpiar el archivo viejo de tarjeta única
old = f"{OUT_DIR}/vantia-tarjeta-contacto.pdf"
if os.path.exists(old):
    os.remove(old)
    print(f"REMOVED: {old}")

# Resumen
print("\nGenerados:")
for side, base in files.items():
    for ext in ("pdf", "png"):
        path = f"{base}.{ext}"
        size = os.path.getsize(path)
        print(f"  {path}  ({size} bytes)")
