from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "fixit.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    connection = get_connection()
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS tecnico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS equipo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id)
        );
        CREATE TABLE IF NOT EXISTS solicitud (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            equipo_id INTEGER NOT NULL,
            tecnico_id INTEGER,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'ABIERTA',
            fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id),
            FOREIGN KEY (equipo_id) REFERENCES equipo(id),
            FOREIGN KEY (tecnico_id) REFERENCES tecnico(id)
        );
    """)
    connection.commit()
    connection.close()
