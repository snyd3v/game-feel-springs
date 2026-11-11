# Game Feel Springs

## Descripción del Proyecto
Este proyecto implementa y analiza el modelo físico-matemático de un **oscilador armónico amortiguado de segundo orden** aplicado a la animación de interfaces gráficas modernas y motores de videojuegos (*Game Feel*):

$$x''(t) + 2\zeta\omega x'(t) + \omega^2 (x(t) - x_f) = 0$$

A través de una **aplicación interactiva en Python (Tkinter + Matplotlib)**, se demuestra la superioridad del modelo físico de segundo orden frente a la interpolación lineal clásica de primer orden (`x += (destino - x) * 0.1`), se verifica la exactitud del integrador numérico Runge-Kutta de orden 4 (RK4) frente a la solución analítica deducida a mano, y se ilustran en tiempo real las tres aplicaciones prácticas exigidas por la guía:
1. **Cámara Cinematográfica ($\zeta = 1.0$ Crítico):** Seguimiento suave sin oscilaciones ni mareo visual (*motion sickness*).
2. **Menú / Modal Desplegable UI ($\zeta = 0.5$ Subamortiguado):** Rebote elástico del $\sim 16\%$ para lograr una interfaz viva y responsiva (*juiciness*).
3. **Barra de Vida RPG ($\zeta = 2.0$ Sobreamortiguado):** Descenso con peso y contundencia, sin rebote falso que simule curación.

### El modelo en pocas palabras
- **ω** controla la *rapidez* del movimiento.
- **ζ** controla su *carácter*:
  - **ζ < 1** (subamortiguado): rebota.
  - **ζ = 1** (crítico): llega a la meta lo más rápido posible sin rebotar.
  - **ζ > 1** (sobreamortiguado): llega lento y pesado.

### Qué incluye
- Solución analítica a mano para $\zeta = 0.3,\ 1\ \text{y}\ 2$, con $\omega = 8$.
- Simulación numérica (RK4) superpuesta a la solución exacta.
- Animación interactiva con deslizadores para $\omega$ y $\zeta$.
- Comparación contra la interpolación lineal clásica (`x += (destino - x) * 0.1`).
- Tres aplicaciones: cámara, menú y barra de vida.

---

## Requisitos del Sistema
- **Python 3.10 o superior**
- **NumPy**
- **Matplotlib**
- **Tkinter** (incluido por defecto en la instalación estándar de Python en Windows)

Las dependencias están listadas en [requirements.txt](requirements.txt) y se instalan dentro de un entorno virtual (`venv`).

---

## Cómo Ejecutar la Aplicación (con venv)

1. **Abre una terminal** (PowerShell) en la carpeta del proyecto.

2. **Crea el entorno virtual** (solo la primera vez):
   ```powershell
   python -m venv venv
   ```

