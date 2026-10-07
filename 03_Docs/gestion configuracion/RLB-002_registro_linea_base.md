# Registro de líneas base

| Línea base | Tag / release | Fecha | Origen | Aprobada por | Commit |
|---|---|---|---|---|---|
| LB 1.0 | LB-1.0 | [23/09/2026] | Estado inicial | [nombre] | [hash] |
| LB 1.1 | LB-1.1 | [fecha] | CR-001 | [nombre] | [hash] |
| LB 1.2 | LB-1.2 | [fecha] | CR-002 | [nombre] | [hash] |

> CR-003 es rechazada y no genera línea base: se conserva LB 1.2.

## Composición de cada línea base
### LB 1.0
| CI | Versión |
|---|---|
| ESP-001 | 1.0 |
| ... | ... |

### LB 1.1
(Completar al cerrar CR-001. Indicar versión de todos los CI, marcando los modificados.)

### LB 1.2
(Completar al cerrar CR-002.)

## Verificación antes de marcar una línea base
- [ ] Todos los CI incluidos están en estado Aprobado.
- [ ] Pruebas ejecutadas con resultado registrado.
- [ ] Documentación coherente con el código.
- [ ] Revisión realizada por una persona distinta del implementador.
- [ ] Inventario y trazabilidad actualizados.

## Cómo recuperar una línea base
```bash
git checkout LB-1.0
```