"""Casos CP-005 y CP-006 - asignacion de tecnico y cambio de estado.

CI: PRU-002 v1.0 | Plan: PRU-001 seccion 7
Requisitos verificados: RF-004, RF-006
"""

import pytest

from conftest import campo, cliente_con_equipo

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
    assert campo(inicial, "tecnico_id") is None, (
        "RF-004: una solicitud podra encontrarse inicialmente sin tecnico asignado"
    )

    servicios.asignar_tecnico(solicitud_id=solicitud_id, tecnico_id=tecnico_id)

    asignada = servicios.obtener_solicitud(solicitud_id)
    assert campo(asignada, "tecnico_id") == tecnico_id, (
        "RF-004: el sistema debe conservar la relacion entre solicitud y tecnico"
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
