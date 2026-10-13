"""Síntesis local del guion aprobado, conservando límites de párrafo reales."""
from pathlib import Path
import json, time, wave
import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Users/SOPORTE/AppData/Local/ObservatorioVideo')
start=time.time()
voice=PiperVoice.load(str(WORK/'models/es_MX-claude-high.onnx'), use_cuda=False)
sections=[s.strip() for s in (ROOT/'docs/LOCUCION.txt').read_text(encoding='utf-8').split('\n\n') if s.strip()]
samples=[]
timeline=[]
position=0
rate=voice.config.sample_rate
for i,text in enumerate(sections):
    path=WORK/f'tmp/voz_{i:02d}.wav'
    with wave.open(str(path),'wb') as f:
        voice.synthesize_wav(text,f,syn_config=SynthesisConfig(length_scale=1.06,volume=0.85))
    with wave.open(str(path),'rb') as f:
        chunk=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).copy()
    timeline.append({'index':i,'start':position/rate,'end':(position+len(chunk))/rate,'text':text})
    samples.append(chunk)
    silence=np.zeros(int(rate*(0.40 if i<7 else 1.5)),dtype=np.int16)
    samples.append(silence)
    position+=len(chunk)+len(silence)
    print(i,round(len(chunk)/rate,2),text[:65],flush=True)
with wave.open(str(WORK/'tmp/narracion.wav'),'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate)
    f.writeframes(np.concatenate(samples).tobytes())
(WORK/'tmp/narracion.json').write_text(json.dumps({'sample_rate':rate,'duration':position/rate,
    'synthesis_seconds':time.time()-start,'sections':timeline},ensure_ascii=False,indent=2),encoding='utf-8')
print('Duración total:',position/rate,flush=True)
