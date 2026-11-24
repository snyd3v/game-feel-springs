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
  ink: '', text: '', muted: '', line: '', grid: '', stage: '',
  fill: '', spring: '', lerp: '', exact: '', target: '', good: '', warn: '',
  z03: '', z1: '', z2: '',
  ground: '', groundLine: '', post: '', wall: '', device: '', screen: '', screenItem: '', track: '',
};
COLORS.load();
const FONT = "'Segoe UI', system-ui, -apple-system, sans-serif";
