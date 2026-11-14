import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(48, 18, 70), bg2=(16, 8, 32), accent=(190, 242, 100), accent2=(205, 130, 255), text=(250, 248, 255))
PURP, PURP2, SKIN, WHITE, YEL, BLUE, TEAR = (150, 70, 200), (110, 45, 160), (230, 200, 240), (255, 255, 255), (255, 210, 60), (90, 170, 255), (120, 200, 255)

def onion(P, x, y, s=1.0, col=PURP, col2=PURP2, face=None):
    P.line([(x, y - 190 * s), (x - 18 * s, y - 280 * s)], (120, 200, 90), 16 * s)
    P.line([(x, y - 190 * s), (x + 22 * s, y - 270 * s)], (120, 200, 90), 16 * s)
    P.poly([(x - 60 * s, y - 150 * s), (x, y - 215 * s), (x + 60 * s, y - 150 * s)], fill=col)
    P.circle(x, y, 190 * s, fill=col)
    for k in (0.55, 0.8):
        P.arc(x, y, 190 * s * k, 200, 340, col2, 10 * s)
    for dx in (-30, 0, 30):
        P.line([(x + dx * s, y + 185 * s), (x + dx * 1.6 * s, y + 230 * s)], (220, 200, 170), 7 * s)
    if face == "sad":
        P.circle(x - 60 * s, y - 10 * s, 16 * s, fill=WHITE); P.circle(x + 60 * s, y - 10 * s, 16 * s, fill=WHITE)
        P.arc(x, y + 90 * s, 50 * s, 200, 340, WHITE, 9 * s)

