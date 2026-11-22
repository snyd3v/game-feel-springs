# Guía para exponer: Proyecto 4, Resortes para animar

Guía interna del grupo. Son **15 minutos + 5 de preguntas**. La idea que debe quedar al final:

> **Las raíces de la ecuación característica deciden cómo se siente una animación.**

## 1. Reparto

El orden es una propuesta. Pueden intercambiar nombres, pero cada bloque va completo con su parte de código.

| Tiempo | Quién | Tema | Secciones | Rúbrica |
|:---:|---|---|:---:|---|
| 0:00 a 3:30 | **1. Edwin** | Modelo, cambio de variable, ecuación característica | 1, 2, 3 | Solución analítica |
| 3:30 a 7:30 | **2. Cristian** | Los tres ejercicios con condiciones iniciales | 4 | Solución analítica |
| 7:30 a 11:30 | **3. Luis** | Demo con el público, por qué rebota, lerp | 5, 6 | Animación |
| 11:30 a 15:00 | **4. Andrés** | Verificación, tres aplicaciones, conclusión | 7, 8 | Modelo, verificación, conclusión |
| 15:00 a 20:00 | **Los cuatro** | Preguntas | Todas | Defensa |

Las secciones son las de [Desarrollo_matematico.md](Desarrollo_matematico.md).

---

## 2. Persona 1: el modelo (3:30)

**Pantalla:** Laboratorio, con ζ = 0.3.

| Tiempo | Qué hace | Idea que dice |
|:---:|---|---|
| 0:30 | Pulsa **Reiniciar** | «Este movimiento no está dibujado a mano: lo produce una ecuación diferencial de segundo orden.» |
| 1:00 | Dibuja masa, resorte y amortiguador | «El resorte tira hacia el destino, el amortiguador frena según la velocidad y Newton los une.» |
| 1:00 | Hace el cambio de variable | «La original no es homogénea por la constante. Si medimos desde el destino, queda homogénea.» |
| 1:00 | Saca la ecuación característica | «El signo del discriminante nos define todo: tres regímenes.» |

**En el tablero:**

```math
\begin{aligned}
mx''&=-k(x-x_f)-cx'\\
x''+2\zeta\omega x'+\omega^2(x-x_f)&=0\\
u=x-x_f\ \Longrightarrow\ u''+2\zeta\omega u'+\omega^2u&=0\\
r^2+2\zeta\omega r+\omega^2&=0\\
r&=-\zeta\omega\pm\omega\sqrt{\zeta^2-1}
\end{aligned}
```

**Al pasar la palabra:** «Con esa ecuación, Cristian resuelve los tres casos de la guía.»

## 3. Persona 2: los tres ejercicios (4:00)

**Antes de empezar:** tener el manuscrito a la mano y la tabla de abajo ya escrita en una esquina, sin la última columna.

| Tiempo | Qué hace | Idea que dice |
|:---:|---|---|
| 0:30 | Señala las raíces | «Cambiando solo ζ caemos en los tres casos de raíces que vimos en clase.» |
| 2:00 | Resuelve **b) completo** (es el más corto) | «Raíz doble, entonces se multiplica por t. Luego aplico las dos condiciones iniciales.» |
| 0:45 | Explica a) sin desarrollarlo | «La parte real es −2.4 y amortigua. La imaginaria es 7.63 y oscila.» |
| 0:45 | Explica c) sin desarrollarlo | «Son dos exponenciales. Las constantes salen de un sistema 2×2.» |

**En el tablero, el ejercicio b):**

```math
\begin{aligned}
u''+16u'+64u&=0\\
e^{rt}(r^2+16r+64)&=0\\
(r+8)^2=0&\ \Longrightarrow\ r=-8\ \text{(multiplicidad 2)}\\
u&=(C_1+C_2t)e^{-8t}\\
u(0)=-1&\ \Longrightarrow\ C_1=-1\\
u'&=C_2e^{-8t}-8(C_1+C_2t)e^{-8t}\\
u'(0)=0&\ \Longrightarrow\ C_2=-8\\
x=u+1&=1-(1+8t)e^{-8t}
\end{aligned}
```

