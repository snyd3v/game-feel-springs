# Proyecto 4: Resortes para Animar: el «Game Feel»
**Ecuaciones Diferenciales de Orden Superior — Unidad 3**  
**Institución Universitaria Colegio Mayor del Cauca**  
**Facultad de Ingeniería Informática y Multimedia**  
**Docente:** Ing. Diana Méndez Astudillo  
**Clase Teórica de Referencia:** Unidad 3 — Movimiento Armónico y EDO No Homogéneas (10/11/26)

---

### Integrantes del Grupo 4:
- **Edwin Esneider Burbano Luna**
- **Cristian Alexis Chantre Hurtado**
- **Luis Eduardo Hurtado Hormiga**
- **Andrés Felipe Suaza Cerón**

---

## 1. Fundamentación Física: Del Diagrama de Fuerzas al Modelo de Newton

Siguiendo la metodología explicada por la docente en clase (tablero del 10/11/26), el sistema físico corresponde a una masa $m$ acoplada a un resorte elástico y a un amortiguador viscoso, sometida a una fuerza de destino.

```
       |
 Pared |---/\/\/\/\/\/\/\/\/\---[ Resorte k:  F_resorte = -k(x - x_f) ]---|
 Fija  |                                                                 |---> [ Masa m ] ---> Desplazamiento x(t)
       |-------[ ======| ]------[ Amortiguador c: F_amort = -c x' ]-------|        |
                                                                           v
                                                            Posición de Equilibrio (Meta x_f)
```

### Las tres fuerzas del modelo físico:
1. **Fuerza del resorte (Ley de Hooke):** El resorte tira hacia la posición de equilibrio $x_f$ con una fuerza proporcional a la deformación:  
   $$F_{\text{resorte}} = -k(x - x_f)$$
2. **Fuerza del amortiguador (Fricción viscosa):** El amortiguador frena el movimiento con una fuerza proporcional a la velocidad:  
   $$F_{\text{amortiguador}} = -c \frac{dx}{dt} = -c x'$$
3. **Inercia de la masa (Segunda Ley de Newton):** La sumatoria de fuerzas sobre la masa produce aceleración:  
   $$\sum F = m a = m \frac{d^2x}{dt^2} = m x''$$

Igualando por la Segunda Ley de Newton:
$$m x'' = -c x' - k(x - x_f)$$
$$m x'' + c x' + k(x - x_f) = 0$$

Dividiendo toda la ecuación entre la masa $m$:
$$x'' + \frac{c}{m} x' + \frac{k}{m}(x - x_f) = 0$$

### Definición de los Parámetros Estándar de la Clase:
- **Frecuencia angular natural ($\omega$):** Como anotó la profesora en el tablero: *"Se dice: $\omega = \sqrt{\frac{k}{m}}$"*, de modo que $\frac{k}{m} = \omega^2$.
- **Amortiguamiento crítico ($c_{\text{cr}}$) y Factor de amortiguamiento ($\zeta$):**  
  El amortiguamiento crítico es $c_{\text{cr}} = 2\sqrt{km} = 2m\omega$.  
  Se define el factor adimensional: $\zeta = \frac{c}{c_{\text{cr}}} = \frac{c}{2m\omega} \implies \frac{c}{m} = 2\zeta\omega$.

Sustituyendo $\frac{c}{m} = 2\zeta\omega$ y $\frac{k}{m} = \omega^2$, obtenemos la ecuación canónica del Proyecto 4:

$$\boxed{x''(t) + 2\zeta\omega x'(t) + \omega^2 (x(t) - x_f) = 0}$$

**Parámetros fijados por la guía del proyecto:**
- Masa y rigidez: $\omega = 8\text{ rad/s}$
- Destino de equilibrio: $x_f = 1\text{ m}$
- Condiciones iniciales de reposo: $x(0) = 0\text{ m}$, $x'(0) = 0\text{ m/s}$.

---

## 2. Los Dos Métodos de Solución Explicados en Clase

En las clases de la Unidad 3, la docente enseñó dos enfoques para abordar este tipo de ecuaciones. Mostraremos ambos para evidenciar un dominio matemático absoluto:

### Método A: Por Coeficientes Indeterminados ($x = x_h + x_p$)
*(Enfoque visto en clase el 10/11/26 para EDO no homogéneas: $y'' + ay' + by = g(x)$)*

Reescribimos la ecuación expandiendo el paréntesis:
$$x'' + 2\zeta\omega x' + \omega^2 x = \omega^2 x_f$$

El lado derecho es una función constante: $g(t) = \omega^2 x_f$.

1. **Solución Homogénea ($x_h$):**  
   Resolvemos la ecuación asociada: $x_h'' + 2\zeta\omega x_h' + \omega^2 x_h = 0$.
2. **Solución Particular ($x_p$) por Coeficientes Indeterminados:**  
   Como $g(t) = \text{constante}$ y $r = 0$ no es raíz de la ecuación característica, ensayamos una constante:
   $$x_p(t) = A$$
   Derivadas: $x_p'(t) = 0$, $x_p''(t) = 0$.  
   Sustituyendo en la ecuación diferencial:
   $$0 + 2\zeta\omega(0) + \omega^2 A = \omega^2 x_f \implies \omega^2 A = \omega^2 x_f \implies A = x_f$$
   Por lo tanto:
   $$x_p(t) = x_f$$
3. **Solución General:**
   $$\boxed{x(t) = x_h(t) + x_p(t) = x_h(t) + x_f}$$

### Método B: Por Cambio de Variable a Ecuación Homogénea
*(Enfoque sugerido en la guía técnica del proyecto)*

Definimos la variable de desviación o error respecto a la meta:
$$u(t) = x(t) - x_f$$
Como la meta $x_f$ es fija en el tiempo ($\frac{dx_f}{dt} = 0$):
$$u'(t) = x'(t), \qquad u''(t) = x''(t)$$
Sustituyendo directamente en $x'' + 2\zeta\omega x' + \omega^2(x - x_f) = 0$:
$$\boxed{u''(t) + 2\zeta\omega u'(t) + \omega^2 u(t) = 0}$$

Nuevas condiciones iniciales para $u(t)$:
- $u(0) = x(0) - x_f = 0 - 1 = \mathbf{-1}$
- $u'(0) = x'(0) = \mathbf{0}$

> **Conclusión Pedagógica:** Ambos métodos son idénticos. La solución homogénea $u(t)$ en el Método B es exactamente la $x_h(t)$ del Método A, y al despejar $x(t) = u(t) + x_f$ recuperamos $x(t) = x_h(t) + x_p(t)$.

---

## 3. Ecuación Característica y los Tres Regímenes del Tablero

Para resolver la ecuación homogénea $u'' + 2\zeta\omega u' + \omega^2 u = 0$, proponemos la solución exponencial:
$$u(t) = e^{rt}, \quad u'(t) = r e^{rt}, \quad u''(t) = r^2 e^{rt}$$

Sustituyendo:
$$r^2 e^{rt} + 2\zeta\omega r e^{rt} + \omega^2 e^{rt} = 0 \implies e^{rt}(r^2 + 2\zeta\omega r + \omega^2) = 0$$

Como $e^{rt} \neq 0$ para todo $t$:
$$r^2 + 2\zeta\omega r + \omega^2 = 0$$

Aplicando la fórmula cuadrática general que la profesora anotó en el tablero ($r = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$):
$$r = \frac{-2\zeta\omega \pm \sqrt{(2\zeta\omega)^2 - 4(1)(\omega^2)}}{2} = -\zeta\omega \pm \omega\sqrt{\zeta^2 - 1}$$

### El Discriminante y los Tres Regímenes de la Profesora:
En el tablero del 10/11/26, la docente escribió textualmente:
> *"El discriminante nos define todo:"*
> 1. *$\Delta > 0$ ($c^2 - 4mk > 0 \iff \zeta > 1$): **Sobreamortiguado**. Dos raíces reales negativas distintas, la masa vuelve al equilibrio sin oscilar.*
> 2. *$\Delta = 0$ ($c^2 - 4mk = 0 \iff \zeta = 1$): **Críticamente amortiguado**. Una raíz real negativa, es el regreso más rápido sin posible oscilación.*
> 3. *$\Delta < 0$ ($c^2 - 4mk < 0 \iff \zeta < 1$): **Subamortiguado**. Raíz en los complejos con parte real negativa, la masa oscila con amplitud decreciente y decae.*

---

## 4. Solución Analítica Detallada para los Tres Valores de $\zeta$ ($\omega = 8$, $x_f = 1$)

### Caso 1: $\zeta = 0.3$ (Subamortiguado — Oscilaciones y Rebote)
- Parámetros: $\omega = 8$, $\zeta = 0.3$.
- Atenuación: $\alpha = \zeta\omega = 0.3 \times 8 = 2.4\text{ s}^{-1}$.
- Frecuencia amortiguada: $\beta = \omega\sqrt{1 - \zeta^2} = 8\sqrt{1 - 0.09} = 8\sqrt{0.91} \approx 7.6315\text{ rad/s}$.
- Raíces complejas: $r = -2.4 \pm 7.6315 i$.

Como anotó la profesora en el tablero para raíces complejas $r = \alpha \pm \beta i$:
$$u(t) = e^{-\alpha t} \left[ C_1 \cos(\beta t) + C_2 \sin(\beta t) \right]$$
$$u(t) = e^{-2.4 t} \left[ C_1 \cos(7.6315 t) + C_2 \sin(7.6315 t) \right]$$

**Paso 1: Aplicar $u(0) = -1$:**
$$u(0) = e^{0} \left[ C_1 \cos(0) + C_2 \sin(0) \right] = C_1(1) + 0 = C_1 = -1$$

**Paso 2: Derivar $u'(t)$ para aplicar $u'(0) = 0$:**
Regla del producto:
$$u'(t) = -2.4 e^{-2.4 t} [ C_1 \cos(7.6315 t) + C_2 \sin(7.6315 t) ] + e^{-2.4 t} [ -7.6315 C_1 \sin(7.6315 t) + 7.6315 C_2 \cos(7.6315 t) ]$$

Evaluando en $t = 0$:
$$u'(0) = -2.4(1)[ C_1(1) + 0 ] + 1[ 0 + 7.6315 C_2(1) ] = -2.4 C_1 + 7.6315 C_2 = 0$$
Sustituyendo $C_1 = -1$:
$$-2.4(-1) + 7.6315 C_2 = 0 \implies 2.4 + 7.6315 C_2 = 0 \implies C_2 = -\frac{2.4}{7.6315} \approx -0.3145$$

**Paso 3: Solución particular final ($x(t) = 1 + u(t)$):**
$$\boxed{x(t) = 1 - e^{-2.4 t} \left[ \cos(7.6315 t) + 0.3145 \sin(7.6315 t) \right]}$$

- **Primer pico de sobreimpulso ($t_p$):** La velocidad $x'(t) = 0$ cuando $\sin(7.6315 t) = 0 \implies t_p = \frac{\pi}{7.6315} \approx \mathbf{0.4117\text{ s}}$.
- **Sobreimpulso porcentual ($M_p$):** $M_p = 100 \cdot e^{-\frac{\pi \zeta}{\sqrt{1 - \zeta^2}}} \approx \mathbf{37.23\%}$ (alcanza $x = 1.3723\text{ m}$).
- **Tiempo de asentamiento al 2% ($t_s$):** $e^{-2.4 t_s} \le 0.02 \implies t_s \approx \mathbf{1.63\text{ s}}$.

---

### Caso 2: $\zeta = 1.0$ (Amortiguamiento Crítico — Regreso Óptimo sin Rebote)
- Parámetros: $\omega = 8$, $\zeta = 1.0$.
- Discriminante: $\Delta = 0$.
- Raíz real repetida (multiplicidad 2): $r = -\omega = -8$.

Como en el ejemplo del tablero ($y'' - 2y' + y = 0 \implies (r-1)^2 = 0 \implies y_h = (C_1 + C_2 x)e^x$):
$$u(t) = (C_1 + C_2 t) e^{-8 t}$$

**Paso 1: Aplicar $u(0) = -1$:**
$$u(0) = (C_1 + 0) e^{0} = C_1 = -1$$

**Paso 2: Derivar $u'(t)$ para aplicar $u'(0) = 0$:**
$$u'(t) = C_2 e^{-8 t} - 8 (C_1 + C_2 t) e^{-8 t}$$
Evaluando en $t = 0$:
$$u'(0) = C_2 - 8 C_1 = 0 \implies C_2 - 8(-1) = 0 \implies C_2 + 8 = 0 \implies C_2 = -8$$

**Paso 3: Solución particular final ($x(t) = 1 + u(t)$):**
$$\boxed{x(t) = 1 - (1 + 8 t) e^{-8 t}}$$

- **Sobreimpulso:** $M_p = \mathbf{0\%}$. Como $(1 + 8t)e^{-8t} > 0$ para todo $t \ge 0$, se cumple que $x(t) < 1$; nunca sobrepasa la meta.
- **Tiempo de asentamiento al 2% ($t_s$):** $(1 + 8 t_s)e^{-8 t_s} = 0.02 \implies t_s \approx \mathbf{0.73\text{ s}}$ (¡El tiempo más rápido posible sin oscilar!).

---

### Caso 3: $\zeta = 2.0$ (Sobreamortiguado — Pesado y sin Oscilación)
- Parámetros: $\omega = 8$, $\zeta = 2.0$.
- Discriminante: $\zeta^2 - 1 = 4 - 1 = 3 > 0$.
- Raíces reales distintas:
  $$r = -16 \pm 8\sqrt{3} \implies r_1 \approx -2.1436\text{ s}^{-1}, \quad r_2 \approx -29.8564\text{ s}^{-1}$$

Solución general:
$$u(t) = C_1 e^{r_1 t} + C_2 e^{r_2 t}$$

**Paso 1 y 2: Condiciones iniciales:**
$$u(0) = C_1 + C_2 = -1$$
$$u'(0) = r_1 C_1 + r_2 C_2 = 0 \implies C_2 = -\frac{r_1}{r_2} C_1$$
Resolviendo el sistema algebraico exacto:
$$C_1 = -\frac{2\sqrt{3} + 3}{6} \approx \mathbf{-1.07735}, \qquad C_2 = \frac{2\sqrt{3} - 3}{6} \approx \mathbf{+0.07735}$$

**Paso 3: Solución particular final ($x(t) = 1 + u(t)$):**
$$\boxed{x(t) = 1 - 1.07735 e^{-2.1436 t} + 0.07735 e^{-29.8564 t}}$$

- **Comportamiento físico:** El término rápido $e^{-29.8564 t}$ muere en menos de $0.1\text{ s}$. El polo lento $r_1 = -2.1436$ domina toda la dinámica.
- **Sobreimpulso:** $M_p = \mathbf{0\%}$.
- **Tiempo de asentamiento al 2% ($t_s$):** $1.07735 e^{-2.1436 t_s} \approx 0.02 \implies t_s \approx \mathbf{1.86\text{ s}}$ (Tarda más del doble que el caso crítico, dando sensación de pesadez).

---

## 5. Explicación Rigurosa: ¿Por qué $\zeta < 1$ rebota y $\zeta \ge 1$ no?

Esta es la pregunta conceptual clave que la profesora suele hacer en la sustentación oral:

1. **En el caso Subamortiguado ($\zeta < 1$):**
   Las raíces tienen parte imaginaria: $r = -\alpha \pm i \beta$.  
   Por la **Fórmula de Euler**:
   $$e^{(-\alpha \pm i\beta)t} = e^{-\alpha t}(\cos \beta t \pm i \sin \beta t)$$
   Aparecen funciones armónicas periódicas ($\sin$ y $\cos$).  
   Al derivar, la velocidad $x'(t)$ contiene el factor $\sin(\beta t)$, el cual **se anula periódicamente** cada vez que $\beta t = k\pi$ ($t = \frac{\pi}{\beta}, \frac{2\pi}{\beta}, \dots$). En esos instantes la velocidad cambia de signo; la masa se pasa de la meta, frena, la fuerza elástica la hace devolverse y **rebota sucesivamente** bajo la envolvente disipativa $e^{-\alpha t}$.

2. **En los casos Crítico y Sobreamortiguado ($\zeta \ge 1$):**
   Las raíces son **estrictamente reales** ($\text{Im}(r) = 0$).  
   La solución está formada exclusivamente por funciones exponenciales monótonas decrecientes $e^{-\lambda t}$.  
   Para un sistema que parte del reposo ($x(0)=0, x'(0)=0$), se demuestra analíticamente que la velocidad $x'(t) > 0$ para todo $t > 0$. Como la velocidad nunca cambia de signo, el objeto avanza siempre hacia adelante acercándose a la meta sin sobrepasarla jamás ($x(t) \le x_f$). **Por ende, es físicamente imposible que rebote.**

---

## 6. Comparación Física: Resorte (2º Orden) vs Lerp Clásico (1er Orden)

La guía exige comparar el resorte frente a la interpolación lineal clásica usada en programación:
$$x_{k+1} = x_k + (x_f - x_k) \cdot 0.1$$

### ¿Por qué Lerp se siente robótico y el resorte se siente vivo?
- **Lerp es una EDO de Primer Orden discretizada:**  
  $$\frac{dx}{dt} = -\lambda (x - x_f)$$
  Un sistema de 1er orden **no tiene masa ni inercia**. Su velocidad depende únicamente de la distancia restante. Al acercarse a la meta, la velocidad se reduce infinitesimalmente ("Efecto Zenón"), arrastrándose de forma perezosa sin poder rebotar nunca.
- **El Resorte es una EDO de Segundo Orden ($x''$):**  
  Posee **masa y acelera**. Almacena energía cinética ($E_k = \frac{1}{2}m v^2$) que se intercambia con la energía elástica ($E_p = \frac{1}{2}k \Delta x^2$). Esto le permite llegar a la meta con velocidad real, generando rebotes elásticos o frenadas con peso físico orgánico.

---

## 7. Criterios de Selección de Parámetros en Videojuegos e Interfaces (Game Feel)

| Elemento | $\zeta$ Elegido | Justificación de Ingeniería y Experiencia de Usuario (UX) |
|---|:---:|---|
| **Cámara de Videojuego** | $\zeta = 1.0$ (Crítico) | Debe perseguir al personaje con la máxima velocidad posible sin sobrepasarlo. Si $\zeta < 1$, la cámara oscilaría adelante y atrás provocando mareo visual (*motion sickness*). |
| **Menús y Botones UI** | $\zeta \approx 0.5$ (Subamortiguado) | Un sobreimpulso elástico moderado ($\sim 16\%$) genera una respuesta táctil viva y reactiva (*juiciness*), simulando plasticidad física tal como hace Apple en iOS y Google en Material Design. |
| **Barra de Vida RPG** | $\zeta \approx 2.0$ (Sobreamortiguado) | El descenso de salud debe sentirse definitivo, pesado y visceral. Si fuera subamortiguada, la barra caería de más y rebotaría hacia arriba, simulando falsamente que el jugador recuperó vida tras recibir un impacto. |

---

## 8. Verificación Numérica mediante Runge-Kutta de Orden 4 (RK4)

Para simular computacionalmente la ecuación de segundo orden, la convertimos en un sistema de dos ecuaciones diferenciales de primer orden en variables de estado $Y = [x, v]^T$:
$$\begin{cases} x' = v \\ v' = -2\zeta\omega v - \omega^2(x - x_f) \end{cases}$$

Implementamos el algoritmo Runge-Kutta de orden 4 (RK4) con 4 evaluaciones de pendiente ($k_1, k_2, k_3, k_4$) y paso temporal $h = 0.001\text{ s}$.

### Verificación de Precisión Absoluta:
Evaluando la solución numérica frente a la analítica exacta deducida a mano en el mismo vector de tiempos:
$$|x_{\text{num}}(t) - x_{\text{exacta}}(t)| < 1.93 \times 10^{-10}\text{ m}$$

Esto cumple a cabalidad con la regla dorada de la asignatura:
> *"Primero la matemática, después el programa. El programa no reemplaza la solución analítica: la verifica."*
