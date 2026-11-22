/* Presentación: cambia de diapositiva, muestra la app en las demostraciones y dibuja la gráfica.
 * No tiene matemática propia: las curvas salen de Physics.exactPosition. */
(() => {
  const $ = (id) => document.getElementById(id);
  const DEMO_SCALE = 0.8; // la app se ve un poco reducida para que quepa en la diapositiva
  const slides = [...document.querySelectorAll('.slide')];
  let current = -1;

  function openDemo(box) {
    const frame = document.createElement('iframe');
    frame.title = 'Demostración';
    frame.src = `/#${box.dataset.view}`;
    frame.style.width = `${box.clientWidth / DEMO_SCALE}px`;
    frame.style.height = `${box.clientHeight / DEMO_SCALE}px`;
    frame.style.transform = `scale(${DEMO_SCALE})`;
    frame.addEventListener('load', () => {
      const doc = frame.contentDocument;
      // El título y la ecuación ya están en las diapositivas.
      const style = doc.createElement('style');
      style.textContent = '.topbar, .model { display: none } main { padding: 8px 28px 0 }';
      doc.head.append(style);
      // Dentro de la demo solo AvPág/RePág cambian de diapositiva (las flechas mueven la cámara).
      doc.addEventListener('keydown', (e) => { if (e.key.startsWith('Page')) onKey(e); });
    });
    box.append(frame);
  }

  function show(index) {
    const n = Math.min(slides.length - 1, Math.max(0, index));
    if (n === current) return;
    document.querySelector('.demo iframe')?.remove(); // al volver, la demo empieza con sus valores iniciales
    slides.forEach((s, i) => s.classList.toggle('active', i === n));
    current = n;
    const demo = slides[n].querySelector('.demo');
    if (demo) openDemo(demo);
    $('count').textContent = `${n + 1} / ${slides.length}`;
    history.replaceState(null, '', `#${n + 1}`);
  }

  function onKey(e) {
    const target = { ArrowRight: current + 1, PageDown: current + 1, ArrowLeft: current - 1, PageUp: current - 1,
                     Home: 0, End: slides.length - 1 }[e.key];
    if (target === undefined) return;
    e.preventDefault();
    show(target);
  }

  function fit() {
    const scale = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    $('deck').style.setProperty('--scale', scale);
  }

  function drawSolutions() {
    const cases = [[0.3, COLORS.z03], [1, COLORS.z1], [2, COLORS.z2]];
    const chart = Charts.create($('solutions-chart'), {
      xLabel: 'Tiempo t (s)', yLabel: 'Posición x (m)', xMin: 0, xMax: 3, xStep: 0.5, yMin: 0, yMax: 1.5, yStep: 0.5,
      series: [
        ...cases.map(([zeta, color]) => ({ label: `ζ = ${zeta}`, color, width: 4 })),
        { label: 'Destino', color: COLORS.target, dash: [6, 5], width: 2 },
      ],
    });
    const times = Array.from({ length: 301 }, (_, i) => i / 100);
    cases.forEach(([zeta], i) => {
      chart.data.datasets[i].data = times.map((t) => ({ x: t, y: Physics.exactPosition(t, 8, zeta, 0, 0, 1) }));
    });
    chart.data.datasets[cases.length].data = [{ x: 0, y: 1 }, { x: 3, y: 1 }];
    // Tamaño fijo: lo que se escala es la diapositiva completa, no la gráfica.
    const box = chart.canvas.parentNode;
    chart.options.responsive = false;
    chart.options.locale = 'en-US'; // punto decimal, como en las fórmulas
    // Letra más grande y más nitidez para el proyector.
    const { plugins, scales } = chart.options;
    chart.options.devicePixelRatio = 2;
    plugins.legend.labels.font = { size: 16 };
    for (const axis of [scales.x, scales.y]) {
      axis.title.font.size = 18;
      axis.ticks.font = { size: 16 };
    }
    chart.update('none');
    chart.resize(box.clientWidth, box.clientHeight);
  }

  $('prev').addEventListener('click', () => show(current - 1));
  $('next').addEventListener('click', () => show(current + 1));
  document.addEventListener('keydown', onKey);
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => show((parseInt(location.hash.slice(1), 10) || 1) - 1));

  drawSolutions();
  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
