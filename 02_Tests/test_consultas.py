"""Casos CP-007 y CP-008 - consulta de solicitudes abiertas y de detalle.

CI: PRU-002 v1.0 | Plan: PRU-001 seccion 7
Requisitos verificados: RF-007, RF-008
"""

from conftest import campo, cliente_con_equipo


def _identificadores(resultado):
    """Extrae los identificadores de una coleccion de solicitudes."""
    return {campo(fila, "id") for fila in resultado}


def test_cp_007_consultar_abiertas_excluye_cerradas(servicios, db):
    """CP-007 / RF-007: la consulta devuelve las no cerradas y excluye las cerradas.

    Verifica la interpretacion correcta de "abierta": significa no cerrada, no
    unicamente el estado ABIERTA. Una solicitud EN_PROCESO sigue estando abierta.
    """
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    def nueva(descripcion):
        return servicios.crear_solicitud(
            cliente_id=cliente_id, equipo_id=equipo_id, descripcion=descripcion
        )

    abierta = nueva("Sin encender")
    en_proceso = nueva("Cambio de disco")
    cerrada = nueva("Ya resuelta")

    servicios.cambiar_estado(solicitud_id=en_proceso, nuevo_estado="EN_PROCESO")
    servicios.cambiar_estado(solicitud_id=cerrada, nuevo_estado="CERRADA")

    resultado = servicios.listar_solicitudes_abiertas()
    presentes = _identificadores(resultado)

    assert abierta in presentes, "RF-007: una solicitud ABIERTA debe aparecer"
    assert en_proceso in presentes, (
        "RF-007: 'abiertas' son las no cerradas; una solicitud EN_PROCESO debe aparecer"
    )
    assert cerrada not in presentes, (
        "RF-007: una solicitud CERRADA no debe aparecer en la consulta de abiertas"
    )


def test_cp_007_consulta_expone_campos_requeridos(servicios, db):
    """CP-007 / RF-007: cada fila expone los campos minimos especificados."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )
    tecnico_id = servicios.crear_tecnico(
        nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com"
    )
    servicios.asignar_tecnico(solicitud_id=solicitud_id, tecnico_id=tecnico_id)

    resultado = servicios.listar_solicitudes_abiertas()
    fila = next(f for f in resultado if campo(f, "id") == solicitud_id)

    for nombre in ("id", "cliente_id", "equipo_id", "tecnico_id", "estado", "fecha_creacion"):
        assert campo(fila, nombre) is not None or nombre == "tecnico_id", (
            f"RF-007: la consulta debe exponer {nombre}"
        )
    assert campo(fila, "tecnico_id") == tecnico_id


def test_cp_008_consultar_detalle_con_relaciones(servicios, db):
    """CP-008 / RF-008: el detalle expone los datos y las tres relaciones."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="Pantalla intermitente"
    )
    tecnico_id = servicios.crear_tecnico(
        nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com"
    )
    servicios.asignar_tecnico(solicitud_id=solicitud_id, tecnico_id=tecnico_id)

    detalle = servicios.obtener_solicitud(solicitud_id)

    assert campo(detalle, "descripcion") == "Pantalla intermitente"
    assert campo(detalle, "estado") is not None
    assert campo(detalle, "fecha_creacion") is not None
    assert campo(detalle, "cliente_id") == cliente_id, "RF-008: relacion con cliente"
    assert campo(detalle, "equipo_id") == equipo_id, "RF-008: relacion con equipo"
    assert campo(detalle, "tecnico_id") == tecnico_id, "RF-008: relacion con tecnico"


def test_cp_008_detalle_de_solicitud_inexistente(servicios, db):
    """CP-008 / RF-008: consultar un identificador inexistente no da resultado valido."""
    try:
        resultado = servicios.obtener_solicitud(999999)
    except Exception:
        return  # rechazo por excepcion: comportamiento aceptable

    assert not resultado, (
        "RF-008: un identificador inexistente no debe producir un resultado valido"
    )
