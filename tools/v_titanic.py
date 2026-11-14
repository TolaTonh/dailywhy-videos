"""Titanic Short in the vintage-map + characters style."""
import sys, json, math, random, subprocess
sys.path.insert(0, "/home/claude/shorts")
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import mapstyle as M
from engine import Pen, FB, FX, FS, ease, back, clamp, lerp, mix, caption_chunks

W, H, FPS = 1080, 1920, 30
KEY = "titanic"
TM = json.load(open(f"/home/claude/shorts/{KEY}_timing.json")); SENT = TM["sentences"]; DUR = TM["duration"]
SS = 2
INK, WHITE, BLACK = (60, 45, 35), (255, 255, 255), (20, 20, 25)
ACC = (255, 196, 70)

# ---------- backgrounds ----------
def make_bg(lon, lat, kmpx, seed, hl=()):
    im, proj = M.vintage_map(lon, lat, kmpx, highlight=set(hl), seed=seed, w=int(W * 1.25), h=int(H * 1.25))
    return im, proj
BG_ATL, P_ATL = make_bg(-38, 45, 5.2, 4)          # whole North Atlantic
BG_ICE, P_ICE = make_bg(-50, 40.6, 1.2, 5)          # near Newfoundland
def plain_bg(seed, col=(214, 196, 150)):
    im = Image.new("RGB", (int(W * 1.25), int(H * 1.25)), col)
    arr = np.asarray(im).astype(np.float32) + M.paper_noise(im.width, im.height, seed)[..., None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))
BG_PAPER = plain_bg(7)
BG_SEA = plain_bg(8, (70, 120, 135))

def cam(bg, z):
    """Crop bg (1.25x oversize) to frame with zoom z in [1, 1.25]."""
    cw, ch = int(bg.width / z), int(bg.height / z)
    x0, y0 = (bg.width - cw) // 2, (bg.height - ch) // 2
    return bg.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
def bgpt(proj, z, lon, lat, bg):
    """Map lon/lat to frame coords after cam()."""
    x, y = proj(lon, lat); cw, ch = bg.width / z, bg.height / z
    return ((x - (bg.width - cw) / 2) * W / cw, (y - (bg.height - ch) / 2) * H / ch)

# ---------- drawing helpers (on 2x layer) ----------
def ship(P, x, y, s, tilt=0.0, sink=0.0):
    """Side view of the liner, bow to the right. tilt in degrees (bow down positive)."""
    a = math.radians(tilt); c, sn = math.cos(a), math.sin(a)
    def R(px, py): return (x + px * s * c - py * s * sn, y + sink + px * s * sn + py * s * c)
    hull = [(-300, -20), (300, -20), (330, -45), (320, 40), (-290, 40), (-310, -10)]
    P.poly([R(*p) for p in hull], fill=(25, 25, 30))
    P.poly([R(*p) for p in [(-300, 25), (320, 25), (318, 40), (-290, 40)]], fill=(150, 40, 40))
    P.poly([R(*p) for p in [(-250, -20), (240, -20), (240, -55), (-250, -55)]], fill=(245, 242, 232))
    P.poly([R(*p) for p in [(-200, -55), (180, -55), (180, -80), (-200, -80)]], fill=(245, 242, 232))
    for i in range(4):
        fx = -150 + i * 90
        P.poly([R(*p) for p in [(fx - 14, -80), (fx + 14, -80), (fx + 20, -150), (fx - 8, -150)]], fill=(215, 160, 80))
        P.poly([R(*p) for p in [(fx - 9, -135), (fx + 19, -135), (fx + 20, -150), (fx - 8, -150)]], fill=(25, 25, 30))
    for i in range(18):
        wx = -230 + i * 26; P.circle(*R(wx, -38), 4 * s, fill=(60, 70, 90))

def iceberg(P, x, y, s):
    P.poly([(x - 120 * s, y), (x - 60 * s, y - 130 * s), (x - 10 * s, y - 90 * s), (x + 40 * s, y - 170 * s), (x + 130 * s, y)], fill=(235, 245, 250))
    P.poly([(x + 40 * s, y - 170 * s), (x + 130 * s, y), (x + 50 * s, y)], fill=(200, 222, 235))
    P.poly([(x - 160 * s, y), (x + 170 * s, y), (x + 90 * s, y + 140 * s), (x - 110 * s, y + 120 * s)], fill=(150, 200, 220, 140))

