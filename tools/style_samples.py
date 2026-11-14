import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import mapstyle as M
from engine import Pen, FB, FX, FS
import v_titanic as VT

W, H, SS = 1080, 1920, 2
F = "/usr/share/fonts/opentype/inter/"
OUT = "/home/claude/shorts/"

def brand(d, dark=True, acc=(255, 196, 70)):
    d.rounded_rectangle([40, 70, 270, 130], radius=30, fill=(25, 25, 30) if dark else (245, 240, 225))
    d.text((60, 100), "DAILY", font=FX[36], fill=(255, 255, 255) if dark else (25, 25, 30), anchor="lm")
    d.text((60 + d.textlength("DAILY ", font=FX[36]), 100), "WHY", font=FX[36], fill=acc, anchor="lm")

def caption(d, words, hi, y=1150, col=(255, 255, 255), acc=(255, 196, 70), stroke=(25, 25, 30)):
    f = ImageFont.truetype(F + "Inter-Black.otf", 74); lw = d.textlength(" ".join(words), font=f); x = W / 2 - lw / 2
    for i, w in enumerate(words):
        d.text((x, y), w, font=f, fill=acc if i == hi else col, anchor="lm", stroke_width=8, stroke_fill=stroke); x += d.textlength(w + " ", font=f)

