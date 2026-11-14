"""v2 audio: procedural music bed, sound effects, and ducked mix. All generated here, so no copyright issues."""
import numpy as np, soundfile as sf

SR = 48000

def _onepole_lp(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

def _lp_fast(x, cutoff):
    # simple FIR moving-average approximation (fast enough for long buffers)
    n = max(1, int(SR / cutoff / 2)); k = np.ones(n) / n
    return np.convolve(x, k, mode="same")

NOTE = {"A2": 110.0, "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.0, "A3": 220.0, "B3": 246.94,
        "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0, "A4": 440.0, "B4": 493.88, "C5": 523.25, "E5": 659.25}
PROGS = {
    "curious": [("A2", ["A3", "C4", "E4"]), ("F3", ["F3", "A3", "C4"]), ("C3", ["G3", "C4", "E4"]), ("G3", ["G3", "B3", "D4"])],
    "tense":   [("A2", ["A3", "C4", "E4"]), ("A2", ["A3", "C4", "F4"]), ("D3", ["A3", "D4", "F4"]), ("E3", ["G3", "B3", "E4"])],
    "bright":  [("C3", ["C4", "E4", "G4"]), ("G3", ["B3", "D4", "G4"]), ("A2", ["A3", "C4", "E4"]), ("F3", ["A3", "C4", "F4"])],
}

def music(duration, mood="curious", bpm=100, seed=1):
    rng = np.random.default_rng(seed)
    n = int(duration * SR); t = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm; bar = beat * 4; prog = PROGS[mood]
    nb = int(np.ceil(duration / bar)) + 1
    for b in range(nb):
        root, chord = prog[b % len(prog)]; t0 = b * bar
        i0, i1 = int(t0 * SR), min(n, int((t0 + bar) * SR))
        if i0 >= n: break
        tt = t[i0:i1] - t0
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.4)  # pad swell
        pad = sum(np.sin(2 * np.pi * NOTE[nm] * f * tt) for nm in chord for f in (1.0, 1.004)) / 6
        bass = np.sin(2 * np.pi * NOTE[root] / 2 * tt) * 0.6
        out[i0:i1] += (pad * 0.5 + bass * 0.35) * env
        # plucked arpeggio, 8th notes
        arp = chord + [chord[1]]
        for k in range(8):
            ts = t0 + k * beat / 2; j0 = int(ts * SR)
            if j0 >= n: break
            j1 = min(n, j0 + int(0.45 * SR)); u = (np.arange(j1 - j0)) / SR
            f = NOTE[arp[k % 4]] * 2
            out[j0:j1] += np.sin(2 * np.pi * f * u) * np.exp(-u * 9) * 0.22
        # soft pulse on beats (very light)
        for k in range(4):
            j0 = int((t0 + k * beat) * SR)
            if j0 >= n: break
            j1 = min(n, j0 + int(0.12 * SR)); u = np.arange(j1 - j0) / SR
            out[j0:j1] += np.sin(2 * np.pi * 55 * u) * np.exp(-u * 30) * (0.35 if k % 2 == 0 else 0.2)
    out = _lp_fast(out, 3500)
    out /= (np.abs(out).max() + 1e-9)
    fade = np.minimum(1, t / 0.3) * np.minimum(1, (duration - t) / 0.8)
    return out * fade

def whoosh(dur=0.45, up=True, seed=0):
    rng = np.random.default_rng(seed); n = int(dur * SR); u = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    env = np.sin(np.pi * np.clip(u / dur, 0, 1)) ** 2
    lo = _lp_fast(noise, 900); hi = noise - _lp_fast(noise, 2500)
    mixw = (u / dur) if up else (1 - u / dur)
    x = (lo * (1 - mixw) + hi * mixw * 0.6) * env
    return x / (np.abs(x).max() + 1e-9)

def impact(dur=0.9):
    n = int(dur * SR); u = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (60 - 25 * u) * u) * np.exp(-u * 4)
    rng = np.random.default_rng(3); click = _lp_fast(rng.normal(0, 1, n), 1500) * np.exp(-u * 40)
    x = boom + click * 0.5
    return x / (np.abs(x).max() + 1e-9)

def tick(freq=1400, dur=0.08):
    n = int(dur * SR); u = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * u) * np.exp(-u * 60)
    return x / (np.abs(x).max() + 1e-9)

def riser(dur=0.6):
    n = int(dur * SR); u = np.arange(n) / SR
    rng = np.random.default_rng(5); noise = rng.normal(0, 1, n) - _lp_fast(rng.normal(0, 1, n), 1200)
    tone = np.sin(2 * np.pi * (300 + 900 * (u / dur) ** 2) * u) * 0.3
    x = (noise * 0.5 + tone) * (u / dur) ** 2
    return x / (np.abs(x).max() + 1e-9)

def _resample_to_sr(x, sr):
    if sr == SR: return x
    idx = np.arange(int(len(x) * SR / sr)) * sr / SR
    return np.interp(idx, np.arange(len(x)), x)

def mix(voice_path, out_path, duration, events, mood="curious", bpm=100, music_level=0.085, sfx_level=0.35):
    """events: list of (time, kind) with kind in whoosh/impact/tick/riser."""
    v, vsr = sf.read(voice_path); v = v if v.ndim == 1 else v.mean(1); v = _resample_to_sr(v, vsr)
    n = int(duration * SR); voice = np.zeros(n); voice[: min(n, len(v))] = v[:n]
    voice /= (np.abs(voice).max() + 1e-9); voice *= 0.9
    m = music(duration, mood, bpm)
    # duck music under the voice
    envv = _lp_fast(np.abs(voice), 8); envv /= (envv.max() + 1e-9)
    duck = 1 - 0.45 * np.clip(envv * 3, 0, 1)
    out = voice + m * music_level * duck
    for tm, kind in events:
        s = {"whoosh": whoosh(seed=int(tm * 10)), "impact": impact(), "tick": tick(), "riser": riser()}[kind]
        lvl = {"whoosh": sfx_level, "impact": sfx_level * 1.3, "tick": sfx_level * 0.6, "riser": sfx_level * 0.8}[kind]
        if kind == "riser": tm = max(0, tm - 0.6)
        i0 = int(tm * SR)
        if i0 >= n: continue
        i1 = min(n, i0 + len(s)); out[i0:i1] += s[: i1 - i0] * lvl
    out /= (np.abs(out).max() + 1e-9); out *= 0.95
    sf.write(out_path, out.astype(np.float32), SR)

def loudnorm_2pass(src, dst, I=-14, TP=-1.5, LRA=11):
    """Accurate two-pass EBU R128 loudness normalization with ffmpeg."""
    import subprocess, json, re
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"): r.rindex("}") + 1])
    f = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", f, "-ar", "48000", dst], check=True)