def scene_hook(P, t, sd, th):
    b = math.sin(t * 5) * 12
    onion(P, 540, 500 + b, 1.05, face="sad")
    for i in range(6):
        ph = (t * 0.9 + i / 6) % 1
        x = 300 + (i % 2) * 480 + (i // 2) * 12
        P.drop(x, 330 + ph * 600, 22, TEAR + (int(255 * (1 - ph)),))
    P.rrect(250, 820, 830, 905, 45, fill=(0, 0, 0, 120))
    P.text(540, 862, "tiny chemical defense", FX[44], th["accent"])

def scene_cells(P, t, sd, th):
    p = t / sd
    # cell with two chambers
    P.rrect(150, 220, 930, 760, 60, fill=(255, 255, 255, 30), outline=th["accent2"], width=8)
    cut = ease((p - 0.45) / 0.15)
    if cut < 1:
        P.rect(532, 230, 548, 750, fill=th["accent2"] + (int(255 * (1 - cut)),))
    rnd = random.Random(3)
    for i in range(14):  # sulfur dots
        bx, by = rnd.uniform(200, 490), rnd.uniform(270, 710)
        mx = lerp(bx, rnd.uniform(220, 860), ease((p - 0.55) / 0.35)) + math.sin(t * 3 + i) * 6
        P.circle(mx, by, 22, fill=YEL)
    for i in range(6):  # enzymes (pac-man)
        bx, by = rnd.uniform(600, 880), rnd.uniform(280, 700)
        mx = lerp(bx, rnd.uniform(220, 860), ease((p - 0.55) / 0.35))
        a = 25 + 20 * abs(math.sin(t * 6 + i))
        P.d.pieslice([P.s(mx - 34), P.s(by - 34), P.s(mx + 34), P.s(by + 34)], a, 360 - a, fill=BLUE)
    P.text(330, 170, "SULFUR", FX[44], YEL); P.text(750, 170, "ENZYME", FX[44], BLUE)
    if p > 0.42:  # knife slicing down
        k = ease((p - 0.42) / 0.12); ky = lerp(-120, 520, k)
        P.poly([(520, ky - 300), (580, ky - 300), (560, ky + 140), (540, ky + 180)], fill=(220, 225, 235))
        P.rrect(515, ky - 470, 585, ky - 300, 18, fill=(60, 40, 30))
    if p > 0.6:
        P.text(540, 870, "BREAK THE CELLS = THEY MIX", FX[44], th["accent"])

def gas_particles(P, t, x0, y0, spread, rise, n=26, seed=5):
    rnd = random.Random(seed)
    for i in range(n):
        ph = (t * 0.35 + rnd.random()) % 1
        x = x0 + rnd.uniform(-spread, spread) + math.sin(t * 2 + i) * 30
        y = y0 - ph * rise
        P.circle(x, y, 14 + 10 * rnd.random(), fill=(190, 242, 100, int(220 * (1 - ph))))

def scene_gas(P, t, sd, th):
    # cut onion half
    P.ellipse(540, 760, 300, 120, fill=PURP)
    for k in (0.85, 0.65, 0.45, 0.25):
        P.ellipse(540, 760, 300 * k, 120 * k, outline=SKIN, width=8)
    gas_particles(P, t, 540, 700, 230, 560)
    chip = ease((t - 0.6) / 0.4)
    P.rrect(200, 150 - 40 * (1 - chip), 880, 250 - 40 * (1 - chip), 50, fill=(0, 0, 0, int(170 * chip)))
    P.text(540, 200 - 40 * (1 - chip), "propanethial S-oxide", FX[44], th["accent"] + (int(255 * chip),))

def eye(P, x, y, s, open_=1.0, col=WHITE):
    h = 150 * s * open_
    P.poly([(x - 300 * s, y)] + [(x + 300 * s * math.cos(a), y - h * math.sin(a)) for a in [i * math.pi / 30 for i in range(31)]]
           + [(x + 300 * s * math.cos(a), y + h * math.sin(a)) for a in [math.pi - i * math.pi / 30 for i in range(31)]], fill=col)
    if open_ > 0.3:
        P.circle(x, y, 95 * s, fill=(90, 60, 140)); P.circle(x, y, 45 * s, fill=(10, 5, 20)); P.circle(x + 25 * s, y - 25 * s, 16 * s, fill=WHITE)

def scene_eye(P, t, sd, th):
    p = t / sd
    squint = 1 - 0.55 * ease((p - 0.35) / 0.2)
    eye(P, 540, 420, 1.2, squint)
    gas_particles(P, t, 540, 880, 300, 360, n=18, seed=9)
    if p > 0.45:
        for i in range(5):
            ph = (t * 1.1 + i / 5) % 1
            P.drop(330 + i * 105, 560 + ph * 380, 26, TEAR + (int(255 * (1 - ph * 0.8)),))
    lab = "ACID!" if p < 0.5 else "TEARS = WASH IT OUT"
    P.text(540, 120, lab, FB[60], th["accent"])

def snowflake(P, x, y, r, col, rot):
    for k in range(6):
        a = rot + k * math.pi / 3
        x2, y2 = x + r * math.cos(a), y + r * math.sin(a)
        P.line([(x, y), (x2, y2)], col, 14)
        for f in (0.55, 0.8):
            bx, by = x + r * f * math.cos(a), y + r * f * math.sin(a)
            for s_ in (-0.6, 0.6):
                P.line([(bx, by), (bx + r * 0.22 * math.cos(a + s_), by + r * 0.22 * math.sin(a + s_))], col, 10)

def scene_chill(P, t, sd, th):
    p = t / sd
    cold = ease(p / 0.5)
    onion(P, 400, 560, 0.9, col=mix(PURP, (120, 190, 255), cold), col2=mix(PURP2, (80, 140, 220), cold))
    snowflake(P, 820, 330, 110, (200, 235, 255), t * 0.8)
    # thermometer
    P.rrect(770, 460, 850, 800, 40, fill=WHITE); P.circle(810, 830, 70, fill=WHITE)
    lvl = lerp(500, 740, cold); P.rrect(792, lvl, 828, 810, 18, fill=BLUE); P.circle(810, 830, 52, fill=BLUE)
    rate = 1 - 0.7 * cold
    gas_particles(P, t * rate, 400, 380, 120, 260 * rate, n=int(14 * rate) + 3, seed=2)
    P.text(540, 120, "COLD = SLOWER ENZYMES", FX[44], (200, 235, 255))

def garlic(P, x, y, s):
    for dx in (-70, 0, 70):
        P.ellipse(x + dx * s, y, 85 * s, 130 * s, fill=(245, 240, 230), outline=(210, 200, 185), width=5)
    P.poly([(x - 30 * s, y - 120 * s), (x, y - 220 * s), (x + 30 * s, y - 120 * s)], fill=(245, 240, 230))

def scene_garlic(P, t, sd, th):
    garlic(P, 540, 600, 1.4)
    k = back((t - 0.4) / 0.4)
    if t > 0.4:
        P.circle(540, 280, 110 * k, fill=th["accent"])
        P.line([(490, 280), (525, 320), (595, 240)], (30, 30, 30), 22)
    P.text(540, 880, "different sulfur compound", FX[44], th["text"])

def scene_end(P, t, sd, th):
    s = 1 + 0.06 * math.sin(t * 4)
    P.circle(540, 520, 300 * s, fill=th["accent"])
    P.text(540, 520, "?", FB[150].font_variant(size=330), (40, 15, 60))

SCENES = [
    dict(s=0, title="IT'S NOT SADNESS", fn=scene_hook),
    dict(s=2, title="TWO SECRET CHAMBERS", fn=scene_cells),
    dict(s=4, title="A GAS IS BORN", fn=scene_gas),
    dict(s=6, title="STRAIGHT TO YOUR EYES", fn=scene_eye),
    dict(s=8, title="THE TRICK: CHILL IT", fn=scene_chill, title_color=(200, 235, 255)),
    dict(s=10, title="GARLIC? NO GAS", fn=scene_garlic),
    dict(s=11, title="GOT A KITCHEN WHY?", fn=scene_end),
]

if __name__ == "__main__":
    import sys as _s
    if len(_s.argv) > 1 and _s.argv[1] == "preview":
        render("onions", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/on", preview=[1.5, 8, 11, 16, 22, 28, 33, 39])
    else:
        render("onions", SCENES, T, "/home/claude/shorts/onions.mp4")
