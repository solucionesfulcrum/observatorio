"""Registra la preproducción sin simular audio, presentador ni validaciones."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = Path('C:/Users/SOPORTE/.agents/skills/lanshu-create-ai-presenter-video')
for directory in ['assets/audio/reference', 'assets/audio/raw', 'assets/audio/final',
                  'assets/video/candidates', 'assets/video/selected', 'assets/video/render',
                  'assets/captions', 'qa/requests', 'qa/asr', 'qa/contacts', 'renders', 'outputs']:
    (ROOT / directory).mkdir(parents=True, exist_ok=True)
script = (ROOT / 'docs/SCRIPT.md').read_text(encoding='utf-8')
narration = script.split('## Locución\n', 1)[1].split('## Dirección', 1)[0].strip()
(ROOT / 'docs/LOCUCION.txt').write_text(narration + '\n', encoding='utf-8')
job_path = ROOT / 'job.json'
if not job_path.exists():
    job = json.loads((SKILL / 'assets/job.template.json').read_text(encoding='utf-8'))
    job['job_id'] = 'video-observatorio'
    job['input'].update(topic='Observatorio de Adherencia a Guías de Práctica Clínica',
                        script_path='docs/LOCUCION.txt',
                        supporting_media=['assets/source/index.html', 'assets/source/essalud.webp', 'assets/source/IETSI.webp'])
    job['creative'].update(language='es-LATAM', duration_target_s=60, aspect='16:9',
                           width=1920, height=1080, fps=30,
                           style='Institucional y tecnológico; presentador masculino realista; sin música')
    job['voice']['strategy'] = 'stock'
    job['artifacts'].update(script='docs/SCRIPT.md', beat_sheet='docs/BEAT_SHEET.md',
                            timeline='docs/TIMELINE.md', storyboard='docs/STORYBOARD.md')
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
evidence = {'narration_words': len(narration.split()), 'source_files': {}}
for source in (ROOT / 'assets/source').iterdir():
    if source.is_file():
        original = ROOT.parent / source.name
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        evidence['source_files'][source.name] = {
            'sha256': digest,
            'identical_to_original': original.exists() and digest == hashlib.sha256(original.read_bytes()).hexdigest()
        }
(ROOT / 'qa/reports/source_integrity.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(evidence, ensure_ascii=False, indent=2))
