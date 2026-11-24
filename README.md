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

## Cómo ejecutarlo

### Requisitos

- **Python 3.10 o superior** (comprueba con `python --version`; en Windows también sirve `py --version`).
- Ninguna conexión a internet en tiempo de ejecución: Chart.js ya está incluido en `static/vendor/`. Solo `pip install` necesita red la primera vez.

### 1. Obtener el proyecto

```
git clone https://github.com/snyd3v/game-feel-springs.git
cd game-feel-springs
```

(O descomprime el ZIP y abre la terminal dentro de la carpeta `game-feel-springs`.)

### 2. Crear el entorno virtual e instalar dependencias (solo la primera vez)

Elige el bloque según la terminal que uses.

**PowerShell (Windows)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Si PowerShell dice que *la ejecución de scripts está deshabilitada*, ejecuta una vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a activar el entorno.

**Símbolo del sistema / CMD (Windows)**

```bat
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Git Bash (Windows)**

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Linux / macOS (Bash o Zsh)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Cuando el entorno está activo, el indicador `(venv)` aparece al inicio de la línea de comandos.

> Si `python` no se reconoce en Windows, usa el lanzador `py` (`py -m venv venv`) o reinstala Python marcando *Add python.exe to PATH*.

### 3. Iniciar la aplicación

Con el entorno activo, en cualquier terminal:

```
python app.py
```

Abre **http://localhost:5000** en el navegador. Para detener el servidor: `Ctrl + C`.

### Ejecutar sin activar el entorno

Si prefieres no activar el entorno (o PowerShell lo bloquea), llama directamente al Python del `venv`:

| Terminal | Comando |
|---|---|
| PowerShell | `.\venv\Scripts\python.exe app.py` |
| CMD | `venv\Scripts\python.exe app.py` |
| Git Bash | `./venv/Scripts/python.exe app.py` |
| Linux / macOS | `./venv/bin/python app.py` |

### Pruebas automáticas

Verifican la matemática (solución exacta, RK4, orden de convergencia, tiempo de asentamiento). Con el entorno activo:

```
python -m pytest tests
```

### Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `Address already in use` / el puerto 5000 está ocupado | Cierra el otro proceso que lo usa, o cambia `port=5000` al final de `app.py`. |
| `ModuleNotFoundError: No module named 'flask'` | El entorno no está activo o faltó `pip install -r requirements.txt`. |
| La página abre pero sin gráficas | Recarga con `Ctrl + F5` y confirma que existe `static/vendor/`. |

## Qué hay en la aplicación

| Sección | Qué muestra | Requisito de la guía |
|---|---|---|
| **1 · Laboratorio** | Pantalla partida resorte vs. `x += (destino − x)·0.1`. Clic para mover el destino (los objetos viajan desde donde están), deslizadores de ω y ζ en vivo, gráfica x(t) con la curva exacta superpuesta, régimen, raíces, sobreimpulso y tiempo de asentamiento. | Animación interactiva, deslizadores, comparación con lerp |
| **2 · Verificación** | Para ζ = 0.3, 1 y 2 (ω = 8, x(0) = 0, x′(0) = 0, x_f = 1): RK4 y solución exacta superpuestas, gráfica del error, tabla de errores máximos y estudio de convergencia en h. | Gráfica numérica vs. exacta y comentario de la diferencia |
| **3 · Aplicaciones** | Cámara (ζ = 1), menú (ζ = 0.5) y barra de vida (ζ = 2), cada una con su animación, su x(t) al lado y la justificación calculada. | Tres aplicaciones con ζ distinto |
| **4 · Conclusión** | Tabla de parámetros elegidos con sobreimpulso y tiempo de asentamiento y recomendación. | Conclusión de ingeniería |

### Decisiones de implementación

- **Sistema de primer orden:** `x' = v`, `v' = −2ζω v − ω²(x − x_f)`, integrado con **Runge-Kutta 4**.
- **Paso fijo.** La animación usa `h = 1/240 s` con un acumulador de tiempo, no el `deltaTime` del navegador; así la curva numérica es comparable con la exacta.
- **Verificación en el mismo vector de tiempos.** El servidor (`/api/verify`) evalúa RK4 y la solución exacta en los mismos instantes. Con `h = 0.001 s` el error máximo es ≈ 4·10⁻¹¹ m (ζ = 0.3 y 1) y 1.9·10⁻¹⁰ m (ζ = 2); con `h = 1/240 s`, del orden de 10⁻⁸ m. Es el error global de RK4 (∝ h⁴), medido en la sección 2.
- **Overlay exacto en vivo.** En el laboratorio, cada clic o cambio de ω/ζ re-ancla la solución exacta con la posición y velocidad de ese instante, de modo que la verificación sigue vigente aunque se interactúe.

## Estructura del proyecto

```
physics.py            Núcleo: aceleración, RK4, solución exacta (3 casos), métricas
app.py                Servidor Flask: sirve la página y la API de verificación
static/               Interfaz web (index.html, css/, js/, vendor/)
static/js/physics.js  La misma matemática en el navegador (anima la simulación)
tests/                Pruebas con pytest de physics.py
requirements.txt      Dependencias de Python
```

API: `GET /api/verify?zeta=&omega=&h=&T=` · `GET /api/convergence?zeta=&omega=`

## Declaración sobre el uso de asistentes de inteligencia artificial

- **Gemini / Antigravity (Google DeepMind):** versión inicial en Tkinter/Matplotlib, estructura de la deducción en Markdown y de las diapositivas (esa versión ya no está en el repositorio).
- **Claude Code (Anthropic):** migración a la aplicación web (Flask + JavaScript), reorganización del repositorio, API de verificación, pruebas con pytest.
