# Resortes para animar: el «game feel»

Proyecto 4 · Ecuaciones Diferenciales, Unidad 3 · Institución Universitaria Colegio Mayor del Cauca

**Grupo 4:** Edwin Esneider Burbano Luna · Cristian Alexis Chantre Hurtado · Luis Eduardo Hurtado Hormiga · Andrés Felipe Suaza Cerón

## El modelo

Si `x(t)` es la posición del elemento animado y `x_f` su destino:

```
x'' + 2ζω x' + ω² (x − x_f) = 0
```

- `x''` inercia · `2ζω x'` amortiguador viscoso · `ω² (x − x_f)` resorte (ley de Hooke) hacia el destino.
- `ω` controla la **rapidez**, `ζ` el **carácter**: ζ < 1 rebota, ζ = 1 llega lo más rápido sin rebotar, ζ > 1 llega lento y pesado.
- Con `u = x − x_f` la ecuación queda homogénea: `u'' + 2ζω u' + ω² u = 0`.

La deducción (ecuación característica, solución general, condiciones iniciales, ζ = 0.3, 1 y 2 con ω = 8) está en
[docs/Desarrollo_matematico.pdf](docs/Desarrollo_matematico.pdf) / [.md](docs/Desarrollo_matematico.md).
**El programa verifica esa solución, no la reemplaza.**

## Cómo ejecutarlo

Requiere Python 3.10 o superior.

```powershell
python -m venv venv                 # solo la primera vez
.\venv\Scripts\Activate.ps1         # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt     # solo la primera vez
python app.py
```

Abre **http://localhost:5000**. Para detener el servidor: `Ctrl + C`. No necesita internet (Chart.js está incluido en `static/vendor/`).

Diapositivas de la sustentación: **http://localhost:5000/presentacion**. Se avanza con las flechas o AvPág; dentro de una demostración, con AvPág o los botones del pie. `F11` es pantalla completa.

Pruebas automáticas de la matemática (solución exacta, RK4, orden de convergencia, tiempo de asentamiento):

```powershell
python -m pytest tests
```

## Qué hay en la aplicación

| Sección | Qué muestra | Requisito de la guía |
|---|---|---|
| **1 · Laboratorio** | Pantalla partida resorte vs. `x += (destino − x)·0.1`. Clic para mover el destino (los objetos viajan desde donde están), deslizadores de ω y ζ en vivo, gráfica x(t) con la curva exacta superpuesta, régimen, raíces, sobreimpulso y tiempo de asentamiento. | Animación interactiva, deslizadores, comparación con lerp |
| **2 · Verificación** | Para ζ = 0.3, 1 y 2 (ω = 8, x(0) = 0, x′(0) = 0, x_f = 1): RK4 y solución exacta superpuestas, gráfica del error, tabla de errores máximos y estudio de convergencia en h. | Gráfica numérica vs. exacta y comentario de la diferencia |
| **3 · Aplicaciones** | Cámara (ζ = 1), menú (ζ = 0.5) y barra de vida (ζ = 2), cada una con su animación, su x(t) al lado y la justificación calculada. | Tres aplicaciones con ζ distinto |
| **4 · Conclusión** | Tabla de parámetros elegidos con sobreimpulso y tiempo de asentamiento, recomendación y enlace a la deducción a mano. | Conclusión de ingeniería |

### Decisiones de implementación

- **Sistema de primer orden:** `x' = v`, `v' = −2ζω v − ω²(x − x_f)`, integrado con **Runge-Kutta 4**.
- **Paso fijo.** La animación usa `h = 1/240 s` con un acumulador de tiempo, no el `deltaTime` del navegador; así la curva numérica es comparable con la exacta.
- **Verificación en el mismo vector de tiempos.** El servidor (`/api/verify`) evalúa RK4 y la solución exacta en los mismos instantes. Con `h = 0.001 s` el error máximo es ≈ 4·10⁻¹¹ m (ζ = 0.3 y 1) y 1.9·10⁻¹⁰ m (ζ = 2); con `h = 1/240 s`, del orden de 10⁻⁸ m. Es el error global de RK4 (∝ h⁴), medido en la sección 2.
- **Overlay exacto en vivo.** En el laboratorio, cada clic o cambio de ω/ζ re-ancla la solución exacta con la posición y velocidad de ese instante, de modo que la verificación sigue vigente aunque se interactúe.

## Estructura del repositorio y qué defender

```
physics.py          NÚCLEO: aceleración, RK4, solución exacta (3 casos), métricas
static/js/physics.js NÚCLEO: la misma matemática en el navegador (anima la simulación)
app.py              servidor Flask: sirve la página y /api/verify, /api/convergence (RK4 vs exacta con numpy)
tests/              pytest de physics.py
static/             interfaz: index.html, css/ y js/{lab,verify,cases,charts,main}.js (solo dibujo y controles)
static/presentacion.html  diapositivas de /presentacion (con css/ y js/presentacion.*)
docs/               deducción (Markdown y su PDF exportado) y Guia_exposicion.md (organización interna)
```

- **Matemática y lógica (lo que se explica línea por línea):** `physics.py` y `static/js/physics.js`. Cada bloque indica en su cabecera la sección de `docs/Desarrollo_matematico.md` donde está deducido. Python verifica con numpy (como el esqueleto de la guía); JavaScript anima.
- **Interfaz:** `lab.js`, `cases.js`, `verify.js`, `charts.js` y el CSS solo dibujan, leen los deslizadores y llaman a `physics.js`; no contienen matemática propia.

API: `GET /api/verify?zeta=&omega=&h=&T=` · `GET /api/convergence?zeta=&omega=`.

## Declaración sobre el uso de asistentes de inteligencia artificial

- **Gemini / Antigravity (Google DeepMind):** versión inicial en Tkinter/Matplotlib, estructura de la deducción en Markdown y de las diapositivas (esa versión ya no está en el repositorio).
- **Claude Code (Anthropic):** migración a la aplicación web (Flask + JavaScript), reorganización del repositorio, API de verificación, pruebas con pytest, revisión de la matemática contra los apuntes de clase (correcciones del tiempo de asentamiento, notación y citas), redacción del paso a paso de `docs/Desarrollo_matematico.md` siguiendo el procedimiento visto en clase, guía interna de exposición, diapositivas de `/presentacion` y esta documentación.

El desarrollo de `docs/` es la versión mecanografiada, hecha con la asistencia declarada arriba; el manuscrito del grupo se entrega aparte. El grupo revisó y puede explicar el código y cada paso de la deducción.
