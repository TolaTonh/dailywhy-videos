"""16:9 long-form, full-screen photo style. Usage: render2.py <f0> <f1> <out.mp4> | render2.py preview t1 t2 ..."""
import sys, json, math, subprocess
sys.path.insert(0, "/home/claude/shorts")
from engine import FB, FX, FS, ease, back, clamp, mix, wrap, caption_chunks
from PIL import Image, ImageDraw, ImageEnhance
W, H, FPS = 1920, 1080, 30
ACC, RED, GREEN, WHITE, BG = (255, 196, 70), (255, 110, 95), (110, 230, 150), (245, 247, 250), (10, 16, 30)
D = "/home/claude/shorts/long3/"; PH = "/home/claude/shorts/photos/px_%s.jpg"
S = json.load(open(D + "script.json")); TM = json.load(open(D + "long3_timing.json")); SENTS = TM["sentences"]; DUR = TM["duration"]
CHS = {c["key"]: c for c in S["chapters"]}; ORDER = [c["key"] for c in S["chapters"]]
STORY = [k for k in ORDER if CHS[k]["year"]]
PHOTOS = {
 "intro": "1098745 4061487 31113084 10963854 3271942 6861359",
 "white": "2019833 33366061 4432054 5627575 11989285 9015526 1493756",
 "left": "3069147 952872 18518264 36410538 12639108 11795378",
 "row13": "15873638 4637961 11989285 4280698 4606720 4061487",
 "shades": "3271942 19098682 635052 210199 1828940 10839046",
 "lights": "10963854 3768652 12159813 19121739 5383225 6861359",
 "floor": "4606720 3119983 10963854 4280698 5383225 3119979",
 "ashtray": "31113084 764883 13722624 8920674 247040 8048552",
 "ears": "13794463 2868978 31922532 1828940 35486426 11989285 5233240",
 "food": "1640769 7443738 4061487 459402 7801106 5946664",
 "wings": "731217 5071151 20640861 32155436 1493756 10512949",
 "trails": "11593192 164646 22819806 10112536 12850 1831265",
 "height": "7443738 4053019 8210858 4618040 6861359 12720523",
 "repeat": "3099043 3768652 4280698 101522 36410538 29637932",
 "blast": "20179536 459402 35456916 7276734 3876430 5800210",
 "ninety": "5383225 3119983 10963854 4637961 5233240 4606720",
 "outro": "3271942 2019833 15873638 31113084 1098745 7443738",
}
OVER = {
 ("white", 3): [(430, "1,200 LB", ACC, 240), (640, "OF PAINT = 8 PASSENGERS", WHITE, 72)],
 ("left", 1): [(560, "PORT SIDE = LEFT", ACC, 120)],
 ("row13", 3): [(390, "XVII", ACC, 200), (640, "VIXI", RED, 200)],
 ("lights", 1): [(430, "47%", RED, 300), (640, "OF FATAL ACCIDENTS", WHITE, 80)],
 ("floor", 2): [(430, "23", RED, 300), (640, "DID NOT GET OUT", WHITE, 84)],
 ("ashtray", 1): [(470, "1973", ACC, 280), (680, "BANNED IN TOILETS", WHITE, 84)],
 ("food", 2): [(430, "-30%", RED, 300), (640, "SALTY + SWEET", WHITE, 84)],
 ("wings", 2): [(430, "1.5x", ACC, 300), (640, "THE WORST LOAD", WHITE, 84)],
 ("wings", 3): [(430, "25 FEET", RED, 240), (640, "787 WING TEST, 2010", WHITE, 76)],
 ("trails", 1): [(470, "-35 DEGREES", RED, 170), (660, "OR COLDER", WHITE, 84)],
 ("height", 0): [(560, "35,000 FT", ACC, 190)],
 ("repeat", 1): [(430, "583", RED, 300), (640, "TENERIFE, 1977", WHITE, 84)],
 ("blast", 2): [(430, "120 MPH", RED, 240), (640, "200 FEET BEHIND", WHITE, 84)],
 ("ninety", 1): [(430, "90", ACC, 320), (660, "SECONDS TO GET OUT", WHITE, 80)],
}
# ---- build shot list: (start, end, photo, chapter, local, zoom_in) ----
SHOTS = []; CARDT = {}
for ck in ORDER:
    ss = [x for x in SENTS if x["chapter"] == ck]; ph = PHOTOS[ck].split(); pi = 0
    for j, x in enumerate(ss):
        t0 = x["start"] - 0.15; nxt = ss[j + 1]["start"] - 0.15 if j + 1 < len(ss) else None
        if nxt is None:
            k = ORDER.index(ck); nxt = ([y for y in SENTS if y["chapter"] == ORDER[k + 1]][0]["start"] - 1.3) if k + 1 < len(ORDER) else DUR
        n = 2 if (nxt - t0) > 6.5 and (ck, j) not in OVER else 1
        for q in range(n):
            a = t0 + (nxt - t0) * q / n; b = t0 + (nxt - t0) * (q + 1) / n
            SHOTS.append((a, b, ph[pi % len(ph)], ck, j, len(SHOTS) % 2 == 0)); pi += 1
    if CHS[ck]["year"]: CARDT[ck] = ss[0]["start"] - 1.3
