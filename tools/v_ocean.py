import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(10, 78, 108), bg2=(4, 24, 50), accent=(255, 214, 92), accent2=(120, 224, 232), text=(245, 252, 255))
SEA, SEA2, ROCK, ROCK2, GREEN, WHITE, CLOUD, MAG = (30, 140, 200), (20, 100, 160), (140, 130, 120), (100, 92, 85), (90, 170, 110), (255, 255, 255), (230, 240, 248), (255, 110, 40)

def mountains(P, y, col=ROCK, col2=ROCK2):
    P.poly([(60, y), (300, y - 330), (480, y - 120), (640, y - 300), (900, y), ], fill=col)
    P.poly([(300, y - 330), (360, y - 250), (300, y - 230), (250, y - 260)], fill=WHITE)

def river(P, t, col=(110, 200, 240), dots=None):
    pts = [(560, 640), (520, 700), (600, 760), (560, 820), (700, 880), (1000, 900)]
    P.line(pts, col, 46)
    for i in range(10):
        u = ((t * 0.25 + i / 10) % 1) * (len(pts) - 1); j = int(u); f = u - j
        x = lerp(pts[j][0], pts[j + 1][0], f); y = lerp(pts[j][1], pts[j + 1][1], f)
        P.circle(x, y, 9 if dots is None else 13, fill=WHITE if dots is None else dots[i % len(dots)])

def sea(P, y, t, col=SEA, col2=SEA2):
    P.rect(0, y, 1080, 940, fill=col2)
    P.wave(0, 1080, y, 14, 3, t * 3, col, 26)

def scene_fresh(P, t, sd, th):
    mountains(P, 640)
    P.rect(0, 640, 1080, 940, fill=GREEN)
    river(P, t)
    P.poly([(820, 940), (900, 860), (1080, 840), (1080, 940)], fill=SEA)
    k = back((t - 0.3) / 0.4)
    if t > 0.3:
        P.circle(850, 230, 90 * k, fill=th["accent2"]); P.drop(850, 245, 40 * k, WHITE)
        P.text(850, 360, "FRESH", FX[44], th["accent2"])

def scene_why(P, t, sd, th):
    sea(P, 560, t)
    for i in range(3): P.wave(0, 1080, 650 + i * 90, 12, 3, t * 3 + i, (60, 170, 225), 14)
    s = 1 + 0.08 * math.sin(t * 5)
    P.circle(540, 300, 150 * s, fill=th["accent"])
    P.text(540, 300, "?", FB[150].font_variant(size=230), (10, 40, 70))

def cloud(P, x, y, s, col=CLOUD):
    for dx, dy, r in ((-90, 20, 70), (0, -10, 95), (95, 20, 70), (40, 40, 70), (-40, 40, 70)):
        P.circle(x + dx * s, y + dy * s, r * s, fill=col)

def scene_rain(P, t, sd, th):
    p = t / sd
    cloud(P, 540, 160, 1.4, (200, 215, 230))
    rnd = random.Random(1)
    for i in range(26):
        x = rnd.uniform(380, 720); ph = (t * 1.6 + rnd.random()) % 1
        P.line([(x, 250 + ph * 380), (x - 8, 280 + ph * 380)], (150, 210, 255), 7)
    erode = clamp(p * 1.2)
    rs = [(330, 760, 150), (560, 790, 180), (790, 770, 140)]
    for x, y, r in rs:
        rr = r * (1 - 0.25 * erode)
        P.poly([(x - rr, y + 100), (x - rr * 0.8, y - rr * 0.5), (x - rr * 0.1, y - rr * 0.8), (x + rr * 0.7, y - rr * 0.45), (x + rr, y + 100)], fill=ROCK)
    if p > 0.35:
        cols = [(255, 214, 92), (255, 140, 120), (180, 140, 255), (120, 240, 200)]
        for i in range(18):
            ph = (t * 0.5 + i / 18) % 1
            x = 250 + (i * 37) % 600 + math.sin(t * 2 + i) * 20
            P.circle(x, 760 - ph * 140, 12, fill=cols[i % 4] + (int(255 * (1 - ph)),))
    lab = "SLIGHTLY ACIDIC" if p < 0.55 else "IONS (tiny minerals)"
    P.rrect(200, 300 - 40 + 330, 880, 300 + 40 + 330, 40, fill=(0, 0, 0, 140)) if False else None
    P.text(540, 470, lab, FX[58], th["accent"])

def scene_carry(P, t, sd, th):
    mountains(P, 640, (120, 112, 105))
    P.rect(0, 640, 1080, 940, fill=GREEN)
    river(P, t * 1.5, dots=[(255, 214, 92), (255, 140, 120), (180, 140, 255), (120, 240, 200)])
    P.poly([(820, 940), (900, 860), (1080, 840), (1080, 940)], fill=SEA)
    P.arrow(860, 300, 980, 760, th["accent"], 16, 46)
    P.text(780, 250, "TO THE SEA", FX[58], th["accent"])

def sun(P, x, y, r, t, col=(255, 210, 80)):
    for k in range(12):
        a = t * 0.6 + k * math.pi / 6
        P.line([(x + r * 1.25 * math.cos(a), y + r * 1.25 * math.sin(a)), (x + r * 1.6 * math.cos(a), y + r * 1.6 * math.sin(a))], col, 12)
    P.circle(x, y, r, fill=col)

