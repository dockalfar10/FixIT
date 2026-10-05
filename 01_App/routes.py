from flask import Blueprint, flash, redirect, render_template, request, url_for

from .database import get_connection
from .services import (
    asignar_tecnico,
    cambiar_estado,
    crear_cliente,
    crear_equipo,
    crear_solicitud,
    crear_tecnico,
    listar_solicitudes_abiertas,
    obtener_solicitud,
)

bp = Blueprint("main", __name__)


def _clientes():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, nombre, telefono, email FROM cliente ORDER BY nombre"
        ).fetchall()


def _tecnicos():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, nombre, telefono, email FROM tecnico ORDER BY nombre"
        ).fetchall()


def _equipos():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT e.id, e.cliente_id, e.tipo, e.descripcion,
                   c.nombre AS cliente_nombre
            FROM equipo e
            JOIN cliente c ON c.id = e.cliente_id
            ORDER BY e.id DESC
            """
        ).fetchall()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        try:
            crear_cliente(
                request.form.get("nombre", "").strip(),
                request.form.get("telefono", "").strip(),
                request.form.get("email", "").strip(),
            )
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("main.nuevo_cliente"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")
    return render_template("crear_cliente.html")


@bp.route("/tecnicos/nuevo", methods=["GET", "POST"])
def nuevo_tecnico():
    if request.method == "POST":
        try:
            crear_tecnico(
                request.form.get("nombre", "").strip(),
                request.form.get("telefono", "").strip(),
                request.form.get("email", "").strip(),
            )
            flash("Técnico registrado correctamente.", "success")
            return redirect(url_for("main.nuevo_tecnico"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")
    return render_template("crear_tecnico.html")


@bp.route("/equipos/nuevo", methods=["GET", "POST"])
def nuevo_equipo():
    clientes = _clientes()
    if request.method == "POST":
        try:
            crear_equipo(
                int(request.form["cliente_id"]),
                request.form.get("tipo", "").strip(),
                request.form.get("descripcion", "").strip(),
            )
            flash("Equipo registrado correctamente.", "success")
            return redirect(url_for("main.nuevo_equipo"))
        except (ValueError, TypeError, KeyError) as exc:
            flash(str(exc), "error")
    return render_template("crear_equipo.html", clientes=clientes)


@bp.route("/solicitudes")
def solicitudes():
    abiertas = listar_solicitudes_abiertas()
    return render_template("solicitudes.html", solicitudes=abiertas)


@bp.route("/solicitudes/nueva", methods=["GET", "POST"])
def nueva_solicitud():
    clientes = _clientes()
    tecnicos = _tecnicos()
    equipos = _equipos()

    if request.method == "POST":
        try:
            crear_solicitud(
                int(request.form["cliente_id"]),
                int(request.form["equipo_id"]),
                request.form.get("descripcion", "").strip(),
            )
            flash("Solicitud creada correctamente.", "success")
            return redirect(url_for("main.solicitudes"))
        except (ValueError, TypeError, KeyError) as exc:
            flash(str(exc), "error")

    return render_template(
        "crear_solicitud.html",
        clientes=clientes,
        tecnicos=tecnicos,
        equipos=equipos,
    )


@bp.route("/solicitudes/<int:solicitud_id>")
def detalle_solicitud(solicitud_id):
    solicitud = obtener_solicitud(solicitud_id)
    if solicitud is None:
        flash("Solicitud no encontrada.", "error")
        return redirect(url_for("main.solicitudes"))

    tecnicos = _tecnicos()
    return render_template(
        "detalle_solicitud.html",
        solicitud=solicitud,
        tecnicos=tecnicos,
    )


@bp.route("/solicitudes/<int:solicitud_id>/asignar", methods=["POST"])
def asignar_solicitud(solicitud_id):
    try:
        asignar_tecnico(solicitud_id, int(request.form["tecnico_id"]))
        flash("Técnico asignado correctamente.", "success")
    except (ValueError, TypeError, KeyError) as exc:
        flash(str(exc), "error")
    return redirect(url_for("main.detalle_solicitud", solicitud_id=solicitud_id))


@bp.route("/solicitudes/<int:solicitud_id>/estado", methods=["POST"])
def cambiar_estado_solicitud(solicitud_id):
    estado = request.form.get("estado", "").strip()
    try:
        cambiar_estado(solicitud_id, estado)
        flash("Estado actualizado correctamente.", "success")
    except (ValueError, TypeError) as exc:
        flash(str(exc), "error")
    return redirect(url_for("main.detalle_solicitud", solicitud_id=solicitud_id))
