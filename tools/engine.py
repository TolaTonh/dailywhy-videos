"""Daily Why Shorts renderer: animated vector scenes + karaoke captions -> MP4 (1080x1920)."""
import json, math, subprocess, random
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name, size)
FB = {s: font("Inter-Black.otf", s) for s in (40, 52, 60, 72, 84, 96, 120, 150)}
FX = {s: font("Inter-ExtraBold.otf", s) for s in (36, 44, 58, 62, 70)}
FS = {s: font("Inter-SemiBold.otf", s) for s in (34, 40, 46)}

# illustration area (drawn at 2x then downsampled for anti-aliasing)
IX, IY, IW, IH = 0, 330, 1080, 940
SS = 2

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(lerp(c1[i], c2[i], clamp(t))) for i in range(3))

def gradient(c1, c2):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=mix(c1, c2, y / (H - 1)))
    return im

class Pen:
    """Drawing helper in 1080-wide illustration coordinates (auto-scaled by SS)."""
    def __init__(self, d, img=None): self.d = d; self.img = img
    def s(self, v): return v * SS
    def _translucent(self, fill): return self.img is not None and isinstance(fill, tuple) and len(fill) == 4 and fill[3] < 255
    def circle(self, x, y, r, fill=None, outline=None, width=0):
        if r <= 0: return
        if self._translucent(fill):
            R = int(self.s(r)) + 2; patch = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
            ImageDraw.Draw(patch).ellipse([2, 2, 2 * R - 2, 2 * R - 2], fill=fill)
            self.img.alpha_composite(patch, (int(self.s(x)) - R, int(self.s(y)) - R)) if 0 <= int(self.s(x)) - R and 0 <= int(self.s(y)) - R and int(self.s(x)) + R <= self.img.width and int(self.s(y)) + R <= self.img.height else None
            return
        self.d.ellipse([self.s(x - r), self.s(y - r), self.s(x + r), self.s(y + r)], fill=fill, outline=outline, width=int(self.s(width)))
    def ellipse(self, x, y, rx, ry, fill=None, outline=None, width=0):
        self.d.ellipse([self.s(x - rx), self.s(y - ry), self.s(x + rx), self.s(y + ry)], fill=fill, outline=outline, width=int(self.s(width)))
    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=0):
        self.d.rounded_rectangle([self.s(x0), self.s(y0), self.s(x1), self.s(y1)], radius=self.s(r), fill=fill, outline=outline, width=int(self.s(width)))
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=0):
        self.d.rectangle([self.s(x0), self.s(y0), self.s(x1), self.s(y1)], fill=fill, outline=outline, width=int(self.s(width)))
    def poly(self, pts, fill=None, outline=None, width=0):
        p = [(self.s(x), self.s(y)) for x, y in pts]
        if self._translucent(fill):
            x0, y0 = int(min(a for a, b in p)) - 2, int(min(b for a, b in p)) - 2
            x1, y1 = int(max(a for a, b in p)) + 2, int(max(b for a, b in p)) + 2
            if x0 < 0 or y0 < 0 or x1 > self.img.width or y1 > self.img.height: return
            patch = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
            ImageDraw.Draw(patch).polygon([(a - x0, b - y0) for a, b in p], fill=fill)
            self.img.alpha_composite(patch, (x0, y0)); return
        self.d.polygon(p, fill=fill, outline=outline, width=int(self.s(width)) if width else 1)
    def line(self, pts, fill, width):
        p = [(self.s(x), self.s(y)) for x, y in pts]
        self.d.line(p, fill=fill, width=int(self.s(width)), joint="curve")
        r = width / 2
        for x, y in (pts[0], pts[-1]): self.circle(x, y, r, fill=fill)
    def arc(self, x, y, r, a0, a1, fill, width):
        self.d.arc([self.s(x - r), self.s(y - r), self.s(x + r), self.s(y + r)], a0, a1, fill=fill, width=int(self.s(width)))
    def text(self, x, y, s, f, fill, anchor="mm"):
        ff = f.font_variant(size=int(f.size * SS))
        self.d.text((self.s(x), self.s(y)), s, font=ff, fill=fill, anchor=anchor)
    def arrow(self, x0, y0, x1, y1, col, w=14, head=34):
        ang = math.atan2(y1 - y0, x1 - x0)
        bx, by = x1 - head * 0.8 * math.cos(ang), y1 - head * 0.8 * math.sin(ang)
        self.line([(x0, y0), (bx, by)], col, w)
        self.poly([(x1, y1), (bx + head * 0.6 * math.cos(ang + 1.57), by + head * 0.6 * math.sin(ang + 1.57)),
                   (bx + head * 0.6 * math.cos(ang - 1.57), by + head * 0.6 * math.sin(ang - 1.57))], fill=col)
    def drop(self, x, y, r, fill):
        self.circle(x, y, r, fill=fill)
        self.poly([(x - r * 0.92, y - r * 0.35), (x, y - r * 2.1), (x + r * 0.92, y - r * 0.35)], fill=fill)
    def wave(self, x0, x1, y, amp, freq, phase, col, w):
        pts = [(x, y + amp * math.sin(freq * x / 100 + phase)) for x in range(int(x0), int(x1) + 1, 8)]
        self.line(pts, col, w)

