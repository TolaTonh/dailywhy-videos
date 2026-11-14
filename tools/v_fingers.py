import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(84, 34, 52), bg2=(26, 10, 22), accent=(120, 232, 190), accent2=(255, 175, 145), text=(255, 248, 245))
TM = json.load(open("/home/claude/shorts/fingers_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.12
SKIN, SKIN2, WATER, WHITE, RED, NERVE = (250, 196, 160), (220, 150, 120), (90, 170, 230), (255, 255, 255), (220, 60, 70), (255, 220, 90)

def hand(P, x, y, s, col=SKIN):
    P.rrect(x - 150 * s, y - 40 * s, x + 150 * s, y + 260 * s, 80 * s, fill=col)
    for i, (dx, h) in enumerate(((-110, 250), (-40, 300), (35, 290), (105, 240))):
        P.rrect(x + dx * s - 32 * s, y - h * s, x + dx * s + 32 * s, y + 20 * s, 32 * s, fill=col)
    P.rrect(x + 120 * s, y + 40 * s, x + 260 * s, y + 110 * s, 35 * s, fill=col)

def wrinkles(P, x0, y0, x1, y1, amt, col, t=0):
    if amt <= 0: return
    n = 6
    for i in range(n):
        y = lerp(y0, y1, (i + 0.5) / n)
        pts = [(x, y + amt * 10 * math.sin(x / 14 + i)) for x in range(int(x0), int(x1) + 1, 6)]
        P.line(pts, col + (int(255 * clamp(amt)),), 6)

def scene_bath(P, t, sd, th):
    hand(P, 540, 470, 1.1)
    P.rect(0, 620, 1080, 940, fill=(90, 170, 230, 170))
    P.wave(0, 1080, 620, 12, 3, t * 3, (150, 210, 250), 14)
    rnd = random.Random(1)
    for i in range(12):
        ph = (t * 0.5 + rnd.random()) % 1
        P.circle(rnd.uniform(80, 1000), 920 - ph * 280, 8 + rnd.random() * 14, outline=(220, 240, 255), width=4)
    # fingertips wrinkly
    for dx, h in ((-110, 250), (-40, 300), (35, 290), (105, 240)):
        x = 540 + dx * 1.1; top = 470 - h * 1.1
        wrinkles(P, x - 24, top + 20, x + 24, top + 90, 0.8, SKIN2)

def scene_nerve(P, t, sd, th):
    # brain at top, nerve line down to a finger
    P.ellipse(540, 160, 170, 110, fill=(255, 170, 200))
    for i in range(4): P.arc(480 + i * 40, 160, 45, 200, 340, (230, 120, 160), 7)
    hand(P, 540, 780, 0.8)
    k = clamp(t / 1.2)
    pts = [(540, 270), (600, 360), (520, 450), (585, 540), (528, 620)]
    n = max(2, int(k * len(pts)) + 1)
    P.line(pts[:n], NERVE, 14)
    if k >= 1:
        P.circle(528, 620, 26 + 6 * math.sin(t * 10), fill=NERVE)

def fingertip(P, x, y, w, h, squeeze, wr, nerve_ok=True, show_nerve=True):
    sw = w * (1 - 0.08 * squeeze)
    P.rrect(x - sw / 2, y - h / 2, x + sw / 2, y + h / 2, sw / 2, fill=SKIN)
    # blood vessels
    vw = lerp(18, 6, squeeze)
    for dx in (-0.22, 0.22):
        P.line([(x + dx * sw, y + h / 2 - 20), (x + dx * sw, y - h / 2 + 90)], RED, vw)
    wrinkles(P, x - sw / 2 + 25, y - h / 2 + 30, x + sw / 2 - 25, y - h / 2 + 200, wr, SKIN2)
    # nail-less fingertip front
    if show_nerve: P.line([(x, y + h / 2), (x, y + h / 2 + 120)], NERVE if nerve_ok else (140, 140, 140), 12)
    if not nerve_ok:
        P.line([(x - 40, y + h / 2 + 30), (x + 40, y + h / 2 + 100)], (230, 60, 60), 14)
        P.line([(x + 40, y + h / 2 + 30), (x - 40, y + h / 2 + 100)], (230, 60, 60), 14)

def scene_squeeze(P, t, sd, th):
    p = t / sd
    # clock
    k = clamp(t / 1.6)
    P.circle(230, 260, 120, fill=(255, 255, 255, 40)); P.arc(230, 260, 110, -90, -90 + 360 * k, th["accent"], 20)
    P.text(230, 260, "5 min", FX[44], th["text"])
    sq = ease((t - 1.0) / 1.5); wr = ease((t - rel(3, 2)) / 1.5)
    fingertip(P, 700, 470, 300, 560, sq, wr)
    if t > 1.2: P.text(700, 120, "vessels squeeze", FS[40], (255, 140, 150))
    if wr > 0.1: P.text(240, 560, "skin folds", FS[40], th["accent2"])

def scene_proof(P, t, sd, th):
    k = clamp((t - rel(5, 4) + 0.3) / 0.6)
    fingertip(P, 300, 430, 260, 480, 1, 1, True)
    fingertip(P, 780, 430, 260, 480, 0, 0, False)
    P.text(300, 820, "NERVES OK", FX[44], th["accent"]); P.text(780, 820, "NERVE DAMAGE", FX[44], (255, 130, 130) + (int(255 * max(k, 0.25)),))
    if k > 0: P.text(780, 110, "no wrinkles", FS[40], th["text"] + (int(255 * k),))

def scene_why(P, t, sd, th):
    s = 1 + 0.06 * math.sin(t * 4)
    P.circle(540, 470, 260 * s, fill=th["accent2"])
    P.text(540, 470, "?", FB[150].font_variant(size=300), (60, 20, 30))

def tire(P, x, y, r, t):
    P.circle(x, y, r, fill=(40, 40, 45)); P.circle(x, y, r * 0.55, fill=(150, 150, 160)); P.circle(x, y, r * 0.2, fill=(90, 90, 100))
    for k in range(16):
        a = t * 1.5 + k * math.pi / 8
        P.line([(x + r * 0.78 * math.cos(a), y + r * 0.78 * math.sin(a)), (x + r * 0.98 * math.cos(a), y + r * 0.98 * math.sin(a))], (90, 90, 95), 14)

def scene_tread(P, t, sd, th):
    tire(P, 270, 450, 200, t)
    P.text(540, 450, "=", FB[120], th["text"])
    fingertip(P, 820, 430, 240, 480, 1, 1, show_nerve=False)
    for i in range(6):
        ph = (t * 0.6 + i / 6) % 1
        P.drop(760 + (i % 3) * 60, 260 + ph * 300, 14, (120, 200, 255, int(255 * (1 - ph))))
    P.text(540, 820, "channels drain the water", FX[44], th["accent"])

def scene_marbles(P, t, sd, th):
    for row, (lab, speed, col) in enumerate((("WRINKLY", 0.55, th["accent"]), ("SMOOTH", 0.4, th["accent2"]))):
        y = 300 + row * 330
        P.rrect(80, y - 90, 260, y + 90, 24, outline=col, width=8); P.rrect(820, y - 90, 1000, y + 90, 24, outline=col, width=8)
        P.text(540, y - 120, lab, FX[44], col)
        for i in range(3):
            ph = (t * speed + i / 3) % 1
            x = lerp(170, 910, ease_io(ph)); yy = y - math.sin(ph * math.pi) * 90
            P.circle(x, yy, 30, fill=(120, 190, 255)); P.circle(x - 9, yy - 9, 9, fill=WHITE)

def scene_debate(P, t, sd, th):
    a = math.sin(t * 2.2) * 0.22
    cx, cy = 540, 360
    P.poly([(cx - 30, 760), (cx + 30, 760), (cx + 8, cy), (cx - 8, cy)], fill=(200, 200, 210))
    P.rrect(cx - 160, 760, cx + 160, 800, 18, fill=(200, 200, 210))
    lx, ly = cx - 330 * math.cos(a), cy - 330 * math.sin(a); rx, ry = cx + 330 * math.cos(a), cy + 330 * math.sin(a)
    P.line([(lx, ly), (rx, ry)], (220, 220, 230), 16)
    for (x, y, sym, col) in ((lx, ly, "GRIP", th["accent"]), (rx, ry, "NO GRIP", (255, 130, 130))):
        P.line([(x, y), (x - 90, y + 160)], (200, 200, 210), 5); P.line([(x, y), (x + 90, y + 160)], (200, 200, 210), 5)
        P.ellipse(x, y + 170, 120, 30, fill=col)
        P.text(x, y + 240, sym, FX[44], col)

def scene_end(P, t, sd, th):
    k = back(t / 0.5)
    P.rrect(170, 220, 910, 640, 80, fill=th["accent"])
    P.poly([(300, 630), (420, 630), (290, 760)], fill=th["accent"])
    if k > 0.5: P.text(540, 430, "WHAT DO YOU THINK?", FB[60], (40, 15, 25))

SCENES = [
    dict(s=0, title="NOT JUST SOGGY SKIN", fn=scene_bath),
    dict(s=1, title="YOUR NERVES DID IT", fn=scene_nerve),
    dict(s=2, title="AFTER ~5 MINUTES", fn=scene_squeeze),
    dict(s=4, title="HOW DO WE KNOW?", fn=scene_proof),
    dict(s=6, title="BUT WHY?", fn=scene_why),
    dict(s=7, title="RAIN TREADS", fn=scene_tread),
    dict(s=8, title="THE MARBLE TEST", fn=scene_marbles),
    dict(s=9, title="STILL DEBATED", fn=scene_debate, title_color=(255, 175, 145)),
    dict(s=10, title="YOUR TURN", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = TM
        pts = [1.5, tm[1]["start"] + 1.8, tm[3]["start"] + 2, tm[5]["start"] + 2, tm[7]["start"] + 2.5, tm[8]["start"] + 2, tm[9]["start"] + 2, tm[10]["start"] + 1.5]
        render("fingers", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/fi", preview=pts)
    else:
        render("fingers", SCENES, T, "/home/claude/shorts/fingers.mp4")
