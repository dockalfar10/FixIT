# CR-001 — Analisis de impacto sobre pruebas

| Campo | Valor |
|---|---|
| **Solicitud** | CR-001 — Prioridad de solicitudes |
| **Documento** | Aporte de QA al analisis de impacto (fila "Pruebas" de la seccion 12 del caso) |
| **Autor** | QA / Revisor |
| **Fecha** | 2026-10-05 |
| **Linea base vigente al analizar** | LB-1.0 |
| **Linea base que generaria** | LB-1.1 |
| **Estado del analisis** | Emitido **antes** de cualquier implementacion |

> Este documento cubre unicamente la perspectiva de pruebas. Las filas de necesidad,
> alcance, dependencias y decision corresponden al analista de cambio y al comite.

---

## 1. Cambio solicitado

Cada solicitud debe clasificarse como `BAJA`, `MEDIA`, `ALTA` o `CRITICA`, y debe aplicarse
una regla de atencion segun prioridad.

## 2. Lectura de QA sobre el alcance

El enunciado contiene **dos exigencias separables**, y conviene no confundirlas porque se
verifican de forma distinta:

| Exigencia | Naturaleza | Como se verifica |
|---|---|---|
| Clasificar la solicitud en cuatro niveles | Dato persistido | Comprobando que el valor se acepta, se rechaza si es invalido y se recupera |
| **Aplicar una regla de atencion segun prioridad** | Comportamiento | Comprobando que el orden o la seleccion de solicitudes cambia segun la prioridad |

Una implementacion que agregue la columna sin aplicar ninguna regla **no satisface CR-001**.
QA recomienda que el comite exija que la regla de atencion quede declarada explicitamente
en `ESP-001` antes de implementar: mientras no este escrito en que consiste (ordenar la
consulta de abiertas, seleccionar la siguiente a atender, u otra), no es verificable.

## 3. Pruebas nuevas necesarias

| Caso | Objetivo | Nivel |
|---|---|---|
| `CP-011` | Una solicitud acepta las cuatro prioridades declaradas | Servicio |
| `CP-012` | Una prioridad no declarada es rechazada, y el rechazo ocurre en la capa de aplicacion | Servicio |
| `CP-013` | Una solicitud creada sin prioridad explicita recibe el valor por defecto definido | Servicio |
| `CP-014` | La regla de atencion ordena o selecciona las solicitudes abiertas segun prioridad | Servicio |

`CP-012` se construira con el espia de conexion ya disponible en `conftest.py`, igual que
`CP-009`, para que la validacion se verifique en la aplicacion y no dependa del esquema.

`CP-014` solo podra escribirse cuando la regla este especificada. Es una **dependencia
bloqueante**: sin especificacion no hay criterio de aceptacion, y sin criterio no hay prueba.

## 4. Pruebas existentes que deben actualizarse

| Caso | Efecto | Accion |
|---|---|---|
| `CP-001` | Una solicitud nueva ahora tiene prioridad. El caso debe comprobar que nace con el valor por defecto | Ampliar una asercion |
| `CP-007` (campos requeridos) | La consulta de abiertas debe exponer la prioridad | Agregar `prioridad` a la lista de campos verificados |
| `CP-008` | El detalle debe exponer la prioridad | Agregar una asercion |
| `CP-009b` | El esquema incorpora una columna nueva con valor por defecto | Extender la verificacion de valores por defecto |

**Ningun caso existente queda invalidado por CR-001.** El cambio es aditivo: agrega un
atributo y una regla sobre un comportamiento ya existente, sin alterar ninguna regla vigente.

## 5. Riesgo de regresion, y una recomendacion de implementacion

La suite invoca `crear_solicitud()` en **12 lugares** distintos, repartidos en tres archivos
(`test_servicios_solicitud.py`, `test_servicios_flujo.py`, `test_consultas.py`).

Si `prioridad` se implementa como **parametro obligatorio**, esas 12 invocaciones dejan de
ser validas y la suite falla por completo por una razon ajena al cambio: no porque el
comportamiento sea incorrecto, sino porque cambio la firma. Se perderia la capacidad de
distinguir un defecto real de un desajuste de firma, justo durante la verificacion de LB-1.1.

