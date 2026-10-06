# Plan de Pruebas — FixIT (Mesa de Soporte Tecnico)

| Campo | Valor |
|---|---|
| **Codigo del CI** | PRU-001 |
| **Nombre** | Plan de pruebas |
| **Categoria** | Pruebas |
| **Version** | 1.1 |
| **Estado** | En revision |
| **Responsable** | QA / Revisor |
| **Ubicacion** | `03_Docs/pruebas/plan-pruebas.md` |
| **Linea base** | LB-1.0 |
| **Fecha** | 2026-10-06 |

---

## 1. Objetivo

Definir los casos de prueba que verifican que FixIT cumple los requisitos funcionales
declarados en `ESP-001` (RF-001 a RF-010), y establecer los criterios que debe satisfacer
cada linea base antes de ser etiquetada formalmente.

Este documento es el catalogo de referencia. Su implementacion ejecutable es `PRU-002`
(suite automatizada, `02_Tests/`) y el resultado de cada ejecucion se registra en `PRU-003`
(`03_Docs/pruebas/resultados/`).

## 2. Alcance

Cubre la verificacion funcional del producto FixIT en sus tres lineas base:

- **LB-1.0** — alcance inicial: crear solicitud, asignar tecnico, cambiar estado y
  consultar solicitudes abiertas. Casos `CP-001` a `CP-010`, mas `CP-005b`, `CP-009b`
  y `CP-E2E-01`.
- **LB-1.1** — incremento de CR-001 (prioridad). Casos `CP-011` a `CP-014`.
- **LB-1.2** — incremento de CR-002 (evidencia de solucion). Casos `CP-015` a `CP-018`.

## 3. Fuera de alcance

No se verifican en ninguna linea base de este ejercicio:

- Rendimiento, carga o concurrencia.
- Seguridad, autenticacion o autorizacion de usuarios.
- Compatibilidad entre navegadores.
- Usabilidad o accesibilidad de la interfaz.
- Cierre automatico de solicitudes (objeto de CR-003, rechazada; ver
  `analisis-impacto/CR-003-pruebas.md`).

## 4. Nomenclatura

Se distinguen dos planos de identificacion para evitar ambiguedad en la sustentacion:

| Plano | Codigo | Significado |
|---|---|---|
| Elemento de configuracion | `PRU-001`, `PRU-002`, `PRU-003` | Artefactos de prueba bajo control de versiones |
| Caso de prueba | `CP-001` ... `CP-018` | Verificacion individual, contenida en `PRU-001` |

Un `CP-xxx` nunca es un CI: es contenido del CI `PRU-001` e implementado en el CI `PRU-002`.

## 5. Estrategia de prueba

Se emplean dos niveles:

| Nivel | Donde se ejecuta | Que verifica | Por que |
|---|---|---|---|
| **Servicio** | Funciones de `01_App/services.py` | Reglas de negocio, validaciones, transiciones de estado | Las reglas de CR-001 y CR-002 viven en esta capa; probarlas aqui las aisla de cambios en la interfaz |
| **Ruta (E2E)** | Cliente HTTP de Flask sobre `01_App/routes.py` | Que la aplicacion arranca y las rutas responden | Evidencia de que el producto es ejecutable, no solo que sus funciones existen |

La mayoria de casos son de nivel servicio. El nivel ruta se limita a `CP-E2E-01`, para no
acoplar el catalogo a los nombres de los campos de formulario ni a las plantillas HTML.

### 5.1 Contrato de retorno de las consultas

Declarado en la version 1.1, tras la ejecucion 2. `listar_solicitudes_abiertas()` y
`obtener_solicitud()` deben permitir **identificar** al cliente, al equipo y al tecnico
de una solicitud. El plan **no impone la representacion**: la relacion puede viajar como
clave ajena (`cliente_id`) o como dato legible (`cliente`). Ambas identifican y ambas
satisfacen RF-007 y RF-008; la eleccion corresponde a implementacion.

Lo que si se exige es que la relacion este presente y sea correcta. La suite lo verifica
con `valor_relacion()` y `exige_relacion()` en `conftest.py`, que aceptan cualquiera de
las dos formas.

La version 1.0 de este plan no declaraba el contrato, y la suite asumio en silencio la
forma `cliente_id`. Esa asuncion hizo fallar `CP-005`, `CP-007` y `CP-008` contra una
implementacion que cumple el requisito. El defecto estaba en el plan: un criterio de
aceptacion que no esta escrito termina escribiendose solo, y mal.

