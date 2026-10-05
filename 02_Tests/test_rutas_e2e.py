"""Caso CP-E2E-01 - la aplicacion arranca y sus rutas principales responden.

CI: PRU-002 v1.0 | Plan: PRU-001 seccion 7
Verifica la integridad de la linea base: que el producto es ejecutable y no solo que
sus funciones existen. Es el unico caso de nivel ruta, para no acoplar la suite a los
nombres de los campos de formulario ni a las plantillas HTML.
"""

import pytest


@pytest.mark.parametrize("ruta", ["/", "/solicitudes"])
def test_cp_e2e_01_rutas_principales_responden(client, ruta):
    """CP-E2E-01: la aplicacion se construye y las rutas principales dan HTTP 200."""
    respuesta = client.get(ruta)

    assert respuesta.status_code == 200, (
        f"La ruta {ruta} respondio {respuesta.status_code} en lugar de 200"
    )
    assert respuesta.data, f"La ruta {ruta} respondio sin contenido"
