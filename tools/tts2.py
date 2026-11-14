"""v2 voice: ~175 wpm, tight gaps, 0.55 s dramatic pause before the 'reveal' sentence."""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
K = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
S = json.load(open('/home/claude/shorts/scripts.json'))

def make(key, speed=1.08, gap=0.12, reveal_pause=0.55):
    v = S[key]; sr = 24000; parts = []; t = 0.0; timing = []
    reveal = v.get("reveal")
    for i, s in enumerate(v["sentences"]):
        if i == reveal:
            parts.append(np.zeros(int(reveal_pause * sr), np.float32)); t += reveal_pause
        a, sr = K.create(s, voice='am_michael', speed=speed, lang='en-us')
        idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0] - 120): idx[-1] + 360]
        d = len(a) / sr
        timing.append({'text': s, 'start': round(t, 3), 'end': round(t + d, 3)})
        parts.append(a.astype(np.float32)); parts.append(np.zeros(int(gap * sr), np.float32)); t += d + gap
    tail = 0.7  # room for the loop/cover frame
    parts.append(np.zeros(int(tail * sr), np.float32)); t += tail
    audio = np.concatenate(parts); sf.write(f'/home/claude/shorts/{key}.wav', audio, sr)
    json.dump({'duration': len(audio) / sr, 'sentences': timing, 'reveal': reveal}, open(f'/home/claude/shorts/{key}_timing.json', 'w'), indent=1)
    w = sum(len(x['text'].split()) for x in timing)
    print(key, round(len(audio) / sr, 1), 's', round(w / (len(audio) / sr) * 60), 'wpm')

if __name__ == "__main__":
    for k in sys.argv[1:]: make(k)
