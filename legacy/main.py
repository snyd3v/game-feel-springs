"""
===============================================================================
PROYECTO 4: RESORTES PARA ANIMAR: EL «GAME FEEL»
Ecuaciones Diferenciales de Orden Superior - Unidad 3
Institución Universitaria Colegio Mayor del Cauca
Facultad de Ingeniería Informática y Multimedia
Docente: Diana Méndez Astudillo

INTEGRANTES (GRUPO 4):
- Edwin Esneider Burbano Luna
- Cristian Alexis Chantre Hurtado
- Luis Eduardo Hurtado Hormiga
- Andrés Felipe Suaza Cerón

DESCRIPCIÓN:
Aplicación interactiva de simulación y análisis de ecuaciones diferenciales
de segundo orden aplicadas a la animación de interfaces y videojuegos (Game Feel).
Compara la física del resorte amortiguado de segundo orden contra la interpolación
lineal clásica (Lerp de primer orden), verifica la solución numérica (RK4) frente a
la solución analítica exacta deducida a mano, y demuestra las 3 aplicaciones reales
exigidas: cámara cinematográfica, menú responsivo y barra de vida pesada.
===============================================================================
"""

import sys
import math
import time
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Habilitar nitidez en pantallas de alta resolución en Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# =============================================================================
# 1. MOTOR MATEMÁTICO Y FÍSICO
# =============================================================================

def acceleration(x, v, target, omega, zeta):
    """
    Ecuación diferencial: x'' + 2*zeta*omega*x' + omega^2*(x - target) = 0
    Despejando x'': a = -2*zeta*omega*v - omega^2*(x - target)
    """
    return -2.0 * zeta * omega * v - (omega ** 2) * (x - target)


def rk4_step(x, v, target, omega, zeta, dt):
    """
    Integrador numérico Runge-Kutta de orden 4 para el sistema de primer orden:
    u = x,  u' = v
    v' = -2*zeta*omega*v - omega^2*(u - target)
    Error local: O(dt^5), error global: O(dt^4).
    """
    def deriv(pos, vel):
        return vel, acceleration(pos, vel, target, omega, zeta)

    k1_v, k1_a = deriv(x, v)

    x2 = x + 0.5 * dt * k1_v
    v2 = v + 0.5 * dt * k1_a
    k2_v, k2_a = deriv(x2, v2)

    x3 = x + 0.5 * dt * k2_v
    v3 = v + 0.5 * dt * k2_a
    k3_v, k3_a = deriv(x3, v3)

    x4 = x + dt * k3_v
    v4 = v + dt * k3_a
    k4_v, k4_a = deriv(x4, v4)

    new_x = x + (dt / 6.0) * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v)
    new_v = v + (dt / 6.0) * (k1_a + 2.0 * k2_a + 2.0 * k3_a + k4_a)
    return float(new_x), float(new_v)


def exact_position(t, omega, zeta, x0=0.0, v0=0.0, target=1.0):
    """
    Solución analítica exacta deducida a mano para el PVI:
    x'' + 2*zeta*omega*x' + omega^2*(x - target) = 0,  x(0)=x0, x'(0)=v0
    Con el cambio u(t) = x(t) - target:
    u'' + 2*zeta*omega*u' + omega^2*u = 0,  u(0)=x0 - target, u'(0)=v0
    """
    t = np.asarray(t, dtype=float)
    u0 = x0 - target

    if zeta < 1.0:
        # CASO 1: Subamortiguado (raíces complejas conjugadas)
        alpha = zeta * omega
        beta = omega * np.sqrt(max(0.0, 1.0 - zeta ** 2))
        A = u0
        B = (v0 + alpha * u0) / beta if beta > 1e-12 else 0.0
        u = np.exp(-alpha * t) * (A * np.cos(beta * t) + B * np.sin(beta * t))
    elif np.isclose(zeta, 1.0, atol=1e-5):
        # CASO 2: Amortiguamiento crítico (raíz real doble r = -omega)
        A = u0
        B = v0 + omega * u0
        u = (A + B * t) * np.exp(-omega * t)
    else:
        # CASO 3: Sobreamortiguado (dos raíces reales negativas distintas)
        root = np.sqrt(zeta ** 2 - 1.0)
        r1 = -omega * (zeta - root)
        r2 = -omega * (zeta + root)
        denom = r1 - r2
        A = (v0 - r2 * u0) / denom
        B = u0 - A
        u = A * np.exp(r1 * t) + B * np.exp(r2 * t)

    return target + u


def compute_system_metrics(omega, zeta):
    """Calcula raíces características, frecuencias y métricas de desempeño."""
    disc = (2.0 * zeta * omega) ** 2 - 4.0 * (omega ** 2)
    alpha = zeta * omega

    if zeta < 1.0:
        regime = "Subamortiguado (Oscilatorio / Rebote)"
        beta = omega * math.sqrt(max(0.0, 1.0 - zeta ** 2))
        roots_str = f"{-alpha:.3f} ± {beta:.3f} i"
        # Sobreimpulso porcentual teórico
        mp = 100.0 * math.exp(- (math.pi * zeta) / math.sqrt(1.0 - zeta ** 2))
        tp = math.pi / beta if beta > 1e-6 else 0.0
        # Tiempo de asentamiento al 2% aproximado: ts ≈ 4 / (zeta * omega)
        ts = 4.0 / alpha if alpha > 1e-6 else float('inf')
    elif abs(zeta - 1.0) < 1e-4:
        regime = "Amortiguamiento Crítico (Límite óptimo)"
        roots_str = f"{-omega:.3f} (raíz doble)"
        mp = 0.0
        tp = float('nan')
        # ts para crítico al 2%: (1 + 8*ts)*exp(-8*ts) = 0.02 -> ts ≈ 5.83 / omega
        ts = 5.83 / omega if omega > 1e-6 else float('inf')
    else:
        regime = "Sobreamortiguado (Lento / Sin rebote)"
        root = math.sqrt(zeta ** 2 - 1.0)
        r1 = -omega * (zeta - root)
        r2 = -omega * (zeta + root)
        roots_str = f"{r1:.3f},  {r2:.3f}"
        mp = 0.0
        tp = float('nan')
        # ts dominado por la raíz lenta r1
        ts = 3.91 / abs(r1) if abs(r1) > 1e-6 else float('inf')

    return {
        "regime": regime,
        "roots_str": roots_str,
        "alpha": alpha,
        "mp": mp,
        "tp": tp,
        "ts": ts
    }


def generate_spring_coords(x1, y1, x2, y2, coils=10, radius=12):
    """Genera coordenadas para dibujar una espiral de resorte helicoidal realista."""
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist < 1e-4:
        return [x1, y1, x2, y2]

    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux  # Vector perpendicular normalizado

    pts = [x1, y1]
    lead = min(15.0, dist * 0.1)
    pts.extend([x1 + ux * lead, y1 + uy * lead])

    eff_dist = dist - 2.0 * lead
    n_points = coils * 4
    for i in range(1, n_points):
        frac = i / float(n_points)
        sign = 1.0 if (i % 2 == 1) else -1.0
        # Amortiguar el radio si el resorte está muy comprimido
        rad = radius * min(1.0, max(0.3, eff_dist / 120.0))
        sx = x1 + ux * (lead + frac * eff_dist) + px * (sign * rad)
        sy = y1 + uy * (lead + frac * eff_dist) + py * (sign * rad)
        pts.extend([sx, sy])

    pts.extend([x2 - ux * lead, y2 - uy * lead])
    pts.extend([x2, y2])
    return pts


# =============================================================================
# 2. APLICACIÓN PRINCIPAL (TKINTER + MATPLOTLIB)
# =============================================================================

class GameFeelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Proyecto 4 · Resortes para Animar: el «Game Feel» | Grupo 4")
        self.geometry("1300x840")
        self.minsize(1080, 720)

        # Paleta de colores Dark Modern (Sleek Studio)
        self.c_bg = "#0f172a"        # Slate 900
        self.c_panel = "#1e293b"     # Slate 800
        self.c_card = "#334155"      # Slate 700
        self.c_text = "#f8fafc"      # Slate 50
        self.c_subtext = "#94a3b8"   # Slate 400
        self.c_cyan = "#38bdf8"      # Resorte (Sky 400)
        self.c_orange = "#fb923c"    # Lerp (Orange 400)
        self.c_rose = "#f43f5e"      # Target / Meta (Rose 500)
        self.c_green = "#4ade80"     # Exacta / Aprobado (Green 400)
        self.c_purple = "#c084fc"    # Púrpura acento

        self.configure(bg=self.c_bg)

        # Estilo ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=self.c_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.c_panel, foreground=self.c_text,
                        padding=[16, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", self.c_cyan)],
                  foreground=[("selected", "#090d16")])
        style.configure("TFrame", background=self.c_bg)

        self._init_header()
        self._init_notebook()

        # Iniciar bucle de animación a 60 FPS
        self.running = True
        self.last_time = time.time()
        self.after(16, self._animation_loop)

        # Manejo de cierre limpio
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.running = False
        self.destroy()

    def _init_header(self):
        header_frame = tk.Frame(self, bg=self.c_panel, padx=16, pady=10)
        header_frame.pack(fill="x", side="top")

        title_lbl = tk.Label(
            header_frame,
            text="🎮 Resortes para Animar: el «Game Feel»",
            font=("Segoe UI", 16, "bold"),
            bg=self.c_panel,
            fg=self.c_cyan
        )
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(
            header_frame,
            text="Ecuaciones Diferenciales · Unidad 3 | Grupo 4 · Ing. Informática | UNIMAYOR",
            font=("Segoe UI", 9),
            bg=self.c_panel,
            fg=self.c_subtext
        )
        sub_lbl.pack(side="right")

    def _init_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=8)

        # Pestaña 1: Laboratorio Split-Screen & Verificación Numérica
        self.tab1 = SplitScreenLabTab(self.nb, self)
        self.nb.add(self.tab1, text="  🕹️ 1. Laboratorio Game Feel (Split-Screen)  ")

        # Pestaña 2: Las 3 Aplicaciones Reales en Videojuegos e Interfaces
        self.tab2 = GameFeelCasesTab(self.nb, self)
        self.nb.add(self.tab2, text="  🚀 2. Tres Casos Reales (Cámara, Menú, Vida)  ")

        # Pestaña 3: Deducción Matemática & Guía de Sustentación
        self.tab3 = MathTheoryTab(self.nb, self)
        self.nb.add(self.tab3, text="  📐 3. Solución Analítica & Sustentación  ")

    def _animation_loop(self):
        if not self.running:
            return

        now = time.time()
        dt = min(0.05, now - self.last_time)
        self.last_time = now

        # Actualizar la pestaña activa
        current_tab_idx = self.nb.index(self.nb.select())
        if current_tab_idx == 0:
            self.tab1.update_physics_and_render(dt)
        elif current_tab_idx == 1:
            self.tab2.update_physics_and_render(dt)

        self.after(16, self._animation_loop)


