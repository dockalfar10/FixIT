# Manual de usuario

| Campo | Valor |
|---|---|
| Código CI | DOC-002 |
| Versión | 1.0 |
| Estado | Aprobado |
| Responsable | [SthephaniGP / Analista y Documentador] |
| Ubicación | 03_Docs/usuario/manual-usuario.md |
| Línea base | LB 1.0 |

## 1. Introducción
Este manual explica cómo usar FixIT para gestionar solicitudes de soporte técnico.

## 2. Acceso
Abrir en el navegador la dirección `http://127.0.0.1:5000` (ajustar si cambia).

## 3. Crear una solicitud
1. Entrar a la pantalla de nueva solicitud.
2. Seleccionar cliente y equipo.
3. Escribir la descripción de la falla.
4. Pulsar el botón de guardar.

Resultado: la solicitud queda en estado "Abierta".

## 4. Asignar un técnico
1. Abrir la solicitud.
2. Elegir el técnico y confirmar.

Resultado: el estado cambia a "Asignada".

## 5. Cambiar el estado
Desde el detalle de la solicitud, elegir el siguiente estado permitido: Asignada → En proceso.

## 6. Cerrar una solicitud
Con la solicitud "En proceso", pulsar "Cerrar".

## 7. Consultar solicitudes abiertas
Abrir el listado de solicitudes abiertas. Muestra las que no están cerradas.

## 8. Mensajes de error frecuentes
| Mensaje | Causa | Qué hacer |
|---|---|---|
| [mensaje real] | Falta un dato obligatorio | Completar el campo |
| [mensaje real] | Transición no permitida | Seguir el orden de estados |

> Agregar capturas de pantalla reales y mensajes exactos de la aplicación. Documentar solo lo que existe en la LB 1.0.

## Historial de cambios del documento
| Versión | Fecha | Solicitud | Descripción |
|---|---|---|---|
| 1.0 | [23/09/2026] | Línea base inicial | Versión inicial aprobada |
