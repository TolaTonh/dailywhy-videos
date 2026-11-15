"""Source 'article highlight' card: a paper document appears, the camera pushes in, a marker highlights the key line.
frame(t, spec, size) -> PIL image. spec: dict(photo=id, source=str, kind=str, title=str, fact=[lines], date=str)"""
import sys, math
sys.path.insert(0, "/home/claude/shorts")
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
F = "/usr/share/fonts/opentype/inter/"
import glob
def _f(w, s):
    p = [x for x in glob.glob(F + "*") if w in x and "Italic" not in x and "Display" not in x][0]; return ImageFont.truetype(p, s)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
_cache = {}
def _paper(spec, PW):
    """Render the paper at 2x; return (image, highlight boxes [(x0,y0,x1,y1)] per fact line, focus y)."""
    key = (id(spec), PW)
    if key in _cache: return _cache[key]
    m = int(PW * 0.075); x = m; f_lab = _f("SemiBold", int(PW * .028)); f_src = _f("Bold", int(PW * .04))
    f_t = ImageFont.truetype(SERIF, int(PW * .058)); f_fact = ImageFont.truetype(SERIF.replace("-Bold", ""), int(PW * .05))
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    def wrap(txt, f, w):
        out, cur = [], ""
        for wd in txt.split():
            if tmp.textlength((cur + " " + wd).strip(), font=f) <= w: cur = (cur + " " + wd).strip()
            else: out.append(cur); cur = wd
        return out + [cur]
    tl = wrap(spec["title"], f_t, PW - 2 * m); fl = []
    for ln in spec["fact"]: fl += wrap(ln, f_fact, PW - 2 * m)
    lh_t = int(PW * .074); lh_f = int(PW * .074); bar = int(PW * .03)
    Hh = m + int(PW * .05) + int(PW * .07) + int(PW * .04) + len(tl) * lh_t + int(PW * .05) + 3 * bar * 2 + int(PW * .03) + len(fl) * lh_f + int(PW * .04) + 4 * bar * 2 + m
    im = Image.new("RGB", (PW, Hh), (250, 247, 240)); d = ImageDraw.Draw(im); y = m
    d.text((x, y), "SOURCE  ·  " + spec["kind"].upper(), font=f_lab, fill=(150, 60, 50))
    if spec.get("date"): d.text((PW - m, y), spec["date"], font=f_lab, fill=(120, 120, 125), anchor="ra")
    y += int(PW * .05)
    d.text((x, y), spec["source"], font=f_src, fill=(30, 34, 44)); 
    y += int(PW * .07); d.line([(x, y), (PW - m, y)], fill=(30, 34, 44), width=3); y += int(PW * .04)
    for ln in tl: d.text((x, y), ln, font=f_t, fill=(20, 22, 30)); y += lh_t
    y += int(PW * .05)
    import random; r = random.Random(7)
    def bars(n):
        nonlocal y
        for i in range(n):
            w = (PW - 2 * m) * (r.uniform(.82, 1) if i < n - 1 else r.uniform(.4, .7)); d.rounded_rectangle((x, y, x + w, y + bar * .55), 6, fill=(214, 211, 204)); y += bar * 2
    bars(3); y += int(PW * .03); boxes = []
    for ln in fl:
        w = tmp.textlength(ln, font=f_fact); boxes.append((x - 8, y + 2, x + w + 8, y + lh_f - 6)); d.text((x, y + 6), ln, font=f_fact, fill=(20, 22, 30)); y += lh_f
    y += int(PW * .04); bars(4)
    fy = (boxes[0][1] + boxes[-1][3]) / 2
    _cache[key] = (im, boxes, fy, fl); return _cache[key]
def frame(t, spec, size=(1080, 1920), dur=6.0):
    W, H = size; bg = _cache.get(("bg", spec["photo"], size))
    if bg is None:
        bg = ImageOps.fit(Image.open(f"/home/claude/shorts/photos/px_{spec['photo']}.jpg").convert("RGB"), size, Image.LANCZOS)
        bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(18))).enhance(0.35); _cache[("bg", spec["photo"], size)] = bg
    PW = int(min(W * 0.86, H * 0.9) * 1.0) * 2 // 2; PW2 = PW * 2
    paper, boxes, fy, fl = _paper(spec, PW2); paper = paper.copy()
    # marker sweep: lines one after another from t=1.2
    hl = Image.new("RGB", paper.size, (255, 255, 255)); hd = ImageDraw.Draw(hl); t0 = 1.2; per = 0.75
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        k = ease((t - t0 - i * per) / per)
        if k > 0: hd.rounded_rectangle((x0, y0, x0 + (x1 - x0) * k, y1), 10, fill=(255, 226, 60))
    paper = ImageChops.multiply(paper, hl)
    # camera: push in toward the fact
    z = 0.5 * (1.0 + 0.14 * ease((t - 0.3) / (dur - 0.6)))          # paper is 2x
    pw, ph = int(paper.width * z), int(paper.height * z); p = paper.resize((pw, ph), Image.LANCZOS)
    sh = Image.new("RGBA", (pw + 80, ph + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 50, pw + 40, ph + 50), fill=(0, 0, 0, 150)); sh = sh.filter(ImageFilter.GaussianBlur(18))
    card = Image.new("RGBA", sh.size, (0, 0, 0, 0)); card.alpha_composite(sh); card.paste(p, (40, 40))
    card = card.rotate(-2.2 + 1.2 * ease(t / dur), resample=Image.BICUBIC, expand=True)
    kin = ease(t / 0.45); follow = ease((t - 0.3) / (dur - 0.6))
    cy_center = H * 0.5 + (ph / 2 - fy * z) * follow * 0.85
    cx = W / 2 - card.width / 2; cy = cy_center - card.height / 2 + (1 - kin) * H * 0.5
    out = bg.copy().convert("RGBA"); out.alpha_composite(card, (int(cx), int(cy))); return out.convert("RGB")
if __name__ == "__main__":
    import subprocess
    spec = dict(photo="36410538", kind="Official accident report", source="UK Air Accidents Investigation Branch", date="Report 1/92",
                title="Report on the accident to BAC One-Eleven, G-BJRT, over Didcot, Oxfordshire, on 10 June 1990",
                fact=["84 of the 90 windscreen bolts were smaller than the size required."])
    S = "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/"
    for name, size in (("doc_short", (1080, 1920)), ("doc_long", (1920, 1080))):
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", S + name + ".mp4"], stdin=subprocess.PIPE)
        for i in range(180): ff.stdin.write(frame(i / 30, spec, size).tobytes())
        ff.stdin.close(); ff.wait()
        sheet = Image.new("RGB", (4 * 360, 640 if size[1] > size[0] else 203))
        for j, tt in enumerate((0.3, 1.6, 3.0, 5.5)): 
            fr = frame(tt, spec, size); fr = fr.resize((360, int(360 * size[1] / size[0]))); sheet.paste(fr, (j * 360, 0))
        sheet.save(S + name + ".jpg")