## 6. Entorno de prueba

| Elemento | Valor |
|---|---|
| Lenguaje | Python 3.12 |
| Framework de aplicacion | Flask |
| Persistencia | SQLite |
| Framework de prueba | pytest |
| Base de datos de prueba | Temporal y aislada por caso (fixture `db`), nunca la base de desarrollo |
| Comando de ejecucion | `python -m pytest -v` desde la raiz del proyecto |

Cada caso parte de una base de datos limpia. Ningun caso depende del resultado de otro ni
del orden de ejecucion.

## 7. Casos de prueba — LB-1.0

Los diez casos derivan de los requisitos funcionales de `ESP-001`. La direccion de la
derivacion es `RF -> CP`: ningun caso verifica comportamiento que no este especificado.

### CP-001 — Crear solicitud valida

| Campo | Contenido |
|---|---|
| **Verifica** | RF-001 |
| **Nivel** | Servicio |
| **Objetivo** | Una solicitud con datos completos se registra y nace en estado `ABIERTA` |
| **Precondicion** | Existe un cliente y un equipo asociado a ese cliente |
| **Datos** | `crear_solicitud(cliente_id=<valido>, equipo_id=<valido>, descripcion="El equipo no enciende")` |
| **Pasos** | 1. Crear cliente. 2. Crear equipo del cliente. 3. Crear la solicitud. 4. Recuperarla con `obtener_solicitud()` |
| **Resultado esperado** | La solicitud existe, su descripcion es la registrada, su estado es `ABIERTA` y tiene fecha de creacion |
| **Criterio de aceptacion** | El estado inicial es exactamente `ABIERTA`, asignado por el sistema y no por el usuario |

### CP-002 — Registrar cliente

| Campo | Contenido |
|---|---|
| **Verifica** | RF-002 |
| **Nivel** | Servicio |
| **Objetivo** | Un cliente se registra con sus datos minimos y queda disponible para asociar solicitudes |
| **Precondicion** | Base de datos inicializada |
| **Datos** | `crear_cliente(nombre="Ana Morales", telefono="3001234567", email="ana@correo.com")` |
| **Pasos** | 1. Crear el cliente. 2. Consultarlo por su identificador |
| **Resultado esperado** | El cliente existe con el nombre registrado y un identificador asignado por el sistema |
| **Criterio de aceptacion** | El identificador es no nulo y el nombre se conserva sin alteracion |

### CP-003 — Registrar equipo asociado a un cliente

| Campo | Contenido |
|---|---|
| **Verifica** | RF-003 |
| **Nivel** | Servicio |
| **Objetivo** | Un equipo se registra vinculado a su cliente propietario |
| **Precondicion** | Existe un cliente |
| **Datos** | `crear_equipo(cliente_id=<valido>, tipo="Portatil", descripcion="Lenovo ThinkPad T480")` |
| **Pasos** | 1. Crear cliente. 2. Crear equipo con ese `cliente_id`. 3. Consultar el equipo |
| **Resultado esperado** | El equipo existe y su `cliente_id` corresponde al cliente creado |
| **Criterio de aceptacion** | La relacion cliente-equipo se conserva; un equipo sin cliente propietario no se registra |

### CP-004 — Registrar tecnico

| Campo | Contenido |
|---|---|
| **Verifica** | RF-005 |
| **Nivel** | Servicio |
| **Objetivo** | Un tecnico se registra y queda disponible para ser asignado |
| **Precondicion** | Base de datos inicializada |
| **Datos** | `crear_tecnico(nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com")` |
| **Pasos** | 1. Crear el tecnico. 2. Consultarlo por su identificador |
| **Resultado esperado** | El tecnico existe con el nombre registrado y un identificador asignado |
| **Criterio de aceptacion** | El identificador es no nulo y el tecnico es referenciable desde una solicitud |

### CP-005 — Asignar tecnico a una solicitud

