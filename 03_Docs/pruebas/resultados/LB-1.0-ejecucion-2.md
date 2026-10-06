# Registro de resultados de ejecucion — LB-1.0, ejecucion 2

| Campo | Valor |
|---|---|
| **Codigo del CI** | PRU-003 |
| **Nombre** | Registro de resultados de ejecucion |
| **Categoria** | Pruebas |
| **Version** | 1.1 |
| **Estado** | Aprobado (registro de hecho, no requiere aprobacion de contenido) |
| **Responsable** | QA / Revisor |
| **Ubicacion** | `03_Docs/pruebas/resultados/LB-1.0-ejecucion-2.md` |
| **Linea base** | LB-1.0 |
| **Ejecucion numero** | 2 |
| **Fecha de ejecucion** | 2026-10-06 |
| **Ejecucion anterior** | `LB-1.0.md` (ejecucion 1, 2026-10-05). No se sobrescribe |

---

## 1. Resultado global

> **LB-1.0 no cumple todavia su criterio de salida. QA no aprueba el etiquetado,
> pero por un unico defecto acotado y subsanable, no por ausencia de producto.**

| Metrica | Valor |
|---|---|
| Casos recolectados | 27 |
| Pasaron | 26 |
| Fallaron | 1 |
| Error de preparacion | 0 |
| Duracion | 1,22 s |

El cambio respecto de la ejecucion 1 es cualitativo, no solo numerico. Entonces los 26
casos daban error de preparacion porque los CI de implementacion no existian; ahora el
producto existe, carga, arranca y responde. Queda **un** fallo, y es un hallazgo real
sobre el comportamiento del producto.

## 2. Configuracion ejecutada

| Elemento | Valor |
|---|---|
| Rama | `qa/pruebas-lb-1.0` (desde `main`) |
| Commit del producto | `ede4e08` — *Merge pull request #2 from dockalfar10/implementacion* |
| CI ejecutado | `PRU-002` v1.1 (suite automatizada) |
| Plan de referencia | `PRU-001` v1.1 |
| CI bajo prueba | `COD-001` — presente (`__init__.py`, `database.py`, `models.py`, `services.py`, `routes.py`) |
| Python | 3.12.4 |
| pytest | 8.4.2 |
| Flask | 3.1.3 |
| Entorno | Virtualenv limpio creado desde `requirements.txt` |
| Comando | `python -m pytest` desde la raiz del proyecto |

El entorno se construyo **desde `requirements.txt`**, no desde el entorno de trabajo.
Es una correccion metodologica respecto de la ejecucion 1, que se registro con pytest
9.0.3 pese a que `requirements.txt` declara `pytest>=8.0,<9.0`. Un registro de
ejecucion que no se puede reproducir con las dependencias declaradas no sirve como
evidencia. Ver hallazgo H-08.

## 3. Resultado por caso

| Caso | Archivo | Variantes | Resultado |
|---|---|---|---|
| CP-001 | `test_servicios_solicitud.py` | 1 | PASA |
| CP-002 | `test_servicios_catalogo.py` | 1 | PASA |
| CP-003 | `test_servicios_catalogo.py` | 1 | PASA |
| CP-004 | `test_servicios_catalogo.py` | 1 | PASA |
| CP-005 | `test_servicios_flujo.py` | 1 | PASA |
| **CP-005b** | `test_servicios_flujo.py` | 1 | **FALLA — hallazgo D-01** |
| CP-006 | `test_servicios_flujo.py` | 6 | PASA |
| CP-007 | `test_consultas.py` | 2 | PASA |
| CP-008 | `test_consultas.py` | 2 | PASA |
| CP-009 | `test_servicios_solicitud.py` | 3 | PASA |
| CP-009b | `test_esquema.py` | 5 | PASA |
| CP-010 | `test_servicios_solicitud.py` | 1 | PASA |
| CP-E2E-01 | `test_rutas_e2e.py` | 2 | PASA |

## 4. Defecto detectado

### D-01 — `asignar_tecnico()` cambia el estado sin que ningun requisito lo declare

