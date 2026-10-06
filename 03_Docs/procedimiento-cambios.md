# Procedimiento de control de cambios — convenciones operativas

| Campo | Valor |
|---|---|
| **Documento** | Propuesta de QA para adopcion del equipo |
| **Autor** | QA / Revisor |
| **Fecha** | 2026-10-05 |
| **Estado** | **Propuesta.** Requiere adopcion explicita del equipo |
| **Destino** | Seccion 6 del informe de configuracion |

---

## 1. Origen de estas convenciones

El caso de estudio **no prescribe** como escribir un commit, como nombrar una rama ni que
formato dar a un pull request. La seccion 7 abre declarando que *"el equipo es libre de
elegir la herramienta"* y que *"no se exige GitHub"*, y la seccion 16 asigna al equipo la
definicion de la codificacion y la nomenclatura.

Lo unico que el caso exige sobre un cambio individual son dos frases:

- Etapa 5 del flujo obligatorio: *"Modificar solamente los CI necesarios. **Cada cambio debe
  referenciar la solicitud.**"*
- Seccion 19: *"Toda modificacion debe poder relacionarse con una solicitud **o una razon
  documentada**."*

Todo lo demas de este documento son convenciones propias, adoptadas para satisfacer de forma
verificable los ocho mecanismos de la seccion 7 y las ocho reglas de consistencia de la
seccion 19.

Se incorpora ademas el patron procedimental observado en la **Guia practica 3** del caso
demostrativo SoftEdu-SCM, que separa la implementacion del cierre documental en dos pull
requests distintos.

> **Advertencia sobre la fuente.** El ejemplar disponible de la Guia practica 3 esta
> incompleto: solo pudieron recuperarse su portada, su indice y su punto de partida. El
> indice enumera los pasos 43 a 51; el detalle de cada paso no esta disponible. La Guia
> practica 2, que contiene los pasos 1 a 42, no se ha obtenido. Las secciones marcadas como
> *interpretacion* deben confirmarse contra las guias completas.

## 2. El patron de dos pull requests

### 2.1 Lo que la Guia practica 3 establece

Su indice documenta, para el cambio CR-001 ya implementado e integrado:

| Paso | Accion |
|---|---|
| 43 | Solicitar y asignar el cierre documental |
| 44 | Crear la rama `cierre-documental-cr-001` desde `main` |
| 45 | Corregir `TRA-001` para cerrar la trazabilidad |
| 46 | Actualizar `REQ-001`, `DIS-001`, `SRC-001` y `TST-001` |
| 47 | Crear el Pull Request #3 de cierre documental |
| 48 | Revisar y aprobar el Pull Request #3 |
| 49 | Fusionar el Pull Request #3 a `main` |
| 50 | Crear `BL-002` — Linea Base 1.1 |
| 51 | Crear el tag/release `v1.1` |

Su punto de partida declara: CR-001 implementada, `PR #2` aprobado y fusionado, `Issue #1`
cerrado, linea base vigente `BL-001 / tag v1.0`.

De modo que por cada solicitud aprobada hay **dos** pull requests: uno de implementacion y
uno de cierre documental. La linea base y la etiqueta se crean **despues** de fusionar el
segundo.

### 2.2 Por que son dos (interpretacion)

El paso 45 corrige la trazabilidad, y una cadena de trazabilidad termina en el numero del
pull request y la linea base resultante — datos que **no existen todavia mientras ese pull
request esta abierto**. Ningun PR puede citar su propio merge.

De ahi se deriva el criterio de reparto que adopta este documento:

| Pull request | Contiene | Razon |
|---|---|---|
| **PR de implementacion** | Contenido: codigo, esquema, casos de prueba nuevos, registro de la ejecucion | Es lo que se revisa y se verifica. La etapa 7 exige ejecutar las pruebas antes de integrar |
| **PR de cierre documental** | Metadatos: version y estado de cada CI, trazabilidad completa con el numero del PR anterior, inventario, matriz comparativa | Solo puede escribirse una vez integrado el primero |

