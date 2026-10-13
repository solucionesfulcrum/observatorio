# Revisión de la demo del Observatorio

## Contenido y fuentes

La síntesis utiliza el texto de docs/LOCUCION.txt sin cambios. Los cinco archivos fuente originales conservan sus hashes SHA-256. No se modificó el HTML ni el CSS. Las capturas muestran la web real, sus tres guías y el indicador desplegado. No se abrieron tableros remotos ni se generaron cifras o resultados.

## Voz

Se probó es_MX-ald-medium y se sustituyó por es_MX-claude-high por claridad. Ambas son voces Piper ejecutadas en CPU. La transcripción local faster-whisper base conserva el recorrido narrativo, pero presenta discrepancias en términos médicos y nombres propios (por ejemplo IETSI, EsSalud y neumonía). La transcripción automática no certifica una coincidencia verbal exacta; se conserva como evidencia y la pronunciación institucional queda pendiente de revisión auditiva humana. No se han corregido los textos de la web para ajustarlos a errores de reconocimiento.

## Imagen

Avatar ficticio masculino adulto dibujado por código, sin referencias fotográficas. Apertura de boca según energía del audio y parpadeo; no sincronización fonética. Se revisó una hoja de nueve escenas y se corrigió el marco de selección para coincidir con los límites reales de cada tarjeta. La composición mantiene libre la interfaz y usa una combinación con avatar en su escena específica.

## Verificación técnica

El proceso de entrega exige decodificación completa de video y audio sin errores, resolución 1280 × 720, pista H.264, pista de audio y sonoridad -16 ± 0,5 LUFS con pico ≤ -1 dBTP. Los resultados concretos se guardan en demo.json. Los fotogramas de qa/contacts/observatorio_demo.jpg se extraen del MP4 codificado, no solo de la composición previa.

Esta entrega es una demo funcional local autorizada por el usuario, con requisitos reducidos respecto del video institucional final. No se afirma revisión audiovisual humana a velocidad normal ni el estado verified del flujo de producción de la skill.
