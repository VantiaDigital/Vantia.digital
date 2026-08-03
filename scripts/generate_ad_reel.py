"""
Genera el Reel/anuncio de Vantia (9:16) a partir del video cuadrado de fondo.

Version 3: TEXTO ARRIBA (zona segura), vídeo abajo. Evita que el texto choque
con el pie/botones de TikTok, Reels y Shorts (que viven en el tercio inferior).
Ángulo "te vendieron diseño pero no vende", solo texto, sin botón falso.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
SRC  = "C:/Users/facun/Documentos/Vantia Digital/Fotos y videos/IMG_E0674.MOV"
OUT_DIR = os.path.join(ROOT, "_ad")
OUT_FILE = os.path.join(OUT_DIR, "vantia-reel.mp4")
FONT_BODY = os.path.join(ROOT, "assets/fonts/Inter-Variable.ttf")
FONT_DISP = os.path.join(ROOT, "assets/fonts/Fraunces-Regular.ttf")

W, H = 1080, 1920
VID = 1080
VID_Y = 790                 # video en la mitad inferior (deja el texto arriba)
TEXT_CENTER = 500           # centro de la zona de texto (zona segura, fuera de UI)
BRAND_TITLE_Y = 168
BRAND_HANDLE_Y = 230

DEEP   = (26, 24, 19, 255)
CREAM  = (236, 232, 216, 255)
COPPER = (193, 131, 75, 255)
DUR = 14.0

CARDS = [
    (0.3,  2.8,  [("Te vendieron", CREAM, 72), ("una web bonita.", CREAM, 72)]),
    (2.8,  4.9,  [("Pero no vende.", COPPER, 104)]),
    (4.9,  8.9,  [("Nosotros las hacemos", CREAM, 62), ("para vender.", CREAM, 62), ("Y lo medimos.", CREAM, 62)]),
    (8.9,  10.9, [("Ingeniería, no humo.", CREAM, 64)]),
]
CTA_START, CTA_END = 10.9, 14.0


def font(path, size, bold=False):
    f = ImageFont.truetype(path, size)
    if bold:
        try:
            f.set_variation_by_axes([700])
        except Exception:
            pass
    return f


def make_card(idx, lines):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    heights = [int(s * 1.25) for (_t, _c, s) in lines]
    y = TEXT_CENTER - sum(heights) // 2
    for (text, color, size), lh in zip(lines, heights):
        f = font(FONT_BODY, size, bold=True)
        w = d.textlength(text, font=f)
        d.text(((W - w) // 2, y), text, font=f, fill=color)
        y += lh
    p = os.path.join(OUT_DIR, f"card_{idx}.png")
    img.save(p)
    return p


def make_brand():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fb = font(FONT_DISP, 44)
    t1 = "Vantia Digital"
    w1 = d.textlength(t1, font=fb)
    d.text(((W - w1) // 2, BRAND_TITLE_Y), t1, font=fb, fill=CREAM)
    fh = font(FONT_BODY, 28, bold=True)
    t2 = "@vantiadigital"
    w2 = d.textlength(t2, font=fh)
    d.text(((W - w2) // 2, BRAND_HANDLE_Y), t2, font=fh, fill=COPPER)
    p = os.path.join(OUT_DIR, "brand_top.png")
    img.save(p)
    return p


def make_cta():
    # Cierre como TEXTO en la zona segura (sin flecha al fondo: ahi va la UI de la red).
    # En el anuncio de IG, el boton clicable "Mas informacion" lo pone Meta automaticamente.
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f1 = font(FONT_BODY, 60, bold=True)
    t1 = "Más información"
    w1 = d.textlength(t1, font=f1)
    d.text(((W - w1) // 2, TEXT_CENTER - 70), t1, font=f1, fill=CREAM)
    f2 = font(FONT_BODY, 64, bold=True)
    t2 = "vantia.digital"
    w2 = d.textlength(t2, font=f2)
    d.text(((W - w2) // 2, TEXT_CENTER + 10), t2, font=f2, fill=COPPER)
    p = os.path.join(OUT_DIR, "cta.png")
    img.save(p)
    return p


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    brand = make_brand()
    cards = [make_card(i, lines) for i, (_s, _e, lines) in enumerate(CARDS)]
    cta = make_cta()
    print("PNGs generados:", len(cards) + 2)

    inp = ["-i", SRC, "-loop", "1", "-t", "14", "-i", brand]
    for c in cards:
        inp += ["-loop", "1", "-t", "14", "-i", c]
    inp += ["-loop", "1", "-t", "14", "-i", cta]

    fc = "color=c=0x1A1813:s=1080x1920:r=30:d=14[bg];"
    fc += "[0:v]trim=0:14,setpts=PTS-STARTPTS,scale=1080:1080:flags=bicubic,setsar=1[vid];"
    fc += f"[bg][vid]overlay=0:{VID_Y}:shortest=1[base];"
    fc += "[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[brand];"
    fc += "[base][brand]overlay=0:0[s1];"
    prev = "s1"
    for i, (s, e, _lines) in enumerate(CARDS):
        idx = i + 2
        fo = max(s + 0.3, e - 0.35)
        fc += (f"[{idx}:v]format=rgba,fade=in:st={s:.2f}:d=0.28:alpha=1,"
               f"fade=out:st={fo:.2f}:d=0.28:alpha=1[c{i}];")
        fc += f"[{prev}][c{i}]overlay=0:0[o{i}];"
        prev = f"o{i}"
    cta_idx = len(CARDS) + 2
    fc += f"[{cta_idx}:v]format=rgba,fade=in:st={CTA_START:.2f}:d=0.30:alpha=1[cta];"
    fc += f"[{prev}][cta]overlay=0:0[vout];"
    fc += "[0:a]atrim=0:14,asetpts=PTS-STARTPTS[aout]"

    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inp,
           "-filter_complex", fc,
           "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", "-r", "30", "-t", "14",
           "-movflags", "+faststart", OUT_FILE]
    print("Render FFmpeg...")
    subprocess.run(cmd, check=True)
    print("OK ->", OUT_FILE)


if __name__ == "__main__":
    main()
