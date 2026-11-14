"""Why are most planes painted white? — full-screen photo edit (airplane-windows look), engine v2."""
import sys, math
sys.path.insert(0, "/home/claude/shorts")
from engine import FX, FS, FB, clamp, ease, back, lerp
import blueprint as B
import engine2

KEY = "whiteplanes2"
T = dict(bg1=(10, 16, 30), bg2=(6, 10, 20), accent=(255, 196, 70), accent2=(150, 205, 255), text=(245, 247, 250))
ACC, RED, GREEN, WHITE = T["accent"], (255, 110, 95), (110, 230, 150), (255, 255, 255)
PH = "/home/claude/shorts/photos/px_%s.jpg"
def F(pid, **kw): return dict(path=PH % pid, full=True, **kw)

def big(P, y, s, col, size=120, t=1.0):
    k = clamp(back(t / 0.3), 0.05, 1.1); f = FB[150].font_variant(size=max(8, int(size * k)))
    for dx, dy in ((-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4)): P.text(540 + dx, y + dy, s, f, (0, 0, 0))
    P.text(540, y, s, f, col)

def none(P, t, sd, th): pass
def o_heat(P, t, sd, th):
    if t > 0.5: big(P, 760, "REFLECTS THE SUN", ACC, 84, t - 0.5)
def o_cool(P, t, sd, th):
    if t > 0.2: big(P, 760, "COOLER CABIN", GREEN, 96, t - 0.2)
def o_crack(P, t, sd, th):
    k = ease((t - 0.2) / 1.0); cx, cy = lerp(300, 520, k), lerp(520, 400, k)
    P.circle(cx, cy, 130, outline=WHITE, width=12); P.line([(cx + 92, cy + 92), (cx + 185, cy + 185)], WHITE, 18)
    if t > 1.2: B.path(P, [(cx - 60, cy - 30), (cx - 25, cy - 5), (cx - 5, cy - 28), (cx + 30, cy + 8), (cx + 62, cy - 6)], (t - 1.2) / 0.35, RED, 10)
def o_spot(P, t, sd, th):
    if t > 0.2: big(P, 760, "EASY TO SPOT", RED, 96, t - 0.2)
def o_paint(P, t, sd, th):
    if t > 0.3: big(P, 760, "PAINT IS HEAVY", ACC, 92, t - 0.3)
def o_1200(P, t, sd, th):
    v = int(round(1200 * ease(t / 1.0) / 10) * 10)
    big(P, 560, f"{v:,}", ACC, 230); big(P, 740, "LB OF PAINT", WHITE, 84)
def o_eight(P, t, sd, th):
    big(P, 560, "+8", RED, 260, t)
    if t > 0.6: big(P, 760, "EXTRA PASSENGERS", WHITE, 80, t - 0.6)
def o_fuel(P, t, sd, th):
    if t > 0.3: big(P, 760, "LESS PAINT, LESS FUEL", GREEN, 74, t - 0.3)
def o_fade(P, t, sd, th):
    if t > 0.4: big(P, 760, "COLORS FADE FAST", RED, 84, t - 0.4)
def o_repaint(P, t, sd, th):
    if t > 0.2: big(P, 760, "REPAINT SOONER", ACC, 90, t - 0.2)

COVER = F("1098745", focus=(0.5, 0.5), zoom=(1.0, 1.12))
SCENES = [
    dict(s=0, fn=none, photo=COVER),
    dict(s=0, off=1.9, fn=none, photo=F("32155436", focus=(0.42, 0.5), zoom=(1.12, 1.0))),
    dict(s=1, fn=o_heat, title="1. HEAT", photo=F("33366061", focus=(0.45, 0.6), zoom=(1.0, 1.14))),
    dict(s=1, off=2.3, fn=o_cool, title="1. HEAT", hold=True, photo=F("3119983", zoom=(1.14, 1.0))),
    dict(s=2, fn=o_crack, title="2. SAFETY", photo=F("4432054", focus=(0.3, 0.6), zoom=(1.0, 1.12))),
    dict(s=2, off=2.4, fn=o_spot, title="2. SAFETY", hold=True, photo=F("5627575", focus=(0.3, 0.55), zoom=(1.12, 1.0))),
    dict(s=3, fn=o_paint, title="3. WEIGHT", photo=F("2019833", focus=(0.3, 0.5), zoom=(1.0, 1.14))),
    dict(s=3, off=2.2, fn=o_1200, title="3. WEIGHT", hold=True, photo=F("20640861", focus=(0.5, 0.6), zoom=(1.0, 1.1), dim=0.4)),
    dict(s=4, fn=o_eight, title="THAT'S LIKE...", title_color=RED, photo=F("11989285", focus=(0.6, 0.5), zoom=(1.0, 1.14), dim=0.3)),
    dict(s=5, fn=none, title="KEEP IT SIMPLE", title_color=GREEN, photo=F("1493756", focus=(0.66, 0.4), zoom=(1.3, 1.5))),
    dict(s=5, off=2.3, fn=o_fuel, title="KEEP IT SIMPLE", title_color=GREEN, hold=True, photo=F("3768654", focus=(0.3, 0.55), zoom=(1.12, 1.0))),
    dict(s=6, fn=o_fade, title="4. FADING", photo=F("9015526", focus=(0.45, 0.55), zoom=(1.0, 1.14))),
    dict(s=6, off=2.1, fn=o_repaint, title="4. FADING", hold=True, photo=F("19331901", focus=(0.6, 0.55), zoom=(1.14, 1.0))),
    dict(s=7, fn=none, title=None, photo=COVER),
]
if __name__ == "__main__":
    from PIL import Image
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=Image.new("RGB", (1080, 1920), T["bg1"]), hook_lines=["WHY ARE PLANES", "WHITE?"], mood="curious")
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        engine2.render(preview=[0.3, 2.6, 5.0, 7.0, 9.5, 11.8, 14.0, 16.5, 19.5, 22.5, 25.0, 27.5, 29.8, 32.0], **args)
    else:
        engine2.render(**args)
