"""Montaje reproducible de la demo. Todo el cálculo y los temporales van a C:."""
from pathlib import Path
import json, math, subprocess, time, wave, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Users/SOPORTE/AppData/Local/ObservatorioVideo')
TMP=WORK/'tmp'; CAP=WORK/'capturas'
FPS=24; W,H=1280,720
FF=imageio_ffmpeg.get_ffmpeg_exe()
BLUE='#05639e'; INK='#12334a'; BG='#f3f9fd'
def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),size)
def wrap(text,f,width):
    lines=[]; line=''
    for word in text.split():
        test=(line+' '+word).strip()
        if f.getlength(test)>width and line: lines.append(line);line=word
        else: line=test
    if line:lines.append(line)
    return lines
def write(draw,text,xy,size=28,width=700,color=INK,bold=False):
    f=font(size,bold); x,y=xy
    for line in wrap(text,f,width):
        draw.text((x,y),line,font=f,fill=color);y+=size*1.3
    return y
def fit(img,box):
    out=ImageOps.contain(img,(box[2],box[3]),Image.Resampling.LANCZOS)
    return out,(box[0]+(box[2]-out.width)//2,box[1]+(box[3]-out.height)//2)
def presentadora():
    # Recorte de composición del área derecha; sin deformación o animación facial.
    img=Image.open(ROOT/'assets/presenter/presentadora.png').convert('RGBA')
    w,h=img.size
    img=img.crop((round(w*980/1672),round(h*30/941),round(w*1610/1672),h))
    return ImageOps.contain(img,(440,590),Image.Resampling.LANCZOS)
def source(name):return Image.open(CAP/name).convert('RGB')
def base():
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,9),fill=BLUE)
    return im
def logos(im):
    d=ImageDraw.Draw(im);d.rounded_rectangle((48,42,465,131),radius=12,fill=BLUE)
    for file,box in [('essalud.webp',(68,57,160,57)),('IETSI.webp',(266,54,175,63))]:
        img=Image.open(ROOT/'assets/source'/file).convert('RGBA');img,pos=fit(img,box);im.paste(img,pos,img)

