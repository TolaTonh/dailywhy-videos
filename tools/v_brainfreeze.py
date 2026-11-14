import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(12, 52, 88), bg2=(6, 16, 38), accent=(255, 125, 185), accent2=(130, 230, 255), text=(245, 252, 255))
PINK, CONE, CONE2, ICE, RED, WHITE, SKIN = (255, 160, 200), (225, 165, 90), (190, 130, 60), (130, 230, 255), (240, 70, 90), (255, 255, 255), (255, 214, 180)

def cone(P, x, y, s, wob=0):
    P.poly([(x - 110 * s, y), (x + 110 * s, y), (x, y + 330 * s)], fill=CONE)
    for k in range(-3, 4):
        P.line([(x + k * 30 * s, y + 5), (x + k * 30 * s * 0.3 + 40 * s, y + 250 * s)], CONE2, 5 * s)
    P.circle(x + wob, y - 70 * s, 140 * s, fill=PINK)
    P.circle(x - 40 * s + wob, y - 170 * s, 90 * s, fill=(255, 230, 240))
    P.circle(x + 30 * s + wob, y - 120 * s, 22 * s, fill=RED)

def scene_hook(P, t, sd, th):
    cone(P, 540, 470, 1.25, wob=math.sin(t * 6) * 10)
    for i in range(3):
        a = t * 1.5 + i * 2.1
        snowflake_small(P, 540 + 330 * math.cos(a), 450 + 200 * math.sin(a), 40, ICE)