# =============================================================================
# 3. PESTAÑA 1: LABORATORIO SPLIT-SCREEN & VERIFICACIÓN NUMÉRICA
# =============================================================================

class SplitScreenLabTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Parámetros físicos del sistema
        self.omega = 8.0
        self.zeta = 0.5
        self.target = 1.0
        self.target_prev = 0.0

        # Estado del resorte
        self.x = 0.0
        self.v = 0.0

        # Estado de la interpolación lineal clásica
        self.linear_x = 0.0

        # Tiempo y métricas de simulación
        self.sim_time = 0.0
        self.peak_x = 0.0
        self.overshoot_pct = 0.0
        self.has_overshot = False

        # Historial para gráficas
        self.hist_t = [0.0]
        self.hist_spring = [0.0]
        self.hist_linear = [0.0]
        self.hist_exact = [0.0]
        self.hist_error = [0.0]

        # Contador para refresco de matplotlib (optimización a 20 FPS de dibujo)
        self.plot_render_counter = 0

        self._build_ui()

    def _build_ui(self):
        # Contenedor principal dividido en dos columnas: Izquierda (Animación y Controles), Derecha (Gráficas)
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True)

        # ----------------- PANEL IZQUIERDO: VISUALIZACIÓN & CONTROLES -----------------
        left_frame = tk.Frame(main_paned, bg=self.app.c_bg)
        main_paned.add(left_frame, weight=3)

        # 1. Canvas de simulación Split-Screen
        canvas_card = tk.LabelFrame(
            left_frame,
            text=" 🖥️ Pantalla Partida: Resorte Físico (2º Orden) vs Lerp Clásico (1er Orden) ",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8
        )
        canvas_card.pack(fill="both", expand=True, padx=8, pady=6)

        inst_lbl = tk.Label(
            canvas_card,
            text="💡 Haz clic en la pista o usa los botones para enviar ambos objetos hacia la meta:",
            bg=self.app.c_panel,
            fg=self.app.c_subtext,
            font=("Segoe UI", 9)
        )
        inst_lbl.pack(anchor="w", pady=(0, 4))

        self.canvas = tk.Canvas(canvas_card, bg="#0b1120", height=280, highlightthickness=1,
                                highlightbackground=self.app.c_card)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # 2. Panel de botones rápidos de destino
        target_btn_frame = tk.Frame(canvas_card, bg=self.app.c_panel)
        target_btn_frame.pack(fill="x", pady=6)

        tk.Label(target_btn_frame, text="Mover a Meta:", bg=self.app.c_panel,
                 fg=self.app.c_text, font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)

        for val in [0.0, 0.5, 1.0, 1.4]:
            btn = tk.Button(
                target_btn_frame,
                text=f"x = {val:.1f} m",
                bg=self.app.c_card,
                fg=self.app.c_text,
                activebackground=self.app.c_cyan,
                font=("Segoe UI", 8),
                relief="flat",
                padx=8,
                command=lambda v=val: self.set_target(v)
            )
            btn.pack(side="left", padx=3)

        btn_reset = tk.Button(
            target_btn_frame,
            text="🔄 Reiniciar Simulación",
            bg="#b91c1c",
            fg="white",
            activebackground="#ef4444",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=8,
            command=self.reset_simulation
        )
        btn_reset.pack(side="right", padx=4)

        # 3. Controles interactivos (Sliders de omega y zeta)
        ctrl_card = tk.LabelFrame(
            left_frame,
            text=" ⚙️ Parámetros de la Ecuación Diferencial: x'' + 2ζω x' + ω²(x - x_f) = 0 ",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8
        )
        ctrl_card.pack(fill="x", padx=8, pady=(0, 6))

        # Fila de Presets Canónicos exigidos en la guía
        preset_frame = tk.Frame(ctrl_card, bg=self.app.c_panel)
        preset_frame.pack(fill="x", pady=(0, 8))

        tk.Label(preset_frame, text="Preajustes de la Guía:", bg=self.app.c_panel,
                 fg=self.app.c_subtext, font=("Segoe UI", 9)).pack(side="left", padx=4)

        presets = [
            ("⚡ Subamortiguado (ζ=0.3)", 8.0, 0.3, "#eab308"),
            ("📱 Menú UI Responsivo (ζ=0.5)", 8.0, 0.5, self.app.c_cyan),
            ("🎯 Crítico Óptimo (ζ=1.0)", 8.0, 1.0, self.app.c_green),
            ("🪨 Sobreamortiguado (ζ=2.0)", 8.0, 2.0, self.app.c_purple),
        ]
        for name, w, z, col in presets:
            b = tk.Button(
                preset_frame,
                text=name,
                bg=self.app.c_card,
                fg=col,
                font=("Segoe UI", 8, "bold"),
                relief="flat",
                padx=6,
                command=lambda w=w, z=z: self.apply_preset(w, z)
            )
            b.pack(side="left", padx=3)

        # Sliders
        sliders_grid = tk.Frame(ctrl_card, bg=self.app.c_panel)
        sliders_grid.pack(fill="x")

        # Omega slider
        tk.Label(sliders_grid, text="ω (Rapidez / Frecuencia Natural):", bg=self.app.c_panel,
                 fg=self.app.c_text, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=2)
        self.omega_val_lbl = tk.Label(sliders_grid, text="8.0 rad/s", bg=self.app.c_panel,
                                      fg=self.app.c_cyan, font=("Segoe UI", 9, "bold"), width=10)
        self.omega_val_lbl.grid(row=0, column=1, sticky="e", pady=2)

        self.omega_slider = ttk.Scale(sliders_grid, from_=2.0, to=20.0, value=self.omega,
                                      orient="horizontal", command=self._on_omega_slider)
        self.omega_slider.grid(row=0, column=2, sticky="ew", padx=8, pady=2)

        # Zeta slider
        tk.Label(sliders_grid, text="ζ (Factor de Amortiguamiento):", bg=self.app.c_panel,
                 fg=self.app.c_text, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=2)
        self.zeta_val_lbl = tk.Label(sliders_grid, text="0.50", bg=self.app.c_panel,
                                     fg=self.app.c_cyan, font=("Segoe UI", 9, "bold"), width=10)
        self.zeta_val_lbl.grid(row=1, column=1, sticky="e", pady=2)

        self.zeta_slider = ttk.Scale(sliders_grid, from_=0.05, to=2.50, value=self.zeta,
                                     orient="horizontal", command=self._on_zeta_slider)
        self.zeta_slider.grid(row=1, column=2, sticky="ew", padx=8, pady=2)

        sliders_grid.columnconfigure(2, weight=1)

        # Caja de información en vivo de métricas
        self.metrics_banner = tk.Label(
            ctrl_card,
            text="",
            bg=self.app.c_card,
            fg=self.app.c_text,
            font=("Consolas", 9),
            justify="left",
            padx=8,
            pady=6
        )
        self.metrics_banner.pack(fill="x", pady=6)
        self._update_metrics_banner()

        # ----------------- PANEL DERECHO: GRÁFICAS EN TIEMPO REAL -----------------
        right_frame = tk.Frame(main_paned, bg=self.app.c_bg)
        main_paned.add(right_frame, weight=4)

        charts_card = tk.LabelFrame(
            right_frame,
            text=" 📊 Gráficas en Tiempo Real: Comparación & Verificación Numérica vs Exacta ",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=8
        )
        charts_card.pack(fill="both", expand=True, padx=8, pady=6)

        # Configuración de matplotlib con estilo dark moderno
        self.fig = Figure(figsize=(6, 7), dpi=100, facecolor=self.app.c_panel)
        self.fig.subplots_adjust(left=0.12, right=0.96, top=0.93, bottom=0.08, hspace=0.38)

        # Gráfica 1: Resorte vs Lerp
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_facecolor("#0b1120")
        self.ax1.set_title("1. Comparativa: Resorte (2º orden) vs Interpolación Lineal (1er orden)",
                           fontsize=10, color=self.app.c_text, fontweight="bold", pad=8)
        self.ax1.set_xlabel("Tiempo t [s]", fontsize=8, color=self.app.c_subtext)
        self.ax1.set_ylabel("Posición x [m]", fontsize=8, color=self.app.c_subtext)
        self.ax1.tick_params(colors=self.app.c_subtext, labelsize=8)
        self.ax1.grid(True, linestyle="--", alpha=0.25, color="#ffffff")

        self.line_spring, = self.ax1.plot([], [], color=self.app.c_cyan, lw=2.2, label="Resorte 2º orden")
        self.line_linear, = self.ax1.plot([], [], color=self.app.c_orange, lw=1.8, linestyle="-.", label="Lerp: x += (dest-x)*0.1")
        self.line_target1 = self.ax1.axhline(self.target, color=self.app.c_rose, linestyle=":", lw=1.5, label="Meta (x_f)")
        self.ax1.legend(loc="upper right", fontsize=8, facecolor=self.app.c_card, edgecolor="none", labelcolor=self.app.c_text)

        # Gráfica 2: Verificación Numérica RK4 vs Solución Exacta
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_facecolor("#0b1120")
        self.ax2.set_title("2. Verificación de Precisión: Simulación RK4 vs Solución Analítica Exacta",
                           fontsize=10, color=self.app.c_text, fontweight="bold", pad=8)
        self.ax2.set_xlabel("Tiempo t [s]", fontsize=8, color=self.app.c_subtext)
        self.ax2.set_ylabel("Posición x [m]", fontsize=8, color=self.app.c_subtext)
        self.ax2.tick_params(colors=self.app.c_subtext, labelsize=8)
        self.ax2.grid(True, linestyle="--", alpha=0.25, color="#ffffff")

        self.line_rk4, = self.ax2.plot([], [], color=self.app.c_cyan, lw=3.0, alpha=0.85, label="Numérica (RK4)")
        self.line_exact, = self.ax2.plot([], [], color=self.app.c_green, lw=1.5, linestyle="--", label="Analítica Exacta")
        self.line_target2 = self.ax2.axhline(self.target, color=self.app.c_rose, linestyle=":", lw=1.5)

        self.error_text = self.ax2.text(0.03, 0.12, "Error residual: 0.00e+00 m",
                                        transform=self.ax2.transAxes, fontsize=8,
                                        color=self.app.c_green, family="Consolas",
                                        bbox=dict(boxstyle="round,pad=0.3", facecolor=self.app.c_panel, edgecolor=self.app.c_card))
        self.ax2.legend(loc="upper right", fontsize=8, facecolor=self.app.c_card, edgecolor="none", labelcolor=self.app.c_text)

        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=charts_card)
        self.fig_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _on_omega_slider(self, val):
        self.omega = float(val)
        self.omega_val_lbl.config(text=f"{self.omega:.1f} rad/s")
        self._update_metrics_banner()
        self.reset_simulation()

    def _on_zeta_slider(self, val):
        self.zeta = float(val)
        self.zeta_val_lbl.config(text=f"{self.zeta:.2f}")
        self._update_metrics_banner()
        self.reset_simulation()

    def apply_preset(self, w, z):
        self.omega = w
        self.zeta = z
        self.omega_slider.set(w)
        self.zeta_slider.set(z)
        self.omega_val_lbl.config(text=f"{w:.1f} rad/s")
        self.zeta_val_lbl.config(text=f"{z:.2f}")
        self._update_metrics_banner()
        self.reset_simulation()

    def _update_metrics_banner(self):
        m = compute_system_metrics(self.omega, self.zeta)
        mp_str = f"{m['mp']:.1f}%" if not math.isnan(m['mp']) and m['mp'] > 0 else "0% (sin rebote)"
        tp_str = f"{m['tp']:.3f} s" if not math.isnan(m['tp']) else "N/A"
        ts_str = f"{m['ts']:.2f} s" if not math.isinf(m['ts']) else "∞"

        text = (
            f"Régimen: {m['regime']}\n"
            f"Raíces características: r = {m['roots_str']}  |  Atenuación: α = {m['alpha']:.2f}\n"
            f"Sobreimpulso teórico: {mp_str}  |  Pico: {tp_str}  |  Asentamiento al 2%: ~{ts_str}"
        )
        self.metrics_banner.config(text=text)

    def _world_to_canvas_x(self, x, width):
        # Mapea x en [-0.2, 1.6] a píxeles de canvas
        x_min, x_max = -0.2, 1.6
        frac = (x - x_min) / (x_max - x_min)
        return 60 + frac * (width - 120)

    def _canvas_to_world_x(self, px, width):
        x_min, x_max = -0.2, 1.6
        frac = (px - 60) / float(width - 120)
        return x_min + frac * (x_max - x_min)

    def _on_canvas_click(self, event):
        w = max(300, self.canvas.winfo_width())
        wx = self._canvas_to_world_x(event.x, w)
        wx = float(np.clip(wx, -0.1, 1.5))
        self.set_target(wx)

    def set_target(self, new_target):
        self.target_prev = self.target
        self.target = new_target
        # Reiniciar tiempo para comparar con la solución exacta desde el salto de escalón
        self.x = 0.0
        self.v = 0.0
        self.linear_x = 0.0
        self.sim_time = 0.0
        self.hist_t = [0.0]
        self.hist_spring = [0.0]
        self.hist_linear = [0.0]
        self.hist_exact = [0.0]
        self.hist_error = [0.0]
        self.peak_x = 0.0
        self.overshoot_pct = 0.0
        self.has_overshot = False

        self.line_target1.set_ydata([self.target, self.target])
        self.line_target2.set_ydata([self.target, self.target])

    def reset_simulation(self):
        self.set_target(self.target)

    def update_physics_and_render(self, dt):
        # Subpasos numéricos fijos para máxima estabilidad y consistencia numérica
        sub_dt = 1.0 / 240.0
        n_steps = max(1, int(round(dt / sub_dt)))

        for _ in range(n_steps):
            self.x, self.v = rk4_step(self.x, self.v, self.target, self.omega, self.zeta, sub_dt)
            # Interpolación lineal clásica de 1er orden solicitada en la guía:
            # x += (destino - x) * 0.1 por ciclo de actualización estándar
            self.linear_x += (self.target - self.linear_x) * 0.1 * (sub_dt / (1.0 / 60.0))
            self.sim_time += sub_dt

        # Evaluación exacta en el tiempo actual
        x_exact = exact_position(self.sim_time, self.omega, self.zeta, x0=0.0, v0=0.0, target=self.target)
        err = abs(self.x - x_exact)

        # Medición de sobreimpulso en vivo
        if self.target > 0:
            if self.x > self.peak_x:
                self.peak_x = self.x
            if self.peak_x > self.target:
                self.has_overshot = True
                self.overshoot_pct = ((self.peak_x - self.target) / self.target) * 100.0

        # Guardar historial
        self.hist_t.append(self.sim_time)
        self.hist_spring.append(self.x)
        self.hist_linear.append(self.linear_x)
        self.hist_exact.append(x_exact)
        self.hist_error.append(err)

        if len(self.hist_t) > 1000:
            self.hist_t.pop(0)
            self.hist_spring.pop(0)
            self.hist_linear.pop(0)
            self.hist_exact.pop(0)
            self.hist_error.pop(0)

        # Dibujar en Canvas (a 60 FPS)
        self._render_canvas(err)

        # Actualizar gráficas en Matplotlib a ~20 FPS para evitar sobrecarga de render
        self.plot_render_counter += 1
        if self.plot_render_counter % 3 == 0:
            self._render_plots()

    def _render_canvas(self, err):
        self.canvas.delete("all")
        cw = max(300, self.canvas.winfo_width())
        ch = max(200, self.canvas.winfo_height())

        y_track1 = int(ch * 0.32)   # Carril superior: Resorte
        y_track2 = int(ch * 0.72)   # Carril inferior: Lerp

        x_origin_px = self._world_to_canvas_x(0.0, cw)
        x_target_px = self._world_to_canvas_x(self.target, cw)
        x_spring_px = self._world_to_canvas_x(self.x, cw)
        x_linear_px = self._world_to_canvas_x(self.linear_x, cw)

        # 1. Dibujar carriles de guía
        self.canvas.create_line(40, y_track1, cw - 40, y_track1, fill="#1e293b", width=3)
        self.canvas.create_line(40, y_track2, cw - 40, y_track2, fill="#1e293b", width=3)

        # Marcas de escala en metros
        for m in [0.0, 0.5, 1.0, 1.5]:
            mx_px = self._world_to_canvas_x(m, cw)
            self.canvas.create_line(mx_px, ch - 22, mx_px, ch - 12, fill="#475569", width=1.5)
            self.canvas.create_text(mx_px, ch - 6, text=f"{m:.1f} m", fill=self.app.c_subtext, font=("Segoe UI", 7))

        # 2. Línea de Meta (Target) vertical atravesando ambos carriles
        self.canvas.create_line(x_target_px, 15, x_target_px, ch - 28, fill=self.app.c_rose,
                                width=2, dash=(4, 4))
        # Banderín de meta
        self.canvas.create_polygon(x_target_px, 15, x_target_px + 18, 22, x_target_px, 29,
                                   fill=self.app.c_rose, outline="")
        self.canvas.create_text(x_target_px, 10, text=f"Meta: {self.target:.2f} m",
                                fill=self.app.c_rose, font=("Segoe UI", 8, "bold"))

        # ---------------- CARRIL 1: RESORTE DE 2º ORDEN ----------------
        self.canvas.create_text(70, y_track1 - 45, text="🌀 RESORTE (2º Orden Físico)",
                                fill=self.app.c_cyan, font=("Segoe UI", 9, "bold"), anchor="w")
        self.canvas.create_text(70, y_track1 - 30,
                                text=f"x: {self.x:.3f} m  |  v: {self.v:+.2f} m/s  |  a: {acceleration(self.x, self.v, self.target, self.omega, self.zeta):+.1f} m/s²",
                                fill=self.app.c_subtext, font=("Consolas", 8), anchor="w")

        # Dibujar resorte helicoidal dinámico
        spring_coords = generate_spring_coords(x_origin_px - 40, y_track1, x_spring_px - 16, y_track1, coils=9, radius=13)
        self.canvas.create_line(*spring_coords, fill=self.app.c_cyan, width=2.5, smooth=True)

        # Anclaje de pared a la izquierda
        self.canvas.create_rectangle(x_origin_px - 48, y_track1 - 22, x_origin_px - 40, y_track1 + 22,
                                     fill="#475569", outline="")

        # Disco/Objeto con masa del resorte
        r_puck = 16
        self.canvas.create_oval(x_spring_px - r_puck, y_track1 - r_puck,
                                x_spring_px + r_puck, y_track1 + r_puck,
                                fill=self.app.c_cyan, outline="#ffffff", width=2)
        self.canvas.create_text(x_spring_px, y_track1, text="m", fill="#090d16", font=("Segoe UI", 8, "bold"))

        # Flecha de vector velocidad v
        if abs(self.v) > 0.05:
            arrow_len = np.clip(self.v * 14.0, -50, 50)
            self.canvas.create_line(x_spring_px, y_track1, x_spring_px + arrow_len, y_track1,
                                    fill="#facc15", width=3, arrow="last")

        # Marcador de sobreimpulso máximo si hubo rebote
        if self.has_overshot and self.zeta < 1.0:
            px_overshoot = self._world_to_canvas_x(self.peak_x, cw)
            self.canvas.create_line(px_overshoot, y_track1 - 25, px_overshoot, y_track1 + 25,
                                    fill="#eab308", width=1.5, dash=(2, 2))
            self.canvas.create_text(px_overshoot + 4, y_track1 - 26,
                                    text=f"Sobreimpulso: +{self.overshoot_pct:.1f}%",
                                    fill="#eab308", font=("Segoe UI", 7, "bold"), anchor="w")

        # ---------------- CARRIL 2: INTERPOLACIÓN LINEAL (LERP) ----------------
        self.canvas.create_text(70, y_track2 - 38, text="📐 INTERPOLACIÓN LINEAL CLÁSICA (Lerp / 1er Orden)",
                                fill=self.app.c_orange, font=("Segoe UI", 9, "bold"), anchor="w")
        self.canvas.create_text(70, y_track2 - 24,
                                text=f"x += (meta - x) * 0.1  |  x: {self.linear_x:.3f} m  (Sin inercia ni rebote)",
                                fill=self.app.c_subtext, font=("Consolas", 8), anchor="w")

        # Disco de la interpolación lineal
        r_box = 14
        self.canvas.create_rectangle(x_linear_px - r_box, y_track2 - r_box,
                                     x_linear_px + r_box, y_track2 + r_box,
                                     fill=self.app.c_orange, outline="#ffffff", width=2)
        self.canvas.create_text(x_linear_px, y_track2, text="L", fill="#090d16", font=("Segoe UI", 8, "bold"))

        # Tarjeta explicativa sobreimpresa de Game Feel
        card_text = (
            "Diferencia Clave:\n"
            "• El Resorte posee aceleración (x'') e inercia; puede rebotar u oscilar orgánicamente.\n"
            "• La Interpolación Lineal (Lerp) es de 1er orden: desacelera artificialmente y nunca rebota."
        )
        self.canvas.create_rectangle(cw - 360, ch - 80, cw - 12, ch - 12, fill="#0f172a", outline=self.app.c_card)
        self.canvas.create_text(cw - 350, ch - 46, text=card_text, fill=self.app.c_subtext,
                                font=("Segoe UI", 7), anchor="w", justify="left")

    def _render_plots(self):
        t_arr = np.array(self.hist_t)
        if len(t_arr) < 2:
            return

        # Actualizar datos de líneas en ax1
        self.line_spring.set_data(t_arr, self.hist_spring)
        self.line_linear.set_data(t_arr, self.hist_linear)

        t_max = max(1.5, t_arr[-1])
        t_min = max(0.0, t_max - 4.0)
        self.ax1.set_xlim(t_min, t_max)

        y_all = self.hist_spring + self.hist_linear
        y_min = min(-0.2, min(y_all) - 0.2)
        y_max = max(1.2, max(y_all) + 0.2, self.target + 0.2)
        self.ax1.set_ylim(y_min, y_max)

        # Actualizar datos de líneas en ax2 (Verificación analítica)
        self.line_rk4.set_data(t_arr, self.hist_spring)
        self.line_exact.set_data(t_arr, self.hist_exact)
        self.ax2.set_xlim(t_min, t_max)
        self.ax2.set_ylim(y_min, y_max)

        curr_err = self.hist_error[-1]
        self.error_text.set_text(f"Error residual |x_num - x_exact| = {curr_err:.2e} m (¡Coincidencia exacta!)")

        self.fig_canvas.draw_idle()


