# Guía para exponer: Proyecto 4, Resortes para animar

Guía interna del grupo. Son **15 minutos + 5 de preguntas**. La idea que debe quedar al final:

> **Las raíces de la ecuación característica deciden cómo se siente una animación.**

## 1. Reparto

| Tiempo | Quién | Diapositivas | Tema | Secciones | Rúbrica |
|:---:|---|:---:|---|:---:|---|
| 0:00 a 3:30 | **Cristian** | 1 a 5 | Modelo, no homogénea, ecuación característica | 1, 2, 3 | Solución analítica |
| 3:30 a 7:30 | **Edwin** | 6 a 8 | Los tres ejercicios con condiciones iniciales | 4 | Solución analítica |
| 7:30 a 11:30 | **Luis** | 9 a 11 | Demo con el público, por qué rebota, lerp | 5, 6 | Animación |
| 11:30 a 14:15 | **Andrés** | 12 a 14 | Programa, verificación, aplicaciones | 7, 8 | Modelo, verificación |
| 14:15 a 15:00 | **Edwin** | 15 y 16 | Conclusión de ingeniería y cierre | 7 | Conclusión |
| 15:00 a 20:00 | **Los cuatro** | 16 | Preguntas | Todas | Defensa |

Las secciones son las de [Desarrollo_matematico.md](Desarrollo_matematico.md), para estudiar cada bloque.

### Cómo usar el guion

- El texto normal **se dice tal cual**. Lo que está en *[cursiva y corchetes]* es lo que se hace: **no se dice**.
- Las fórmulas están escritas como se pronuncian: «equis prima» es x′, «u dos prima» es u″, «e a la erre te» es eʳᵗ.
- Los decimales se dicen con «punto»: 0.97 es «cero punto noventa y siete».
- El guion es para repasar. **El día de la exposición no se lee**: si se olvida una frase, se sigue con la idea.
- El tiempo de cada diapositiva está junto a su título, para ensayar con cronómetro.

### Manejo de las diapositivas

- Ejecutar `python app.py`, abrir `http://localhost:5000/presentacion` y pulsar `F11`.
- Se avanza con las flechas o con `AvPág`.
- Las diapositivas **9, 13 y 14** traen la app funcionando. Después de hacer clic adentro, se sale con `AvPág` o con los botones del pie: ahí las flechas no cambian de diapositiva.
- Al volver a una demo, empieza otra vez con sus valores iniciales.
- Los números del índice (diapositiva 2) tienen enlace: sirven para saltar a un tema durante las preguntas.

---

## 2. Cristian: el modelo (diapositivas 1 a 5, 3:30)

### Diapositiva 1. Portada (0:00 a 0:15)

Buen día. Somos Cristian Chantre, Edwin Burbano, Luis Hurtado y Andrés Suaza, y nuestro proyecto es Resortes para animar: el game feel, o cómo se siente un movimiento.

### Diapositiva 2. Contenido (0:15 a 0:30)

*[Señala los cuatro bloques, sin leer la lista.]*

Primero veremos el modelo y su solución. Después, cómo se siente ese movimiento. Al final, la verificación del programa y los valores que recomendamos.

### Diapositiva 3. De dónde sale cada término (0:30 a 1:40)

*[Señala la masa en el dibujo.]*

Imaginemos que lo que queremos animar, por ejemplo un menú, es una masa. Equis es su posición y equis efe es el destino.

*[Señala el resorte y luego el amortiguador.]*

El resorte la tira hacia el destino con una fuerza menos ka por equis menos equis efe. El amortiguador la frena según la velocidad, con menos ce por equis prima.

Por la segunda ley de Newton, masa por aceleración es igual a la suma de esas fuerzas.

*[Señala la ecuación del recuadro, término por término.]*

Al dividir entre la masa quedan tres términos: la inercia, el amortiguador y el resorte. Omega es la raíz de ka sobre eme y controla la rapidez. Zeta es ce sobre dos eme omega y controla el carácter del movimiento.

### Diapositiva 4. Ecuación no homogénea (1:40 a 2:40)

Si pasamos la constante al lado derecho, la ecuación es no homogénea. La podemos trabajar por dos caminos.

*[Señala la columna izquierda.]*

El primero es el cambio de variable: u igual a equis menos equis efe. Como el destino es constante, las derivadas de u son las mismas de equis. Al reemplazar, queda homogénea.

*[Señala la columna derecha.]*

El segundo es coeficientes indeterminados. Como el lado derecho es constante, ensayamos una constante A. Cero no es raíz, entonces no hay resonancia. Al reemplazar, la solución particular es el destino.

Los dos caminos llegan a lo mismo: equis es u más el destino.

