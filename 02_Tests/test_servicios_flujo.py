"""Casos CP-005 y CP-006 - asignacion de tecnico y cambio de estado.

CI: PRU-002 v1.1 | Plan: PRU-001 seccion 7
Requisitos verificados: RF-004, RF-006
"""

import pytest

from conftest import campo, cliente_con_equipo, exige_relacion, relacion_vacia

ESTADOS_LB_1_0 = ("ABIERTA", "ASIGNADA", "EN_PROCESO", "CERRADA")


def test_cp_005_asignar_tecnico(servicios, db):
    """CP-005 / RF-004: una solicitud nace sin tecnico y la asignacion persiste."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )
    tecnico_id = servicios.crear_tecnico(
        nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com"
    )

    inicial = servicios.obtener_solicitud(solicitud_id)
    relacion_vacia(inicial, "tecnico")  # RF-004: puede nacer sin tecnico asignado

    servicios.asignar_tecnico(solicitud_id=solicitud_id, tecnico_id=tecnico_id)

    asignada = servicios.obtener_solicitud(solicitud_id)
    exige_relacion(
        asignada, "tecnico", id_esperado=tecnico_id, nombre_esperado="Luis Parra"
    )


def test_cp_005b_asignar_tecnico_no_altera_el_estado(servicios, db):
    """CP-005b / RF-004: asignar un tecnico no debe cambiar el estado por su cuenta.

    Caso agregado en PRU-001 v1.1 a raiz de la ejecucion 2. RF-004 describe la
    asignacion de un tecnico y RF-006 atribuye el cambio de estado a una operacion
    propia (cambiar_estado). La implementacion actual de asignar_tecnico() ejecuta
    ademas "SET estado = 'ASIGNADA'", un efecto que ningun requisito declara.

    No es un detalle cosmetico. Si el efecto es deseado, debe estar en ESP-001 y ser
    verificable; si no lo es, es un defecto. Mientras ESP-001 no lo declare, este
    caso falla y sostiene el hallazgo D-01 del registro de la ejecucion 2.

    Importa para las lineas base siguientes: CR-002 impondra una precondicion al
    cierre, y un cambio de estado no declarado dentro de otra operacion es
    exactamente el tipo de camino que elude una precondicion.
    """
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )
    tecnico_id = servicios.crear_tecnico(
        nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com"
    )

    estado_previo = campo(servicios.obtener_solicitud(solicitud_id), "estado")

    servicios.asignar_tecnico(solicitud_id=solicitud_id, tecnico_id=tecnico_id)

    estado_posterior = campo(servicios.obtener_solicitud(solicitud_id), "estado")
    assert estado_posterior == estado_previo, (
        f"RF-004: asignar_tecnico() cambio el estado de '{estado_previo}' a "
        f"'{estado_posterior}'. Ningun requisito declara ese efecto. El cambio de "
        "estado corresponde a cambiar_estado() (RF-006). Hallazgo D-01."
    )


@pytest.mark.parametrize("estado", ESTADOS_LB_1_0)
def test_cp_006_cambiar_estado_a_estados_validos(servicios, db, estado):
    """CP-006 / RF-006: los cuatro estados de LB-1.0 son aceptados."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )

    servicios.cambiar_estado(solicitud_id=solicitud_id, nuevo_estado=estado)

    actual = servicios.obtener_solicitud(solicitud_id)
    assert campo(actual, "estado") == estado, (
        f"RF-006: el estado {estado} esta declarado para LB-1.0 y debe aceptarse"
    )


def test_cp_006_secuencia_completa_conserva_solo_estado_actual(servicios, db):
    """CP-006 / RF-006: tras varias transiciones se conserva unicamente el actual."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )

    for estado in ("ASIGNADA", "EN_PROCESO", "CERRADA"):
        servicios.cambiar_estado(solicitud_id=solicitud_id, nuevo_estado=estado)
        assert campo(servicios.obtener_solicitud(solicitud_id), "estado") == estado

    final = servicios.obtener_solicitud(solicitud_id)
    assert campo(final, "estado") == "CERRADA", (
        "RF-006: el sistema conserva unicamente el estado actual en esta version"
    )


def test_cp_006_rechazar_estado_no_declarado(servicios, db):
    """CP-006 / RF-006: un estado fuera de los declarados para LB-1.0 es rechazado."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id, equipo_id=equipo_id, descripcion="No enciende"
    )

    try:
        servicios.cambiar_estado(solicitud_id=solicitud_id, nuevo_estado="ARCHIVADA")
    except Exception:
        pass  # rechazo por excepcion: comportamiento aceptable

    actual = campo(servicios.obtener_solicitud(solicitud_id), "estado")
    assert actual in ESTADOS_LB_1_0, (
        f"RF-006: la solicitud quedo en el estado no declarado '{actual}'. "
        "Solo los estados de LB-1.0 deben ser alcanzables."
    )