def main():
    render_start=time.time()
    meta=json.loads((TMP/'narracion.json').read_text(encoding='utf-8'))
    sec=meta['sections'];dur=meta['duration'];frames=math.ceil(dur*FPS)
    portrait=presentadora()
    intro=base();logos(intro);d=ImageDraw.Draw(intro)
    write(d,'Observatorio de Adherencia a Guías de Práctica Clínica',(55,216),43,735,bold=True)
    write(d,'Instituto de Evaluación de Tecnologías en Salud e Investigación',(58,426),26,670)
    write(d,'IETSI · EsSalud',(58,535),24,650,color=BLUE,bold=True)
    write(d,'Presentadora provisional',(923,671),16,330,color='#617587')
    home=source('inicio.png').resize((W,H),Image.Resampling.LANCZOS)
    mixed=base();d=ImageDraw.Draw(mixed)
    write(d,'Guías con resultados disponibles',(35,35),32,1000,bold=True)
    pic,pos=fit(source('inicio.png'),(25,115,930,523));mixed.paste(pic,pos)
    write(d,'Presentadora provisional',(976,671),14,290,color='#617587')
    capture_meta=json.loads((CAP/'metadata.json').read_text(encoding='utf-8'))
    titles=capture_meta['titles']
    cards=[]
    for i,title in enumerate(titles):
        im=base();d=ImageDraw.Draw(im)
        im.paste(home.crop((0,0,1280,85)),(0,0))
        write(d,'Guías con resultados disponibles',(48,120),32,1100,bold=True)
        grid=source('guias.png');pic,pos=fit(grid,(45,235,1190,275));im.paste(pic,pos)
        # Resaltar una tarjeta en el montaje no altera la captura fuente.
        grid_box=capture_meta['grid_box'];card_box=capture_meta['card_boxes'][i]
        scale=pic.width/grid_box['width']
        x=pos[0]+(card_box['x']-grid_box['x'])*scale
        cell_width=card_box['width']*scale
        d.rounded_rectangle((int(x)-5,pos[1]-6,int(x+cell_width)+5,pos[1]+pic.height+6),radius=13,outline='#0077c8',width=4)
        write(d,title,(55,558),28,1170,color=BLUE,bold=True)
        cards.append(im)
    closed=source('indicadores.png').resize((W,H),Image.Resampling.LANCZOS)
    opened=source('indicador_abierto.png').resize((W,H),Image.Resampling.LANCZOS)
    closing=intro.copy()
    segments=[{'scene':'PRESENTADOR','start':0,'end':sec[1]['start']},
       {'scene':'CAPTURA DEL OBSERVATORIO','start':sec[1]['start'],'end':sec[3]['start']},
       {'scene':'PRESENTADOR + INTERFAZ','start':sec[3]['start'],'end':sec[4]['start']},
       {'scene':'GPC DISPONIBLES','start':sec[4]['start'],'end':sec[7]['start']},
       {'scene':'INDICADORES','start':sec[7]['start'],'end':sec[7]['end']},
       {'scene':'CIERRE','start':sec[7]['end'],'end':frames/FPS}]
    cmd=[FF,'-y','-loglevel','warning','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-',
         '-i',str(ROOT/'outputs/observatorio_demo.mp4'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','21',
         '-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart','-shortest',str(TMP/'observatorio_demo.mp4')]
    snapshots=[]
    log=open(TMP/'render.log','w',encoding='utf-8')
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
    try:
        for n in range(frames):
            t=n/FPS; actor=None;actorpos=None
            if t<sec[1]['start']:
                im=intro.copy();actor=portrait;actorpos=(823,69)
            elif t<sec[3]['start']:im=home.copy()
            elif t<sec[4]['start']:
                im=mixed.copy();actor=ImageOps.contain(portrait,(300,423),Image.Resampling.LANCZOS);actorpos=(962,236)
            elif t<sec[7]['start']:
                idx=0 if t<sec[5]['start'] else (1 if t<sec[6]['start'] else 2)
                im=cards[idx].copy()
            elif t<sec[7]['end']:
                im=(closed if t<sec[7]['start']+5.4 else opened).copy()
            else:im=closing.copy();actor=portrait;actorpos=(823,69)
            if actor is not None:im.paste(actor,actorpos,actor)
            proc.stdin.write(im.tobytes())
            if n%round(FPS*8)==0:
                print(f'Render {t:.1f}/{dur:.1f} s',flush=True)
            if n in {int(v*FPS) for v in [2,15,31,36,41,47,54,60,dur-0.6]}:
                snapshots.append((t,im.copy()))
    finally:proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError((TMP/'render.log').read_text())
    log.close()
    (TMP/'timeline.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(960,600),'white');d=ImageDraw.Draw(sheet)
    for i,(t,im) in enumerate(snapshots):
        x=(i%3)*320;y=(i//3)*200
        sheet.paste(im.resize((320,180)),(x,y));d.text((x+5,y+181),f'{t:.2f} s',fill=INK,font=font(13))
    sheet.save(TMP/'contactos.jpg',quality=90)
    report={'duration_seconds':dur,'video_duration_seconds':frames/FPS,'resolution':[W,H],'fps':FPS,
      'render_seconds':time.time()-render_start,'synthesis_seconds':meta['synthesis_seconds'],
      'size_bytes':(TMP/'observatorio_demo.mp4').stat().st_size,'scenes':segments,'voice':'es_MX-claude-high',
      'presenter':'Imagen estática proporcionada: assets/presenter/presentadora.png; sin deformación facial',
      'audio_reused_without_reencoding':True,'music':False,'paid_services':False,'external_inference':False}
    (TMP/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
