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

def test_services_module_loads():
    services = load_app().services
    assert hasattr(services, "crear_cliente")
    assert hasattr(services, "crear_solicitud")