| Campo | Contenido |
|---|---|
| **Verifica** | RF-004 |
| **Nivel** | Servicio |
| **Objetivo** | Una solicitud abierta sin tecnico puede recibir uno, y la relacion se conserva |
| **Precondicion** | Existe una solicitud en estado `ABIERTA` sin tecnico, y existe un tecnico |
| **Datos** | `asignar_tecnico(solicitud_id=<valido>, tecnico_id=<valido>)` |
| **Pasos** | 1. Crear solicitud. 2. Verificar que su `tecnico_id` es nulo. 3. Asignar tecnico. 4. Recuperar la solicitud |
| **Resultado esperado** | El `tecnico_id` de la solicitud corresponde al tecnico asignado |
| **Criterio de aceptacion** | Antes de asignar, no hay tecnico (RF-004: "podra encontrarse inicialmente sin tecnico asignado"); despues, la relacion persiste. La relacion se verifica segun el contrato de la seccion 5.1 |

### CP-005b — Asignar tecnico no altera el estado

| Campo | Contenido |
|---|---|
| **Verifica** | RF-004 (alcance de la operacion) |
| **Nivel** | Servicio |
| **Objetivo** | `asignar_tecnico()` modifica unicamente la relacion con el tecnico, y no el estado de la solicitud |
| **Precondicion** | Existe una solicitud en estado `ABIERTA` sin tecnico, y existe un tecnico |
| **Datos** | `asignar_tecnico(solicitud_id, tecnico_id)` sobre una solicitud `ABIERTA` |
| **Pasos** | 1. Crear solicitud y tecnico. 2. Leer el estado. 3. Asignar tecnico. 4. Leer el estado de nuevo |
| **Resultado esperado** | El estado es el mismo antes y despues de la asignacion |
| **Criterio de aceptacion** | Toda transicion de estado ocurre a traves de `cambiar_estado()` (RF-006). Ninguna otra operacion cambia el estado por su cuenta |

Caso agregado en la version 1.1 a raiz de la ejecucion 2. La implementacion vigente
ejecuta `UPDATE solicitud SET tecnico_id = ?, estado = 'ASIGNADA'`, un efecto que ningun
requisito declara. El caso sostiene el hallazgo **D-01** y falla mientras el efecto no se
declare en `ESP-001` o se retire del codigo.

El criterio no es si el efecto es razonable, sino si esta especificado: un comportamiento
no declarado dentro de una linea base abre la brecha entre codigo y documentacion que la
seccion 19 del caso prohibe. Importa ademas para CR-002, que impondra una precondicion al
cierre: una operacion que cambia el estado por dentro es el camino natural para eludirla.

### CP-006 — Cambiar estado de una solicitud

| Campo | Contenido |
|---|---|
| **Verifica** | RF-006 |
| **Nivel** | Servicio |
| **Objetivo** | El estado de una solicitud puede modificarse a cualquiera de los estados validos de LB-1.0 |
| **Precondicion** | Existe una solicitud en estado `ABIERTA` |
| **Datos** | `cambiar_estado(solicitud_id, nuevo_estado)` para `ASIGNADA`, `EN_PROCESO` y `CERRADA` |
| **Pasos** | 1. Crear solicitud. 2. Cambiar a `EN_PROCESO`. 3. Verificar. 4. Cambiar a `CERRADA`. 5. Verificar |
| **Resultado esperado** | Cada cambio queda reflejado; la solicitud conserva unicamente su estado actual |
| **Criterio de aceptacion** | Los cuatro estados de LB-1.0 son aceptados: `ABIERTA`, `ASIGNADA`, `EN_PROCESO`, `CERRADA`. Un estado no declarado es rechazado |

### CP-007 — Consultar solicitudes abiertas

| Campo | Contenido |
|---|---|
| **Verifica** | RF-007 |
| **Nivel** | Servicio |
| **Objetivo** | La consulta devuelve las solicitudes no cerradas y excluye las cerradas |
| **Precondicion** | Existen al menos tres solicitudes: una `ABIERTA`, una `EN_PROCESO` y una `CERRADA` |
| **Datos** | `listar_solicitudes_abiertas()` |
| **Pasos** | 1. Crear las tres solicitudes y fijar sus estados. 2. Invocar la consulta |
| **Resultado esperado** | El resultado incluye la `ABIERTA` y la `EN_PROCESO`, y no incluye la `CERRADA` |
| **Criterio de aceptacion** | "Abierta" significa "no cerrada", no unicamente el estado `ABIERTA`. Cada fila expone identificador, cliente, equipo, tecnico (si existe), estado y fecha |