def compartments(P, t, flooded, spill_p=0.0, tilt=0.0):
    """Cut-away hull with 16 compartments (bow on the right)."""
    x0, x1, top, bot = 70, 1010, 420, 680
    a = math.radians(tilt); cx = (x0 + x1) / 2
    def R(px, py): return (cx + (px - cx) * math.cos(a) - (py - 550) * math.sin(a), 550 + (px - cx) * math.sin(a) + (py - 550) * math.cos(a))
    P.poly([R(x0, top), R(x1, top), R(x1 + 40, top - 30), R(x1, bot), R(x0 + 20, bot), R(x0 - 20, top + 10)], fill=(40, 40, 46))
    cw = (x1 - x0) / 16
    for i in range(16):
        bx0 = x0 + i * cw; bx1 = bx0 + cw
        lvl = 0
        if 15 - i < flooded: lvl = 1.0
        elif 15 - i < flooded + spill_p * 6:
            lvl = clamp(flooded + spill_p * 6 - (15 - i))
        if lvl > 0:
            wy = bot - (bot - top - 40) * lvl
            P.poly([R(bx0 + 4, wy), R(bx1 - 4, wy), R(bx1 - 4, bot - 6), R(bx0 + 4, bot - 6)], fill=(70, 140, 200))
        P.line([R(bx0, top + 60), R(bx0, bot)], (190, 190, 200), 5)
    P.line([R(x0, top + 60), R(x1, top + 60)], (120, 120, 130), 3)

def chibi2(layer, x, y, s, **kw):
    M.chibi(layer, x * SS, y * SS, s * SS, **kw)

def label(P, x, y, txt, f, col=INK, bg=(245, 238, 220, 230)):
    w = P.d.textlength(txt, font=f.font_variant(size=int(f.size * SS))) / SS + 40
    P.rrect(x - w / 2, y - f.size * 0.8, x + w / 2, y + f.size * 0.8, f.size * 0.8, fill=bg)
    P.text(x, y, txt, f, col)

# ---------- scenes: (bg, zoom, overlay fn) ----------
def s_route(P, L, t, sd):
    z = 1.0 + 0.06 * t / sd
    pts = [bgpt(P_ATL, z, lo, la, BG_ATL) for lo, la in ((-1.4, 50.9), (-8.3, 51.8), (-30, 46), (-49.9, 41.7), (-74, 40.7))]
    k = clamp(t / (sd * 0.8)); n = int(k * 100)
    path = []
    for i in range(len(pts) - 1):
        for j in range(25):
            u = j / 25; path.append((lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u)))
    path = path[: max(2, int(len(path) * min(k, 0.78)))]
    for i in range(0, len(path) - 1, 2): P.line([path[i], path[i + 1]], (180, 40, 40), 7)
    for lo, la, nm in ((-1.4, 50.9, "Southampton"), (-74, 40.7, "New York")):
        x, y = bgpt(P_ATL, z, lo, la, BG_ATL); P.circle(x, y, 12, fill=(180, 40, 40)); label(P, x - 90 if lo > -20 else x + 60, y - 50, nm, FX[36])
    hx, hy = path[-1]; P.circle(hx, hy, 18, fill=ACC, outline=BLACK, width=4)
    label(P, 540, 980, "APRIL 14, 1912", FB[96].font_variant(size=80), (180, 40, 40))
    chibi2(L, 230, 1600, 0.72, coat=(30, 40, 70), hat="cap", hair=(230, 230, 235), mood="neutral")
    return z
def s_ice(P, L, t, sd):
    z = 1.0 + 0.1 * t / sd
    x, y = bgpt(P_ICE, z, -49.9, 41.7, BG_ICE)
    iceberg(P, x + 120, y + 60, 0.9)
    sx = lerp(x - 520, x - 140, ease(t / (sd * 0.7)))
    ship(P, sx, y + 70, 0.55)
    if t > sd * 0.7:
        r = 40 + 200 * ((t - sd * 0.7) * 1.5 % 1); P.circle(x - 20, y + 40, r, outline=(255, 255, 255, int(255 * (1 - (r - 40) / 200))), width=6)
    label(P, 540, 380, "11:40 P.M. · APRIL 14, 1912", FX[44])
    chibi2(L, 850, 1600, 0.72, coat=(30, 40, 70), hat="cap", hair=(230, 230, 235), mood="worried")
    return z
