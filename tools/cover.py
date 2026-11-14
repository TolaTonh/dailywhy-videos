"""Cover / thumbnail maker for Daily Why Shorts (1080x1920)."""
import sys, importlib
sys.path.insert(0, "/home/claude/shorts")
from engine import *

def make_cover(mod_name, scene_fn, t, sd, title_lines, out, accent_line=1):
    m = importlib.import_module(mod_name); th = m.T
    im = gradient(th["bg1"], th["bg2"]); d = ImageDraw.Draw(im)
    # illustration, enlarged
    layer = Image.new("RGBA", (IW * SS, IH * SS), (0, 0, 0, 0))
    getattr(m, scene_fn)(Pen(ImageDraw.Draw(layer), layer), t, sd, th)
    layer = layer.convert("RGBa").resize((int(IW * 1.12), int(IH * 1.12)), Image.LANCZOS).convert("RGBA")
    im.paste(layer, (int((W - layer.width) / 2), 700), layer)
    # big title
    y = 290
    for i, ln in enumerate(title_lines):
        size = 150
        f = FB[150]
        while d.textlength(ln, font=f) > 990 and size > 80:
            size -= 6; f = FB[150].font_variant(size=size)
        col = th["accent"] if i == accent_line else th["text"]
        d.text((W / 2, y), ln, font=f, fill=col, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        y += size * 1.08
    # brand badge
    bw = d.textlength("DAILY WHY", font=FX[58]) + 80
    d.rounded_rectangle([W / 2 - bw / 2, 60, W / 2 + bw / 2, 150], radius=45, fill=(0, 0, 0))
    d.text((W / 2 - bw / 2 + 40, 105), "DAILY", font=FX[58], fill=th["text"], anchor="lm")
    d.text((W / 2 - bw / 2 + 40 + d.textlength("DAILY ", font=FX[58]), 105), "WHY", font=FX[58], fill=th["accent"], anchor="lm")
    im.save(out, quality=92)
    return im

COVERS = {
    "onions": ("v_onions", "scene_eye", 3.0, 5.0, ["WHY ONIONS", "MAKE YOU", "CRY"], 2),
    "brainfreeze": ("v_brainfreeze", "scene_pain", 2.5, 4.0, ["WHY ICE CREAM", "HURTS YOUR", "HEAD"], 2),
    "ocean": ("v_ocean", "scene_evap", 3.0, 5.0, ["WHY IS THE", "SEA SALTY?"], 1),
    "windowhole": ("v_windowhole", "scene_look", 4.0, 4.5, ["WHAT'S THIS", "TINY HOLE?"], 1),
    "fingers": ("v_fingers", "scene_bath", 2.0, 4.0, ["WHY FINGERS", "WRINKLE"], 1),
    "bridge": ("v_bridge", "scene_fall", 2.4, 4.0, ["THE BRIDGE", "THAT TWISTED"], 1),
    "pisa": ("v_pisa", "scene_1990", 3.5, 4.5, ["WHY HASN'T", "IT FALLEN?"], 1),
    "molasses": ("v_molasses", "scene_tank", 3.95, 4.0, ["A DEADLY", "WAVE OF SYRUP"], 1),
}

if __name__ == "__main__":
    keys = sys.argv[1:] or list(COVERS)
    for k in keys:
        mod, fn, t, sd, lines, acc = COVERS[k]
        make_cover(mod, fn, t, sd, lines, f"/home/claude/shorts/covers/{k}_cover.jpg", acc)
        print("ok", k)
