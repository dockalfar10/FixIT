# CR-003 — Analisis de calidad y recomendacion de rechazo

| Campo | Valor |
|---|---|
| **Solicitud** | CR-003 — Cierre automatico de solicitudes |
| **Documento** | Aporte de QA al analisis de impacto |
| **Autor** | QA / Revisor |
| **Fecha** | 2026-10-05 |
| **Linea base vigente al analizar** | LB-1.2 |
| **Recomendacion** | **RECHAZAR** |
| **Efecto sobre lineas base** | Ninguno. Se conserva LB-1.2 |

---

## 1. Solicitud recibida

Se propone cerrar automaticamente toda solicitud de soporte que lleve mas de cinco dias
abierta, **aunque no exista evidencia de solucion**.

## 2. Necesidad que origina el cambio

La necesidad declarada es reducir la cantidad de solicitudes abiertas acumuladas. Es una
necesidad legitima: un inventario creciente de casos sin cerrar dificulta la operacion y
distorsiona cualquier indicador de carga de trabajo.

Sin embargo, la solicitud confunde **el sintoma con el problema**. Un volumen alto de
solicitudes abiertas es un indicador de que los casos no se estan resolviendo. Cerrarlas
automaticamente no resuelve ningun caso: elimina el indicador y conserva el problema.

## 3. Alcance del cambio propuesto

El comportamiento que cambiaria es la transicion al estado `CERRADA`. Hoy esa transicion
requiere una accion humana con evidencia; la propuesta la convertiria en un efecto del paso
del tiempo.

## 4. Conflicto con una decision vigente

Este es el fundamento principal del rechazo.

CR-002 fue aprobada e implementada, y establecio que **para cerrar una solicitud debe
registrarse descripcion de la solucion, fecha y tecnico responsable**. Esa regla esta
vigente en LB-1.2 y esta verificada por el caso `CP-016`, que comprueba precisamente que
**el cierre sin descripcion de solucion es rechazado**.

CR-003 propone exactamente el comportamiento que `CP-016` prohibe. Las dos solicitudes son
mutuamente excluyentes: no existe una implementacion que satisfaga ambas.

Aprobar CR-003 obligaria a **eliminar o debilitar `CP-016`**, es decir, a retirar una prueba
de aceptacion aprobada en la linea base inmediatamente anterior. Un cambio cuya
implementacion exige borrar la verificacion de una regla vigente no es un incremento del
producto: es la reversion no declarada de una decision del comite de cambios.

## 5. CI que se verian afectados

| CI | Efecto si se aprobara |
|---|---|
| `ESP-001` Requisitos | Contradiccion interna: la regla de cierre de CR-002 y la de CR-003 no pueden coexistir |
| `DES-001` Modelo de datos | Requeriria distinguir cierres con evidencia de cierres automaticos, o perder la distincion |
| `COD-001` Codigo | `cambiar_estado()` tendria dos caminos de cierre con reglas opuestas |
| `PRU-001` Plan de pruebas | `CP-016` quedaria invalidado y habria que retirarlo |
| `PRU-002` Suite automatizada | `test_evidencia_cierre.py` fallaria y habria que modificarlo para aceptar lo que hoy rechaza |
| `DOC-001` Documentacion | El manual afirmaria una regla que el codigo ya no cumple |

El numero de CI afectados no es el argumento; lo es **la naturaleza del efecto**: en cuatro
de los seis casos el cambio no agrega comportamiento, sino que retira una verificacion.

## 6. Impacto sobre la calidad del servicio

| Aspecto | Consecuencia |
|---|---|
| **Trazabilidad del caso** | Una solicitud cerrada sin evidencia es indistinguible de una resuelta. Se pierde la capacidad de responder "que se le hizo a este equipo" |
| **Indicadores** | El tiempo de resolucion y la tasa de solucion dejan de ser confiables: todo caso cierra antes del dia seis, resuelto o no |
| **Experiencia del cliente** | Un cliente cuyo equipo sigue averiado veria su caso cerrado sin aviso ni solucion, y tendria que abrir uno nuevo, perdiendo el historial |
| **Responsabilidad** | Al no haber tecnico responsable del cierre, no hay a quien atribuir la decision |
| **Incentivo perverso** | El sistema premiaria no atender un caso: esperar cinco dias produce el mismo estado final que resolverlo |

