/* Tres aplicaciones del resorte: cámara, menú y barra de vida.
 * Las tres integran la MISMA ecuación x'' + 2ζω x' + ω²(x − x_f) = 0 con RK4 de paso fijo;
 * cambia solo el significado de x, el destino x_f y la pareja (ζ, ω) elegida. */
const Cases = (() => {
  const $ = (id) => document.getElementById(id);
  const fmt = (n, d = 2) => n.toFixed(d);
  const overshootOf = (omega, zeta) => Physics.metrics(omega, zeta).overshoot;

  class SpringCase {
    /** opts: {x0, yLabel, destLabel, posLabel, yMin?, yMax?, yStep?, windowS} */
    constructor(key, opts) {
      this.key = key;
      this.opts = opts;
      this.design = DESIGN[key];
      this.omega = this.design.omega;
      this.zeta = this.design.zeta;
      this.s = { x: opts.x0, v: 0 };
      this.target = opts.x0;
      this.t = 0;
      this.frameCount = 0;
      this.stepper = new Physics.FixedStepper();
      this.canvas = $(`${key}-canvas`);
      this.chart = Charts.create($(`${key}-chart`), {
        xLabel: 'Tiempo (s)', yLabel: opts.yLabel, yMin: opts.yMin, yMax: opts.yMax, yStep: opts.yStep,
        series: [
          { label: opts.destLabel, color: COLORS.target, dash: [6, 4], width: 2 },
          { label: opts.posLabel, color: COLORS.spring, width: 3 },
        ],
      });
      this.bindControls();
      this.refresh();
      // La nota habla SOLO del valor elegido (fijo); las tarjetas de arriba siguen a los deslizadores.
      const d = this.design, m = Physics.metrics(d.omega, d.zeta);
      $(`${key}-note`).innerHTML =
        `<b>Valor elegido: ζ = ${fmt(d.zeta, 1)} (${m.regime}), ω = ${d.omega} rad/s.</b> ` + this.justification();
    }

    bindControls() {
      const k = this.key;
      $(`${k}-zeta`).value = this.zeta;
      $(`${k}-omega`).value = this.omega;
      $(`${k}-zeta`).addEventListener('input', (e) => { this.zeta = parseFloat(e.target.value); this.refresh(); });
      $(`${k}-omega`).addEventListener('input', (e) => { this.omega = parseFloat(e.target.value); this.refresh(); });
      this.canvas.addEventListener('pointerdown', (e) => this.onPointer(e));
    }

    onPointer() {}
    preUpdate() {}
    drawScene() {}
    justification() { return ''; }

    refresh() {
      const k = this.key;
      $(`${k}-zeta-val`).textContent = this.zeta.toFixed(2);
      $(`${k}-omega-val`).textContent = this.omega.toFixed(1);
      const m = Physics.metrics(this.omega, this.zeta);
      Charts.renderStats($(`${k}-stats`), [
        ['Régimen', m.regime],
        ['Sobreimpulso', m.overshoot > 0 ? `${fmt(m.overshoot, 1)} %` : 'ninguno'],
        ['Asentamiento (2 %)', `${fmt(m.settling)} s`],
      ]);
    }

    frame(dt) {
      this.preUpdate(dt);
      this.stepper.run(dt, (h) => {
        Physics.rk4Step(this.s, this.target, this.omega, this.zeta, h);
        this.t += h;
      });
      const [dest, pos] = this.chart.data.datasets;
      dest.data.push({ x: this.t, y: this.target });
      pos.data.push({ x: this.t, y: this.s.x });
      this.draw();
      if (++this.frameCount % 3 === 0) {
        Charts.setWindow(this.chart, this.t, this.opts.windowS || 6);
        this.chart.update('none');
      }
    }

    draw() {
      const { ctx, w, h } = Charts.fitCanvas(this.canvas);
      ctx.clearRect(0, 0, w, h);
      ctx.textBaseline = 'alphabetic';
      this.drawScene(ctx, w, h);
    }

    resetChart() { this.chart.data.datasets.forEach((d) => { d.data.length = 0; }); }
  }

  // ======================================================================
  // CÁMARA: x = posición de la cámara (px); x_f = posición del personaje
  // ======================================================================
  class CameraCase extends SpringCase {
    constructor() {
      super('camera', { x0: 0, yLabel: 'Posición horizontal (px)', destLabel: 'Personaje (destino)', posLabel: 'Cámara', windowS: 6 });
      this.player = 0; this.goal = null; this.keys = new Set();
      window.addEventListener('keydown', (e) => this.onKey(e, true));
      window.addEventListener('keyup', (e) => this.onKey(e, false));
      $('camera-left').addEventListener('click', () => { this.goal = this.player - 300; });
      $('camera-right').addEventListener('click', () => { this.goal = this.player + 300; });
      $('camera-jump').addEventListener('click', () => { this.player += 300; this.goal = null; });
    }
    active() { return $('view-cases').classList.contains('active') && $('case-camera').classList.contains('active'); }
    onKey(e, down) {
      const map = { ArrowLeft: -1, a: -1, A: -1, ArrowRight: 1, d: 1, D: 1 };
      if (!(e.key in map) || !this.active()) return;
      e.preventDefault();
      if (down) { this.keys.add(map[e.key]); this.goal = null; } else this.keys.delete(map[e.key]);
    }
    onPointer(e) {
      const r = this.canvas.getBoundingClientRect();
      this.goal = this.s.x + (e.clientX - r.left - r.width / 2);
    }
    preUpdate(dt) {
      const SPEED = 280; // px/s: el personaje avanza a velocidad constante; la cámara lo sigue con resorte
      const dir = [...this.keys].reduce((a, b) => a + b, 0);
      if (dir) this.player += dir * SPEED * dt;
      else if (this.goal !== null) {
        const d = this.goal - this.player;
        if (Math.abs(d) <= SPEED * dt) { this.player = this.goal; this.goal = null; }
        else this.player += Math.sign(d) * SPEED * dt;
      }
      this.target = this.player;
    }
    drawScene(ctx, w, h) {
      const cx = w / 2, ground = h * 0.78, cam = this.s.x;
      ctx.fillStyle = '#e8edf3'; ctx.fillRect(0, ground, w, h - ground);
      ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(0, ground); ctx.lineTo(w, ground); ctx.stroke();
      ctx.font = `11px ${FONT}`; ctx.textAlign = 'center';
      const first = Math.floor((cam - cx) / 150) * 150;
      for (let wx = first; wx < cam + cx + 150; wx += 150) {   // pilares fijos en el mundo
        const sx = cx + wx - cam;
        ctx.fillStyle = '#d5dbe4'; ctx.fillRect(sx - 9, ground - 70, 18, 70);
        ctx.fillStyle = COLORS.muted; ctx.fillText(`${wx} px`, sx, ground + 16);
      }
      const px = cx + this.player - cam;
      ctx.fillStyle = COLORS.good; ctx.beginPath(); ctx.roundRect(px - 14, ground - 44, 28, 44, 5); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.fillRect(px - 8, ground - 34, 5, 7); ctx.fillRect(px + 3, ground - 34, 5, 7);
      // visor de la cámara: siempre al centro de la pantalla
      ctx.strokeStyle = COLORS.spring; ctx.lineWidth = 1.5; ctx.setLineDash([5, 4]);
      ctx.strokeRect(cx - 80, ground - 120, 160, 100); ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(cx - 10, ground - 70); ctx.lineTo(cx + 10, ground - 70);
      ctx.moveTo(cx, ground - 80); ctx.lineTo(cx, ground - 60); ctx.stroke();
      ctx.fillStyle = COLORS.spring; ctx.font = `600 12px ${FONT}`; ctx.fillText('cámara', cx, ground - 127);
      ctx.fillStyle = COLORS.muted; ctx.textAlign = 'left'; ctx.font = `12px ${FONT}`;
      ctx.fillText(`retraso: ${Math.abs(this.player - cam).toFixed(0)} px`, 12, 20);
      if (this.goal !== null) {
        const gx = cx + this.goal - cam;
        ctx.strokeStyle = COLORS.target; ctx.setLineDash([3, 4]);
        ctx.beginPath(); ctx.moveTo(gx, ground - 90); ctx.lineTo(gx, ground); ctx.stroke(); ctx.setLineDash([]);
      }
    }
    justification() {
      const d = this.design, m = Physics.metrics(d.omega, d.zeta);
      return `Sin sobreimpulso y se asienta en ${fmt(m.settling)} s: persigue sin marear. ` +
        `Con ζ = 0.5 se pasaría ${fmt(overshootOf(d.omega, 0.5), 1)} % de cada salto y la imagen oscilaría.`;
    }
  }

  // ======================================================================
  // MENÚ: x = borde izquierdo del panel (px); x_f = 0 (abierto) o −ancho (cerrado)
  // ======================================================================
  class MenuCase extends SpringCase {
    constructor() {
      MenuCase.W = 220;
      super('menu', { x0: -MenuCase.W, yLabel: 'Borde izquierdo del menú (px)', destLabel: 'Destino', posLabel: 'Menú',
                      yMin: -250, yMax: 50, yStep: 50, windowS: 4 });
      this.open = false;
      $('menu-toggle').addEventListener('click', () => this.toggle());
    }
    toggle() {
      this.open = !this.open;
      this.target = this.open ? 0 : -MenuCase.W;
      $('menu-toggle').textContent = this.open ? 'Cerrar menú' : 'Abrir menú';
    }
    onPointer() { this.toggle(); }
    drawScene(ctx, w, h) {
      const PW = 250, PH = h - 24, px = (w - PW) / 2, py = 12;
      ctx.fillStyle = '#1f2937';
      ctx.beginPath(); ctx.roundRect(px - 7, py - 7, PW + 14, PH + 14, 24); ctx.fill();   // carcasa
      ctx.save();
      ctx.beginPath(); ctx.roundRect(px, py, PW, PH, 17); ctx.clip();
      ctx.fillStyle = '#f1f5f9'; ctx.fillRect(px, py, PW, PH);
      ctx.fillStyle = '#e2e8f0'; ctx.fillRect(px + 16, py + 44, PW - 32, 70); ctx.fillRect(px + 16, py + 128, PW - 32, 70);
      const progress = Math.max(0, Math.min(1, (this.s.x + MenuCase.W) / MenuCase.W));
      ctx.fillStyle = `rgba(15,23,42,${0.45 * progress})`; ctx.fillRect(px, py, PW, PH);   // velo
      const mx = px + this.s.x;                                                           // borde izquierdo
      ctx.fillStyle = COLORS.spring;
      ctx.fillRect(mx - 80, py, MenuCase.W + 80, PH);  // cuerpo extendido: no deja hueco si rebota
      ctx.fillStyle = '#fff'; ctx.textAlign = 'left';
      ctx.font = `600 15px ${FONT}`; ctx.fillText('Menú', mx + 20, py + 38);
      ctx.font = `14px ${FONT}`;
      ['Inicio', 'Inventario', 'Ajustes', 'Salir'].forEach((t, i) => ctx.fillText(t, mx + 20, py + 80 + i * 34));
      ctx.restore();
    }
    justification() {
      const d = this.design, m = Physics.metrics(d.omega, d.zeta);
      return `Rebota ${fmt(m.overshoot, 1)} % (≈ ${fmt((m.overshoot / 100) * MenuCase.W, 0)} px) y se asienta en ${fmt(m.settling)} s: ` +
        `se siente vivo sin vibrar. Con ζ ≥ 1 llega sin rebote y se siente rígido.`;
    }
  }

  // ======================================================================
  // BARRA DE VIDA: x = HP mostrado; x_f = HP real
  // ======================================================================
  class HealthCase extends SpringCase {
    constructor() {
      super('health', { x0: 100, yLabel: 'Vida mostrada (HP)', destLabel: 'Vida real (destino)', posLabel: 'Barra',
                        yMin: -20, yMax: 120, yStep: 20, windowS: 6 });
      this.lastDir = 0;
      document.querySelectorAll('#case-health [data-hp]').forEach((b) =>
        b.addEventListener('click', () => this.change(parseFloat(b.dataset.hp))));
      $('health-reset').addEventListener('click', () => { this.s = { x: 100, v: 0 }; this.target = 100; this.lastDir = 0; this.resetChart(); });
    }
    change(delta) {
      const next = Math.max(0, Math.min(100, this.target + delta));
      this.lastDir = Math.sign(next - this.target);
      this.target = next;
    }
    drawScene(ctx, w, h) {
      const bw = Math.min(520, w - 60), bh = 32, bx = (w - bw) / 2, by = h / 2 - 8;
      ctx.fillStyle = COLORS.ink; ctx.font = `600 14px ${FONT}`; ctx.textAlign = 'left';
      ctx.fillText('Guerrero · Nvl. 25', bx, by - 16);
      ctx.textAlign = 'right'; ctx.fillStyle = COLORS.spring;
      ctx.fillText(`${Math.max(0, this.s.x).toFixed(0)} / 100 HP`, bx + bw, by - 16);
      ctx.fillStyle = '#e5e7eb'; ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 8); ctx.fill();
      const f = Math.max(0, Math.min(1, this.s.x / 100));
      ctx.save(); ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 8); ctx.clip();
      ctx.fillStyle = f > 0.5 ? '#22c55e' : f > 0.25 ? '#f59e0b' : '#ef4444';
      ctx.fillRect(bx, by, bw * f, bh);
      ctx.restore();
      const tx = bx + bw * (this.target / 100);                   // vida real
      ctx.strokeStyle = COLORS.ink; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(tx, by - 6); ctx.lineTo(tx, by + bh + 6); ctx.stroke();
      ctx.fillStyle = COLORS.muted; ctx.font = `12px ${FONT}`; ctx.textAlign = 'center';
      ctx.fillText(`vida real ${this.target.toFixed(0)}`, Math.min(bx + bw - 30, Math.max(bx + 30, tx)), by + bh + 24);
      if (this.lastDir !== 0 && this.s.v * this.lastDir < -0.5) {
        ctx.fillStyle = COLORS.warn; ctx.font = `600 13px ${FONT}`;
        ctx.fillText('La barra se mueve en sentido contrario al cambio', w / 2, h - 28);
      }
    }
    justification() {
      const d = this.design, m = Physics.metrics(d.omega, d.zeta);
      return `Nunca rebota y baja con peso; se asienta en ${fmt(m.settling)} s. ` +
        `Con ζ = 0.35 se pasaría ${fmt(overshootOf(d.omega, 0.35), 1)} % del daño y subiría después: parecería una curación.`;
    }
  }

  const cases = { camera: new CameraCase(), menu: new MenuCase(), health: new HealthCase() };
  let current = 'camera';

  document.querySelectorAll('#case-tabs .subtab').forEach((b) =>
    b.addEventListener('click', () => {
      current = b.dataset.case;
      document.querySelectorAll('#case-tabs .subtab').forEach((x) => x.classList.toggle('active', x === b));
      document.querySelectorAll('.case').forEach((c) => c.classList.toggle('active', c.id === `case-${current}`));
      cases[current].chart.resize();
    }));

  return {
    frame: (dt) => cases[current].frame(dt),
    onShow: () => cases[current].chart.resize(),
  };
})();
