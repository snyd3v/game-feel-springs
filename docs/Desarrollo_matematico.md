# Proyecto 4. Resortes para animar: el «game feel»

**Ecuaciones Diferenciales · Unidad 3: Ecuaciones diferenciales de orden superior**\
**Institución Universitaria Colegio Mayor del Cauca**\
**Ingeniería Informática · Ingeniería Multimedia**\
**Docente:** Ing. Diana Méndez Astudillo

**Grupo 4:** Edwin Esneider Burbano Luna · Cristian Alexis Chantre Hurtado · Luis Eduardo Hurtado Hormiga · Andrés Felipe Suaza Cerón

| Parte | Contenido | Secciones |
|---|---|:---:|
| **A. Ejercicio resuelto** | Modelo, cambio de variable, ecuación característica, los tres ejercicios y explicación del rebote | 1 a 5 |
| **B. Análisis de la aplicación** | Comparación con lerp, elección de parámetros y verificación numérica | 6 a 8 |

---

# Parte A. Ejercicio resuelto

### Enunciado

Si $x(t)$ es la posición del elemento animado y $x_f$ su destino:

```math
x''+2\zeta\omega x'+\omega^2(x-x_f)=0
```

1. Con el cambio $u=x-x_f$, mostrar que la ecuación se vuelve homogénea.
2. Resolverla para $\zeta=0.3$, $\zeta=1$ y $\zeta=2$, con las condiciones:

```math
\omega=8,\qquad x(0)=0,\qquad x'(0)=0,\qquad x_f=1
```

3. Explicar, a partir de la forma de la solución, por qué $\zeta<1$ produce rebote y $\zeta\geq 1$ no.

**Convención:** se opera con valores exactos y se redondea al final. El signo $\approx$ indica un valor redondeado.

---

## 1. El modelo: de dónde sale cada término

Una masa $m$ está sujeta a un resorte de constante $k$ y a un amortiguador de constante $c$. Su posición de equilibrio es el destino $x_f$.

```text
  /|            k
  /|                          +-------+
  /|-----/\/\/\/\/\/\/\-------|       |
  /|                          |   m   |
  /|            c             |       |
  /|----------[ =|  ]---------|       |
  /|                          +---+---+
  /|                              :   ---> x(t)
                                  :
                          equilibrio: x = x_f
```

**Las fuerzas del modelo son:**

```math
\begin{aligned}
&\text{El resorte tira hacia el destino:} &&\quad F_r=-k(x-x_f)\\[4pt]
&\text{El amortiguador frena según la velocidad:} &&\quad F_a=-cx'\\[4pt]
&\text{No hay otra fuerza externa:} &&\quad F(t)=0
\end{aligned}
```

**Por la segunda ley de Newton**, con $x''$ como aceleración:

```math
\begin{aligned}
mx''&=F_r+F_a+F(t)\\[4pt]
mx''&=-k(x-x_f)-cx'\\[4pt]
mx''+cx'+k(x-x_f)&=0
\end{aligned}
```

Es la forma vista en clase, $mx''+cx'+kx=F(t)$, con el término constante $kx_f$ al lado derecho.

**Dividimos entre la masa**, pues $m\neq 0$:

```math
x''+\frac{c}{m}x'+\frac{k}{m}(x-x_f)=0
```

**Se dice** que la frecuencia natural es $\omega$:

```math
\omega=\sqrt{\frac{k}{m}}
\quad\Longrightarrow\quad
\frac{k}{m}=\omega^2
```

**El amortiguamiento crítico** es el valor de $c$ que anula el discriminante de $mr^2+cr+k=0$:

```math
c^2-4mk=0
\quad\Longrightarrow\quad
c_{cr}=2\sqrt{mk}=2m\sqrt{\frac{k}{m}}=2m\omega
```

**El factor de amortiguamiento** $\zeta$ compara $c$ con ese valor crítico:

```math
\zeta=\frac{c}{c_{cr}}=\frac{c}{2m\omega}
\quad\Longrightarrow\quad
\frac{c}{m}=2\zeta\omega
```

**Reemplazamos** los dos cocientes:

```math
\boxed{\underbrace{x''}_{\text{inercia}}+\underbrace{2\zeta\omega x'}_{\text{amortiguador}}+\underbrace{\omega^2(x-x_f)}_{\text{resorte}}=0}
```

Aquí $\omega$ (en rad/s) controla la rapidez y $\zeta$ (sin unidades) el carácter del movimiento.

---

## 2. Cambio de variable y solución particular

### 2.1 La ecuación se vuelve homogénea

Al quitar el paréntesis se ve que la ecuación original **no es homogénea**:

```math
x''+2\zeta\omega x'+\omega^2x=\underbrace{\omega^2x_f}_{g(t)\,\neq\,0}
```

**Sea** el cambio de variable:

```math
u=x-x_f
```

**Derivamos**, teniendo en cuenta que $x_f$ es constante y su derivada es cero:

```math
\begin{aligned}
u'&=x'-0=x'\\[4pt]
u''&=x''
\end{aligned}
```

**Reemplazamos** en el modelo:

```math
\underbrace{x''}_{u''}+2\zeta\omega\underbrace{x'}_{u'}+\omega^2\underbrace{(x-x_f)}_{u}=0
```

**Por lo tanto:**

```math
\boxed{u''+2\zeta\omega u'+\omega^2u=0}
```

