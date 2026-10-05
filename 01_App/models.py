from dataclasses import dataclass
from typing import Optional

ESTADOS_SOLICITUD = {"ABIERTA", "ASIGNADA", "EN_PROCESO", "CERRADA"}

@dataclass
class Cliente:
    id: Optional[int]
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Tecnico:
    id: Optional[int]
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Equipo:
    id: Optional[int]
    cliente_id: int
    tipo: str
    descripcion: str

@dataclass
class Solicitud:
    id: Optional[int]
    cliente_id: int
    equipo_id: int
    tecnico_id: Optional[int]
    descripcion: str
    estado: str = "ABIERTA"
    fecha_creacion: Optional[str] = None