def s_open(P, L, t, sd):
    x, y = bgpt(P_ICE, 1.0, -49.9, 41.7, BG_ICE)
    iceberg(P, x + 120, y + 60, 0.9); ship(P, x - 140, y + 70, 0.55)
    ph = (t * 0.9) % 1; r = 40 + 200 * ph
    P.circle(x - 20, y + 40, r, outline=(255, 255, 255, int(255 * (1 - ph))), width=6)
    label(P, 540, 700, "sank in 2 h 40 min", FB[96].font_variant(size=80), (180, 40, 40))
    chibi2(L, 850, 1600, 0.72, coat=(30, 40, 70), hat="cap", hair=(230, 230, 235), mood="worried")
    return 1.0

def s_comp(P, L, t, sd):
    k = clamp((t - 0.6) / 1.5); n = int(4 * k)
    compartments(P, t, n)
    label(P, 540, 300, "16 WATERTIGHT COMPARTMENTS", FX[44])
    label(P, 540, 820, "safe with up to 4 flooded", FB[60], (40, 110, 60)) if t > 0.6 else None
    chibi2(L, 230, 1600, 0.72, coat=(35, 35, 45), hat="top", hair=(120, 90, 60), mood="neutral", extra="blueprint")
    return 1.0
def s_five(P, L, t, sd):
    k = clamp(t / 1.2); n = 4 + int(k * 1.99) if k < 1 else 5
    compartments(P, t, n)
    label(P, 540, 820, f"{n} flooded", FB[60], (180, 40, 40))
    chibi2(L, 230, 1600, 0.72, coat=(35, 35, 45), hat="top", hair=(120, 90, 60), mood="worried")
    return 1.0
def s_spill(P, L, t, sd):
    p = clamp(t / sd); tilt = 6 * ease(p)
    compartments(P, t, 5, spill_p=ease(p), tilt=tilt)
    label(P, 540, 300, "WATER SPILLS OVER THE WALLS", FX[44])
    # ice cube tray icon
    P.rrect(250, 830, 830, 1000, 24, fill=(235, 245, 250), outline=INK, width=5)
    for i in range(6):
        lv = clamp(p * 7 - i); x = 275 + i * 92
        (P.rect(x, 985 - 130 * lv, x + 78, 985, fill=(110, 170, 220)) if lv > 0.02 else None); P.line([(x + 84, 840), (x + 84, 990)], INK, 4)
    return 1.0