Es lineal, de orden 2, con coeficientes constantes y con $g(t)=0$: **es homogénea**.

**Las condiciones iniciales también cambian:**

```math
\begin{aligned}
u(0)&=x(0)-x_f=0-1=-1\\[4pt]
u'(0)&=x'(0)=0
\end{aligned}
```

### 2.2 La solución particular por coeficientes indeterminados

La ecuación en $x$ no es homogénea, entonces su solución general es:

```math
x=x_h+x_p
```

**Sol/: 1) Homogénea,** $x_h$

```math
x_h''+2\zeta\omega x_h'+\omega^2x_h=0
```

Es la misma ecuación de $u$. Se resuelve en las secciones 3 y 4.

**2) No es homogénea,** $x_p$

Como $g(t)=\omega^2x_f$ es una constante, la tabla del método dice ensayar:

```math
x_p=A
```

**Revisamos si hay resonancia.** Una constante solo aparece en $x_h$ si $r=0$ es raíz de la ecuación característica:

```math
(0)^2+2\zeta\omega(0)+\omega^2=\omega^2\neq 0
```

No hay resonancia, entonces no se multiplica por $t$.

**Derivamos:**

```math
x_p=A,\qquad x_p'=0,\qquad x_p''=0
```

**Reemplazo:**

```math
\begin{aligned}
0+2\zeta\omega(0)+\omega^2A&=\omega^2x_f\\[4pt]
\omega^2A&=\omega^2x_f\\[4pt]
A&=x_f
\end{aligned}
```

**Comparamos con el cambio de variable.** Como $x_h=x-x_p=x-x_f$, sus condiciones iniciales son:

```math
x_h(0)=0-1=-1,\qquad x_h'(0)=0
```

Son la misma ecuación y las mismas condiciones de $u$, entonces $x_h=u$.

**Por lo tanto:**

```math
\boxed{x(t)=x_h+x_p=u(t)+x_f}
```

El cambio de variable y los coeficientes indeterminados llevan a la misma solución.

---

## 3. Ecuación característica y los tres regímenes

**Ensayar** con:

```math
u=e^{rt},\qquad u'=re^{rt},\qquad u''=r^2e^{rt}
```

**Reemplazamos** en la ecuación homogénea:

```math
\begin{aligned}
r^2e^{rt}+2\zeta\omega re^{rt}+\omega^2e^{rt}&=0\\[4pt]
e^{rt}\left(r^2+2\zeta\omega r+\omega^2\right)&=0
\end{aligned}
```

**Como** la exponencial nunca se anula:

```math
e^{rt}\neq 0
\quad\wedge\quad
\boxed{r^2+2\zeta\omega r+\omega^2=0}
```

**Fórmula del estudiante:**

```math
ar^2+br+c=0
\quad\Longrightarrow\quad
r=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
```

**Para nuestra ecuación,** los coeficientes de la fórmula son $1$, $2\zeta\omega$ y $\omega^2$:

```math
\begin{aligned}
r&=\frac{-2\zeta\omega\pm\sqrt{(2\zeta\omega)^2-4(1)(\omega^2)}}{2(1)}\\[6pt]
&=\frac{-2\zeta\omega\pm\sqrt{4\zeta^2\omega^2-4\omega^2}}{2}\\[6pt]
&=\frac{-2\zeta\omega\pm\sqrt{4\omega^2(\zeta^2-1)}}{2}\\[6pt]
&=\frac{-2\zeta\omega\pm 2\omega\sqrt{\zeta^2-1}}{2}\\[6pt]
&=\frac{2\left(-\zeta\omega\pm\omega\sqrt{\zeta^2-1}\right)}{2}
\end{aligned}
```

```math
\boxed{r=-\zeta\omega\pm\omega\sqrt{\zeta^2-1}}
```

**El signo del discriminante define todo.** Con $c=2m\zeta\omega$ y $k=m\omega^2$, el discriminante del sistema masa–resorte es:

```math
\begin{aligned}
c^2-4mk&=(2m\zeta\omega)^2-4m(m\omega^2)\\[4pt]
&=4m^2\omega^2(\zeta^2-1)
\end{aligned}
```

Como $4m^2\omega^2$ es positivo, el signo lo decide $\zeta^2-1$. Para $\zeta>0$:

| Signo de $c^2-4mk$ | Valor de $\zeta$ | Raíces | Régimen | Solución |
|:---:|:---:|---|---|---|
| Positivo | $\zeta>1$ | **Caso 1:** reales negativas distintas | Sobreamortiguado | $u=C_1e^{r_1t}+C_2e^{r_2t}$ |
| Cero | $\zeta=1$ | **Caso 2:** real negativa doble | Crítico | $u=(C_1+C_2t)e^{rt}$ |
| Negativo | $\zeta<1$ | **Caso 3:** complejas $a\pm bi$ | Subamortiguado | $u=e^{at}(C_1\cos bt+C_2\ \mathrm{sen}\ bt)$ |

Los coeficientes son constantes, luego continuos, y el de $u''$ es $1\neq 0$. Por el teorema de existencia y unicidad, **cada problema de valor inicial tiene una única solución**.

---

## 4. Solución para cada valor de ζ

En los tres ejercicios:

```math
\omega=8,\qquad \omega^2=64,\qquad x_f=1,\qquad u(0)=-1,\qquad u'(0)=0
```

