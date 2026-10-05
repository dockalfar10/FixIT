"""Casos CP-002, CP-003 y CP-004 - registro de clientes, equipos y tecnicos.

CI: PRU-002 v1.0 | Plan: PRU-001 seccion 7
Requisitos verificados: RF-002, RF-003, RF-005
"""

from conftest import campo, contar


def test_cp_002_registrar_cliente(servicios, db):
    """CP-002 / RF-002: un cliente se registra con sus datos minimos."""
    cliente_id = servicios.crear_cliente(
        nombre="Ana Morales", telefono="3001234567", email="ana@correo.com"
    )

    assert cliente_id is not None, "crear_cliente() no devolvio identificador"
    assert contar(db, "cliente") == 1

    import sqlite3

    conexion = sqlite3.connect(db)
    conexion.row_factory = sqlite3.Row
    try:
        fila = conexion.execute(
            "SELECT * FROM cliente WHERE id = ?", (cliente_id,)
        ).fetchone()
    finally:
        conexion.close()

    assert fila is not None, "El cliente creado no es recuperable por su identificador"
    assert campo(fila, "nombre") == "Ana Morales", (
        "RF-002: el nombre debe conservarse sin alteracion"
    )


def test_cp_003_registrar_equipo_asociado_a_cliente(servicios, db):
    """CP-003 / RF-003: el equipo queda vinculado a su cliente propietario."""
    cliente_id = servicios.crear_cliente(
        nombre="Ana Morales", telefono="3001234567", email="ana@correo.com"
    )

    equipo_id = servicios.crear_equipo(
        cliente_id=cliente_id, tipo="Portatil", descripcion="Lenovo ThinkPad T480"
    )

    assert equipo_id is not None, "crear_equipo() no devolvio identificador"

    import sqlite3

    conexion = sqlite3.connect(db)
    conexion.row_factory = sqlite3.Row
    try:
        fila = conexion.execute(
            "SELECT * FROM equipo WHERE id = ?", (equipo_id,)
        ).fetchone()
    finally:
        conexion.close()

    assert fila is not None, "El equipo creado no es recuperable"
    assert campo(fila, "cliente_id") == cliente_id, (
        "RF-003: el equipo debe conservar la relacion con su cliente propietario"
    )
    assert campo(fila, "tipo") == "Portatil"


def test_cp_004_registrar_tecnico(servicios, db):
    """CP-004 / RF-005: un tecnico se registra y queda disponible para asignacion."""
    tecnico_id = servicios.crear_tecnico(
        nombre="Luis Parra", telefono="3109876543", email="luis@fixit.com"
    )

    assert tecnico_id is not None, "crear_tecnico() no devolvio identificador"
    assert contar(db, "tecnico") == 1

    import sqlite3

    conexion = sqlite3.connect(db)
    conexion.row_factory = sqlite3.Row
    try:
        fila = conexion.execute(
            "SELECT * FROM tecnico WHERE id = ?", (tecnico_id,)
        ).fetchone()
    finally:
        conexion.close()

    assert fila is not None, "El tecnico creado no es recuperable"
    assert campo(fila, "nombre") == "Luis Parra"
