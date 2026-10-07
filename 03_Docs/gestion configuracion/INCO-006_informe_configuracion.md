# Informe de Gestion de la Configuracion — FixIT

**Caso 6. FixIT — Mesa de soporte tecnico**
Ingenieria de Software 2 · Caso de estudio de Gestion de la Configuracion
Entregable 2 · Fecha de esta version: 2026-10-06 · Version 0.2

---

## Nota sobre el estado de este documento

Este informe se encuentra **en construccion**. Las secciones cuyo contenido depende de
hechos que aun no han ocurrido en el proyecto estan marcadas como pendientes, con el rol
responsable y el contenido minimo que exige el caso de estudio.

No se han redactado afirmaciones sobre lineas base no establecidas ni sobre solicitudes de
cambio no tramitadas. El caso de estudio lo prohibe expresamente: *"la documentacion no
puede afirmar una funcionalidad que el codigo no contiene si ambos forman parte de la misma
linea base"* (seccion 19).

| Seccion | Estado | Responsable |
|---|---|---|
| 1. Portada e integrantes | **Pendiente** | Equipo |
| 2. Producto y alcance inicial | **Pendiente** | Analista de cambio |
| 3. Metodo de Ingenieria de Software adoptado | **Pendiente** | Equipo |
| 4. Estructura del producto y justificacion de artefactos | **Parcial** | Responsable de configuracion |
| 5. Inventario inicial de CI | **Parcial** | Responsable de configuracion |
| 6. Herramientas y convenciones | **Parcial** | Equipo |
| 7. Descripcion de la Linea Base 1.0 | **Parcial** | Responsable de configuracion |
| 8. Gestion de CR-001 y LB-1.1 | **Pendiente** | Equipo |
| 9. Gestion de CR-002 y LB-1.2 | **Pendiente** | Equipo |
| 10. Analisis y rechazo de CR-003 | **Completa** | QA / Revisor |
| 11. Matriz final de trazabilidad | **Parcial** | Responsable de configuracion |
| 12. Comparativa de CI por linea base | **Parcial** | Responsable de configuracion |
| 13. Lecciones aprendidas | **Parcial** | Equipo |

---

## 1. Portada e integrantes

> **PENDIENTE — Responsable: equipo.**
>
> Contenido minimo: nombre del producto, asignatura, integrantes y **rol asignado a cada
> uno**. La seccion 14 del caso de estudio sugiere los roles de responsable de
> configuracion, analista de cambio, implementador, revisor, responsable de pruebas y comite
> de cambio, y advierte que *"la revision y aprobacion de un cambio no deberian recaer
> exclusivamente en la misma persona que lo implemento"*.
>
> El historial del repositorio registra hasta la fecha tres autores distintos. La asignacion
> formal de roles debe quedar escrita aqui, porque de ella depende la validez del flujo de
> revision.

---

## 2. Descripcion breve del producto y alcance inicial

> **PENDIENTE — Responsable: analista de cambio.**
>
> Contenido minimo: que hace FixIT y que permite la version inicial. El enunciado del caso
> establece el alcance de partida: *"crear una solicitud, asignarla, cambiar estado y
> consultar solicitudes abiertas"*.
>
> Material disponible para redactarla: los requisitos `RF-001` a `RF-010` ya especificados,
> y la declaracion de exclusiones de LB-1.0 (prioridad, evidencia de solucion y cierre
> automatico quedan fuera por diseno, para que los cambios posteriores sean observables).

---

## 3. Metodo o estructura de Ingenieria de Software adoptada

> **PENDIENTE — Responsable: equipo.**
>
> Contenido minimo: que enfoque se eligio (tradicional, agil o hibrido) y **por que resulta
> adecuado para este caso**. La seccion 3 del caso aclara que no se califica que un metodo
> sea mejor que otro, sino *"la coherencia entre la estructura definida, los artefactos
> seleccionados y el proceso de Gestion de la Configuracion aplicado"*.
>
> Es la primera pregunta de la sustentacion, de modo que la justificacion debe estar escrita
> y no improvisarse.

---

## 4. Estructura del producto y justificacion de los artefactos

### 4.1 Estructura actual del repositorio