### Diapositiva 5. Ecuación característica (2:40 a 3:30)

*[Señala la franja de arriba.]*

En la homogénea ensayamos e a la erre te. Como esa exponencial nunca es cero, queda la ecuación característica, y la resolvemos con la fórmula del estudiante.

*[Señala las tres columnas, una por una.]*

Todo depende de zeta al cuadrado menos uno. Si es negativo, las raíces son complejas y el sistema oscila. Si es cero, la raíz es doble: es el caso crítico. Si es positivo, son dos raíces reales y llega más lento.

Con esto, Edwin resuelve los tres casos.

---

## 3. Edwin: los tres ejercicios (diapositivas 6 a 8, 4:00)

**Antes de empezar:** tener el manuscrito a la mano, por si piden un paso intermedio.

### Diapositiva 6. Ejercicio b, completo (3:30 a 5:20)

Gracias, Cristian. Los tres ejercicios tienen omega igual a 8, posición inicial cero, velocidad inicial cero y destino en un metro. Empiezo por el b, con zeta igual a uno, y lo explico completo.

*[Señala la columna izquierda, renglón por renglón.]*

Reemplazamos zeta y omega, y queda u dos prima, más 16 u prima, más 64 u, igual a cero.

Ensayamos e a la erre te y obtenemos erre al cuadrado, más 16 erre, más 64, igual a cero. Esto es erre más 8, al cuadrado. Entonces la raíz es menos 8, con multiplicidad dos.

Como la raíz se repite, la segunda solución se multiplica por te. Por eso la solución general es ce uno más ce dos te, todo por e a la menos 8 te.

*[Señala la columna derecha.]*

Ahora aplico las condiciones iniciales. U en cero es cero menos uno, o sea menos uno. Como e a la cero vale uno, ce uno es menos uno.

Para la segunda condición derivo con la regla del producto, antes de evaluar. La derivada en cero queda ce dos más 8, igual a cero. Entonces ce dos es menos 8.

*[Señala el recuadro final.]*

Por último vuelvo a la variable original, sumando el destino. Por lo tanto, equis de te es uno, menos uno más 8 te, por e a la menos 8 te.

### Diapositiva 7. Ejercicios a y c (5:20 a 6:40)

El a y el c siguen el mismo procedimiento, así que señalo lo que cambia.

*[Señala la columna izquierda.]*

En el a, zeta es 0.3 y las raíces son complejas: menos 2.4, más o menos 7.63 i. La parte real va en la exponencial y amortigua. La imaginaria va en el seno y el coseno, y hace oscilar. Con las condiciones iniciales, ce uno es menos uno y ce dos es menos 0.31.

*[Señala la columna derecha.]*

En el c, zeta es 2 y hay dos raíces reales negativas, entonces la solución es la suma de dos exponenciales.

Las condiciones iniciales forman un sistema de dos ecuaciones con dos incógnitas. Al resolverlo, ce uno es menos 1.077 y ce dos es 0.077.

### Diapositiva 8. Las tres soluciones (6:40 a 7:30)

*[Sigue cada curva con el cursor o con la mano.]*

Aquí están las tres soluciones juntas. La naranja, zeta 0.3, se pasa 37.2 por ciento y se asienta a más tardar en 1.65 segundos. Asentarse es quedar a menos del 2 por ciento del destino.

La verde, zeta uno, no se pasa y se asienta en 0.73 segundos. La morada, zeta 2, tampoco se pasa, pero tarda 1.86.

Solo cambió zeta. Luis nos muestra cómo se siente eso.

---

## 4. Luis: demo y rebote (diapositivas 9 a 11, 4:00)

La guía de la profe pide este orden: **primero el público mueve los deslizadores, luego se explica la fórmula.**

### Diapositiva 9. Demostración con el público (7:30 a 9:15)

Gracias, Edwin. Esta es la aplicación funcionando. Arriba está el resorte y abajo la interpolación lineal, o lerp. Al lado se dibuja la posición contra el tiempo.

*[Pulsa **ζ = 0.3**.]*

Con zeta 0.3 se pasa del destino y vuelve.

*[Pulsa **ζ = 1**.]*

Con zeta uno llega sin pasarse.

*[Pulsa **ζ = 2**.]*

Y con zeta 2 llega más lento, se siente pesado.

Fíjense en algo que la gráfica sola no muestra igual: la flecha es la velocidad y el rastro también la muestra. Puntos separados es que va rápido, puntos juntos es que va frenando.

Ahora necesito a alguien del público. Mueve zeta u omega hasta el valor que quieras.

*[Espera a que lo mueva y mira el valor de ζ.]*

Antes de soltarlo, ¿ustedes creen que va a rebotar?

