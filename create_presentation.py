"""
Generador de la Presentación de Alto Nivel para el Proyecto 4:
Resortes para Animar: el «Game Feel»
Adaptada fielmente a la teoría, métodos y pizarra de la clase del 10/11/26
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

C_BG = RGBColor(15, 23, 42)        # Slate 900
C_CARD = RGBColor(30, 41, 59)      # Slate 800
C_BORDER = RGBColor(51, 65, 85)    # Slate 700
C_TEXT = RGBColor(248, 250, 252)   # Slate 50
C_SUBTEXT = RGBColor(148, 163, 184) # Slate 400
C_CYAN = RGBColor(56, 189, 248)    # Sky 400
C_GREEN = RGBColor(74, 222, 128)   # Green 400
C_ORANGE = RGBColor(251, 146, 60)  # Orange 400
C_ROSE = RGBColor(244, 63, 94)     # Rose 500
C_PURPLE = RGBColor(192, 132, 252) # Purple 400
C_YELLOW = RGBColor(250, 204, 21)  # Yellow 400


def add_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg


def add_header(slide, title, category, speaker, time_slot):
    cat_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.3), Inches(0.32))
    cat_shape.fill.solid()
    cat_shape.fill.fore_color.rgb = C_CARD
    cat_shape.line.color.rgb = C_CYAN
    cat_shape.line.width = Pt(1)
    tf_c = cat_shape.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category
    p_c.font.size = Pt(8.5)
    p_c.font.bold = True
    p_c.font.color.rgb = C_CYAN
    p_c.alignment = PP_ALIGN.CENTER

    spk_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(0.35), Inches(4.2), Inches(0.32))
    spk_shape.fill.solid()
    spk_shape.fill.fore_color.rgb = C_CARD
    spk_shape.line.color.rgb = C_GREEN
    spk_shape.line.width = Pt(1)
    tf_s = spk_shape.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = f"👤 {speaker}  |  ⏱️ {time_slot}"
    p_s.font.size = Pt(8.5)
    p_s.font.bold = True
    p_s.font.color.rgb = C_GREEN
    p_s.alignment = PP_ALIGN.CENTER

    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.7), Inches(0.65))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT


def add_card(slide, left, top, width, height, title="", title_color=C_CYAN, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.16)
    tf.margin_bottom = Inches(0.16)

    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(6)

    return card, tf


def set_notes(slide, text):
    notes = slide.notes_slide.notes_text_frame
    notes.text = text


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(5.4), Inches(0.35))
    tag.fill.solid(); tag.fill.fore_color.rgb = C_CARD
    tag.line.color.rgb = C_CYAN
    tf_tag = tag.text_frame
    tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
    p = tf_tag.paragraphs[0]
    p.text = "PROYECTO DE AULA · UNIDAD 3: EDO DE ORDEN SUPERIOR"
    p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = C_CYAN; p.alignment = PP_ALIGN.CENTER

    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(1.4))
    tf_title = title_box.text_frame; tf_title.word_wrap = True
    p1 = tf_title.paragraphs[0]
    p1.text = "Resortes para Animar: el «Game Feel»"
    p1.font.size = Pt(34); p1.font.bold = True; p1.font.color.rgb = C_CYAN

    p2 = tf_title.add_paragraph()
    p2.text = "Modelado Físico y Matemático con Ecuaciones Diferenciales de Segundo Orden"
    p2.font.size = Pt(15); p2.font.color.rgb = C_TEXT; p2.space_before = Pt(4)

    _, tf_inst = add_card(s1, 1.0, 3.0, 5.4, 3.8, "🏛️ Datos Institucionales", C_GREEN)
    items_inst = [
        ("Institución:", "Institución Universitaria Colegio Mayor del Cauca"),
        ("Facultad:", "Ingeniería Informática e Ingeniería Multimedia"),
        ("Asignatura:", "Ecuaciones Diferenciales (Unidad 3)"),
        ("Docente:", "Ing. Diana Méndez Astudillo"),
        ("Fecha:", "Noviembre 2026"),
        ("Estructura:", "15 min de exposición ordenada + 5 min de preguntas")
    ]
    for lbl, val in items_inst:
        p = tf_inst.add_paragraph()
        p.text = f"• {lbl} "
        p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
        p.space_after = Pt(3)
        run = p.add_run()
        run.text = val
        run.font.bold = False; run.font.color.rgb = C_SUBTEXT

    _, tf_team = add_card(s1, 6.8, 3.0, 5.5, 3.8, "👥 Integrantes del Grupo 4 & Roles de Defensa", C_CYAN)
    team_roles = [
        ("Edwin Esneider Burbano Luna", "Min 0-4: Modelo físico de fuerzas (Newton) y homogeneización."),
        ("Cristian Alexis Chantre Hurtado", "Min 4-8: Ecuación característica, discriminante y soluciones a mano."),
        ("Luis Eduardo Hurtado Hormiga", "Min 8-11: Comparación física con Lerp y verificación numérica RK4."),
        ("Andrés Felipe Suaza Cerón", "Min 11-15: Tres aplicaciones de Game Feel y demostración interactiva.")
    ]
    for name, role in team_roles:
        p = tf_team.add_paragraph()
        p.text = f"👤 {name}"
        p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_CYAN
        p.space_before = Pt(3)
        p_sub = tf_team.add_paragraph()
        p_sub.text = f"   {role}"
        p_sub.font.size = Pt(9); p_sub.font.color.rgb = C_SUBTEXT
        p_sub.space_after = Pt(3)

    set_notes(s1, (
        "INICIA EDWIN BURBANO (0:00 - 1:00 min):\n"
        "Buenos días profesora Diana y compañeros. Nuestro equipo, el Grupo 4, presenta el Proyecto 4: "
        "'Resortes para animar: el Game Feel'.\n"
        "En nuestra exposición nos basaremos exactamente en la teoría que vimos en clase: el diagrama de fuerzas de Newton, "
        "el análisis del discriminante para los tres regímenes y los métodos para resolver la no homogeneidad.\n"
        "Demostraremos cómo esta matemática es la que usan Apple en iOS y los videojuegos para dar peso, inercia y rebote a las interfaces."
    ))

    # =========================================================================
    # SLIDE 2: MOTIVACIÓN Y GAME FEEL
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "¿Qué es el «Game Feel» y por qué usar Resortes?", "[ 1. CONTEXTO Y MOTIVACIÓN ]", "Edwin Burbano", "Min 1:00 - 2:00")

    _, tf_prob = add_card(s2, 0.8, 1.5, 5.6, 3.6, "❌ El Problema de las Animaciones Tradicionales", C_ROSE, C_ROSE)
    p = tf_prob.add_paragraph()
    p.text = "• Animación Lineal Rígida (x += v * dt):"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_prob.add_paragraph()
    p2.text = "  Velocidad constante y artificial. Frenazos instantáneos sin inercia que se sienten plásticos y robóticos."
    p2.font.size = Pt(9); p2.font.color.rgb = C_SUBTEXT; p2.space_after = Pt(6)

    p3 = tf_prob.add_paragraph()
    p3.text = "• Interpolación Clásica (Lerp: x += (dest - x) * 0.1):"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_prob.add_paragraph()
    p4.text = "  Es una EDO de Primer Orden discretizada: dx/dt = -λ(x - x_f).\n" \
              "  No tiene masa ni aceleración. Frena de forma asintótica infinitesimal ('Efecto Zenón') y jamás puede rebotar."
    p4.font.size = Pt(9); p4.font.color.rgb = C_SUBTEXT

    _, tf_sol = add_card(s2, 6.8, 1.5, 5.7, 3.6, "✅ La Solución: Física Real de Segundo Orden", C_GREEN, C_GREEN)
    p = tf_sol.add_paragraph()
    p.text = "• El Oscilador Físico Amortiguado:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_sol.add_paragraph()
    p2.text = "  Se modela el elemento de interfaz con masa (m), aceleración (x''), amortiguamiento viscoso (c) y resorte elástico (k)."
    p2.font.size = Pt(9); p2.font.color.rgb = C_SUBTEXT; p2.space_after = Pt(6)

    p3 = tf_sol.add_paragraph()
    p3.text = "• ¿Dónde se utiliza en la industria tecnológica?:"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_sol.add_paragraph()
    p4.text = "  - Apple iOS: CASpringAnimation (menús, modales, iconos).\n" \
              "  - Android: SpringForce & DynamicAnimation.\n" \
              "  - Motores de Videojuegos: Seguimiento de cámaras, barras de vida y retroalimentación de impacto."
    p4.font.size = Pt(9); p4.font.color.rgb = C_SUBTEXT

    _, tf_pilares = add_card(s2, 0.8, 5.3, 11.7, 1.8, "🎯 Los Tres Pilares que Explicaremos con la Matemática", C_CYAN)
    pilares = [
        ("1. Inercia Real (x''):", "El objeto físico posee masa y momento; no frena en seco de la nada sino con disipación real."),
        ("2. Elasticidad Orgánica:", "Un sobreimpulso controlado (~16%) confiere reactividad táctil ('juiciness') en interfaces."),
        ("3. Continuidad Dinámica:", "Si el usuario interrumpe la animación en pleno vuelo, el resorte absorbe el cambio suavemente.")
    ]
    for tit, desc in pilares:
        p = tf_pilares.add_paragraph()
        p.text = f"• {tit} "
        p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = C_CYAN
        run = p.add_run()
        run.text = desc
        run.font.bold = False; run.font.color.rgb = C_SUBTEXT

    set_notes(s2, (
        "EXPONE EDWIN BURBANO (1:00 - 2:00 min):\n"
        "Para entender el problema: cuando un diseñador programa una animación sumando posición lineal, se ve rígida.\n"
        "Y cuando usa 'Lerp' clásico (x += (destino - x)*0.1), como la profesora explicó en clase, estamos ante una ecuación de PRIMER orden: "
        "la velocidad depende solo de la distancia que falta. Cuando está muy cerca de la meta, desacelera infinitamente pero no tiene inercia.\n"
        "En cambio, si aplicamos la Segunda Ley de Newton con un resorte amortiguado de SEGUNDO orden, le damos masa y aceleración al objeto. "
        "Eso es el Game Feel."
    ))

    # =========================================================================
    # SLIDE 3: MODELO FÍSICO DE NEWTON
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Fundamentación Física: Diagrama de Fuerzas y Ley de Newton", "[ 2. DEDUCCIÓN DEL MODELO ]", "Edwin Burbano", "Min 2:00 - 3:30")

    # Ecuación en banner superior
    _, tf_eq = add_card(s3, 0.8, 1.45, 11.7, 1.15, border_color=C_CYAN)
    p = tf_eq.paragraphs[0]
    p.text = "m x''(t)  +  c x'(t)  +  k ( x(t) - x_f )  =  0    ===>    x''(t) + 2ζω x'(t) + ω² (x(t) - x_f) = 0"
    p.font.size = Pt(17.5); p.font.bold = True; p.font.color.rgb = C_CYAN; p.alignment = PP_ALIGN.CENTER
    p_sub = tf_eq.add_paragraph()
    p_sub.text = "Deducción exacta a partir de la Segunda Ley de Newton vista en clase: Σ F = m · a"
    p_sub.font.size = Pt(9.5); p_sub.font.color.rgb = C_SUBTEXT; p_sub.alignment = PP_ALIGN.CENTER

    # Tres columnas detallando cada fuerza exactamente como en el tablero
    cols_data = [
        ("m x''(t)", "Inercia de la Masa (Newton)", C_YELLOW,
         "• Segunda Ley: Σ F = m · a\n"
         "• Con masa m (en el proyecto m = 1).\n"
         "• Representa la inercia: almacena cantidad de movimiento (momento lineal p = m·v).\n"
         "• Permite que el objeto llegue a la meta con velocidad distinta de cero."),
        ("c x'(t)  [ 2ζω x' ]", "Fricción del Amortiguador", C_ORANGE,
         "• En el tablero: 'El amortiguador frena con -c x''.\n"
         "• Fuerza disipativa opuesta a la velocidad.\n"
         "• Drena energía cinética hacia el medio en forma de calor.\n"
         "• Donde c/m = 2ζω, siendo ζ = c / (2mω) el factor adimensional de amortiguamiento."),
        ("k (x - x_f)  [ ω²(x - x_f) ]", "Tirón del Resorte (Hooke)", C_GREEN,
         "• En el tablero: 'El resorte tira con -k(x - x_f)'.\n"
         "• Fuerza elástica restauradora hacia el equilibrio x_f.\n"
         "• Frecuencia natural: ω = √(k/m), luego k/m = ω².\n"
         "• Cuanto más lejos esté la meta, mayor es la fuerza restauradora inicial.")
    ]
    for i, (term, sub, col, desc) in enumerate(cols_data):
        left_pos = 0.8 + i * 4.0
        _, tf_col = add_card(s3, left_pos, 2.75, 3.7, 3.4, f"{term}\n{sub}", col)
        for line in desc.split("\n"):
            p = tf_col.add_paragraph()
            p.text = line
            p.font.size = Pt(8.5); p.font.color.rgb = C_TEXT
            p.space_after = Pt(2)

    _, tf_params = add_card(s3, 0.8, 6.3, 11.7, 0.85, border_color=C_PURPLE)
    p = tf_params.paragraphs[0]
    p.text = "DATOS DEL PROYECTO:   ω = 8 rad/s   |   Destino: x_f = 1 m   |   Condiciones Iniciales: x(0) = 0 m,   x'(0) = 0 m/s (Reposo en el origen)"
    p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.alignment = PP_ALIGN.CENTER

    set_notes(s3, (
        "EXPONE EDWIN BURBANO (2:00 - 3:30 min):\n"
        "Veamos el modelo físico tal como lo explicó la profesora en el tablero.\n"
        "Tenemos una masa m conectada a un resorte con constante k y a un amortiguador con constante c.\n"
        "Las tres fuerzas del modelo son:\n"
        "1. El resorte tira hacia la meta con -k(x - x_f) según la Ley de Hooke.\n"
        "2. El amortiguador frena proporcional a la velocidad con -c*x'.\n"
        "3. La Segunda Ley de Newton dice que m*x'' = suma de fuerzas = -c*x' - k(x - x_f).\n"
        "Al dividir entre m, usamos las dos definiciones de clase: omega = sqrt(k/m) y c/m = 2*zeta*omega.\n"
        "Así obtenemos la ecuación canónica: x'' + 2*zeta*omega*x' + omega^2*(x - x_f) = 0."
    ))

    # =========================================================================
    # SLIDE 4: LOS DOS MÉTODOS DE SOLUCIÓN
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Los Dos Métodos de Solución: Coeficientes Indeterminados vs Cambio de Variable", "[ 3. MÉTODOS DE SOLUCIÓN ]", "Edwin Burbano", "Min 3:30 - 4:30")

    _, tf_m1 = add_card(s4, 0.8, 1.5, 5.7, 5.4, "Método A: Coeficientes Indeterminados (x = x_h + x_p)", C_CYAN)
    p = tf_m1.add_paragraph()
    p.text = "1. EDO No Homogénea de Clase:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_m1.add_paragraph()
    p2.text = "   x'' + 2ζω x' + ω² x = ω² x_f\n" \
              "   El lado derecho es una constante g(t) = ω² x_f."
    p2.font.size = Pt(9); p2.font.color.rgb = C_SUBTEXT; p2.space_after = Pt(4)

    p3 = tf_m1.add_paragraph()
    p3.text = "2. Solución Particular por Coeficientes Indeterminados:"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_m1.add_paragraph()
    p4.text = "   Como g(t) es constante, ensayamos x_p(t) = A (constante).\n" \
              "   Derivadas: x_p' = 0,  x_p'' = 0.\n" \
              "   Sustituyendo: 0 + 0 + ω² A = ω² x_f  ==>  A = x_f.\n" \
              "   ===>  x_p(t) = x_f"
    p4.font.size = Pt(9); p4.font.color.rgb = C_GREEN; p4.space_after = Pt(4)

    p5 = tf_m1.add_paragraph()
    p5.text = "3. Solución General Total:"
    p5.font.size = Pt(10.5); p5.font.bold = True; p5.font.color.rgb = C_TEXT
    p6 = tf_m1.add_paragraph()
    p6.text = "   x(t) = x_h(t) + x_p(t) = x_h(t) + x_f\n" \
              "   (Donde x_h es la solución de la homogénea)."
    p6.font.size = Pt(9.5); p6.font.color.rgb = C_CYAN

    _, tf_m2 = add_card(s4, 6.8, 1.5, 5.7, 5.4, "Método B: Cambio de Variable u = x - x_f (Guía)", C_PURPLE)
    p = tf_m2.add_paragraph()
    p.text = "1. Definición del Desplazamiento Relativo u(t):"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_m2.add_paragraph()
    p2.text = "   u(t) = x(t) - x_f (distancia que falta para la meta).\n" \
              "   Como x_f es constante: u'(t) = x'(t)  y  u''(t) = x''(t)."
    p2.font.size = Pt(9); p2.font.color.rgb = C_SUBTEXT; p2.space_after = Pt(4)

    p3 = tf_m2.add_paragraph()
    p3.text = "2. Ecuación Homogénea Resultante:"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_m2.add_paragraph()
    p4.text = "   u''(t) + 2ζω u'(t) + ω² u(t) = 0"
    p4.font.size = Pt(11); p4.font.bold = True; p4.font.color.rgb = C_PURPLE; p4.space_after = Pt(4)

    p5 = tf_m2.add_paragraph()
    p5.text = "3. Condiciones Iniciales para u(t):"
    p5.font.size = Pt(10.5); p5.font.bold = True; p5.font.color.rgb = C_TEXT
    p6 = tf_m2.add_paragraph()
    p6.text = "   u(0) = x(0) - x_f = 0 - 1 = -1\n" \
              "   u'(0) = x'(0) = 0"
    p6.font.size = Pt(9); p6.font.color.rgb = C_SUBTEXT; p6.space_after = Pt(4)

    p7 = tf_m2.add_paragraph()
    p7.text = "💡 Equivalencia Matemática:"
    p7.font.size = Pt(10.5); p7.font.bold = True; p7.font.color.rgb = C_YELLOW
    p8 = tf_m2.add_paragraph()
    p8.text = "   Ambos métodos son idénticos: u(t) es exactamente x_h(t).\n" \
              "   Al despejar: x(t) = u(t) + x_f = x_h(t) + x_p(t)."
    p8.font.size = Pt(9); p8.font.color.rgb = C_TEXT

    set_notes(s4, (
        "EXPONE EDWIN BURBANO (3:30 - 4:30 min):\n"
        "Queremos resaltar que en nuestra solución dominamos los dos métodos que la profesora enseñó:\n"
        "En el Método A, usando Coeficientes Indeterminados (como los ejemplos que resolvimos en clase el 10 de noviembre): "
        "el lado derecho es la constante omega^2*x_f, ensayamos una constante A, y nos da inmediatamente x_p = x_f.\n"
        "En el Método B, sugerido por la guía, hacemos el cambio de variable u = x - x_f. Como la meta es constante, "
        "sus derivadas son cero y obtenemos la homogénea u'' + 2*zeta*omega*u' + omega^2*u = 0 con u(0) = -1 y u'(0) = 0.\n"
        "Comprobamos que ambos métodos son exactamente lo mismo: x(t) = u(t) + x_f = x_h(t) + x_p(t).\n"
        "Ahora le doy la palabra a Cristian Chantre para analizar la ecuación característica y las soluciones a mano."
    ))

    # =========================================================================
    # SLIDE 5: ECUACIÓN CARACTERÍSTICA Y TRES REGÍMENES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Ecuación Característica y los Tres Regímenes de Clase", "[ 4. ANÁLISIS DEL DISCRIMINANTE ]", "Cristian Chantre", "Min 4:30 - 5:45")

    _, tf_poly = add_card(s5, 0.8, 1.45, 11.7, 1.15, border_color=C_CYAN)
    p = tf_poly.paragraphs[0]
    p.text = "r²  +  2ζω r  +  ω²  =  0   ===>   r = -ζω  ±  ω √( ζ² - 1 )"
    p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_CYAN; p.alignment = PP_ALIGN.CENTER
    p_disc = tf_poly.add_paragraph()
    p_disc.text = "En el tablero: 'El discriminante c² - 4mk nos define todo' (aquí Δ = 4ω²(ζ² - 1))"
    p_disc.font.size = Pt(10); p_disc.font.color.rgb = C_SUBTEXT; p_disc.alignment = PP_ALIGN.CENTER

    cases = [
        ("CASO 1: ζ < 1", "Subamortiguado (Rebote)", C_YELLOW,
         "• En el tablero: 'c² - 4mk < 0: Raíz en los complejos con parte real negativa, la masa oscila con amplitud decreciente y decae'.\n"
         "• Raíces: r = -α ± i β con β = ω√(1 - ζ²)\n"
         "• Solución: e^(-αt)[C1 cos βt + C2 sin βt]\n"
         "• Comportamiento: Cruza la meta y rebota."),
        ("CASO 2: ζ = 1", "Críticamente Amortiguado", C_GREEN,
         "• En el tablero: 'c² - 4mk = 0: Una raíz real negativa, es el regreso más rápido sin posible oscilación'.\n"
         "• Raíz doble: r = -ω (Multiplicidad 2)\n"
         "• Solución: (C1 + C2 t) e^(-ω t)\n"
         "• Comportamiento: Llega a la meta en tiempo récord sin sobrepasarla jamás."),
        ("CASO 3: ζ > 1", "Sobreamortiguado (Pesado)", C_PURPLE,
         "• En el tablero: 'c² - 4mk > 0: Dos raíces reales negativas distintas, la masa vuelve al equilibrio sin oscilar'.\n"
         "• Raíces: r1, r2 = -ζω ± ω√(ζ² - 1) < 0\n"
         "• Solución: C1 e^(r1 t) + C2 e^(r2 t)\n"
         "• Comportamiento: Lento, pesado y sin rebote.")
    ]
    for i, (tit, reg, col, desc) in enumerate(cases):
        left_pos = 0.8 + i * 4.0
        _, tf_c = add_card(s5, left_pos, 2.75, 3.7, 4.3, f"{tit}\n{reg}", col)
        for line in desc.split("\n"):
            p = tf_c.add_paragraph()
            p.text = line
            p.font.size = Pt(9); p.font.color.rgb = C_TEXT
            p.space_after = Pt(2)

    set_notes(s5, (
        "EXPONE CRISTIAN CHANTRE (4:30 - 5:45 min):\n"
        "Gracias Edwin. Al proponer la solución exponencial u = e^(rt), obtenemos la ecuación característica r^2 + 2*zeta*omega*r + omega^2 = 0.\n"
        "Como la profesora anotó textualmente en el tablero el 10 de noviembre: 'El discriminante nos define todo'.\n"
        "Aquí el discriminante depende de (zeta^2 - 1):\n"
        "1. Si zeta < 1: el radicando es negativo. Tenemos raíces complejas con senos y cosenos: el caso SUBAMORTIGUADO que oscila y rebota.\n"
        "2. Si zeta = 1: el discriminante es cero. Tenemos una raíz real doble: el caso CRÍTICO, que es el regreso más veloz a la meta sin oscilar.\n"
        "3. Si zeta > 1: el discriminante es positivo. Tenemos dos raíces reales negativas distintas: el caso SOBREAMORTIGUADO, que vuelve al equilibrio lentamente sin rebotar."
    ))

    # =========================================================================
    # SLIDE 6: SOLUCIONES ANALÍTICAS EXACTAS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Soluciones Analíticas Deducidas a Mano (ω = 8, x_f = 1)", "[ 5. DEDUCCIÓN PASO A PASO ]", "Cristian Chantre", "Min 5:45 - 7:00")

    _, tf_sol1 = add_card(s6, 0.8, 1.45, 6.0, 1.7, "Caso 1: ζ = 0.3 (Subamortiguado)", C_YELLOW)
    p = tf_sol1.add_paragraph()
    p.text = "x(t) = 1 - e^(-2.4 t) [ cos(7.6315 t) + 0.3145 sin(7.6315 t) ]"
    p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = C_YELLOW
    p2 = tf_sol1.add_paragraph()
    p2.text = "• Raíces: r = -2.4 ± 7.6315 i   |   Sobreimpulso: Mp = 37.2% en t_p = 0.41 s\n• Tiempo de asentamiento al 2%: t_s ≈ 1.63 s"
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    _, tf_sol2 = add_card(s6, 0.8, 3.3, 6.0, 1.7, "Caso 2: ζ = 1.0 (Amortiguamiento Crítico)", C_GREEN)
    p = tf_sol2.add_paragraph()
    p.text = "x(t) = 1 - ( 1 + 8 t ) e^(-8 t)"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_GREEN
    p2 = tf_sol2.add_paragraph()
    p2.text = "• Raíz doble: r = -8   |   Sobreimpulso: Mp = 0% (Sin rebote alguno)\n• Tiempo de asentamiento al 2%: t_s ≈ 0.73 s  (¡Llegada óptima más rápida!)"
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    _, tf_sol3 = add_card(s6, 0.8, 5.15, 6.0, 1.95, "Caso 3: ζ = 2.0 (Sobreamortiguado)", C_PURPLE)
    p = tf_sol3.add_paragraph()
    p.text = "x(t) = 1 - 1.0774 e^(-2.1436 t) + 0.0774 e^(-29.8564 t)"
    p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = C_PURPLE
    p2 = tf_sol3.add_paragraph()
    p2.text = "• Raíces: r1 = -2.1436,  r2 = -29.8564   |   Sobreimpulso: Mp = 0%\n• El modo rápido r2 se extingue en 0.1 s; el polo lento r1 hace la llegada pesada (t_s ≈ 1.86 s)."
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    chart_path = "assets/slide_chart_regimes.png"
    if os.path.exists(chart_path):
        s6.shapes.add_picture(chart_path, Inches(7.1), Inches(1.45), width=Inches(5.4))

    set_notes(s6, (
        "EXPONE CRISTIAN CHANTRE (5:45 - 7:00 min):\n"
        "Aplicando las condiciones iniciales paso a paso exactamente como la profesora lo hizo en el tablero:\n"
        "- Para zeta = 0.3: evaluamos u(0) = -1 y se cancela el seno (sin(0)=0), dándonos C1 = -1. "
        "Luego derivamos con regla del producto, cancelamos el seno en t=0 y despejamos C2 = -0.3145. "
        "La función alcanza su primer pico a los 0.41 segundos y se pasa un 37.2% de la meta.\n"
        "- Para zeta = 1.0: la raíz doble nos da (C1 + C2*t)e^(-8t). Con u(0)=-1 y u'(0)=0 obtenemos C1=-1 y C2=-8. "
        "Llega a la meta en solo 0.73 segundos sin rebasar jamás el 1.0.\n"
        "- Para zeta = 2.0: tenemos dos raíces reales. El término con e^(-29.8t) muere en menos de 0.1 segundos, "
        "pero el polo lento e^(-2.14t) hace que tarde 1.86 segundos en asentarse.\n"
        "En la gráfica de la derecha pueden ver cómo coinciden exactamente con la banda de asentamiento del 2%."
    ))

    # =========================================================================
    # SLIDE 7: POR QUÉ REBOTA Y POR QUÉ NO
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "¿Por qué ζ < 1 Rebota y ζ ≥ 1 No? (Explicación Física y Matemática)", "[ 6. FUNDAMENTACIÓN TEÓRICA ]", "Cristian Chantre", "Min 7:00 - 8:00")

    _, tf_why1 = add_card(s7, 0.8, 1.5, 5.7, 5.5, "🌀 Caso ζ < 1 : El Secreto de la Fórmula de Euler", C_YELLOW)
    p = tf_why1.add_paragraph()
    p.text = "1. Raíces Complejas Conjugadas:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_why1.add_paragraph()
    p2.text = "   r = -α ± i β,  donde β = ω√(1 - ζ²) ≠ 0."
    p2.font.size = Pt(9.5); p2.font.color.rgb = C_YELLOW; p2.space_after = Pt(4)

    p3 = tf_why1.add_paragraph()
    p3.text = "2. Identidad de Euler (del Tablero):"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_why1.add_paragraph()
    p4.text = "   e^((-α ± iβ)t) = e^(-α t) [ cos(β t) ± i sin(β t) ]\n" \
              "   La parte imaginaria forzosamente engendra funciones armónicas senoidales reales."
    p4.font.size = Pt(9); p4.font.color.rgb = C_SUBTEXT; p4.space_after = Pt(4)

    p5 = tf_why1.add_paragraph()
    p5.text = "3. Cruce por Cero de la Velocidad x'(t):"
    p5.font.size = Pt(10.5); p5.font.bold = True; p5.font.color.rgb = C_TEXT
    p6 = tf_why1.add_paragraph()
    p6.text = "   La velocidad x'(t) contiene sin(β t), que se anula cíclicamente en t_k = kπ/β.\n" \
              "   En esos instantes la velocidad cambia de signo (+ a - y viceversa).\n" \
              "   ===> La masa se pasa del equilibrio, la fuerza restauradora la devuelve y rebota periódicamente."
    p6.font.size = Pt(9); p6.font.color.rgb = C_TEXT

    _, tf_why2 = add_card(s7, 6.8, 1.5, 5.7, 5.5, "🛑 Caso ζ ≥ 1 : Ausencia Físico-Matemática de Rebote", C_GREEN)
    p = tf_why2.add_paragraph()
    p.text = "1. Raíces Estrictamente Reales:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_why2.add_paragraph()
    p2.text = "   Im(r) = 0. No existe componente compleja ni funciones trigonométricas."
    p2.font.size = Pt(9.5); p2.font.color.rgb = C_GREEN; p2.space_after = Pt(4)

    p3 = tf_why2.add_paragraph()
    p3.text = "2. Exponenciales Monótonas Decrecientes:"
    p3.font.size = Pt(10.5); p3.font.bold = True; p3.font.color.rgb = C_TEXT
    p4 = tf_why2.add_paragraph()
    p4.text = "   La base de soluciones es una suma de e^(-λ t).\n" \
              "   Una exponencial decreciente jamás oscila ni cambia de signo."
    p4.font.size = Pt(9); p4.font.color.rgb = C_SUBTEXT; p4.space_after = Pt(4)

    p5 = tf_why2.add_paragraph()
    p5.text = "3. Velocidad Siempre Positiva hacia Adelante:"
    p5.font.size = Pt(10.5); p5.font.bold = True; p5.font.color.rgb = C_TEXT
    p6 = tf_why2.add_paragraph()
    p6.text = "   Partiendo del reposo (x(0)=0, x'(0)=0), se demuestra que x'(t) > 0 para todo t > 0.\n" \
              "   Como la velocidad nunca cambia de signo, el objeto avanza siempre hacia adelante " \
              "sin sobrepasar jamás la meta (x(t) ≤ x_f). ¡El rebote es imposible!"
    p6.font.size = Pt(9); p6.font.color.rgb = C_TEXT

    set_notes(s7, (
        "EXPONE CRISTIAN CHANTRE (7:00 - 8:00 min):\n"
        "Esta es la pregunta conceptual que define todo: ¿por qué zeta < 1 rebota y zeta >= 1 no?\n"
        "La explicación matemática es la Fórmula de Euler que vimos en clase: e^(i*beta*t) = cos(beta*t) + i*sin(beta*t). "
        "Cuando zeta < 1, la parte imaginaria introduce senos y cosenos reales. La velocidad contiene un seno que se hace cero periódicamente "
        "y cambia de signo. Eso significa físicamente que el objeto pasa de largo la meta, frena y se devuelve: hay rebote.\n"
        "En cambio, cuando zeta >= 1, las raíces son puramente reales. La solución solo tiene exponenciales decrecientes e^(-lambda*t). "
        "Partiendo del reposo, la velocidad es siempre positiva: se acerca monótonamente por debajo y nunca cruza hacia el otro lado. "
        "Por eso es físicamente imposible que rebote.\n"
        "Ahora le doy paso a Luis Hurtado para comparar el resorte frente a Lerp y mostrar la verificación numérica."
    ))

    # =========================================================================
    # SLIDE 8: RESORTE VS LERP
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Resorte (2º Orden) vs Interpolación Lineal (Lerp / 1er Orden)", "[ 7. COMPARACIÓN FÍSICA ]", "Luis Hurtado", "Min 8:00 - 9:30")

    _, tf_comp1 = add_card(s8, 0.8, 1.45, 6.0, 2.7, "📐 Interpolación Lineal Clásica (Lerp / 1er Orden)", C_ORANGE)
    p = tf_comp1.add_paragraph()
    p.text = "Fórmula clásica en código:  x += (destino - x) * 0.1"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_ORANGE
    p2 = tf_comp1.add_paragraph()
    p2.text = "• Modelo continuo:  dx/dt = -λ (x - x_f)  (EDO de Primer Orden).\n" \
              "• Solución exacta: Decaimiento exponencial simple x(t) = x_f + (x0 - x_f)e^(-λ t).\n" \
              "• Carencia física: NO tiene masa ni aceleración. La velocidad está atada a la distancia restante.\n" \
              "• Sensación: Se arrastra lentamente al final y jamás rebota ni tiene inercia."
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    _, tf_comp2 = add_card(s8, 0.8, 4.35, 6.0, 2.7, "🌀 Resorte Dinámico (EDO de 2º Orden)", C_CYAN)
    p = tf_comp2.add_paragraph()
    p.text = "Ecuación:  x''(t) + 2ζω x'(t) + ω² (x - x_f) = 0"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_CYAN
    p2 = tf_comp2.add_paragraph()
    p2.text = "• Modelo continuo: EDO de Segundo Orden con estado Y = [x, v]^T.\n" \
              "• Preserva energía cinética: E_k = (1/2)m v², convirtiéndola en energía elástica E_p = (1/2)k Δx².\n" \
              "• Capacidad dinámica: Puede llegar a la meta con velocidad distinta de cero.\n" \
              "• Sensación: Fluida, viva, con peso y rebote orgánico personalizable."
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    chart_lerp = "assets/slide_chart_lerp_vs_spring.png"
    if os.path.exists(chart_lerp):
        s8.shapes.add_picture(chart_lerp, Inches(7.1), Inches(1.45), width=Inches(5.4))

    set_notes(s8, (
        "EXPONE LUIS HURTADO (8:00 - 9:30 min):\n"
        "Gracias Cristian. El numeral 2 del proyecto nos pide comparar el resorte frente a la interpolación lineal clásica: x += (destino - x)*0.1.\n"
        "Desde la matemática de nuestra asignatura, la diferencia es abismal:\n"
        "La regla clásica es una ecuación de PRIMER orden dx/dt = -lambda*(x - x_f). "
        "No tiene derivada segunda, lo que significa que el objeto no tiene masa ni inercia. Su velocidad depende solo de la distancia restante. "
        "Cuando está cerca de la meta, desacelera infinitesimalmente, sufriendo el efecto Zenón: se arrastra perezosamente y jamás puede rebotar.\n"
        "En cambio, el resorte es de SEGUNDO orden. Posee masa, acelera y acumula energía cinética. "
        "Al llegar a la meta llega con velocidad real, lo que permite lograr ese rebote elástico y orgánico que pueden ver en la gráfica de la derecha."
    ))

    # =========================================================================
    # SLIDE 9: VERIFICACIÓN NUMÉRICA RK4
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Verificación Numérica: Runge-Kutta 4 (RK4) vs Solución Exacta", "[ 8. VERIFICACIÓN COMPUTACIONAL ]", "Luis Hurtado", "Min 9:30 - 11:00")

    _, tf_rk = add_card(s9, 0.8, 1.45, 6.0, 2.5, "⚙️ Conversión a Sistema de Primer Orden & RK4", C_CYAN)
    p = tf_rk.add_paragraph()
    p.text = "Sistema dinámico en variables de estado Y = [x, v]^T:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_rk.add_paragraph()
    p2.text = "   { x' = v\n" \
              "   { v' = -2ζω v - ω² (x - x_f)\n" \
              "• Implementamos el algoritmo Runge-Kutta de 4º orden (RK4):\n" \
              "   Evalúa 4 pendientes intermedias k1, k2, k3, k4 por cada paso dt.\n" \
              "   Error local: O(dt^5), error global acumulado: O(dt^4)."
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_SUBTEXT

    _, tf_rule = add_card(s9, 0.8, 4.15, 6.0, 2.9, "🎯 Cumplimiento de la Regla de Oro del Proyecto", C_GREEN, C_GREEN)
    p = tf_rule.add_paragraph()
    p.text = "«Primero la matemática, después el programa. El programa no reemplaza la solución analítica: la verifica.»"
    p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = C_GREEN; p.space_after = Pt(4)
    p2 = tf_rule.add_paragraph()
    p2.text = "• Verificación de Superposición:\n" \
              "  Evaluamos la solución exacta deducida a mano y la solución de RK4 en el mismo vector de tiempos.\n" \
              "• Error Absoluto Residual Medido:\n" \
              "  |x_num(t) - x_exacta(t)| < 1.93 × 10^(-10) m.\n" \
              "• Conclusión: Coincidencia matemática absoluta. La simulación comprueba que el desarrollo analítico a mano es 100% exacto."
    p2.font.size = Pt(8.5); p2.font.color.rgb = C_TEXT

    chart_rk4 = "assets/slide_chart_rk4_verification.png"
    if os.path.exists(chart_rk4):
        s9.shapes.add_picture(chart_rk4, Inches(7.1), Inches(1.45), width=Inches(5.4))

    set_notes(s9, (
        "EXPONE LUIS HURTADO (9:30 - 11:00 min):\n"
        "La regla central de la rúbrica dice: 'Primero la matemática, después el programa. El programa no reemplaza la solución analítica: la verifica'.\n"
        "Para simular en Python, convertimos la ecuación de segundo orden en un sistema de primer orden con posición x y velocidad v. "
        "Programamos el método Runge-Kutta de orden 4 (RK4).\n"
        "Como observan en la gráfica de la derecha, la curva numérica de RK4 (azul) y la solución exacta deducida a mano (verde punteada) "
        "se superponen milimétricamente. En la parte inferior medimos el error residual en cada instante de tiempo: es menor a 10^(-10) metros, "
        "lo que demuestra una concordancia matemática perfecta.\n"
        "Ahora le doy paso a Andrés Suaza para presentar las tres aplicaciones reales en videojuegos e interfaces."
    ))

    # =========================================================================
    # SLIDE 10: TRES CASOS REALES EN LA INDUSTRIA
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Los Tres Casos Reales en Videojuegos e Interfaces", "[ 9. CASOS DE APLICACIÓN ]", "Andrés Suaza", "Min 11:00 - 12:15")

    _, tf_c1 = add_card(s10, 0.8, 1.45, 6.0, 1.75, "1. Cámara de Videojuegos (ζ = 1.0 Crítico)", C_GREEN)
    p = tf_c1.add_paragraph()
    p.text = "• Objetivo: Seguir al personaje con la máxima rapidez posible sin marear.\n" \
             "• Justificación de Ingeniería: Si ζ < 1, la cámara rebotaría y oscilaría adelante y atrás provocando mareo visual ('motion sickness'). Con ζ = 1.0 se detiene suavemente sin oscilar."
    p.font.size = Pt(8.5); p.font.color.rgb = C_TEXT

    _, tf_c2 = add_card(s10, 0.8, 3.35, 6.0, 1.75, "2. Menús y Modales Emergentes UI (ζ ≈ 0.5)", C_CYAN)
    p = tf_c2.add_paragraph()
    p.text = "• Objetivo: Aparición de tarjetas, hojas y menús desplegables en interfaces móviles.\n" \
             "• Justificación de Ingeniería: Un sobreimpulso elástico moderado (~16%) genera 'juiciness' y retroalimentación táctil reactiva, simulando plasticidad física (iOS / Material Design)."
    p.font.size = Pt(8.5); p.font.color.rgb = C_TEXT

    _, tf_c3 = add_card(s10, 0.8, 5.25, 6.0, 1.85, "3. Barra de Vida / Daño RPG (ζ ≈ 2.0)", C_ROSE)
    p = tf_c3.add_paragraph()
    p.text = "• Objetivo: Visualización del impacto de daño recibido en el combate de un videojuego.\n" \
             "• Justificación de Ingeniería: El descenso de salud debe ser pesado y definitivo. Si ζ < 1, la barra caería por debajo y rebotaría hacia arriba, simulando falsamente que el jugador curó vida tras recibir un golpe."
    p.font.size = Pt(8.5); p.font.color.rgb = C_TEXT

    chart_three = "assets/slide_chart_three_cases.png"
    if os.path.exists(chart_three):
        s10.shapes.add_picture(chart_three, Inches(7.1), Inches(1.45), width=Inches(5.4))

    set_notes(s10, (
        "EXPONE ANDRÉS SUAZA (11:00 - 12:15 min):\n"
        "Muchas gracias Luis. El punto 3 de la guía nos pide aplicar el resorte a tres casos reales eligiendo y justificando un zeta distinto:\n"
        "1. Para la cámara de un videojuego, elegimos amortiguamiento crítico zeta = 1.0. Debe seguir al personaje con la máxima velocidad "
        "pero sin sobrepasarlo. Si tuviera rebote, el jugador sufriría mareo visual (motion sickness).\n"
        "2. Para un menú o botón emergente, elegimos subamortiguado zeta = 0.5. Al desplegarse la tarjeta en pantalla, hace un pequeño rebote "
        "del 16% que transmite reactividad táctil ('juiciness'), idéntico a las animaciones de iOS.\n"
        "3. Y para una barra de vida de un juego RPG, elegimos sobreamortiguado zeta = 2.0. Cuando te golpean, la barra debe caer con peso. "
        "Si fuera subamortiguada, rebotaría hacia arriba, dando la falsa ilusión óptica de que recuperaste salud."
    ))

    # =========================================================================
    # SLIDE 11: DEMOSTRACIÓN INTERACTIVA EN VIVO
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Demostración Interactiva en Vivo de la Aplicación", "[ 10. DEMO EN VIVO ]", "Andrés Suaza", "Min 12:15 - 13:30")

    _, tf_live = add_card(s11, 0.8, 1.45, 11.7, 1.55, "🎮 Transición a la Aplicación de Escritorio: python main.py", C_YELLOW, C_YELLOW)
    p = tf_live.add_paragraph()
    p.text = "¡Invitamos a la profesora Diana y al público a mover los controles deslizantes en vivo!"
    p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = C_TEXT
    p2 = tf_live.add_paragraph()
    p2.text = "Desarrollamos una suite interactiva completa en Python nativo (Tkinter + Matplotlib) a 60 FPS con física real y gráficas sincronizadas."
    p2.font.size = Pt(9.5); p2.font.color.rgb = C_SUBTEXT

    demos = [
        ("Pestaña 1: Split-Screen", C_CYAN,
         "• Clic en la pista para enviar objetos a la meta.\n"
         "• Muelle helicoidal dinámico, masa y vector velocidad.\n"
         "• Comparación en vivo frente al arrastre de Lerp.\n"
         "• Gráficas temporales y error residual de RK4."),
        ("Pestaña 2: Tres Casos Reales", C_GREEN,
         "• Mini-juego de cámara con avatar controlable y prueba interactiva del 'efecto mareo'.\n"
         "• Menú modal de smartphone con rebote elástico.\n"
         "• Barra de vida RPG con prueba del error visual de rebote."),
        ("Pestaña 3: Fórmulas y Métricas", C_PURPLE,
         "• Calculadora en vivo de raíces y parámetros.\n"
         "• Tiempo de asentamiento t_s y sobreimpulso M_p.\n"
         "• Resumen teórico accesible para responder preguntas.")
    ]
    for i, (tit, col, desc) in enumerate(demos):
        left_pos = 0.8 + i * 4.0
        _, tf_d = add_card(s11, left_pos, 3.2, 3.7, 3.9, tit, col)
        for line in desc.split("\n"):
            p = tf_d.add_paragraph()
            p.text = line
            p.font.size = Pt(9); p.font.color.rgb = C_TEXT
            p.space_after = Pt(3)

    set_notes(s11, (
        "EXPONE ANDRÉS SUAZA (12:15 - 13:30 min):\n"
        "[EN ESTE MOMENTO CAMBIAR A LA VENTANA DE LA APLICACIÓN main.py]\n"
        "'Profesora Diana, para cumplir con el requisito de exposición en vivo, abrimos nuestra aplicación interactiva.'\n"
        "- Muestran la pestaña 1: hacen clic en la pista, mueven omega y zeta, y muestran la diferencia visual entre el resorte con masa "
        "y el objeto de Lerp que se arrastra.\n"
        "- Muestran la pestaña 2: mueven al personaje y activan el modo zeta = 0.25 en la cámara para que todos vean cómo marea la oscilación, "
        "luego abren el menú elástico y golpean al guerrero RPG para ver la barra de vida.\n"
        "- Muestran el gráfico de error residual verificando que la simulación coincide con la matemática exacta."
    ))

    # =========================================================================
    # SLIDE 12: CONCLUSIONES DE INGENIERÍA
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Conclusiones de Ingeniería y Recomendaciones de Diseño", "[ 11. CONCLUSIONES ]", "Andrés Suaza", "Min 13:30 - 14:30")

    conclusions = [
        ("1. Poder del Modelado Físico-Matemático en Software", C_CYAN,
         "• La matemática de ecuaciones diferenciales de segundo orden es la herramienta que permite a los ingenieros controlar con rigor físico la sensación de movimiento (Game Feel).\n"
         "• Las métricas analíticas (frecuencia amortiguada ω_d, sobreimpulso M_p y tiempo de asentamiento t_s) permiten predecir exactamente el comportamiento dinámico sin recurrir a tanteos a ciegas."),
        ("2. No Existe un Amortiguamiento Universal", C_GREEN,
         "• Cada elemento interactivo exige un régimen distinto según su propósito funcional:\n"
         "   - Estabilidad y seguimiento visual => Amortiguamiento Crítico (ζ = 1.0).\n"
         "   - Reactividad táctil y confirmación háptica => Subamortiguado elástico (ζ ≈ 0.5).\n"
         "   - Sensación de impacto, peso y pérdida definitiva => Sobreamortiguado (ζ ≈ 2.0)."),
        ("3. Superioridad del Modelo Físico frente a Fórmulas Simples", C_PURPLE,
         "• Las interpolaciones de primer orden (Lerp) carecen de memoria e inercia, resultando en movimientos robóticos y desaceleraciones asintóticas artificiales.\n"
         "• El oscilador armónico de segundo orden conserva cantidad de movimiento, gestiona transiciones dinámicas continuas ante interrupciones del usuario y transforma código frío en 'Game Feel' vivo.")
    ]
    for i, (tit, col, desc) in enumerate(conclusions):
        top_pos = 1.45 + i * 1.85
        _, tf_con = add_card(s12, 0.8, top_pos, 11.7, 1.7, tit, col)
        for line in desc.split("\n"):
            p = tf_con.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5); p.font.color.rgb = C_TEXT
            p.space_after = Pt(2)

    set_notes(s12, (
        "EXPONE ANDRÉS SUAZA (13:30 - 14:30 min):\n"
        "Para concluir nuestra exposición desde la perspectiva de la ingeniería de software y multimedia:\n"
        "Primero: comprobamos que las ecuaciones diferenciales de segundo orden son la verdadera base matemática del Game Feel. "
        "Calcular el tiempo de asentamiento y el sobreimpulso nos da control cuantitativo exacto.\n"
        "Segundo: no existe un zeta mágico para todo. Una cámara necesita zeta = 1.0 para no marear; un menú necesita zeta = 0.5 "
        "para sentirse vivo; y una barra de vida necesita zeta = 2.0 para sentirse pesada.\n"
        "Tercero: el resorte de segundo orden supera totalmente al Lerp clásico porque almacena momento cinético y permite responder "
        "con suavidad si el usuario interrumpe la animación en pleno vuelo."
    ))

    # =========================================================================
    # SLIDE 13: REFERENCIAS Y TRANSPARENCIA DE IA
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Referencias & Transparencia en el Uso de IA", "[ 12. ÉTICA Y PREGUNTAS ]", "Todos los Integrantes", "Min 14:30 - 15:00")

    _, tf_ref = add_card(s13, 0.8, 1.45, 5.6, 4.3, "📚 Referencias Bibliográficas", C_CYAN)
    refs = [
        ("Edwards, C. H. & Penney, D. E.", "Ecuaciones diferenciales y problemas con valores en la frontera. Cap. 3: Ecuaciones lineales de orden superior."),
        ("Zill, Dennis G.", "Ecuaciones diferenciales con aplicaciones de modelado. Cap. 3: Modelado con ecuaciones de primer orden y Cap. 5: Modelos de orden superior."),
        ("Guía de Proyectos de Aula:", "Ecuaciones Diferenciales - Unidad 3, Institución Universitaria Colegio Mayor del Cauca (Docente: Diana Méndez Astudillo)."),
        ("Apple Developer Documentation:", "CASpringAnimation & UIKit Dynamics Physics Engine."),
        ("Android Developers:", "SpringForce Animation & DynamicAnimation System.")
    ]
    for auth, work in refs:
        p = tf_ref.add_paragraph()
        p.text = f"• {auth} "
        p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = C_TEXT
        run = p.add_run()
        run.text = work
        run.font.bold = False; run.font.color.rgb = C_SUBTEXT
        p.space_after = Pt(4)

    _, tf_ai = add_card(s13, 6.8, 1.45, 5.7, 4.3, "🤖 Declaración de Transparencia de IA (Pág. 11 de la Guía)", C_GREEN)
    p = tf_ai.add_paragraph()
    p.text = "Cumplimiento de la directiva docente:"
    p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = C_GREEN
    p2 = tf_ai.add_paragraph()
    p2.text = "• Herramienta utilizada: Asistente Gemini / Antigravity de Google DeepMind.\n\n" \
              "• Propósito y alcance: Apoyo en el diseño arquitectónico de la interfaz gráfica interactiva en Tkinter/Matplotlib, " \
              "optimización de los algoritmos numéricos RK4 a 60 FPS, redacción estructurada del documento de desarrollo matemático " \
              "y maquetación de diapositivas.\n\n" \
              "• Compromiso y dominio del grupo: Todos los integrantes (Edwin, Cristian, Luis y Andrés) revisaron, verificaron " \
              "numéricamente y comprenden con total solvencia cada fórmula, cada línea de código y cada deducción analítica."
    p2.font.size = Pt(9); p2.font.color.rgb = C_TEXT

    _, tf_qa = add_card(s13, 0.8, 6.0, 11.7, 1.1, border_color=C_YELLOW)
    p = tf_qa.paragraphs[0]
    p.text = "❓ SESIÓN DE PREGUNTAS Y DEFENSA DEL TRABAJO (5 MINUTOS)"
    p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = C_YELLOW; p.alignment = PP_ALIGN.CENTER
    p_sub = tf_qa.add_paragraph()
    p_sub.text = "¡Muchas gracias por su atención! Quedamos atentos a las preguntas de la docente y compañeros."
    p_sub.font.size = Pt(10); p_sub.font.color.rgb = C_TEXT; p_sub.alignment = PP_ALIGN.CENTER

    set_notes(s13, (
        "EXPONEN TODOS LOS INTEGRANTES (14:30 - 15:00 min):\n"
        "Finalmente, como exige la página 11 de la guía, declaramos de manera transparente que utilizamos la asistencia de IA "
        "(Google Antigravity / Gemini) para apoyarnos en la estructuración gráfica y optimización de la aplicación.\n"
        "Todos los miembros del grupo revisamos, verificamos y comprendemos a profundidad cada ecuación y cada línea de código que entregamos hoy.\n"
        "Agradecemos su atención y quedamos listos para responder las preguntas de la profesora Diana y del curso."
    ))

    out_path_1 = "Presentacion_Proyecto_4.pptx"
    out_path_2 = os.path.join("Proyecto_4_Grupo_4", "Presentacion_Proyecto_4.pptx")
    prs.save(out_path_1)
    if os.path.exists("Proyecto_4_Grupo_4"):
        prs.save(out_path_2)

    print("Updated presentation successfully created!")


if __name__ == "__main__":
    build()
