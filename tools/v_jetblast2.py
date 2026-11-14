"""Why is jet blast so dangerous? — default full-screen photo edit."""
import sys
sys.path.insert(0, "/home/claude/shorts")
from v_whiteplanes2 import big, none, F, ACC, RED, GREEN, WHITE, T
from engine import ease
import engine2
from PIL import Image
KEY = "jetblast2"

def o_how(P, t, sd, th):
    if t > 1.3: big(P, 760, "HOW?", ACC, 150, t - 1.3)
def o_back(P, t, sd, th):
    if t > 0.3: big(P, 760, "AIR OUT, FAST", RED, 96, t - 0.3)
def o_40(P, t, sd, th):
    big(P, 600, "40%", ACC, 230, t); big(P, 770, "POWER", WHITE, 90)
def o_120(P, t, sd, th):
    v = int(120 * ease(t / 0.9)); big(P, 580, f"{v}", RED, 260); big(P, 770, "MPH", WHITE, 100)
def o_200(P, t, sd, th):
    if t > 0.4: big(P, 620, "200 FT", ACC, 190, t - 0.4); 
    if t > 0.9: big(P, 780, "BEHIND THE JET", WHITE, 76, t - 0.9)
def o_hurr(P, t, sd, th):
    big(P, 620, "HURRICANE", RED, 150, t); 
    if t > 0.4: big(P, 780, "FORCE WIND", WHITE, 100, t - 0.4)
def o_light(P, t, sd, th):
    if t > 0.5: big(P, 760, "HITS OTHER AIRCRAFT", ACC, 76, t - 0.5)
def o_5000(P, t, sd, th):
    big(P, 620, "UNDER", WHITE, 90, t); big(P, 770, "5,000 LB", RED, 150, t)
def o_dist(P, t, sd, th):
    if t > 0.4: big(P, 760, "KEEP YOUR DISTANCE", GREEN, 78, t - 0.4)
def o_tail(P, t, sd, th):
    if t > 0.2: big(P, 760, "NEVER TAIL-FIRST", ACC, 84, t - 0.2)

COVER = F("20179536", focus=(0.5, 0.55), zoom=(1.0, 1.12))
SCENES = [
    dict(s=0, fn=none, photo=COVER),
    dict(s=0, off=2.6, fn=o_how, photo=F("7276734", focus=(0.6, 0.6), zoom=(1.12, 1.0))),
    dict(s=1, fn=none, title="HOW A JET PUSHES", photo=F("459402", focus=(0.48, 0.5), zoom=(1.0, 1.15))),
    dict(s=1, off=1.9, fn=o_back, title="HOW A JET PUSHES", hold=True, photo=F("30210231", focus=(0.5, 0.3), zoom=(1.15, 1.0))),
    dict(s=2, fn=o_40, title="THE WIND BEHIND IT", title_color=RED, photo=F("35456916", focus=(0.62, 0.5), zoom=(1.0, 1.12), dim=0.3)),
    dict(s=2, off=2.6, fn=o_120, title="THE WIND BEHIND IT", title_color=RED, hold=True, photo=F("1493756", focus=(0.66, 0.4), zoom=(1.5, 1.3), dim=0.25)),
    dict(s=3, fn=o_200, title="AND IT REACHES FAR", photo=F("32155436", focus=(0.42, 0.5), zoom=(1.0, 1.12), dim=0.25)),
    dict(s=4, fn=o_hurr, title="THAT'S...", title_color=RED, photo=F("31922532", focus=(0.5, 0.3), zoom=(1.0, 1.15), dim=0.3)),
    dict(s=5, fn=o_light, title="WHO GETS HIT?", photo=F("5800210", focus=(0.55, 0.55), zoom=(1.0, 1.14))),
    dict(s=5, off=3.2, fn=o_5000, title="WHO GETS HIT?", hold=True, photo=F("6308947", focus=(0.5, 0.45), zoom=(1.14, 1.0), dim=0.3)),
    dict(s=6, fn=o_dist, title="THE PILOT'S RULE", title_color=GREEN, photo=F("36410538", focus=(0.6, 0.5), zoom=(1.0, 1.12), dim=0.2)),
    dict(s=6, off=2.3, fn=o_tail, title="THE PILOT'S RULE", title_color=GREEN, hold=True, photo=F("3876430", focus=(0.5, 0.25), zoom=(1.3, 1.15))),
    dict(s=7, fn=none, title=None, photo=COVER),
]
if __name__ == "__main__":
    args = dict(key=KEY, scenes=SCENES, theme=T, bg_img=Image.new("RGB", (1080, 1920), T["bg1"]), hook_lines=["KNOCKED OVER", "BY A JET?"], mood="tense")
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        import json; tm = json.load(open(f"/home/claude/shorts/{KEY}_timing.json"))["sentences"]
        ts = [0.3]
        for sc in SCENES[1:-1]: ts.append(tm[sc["s"]]["start"] + sc.get("off", 0) + 1.5)
        ts.append(tm[-1]["end"] + 0.5)
        engine2.render(preview=ts, **args)
    else:
        engine2.render(**args)
