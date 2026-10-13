# Auditoría de proveedores de la skill instalada

Se revisaron SKILL.md, README.md, references/generation.md, la plantilla de trabajo y los cinco scripts incluidos en la instalación local de lanshu-create-ai-presenter-video.

## Resultado

La skill es independiente del proveedor. Describe un flujo de producción, pero no incluye clientes de API ni adaptadores de generación de voz, presentador o sincronización labial.

| Capacidad | Proveedores integrados | API key definida por la skill | Variable de credenciales leída por sus scripts |
| --- | --- | --- | --- |
| Voz | Ninguno | Ninguna | Ninguna |
| Generación de presentador | Ninguno | Ninguna | Ninguna |
| Lip-sync o reparación de sincronización labial | Ninguno | Ninguna | Ninguna |

El README, línea 79, requiere acceso independiente a estas capacidades mediante una CLI en la nube, una API o un modelo local. references/generation.md indica que se seleccionan durante la ejecución según las capacidades disponibles. Los campos vacíos capabilities.voice_generation, capabilities.main_presenter y capabilities.lipsync_repair de job.json son registros de la selección, no conectores instalados.

No hay una lista cerrada de proveedores certificados ni nombres de variables API definidos por esta skill. Configurar una clave no instala ni implementa una integración. Una alternativa externa requerirá revisar su documentación y preparar un cliente específico antes de utilizarla.

## Variables locales documentadas

- PROGRAM_LUFS: utilizada por scripts/finalize_delivery.sh, valor predeterminado -16. Controla la sonoridad de salida; no es una credencial.
- SKILL_DIR: variable auxiliar de shell en los ejemplos para localizar los scripts; no configura un proveedor.
- PATH: debe permitir localizar las herramientas locales requeridas; no es una credencial de proveedor.

## Restricciones vigentes del proyecto

Presentador ficticio adulto masculino; no usar imagen de ninguna persona real. Recursos generados exclusivamente en almacenamiento local. No realizar cargas externas ni operaciones de pago mientras no exista selección e instrucción posterior del usuario. No se ha seleccionado proveedor, enviado archivos ni ejecutado generación remota en esta revisión.