**La tabla:**

| ζ | Raíces | Solución |
|:---:|---|---|
| 0.3 | $-2.4\pm 7.6315i$ | $1-e^{-2.4t}[\cos 7.6315t+0.3145\ \mathrm{sen}\ 7.6315t]$ |
| 1 | $-8$ (doble) | $1-(1+8t)e^{-8t}$ |
| 2 | $-2.1436$ y $-29.8564$ | $1-1.07735e^{-2.1436t}+0.07735e^{-29.8564t}$ |

**Al pasar la palabra:** «Luis muestra cómo se ve cada una de esas fórmulas.»

## 4. Persona 3: demo y rebote (4:00)

La guía pide este orden: **primero el público mueve los deslizadores, luego se explica la fórmula.**

| Tiempo | Qué hace | Idea que dice |
|:---:|---|---|
| 0:30 | Botones **ζ = 0.3**, **ζ = 1**, **ζ = 2** | «Misma ecuación y mismo destino. Solo cambia ζ.» |
| 1:15 | Alguien del público mueve ζ o ω. Después pulsa **Reiniciar** | «Antes de soltarlo: ¿creen que va a rebotar?» |
| 1:15 | Explica en el tablero | «Rebotar es que u cruce por cero.» |
| 1:00 | Señala el carril del lerp y los puntos del rastro | «El lerp sale de golpe y frena. El resorte acelera, trae velocidad y puede pasarse.» |

**En el tablero:**

```math
\begin{aligned}
\zeta<1:&\quad \tan\beta t=-\beta/\alpha &&\Longrightarrow\ \text{infinitos cruces: rebota}\\
\zeta=1:&\quad t=-1/\omega<0 &&\Longrightarrow\ \text{no cruza}\\
\zeta>1:&\quad t=\frac{\ln(r_2/r_1)}{r_2-r_1}<0 &&\Longrightarrow\ \text{no cruza}
\end{aligned}
```

**Qué parte de la fórmula produce lo que se ve:**

| Lo que ve el público | Lo que lo produce |
|---|---|
| El vaivén | El seno y el coseno, que salen de la parte imaginaria |
| Cada rebote es menor | La exponencial $e^{-\zeta\omega t}$ |
| Sube ω y todo es más rápido, con igual porcentaje de rebote | En la solución ω multiplica a t. El porcentaje depende solo de ζ |
| Con ζ grande se siente pesado | La raíz cercana a cero, que decae lento |
| Lo que la gráfica sola no comunica | El rastro y la flecha: se ve la velocidad y el momento en que se devuelve |

**Cuidados con la demo:**

- Después de mover un deslizador, **siempre Reiniciar**. Si el objeto estaba quieto en el destino, sin eso no pasa nada.
- Si hacen clic mientras se mueve, con ζ ≥ 1 **puede pasarse una vez**, aunque la tarjeta diga «ninguno». No es un error: las tarjetas suponen salida desde el reposo y ahí ya traía velocidad.

**Al pasar la palabra:** «Andrés demuestra que la simulación coincide con lo que resolvimos.»

## 5. Persona 4: verificación y conclusión (3:30)

| Tiempo | Qué hace | Idea que dice |
|:---:|---|---|
| 1:00 | Pestaña **Verificación** | «Se superponen. La diferencia máxima es del orden de 10⁻¹⁰ m, porque RK4 avanza por pasos.» |
| 0:30 | **Cámara**: botón **Salto +300 px** | «ζ = 1: se asienta en 0.97 s sin pasarse. No marea.» |
| 0:30 | **Menú**: botón **Abrir menú** | «ζ = 0.5: toca el destino en 0.24 s y rebota 36 px. Se siente responsivo.» |
| 0:30 | **Barra de vida**: botón **Golpe −45** | «ζ = 2: baja con peso en 1.86 s. Si rebotara parecería una curación.» |
| 1:00 | Pestaña **Conclusión** | «Recomendamos 1 para acompañar, 0.5 para responder y 2 para comunicar una pérdida. ζ se elige por carácter y ω por rapidez.» |