### CP-008 — Consultar detalle de una solicitud

| Campo | Contenido |
|---|---|
| **Verifica** | RF-008 |
| **Nivel** | Servicio |
| **Objetivo** | El detalle expone los datos de la solicitud y sus relaciones con cliente, equipo y tecnico |
| **Precondicion** | Existe una solicitud con cliente, equipo y tecnico asignado |
| **Datos** | `obtener_solicitud(solicitud_id=<valido>)` |
| **Pasos** | 1. Crear la solicitud completa y asignarle tecnico. 2. Consultar su detalle |
| **Resultado esperado** | El detalle contiene descripcion, estado, fecha y las referencias a cliente, equipo y tecnico |
| **Criterio de aceptacion** | Las tres relaciones son recuperables desde el detalle. Consultar un identificador inexistente no produce un resultado valido |

### CP-009 — Rechazar solicitud con datos obligatorios ausentes (capa de aplicacion)

| Campo | Contenido |
|---|---|
| **Verifica** | RF-009 |
| **Nivel** | Servicio |
| **Objetivo** | La aplicacion impide crear una solicitud sin cliente, sin equipo o sin descripcion, y lo hace antes de intentar persistir |
| **Precondicion** | Base de datos inicializada |
| **Datos** | Tres invocaciones invalidas: sin `cliente_id`, sin `equipo_id`, y con `descripcion` vacia |
| **Pasos** | Por cada caso: 1. Instalar un espia sobre `get_connection`. 2. Invocar `crear_solicitud()` con el dato ausente. 3. Verificar el rechazo. 4. Verificar que no se creo ningun registro. 5. Verificar que no se abrio ninguna conexion |
| **Resultado esperado** | Las tres invocaciones son rechazadas, la tabla permanece sin registros nuevos y **en ninguna se llego a ejecutar el INSERT** |
| **Criterio de aceptacion** | El rechazo es explicito (error o excepcion) y ocurre **en la capa de aplicacion**, antes de intentar el INSERT. Este es un caso negativo: su exito consiste en que la operacion NO ocurra |

La comprobacion sobre la capa no es accesoria. El esquema declara `cliente_id` y
`equipo_id` como `NOT NULL`, de modo que SQLite rechazaria el INSERT por su cuenta incluso
sin validacion en la aplicacion. Sin esta comprobacion, una implementacion sin ninguna
validacion pasaria la prueba, y la validacion desapareceria el dia que alguien modifique el
esquema. La red de seguridad del esquema se verifica por separado en CP-009b.

**Precision del criterio, version 1.1.** La version 1.0 exigia que no se abriera ninguna
conexion. Ese enunciado confunde dos cosas distintas: *validar consultando* y *delegar la
validacion en el esquema*. Comprobar que el cliente referido existe obliga a un SELECT y
es validacion legitima de la capa de aplicacion; lo que RF-009 prohibe es lanzar el INSERT
y dejar que el esquema lo rechace. El criterio correcto es por tanto **"no se ejecuto el
INSERT"**, verificado sobre el SQL que la operacion emite.

Se comprobo por mutacion que la alternativa facil —relajar la asercion a "no se creo
registro"— deja pasar una implementacion sin ninguna validacion. El criterio sobre el SQL
conserva la deteccion en las tres variantes. Para `descripcion`, que es verificable sin
consultar la base, se sigue exigiendo ademas cero conexiones.

### CP-009b — Integridad del esquema de persistencia

| Campo | Contenido |
|---|---|
| **Verifica** | RF-009 (capa de persistencia) y RF-001 (valores por defecto) |
| **Nivel** | Persistencia (SQL directo, sin pasar por la capa de servicios) |
| **Objetivo** | La base de datos rechaza por su cuenta un registro invalido, si alguna ruta de codigo eludiera la validacion de la aplicacion |
| **Precondicion** | Base de datos inicializada por `init_db()` |
| **Datos** | Sentencias `INSERT` directas con `cliente_id` nulo, `equipo_id` nulo, `descripcion` nula, y una clave ajena inexistente |
| **Pasos** | Por cada caso: 1. Abrir conexion directa. 2. Ejecutar el INSERT invalido. 3. Verificar que se produce `IntegrityError`. Ademas: insertar sin estado y verificar los valores por defecto |
| **Resultado esperado** | Las cuatro sentencias invalidas producen `IntegrityError`. Una solicitud insertada sin estado nace `ABIERTA` y con fecha de creacion |
| **Criterio de aceptacion** | Las restricciones `NOT NULL` estan declaradas, `PRAGMA foreign_keys` esta activo y se aplica, y los valores por defecto del esquema coinciden con RF-001 |

