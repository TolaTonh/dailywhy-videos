import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(98, 60, 44), bg2=(28, 16, 14), accent=(255, 212, 120), accent2=(150, 210, 255), text=(255, 250, 244))
TM = json.load(open("/home/claude/shorts/pisa_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.12
MARBLE, MARBLE2, SHADOW, GRASS, CLAY, SAND, WHITE, RED = (245, 240, 228), (215, 205, 190), (180, 170, 155), (110, 160, 90), (150, 105, 75), (215, 185, 120), (255, 255, 255), (220, 70, 70)

def rot(pts, px, py, ang):
    c, s = math.cos(ang), math.sin(ang)
    return [(px + (x - px) * c - (y - py) * s, py + (x - px) * s + (y - py) * c) for x, y in pts]

def tower(P, bx, by, ang_deg, floors=8, scale=1.0, sink=0):
    """Tower with base centre (bx, by); positive angle leans right (south)."""
    a = math.radians(ang_deg); w = 120 * scale; fh = 70 * scale
    by = by + sink
    for f in range(min(floors, 7)):
        y0 = by - f * fh; y1 = y0 - fh
        P.poly(rot([(bx - w, y0), (bx + w, y0), (bx + w, y1), (bx - w, y1)], bx, by, a), fill=MARBLE)
        P.poly(rot([(bx - w - 8 * scale, y1 + 6 * scale), (bx + w + 8 * scale, y1 + 6 * scale), (bx + w + 8 * scale, y1 - 4 * scale), (bx - w - 8 * scale, y1 - 4 * scale)], bx, by, a), fill=MARBLE2)
        for k in range(5):
            ax = bx - w + 26 * scale + k * 47 * scale
            P.poly(rot([(ax, y0 - 12 * scale), (ax + 22 * scale, y0 - 12 * scale), (ax + 22 * scale, y1 + 22 * scale), (ax, y1 + 22 * scale)], bx, by, a), fill=SHADOW)
    if floors >= 8:
        y0 = by - 7 * fh; y1 = y0 - fh * 0.9; ww = w * 0.72
        P.poly(rot([(bx - ww, y0), (bx + ww, y0), (bx + ww, y1), (bx - ww, y1)], bx, by, a), fill=MARBLE)
        for k in range(3):
            ax = bx - ww + 22 * scale + k * 50 * scale
            P.poly(rot([(ax, y0 - 10 * scale), (ax + 22 * scale, y0 - 10 * scale), (ax + 22 * scale, y1 + 18 * scale), (ax, y1 + 18 * scale)], bx, by, a), fill=SHADOW)

def ground(P, y, layers=False):
    if layers:
        P.rect(0, y, 1080, y + 120, fill=SAND); P.rect(0, y + 120, 1080, 940, fill=CLAY)
        P.text(980, y + 60, "SAND", FX[36], (120, 90, 50), anchor="rm"); P.text(980, y + 200, "SOFT CLAY", FX[36], (90, 60, 40), anchor="rm")
    else:
        P.rect(0, y, 1080, 940, fill=GRASS)

def angle_arc(P, bx, by, ang, r, col):
    P.line([(bx, by), (bx, by - r - 40)], (255, 255, 255, 120), 4)
    P.arc(bx, by, r, -90, -90 + ang, col, 8)

def scene_hook(P, t, sd, th):
    ground(P, 820)
    tower(P, 540, 820, 4.0, scale=1.12)
    P.rrect(130, 110, 450, 190, 40, fill=(0, 0, 0, 140)); P.text(290, 150, "since the 1170s", FX[36], th["accent"])

def scene_why(P, t, sd, th):
    ground(P, 820)
    wob = 4 + 3.5 * math.sin(t * 3) * math.exp(-t * 0.6)
    tower(P, 540, 820, wob, scale=1.12)

def scene_build(P, t, sd, th):
    ground(P, 820)
    yr = int(1173 + 5 * clamp((t - rel(3, 2)) / 1.5)) if t > rel(3, 2) else 1173
    floors = 1 + int(2 * clamp(t / 1.6))
    tower(P, 540, 820, 0, floors=floors + (1 if t > 2 else 0), scale=1.12)
    P.text(540, 150, str(yr), FB[120], th["accent"])

def scene_sink(P, t, sd, th):
    ground(P, 700, layers=True)
    k = ease(t / 3.0)
    tower(P, 540, 700, 3.0 * k, floors=3, scale=1.2, sink=10 * k)
    for x in (640, 720):
        oy = (t * 60) % 60
        P.arrow(x, 740 + oy, x, 800 + oy, (255, 255, 255, 200), 10, 28)
    P.text(150, 760, "N", FB[60], th["text"]); P.text(930, 640, "S", FB[60], th["text"])

def scene_pause(P, t, sd, th):
    ground(P, 700, layers=True)
    tower(P, 540, 700, 2.5, floors=3, scale=1.2, sink=10)
    yr = int(1178 + 94 * ease(t / 2.4))
    P.rrect(330, 90, 750, 200, 40, fill=(0, 0, 0, 140)); P.text(540, 145, f"{yr}", FB[72], th["accent"])
    if t > rel(6, 5):
        for i in range(8):
            y = 760 + i * 22; P.line([(60, y), (1020, y)], (110, 75, 55, 160), 4)
        P.rrect(240, 230, 840, 300, 35, fill=(0, 0, 0, 140)); P.text(540, 265, "soil settles & firms up", FX[44], th["text"])

def scene_1990(P, t, sd, th):
    ground(P, 820)
    a = 5.5 * ease(t / 1.0)
    tower(P, 480, 820, a, scale=1.08)
    angle_arc(P, 480, 820, a * 6, 300, th["accent"])
    P.text(860, 300, f"{a:.1f}°", FB[96], th["accent"])
    if t > rel(7, 7) + 1.6:
        P.rrect(690, 520, 1010, 620, 20, fill=RED); P.text(850, 570, "CLOSED", FB[60], WHITE)

def scene_fix(P, t, sd, th):
    ground(P, 700, layers=True)
    p = clamp((t - 1.0) / max(0.1, sd - 1.6))
    a = lerp(5.5, 4.0, ease(p))
    tower(P, 540, 700, a, scale=0.95)
    # extraction tubes on north (left) side
    for i, y in enumerate((760, 820)):
        P.line([(60, y - 160), (380, y)], (90, 90, 100), 16)
        for j in range(5):
            ph = (t * 0.7 + j / 5 + i * 0.1) % 1
            P.circle(lerp(380, 60, ph), lerp(y, y - 160, ph), 10, fill=SAND)
    P.text(150, 600, "N", FB[60], th["text"]); P.text(930, 600, "S", FB[60], th["text"])
    P.rrect(320, 90, 760, 190, 40, fill=(0, 0, 0, 140)); P.text(540, 140, f"{a:.1f}°", FB[72], th["accent"])

def scene_end(P, t, sd, th):
    ground(P, 820)
    tower(P, 540, 820, 4.0, scale=1.12)
    k = back((t - 0.3) / 0.5)
    if t > 0.3:
        P.circle(860, 260, 90 * clamp(k, 0, 1.2), fill=(80, 200, 130)); P.line([(815, 262), (848, 295), (905, 228)], WHITE, 18)
    P.rrect(90, 110, 470, 200, 40, fill=(0, 0, 0, 140)); P.text(280, 155, "reopened 2001", FX[44], th["accent"])

SCENES = [
    dict(s=0, title="800+ YEARS OF LEANING", fn=scene_hook),
    dict(s=1, title="SO WHY NO FALL?", fn=scene_why),
    dict(s=2, title="IT STARTED IN 1173", fn=scene_build),
    dict(s=3, title="THE GROUND GAVE WAY", fn=scene_sink),
    dict(s=5, title="A 100-YEAR PAUSE", fn=scene_pause),
    dict(s=7, title="DANGER ZONE", fn=scene_1990, title_color=(255, 140, 120)),
    dict(s=8, title="THE CLEVER FIX", fn=scene_fix, title_color=(150, 210, 255)),
    dict(s=10, title="SAFE FOR ~200 YEARS", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = TM
        pts = [2, tm[1]["start"] + 0.8, tm[2]["start"] + 2.5, tm[4]["start"] + 1, tm[6]["start"] + 1.5, tm[7]["start"] + 3.5, tm[9]["start"] + 1.5, tm[10]["start"] + 2]
        render("pisa", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/pi", preview=pts)
    else:
        render("pisa", SCENES, T, "/home/claude/shorts/pisa.mp4")