### 4.1 Ejercicio a) ζ = 0.3, subamortiguado

**Paso 1. Reemplazamos los valores**

```math
2\zeta\omega=2(0.3)(8)=4.8
\quad\Longrightarrow\quad
u''+4.8u'+64u=0
```

**Paso 2. Ecuación característica**

Con $u=e^{rt}$, sus derivadas son $u'=re^{rt}$ y $u''=r^2e^{rt}$:

```math
\begin{aligned}
r^2e^{rt}+4.8re^{rt}+64e^{rt}&=0\\[4pt]
e^{rt}(r^2+4.8r+64)&=0
\end{aligned}
```

```math
e^{rt}\neq 0\quad\wedge\quad r^2+4.8r+64=0
```

**Paso 3. Raíces por la fórmula del estudiante**

```math
\begin{aligned}
r&=\frac{-4.8\pm\sqrt{(4.8)^2-4(1)(64)}}{2(1)}\\[6pt]
&=\frac{-4.8\pm\sqrt{23.04-256}}{2}
=\frac{-4.8\pm\sqrt{-232.96}}{2}\\[6pt]
&=\frac{-4.8\pm\sqrt{(-1)(1.6)^2(91)}}{2}\\[6pt]
&=\frac{-4.8\pm 1.6\sqrt{91}\,i}{2}
=\frac{2\left(-2.4\pm 0.8\sqrt{91}\,i\right)}{2}
\end{aligned}
```

```math
r_1=-2.4+0.8\sqrt{91}\,i
\qquad\text{y}\qquad
r_2=-2.4-0.8\sqrt{91}\,i
```

**Tomando** $r_1$:

```math
a=-2.4
\qquad\text{y}\qquad
b=0.8\sqrt{91}\approx 7.6315
```

**Paso 4. Solución general (Caso 3: raíces complejas conjugadas)**

```math
u(t)=e^{-2.4t}\big(C_1\cos(bt)+C_2\,\mathrm{sen}(bt)\big)
```

**Paso 5. Aplico las condiciones iniciales**

Para $u(0)=-1$:

```math
\begin{aligned}
u(0)=\underbrace{e^{-2.4(0)}}_{1}\Big(C_1\underbrace{\cos(0)}_{1}+C_2\underbrace{\mathrm{sen}(0)}_{0}\Big)&=-1\\[4pt]
C_1&=-1
\end{aligned}
```

Para $u'(0)=0$ primero derivamos, por la regla del producto:

```math
\begin{aligned}
u'(t)={}&\left(e^{-2.4t}\right)'\big(C_1\cos bt+C_2\,\mathrm{sen}\,bt\big)+e^{-2.4t}\big(C_1\cos bt+C_2\,\mathrm{sen}\,bt\big)'\\[6pt]
={}&-2.4e^{-2.4t}\big(C_1\cos bt+C_2\,\mathrm{sen}\,bt\big)+e^{-2.4t}\big(-bC_1\,\mathrm{sen}\,bt+bC_2\cos bt\big)
\end{aligned}
```

Evaluamos en $t=0$:

```math
\begin{aligned}
u'(0)=-2.4(1)\big(C_1(1)+C_2(0)\big)+(1)\big(-bC_1(0)+bC_2(1)\big)&=0\\[4pt]
-2.4C_1+bC_2&=0
\end{aligned}
```

Como $C_1=-1$:

```math
\begin{aligned}
2.4+bC_2&=0\\[4pt]
C_2&=-\frac{2.4}{b}=-\frac{2.4}{0.8\sqrt{91}}=-\frac{3}{\sqrt{91}}\approx -0.3145
\end{aligned}
```

**Paso 6. Por lo tanto, la solución particular del problema es**

```math
u(t)=-e^{-2.4t}\left(\cos bt+\frac{3}{\sqrt{91}}\,\mathrm{sen}\,bt\right)
```

Como $x=u+x_f=u+1$:

```math
x(t)=1-e^{-2.4t}\left[\cos\!\left(0.8\sqrt{91}\,t\right)+\frac{3}{\sqrt{91}}\,\mathrm{sen}\!\left(0.8\sqrt{91}\,t\right)\right]
```

```math
\boxed{x(t)\approx 1-e^{-2.4t}\big[\cos(7.6315t)+0.3145\,\mathrm{sen}(7.6315t)\big]}
```

**Paso 7. Comprobamos las condiciones iniciales**

```math
x(0)=1-1\,(1+0)=0
```

Agrupamos la derivada del paso 5 por coseno y seno:

```math
x'(t)=u'(t)=e^{-2.4t}\Big[\underbrace{(-2.4C_1+bC_2)}_{0}\cos bt+\underbrace{(-bC_1-2.4C_2)}_{80/\sqrt{91}}\,\mathrm{sen}\,bt\Big]
```

El coeficiente del seno, con $b=0.8\sqrt{91}$, sale de:

```math
-bC_1-2.4C_2=0.8\sqrt{91}+\frac{7.2}{\sqrt{91}}=\frac{72.8+7.2}{\sqrt{91}}=\frac{80}{\sqrt{91}}\approx 8.3863
```

```math
x'(t)\approx 8.3863\,e^{-2.4t}\,\mathrm{sen}(7.6315t)
\quad\Longrightarrow\quad
x'(0)=0
```

---

### 4.2 Ejercicio b) ζ = 1, críticamente amortiguado