| Campo | Contenido |
|---|---|
| **Caso que lo detecta** | CP-005b |
| **CI afectado** | `COD-001` (`01_App/services.py`) y `ESP-001` |
| **Severidad** | Media |
| **Estado** | Abierto |

`asignar_tecnico()` ejecuta `UPDATE solicitud SET tecnico_id = ?, estado = 'ASIGNADA'`.
El cambio de estado no esta declarado en RF-004, que describe unicamente la asignacion
del tecnico, y RF-006 atribuye el cambio de estado a una operacion propia
(`cambiar_estado()`).

Mensaje reportado, textual:

```
RF-004: asignar_tecnico() cambio el estado de 'ABIERTA' a 'ASIGNADA'. Ningun
requisito declara ese efecto. El cambio de estado corresponde a cambiar_estado()
(RF-006). Hallazgo D-01.
```

**Por que no se clasifica como comportamiento aceptable sin mas.** Que el efecto sea
razonable no es el criterio: el criterio es que sea declarado y verificable. Hoy el
producto hace algo que la especificacion no dice, de modo que no existe forma de saber
si es una decision de diseno o un descuido. La seccion 19 del caso de estudio establece
que documentacion y codigo no pueden afirmar cosas distintas dentro de una misma linea
base; incorporar a LB-1.0 un comportamiento no especificado abre exactamente esa brecha.

**Por que importa mas adelante.** CR-002 impondra una precondicion a la transicion a
`CERRADA`. Una operacion que cambia el estado por dentro, sin pasar por `cambiar_estado()`,
es precisamente el tipo de camino que elude una precondicion. Resolver D-01 ahora evita
que CR-002 se implemente sobre un supuesto falso.

**Resolucion posible, a decidir por el comite, no por QA.** Dos salidas, ambas validas:

1. `ESP-001` declara el efecto (la asignacion transiciona la solicitud a `ASIGNADA`).
   Entonces CP-005b se reescribe para verificar ese comportamiento y pasa.
2. Se retira `estado = 'ASIGNADA'` de `asignar_tecnico()`. Entonces CP-005b pasa tal
   como esta.

QA no elige entre las dos: la primera es una decision de alcance y la segunda de
implementacion. Lo que QA sostiene es que el estado actual —hacerlo sin declararlo— no
es una de las dos.

## 5. Correcciones aplicadas a `PRU-001` y `PRU-002` antes de esta ejecucion

Cuatro casos fallaron en un ensayo previo contra este mismo commit. El analisis mostro
que el defecto estaba en el plan, no en el producto. Se corrigieron antes de registrar
la ejecucion, y las correcciones quedan declaradas aqui para que la trazabilidad no
dependa de la memoria del equipo.

| Caso | Sintoma | Causa real | Correccion |
|---|---|---|---|
| CP-005, CP-007, CP-008 | `KeyError: 'cliente_id'` / `'tecnico_id'` | `PRU-001` v1.0 nunca declaro el contrato de retorno de las consultas, y la suite asumio claves ajenas. La implementacion expone las relaciones por nombre (`cliente`, `equipo`, `tecnico`), que tambien satisface RF-007 y RF-008 | `PRU-001` v1.1 declara el contrato: la relacion debe ser *identificable*, en cualquiera de las dos formas. La suite incorpora `valor_relacion()` y `exige_relacion()` |
| CP-009 `[cliente]`, `[equipo]` | "se abrieron 1 conexiones" | El criterio "cero conexiones" confundia *validar consultando* con *delegar en el esquema*. Comprobar que el cliente referido existe exige un SELECT y es validacion legitima de la capa de aplicacion | `PRU-001` v1.1 reemplaza el criterio por "no se intento el INSERT", verificado sobre el SQL ejecutado |

**La segunda correccion estuvo a punto de debilitar la suite.** El primer intento fue
simplemente relajar la asercion para las dos variantes referenciales. Se comprobo por
mutacion que, asi relajado, CP-009 dejaba pasar una implementacion sin ninguna
validacion en la capa de aplicacion: el caso quedaba verde ante el defecto que fue
creado para detectar. Por eso el criterio final no es "no se abrio conexion" ni "no se
creo registro", sino **"no se ejecuto el INSERT"**, que distingue las dos situaciones y
conserva la deteccion. Queda registrado porque es la clase de error que, sin mutacion,
no se habria notado.

