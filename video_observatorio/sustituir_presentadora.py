"""Prepara una sustitución estática, conserva guion, capturas y audio existente."""
from pathlib import Path
import hashlib,json,time
ROOT=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[ROOT/'docs/SCRIPT.md',ROOT/'docs/LOCUCION.txt',ROOT/'assets/audio/final/narracion_demo.wav',ROOT/'assets/presenter/presentadora.png']
files+=list((ROOT/'assets/screenshots').glob('*.png'))
record={'start_time':time.time(),'files':{p.relative_to(ROOT).as_posix():digest(p) for p in files}}
(ROOT/'qa/reports/presentadora_inputs.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
path=ROOT/'montar_demo.py';code=path.read_text(encoding='utf-8')
start=code.index('def avatar(');end=code.index('def source(',start)
code=code[:start]+'''def presentadora():
    # Recorte de composición del área derecha; sin deformación o animación facial.
    img=Image.open(ROOT/'assets/presenter/presentadora.png').convert('RGBA')
    w,h=img.size
    img=img.crop((round(w*980/1672),round(h*30/941),round(w*1610/1672),h))
    return ImageOps.contain(img,(440,590),Image.Resampling.LANCZOS)
'''+code[end:]
start=code.index("    with wave.open(");end=code.index('    intro=base()',start)
code=code[:start]+"    portrait=presentadora()\n"+code[end:]
code=code.replace('Presentador 2D provisional','Presentadora provisional')
code=code.replace('actor=avatar(t,rms[n])','actor=portrait')
code=code.replace('actor=avatar(t,0)','actor=portrait')
code=code.replace("'-i',str(TMP/'narracion.wav')","'-i',str(ROOT/'outputs/observatorio_demo.mp4')")
code=code.replace("'-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000',","'-pix_fmt','yuv420p','-c:a','copy',")
code=code.replace("'presenter':'Avatar masculino ficticio 2D dibujado con Pillow; apertura de boca guiada por RMS'","'presenter':'Imagen estática proporcionada: assets/presenter/presentadora.png; sin deformación facial'")
code=code.replace("'music':False", "'audio_reused_without_reencoding':True,'music':False")
path.write_text(code,encoding='utf-8')
delivery=ROOT/'entregar_demo.py';code=delivery.read_text(encoding='utf-8')
code=code.replace('from montar_demo import avatar','')
code=code.replace("time.time()-1790801872.73842","time.time()-json.loads((ROOT/'qa/reports/presentadora_inputs.json').read_text())['start_time']")
code=code.replace('Demo funcional 2D; no certificación de presentador realista ni estado verified de la skill','Demo con presentadora estática; sin animación facial ni estado verified de la skill')
code=code.replace("for capture in (WORK/'capturas').glob('*.png'):shutil.copy2(capture,ROOT/'assets/screenshots'/capture.name)","# Las capturas existentes se conservan sin sobrescribir.")
code=code.replace("shutil.copy2(TMP/'narracion.wav',ROOT/'assets/audio/final/narracion_demo.wav')","# Se conserva el WAV original sin regenerarlo.")
code=code.replace("avatar(2,0).save(ROOT/'assets/source/avatar_demo.png')","")
code=code.replace('El cierre conserva 1,5 segundos de pausa con boca en reposo. El avatar es un sustituto provisional y no representa a una persona real.','El cierre conserva 1,5 segundos de pausa. La presentadora utiliza una imagen estática provisional, sin animación facial.')
code=code.replace('Avatar 2D ficticio adulto masculino, autorizado como sustituto provisional','Presentadora estática de assets/presenter/presentadora.png autorizada por el usuario')
code=code.replace('Demo institucional con avatar 2D provisional y capturas reales; sin música','Demo institucional con presentadora estática y capturas reales; sin música')
code=code.replace("{'provider':'local','model':'Pillow procedural 2D','motion':'RMS audio + parpadeo','remote':False}","{'provider':'local','model':'Imagen proporcionada','image':'assets/presenter/presentadora.png','motion':'ninguno; imagen estática','remote':False}")
delivery.write_text(code,encoding='utf-8')
print('Sustitución preparada. Se reutilizará la pista AAC existente sin recodificar.')
