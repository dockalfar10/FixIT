# Guía de instalación

| Campo | Valor |
|---|---|
| Código CI | DOC-003 |
| Versión | 1.0 |
| Estado | Aprobado |
| Responsable | [SthephaniGP / Analista y Documentador] |
| Ubicación | 03_Docs/usuario/guia-instalacion.md |
| Línea base | LB 1.0 |

## 1. Requisitos previos
- Python 3.10 o superior (ajustar a la versión usada)
- Git
- Navegador web

## 2. Obtener el código
```bash
git clone [URL del repositorio]
cd FIXIT
```

Para recuperar una línea base concreta:
```bash
git checkout LB-1.0
```

## 3. Entorno virtual y dependencias
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Ejecución
```bash
python run.py
```
Abrir `http://127.0.0.1:5000`.

## 5. Ejecución de pruebas
```bash
pytest
```

## 6. Problemas comunes
| Problema | Solución |
|---|---|
| `ModuleNotFoundError` | Activar el entorno virtual e instalar dependencias |
| Puerto ocupado | Cambiar el puerto en run.py |

## Historial de cambios del documento
| Versión | Fecha | Solicitud | Descripción |
|---|---|---|---|
| 1.0 | [23/09/2026] | Línea base inicial | Versión inicial aprobada |
