# Guía para exponer: Proyecto 4, Resortes para animar

Guía interna del grupo. Son **15 minutos + 5 de preguntas**. La idea que debe quedar al final:

> **Las raíces de la ecuación característica deciden cómo se siente una animación.**

## 1. Reparto

| Tiempo | Quién | Diapositivas | Tema | Secciones | Rúbrica |
|:---:|---|:---:|---|:---:|---|
| 0:00 a 3:30 | **Edwin** | 1 a 5 | Modelo, no homogénea, ecuación característica | 1, 2, 3 | Solución analítica |
| 3:30 a 7:30 | **Cristian** | 6 a 8 | Los tres ejercicios con condiciones iniciales | 4 | Solución analítica |
| 7:30 a 11:30 | **Luis** | 9 a 11 | Demo con el público, por qué rebota, lerp | 5, 6 | Animación |
| 11:30 a 15:00 | **Andrés** | 12 a 15 | Programa, verificación, aplicaciones, conclusión | 7, 8 | Modelo, verificación, conclusión |
| 15:00 a 20:00 | **Los cuatro** | 16 | Preguntas | Todas | Defensa |

Las secciones son las de [Desarrollo_matematico.md](Desarrollo_matematico.md), para estudiar cada bloque.

### Manejo de las diapositivas

- Ejecutar `python app.py`, abrir `http://localhost:5000/presentacion` y pulsar `F11`.
- Se avanza con las flechas o con `AvPág`.
- Las diapositivas **9, 13 y 14** traen la app funcionando. Después de hacer clic adentro, se sale con `AvPág` o con los botones del pie: ahí las flechas no cambian de diapositiva.
- Al volver a una demo, empieza otra vez con sus valores iniciales.
- Los números del índice (diapositiva 2) tienen enlace: sirven para saltar a un tema durante las preguntas.

---

## 2. Edwin: el modelo (diapositivas 1 a 5, 3:30)

| N.º | Reloj | Qué hace | Idea que dice |
|:---:|:---:|---|---|
| 1 | 0:00 a 0:15 | Presenta al grupo | «Vamos a mostrar que una animación se puede producir con una ecuación diferencial de segundo orden.» |
| 2 | 0:15 a 0:30 | Nombra las cuatro partes, sin leer la lista | «Primero la matemática, luego cómo se ve y al final qué valores elegimos.» |
| 3 | 0:30 a 1:40 | Señala el dibujo y cada término | «El resorte tira hacia el destino, el amortiguador frena según la velocidad y Newton los une.» |
| 4 | 1:40 a 2:40 | Compara los dos caminos | «No es homogénea por la constante. Con el cambio de variable queda homogénea, y por coeficientes indeterminados la particular da el mismo destino.» |
| 5 | 2:40 a 3:30 | Señala el discriminante y los tres casos | «El signo de ζ² − 1 decide el tipo de raíces, y las raíces deciden el movimiento.» |

**Al pasar la palabra:** «Con esa ecuación, Cristian resuelve los tres casos de la guía.»

## 3. Cristian: los tres ejercicios (diapositivas 6 a 8, 4:00)

**Antes de empezar:** tener el manuscrito a la mano, por si piden un paso intermedio.

| N.º | Reloj | Qué hace | Idea que dice |
|:---:|:---:|---|---|
| 6 | 3:30 a 5:20 | Explica **b) completo**, paso por paso | «Raíz doble, entonces se multiplica por t. Luego aplico las dos condiciones iniciales.» |
| 7 | 5:20 a 6:40 | **No la desarrolla:** señala raíces y constantes | «En a) la parte real amortigua y la imaginaria oscila. En c) son dos exponenciales y las constantes salen de un sistema 2×2.» |
| 8 | 6:40 a 7:30 | Sigue cada curva con el dedo o el cursor | «Misma ecuación y mismas condiciones: solo cambió ζ, y cambió todo el movimiento.» |

**Al pasar la palabra:** «Luis muestra cómo se siente cada una de esas fórmulas.»

## 4. Luis: demo y rebote (diapositivas 9 a 11, 4:00)

La guía de la profe pide este orden: **primero el público mueve los deslizadores, luego se explica la fórmula.**