**Cierre:** «Primero la matemática, después el programa: el programa verificó lo que resolvimos.»

**Cuidado:** en la barra de vida hagan **un solo golpe, con la barra quieta**. Si la golpean mientras sube por una poción, sigue subiendo un momento por la velocidad que traía.

---

## 6. Quién responde por cada parte del código

La guía dice que una línea que nadie pueda explicar no cuenta.

| Archivo o función | Responde | En una frase |
|---|:---:|---|
| `acceleration` (Python y JS) | 1 | Es la ecuación con la segunda derivada despejada |
| `config.js`, `main.js`, `index.html`, `styles.css` | 1 | Parámetros elegidos, navegación y tabla de conclusión, estructura y estilo |
| `exact_position`, `exactPosition` | 2 | Las tres soluciones de la sección 4, para condiciones iniciales cualesquiera |
| `app.py`, `tests/` | 2 | El servidor que entrega la comparación y las pruebas de la matemática |
| `system_metrics`, `metrics`, `formatRoots` | 3 | Raíces y fórmulas de 5.5 y 5.6 |
| `lab.js`, `charts.js`, `FixedStepper` | 3 | Animación, gráficas y reloj de paso fijo |
| `rk4_step`, `rk4_solve`, `rk4Step` | 4 | Cuatro pendientes y su promedio ponderado |
| `verify.js`, `cases.js` | 4 | Gráficas de error y las tres aplicaciones |

Además, **los cuatro** deben poder explicar sin ayuda esta cadena: ecuación → cambio de variable → raíces → solución → sistema de primer orden → RK4.

---

## 7. Preguntas probables

Responde quien tiene el número. Si no lo sabe, otro complementa. Si nadie lo sabe, se reconoce: la rúbrica lo valora.

### Matemática

**¿Por qué se volvió homogénea? (1)**\
Porque el destino es constante: las derivadas de u y de x son iguales y el término sin la incógnita queda absorbido en u.

**¿Dónde están los coeficientes indeterminados? (1)**\
En la ecuación original. Como g es constante se ensaya A y da el destino. Es equivalente al cambio de variable.

**¿Por qué no hay resonancia? (1)**\
Una constante corresponde a r = 0, y cero no es raíz porque ω² no es cero.

**¿El amortiguador es −cx o −cx′? (1)**\
−cx′, porque frena según la velocidad. Con −cx sería otro resorte y no habría primera derivada.

**¿Por qué aparece te⁻⁸ᵗ? (2)**\
La raíz tiene multiplicidad 2 y hacen falta dos soluciones linealmente independientes.

**¿Por qué seno y coseno si las raíces son complejas? (2)**\
Por la fórmula de Euler: la parte imaginaria se convierte en oscilación y la real queda en la exponencial.

**¿Es lo mismo ω que 7.63? (2)**\
No. ω = 8 es la frecuencia natural, sin amortiguar. 7.63 es la frecuencia con la que oscila ya amortiguado.

**¿Con ζ ≥ 1 nunca se pasa? (3)**\
Saliendo del reposo, nunca. Con velocidad inicial hacia el destino puede pasarse una sola vez, porque la solución tiene a lo sumo un cero.

**¿ζ = 1 es lo más rápido? (3)**\
Es lo más rápido sin oscilar. Si se tolera un rebote pequeño, un ζ algo menor puede asentarse antes.

**¿Por qué 1.65 s si en la gráfica se asienta antes? (3)**\
Es una cota por la envolvente. La curva entra definitivamente a 1.40 s.

**¿De dónde sale el 5.83 del código? (3)**\
De resolver (1 + s)e⁻ˢ = 0.02 por tanteo, con s = ωt.

### Programa

