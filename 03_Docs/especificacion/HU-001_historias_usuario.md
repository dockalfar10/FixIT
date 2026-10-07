# Historias de usuario y requisitos funcionales

| Campo | Valor |
|---|---|
| Código CI | HU-001 |
| Versión | 1.0 |
| Estado | Aprobado |
| Responsable | [SthephaniGP / Analista y documentador] |
| Ubicación | 03_Docs/especificacion/historias-usuario.md |
| Línea base | LB 1.0 |

## Formato
Como **[rol]** quiero **[acción]** para **[beneficio]**.

## Requisitos funcionales
| ID | Requisito | Historia |
|---|---|---|
| RF-01 | El sistema permite registrar clientes y equipos | HU-01 |
| RF-02 | El sistema permite crear una solicitud de soporte | HU-02 |
| RF-03 | El sistema permite asignar un técnico a una solicitud | HU-03 |
| RF-04 | El sistema permite cambiar el estado de una solicitud | HU-04 |
| RF-05 | El sistema permite cerrar una solicitud | HU-05 |
| RF-06 | El sistema permite consultar las solicitudes abiertas | HU-06 |

> Ajustar la lista a lo que realmente implementa el código. No documentar nada que no exista.

## HU-01 Registrar cliente y equipo
Como operador quiero registrar clientes y sus equipos para asociarles solicitudes.

**Criterios de aceptación**
- Dado un cliente con nombre válido, cuando lo registro, queda guardado y disponible para solicitudes.
- Dado un equipo, cuando lo registro, debe quedar asociado a un cliente.

**Reglas relacionadas:** RN-01

## HU-02 Crear solicitud
Como operador quiero crear una solicitud indicando cliente, equipo y descripción de la falla para dejar constancia del caso.

**Criterios de aceptación**
- Si faltan cliente, equipo o descripción, el sistema rechaza la creación con un mensaje claro.
- La solicitud creada queda con estado "Abierta" y con fecha de creación.

**Reglas relacionadas:** RN-01, RN-02

## HU-03 Asignar técnico
Como operador quiero asignar un técnico a una solicitud para que alguien sea responsable de atenderla.

**Criterios de aceptación**
- Solo se puede asignar un técnico existente.
- Al asignar, el estado pasa a "Asignada".
- No se puede asignar una solicitud cerrada.

**Reglas relacionadas:** RN-03, RN-05

## HU-04 Cambiar estado
Como técnico quiero cambiar el estado de una solicitud para reflejar el avance del trabajo.

**Criterios de aceptación**
- Solo se permiten las transiciones definidas en el diagrama de estados.
- Una transición no permitida se rechaza con un mensaje.

**Reglas relacionadas:** RN-04

## HU-05 Cerrar solicitud
Como técnico quiero cerrar una solicitud atendida para que deje de aparecer entre las abiertas.

**Criterios de aceptación**
- Solo se puede cerrar una solicitud "En proceso".
- Una solicitud cerrada no admite más cambios.

**Reglas relacionadas:** RN-04, RN-05

## HU-06 Consultar solicitudes abiertas
Como operador quiero ver las solicitudes abiertas para saber qué casos siguen pendientes.

**Criterios de aceptación**
- El listado muestra todas las solicitudes cuyo estado no es "Cerrada".
- Cada fila muestra id, cliente, equipo, estado y técnico asignado.

**Reglas relacionadas:** RN-06

## Historial de cambios del documento
| Versión | Fecha | Solicitud | Descripción |
|---|---|---|---|
| 1.0 | [23/09/2026] | Línea base inicial | Versión inicial aprobada |