*[Espera la respuesta y pulsa **Reiniciar**. Luego dice solo la frase que corresponda.]*

- **Si ζ quedó menor que 1:** Como zeta es menor que uno, se pasa del destino. Entre más cerca de uno, menos se nota.
- **Si ζ quedó en 1 o más:** Como zeta no es menor que uno y salió del reposo, llega sin pasarse.

Gracias. Veamos qué parte de la fórmula produce eso.

*[Sale de la demo con `AvPág`.]*

### Diapositiva 10. Por qué rebota (9:15 a 10:35)

Rebotar es pasarse del destino. Como u es la distancia al destino, rebota si u cruza por cero después de arrancar.

*[Señala la primera fila.]*

Con zeta menor que uno hay seno y coseno. Al igualar a cero queda una tangente, que tiene infinitas soluciones: por eso rebota.

*[Señala la segunda y la tercera fila.]*

Con zeta igual o mayor que uno, saliendo del reposo, el único cruce da un tiempo negativo, antes de empezar. Por eso no rebota.

*[Señala los cuatro recuadros de abajo.]*

Entonces, lo que vimos sale de aquí: el vaivén, del seno y el coseno. Que cada rebote sea menor, de la exponencial. La rapidez, de omega, que multiplica al tiempo sin cambiar el porcentaje de rebote. Y lo pesado, de la raíz cercana a cero, que decae lento.

### Diapositiva 11. Resorte frente a lerp (10:35 a 11:30)

*[Señala la columna derecha y luego la izquierda.]*

El lerp es de primer orden. En cada cuadro avanza el 10 por ciento de lo que falta: arranca de golpe, solo frena y nunca rebota. Además depende del monitor: tarda 0.63 segundos a 60 hercios y 0.26 a 144.

El resorte es de segundo orden: guarda posición y velocidad. Por eso acelera, tiene inercia y puede pasarse. Con paso fijo, no depende del monitor.

Andrés nos muestra que el programa coincide con la solución exacta.

**Cuidados con la demo:**

- Después de mover un deslizador, **siempre Reiniciar**. Si el objeto estaba quieto en el destino, sin eso no pasa nada.
- Si hacen clic mientras se mueve, con ζ ≥ 1 **puede pasarse una vez**, aunque la tarjeta diga «ninguno». No es un error: las tarjetas suponen salida desde el reposo y ahí ya traía velocidad.

---

## 5. Andrés: programa y aplicaciones (diapositivas 12 a 14, 2:45)

### Diapositiva 12. La ecuación en el programa (11:30 a 12:20)

Gracias, Luis. Para programar la ecuación la convertimos en un sistema de primer orden: equis prima es la velocidad, y uve prima es la aceleración despejada.

*[Señala la línea de código.]*

Esta línea es esa misma ecuación, y omega y zeta vienen de los deslizadores.

La resolvemos con Runge-Kutta 4 y paso fijo. La exacta es una fórmula. La numérica avanza por pasos y acumula un error proporcional a hache a la cuatro.

### Diapositiva 13. Verificación (12:20 a 13:10)

*[Señala la gráfica izquierda.]*

Aquí está la verificación. La línea de color es la numérica y la negra discontinua es la exacta, calculadas en los mismos tiempos. Como ven, se superponen.

*[Señala la gráfica derecha y la columna de error máximo.]*

Esta es la diferencia. Con un paso de 0.001 segundos, la mayor es 1.9 por diez a la menos diez metros, menos de un nanómetro. No es cero por el error que acumula cada paso.

### Diapositiva 14. Tres aplicaciones (13:10 a 14:15)

La misma ecuación sirve para tres cosas, cada una con su gráfica al lado.

*[Pulsa **Salto +300 px**.]*

La cámara usa zeta uno: alcanza al personaje sin pasarse y se asienta en 0.97 segundos. Así no marea.

*[Pulsa la pestaña **Menú** y luego **Abrir menú**.]*

El menú usa zeta 0.5: toca el destino en 0.24 segundos y se pasa 36 píxeles. Ese rebote pequeño lo hace sentir vivo.

*[Pulsa la pestaña **Barra de vida** y luego **Golpe −45**.]*

La barra de vida usa zeta 2: baja con peso, en 1.86 segundos, y sin rebotar.

*[Sale de la demo con `AvPág`.]*

Edwin cierra con nuestra recomendación.

**Cuidados:**

- En la 13, la gráfica de error según h queda más abajo: se llega con la rueda del mouse, solo si la preguntan.
- En la barra de vida hagan **un solo golpe, con la barra quieta**. Si la golpean mientras sube por una poción, sigue subiendo un momento por la velocidad que traía.

---

