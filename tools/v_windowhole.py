import sys, math, random
sys.path.insert(0, "/home/claude/shorts")
from engine import *

T = dict(bg1=(22, 48, 96), bg2=(8, 18, 42), accent=(255, 176, 32), accent2=(130, 205, 255), text=(245, 247, 250))
TM = json.load(open("/home/claude/shorts/windowhole_timing.json"))["sentences"]
def rel(i, base): return TM[i]["start"] - TM[base]["start"] + 0.12
FRAME, SKY, SKY2, WHITE, PANE = (232, 236, 242), (120, 190, 245), (190, 225, 255), (255, 255, 255), (170, 215, 255)

def window(P, cx, cy, w, h, t, hole=True, hole_r=7):
    P.rrect(cx - w / 2 - 60, cy - h / 2 - 60, cx + w / 2 + 60, cy + h / 2 + 60, min(w, h) * 0.5, fill=FRAME)
    P.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, min(w, h) * 0.42, fill=SKY)
    for i in range(3):
        x = cx - w / 2 + ((t * 60 + i * 170) % (w + 200)) - 100
        y = cy - h / 4 + i * h / 4
        if cx - w / 2 + 40 < x < cx + w / 2 - 40:
            for dx, r in ((-30, 30), (0, 40), (30, 30)):
                P.circle(x + dx, y, r, fill=SKY2)
    if hole:
        P.circle(cx, cy + h / 2 - 50, hole_r, fill=(40, 60, 90))

def scene_look(P, t, sd, th):
    z = 1 + 0.12 * ease(t / sd)
    window(P, 540, 480, 380 * z, 520 * z, t)
    hy = 480 + 520 * z / 2 - 50
    k = clamp((t - rel(1, 0)) / 0.5)
    if k > 0:
        P.circle(540, hy, 110 * back(k), outline=th["accent"], width=12)
        P.line([(540 + 78 * back(k), hy + 78 * back(k)), (540 + 150 * k, hy + 150 * k)], th["accent"], 18)
        P.text(540, 880, "a tiny hole", FX[58], th["accent"])

def scene_ok(P, t, sd, th):
    window(P, 540, 480, 380, 520, t)
    k = back(t / 0.5)
    P.circle(760, 260, 110 * k, fill=(80, 210, 140))
    if k > 0.6: P.line([(705, 260), (745, 300), (815, 220)], WHITE, 22)

def panes(P, gap, labels, t, th, hole_glow=0.0, flow=False, force=0.0):
    # side cross-section: cabin on the left, outside on the right
    xs = [540 - gap, 540, 540 + gap]  # inner, middle, outer
    widths = [18, 26, 46]
    names = ["INNER", "MIDDLE", "OUTER"]
    cols = [(200, 225, 250), PANE, (120, 190, 255)]
    P.text(130, 140, "CABIN", FX[44], th["text"]); P.text(950, 140, "OUTSIDE", FX[44], th["accent2"])
    for i, x in enumerate(xs):
        w = widths[i]
        if i == 1:  # middle pane with hole
            P.rrect(x - w / 2, 200, x + w / 2, 640, 10, fill=cols[i]); P.rrect(x - w / 2, 690, x + w / 2, 780, 10, fill=cols[i])
            if hole_glow > 0: P.circle(x, 665, 40 * hole_glow, outline=th["accent"], width=8)
        else:
            P.rrect(x - w / 2, 200, x + w / 2, 780, 10, fill=cols[i])
        if labels[i] > 0:
            a = int(255 * clamp(labels[i]))
            P.text(x, 850, names[i], FX[44], (th["accent"] if i == 2 else th["text"]) + (a,))
    if flow:
        for j in range(8):
            ph = (t * 0.5 + j / 8) % 1
            x = lerp(xs[0] + 30, xs[2] - 40, ph); y = 665 + math.sin(ph * 6.28 + j) * (60 if abs(x - xs[1]) > 40 else 4)
            P.circle(x, y, 11, fill=(255, 255, 255, 220))
    if force > 0:
        for k_, y in enumerate((280, 420, 560, 720)):
            off = math.sin(t * 6 + k_) * 10
            P.arrow(xs[2] - 230 + off, y, xs[2] - 40 + off, y, th["accent"], 14, 40) if False else None
        for k_, y in enumerate((300, 480, 660)):
            off = math.sin(t * 6 + k_) * 10
            P.arrow(xs[2] - 150 + off, y, xs[2] - 32, y, th["accent"] + (int(255 * force),), 16, 42)