3. **Actívalo:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   > Si PowerShell bloquea el script, ejecuta una vez:
   > `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
   > En CMD usa `venv\Scripts\activate.bat`. En Linux/macOS: `source venv/bin/activate`.

4. **Instala las dependencias** (solo la primera vez):
   ```powershell
   pip install -r requirements.txt
   ```

5. **Ejecuta la aplicación:**
   ```powershell
   python main.py
   ```

6. **Al terminar**, desactiva el entorno con `deactivate`.

Las siguientes veces solo necesitas los pasos 1, 3 y 5.

**Opcional:** para regenerar el PDF y la presentación, con el entorno activo:
```powershell
python generate_pdf.py
python create_presentation.py
```

---

## Estructura y Navegación de la Aplicación

La aplicación cuenta con una interfaz gráfica oscura, moderna y dividida en 3 pestañas:

### 1. Laboratorio Game Feel (Pantalla Partida & Verificación)
- **Pista Superior (Resorte de 2º Orden):** Muelle helicoidal visible dinámico, masa física, vector velocidad instantánea y marcador de sobreimpulso máximo.
- **Pista Inferior (Interpolación Lineal de 1er Orden):** Ilustra por qué la fórmula clásica `x += (destino - x) * 0.1` carece de inercia, desacelera asintóticamente y nunca rebota.
- **Interactividad en Vivo:** Haz clic en cualquier punto de la pista para enviar ambos objetos a la meta, o usa los botones rápidos ($0.0\text{ m}, 0.5\text{ m}, 1.0\text{ m}, 1.4\text{ m}$).
- **Deslizadores:** Modifica en tiempo real la rapidez $\omega$ y el amortiguamiento $\zeta$, o pulsa los preajustes de la guía ($\zeta = 0.3, 0.5, 1.0, 2.0$).
- **Gráfica 1 (Comparativa en Vivo):** Superpone las trayectorias temporales $x(t)$ del resorte vs Lerp.
- **Gráfica 2 (Verificación de Precisión Numérica):** Superpone la simulación numérica RK4 con la solución analítica exacta deducida a mano, mostrando en pantalla el error residual $\Delta \approx 10^{-11}\text{ m}$.

### 2. Tres Casos Reales en Videojuegos e Interfaces
- **Caso 1 (Cámara):** Escena 2D con un personaje controlable y una cámara elástica. Permite alternar entre $\zeta = 1.0$ (suavidad óptima), $\zeta = 0.25$ (efecto mareo por oscilación) y $\zeta = 2.5$ (rezagada), con su gráfica $x_{\text{jugador}}(t)$ vs $x_{\text{cámara}}(t)$.
- **Caso 2 (Menú UI):** Pantalla de smartphone con tarjeta modal emergente que rebota elásticamente ($\zeta = 0.5$) al abrirse, junto a su gráfica vertical $y(t)$.
- **Caso 3 (Barra de Vida RPG):** HUD de combate con botones de daño (-20 HP, -45 HP) y curación. Incluye una demostración de ingeniería de por qué una barra de vida jamás debe ser subamortiguada (evita falsos rebotes de curación).

### 3. Solución Analítica & Guía de Sustentación
- Procedimiento paso a paso: transformación a homogénea $u = x - x_f$, ecuación característica, raíces y deducción de constantes para $\zeta = 0.3$, $\zeta = 1.0$ y $\zeta = 2.0$.
- Demostración rigurosa de por qué $\zeta < 1$ produce rebote (raíces complejas conjugadas y fórmula de Euler) y $\zeta \ge 1$ no.
- Métricas de ingeniería ($M_p$ sobreimpulso y $t_s$ tiempo de asentamiento).
- Reparto de roles para la exposición de 15 minutos entre los cuatro integrantes.

---

## Declaración sobre el uso de Asistentes de Inteligencia Artificial
En cumplimiento estricto con la directiva docente indicada en la página 11 de la guía de proyectos (*«Sobre el uso de asistentes de inteligencia artificial: Primera: declárenlo en el README... Segunda: respondan por lo que entregan»*):

- **Herramienta utilizada:** Asistente de IA (Gemini / Antigravity de Google DeepMind).
- **Finalidad y alcance:** Se empleó como apoyo para el diseño arquitectónico de la interfaz gráfica interactiva en Tkinter/Matplotlib, optimización del algoritmo RK4 a 60 FPS, redacción estructurada de la deducción matemática en Markdown y organización de las diapositivas de sustentación.
- **Compromiso del grupo:** Todos los integrantes del Grupo 4 revisaron, verificaron numéricamente y comprenden a cabalidad cada línea de código y cada paso de la deducción analítica, estando completamente preparados para defender el trabajo en la sesión de exposición.

---

## Contenido del Repositorio
- `main.py`: Código fuente completo de la aplicación interactiva con interfaz gráfica, simulación RK4 y visualización de Game Feel.
- `Desarrollo_matematico.md`: Documento formal con la deducción analítica paso a paso, ecuaciones características, cálculo de constantes y justificaciones de diseño.
- `Desarrollo_matematico.pdf`: Versión en documento PDF del desarrollo matemático.
- `Presentacion_Proyecto_4.pptx`: Presentación con las diapositivas para la exposición de 15 minutos.
- `generate_pdf.py`: Script que genera `Desarrollo_matematico.pdf` (requiere `reportlab`). Ejecutar con `python generate_pdf.py`.
- `create_presentation.py`: Script que genera `Presentacion_Proyecto_4.pptx` (requiere `python-pptx`). Ejecutar con `python create_presentation.py`.
- `README.md`: Este archivo con las instrucciones de instalación, uso y defensa.
