/* Verificación: RK4 (numpy en el servidor) vs. solución analítica exacta. */
const Verify = (() => {
  const $ = (id) => document.getElementById(id);
  const CASES = [
    { zeta: 0.3, color: 'z03' },
    { zeta: 1.0, color: 'z1' },
    { zeta: 2.0, color: 'z2' },
  ];
  const OMEGA = 8;
  let loaded = false;

  const toPts = (xs, ys, floor) => xs.map((x, i) => ({ x, y: floor ? Math.max(ys[i], floor) : ys[i] }));

  // Series 0,2,4 = numéricas (color, con leyenda); 1,3,5 = exactas (negro discontinuo, sin leyenda)
  const solutionChart = Charts.create($('verify-chart'), {
    title: 'Posición x(t)',
    subtitle: 'línea de color: RK4 · línea discontinua: solución exacta',
    xLabel: 'Tiempo (s)', yLabel: 'Posición (m)', xMin: 0, xMax: 3, xStep: 0.5,
    legendFilter: (item) => item.datasetIndex % 2 === 0,
    series: CASES.flatMap((c) => [
      { label: `ζ = ${c.zeta}`, color: c.color, width: 5 },
      { label: `exacta ζ = ${c.zeta}`, color: 'exact', dash: [6, 5], width: 1.5, order: -1 },
    ]),
  });
  const errorChart = Charts.create($('verify-error'), {
    title: 'Diferencia entre numérica y exacta',
    xLabel: 'Tiempo (s)', yLabel: 'Error |x numérica − x exacta| (m)', xMin: 0, xMax: 3, xStep: 0.5, yType: 'logarithmic',
    series: CASES.map((c) => ({ label: `ζ = ${c.zeta}`, color: c.color, width: 2 })),
  });
  const convChart = Charts.create($('conv-chart'), {
    title: 'Error máximo según el paso h',
    xLabel: 'Paso h (s)', yLabel: 'Error máximo (m)', xType: 'logarithmic', yType: 'logarithmic',
    series: CASES.map((c) => ({ label: `ζ = ${c.zeta}`, color: c.color, width: 2, points: true })),
  });

  const get = (url) => fetch(url).then((r) => {
    if (!r.ok) throw new Error(`${url}: ${r.status}`);
    return r.json();
  });

  async function loadSolutions() {
    const h = $('verify-h').value;
    const results = await Promise.all(CASES.map((c) => get(`/api/verify?omega=${OMEGA}&zeta=${c.zeta}&h=${h}&T=3`)));
    results.forEach((r, i) => {
      solutionChart.data.datasets[2 * i].data = toPts(r.t, r.numeric);
      solutionChart.data.datasets[2 * i + 1].data = toPts(r.t, r.exact);
      errorChart.data.datasets[i].data = toPts(r.t, r.error, 1e-17); // 0 no existe en escala log
    });
    solutionChart.update('none');
    errorChart.update('none');
    renderTable(results);
  }

  function renderTable(results) {
    const rows = results.map((r, i) => {
      const m = r.metrics;
      return `<tr>
        <td><span class="dot" style="background:var(--${CASES[i].color})"></span>ζ = ${CASES[i].zeta}</td>
        <td>${m.regime}</td>
        <td class="num">${Physics.formatRoots({ regime: m.regime, roots: m.roots })}</td>
        <td class="num">${m.overshoot_pct > 0 ? m.overshoot_pct.toFixed(1) + ' %' : 'ninguno'}</td>
        <td class="num">${Charts.sci(r.max_error)} m</td>
      </tr>`;
    }).join('');
    $('verify-table-wrap').innerHTML =
      `<table><thead><tr><th>Caso</th><th>Régimen</th><th>Raíces (s⁻¹)</th><th>Sobreimpulso</th><th>Error máximo</th></tr></thead><tbody>${rows}</tbody></table>`;
  }

  async function loadConvergence() {
    const results = await Promise.all(CASES.map((c) => get(`/api/convergence?omega=${OMEGA}&zeta=${c.zeta}`)));
    results.forEach((r, i) => { convChart.data.datasets[i].data = toPts(r.h, r.max_error); });
    convChart.update('none');
    const order = (results.reduce((s, r) => s + r.order, 0) / results.length).toFixed(1);
    $('verify-comment').innerHTML =
      `<li>El error global de RK4 es proporcional a h⁴: la pendiente medida es ≈ ${order}. Al reducir h a la mitad, el error baja unas 16 veces.</li>` +
      `<li>Con h muy pequeño domina el redondeo del computador (≈ 10⁻¹⁵ m) y ya no se gana precisión.</li>` +
      `<li>La animación usa un paso fijo h = 1/240 s (error ≈ 10⁻⁸ m), no el <i>deltaTime</i> del navegador.</li>`;
  }

  async function load() {
    if (loaded) return;
    loaded = true;
    try { await Promise.all([loadSolutions(), loadConvergence()]); }
    catch (e) { loaded = false; $('verify-table-wrap').textContent = `No se pudo consultar el servidor: ${e.message}`; }
  }

  $('verify-h').addEventListener('change', () => loadSolutions().catch(() => {}));

  return { onShow() { load(); [solutionChart, errorChart, convChart].forEach((c) => c.resize()); } };
})();