**Paso 1. Reemplazamos los valores**

```math
2\zeta\omega=2(1)(8)=16
\quad\Longrightarrow\quad
u''+16u'+64u=0
```

**Paso 2. Ecuación característica**

Con $u=e^{rt}$, sus derivadas son $u'=re^{rt}$ y $u''=r^2e^{rt}$:

```math
\begin{aligned}
r^2e^{rt}+16re^{rt}+64e^{rt}&=0\\[4pt]
e^{rt}(r^2+16r+64)&=0
\end{aligned}
```

```math
e^{rt}\neq 0\quad\wedge\quad r^2+16r+64=0
```

**Paso 3. Raíces**

El discriminante es cero, entonces es un trinomio cuadrado perfecto:

```math
\begin{aligned}
(16)^2-4(1)(64)&=256-256=0\\[4pt]
(r+8)^2&=0\\[4pt]
r&=-8
\end{aligned}
```

$r=-8$ tiene multiplicidad 2.

**Paso 4. Solución general (Caso 2: raíz real con multiplicidad)**

Una raíz de multiplicidad 2 aporta las soluciones $e^{-8t}$ y $te^{-8t}$:

```math
u(t)=C_1e^{-8t}+C_2te^{-8t}=(C_1+C_2t)e^{-8t}
```

**Paso 5. Aplico las condiciones iniciales**

Para $u(0)=-1$:

```math
\begin{aligned}
u(0)=\big(C_1+C_2(0)\big)\underbrace{e^{-8(0)}}_{1}&=-1\\[4pt]
C_1&=-1
\end{aligned}
```

Para $u'(0)=0$ derivamos, por la regla del producto:

```math
\begin{aligned}
u'(t)&=(C_1+C_2t)'e^{-8t}+(C_1+C_2t)\left(e^{-8t}\right)'\\[4pt]
&=C_2e^{-8t}-8(C_1+C_2t)e^{-8t}
\end{aligned}
```

Evaluamos en $t=0$:

```math
\begin{aligned}
u'(0)=C_2(1)-8(C_1+0)(1)&=0\\[4pt]
C_2-8(-1)&=0\\[4pt]
C_2&=-8
\end{aligned}
```

**Paso 6. Por lo tanto, la solución particular del problema es**

```math
u(t)=(-1-8t)e^{-8t}=-(1+8t)e^{-8t}
```

Como $x=u+1$:

```math
\boxed{x(t)=1-(1+8t)e^{-8t}}
```

**Paso 7. Comprobamos las condiciones iniciales**

```math
x(0)=1-(1+0)(1)=0
```

```math
\begin{aligned}
x'(t)=u'(t)&=-8e^{-8t}-8(-1-8t)e^{-8t}\\[4pt]
&=64te^{-8t}
\quad\Longrightarrow\quad
x'(0)=0
\end{aligned}
```

---

### 4.3 Ejercicio c) ζ = 2, sobreamortiguado

**Paso 1. Reemplazamos los valores**

```math
2\zeta\omega=2(2)(8)=32
\quad\Longrightarrow\quad
u''+32u'+64u=0
```

**Paso 2. Ecuación característica**

Con $u=e^{rt}$, sus derivadas son $u'=re^{rt}$ y $u''=r^2e^{rt}$:

```math
\begin{aligned}
r^2e^{rt}+32re^{rt}+64e^{rt}&=0\\[4pt]
e^{rt}(r^2+32r+64)&=0
\end{aligned}
```

```math
e^{rt}\neq 0\quad\wedge\quad r^2+32r+64=0
```

**Paso 3. Raíces por la fórmula del estudiante**

```math
\begin{aligned}
r&=\frac{-32\pm\sqrt{(32)^2-4(1)(64)}}{2(1)}\\[6pt]
&=\frac{-32\pm\sqrt{1024-256}}{2}
=\frac{-32\pm\sqrt{768}}{2}\\[6pt]
&=\frac{-32\pm\sqrt{(16)^2(3)}}{2}
=\frac{2\left(-16\pm 8\sqrt{3}\right)}{2}
\end{aligned}
```

```math
r_1=-16+8\sqrt{3}\approx -2.1436
\qquad\text{y}\qquad
r_2=-16-8\sqrt{3}\approx -29.8564
```

**Paso 4. Solución general (Caso 1: raíces reales distintas)**

```math
u(t)=C_1e^{r_1t}+C_2e^{r_2t}
```

**Paso 5. Aplico las condiciones iniciales**

Para $u(0)=-1$:

```math
\begin{aligned}
u(0)=C_1\underbrace{e^{r_1(0)}}_{1}+C_2\underbrace{e^{r_2(0)}}_{1}&=-1\\[4pt]
C_1+C_2&=-1
\end{aligned}
```

Para $u'(0)=0$ derivamos:

```math
u'(t)=r_1C_1e^{r_1t}+r_2C_2e^{r_2t}
```

Evaluamos en $t=0$:

```math
\begin{aligned}
u'(0)=r_1C_1(1)+r_2C_2(1)&=0\\[4pt]
r_1C_1+r_2C_2&=0
\end{aligned}
```

**Sistema 2×2:**

```math
\begin{cases}
C_1+C_2=-1 & \quad(1)\\
r_1C_1+r_2C_2=0 & \quad(2)
\end{cases}
```

Multiplicamos (1) por $-r_1$ y le sumamos (2), para eliminar $C_1$:

