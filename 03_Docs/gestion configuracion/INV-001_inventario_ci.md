# Inventario de elementos de configuración (CI)

| Campo | Valor |
|---|---|
| Responsable | Responsable de configuración: [SthephaniGP] |
| Última actualización | [23/09/2026] |
| Línea base vigente | LB 1.0 |

## Criterio de selección
Es CI el artefacto que se identifica de forma única, cuya modificación afecta la integridad o trazabilidad del producto y que tiene versión, estado y ubicación. No son CI los archivos de soporte (`.gitignore`, `pytest.ini`, `run.py`, `__init__.py`, `__pycache__/`).

## Inventario
| Código | Nombre | Categoría | Versión | Estado | Responsable | Ubicación | Línea base |
|---|---|---|---|---|---|---|---|
| ESP-001 | Visión y alcance | Especificación | 1.0 | Aprobado | [nombre] | 03_Docs/especificacion/vision-alcance.md | LB 1.0 |
| ESP-002 | Historias de usuario | Especificación | 1.0 | Aprobado | [nombre] | 03_Docs/especificacion/historias-usuario.md | LB 1.0 |
| ESP-003 | Reglas de negocio | Especificación | 1.0 | Aprobado | [nombre] | 03_Docs/especificacion/reglas-negocio.md | LB 1.0 |
| DIS-001 | Modelo de datos | Diseño | 1.0 | Aprobado | [nombre] | 03_Docs/diseno/modelo-datos.md | LB 1.0 |
| DIS-002 | Diagrama de estados | Diseño | 1.0 | Aprobado | [nombre] | 03_Docs/diseno/diagrama-estados.md | LB 1.0 |
| DIS-003 | Arquitectura | Diseño | 1.0 | Aprobado | [nombre] | 03_Docs/diseno/arquitectura.md | LB 1.0 |
| IMP-001 | Modelos | Implementación | 1.0 | Aprobado | [nombre] | 01_App/models.py | LB 1.0 |
| IMP-002 | Lógica de negocio | Implementación | 1.0 | Aprobado | [nombre] | 01_App/services.py | LB 1.0 |
| IMP-003 | Persistencia | Implementación | 1.0 | Aprobado | [nombre] | 01_App/database.py | LB 1.0 |
| IMP-004 | Rutas | Implementación | 1.0 | Aprobado | [nombre] | 01_App/routes.py | LB 1.0 |
| IMP-005 | Plantillas de interfaz | Implementación | 1.0 | Aprobado | [nombre] | 01_App/templates/ | LB 1.0 |
| IMP-006 | Dependencias | Implementación | 1.0 | Aprobado | [nombre] | requirements.txt | LB 1.0 |
| PRU-001 | Plan de pruebas | Pruebas | 1.0 | Aprobado | [nombre] | 03_Docs/pruebas/plan-pruebas.md | LB 1.0 |
| PRU-002 | Casos de prueba | Pruebas | 1.0 | Aprobado | [nombre] | 03_Docs/pruebas/casos-prueba.md | LB 1.0 |
| PRU-003 | Pruebas automatizadas | Pruebas | 1.0 | Aprobado | [nombre] | 02_Tests/ | LB 1.0 |
| DOC-001 | README | Documentación | 1.0 | Aprobado | [nombre] | README.md | LB 1.0 |
| DOC-002 | Manual de usuario | Documentación | 1.0 | Aprobado | [nombre] | 03_Docs/usuario/manual-usuario.md | LB 1.0 |
| DOC-003 | Guía de instalación | Documentación | 1.0 | Aprobado | [nombre] | 03_Docs/usuario/guia-instalacion.md | LB 1.0 |

## Estados permitidos
Borrador, En revisión, Aprobado, En modificación, Obsoleto.
