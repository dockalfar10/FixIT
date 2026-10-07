# Reglas de negocio

| Campo | Valor |
|---|---|
| Código CI | REN-002 |
| Versión | 1.0 |
| Estado | Aprobado |
| Responsable | [SthephaniGP / Analista y Documentador] |
| Ubicación | 03_Docs/especificacion/reglas-negocio.md |
| Línea base | LB 1.0 |

## Reglas vigentes en LB 1.0
| ID | Regla | Requisito relacionado |
|---|---|---|
| RN-01 | Una solicitud debe estar asociada a un cliente y a un equipo existentes y tener una descripción no vacía | RF-02 |
| RN-02 | Toda solicitud nueva se crea en estado "Abierta" y registra su fecha de creación | RF-02 |
| RN-03 | Una solicitud solo puede asignarse a un técnico registrado; al asignarla pasa a "Asignada" | RF-03 |
| RN-04 | Transiciones permitidas: Abierta → Asignada → En proceso → Cerrada. No se permiten retrocesos ni saltos | RF-04, RF-05 |
| RN-05 | Una solicitud cerrada no puede modificarse ni reasignarse | RF-03, RF-05 |
| RN-06 | Se consideran "abiertas" todas las solicitudes cuyo estado es distinto de "Cerrada" | RF-06 |

> Los estados y transiciones deben coincidir exactamente con `services.py` y con DIS-002.

## Reglas que se agregarán por cambios (no existen en LB 1.0)
- Regla de prioridad y atención según prioridad (CR-001).
- Obligatoriedad de evidencia de solución al cerrar (CR-002).

## Historial de cambios del documento
| Versión | Fecha | Solicitud | Descripción |
|---|---|---|---|
| 1.0 | [23/09/2026] | Línea base inicial | Versión inicial aprobada |
