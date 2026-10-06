# Registro de resultados de ejecucion — LB-1.0

| Campo | Valor |
|---|---|
| **Codigo del CI** | PRU-003 |
| **Nombre** | Registro de resultados de ejecucion |
| **Categoria** | Pruebas |
| **Version** | 1.0 |
| **Estado** | Aprobado (registro de hecho, no requiere aprobacion de contenido) |
| **Responsable** | QA / Revisor |
| **Ubicacion** | `03_Docs/pruebas/resultados/LB-1.0.md` |
| **Linea base** | LB-1.0 |
| **Ejecucion numero** | 1 |
| **Fecha de ejecucion** | 2026-10-05 |
| **Procedencia** | Registro trasladado desde la rama `qa/lb-1.0-artefactos`, commit `8477cab`, sin modificaciones de contenido |
| **Ejecucion siguiente** | `LB-1.0-ejecucion-2.md` (2026-10-06). Este registro no se sobrescribe |

---

## 1. Resultado global

> **LB-1.0 NO cumple su criterio de salida. QA no aprueba el etiquetado de la linea base.**

| Metrica | Valor |
|---|---|
| Casos recolectados | 26 |
| Pasaron | 0 |
| Fallaron | 0 |
| Error de preparacion | 26 |
| Duracion | 0,16 s |

Causa unica: **los elementos de configuracion de implementacion no existen en el
repositorio.** La carpeta `01_App/` no contiene codigo fuente; solo conserva bytecode
compilado en `01_App/__pycache__/`. Ninguno de los modulos que la suite requiere
(`__init__.py`, `database.py`, `models.py`, `services.py`, `routes.py`) esta presente.

No se trata de defectos del producto: no hay producto que ejecutar.

## 2. Configuracion ejecutada

| Elemento | Valor |
|---|---|
| Rama | `main` |
| Commit | `c3dc32a` |
| CI ejecutado | `PRU-002` v1.0 (suite automatizada) |
| Plan de referencia | `PRU-001` v1.0 |
| CI bajo prueba | `COD-001` — **ausente** |
| Python | 3.12.4 |
| pytest | 9.0.3 |
| Flask | **no instalado** (`ModuleNotFoundError: No module named 'flask'`) |
| Comando | `python -m pytest` desde la raiz del proyecto |

## 3. Resultado por caso

Los 26 casos reportan el mismo motivo. Se listan individualmente porque el criterio de
salida de `PRU-001` se evalua caso por caso.

| Caso | Archivo | Resultado | Motivo |
|---|---|---|---|
| CP-001 | `test_servicios_solicitud.py` | ERROR | Implementacion ausente |
| CP-002 | `test_servicios_catalogo.py` | ERROR | Implementacion ausente |
| CP-003 | `test_servicios_catalogo.py` | ERROR | Implementacion ausente |
| CP-004 | `test_servicios_catalogo.py` | ERROR | Implementacion ausente |
| CP-005 | `test_servicios_flujo.py` | ERROR | Implementacion ausente |
| CP-006 | `test_servicios_flujo.py` | ERROR (6 variantes) | Implementacion ausente |
| CP-007 | `test_consultas.py` | ERROR (2 variantes) | Implementacion ausente |
| CP-008 | `test_consultas.py` | ERROR (2 variantes) | Implementacion ausente |
| CP-009 | `test_servicios_solicitud.py` | ERROR (3 variantes) | Implementacion ausente |
| CP-009b | `test_esquema.py` | ERROR (5 variantes) | Implementacion ausente |
| CP-010 | `test_servicios_solicitud.py` | ERROR | Implementacion ausente |
| CP-E2E-01 | `test_rutas_e2e.py` | ERROR (2 variantes) | Implementacion ausente |

Mensaje reportado por los 26 casos, textual:

```
Implementacion ausente: no existe 01_App/__init__.py. La carpeta 01_App no contiene
codigo fuente, solo bytecode compilado en __pycache__. Los CI de implementacion
(COD-001) no estan disponibles.
```

## 4. Evaluacion del criterio de salida de LB-1.0

`PRU-001` seccion 10 exige, para aprobar el etiquetado de LB-1.0, que pasen los casos
CP-001 a CP-010, CP-009b y CP-E2E-01, con los resultados registrados en `PRU-003`.

| Condicion | Cumple |
|---|---|
| CP-001 a CP-010 pasan | **No** |
| CP-009b pasa | **No** |
| CP-E2E-01 pasa | **No** |
| Resultados registrados | Si (este documento) |

**Conclusion: el criterio de salida no se cumple. QA no aprueba el etiquetado de LB-1.0.**

Se hace notar que LB-1.0 **no esta etiquetada** en el repositorio: `git tag` no devuelve
ninguna etiqueta. El commit `e23ab70` lleva el mensaje `[LB-1.0] baseline: establecer linea
base del proyecto`, pero un mensaje de commit no constituye una linea base recuperable. La
ausencia de etiqueta es, en este caso, coherente con el resultado de esta verificacion.

