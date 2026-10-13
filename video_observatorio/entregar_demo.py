"""Verifica el MP4 completo antes de publicarlo en la carpeta del proyecto."""
from pathlib import Path
import json, subprocess, shutil, time, hashlib
import av
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg


ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Users/SOPORTE/AppData/Local/ObservatorioVideo')
TMP=WORK/'tmp';VIDEO=TMP/'observatorio_demo.mp4'
ff=imageio_ffmpeg.get_ffmpeg_exe()
result=subprocess.run([ff,'-v','error','-xerror','-i',str(VIDEO),'-f','null','-'],capture_output=True,text=True)
if result.returncode:raise RuntimeError(result.stderr)
measurement=subprocess.run([ff,'-hide_banner','-i',str(VIDEO),'-af',
 'loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True)
text=measurement.stderr
audio=json.loads(text[text.rfind('{'):text.rfind('}')+1])
assert abs(float(audio['input_i'])+16)<=.5 and float(audio['input_tp'])<=-1
container=av.open(str(VIDEO));v=container.streams.video[0]
assert (v.width,v.height)==(1280,720)
assert container.streams.audio and v.codec_context.name=='h264'
report=json.loads((TMP/'render_report.json').read_text(encoding='utf-8'))
report.update(duration_seconds=container.duration/1e6,full_decode_passed=True,
    loudness_lufs=float(audio['input_i']),true_peak_dbtp=float(audio['input_tp']),
    elapsed_total_seconds=time.time()-json.loads((ROOT/'qa/reports/presentadora_inputs.json').read_text())['start_time'],sha256=hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
    quality_scope='Demo con presentadora estática; sin animación facial ni estado verified de la skill',
    storage_runtime=str(WORK),output='outputs/observatorio_demo.mp4')
sections=json.loads((TMP/'narracion.json').read_text(encoding='utf-8'))['sections']
times=[2,(sections[1]['start']+sections[3]['start'])/2,
 (sections[3]['start']+sections[4]['start'])/2]+[(sections[i]['start']+sections[i]['end'])/2 for i in (4,5,6)]+[
 sections[7]['start']+2,sections[7]['end']-1,report['duration_seconds']-.6]
target=0
sheet=Image.new('RGB',(960,600),'white');draw=ImageDraw.Draw(sheet)
for frame in container.decode(video=0):
    t=float(frame.pts*frame.time_base)
    if target<len(times) and t>=times[target]:
        x=(target%3)*320;y=(target//3)*200
        sheet.paste(frame.to_image().resize((320,180)),(x,y))
        draw.text((x+5,y+183),f'{t:.2f} s',fill='black',font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12))
        target+=1
container.close()
assert target==len(times)
for directory in ['outputs','assets/screenshots','assets/audio/final','assets/source','qa/reports','qa/contacts','qa/asr']:
    (ROOT/directory).mkdir(parents=True,exist_ok=True)
sheet.save(ROOT/'qa/contacts/observatorio_demo.jpg',quality=90)
shutil.copy2(VIDEO,ROOT/'outputs/observatorio_demo.mp4')
assert hashlib.sha256((ROOT/'outputs/observatorio_demo.mp4').read_bytes()).hexdigest()==report['sha256']
# Las capturas existentes se conservan sin sobrescribir.
# Se conserva el WAV original sin regenerarlo.

asr=TMP/'asr.json'
if asr.exists():shutil.copy2(asr,ROOT/'qa/asr/demo.json')
(ROOT/'qa/reports/demo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Línea de tiempo de la demo local','',
 'Montaje basado en los tiempos reales de la narración Piper. 1280 × 720, 24 fps, sin música.','',
 '| Escena | Inicio (s) | Fin (s) |','| --- | ---: | ---: |']
for scene in report['scenes']:lines.append(f"| {scene['scene']} | {scene['start']:.3f} | {scene['end']:.3f} |")
lines+=['','Los tres títulos se muestran con sus capturas originales. El modal cambia al indicador desplegado 5,4 segundos después del comienzo de la escena INDICADORES.',
 'El cierre conserva 1,5 segundos de pausa. La presentadora utiliza una imagen estática provisional, sin animación facial.']
(ROOT/'docs/TIMELINE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
job=json.loads((ROOT/'job.json').read_text(encoding='utf-8'))
job['user_constraints'].update(presenter='Presentadora estática de assets/presenter/presentadora.png autorizada por el usuario',
 storage='Proyecto y resultado en E:; entorno, modelos, caché y temporales en C:/Users/SOPORTE/AppData/Local/ObservatorioVideo',
 provider_selection='Piper local + Pillow + FFmpeg; sin APIs de generación ni servicios de pago')
job['creative'].update(width=1280,height=720,fps=24,style='Demo institucional con presentadora estática y capturas reales; sin música')
job['capabilities']['voice_generation']={'provider':'local','model':'Piper es_MX-claude-high','version':'piper-tts 1.8.0','device':'CPU'}
job['capabilities']['main_presenter']={'provider':'local','model':'Imagen proporcionada','image':'assets/presenter/presentadora.png','motion':'ninguno; imagen estática','remote':False}
job['capabilities']['timeline_compositor']={'provider':'local','tool':'Pillow + FFmpeg','script':'montar_demo.py'}
job['artifacts'].update(final_audio='assets/audio/final/narracion_demo.wav',rendered='outputs/observatorio_demo.mp4')
job['demo_delivery']={'status':'functional_demo','report':'qa/reports/demo.json','production_skill_verified':False}
(ROOT/'job.json').write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
