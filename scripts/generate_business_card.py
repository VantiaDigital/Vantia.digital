"""
Generador de tarjeta de contacto PDF para Vantia.
Output: assets/downloads/vantia-tarjeta-contacto.pdf
"""

import io, os
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import qrcode

# === Paths ===
ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FONTS_DIR = f"{ROOT}/assets/fonts"
OUT_DIR = f"{ROOT}/assets/downloads"
os.makedirs(OUT_DIR, exist_ok=True)
OUT = f"{OUT_DIR}/vantia-tarjeta-contacto.pdf"

# === Fonts ===
pdfmetrics.registerFont(TTFont('Fraunces', f'{FONTS_DIR}/Fraunces-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inter', f'{FONTS_DIR}/Inter-Regular.ttf'))

# === Brand palette ===
DARK = HexColor('#1A1813')
OLIVE = HexColor('#3C3A2F')
COPPER = HexColor('#C1834B')
CREAM = HexColor('#ECE8D8')
MUTED = HexColor('#A99B80')

# === Card dims (business card landscape) ===
CARD_W, CARD_H = 85*mm, 55*mm

# === QR generator ===
def make_qr(data):
    """White bg, dark squares — scaneable sobre cualquier fondo."""
    qr = qrcode.QRCode(
        version=None,
        box_size=20,
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1A1813", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return ImageReader(buf)

# === Logo SVG paths (V + A interlocking) ===
# Coordinates from /assets/images/logo.svg (viewBox 1269 x 1012)
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VIEWBOX_W, VIEWBOX_H = 1269, 1012

def draw_logo(c, x, y, width):
    """Draw V+A logo at (x,y), with given width in pts. y = top-left of logo."""
    scale = width / VIEWBOX_W
    height = VIEWBOX_H * scale
    c.saveState()
    c.translate(x, y - height)
    c.scale(scale, scale)
    # SVG y-axis is down, PDF is up. Flip vertically:
    c.translate(0, VIEWBOX_H)
    c.scale(1, -1)
    # V
    p = c.beginPath()
    p.moveTo(*V_PATH[0])
    for pt in V_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(CREAM)
    c.drawPath(p, fill=1, stroke=0)
    # A
    p = c.beginPath()
    p.moveTo(*A_PATH[0])
    for pt in A_PATH[1:]: p.lineTo(*pt)
    p.close()
    c.setFillColor(COPPER)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

# ============================================
# CANVAS
# ============================================
c = canvas.Canvas(OUT, pagesize=(CARD_W, CARD_H))
c.setTitle("Vantia · Marketing Digital — Tarjeta de contacto")
c.setAuthor("Vantia · Marketing Digital")
c.setSubject("Contact card")
c.setKeywords("vantia digital marketing")

# Background — deep dark
c.setFillColor(DARK)
c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)

# Subtle copper accent — top strip 0.6mm
c.setFillColor(COPPER)
c.rect(0, CARD_H - 0.6*mm, CARD_W, 0.6*mm, fill=1, stroke=0)

# Logo (top-left)
LOGO_W = 14*mm
draw_logo(c, x=5*mm, y=CARD_H - 5*mm, width=LOGO_W)

# Brand name (right of logo)
text_x = 5*mm + LOGO_W + 3*mm
brand_y = CARD_H - 11*mm
c.setFillColor(CREAM)
c.setFont('Fraunces', 14)
c.drawString(text_x, brand_y, "Vantia")

# middle dot (copper italic visual)
brand_w = c.stringWidth("Vantia", 'Fraunces', 14)
c.setFillColor(COPPER)
c.drawString(text_x + brand_w + 1.5*mm, brand_y, "·")

# "Marketing Digital"
md_x = text_x + brand_w + 4*mm
c.setFillColor(CREAM)
c.drawString(md_x, brand_y, "Marketing Digital")

# Tagline (muted, below brand)
c.setFillColor(MUTED)
c.setFont('Inter', 5.5)
c.drawString(text_x, brand_y - 4*mm, "Agencia técnica  ·  Ingeniería Web  ·  SEO + GEO  ·  Paid Media")

# Hairline divider
div_y = CARD_H - 22*mm
c.setStrokeColor(HexColor('#3C3A2F'))
c.setLineWidth(0.4)
c.line(5*mm, div_y, CARD_W - 5*mm, div_y)

# Contact details (left side)
c.setFillColor(CREAM)
c.setFont('Inter', 8)
y = div_y - 5.5*mm
line_h = 4.2*mm
c.drawString(5*mm, y, "admin@vantia.digital")
c.drawString(5*mm, y - line_h, "+34 645 720 420")
c.drawString(5*mm, y - 2*line_h, "vantia.digital")

c.setFillColor(MUTED)
c.setFont('Inter', 6.5)
c.drawString(5*mm, y - 3*line_h - 0.5*mm, "Barcelona, España")

# QR codes (right side, bottom-right area)
QR_SIZE = 14*mm
QR_Y = 5*mm
QR_X_WA = CARD_W - 5*mm - QR_SIZE
QR_X_WEB = QR_X_WA - QR_SIZE - 2*mm

# QR Web
c.drawImage(make_qr("https://vantia.digital"), QR_X_WEB, QR_Y,
            width=QR_SIZE, height=QR_SIZE, mask='auto')
c.setFillColor(MUTED)
c.setFont('Inter', 5)
c.drawCentredString(QR_X_WEB + QR_SIZE/2, QR_Y - 2*mm, "WEB")

# QR WhatsApp
wa_url = "https://wa.me/34645720420?text=Hola%20Vantia%20Digital%2C%20me%20gustar%C3%ADa%20agendar%20una%20sesi%C3%B3n%20gratuita."
c.drawImage(make_qr(wa_url), QR_X_WA, QR_Y,
            width=QR_SIZE, height=QR_SIZE, mask='auto')
c.drawCentredString(QR_X_WA + QR_SIZE/2, QR_Y - 2*mm, "WHATSAPP")

c.showPage()
c.save()
print(f"OK: {OUT}")
print(f"Size: {os.path.getsize(OUT)} bytes")