```math
\begin{array}{lrcl}
(1)\cdot(-r_1): & -r_1C_1-r_1C_2 & = & r_1\\
+\,(2): & r_1C_1+r_2C_2 & = & 0\\
\hline
& (r_2-r_1)C_2 & = & r_1
\end{array}
```

Como $r_2-r_1=-16\sqrt{3}$:

```math
\begin{aligned}
C_2&=\frac{r_1}{r_2-r_1}=\frac{-16+8\sqrt{3}}{-16\sqrt{3}}=\frac{-8(2-\sqrt{3})}{-8(2\sqrt{3})}=\frac{2-\sqrt{3}}{2\sqrt{3}}\\[6pt]
&=\frac{2-\sqrt{3}}{2\sqrt{3}}\cdot\frac{\sqrt{3}}{\sqrt{3}}=\frac{2\sqrt{3}-3}{6}\approx 0.07735
\end{aligned}
```

Si $C_1+C_2=-1$, entonces:

```math
\begin{aligned}
C_1&=-1-C_2=-1-\frac{2\sqrt{3}-3}{6}\\[6pt]
&=\frac{-6-2\sqrt{3}+3}{6}=-\frac{3+2\sqrt{3}}{6}\approx -1.07735
\end{aligned}
```

**Paso 6. Por lo tanto, la solución particular del problema es**

```math
u(t)=-\frac{3+2\sqrt{3}}{6}e^{r_1t}+\frac{2\sqrt{3}-3}{6}e^{r_2t}
```

Como $x=u+1$:

```math
x(t)=1-\frac{3+2\sqrt{3}}{6}e^{(-16+8\sqrt{3})t}+\frac{2\sqrt{3}-3}{6}e^{(-16-8\sqrt{3})t}
```

```math
\boxed{x(t)\approx 1-1.07735e^{-2.1436t}+0.07735e^{-29.8564t}}
```

**Paso 7. Comprobamos las condiciones iniciales**

```math
x(0)\approx 1-1.07735+0.07735=0
```

En la derivada del paso 5 reemplazamos los dos productos:

```math
r_1C_1=\frac{4\sqrt{3}}{3}\approx 2.3094,\qquad r_2C_2=-\frac{4\sqrt{3}}{3}\approx -2.3094
```

```math
x'(t)=u'(t)\approx 2.3094\left(e^{-2.1436t}-e^{-29.8564t}\right)
\quad\Longrightarrow\quad
x'(0)=0
```

---

## 5. ¿Por qué ζ < 1 produce rebote y ζ ≥ 1 no?

### 5.1 Qué significa rebotar

Rebotar es pasarse del destino y devolverse. Como $u=x-x_f$:

```math
\begin{aligned}
u<0 &\iff \text{todavía no llega}\\
u=0 &\iff \text{está en el destino}\\
u>0 &\iff \text{se pasó}
\end{aligned}
```

El objeto empieza en $u(0)=-1$. Para pasarse, $u(t)$ **tiene que cruzar por cero** en algún $t>0$. Entonces buscamos si $u(t)=0$ tiene solución para $t>0$, con cualquier $\omega>0$ y saliendo del reposo.

### 5.2 Si 0 < ζ < 1: hay rebote

Las raíces son complejas. Llamamos $\alpha=\zeta\omega$ a la parte que amortigua y $\beta$ a la que oscila:

```math
r=-\alpha\pm\beta i,
\qquad
\alpha=\zeta\omega,
\qquad
\beta=\omega\sqrt{1-\zeta^2}
```

Es decir, $a=-\alpha$ y $b=\beta$. Aplicamos las condiciones iniciales como en el ejercicio a):

```math
\begin{aligned}
u(0)=C_1&=-1\\[4pt]
u'(0)=-\alpha C_1+\beta C_2=0&\quad\Longrightarrow\quad C_2=-\frac{\alpha}{\beta}
\end{aligned}
```

Entonces:

```math
u(t)=-e^{-\alpha t}\left(\cos\beta t+\frac{\alpha}{\beta}\,\mathrm{sen}\,\beta t\right)
```

**Igualamos a cero.** La exponencial no se anula, entonces:

```math
\cos\beta t+\frac{\alpha}{\beta}\,\mathrm{sen}\,\beta t=0
```

Si el coseno fuera cero, el seno sería $\pm 1$ y no se cumpliría la igualdad. Podemos dividir entre el coseno:

```math
\begin{aligned}
1+\frac{\alpha}{\beta}\tan\beta t&=0\\[4pt]
\tan\beta t&=-\frac{\beta}{\alpha}
\end{aligned}
```

La tangente es periódica, entonces hay **infinitas soluciones positivas**:

```math
t_n=\frac{\pi-\arctan(\beta/\alpha)+n\pi}{\beta},
\qquad n=0,1,2,\ldots
```

En cada una $u$ cambia de signo, porque una combinación de seno y coseno de igual frecuencia es una onda que atraviesa el cero. Es decir, el objeto cruza el destino una y otra vez. **Hay rebote**, cada vez más pequeño porque $e^{-\alpha t}$ tiende a cero.

En el ejercicio a), el primer cruce es:

```math
t_0=\frac{\pi-\arctan(7.6315/2.4)}{7.6315}\approx 0.2458\ \text{s}
```

### 5.3 Si ζ = 1: no hay rebote