| N.º | Reloj | Qué hace | Idea que dice |
|:---:|:---:|---|---|
| 9 | 7:30 a 9:15 | Botones **ζ = 0.3**, **ζ = 1** y **ζ = 2**. Luego alguien del público mueve ζ u ω y se pulsa **Reiniciar** | «Antes de soltarlo: ¿creen que va a rebotar? Fíjense en la flecha y el rastro: muestran la velocidad.» |
| 10 | 9:15 a 10:35 | Recorre la tabla fila por fila | «Rebotar es que u cruce por cero. Saliendo del reposo, solo la forma con seno y coseno lo cruza.» |
| 11 | 10:35 a 11:30 | Compara las dos columnas | «El lerp sale de golpe y frena. El resorte acelera, trae velocidad y puede pasarse.» |

**Qué parte de la fórmula produce lo que se vio:**

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

**Al pasar la palabra:** «Andrés demuestra que el programa coincide con lo que resolvimos.»

## 5. Andrés: programa y conclusión (diapositivas 12 a 15, 3:30)

| N.º | Reloj | Qué hace | Idea que dice |
|:---:|:---:|---|---|
| 12 | 11:30 a 12:20 | Señala el sistema y la línea de código | «Es la misma ecuación con la aceleración despejada. RK4 la avanza por pasos, por eso tiene un error muy pequeño.» |
| 13 | 12:20 a 13:10 | Señala la superposición y la columna de error | «Se superponen. La diferencia máxima es del orden de 10⁻¹⁰ m.» |
| 14 | 13:10 a 14:15 | **Cámara**: botón **Salto +300 px** | «ζ = 1: se asienta en 0.97 s sin pasarse. No marea.» |
| | | **Menú**: botón **Abrir menú** | «ζ = 0.5: toca el destino en 0.24 s y se pasa 36 px. Se siente responsivo.» |
| | | **Barra de vida**: botón **Golpe −45** | «ζ = 2: baja con peso en 1.86 s. Si rebotara parecería una curación.» |
| 15 | 14:15 a 15:00 | Señala la franja y una cifra por fila | «Recomendamos 1 para acompañar, 0.5 para responder y 2 para comunicar una pérdida. ζ se elige por carácter y ω por rapidez.» |

**Cierre, al pasar a la 16:** «Primero la matemática, después el programa: las raíces deciden cómo se siente una animación.»

**Cuidados:**

- En la 13, la gráfica de error según h queda más abajo: se llega con la rueda del mouse, solo si la preguntan.
- En la barra de vida hagan **un solo golpe, con la barra quieta**. Si la golpean mientras sube por una poción, sigue subiendo un momento por la velocidad que traía.

---

## 6. Quién responde por cada parte del código

La guía dice que una línea que nadie pueda explicar no cuenta.

| Archivo o función | Responde | En una frase |
|---|:---:|---|
| `config.js`, `main.js`, `index.html`, `styles.css` | Edwin | Parámetros elegidos, navegación y tabla de conclusión, estructura y estilo |
| `presentacion.html`, `presentacion.css`, `presentacion.js` | Edwin | Las diapositivas: cambian de página, muestran la app y grafican con la solución exacta de `physics.js` |
| `exact_position`, `exactPosition`, `is_critical`, `isCritical` | Cristian | Las tres soluciones de la sección 4, para condiciones iniciales cualesquiera, y la tolerancia con que se reconoce ζ = 1 |
| `app.py`, `tests/` | Cristian | El servidor que entrega la app, las diapositivas y la comparación, y las pruebas de la matemática |
| `system_metrics`, `metrics`, `formatRoots` | Luis | Raíces y fórmulas de 5.5 y 5.6 |
| `lab.js`, `charts.js`, `FixedStepper` | Luis | Animación, gráficas y reloj de paso fijo |
| `acceleration` (Python y JS) | Andrés | Es la ecuación con la segunda derivada despejada, la línea de la diapositiva 12 |
| `rk4_step`, `rk4_solve`, `rk4Step` | Andrés | Cuatro pendientes y su promedio ponderado |
| `verify.js`, `cases.js` | Andrés | Gráficas de error y las tres aplicaciones |

Además, **los cuatro** deben poder explicar sin ayuda esta cadena: ecuación → cambio de variable → raíces → solución → sistema de primer orden → RK4.

---

## 7. Preguntas probables

Responde la persona indicada y, si le sirve, salta a la diapositiva que aparece al lado. Si no lo sabe, otro complementa. Si nadie lo sabe, se reconoce: la rúbrica lo valora.

### Matemática

**¿Por qué se volvió homogénea? (Edwin, diapositiva 4)**\
Porque el destino es constante: las derivadas de u y de x son iguales y el término sin la incógnita queda absorbido en u.