## 6. Edwin: conclusión y cierre (diapositivas 15 y 16, 0:45)

Edwin vuelve a pasar adelante después de las aplicaciones.

### Diapositiva 15. Conclusión (14:15 a 15:00)

*[Señala una fila a la vez.]*

Gracias, Andrés. Nuestra recomendación es esta. Zeta uno para la cámara, porque con 0.5 se pasaría 16.3 por ciento y con 2 tardaría 2.48 segundos.

Zeta 0.5 para el menú, porque responde en 0.24 segundos y solo se pasa 36 píxeles.

Y zeta 2 para la vida, porque con 0.35 se pasaría 30.9 por ciento y parecería una curación.

En resumen, zeta da el carácter y omega la rapidez.

### Diapositiva 16. Cierre y preguntas (desde 15:00)

Primero la matemática, después el programa: las raíces de la ecuación característica deciden cómo se siente una animación. Muchas gracias. ¿Tienen preguntas?

---

## 7. Quién responde por cada parte del código

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

## 8. Preguntas probables

Responde la persona indicada y, si le sirve, salta a la diapositiva que aparece al lado. Si no lo sabe, otro complementa. Si nadie lo sabe, se reconoce: la rúbrica lo valora.

### Matemática

**¿Por qué se volvió homogénea? (Cristian, diapositiva 4)**\
Porque el destino es constante: las derivadas de u y de x son iguales y el término sin la incógnita queda absorbido en u.

**¿Dónde están los coeficientes indeterminados? (Cristian, diapositiva 4)**\
En la ecuación original. Como g es constante se ensaya A y da el destino. Es equivalente al cambio de variable.

**¿Por qué no hay resonancia? (Cristian, diapositiva 4)**\
Una constante corresponde a r = 0, y cero no es raíz porque ω² no es cero.

**¿El amortiguador es −cx o −cx′? (Cristian, diapositiva 3)**\
−cx′, porque frena según la velocidad. Con −cx sería otro resorte y no habría primera derivada.

**¿Por qué aparece te⁻⁸ᵗ? (Edwin, diapositiva 6)**\
La raíz tiene multiplicidad 2 y hacen falta dos soluciones linealmente independientes.

**¿Por qué seno y coseno si las raíces son complejas? (Edwin, diapositiva 5)**\
Por la fórmula de Euler: la parte imaginaria se convierte en oscilación y la real queda en la exponencial.

**¿Es lo mismo ω que 7.63? (Edwin, diapositiva 7)**\
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

## 9. Preparación

### El manuscrito

- [ ] Se entrega la **Parte A (secciones 1 a 5)**. La Parte B es apoyo para exponer.
- [ ] Cada quien resuelve primero su ejercicio con el documento cerrado y después compara. Es lo mismo que evalúa el parcial.
- [ ] No saltarse el reemplazo, el «e elevado a rt es distinto de cero», el caso de raíces, la derivada antes de evaluar ni el sistema 2×2.
- [ ] Encerrar las tres soluciones finales.
- [ ] Bosquejar las tres curvas con la tabla de 5.7, con ejes t (s) y x (m), leyenda y la línea del destino en 1.
- [ ] Revisarlo entre los cuatro y escanearlo.

### Ensayo

- [ ] Dos ensayos completos con las diapositivas y cronómetro. En el segundo, cada quien responde dos preguntas de otro bloque.
- [ ] Cada quien repasa su guion en voz alta hasta decirlo sin mirarlo. Al exponer, nadie lee las diapositivas ni esta guía.
- [ ] Quien no expone saca 0, así que cada uno debe hablar, y además conocer el bloque vecino por si un compañero se traba.

### El día

- [ ] Ejecutar `python app.py` y abrir `http://localhost:5000/presentacion` **antes** de entrar. No necesita internet.
- [ ] Probar el proyector con `F11` y mirar las demos desde el fondo del salón. Llevar el cargador.
- [ ] Llevar por si el equipo falla: las diapositivas en PDF (`Ctrl+P`), un video corto de las demos (en ese PDF salen en blanco) y el PDF del desarrollo.
- [ ] Dejar la presentación en la diapositiva 1 (tecla `Inicio`).

### Si van atrasados

1. Edwin cambia el guion de la 7 por: «El a y el c siguen el mismo procedimiento: cambian las raíces y, con las condiciones iniciales, quedan estas constantes».
2. Andrés se salta el párrafo del menú en la 14. Igual queda mencionado en la 15.
3. **Nunca se recortan:** la 4 (no homogénea), la 6 (ejercicio con condiciones iniciales), la 9 (el público participa), la 10 (por qué rebota), la 13 (superposición) y la 15 (conclusión).

---

## 10. Números para memorizar

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
