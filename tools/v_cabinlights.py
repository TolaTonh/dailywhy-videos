"""Why do planes dim the lights before landing? — default full-screen photo edit."""
import sys
sys.path.insert(0, "/home/claude/shorts")
from v_whiteplanes2 import big, none, F, ACC, RED, GREEN, WHITE, T
from engine import ease, FS
import blueprint as B
import engine2
from PIL import Image
KEY = "cabinlights"

def o_why(P, t, sd, th):
    if t > 0.5: big(P, 760, "WHY?", ACC, 150, t - 0.5)
def o_sleep(P, t, sd, th):
    big(P, 620, "NOT FOR SLEEP", WHITE, 96, t)
    if t > 1.3: big(P, 780, "IT'S FOR SAFETY", ACC, 96, t - 1.3)
def o_47(P, t, sd, th):
    v = int(47 * ease(t / 0.9)); big(P, 580, f"{v}%", RED, 260); big(P, 770, "OF FATAL ACCIDENTS", WHITE, 72)
def o_land(P, t, sd, th):
    big(P, 660, "APPROACH + LANDING", ACC, 78, t)
    B.label(P, 540, 780, "Boeing data, 2004-2013", WHITE, FS[34].font_variant(size=38))
def o_smoke(P, t, sd, th):
    if t > 0.9: big(P, 760, "DARKNESS OR SMOKE", RED, 84, t - 0.9)
def o_eyes(P, t, sd, th):
    big(P, 620, "YOUR EYES", WHITE, 110, t)
    if t > 0.7: big(P, 780, "ALREADY ADJUSTED", GREEN, 90, t - 0.7)
def o_exit(P, t, sd, th):
    if t > 0.6: big(P, 760, "EXIT SIGNS STAND OUT", GREEN, 74, t - 0.6)
def o_shade(P, t, sd, th):
    if t > 0.5: big(P, 760, "SHADES STAY OPEN", ACC, 86, t - 0.5)
def o_fire(P, t, sd, th):
    if t > 0.2: big(P, 760, "SPOT FIRE OUTSIDE", RED, 86, t - 0.2)

COVER = F("3271942", focus=(0.5, 0.45), zoom=(1.0, 1.12), dim=0.0)
SCENES = [
    dict(s=0, fn=none, photo=COVER),
    dict(s=0, off=1.8, fn=o_why, photo=F("10963854", focus=(0.5, 0.4), zoom=(1.12, 1.0), dim=0.0)),
    dict(s=1, fn=o_sleep, title="THE REAL REASON", photo=F("4606720", focus=(0.55, 0.5), zoom=(1.0, 1.12), dim=0.35)),
    dict(s=2, fn=o_47, title="THE RISKY MINUTES", title_color=RED, photo=F("3768652", focus=(0.5, 0.6), zoom=(1.0, 1.14), dim=0.3)),
    dict(s=2, off=2.5, fn=o_land, title="THE RISKY MINUTES", title_color=RED, hold=True, photo=F("6861359", focus=(0.5, 0.5), zoom=(1.14, 1.0), dim=0.25)),
    dict(s=3, fn=none, title="IF IT GOES WRONG", title_color=RED, photo=F("19098682", focus=(0.5, 0.45), zoom=(1.0, 1.12))),
    dict(s=3, off=2.0, fn=o_smoke, title="IF IT GOES WRONG", title_color=RED, hold=True, photo=F("12159813", focus=(0.5, 0.5), zoom=(1.12, 1.0))),
    dict(s=4, fn=o_eyes, title="SO THE CREW...", title_color=GREEN, photo=F("19121739", focus=(0.5, 0.6), zoom=(1.0, 1.14), dim=0.15)),
    dict(s=5, fn=o_exit, title="AND ONE MORE THING", photo=F("5383225", focus=(0.55, 0.5), zoom=(1.0, 1.12), dim=0.15)),
    dict(s=5, off=2.4, fn=none, title="AND ONE MORE THING", hold=True, photo=F("10963854", focus=(0.5, 0.75), zoom=(1.3, 1.15))),
    dict(s=6, fn=o_shade, title="WINDOW SHADES", photo=F("3271942", focus=(0.5, 0.4), zoom=(1.25, 1.1))),
    dict(s=6, off=2.8, fn=o_fire, title="WINDOW SHADES", hold=True, photo=F("210199", focus=(0.52, 0.5), zoom=(1.14, 1.0))),
    dict(s=7, fn=none, title=None, photo=COVER),
]
if __name__ == "__main__":
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=Image.new("RGB", (1080, 1920), T["bg1"]), hook_lines=["WHY DO CABIN", "LIGHTS DIM?"], mood="curious")
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        import json; tm = json.load(open(f"/home/claude/shorts/{KEY}_timing.json"))["sentences"]
        ts = [0.3]
        for sc in SCENES[1:-1]: ts.append(tm[sc["s"]]["start"] + sc.get("off", 0) + 1.6)
        ts.append(tm[-1]["end"] + 0.5)
        engine2.render(preview=ts, **args)
    else:
        engine2.render(**args)