def wrap(text, f, maxw, d):
    words = text.split(); lines = []; cur = []
    for w_ in words:
        test = " ".join(cur + [w_])
        if d.textlength(test, font=f) <= maxw or not cur: cur.append(w_)
        else: lines.append(cur); cur = [w_]
    if cur: lines.append(cur)
    return lines

def caption_chunks(sentences, maxwords=6):
    """Split each sentence into chunks (<= maxwords) with word-level times by char proportion."""
    chunks = []
    for s in sentences:
        words = s["text"].split(); n = len(words)
        k = math.ceil(n / maxwords); size = math.ceil(n / k)
        total = sum(len(w) + 1 for w in words); t0, dur = s["start"], s["end"] - s["start"]
        acc = 0; wt = []
        for w_ in words:
            ws = t0 + dur * acc / total; acc += len(w_) + 1; wt.append((w_, ws, t0 + dur * acc / total))
        for i in range(0, n, size):
            part = wt[i:i + size]
            chunks.append({"words": part, "start": part[0][1], "end": part[-1][2]})
    for i in range(len(chunks) - 1):  # hold each chunk until the next one begins
        chunks[i]["hold"] = chunks[i + 1]["start"]
    chunks[-1]["hold"] = chunks[-1]["end"] + 0.6
    return chunks

