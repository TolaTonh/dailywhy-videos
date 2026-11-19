"""16:9 long-form, full-screen photo style. Usage: render2.py <f0> <f1> <out.mp4> | render2.py preview t1 t2 ..."""
import sys, json, math, subprocess
sys.path.insert(0, "/home/claude/shorts")
from engine import FB, FX, FS, ease, back, clamp, mix, wrap, caption_chunks
from PIL import Image, ImageDraw, ImageEnhance
W, H, FPS = 1920, 1080, 30
ACC, RED, GREEN, WHITE, BG = (255, 196, 70), (255, 110, 95), (110, 230, 150), (245, 247, 250), (10, 16, 30)
D = "/home/claude/shorts/long8/"; PH = "/home/claude/shorts/photos/px_%s.jpg"
S = json.load(open(D + "script.json")); TM = json.load(open(D + "long8_timing.json")); SENTS = TM["sentences"]; DUR = TM["duration"]
CHS = {c["key"]: c for c in S["chapters"]}; ORDER = [c["key"] for c in S["chapters"]]
STORY = [k for k in ORDER if CHS[k]["year"]]
PHOTOS = {
 "intro": "27015975 1493756 4618040 12159813 27015975 31922532",
 "dream": "6894105 3862628 6614747 27015975 1815388 4618040",
 "cost": "6614747 6894105 20640861 8689333 3862628 9291217 20640861 6728549",
 "orders": "4053019 3939833 1098745 2315265 27046715 12257586 20640861 6614747",
 "boom": "16137173 1493756 4618040 12159813 19121739 3608311 34407923 10005973",
 "flying": "27015975 31922532 4618040 1493756 19098682 4637961 3119983",
 "numbers": "5262815 2315265 459402 6614747 3862628 20640861 8689333",
 "crash": "3768652 6494669 19121739 12341575 9313773 16071107 3862628",
 "last": "12159813 19121739 4053019 20640861 1098745 31922532 3271942",
 "lessons": "6894105 27015975 1493756 3862628 6614747 4618040 731217",
 "outro": "27015975 20640861 1493756 3271942",
}
OVER = {
 ("dream", 6): [(470, "FIRST FLIGHT: 1969", ACC, 170)],
 ("cost", 5): [(430, "\u00a370 MILLION", ACC, 200), (640, "FIRST ESTIMATE", WHITE, 90)],
 ("cost", 6): [(430, "\u00a31.3 BILLION+", RED, 200), (640, "FINAL COST", WHITE, 90)],
 ("orders", 0): [(430, "70+ ORDERS", ACC, 220), (650, "16 AIRLINES", WHITE, 110)],
 ("orders", 2): [(470, "1973 OIL CRISIS", RED, 190)],
 ("orders", 7): [(430, "20 BUILT", ACC, 260), (650, "14 IN SERVICE", WHITE, 110)],
 ("boom", 2): [(470, "16-MILE-WIDE BOOM", RED, 160)],
 ("boom", 6): [(430, "~4,500 MILES", ACC, 220), (650, "RANGE", WHITE, 110)],
 ("flying", 2): [(430, "MACH 2", ACC, 280), (650, "60,000 FT", WHITE, 120)],
 ("flying", 4): [(470, "~3.5 HOURS", ACC, 240)],
 ("flying", 6): [(430, "~$10,000", ACC, 260), (650, "ROUND TRIP", WHITE, 110)],
 ("numbers", 1): [(410, "6,700 GAL/H", RED, 190), (620, "747: 3,600", WHITE, 130)],
 ("numbers", 3): [(410, "16 VS 46", ACC, 220), (630, "PASSENGER-MILES PER GALLON", WHITE, 72)],
 ("numbers", 5): [(430, "18 HOURS", RED, 240), (650, "WORK PER FLIGHT HOUR", WHITE, 84)],
 ("crash", 3): [(430, "113", RED, 320), (660, "LIVES LOST", WHITE, 96)],
 ("last", 5): [(430, "24 OCT 2003", ACC, 220), (650, "LAST COMMERCIAL FLIGHT", WHITE, 84)],
}
_P = dict(kind="Magazine article", source="Popular Science", title="Behind the supersonic rise and fall of the Concorde")
SRC = {
 ("lessons", 3): dict(_P, fact=["Prowess first, economics second"]),
 ("numbers", 2): dict(kind="Article", source="Controllable Delay", title="Why Concorde Failed", fact=["Concorde: 15.8 passenger-miles per gallon. 747: 46.4"]),
}
# ---- build shot list: (start, end, photo, chapter, local, zoom_in) ----
SHOTS = []; CARDT = {}
for ck in ORDER:
    ss = [x for x in SENTS if x["chapter"] == ck]; ph = PHOTOS[ck].split(); pi = 0
    for j, x in enumerate(ss):
        t0 = x["start"] - 0.15; nxt = ss[j + 1]["start"] - 0.15 if j + 1 < len(ss) else None
        if nxt is None:
            k = ORDER.index(ck); nxt = ([y for y in SENTS if y["chapter"] == ORDER[k + 1]][0]["start"] - 1.3) if k + 1 < len(ORDER) else DUR
        n = 2 if (nxt - t0) > 6.5 and (ck, j) not in OVER and (ck, j) not in SRC else 1
        for q in range(n):
            a = t0 + (nxt - t0) * q / n; b = t0 + (nxt - t0) * (q + 1) / n
            SHOTS.append((a, b, ph[pi % len(ph)], ck, j, len(SHOTS) % 2 == 0)); pi += 1
    if CHS[ck]["year"]: CARDT[ck] = ss[0]["start"] - 1.3
SHOTS[0] = (0.0,) + SHOTS[0][1:]
import sys as _s; _s.path.insert(0, '/home/claude/shorts')
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
    srcs = SRC.get((ck, j))
    if srcs and not card:
        import doccard2 as DC
        im = DC.frame(max(0.0, t - a), dict(srcs, photo=pid), (W, H), "dark", max(b - a, 1.0), u=1.12).convert("RGBA")
    im.alpha_composite(GR); d = ImageDraw.Draw(im)
    if card:
        k_, tc = card; c = CHS[k_]; n = STORY.index(k_) + 1; p = clamp(back(tc / 0.45), 0.05, 1.1)
        stext(d, W / 2, 300, f"CHAPTER {n} OF 9", FX[58], WHITE, 5)
        stext(d, W / 2, 500, c["year"], fsz(300 if len(c["year"]) <= 5 else 210 if len(c["year"]) <= 9 else 170, p), ACC, 14)
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
