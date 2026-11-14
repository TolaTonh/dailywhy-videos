"""Why are manhole covers round? — first Short on engine v2, blueprint style."""
import sys, math, json
sys.path.insert(0, "/home/claude/shorts")
from engine import FX, FS, FB, clamp, ease, back, lerp
import blueprint as B
import engine2

KEY = "manhole"
TM = json.load(open(f"/home/claude/shorts/{KEY}_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.1
T = B.THEME; LINE, RED, DIM, ACC = B.LINE, B.RED, B.DIM, T["accent"]

def cover_top(P, cx, cy, r, prog, col=LINE):
    B.circle(P, cx, cy, r, prog, col, 8)
    B.circle(P, cx, cy, r * 0.82, prog * 1.2 - 0.2, col, 4)
    k = clamp(prog * 1.5 - 0.5)
    for i in range(-3, 4):
        x = cx + i * r * 0.22; h = math.sqrt(max(0, (r * 0.8) ** 2 - (x - cx) ** 2))
        B.path(P, [(x, cy - h), (x, cy + h)], k, col, 3)
    if k > 0.6: B.label(P, cx, cy, "CITY WORKS", col, FX[36])

def section(P, t, cover_ang=None, cover_y=None, shape="square", worker=False, prog=1.0):
    """Cross-section of the street: ground, shaft opening with a seat (lip)."""
    gy, hx0, hx1, lip = 300, 400, 680, 26
    B.path(P, [(60, gy), (hx0 - lip, gy)], prog, LINE, 6); B.path(P, [(hx1 + lip, gy), (1020, gy)], prog, LINE, 6)
    B.path(P, [(hx0 - lip, gy), (hx0 - lip, gy + 30), (hx0, gy + 30), (hx0, 900)], prog, LINE, 6)
    B.path(P, [(hx1 + lip, gy), (hx1 + lip, gy + 30), (hx1, gy + 30), (hx1, 900)], prog, LINE, 6)
    B.hatch(P, 60, gy + 10, hx0 - lip - 10, 880, prog, DIM, 34); B.hatch(P, hx1 + lip + 10, gy + 10, 1020, 880, prog, DIM, 34)
    if worker:
        x, y = 540, 820
        B.circle(P, x, y - 30, 34, 1, ACC, 5)
        P.poly([(x - 48 + 96 * i / 20 if False else x + 48 * math.cos(math.pi + math.pi * i / 20), y - 52 + 48 * math.sin(math.pi + math.pi * i / 20) * 0.9) for i in range(21)], fill=ACC)
        P.line([(x - 66, y - 52), (x + 66, y - 52)], ACC, 8)
        B.path(P, [(x - 50, y + 20), (x - 50, y + 80), (x + 50, y + 80), (x + 50, y + 20)], 1, ACC, 5)
    return gy, hx0, hx1, lip

def slab(P, cx, cy, w, ang, col, th=26):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    pts = [(-w / 2, -th / 2), (w / 2, -th / 2), (w / 2, th / 2), (-w / 2, th / 2), (-w / 2, -th / 2)]
    P.line([(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts], col, 6)

# ---------------- scenes ----------------
def s_hook(P, t, sd, th):
    cover_top(P, 540, 560, 270, 1)
    r = 290 + 25 * ((t * 0.8) % 1); P.circle(540, 560, r, outline=ACC + (int(200 * (1 - (t * 0.8) % 1)),), width=6)

def s_weight(P, t, sd, th):
    k = ease(t / 0.8)
    B.path(P, [(240, 520), (840, 520)], k, LINE, 8); B.path(P, [(240, 580), (840, 580)], k, LINE, 8)
    B.path(P, [(240, 520), (240, 580)], k, LINE, 8); B.path(P, [(840, 520), (840, 580)], k, LINE, 8)
    for i in range(3):
        x = 380 + i * 160; P.arrow(x, 330 + 12 * math.sin(t * 6 + i), x, 500, RED, 10, 34)
    k2 = back((t - 0.3) / 0.5)
    if t > 0.3: B.label(P, 540, 700, "200–300 LB", ACC, FB[96].font_variant(size=int(96 * clamp(k2, 0.05, 1.1))))

def s_square(P, t, sd, th):
    B.rect(P, 300, 300, 780, 780, ease(t / 0.9), LINE, 8)
    if t > 0.7: B.dim(P, 300, 830, 780, 830, "SIDE", clamp((t - 0.7) / 0.4), DIM, off=45)

def s_diag(P, t, sd, th):
    split = rel(3, 3) + 2.6
    if t < split:
        B.rect(P, 300, 300, 780, 780, 1, LINE, 8)
        B.dim(P, 300, 830, 780, 830, "SIDE", 1, DIM, off=45)
        k = ease((t - 0.2) / 0.8)
        B.path(P, [(300, 780), (780, 300)], k, RED, 8)
        if k >= 1: B.label(P, 540, 230, "DIAGONAL = 1.41 × SIDE", RED, FX[44])
    else:
        tt = t - split
        gy, hx0, hx1, lip = section(P, t)
        # square lid turned on edge: its diagonal fits through the opening
        f = ease(clamp(tt / 1.8)); ang = lerp(0, 72, ease(clamp(tt / 0.8)))
        cy = lerp(gy + 15, 700, f) if tt > 0.6 else gy + 15
        slab(P, 540, cy, 300, ang, RED)
        B.label(P, 540, 200, "SQUARE LID, TURNED", RED, FX[44])

def s_reveal(P, t, sd, th):
    gy, hx0, hx1, lip = section(P, t, worker=True)
    f = ease(clamp(t / 0.7)); slab(P, 540, lerp(520, 690, f), 300, 72 + 10 * f, RED)
    s = 1 + 0.08 * math.sin(t * 10)
    P.poly([(870, 520 - 70 * s), (870 + 70 * s, 640), (870 - 70 * s, 640)], fill=RED); P.text(870, 600, "!", FB[72], (30, 30, 40))

def s_circle(P, t, sd, th):
    split = 2.6
    if t < split:
        rot = t * 90; r = 230
        B.circle(P, 540, 520, r, 1, LINE, 8)
        for k in range(3):
            a = math.radians(rot + k * 60)
            x0, y0 = 540 + r * math.cos(a), 520 + r * math.sin(a); x1, y1 = 540 - r * math.cos(a), 520 - r * math.sin(a)
            P.line([(x0, y0), (x1, y1)], DIM + (200 if k == 0 else 90,), 5 if k == 0 else 3)
        B.label(P, 540, 820, "SAME WIDTH, EVERY WAY", ACC, FX[58])
    else:
        tt = t - split
        gy, hx0, hx1, lip = section(P, t)
        ang = 45 + 25 * math.sin(tt * 2.5)
        slab(P, 540, gy + 15 + 40 * math.sin(math.radians(ang)) * 0.0, hx1 - hx0 + 2 * lip + 30, 0 if tt > 1.6 else ang * 0.25, (110, 230, 150))
        B.label(P, 540, 200, "WIDER THAN THE HOLE, ALWAYS", (110, 230, 150), FX[44])
        if tt > 1.0: P.circle(880, 500, 60, fill=(80, 200, 130)); P.line([(850, 500), (872, 524), (912, 474)], (255, 255, 255), 12)

def s_roll(P, t, sd, th):
    split = sd * 0.55
    if t < split:
        x = lerp(200, 880, t / split); r = 130; rot = (x - 200) / r
        B.path(P, [(60, 700), (1020, 700)], 1, LINE, 6)
        B.circle(P, x, 700 - r, r, 1, LINE, 8)
        for k in range(4):
            a = rot + k * math.pi / 4; P.line([(x - r * 0.8 * math.cos(a), 700 - r - r * 0.8 * math.sin(a)), (x + r * 0.8 * math.cos(a), 700 - r + r * 0.8 * math.sin(a))], DIM, 3)
        B.label(P, 540, 820, "ROLL IT", ACC, FX[58])
    else:
        tt = t - split; a = tt * 160
        cover_top(P, 540, 500, 230, 1)
        P.arc(540, 500, 280, a % 360, a % 360 + 80, ACC, 10)
        B.label(P, 540, 820, "FITS AT ANY ANGLE", ACC, FX[58])

def s_loop(P, t, sd, th):
    cover_top(P, 540, 560, 270, 1)

def p_none(P, t, sd, th): pass
def p_weight(P, t, sd, th):
    k = back((t - 0.3) / 0.5)
    if t > 0.3:
        P.rrect(250, 730, 830, 860, 40, fill=(0, 0, 0, 190)); B.label(P, 540, 795, "200–300 LB", ACC, FB[96].font_variant(size=int(88 * clamp(k, 0.05, 1.05))))
PHOTO_COVER = dict(path="/home/claude/shorts/photos/px_13961561.jpg", focus=(0.36, 0.42), zoom=(1.25, 1.4))

SCENES = [
    dict(s=0, fn=p_none, photo=PHOTO_COVER),
    dict(s=1, fn=p_weight, title="HEAVY LIDS", photo=dict(path="/home/claude/shorts/photos/px_3977241.jpg", focus=(0.6, 0.6), zoom=(1.0, 1.12))),
    dict(s=2, fn=s_square, title="NOW MAKE IT SQUARE"),
    dict(s=3, fn=s_diag, title="THE DIAGONAL PROBLEM", title_color=RED),
    dict(s=4, fn=s_reveal, title="LOOK OUT BELOW", title_color=RED),
    dict(s=5, fn=s_circle, title="THE CIRCLE FIX", title_color=(110, 230, 150)),
    dict(s=6, fn=s_roll, title="BONUS"),
    dict(s=7, fn=p_none, title=None, photo=PHOTO_COVER),
]

if __name__ == "__main__":
    bg = B.background(11)
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=bg, hook_lines=["WHY IS IT", "ROUND?"], mood="curious", title_block=B.title_block("DAILY WHY · DWG 01"))
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        engine2.render(preview=[0.0, 1.0, 4.5, 7.0, 9.0, 12.0, 14.6, 17.0, 20.0, 22.0, 23.5, 26.2], **args)
    else:
        engine2.render(**args)
