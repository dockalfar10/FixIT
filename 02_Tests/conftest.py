"""Infraestructura comun de la suite de pruebas de FixIT.

CI: PRU-002 (Pruebas automatizadas) - version 1.1
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


# Cada relacion de una solicitud puede exponerse de dos formas igualmente validas:
# como clave ajena ("cliente_id") o como dato legible ("cliente"). Se registran las
# dos para cada una, en orden de preferencia.
RELACIONES = {
    "cliente": ("cliente_id", "cliente"),
    "equipo": ("equipo_id", "equipo"),
    "tecnico": ("tecnico_id", "tecnico"),
}


def valor_relacion(registro, base):
    """Lee la relacion 'base' tal como el registro la exponga.

    Devuelve (nombre_del_campo_encontrado, valor). Si el registro no expone la
    relacion de ninguna de las dos formas, falla el caso.

    PRU-001 v1.1 declara el contrato de RF-007 y RF-008 en estos terminos: la
    consulta y el detalle deben permitir *identificar* al cliente, al equipo y al
    tecnico de una solicitud. El plan no especifica si la relacion viaja como clave
    ajena o como dato legible, porque ambas la identifican y la eleccion corresponde
    a implementacion. Lo que si se exige es que la relacion este presente y sea
    correcta.

    La version 1.0 del plan no declaraba este contrato y la suite asumia la forma
    "cliente_id". Esa asuncion hizo fallar CP-005, CP-007 y CP-008 contra una
    implementacion que satisface el requisito exponiendo los nombres. El defecto
    estaba en el plan, no en el producto.
    """
    if base not in RELACIONES:
        raise AssertionError(f"Relacion desconocida: '{base}'")
    if registro is None:
        raise AssertionError("El registro consultado es None")

    for nombre in RELACIONES[base]:
        try:
            return nombre, campo(registro, nombre)
        except (KeyError, IndexError, AssertionError):
            continue

    formas = " ni ".join(f"'{n}'" for n in RELACIONES[base])
    raise AssertionError(
        f"El registro no expone la relacion con {base}: no se encontro {formas}. "
        "RF-007 y RF-008 exigen que la relacion sea identificable desde la consulta."
    )


def exige_relacion(registro, base, id_esperado=None, nombre_esperado=None):
    """Verifica que el registro identifique correctamente la relacion 'base'.

    Se compara contra el identificador o contra el dato legible, segun lo que la
    implementacion exponga. El llamador aporta los dos valores esperados.
    """
    nombre_campo, valor = valor_relacion(registro, base)
    esperado = id_esperado if nombre_campo.endswith("_id") else nombre_esperado
    assert valor == esperado, (
        f"La relacion con {base} se expone como '{nombre_campo}' con valor {valor!r}, "
        f"y se esperaba {esperado!r}."
    )
    return valor


def relacion_vacia(registro, base):
    """Verifica que el registro no tenga asociada la relacion 'base'.

    Se usa en CP-005, donde RF-004 declara que una solicitud "podra encontrarse
    inicialmente sin tecnico asignado".
    """
    nombre_campo, valor = valor_relacion(registro, base)
    assert valor is None, (
        f"Se esperaba que la solicitud no tuviera {base} asignado, pero "
        f"'{nombre_campo}' vale {valor!r}."
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


class _ConexionEspiada:
    """Envoltorio de una conexion que registra cada sentencia SQL ejecutada.

    Delega todo lo demas en la conexion real, de modo que la implementacion no
    percibe diferencia: execute() devuelve el cursor autentico y commit(), close()
    o cualquier otro atributo se resuelven contra el objeto original.
    """

    def __init__(self, conexion, registro):
        self._conexion = conexion
        self._registro = registro

    def execute(self, sql, *args, **kwargs):
        self._registro.append(" ".join(str(sql).split()))
        return self._conexion.execute(sql, *args, **kwargs)

    def executemany(self, sql, *args, **kwargs):
        self._registro.append(" ".join(str(sql).split()))
        return self._conexion.executemany(sql, *args, **kwargs)

    def executescript(self, sql, *args, **kwargs):
        self._registro.append(" ".join(str(sql).split()))
        return self._conexion.executescript(sql, *args, **kwargs)

    def __getattr__(self, nombre):
        return getattr(self._conexion, nombre)

    def __enter__(self):
        self._conexion.__enter__()
        return self

    def __exit__(self, *args):
        return self._conexion.__exit__(*args)


def espia_sentencias(monkeypatch, servicios_mod):
    """Instala un espia que registra el SQL ejecutado. Devuelve la lista de sentencias.

    Es la version precisa del criterio de capa que CP-009 necesita. La pregunta que
    RF-009 plantea no es "cuantas conexiones se abrieron" sino "se intento persistir
    un dato invalido". Son cosas distintas:

    - Validar que el cliente referido existe EXIGE consultar la base. Es una
      comprobacion previa legitima, y produce un SELECT.
    - Delegar la validacion en el esquema consiste en lanzar el INSERT y dejar que
      SQLite lo rechace. Eso es lo que RF-009 prohibe, y produce un INSERT.

    Contar conexiones no distingue los dos casos: ambos abren una. Mirar el SQL si.
    Por eso PRU-001 v1.1 reemplaza el criterio "cero conexiones" por "ningun INSERT
    sobre la tabla", que conserva la deteccion por mutacion para las tres variantes.
    """
    database = _modulo("database")
    original = database.get_connection
    sentencias = []

    def espia(*args, **kwargs):
        return _ConexionEspiada(original(*args, **kwargs), sentencias)

    monkeypatch.setattr(database, "get_connection", espia, raising=False)
    if hasattr(servicios_mod, "get_connection"):
        monkeypatch.setattr(servicios_mod, "get_connection", espia, raising=False)
    return sentencias


def inserciones_sobre(sentencias, tabla):
    """Filtra las sentencias que intentan insertar en una tabla."""
    marca = f"insert into {tabla.lower()}"
    return [s for s in sentencias if marca in s.lower()]
