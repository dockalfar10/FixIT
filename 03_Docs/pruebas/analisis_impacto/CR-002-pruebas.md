# CR-002 — Analisis de impacto sobre pruebas

| Campo | Valor |
|---|---|
| **Solicitud** | CR-002 — Evidencia de solucion para cerrar una solicitud |
| **Documento** | Aporte de QA al analisis de impacto (fila "Pruebas" de la seccion 12 del caso) |
| **Autor** | QA / Revisor |
| **Fecha** | 2026-10-05 |
| **Linea base vigente al analizar** | LB-1.1 (prevista tras CR-001) |
| **Linea base que generaria** | LB-1.2 |
| **Estado del analisis** | Emitido **antes** de cualquier implementacion |

> Este documento cubre unicamente la perspectiva de pruebas. Las filas de necesidad,
> alcance, dependencias y decision corresponden al analista de cambio y al comite.

---

## 1. Cambio solicitado

Para cerrar una solicitud debe registrarse descripcion de la solucion, fecha y tecnico
responsable.

## 2. Lectura de QA sobre el alcance

A diferencia de CR-001, **este cambio no es aditivo: es restrictivo.** No agrega un atributo
sobre un comportamiento intacto, sino que **impone una precondicion a una transicion que hoy
no la tiene**. Pasar a `CERRADA` deja de ser siempre posible.

Esa diferencia es la que determina todo el impacto sobre pruebas: un cambio restrictivo
invalida los casos existentes que ejercitaban el comportamiento permisivo.

## 3. Pruebas existentes que quedan invalidadas

Esta es la seccion critica del analisis. Tres pruebas vigentes **fallaran** al implementar
CR-002, y no por un defecto, sino porque verifican una regla que el cambio deroga.

| Caso | Archivo y linea | Por que falla | Accion requerida |
|---|---|---|---|
| `CP-006[CERRADA]` | `test_servicios_flujo.py:11` (`ESTADOS_LB_1_0`) | Es un caso parametrizado que cierra la solicitud sin evidencia alguna. Tras CR-002 esa operacion debe ser rechazada | Retirar `CERRADA` de la parametrizacion generica y trasladar el cierre a `CP-015`, que si aporta evidencia |
| `CP-006` secuencia completa | `test_servicios_flujo.py:60` | Recorre `ASIGNADA -> EN_PROCESO -> CERRADA` sin evidencia y afirma que el estado final es `CERRADA` | Detener la secuencia en `EN_PROCESO`; el cierre pasa a ser objeto de `CP-015` |
| `CP-007` abiertas excluye cerradas | `test_consultas.py:33` | Su **precondicion** cierra una solicitud sin evidencia para comprobar que no aparece entre las abiertas. La precondicion deja de ser alcanzable | Cerrar esa solicitud aportando evidencia valida |

El caso de `CP-007` merece atencion especial: **no falla en su asercion, falla en su
preparacion.** El comportamiento que verifica (una cerrada no aparece entre las abiertas)
sigue siendo correcto; lo que cambia es la forma de llegar al estado inicial. Es un efecto
de segundo orden, del tipo que la seccion 12 del caso llama dependencias, y es exactamente
la razon por la que este analisis debe existir antes de implementar: si se descubre durante
la ejecucion, parecera un defecto del producto y no lo es.

## 4. Pruebas existentes que NO se ven afectadas

Conviene declararlo, porque la seccion 9 del caso pide justificar tambien lo que no cambia:

| Caso | Por que no se afecta |
|---|---|
| `CP-001`, `CP-009`, `CP-010` | Operan sobre la creacion, no sobre el cierre |
| `CP-002`, `CP-003`, `CP-004` | Catalogos de cliente, equipo y tecnico |
| `CP-005` | Asignacion de tecnico, previa al cierre |
| `CP-006` para `ABIERTA`, `ASIGNADA`, `EN_PROCESO` | Transiciones sin precondicion nueva |
| `CP-008` | Consulta de detalle; se amplia, no se invalida |
| `CP-009b` | Integridad del esquema; se amplia con las columnas nuevas |
| `CP-E2E-01` | Arranque de la aplicacion |

## 5. Pruebas nuevas necesarias

| Caso | Objetivo | Nivel |
|---|---|---|
| `CP-015` | Una solicitud con descripcion de solucion, fecha y tecnico responsable se cierra correctamente | Servicio |
| `CP-016` | **El cierre sin descripcion de solucion es rechazado**, y el rechazo ocurre en la capa de aplicacion | Servicio |
| `CP-017` | Al cerrar se registran y se recuperan la fecha de cierre y el tecnico responsable | Servicio |
| `CP-018` | Regresion dirigida: las transiciones a `ASIGNADA` y `EN_PROCESO` siguen funcionando **sin** exigir evidencia | Servicio |

`CP-016` es el caso que establece la regla de negocio del cambio. `CP-018` existe para
acotar el alcance de la restriccion: verifica que la precondicion se aplique **solo** al
cierre y no se haya extendido por error al resto de las transiciones. Sin `CP-018`, una
implementacion que exigiera evidencia para cualquier cambio de estado pasaria inadvertida.

## 6. Impacto sobre los datos

| Aspecto | Efecto |
|---|---|
| Estructura | Tres columnas nuevas en `solicitud`: descripcion de la solucion, fecha de cierre y tecnico responsable del cierre |
| Nulabilidad | Deben admitir nulo: una solicitud abierta no tiene solucion. La obligatoriedad es **condicional al cierre**, no estructural |
| Validacion | Nueva regla condicional en la transicion a `CERRADA` |
| Filas existentes | Las solicitudes ya cerradas bajo LB-1.0 o LB-1.1 no tienen evidencia. Quedarian cerradas sin solucion registrada |
| Tecnico responsable | Conviene definir si es el tecnico asignado o puede ser otro. Afecta el criterio de aceptacion de `CP-017` |