La raíz es $r=-\omega$, doble. Aplicamos las condiciones iniciales como en el ejercicio b):

```math
\begin{aligned}
u(0)=C_1&=-1\\[4pt]
u'(0)=C_2-\omega C_1=0&\quad\Longrightarrow\quad C_2=-\omega
\end{aligned}
```

Entonces:

```math
u(t)=-(1+\omega t)e^{-\omega t}
```

**Igualamos a cero:**

```math
e^{-\omega t}\neq 0
\quad\wedge\quad
1+\omega t=0
\quad\Longrightarrow\quad
t=-\frac{1}{\omega}<0
```

El único cero está en un tiempo negativo. Para $t\geq 0$ siempre es $u<0$, es decir $x<x_f$. **No hay rebote.**

En el ejercicio b) ese cero es $t=-1/8$.

### 5.4 Si ζ > 1: no hay rebote

Las raíces son reales y cumplen $r_2<r_1<0$, porque $\sqrt{\zeta^2-1}<\zeta$. Del mismo sistema 2×2 del ejercicio c):

```math
C_2=\frac{r_1}{r_2-r_1},
\qquad
C_1=-1-C_2=\frac{-r_2}{r_2-r_1}
```

```math
u(t)=\frac{-r_2e^{r_1t}+r_1e^{r_2t}}{r_2-r_1}
```

**Igualamos a cero** el numerador, dividimos entre $r_1e^{r_1t}$ y aplicamos logaritmo natural:

```math
\begin{aligned}
-r_2e^{r_1t}+r_1e^{r_2t}&=0\\[4pt]
r_1e^{r_2t}&=r_2e^{r_1t}\\[4pt]
e^{(r_2-r_1)t}&=\frac{r_2}{r_1}\\[4pt]
(r_2-r_1)t&=\ln\!\left(\frac{r_2}{r_1}\right)\\[4pt]
t&=\frac{\ln(r_2/r_1)}{r_2-r_1}<0
\end{aligned}
```

Es negativo porque $r_2/r_1>1$, así que el logaritmo es positivo, y el denominador $r_2-r_1$ es negativo. Para $t\geq 0$ siempre es $u<0$. **No hay rebote.**

En el ejercicio c) ese cero es:

```math
t=\frac{\ln(13.928)}{-27.7128}\approx -0.0950\ \text{s}
```

### 5.5 ¿Cuánto rebota? Primer pico y sobreimpulso

El pico ocurre cuando la velocidad es cero. Para $0<\zeta<1$ derivamos $u$:

```math
\begin{aligned}
u'(t)={}&\alpha e^{-\alpha t}\left(\cos\beta t+\frac{\alpha}{\beta}\,\mathrm{sen}\,\beta t\right)-e^{-\alpha t}\left(-\beta\,\mathrm{sen}\,\beta t+\alpha\cos\beta t\right)\\[6pt]
={}&e^{-\alpha t}\bigg[\underbrace{(\alpha-\alpha)}_{0}\cos\beta t+\left(\frac{\alpha^2}{\beta}+\beta\right)\mathrm{sen}\,\beta t\bigg]\\[6pt]
={}&\frac{\alpha^2+\beta^2}{\beta}e^{-\alpha t}\,\mathrm{sen}\,\beta t
\end{aligned}
```

Simplificamos el numerador:

```math
\alpha^2+\beta^2=\zeta^2\omega^2+\omega^2(1-\zeta^2)=\omega^2
```

Como $x'=u'$:

```math
x'(t)=\frac{\omega^2}{\beta}e^{-\alpha t}\,\mathrm{sen}\,\beta t
```

La velocidad es cero cuando $\beta t=n\pi$. El primer pico es con $n=1$, porque allí la velocidad pasa de positiva a negativa:

```math
\boxed{t_p=\frac{\pi}{\beta}}
```

Reemplazamos en $u$, con coseno igual a $-1$ y seno igual a $0$:

```math
u(t_p)=-e^{-\alpha\pi/\beta}(-1+0)=e^{-\alpha\pi/\beta}
```

El exponente solo depende de $\zeta$, porque $\omega$ se cancela:

```math
\frac{\alpha}{\beta}=\frac{\zeta\omega}{\omega\sqrt{1-\zeta^2}}=\frac{\zeta}{\sqrt{1-\zeta^2}}
```

Como el salto mide 1, el sobreimpulso en porcentaje es:

```math
\boxed{M_p=100\,e^{-\pi\zeta/\sqrt{1-\zeta^2}}}
```

En el ejercicio a):

```math
\begin{aligned}
t_p&=\frac{\pi}{7.6315}\approx 0.4117\ \text{s}\\[6pt]
x(t_p)&=1+e^{-2.4(0.4117)}\approx 1.3723\ \text{m}\\[6pt]
M_p&\approx 37.23\,\%
\end{aligned}
```

### 5.6 ¿Cuánto tarda en asentarse?

Se considera asentado cuando queda a menos del 2 % del salto, es decir $|u|\leq 0.02$.

**Ejercicio a).** La combinación de seno y coseno es una sola onda de amplitud $\sqrt{C_1^2+C_2^2}$, entonces nunca la supera:

```math
|u(t)|\leq e^{-2.4t}\sqrt{(-1)^2+\left(\frac{-3}{\sqrt{91}}\right)^2}\approx 1.0483e^{-2.4t}
```

Exigimos que esa envolvente sea menor o igual a 0.02:

```math
\begin{aligned}
1.0483e^{-2.4t}&\leq 0.02\\[4pt]
e^{-2.4t}&\leq\frac{0.02}{1.0483}\\[4pt]
-2.4t&\leq\ln\!\left(\frac{0.02}{1.0483}\right)\approx -3.9592\\[4pt]
t&\geq 1.65\ \text{s}
\end{aligned}
```

La desigualdad se invierte al dividir entre $-2.4$. Es una cota: desde 1.65 s está asentado con seguridad (en la simulación entra definitivamente a 1.40 s).

**Ejercicio b).** Con $s=8t$:

```math
(1+s)e^{-s}=0.02
```

No se puede despejar, se resuelve por tanteo:

| $s$ | 5 | 5.8 | 5.834 | 5.9 |
|:---:|:---:|:---:|:---:|:---:|
| $(1+s)e^{-s}$ | 0.0404 | 0.0206 | 0.0200 | 0.0189 |

```math
t=\frac{5.834}{8}\approx 0.73\ \text{s}
```

**Ejercicio c).** El término con $e^{-29.8564t}$ desaparece muy rápido, queda el término lento:

```math
\begin{aligned}
1.07735e^{-2.1436t}&=0.02\\[4pt]
-2.1436t&=\ln\!\left(\frac{0.02}{1.07735}\right)\approx -3.9865\\[4pt]
t&\approx 1.86\ \text{s}
\end{aligned}
```

### 5.7 Comparación de los tres regímenes

| | a) $\zeta=0.3$ | b) $\zeta=1$ | c) $\zeta=2$ |
|---|:---:|:---:|:---:|
| Raíces | $-2.4\pm 7.6315i$ | $-8$ (doble) | $-2.1436$ y $-29.8564$ |
| Régimen | Subamortiguado | Crítico | Sobreamortiguado |
| ¿Rebota? | Sí | No | No |
| Sobreimpulso | 37.23 % | 0 % | 0 % |
| Asentamiento al 2 % | 1.65 s (cota) | 0.73 s | 1.86 s |

Valores de $x(t)$, en metros, para bosquejar las tres curvas:

| $t$ (s) | 0 | 0.25 | 0.41 | 0.82 | 1.23 | 2 | 3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $\zeta=0.3$ | 0 | 1.019 | 1.372 | 0.861 | 1.052 | 1.006 | 1.001 |
| $\zeta=1$ | 0 | 0.594 | 0.839 | 0.989 | 0.999 | 1.000 | 1.000 |
| $\zeta=2$ | 0 | 0.370 | 0.553 | 0.814 | 0.923 | 0.985 | 0.998 |

**Respuesta.** Con $\zeta<1$ las raíces tienen parte imaginaria. De ella salen el seno y el coseno, que hacen cambiar de signo a $u$ muchas veces: hay rebote. Con $\zeta\geq 1$ las raíces son reales, solo hay exponenciales y, saliendo del reposo, $u$ no se anula para $t>0$: no hay rebote.

Si el objeto ya trae velocidad hacia el destino, con $\zeta\geq 1$ puede pasarse **como máximo una vez**, porque esas soluciones tienen a lo sumo un cero. Nunca oscila.

---

# Parte B. Análisis de la aplicación

## 6. Resorte contra interpolación lineal (lerp)

La interpolación de la guía, `x += (destino - x) * 0.1`, se escribe por cuadros así:

```math
x_{k+1}=x_k+0.1(1-x_k),\qquad x_0=0
```

**Restamos ambos lados de 1** para ver la distancia que falta:

```math
\begin{aligned}
1-x_{k+1}&=1-x_k-0.1(1-x_k)\\[4pt]
&=0.9(1-x_k)
\end{aligned}
```

En cada cuadro la distancia se multiplica por 0.9. Como al inicio es $1-x_0=1$, después de $k$ cuadros:

```math
\begin{aligned}
1-x_k&=(0.9)^k\\[4pt]
x_k&=1-(0.9)^k
\end{aligned}
```

Como $(0.9)^k$ siempre es positivo, **el lerp nunca se pasa del destino**. Para quedar a menos del 2 %:

```math
\begin{aligned}
(0.9)^k&\leq 0.02\\[4pt]
k&\geq\frac{\ln 0.02}{\ln 0.9}\approx 37.13
\quad\Longrightarrow\quad
k=38\ \text{cuadros}
\end{aligned}
```

| Característica | Lerp | Resorte |
|---|---|---|
| Orden | 1: solo guarda la posición | 2: guarda posición y velocidad |
| Arranque, en un salto de 1 m | A máxima velocidad: 6 m/s a 60 cuadros/s | Desde el reposo, con aceleración inicial de 64 m/s² |
| Rebote | Nunca | Sí, si $\zeta<1$ |
| Asentamiento | 38 cuadros: 0.63 s a 60 Hz y 0.26 s a 144 Hz | En segundos, según $\zeta$ y $\omega$ |
| Parámetros | Un solo factor | Rapidez y carácter por separado |

**La diferencia no es cuál llega primero, sino cómo se mueve.** El resorte conserva la velocidad de un instante al otro (inercia). En la aplicación el lerp se fija a 60 pasos por segundo para que la comparación sea justa.

---

## 7. Elección de parámetros y conclusión de ingeniería

