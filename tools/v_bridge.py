import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(44, 58, 80), bg2=(10, 16, 28), accent=(255, 198, 60), accent2=(150, 205, 245), text=(245, 248, 252))
TM = json.load(open("/home/claude/shorts/bridge_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.12
STEEL, DECK, WATER, WATER2, CABLE, WHITE, HILL = (120, 140, 160), (200, 205, 215), (40, 90, 130), (60, 120, 165), (220, 225, 235), (255, 255, 255), (60, 85, 70)

def side_bridge(P, t, amp=0.0, twist=0.0, gap=None, truss=False, fall=0.0):
    """Side view of a suspension bridge. amp: wave amplitude; gap: (x0,x1) section missing; fall: 0..1 falling section."""
    P.rect(0, 720, 1080, 940, fill=WATER)
    for i in range(3): P.wave(0, 1080, 735 + i * 55, 8, 2.5, t * 2 + i, WATER2, 10)
    P.poly([(0, 720), (0, 560), (90, 600), (130, 720)], fill=HILL); P.poly([(1080, 720), (1080, 540), (980, 590), (950, 720)], fill=HILL)
    tx = (250, 830)
    for x in tx:
        P.rect(x - 16, 260, x + 16, 720, fill=STEEL)
    def deck_y(x):
        if 120 <= x <= 960:
            return 560 + amp * math.sin((x - 120) / 840 * 2 * math.pi * 1.5 - t * 2.4)
        return 560
    # main cable
    pts = []
    for x in range(110, 971, 10):
        if x < tx[0]: y = 560 - (x - 110) / (tx[0] - 110) * 300
        elif x > tx[1]: y = 260 + (x - tx[1]) / (970 - tx[1]) * 300
        else:
            u = (x - tx[0]) / (tx[1] - tx[0]); y = 260 + 4 * 270 * u * (1 - u)
        pts.append((x, y))
    P.line(pts, CABLE, 7)
    # hangers + deck
    for (x, y) in pts[::3]:
        if gap and gap[0] < x < gap[1]: continue
        if tx[0] < x < tx[1]: P.line([(x, y), (x, deck_y(x))], CABLE + (170,), 3)
    seg = []
    for x in range(100, 981, 10):
        if gap and gap[0] < x < gap[1]:
            if seg: P.line(seg, DECK, 22 if not truss else 18); seg = []
            continue
        seg.append((x, deck_y(x)))
    if seg: P.line(seg, DECK, 22 if not truss else 18)
    if truss:
        for x in range(110, 971, 40):
            P.line([(x, 572), (x + 20, 610), (x + 40, 572)], STEEL, 6)
        P.line([(100, 610), (980, 610)], STEEL, 6)
    if gap and fall > 0:
        y = 560 + fall * fall * 260; a = fall * 0.4
        cx = (gap[0] + gap[1]) / 2; hw = (gap[1] - gap[0]) / 2
        P.line([(cx - hw * math.cos(a), y - hw * math.sin(a)), (cx + hw * math.cos(a), y + hw * math.sin(a))], DECK, 22)
        if fall > 0.95:
            for i in range(14):
                ang = math.pi + i * math.pi / 13; r = 60 + 90 * ((t * 2) % 1)
                P.circle(cx + r * math.cos(ang) * 1.6, 720 + r * math.sin(ang) * 0.8, 12, fill=(220, 240, 255, 200))

def scene_hook(P, t, sd, th):
    side_bridge(P, t, amp=22)
    k = back((t - rel(1, 0)) / 0.5)
    if t > rel(1, 0):
        P.rrect(240, 110, 840, 200, 45, fill=th["accent"])
        P.text(540, 155, "\"GALLOPING GERTIE\"", FB[52], (30, 30, 40))

def scene_thin(P, t, sd, th):
    side_bridge(P, t, amp=4)
    k = ease(t / 0.8)
    P.arrow(540, 700, 540, 590, th["accent"], 12, 34)
    P.text(540, 820, "LONG, LIGHT, VERY THIN", FX[58], th["accent"])
    P.rrect(150, 120, 930, 200, 40, fill=(0, 0, 0, 140))
    P.text(540, 160, "Tacoma Narrows Bridge, Washington", FS[40], th["text"])

def gauge(P, cx, cy, r, val, mx, t, th):
    P.arc(cx, cy, r, 180, 360, (90, 105, 125), 30)
    P.arc(cx, cy, r, 180, 180 + 180 * val / mx, th["accent"], 30)
    a = math.pi + math.pi * val / mx
    P.line([(cx, cy), (cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a))], WHITE, 12); P.circle(cx, cy, 24, fill=WHITE)

def scene_wind(P, t, sd, th):
    P.rrect(170, 120, 470, 400, 30, fill=WHITE)
    P.rect(170, 120, 470, 190, fill=(220, 70, 70)); P.text(320, 155, "NOV", FX[44], WHITE)
    P.text(320, 290, "7", FB[150], (30, 30, 40)); P.text(320, 365, "1940", FX[36], (90, 90, 100))
    v = 42 * ease((t - 0.3) / 1.6)
    gauge(P, 760, 400, 200, v, 80, t, th)
    P.text(760, 470, f"{v:.0f} mph", FB[72], th["accent"])
    rnd = random.Random(3)
    for i in range(10):
        ph = (t * 0.8 + rnd.random()) % 1; y = rnd.uniform(560, 880)
        P.line([(ph * 1200 - 200, y), (ph * 1200 - 60, y)], (200, 220, 240, int(200 * (1 - ph))), 8)
    if t > rel(4, 3):
        P.text(540, 640, "not a hurricane", FX[58], th["accent2"])

def section(P, cx, cy, ang, dy, col=DECK):
    w, h = 300, 34
    pts = [(-w, -h), (w, -h), (w, h), (-w, h)]
    ca, sa = math.cos(ang), math.sin(ang)
    P.poly([(cx + x * ca - y * sa, cy + dy + x * sa + y * ca) for x, y in pts], fill=col)
    # cars as small dots? cables to each side
    for sx in (-w, w):
        P.line([(cx + sx * ca, cy + dy + sx * sa), (cx + sx * 1.05, 150)], CABLE + (150,), 4)

def scene_motion(P, t, sd, th):
    tw = clamp((t - (rel(5, 5) + (TM[5]["end"] - TM[5]["start"]) * 0.5)) / 1.0)
    dy = (1 - tw) * 60 * math.sin(t * 4)
    ang = tw * math.radians(20) * math.sin(t * 2.4)
    section(P, 540, 520, ang, dy)
    P.text(540, 820, "UP & DOWN..." if tw < 0.5 else "...THEN TWIST", FB[60], th["accent"])
    P.text(540, 900, "(looking down the road)", FS[34], th["accent2"])

def scene_tilt(P, t, sd, th):
    a = math.radians(45) * math.sin(t * 2.2) * ease(t / 1.2)
    section(P, 540, 520, a, 0)
    P.line([(180, 520), (900, 520)], (255, 255, 255, 90), 4)
    P.text(540, 820, f"{abs(math.degrees(a)):.0f}°", FB[96], th["accent"])

def scene_vortex(P, t, sd, th):
    grow = 0.25 + 0.75 * ease(t / sd)
    a = math.radians(40) * grow * math.sin(t * 2.4)
    section(P, 640, 520, a, 0)
    for i in range(6):
        ph = (t * 0.6 + i / 6) % 1
        x = 360 + ph * 700 + 300; y = 520 + (90 if i % 2 else -90)
        r = 30 + 20 * ph
        P.arc(lerp(380, 1040, ph), y, r, (t * 300 + i * 60) % 360, (t * 300 + i * 60) % 360 + 270, (200, 225, 250, int(230 * (1 - ph))), 7)
    for y in (420, 520, 620):
        P.arrow(60, y, 260, y, th["accent2"], 10, 30)
    P.text(540, 820, "bigger... and bigger", FX[58], th["accent"])

def scene_fall(P, t, sd, th):
    fall = clamp((t - 0.6) / 1.4)
    side_bridge(P, t, amp=18 * (1 - fall), gap=(380, 700), fall=fall)
    P.rrect(330, 110, 750, 200, 45, fill=(220, 70, 70))
    P.text(540, 155, "11:02 A.M.", FB[60], WHITE)

def scene_lesson(P, t, sd, th):
    k = back(t / 0.5)
    P.circle(540, 470, 230 * clamp(k, 0, 1.15), fill=th["accent"])
    if k > 0.5:
        P.text(540, 430, "LESSON", FB[96], (30, 30, 40))
        P.text(540, 530, "LEARNED", FB[96], (30, 30, 40))

def scene_tunnel(P, t, sd, th):
    P.rrect(90, 250, 990, 700, 40, fill=(30, 40, 55), outline=(150, 170, 190), width=8)
    # fan
    for k in range(4):
        a = t * 12 + k * math.pi / 2
        P.poly([(170, 475), (170 + 70 * math.cos(a - 0.3), 475 + 70 * math.sin(a - 0.3)), (170 + 70 * math.cos(a + 0.3), 475 + 70 * math.sin(a + 0.3))], fill=(150, 170, 190))
    P.circle(170, 475, 16, fill=WHITE)
    for i in range(6):
        y = 320 + i * 60; ph = (t * 0.8 + i * 0.17) % 1
        x0 = 260 + ph * 600
        P.line([(x0, y), (x0 + 120, y + 10 * math.sin(t * 3 + i))], (150, 205, 245, int(255 * (1 - ph))), 6)
    # model bridge (steady)
    P.rect(420, 480, 860, 500, fill=DECK)
    for x in range(420, 860, 30): P.line([(x, 500), (x + 15, 530), (x + 30, 500)], STEEL, 4)
    P.rect(440, 380, 452, 560, fill=STEEL); P.rect(828, 380, 840, 560, fill=STEEL)
    P.text(540, 790, "models tested first", FX[58], th["accent2"])

def scene_end(P, t, sd, th):
    side_bridge(P, t, amp=0, truss=True)
    k = back((t - 0.3) / 0.5)
    if t > 0.3:
        P.circle(540, 160, 70 * clamp(k, 0, 1.2), fill=(80, 210, 140)); P.line([(505, 160), (530, 188), (580, 132)], WHITE, 14)

SCENES = [
    dict(s=0, title="THE DANCING BRIDGE", fn=scene_hook),
    dict(s=2, title="BUILT TOO THIN", fn=scene_thin),
    dict(s=3, title="JUST A STRONG WIND", fn=scene_wind),
    dict(s=5, title="THEN IT TWISTED", fn=scene_motion),
    dict(s=6, title="UP TO 45 DEGREES", fn=scene_tilt),
    dict(s=7, title="THE WIND KEPT PUSHING", fn=scene_vortex, title_color=(150, 205, 245)),
    dict(s=8, title="COLLAPSE", fn=scene_fall, title_color=(255, 110, 110)),
    dict(s=9, title="EVERYONE ESCAPED", fn=scene_lesson),
    dict(s=10, title="WIND TUNNEL TESTS", fn=scene_tunnel),
    dict(s=11, title="STIFF = STEADY", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = TM
        pts = [3, tm[2]["start"] + 1.5, tm[3]["start"] + 2.2, tm[5]["start"] + 3.2, tm[6]["start"] + 2, tm[7]["start"] + 4, tm[8]["start"] + 3.5, tm[10]["start"] + 2]
        render("bridge", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/br", preview=pts)
    else:
        render("bridge", SCENES, T, "/home/claude/shorts/bridge.mp4")