SHOTS[0] = (0.0,) + SHOTS[0][1:]
import copy
DISP = copy.deepcopy(SENTS)
for x in DISP:
    for a_, b_ in (("D C seven", "DC-7"), ("D C nine", "DC-9"), ("F A A", "FAA"), ("seven oh seven", "707"), ("seven three seven", "737")): x["text"] = x["text"].replace(a_, b_)
CHUNKS = caption_chunks(DISP, maxwords=8)
_c = {}
def load(pid):
    if pid not in _c:
        im = Image.open(PH % pid).convert("RGB"); im.thumbnail((2400, 2400)); _c[pid] = im
        if len(_c) > 6: _c.pop(next(iter(_c)))
    return _c[pid]
GR = Image.new("RGBA", (W, H), (0, 0, 0, 255)); g = Image.new("L", (1, H))
for y in range(H): g.putpixel((0, y), int(min(255, max(0, 1 - y / 300) ** 1.4 * 170 + max(0, (y - 620) / 460) ** 1.2 * 225)))
GR.putalpha(g.resize((W, H)))
def photo(pid, p, zin, dim=0.15):
    src = load(pid); sw, sh = src.size; ar = W / H
    cw, ch = (sw, sw / ar) if sw / sh < ar else (sh * ar, sh)
    z = 1.0 + 0.10 * (p if zin else 1 - p); cw, ch = cw / z, ch / z
    cx, cy = sw / 2, sh * (0.45 if sh > sw else 0.5); cy = min(max(cy, ch / 2), sh - ch / 2)
    im = src.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    return ImageEnhance.Brightness(im).enhance(1 - dim).convert("RGBA")
