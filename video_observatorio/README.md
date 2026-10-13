# Video del Observatorio — demo local

Resultado actualizado: `outputs/observatorio_demo.mp4`. Guion original, pista de audio Piper conservada exactamente, capturas reales y presentadora estática de `assets/presenter/presentadora.png`. Horizontal 1280 × 720, 24 fps, sin música. Se encuadra el retrato sin deformar ni animar el rostro. Aparece en introducción, presentadora + interfaz y cierre.

- `docs/SCRIPT.md`: guion y dirección de voz.
- `docs/LOCUCION.txt`: texto limpio para síntesis de voz.
- `docs/ANALISIS_HTML.md`: correspondencia del contenido con la fuente.
- `docs/BEAT_SHEET.md` y `docs/STORYBOARD.md`: distribución preliminar de escenas.
- `assets/source/`: HTML, CSS y logos originales.
- `job.json`: registro compatible con la skill, sin avances ni aprobaciones ficticias.
- `qa/reports/source_integrity.json`: comprobación de integridad de los originales copiados.

## Producción y almacenamiento

Entorno, modelos, caché y temporales: `C:/Users/SOPORTE/AppData/Local/ObservatorioVideo`. Python del entorno: `venv/Scripts/python.exe` dentro de esa carpeta.

Scripts reproducibles, en orden:

1. `capturar_demo.py`: Chrome/Playwright captura el HTML original, sin abrir tableros externos.
2. `narrar_demo.py`: Piper convierte el guion a voz mexicana en CPU.
3. `montar_demo.py`: compone la presentadora estática, monta las capturas y codifica con FFmpeg; reutiliza sin recodificar la pista AAC del MP4 existente.
4. `verificar_voz_demo.py`: transcripción local con faster-whisper base.
5. `entregar_demo.py`: decodifica el MP4 completo, mide volumen y publica el resultado.

Evidencias: `qa/reports/demo.json` y `qa/contacts/observatorio_demo.jpg`. Audio conservado en `assets/audio/final/narracion_demo.wav`; capturas en `assets/screenshots`.

Para animar esta misma imagen, evaluar SadTalker local: retrato + narración existente → rostro animado con boca y movimientos faciales. Requiere su propio entorno, PyTorch y modelos; no se instaló en esta revisión. Sustituir después la composición estática por la pista generada conservando guion, audio, capturas y tiempos. Referencia: https://github.com/OpenTalker/SadTalker

No se utilizaron servicios de pago ni APIs externas de generación, ni se cargaron recursos del Observatorio a proveedores. Esta es una demo funcional, no una certificación de calidad de producción ni el estado `verified` de la skill original.