def scene_evap(P, t, sd, th):
    p = t / sd
    sun(P, 860, 170, 90, t)
    sea(P, 480, t)
    for i in range(7):
        ph = (t * 0.7 + i / 7) % 1
        P.drop(180 + i * 100, 470 - ph * 300, 16, (170, 220, 255, int(255 * (1 - ph))))
    # salt crystals accumulate on sea floor
    n = int(4 + p * 30); rnd = random.Random(4)
    for i in range(n):
        x, y = rnd.uniform(80, 1000), rnd.uniform(830, 910)
        P.rect(x - 14, y - 14, x + 14, y + 14, fill=WHITE)
    P.text(270, 610, "WATER UP", FX[44], (190, 230, 255))
    P.text(780, 760, "SALT STAYS", FX[44], th["accent"])

def scene_vent(P, t, sd, th):
    P.poly([(0, 940), (0, 760), (380, 720), (470, 560), (610, 560), (700, 720), (1080, 760), (1080, 940)], fill=(60, 50, 50))
    P.poly([(500, 940), (520, 640), (560, 640), (580, 940)], fill=MAG)
    glow = 0.5 + 0.5 * math.sin(t * 4)
    P.circle(540, 560, 60 + 10 * glow, fill=(255, 150, 60, 200))
    rnd = random.Random(7)
    for i in range(30):
        ph = (t * 0.5 + rnd.random()) % 1
        x = 540 + rnd.uniform(-40, 40) * (1 + ph * 4) + math.sin(t * 2 + i) * 15
        P.circle(x, 540 - ph * 420, 16 + ph * 22, fill=(90, 90, 100, int(200 * (1 - ph))))
    P.text(540, 120, "MAGMA-HEATED WATER", FX[44], (255, 170, 110))

def scene_pct(P, t, sd, th):
    k = ease(t / 1.4)
    P.text(470, 330, f"{3.5 * k:.1f}", FB[150].font_variant(size=260), th["accent"])
    P.text(770, 360, "%", FB[150], th["accent"])
    P.text(540, 520, "of seawater's weight is salt", FX[44], th["text"])
    # glass bar
    P.rrect(140, 640, 940, 740, 30, fill=(60, 150, 210))
    P.rect(140, 640, 140 + 800 * 0.035 * k, 740, fill=WHITE) if k > 0 else None
    P.text(540, 800, "about 35 grams of salt in every kilo of seawater", FS[34], th["accent2"])

def scene_nacl(P, t, sd, th):
    j = ease((t - 0.2) / 0.9)
    P.circle(lerp(220, 440, j), 330, 120, fill=(180, 120, 255)); P.text(lerp(220, 440, j), 330, "Na", FB[84], WHITE)
    P.circle(lerp(860, 640, j), 330, 140, fill=(110, 220, 140)); P.text(lerp(860, 640, j), 330, "Cl", FB[84], WHITE)
    # fries
    if t > 1.5:
        P.poly([(400, 560), (680, 560), (650, 800), (430, 800)], fill=(230, 60, 60))
        for i in range(7):
            x = 410 + i * 40; P.rrect(x, 470 + (i % 3) * 25, x + 30, 620, 8, fill=(255, 205, 90))
        rnd = random.Random(2)
        for i in range(25):
            ph = (t * 0.8 + rnd.random()) % 1
            P.rect(400 + rnd.uniform(0, 280) - 4, 420 + ph * 220 - 4, 400 + rnd.uniform(0, 280) * 0 + 4 + rnd.uniform(0, 280), 420 + ph * 220 + 4, fill=WHITE) if False else P.circle(400 + rnd.uniform(20, 260), 440 + ph * 200, 6, fill=WHITE)

SCENES = [
    dict(s=0, title="RIVERS ARE FRESH", fn=scene_fresh, title_color=(120, 224, 232)),
    dict(s=2, title="SO WHY IS THE SEA SALTY?", fn=scene_why),
    dict(s=3, title="BLAME THE RAIN", fn=scene_rain),
    dict(s=6, title="RIVERS CARRY IT", fn=scene_carry),
    dict(s=7, title="THE SUN DOES THE REST", fn=scene_evap),
    dict(s=8, title="BONUS: SEA-FLOOR CRACKS", fn=scene_vent, title_color=(255, 170, 110)),
    dict(s=9, title="HOW SALTY?", fn=scene_pct),
    dict(s=10, title="SAME AS TABLE SALT", fn=scene_nacl),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = json.load(open("/home/claude/shorts/ocean_timing.json"))["sentences"]
        pts = [1.5, tm[2]["start"] + 1, tm[4]["start"] + 2, tm[5]["start"] + 1, tm[6]["start"] + 1.5, tm[7]["start"] + 2.5, tm[8]["start"] + 2.5, tm[9]["start"] + 2.5]
        render("ocean", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/oc", preview=pts)
        render("ocean", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/oc2", preview=[tm[10]["start"] + 2.5])
    else:
        render("ocean", SCENES, T, "/home/claude/shorts/ocean.mp4")