```
FixIT/
├── 01_App/              Implementacion (codigo, plantillas y estaticos)
├── 02_Tests/            Pruebas automatizadas (conftest.py + 7 archivos de casos)
├── 03_Docs/             Documentacion y artefactos de gestion
│   ├── informe-configuracion.md
│   └── pruebas/
│       ├── plan-pruebas.md
│       ├── analisis-impacto/
│       │   ├── CR-001-pruebas.md
│       │   ├── CR-002-pruebas.md
│       │   └── CR-003-pruebas.md
│       └── resultados/
│           ├── LB-1.0.md               ejecucion 1
│           └── LB-1.0-ejecucion-2.md   ejecucion 2
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

### 4.2 Categorias obligatorias y su representacion

La seccion 4 del caso exige representar cinco categorias. Estado actual:

| Categoria obligatoria | Representada | Artefactos |
|---|---|---|
| Especificacion | **No en el repositorio** | `RF-001` a `RF-010` y las historias de usuario existen como borrador fuera del control de versiones |
| Diseno | **No en el repositorio** | Modelo de datos y arquitectura, idem |
| Implementacion | **Si** | `01_App/`: cinco modulos Python, 8 plantillas y la hoja de estilos. Pendiente de inventariar como `COD-001` |
| Pruebas | **Si** | `PRU-001`, `PRU-002`, `PRU-003` |
| Documentacion | **Parcial** | `README.md`, este informe |

> **PENDIENTE — Responsable: responsable de configuracion.**
>
> Dos de las cinco categorias obligatorias siguen sin representacion bajo control de
> versiones: **especificacion** y **diseno**. La de implementacion quedo cubierta al
> restituirse el codigo, pero el artefacto aun no esta inventariado como CI.
>
> La ausencia de `ESP-001` es la mas urgente: la matriz de trazabilidad de la seccion 11
> referencia `RF-001` a `RF-010`, que no existen en ninguna version controlada. Toda la
> cadena de trazabilidad arranca hoy en un documento que no esta en el repositorio.

---

## 5. Inventario inicial de elementos de configuracion

La seccion 6 del caso define los ocho campos que debe tener cada CI. Un CI debe poder
identificarse de forma unica, tener version, estado y ubicacion conocida.

### 5.1 CI de pruebas (completos)

| Codigo | Nombre | Categoria | Version | Estado | Responsable | Ubicacion | Linea base |
|---|---|---|---|---|---|---|---|
| `PRU-001` | Plan de pruebas | Pruebas | 1.1 | En revision | QA / Revisor | `03_Docs/pruebas/plan-pruebas.md` | LB-1.0 |
| `PRU-002` | Suite de pruebas automatizadas | Pruebas | 1.1 | En revision | QA / Revisor | `02_Tests/` | LB-1.0 |
| `PRU-003` | Registro de resultados de ejecucion | Pruebas | 1.1 | Aprobado | QA / Revisor | `03_Docs/pruebas/resultados/` | LB-1.0 |

Los tres pasan a 1.1 tras la ejecucion 2: `PRU-001` incorpora el contrato de retorno de
las consultas y el caso `CP-005b`; `PRU-002` implementa ambos y corrige el criterio de
capa de `CP-009`; `PRU-003` suma el registro de la ejecucion 2. Es un incremento de
version **dentro de la misma linea base**, posible porque LB-1.0 todavia no esta
etiquetada: no hay conjunto aprobado al que la version anterior pertenezca.

`PRU-001` y `PRU-002` permanecen en estado **En revision** y no **Aprobado**: fueron
elaborados por el rol de QA y la seccion 14 del caso establece que la revision y aprobacion
no deben recaer en quien produjo el artefacto. Su aprobacion requiere la revision de otro
integrante.

### 5.2 CI del producto

> **PENDIENTE — Responsable: responsable de configuracion.**
>
> Deben inventariarse los CI de especificacion (`ESP-xxx`), diseno (`DES-xxx`),
> implementacion (`COD-xxx`) y documentacion (`DOC-xxx`), con sus ocho campos.
>
> **Advertencia de consistencia.** Un borrador de inventario previo declaraba ubicaciones
> que no existen en el repositorio: `app/`, `tests/` y `docs/pruebas/`, cuando las rutas
> reales son `01_App/`, `02_Tests/` y `03_Docs/pruebas/`. La seccion 6 exige que la
> ubicacion de un CI sea conocida y verificable; un inventario que apunte a rutas
> inexistentes no cumple ese requisito. Este informe adopta las rutas reales del
> repositorio.

### 5.3 Criterio de seleccion de CI

> **PENDIENTE — Responsable: responsable de configuracion.**
>
> El caso advierte que *"el equipo no debe registrar cada archivo trivial del proyecto como
> un CI independiente"*. Debe quedar escrito por que ciertos artefactos son CI y otros no.
> Es la segunda pregunta de la sustentacion.
>
> Criterio aplicado por QA a sus propios artefactos, como referencia: se registraron como CI
> los tres artefactos de prueba cuya modificacion afecta la trazabilidad (plan, suite y
> registro de resultados), y **no** se registraron como CI los archivos de configuracion
> auxiliares (`pytest.ini`, `requirements.txt`, `.gitignore`), porque su modificacion no
> altera lo que se verifica ni la relacion entre solicitud, prueba y linea base.

---

## 6. Herramientas seleccionadas y convenciones de trabajo

### 6.1 Herramientas

| Funcion | Herramienta | Evidencia que aporta |
|---|---|---|
| Control de versiones | Git | Historial, autores, diferencias entre versiones |
| Alojamiento y revision | GitHub | Pull requests, revision antes de integrar |
| Lineas base | Etiquetas de Git (`v1.0`, `v1.1`, `v1.2`) | **Aun no utilizadas** (ver seccion 7.2) |
| Solicitudes de cambio | Por definir | — |
| Lenguaje y entorno | Python 3.12.4, Flask, SQLite | — |
| Pruebas | pytest 9.0.3 | Resultados de ejecucion registrables |

> **PENDIENTE — Responsable: equipo.** Debe definirse donde se registran formalmente las
> solicitudes de cambio (issues de GitHub, u otra herramienta). Si se usan dos herramientas,
> la seccion 7 del caso exige que *"cada solicitud conserve el mismo identificador en ambas"*.

### 6.2 Convenciones de nomenclatura

| Plano | Codigo | Significado |
|---|---|---|
| Requisito funcional | `RF-001` … `RF-010` | Requisito especificado |
| Solicitud de cambio | `CR-001`, `CR-002`, `CR-003` | Fijadas por el enunciado del caso |
| Linea base | `LB-1.0`, `LB-1.1`, `LB-1.2` | Estado aprobado del conjunto de CI |
| CI de pruebas | `PRU-001`, `PRU-002`, `PRU-003` | Artefacto de prueba bajo control de versiones |
| Caso de prueba | `CP-001` … `CP-018` | Verificacion individual, contenida en `PRU-001` |

La distincion entre `PRU-xxx` y `CP-xxx` es deliberada. Un borrador previo usaba `PRU-001`
para dos cosas distintas: el CI "plan de pruebas" y el caso de prueba "crear solicitud
valida". La seccion 6 del caso exige que un CI se identifique de forma unica, de modo que se
separaron los dos planos: los CI usan `PRU-xxx` y los casos de prueba `CP-xxx`.

### 6.3 Convenciones de prueba

| Convencion | Definicion |
|---|---|
| Comando de ejecucion | `python -m pytest` desde la raiz del proyecto |
| Configuracion | `pytest.ini`, con `testpaths = 02_Tests` |
| Niveles | **Servicio** para reglas de negocio y validaciones; **ruta** solo para verificar que la aplicacion arranca; **persistencia** para restricciones del esquema |
| Aislamiento | Cada caso recibe una base de datos SQLite temporal y vacia. Ningun caso depende del orden de ejecucion ni de otro caso |
| Derivacion | La direccion es `RF -> CP`. Ningun caso verifica comportamiento que no este especificado |
| Casos negativos | Un caso negativo tiene exito cuando la operacion **no** ocurre. Se verifica el rechazo, la ausencia de registro y la capa en que se rechaza |
| Reproducibilidad | `requirements.txt` fija las dependencias. `.gitignore` excluye `__pycache__/`, cache derivada que nunca debe versionarse |
| Validacion de la suite | Las pruebas se validan por mutacion: se inyectan defectos deliberados y se comprueba que el caso correcto falle |

### 6.4 Convenciones operativas de control de cambios

Documento de respaldo: `03_Docs/procedimiento-cambios.md`, en estado de **propuesta**
pendiente de adopcion explicita por el equipo.

El caso de estudio no prescribe formato de commit, nombres de rama ni estructura de pull
request: la seccion 7 declara que *"el equipo es libre de elegir la herramienta"* y la
seccion 16 asigna al equipo la definicion de la nomenclatura. Lo unico exigido sobre un
cambio individual es que *"cada cambio debe referenciar la solicitud"* (etapa 5) *"o una
razon documentada"* (seccion 19).

**Mensajes de commit.** Formato `[referencia][CI] descripcion en infinitivo`:

```
[LB-1.0][PRU-001] agregar plan de pruebas con 12 casos de LB-1.0
[CR-001][PRU-002] agregar CP-011..CP-014 para verificar prioridad
```

La referencia satisface la etapa 5; el codigo de CI hace visible que elemento toco cada
commit sin abrir el diff.

**Ramas.** `main` como estado principal; `cr-00x-<nombre>` para la implementacion de cada
solicitud; `cierre-documental-cr-00x` para su cierre documental. Las ramas no se eliminan
tras el merge: son la evidencia del espacio de trabajo aislado que exige la etapa 4.

**Patron de dos pull requests.** Por cada solicitud aprobada se abren dos pull requests
distintos, siguiendo el procedimiento del caso demostrativo SoftEdu-SCM documentado en la
Guia practica 3:

| Pull request | Contiene | Razon |
|---|---|---|
| Implementacion | Codigo, esquema, casos de prueba nuevos, registro de la ejecucion | Es lo que se revisa y verifica antes de integrar (etapas 6 y 7) |
| Cierre documental | Version y estado de cada CI, trazabilidad completa, inventario, matriz | Solo puede escribirse una vez integrado el primero (etapa 9) |

La separacion responde a una restriccion logica: la cadena de trazabilidad termina en el
numero del pull request y la linea base resultante, datos que no existen mientras ese pull
request esta abierto. Ningun PR puede citar su propio merge.

La linea base y su etiqueta se crean **despues** de fusionar el PR de cierre documental,
conforme a la seccion 19: *"las etiquetas o lineas base deben crearse unicamente cuando el
conjunto ha sido revisado y aprobado"*.

Este patron no aplica a la construccion de LB-1.0, que no es un cambio sobre una linea base
existente sino el establecimiento del estado inicial, y que la seccion 8 trata como un
procedimiento propio.

**Lineas base y etiquetas.** Se adopta el par identificador de linea base mas etiqueta de
Git: `LB-1.0`/`v1.0`, `LB-1.1`/`v1.1`, `LB-1.2`/`v1.2`. La linea base nombra el conjunto
aprobado de CI; la etiqueta es el punto recuperable en el repositorio.

**Operaciones prohibidas.** Derivadas de la seccion 19 (*"no se permite borrar evidencia
para 'limpiar' el historial"*): `push --force`, `rebase` o `commit --amend` sobre commits ya
publicados, *squash and merge*, eliminacion de ramas fusionadas y eliminacion del registro
de CR-003. Se integra con merge commit.

**Revision.** Quien abre un pull request no lo aprueba (seccion 14).

## 7. Descripcion de la Linea Base 1.0

### 7.1 Historial del repositorio

| Commit | Fecha | Mensaje |
|---|---|---|
| `2543860` | 2026-09-29 | Initial commit |
| `e23ab70` | 2026-10-04 | `[LB-1.0] baseline: establecer linea base del proyecto` |
| `c3dc32a` | 2026-10-05 | Merge pull request #1 from dockalfar10/implementacion |
| `d7cf46f`, `9346f11` | 2026-10-06 | Sincronizar implementacion con main — **restitucion del codigo fuente** |
| `5750319` | 2026-10-06 | Excluir archivos locales del repositorio (`.gitignore`) |
| `ede4e08` | 2026-10-06 | Merge pull request #2 from dockalfar10/implementacion |

Ramas: `main`, `implementacion`, `qa/lb-1.0-artefactos`, `qa/pruebas-lb-1.0`.
Etiquetas: **ninguna**.

`qa/lb-1.0-artefactos` se conserva sin fusionar, de forma deliberada. Documenta el orden
en que se produjeron los artefactos de prueba cuando el producto aun no existia en el
repositorio, y esa cronologia es la evidencia de que el plan precedio a la suite y de que
los analisis de impacto se emitieron antes de toda implementacion. El trabajo vigente
continua en `qa/pruebas-lb-1.0`, abierta desde `main` ya con el codigo restituido.

### 7.2 Estado de la linea base: no establecida

**LB-1.0 no se encuentra establecida.** Dos razones independientes:

1. **No esta marcada formalmente.** El paso 8 de la seccion 8 del caso exige *"marcar
   formalmente la Linea Base 1.0 mediante tag, release, snapshot o mecanismo equivalente"*.
   El repositorio no tiene ninguna etiqueta. El commit `e23ab70` lleva `[LB-1.0]` en su
   mensaje, pero un mensaje de commit no constituye una linea base recuperable: no responde
   a la pregunta de sustentacion *"como puedo recuperar el producto tal como estaba en esa
   linea base"*.

2. **No cumple su criterio de salida.** Dos verificaciones registradas:

   | Ejecucion | Commit | Resultado | Causa |
   |---|---|---|---|
   | 1 (2026-10-05) | `c3dc32a` | 26 de 26 en error de preparacion | Los CI de implementacion no existian |
   | 2 (2026-10-06) | `ede4e08` | 26 de 27 pasan, 1 falla | Defecto **D-01** |

   La ejecucion 2 cambia la naturaleza del bloqueo. El producto ya existe, carga, arranca
   y responde; lo que queda es un unico defecto acotado: `asignar_tecnico()` cambia el
   estado de la solicitud sin que ningun requisito lo declare. QA sigue sin aprobar el
   etiquetado, pero por un punto con dos salidas posibles y de bajo costo, no por ausencia
   de producto.

La seccion 19 del caso establece que *"las etiquetas o lineas base deben crearse unicamente
cuando el conjunto ha sido revisado y aprobado"*. La ausencia de etiqueta es, en este caso,
coherente con el resultado de la verificacion.

### 7.3 Hallazgos de configuracion

Detectados durante la verificacion. El detalle completo, con severidad y efecto, esta en
`PRU-003` v1.0, seccion 5.

| N. | Hallazgo | Severidad | Estado al 2026-10-06 |
|---|---|---|---|
| H-01 | `01_App/` no contiene codigo fuente; solo bytecode en `__pycache__/` | **Critica** | Cerrado |
| H-02 | `__pycache__/` esta bajo control de versiones. Causa raiz de H-01 | Alta | **Abierto** |
| H-03 | Coexisten `.pyc` de CPython 3.12 y 3.13: dos entornos distintos sin declarar | Informativa | Cerrado |
| H-04 | No existian `requirements.txt` ni `.gitignore` | Alta | Cerrado |
| H-05 | Las 7 plantillas HTML que referencia `routes.py` no estan versionadas | Alta | Cerrado **con reserva** |
| H-06 | LB-1.0 no esta marcada con etiqueta ni mecanismo equivalente | Alta | **Abierto** |
| H-07 | El inventario de CI declara ubicaciones inexistentes | Media | Cerrado |
| H-08 | `requirements.txt` fija `pytest<9` pero la ejecucion 1 se registro con pytest 9.0.3 | Media | Cerrado |
| H-09 | Dos suites de prueba coexistian en `02_Tests/` reclamando la identidad de `PRU-002` | Alta | Cerrado |

**D-01**, el defecto del producto detectado en la ejecucion 2, se registra aparte: no es
un hallazgo de configuracion sino de comportamiento. Su descripcion y las dos resoluciones
posibles estan en `LB-1.0-ejecucion-2.md`, seccion 4.

**Reserva sobre H-05.** Las plantillas existen hoy en el repositorio, pero **no son las de
la LB-1.0 original: son una reconstruccion**. El codigo Python era reconstruible desde el
bytecode; las plantillas Jinja no se compilan y no dejaron rastro. De `routes.pyc` solo se
recuperaron sus nombres (`index.html`, `solicitudes.html`, `crear_cliente.html`,
`crear_tecnico.html`, `crear_equipo.html`, `crear_solicitud.html`,
`detalle_solicitud.html`), no su contenido.

Esto afecta una pregunta directa de sustentacion: *"como puedo recuperar el producto tal
como estaba en esa linea base"*. Para las plantillas la respuesta honesta es que no se
puede. Lo que se etiquete como `v1.0` sera un estado coherente y verificado, pero no
identico al anterior a la perdida.

### 7.4 Acciones requeridas para establecer LB-1.0

Dirigidas al rol de implementacion. Detalle en `PRU-003` v1.0, seccion 7.

1. **Resolver D-01**: declarar en `ESP-001` que la asignacion transiciona la solicitud a
   `ASIGNADA`, o retirar ese efecto de `asignar_tecnico()`. Decision del comite o del
   implementador, no de QA.
2. Retirar `__pycache__/` del control de versiones: `git rm -r --cached 01_App/__pycache__`
   (H-02, sigue abierto pese a que `.gitignore` ya lo excluye).
3. Incorporar `ESP-001` y `DES-001` al control de versiones (seccion 4.2).
4. Inventariar `COD-001` y `DOC-001` con sus ocho campos (seccion 5.2).
5. Revisar y aprobar `PRU-001` y `PRU-002`, hoy en estado *En revision*. No puede hacerlo
   QA, que los produjo (seccion 14 del caso).

Cumplido el punto 1, QA ejecuta de nuevo y registra la ejecucion 3. Si se cumple el
criterio de salida, se etiqueta LB-1.0 como `v1.0`.

---

## 8. Gestion completa de CR-001 y evidencia de LB-1.1

> **PENDIENTE — Responsable: equipo.** No puede redactarse: la solicitud no ha sido
> tramitada.
>
> Contenido minimo que exige el caso (seccion 17, entregable 4): solicitud, analisis de
> impacto, decision, implementacion, revision, pruebas, trazabilidad y LB-1.1.
>
> **Aporte de QA ya disponible:** `03_Docs/pruebas/analisis-impacto/CR-001-pruebas.md`
> contiene la fila "Pruebas" del analisis de impacto, emitida antes de cualquier
> implementacion. Declara los cuatro casos nuevos (`CP-011` a `CP-014`), los cuatro casos
> existentes que deben ampliarse, cuatro riesgos con su mitigacion, el criterio de salida
> propuesto para LB-1.1 y concepto favorable con dos condiciones previas.

---

## 9. Gestion completa de CR-002 y evidencia de LB-1.2

> **PENDIENTE — Responsable: equipo.** No puede redactarse: la solicitud no ha sido
> tramitada.
>
> Contenido minimo: el mismo del entregable 4, con LB-1.2 como resultado.
>
> **Aporte de QA ya disponible:** `03_Docs/pruebas/analisis-impacto/CR-002-pruebas.md`.
> Declara los cuatro casos nuevos (`CP-015` a `CP-018`) y, sobre todo, identifica que
> **CR-002 invalida tres pruebas vigentes** (`CP-006[CERRADA]`, `CP-006` secuencia completa y
> la precondicion de `CP-007`), con la accion de adaptacion concreta para cada una. A
> diferencia de CR-001, que es aditivo, CR-002 es restrictivo: impone una precondicion a una
> transicion que hoy no la tiene.

---

## 10. Analisis y rechazo de CR-003

**Seccion completa.** Documento de respaldo:
`03_Docs/pruebas/analisis-impacto/CR-003-pruebas.md`.

### 10.1 Solicitud y decision

CR-003 propone cerrar automaticamente toda solicitud con mas de cinco dias abierta, aunque
no exista evidencia de solucion.

**Decision: rechazada.** No genera nueva linea base; se conserva LB-1.2.

### 10.2 Fundamento del rechazo

CR-002, aprobada e implementada, establece que para cerrar una solicitud debe registrarse
descripcion de la solucion, fecha y tecnico responsable. Esa regla queda verificada por el
caso `CP-016`, que comprueba que **el cierre sin descripcion de solucion es rechazado**.

CR-003 propone exactamente la operacion que `CP-016` prohibe. Las dos solicitudes son
mutuamente excluyentes: no existe implementacion que satisfaga ambas. Aprobar CR-003
obligaria a retirar `CP-016`, es decir, a derogar una regla verificada en la linea base
inmediatamente anterior. Un cambio cuya implementacion exige borrar la verificacion de una
regla vigente no es un incremento del producto: es la reversion no declarada de una decision
del comite.

### 10.3 Impacto sobre la calidad del servicio

| Aspecto | Consecuencia |
|---|---|
| Trazabilidad | Una solicitud cerrada sin evidencia es indistinguible de una resuelta |
| Indicadores | El tiempo de resolucion deja de ser confiable: todo caso cierra antes del dia seis |
| Cliente | Veria su caso cerrado sin solucion y perderia el historial al reabrir |
| Responsabilidad | Sin tecnico responsable del cierre, no hay a quien atribuir la decision |
| Incentivo | El sistema premiaria no atender un caso: esperar cinco dias da el mismo estado final que resolverlo |

El ultimo punto es el mas grave: el cambio **vuelve indistinguible el trabajo hecho del
trabajo no hecho**.

### 10.4 Alternativas registradas

Se dejaron registradas cuatro alternativas que atenderian la necesidad sin destruir
evidencia (estado `INACTIVA` distinto de `CERRADA`, alerta sin cierre, cierre por
inactividad del cliente con motivo, e informe de antiguedad). Cualquiera requeriria
tramitarse como solicitud nueva.

### 10.5 Cierre

| Accion | Estado |
|---|---|
| Analisis realizado antes de cualquier implementacion | Si |
| Artefactos del producto modificados | **Ninguno** |
| Casos de prueba agregados o modificados | **Ninguno** |
| Nueva linea base | **Ninguna.** Se conserva LB-1.2 |
| Solicitud conservada como evidencia | Si |

El rechazo es evidencia de que el cambio fue considerado y evaluado, no de que fue ignorado.

---

## 11. Matriz final de trazabilidad

### 11.1 Cadenas de LB-1.0: requisito a caso de prueba

| Requisito | Caso | Implementacion del caso | Linea base |
|---|---|---|---|
| RF-001 | CP-001 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| RF-002 | CP-002 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-003 | CP-003 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-004 | CP-005 | `02_Tests/test_servicios_flujo.py` | LB-1.0 |
| RF-005 | CP-004 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-006 | CP-006 | `02_Tests/test_servicios_flujo.py` | LB-1.0 |
| RF-007 | CP-007 | `02_Tests/test_consultas.py` | LB-1.0 |
| RF-008 | CP-008 | `02_Tests/test_consultas.py` | LB-1.0 |
| RF-009 | CP-009 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| RF-009 | CP-009b | `02_Tests/test_esquema.py` | LB-1.0 |
| RF-010 | CP-010 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| (integridad) | CP-E2E-01 | `02_Tests/test_rutas_e2e.py` | LB-1.0 |

RF-009 tiene dos casos porque se verifican dos riesgos independientes: `CP-009` falla si se
elimina la validacion de la aplicacion y `CP-009b` falla si se debilita el esquema. Se
comprobo por mutacion que ninguno cubre el defecto del otro.

### 11.2 Cadenas previstas de las solicitudes de cambio

```
CR-001 -> ESP-001 -> DES-001 -> COD-001 -> PRU-001 v1.1 -> CP-011..CP-014
       -> PRU-002 v1.1 -> PRU-003 v1.1 -> revision PR -> LB-1.1