> **Recomendacion de QA al implementador:** que `prioridad` sea un parametro **opcional con
> valor por defecto** (`MEDIA` o el que `ESP-001` defina). Asi RF-001 sigue cumpliendose sin
> modificar las invocaciones existentes, el cambio permanece aditivo y la regresion de LB-1.0
> conserva su valor como evidencia.

Esta recomendacion no es una exigencia funcional: es una restriccion de diseno que reduce la
superficie de regresion. Corresponde al comite aceptarla o descartarla.

## 6. Impacto sobre los datos

| Aspecto | Efecto |
|---|---|
| Estructura | Nueva columna `prioridad` en la tabla `solicitud` |
| Validacion | Nuevo dominio cerrado de cuatro valores. Debe declararse donde ya vive `ESTADOS_SOLICITUD`, en `models.py`, por coherencia |
| Filas existentes | Las solicitudes creadas bajo LB-1.0 no tienen prioridad. Requieren un valor por defecto en el esquema, o quedan nulas y rompen `CP-011` |
| Persistencia | Sin cambios en claves ajenas ni en las demas tablas |

El punto de las filas existentes es el unico con riesgo de datos: si la columna se agrega
sin `DEFAULT`, las solicitudes previas quedan con prioridad nula y la regla de atencion de
`CP-014` tendria que decidir que hacer con ellas.

## 7. Riesgos identificados desde pruebas

| N. | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Se implementa la columna pero no la regla de atencion, y CR-001 se declara cumplida | `CP-014` es obligatorio para el criterio de salida de LB-1.1 |
| R-02 | La regla de atencion no se especifica y `CP-014` se escribe adivinando el comportamiento | Bloquear la implementacion hasta que `ESP-001` declare la regla |
| R-03 | `prioridad` obligatoria rompe las 12 invocaciones y oculta defectos reales | Recomendacion de la seccion 5 |
| R-04 | Las solicitudes de LB-1.0 quedan con prioridad nula | Exigir `DEFAULT` en el esquema |

## 8. Esfuerzo estimado de QA

| Actividad | Estimacion |
|---|---|
| Escribir `CP-011` a `CP-014` en `02_Tests/test_prioridad.py` | 4 casos nuevos |
| Actualizar `CP-001`, `CP-007`, `CP-008`, `CP-009b` | 4 aserciones ampliadas |
| Ejecutar y registrar en `PRU-003` | Ejecucion numero 3 |
| Revisar el PR de implementacion | 1 revision |

## 9. Criterio de salida propuesto para LB-1.1

QA aprobara el etiquetado de LB-1.1 cuando:

1. Pasen los 26 casos de LB-1.0, incluidos los cuatro actualizados (**regresion completa,
   ningun caso degradado**).
2. Pasen `CP-011` a `CP-014`.
3. `CP-014` verifique la regla de atencion declarada en `ESP-001`, no un comportamiento
   supuesto.
4. Los resultados queden registrados en `PRU-003`.

## 10. Versiones de los CI de pruebas que resultarian

| CI | LB-1.0 | LB-1.1 | Justificacion |
|---|---|---|---|
| `PRU-001` Plan de pruebas | 1.0 | **1.1** | Incorpora `CP-011` a `CP-014` y modifica cuatro fichas existentes |
| `PRU-002` Suite automatizada | 1.0 | **1.1** | Archivo nuevo `test_prioridad.py` y cuatro archivos modificados |
| `PRU-003` Registro de resultados | 1.0 | **1.1** | Nueva ejecucion registrada |

## 11. Trazabilidad prevista

```
CR-001 -> ESP-001 (RF nuevo de prioridad) -> DES-001 (columna prioridad)
       -> COD-001 (services.py, database.py)
       -> PRU-001 v1.1 -> CP-011..CP-014 -> PRU-002 v1.1
       -> PRU-003 v1.1 (ejecucion 3) -> revision PR -> LB-1.1
```

## 12. Concepto de QA

**Favorable a la aprobacion**, con dos condiciones previas a la implementacion:

1. Que `ESP-001` declare explicitamente en que consiste la regla de atencion (sin ella
   `CP-014` no es escribible y R-02 se materializa).
2. Que la columna `prioridad` tenga valor por defecto, tanto en el esquema como en la firma
   de `crear_solicitud()`.

El cambio es aditivo, no contradice ninguna regla vigente en LB-1.0 y es verificable.