# ---------- 1. BLUEPRINT ----------
def blueprint():
    BG, GRID, LINE = (22, 64, 120), (40, 90, 150), (225, 238, 255)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for x in range(0, W, 30): d.line([(x, 0), (x, H)], fill=GRID if x % 150 else (60, 112, 172), width=1 if x % 150 else 2)
    for y in range(0, H, 30): d.line([(0, y), (W, y)], fill=GRID if y % 150 else (60, 112, 172), width=1 if y % 150 else 2)
    arr = np.asarray(im).astype(np.float32) + M.paper_noise(W, H, 11, 8)[..., None]; im = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA")
    L = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d2 = ImageDraw.Draw(L); P = Pen(d2, L)
    # ship side elevation in line art
    x0, x1, top, bot = 90, 990, 520, 700
    P.poly([(x0 + 10, top), (x1, top), (x1 + 40, top - 40), (x1 - 10, bot), (x0 + 40, bot), (x0 - 20, top + 30)], outline=LINE, width=5)
    for i in range(1, 16):
        bx = x0 + i * (x1 - x0) / 16; P.line([(bx, top + 50), (bx, bot)], LINE + (200,), 3)
    for i in range(4):
        fx = 330 + i * 120; P.poly([(fx - 22, top), (fx + 22, top), (fx + 30, top - 140), (fx - 12, top - 140)], outline=LINE, width=4)
    P.line([(200, top - 40), (850, top - 40)], LINE, 4); P.line([(200, top - 40), (200, top)], LINE, 4); P.line([(850, top - 40), (850, top)], LINE, 4)
    # flooded compartments hatched
    for c in range(5):
        bx0 = x1 - (c + 1) * (x1 - x0) / 16
        for k in range(0, 60, 12): P.line([(bx0 + k, bot - 4), (bx0 + k + 50, top + 54)], (255, 120, 100), 3)
    # dimension line
    P.line([(x0, 780), (x1, 780)], LINE, 3); P.line([(x0, 765), (x0, 795)], LINE, 3); P.line([(x1, 765), (x1, 795)], LINE, 3)
    P.text(540, 820, "882 FT 9 IN  ·  16 COMPARTMENTS", FX[36], LINE)
    P.rrect(560, 300, 990, 380, 10, outline=(255, 120, 100), width=4); P.text(775, 340, "5 FLOODED > 4 MAX", FX[36], (255, 140, 120))
    # title block
    P.rect(620, 1500, 1040, 1680, outline=LINE, width=4); P.line([(620, 1560), (1040, 1560)], LINE, 3)
    P.text(830, 1530, "DAILY WHY · DWG 07", FS[34], LINE); P.text(830, 1620, "TITANIC, 1912", FX[44], LINE)
    im.alpha_composite(L.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA"))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(F + "Inter-Black.otf", 80); d.text((W / 2, 220), "THE FATAL FLAW", font=f, fill=(255, 255, 255), anchor="mm")
    caption(d, ["it", "could", "survive"], 2, y=1150, acc=(255, 200, 90), stroke=(10, 30, 70)); brand(d)
    return im.convert("RGB")

# ---------- 2. OLD NEWSPAPER ----------
def newspaper():
    PAPER, INK = (236, 226, 200), (40, 34, 28)
    im = Image.new("RGB", (W, H), (60, 52, 44)); d = ImageDraw.Draw(im)
    # page with slight rotation
    page = Image.new("RGB", (900, 1350), PAPER); pd = ImageDraw.Draw(page)
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    try: fs = ImageFont.truetype(serif, 52)
    except Exception: fs = FB[60]
    pd.text((450, 80), "THE EVENING CHRONICLE", font=fs, fill=INK, anchor="mm")
    pd.line([(40, 130), (860, 130)], fill=INK, width=4); pd.text((450, 155), "APRIL 15, 1912  ·  ONE CENT", font=FS[34], fill=INK, anchor="mm"); pd.line([(40, 180), (860, 180)], fill=INK, width=2)
    fh = ImageFont.truetype(F + "Inter-Black.otf", 120)
    pd.text((450, 290), "TITANIC", font=fh, fill=INK, anchor="mm"); pd.text((450, 420), "SINKS", font=fh, fill=INK, anchor="mm")
    pd.text((450, 520), "1,500 FEARED LOST AT SEA", font=FX[44], fill=INK, anchor="mm")
    # engraving-style ship
    L = Image.new("RGBA", (900 * SS, 1350 * SS), (0, 0, 0, 0)); P = Pen(ImageDraw.Draw(L), L)
    VT.ship(P, 450, 760, 1.1, tilt=8)
    for y in range(820, 900, 8): P.line([(80, y), (820, y)], INK + (120,), 2)
    page = page.convert("RGBA"); g = L.convert("RGBa").resize((900, 1350), Image.LANCZOS).convert("RGBA")
    gray = Image.merge("RGBA", (*[g.convert("L")] * 3, g.getchannel("A"))); page.alpha_composite(gray)
    pd = ImageDraw.Draw(page)
    for col in range(3):
        for r in range(12): pd.rectangle([60 + col * 270, 960 + r * 28, 60 + col * 270 + 230 - (r % 4) * 20, 970 + r * 28], fill=(150, 140, 120))
    arr = np.asarray(page.convert("RGB")).astype(np.float32) + M.paper_noise(900, 1350, 13, 14)[..., None]
    page = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA").rotate(-3, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", page.size, (0, 0, 0, 0)); sh.putalpha(page.getchannel("A").point(lambda v: int(v * 0.5))); sh = sh.filter(ImageFilter.GaussianBlur(20))
    im = im.convert("RGBA"); im.alpha_composite(sh, (W // 2 - page.width // 2 + 20, 250)); im.alpha_composite(page, (W // 2 - page.width // 2, 230))
    d = ImageDraw.Draw(im)
    st = Image.new("RGBA", (420, 140), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([5, 5, 415, 135], radius=16, outline=(190, 40, 40), width=10); sd.text((210, 70), "2 HRS 40 MIN", font=FB[60], fill=(190, 40, 40), anchor="mm")
    st = st.rotate(12, expand=True); im.alpha_composite(st, (560, 1150))
    caption(d, ["in", "just", "two", "hours"], 3, y=1500); brand(d)
    return im.convert("RGB")

# ---------- 3. MAP + CHARACTERS (existing) ----------
def mapframe():
    import json
    s = VT.SENT; sd = s[2]["start"] - s[1]["start"]
    L = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); P = Pen(ImageDraw.Draw(L), L)
    z = VT.s_ice(P, L, sd * 0.68, sd)
    im = VT.cam(VT.BG_ICE, z).convert("RGBA"); im.alpha_composite(L.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA"))
    d = ImageDraw.Draw(im); caption(d, ["it", "hit", "an", "iceberg"], 3); brand(d)
    return im.convert("RGB")

if __name__ == "__main__":
    ims = [mapframe(), blueprint(), newspaper()]
    for im, n in zip(ims, ["A_map", "B_blueprint", "C_newspaper"]): im.save(OUT + f"style_{n}.jpg", quality=90)
    sheet = Image.new("RGB", (540 * 3 + 40, 960), (255, 255, 255))
    for i, im in enumerate(ims): sheet.paste(im.resize((540, 960)), (i * 560, 0))
    d = ImageDraw.Draw(sheet)
    for i, lab in enumerate(["A  Map + characters", "B  Blueprint", "C  Old newspaper"]):
        d.rounded_rectangle([i * 560 + 150, 880, i * 560 + 390, 930], radius=20, fill=(25, 25, 30)); d.text((i * 560 + 270, 905), lab, font=FX[36].font_variant(size=24), fill=(255, 255, 255), anchor="mm")
    sheet.save(OUT + "style_comparison.jpg", quality=90)