CR-002 -> ESP-001 -> DES-001 -> COD-001 -> PRU-001 v1.2 -> CP-015..CP-018
       -> PRU-002 v1.2 -> PRU-003 v1.2 -> revision PR -> LB-1.2

CR-003 -> analisis de impacto -> decision: RECHAZADA -> sin modificacion de CI
       -> sin nueva linea base (se conserva LB-1.2)
```

### 11.3 Eslabones pendientes

> **PENDIENTE — Responsable: responsable de configuracion.**
>
> Las cadenas anteriores cubren el tramo `requisito -> caso -> linea base`. Faltan los
> eslabones de especificacion, diseno e implementacion (`ESP-xxx`, `DES-xxx`, `COD-xxx`), que
> no pueden referenciarse mientras esos CI no esten inventariados ni versionados. Falta
> tambien el numero de PR de cada revision.

---

## 12. Tabla comparativa de CI y versiones por linea base

### 12.1 CI de pruebas

| CI | LB-1.0 | LB-1.1 | LB-1.2 | Justificacion del cambio de version |
|---|---|---|---|---|
| `PRU-001` Plan de pruebas | 1.0 | 1.1 | 1.2 | Cada solicitud aprobada incorpora casos nuevos y modifica fichas existentes |
| `PRU-002` Suite automatizada | 1.0 | 1.1 | 1.2 | Archivos nuevos por cada CR, mas la adaptacion de casos vigentes |
| `PRU-003` Registro de resultados | 1.0 | 1.1 | 1.2 | Cada linea base exige una ejecucion nueva registrada |

Los tres CI de pruebas cambian de version en las tres lineas base, y la justificacion es que
ambas solicitudes aprobadas modifican comportamiento observable. Esto difiere del ejemplo
ilustrativo de la seccion 9 del caso, donde un manual de usuario permanece en 1.0 durante
varias lineas base: alli el cambio no altera el contenido del documento, aqui si.

`PRU-002` merece una precision para la sustentacion: pasa a 1.1 por **adicion** (un archivo
nuevo, `test_prioridad.py`, sin invalidar nada) y a 1.2 por **adicion y adaptacion** (un
archivo nuevo mas tres casos vigentes que CR-002 invalida). Dos incrementos de version con
naturaleza distinta.

### 12.2 CI del producto

> **PENDIENTE — Responsable: responsable de configuracion.** Requiere que los CI de
> especificacion, diseno, implementacion y documentacion esten inventariados (seccion 5.2).
>
> El caso advierte (seccion 9) que *"una nueva linea base no obliga a que todos los CI
> cambien de version. Solo deben cambiar los elementos realmente modificados"*, y que el
> equipo debe justificar por que un CI cambia o permanece igual. Esa justificacion es una
> pregunta directa de la sustentacion.

---

## 13. Lecciones aprendidas

### 13.1 Inconsistencias encontradas

| Inconsistencia | Como se detecto | Leccion |
|---|---|---|
| El codigo fuente nunca quedo bajo control de versiones; solo su bytecode | Al preparar la ejecucion de la suite | Un `.gitignore` es parte de la linea base inicial, no un detalle posterior. Su ausencia no produce un error visible: produce un repositorio que parece completo y no lo es |
| Las plantillas HTML se perdieron sin posibilidad de recuperacion | Al recuperar los nombres de plantilla del bytecode | No todo artefacto deja rastro derivado. El codigo se reconstruye desde un `.pyc`; una plantilla Jinja, no |
| `PRU-001` identificaba a la vez un CI y un caso de prueba | Al redactar el plan de pruebas | Un esquema de codificacion debe asignar cada codigo a un unico plano. La ambiguedad no molesta al escribir, molesta al sustentar |
| El inventario de CI apuntaba a rutas inexistentes | Al contrastar el inventario con el repositorio | Un inventario es verificable o no es inventario. La ubicacion de un CI debe comprobarse contra el arbol de archivos |
| LB-1.0 se dio por establecida con un mensaje de commit | Al buscar las etiquetas del repositorio | Un mensaje de commit describe una intencion; una etiqueta crea un punto recuperable. Solo la segunda responde "como recupero el producto en esa linea base" |
| `CP-009` no detectaba la ausencia de validacion en la aplicacion | Mediante pruebas de mutacion | Una prueba que pasa puede estar pasando porque no verifica nada. La unica forma de saberlo es romper el producto a proposito y comprobar que la prueba correcta falle |
| `PRU-001` v1.0 nunca declaro el contrato de retorno de las consultas, y la suite lo invento por su cuenta | Al ejecutar contra el producto restituido: tres casos fallaban contra una implementacion correcta | Un criterio de aceptacion que no se escribe se escribe solo, dentro del codigo de la prueba, donde nadie lo revisa. El defecto no estaba en el producto sino en el plan |
| Relajar un criterio para que una prueba pase puede dejarla sin poder de deteccion | Al re-validar por mutacion despues de corregir `CP-009` | Toda correccion a una prueba debe re-validarse por mutacion. Una prueba verde que ya no detecta nada es peor que una roja: parece evidencia y no lo es |
| Coexistian dos suites reclamando ser `PRU-002` | Al abrir la rama nueva desde `main` | Trabajar aislado produce artefactos de calidad e integracion nula. Un CI con dos contenidos distintos no tiene ubicacion verificable, que es lo que la seccion 6 exige |

### 13.2 Decisiones tomadas

| Decision | Motivo |
|---|---|
| Conservar la estructura `01_App/` y `02_Tests/` en lugar de reorganizarla | Reubicar los CI exigiria una razon documentada; no existe solicitud de cambio que la respalde |
| Separar `PRU-xxx` (CI) de `CP-xxx` (casos) | Un CI debe identificarse de forma unica |
| Probar mayoritariamente en la capa de servicios | Las reglas de negocio de ambos CR viven alli; probarlas en la interfaz las acoplaria a las plantillas |
| Desdoblar RF-009 en `CP-009` y `CP-009b` | Son dos riesgos independientes: validacion de la aplicacion y restriccion del esquema |
| No incrementar `PRU-001` a 1.1 al corregir `CP-009` | El documento esta en revision y nunca fue aprobado ni incluido en una linea base etiquetada. Corregir un borrador es revisarlo, no versionarlo |
| Registrar la ejecucion fallida de LB-1.0 en lugar de esperar a tener codigo | Una verificacion con resultado negativo es evidencia fechada; omitirla dejaria sin justificar por que la linea base no se etiqueto |

### 13.3 Mejoras posibles

> **PENDIENTE — Responsable: equipo.** Esta subseccion debe recoger las mejoras que el
> equipo identifique al cerrar el caso.
>
> Propuestas desde QA: integracion continua que ejecute la suite en cada pull request, de
> modo que la verificacion no dependa de que alguien la recuerde; y una plantilla de
> solicitud de cambio que exija el analisis de impacto completo antes de permitir la
> implementacion.

---

## Historial de versiones de este informe

| Version | Fecha | Cambio |
|---|---|---|
| 0.2 | 2026-10-06 | Actualizacion tras la restitucion del producto y la ejecucion 2. Seccion 7 reescrita: historial, estado de la linea base y los nueve hallazgos con su estado. Seccion 4.2 actualizada. Seccion 5.1 con los CI de pruebas en 1.1. Cuatro lecciones aprendidas nuevas |
| 0.1 | 2026-10-05 | Estructura completa de 13 secciones segun la seccion 18 del caso. Secciones 10 completa, 4, 5, 6, 7, 11, 12 y 13 parciales con el aporte de QA. Secciones 1, 2, 3, 8 y 9 pendientes con rol responsable asignado |
