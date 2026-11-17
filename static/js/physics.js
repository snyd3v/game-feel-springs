/*
 * Motor matemático en el navegador (misma matemática que physics.py).
 *
 *   x'' + 2ζω x' + ω²(x - x_f) = 0      ->      x' = v,  v' = -2ζω v - ω²(x - x_f)
 *
 * La simulación avanza SIEMPRE con paso fijo H (no con deltaTime del navegador):
 * así la curva numérica es comparable con la exacta.
 */
const Physics = (() => {
  const H = 1 / 240; // paso fijo de integración [s]
  const ZETA_CRITICAL_TOL = 1e-4;

  function acceleration(x, v, target, omega, zeta) {
    return -2 * zeta * omega * v - omega * omega * (x - target);
  }

  /** Un paso RK4 sobre el estado {x, v}; modifica y devuelve el mismo objeto. */
  function rk4Step(s, target, omega, zeta, h) {
    const { x, v } = s;
    const k1x = v;
    const k1v = acceleration(x, v, target, omega, zeta);
    const k2x = v + 0.5 * h * k1v;
    const k2v = acceleration(x + 0.5 * h * k1x, v + 0.5 * h * k1v, target, omega, zeta);
    const k3x = v + 0.5 * h * k2v;
    const k3v = acceleration(x + 0.5 * h * k2x, v + 0.5 * h * k2v, target, omega, zeta);
    const k4x = v + h * k3v;
    const k4v = acceleration(x + h * k3x, v + h * k3v, target, omega, zeta);
    s.x = x + (h / 6) * (k1x + 2 * k2x + 2 * k3x + k4x);
    s.v = v + (h / 6) * (k1v + 2 * k2v + 2 * k3v + k4v);
    return s;
  }

  const isCritical = (zeta) => Math.abs(zeta - 1) < ZETA_CRITICAL_TOL;

  /** Solución analítica x(t) para u(0)=x0-x_f, u'(0)=v0 (deducción a mano). */
  function exactPosition(t, omega, zeta, x0, v0, target) {
    const u0 = x0 - target;
    let u;
    if (isCritical(zeta)) {
      u = (u0 + (v0 + omega * u0) * t) * Math.exp(-omega * t);
    } else if (zeta < 1) {
      const alpha = zeta * omega;
      const beta = omega * Math.sqrt(1 - zeta * zeta);
      const c2 = (v0 + alpha * u0) / beta;
      u = Math.exp(-alpha * t) * (u0 * Math.cos(beta * t) + c2 * Math.sin(beta * t));
    } else {
      const root = Math.sqrt(zeta * zeta - 1);
      const r1 = -omega * (zeta - root);
      const r2 = -omega * (zeta + root);
      const c1 = (v0 - r2 * u0) / (r1 - r2);
      u = c1 * Math.exp(r1 * t) + (u0 - c1) * Math.exp(r2 * t);
    }
    return target + u;
  }

  /** Régimen, raíces y métricas para un paso 0 -> x_f desde el reposo. */
  function metrics(omega, zeta) {
    const alpha = zeta * omega;
    if (isCritical(zeta)) {
      return { regime: 'crítico', roots: [{ re: -omega, im: 0 }, { re: -omega, im: 0 }], alpha,
               overshoot: 0, peakTime: null, settling: 5.83 / omega };
    }
    if (zeta < 1) {
      const beta = omega * Math.sqrt(1 - zeta * zeta);
      return { regime: 'subamortiguado', roots: [{ re: -alpha, im: beta }, { re: -alpha, im: -beta }], alpha,
               overshoot: 100 * Math.exp((-Math.PI * zeta) / Math.sqrt(1 - zeta * zeta)),
               peakTime: Math.PI / beta, settling: Math.log(50) / alpha };
    }
    const root = Math.sqrt(zeta * zeta - 1);
    const r1 = -omega * (zeta - root);
    const r2 = -omega * (zeta + root);
    const c1 = Math.abs(r2 / (r2 - r1)); // amplitud del modo lento (paso desde reposo)
    return { regime: 'sobreamortiguado', roots: [{ re: r1, im: 0 }, { re: r2, im: 0 }], alpha,
             overshoot: 0, peakTime: null, settling: Math.log(c1 / 0.02) / Math.abs(r1) };
  }

  /** Acumulador de tiempo: ejecuta `fn(H)` las veces necesarias con paso fijo. */
  class FixedStepper {
    constructor(h = H) { this.h = h; this.acc = 0; }
    run(dt, fn) {
      this.acc += Math.min(dt, 0.05);
      while (this.acc >= this.h) { fn(this.h); this.acc -= this.h; }
    }
  }

  function formatRoots(m) {
    const f = (r) => (r.im === 0 ? r.re.toFixed(2) : `${r.re.toFixed(2)} ${r.im >= 0 ? '+' : '−'} ${Math.abs(r.im).toFixed(2)}i`);
    return m.regime === 'crítico' ? `${f(m.roots[0])} (doble)` : m.roots.map(f).join(' ; ');
  }

  return { H, acceleration, rk4Step, exactPosition, metrics, FixedStepper, formatRoots, isCritical };
})();