def snowflake_small(P, x, y, r, col):
    for k in range(3):
        a = k * math.pi / 3
        P.line([(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], col, 9)

def scene_name(P, t, sd, th):
    word1, word2 = "SPHENOPALATINE", "GANGLIONEURALGIA"
    n = int(clamp(t / 1.6) * (len(word1) + len(word2)))
    P.rrect(60, 200, 1020, 560, 50, fill=(255, 255, 255, 25), outline=th["accent2"], width=6)
    P.text(540, 310, word1[:n], FB[96].font_variant(size=76), th["accent2"])
    P.text(540, 440, word2[:max(0, n - len(word1))], FB[96].font_variant(size=76), th["accent2"])
    if t > sd * 0.5:
        k = back((t - sd * 0.5) / 0.4)
        P.text(540, 690, "(try saying it with", FX[58], th["text"] + (int(255 * clamp(k)),))
        P.text(540, 770, "a mouth full of ice cream)", FX[58], th["text"] + (int(255 * clamp(k)),))

def head(P, x, y, s, skin=SKIN):
    # side profile facing right
    P.circle(x - 40 * s, y - 120 * s, 230 * s, fill=skin)
    P.poly([(x + 140 * s, y - 180 * s), (x + 215 * s, y - 40 * s), (x + 175 * s, y - 20 * s), (x + 190 * s, y + 40 * s),
            (x + 180 * s, y + 120 * s), (x + 60 * s, y + 200 * s), (x - 60 * s, y + 220 * s), (x - 120 * s, y + 80 * s)], fill=skin)
    P.rect(x - 130 * s, y + 150 * s, x + 20 * s, y + 360 * s, fill=skin)
    P.circle(x + 110 * s, y - 140 * s, 18 * s, fill=(40, 40, 60))

def scene_mouth(P, t, sd, th):
    head(P, 470, 520, 1.25)
    # mouth opening + palate line
    P.ellipse(690, 600, 50, 26, fill=(140, 40, 60))
    P.line([(700, 575), (560, 560), (440, 590)], (255, 255, 255, 230), 10)
    # spoon/ice cream moving in
    k = ease(t / 1.2)
    P.circle(lerp(1050, 760, k), 600, 55, fill=PINK)
    cold = clamp((t - 1.0) / 1.0)
    for i in range(4):
        r = 60 + ((t * 120 + i * 60) % 240)
        P.arc(560, 565, r, 180, 360, ICE + (int(255 * cold * (1 - (r - 60) / 240)),), 8)
    if t > 1.4:
        P.rrect(150, 830, 930, 910, 40, fill=(0, 0, 0, 150))
        P.text(540, 870, "nerves + blood vessels chill", FX[44], th["accent2"])

def scene_vessel(P, t, sd, th):
    p = t / sd
    squeeze = math.sin(clamp(p / 0.9) * math.pi)  # 0 -> 1 -> 0
    r = lerp(110, 38, squeeze)
    P.rrect(80, 460 - r - 18, 1000, 460 + r + 18, r + 18, fill=(255, 150, 160))
    P.rrect(80, 460 - r, 1000, 460 + r, r, fill=RED)
    for i in range(7):
        x = 80 + ((t * 260 + i * 140) % 920)
        P.ellipse(x, 460, min(46, r * 0.8), min(30, r * 0.55), fill=(180, 30, 50))
    lab = "SQUEEZE" if p < 0.5 else "WIDEN!"
    P.text(540, 220, lab, FB[96], th["accent2"] if p < 0.5 else th["accent"])
    P.arrow(540, 780, 540, 700 if p < 0.5 else 860, th["text"]) if False else None

def scene_pain(P, t, sd, th):
    head(P, 470, 560, 1.25)
    # brain
    P.ellipse(410, 400, 170, 120, fill=(255, 170, 200))
    for i in range(4): P.arc(410 - 60 + i * 40, 400, 50, 200, 340, (230, 120, 160), 7)
    # bolt from palate to forehead
    k = clamp((t - 0.3) / 0.8)
    pts = [(560, 600), (620, 520), (580, 500), (650, 400), (610, 380), (690, 300)]
    n = max(2, int(k * len(pts)))
    P.line(pts[:n], (255, 230, 80), 16)
    if k >= 1:
        s = 1 + 0.15 * math.sin(t * 12)
        star = [(690 + (90 if i % 2 == 0 else 40) * s * math.cos(i * math.pi / 6), 290 + (90 if i % 2 == 0 else 40) * s * math.sin(i * math.pi / 6)) for i in range(12)]
        P.poly(star, fill=(255, 230, 80))
        P.text(860, 180, "OUCH!", FB[84], th["accent"])

def scene_study(P, t, sd, th):
    P.text(540, 140, "145 students, 100 ml of ice cream", FX[44], th["text"])
    bars = [("UNDER 5 SEC", 27, th["accent"]), ("SLOW (30+ SEC)", 12.5, th["accent2"])]
    for i, (lab, v, col) in enumerate(bars):
        x = 300 + i * 480; k = ease((t - 0.3 - i * 0.3) / 1.0)
        h = 430 * (v / 30) * k
        P.rrect(x - 120, 760 - h, x + 120, 760, 24, fill=col)
        P.text(x, 760 - h - 60, (f"{v * k:.1f}%" if v % 1 else f"{v * k:.0f}%"), FB[72], col)
        P.text(x, 815, lab, FX[36], th["text"])
    if t > 2:
        P.text(540, 205, "how many got brain freeze", FS[40], th["accent2"])

def mug(P, x, y, s, t):
    P.rrect(x - 140 * s, y - 150 * s, x + 140 * s, y + 150 * s, 40 * s, fill=(255, 140, 90))
    P.arc(x + 150 * s, y, 80 * s, 270, 90, (255, 140, 90), 28 * s)
    for i in range(3):
        ph = (t * 0.6 + i / 3) % 1
        P.wave(x - 80 * s + i * 70 * s, x - 40 * s + i * 70 * s, y - 220 * s - ph * 140, 18, 6, t * 5 + i, (255, 255, 255, int(220 * (1 - ph))), 10)

def scene_fix(P, t, sd, th):
    P.rrect(80, 160, 520, 820, 50, fill=(255, 255, 255, 22))
    P.rrect(560, 160, 1000, 820, 50, fill=(255, 255, 255, 22))
    # tongue up
    P.ellipse(300, 470, 150, 90, fill=(140, 40, 60))
    ty = lerp(520, 430, (math.sin(t * 3) + 1) / 2)
    P.ellipse(300, ty, 110, 55, fill=(255, 120, 150))
    P.line([(160, 400), (440, 400)], WHITE, 10)
    P.text(300, 720, "TONGUE UP", FX[44], th["accent"])
    mug(P, 760, 520, 0.9, t)
    P.text(780, 720, "SIP WARM", FX[44], (255, 170, 120))

def scene_end(P, t, sd, th):
    # snail
    x = lerp(150, 620, clamp(t / sd)); y = 600
    P.rrect(x - 160, y + 40, x + 160, y + 110, 35, fill=(170, 220, 140))
    P.circle(x, y - 40, 130, fill=th["accent"])
    for r in (95, 60, 28): P.arc(x, y - 40, r, 0, 300, (200, 80, 130), 12)
    P.line([(x + 140, y + 50), (x + 190, y - 60)], (170, 220, 140), 14); P.circle(x + 190, y - 70, 14, fill=(40, 40, 60))

SCENES = [
    dict(s=0, title="IT HAS A REAL NAME", fn=scene_hook),
    dict(s=1, title="SAY IT FAST...", fn=scene_name),
    dict(s=3, title="THE ROOF OF YOUR MOUTH", fn=scene_mouth, title_color=(130, 230, 255)),
    dict(s=4, title="BLOOD VESSELS REACT", fn=scene_vessel),
    dict(s=5, title="WRONG ADDRESS", fn=scene_pain),
    dict(s=6, title="THE ICE CREAM STUDY", fn=scene_study),
    dict(s=7, title="QUICK FIX", fn=scene_fix),
    dict(s=8, title="EAT SLOW", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = json.load(open("/home/claude/shorts/brainfreeze_timing.json"))["sentences"]
        pts = [1.5, tm[1]["start"] + 2.5, tm[3]["start"] + 2.5, tm[4]["start"] + 0.8, tm[4]["end"] - 0.3, tm[5]["start"] + 2.5, tm[6]["start"] + 3, tm[7]["start"] + 2]
        render("brainfreeze", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/bf", preview=pts)
    else:
        render("brainfreeze", SCENES, T, "/home/claude/shorts/brainfreeze.mp4")
