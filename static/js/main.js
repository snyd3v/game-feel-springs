/* Menú lateral, navegación entre secciones, bucle de animación y tabla de conclusión. */
(() => {
  const $ = (id) => document.getElementById(id);
  const views = { lab: Lab, verify: Verify, cases: Cases, conclusion: null };
  let current = 'lab';

  const items = document.querySelectorAll('#main-nav .nav-item');
  const toggle = $('sidebar-toggle');
  const root = document.documentElement;

  function show(name) {
    current = name;
    items.forEach((b) => {
      const on = b.dataset.view === name;
      b.classList.toggle('active', on);
      b.setAttribute('aria-selected', on);
      if (on) $('page-title').textContent = b.dataset.tooltip;
    });
    document.querySelectorAll('.view').forEach((v) => v.classList.toggle('active', v.id === `view-${name}`));
    views[name]?.onShow?.();
  }
  items.forEach((b) => b.addEventListener('click', () => {
    show(b.dataset.view);
    history.replaceState(null, '', `#${b.dataset.view}`);
  }));

  // Sidebar colapsable: solo iconos (con tooltip) o icono + texto. El estado se recuerda entre visitas.
  function syncToggle() {
    const collapsed = root.classList.contains('sb-collapsed');
    toggle.setAttribute('aria-expanded', !collapsed);
    toggle.dataset.tooltip = collapsed ? 'Expandir menú' : 'Colapsar menú';
  }
  toggle.addEventListener('click', () => {
    const collapsed = root.classList.toggle('sb-collapsed');
    try { localStorage.setItem('sidebar-collapsed', collapsed ? '1' : '0'); } catch (e) {}
    syncToggle();
  });
  syncToggle();

  // Solo se anima la sección visible. La pestaña oculta no consume CPU.
  let last = performance.now();
  function loop(now) {
    const dt = (now - last) / 1000;
    last = now;
    if (!document.hidden) views[current]?.frame?.(dt);
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  // Permite abrir directamente una sección (p. ej. /#verify).
  const initial = location.hash.slice(1);
  if (initial in views) show(initial);

  // ---- Conclusión: tabla calculada con las mismas funciones que la animación ----
  const f = (n, d = 2) => n.toFixed(d);
  const rows = [
    { name: 'Cámara', key: 'camera', why: 'Alcanza al personaje lo más rápido posible sin pasarse; un rebote marea.' },
    { name: 'Menú', key: 'menu', why: 'Un rebote pequeño se siente responsivo y se asienta rápido.' },
    { name: 'Barra de vida', key: 'health', why: 'Baja con peso y nunca sube después de un golpe.' },
  ].map((r) => {
    const p = DESIGN[r.key], m = Physics.metrics(p.omega, p.zeta);
    return `<tr>
      <td><b>${r.name}</b></td>
      <td class="num">${f(p.zeta, 1)}</td><td class="num">${p.omega}</td>
      <td>${m.regime}</td>
      <td class="num">${m.overshoot > 0 ? f(m.overshoot, 1) + ' %' : 'ninguno'}</td>
      <td class="num">${f(m.settling)} s</td>
      <td>${r.why}</td></tr>`;
  }).join('');
  $('conclusion-table-wrap').innerHTML =
    `<table><thead><tr><th>Elemento</th><th>ζ</th><th>ω (rad/s)</th><th>Régimen</th><th>Sobreimpulso</th><th>Asentamiento</th><th>Por qué</th></tr></thead><tbody>${rows}</tbody></table>`;
  $('conclusion-text').innerHTML =
    '<b>Regla práctica:</b> ζ ≈ 1 si el elemento debe acompañar al usuario, ζ ≈ 0.5 si debe sentirse vivo y ζ &gt; 1 si comunica algo irreversible, como el daño.';
})();
