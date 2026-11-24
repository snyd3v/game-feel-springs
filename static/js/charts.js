/* Utilidades de interfaz: gráficas (Chart.js), canvas, resorte dibujado y tarjetas de datos. */
const Charts = (() => {
  Chart.defaults.color = COLORS.muted;
  Chart.defaults.font.family = FONT;
  Chart.defaults.font.size = 12;
  Chart.defaults.animation = false;

  const live = []; // gráficas creadas, para recolorearlas al cambiar de tema

  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  const sup = (n) => String(n).split('').map((c) => SUP[c]).join('');

  /** 1.3×10⁻⁸ (notación científica legible). */
  function sci(value, digits = 1) {
    if (value === 0) return '0';
    const exp = Math.floor(Math.log10(Math.abs(value)));
    return `${(value / 10 ** exp).toFixed(digits)}×10${sup(exp)}`;
  }

  /** En ejes logarítmicos solo se rotulan las potencias de 10: 10⁻⁹, 10⁻⁶, 1, 10⁻¹… */
  function logTick(value) {
    const e = Math.log10(value);
    if (Math.abs(e - Math.round(e)) > 1e-9) return '';
    const n = Math.round(e);
    return n === 0 ? '1' : `10${sup(n)}`;
  }

  /**
   * cfg: {series, xLabel, yLabel, title?, subtitle?, xType?, yType?, xMin?, xMax?, yMin?, yMax?,
   *       xStep?, yStep?, legendFilter?}
   * series: {label, color, dash?, width?, order?}
   */
  function create(canvas, cfg) {
    const datasets = cfg.series.map((s) => ({
      label: s.label,
      data: [],
      _key: s.color,                       // clave de COLORS (o color literal): permite recolorear al cambiar de tema
      borderColor: COLORS[s.color] ?? s.color,
      backgroundColor: COLORS[s.color] ?? s.color,
      borderDash: s.dash || [],
      borderWidth: s.width || 2,
      pointRadius: s.points ? 4 : 0,
      showLine: true,
      tension: 0,
      order: s.order ?? 0,
    }));
    const axis = (type, label, min, max, step) => ({
      type: type || 'linear',
      min, max,
      title: { display: true, text: label, color: COLORS.text, font: { size: 12, weight: '500' }, padding: 6 },
      grid: { color: COLORS.grid },
      border: { color: COLORS.line },
      ticks: {
        color: COLORS.muted,
        includeBounds: false,
        maxTicksLimit: 8,
        ...(step ? { stepSize: step } : {}),
        ...(type === 'logarithmic' ? { callback: logTick } : {}),
      },
    });
    const chart = new Chart(canvas, {
      type: 'scatter',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: COLORS.text, boxWidth: 26, boxHeight: 3, padding: 14,
                      ...(cfg.legendFilter ? { filter: cfg.legendFilter } : {}) },
          },
          title: { display: !!cfg.title, text: cfg.title, color: COLORS.ink, font: { size: 13, weight: '600' } },
          subtitle: { display: !!cfg.subtitle, text: cfg.subtitle, color: COLORS.muted, font: { size: 11 }, padding: { bottom: 6 } },
          tooltip: { enabled: false },
        },
        scales: {
          x: axis(cfg.xType, cfg.xLabel, cfg.xMin, cfg.xMax, cfg.xStep),
          y: axis(cfg.yType, cfg.yLabel, cfg.yMin, cfg.yMax, cfg.yStep),
        },
      },
    });
    live.push(chart);
    return chart;
  }

  /** Vuelve a aplicar la paleta (COLORS ya releída) a todas las gráficas creadas. */
  function applyTheme() {
    Chart.defaults.color = COLORS.muted;
    for (const chart of live) {
      chart.data.datasets.forEach((ds) => { ds.borderColor = ds.backgroundColor = COLORS[ds._key] ?? ds._key; });
      const o = chart.options;
      for (const axis of [o.scales.x, o.scales.y]) {
        axis.title.color = COLORS.text;
        axis.grid.color = COLORS.grid;
        axis.border.color = COLORS.line;
        axis.ticks.color = COLORS.muted;
      }
      o.plugins.legend.labels.color = COLORS.text;
      o.plugins.title.color = COLORS.ink;
      o.plugins.subtitle.color = COLORS.muted;
      chart.update('none');
    }
  }

  /** Ventana deslizante: muestra los últimos `windowSec` segundos con el eje desplazándose en pasos enteros. */
  function setWindow(chart, tNow, windowSec) {
    const hi = Math.max(windowSec, Math.ceil(tNow));
    const lo = hi - windowSec;
    chart.options.scales.x.min = lo;
    chart.options.scales.x.max = hi;
    for (const ds of chart.data.datasets) {
      while (ds.data.length > 2 && ds.data[1].x < lo) ds.data.shift();
    }
  }

  /** Ajusta el canvas a su tamaño CSS con densidad de pantalla; devuelve {ctx, w, h} en px CSS. */
  function fitCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    // Alto lógico en px CSS: se lee UNA vez. Asignar canvas.height reescribe el atributo (px de
    // dispositivo); releerlo cada frame lo multiplicaría por dpr.
    if (!canvas.dataset.cssHeight) canvas.dataset.cssHeight = canvas.getAttribute('height');
    const h = parseInt(canvas.dataset.cssHeight, 10);
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.height = h + 'px';
    }
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx, w, h };
  }

  /** Resorte helicoidal (zigzag) de (x1,y) a (x2,y). */
  function drawSpring(ctx, x1, x2, y, coils = 9, radius = 12) {
    const lead = Math.min(14, Math.abs(x2 - x1) * 0.12);
    const dir = x2 >= x1 ? 1 : -1;
    const a = x1 + dir * lead, b = x2 - dir * lead;
    const n = coils * 2;
    const rad = radius * Math.min(1, Math.max(0.35, Math.abs(b - a) / 140));
    ctx.beginPath();
    ctx.moveTo(x1, y);
    ctx.lineTo(a, y);
    for (let i = 1; i < n; i++) ctx.lineTo(a + ((b - a) * i) / n, y + (i % 2 ? -rad : rad));
    ctx.lineTo(b, y);
    ctx.lineTo(x2, y);
    ctx.stroke();
  }

  /** Tarjetas "etiqueta / valor" bajo una gráfica. items: [[etiqueta, valor], ...] */
  function renderStats(el, items) {
    el.innerHTML = items.map(([k, v]) => `<div class="stat"><span>${k}</span><b>${v}</b></div>`).join('');
  }

  return { create, applyTheme, setWindow, fitCanvas, drawSpring, renderStats, sci };
})();