El ultimo punto es el mas grave desde la perspectiva de calidad: el cambio no solo oculta
los casos no resueltos, sino que **vuelve indistinguible el trabajo hecho del trabajo no
hecho**.

## 7. Riesgos de implementar el cambio

1. **Perdida irreversible de informacion operativa** sobre casos realmente pendientes.
2. **Regresion silenciosa de CR-002**, sin una solicitud de cambio que la declare como tal.
3. **Inconsistencia documental**: la documentacion afirmaria una regla que el codigo ya no
   contiene, lo que vulnera las reglas de consistencia del ejercicio.
4. **Cierre de casos con equipos aun averiados**, con el consiguiente reclamo del cliente.

## 8. Consecuencia de no implementar el cambio

El inventario de solicitudes abiertas sigue creciendo mientras los casos no se atiendan.
Esto es un costo real, pero es **visible y medible**, y la informacion para gestionarlo se
conserva. La necesidad subyacente puede atenderse sin destruir evidencia; ver la seccion 9.

## 9. Alternativas que atenderian la necesidad sin el riesgo

Se dejan registradas para que el comite disponga de opciones, no como parte de esta
solicitud:

| Alternativa | Que resuelve | Que conserva |
|---|---|---|
| Estado `INACTIVA` o `SIN_RESPUESTA` distinto de `CERRADA` | Saca el caso de la bandeja activa | El caso sigue existiendo, sin evidencia falsa de solucion |
| Alerta al superar cinco dias, sin cierre | Visibiliza el caso estancado | La decision de cierre permanece humana |
| Cierre por inactividad **del cliente**, con motivo registrado | Cierra casos realmente abandonados | Queda registrado por que se cerro y quien lo decidio |
| Informe de antiguedad de solicitudes abiertas | Da la metrica que motivo la solicitud | No altera ninguna regla de negocio |

Cualquiera de estas tendria que tramitarse como una solicitud de cambio nueva, con su propio
analisis de impacto.

## 10. Recomendacion

**Rechazar CR-003.**

La solicitud es incompatible con la regla de negocio establecida por CR-002 y vigente en
LB-1.2, y su implementacion exigiria retirar el caso de prueba `CP-016` que verifica esa
regla. El beneficio buscado (reducir solicitudes abiertas) se obtiene eliminando el
indicador en lugar de atender la causa, y el costo es la perdida de trazabilidad de los
casos de soporte.

## 11. Cierre de la solicitud

| Accion | Estado |
|---|---|
| Solicitud registrada | Si |
| Analisis de impacto realizado antes de cualquier implementacion | Si |
| Decision documentada | Rechazada |
| Artefactos del producto modificados | **Ninguno** |
| Casos de prueba agregados o modificados | **Ninguno** |
| Nueva linea base generada | **Ninguna.** Se conserva LB-1.2 |
| Solicitud conservada como evidencia | Si |

La solicitud permanece registrada. El rechazo es evidencia de que el cambio fue considerado
y evaluado, no de que fue ignorado.

## 12. Respuestas a las preguntas de sustentacion

**Por que CR-003 fue rechazada.** Porque contradice la regla de cierre establecida por
CR-002 y vigente en LB-1.2, y su implementacion exigiria retirar el caso de prueba `CP-016`
que la verifica.

**Que habria cambiado si CR-003 se hubiera aprobado.** `ESP-001` habria quedado con una
contradiccion interna; `cambiar_estado()` habria tenido dos reglas de cierre opuestas;
`CP-016` habria tenido que eliminarse; y las solicitudes cerradas sin evidencia habrian
quedado indistinguibles de las resueltas.

**Por que el rechazo no produjo una nueva linea base.** Porque una linea base identifica un
conjunto de CI en versiones determinadas, y el rechazo no modifico ningun CI del producto.
La evidencia del analisis es un artefacto de gestion de la configuracion, no una version
nueva del producto.
