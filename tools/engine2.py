"""Daily Why Shorts engine v2.
Changes from v1: instant first frame + text hook, camera punch-in on every caption chunk (visual change every ~2 s),
loop ending (last 0.5 s = opening frame = cover), music + SFX mix, same editing frame (titles, karaoke captions, badge, progress bar)."""
import json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw
import engine as E
from engine import Pen, FB, FX, FS, ease, back, clamp, mix, wrap, caption_chunks, IW, IH, IX, IY, SS
import audio2

W, H, FPS = 1080, 1920, 30

def render(key, scenes, theme, bg_img, hook_lines, out_dir="/home/claude/shorts", mood="curious", preview=None, title_block=None):
    tm = json.load(open(f"{out_dir}/{key}_timing.json")); sents = tm["sentences"]; dur = tm["duration"]
    bounds = [0.0 if i == 0 else sents[sc["s"]]["start"] - 0.1 + sc.get("off", 0) for i, sc in enumerate(scenes)] + [dur]
    chunks = caption_chunks(sents, maxwords=4)
    hook_end = sents[0]["end"]
    loop_t = dur - 0.5
    acc, txt = theme["accent"], theme["text"]

    def frame(t, for_cover=False):
        tt = 0.9 if t >= loop_t else t           # loop: last 0.5 s shows the opening frame
        loop = t >= loop_t or for_cover
        si = max(i for i in range(len(scenes)) if bounds[i] <= tt)
        sc = scenes[si]; ts = tt - bounds[si]; sd = bounds[si + 1] - bounds[si]
        im = bg_img.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        if sc.get("photo"):
            import photo as PH
            ph = dict(sc["photo"])
            if ph.pop("full", False): PH.full(im, ph.pop("path"), ts / max(sd, 0.1), **ph)
            else: PH.card(im, ph.pop("path"), ts / max(sd, 0.1), **ph)
        layer = Image.new("RGBA", (IW * SS, IH * SS), (0, 0, 0, 0))
        sc["fn"](Pen(ImageDraw.Draw(layer), layer), ts, sd, theme)
        # punch-in: small zoom jump at each caption chunk start, easing back
        cur = [c for c in chunks if c["start"] <= tt]
        p = 0.0
        if cur and not loop:
            age = tt - cur[-1]["start"]; p = max(0.0, 1 - age / 0.35)
        s = 1.0 + 0.045 * ease(p) + 0.012 * math.sin(tt * 0.9)
        lw, lh = int(IW * s), int(IH * s)
        lay = layer.convert("RGBa").resize((lw, lh), Image.LANCZOS).convert("RGBA")
        a_in = 1.0 if (si == 0 or loop) else ease(ts / 0.3)
        if a_in < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a_in)))
        im.alpha_composite(lay, (int(IX + (IW - lw) / 2), int(IY + (IH - lh) / 2 + (1 - a_in) * 50)))
        # badge + progress
        d.rounded_rectangle([40, 70, 40 + d.textlength("DAILY WHY", font=FX[36]) + 40, 130], radius=30, fill=mix(theme["bg1"], (0, 0, 0), 0.45))
        d.text((60, 100), "DAILY", font=FX[36], fill=txt, anchor="lm"); d.text((60 + d.textlength("DAILY ", font=FX[36]), 100), "WHY", font=FX[36], fill=acc, anchor="lm")
        if not loop:
            d.rectangle([0, 0, W, 10], fill=mix(theme["bg1"], (0, 0, 0), 0.4)); d.rectangle([0, 0, int(W * t / dur), 10], fill=acc)
        if title_block:
            title_block(d, theme)
        # hook text (frame 1 + loop/cover) or scene title
        if tt < hook_end or loop:
            sz = 124
            while max(d.textlength(ln, font=FB[150].font_variant(size=sz)) for ln in hook_lines) > 960 and sz > 70: sz -= 4
            f_ = FB[150].font_variant(size=sz); y = 230
            for i, ln in enumerate(hook_lines):
                d.text((W / 2, y + i * 130), ln, font=f_, fill=acc if i == len(hook_lines) - 1 else txt, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        elif sc.get("title"):
            pp = 1.0 if sc.get("hold") else back(ts / 0.4); title = sc["title"]; f_ = FB[84] if len(title) <= 16 else FB[72] if len(title) <= 20 else FB[60]
            lines = wrap(title, f_, 960, d); y0 = 250 - (len(lines) - 1) * f_.size * 0.55
            for li, ln in enumerate(lines):
                s_ = " ".join(ln); tmp = Image.new("RGBA", (W, int(f_.size * 1.4)), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
                td.text((W / 2, f_.size * 0.7), s_, font=f_, fill=sc.get("title_color", acc), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
                if pp < 0.999: tmp = tmp.resize((max(1, int(W * max(pp, 0.05))), max(1, int(tmp.height * max(pp, 0.05)))))
                im.alpha_composite(tmp, (int(W / 2 - tmp.width / 2), int(y0 + li * f_.size * 1.1 + f_.size * 0.7 - tmp.height / 2)))
        # karaoke captions
        if not loop:
            cc = [c for c in chunks if c["start"] - 0.05 <= t < c["hold"]]
            if cc:
                c = cc[-1]; f_ = FX[62]
                words = [w_ for w_, _, _ in c["words"]]; lines = wrap(" ".join(words), f_, 920, d)
                lh_ = 86; ytop = 1330 - (len(lines) - 1) * lh_ / 2
                boxw = max(d.textlength(" ".join(l), font=f_) for l in lines) + 70
                d.rounded_rectangle([W / 2 - boxw / 2, ytop - 62, W / 2 + boxw / 2, ytop + (len(lines) - 1) * lh_ + 62], radius=28, fill=(0, 0, 0))
                wi = 0
                for li, ln in enumerate(lines):
                    lw_ = d.textlength(" ".join(ln), font=f_); x = W / 2 - lw_ / 2; y = ytop + li * lh_
                    for w_ in ln:
                        _, ws, we = c["words"][wi]; wi += 1
                        col = acc if ws <= t < we + 0.08 else (txt if t >= ws else mix(txt, (0, 0, 0), 0.35))
                        d.text((x, y), w_, font=f_, fill=col, anchor="lm"); x += d.textlength(w_ + " ", font=f_)
        return im.convert("RGB")

    # cover = loop frame
    cover = frame(0.9, for_cover=True); os.makedirs(f"{out_dir}/covers", exist_ok=True)
    cover.save(f"{out_dir}/covers/{key}_cover.jpg", quality=92)
    if preview:
        for p_ in preview: frame(p_).resize((540, 960)).save(f"{preview_dir}/{key}_{int(p_ * 100):05d}.png")
        return
    # audio: whoosh on each scene change, riser + impact at the reveal, tick on hook
    events = [(bounds[i], "whoosh") for i in range(1, len(scenes))]
    if tm.get("reveal") is not None:
        rt = sents[tm["reveal"]]["start"]; events += [(rt, "riser"), (rt, "impact")]
        events = [e for e in events if abs(e[0] - rt) > 0.3 or e[1] != "whoosh"]
    events += [(0.05, "tick"), (loop_t, "whoosh")]
    audio2.mix(f"{out_dir}/{key}.wav", f"{out_dir}/{key}_mix_raw.wav", dur, events, mood=mood)
    audio2.loudnorm_2pass(f"{out_dir}/{key}_mix_raw.wav", f"{out_dir}/{key}_mix.wav")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", f"{out_dir}/{key}_mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                           f"{out_dir}/{key}_final.mp4"], stdin=subprocess.PIPE)
    for fi in range(int(dur * FPS)):
        ff.stdin.write(frame(fi / FPS).tobytes())
    ff.stdin.close(); ff.wait()

preview_dir = "/tmp/claude-0/-home-claude/9d670411-ef6e-51b8-9718-147962d89438/scratchpad"