**¿Dónde están los coeficientes indeterminados? (Edwin, diapositiva 4)**\
En la ecuación original. Como g es constante se ensaya A y da el destino. Es equivalente al cambio de variable.

**¿Por qué no hay resonancia? (Edwin, diapositiva 4)**\
Una constante corresponde a r = 0, y cero no es raíz porque ω² no es cero.

**¿El amortiguador es −cx o −cx′? (Edwin, diapositiva 3)**\
−cx′, porque frena según la velocidad. Con −cx sería otro resorte y no habría primera derivada.

**¿Por qué aparece te⁻⁸ᵗ? (Cristian, diapositiva 6)**\
La raíz tiene multiplicidad 2 y hacen falta dos soluciones linealmente independientes.

**¿Por qué seno y coseno si las raíces son complejas? (Cristian, diapositiva 5)**\
Por la fórmula de Euler: la parte imaginaria se convierte en oscilación y la real queda en la exponencial.

**¿Es lo mismo ω que 7.63? (Cristian, diapositiva 7)**\
No. ω = 8 es la frecuencia natural, sin amortiguar. 7.63 es la frecuencia con la que oscila ya amortiguado.

**¿Con ζ ≥ 1 nunca se pasa? (Luis, diapositiva 10)**\
Saliendo del reposo, nunca. Con velocidad inicial hacia el destino puede pasarse una sola vez, porque la solución tiene a lo sumo un cero.

**¿ζ = 1 es lo más rápido? (Luis, diapositiva 8)**\
Es lo más rápido sin oscilar. Si se tolera un rebote pequeño, un ζ algo menor puede asentarse antes.

**¿Por qué 1.65 s si en la gráfica se asienta antes? (Luis, diapositiva 8)**\
Es una cota por la envolvente. La curva entra definitivamente a 1.40 s.

**¿De dónde sale el 5.83 del código? (Luis)**\
De resolver (1 + s)e⁻ˢ = 0.02 por tanteo, con s = ωt.

### Programa

**¿Por qué convertir a un sistema? (Andrés, diapositiva 12)**\
RK4 trabaja con primeras derivadas, por eso la velocidad se vuelve otra incógnita.

**¿Por qué RK4 y no Euler? (Andrés, diapositiva 12)**\
El error de Euler es proporcional a h y el de RK4 a h⁴. Con el mismo paso es muchísimo más preciso.

**¿Por qué paso fijo y no deltaTime? (Luis, diapositiva 12)**\
deltaTime cambia en cada cuadro y arruina la comparación con la exacta. Usamos 1/240 s.

**Si el lerp depende de los cuadros, ¿por qué en la app no cambia con el monitor? (Luis, diapositiva 11)**\
Lo fijamos a 60 pasos por segundo para comparar. Escrito directamente en cada cuadro sí cambiaría.

**¿Por qué la misma matemática en Python y en JS? (Cristian)**\
JS anima en el navegador. Python verifica con numpy, como propone la guía.

**¿Por qué una tolerancia de 0.0001 para ζ = 1? (Cristian)**\
Los decimales del computador no son exactos, y muy cerca de 1 las otras fórmulas dividen por números casi cero.

**¿Por qué la cámara dice 91 px si la fórmula da 93.3? (Andrés, diapositiva 14)**\
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

- [ ] Dos ensayos completos con las diapositivas y cronómetro. En el segundo, cada quien responde dos preguntas de otro bloque.
- [ ] Nadie lee las diapositivas ni esta guía: cada bloque se dice con palabras propias. Las frases entre comillas son solo la idea.
- [ ] Quien no expone saca 0, así que cada uno debe hablar, y además conocer el bloque vecino por si un compañero se traba.

### El día

- [ ] Ejecutar `python app.py` y abrir `http://localhost:5000/presentacion` **antes** de entrar. No necesita internet.
- [ ] Probar el proyector con `F11` y mirar las demos desde el fondo del salón. Llevar el cargador.
- [ ] Llevar por si el equipo falla: las diapositivas en PDF (`Ctrl+P`), un video corto de las demos (en ese PDF salen en blanco) y el PDF del desarrollo.
- [ ] Dejar la presentación en la diapositiva 1 (tecla `Inicio`).

### Si van atrasados

1. Cristian pasa la 7 señalando solo las constantes.
2. Andrés omite el menú en la 14 y lo menciona en la 15.
3. **Nunca se recortan:** la 4 (no homogénea), la 6 (ejercicio con condiciones iniciales), la 9 (el público participa), la 10 (por qué rebota), la 13 (superposición) y la 15 (conclusión).

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
