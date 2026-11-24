"""
Motor matemático del Proyecto 4 (Resortes para animar).

Modelo:      x'' + 2*zeta*omega*x' + omega^2 * (x - x_f) = 0
Cambio:      u = x - x_f   ->   u'' + 2*zeta*omega*u' + omega^2*u = 0
Sistema 1er orden:  x' = v,   v' = -2*zeta*omega*v - omega^2*(x - x_f)

Aquí viven la solución numérica (RK4, paso fijo) y la solución analítica exacta
deducida a mano. El programa verifica, no reemplaza.

Mapa:
    acceleration, rk4_step, rk4_solve  -> sistema de 1.er orden y RK4
    exact_position                      -> ecuación característica y los 3 casos de raíces
    system_metrics                      -> raíces, sobreimpulso, tiempo de pico y asentamiento
"""
import math

import numpy as np

# Tolerancia única para decir "ζ = 1" (amortiguamiento crítico) en todo el proyecto.
ZETA_CRITICAL_TOL = 1e-4


def acceleration(x, v, target, omega, zeta):
    """x'' despejada de la ecuación diferencial."""
    return -2.0 * zeta * omega * v - omega**2 * (x - target)


def rk4_step(x, v, target, omega, zeta, h):
    """Un paso de Runge-Kutta de orden 4 sobre el sistema [x, v]."""
    k1x, k1v = v, acceleration(x, v, target, omega, zeta)
    k2x = v + 0.5 * h * k1v
    k2v = acceleration(x + 0.5 * h * k1x, v + 0.5 * h * k1v, target, omega, zeta)
    k3x = v + 0.5 * h * k2v
    k3v = acceleration(x + 0.5 * h * k2x, v + 0.5 * h * k2v, target, omega, zeta)
    k4x = v + h * k3v
    k4v = acceleration(x + h * k3x, v + h * k3v, target, omega, zeta)
    x_new = x + h / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x)
    v_new = v + h / 6.0 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return x_new, v_new


def rk4_solve(omega, zeta, x0=0.0, v0=0.0, target=1.0, t_end=3.0, h=1e-3):
    """Integra con paso fijo h. Devuelve (t, x, v) sobre el mismo vector de tiempos."""
    n = int(round(t_end / h))
    t = np.arange(n + 1) * h
    x = np.empty(n + 1)
    v = np.empty(n + 1)
    x[0], v[0] = x0, v0
    for i in range(n):
        x[i + 1], v[i + 1] = rk4_step(x[i], v[i], target, omega, zeta, h)
    return t, x, v


def is_critical(zeta):
    return abs(zeta - 1.0) < ZETA_CRITICAL_TOL


def exact_position(t, omega, zeta, x0=0.0, v0=0.0, target=1.0):
    """Solución analítica x(t) = x_f + u(t) para u(0)=x0-x_f, u'(0)=v0."""
    t = np.asarray(t, dtype=float)
    u0 = x0 - target
    if is_critical(zeta):
        # Raíz doble r = -omega:  u = (C1 + C2 t) e^{-omega t}
        c1 = u0
        c2 = v0 + omega * u0
        u = (c1 + c2 * t) * np.exp(-omega * t)
    elif zeta < 1.0:
        # Raíces complejas -alpha ± i beta:  u = e^{-alpha t}(C1 cos bt + C2 sin bt)
        alpha = zeta * omega
        beta = omega * math.sqrt(1.0 - zeta**2)
        c1 = u0
        c2 = (v0 + alpha * u0) / beta
        u = np.exp(-alpha * t) * (c1 * np.cos(beta * t) + c2 * np.sin(beta * t))
    else:
        # Dos raíces reales distintas:  u = C1 e^{r1 t} + C2 e^{r2 t}
        root = math.sqrt(zeta**2 - 1.0)
        r1 = -omega * (zeta - root)
        r2 = -omega * (zeta + root)
        c1 = (v0 - r2 * u0) / (r1 - r2)
        c2 = u0 - c1
        u = c1 * np.exp(r1 * t) + c2 * np.exp(r2 * t)
    return target + u


def system_metrics(omega, zeta):
    """Régimen, raíces características y métricas de desempeño (paso x0=0 -> x_f)."""
    alpha = zeta * omega
    if is_critical(zeta):
        regime = "crítico"
        roots = [-omega, -omega]
        mp = 0.0
        tp = None
        ts = 5.83 / omega  # (1+w t)e^{-w t} = 0.02
    elif zeta < 1.0:
        regime = "subamortiguado"
        beta = omega * math.sqrt(1.0 - zeta**2)
        roots = [complex(-alpha, beta), complex(-alpha, -beta)]
        mp = 100.0 * math.exp(-math.pi * zeta / math.sqrt(1.0 - zeta**2))
        tp = math.pi / beta
        # Cota por envolvente: |u| <= e^{-alpha t} / sqrt(1 - zeta^2) <= 0.02 (paso desde reposo).
        # Es una cota, no el instante exacto de la última salida de la banda del 2 %.
        ts = math.log(50.0 / math.sqrt(1.0 - zeta**2)) / alpha
    else:
        regime = "sobreamortiguado"
        root = math.sqrt(zeta**2 - 1.0)
        roots = [-omega * (zeta - root), -omega * (zeta + root)]
        mp = 0.0
        tp = None
        c1 = abs(roots[1] / (roots[1] - roots[0]))  # amplitud del modo lento (paso desde reposo)
        ts = math.log(c1 / 0.02) / abs(roots[0])  # modo lento domina: c1 e^{r1 t} <= 0.02
    return {
        "regime": regime,
        "roots": [
            {"re": r.real, "im": r.imag} if isinstance(r, complex) else {"re": r, "im": 0.0}
            for r in roots
        ],
        "alpha": alpha,
        "overshoot_pct": mp,
        "peak_time": tp,
        "settling_time": ts,
    }