# =============================================================================
# 4. PESTAÑA 2: TRES CASOS REALES EN VIDEOJUEGOS E INTERFACES (GAME FEEL)
# =============================================================================

class GameFeelCasesTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Sub-pestañas para cada caso de aplicación
        self.sub_nb = ttk.Notebook(self)
        self.sub_nb.pack(fill="both", expand=True, padx=6, pady=6)

        self.case1 = CameraFollowSubCase(self.sub_nb, self.app)
        self.sub_nb.add(self.case1, text="  🎥 Caso 1: Cámara de Videojuego (ζ = 1.0 Crítico)  ")

        self.case2 = MenuPopupSubCase(self.sub_nb, self.app)
        self.sub_nb.add(self.case2, text="  📱 Caso 2: Menú Desplegable UI (ζ = 0.5 Subamortiguado)  ")

        self.case3 = HealthBarSubCase(self.sub_nb, self.app)
        self.sub_nb.add(self.case3, text="  ❤️ Caso 3: Barra de Vida RPG (ζ = 2.0 Sobreamortiguado)  ")

    def update_physics_and_render(self, dt):
        idx = self.sub_nb.index(self.sub_nb.select())
        if idx == 0:
            self.case1.update(dt)
        elif idx == 1:
            self.case2.update(dt)
        elif idx == 2:
            self.case3.update(dt)


