# Registro de versiones y estados

Regla: un CI solo cambia de versión cuando tiene una modificación real, vinculada a una solicitud de cambio.

| CI | Versión | Fecha | Solicitud | Descripción del cambio | Autor | Revisor | Estado resultante |
|---|---|---|---|---|---|---|---|
| ESP-001 | 1.0 | [fecha] | Línea base inicial | Versión inicial | [nombre] | [nombre] | Aprobado |
| ESP-002 | 1.0 | [fecha] | Línea base inicial | Versión inicial | [nombre] | [nombre] | Aprobado |
| ... | ... | ... | ... | ... | ... | ... | ... |

> Una fila por cada versión de cada CI. Para LB 1.0 se registran los 18 CI del inventario. Las versiones 1.1 y 1.2 se agregan al cerrar CR-001 y CR-002.

## Política de versionamiento
- Versión mayor.menor (1.0, 1.1, 1.2).
- Cada CI tiene su propia versión.
- Una nueva línea base no obliga a cambiar la versión de todos los CI.
- Los cambios de versión se justifican en este registro.