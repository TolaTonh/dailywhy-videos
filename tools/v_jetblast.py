"""Why is jet blast so dangerous? — trend Short (Nov 2026 news), engine v2, blueprint style."""
import sys, math, json, random
sys.path.insert(0, "/home/claude/shorts")
from engine import FX, FS, FB, clamp, ease, back, lerp
import blueprint as B
import engine2

KEY = "jetblast"
T = dict(B.THEME); LINE, RED, DIM, ACC, GREEN = B.LINE, B.RED, B.DIM, T["accent"], (110, 230, 150)

def jet(P, x, y, s, col=LINE):
    """Side view, nose left; exhaust leaves to the right at (x + 95s, y + 85s)."""
    P.rrect(x - 260 * s, y - 36 * s, x + 240 * s, y + 36 * s, 36 * s, outline=col, width=6)
    P.line([(x + 170 * s, y - 36 * s), (x + 250 * s, y - 150 * s), (x + 290 * s, y - 150 * s), (x + 240 * s, y - 30 * s)], col, 6)
    P.line([(x - 40 * s, y + 30 * s), (x + 70 * s, y + 70 * s)], col, 5)
    P.rrect(x - 30 * s, y + 60 * s, x + 95 * s, y + 110 * s, 22 * s, outline=col, width=5)
    for i in range(7): P.circle(x - 190 * s + i * 45 * s, y - 8 * s, 6 * s, fill=col)
    return (x + 95 * s, y + 85 * s)

def small_plane(P, x, y, s, ang, col=ACC):
    a = math.radians(ang); c, sn = math.cos(a), math.sin(a)
    R = lambda px, py: (x + px * s * c - py * s * sn, y + px * s * sn + py * s * c)
    P.line([R(-80, 0), R(70, 0)], col, 14 * s)
    P.line([R(-30, -22), R(40, -22)], col, 8 * s); P.line([R(5, -22), R(5, 0)], col, 5 * s)
    P.line([R(60, 0), R(85, -40)], col, 8 * s)
    P.line([R(-88, -24), R(-88, 24)], col, 5 * s)
    for wx in (-40, 20): P.circle(*R(wx, 26), 9 * s, fill=col)

