"""Daily Why source cards. style 'dark' = dark card with accent; style 'photo' = text on the full-screen photo with a marker sweep."""
import sys, glob, subprocess
sys.path.insert(0, "/home/claude/shorts")
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
F = "/usr/share/fonts/opentype/inter/"
def _f(w, s): return ImageFont.truetype([x for x in glob.glob(F + "*") if w in x and "Italic" not in x and "Display" not in x][0], s)
ACC, WHITE, BG, RED = (255, 196, 70), (245, 247, 250), (10, 16, 30), (255, 110, 95)
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def wrap(d, txt, f, w):
    out, cur = [], ""
    for wd in txt.split():
        if d.textlength((cur + " " + wd).strip(), font=f) <= w: cur = (cur + " " + wd).strip()
        else: out.append(cur); cur = wd
    return out + [cur]
_bg = {}
def bgimg(pid, size, blur, dim, t, dur):
    k = (pid, size, blur)
    if k not in _bg:
        im = ImageOps.fit(Image.open(f"/home/claude/shorts/photos/px_{pid}.jpg").convert("RGB"), (int(size[0] * 1.15), int(size[1] * 1.15)), Image.LANCZOS)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        _bg[k] = ImageEnhance.Brightness(im).enhance(dim)
    im = _bg[k]; z = 1.15 - 0.12 * (t / dur); w, h = int(size[0] * z), int(size[1] * z)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h)).resize(size, Image.BILINEAR)
def marker_lines(d, lines, f, x, y, lh, t, t0, per, center=None, pad=14):
    for i, ln in enumerate(lines):
        w = d.textlength(ln, font=f); lx = (center - w / 2) if center else x; k = ease((t - t0 - i * per) / per)
        if k > 0: d.rounded_rectangle((lx - pad, y + i * lh - 4, lx - pad + (w + 2 * pad) * k, y + i * lh + lh - 14), 12, fill=ACC)
        # text: dark where highlighted, white elsewhere
        d.text((lx, y + i * lh), ln, font=f, fill=WHITE)
        if k > 0:
            n = 0; 
            for j in range(len(ln) + 1):
                if d.textlength(ln[:j], font=f) <= (w + 2 * pad) * k - pad: n = j
            d.text((lx, y + i * lh), ln[:n], font=f, fill=BG)
def frame(t, spec, size=(1080, 1920), style="dark", dur=6.0):
    W, H = size; U = min(W, H * 0.62) / 1080  # scale unit
    if style == "dark":
        im = bgimg(spec["photo"], size, 14, 0.4, t, dur).convert("RGBA"); cw = int(900 * U); m = int(56 * U)
        f_lab, f_src, f_t, f_fact = _f("Bold", int(30 * U)), _f("SemiBold", int(34 * U)), _f("Bold", int(44 * U)), _f("Black", int(64 * U))
        tmp = ImageDraw.Draw(im); tl = wrap(tmp, spec["title"], f_t, cw - 2 * m); fl = []
        for ln in spec["fact"]: fl += wrap(tmp, ln.upper(), f_fact, cw - 2 * m)
        lh_t, lh_f = int(58 * U), int(84 * U)
        ch = m + int(50 * U) + int(54 * U) + int(30 * U) + len(tl) * lh_t + int(40 * U) + len(fl) * lh_f + m
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, cw - 1, ch - 1), int(36 * U), fill=(12, 18, 34, 238), outline=ACC, width=max(3, int(5 * U)))
        y = m; lab = "SOURCE"; lw = d.textlength(lab, font=f_lab)
        d.rounded_rectangle((m, y - 6, m + lw + 36 * U, y + 44 * U), int(22 * U), fill=ACC); d.text((m + 18 * U, y), lab, font=f_lab, fill=BG)
        d.text((m + lw + 56 * U, y), spec["kind"].upper(), font=f_lab, fill=(170, 176, 190)); y += int(64 * U)
        d.text((m, y), spec["source"], font=f_src, fill=ACC); y += int(54 * U)
        d.line([(m, y), (cw - m, y)], fill=(70, 78, 98), width=2); y += int(26 * U)
        for ln in tl: d.text((m, y), ln, font=f_t, fill=(205, 210, 220)); y += lh_t
        y += int(40 * U); marker_lines(d, fl, f_fact, m, y, lh_f, t, 1.2, 0.7)
        z = 0.94 + 0.1 * ease(t / dur); kin = ease(t / 0.4)
        c2 = card.resize((int(cw * z), int(ch * z)), Image.LANCZOS); c2.putalpha(c2.getchannel("A").point(lambda a: int(a * kin)))
        im.alpha_composite(c2, (int(W / 2 - c2.width / 2), int(H * 0.5 - c2.height / 2 + (1 - kin) * 80)))
    else:
        im = bgimg(spec["photo"], size, 0, 0.45, t, dur).convert("RGBA"); d = ImageDraw.Draw(im)
        f_lab, f_src, f_fact = _f("Bold", int(34 * U)), _f("SemiBold", int(36 * U)), _f("Black", int(84 * U))
        fl = []
        for ln in spec["fact"]: fl += wrap(d, ln.upper(), f_fact, W * 0.84 if W < H else W * 0.6)
        lh = int(112 * U); y0 = int(H * 0.5 - len(fl) * lh / 2); kin = ease(t / 0.4)
        if kin > 0.05:
            lab = "SOURCE"; lw = d.textlength(lab, font=f_lab); src = spec["short"]; sw = d.textlength(src, font=f_src); tot = lw + 36 * U + 20 * U + sw; x = W / 2 - tot / 2; yy = y0 - int(110 * U)
            d.rounded_rectangle((x, yy - 6, x + lw + 36 * U, yy + 48 * U), int(24 * U), fill=ACC); d.text((x + 18 * U, yy), lab, font=f_lab, fill=BG)
            d.text((x + lw + 56 * U, yy), src, font=f_src, fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))
            marker_lines(d, fl, f_fact, 0, y0, lh, t, 0.9, 0.6, center=W / 2, pad=int(20 * U))
    return im.convert("RGB")
if __name__ == "__main__":
    spec = dict(photo="36410538", kind="Official accident report", source="UK Air Accidents Investigation Branch", short="AAIB REPORT 1/92",
                title="Report on the accident to BAC One-Eleven, G-BJRT, over Didcot, on 10 June 1990", fact=["84 of the 90 windscreen bolts were too small"])
    S = "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad/"
    sheet = Image.new("RGB", (6 * 270, 480))
    for si, st in enumerate(("dark", "photo")):
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", S + f"src_{st}.mp4"], stdin=subprocess.PIPE)
        for i in range(150): ff.stdin.write(frame(i / 30, spec, style=st, dur=5.0).tobytes())
        ff.stdin.close(); ff.wait()
        for j, tt in enumerate((0.5, 1.7, 4.5)): sheet.paste(frame(tt, spec, style=st, dur=5.0).resize((270, 480)), ((si * 3 + j) * 270, 0))
    sheet.save(S + "src_styles.jpg")
    frame(4.5, spec, (1920, 1080), "dark", 5.0).resize((640, 360)).save(S + "src_dark_wide.jpg")
