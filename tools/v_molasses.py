import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(66, 40, 22), bg2=(18, 10, 6), accent=(255, 182, 64), accent2=(150, 205, 245), text=(255, 248, 238))
TM = json.load(open("/home/claude/shorts/molasses_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.12
MOL, MOL2, BLD, BLD2, TANK, WHITE, SNOW, STREET = (120, 60, 20), (160, 90, 35), (70, 62, 70), (95, 85, 95), (150, 155, 165), (255, 255, 255), (230, 240, 250), (55, 50, 55)

def city(P, base=760):
    rnd = random.Random(5)
    x = 0
    while x < 1080:
        w = rnd.randint(90, 160); h = rnd.randint(160, 380)
        P.rect(x, base - h, x + w - 8, base, fill=BLD if (x // 100) % 2 else BLD2)
        for wy in range(base - h + 30, base - 30, 60):
            for wx in range(x + 18, x + w - 30, 40):
                P.rect(wx, wy, wx + 18, wy + 26, fill=(255, 210, 120, 120))
        x += w
    P.rect(0, base, 1080, 940, fill=STREET)

def tank(P, cx, base, s=1.0, crack=0.0, fill_lvl=0.85):
    w, h = 210 * s, 420 * s
    P.rect(cx - w, base - h, cx + w, base, fill=TANK)
    P.rect(cx - w + 12, base - h * fill_lvl, cx + w - 12, base - 10, fill=MOL)
    P.ellipse(cx, base - h, w, 40 * s, fill=(175, 180, 190))
    for i in range(6):
        P.line([(cx - w, base - h + i * h / 6), (cx + w, base - h + i * h / 6)], (120, 125, 135), 4)
    if crack > 0:
        pts = [(cx + 40 * s, base - h * 0.2), (cx + 10 * s, base - h * 0.35), (cx + 55 * s, base - h * 0.5), (cx + 20 * s, base - h * 0.65), (cx + 60 * s, base - h * 0.8)]
        n = max(2, int(crack * len(pts)))
        P.line(pts[:n], (30, 20, 15), 9)

def scene_hook(P, t, sd, th):
    city(P)
    tank(P, 800, 760, 0.8)
    P.rrect(90, 110, 480, 200, 45, fill=(0, 0, 0, 150)); P.text(285, 155, "BOSTON, 1919", FX[44], th["accent"])

def scene_joke(P, t, sd, th):
    city(P)
    tank(P, 800, 760, 0.8)
    P.rect(0, 0, 1080, 940, fill=(0, 0, 0, 110))

def scene_tank(P, t, sd, th):
    crack = clamp((t - (sd - 1.6)) / 1.2)
    shake = (math.sin(t * 60) * 6 * crack) if crack > 0 else 0
    tank(P, 540 + shake, 820, 1.25, crack=crack)
    v = 2.3 * ease(t / 2.0)
    P.rrect(170, 90, 910, 210, 40, fill=(0, 0, 0, 150))
    P.text(540, 150, f"{v:.1f} MILLION GALLONS", FB[60], th["accent"])

def scene_wave(P, t, sd, th):
    city(P, 700)
    p = ease(t / (sd * 0.8))
    front = lerp(-200, 1200, p)
    pts = [(-50, 940), (-50, 380)]
    for x in range(-50, int(front) + 1, 20):
        pts.append((x, 380 + 18 * math.sin(x / 60 + t * 4) + max(0, (x - front + 260)) * 0.9))
    pts += [(front + 40, 940)]
    if front > -50: P.poly(pts, fill=MOL)
    if front > -50: P.wave(-50, max(-40, front - 200), 385, 14, 1.6, t * 4, MOL2, 14)
    P.rrect(120, 100, 480, 190, 40, fill=(0, 0, 0, 150)); P.text(300, 145, "up to 40 ft", FX[44], th["accent"])
    P.rrect(600, 100, 960, 190, 40, fill=(0, 0, 0, 150)); P.text(780, 145, "~35 mph", FX[44], th["accent"])

def scene_lives(P, t, sd, th):
    for i in range(21):
        k = clamp((t - i * 0.06) / 0.4)
        x = 160 + (i % 7) * 127; y = 260 + (i // 7) * 160
        P.circle(x, y, 34 * k, fill=(245, 225, 190, int(230 * k)))
        fl = 10 + 3 * math.sin(t * 8 + i)
        P.ellipse(x, y - 52, 9, fl, fill=(255, 190, 80, int(255 * k)))
    P.text(540, 790, "21 lives lost  ·  ~150 injured", FX[44], th["text"])

def scene_why(P, t, sd, th):
    s = 1 + 0.05 * math.sin(t * 4)
    P.circle(540, 470, 240 * s, fill=th["accent"])
    P.text(540, 470, "?", FB[150].font_variant(size=280), (50, 28, 12))

def thermo(P, x, top, bot, lvl, col, lab, th):
    P.rrect(x - 40, top, x + 40, bot, 40, fill=WHITE); P.circle(x, bot + 30, 64, fill=WHITE)
    P.rrect(x - 20, lerp(bot, top + 30, lvl), x + 20, bot, 20, fill=col); P.circle(x, bot + 30, 46, fill=col)
    P.text(x, bot + 140, lab, FX[44], th["text"])

def scene_cold(P, t, sd, th):
    b = rel(7, 6)
    if t < b:
        thermo(P, 330, 160, 600, 0.6, (230, 120, 60), "MOLASSES", th)
        thermo(P, 750, 160, 600, 0.25, (90, 160, 240), "WINTER AIR", th)
        P.text(540, 120, "warmer than the air", FS[40], th["accent"])
    else:
        k = ease((t - b) / 1.6)
        P.text(540, 170, "THICKNESS", FX[44], th["text"])
        P.rrect(140, 260, 940, 380, 40, fill=(255, 255, 255, 30))
        P.rrect(140, 260, 140 + 200 + 600 * k, 380, 40, fill=MOL2)
        P.text(540, 320, f"{1 + 3 * k:.0f}x+", FB[72], WHITE)
        rnd = random.Random(2)
        for i in range(10):
            ph = (t * 0.6 + rnd.random()) % 1
            snowflake_s(P, rnd.uniform(100, 980), 450 + ph * 380, 22, SNOW + (int(255 * (1 - ph)),))

def snowflake_s(P, x, y, r, col):
    for k in range(3):
        a = k * math.pi / 3
        P.line([(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], col, 6)

def scene_stuck(P, t, sd, th):
    for i, (lab, speed, x, col) in enumerate((("WATER", 1.0, 300, (90, 160, 240)), ("COLD MOLASSES", 0.12, 780, MOL))):
        P.rrect(x - 170, 200, x + 170, 800, 30, fill=col + (200,))
        y = 240 + ((t * speed * 520) % 520)
        P.circle(x, y, 40, fill=WHITE)
        P.text(x, 860, lab, FX[44], th["text"])

def scene_wall(P, t, sd, th):
    k = ease(t / 1.2)
    P.text(540, 150, "TANK WALL THICKNESS", FX[44], th["text"])
    P.rrect(200, 260, 200 + 680 * k, 360, 20, fill=th["accent2"]); P.text(540, 410, "needed", FS[40], th["accent2"])
    P.rrect(200, 500, 200 + 340 * k, 600, 20, fill=(240, 90, 80)); P.text(540, 650, "actual: about half", FS[40], (255, 140, 130))

def scene_lab(P, t, sd, th):
    P.rrect(170, 160, 910, 820, 40, fill=(200, 225, 245, 40), outline=th["accent2"], width=8)
    snowflake_s(P, 820, 240, 40, SNOW)
    P.text(380, 230, "COLD ROOM", FX[44], th["accent2"])
    # slow syrup spreading
    k = ease(t / sd)
    P.rect(260, 700, 820, 760, fill=(120, 120, 130))
    P.poly([(300, 700), (300 + 420 * k, 700), (300 + 420 * k - 20, 680), (300, 600)], fill=(230, 170, 70))
    P.text(540, 890, "corn syrup model", FX[44], th["text"])

def scene_end(P, t, sd, th):
    P.circle(380, 470, 160, fill=th["accent2"]); snowflake_s(P, 380, 470, 90, WHITE)
    P.text(560, 470, "+", FB[120], th["text"])
    P.circle(760, 470, 160, fill=MOL2); P.drop(760, 500, 70, (255, 200, 110))

SCENES = [
    dict(s=0, title="A WAVE OF MOLASSES", fn=scene_hook),
    dict(s=1, title="NOT A JOKE", fn=scene_joke, title_color=(255, 140, 120)),
    dict(s=2, title="THE TANK BURST", fn=scene_tank),
    dict(s=3, title="A STICKY TSUNAMI", fn=scene_wave),
    dict(s=4, title="JANUARY 15, 1919", fn=scene_lives, title_color=(245, 225, 190)),
    dict(s=5, title="WHY SO DEADLY?", fn=scene_why),
    dict(s=6, title="THE COLD MADE IT WORSE", fn=scene_cold, title_color=(150, 205, 245)),
    dict(s=8, title="LIKE MOVING IN GLUE", fn=scene_stuck),
    dict(s=9, title="A WEAK TANK", fn=scene_wall),
    dict(s=10, title="SCIENCE CONFIRMED IT", fn=scene_lab, title_color=(150, 205, 245)),
    dict(s=11, title="COLD + SYRUP = TRAP", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = TM
        pts = [2, tm[2]["start"] + 4.5, tm[3]["start"] + 3, tm[4]["start"] + 2, tm[6]["start"] + 1, tm[7]["start"] + 2, tm[8]["start"] + 2, tm[9]["start"] + 3]
        render("molasses", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/mo", preview=pts)
    else:
        render("molasses", SCENES, T, "/home/claude/shorts/molasses.mp4")
