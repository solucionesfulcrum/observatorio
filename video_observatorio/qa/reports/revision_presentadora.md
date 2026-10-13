# Sustitución por presentadora estática

Se sustituyó el avatar masculino en las escenas de introducción, presentadora + interfaz y cierre. El rostro no se anima ni se deforma. Solo se recorta el área del retrato para excluir los textos de la imagen proporcionada y se escala proporcionalmente para el montaje.

Se comprobó por SHA-256 que SCRIPT.md, LOCUCION.txt, el WAV, la imagen proporcionada y todas las capturas conservan exactamente sus bytes. La pista AAC se copió sin recodificación y su hash coincide con la versión anterior. Evidencia: presentadora_preservacion.json.

El MP4 pasó decodificación completa y revisión de nueve fotogramas extraídos del archivo final. Conserva 1280 × 720, 24 fps, sin música. Se mantienen los seis intervalos del storyboard; únicamente cambia la presentadora.

Para animación posterior: SadTalker local con el recorte de la misma imagen y el WAV existente. Es una propuesta, no una dependencia instalada ni un resultado de animación probado en este equipo. Documentación oficial: https://github.com/OpenTalker/SadTalker
