"""
Servidor local del Proyecto 4: Resortes para animar (game feel).

    python app.py   ->   http://localhost:5000
                         http://localhost:5000/presentacion  (diapositivas)

Sirve la interfaz (static/) y una pequeña API que usa numpy para verificar la
simulación numérica (RK4) contra la solución analítica exacta.
"""
import math
from pathlib import Path

import numpy as np
from flask import Flask, abort, jsonify, request, send_from_directory

from physics import exact_position, rk4_solve, system_metrics

BASE = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE / "static"), static_url_path="/static")

MAX_POINTS = 600  # puntos que se mandan al navegador por curva


def _param(name, default, lo, hi):
    """Lee un parámetro float de la query y lo valida."""
    raw = request.args.get(name, default)
    try:
        value = float(raw)
    except (TypeError, ValueError):
        abort(400, f"Parámetro '{name}' inválido")
    if not math.isfinite(value) or not lo <= value <= hi:
        abort(400, f"'{name}' debe estar entre {lo} y {hi}")
    return value


def _verify(omega, zeta, h, t_end, x0=0.0, v0=0.0, target=1.0):
    t, x_num, _ = rk4_solve(omega, zeta, x0=x0, v0=v0, target=target, t_end=t_end, h=h)
    x_ex = exact_position(t, omega, zeta, x0=x0, v0=v0, target=target)  # mismo vector t
    err = np.abs(x_num - x_ex)
    return t, x_num, x_ex, err


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/presentacion")
def presentacion():
    return send_from_directory(app.static_folder, "presentacion.html")


@app.get("/docs/<path:filename>")
def docs(filename):
    return send_from_directory(BASE / "docs", filename)


@app.get("/api/verify")
def api_verify():
    omega = _param("omega", 8.0, 0.5, 50.0)
    zeta = _param("zeta", 0.3, 0.01, 5.0)
    h = _param("h", 1e-3, 1e-4, 0.05)
    t_end = _param("T", 3.0, 0.5, 10.0)
    t, x_num, x_ex, err = _verify(omega, zeta, h, t_end)
    step = max(1, len(t) // MAX_POINTS)
    return jsonify(
        omega=omega,
        zeta=zeta,
        h=h,
        t=t[::step].tolist(),
        numeric=x_num[::step].tolist(),
        exact=x_ex[::step].tolist(),
        error=err[::step].tolist(),
        max_error=float(err.max()),  # sobre todos los pasos, no solo los enviados
        metrics=system_metrics(omega, zeta),
    )


@app.get("/api/convergence")
def api_convergence():
    omega = _param("omega", 8.0, 0.5, 50.0)
    zeta = _param("zeta", 0.3, 0.01, 5.0)
    hs = [0.02, 0.01, 0.005, 0.0025, 0.00125]
    errors = [float(_verify(omega, zeta, h, 3.0)[3].max()) for h in hs]
    slope = float(np.polyfit(np.log(hs), np.log(errors), 1)[0])
    return jsonify(h=hs, max_error=errors, order=slope)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
