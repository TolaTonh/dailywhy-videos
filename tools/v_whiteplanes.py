"""Why are most planes painted white? — engine v2, blueprint style, real photos."""
import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import FX, FS, FB, clamp, ease, back, lerp, mix
import blueprint as B
import engine2

KEY = "whiteplanes"
T = dict(B.THEME); LINE, RED, DIM, ACC, GREEN = B.LINE, B.RED, B.DIM, T["accent"], (110, 230, 150)
PH = "/home/claude/shorts/photos/"

def jet(P, x, y, s, col=LINE, fill=None):
    """Side view, nose left."""
    P.rrect(x - 260 * s, y - 36 * s, x + 240 * s, y + 36 * s, 36 * s, fill=fill, outline=col, width=6)
    P.line([(x + 170 * s, y - 36 * s), (x + 250 * s, y - 150 * s), (x + 290 * s, y - 150 * s), (x + 240 * s, y - 30 * s)], col, 6)
    P.line([(x - 40 * s, y + 30 * s), (x + 70 * s, y + 70 * s)], col, 5)
    P.rrect(x - 30 * s, y + 60 * s, x + 95 * s, y + 110 * s, 22 * s, outline=col, width=5)
    for i in range(7): P.circle(x - 190 * s + i * 45 * s, y - 8 * s, 6 * s, fill=col)

def banner(P, y, s, col, w=None):
    f = FX[44]; w = w or (len(s) * 27 + 80)
    P.rrect(540 - w / 2, y - 48, 540 + w / 2, y + 48, 40, fill=(0, 0, 0, 200)); B.label(P, 540, y, s, col, f)

def p_none(P, t, sd, th): pass

def s_heat(P, t, sd, th):
    # sun top-left, rays hit the fuselage and bounce away
    P.circle(170, 230, 70, fill=ACC)
    for i in range(10):
        a = math.radians(i * 36 + t * 30); P.line([(170 + 90 * math.cos(a), 230 + 90 * math.sin(a)), (170 + 125 * math.cos(a), 230 + 125 * math.sin(a))], ACC, 8)
    jet(P, 560, 620, 1.25)
    k = clamp((t - 0.8) / 0.9)
    for i, hx in enumerate((380, 540, 700)):
        kk = clamp(k * 1.4 - i * 0.15)
        if kk > 0:
            sx, sy = 230 + i * 20, 290
            hy = 575
            P.line([(sx, sy), (lerp(sx, hx, kk), lerp(sy, hy, kk))], ACC, 7)
        k2 = clamp((t - 1.9 - i * 0.12) / 0.6)
        if k2 > 0:
            P.arrow(hx, 575, hx + 150 * k2, 575 - 210 * k2, ACC, 8, 26)
    if t > 2.6: banner(P, 850, "REFLECTS THE SUN", ACC)

def p_safety(P, t, sd, th):
    # magnifier ring sweeping across the photo, then a red crack mark
    k = ease((t - 0.4) / 1.6); cx = lerp(250, 560, k); cy = lerp(520, 420, k)
    P.circle(cx, cy, 120, outline=LINE, width=10)
    P.line([(cx + 85, cy + 85), (cx + 170, cy + 170)], LINE, 16)
    if t > 1.9:
        kk = clamp((t - 1.9) / 0.4)
        pts = [(cx - 60, cy - 30), (cx - 25, cy - 5), (cx - 5, cy - 28), (cx + 30, cy + 8), (cx + 62, cy - 6)]
        B.path(P, pts, kk, RED, 9)
    if t > 2.4: banner(P, 800, "DAMAGE SHOWS UP", RED)

def s_weight(P, t, sd, th):
    jet(P, 540, 330, 0.95)
    # scale platform
    P.line([(240, 420), (840, 420)], LINE, 8)
    P.poly([(440, 420), (640, 420), (700, 520), (380, 520)], outline=LINE, width=6)
    k = ease((t - 1.6) / 1.4)
    if t > 1.6:
        v = int(round(1200 * k / 10) * 10)
        B.label(P, 540, 635, f"{v:,}", ACC, FB[150].font_variant(size=210))
        B.label(P, 540, 822, "LB OF PAINT", ACC, FB[72])
        B.label(P, 540, 900, "full livery, large airliner (up to)", DIM, FS[34])

def person(P, x, y, s, col):
    P.circle(x, y - 62 * s, 26 * s, fill=col)
    P.rrect(x - 34 * s, y - 30 * s, x + 34 * s, y + 70 * s, 24 * s, fill=col)

def s_eight(P, t, sd, th):
    for i in range(8):
        k = back((t - 0.25 - i * 0.16) / 0.3)
        if k > 0.02:
            x = 150 + (i % 4) * 260; y = 330 + (i // 4) * 250
            person(P, x, y, 1.15 * clamp(k, 0, 1.12), ACC)
    if t > 1.7:
        B.label(P, 540, 830, "8 EXTRA PASSENGERS", RED, FB[72])
        B.label(P, 540, 900, "on every flight", LINE, FS[34].font_variant(size=40))

def p_simple(P, t, sd, th):
    k = clamp((t - 0.7) / 0.4)
    if k > 0: banner(P, 800, "LESS PAINT = LESS FUEL", GREEN, 780)

def s_fade(P, t, sd, th):
    k = ease((t - 0.6) / 2.4)
    dark0, dark1 = (40, 70, 190), (120, 135, 170)
    jet(P, 540, 300, 0.85, col=LINE, fill=mix(dark0, dark1, k))
    B.label(P, 540, 440, "DARK: FADES FAST", RED if k > 0.5 else LINE)
    jet(P, 540, 640, 0.85, col=LINE, fill=(245, 248, 255))
    B.label(P, 540, 780, "WHITE: STILL WHITE", GREEN)
    P.circle(940, 150, 46, fill=ACC)
    for i in range(8):
        a = math.radians(i * 45 + t * 40); P.line([(940 + 60 * math.cos(a), 150 + 60 * math.sin(a)), (940 + 84 * math.cos(a), 150 + 84 * math.sin(a))], ACC, 7)

COVER = dict(path=PH + "px_1098745.jpg", focus=(0.52, 0.5), zoom=(1.0, 1.12))
SCENES = [
    dict(s=0, fn=p_none, photo=COVER),
    dict(s=1, fn=s_heat, title="1. HEAT"),
    dict(s=2, fn=p_safety, title="2. SAFETY", photo=dict(path=PH + "px_4432054.jpg", focus=(0.35, 0.6), zoom=(1.0, 1.12))),
    dict(s=3, fn=s_weight, title="3. WEIGHT"),
    dict(s=4, fn=s_eight, title="THAT'S LIKE...", title_color=RED),
    dict(s=5, fn=p_simple, title="SO KEEP IT SIMPLE", title_color=GREEN, photo=dict(path=PH + "px_5627575.jpg", focus=(0.4, 0.55), zoom=(1.0, 1.12))),
    dict(s=6, fn=s_fade, title="4. FADING"),
    dict(s=7, fn=p_none, title=None, photo=COVER),
]

if __name__ == "__main__":
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=B.background(14), hook_lines=["WHY ARE PLANES", "WHITE?"], mood="curious", title_block=B.title_block("DAILY WHY · DWG 03"))
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        engine2.render(preview=[0.0, 2.0, 5.0, 7.5, 9.5, 12.0, 14.5, 17.0, 20.5, 24.0, 27.5, 30.0, 32.0], **args)
    else:
        engine2.render(**args)