El sobreimpulso depende solo de $\zeta$. El asentamiento, para un $\zeta$ fijo, es inversamente proporcional a $\omega$. Por eso $\zeta$ se elige por el carácter y $\omega$ por la rapidez.

### 7.1 Parámetros elegidos

| Elemento | $\zeta$ | $\omega$ (rad/s) | Sobreimpulso | Asentamiento al 2 % |
|---|:---:|:---:|:---:|:---:|
| Cámara | 1 | 6 | 0 % | $5.834/6\approx 0.97$ s |
| Menú | 0.5 | 10 | 16.3 % (36 px de 220 px) | 0.81 s (cota) |
| Barra de vida | 2 | 8 | 0 % | 1.86 s |

- **Cámara, ζ = 1.** Con ζ = 0.5 se pasaría 16.3 % en cada salto y marearía. Con ζ = 2 tampoco rebota, pero tardaría 2.48 s en lugar de 0.97 s.
- **Menú, ζ = 0.5.** Toca su destino a los 0.24 s, cuando uno crítico con el mismo ω apenas va en el 70 %: se siente responsivo. El costo es un rebote de 36 px y asentarse más tarde (0.81 s contra 0.58 s).
- **Barra de vida, ζ = 2.** Con ζ = 0.35, un golpe de 45 puntos se pasaría 30.9 % (unos 14 puntos) y la barra subiría después, como si fuera una curación. Con ζ = 2 baja con peso y, desde el reposo, no se devuelve.

**Conclusión.** Recomendamos ζ = 1 para lo que acompaña al usuario, ζ = 0.5 para lo que debe responder con vida y ζ = 2 para lo que comunica una pérdida.

### 7.2 La cámara cuando el personaje camina

Si el personaje avanza a velocidad constante $v$, el destino es $x_f=vt$ y la ecuación **no es homogénea**:

```math
x''+2\zeta\omega x'+\omega^2x=\omega^2vt
```

Como $g(t)$ es un polinomio de grado 1 y $r=0$ no es raíz, **ensayar** sin multiplicar por $t$:

```math
x_p=At+B,\qquad x_p'=A,\qquad x_p''=0
```

**Reemplazo e igualo coeficientes:**

```math
\begin{aligned}
2\zeta\omega A+\omega^2(At+B)&=\omega^2vt\\[4pt]
\omega^2A\,t+(2\zeta\omega A+\omega^2B)&=\omega^2vt+0
\end{aligned}
```

```math
\begin{aligned}
\omega^2A=\omega^2v&\quad\Longrightarrow\quad A=v\\[4pt]
2\zeta\omega v+\omega^2B=0&\quad\Longrightarrow\quad B=-\frac{2\zeta v}{\omega}
\end{aligned}
```

**Por lo tanto:**

```math
x(t)=x_h+vt-\frac{2\zeta v}{\omega}
```

Como $x_h$ tiende a cero, la cámara queda atrás una distancia constante:

```math
x_f-x=\frac{2\zeta v}{\omega}=\frac{2(1)(280)}{6}\approx 93.3\ \text{px}
```

La aplicación muestra cerca de 91 px a 60 cuadros/s. La diferencia se debe a que el destino se mueve una vez por cuadro, antes de los pasos de integración, lo que lo adelanta en promedio medio cuadro:

```math
280\cdot\frac{1}{2(60)}\approx 2.3\ \text{px}
```

---

## 8. Verificación numérica

### 8.1 De segundo orden a sistema de primer orden

Con $v=x'$ como velocidad:

```math
\begin{cases}
x'=v\\
v'=-2\zeta\omega v-\omega^2(x-x_f)
\end{cases}
```

### 8.2 Runge–Kutta de orden 4

Con $Y=(x,v)$, el lado derecho del sistema como $F(Y)$ y un paso fijo $h$:

```math
\begin{aligned}
k_1&=F(Y_i)\\
k_2&=F\!\left(Y_i+\tfrac{h}{2}k_1\right)\\
k_3&=F\!\left(Y_i+\tfrac{h}{2}k_2\right)\\
k_4&=F(Y_i+hk_3)\\[4pt]
Y_{i+1}&=Y_i+\frac{h}{6}(k_1+2k_2+2k_3+k_4)
\end{aligned}
```

### 8.3 Numérica contra exacta

Las dos se evalúan en el mismo vector de tiempos, de 0 a 3 s. Error máximo, en metros:

| Paso | $\zeta=0.3$ | $\zeta=1$ | $\zeta=2$ |
|---|:---:|:---:|:---:|
| 0.01 s | $4.4\times 10^{-7}$ | $4.3\times 10^{-7}$ | $2.4\times 10^{-6}$ |
| 1/240 s (animación) | $1.3\times 10^{-8}$ | $1.2\times 10^{-8}$ | $6.3\times 10^{-8}$ |
| 0.001 s (verificación) | $4.4\times 10^{-11}$ | $4.0\times 10^{-11}$ | $1.9\times 10^{-10}$ |

**¿En qué se diferencian y por qué?** La solución exacta es una fórmula. La numérica avanza por pasos y en cada uno comete un error proporcional a $h^5$, que acumulado queda proporcional a $h^4$: si $h$ se divide entre 2, el error baja unas 16 veces. Con pasos muy pequeños ya domina el redondeo del computador, entre $10^{-15}$ y $10^{-14}$ m.

> **Primero la matemática, después el programa.** El programa no reemplaza la solución analítica: la verifica.