## 5. Hallazgos de configuracion

Detectados durante la preparacion de la ejecucion. No son defectos del producto sino de la
gestion de la configuracion.

| N. | Hallazgo | Severidad | Efecto |
|---|---|---|---|
| H-01 | `01_App/` no contiene codigo fuente. Solo hay bytecode en `__pycache__/`, versionado por error | **Critica** | LB-1.0 no es recuperable ni ejecutable. El CI `COD-001` no existe |
| H-02 | `01_App/__pycache__/` esta bajo control de versiones. Es un artefacto derivado, atado a la version del interprete | **Alta** | Causa raiz de H-01: se versiono la cache en lugar del fuente |
| H-03 | Coexisten `.pyc` de CPython 3.12 y 3.13 para `__init__`, lo que indica ejecucion en dos entornos distintos | Informativa | Evidencia de que no habia entorno reproducible declarado |
| H-04 | No existian `requirements.txt` ni `.gitignore` | **Alta** | El entorno no era reproducible; sin `.gitignore` se produjo H-02 |
| H-05 | Las 7 plantillas HTML referenciadas por `routes.py` no estan versionadas. Sus nombres se recuperaron del bytecode | **Alta** | La interfaz de LB-1.0 no es recuperable. Jinja no se compila, no hay forma de reconstruirlas |
| H-06 | LB-1.0 no esta marcada con etiqueta, release ni mecanismo equivalente | **Alta** | No se puede recuperar el estado inicial del producto |
| H-07 | El inventario de CI declara ubicaciones que no existen (`tests/`, `docs/pruebas/`, `app/`) frente a las reales (`02_Tests/`, `01_App/`) | Media | Un CI debe tener ubicacion conocida y verificable |

H-05 es el unico hallazgo **no subsanable**: el codigo Python es recuperable desde el
bytecode, pero las plantillas no dejaron rastro compilado.

## 6. Validacion de la propia suite

Como el producto no es ejecutable, la suite no pudo validarse contra el. Para no registrar
una suite cuya correccion no estuviera demostrada, se verifico contra una implementacion de
referencia construida al efecto, **fuera del repositorio y descartada despues**. No forma
parte de ningun CI ni de ninguna linea base.

| Comprobacion | Resultado |
|---|---|
| Sin implementacion, la suite reporta caso por caso y no aborta la recoleccion | 26 errores individuales con motivo |
| Con implementacion de referencia | 26 de 26 pasan |
| Mutante: estado inicial `CERRADA` en vez de `ABIERTA` | Fallan CP-001 y CP-007 |
| Mutante: sin validacion de datos obligatorios en la aplicacion | Fallan las 3 variantes de CP-009 |
| Mutante: consulta de abiertas sin filtrar cerradas | Falla CP-007 |
| Mutante: `NOT NULL` retirado del esquema | Fallan 2 variantes de CP-009b, y CP-009 sigue pasando |

El ultimo par confirma que CP-009 y CP-009b verifican riesgos independientes: ninguno cubre
el defecto del otro. La suite detecta defectos; no pasa por no verificar nada.

## 7. Acciones requeridas antes de una nueva ejecucion

Dirigidas al rol de implementacion. QA no las ejecuta: la seccion 14 del caso de estudio
establece que la revision y la implementacion no deben recaer en la misma persona.

1. Restituir el codigo fuente en `01_App/` (`__init__.py`, `database.py`, `models.py`,
   `services.py`, `routes.py`) con las firmas que `PRU-001` especifica.
2. Restituir las 7 plantillas HTML que `routes.py` referencia: `index.html`,
   `solicitudes.html`, `crear_cliente.html`, `crear_tecnico.html`, `crear_equipo.html`,
   `crear_solicitud.html`, `detalle_solicitud.html`.
3. Retirar `__pycache__/` del control de versiones (`git rm -r --cached`), ahora que
   `.gitignore` lo excluye.
4. Corregir el inventario de CI para que las ubicaciones coincidan con el repositorio.

Cuando se completen, QA ejecuta de nuevo y registra la ejecucion numero 2. Este registro no
se sobrescribe.

## 8. Trazabilidad de esta ejecucion

```
PRU-001 v1.0 (plan) -> PRU-002 v1.0 (suite) -> ejecucion 1 sobre commit c3dc32a
  -> PRU-003 v1.0 (este registro) -> criterio de salida de LB-1.0 NO cumplido
  -> LB-1.0 no etiquetada
```

## 9. Historial de versiones de este documento

| Version | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-10-05 | Registro de la ejecucion 1 sobre el commit `c3dc32a`. Criterio de salida de LB-1.0 no cumplido por ausencia de los CI de implementacion. Siete hallazgos de configuracion |
