/* Laboratorio: resorte (2º orden) vs. lerp (1er orden) en pantalla partida. */
const Lab = (() => {
  const $ = (id) => document.getElementById(id);
  const canvas = $('lab-canvas');
  const X_MIN = -0.2, X_MAX = 1.6;     // rango visible de la pista [m]
  const PAD_L = 56, PAD_R = 36;
  const T_MAX = 4;                      // la gráfica muestra los primeros 4 s tras cada cambio

  const st = {
    omega: 8, zeta: 0.3, target: 1,
    spring: { x: 0, v: 0 }, lerp: 0,
    t: 0,                               // tiempo global [s] (solo para el rastro)
    tc: 0,                              // tiempo desde el último clic/cambio [s] (eje x de la gráfica)
    x0: 0, v0: 0,                       // condiciones iniciales de la solución exacta vigente
    maxErr: 0, curErr: 0,
    trailAcc: 0, trail: [], frame: 0,
  };
  const stepper = new Physics.FixedStepper();
  const lerpStepper = new Physics.FixedStepper(1 / 60); // lerp por "frame" a 60 Hz: fórmula literal

  const chart = Charts.create($('lab-chart'), {
    xLabel: 'Tiempo desde el último cambio (s)', yLabel: 'Posición (m)',
    xMin: 0, xMax: T_MAX, xStep: 1, yMin: -0.5, yMax: 2, yStep: 0.5,
    series: [
      { label: 'Resorte (RK4)', color: 'spring', width: 3 },
      { label: 'Solución exacta', color: 'exact', dash: [6, 5], width: 1.5, order: -1 },
      { label: 'Lerp', color: 'lerp', width: 2 },
      { label: 'Destino', color: 'target', dash: [2, 4], width: 1.5 },
    ],
  });
  const [dsSpring, dsExact, dsLerp, dsTarget] = chart.data.datasets;

  const worldToPx = (x, w) => PAD_L + ((x - X_MIN) / (X_MAX - X_MIN)) * (w - PAD_L - PAD_R);
  const pxToWorld = (px, w) => X_MIN + ((px - PAD_L) / (w - PAD_L - PAD_R)) * (X_MAX - X_MIN);

  /** Nueva curva: la exacta y la gráfica parten del estado actual del resorte. */
  function restartCurve() {
    st.tc = 0; st.x0 = st.spring.x; st.v0 = st.spring.v; st.maxErr = 0;
    for (const ds of chart.data.datasets) ds.data.length = 0;
    sample();
  }

  function setTarget(x) {
    st.target = Math.min(1.5, Math.max(-0.1, x));
    restartCurve();
  }

  function restart() {
    st.spring = { x: 0, v: 0 }; st.lerp = 0; st.target = 1; st.t = 0; st.trail = [];
    restartCurve();
  }

  function applyParams(omega, zeta) {
    st.omega = omega; st.zeta = zeta;
    $('lab-omega').value = omega; $('lab-zeta').value = zeta;
    $('lab-omega-val').textContent = omega.toFixed(1);
    $('lab-zeta-val').textContent = zeta.toFixed(2);
  }

  function sample() {
    const exact = Physics.exactPosition(st.tc, st.omega, st.zeta, st.x0, st.v0, st.target);
    st.curErr = Math.abs(st.spring.x - exact);
    st.maxErr = Math.max(st.maxErr, st.curErr);
    if (st.tc > T_MAX) return;
    dsSpring.data.push({ x: st.tc, y: st.spring.x });
    dsExact.data.push({ x: st.tc, y: exact });
    dsLerp.data.push({ x: st.tc, y: st.lerp });
    dsTarget.data.push({ x: st.tc, y: st.target });
  }

  function updateStats() {
    const m = Physics.metrics(st.omega, st.zeta);
    Charts.renderStats($('lab-stats'), [
      ['Régimen', m.regime],
      ['Raíces (s⁻¹)', Physics.formatRoots(m)],
      ['Sobreimpulso', m.overshoot > 0 ? `${m.overshoot.toFixed(1)} %` : 'ninguno'],
      ['Asentamiento (2 %)', `${m.settling.toFixed(2)} s`],
      ['Error vs. exacta (máx.)', `${Charts.sci(st.maxErr)} m`],
    ]);
  }

  function frame(dt) {
    stepper.run(dt, (h) => {
      Physics.rk4Step(st.spring, st.target, st.omega, st.zeta, h);
      st.t += h; st.tc += h;
    });
    lerpStepper.run(dt, () => { st.lerp += (st.target - st.lerp) * 0.1; });
    sample();

    st.trailAcc += dt;
    if (st.trailAcc >= 0.05) { st.trailAcc = 0; st.trail.push({ t: st.t, s: st.spring.x, l: st.lerp }); }
    while (st.trail.length && st.t - st.trail[0].t > 1.5) st.trail.shift();

    draw();
    if (++st.frame % 3 === 0) chart.update('none');
    if (st.frame % 6 === 0) updateStats();
  }

  function draw() {
    const { ctx, w, h } = Charts.fitCanvas(canvas);
    ctx.clearRect(0, 0, w, h);
    ctx.textBaseline = 'alphabetic';
    const lanes = [
      { y: h * 0.30, name: 'Resorte', color: COLORS.spring, x: st.spring.x, key: 's' },
      { y: h * 0.70, name: 'Lerp', color: COLORS.lerp, x: st.lerp, key: 'l' },
    ];

    // escala en metros
    ctx.font = `12px ${FONT}`; ctx.textAlign = 'center';
    for (const m of [0, 0.5, 1, 1.5]) {
      const px = worldToPx(m, w);
      ctx.strokeStyle = COLORS.grid; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(px, 28); ctx.lineTo(px, h - 24); ctx.stroke();
      ctx.fillStyle = COLORS.muted; ctx.fillText(`${m.toFixed(1)}`, px, h - 8);
    }
    ctx.textAlign = 'right'; ctx.fillText('m', w - 8, h - 8);

    // separador de la pantalla partida
    ctx.strokeStyle = COLORS.line; ctx.beginPath(); ctx.moveTo(0, h / 2); ctx.lineTo(w, h / 2); ctx.stroke();

    // destino
    const tx = worldToPx(st.target, w);
    ctx.strokeStyle = COLORS.target; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(tx, 26); ctx.lineTo(tx, h - 24); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = COLORS.target; ctx.font = `600 12px ${FONT}`; ctx.textAlign = 'center';
    ctx.fillText(`destino ${st.target.toFixed(2)} m`, Math.min(w - 60, Math.max(60, tx)), 18);

    for (const lane of lanes) {
      ctx.fillStyle = lane.color; ctx.font = `600 13px ${FONT}`; ctx.textAlign = 'left';
      ctx.fillText(lane.name, 12, lane.y - 36);
      ctx.strokeStyle = COLORS.line; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(PAD_L - 20, lane.y); ctx.lineTo(w - PAD_R + 10, lane.y); ctx.stroke();

      // rastro: el espaciado entre puntos muestra la velocidad
      for (const p of st.trail) {
        ctx.fillStyle = lane.color; ctx.globalAlpha = Math.max(0, 1 - (st.t - p.t) / 1.5) * 0.35;
        ctx.beginPath(); ctx.arc(worldToPx(p[lane.key], w), lane.y, 4, 0, 7); ctx.fill();
      }
      ctx.globalAlpha = 1;

      const px = worldToPx(lane.x, w);
      if (lane.key === 's') {
        ctx.fillStyle = COLORS.wall; ctx.fillRect(PAD_L - 26, lane.y - 22, 6, 44); // pared
        ctx.strokeStyle = lane.color; ctx.lineWidth = 2.5; ctx.lineJoin = 'round';
        Charts.drawSpring(ctx, PAD_L - 20, px - 16, lane.y, 9, 13);
        ctx.fillStyle = lane.color; ctx.beginPath(); ctx.arc(px, lane.y, 16, 0, 7); ctx.fill();
        const v = st.spring.v;                                                 // flecha de velocidad
        if (Math.abs(v) > 0.05) {
          const len = Math.max(-60, Math.min(60, v * 14));
          ctx.strokeStyle = COLORS.ink; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(px, lane.y - 26); ctx.lineTo(px + len, lane.y - 26); ctx.stroke();
        }
      } else {
        ctx.fillStyle = lane.color; ctx.beginPath(); ctx.roundRect(px - 15, lane.y - 15, 30, 30, 6); ctx.fill();
      }
    }
  }

  // ---- eventos ----
  canvas.addEventListener('pointerdown', (e) => {
    const r = canvas.getBoundingClientRect();
    setTarget(pxToWorld(e.clientX - r.left, r.width));
  });
  $('lab-omega').addEventListener('input', (e) => { applyParams(parseFloat(e.target.value), st.zeta); restartCurve(); });
  $('lab-zeta').addEventListener('input', (e) => { applyParams(st.omega, parseFloat(e.target.value)); restartCurve(); });
  document.querySelectorAll('#view-lab .chip[data-zeta]').forEach((b) =>
    b.addEventListener('click', () => { applyParams(8, parseFloat(b.dataset.zeta)); restart(); }));
  $('lab-reset').addEventListener('click', restart);

  applyParams(st.omega, st.zeta);
  restart();
  updateStats();

  return { frame, onShow: () => chart.resize() };
})();