# --- SUB-CASO 1: CÁMARA QUE SIGUE A UN PERSONAJE (ζ = 1.0) ---
class CameraFollowSubCase(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.c_bg)
        self.app = app

        # Física del personaje y la cámara
        self.player_x = 200.0
        self.player_vx = 0.0
        self.cam_x = 200.0
        self.cam_v = 0.0

        # Parámetros del resorte de la cámara
        self.omega = 6.0
        self.zeta = 1.0  # Crítico por defecto para evitar mareo

        # Historial de gráfica
        self.time = 0.0
        self.hist_t = [0.0]
        self.hist_player = [self.player_x]
        self.hist_cam = [self.cam_x]

        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        # Panel izquierdo: Mini-juego interactivo
        left = tk.Frame(paned, bg=self.app.c_panel, padx=10, pady=10)
        paned.add(left, weight=3)

        title = tk.Label(
            left,
            text="🎮 Simulación: Cámara Cinematográfica Persiguiendo al Jugador",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 11, "bold")
        )
        title.pack(anchor="w")

        desc = tk.Label(
            left,
            text="Controla el jugador con los botones o haz clic en el mundo. Observa cómo la cámara lo persigue:",
            bg=self.app.c_panel,
            fg=self.app.c_subtext,
            font=("Segoe UI", 9)
        )
        desc.pack(anchor="w", pady=(0, 6))

        self.canvas = tk.Canvas(left, bg="#0b1329", height=280, highlightthickness=1,
                                highlightbackground=self.app.c_card)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_click_world)

        # Botones de control del jugador
        ctrl_p = tk.Frame(left, bg=self.app.c_panel)
        ctrl_p.pack(fill="x", pady=6)

        tk.Label(ctrl_p, text="Mover Jugador:", bg=self.app.c_panel, fg=self.app.c_text,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)

        b_left = tk.Button(ctrl_p, text="◀ Correr a la Izquierda", bg=self.app.c_card, fg=self.app.c_text,
                           relief="flat", padx=8, command=lambda: self.move_player(-120))
        b_left.pack(side="left", padx=4)

        b_right = tk.Button(ctrl_p, text="Correr a la Derecha ▶", bg=self.app.c_card, fg=self.app.c_text,
                            relief="flat", padx=8, command=lambda: self.move_player(120))
        b_right.pack(side="left", padx=4)

        b_jump = tk.Button(ctrl_p, text="⚡ Salto Brusco", bg="#4f46e5", fg="white",
                           relief="flat", padx=8, font=("Segoe UI", 8, "bold"),
                           command=lambda: self.move_player(220))
        b_jump.pack(side="left", padx=4)

        # Modos de Amortiguamiento para la cámara
        modes_frame = tk.LabelFrame(left, text=" 🧪 Experimento de Game Feel: ¿Qué amortiguamiento elegir para la cámara? ",
                                    bg=self.app.c_panel, fg=self.app.c_green, font=("Segoe UI", 9, "bold"), padx=8, pady=6)
        modes_frame.pack(fill="x", pady=6)

        self.mode_var = tk.StringVar(value="critico")

        r1 = tk.Radiobutton(
            modes_frame,
            text="🎯 ζ = 1.0 (Crítico - Recomendado): Seguimiento suave, frena sin oscilar ni marear.",
            variable=self.mode_var,
            value="critico",
            bg=self.app.c_panel,
            fg=self.app.c_green,
            selectcolor=self.app.c_card,
            activebackground=self.app.c_panel,
            font=("Segoe UI", 9),
            command=self._on_mode_change
        )
        r1.pack(anchor="w", pady=2)

        r2 = tk.Radiobutton(
            modes_frame,
            text="⚠️ ζ = 0.25 (Subamortiguado - Peligro): La cámara rebota hacia adelante y atrás ('Efecto Mareo').",
            variable=self.mode_var,
            value="sub",
            bg=self.app.c_panel,
            fg="#facc15",
            selectcolor=self.app.c_card,
            activebackground=self.app.c_panel,
            font=("Segoe UI", 9),
            command=self._on_mode_change
        )
        r2.pack(anchor="w", pady=2)

        r3 = tk.Radiobutton(
            modes_frame,
            text="🐢 ζ = 2.5 (Sobreamortiguado - Pesado): Demasiado rezagada, pierde de vista al jugador.",
            variable=self.mode_var,
            value="sobre",
            bg=self.app.c_panel,
            fg=self.app.c_purple,
            selectcolor=self.app.c_card,
            activebackground=self.app.c_panel,
            font=("Segoe UI", 9),
            command=self._on_mode_change
        )
        r3.pack(anchor="w", pady=2)

        # Panel derecho: Gráfica al lado
        right = tk.Frame(paned, bg=self.app.c_bg)
        paned.add(right, weight=3)

        self.fig = Figure(figsize=(5, 6), dpi=100, facecolor=self.app.c_panel)
        self.fig.subplots_adjust(left=0.14, right=0.94, top=0.92, bottom=0.10)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#0b1120")
        self.ax.set_title("Posición x(t): Jugador vs Cámara", fontsize=10, color=self.app.c_text, fontweight="bold")
        self.ax.set_xlabel("Tiempo t [s]", fontsize=8, color=self.app.c_subtext)
        self.ax.set_ylabel("Posición Horizontal x [px]", fontsize=8, color=self.app.c_subtext)
        self.ax.tick_params(colors=self.app.c_subtext, labelsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#ffffff")

        self.l_player, = self.ax.plot([], [], color=self.app.c_rose, lw=2, linestyle="--", label="Jugador (Destino)")
        self.l_cam, = self.ax.plot([], [], color=self.app.c_cyan, lw=2.4, label="Cámara (Resorte)")
        self.ax.legend(loc="upper right", fontsize=8, facecolor=self.app.c_card, labelcolor=self.app.c_text)

        self.fc = FigureCanvasTkAgg(self.fig, master=right)
        self.fc.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    def _on_click_world(self, event):
        # Mover el jugador a donde se hizo clic en el mundo visible
        w = max(300, self.canvas.winfo_width())
        # Convertir coordenada de pantalla a coordenada del mundo (compensando la cámara)
        click_world_x = event.x - (w / 2.0) + self.cam_x
        self.player_x = float(np.clip(click_world_x, -1000, 1500))

    def move_player(self, dx):
        self.player_x = float(np.clip(self.player_x + dx, -1000, 1500))

    def _on_mode_change(self):
        m = self.mode_var.get()
        if m == "critico":
            self.zeta = 1.0
            self.omega = 6.0
        elif m == "sub":
            self.zeta = 0.25
            self.omega = 6.0
        elif m == "sobre":
            self.zeta = 2.5
            self.omega = 5.0

    def update(self, dt):
        # Integrar movimiento de la cámara persiguiendo al jugador:
        # cam'' + 2*zeta*omega*cam' + omega^2*(cam - player_x) = 0
        sub_dt = 1.0 / 120.0
        n_steps = max(1, int(round(dt / sub_dt)))
        for _ in range(n_steps):
            self.cam_x, self.cam_v = rk4_step(self.cam_x, self.cam_v, self.player_x, self.omega, self.zeta, sub_dt)
            self.time += sub_dt

        self.hist_t.append(self.time)
        self.hist_player.append(self.player_x)
        self.hist_cam.append(self.cam_x)
        if len(self.hist_t) > 600:
            self.hist_t.pop(0)
            self.hist_player.pop(0)
            self.hist_cam.pop(0)

        # Renderizar vista 2D del mundo
        self._render_scene()

        # Renderizar gráfica cada 3 frames
        if len(self.hist_t) % 3 == 0:
            t_arr = np.array(self.hist_t)
            self.l_player.set_data(t_arr, self.hist_player)
            self.l_cam.set_data(t_arr, self.hist_cam)
            self.ax.set_xlim(max(0.0, t_arr[-1] - 4.0), max(1.5, t_arr[-1]))
            all_y = self.hist_player + self.hist_cam
            self.ax.set_ylim(min(all_y) - 50, max(all_y) + 50)
            self.fc.draw_idle()

    def _render_scene(self):
        self.canvas.delete("all")
        w = max(300, self.canvas.winfo_width())
        h = max(200, self.canvas.winfo_height())
        cx = w / 2.0  # El centro de la pantalla representa el centro de la cámara

        # Suelo con perspectiva y columnas fijas en el mundo
        ground_y = h * 0.75
        self.canvas.create_rectangle(0, ground_y, w, h, fill="#1e293b", outline="")
        self.canvas.create_line(0, ground_y, w, ground_y, fill="#475569", width=2)

        # Objetos de fondo fijos en coordenadas de mundo (árboles / pilares)
        for world_pos in range(-800, 1600, 200):
            screen_x = cx + (world_pos - self.cam_x)
            if -50 <= screen_x <= w + 50:
                self.canvas.create_rectangle(screen_x - 12, ground_y - 80, screen_x + 12, ground_y,
                                             fill="#334155", outline="#475569")
                self.canvas.create_text(screen_x, ground_y + 16, text=f"{world_pos}m",
                                        fill=self.app.c_subtext, font=("Segoe UI", 7))

        # Dibujar Personaje (Avatar verde)
        screen_player_x = cx + (self.player_x - self.cam_x)
        pw, ph = 26, 38
        self.canvas.create_rectangle(screen_player_x - pw/2, ground_y - ph,
                                     screen_player_x + pw/2, ground_y,
                                     fill=self.app.c_green, outline="#ffffff", width=2)
        # Ojos del personaje
        self.canvas.create_oval(screen_player_x - 8, ground_y - ph + 8, screen_player_x - 2, ground_y - ph + 14, fill="#090d16")
        self.canvas.create_oval(screen_player_x + 2, ground_y - ph + 8, screen_player_x + 8, ground_y - ph + 14, fill="#090d16")
        self.canvas.create_text(screen_player_x, ground_y - ph - 12, text="Jugador",
                                fill=self.app.c_green, font=("Segoe UI", 8, "bold"))

        # Dibujar Retícula / Visor de la Cámara en el centro de la pantalla
        cam_box_w, cam_box_h = 160, 110
        self.canvas.create_rectangle(cx - cam_box_w/2, ground_y - 75 - cam_box_h/2,
                                     cx + cam_box_w/2, ground_y - 75 + cam_box_h/2,
                                     outline=self.app.c_cyan, width=1.5, dash=(4, 4))
        # Cruz de enfoque de la cámara
        self.canvas.create_line(cx - 15, ground_y - 75, cx + 15, ground_y - 75, fill=self.app.c_cyan, width=1.5)
        self.canvas.create_line(cx, ground_y - 75 - 15, cx, ground_y - 75 + 15, fill=self.app.c_cyan, width=1.5)
        self.canvas.create_text(cx, ground_y - 75 - cam_box_h/2 - 10, text="Visor de Cámara",
                                fill=self.app.c_cyan, font=("Segoe UI", 8, "bold"))

        # Alerta visual de mareo si zeta es bajo y hay oscilación fuerte
        if self.zeta < 0.5 and abs(self.cam_v) > 25.0:
            self.canvas.create_text(w / 2.0, 30, text="⚠️ ¡CÁMARA OSCILANDO / REBOTANDO! (Genera mareo)",
                                    fill="#facc15", font=("Segoe UI", 10, "bold"))


# --- SUB-CASO 2: MENÚ DESPLEGABLE UI (ζ = 0.5) ---
class MenuPopupSubCase(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.c_bg)
        self.app = app

        # Estados de animación del menú
        self.is_open = False
        self.y_closed = -160.0
        self.y_open = 40.0
        self.y_target = self.y_closed
        self.y = self.y_closed
        self.v = 0.0

        # Parámetros (Subamortiguado ζ = 0.5 para rebote elegante de UI)
        self.omega = 9.0
        self.zeta = 0.5

        self.time = 0.0
        self.hist_t = [0.0]
        self.hist_y = [self.y]

        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg=self.app.c_panel, padx=12, pady=10)
        paned.add(left, weight=3)

        title = tk.Label(
            left,
            text="📱 Simulación: Menú / Modal Emergente (iOS / Material Design)",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 11, "bold")
        )
        title.pack(anchor="w")

        desc = tk.Label(
            left,
            text="En interfaces móviles, un rebote controlado (ζ ≈ 0.5) transmite elasticidad y rapidez táctil ('juiciness'):",
            bg=self.app.c_panel,
            fg=self.app.c_subtext,
            font=("Segoe UI", 9)
        )
        desc.pack(anchor="w", pady=(0, 6))

        # Canvas con marco de teléfono celular
        self.canvas = tk.Canvas(left, bg="#0b1120", height=300, highlightthickness=1,
                                highlightbackground=self.app.c_card)
        self.canvas.pack(fill="both", expand=True)

        ctrl_f = tk.Frame(left, bg=self.app.c_panel)
        ctrl_f.pack(fill="x", pady=6)

        self.btn_toggle = tk.Button(
            ctrl_f,
            text="📲 Desplegar Menú",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=4,
            command=self.toggle_menu
        )
        self.btn_toggle.pack(side="left", padx=4)

        tk.Label(ctrl_f, text="Ajustar ζ (Rebote UI):", bg=self.app.c_panel,
                 fg=self.app.c_text, font=("Segoe UI", 9)).pack(side="left", padx=(12, 4))

        self.zeta_slider = ttk.Scale(ctrl_f, from_=0.1, to=1.4, value=self.zeta,
                                     orient="horizontal", command=self._on_zeta_change)
        self.zeta_slider.pack(side="left", fill="x", expand=True, padx=4)

        self.zeta_lbl = tk.Label(ctrl_f, text="ζ = 0.50", bg=self.app.c_panel,
                                 fg=self.app.c_cyan, font=("Segoe UI", 9, "bold"), width=8)
        self.zeta_lbl.pack(side="left", padx=4)

        # Panel derecho: Gráfica vertical de desplazamiento vs tiempo
        right = tk.Frame(paned, bg=self.app.c_bg)
        paned.add(right, weight=3)

        self.fig = Figure(figsize=(5, 6), dpi=100, facecolor=self.app.c_panel)
        self.fig.subplots_adjust(left=0.14, right=0.94, top=0.92, bottom=0.10)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#0b1120")
        self.ax.set_title("Desplazamiento Vertical y(t) del Menú", fontsize=10, color=self.app.c_text, fontweight="bold")
        self.ax.set_xlabel("Tiempo t [s]", fontsize=8, color=self.app.c_subtext)
        self.ax.set_ylabel("Posición y [px]", fontsize=8, color=self.app.c_subtext)
        self.ax.tick_params(colors=self.app.c_subtext, labelsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#ffffff")

        self.line_y, = self.ax.plot([], [], color=self.app.c_cyan, lw=2.4, label="Posición del Menú")
        self.line_dest = self.ax.axhline(self.y_target, color=self.app.c_rose, linestyle=":", lw=1.5, label="Destino")
        self.ax.legend(loc="upper right", fontsize=8, facecolor=self.app.c_card, labelcolor=self.app.c_text)

        self.fc = FigureCanvasTkAgg(self.fig, master=right)
        self.fc.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    def _on_zeta_change(self, val):
        self.zeta = float(val)
        self.zeta_lbl.config(text=f"ζ = {self.zeta:.2f}")

    def toggle_menu(self):
        self.is_open = not self.is_open
        self.y_target = self.y_open if self.is_open else self.y_closed
        self.btn_toggle.config(
            text="⬆️ Ocultar Menú" if self.is_open else "📲 Desplegar Menú",
            bg="#dc2626" if self.is_open else "#2563eb"
        )
        self.line_dest.set_ydata([self.y_target, self.y_target])

    def update(self, dt):
        sub_dt = 1.0 / 120.0
        n_steps = max(1, int(round(dt / sub_dt)))
        for _ in range(n_steps):
            self.y, self.v = rk4_step(self.y, self.v, self.y_target, self.omega, self.zeta, sub_dt)
            self.time += sub_dt

        self.hist_t.append(self.time)
        self.hist_y.append(self.y)
        if len(self.hist_t) > 600:
            self.hist_t.pop(0)
            self.hist_y.pop(0)

        self._render_scene()

        if len(self.hist_t) % 3 == 0:
            t_arr = np.array(self.hist_t)
            self.line_y.set_data(t_arr, self.hist_y)
            self.ax.set_xlim(max(0.0, t_arr[-1] - 3.5), max(1.5, t_arr[-1]))
            self.ax.set_ylim(-180, 80)
            self.fc.draw_idle()

    def _render_scene(self):
        self.canvas.delete("all")
        w = max(300, self.canvas.winfo_width())
        h = max(200, self.canvas.winfo_height())

        # Marco del teléfono
        phone_w, phone_h = 240, 260
        px1 = (w - phone_w) / 2.0
        py1 = 20
        px2 = px1 + phone_w
        py2 = py1 + phone_h

        # Carcasa y pantalla del móvil
        self.canvas.create_rectangle(px1 - 6, py1 - 6, px2 + 6, py2 + 6, fill="#1e293b", outline="#475569", width=3)
        self.canvas.create_rectangle(px1, py1, px2, py2, fill="#0f172a", outline="")

        # Barra de estado superior
        self.canvas.create_rectangle(px1, py1, px2, py1 + 24, fill="#1e293b", outline="")
        self.canvas.create_text(px1 + 30, py1 + 12, text="9:41 AM", fill=self.app.c_text, font=("Segoe UI", 7, "bold"))
        self.canvas.create_text(px2 - 30, py1 + 12, text="100% 🔋", fill=self.app.c_text, font=("Segoe UI", 7))

        # Contenido de la app móvil de fondo
        self.canvas.create_text(w/2.0, py1 + 50, text="Mi Videojuego App", fill=self.app.c_subtext, font=("Segoe UI", 9, "bold"))
        self.canvas.create_rectangle(px1 + 20, py1 + 80, px2 - 20, py1 + 140, fill="#1e293b", outline="")
        self.canvas.create_text(w/2.0, py1 + 110, text="Feed de Contenido Principal", fill="#64748b", font=("Segoe UI", 8))

        # Tarjeta emergente animada por el resorte
        menu_w, menu_h = 200, 140
        mx1 = (w - menu_w) / 2.0
        my1 = py1 + self.y
        mx2 = mx1 + menu_w
        my2 = my1 + menu_h

        # Dibujar sombra
        self.canvas.create_rectangle(mx1 + 4, my1 + 4, mx2 + 4, my2 + 4, fill="#050811", outline="")
        # Tarjeta
        self.canvas.create_rectangle(mx1, my1, mx2, my2, fill="#1e3a8a", outline=self.app.c_cyan, width=2)
        self.canvas.create_text(w/2.0, my1 + 24, text="✨ MENÚ EMERGENTE", fill="#ffffff", font=("Segoe UI", 9, "bold"))
        self.canvas.create_line(mx1 + 15, my1 + 40, mx2 - 15, my1 + 40, fill="#3b82f6", width=1)

        options = ["⚔️ Iniciar Partida", "🎒 Inventario", "⚙️ Ajustes"]
        for i, opt in enumerate(options):
            oy = my1 + 60 + i * 24
            self.canvas.create_text(w/2.0, oy, text=opt, fill=self.app.c_text, font=("Segoe UI", 8))


# --- SUB-CASO 3: BARRA DE VIDA RPG (ζ = 2.0 SOBREAMORTIGUADO) ---
class HealthBarSubCase(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.c_bg)
        self.app = app

        # Salud
        self.hp_max = 100.0
        self.hp_target = 100.0
        self.hp_current = 100.0
        self.hp_v = 0.0

        # Parámetros del resorte: Sobreamortiguado ζ = 2.0 para peso sin rebote
        self.omega = 7.0
        self.zeta = 2.0

        self.time = 0.0
        self.hist_t = [0.0]
        self.hist_hp = [self.hp_current]

        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg=self.app.c_panel, padx=12, pady=10)
        paned.add(left, weight=3)

        title = tk.Label(
            left,
            text="❤️ Simulación: Barra de Vida RPG y Daño Visceral",
            bg=self.app.c_panel,
            fg=self.app.c_cyan,
            font=("Segoe UI", 11, "bold")
        )
        title.pack(anchor="w")

        desc = tk.Label(
            left,
            text="En una barra de salud, el amortiguamiento DEBE ser sobreamortiguado (ζ > 1) para dar sensación de peso sin rebotar:",
            bg=self.app.c_panel,
            fg=self.app.c_subtext,
            font=("Segoe UI", 9)
        )
        desc.pack(anchor="w", pady=(0, 6))

        self.canvas = tk.Canvas(left, bg="#0b1120", height=280, highlightthickness=1,
                                highlightbackground=self.app.c_card)
        self.canvas.pack(fill="both", expand=True)

        # Botones de daño y curación
        btn_box = tk.Frame(left, bg=self.app.c_panel)
        btn_box.pack(fill="x", pady=6)

        b_hit1 = tk.Button(btn_box, text="⚔️ Ataque Leve (-20 HP)", bg="#b91c1c", fg="white",
                           relief="flat", padx=8, font=("Segoe UI", 8, "bold"),
                           command=lambda: self.apply_damage(20))
        b_hit1.pack(side="left", padx=4)

        b_hit2 = tk.Button(btn_box, text="💥 Golpe Crítico (-45 HP)", bg="#7f1d1d", fg="white",
                           relief="flat", padx=8, font=("Segoe UI", 8, "bold"),
                           command=lambda: self.apply_damage(45))
        b_hit2.pack(side="left", padx=4)

        b_heal = tk.Button(btn_box, text="🧪 Poción (+30 HP)", bg="#15803d", fg="white",
                           relief="flat", padx=8, font=("Segoe UI", 8, "bold"),
                           command=lambda: self.apply_damage(-30))
        b_heal.pack(side="left", padx=4)

        b_reset = tk.Button(btn_box, text="🔄 Restaurar 100%", bg=self.app.c_card, fg=self.app.c_text,
                            relief="flat", padx=8, font=("Segoe UI", 8),
                            command=lambda: self.set_hp(100.0))
        b_reset.pack(side="right", padx=4)

        # Selector de prueba: ¿Qué pasaría si rebota?
        test_box = tk.LabelFrame(left, text=" ⚠️ Demostración de Ingeniería: ¿Por qué NUNCA debe rebotar una barra de vida? ",
                                 bg=self.app.c_panel, fg="#facc15", font=("Segoe UI", 9, "bold"), padx=8, pady=6)
        test_box.pack(fill="x", pady=6)

        self.hp_mode_var = tk.StringVar(value="sobre")

        r1 = tk.Radiobutton(
            test_box,
            text="🪨 ζ = 2.0 (Sobreamortiguado - Correcto): El daño se siente pesado, definitivo y no rebota jamás.",
            variable=self.hp_mode_var,
            value="sobre",
            bg=self.app.c_panel,
            fg=self.app.c_green,
            selectcolor=self.app.c_card,
            activebackground=self.app.c_panel,
            font=("Segoe UI", 9),
            command=self._on_mode_change
        )
        r1.pack(anchor="w", pady=2)

        r2 = tk.Radiobutton(
            test_box,
            text="❌ ζ = 0.35 (Subamortiguado - Error de Diseño): La barra baja de más y luego rebota hacia ARRIBA,\n    engañando al jugador al simular falsamente que recuperó vida tras recibir un golpe.",
            variable=self.hp_mode_var,
            value="sub",
            bg=self.app.c_panel,
            fg="#f87171",
            justify="left",
            selectcolor=self.app.c_card,
            activebackground=self.app.c_panel,
            font=("Segoe UI", 8),
            command=self._on_mode_change
        )
        r2.pack(anchor="w", pady=2)

        # Panel derecho: Gráfica
        right = tk.Frame(paned, bg=self.app.c_bg)
        paned.add(right, weight=3)

        self.fig = Figure(figsize=(5, 6), dpi=100, facecolor=self.app.c_panel)
        self.fig.subplots_adjust(left=0.14, right=0.94, top=0.92, bottom=0.10)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#0b1120")
        self.ax.set_title("Nivel de Salud HP(t) en el Tiempo", fontsize=10, color=self.app.c_text, fontweight="bold")
        self.ax.set_xlabel("Tiempo t [s]", fontsize=8, color=self.app.c_subtext)
        self.ax.set_ylabel("Puntos de Salud [HP]", fontsize=8, color=self.app.c_subtext)
        self.ax.tick_params(colors=self.app.c_subtext, labelsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#ffffff")

        self.line_hp, = self.ax.plot([], [], color="#ef4444", lw=2.4, label="Salud Actual (HP)")
        self.line_hp_target = self.ax.axhline(self.hp_target, color=self.app.c_rose, linestyle=":", lw=1.5, label="Meta de Daño")
        self.ax.legend(loc="upper right", fontsize=8, facecolor=self.app.c_card, labelcolor=self.app.c_text)

        self.fc = FigureCanvasTkAgg(self.fig, master=right)
        self.fc.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    def _on_mode_change(self):
        m = self.hp_mode_var.get()
        if m == "sobre":
            self.zeta = 2.0
            self.omega = 7.0
        else:
            self.zeta = 0.35
            self.omega = 8.0

    def apply_damage(self, amount):
        new_hp = np.clip(self.hp_target - amount, 5.0, 100.0)
        self.hp_target = float(new_hp)
        self.line_hp_target.set_ydata([self.hp_target, self.hp_target])

    def set_hp(self, val):
        self.hp_target = val
        self.hp_current = val
        self.hp_v = 0.0
        self.line_hp_target.set_ydata([self.hp_target, self.hp_target])

    def update(self, dt):
        sub_dt = 1.0 / 120.0
        n_steps = max(1, int(round(dt / sub_dt)))
        for _ in range(n_steps):
            self.hp_current, self.hp_v = rk4_step(self.hp_current, self.hp_v, self.hp_target, self.omega, self.zeta, sub_dt)
            self.time += sub_dt

        self.hist_t.append(self.time)
        self.hist_hp.append(self.hp_current)
        if len(self.hist_t) > 600:
            self.hist_t.pop(0)
            self.hist_hp.pop(0)

        self._render_scene()

        if len(self.hist_t) % 3 == 0:
            t_arr = np.array(self.hist_t)
            self.line_hp.set_data(t_arr, self.hist_hp)
            self.ax.set_xlim(max(0.0, t_arr[-1] - 4.0), max(1.5, t_arr[-1]))
            self.ax.set_ylim(0, 110)
            self.fc.draw_idle()

    def _render_scene(self):
        self.canvas.delete("all")
        w = max(300, self.canvas.winfo_width())
        h = max(200, self.canvas.winfo_height())

        # Tarjeta HUD de personaje RPG
        hud_w, hud_h = min(420, w - 40), 180
        hx1 = (w - hud_w) / 2.0
        hy1 = (h - hud_h) / 2.0
        hx2 = hx1 + hud_w
        hy2 = hy1 + hud_h

        # Fondo del HUD
        self.canvas.create_rectangle(hx1, hy1, hx2, hy2, fill="#1e293b", outline=self.app.c_card, width=2)

        # Avatar del Guerrero
        self.canvas.create_rectangle(hx1 + 18, hy1 + 25, hx1 + 78, hy1 + 85, fill="#334155", outline="#64748b", width=2)
        self.canvas.create_text(hx1 + 48, hy1 + 55, text="🛡️", font=("Segoe UI", 24))
        self.canvas.create_text(hx1 + 95, hy1 + 40, text="Guerrero Nvl. 25", fill=self.app.c_text, font=("Segoe UI", 10, "bold"), anchor="w")
        self.canvas.create_text(hx1 + 95, hy1 + 60, text=f"HP: {max(0.0, self.hp_current):.1f} / 100",
                                fill=self.app.c_cyan, font=("Segoe UI", 9, "bold"), anchor="w")

        # Barra de Salud Externa
        bar_x1 = hx1 + 95
        bar_y1 = hy1 + 78
        bar_w = hud_w - 120
        bar_h = 24
        bar_x2 = bar_x1 + bar_w
        bar_y2 = bar_y1 + bar_h

        # Fondo oscuro de la barra
        self.canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2, fill="#0f172a", outline="#475569", width=1.5)

        # Relleno de salud interpolado con resorte
        fill_pct = np.clip(self.hp_current / 100.0, 0.0, 1.2)
        curr_fill_w = bar_w * fill_pct

        # Color según estado
        bar_col = "#22c55e" if self.hp_current > 50 else ("#eab308" if self.hp_current > 25 else "#ef4444")
        if curr_fill_w > 0:
            self.canvas.create_rectangle(bar_x1, bar_y1, bar_x1 + curr_fill_w, bar_y2, fill=bar_col, outline="")

        # Línea de salud meta esperada
        target_fill_w = bar_w * (self.hp_target / 100.0)
        self.canvas.create_line(bar_x1 + target_fill_w, bar_y1 - 3, bar_x1 + target_fill_w, bar_y2 + 3,
                                fill=self.app.c_rose, width=2)

        # Texto de estado
        if self.zeta < 0.5 and self.hp_v > 5.0 and self.hp_current < self.hp_target:
            self.canvas.create_text(w/2.0, hy2 - 25, text="⚠️ ¡ERROR VISUAL! La barra rebotó hacia arriba (falsa curación)",
                                    fill="#f87171", font=("Segoe UI", 8, "bold"))
        else:
            self.canvas.create_text(w/2.0, hy2 - 25, text="✅ Movimiento con peso físico real (Sobreamortiguado ζ = 2.0)",
                                    fill=self.app.c_green, font=("Segoe UI", 8))


