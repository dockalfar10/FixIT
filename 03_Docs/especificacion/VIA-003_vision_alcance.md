# Visión y alcance de FixIT

| Campo | Valor |
|---|---|
| Código CI | VIA-003 |
| Versión | 1.0 |
| Estado | Aprobado |
| Responsable | [SthephaniGP / Analista y Documentador] |
| Ubicación | 03_Docs/especificacion/vision-alcance.md |
| Línea base | LB 1.0 |

## 1. Propósito
FixIT es una aplicación web para la mesa de soporte técnico. Permite registrar solicitudes de soporte de los clientes sobre sus equipos, asignarlas a un técnico, seguir su estado y cerrarlas.

## 2. Problema que resuelve
Describir en 3 o 4 líneas cómo se gestionan hoy las solicitudes (correo, llamadas, papel) y qué dificultades genera: pérdida de solicitudes, falta de responsable, falta de seguimiento.

## 3. Usuarios
| Rol | Descripción | Qué necesita |
|---|---|---|
| Operador de mesa | Recibe y registra solicitudes | Crear solicitudes, asignarlas |
| Técnico | Atiende las solicitudes | Ver sus casos, cambiar estado, cerrar |
| Cliente | Reporta fallas de sus equipos | (Interacción indirecta en LB 1.0) |

## 4. Alcance de la versión inicial (LB 1.0)
Incluye:
- Registrar solicitudes de soporte asociadas a un cliente y un equipo.
- Asignar un técnico a una solicitud.
- Cambiar el estado de una solicitud.
- Cerrar una solicitud.
- Consultar las solicitudes abiertas.

## 5. Fuera de alcance de LB 1.0
- Clasificación por prioridad y reglas de atención por prioridad (se tratará en CR-001).
- Registro de evidencia de solución al cerrar (se tratará en CR-002).
- Autenticación avanzada, notificaciones, reportes e integraciones externas.

## 6. Restricciones y supuestos
- Aplicación web desarrollada en Python con Flask.
- Persistencia en SQLite.
- [Agregar otras restricciones del equipo]

## 7. Criterios de éxito
- Las cinco funciones del alcance operan de extremo a extremo.
- Las pruebas automatizadas de la LB 1.0 pasan.
- La documentación coincide con el comportamiento real del código.

## 8. Historial de cambios del documento
| Versión | Fecha | Solicitud | Descripción |
|---|---|---|---|
| 1.0 | [23/09/2026] | Línea base inicial | Versión inicial aprobada |