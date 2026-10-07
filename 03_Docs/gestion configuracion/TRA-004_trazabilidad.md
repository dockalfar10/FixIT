# Matriz de trazabilidad

Cadena esperada: Solicitud → Requisito → Diseño → Código → Prueba → Revisión (PR) → Línea base.

## Trazabilidad de LB 1.0 (requisito a prueba)
| Requisito | Regla | Diseño | Código | Prueba | Línea base |
|---|---|---|---|---|---|
| RF-01 | RN-01 | DIS-001 | IMP-001, IMP-003 | CP-010 | LB 1.0 |
| RF-02 | RN-01, RN-02 | DIS-001, DIS-002 | IMP-002, IMP-004 | CP-001, CP-002 | LB 1.0 |
| RF-03 | RN-03, RN-05 | DIS-002 | IMP-002 | CP-003, CP-004, CP-008 | LB 1.0 |
| RF-04 | RN-04 | DIS-002 | IMP-002 | CP-005, CP-006 | LB 1.0 |
| RF-05 | RN-04, RN-05 | DIS-002 | IMP-002 | CP-007 | LB 1.0 |
| RF-06 | RN-06 | DIS-001 | IMP-002, IMP-004 | CP-009 | LB 1.0 |

## Trazabilidad de solicitudes de cambio
| CR | Requisito nuevo o afectado | CI modificados | Commits | Pull Request | Pruebas | Resultado | Línea base |
|---|---|---|---|---|---|---|---|
| CR-001 | [RF-07] | [ ] | [hash] | [#] | [CP-0xx] | Aprobada | LB 1.1 |
| CR-002 | [RF-08] | [ ] | [hash] | [#] | [CP-0xx] | Aprobada | LB 1.2 |
| CR-003 | — | Ninguno | — | — | — | Rechazada | Sin cambio (LB 1.2) |
