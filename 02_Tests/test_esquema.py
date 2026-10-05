"""Caso CP-009b - integridad del esquema de persistencia.

CI: PRU-002 v1.0 | Plan: PRU-001 seccion 7
Requisito verificado: RF-009 (capa de persistencia)

Complementa a CP-009. Mientras CP-009 verifica que la aplicacion valide los datos
obligatorios antes de persistir, este caso verifica la red de seguridad del esquema:
que la base de datos rechace por su cuenta un registro invalido si alguna vez una
ruta de codigo elude la validacion de la aplicacion.

Son dos riesgos distintos y se verifican por separado:

- CP-009 falla si se elimina la validacion de la aplicacion.
- CP-009b falla si se debilita el esquema (se quita un NOT NULL o una clave ajena).

Las pruebas de este archivo operan con SQL directo, sin pasar por la capa de
servicios, porque su objeto de verificacion es el esquema y no la aplicacion.
"""

import sqlite3

import pytest

from conftest import cliente_con_equipo


@pytest.mark.parametrize(
    "columna_nula, sql",
    [
        (
            "cliente_id",
            "INSERT INTO solicitud (cliente_id, equipo_id, descripcion) VALUES (NULL, ?, ?)",
        ),
        (
            "equipo_id",
            "INSERT INTO solicitud (cliente_id, equipo_id, descripcion) VALUES (?, NULL, ?)",
        ),
    ],
)
def test_cp_009b_esquema_rechaza_columnas_obligatorias_nulas(
    servicios, db, columna_nula, sql
):
    """CP-009b / RF-009: el esquema rechaza NULL en las columnas obligatorias."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    valor_presente = equipo_id if columna_nula == "cliente_id" else cliente_id

    conexion = sqlite3.connect(db)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conexion.execute(sql, (valor_presente, "Descripcion de prueba"))
            conexion.commit()
    finally:
        conexion.close()


def test_cp_009b_esquema_rechaza_descripcion_nula(servicios, db):
    """CP-009b / RF-009: el esquema rechaza una descripcion nula."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    conexion = sqlite3.connect(db)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conexion.execute(
                "INSERT INTO solicitud (cliente_id, equipo_id, descripcion) "
                "VALUES (?, ?, NULL)",
                (cliente_id, equipo_id),
            )
            conexion.commit()
    finally:
        conexion.close()


def test_cp_009b_claves_ajenas_activas(servicios, db):
    """CP-009b / RF-009: las claves ajenas estan activas y se aplican.

    SQLite no aplica las claves ajenas si no se activa PRAGMA foreign_keys. El modulo
    database lo activa en get_connection(); este caso verifica que efectivamente
    impida referenciar un cliente inexistente.
    """
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    conexion = sqlite3.connect(db)
    conexion.execute("PRAGMA foreign_keys = ON")
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conexion.execute(
                "INSERT INTO solicitud (cliente_id, equipo_id, descripcion) "
                "VALUES (?, ?, ?)",
                (999999, equipo_id, "Cliente inexistente"),
            )
            conexion.commit()
    finally:
        conexion.close()


def test_cp_009b_estado_por_defecto_del_esquema(servicios, db):
    """CP-009b / RF-001: el esquema aplica ABIERTA como estado por omision.

    Verifica el valor por defecto declarado en la tabla, independientemente de que la
    aplicacion lo fije de forma explicita. Si el esquema cambiara ese valor, una
    solicitud insertada sin estado nacería en un estado distinto al especificado.
    """
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    conexion = sqlite3.connect(db)
    conexion.row_factory = sqlite3.Row
    try:
        cursor = conexion.execute(
            "INSERT INTO solicitud (cliente_id, equipo_id, descripcion) VALUES (?, ?, ?)",
            (cliente_id, equipo_id, "Sin estado explicito"),
        )
        conexion.commit()
        fila = conexion.execute(
            "SELECT estado, fecha_creacion FROM solicitud WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    finally:
        conexion.close()

    assert fila["estado"] == "ABIERTA", (
        "RF-001: el esquema debe declarar ABIERTA como estado por defecto"
    )
    assert fila["fecha_creacion"] is not None, (
        "RF-001: el esquema debe asignar la fecha de creacion por defecto"
    )
