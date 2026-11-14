"""Blueprint style: grid background + draw-on line helpers (draw in the 1080x940 scene space)."""
import math
import numpy as np
from PIL import Image, ImageDraw
import mapstyle as M
from engine import FX, FS, FB, clamp, ease

THEME = dict(bg1=(22, 64, 120), bg2=(14, 44, 88), accent=(255, 196, 70), accent2=(150, 205, 255), text=(240, 246, 255))
LINE, RED, DIM = (228, 240, 255), (255, 120, 100), (150, 190, 235)

def background(seed=11, W=1080, H=1920):
    BG, GRID, MAJOR = (22, 64, 120), (36, 84, 144), (58, 108, 170)
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(H):  # gentle vignette
        k = abs(y - H / 2) / (H / 2); d.line([(0, y), (W, y)], fill=tuple(int(BG[i] * (1 - 0.25 * k)) for i in range(3)))
    for x in range(0, W, 30): d.line([(x, 0), (x, H)], fill=MAJOR if x % 150 == 0 else GRID, width=2 if x % 150 == 0 else 1)
    for y in range(0, H, 30): d.line([(0, y), (W, y)], fill=MAJOR if y % 150 == 0 else GRID, width=2 if y % 150 == 0 else 1)
    arr = np.asarray(im).astype(np.float32) + M.paper_noise(W, H, seed, 7)[..., None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

def title_block(label):
    def fn(d, th):
        x0, y0 = 750, 70
        d.rectangle([x0, y0, 1040, y0 + 60], outline=LINE, width=3)
        d.text((x0 + 145, y0 + 30), label, font=FS[34].font_variant(size=26), fill=LINE, anchor="mm")
    return fn

def path(P, pts, prog, col=LINE, w=6):
    """Draw a polyline up to fraction prog of its length (draw-on animation)."""
    if prog <= 0 or len(pts) < 2: return
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; L = sum(segs) * clamp(prog)
    out = [pts[0]]
    for i, s in enumerate(segs):
        if L >= s: out.append(pts[i + 1]); L -= s
        else:
            f = L / s if s else 0; out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
    P.line(out, col, w)

def circle(P, cx, cy, r, prog, col=LINE, w=6, start=-90):
    n = 72; pts = [(cx + r * math.cos(math.radians(start + 360 * i / n)), cy + r * math.sin(math.radians(start + 360 * i / n))) for i in range(n + 1)]
    path(P, pts, prog, col, w)

def rect(P, x0, y0, x1, y1, prog, col=LINE, w=6, ang=0, c=None):
    cx, cy = c if c else ((x0 + x1) / 2, (y0 + y1) / 2); a = math.radians(ang)
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    pts = [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]
    path(P, pts, prog, col, w)

def dim(P, x0, y0, x1, y1, label, prog=1.0, col=DIM, off=0):
    """Dimension line with end ticks and a label."""
    path(P, [(x0, y0), (x1, y1)], prog, col, 4)
    if prog >= 1:
        ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2; dx, dy = 16 * math.cos(ang), 16 * math.sin(ang)
        for x, y in ((x0, y0), (x1, y1)): P.line([(x - dx, y - dy), (x + dx, y + dy)], col, 4)
        P.text((x0 + x1) / 2 + off * math.cos(ang), (y0 + y1) / 2 + off * math.sin(ang), label, FX[44], col)

def hatch(P, x0, y0, x1, y1, prog=1.0, col=RED, step=22):
    n = int(((x1 - x0) + (y1 - y0)) / step * clamp(prog))
    for i in range(n):
        k = i * step
        a = (x0 + k, y0) if k <= x1 - x0 else (x1, y0 + k - (x1 - x0))
        b = (x0, y0 + k) if k <= y1 - y0 else (x0 + k - (y1 - y0), y1)
        P.line([a, b], col + (170,), 3)

def label(P, x, y, s, col=LINE, f=None):
    P.text(x, y, s, f or FX[44], col)
