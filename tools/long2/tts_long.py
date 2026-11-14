import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro('/home/claude/tts/kokoro-v1.0.onnx','/home/claude/tts/voices-v1.0.bin')
S=json.load(open('script.json')); sr=24000
parts=[np.zeros(int(0.3*sr),np.float32)]; t=0.3; out=[]; gi=0
for ci,ch in enumerate(S['chapters']):
    if ci>0:
        g=1.4; parts.append(np.zeros(int(g*sr),np.float32)); t+=g
    ch_start=t
    for li,s in enumerate(ch['sentences']):
        a,sr=k.create(s,voice='am_michael',speed=1.0,lang='en-us')
        idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-240):idx[-1]+480]
        d=len(a)/sr
        out.append({'text':s,'start':round(t,3),'end':round(t+d,3),'chapter':ch['key'],'local':li})
        parts.append(a.astype(np.float32)); gap=0.35; parts.append(np.zeros(int(gap*sr),np.float32)); t+=d+gap
parts.append(np.zeros(int(1.5*sr),np.float32)); t+=1.5
audio=np.concatenate(parts); sf.write('long2.wav',audio,sr)
json.dump({'duration':len(audio)/sr,'sentences':out},open('long2_timing.json','w'),indent=1)
print(round(len(audio)/sr,1))
for ch in S['chapters']:
    f=[x for x in out if x['chapter']==ch['key']][0]; print(ch['key'], round(f['start'],1))