def s_boats(P, L, t, sd):
    for i in range(20):
        k = clamp((t - i * 0.05) / 0.3); x = 140 + (i % 5) * 200; y = 330 + (i // 5) * 120
        P.poly([(x - 70 * k, y), (x + 70 * k, y), (x + 50 * k, y + 40 * k), (x - 50 * k, y + 40 * k)], fill=(245, 242, 232), outline=INK)
    P.text(540, 830, "20 lifeboats", FB[60], INK)
    k = ease((t - 1.0) / 1.2)
    P.rrect(140, 900, 940, 970, 30, fill=(200, 190, 170)); P.rrect(140, 900, 140 + 800 * 0.53 * k, 970, 30, fill=(70, 140, 90))
    P.text(540, 1035, "room for barely half aboard", FX[44], INK)
    return 1.0
def s_memorial(P, L, t, sd):
    n = 150
    for i in range(n):
        k = clamp((t - i * 0.01) / 0.4); x = 120 + (i % 15) * 60; y = 330 + (i // 15) * 60
        P.circle(x, y, 14 * k, fill=(245, 225, 190, int(230 * k)))
    P.text(540, 1000, "1,500+ lives lost", FB[60], (245, 225, 190))
    P.text(540, 1070, "(each light = 10 people)", FS[34], (220, 210, 190))
    return 1.0
def s_treaty(P, L, t, sd):
    P.rect(220, 260, 860, 820, fill=(245, 240, 225), outline=INK, width=6)
    P.text(540, 330, "SAFETY OF LIFE AT SEA", FX[44], INK); P.text(540, 390, "1914", FB[60], (180, 40, 40))
    items = ["Lifeboats for everyone", "24-hour radio watch", "Ice patrol"]
    for i, it in enumerate(items):
        k = clamp((t - 0.8 - i * 0.7) / 0.4); y = 500 + i * 90
        P.circle(290, y, 22 * k, fill=(70, 140, 90))
        if k > 0.6: P.line([(278, y), (288, y + 10), (304, y - 10)], WHITE, 6)
        P.text(330, y, it, FX[44], INK + (int(255 * k),), anchor="lm")
    chibi2(L, 220, 1600, 0.72, coat=(35, 35, 45), hat="top", hair=(200, 200, 205), mood="stern")
    chibi2(L, 860, 1600, 0.72, coat=(30, 40, 70), hat="cap", hair=(120, 90, 60), mood="neutral")
    return 1.0

def s_open_photo(P, L, t, sd):
    label(P, 300, 1055, "Illustration: Willy Stöwer, 1912", FS[34].font_variant(size=24))
    chibi2(L, 850, 1600, 0.72, coat=(30, 40, 70), hat="cap", hair=(230, 230, 235), mood="worried")
    return 1.0
_s_five0 = s_five
def s_five(P, L, t, sd):
    z = _s_five0(P, L, t, sd)
    label(P, 540, 372, "Iceberg photographed nearby, April 15, 1912", FS[34].font_variant(size=24))
    return z
PH_PAINT = dict(path="/home/claude/shorts/photos/wm_Stöwer_Titanic.jpg", box=(70, 560, 1010, 1085), focus=(0.55, 0.45), zoom=(1.0, 1.1))
PH_BERG = dict(path="/home/claude/shorts/photos/wm_Titanic_iceberg.jpg", box=(260, 150, 820, 390), focus=(0.5, 0.5), zoom=(1.0, 1.08))
SCENES = [(0, BG_SEA, s_open_photo, PH_PAINT), (1, BG_ATL, s_route, None), (2, BG_PAPER, s_comp, None), (3, BG_PAPER, s_five, PH_BERG), (4, BG_PAPER, s_spill, None),
          (5, BG_SEA, s_boats, None), (6, BG_SEA, s_memorial, None), (7, BG_PAPER, s_treaty, None), (8, BG_SEA, s_open_photo, PH_PAINT)]
HOOK = ["WHY DID IT", "SINK SO FAST?"]

def caption(im, t, chunks):
    cur = [c for c in chunks if c["start"] - 0.05 <= t < c["hold"]]
    if not cur: return
    c = cur[-1]; d = ImageDraw.Draw(im); f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Black.otf", 74)
    words = c["words"]; txt = " ".join(w for w, _, _ in words)
    lines = []; line = []
    for w, ws, we in words:
        if d.textlength(" ".join([x[0] for x in line] + [w]), font=f) > 900 and line: lines.append(line); line = []
        line.append((w, ws, we))
    lines.append(line)
    y0 = 1150 - (len(lines) - 1) * 46
    for li, ln in enumerate(lines):
        lw = d.textlength(" ".join(w for w, _, _ in ln), font=f); x = W / 2 - lw / 2; y = y0 + li * 92
        for w, ws, we in ln:
            col = ACC if ws <= t < we + 0.08 else WHITE
            d.text((x, y), w, font=f, fill=col, anchor="lm", stroke_width=8, stroke_fill=(25, 25, 30)); x += d.textlength(w + " ", font=f)

def render(out, preview=None):
    import audio2
    bounds = [0.0 if i == 0 else SENT[sc_[0]]["start"] - 0.12 for i, sc_ in enumerate(SCENES)] + [DUR]
    chunks = caption_chunks(SENT, maxwords=3); hook_end = SENT[0]["end"]; loop_t = DUR - 0.5

    def frame(t, for_cover=False):
        loop = for_cover or t >= loop_t; tt = 0.9 if loop else t
        si = max(i for i in range(len(SCENES)) if bounds[i] <= tt)
        _, bg, fn, ph_ = SCENES[si]; ts = tt - bounds[si]; sd = bounds[si + 1] - bounds[si]
        layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); P = Pen(ImageDraw.Draw(layer), layer)
        z = fn(P, layer, ts, sd) or 1.0
        im = cam(bg, z).convert("RGBA")
        if ph_:
            import photo as PHM
            kw = dict(ph_); PHM.card(im, kw.pop("path"), ts / max(sd, 0.1), **kw)
        layer = layer.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA")
        a = 1.0 if (si == 0 or loop) else ease(ts / 0.3)
        if a < 1: layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
        im.alpha_composite(layer)
        # punch-in on each caption chunk
        cur = [c for c in chunks if c["start"] <= tt]
        p = 0.0 if (loop or not cur) else max(0.0, 1 - (tt - cur[-1]["start"]) / 0.35)
        sc = 1.0 + 0.04 * ease(p)
        if sc > 1.001:
            cw, ch = int(W / sc), int(H / sc); im = im.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([40, 70, 270, 130], radius=30, fill=(25, 25, 30))
        d.text((60, 100), "DAILY", font=FX[36], fill=WHITE, anchor="lm"); d.text((60 + d.textlength("DAILY ", font=FX[36]), 100), "WHY", font=FX[36], fill=ACC, anchor="lm")
        if not loop:
            d.rectangle([0, 0, W, 10], fill=(25, 25, 30)); d.rectangle([0, 0, int(W * t / DUR), 10], fill=ACC)
        if tt < hook_end or loop:
            for i, ln in enumerate(HOOK):
                d.text((W / 2, 300 + i * 135), ln, font=FB[150].font_variant(size=118), fill=ACC if i == len(HOOK) - 1 else WHITE, anchor="mm", stroke_width=12, stroke_fill=(25, 25, 30))
        if not loop: caption(im, t, chunks)
        return im.convert("RGB")

    frame(0.9, True).save("/home/claude/shorts/covers/titanic_cover.jpg", quality=92)
    if preview:
        for p_ in preview: frame(p_).resize((540, 960)).save(f"{out}_{int(p_ * 100):05d}.png")
        return
    events = [(bounds[i], "whoosh") for i in range(1, len(SCENES))]
    rt = SENT[TM["reveal"]]["start"]; events = [e for e in events if abs(e[0] - rt) > 0.3] + [(rt, "riser"), (rt, "impact"), (0.05, "tick"), (loop_t, "whoosh")]
    audio2.mix(f"/home/claude/shorts/{KEY}.wav", f"/home/claude/shorts/{KEY}_mix_raw.wav", DUR, events, mood="tense", bpm=90)
    audio2.loudnorm_2pass(f"/home/claude/shorts/{KEY}_mix_raw.wav", f"/home/claude/shorts/{KEY}_mix.wav")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", f"/home/claude/shorts/{KEY}_mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)): ff.stdin.write(frame(fi / FPS).tobytes())
    ff.stdin.close(); ff.wait()

