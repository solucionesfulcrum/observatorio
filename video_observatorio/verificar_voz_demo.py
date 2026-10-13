"""ASR local, sin carga de audio ni inferencia externa."""
from pathlib import Path
import os,json,time,subprocess
import numpy as np
import imageio_ffmpeg
WORK=Path('C:/Users/SOPORTE/AppData/Local/ObservatorioVideo')
os.environ['HF_HOME']=str(WORK/'cache/huggingface')
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING']='1'
from faster_whisper import WhisperModel
start=time.time()
model=WhisperModel('base',device='cpu',compute_type='int8',download_root=str(WORK/'models/whisper'),cpu_threads=4)
pcm=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(WORK/'tmp/narracion.wav'),
 '-f','f32le','-ar','16000','-ac','1','-'],capture_output=True,check=True).stdout
segments,info=model.transcribe(np.frombuffer(pcm,dtype=np.float32),language='es',beam_size=5,word_timestamps=True)
out=[]
for segment in segments:
    print(f'{segment.start:.2f} - {segment.end:.2f}: {segment.text}',flush=True)
    out.append({'start':segment.start,'end':segment.end,'text':segment.text,
      'words':[{'start':w.start,'end':w.end,'text':w.word} for w in segment.words]})
(WORK/'tmp/asr.json').write_text(json.dumps({'model':'faster-whisper base int8 CPU','elapsed_seconds':time.time()-start,
 'segments':out},ensure_ascii=False,indent=2),encoding='utf-8')
