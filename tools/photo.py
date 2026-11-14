"""Real photos inside the editing frame: framed card with slow zoom (Ken Burns)."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
_cache = {}
def _load(path, maxside=2200):
    if path not in _cache:
        im = Image.open(path).convert("RGB"); im.thumbnail((maxside, maxside), Image.LANCZOS); _cache[path] = im
    return _cache[path]

def card(im, path, p, box=(70, 470, 1010, 1230), focus=(0.5, 0.5), zoom=(1.0, 1.10), dim=0.0, border=(240, 246, 255), radius=26):
    """Paste photo into RGBA frame `im`. p = 0..1 progress through the scene."""
    src = _load(path); x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    z = zoom[0] + (zoom[1] - zoom[0]) * max(0.0, min(1.0, p))
    ar = bw / bh; sw, sh = src.size
    cw, ch = (sw, sw / ar) if sw / sh < ar else (sh * ar, sh)
    cw, ch = cw / z, ch / z
    cx = min(max(focus[0] * sw, cw / 2), sw - cw / 2); cy = min(max(focus[1] * sh, ch / 2), sh - ch / 2)
    crop = src.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((bw, bh), Image.BILINEAR)
    if dim > 0: crop = ImageEnhance.Brightness(crop).enhance(1 - dim)
    mask = Image.new("L", (bw, bh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=radius, fill=255)
    sh_ = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh_).rounded_rectangle([40, 48, bw + 40, bh + 48], radius=radius, fill=(0, 0, 0, 150))
    im.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(16)), (x0 - 40, y0 - 40))
    im.paste(crop, (x0, y0), mask)
    ImageDraw.Draw(im).rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=border, width=6)


_grad = {}
def full(im, path, p, focus=(0.5, 0.5), zoom=(1.0, 1.12), dim=0.12, pan=(0.0, 0.0)):
    """Full-screen photo (1080x1920) with slow zoom/pan and dark top/bottom gradients for text."""
    src = _load(path); W, H = im.size; p = max(0.0, min(1.0, p))
    z = zoom[0] + (zoom[1] - zoom[0]) * p
    ar = W / H; sw, sh = src.size
    cw, ch = (sw, sw / ar) if sw / sh < ar else (sh * ar, sh)
    cw, ch = cw / z, ch / z
    fx, fy = focus[0] + pan[0] * (p - 0.5), focus[1] + pan[1] * (p - 0.5)
    cx = min(max(fx * sw, cw / 2), sw - cw / 2); cy = min(max(fy * sh, ch / 2), sh - ch / 2)
    crop = src.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    if dim > 0: crop = ImageEnhance.Brightness(crop).enhance(1 - dim)
    im.paste(crop, (0, 0))
    if (W, H) not in _grad:
        g = Image.new("L", (1, H))
        for y in range(H):
            a = max(0, 1 - y / 520) ** 1.4 * 200 + max(0, (y - 1080) / 840) ** 1.2 * 215
            g.putpixel((0, y), int(min(255, a)))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 255)); ov.putalpha(g.resize((W, H)))
        _grad[(W, H)] = ov
    im.alpha_composite(_grad[(W, H)])
