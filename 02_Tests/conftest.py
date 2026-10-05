"""Infraestructura comun de la suite de pruebas de FixIT.

CI: PRU-002 (Pruebas automatizadas) - version 1.0
Plan de referencia: 03_Docs/pruebas/plan-pruebas.md (PRU-001)

Este modulo resuelve dos problemas de carga y expone las fixtures que consumen
todos los archivos de prueba.

Problema 1 - el nombre del paquete no es un identificador valido.
    La carpeta de la aplicacion se llama "01_App" y en Python un identificador no
    puede empezar por digito, de modo que "import 01_App" es imposible. La carga se
    hace registrando el paquete en sys.modules bajo el alias "fixit_app".

Problema 2 - los modulos de la aplicacion usan imports relativos.
    services.py, routes.py y __init__.py importan con "from .database import ...".
    Un import relativo solo se resuelve si el modulo se carga como parte de un
    paquete, no como archivo suelto. Por eso se construye el spec con
    submodule_search_locations, de forma que fixit_app.services pueda resolver
    .database como fixit_app.database.

Mientras no exista implementacion en 01_App, la carga falla de forma controlada: cada
caso de prueba reporta su propio fallo con el motivo, en lugar de abortar la
recoleccion completa. Esto permite que el registro de resultados (PRU-003) muestre el
estado de cada caso individualmente.
"""

import importlib
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
APP_DIR = RAIZ / "01_App"
ALIAS = "fixit_app"

# Modulos que la suite espera encontrar en el paquete de la aplicacion.
MODULOS_ESPERADOS = ("database", "models", "services", "routes")


def _cargar_paquete():
    """Registra 01_App en sys.modules como paquete 'fixit_app'.

    Devuelve (paquete, None) si la carga fue posible, o (None, motivo) si no.
    No lanza excepciones: el motivo se propaga a cada caso de prueba.
    """
    if ALIAS in sys.modules:
        return sys.modules[ALIAS], None

    init = APP_DIR / "__init__.py"
    if not init.is_file():
        return None, (
            f"Implementacion ausente: no existe {init.relative_to(RAIZ)}. "
            "La carpeta 01_App no contiene codigo fuente, solo bytecode compilado "
            "en __pycache__. Los CI de implementacion (COD-001) no estan disponibles."
        )

    faltantes = [
        m for m in MODULOS_ESPERADOS if not (APP_DIR / f"{m}.py").is_file()
    ]
    if faltantes:
        nombres = ", ".join(f"{m}.py" for m in faltantes)
        return None, (
            f"Implementacion incompleta: faltan los modulos {nombres} en 01_App/."
        )

    spec = importlib.util.spec_from_file_location(
        ALIAS, init, submodule_search_locations=[str(APP_DIR)]
    )
    paquete = importlib.util.module_from_spec(spec)
    sys.modules[ALIAS] = paquete
    try:
        spec.loader.exec_module(paquete)
    except Exception as exc:  # la implementacion existe pero no carga
        del sys.modules[ALIAS]
        return None, f"El paquete 01_App existe pero no se pudo importar: {exc!r}"
    return paquete, None


PAQUETE, MOTIVO_NO_DISPONIBLE = _cargar_paquete()


def _exigir_implementacion():
    """Falla el caso actual con el motivo exacto si no hay implementacion."""
    if PAQUETE is None:
        pytest.fail(MOTIVO_NO_DISPONIBLE, pytrace=False)


def _modulo(nombre):
    """Importa un submodulo de la aplicacion, o falla el caso con el motivo."""
    _exigir_implementacion()
    try:
        return importlib.import_module(f"{ALIAS}.{nombre}")
    except Exception as exc:
        pytest.fail(f"No se pudo importar {nombre}.py: {exc!r}", pytrace=False)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path, monkeypatch):
    """Base de datos SQLite temporal, vacia e inicializada, aislada por caso.

    Redirige DATABASE_PATH del modulo database hacia un archivo temporal antes de
    invocar init_db(), de modo que ninguna prueba toque la base de desarrollo. El
    archivo lo elimina pytest al terminar el caso.
    """
    database = _modulo("database")
    ruta = tmp_path / "fixit_prueba.sqlite3"
    monkeypatch.setattr(database, "DATABASE_PATH", ruta, raising=False)
    database.init_db()
    return ruta