def scene_layers(P, t, sd, th):
    gap = lerp(0, 230, ease(t / 1.2))
    labels = [clamp((t - 1.0) / 0.4) * 0.6, clamp((t - rel(5, 3)) / 0.4), clamp((t - rel(4, 3)) / 0.4)]
    panes(P, max(gap, 1), labels, t, th)

def scene_hole(P, t, sd, th):
    glow = 0.8 + 0.2 * math.sin(t * 6)
    panes(P, 230, [0.6, 1, 1], t, th, hole_glow=glow, flow=t > rel(7, 6) - 0.3)
    P.rrect(220, 920 - 70, 860, 920, 34, fill=(0, 0, 0, 0)) if False else None

def scene_force(P, t, sd, th):
    panes(P, 230, [0.6, 1, 1], t, th, force=ease(t / 0.6))
    k = clamp((t - 1.6) / 0.5)
    if k > 0:
        P.rrect(330, 70, 750 + 0, 130, 30, fill=(80, 210, 140, int(230 * k)))
        P.text(540, 100, "BACKUP READY", FX[36], WHITE + (int(255 * k),))

def gauge(P, x, val, mx, lab, col, t, th):
    k = ease(t / 1.2)
    P.rrect(x - 110, 240, x + 110, 780, 40, fill=(255, 255, 255, 30))
    h = 520 * (val / mx) * k
    P.rrect(x - 90, 770 - h, x + 90, 770, 30, fill=col)
    P.text(x, 220 - 10, f"{val * k:.1f} psi", FB[60], col)
    P.text(x, 840, lab, FX[44], th["text"])

def scene_pressure(P, t, sd, th):
    gauge(P, 330, 11.0, 12, "CABIN", th["accent"], t, th)
    gauge(P, 750, 3.4, 12, "OUTSIDE", th["accent2"], t, th)
    P.text(540, 120, "at about 35,000 feet", FS[40], th["text"])

def scene_end(P, t, sd, th):
    window(P, 420, 470, 260, 360, t, hole=False)
    k = back((t - 0.3) / 0.5)
    P.circle(760, 470, 150 * clamp(k, 0, 1.2), fill=th["accent"])
    if k > 0.5: P.text(760, 470, "2", FB[150], (20, 40, 80))
    P.text(540, 830, "Part 1: why windows are round", FX[44], th["accent2"])

SCENES = [
    dict(s=0, title="LOOK CLOSER", fn=scene_look),
    dict(s=2, title="IT'S ON PURPOSE", fn=scene_ok),
    dict(s=3, title="3 LAYERS OF WINDOW", fn=scene_layers),
    dict(s=6, title="THE BREATHER HOLE", fn=scene_hole),
    dict(s=8, title="OUTER PANE TAKES IT", fn=scene_force),
    dict(s=9, title="ABOUT 1/3 THE PRESSURE", fn=scene_pressure, title_color=(130, 205, 255)),
    dict(s=10, title="AIRPLANE WINDOWS, PART 2", fn=scene_end),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tm = TM
        pts = [1.0, tm[1]["start"] + 1, tm[2]["start"] + 1, tm[5]["start"] + 1.5, tm[7]["start"] + 1.5, tm[8]["start"] + 3, tm[9]["start"] + 3, tm[10]["start"] + 3]
        render("windowhole", SCENES, T, "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/wh", preview=pts)
    else:
        render("windowhole", SCENES, T, "/home/claude/shorts/windowhole.mp4")