def cover(out):
    """Thumbnail: iceberg scene + big title."""
    sd = SENT[2]["start"] - SENT[1]["start"]
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); P = Pen(ImageDraw.Draw(layer), layer)
    z = s_ice(P, layer, sd * 0.68, sd)
    im = cam(BG_ICE, z).convert("RGBA"); im.alpha_composite(layer.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA"))
    d = ImageDraw.Draw(im); f = FB[150]
    for i, (ln, col) in enumerate((("WHY DID IT", WHITE), ("SINK SO FAST?", ACC))):
        d.text((W / 2, 560 + i * 135), ln, font=f.font_variant(size=122), fill=col, anchor="mm", stroke_width=12, stroke_fill=(25, 25, 30))
    bw = d.textlength("DAILY WHY", font=FX[58]) + 80
    d.rounded_rectangle([W / 2 - bw / 2, 230, W / 2 + bw / 2, 320], radius=45, fill=(25, 25, 30))
    d.text((W / 2 - bw / 2 + 40, 275), "DAILY", font=FX[58], fill=WHITE, anchor="lm"); d.text((W / 2 - bw / 2 + 40 + d.textlength("DAILY ", font=FX[58]), 275), "WHY", font=FX[58], fill=ACC, anchor="lm")
    im.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cover":
        cover("/home/claude/shorts/covers/titanic_cover.jpg"); sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        pts = [0.0] + [SENT[i]["start"] + 1.6 for i in range(1, 9)] + [DUR - 0.2]
        render("/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/ti", preview=pts)
    else:
        render(f"/home/claude/shorts/{KEY}_final.mp4")
