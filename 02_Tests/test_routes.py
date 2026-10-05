from pathlib import Path
import importlib.util
import sys

APP_DIR = Path(__file__).resolve().parents[1] / "01_App"

def load_app():
    name = "_fixit_app"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(
        name, APP_DIR / "__init__.py",
        submodule_search_locations=[str(APP_DIR)]
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar la aplicación desde {APP_DIR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

import pytest

@pytest.fixture()
def client():
    app = load_app().create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_inicio(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"FixIT" in response.data

def test_lista_solicitudes(client):
    response = client.get("/solicitudes")
    assert response.status_code == 200
    assert b"Solicitudes abiertas" in response.data

def test_formulario_cliente(client):
    response = client.get("/clientes/nuevo")
    assert response.status_code == 200
    assert b"Registrar cliente" in response.data

def test_formulario_tecnico(client):
    response = client.get("/tecnicos/nuevo")
    assert response.status_code == 200
    assert b"Registrar t" in response.data

def test_formulario_equipo(client):
    response = client.get("/equipos/nuevo")
    assert response.status_code == 200
    assert b"Registrar equipo" in response.data

def test_formulario_solicitud(client):
    response = client.get("/solicitudes/nueva")
    assert response.status_code == 200
    assert b"Crear solicitud" in response.data