def streaks(P, x0, y0, x1, t, n=9, spread=70, col=RED, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        ph = (t * 1.6 + rnd.random()) % 1; yy = y0 + rnd.uniform(-spread, spread) * (0.3 + 0.7 * ph)
        xa = lerp(x0, x1, ph); L = 70 + 60 * rnd.random()
        P.line([(xa, yy), (min(x1, xa + L), yy)], col + (int(230 * (1 - ph * 0.7)),), 6)

def s_hook(P, t, sd, th):
    ex, ey = jet(P, 380, 400, 1.15)
    streaks(P, ex, ey, 1040, t, n=13, spread=110)
    small_plane(P, 800, 720, 1.6, 38 + 6 * math.sin(t * 5))
    P.line([(520, 820), (1040, 820)], LINE, 5)

def s_engine(P, t, sd, th):
    k = ease(t / 0.8)
    B.path(P, [(240, 380), (840, 420), (840, 560), (240, 600), (240, 380)], k, LINE, 7)
    for i in range(5):
        y = 400 + i * 45; B.path(P, [(300, y), (330, y + 12)], k, DIM, 5)
    for i in range(3):
        ph = (t * 0.8 + i / 3) % 1; y = 440 + i * 50
        P.arrow(40 + ph * 120, y, 130 + ph * 120, y, DIM + (int(255 * (1 - ph)),), 8, 24)
    streaks(P, 850, 490, 1060, t, n=8, spread=60, seed=4)
    B.label(P, 150, 300, "AIR IN", DIM); B.label(P, 870, 300, "AIR OUT, FAST", RED)

def s_speed(P, t, sd, th):
    B.label(P, 540, 250, "AT JUST 40% POWER", LINE)
    P.rrect(190, 310, 890, 370, 30, outline=LINE, width=5)
    P.rrect(196, 316, 196 + 688 * 0.4 * ease(t / 1.0), 364, 26, fill=ACC)
    v = int(120 * ease((t - 2.2) / 1.2))
    if t > 2.2:
        B.label(P, 540, 570, f"{v}", RED, FB[150].font_variant(size=230)); B.label(P, 540, 730, "MPH", RED, FB[72])

def s_distance(P, t, sd, th):
    ex, ey = jet(P, 210, 430, 0.5)
    streaks(P, ex, ey, 960, t, n=10, spread=70, seed=7)
    k = ease(t / 1.0)
    B.dim(P, ex, 620, ex + (940 - ex) * k, 620, "200 FT", 1.0 if k > 0.98 else 0.99, DIM, off=50)
    if k > 0.98: small_plane(P, 940, 470, 0.55, 0, ACC)

def s_hurricane(P, t, sd, th):
    for k in range(5):
        a0 = (t * 220 + k * 72) % 360
        P.arc(540, 480, 90 + k * 55, a0, a0 + 230, RED + (230 - k * 30,), 14)
    P.circle(540, 480, 30, fill=T["bg1"])
    p = back(t / 0.4)
    B.label(P, 540, 850, "HURRICANE FORCE", RED, FB[84].font_variant(size=int(84 * clamp(p, 0.05, 1.1))))

def s_nasa(P, t, sd, th):
    k = ease(t / 1.2)
    B.label(P, 540, 330, f"{int(85 * k)}%", ACC, FB[150].font_variant(size=230))
    B.label(P, 540, 500, "of jet-blast damage hits other aircraft", LINE)
    if t > 3.2:
        small_plane(P, 540, 660, 0.9, 0); B.label(P, 540, 760, "MOSTLY UNDER 5,000 LB", ACC)
    B.label(P, 540, 880, "NASA ASRS study of 51 reports", DIM, FS[34])

def s_rule(P, t, sd, th):
    ex, ey = jet(P, 300, 380, 0.6)
    k = ease(t / 0.8)
    cone = [(ex, ey - 20), (ex + 620 * k, ey - 150 * k), (ex + 620 * k, ey + 150 * k), (ex, ey + 20)]
    P.poly(cone, fill=RED + (70,)); P.line(cone + [cone[0]], RED, 5)
    if k > 0.9: B.label(P, 760, ey, "KEEP CLEAR", RED, FX[58])
    if t > 1.6:
        small_plane(P, 330, 760, 0.8, 0, GREEN)
        P.circle(540, 760, 44, fill=(80, 200, 130)); P.line([(518, 760), (534, 778), (564, 742)], (255, 255, 255), 10)
        B.label(P, 790, 760, "safe distance", GREEN)

def p_none(P, t, sd, th): pass
def p_engine(P, t, sd, th):
    k = clamp((t - 0.6) / 0.4)
    if k > 0:
        P.rrect(170, 760, 910, 860, 40, fill=(0, 0, 0, 190)); B.label(P, 540, 810, "THROWS AIR BACKWARD, FAST", RED)
def p_nasa(P, t, sd, th):
    k = ease(t / 1.2)
    B.label(P, 540, 330, f"{int(85 * k)}%", ACC, FB[150].font_variant(size=230))
    B.label(P, 540, 480, "of jet-blast damage hits other aircraft", LINE)
    if t > 3.2:
        P.rrect(240, 740, 840, 830, 40, fill=(0, 0, 0, 190)); B.label(P, 540, 785, "MOSTLY UNDER 5,000 LB", ACC)
    B.label(P, 540, 870, "NASA ASRS study of 51 reports", LINE, FS[34])
PHOTO_COVER = dict(path="/home/claude/shorts/photos/px_20179536.jpg", focus=(0.5, 0.52), zoom=(1.0, 1.12))

SCENES = [
    dict(s=0, fn=p_none, photo=PHOTO_COVER),
    dict(s=1, fn=p_engine, title="HOW A JET PUSHES", photo=dict(path="/home/claude/shorts/photos/px_459402.jpg", focus=(0.45, 0.5), zoom=(1.0, 1.15))),
    dict(s=2, fn=s_speed, title="THE WIND BEHIND IT", title_color=RED),
    dict(s=3, fn=s_distance, title="AND IT REACHES FAR"),
    dict(s=4, fn=s_hurricane, title="THAT'S...", title_color=RED),
    dict(s=5, fn=p_nasa, title="WHO GETS HIT?", photo=dict(path="/home/claude/shorts/photos/px_7276734.jpg", focus=(0.55, 0.6), zoom=(1.0, 1.1), dim=0.55)),
    dict(s=6, fn=s_rule, title="THE PILOT'S RULE", title_color=GREEN),
    dict(s=7, fn=p_none, title=None, photo=PHOTO_COVER),
]

if __name__ == "__main__":
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=B.background(12), hook_lines=["KNOCKED OVER", "BY A JET?"], mood="tense", title_block=B.title_block("DAILY WHY · DWG 02"))
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        engine2.render(preview=[0.0, 2.5, 7.5, 10.5, 14.5, 17.5, 19.5, 23.0, 27.0, 31.5, 34.5], **args)
    else:
        engine2.render(**args)