CP-009 y CP-009b verifican **riesgos distintos y no se solapan**: CP-009 falla si se
elimina la validacion de la aplicacion, y CP-009b falla si se debilita el esquema. Se
comprobo experimentalmente que ninguno de los dos cubre el defecto del otro.

### CP-010 — Identificador unico por solicitud

| Campo | Contenido |
|---|---|
| **Verifica** | RF-010 |
| **Nivel** | Servicio |
| **Objetivo** | Cada solicitud recibe un identificador unico generado por el sistema |
| **Precondicion** | Base de datos inicializada |
| **Datos** | Tres solicitudes creadas con datos identicos entre si |
| **Pasos** | 1. Crear tres solicitudes con el mismo cliente, equipo y descripcion. 2. Comparar sus identificadores |
| **Resultado esperado** | Los tres identificadores son distintos y no nulos |
| **Criterio de aceptacion** | El identificador lo genera el sistema, no el usuario, y permite localizar la solicitud para relacionarla con pruebas y evidencias |

### CP-E2E-01 — La aplicacion arranca y responde

| Campo | Contenido |
|---|---|
| **Verifica** | Integridad de LB-1.0 (seccion 8.7 del caso de estudio) |
| **Nivel** | Ruta |
| **Objetivo** | La aplicacion Flask se construye y sus rutas principales responden |
| **Precondicion** | `create_app()` disponible |
| **Datos** | Peticiones `GET` a `/` y a `/solicitudes` |
| **Pasos** | 1. Construir la aplicacion. 2. Obtener su cliente de prueba. 3. Solicitar ambas rutas |
| **Resultado esperado** | Ambas responden codigo HTTP 200 y contenido HTML |
| **Criterio de aceptacion** | Demuestra que el producto es ejecutable, no solo que sus funciones existen |

## 8. Casos previstos para las solicitudes de cambio

Se declaran aqui por anticipado para que el analisis de impacto de cada CR pueda
referenciarlos antes de la implementacion. No se implementan hasta que la solicitud
correspondiente sea aprobada.

### CR-001 — Prioridad (generaria LB-1.1, `PRU-001` v1.1)

| Caso | Verifica | Objetivo |
|---|---|---|
| `CP-011` | CR-001 | Una solicitud acepta las cuatro prioridades: `BAJA`, `MEDIA`, `ALTA`, `CRITICA` |
| `CP-012` | CR-001 | Una prioridad no declarada es rechazada |
| `CP-013` | CR-001 | Una solicitud creada sin prioridad explicita recibe el valor por defecto definido |
| `CP-014` | CR-001 | **La regla de atencion ordena las solicitudes abiertas segun prioridad** |

`CP-014` es el caso critico de CR-001: el caso de estudio exige "aplicar una regla de
atencion segun prioridad", no unicamente almacenar el campo. Una implementacion que agregue
la columna sin aplicar la regla no satisface la solicitud.

### CR-002 — Evidencia de solucion (generaria LB-1.2, `PRU-001` v1.2)

| Caso | Verifica | Objetivo |
|---|---|---|
| `CP-015` | CR-002 | Una solicitud con descripcion de solucion, fecha y tecnico responsable se cierra correctamente |
| `CP-016` | CR-002 | **El cierre sin descripcion de solucion es rechazado** |
| `CP-017` | CR-002 | Al cerrar se registran la fecha de cierre y el tecnico responsable |
| `CP-018` | CR-002 | Regresion: las transiciones a `ASIGNADA` y `EN_PROCESO` siguen funcionando sin exigir evidencia |

`CP-016` es el caso que establece la regla de negocio de CR-002 y el que hace incompatible
la propuesta de CR-003.

### CR-003 — Cierre automatico (rechazada, no genera linea base)

No se define ningun caso de prueba. Una solicitud rechazada no modifica el producto, por lo
que no hay comportamiento nuevo que verificar. El analisis de calidad que sustenta el
rechazo esta en `analisis-impacto/CR-003-pruebas.md`.

## 9. Trazabilidad requisito - caso - implementacion