La nulabilidad condicional es el punto delicado: **la restriccion no puede expresarse con un
`NOT NULL`**, porque las solicitudes abiertas legitimamente no tienen solucion. Eso implica
que el esquema no puede garantizar esta regla y la responsabilidad recae enteramente en la
capa de aplicacion. Por eso `CP-016` debe verificar la aplicacion, y por eso no existe un
`CP-016b` de esquema equivalente a `CP-009b`.

## 7. Riesgos identificados desde pruebas

| N. | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Los tres casos invalidados se "arreglan" borrandolos en lugar de adaptarlos, perdiendo cobertura | La seccion 3 fija la accion concreta para cada uno; la revision del PR lo verifica |
| R-02 | La exigencia de evidencia se aplica a todas las transiciones, no solo al cierre | `CP-018` |
| R-03 | La regla se implementa solo en la interfaz y no en la capa de servicios, quedando eludible | `CP-016` opera en la capa de servicios, no por HTTP |
| R-04 | Las solicitudes cerradas en lineas base anteriores quedan sin evidencia | Decision del comite: migrar, marcar como historicas, o aceptar la inconsistencia documentandola |
| R-05 | Se interpreta que el cambio permite cerrar sin evidencia "si es antiguo", anticipando CR-003 | `CP-016` no admite excepciones por antiguedad |

## 8. Relacion con CR-003

CR-003 propone cerrar automaticamente solicitudes con mas de cinco dias abiertas **aunque no
exista evidencia de solucion**: exactamente la operacion que `CP-016` prohibira.

Las dos solicitudes son mutuamente excluyentes. Si CR-002 se aprueba e implementa, CR-003
solo podria aprobarse retirando `CP-016`, es decir, derogando una regla verificada en la
linea base inmediatamente anterior. Esta incompatibilidad es el fundamento del concepto
desfavorable emitido en `CR-003-pruebas.md`.

## 9. Esfuerzo estimado de QA

| Actividad | Estimacion |
|---|---|
| Adaptar `CP-006[CERRADA]`, `CP-006` secuencia y `CP-007` | 3 casos modificados |
| Escribir `CP-015` a `CP-018` en `02_Tests/test_evidencia_cierre.py` | 4 casos nuevos |
| Ampliar `CP-008` y `CP-009b` con las columnas nuevas | 2 aserciones ampliadas |
| Ejecutar y registrar en `PRU-003` | Ejecucion numero 4 |
| Revisar el PR de implementacion | 1 revision |

Es un esfuerzo mayor que el de CR-001 pese a tratarse de menos funcionalidad, precisamente
porque el cambio es restrictivo y obliga a reconstruir precondiciones existentes.

## 10. Criterio de salida propuesto para LB-1.2

QA aprobara el etiquetado de LB-1.2 cuando:

1. Pasen todos los casos de LB-1.1, incluidos los tres adaptados (**regresion completa**).
2. Pasen `CP-015` a `CP-018`.
3. `CP-018` demuestre que la restriccion se aplica unicamente al cierre.
4. Ningun caso de LB-1.0 ni de LB-1.1 se haya eliminado para hacer pasar la suite. La
   revision del PR verifica el diff de `02_Tests/` con este criterio.
5. Los resultados queden registrados en `PRU-003`.

El punto 4 es una condicion de revision, no de ejecucion: una suite puede quedar verde
borrando lo que molesta, y el caso de estudio prohibe borrar evidencia para limpiar el
historial.

## 11. Versiones de los CI de pruebas que resultarian

| CI | LB-1.1 | LB-1.2 | Justificacion |
|---|---|---|---|
| `PRU-001` Plan de pruebas | 1.1 | **1.2** | Incorpora `CP-015` a `CP-018` y modifica cinco fichas existentes |
| `PRU-002` Suite automatizada | 1.1 | **1.2** | Archivo nuevo `test_evidencia_cierre.py`, tres archivos adaptados |
| `PRU-003` Registro de resultados | 1.1 | **1.2** | Nueva ejecucion registrada |

## 12. Trazabilidad prevista

```
CR-002 -> ESP-001 (RF nuevo de evidencia de cierre) -> DES-001 (3 columnas nuevas)
       -> COD-001 (services.py, database.py)
       -> PRU-001 v1.2 -> CP-015..CP-018 + 3 casos adaptados -> PRU-002 v1.2
       -> PRU-003 v1.2 (ejecucion 4) -> revision PR -> LB-1.2
```

## 13. Concepto de QA

**Favorable a la aprobacion.** El cambio mejora de forma directa la trazabilidad del
servicio: tras implementarlo, toda solicitud cerrada tiene constancia de que se hizo, cuando
y quien respondio.

Se advierte, sin oponerse, que es un cambio **restrictivo** y por tanto mas costoso de
verificar que CR-001: invalida tres pruebas vigentes cuya adaptacion esta especificada en la
seccion 3 de este documento. Esas tres adaptaciones deben realizarse como parte de CR-002 y
quedar visibles en el PR, no resolverse eliminando los casos.

Se advierte ademas que la regla no puede garantizarse desde el esquema (seccion 6), de modo
que su cumplimiento depende enteramente de la capa de aplicacion y de `CP-016`.