Esto corresponde a las etapas 9 y 10 del flujo obligatorio (*"actualizacion de
configuracion"* y *"nueva linea base"*), que el caso de estudio ya enumera como etapas
separadas de la implementacion y la integracion.

### 2.3 Cuando NO aplica

El patron de dos PR aplica a **cambios sobre una linea base existente**. No aplica a la
construccion de LB-1.0, que no es un cambio sino el establecimiento del estado inicial: la
seccion 8 la trata como un procedimiento propio, cuyo paso 6 es *"asignar version 1.0 a los
CI que forman parte del estado inicial aprobado"*. Durante esa construccion los CI pueden
declarar `LB-1.0` en su cabecera sin esperar a ningun merge.

## 3. Convenciones adoptadas

### 3.1 Ramas

| Proposito | Nombre | Origen |
|---|---|---|
| Estado principal | `main` | — |
| Construccion de LB-1.0 (artefactos de QA) | `qa/pruebas-lb-1.0` | `main` |
| Implementacion de una solicitud | `cr-001-prioridad`, `cr-002-evidencia-cierre` | `main` |
| Cierre documental de una solicitud | `cierre-documental-cr-001`, `cierre-documental-cr-002` | `main`, **despues** del merge de implementacion |

Las ramas **no se eliminan** tras el merge: son la evidencia del *"espacio de trabajo
aislado"* que exige la etapa 4, y la seccion 19 prohibe borrar evidencia.

### 3.2 Mensajes de commit

Formato: `[referencia][CI] descripcion en infinitivo`

```
[LB-1.0][PRU-001] agregar plan de pruebas con 12 casos de LB-1.0
[CR-001][PRU-002] agregar CP-011..CP-014 para verificar prioridad
[CR-001][PRU-001] actualizar version de 1.0 a 1.1
```

- La **referencia** (`LB-1.0` o `CR-00x`) satisface la etapa 5 y la tercera regla de la
  seccion 19. Para los artefactos de LB-1.0 la "razon documentada" es la construccion de la
  linea base inicial, respaldada por la seccion 8.
- El **codigo de CI** permite ver que elemento toco cada commit sin abrir el diff, lo que
  sirve al mecanismo de *"trazabilidad entre la solicitud de cambio y los artefactos
  modificados"*.
- Un commit que toque varios CI los lista: `[CR-001][PRU-001][PRU-002] ...`

### 3.3 Cuerpo del pull request

**PR de implementacion:**

```
Solicitud: CR-001
Issue: #<n>
Analisis de impacto previo: 03_Docs/pruebas/analisis-impacto/CR-001-pruebas.md
CI con contenido modificado: ESP-001, DES-001, COD-001, PRU-001, PRU-002, PRU-003
Casos de prueba: CP-011..CP-014 nuevos; CP-001, CP-007, CP-008, CP-009b ampliados
Resultado de ejecucion: 03_Docs/pruebas/resultados/CR-001-ejecucion.md
Revisor solicitado: @<otro integrante>
```

**PR de cierre documental:**

```
Solicitud: CR-001
Cierre documental de PR #<n del PR de implementacion>
CI que cambian de version:
  ESP-001  1.0 -> 1.1
  DES-001  1.0 -> 1.1
  COD-001  1.0 -> 1.1
  PRU-001  1.0 -> 1.1
  PRU-002  1.0 -> 1.1
  PRU-003  1.0 -> 1.1
CI que NO cambian y por que: DOC-001 permanece en 1.0, el cambio no altera su contenido
Trazabilidad: CR-001 -> RF-xxx -> DES-001 -> COD-001 -> CP-011..CP-014 -> PR #<n> -> LB-1.1
Linea base resultante: LB-1.1 (tag v1.1), a crear una vez fusionado
Revisor solicitado: @<otro integrante>
```

El campo *"CI que NO cambian y por que"* existe porque la seccion 9 del caso exige que *"el
equipo debe justificar por que un CI cambia o permanece igual"*, y es una pregunta directa de
la sustentacion.

### 3.4 Lineas base y etiquetas

Se adopta el par **linea base + etiqueta** que usa la guia del docente:

| Linea base | Etiqueta en Git | Momento de creacion |
|---|---|---|
| `LB-1.0` | `v1.0` | Tras fusionar el PR de construccion y con verificacion aprobada |
| `LB-1.1` | `v1.1` | Tras fusionar el PR de cierre documental de CR-001 |
| `LB-1.2` | `v1.2` | Tras fusionar el PR de cierre documental de CR-002 |

La linea base nombra el **conjunto aprobado de CI**; la etiqueta es el **punto recuperable**
en el repositorio. Mantener los dos identificadores responde la pregunta de sustentacion
*"que diferencia existe entre la version de un CI y la version o identificador de una linea
base"*.

La seccion 19 condiciona su creacion: *"las etiquetas o lineas base deben crearse unicamente
cuando el conjunto ha sido revisado y aprobado"*. Nunca antes del merge ni antes de la
verificacion.

### 3.5 Operaciones prohibidas

Derivadas de una sola regla de la seccion 19: *"No se permite borrar evidencia para 'limpiar'
el historial. La historia del producto hace parte del ejercicio."*

| Prohibido | Efecto que lo prohibe |
|---|---|
| `git push --force` | Reescribe historia publicada |
| `git rebase` sobre commits ya subidos | Reescribe historia publicada |
| `git commit --amend` de algo ya subido | Reescribe historia publicada |
| *Squash and merge* | Colapsa los commits: desaparece el orden en que ocurrieron los hechos |
| Borrar ramas tras el merge | Elimina la evidencia del trabajo aislado de la etapa 4 |
| Borrar o eliminar el registro de CR-003 | *"Una solicitud rechazada no modifica el producto, pero si deja evidencia de analisis y decision"* |
| Commitear directo a `main` | *"Una solicitud aprobada no debe aparecer directamente en la rama principal sin evidencia del flujo de revision"* |

Se usa **Merge pull request** (merge commit), no *squash* ni *rebase and merge*.

### 3.6 Revision

La seccion 14 establece que *"la revision y aprobacion de un cambio no deberian recaer
exclusivamente en la misma persona que lo implemento"*. En consecuencia:

- Quien abre un PR no lo aprueba.
- Los artefactos producidos por QA requieren la revision de otro integrante. Por eso
  `PRU-001` y `PRU-002` permanecen en estado **En revision** y no **Aprobado**.
- QA revisa los PR de implementacion verificando, segun la etapa 6, *"consistencia, alcance,
  versionamiento y trazabilidad"*, y ademas que no se hayan eliminado casos de prueba para
  hacer pasar la suite.

## 4. Secuencia completa

### 4.1 Fase actual — construccion de LB-1.0 (un solo PR)

Rama `qa/pruebas-lb-1.0`, abierta desde `main` una vez que el codigo del producto quedo
restituido. Sustituye a `qa/lb-1.0-artefactos`, que se conserva sin fusionar en `origin`
como evidencia fechada del orden en que se produjeron los artefactos: el plan antes que la
suite, y los analisis de impacto antes de toda implementacion. Borrarla eliminaria esa
evidencia, que la seccion 19 protege.

Los commits van **en este orden**, por la misma razon:

| # | Commit | Por que en esa posicion |
|---|---|---|
| 1 | `[LB-1.0] agregar .gitignore, requirements.txt y pytest.ini` | Subsana los hallazgos H-02 y H-04. La reproducibilidad primero |
| 2 | `[LB-1.0][PRU-001] agregar plan de pruebas con 12 casos de LB-1.0` | El plan antes que la suite: los casos derivan de la especificacion |
| 3 | `[LB-1.0][PRU-002] agregar suite automatizada con 26 casos` | Implementa el plan del commit anterior |
| 4 | `[LB-1.0][PRU-003] registrar ejecucion 1 y siete hallazgos de configuracion` | Requiere que la suite exista |
| 5 | `[CR-001][CR-002][CR-003] agregar analisis de impacto de pruebas` | Fechado antes de cualquier implementacion, como exige la seccion 12 |
| 6 | `[LB-1.0] agregar informe de configuracion` | Al final: referencia todo lo anterior |

Luego: PR hacia `main`, revision de otro integrante, merge. **El tag `v1.0` no se crea
todavia**: `PRU-003` registra que LB-1.0 no cumple su criterio de salida.

El commit 5 lleva tres referencias porque un solo analisis cubre las tres solicitudes y
ninguna esta aun aprobada; no modifica el producto, solo registra el analisis previo.

### 4.2 Por cada solicitud aprobada — dos PR

```
 1. Registrar la solicitud como Issue                        etapa 1
 2. Analisis de impacto en la rama o adjunto al Issue         etapa 2  (QA ya lo aporto)
 3. Decision del comite, registrada en el Issue               etapa 3
 4. Rama cr-00x-<nombre> desde main                           etapa 4
 5. Commits [CR-00x][CI] con contenido                        etapa 5
 6. PR de implementacion -> revision de otro integrante       etapa 6
 7. QA ejecuta la suite y registra el resultado               etapa 7
 8. Merge del PR de implementacion                            etapa 8
 9. Rama cierre-documental-cr-00x desde main
10. Commits de version, estado y trazabilidad                 etapa 9
11. PR de cierre documental -> revision -> merge
12. Crear LB-1.x y el tag v1.x                                etapa 10
```

Las doce acciones cubren las diez etapas del flujo obligatorio. Las acciones 9 a 11 son el
cierre documental que la Guia practica 3 trata como un PR independiente.

### 4.3 CR-003 — solicitud rechazada

```
1. Registrar la solicitud como Issue                          etapa 1
2. Analisis de impacto                                        etapa 2  (QA ya lo aporto)
3. Decision: rechazada, registrada en el Issue                etapa 3
4. Cerrar el Issue como rechazado, sin eliminarlo
```

No hay rama, ni PR, ni commits sobre el producto, ni linea base nueva. El analisis y la
decision quedan como evidencia. Se conserva LB-1.2.

## 5. Pendiente de confirmar

| Punto | Como se resuelve |
|---|---|
| Detalle de los pasos 43 a 51 | Obtener la Guia practica 3 completa |
| Pasos 1 a 42: repositorio, inventario, BL-001, Issue, PR de implementacion | Obtener la Guia practica 2 |
| Donde se registran formalmente las solicitudes | Decision del equipo. Issues de GitHub es lo coherente con el resto |
| Nomenclatura de los CI del producto | Decision del equipo. Las guias usan `REQ/DIS/SRC/TST/TRA`; el borrador del equipo usa `ESP/DES/COD/PRU` |
