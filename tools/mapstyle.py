"""Daily Why 'map + chibi characters' style (inspired look, original drawings)."""
import math, random, warnings
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
warnings.filterwarnings("ignore")
import geopandas as gpd

W, H = 1080, 1920
SEA, SEA2, LAND, LAND2, INK = (96, 150, 160), (80, 132, 142), (214, 196, 150), (190, 170, 124), (60, 45, 35)
HILITE = (52, 82, 180)
F = "/usr/share/fonts/opentype/inter/"
_world = None
def world():
    global _world
    if _world is None: _world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    return _world

def paper_noise(w, h, seed=1, strength=12):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (h // 4, w // 4)).astype(np.float32)
    img = Image.fromarray(((n * 0.5 + 0.5).clip(0, 1) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    fine = rng.normal(0, 1, (h, w)).astype(np.float32)
    a = (np.asarray(img).astype(np.float32) - 128) / 128 * strength + fine * strength * 0.35
    return a

def vintage_map(center_lon, center_lat, km_per_px, highlight=(), seed=1, w=W, h=H):
    """Equirectangular-ish view. km_per_px controls zoom."""
    deg_per_px_lat = km_per_px / 111.0; deg_per_px_lon = deg_per_px_lat / math.cos(math.radians(center_lat))
    def proj(lon, lat): return ((lon - center_lon) / deg_per_px_lon + w / 2, (center_lat - lat) / deg_per_px_lat + h / 2)
    im = Image.new("RGB", (w, h), SEA); d = ImageDraw.Draw(im)
    for y in range(h):  # soft vignette in the sea
        t = abs(y - h / 2) / (h / 2); d.line([(0, y), (w, y)], fill=tuple(int(SEA[i] + (SEA2[i] - SEA[i]) * t) for i in range(3)))
    for _, row in world().iterrows():
        geoms = row.geometry.geoms if row.geometry.geom_type == "MultiPolygon" else [row.geometry]
        col = HILITE if row["name"] in highlight else LAND
        for g in geoms:
            pts = [proj(x, y) for x, y in g.exterior.coords]
            if max(p[0] for p in pts) < -50 or min(p[0] for p in pts) > w + 50 or max(p[1] for p in pts) < -50 or min(p[1] for p in pts) > h + 50: continue
            d.polygon(pts, fill=col)
            d.line(pts + [pts[0]], fill=(30, 40, 90) if col == HILITE else LAND2, width=4 if col == HILITE else 3)
    # coastal halo in the sea + soft inner shading on land
    land = Image.new("L", (w, h), 0); ld = ImageDraw.Draw(land)
    for _, row in world().iterrows():
        geoms = row.geometry.geoms if row.geometry.geom_type == "MultiPolygon" else [row.geometry]
        for g in geoms: ld.polygon([proj(x, y) for x, y in g.exterior.coords], fill=255)
    halo = land.filter(ImageFilter.GaussianBlur(12))
    lightsea = Image.new("RGB", (w, h), (150, 190, 192))
    im = Image.composite(lightsea, im, Image.eval(halo, lambda v: int(v * 0.4) if v < 250 else 0).point(lambda v: v)) if True else im
    im.paste(im, (0, 0))
    inner = Image.eval(land.filter(ImageFilter.GaussianBlur(14)), lambda v: 255 - v)
    shade = Image.new("RGB", (w, h), (165, 140, 95))
    landmask = Image.eval(land, lambda v: v)
    tmp = Image.composite(shade, im, Image.eval(inner, lambda v: int(v * 0.5)))
    im = Image.composite(tmp, im, landmask)
    # paper texture
    arr = np.asarray(im).astype(np.float32) + paper_noise(w, h, seed)[..., None]
    im = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    return im, proj

def shadow(d, x, y, w):
    d.ellipse([x - w, y - w * 0.18, x + w, y + w * 0.18], fill=(0, 0, 0, 70))

def chibi(img, x, y, s=1.0, coat=(40, 40, 50), hat=None, hair=(80, 55, 40), mood="neutral", extra=None, look=0):
    """Draw a bobble-head character with feet at (x, y)."""
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ol = (45, 32, 28); skin = (250, 232, 214)
    shadow(d, x, y + 4 * s, 120 * s)
    # body / coat
    bw, bh = 95 * s, 190 * s
    dark = tuple(max(0, c - 30) for c in coat)
    d.rounded_rectangle([x - bw, y - bh, x + bw, y], radius=60 * s, fill=coat, outline=ol, width=int(5 * s))
    d.rounded_rectangle([x + bw * 0.25, y - bh + 10 * s, x + bw - 6 * s, y - 6 * s], radius=50 * s, fill=dark)
    for sx in (-1, 1):
        d.rounded_rectangle([x + sx * bw - 22 * s, y - bh + 40 * s, x + sx * bw + 22 * s, y - 50 * s], radius=22 * s, fill=coat, outline=ol, width=int(4 * s))
        d.ellipse([x + sx * bw - 18 * s, y - 70 * s, x + sx * bw + 18 * s, y - 34 * s], fill=(250, 232, 214), outline=ol, width=int(3 * s))
    d.rectangle([x - 8 * s, y - bh + 30 * s, x + 8 * s, y - 10 * s], fill=tuple(min(255, c + 25) for c in coat))
    for i in range(3): d.ellipse([x + 16 * s, y - bh + 50 * s + i * 40 * s, x + 30 * s, y - bh + 64 * s + i * 40 * s], fill=(200, 170, 90))
    d.polygon([(x - 40 * s, y - bh + 4 * s), (x, y - bh + 60 * s), (x + 40 * s, y - bh + 4 * s)], fill=(245, 242, 235), outline=ol)
    # head
    hr = 115 * s; hy = y - bh - hr + 30 * s
    d.ellipse([x - hr, hy - hr * 0.92, x + hr, hy + hr * 0.92], fill=skin, outline=ol, width=int(5 * s))
    d.ellipse([x + hr * 0.35, hy - hr * 0.5, x + hr * 0.95, hy + hr * 0.8], fill=(238, 214, 192)) if False else None
    if hair: d.chord([x - hr, hy - hr * 0.92, x + hr, hy + hr * 0.6], 180, 360, fill=hair, outline=ol, width=int(5 * s))
    ex = 38 * s; ey = hy + 18 * s
    for sx in (-1, 1):
        d.ellipse([x + sx * ex - 9 * s + look * 6 * s, ey - 11 * s, x + sx * ex + 9 * s + look * 6 * s, ey + 11 * s], fill=(25, 20, 20))
    if mood == "worried":
        d.line([(x - ex - 18 * s, ey - 30 * s), (x - ex + 14 * s, ey - 40 * s)], fill=ol, width=int(6 * s)); d.line([(x + ex + 18 * s, ey - 30 * s), (x + ex - 14 * s, ey - 40 * s)], fill=ol, width=int(6 * s))
        d.arc([x - 22 * s, ey + 28 * s, x + 22 * s, ey + 58 * s], 200, 340, fill=ol, width=int(5 * s))
    elif mood == "stern":
        d.line([(x - ex - 18 * s, ey - 38 * s), (x - ex + 14 * s, ey - 26 * s)], fill=ol, width=int(7 * s)); d.line([(x + ex + 18 * s, ey - 38 * s), (x + ex - 14 * s, ey - 26 * s)], fill=ol, width=int(7 * s))
        d.line([(x - 18 * s, ey + 42 * s), (x + 18 * s, ey + 42 * s)], fill=ol, width=int(5 * s))
    else:
        d.line([(x - 16 * s, ey + 42 * s), (x + 16 * s, ey + 42 * s)], fill=ol, width=int(5 * s))
    if hat == "top":
        d.rectangle([x - 70 * s, hy - hr * 0.92 - 110 * s, x + 70 * s, hy - hr * 0.7], fill=(30, 28, 32), outline=ol, width=int(4 * s))
        d.rounded_rectangle([x - 110 * s, hy - hr * 0.78, x + 110 * s, hy - hr * 0.62], radius=10 * s, fill=(30, 28, 32), outline=ol)
    elif hat == "hard":
        d.chord([x - hr * 0.95, hy - hr * 1.15, x + hr * 0.95, hy - hr * 0.1], 180, 360, fill=(235, 190, 60), outline=ol, width=int(5 * s))
        d.rounded_rectangle([x - hr * 1.05, hy - hr * 0.68, x + hr * 1.05, hy - hr * 0.56], radius=8 * s, fill=(225, 175, 50), outline=ol)
    elif hat == "cap":
        d.chord([x - hr * 0.95, hy - hr * 1.12, x + hr * 0.95, hy - hr * 0.2], 180, 360, fill=(40, 50, 80), outline=ol, width=int(5 * s))
        d.rectangle([x - hr * 0.95, hy - hr * 0.72, x + hr * 0.95, hy - hr * 0.6], fill=(200, 170, 90))
    if extra == "blueprint":
        d.rectangle([x + bw - 30 * s, y - bh + 80 * s, x + bw + 110 * s, y - bh + 180 * s], fill=(60, 100, 170), outline=ol, width=int(4 * s))
        for i in range(3): d.line([(x + bw - 15 * s, y - bh + 105 * s + i * 25 * s), (x + bw + 95 * s, y - bh + 105 * s + i * 25 * s)], fill=(200, 220, 250), width=int(3 * s))
    img.alpha_composite(L)

def word_caption(img, word, y=1150):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(F + "Inter-ExtraBold.otf", 64)
    d.text((W / 2, y), word, font=f, fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(30, 30, 40))

if __name__ == "__main__":
    base, proj = vintage_map(-70, 46.0, 1.6, highlight={"Canada"} and set(), seed=3)
    im = base.convert("RGBA"); d = ImageDraw.Draw(im)
    qx, qy = proj(-71.29, 46.75)  # Quebec City
    d.ellipse([qx - 16, qy - 16, qx + 16, qy + 16], fill=(200, 50, 50), outline=(255, 255, 255), width=5)
    d.text((qx + 30, qy), "Québec", font=ImageFont.truetype(F + "Inter-Bold.otf", 48), fill=(60, 45, 35), anchor="lm")
    chibi(im, 330, 1480, 1.0, coat=(35, 35, 45), hat="top", hair=(200, 200, 205), mood="stern", extra="blueprint")
    chibi(im, 760, 1500, 0.95, coat=(120, 80, 50), hat="hard", hair=None, mood="worried", look=-1)
    word_caption(im, "bending", 1700)
    im.convert("RGB").save("/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/mapstyle_test.jpg", quality=90)
