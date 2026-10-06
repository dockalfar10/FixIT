"""Casos CP-001, CP-009 y CP-010 - creacion e identificacion de solicitudes.

CI: PRU-002 v1.1 | Plan: PRU-001 seccion 7
Requisitos verificados: RF-001, RF-009, RF-010
"""

import pytest

from conftest import (
    campo,
    cliente_con_equipo,
    contar,
    espia_conexion,
    espia_sentencias,
    inserciones_sobre,
)


def test_cp_001_crear_solicitud_valida(servicios, db):
    """CP-001 / RF-001: una solicitud con datos completos nace en estado ABIERTA."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    solicitud_id = servicios.crear_solicitud(
        cliente_id=cliente_id,
        equipo_id=equipo_id,
        descripcion="El equipo no enciende",
    )

    assert solicitud_id is not None, "crear_solicitud() no devolvio identificador"

    solicitud = servicios.obtener_solicitud(solicitud_id)
    assert campo(solicitud, "descripcion") == "El equipo no enciende"
    assert campo(solicitud, "estado") == "ABIERTA", (
        "RF-001 exige que el sistema asigne automaticamente el estado ABIERTA"
    )
    assert campo(solicitud, "fecha_creacion") is not None, (
        "RF-001 exige registrar fecha de creacion"
    )


@pytest.mark.parametrize(
    "dato_ausente, valores, exige_cero_conexiones",
    [
        ("cliente", {"cliente_id": None}, False),
        ("equipo", {"equipo_id": None}, False),
        ("descripcion", {"descripcion": ""}, True),
    ],
)
def test_cp_009_rechazar_datos_obligatorios(
    servicios, db, monkeypatch, dato_ausente, valores, exige_cero_conexiones
):
    """CP-009 / RF-009: la aplicacion rechaza los datos obligatorios ausentes.

    Caso negativo de capa de aplicacion. Verifica tres cosas:

    1. La operacion es rechazada.
    2. No queda ningun registro en la tabla.
    3. El rechazo ocurre ANTES de abrir una conexion a la base de datos.

    El punto 3 es lo que distingue este caso de CP-009b. El esquema declara
    cliente_id y equipo_id como NOT NULL, de modo que SQLite rechazaria el INSERT
    por su cuenta incluso sin validacion en la aplicacion. Sin esta comprobacion,
    una implementacion sin ninguna validacion pasaria la prueba, y la validacion
    desapareceria el dia que alguien modifique el esquema. RF-009 atribuye la
    responsabilidad al sistema; este caso la ubica en la capa de aplicacion y
    CP-009b verifica la red de seguridad del esquema por separado.

    Correccion introducida en PRU-001 v1.1 tras la ejecucion 2. El punto 3 se
    enuncia ahora como "no se intento el INSERT", no como "no se abrio conexion":

    - "descripcion" vacia se detecta mirando el argumento. No requiere la base, y
      para esta variante se sigue exigiendo ademas cero conexiones.
    - "cliente" y "equipo" ausentes exigen comprobar que la entidad referida exista,
      y eso solo se sabe consultando. El SELECT previo es validacion legitima en la
      capa de aplicacion; lo que RF-009 prohibe es lanzar el INSERT y dejar que el
      esquema lo rechace.

    El criterio de la version 1.0 ("cero conexiones" para las tres) hacia fallar dos
    variantes contra una implementacion correcta. Pero relajarlo sin mas, dejando
    solo "no se creo registro", habria dejado pasar una implementacion sin ninguna
    validacion: se comprobo por mutacion que el caso seguia verde al retirar las dos
    comprobaciones de existencia. Mirar el SQL conserva la deteccion.
    """
    cliente_id, equipo_id = cliente_con_equipo(servicios)
    argumentos = {
        "cliente_id": cliente_id,
        "equipo_id": equipo_id,
        "descripcion": "El equipo no enciende",
    }
    argumentos.update(valores)

    antes = contar(db, "solicitud")
    conexiones = espia_conexion(monkeypatch, servicios)
    sentencias = espia_sentencias(monkeypatch, servicios)

    try:
        resultado = servicios.crear_solicitud(**argumentos)
    except Exception:
        resultado = None  # rechazo por excepcion: comportamiento aceptable

    despues = contar(db, "solicitud")
    assert despues == antes, (
        f"RF-009: se creo una solicitud sin {dato_ausente}. "
        "La validacion de datos obligatorios no se esta aplicando."
    )
    assert not resultado, (
        f"RF-009: crear_solicitud() reporto exito pese a faltar {dato_ausente}."
    )
    intentos = inserciones_sobre(sentencias, "solicitud")
    assert not intentos, (
        f"RF-009: la solicitud sin {dato_ausente} llego a intentar el INSERT y fue "
        "el esquema quien la rechazo, no la capa de aplicacion. Sentencia "
        f"ejecutada: {intentos[0][:90]}... La validacion debe ocurrir antes de "
        "intentar persistir: de lo contrario depende del esquema y desaparece si el "
        "esquema cambia."
    )

    if exige_cero_conexiones:
        assert not conexiones, (
            f"RF-009: la solicitud sin {dato_ausente} se rechazo recien al llegar a "
            "la base de datos, no en la capa de aplicacion. Se abrieron "
            f"{len(conexiones)} conexiones. Este dato es verificable sin consultar "
            "la base: la validacion debe ocurrir antes de intentar persistir, de lo "
            "contrario depende del esquema y desaparece si el esquema cambia."
        )


def test_cp_010_identificador_unico(servicios, db):
    """CP-010 / RF-010: tres solicitudes identicas reciben identificadores distintos."""
    cliente_id, equipo_id = cliente_con_equipo(servicios)

    identificadores = [
        servicios.crear_solicitud(
            cliente_id=cliente_id,
            equipo_id=equipo_id,
            descripcion="Pantalla intermitente",
        )
        for _ in range(3)
    ]

    assert all(i is not None for i in identificadores), (
        "RF-010: el sistema debe generar un identificador para cada solicitud"
    )
    assert len(set(identificadores)) == 3, (
        f"RF-010: los identificadores deben ser unicos, se obtuvo {identificadores}"
    )
