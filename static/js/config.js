const DESIGN = {
  camera: { zeta: 1.0, omega: 6 },
  menu:   { zeta: 0.5, omega: 10 },
  health: { zeta: 2.0, omega: 8 },
};

/* Paleta: la fuente de verdad son las variables CSS de styles.css (tema claro y oscuro).
 * COLORS guarda sus valores para el código que dibuja en canvas y gráficas; COLORS.load()
 * los vuelve a leer cuando cambia el tema. */
const COLORS = {
  load() {
    const css = getComputedStyle(document.documentElement);
    for (const key of Object.keys(this)) {
      if (typeof this[key] !== 'string') continue;
      const value = css.getPropertyValue('--' + key.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase())).trim();
      if (value) this[key] = value;
    }
  },
  // Valores del tema claro: se usan tal cual si la página no define la variable CSS (p. ej. /presentacion).
  ink: '#111827', text: '#374151', muted: '#6b7280', line: '#e5e7eb', grid: '#eef0f3', stage: '#f8fafc',
  fill: '#2563eb', spring: '#2563eb', lerp: '#ea580c', exact: '#111827', target: '#dc2626', good: '#16a34a', warn: '#d97706',
  z03: '#d97706', z1: '#16a34a', z2: '#7c3aed',
  ground: '#e8edf3', groundLine: '#cbd5e1', post: '#d5dbe4', wall: '#9ca3af',
  device: '#1f2937', screen: '#f1f5f9', screenItem: '#e2e8f0', track: '#e5e7eb',
};
COLORS.load();
const FONT = "'Segoe UI', system-ui, -apple-system, sans-serif";
