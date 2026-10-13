"""Captura el HTML original; no modifica su diseño ni abre tableros remotos."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
WORK = Path('C:/Users/SOPORTE/AppData/Local/ObservatorioVideo')
OUT = WORK / 'capturas'
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',
        headless=True, args=['--disable-gpu', '--disable-software-rasterizer', '--disable-gpu-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=2)
    page.goto((ROOT/'assets/source/index.html').as_uri(), wait_until='networkidle', timeout=60000)
    page.evaluate('document.fonts.ready')
    page.screenshot(path=str(OUT/'inicio.png'))
    page.locator('.ggrid').screenshot(path=str(OUT/'guias.png'))
    for i, card in enumerate(page.locator('.gc').all()):
        card.screenshot(path=str(OUT/f'guia_{i+1}.png'))
    grid_box=page.locator('.ggrid').bounding_box()
    card_boxes=[card.bounding_box() for card in page.locator('.gc').all()]
    page.locator('.gc .btn-v').first.click()
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT/'indicadores.png'))
    page.locator('#ind-01 .ind-item-hdr').click()
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT/'indicador_abierto.png'))
    page.locator('#modal-nac .modal').screenshot(path=str(OUT/'modal.png'))
    (OUT/'metadata.json').write_text(json.dumps({'viewport':[1280,720], 'source':str(ROOT/'assets/source/index.html'),
        'grid_box':grid_box,'card_boxes':card_boxes,
        'titles':page.locator('.gc-name').all_text_contents()},ensure_ascii=False,indent=2),encoding='utf-8')
    browser.close()
print('Capturas guardadas:', OUT)