@pytest.fixture()
def servicios(db):
    """Capa de servicios operando sobre la base de datos temporal."""
    return _modulo("services")


@pytest.fixture()
def modelos():
    """Modulo de modelos (dataclasses y constantes de dominio)."""
    return _modulo("models")


@pytest.fixture()
def app(db):
    """Aplicacion Flask construida con create_app(), sobre la base temporal."""
    _exigir_implementacion()
    if not hasattr(PAQUETE, "create_app"):
        pytest.fail(
            "El paquete 01_App no expone create_app().", pytrace=False
        )
    aplicacion = PAQUETE.create_app()
    aplicacion.config["TESTING"] = True
    return aplicacion


@pytest.fixture()
def client(app):
    """Cliente HTTP de prueba de Flask."""
    return app.test_client()


# ---------------------------------------------------------------------------
# Utilidades compartidas
# ---------------------------------------------------------------------------


def campo(registro, nombre):
    """Lee un campo de un registro sin asumir su representacion concreta.

    obtener_solicitud() puede devolver un sqlite3.Row, un dict o una dataclass
    Solicitud segun como se implemente. La suite no debe quedar acoplada a esa
    decision, que corresponde al equipo de implementacion: lo que el plan de pruebas
    especifica es el dato, no su envoltorio.
    """
    if registro is None:
        raise AssertionError("El registro consultado es None")
    if isinstance(registro, dict):
        return registro[nombre]
    if isinstance(registro, sqlite3.Row):
        return registro[nombre]
    if hasattr(registro, nombre):
        return getattr(registro, nombre)
    try:
        return registro[nombre]
    except Exception:
        raise AssertionError(
            f"No se pudo leer el campo '{nombre}' de un registro {type(registro).__name__}"
        )


def contar(ruta_db, tabla):
    """Cuenta filas de una tabla. Se usa en los casos negativos."""
    conexion = sqlite3.connect(ruta_db)
    try:
        return conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
    finally:
        conexion.close()


def cliente_con_equipo(servicios, nombre="Ana Morales"):
    """Precondicion frecuente: un cliente con un equipo asociado.

    Devuelve (cliente_id, equipo_id).
    """
    cliente_id = servicios.crear_cliente(
        nombre=nombre, telefono="3001234567", email="ana@correo.com"
    )
    equipo_id = servicios.crear_equipo(
        cliente_id=cliente_id, tipo="Portatil", descripcion="Lenovo ThinkPad T480"
    )
    return cliente_id, equipo_id


def espia_conexion(monkeypatch, servicios_mod):
    """Instala un espia sobre get_connection y devuelve el contador de llamadas.

    Permite distinguir en que capa se rechaza una operacion invalida:

    - Si la aplicacion valida los datos antes de persistir, nunca abre una conexion
      y el contador queda en cero.
    - Si la aplicacion delega la validacion en el esquema de la base de datos, abre
      la conexion, intenta el INSERT y recibe un IntegrityError. El contador queda
      en uno o mas.

    Se parchean las dos ubicaciones posibles del nombre, porque la ligadura depende
    de como importe el modulo de servicios:

    - "from .database import get_connection" liga el nombre en services
    - "from . import database" lo deja en database

    La suite no debe quedar acoplada a esa decision de implementacion.
    """
    database = _modulo("database")
    original = database.get_connection
    llamadas = []

    def espia(*args, **kwargs):
        llamadas.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(database, "get_connection", espia, raising=False)
    if hasattr(servicios_mod, "get_connection"):
        monkeypatch.setattr(servicios_mod, "get_connection", espia, raising=False)
    return llamadas