def render(key, scenes, theme, out, preview=None):
    """scenes: list of dict(start_sentence, title, fn). Scene spans from its first sentence start to next scene's."""
    tm = json.load(open(f"/home/claude/shorts/{key}_timing.json"))
    sents = tm["sentences"]; dur = tm["duration"]
    bounds = [0.0 if i == 0 else sents[sc["s"]]["start"] - 0.12 for i, sc in enumerate(scenes)] + [dur]
    chunks = caption_chunks(sents)
    bg = gradient(theme["bg1"], theme["bg2"])
    # subtle pattern on background
    bd = ImageDraw.Draw(bg)
    for y in range(0, H, 90):
        for x in range(0, W, 90):
            bd.ellipse([x + 43, y + 43, x + 47, y + 47], fill=mix(theme["bg1"], (255, 255, 255), 0.06))
    nframes = int(dur * FPS)
    frame_ids = [int(p * FPS) for p in preview] if preview else range(nframes)
    ff = None if preview else subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-i", f"/home/claude/shorts/{key}.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    acc, acc2, txt = theme["accent"], theme["accent2"], theme["text"]
    for fi in frame_ids:
        t = fi / FPS
        si = max(i for i in range(len(scenes)) if bounds[i] <= t)
        sc = scenes[si]; ts = t - bounds[si]; sd = bounds[si + 1] - bounds[si]
        im = bg.copy(); d = ImageDraw.Draw(im)
        # scene transition flash/slide
        layer = Image.new("RGBA", (IW * SS, IH * SS), (0, 0, 0, 0))
        sc["fn"](Pen(ImageDraw.Draw(layer), layer), ts, sd, theme)
        layer = layer.convert("RGBa").resize((IW, IH), Image.LANCZOS).convert("RGBA")
        a_in = ease(ts / 0.35)
        if a_in < 1:
            alpha = layer.getchannel("A").point(lambda v: int(v * a_in)); layer.putalpha(alpha)
        im.paste(layer, (IX, IY + int((1 - a_in) * 60)), layer)
        # brand bug + progress bar
        d.rounded_rectangle([40, 70, 40 + d.textlength("DAILY WHY", font=FX[36]) + 40, 130], radius=30, fill=mix(theme["bg1"], (0, 0, 0), 0.35))
        d.text((60, 100), "DAILY", font=FX[36], fill=txt, anchor="lm")
        d.text((60 + d.textlength("DAILY ", font=FX[36]), 100), "WHY", font=FX[36], fill=acc, anchor="lm")
        d.rectangle([0, 0, W, 10], fill=mix(theme["bg1"], (0, 0, 0), 0.4)); d.rectangle([0, 0, int(W * t / dur), 10], fill=acc)
        # scene headline (pop in)
        title = sc.get("title")
        if title:
            p = back(ts / 0.45); f_ = FB[84] if len(title) <= 16 else FB[72] if len(title) <= 20 else FB[60]
            lines = wrap(title, f_, 960, d); y0 = 250 - (len(lines) - 1) * f_.size * 0.55
            for li, ln in enumerate(lines):
                s_ = " ".join(ln); tmp = Image.new("RGBA", (W, int(f_.size * 1.4)), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
                td.text((W / 2, f_.size * 0.7), s_, font=f_, fill=sc.get("title_color", acc), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
                if p < 0.999:
                    sz = max(1, int(W * max(p, 0.05))), max(1, int(tmp.height * max(p, 0.05)))
                    tmp = tmp.resize(sz)
                im.paste(tmp, (int(W / 2 - tmp.width / 2), int(y0 + li * f_.size * 1.1 + f_.size * 0.7 - tmp.height / 2)), tmp)
        # karaoke captions
        cur = [c for c in chunks if c["start"] - 0.05 <= t < c["hold"]]
        if cur:
            c = cur[-1]; f_ = FX[62]
            words = [w_ for w_, _, _ in c["words"]]
            lines = wrap(" ".join(words), f_, 920, d)
            lh = 86; ytop = 1330 - (len(lines) - 1) * lh / 2
            boxw = max(d.textlength(" ".join(l), font=f_) for l in lines) + 70
            d.rounded_rectangle([W / 2 - boxw / 2, ytop - 62, W / 2 + boxw / 2, ytop + (len(lines) - 1) * lh + 62], radius=28, fill=(0, 0, 0))
            wi = 0
            for li, ln in enumerate(lines):
                lw = d.textlength(" ".join(ln), font=f_); x = W / 2 - lw / 2; y = ytop + li * lh
                for w_ in ln:
                    _, ws, we = c["words"][wi]; wi += 1
                    col = acc if ws <= t < we + 0.08 else (txt if t >= ws else mix(txt, (0, 0, 0), 0.35))
                    d.text((x, y), w_, font=f_, fill=col, anchor="lm")
                    x += d.textlength(w_ + " ", font=f_)
        if preview:
            im.resize((540, 960)).save(f"{out}_{fi:05d}.png")
        else:
            ff.stdin.write(im.tobytes())
    if ff:
        ff.stdin.close(); ff.wait()
    return dur