| Requisito | Caso | Archivo de implementacion (`PRU-002`) | Linea base |
|---|---|---|---|
| RF-001 | CP-001 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| RF-002 | CP-002 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-003 | CP-003 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-005 | CP-004 | `02_Tests/test_servicios_catalogo.py` | LB-1.0 |
| RF-004 | CP-005 | `02_Tests/test_servicios_flujo.py` | LB-1.0 |
| RF-004 | CP-005b | `02_Tests/test_servicios_flujo.py` | LB-1.0 |
| RF-006 | CP-006 | `02_Tests/test_servicios_flujo.py` | LB-1.0 |
| RF-007 | CP-007 | `02_Tests/test_consultas.py` | LB-1.0 |
| RF-008 | CP-008 | `02_Tests/test_consultas.py` | LB-1.0 |
| RF-009 | CP-009 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| RF-009 | CP-009b | `02_Tests/test_esquema.py` | LB-1.0 |
| RF-010 | CP-010 | `02_Tests/test_servicios_solicitud.py` | LB-1.0 |
| (integridad) | CP-E2E-01 | `02_Tests/test_rutas_e2e.py` | LB-1.0 |
| CR-001 | CP-011 a CP-014 | `02_Tests/test_prioridad.py` | LB-1.1 |
| CR-002 | CP-015 a CP-018 | `02_Tests/test_evidencia_cierre.py` | LB-1.2 |

## 10. Criterios de entrada y de salida

**Criterio de entrada** (cuando puede iniciar la ejecucion de pruebas de una linea base):

1. Los requisitos afectados estan especificados y aprobados en `ESP-001`.
2. Existe implementacion en `01_App/` para el alcance declarado.
3. El entorno es reproducible: `requirements.txt` permite instalar las dependencias.
4. Para una solicitud de cambio: el analisis de impacto existe y esta aprobado.

**Criterio de salida** (cuando QA puede aprobar el etiquetado de una linea base):

| Linea base | Casos que deben pasar | Condicion adicional |
|---|---|---|
| LB-1.0 | CP-001 a CP-010, mas CP-005b, CP-009b y CP-E2E-01 | Resultados registrados en `PRU-003`, con el entorno construido desde `requirements.txt` |
| LB-1.1 | Los de LB-1.0 (regresion) mas CP-011 a CP-014 | Ningun caso de LB-1.0 se degrada |
| LB-1.2 | Los de LB-1.1 (regresion) mas CP-015 a CP-018 | Ningun caso anterior se degrada |

Mientras un criterio de salida no se cumpla, QA no aprueba el etiquetado. Esto implementa
la regla del caso de estudio segun la cual las lineas base "deben crearse unicamente cuando
el conjunto ha sido revisado y aprobado".

## 11. Registro de resultados

Cada ejecucion asociada a una linea base se registra como un documento independiente en
`03_Docs/pruebas/resultados/` (CI `PRU-003`), con: fecha, version de cada CI ejecutado,
identificador del commit, resultado por caso, y defectos detectados. No se sobrescriben
registros anteriores: la historia de ejecuciones forma parte de la evidencia.

## 12. Historial de versiones de este documento

| Version | Fecha | Cambio | Origen |
|---|---|---|---|
| 1.0 | 2026-10-05 | Version inicial: CP-001 a CP-010, CP-E2E-01, criterios de entrada y salida, y declaracion anticipada de los casos de CR-001 y CR-002 | LB-1.0 |
| 1.1 | 2026-10-06 | Declaracion del contrato de retorno de las consultas (seccion 5.1), que la version 1.0 omitia. Nuevo caso `CP-005b` por el hallazgo D-01. Precision del criterio de capa de `CP-009`: de "cero conexiones" a "no se ejecuto el INSERT". Se incrementa la version porque el documento ya fue ejecutado y registrado en `PRU-003` v1.0 | Ejecucion 2 |
| 1.0 | 2026-10-05 | Correccion durante la revision, antes de la aprobacion: CP-009 pasa a verificar la capa de aplicacion y se agrega CP-009b para el esquema. Se detecto mediante pruebas de mutacion que la version anterior de CP-009 no detectaba la ausencia de validacion en la aplicacion. No se incrementa la version porque el documento se encuentra en estado En revision y no ha sido aprobado ni incluido en una linea base etiquetada | LB-1.0 |