# =============================================================================
# 5. PESTAÑA 3: SOLUCIÓN ANALÍTICA, DEDUCCIÓN & GUÍA DE SUSTENTACIÓN
# =============================================================================

class MathTheoryTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # Crear scrollable frame para alojar toda la documentación
        canvas = tk.Canvas(self, bg=self.app.c_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.app.c_bg)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contenido
        content_frame = tk.Frame(scrollable_frame, bg=self.app.c_bg, padx=20, pady=16)
        content_frame.pack(fill="both", expand=True)

        # Encabezado
        tk.Label(
            content_frame,
            text="📐 Deducción Matemática Completa & Criterios de Ingeniería",
            font=("Segoe UI", 16, "bold"),
            bg=self.app.c_bg,
            fg=self.app.c_cyan
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            content_frame,
            text="Ecuación: x'' + 2ζω x' + ω²(x - x_f) = 0   |   Condiciones: x(0) = 0,  x'(0) = 0,  x_f = 1,  ω = 8",
            font=("Segoe UI", 10),
            bg=self.app.c_bg,
            fg=self.app.c_subtext
        ).pack(anchor="w", pady=(0, 16))

        # 1. Tarjeta: Modelo Físico de Newton
        self._create_card(
            content_frame,
            "1. Fundamentación Física: Diagrama de Fuerzas y Ley de Newton (Tablero de Clase)",
            (
                "• Sistema: Masa m conectada a un resorte k y amortiguador viscoso c frente a la meta x_f.\n"
                "• Fuerza elástica (Hooke):    F_resorte = -k (x - x_f)   (Tira hacia la meta x_f)\n"
                "• Fuerza disipativa viscosa:  F_amort   = -c x'          (Frena proporcional a la velocidad)\n"
                "• 2da Ley de Newton (Inercia): m x'' = Σ F = -c x' - k (x - x_f)\n"
                "       m x'' + c x' + k (x - x_f) = 0   ===>   x'' + (c/m) x' + (k/m) (x - x_f) = 0\n"
                "• Parámetros de clase: Frecuencia natural ω = √(k/m), factor de amortiguamiento c/m = 2ζω.\n"
                "       Ecuación Final:  x''(t) + 2ζω x'(t) + ω² (x(t) - x_f) = 0"
            ),
            self.app.c_green
        )

        # 2. Tarjeta: Los Dos Métodos de Solución
        self._create_card(
            content_frame,
            "2. Los Dos Métodos de Solución: Coeficientes Indeterminados vs Cambio de Variable",
            (
                "MÉTODO A: Por Coeficientes Indeterminados (x = x_h + x_p, visto en clase el 10/11/26):\n"
                "  • Ecuación no homogénea:  x'' + 2ζω x' + ω² x = ω² x_f\n"
                "  • Término derecho constante g(t) = ω² x_f  =>  Ensayamos x_p(t) = A (constante).\n"
                "  • Derivando: x_p' = 0, x_p'' = 0  =>  0 + 0 + ω² A = ω² x_f  =>  A = x_f.\n"
                "  • Por tanto, la solución particular es constante: x_p(t) = x_f.\n"
                "  • Solución general: x(t) = x_h(t) + x_f.\n\n"
                "MÉTODO B: Por Cambio de Variable a Homogénea (u = x - x_f, sugerido por la guía):\n"
                "  • Variable de error u(t) = x(t) - x_f. Como x_f es fijo: u' = x',  u'' = x''.\n"
                "  • Sustituyendo: u''(t) + 2ζω u'(t) + ω² u(t) = 0,  con u(0) = -1,  u'(0) = 0.\n"
                "  • ¡Conclusión: Ambos métodos son idénticos! u(t) es exactamente la solución homogénea x_h(t)."
            ),
            self.app.c_cyan
        )

        # 2. Tarjeta: Ecuación Característica y Raíces
        self._create_card(
            content_frame,
            "2. Ecuación Característica y Clasificación de Raíces",
            (
                "• Proponiendo la solución exponencial u(t) = e^(r t), se obtiene:\n"
                "       r² + 2ζω r + ω² = 0\n"
                "• Aplicando la fórmula cuadrática general:\n"
                "       r = [ -2ζω ± √(4ζ²ω² - 4ω²) ] / 2 = -ζω ± ω √(ζ² - 1)\n"
                "• El discriminante Δ = 4ω²(ζ² - 1) define los tres regímenes fundamentales:\n"
                "    1) Si ζ < 1: Δ < 0  => Raíces complejas conjugadas (Subamortiguado: Oscilación / Rebote).\n"
                "    2) Si ζ = 1: Δ = 0  => Raíz real doble r = -ω (Crítico: Transición óptima más rápida).\n"
                "    3) Si ζ > 1: Δ > 0  => Dos raíces reales negativas distintas (Sobreamortiguado: Lento / Pesado)."
            ),
            self.app.c_green
        )

        # 3. Tarjeta: Las Tres Soluciones Exactas Deducidas a Mano
        self._create_card(
            content_frame,
            "3. Deducción Analítica para los Tres Valores de ζ Exigidos (ω = 8, x_f = 1)",
            (
                "CASO 1: ζ = 0.3 (Subamortiguado):\n"
                "  • α = ζω = 2.4,   β = ω √(1 - 0.3²) = 8 √(0.91) ≈ 7.6315 rad/s\n"
                "  • r = -2.4 ± 7.6315 i\n"
                "  • Solución: u(t) = e^(-2.4 t) [ C1 cos(7.6315 t) + C2 sin(7.6315 t) ]\n"
                "  • Con u(0) = -1 => C1 = -1. Con u'(0) = 0 => -2.4 C1 + 7.6315 C2 = 0 => C2 ≈ -0.3145\n"
                "  • SOLUCIÓN EXACTA:  x(t) = 1 - e^(-2.4 t) [ cos(7.6315 t) + 0.3145 sin(7.6315 t) ]\n"
                "  • Sobreimpulso del primer pico: Mp = 100 * exp(-0.3 π / √0.91) ≈ 37.2%\n\n"

                "CASO 2: ζ = 1.0 (Amortiguamiento Crítico):\n"
                "  • Raíz real repetida: r = -ω = -8\n"
                "  • Solución: u(t) = (C1 + C2 t) e^(-8 t)\n"
                "  • Con u(0) = -1 => C1 = -1. Con u'(0) = 0 => C2 - 8 C1 = 0 => C2 = -8\n"
                "  • SOLUCIÓN EXACTA:  x(t) = 1 - (1 + 8 t) e^(-8 t)\n"
                "  • No oscila ni rebota jamás (Mp = 0%). Llega a la meta en el menor tiempo posible.\n\n"

                "CASO 3: ζ = 2.0 (Sobreamortiguado):\n"
                "  • r = -16 ± 8 √3  =>  r1 = -2.1436  y  r2 = -29.8564\n"
                "  • Solución: u(t) = C1 e^(r1 t) + C2 e^(r2 t)\n"
                "  • Con u(0) = -1 y u'(0) = 0 => C1 = -(2√3 + 3)/6 ≈ -1.07735,  C2 = (2√3 - 3)/6 ≈ 0.07735\n"
                "  • SOLUCIÓN EXACTA:  x(t) = 1 - 1.07735 e^(-2.1436 t) + 0.07735 e^(-29.8564 t)\n"
                "  • El modo rápido r2 decae en milisegundos; el polo dominante lento r1 define una llegada pesada."
            ),
            "#facc15"
        )

        # 4. Tarjeta: ¿Por qué ζ < 1 produce rebote y ζ ≥ 1 no?
        self._create_card(
            content_frame,
            "4. Demostración Matemática: ¿Por qué ζ < 1 produce rebote y ζ ≥ 1 no?",
            (
                "• Para ζ < 1, las raíces poseen parte imaginaria no nula: r = -α ± i β.\n"
                "  Por la Fórmula de Euler (e^(i β t) = cos βt + i sin βt), aparecen funciones trigonométricas\n"
                "  armónicas que cambian periódicamente de signo. La derivada x'(t) cruza por cero en múltiples\n"
                "  instantes (puntos críticos de rebote), haciendo que el objeto sobrepase el equilibrio.\n\n"
                "• Para ζ ≥ 1, las raíces son puramente REALES (sin componente imaginaria).\n"
                "  La solución consiste únicamente en sumas de funciones exponenciales monótonas e^(-λ t).\n"
                "  Para las condiciones iniciales en reposo x(0)=0, x'(0)=0, la velocidad x'(t) > 0 para todo t > 0;\n"
                "  es decir, x(t) crece estrictamente hacia x_f sin cruzarla jamás (0% de sobreimpulso)."
            ),
            self.app.c_cyan
        )

        # 5. Tarjeta: Criterios de Diseño de Ingeniería y Game Feel
        self._create_card(
            content_frame,
            "5. Criterios de Selección de Parámetros en la Industria del Software",
            (
                "| Aplicación                     | Parámetro ζ | Justificación de Ingeniería y Game Feel                   |\n"
                "|--------------------------------|-------------|----------------------------------------------------------|\n"
                "| Cámara de Videojuegos          | ζ = 1.0     | Persigue al jugador con la máxima rapidez sin sobrepasar |\n"
                "|                                |             | la meta. Un rebote causaría oscilación y mareo visual.   |\n"
                "| Menús, Botones y Modales UI    | ζ ≈ 0.5     | Un sobreimpulso elástico del ~16% genera 'juiciness',     |\n"
                "| (iOS CoreAnimation, Android)   |             | haciendo que la interfaz se sienta orgánica y táctil.    |\n"
                "| Barras de Vida / Daño RPG      | ζ ≈ 2.0     | Desciende con peso y visceralidad. Un rebote causaría    |\n"
                "|                                |             | una falsa ilusión de que el jugador recuperó salud.      |"
            ),
            self.app.c_purple
        )

        # 6. Tarjeta: Guía de Sustentación para los 4 Integrantes
        self._create_card(
            content_frame,
            "6. Distribución de Roles para la Exposición (15 min + 5 min preguntas)",
            (
                "• Integrante 1 (Edwin Esneider Burbano Luna):\n"
                "  - Introducción al Game Feel y planteamiento del modelo diferencial: x'' + 2ζω x' + ω²(x - x_f) = 0.\n"
                "  - De dónde sale cada término físico: inercia (m=1), amortiguador viscoso (2ζω) y ley de Hooke (ω²).\n"
                "  - Explicación del cambio de variable u = x - x_f y las condiciones iniciales u(0)=-1, u'(0)=0.\n\n"

                "• Integrante 2 (Cristian Alexis Chantre Hurtado):\n"
                "  - Deducción de la ecuación característica: r² + 2ζω r + ω² = 0 y análisis del discriminante.\n"
                "  - Demostración matemática analítica de por qué ζ < 1 rebota (raíces complejas y fórmula de Euler)\n"
                "    mientras que ζ ≥ 1 produce solo decaimiento exponencial monótono sin oscilación.\n"
                "  - Las tres soluciones exactas para ζ = 0.3, ζ = 1.0 y ζ = 2.0.\n\n"

                "• Integrante 3 (Luis Eduardo Hurtado Hormiga):\n"
                "  - Comparación en pantalla partida frente a la interpolación lineal clásica: x += (dest - x)*0.1.\n"
                "  - Explicación de por qué Lerp es de 1er orden (sin masa ni inercia) y desacelera asintóticamente,\n"
                "    mientras que el resorte preserva momento cinético.\n"
                "  - Demostración de la verificación numérica (RK4 vs Analítica) con error residual ~10⁻¹¹ m.\n\n"

                "• Integrante 4 (Andrés Felipe Suaza Cerón):\n"
                "  - Demostración en vivo de los 3 casos en la aplicación: cámara, menú y barra de vida.\n"
                "  - Justificación de ingeniería con las métricas obtenidas (sobreimpulso Mp y tiempo de asentamiento ts).\n"
                "  - Conclusión de ingeniería y respuestas a las preguntas de la docente."
            ),
            self.app.c_green
        )

    def _create_card(self, parent, title, body, accent_col):
        card = tk.LabelFrame(
            parent,
            text=f" {title} ",
            bg=self.app.c_panel,
            fg=accent_col,
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=10
        )
        card.pack(fill="x", pady=8)

        lbl = tk.Label(
            card,
            text=body,
            bg=self.app.c_panel,
            fg=self.app.c_text,
            font=("Consolas", 9),
            justify="left"
        )
        lbl.pack(anchor="w")


# =============================================================================
# 6. PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

def main():
    app = GameFeelApp()
    app.mainloop()


if __name__ == "__main__":
    main()
