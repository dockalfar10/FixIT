# Texto para registrar las solicitudes de cambio como Issues

> **Que es este archivo.** Material de origen para crear los tres Issues en GitHub. No es un
> elemento de configuracion ni pretende sustituir el registro en la herramienta.
>
> La seccion 7 del caso de estudio advierte que, si se usan dos herramientas, *"cada
> solicitud debe conservar el mismo identificador en ambas"*. Para evitar dos fuentes de
> verdad en conflicto, el equipo debe decidir **una** sola:
>
> - **Opcion A (recomendada):** los Issues de GitHub son el registro oficial. Una vez
>   creados los tres, este archivo se elimina.
> - **Opcion B:** se mantienen documentos en el repositorio ademas de los Issues. En ese
>   caso estos tres textos pasan a ser CI (`CR-001.md`, `CR-002.md`, `CR-003.md`) y deben
>   inventariarse con sus ocho campos.
>
> Los campos *Solicitante* y *Prioridad* son propuestas: el enunciado del caso no los
> especifica y el equipo puede ajustarlos.

---

## Issue 1

**Titulo:** `CR-001 — Clasificacion por prioridad de las solicitudes de soporte`

**Etiquetas sugeridas:** `solicitud-de-cambio`, `CR-001`

**Cuerpo:**

```markdown
## Registro de la solicitud

| Campo | Valor |
|---|---|
| Identificador | CR-001 |
| Solicitante | Coordinacion de la mesa de soporte |
| Fecha de registro | <fecha> |
| Prioridad | Alta |
| Linea base vigente | LB-1.0 |
| Estado | Registrada — pendiente de analisis de impacto |

## Descripcion

Cada solicitud de soporte debe poder clasificarse en uno de cuatro niveles de prioridad:
BAJA, MEDIA, ALTA o CRITICA. Ademas, debe aplicarse una regla de atencion segun la
prioridad asignada.

## Justificacion

Actualmente todas las solicitudes se tratan por igual, sin distinguir una averia critica
que detiene la operacion de un cliente de una consulta menor. Sin un criterio de
clasificacion no es posible priorizar la atencion ni medir si los casos urgentes se
atienden antes.

## Alcance declarado

La solicitud contiene dos exigencias separables:

1. Clasificar la solicitud en cuatro niveles (dato persistido).
2. Aplicar una regla de atencion segun prioridad (comportamiento).

Una implementacion que agregue la columna sin aplicar ninguna regla no satisface esta
solicitud.

## Pendiente antes de implementar

- [ ] Analisis de impacto completo (etapa 2)
- [ ] Declarar en ESP-001 en que consiste exactamente la regla de atencion
- [ ] Decision del comite (etapa 3)

## Referencias

- Analisis de impacto sobre pruebas: `03_Docs/pruebas/analisis-impacto/CR-001-pruebas.md`
- Linea base que generaria: LB-1.1 (tag v1.1)
```

---

## Issue 2

**Titulo:** `CR-002 — Evidencia de solucion obligatoria para cerrar una solicitud`

**Etiquetas sugeridas:** `solicitud-de-cambio`, `CR-002`

**Cuerpo:**

```markdown
## Registro de la solicitud

| Campo | Valor |
|---|---|
| Identificador | CR-002 |
| Solicitante | Coordinacion de la mesa de soporte |
| Fecha de registro | <fecha> |
| Prioridad | Alta |
| Linea base vigente | LB-1.1 (prevista tras CR-001) |
| Estado | Registrada — pendiente de analisis de impacto |

## Descripcion

Para cerrar una solicitud de soporte debe registrarse obligatoriamente:

- Descripcion de la solucion aplicada
- Fecha de cierre
- Tecnico responsable del cierre

## Justificacion

Hoy una solicitud puede pasar al estado CERRADA sin dejar constancia de que se hizo para
resolverla. Eso impide responder que se le hizo a un equipo, atribuir responsabilidad sobre
la solucion y construir cualquier indicador fiable de resolucion.

## Alcance declarado

El cambio es restrictivo, no aditivo: impone una precondicion a una transicion que hoy no
la tiene. Pasar a CERRADA deja de ser siempre posible.

## Pendiente antes de implementar

- [ ] Analisis de impacto completo (etapa 2)
- [ ] Definir si el tecnico responsable del cierre es necesariamente el tecnico asignado
- [ ] Decidir que hacer con las solicitudes ya cerradas en lineas base anteriores
- [ ] Decision del comite (etapa 3)

## Referencias

- Analisis de impacto sobre pruebas: `03_Docs/pruebas/analisis-impacto/CR-002-pruebas.md`
- Linea base que generaria: LB-1.2 (tag v1.2)

## Advertencia de QA

Esta solicitud invalida tres casos de prueba vigentes, que deben adaptarse como parte de su
implementacion y no eliminarse. El detalle, con archivo y linea, esta en la seccion 3 del
analisis referenciado.
```

---

## Issue 3

**Titulo:** `CR-003 — Cierre automatico de solicitudes con mas de cinco dias abiertas`

**Etiquetas sugeridas:** `solicitud-de-cambio`, `CR-003`

**Cuerpo:**

```markdown
## Registro de la solicitud

| Campo | Valor |
|---|---|
| Identificador | CR-003 |
| Solicitante | Operacion de la mesa de soporte |
| Fecha de registro | <fecha> |
| Prioridad | Media |
| Linea base vigente | LB-1.2 |
| Estado | Registrada — pendiente de analisis de impacto |

## Descripcion

Se propone cerrar automaticamente toda solicitud que lleve mas de cinco dias abierta,
aunque no exista evidencia de solucion.

## Justificacion del solicitante

Reducir la cantidad de solicitudes abiertas acumuladas, que dificulta la operacion diaria
y distorsiona los indicadores de carga de trabajo.

## Pendiente antes de decidir

- [ ] Analisis de impacto completo (etapa 2)
- [ ] Evaluar el efecto sobre la trazabilidad y la calidad del servicio
- [ ] Evaluar la compatibilidad con la regla establecida por CR-002
- [ ] Decision del comite (etapa 3)

## Referencias

- Analisis de impacto sobre pruebas: `03_Docs/pruebas/analisis-impacto/CR-003-pruebas.md`

## Nota de procedimiento

Este Issue no debe eliminarse en ningun caso. La seccion 19 del caso de estudio establece
que *"una solicitud rechazada no modifica el producto, pero si deja evidencia de analisis y
decision"*. Si la solicitud se rechaza, el Issue se cierra registrando la decision y su
fundamento, pero permanece visible.
```

---

## Despues de crear los tres Issues

1. Anotar el numero asignado por GitHub a cada uno (`#2`, `#3`, `#4` o el que corresponda).
2. Registrarlos en la matriz de trazabilidad del informe, seccion 11.
3. Si se adopta la Opcion A, eliminar este archivo.
