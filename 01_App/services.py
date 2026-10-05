from .database import get_connection
from .models import ESTADOS_SOLICITUD

def crear_cliente(nombre, telefono=None, email=None):
    if not nombre or not nombre.strip(): raise ValueError("El nombre del cliente es obligatorio.")
    c = get_connection(); cur = c.execute("INSERT INTO cliente (nombre, telefono, email) VALUES (?, ?, ?)", (nombre.strip(), telefono, email)); c.commit(); r = cur.lastrowid; c.close(); return r

def crear_tecnico(nombre, telefono=None, email=None):
    if not nombre or not nombre.strip(): raise ValueError("El nombre del técnico es obligatorio.")
    c = get_connection(); cur = c.execute("INSERT INTO tecnico (nombre, telefono, email) VALUES (?, ?, ?)", (nombre.strip(), telefono, email)); c.commit(); r = cur.lastrowid; c.close(); return r

def crear_equipo(cliente_id, tipo, descripcion):
    if not tipo or not tipo.strip(): raise ValueError("El tipo de equipo es obligatorio.")
    if not descripcion or not descripcion.strip(): raise ValueError("La descripción del equipo es obligatoria.")
    c = get_connection(); cliente = c.execute("SELECT id FROM cliente WHERE id = ?", (cliente_id,)).fetchone()
    if cliente is None: c.close(); raise ValueError("El cliente indicado no existe.")
    cur = c.execute("INSERT INTO equipo (cliente_id, tipo, descripcion) VALUES (?, ?, ?)", (cliente_id, tipo.strip(), descripcion.strip())); c.commit(); r = cur.lastrowid; c.close(); return r

def crear_solicitud(cliente_id, equipo_id, descripcion):
    if not descripcion or not descripcion.strip(): raise ValueError("La descripción del problema es obligatoria.")
    c = get_connection(); cliente = c.execute("SELECT id FROM cliente WHERE id = ?", (cliente_id,)).fetchone(); equipo = c.execute("SELECT id, cliente_id FROM equipo WHERE id = ?", (equipo_id,)).fetchone()
    if cliente is None: c.close(); raise ValueError("El cliente indicado no existe.")
    if equipo is None: c.close(); raise ValueError("El equipo indicado no existe.")
    if equipo["cliente_id"] != cliente_id: c.close(); raise ValueError("El equipo no pertenece al cliente indicado.")
    cur = c.execute("INSERT INTO solicitud (cliente_id, equipo_id, descripcion, estado) VALUES (?, ?, ?, 'ABIERTA')", (cliente_id, equipo_id, descripcion.strip())); c.commit(); r = cur.lastrowid; c.close(); return r

def asignar_tecnico(solicitud_id, tecnico_id):
    c = get_connection(); s = c.execute("SELECT id FROM solicitud WHERE id = ?", (solicitud_id,)).fetchone(); t = c.execute("SELECT id FROM tecnico WHERE id = ?", (tecnico_id,)).fetchone()
    if s is None: c.close(); raise ValueError("La solicitud indicada no existe.")
    if t is None: c.close(); raise ValueError("El técnico indicado no existe.")
    c.execute("UPDATE solicitud SET tecnico_id = ?, estado = 'ASIGNADA' WHERE id = ?", (tecnico_id, solicitud_id)); c.commit(); c.close()

def cambiar_estado(solicitud_id, nuevo_estado):
    if nuevo_estado not in ESTADOS_SOLICITUD: raise ValueError("Estado de solicitud no válido.")
    c = get_connection(); s = c.execute("SELECT id FROM solicitud WHERE id = ?", (solicitud_id,)).fetchone()
    if s is None: c.close(); raise ValueError("La solicitud indicada no existe.")
    c.execute("UPDATE solicitud SET estado = ? WHERE id = ?", (nuevo_estado, solicitud_id)); c.commit(); c.close()

def listar_solicitudes_abiertas():
    c = get_connection(); rows = c.execute("""SELECT s.id, c.nombre AS cliente, e.tipo AS tipo_equipo, e.descripcion AS equipo, t.nombre AS tecnico, s.descripcion, s.estado, s.fecha_creacion FROM solicitud s JOIN cliente c ON c.id=s.cliente_id JOIN equipo e ON e.id=s.equipo_id LEFT JOIN tecnico t ON t.id=s.tecnico_id WHERE s.estado != 'CERRADA' ORDER BY s.id DESC""").fetchall(); c.close(); return [dict(r) for r in rows]

def obtener_solicitud(solicitud_id):
    c = get_connection(); r = c.execute("""SELECT s.id, c.nombre AS cliente, e.tipo AS tipo_equipo, e.descripcion AS equipo, t.nombre AS tecnico, s.descripcion, s.estado, s.fecha_creacion FROM solicitud s JOIN cliente c ON c.id=s.cliente_id JOIN equipo e ON e.id=s.equipo_id LEFT JOIN tecnico t ON t.id=s.tecnico_id WHERE s.id=?""", (solicitud_id,)).fetchone(); c.close(); return dict(r) if r else None
