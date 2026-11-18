import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics import acceleration, exact_position, rk4_solve, system_metrics  # noqa: E402

OMEGA = 8.0


@pytest.mark.parametrize("zeta", [0.3, 1.0, 2.0])
def test_exact_initial_conditions(zeta):
    x0, v0 = 0.2, -0.7
    assert exact_position(0.0, OMEGA, zeta, x0=x0, v0=v0) == pytest.approx(x0)
    h = 1e-6
    v_est = (exact_position(h, OMEGA, zeta, x0=x0, v0=v0) - exact_position(-h, OMEGA, zeta, x0=x0, v0=v0)) / (2 * h)
    assert v_est == pytest.approx(v0, abs=1e-4)


@pytest.mark.parametrize("zeta", [0.3, 1.0, 2.0])
def test_exact_satisfies_ode(zeta):
    t = np.linspace(0.1, 2.0, 7)
    h = 1e-4
    x = exact_position(t, OMEGA, zeta)
    xp = exact_position(t + h, OMEGA, zeta)
    xm = exact_position(t - h, OMEGA, zeta)
    v = (xp - xm) / (2 * h)
    a = (xp - 2 * x + xm) / h**2
    residual = a - acceleration(x, v, 1.0, OMEGA, zeta)
    assert np.max(np.abs(residual)) < 1e-2  # tolerancia de la diferencia finita


@pytest.mark.parametrize("zeta", [0.3, 1.0, 2.0])
def test_rk4_matches_exact(zeta):
    t, x, _ = rk4_solve(OMEGA, zeta, t_end=3.0, h=1e-3)
    assert np.max(np.abs(x - exact_position(t, OMEGA, zeta))) < 1e-9


def test_rk4_is_fourth_order():
    errs = []
    for h in (0.01, 0.005):
        t, x, _ = rk4_solve(OMEGA, 0.3, t_end=3.0, h=h)
        errs.append(np.max(np.abs(x - exact_position(t, OMEGA, 0.3))))
    assert math.log2(errs[0] / errs[1]) == pytest.approx(4.0, abs=0.5)


def test_hand_solutions():
    # Resultados de la deducción a mano (ω = 8, x_f = 1, reposo).
    t = 0.37
    assert exact_position(t, OMEGA, 1.0) == pytest.approx(1 - (1 + 8 * t) * math.exp(-8 * t))
    beta = 8 * math.sqrt(0.91)
    expected = 1 - math.exp(-2.4 * t) * (math.cos(beta * t) + 2.4 / beta * math.sin(beta * t))
    assert exact_position(t, OMEGA, 0.3) == pytest.approx(expected)
    r1, r2 = -16 + 8 * math.sqrt(3), -16 - 8 * math.sqrt(3)
    c1, c2 = -(2 * math.sqrt(3) + 3) / 6, (2 * math.sqrt(3) - 3) / 6
    assert exact_position(t, OMEGA, 2.0) == pytest.approx(1 + c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t))


def test_overshoot_only_when_underdamped():
    for zeta, rebota in [(0.3, True), (1.0, False), (2.0, False)]:
        t, x, _ = rk4_solve(OMEGA, zeta, t_end=3.0, h=1e-3)
        assert (x.max() > 1.0 + 1e-9) == rebota
    assert system_metrics(OMEGA, 0.3)["overshoot_pct"] == pytest.approx(37.23, abs=0.01)


@pytest.mark.parametrize("omega, zeta", [(8.0, 0.3), (10.0, 0.5), (6.0, 0.7)])
def test_settling_time_is_envelope_bound(omega, zeta):
    # t_s de system_metrics es una cota: la última salida real de la banda del 2 % no la supera.
    t, x, _ = rk4_solve(omega, zeta, t_end=6.0, h=1e-4)
    real = t[np.where(np.abs(x - 1.0) > 0.02)[0][-1] + 1]
    bound = system_metrics(omega, zeta)["settling_time"]
    assert real <= bound + 1e-3
    assert bound - real < 0.3 * bound