## 6. Validacion de la suite por mutacion

Ejecutada sobre copias del producto fuera del repositorio, descartadas despues. No
forman parte de ningun CI ni de ninguna linea base.

| Mutante inyectado | Casos que fallan | Veredicto |
|---|---|---|
| Estado inicial `CERRADA` en vez de `ABIERTA` | CP-001, CP-007 | Detectado |
| `listar_solicitudes_abiertas()` sin filtrar las cerradas | CP-007 | Detectado |
| `crear_solicitud()` sin ninguna validacion en la aplicacion | CP-009, las 3 variantes | Detectado |
| `NOT NULL` retirado del esquema | CP-009b, 3 variantes. **CP-009 sigue pasando** | Detectado |

La ultima fila vuelve a confirmar lo que la ejecucion 1 ya habia establecido: CP-009 y
CP-009b verifican riesgos independientes y ninguno cubre el defecto del otro. La
correccion del criterio de CP-009 no altero esa propiedad.

> **Nota de lectura.** CP-005b falla en los cuatro mutantes, porque D-01 esta abierto en
> el producto base. No es un efecto de los mutantes y no debe leerse como deteccion.

## 7. Estado de los hallazgos de configuracion de la ejecucion 1

| N. | Hallazgo | Estado | Evidencia |
|---|---|---|---|
| H-01 | `01_App/` sin codigo fuente | **Cerrado** | Los cinco modulos estan versionados y la suite los carga |
| H-02 | `__pycache__` bajo control de versiones | **Abierto** | Siguen rastreados 5 `.pyc` en `01_App/__pycache__/`. El `.gitignore` se agrego pero falto `git rm -r --cached` |
| H-03 | Bytecode de dos intepretes distintos | Cerrado | Solo quedan `.pyc` de CPython 3.12 |
| H-04 | Sin `requirements.txt` ni `.gitignore` | **Cerrado** | Ambos en `main`. `pytest.ini` se aporta en esta rama |
| H-05 | Plantillas HTML no versionadas | **Cerrado con reserva** | Las 7 estan versionadas, mas `base.html`. Ver seccion 8 |
| H-06 | LB-1.0 sin etiqueta | **Abierto** | `git tag` sigue sin devolver ninguna etiqueta |
| H-07 | Inventario con ubicaciones inexistentes | **Cerrado** | El informe adopta las rutas reales del repositorio |

### Hallazgos nuevos de esta ejecucion

| N. | Hallazgo | Severidad | Efecto |
|---|---|---|---|
| H-08 | `requirements.txt` declara `pytest>=8.0,<9.0`, pero la ejecucion 1 se registro con pytest 9.0.3 | Media | Un registro que no se reproduce con las dependencias declaradas no es evidencia. Corregido en esta ejecucion construyendo el entorno desde el archivo |
| H-09 | Coexistian dos suites de prueba en `02_Tests/` reclamando la identidad del CI `PRU-002` | Alta | Resuelto en esta rama. Ver seccion 9 |

## 8. Reserva sobre H-05: lo que hay no es lo que habia

Las plantillas existen hoy, pero **no son las de la LB-1.0 original: son una
reconstruccion**. La ejecucion 1 dejo constancia de que el contenido de las plantillas
se habia perdido de forma irrecuperable, porque Jinja no deja rastro compilado; solo se
pudieron recuperar sus nombres desde las constantes de `routes.pyc`.

Esto debe quedar escrito porque afecta directamente a una pregunta de sustentacion:
*"como puedo recuperar el producto tal como estaba en esa linea base"*. La respuesta
honesta para las plantillas de LB-1.0 es que no se puede. Lo que se etiquete como
`v1.0`, cuando se etiquete, sera un estado coherente y verificado, pero no identico al
que existia antes de la perdida. Registrarlo cuesta una linea y omitirlo invalida la
respuesta.

## 9. Resolucion de la duplicidad de suites (H-09)

Hasta esta rama, `02_Tests/` contenia dos conjuntos de pruebas:

| Conjunto | Archivos | Que verifica |
|---|---|---|
| Suite de QA | `conftest.py` + 7 archivos de casos | Las reglas de negocio derivadas de RF-001 a RF-010 |
| Suite de humo | `test_services.py`, `test_smoke.py`, `test_database.py`, `test_routes.py` | Que los modulos cargan y exponen ciertos nombres (`hasattr`) |

La seccion 6 del caso de estudio exige que un CI tenga **ubicacion conocida y
verificable**. Dos conjuntos en el mismo directorio reclamando ser `PRU-002` incumplen
ese requisito: no hay forma de responder que version del CI se ejecuto.

**Decision: `PRU-002` es la suite de QA.** Los cuatro archivos de humo se retiran en
esta rama. El fundamento es verificable, no de preferencia: las 9 pruebas de humo pasan
contra los cuatro mutantes de la seccion 6, es decir, pasan igual con el producto roto.
No aportan criterio de salida.

Retirarlos no vulnera la prohibicion de borrar evidencia de la seccion 19: esa regla
prohibe reescribir el historial, y aqui la eliminacion queda **en** el historial y es
recuperable en cualquier momento.

## 10. Evaluacion del criterio de salida de LB-1.0

`PRU-001` v1.1, seccion 10, exige para aprobar el etiquetado de LB-1.0 que pasen los
casos CP-001 a CP-010, CP-009b y CP-E2E-01, con los resultados registrados en `PRU-003`.

| Condicion | Cumple |
|---|---|
| CP-001 a CP-005, CP-006 a CP-010 pasan | Si |
| CP-005b pasa | **No** (D-01) |
| CP-009b pasa | Si |
| CP-E2E-01 pasa | Si |
| Resultados registrados | Si (este documento) |
| Entorno reproducible desde `requirements.txt` | Si |

**Conclusion: el criterio de salida no se cumple. QA no aprueba el etiquetado de LB-1.0.**

A diferencia de la ejecucion 1, el bloqueo es ahora de un solo punto y tiene dos salidas
posibles, ambas de bajo costo. Resuelto D-01 y cerrado H-02, LB-1.0 queda en condiciones
de etiquetarse como `v1.0`.

## 11. Acciones requeridas antes de la ejecucion 3

Dirigidas a los roles que corresponden. QA no las ejecuta: la seccion 14 del caso
establece que la revision y la implementacion no deben recaer en la misma persona.

| N. | Accion | Rol |
|---|---|---|
| 1 | Resolver D-01: declarar el efecto en `ESP-001` o retirarlo de `asignar_tecnico()` | Comite / Implementador |
| 2 | `git rm -r --cached 01_App/__pycache__` (H-02) | Implementador |
| 3 | Incorporar `ESP-001` al control de versiones. Hoy la matriz de trazabilidad referencia RF-001 a RF-010, que no estan versionados en ninguna parte | Analista de cambio |
| 4 | Inventariar `DES-001`, `COD-001` y `DOC-001` con sus ocho campos | Responsable de configuracion |
| 5 | Revisar y aprobar `PRU-001` y `PRU-002`, hoy en estado *En revision* | Otro integrante, no QA |

Cumplido el punto 1, QA ejecuta de nuevo y registra la ejecucion 3. Este registro no se
sobrescribe.

## 12. Trazabilidad de esta ejecucion

```
PRU-001 v1.1 (plan) -> PRU-002 v1.1 (suite) -> ejecucion 2 sobre commit ede4e08
  -> PRU-003 v1.1 (este registro)
  -> 26 de 27 casos pasan; D-01 abierto (CP-005b)
  -> criterio de salida de LB-1.0 NO cumplido
  -> LB-1.0 no etiquetada
```

## 13. Historial de versiones de este documento

| Version | Fecha | Cambio |
|---|---|---|
| 1.1 | 2026-10-06 | Registro de la ejecucion 2 sobre el commit `ede4e08`, con el producto ya restituido. 26 de 27 casos pasan. Un defecto abierto (D-01), dos hallazgos de configuracion nuevos (H-08, H-09), cinco hallazgos de la ejecucion 1 cerrados y dos todavia abiertos (H-02, H-06) |