**¿Por qué convertir a un sistema? (4)**\
RK4 trabaja con primeras derivadas, por eso la velocidad se vuelve otra incógnita.

**¿Por qué RK4 y no Euler? (4)**\
El error de Euler es proporcional a h y el de RK4 a h⁴. Con el mismo paso es muchísimo más preciso.

**¿Por qué paso fijo y no deltaTime? (3)**\
deltaTime cambia en cada cuadro y arruina la comparación con la exacta. Usamos 1/240 s.

**Si el lerp depende de los cuadros, ¿por qué en la app no cambia con el monitor? (3)**\
Lo fijamos a 60 pasos por segundo para comparar. Escrito directamente en cada cuadro sí cambiaría.

**¿Por qué la misma matemática en Python y en JS? (2)**\
JS anima en el navegador. Python verifica con numpy, como propone la guía.

**¿Por qué una tolerancia de 0.0001 para ζ = 1? (2)**\
Los decimales del computador no son exactos, y muy cerca de 1 las otras fórmulas dividen por números casi cero.

**¿Por qué la cámara dice 91 px si la fórmula da 93.3? (4)**\
El destino avanza una vez por cuadro, antes de integrar, y eso lo adelanta medio cuadro: unos 2.3 px.

**¿Usaron inteligencia artificial? (cualquiera)**\
Sí, y está declarado en el README con herramienta y uso. Digan exactamente eso y expliquen el paso o la línea que les pregunten.

---

## 8. Preparación

### El manuscrito

- [ ] Se entrega la **Parte A (secciones 1 a 5)**. La Parte B es apoyo para exponer.
- [ ] Cada quien resuelve primero su ejercicio con el documento cerrado y después compara. Es lo mismo que evalúa el parcial.
- [ ] No saltarse el reemplazo, el «e elevado a rt es distinto de cero», el caso de raíces, la derivada antes de evaluar ni el sistema 2×2.
- [ ] Encerrar las tres soluciones finales.
- [ ] Bosquejar las tres curvas con la tabla de 5.7, con ejes t (s) y x (m), leyenda y la línea del destino en 1.
- [ ] Revisarlo entre los cuatro y escanearlo.

### Ensayo

- [ ] Dos ensayos completos con cronómetro. En el segundo, cada quien responde dos preguntas de otro bloque.
- [ ] Nadie lee: cada bloque se dice con palabras propias.
- [ ] Quien no expone saca 0, así que cada uno debe hablar, y además conocer el bloque vecino por si un compañero se traba.

### El día

- [ ] Ejecutar `python app.py` y abrir `http://localhost:5000` **antes** de entrar. No necesita internet.
- [ ] Probar el proyector con el zoom del navegador, el cargador y los marcadores de colores.
- [ ] Llevar un video corto de la demo y el PDF por si el equipo falla.
- [ ] Dejar los deslizadores en sus valores iniciales (recargar la página).

### Si van atrasados

1. La persona 2 solo señala la tabla en a) y c).
2. La persona 4 omite el menú y lo menciona en la tabla de conclusión.
3. **Nunca se recortan:** el cambio de variable, un ejercicio con condiciones iniciales, el porqué del rebote, la superposición y la conclusión.

---

## 9. Números para memorizar

| | ζ = 0.3 | ζ = 1 | ζ = 2 |
|---|:---:|:---:|:---:|
| Raíces, con ω = 8 | −2.4 ± 7.63i | −8 doble | −2.14 y −29.86 |
| Constantes C₁ y C₂ | −1 y −0.3145 | −1 y −8 | −1.077 y 0.077 |
| Rebote | 37.2 % | No | No |
| Asentamiento | 1.65 s | 0.73 s | 1.86 s |

| | Cámara | Menú | Barra de vida |
|---|:---:|:---:|:---:|
| ζ y ω | 1 y 6 | 0.5 y 10 | 2 y 8 |
| Rebote | No | 16.3 % | No |
| Asentamiento | 0.97 s | 0.81 s | 1.86 s |