def stext(d, x, y, s, f, col, sw=8): d.text((x, y), s, font=f, fill=col, anchor="mm", stroke_width=sw, stroke_fill=(0, 0, 0))
def fsz(sz, k=1.0): return FB[150].font_variant(size=max(8, int(sz * k)))
def frame(t):
    si = max(i for i, s_ in enumerate(SHOTS) if s_[0] <= t); a, b, pid, ck, j, zin = SHOTS[si]
    card = None
    for k_, ct in CARDT.items():
        if ct <= t < ct + 2.6: card = (k_, t - ct)
    over = OVER.get((ck, j)); sent = [x for x in SENTS if x["chapter"] == ck and x["local"] == j][0]
    lesson = sent["text"].startswith("Lesson")
    if card: pid = PHOTOS[card[0]].split()[0]
    im = photo(pid, clamp((t - a) / max(b - a, 0.1)), zin, 0.55 if (card or lesson) else (0.4 if over else 0.15))
    im.alpha_composite(GR); d = ImageDraw.Draw(im)
    if card:
        k_, tc = card; c = CHS[k_]; n = STORY.index(k_) + 1; p = clamp(back(tc / 0.45), 0.05, 1.1)
        stext(d, W / 2, 300, f"STRANGE THING {n} OF 15", FX[58], WHITE, 5)
        stext(d, W / 2, 500, c["year"], fsz(300, p), ACC, 14)
        if tc > 0.5: stext(d, W / 2, 720, c["card"], fsz(96, clamp(back((tc - 0.5) / 0.35), 0.05, 1.08)), RED, 10)
    elif lesson:
        ts = t - sent["start"]; head, body = sent["text"].split(". ", 1); p = clamp(back(ts / 0.4), 0.05, 1.1)
        bw = d.textlength(head.upper(), font=fsz(84)) + 90
        d.rounded_rectangle([W / 2 - bw / 2, 330, W / 2 + bw / 2, 460], radius=60, fill=ACC)
        d.text((W / 2, 395), head.upper(), font=fsz(84), fill=(20, 20, 25), anchor="mm")
        if ts > 1.0:
            lines = wrap(body.upper(), fsz(96), 1600, d)
            for li, ln in enumerate(lines): stext(d, W / 2, 600 + li * 115, " ".join(ln), fsz(96, clamp(back((ts - 1.0) / 0.35), 0.05, 1.06)), WHITE, 10)
    elif over:
        ts = t - sent["start"]
        for oi, (y, text, col, size) in enumerate(over):
            dl = 0.5 + oi * 0.5
            if ts > dl: stext(d, W / 2, y, text, fsz(size, clamp(back((ts - dl) / 0.3), 0.05, 1.08)), col, 12)
    # badge, chapter, progress
    d.rounded_rectangle([40, 36, 40 + d.textlength("DAILY WHY", font=FX[36]) + 40, 92], radius=28, fill=(0, 0, 0))
    d.text((60, 64), "DAILY", font=FX[36], fill=WHITE, anchor="lm"); d.text((60 + d.textlength("DAILY ", font=FX[36]), 64), "WHY", font=FX[36], fill=ACC, anchor="lm")
    if not card:
        nm = CHS[ck]["name"].upper(); cw_ = d.textlength(nm, font=FX[36]) + 50
        d.rounded_rectangle([W - 40 - cw_, 36, W - 40, 92], radius=28, fill=(0, 0, 0)); d.text((W - 40 - cw_ / 2, 64), nm, font=FX[36], fill=ACC, anchor="mm")
    d.rectangle([0, H - 8, W, H], fill=(0, 0, 0)); d.rectangle([0, H - 8, int(W * t / DUR), H], fill=ACC)
    cur = [c for c in CHUNKS if c["start"] - 0.05 <= t < c["hold"]]
    if cur and not card:
        c = cur[-1]; f_ = FX[58].font_variant(size=50); words = [w_ for w_, _, _ in c["words"]]
        lines = wrap(" ".join(words), f_, 1500, d); lh = 66; ytop = 950 - (len(lines) - 1) * lh / 2
        boxw = max(d.textlength(" ".join(l), font=f_) for l in lines) + 60
        d.rounded_rectangle([W / 2 - boxw / 2, ytop - 46, W / 2 + boxw / 2, ytop + (len(lines) - 1) * lh + 46], radius=24, fill=(0, 0, 0))
        wi = 0
        for li, ln in enumerate(lines):
            lw = d.textlength(" ".join(ln), font=f_); x = W / 2 - lw / 2; y = ytop + li * lh
            for w_ in ln:
                _, ws, we = c["words"][wi]; wi += 1
                col = ACC if ws <= t < we + 0.08 else (WHITE if t >= ws else (150, 152, 158))
                d.text((x, y), w_, font=f_, fill=col, anchor="lm"); x += d.textlength(w_ + " ", font=f_)
    return im.convert("RGB")
if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for ts in sys.argv[2:]:
            frame(float(ts)).resize((640, 360)).save(f"/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/L3_{int(float(ts)*10):05d}.jpg")
    elif sys.argv[1] == "info":
        print(len(SHOTS), "shots", round(DUR / len(SHOTS), 1), "s avg"); print(CARDT)
    else:
        f0, f1, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(f0, f1): ff.stdin.write(frame(fi / FPS).tobytes())
        ff.stdin.close(); ff.wait()
