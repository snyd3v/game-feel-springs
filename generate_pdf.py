"""
Generador de Documento PDF Profesional para el Desarrollo Matemático:
Proyecto 4: Resortes para Animar: el «Game Feel»
Ecuaciones Diferenciales - Unidad 3 - Grupo 4
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def build_pdf():
    pdf_path_1 = "Desarrollo_matematico.pdf"
    pdf_path_2 = os.path.join("Proyecto_4_Grupo_4", "Desarrollo_matematico.pdf")

    doc = SimpleDocTemplate(
        pdf_path_1,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_accent = colors.HexColor("#0284C7")     # Sky 600
    c_box_bg = colors.HexColor("#F1F5F9")     # Slate 100
    c_box_border = colors.HexColor("#CBD5E1") # Slate 300

    style_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=3
    )

    style_subtitle = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=c_accent,
        spaceAfter=10
    )

    style_h1 = ParagraphStyle(
        "DocH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        "DocH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    style_formula = ParagraphStyle(
        "DocFormula",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0369A1"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=3
    )

    story = []

    # Encabezado Institucional
    story.append(Paragraph("PROYECTO DE AULA — UNIDAD 3: EDO DE ORDEN SUPERIOR", style_subtitle))
    story.append(Paragraph("Resortes para Animar: el «Game Feel»", style_title))
    story.append(Paragraph("<b>Institución Universitaria Colegio Mayor del Cauca</b> · Facultad de Ingeniería Informática y Multimedia<br/><b>Docente:</b> Ing. Diana Méndez Astudillo · <i>Metodología y Teoría de Clase del 10/11/26</i>", style_body))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=6))

    # Tarjeta de Integrantes
    team_data = [
        [
            Paragraph("<b>Grupo 4 — Integrantes:</b>", style_body),
            Paragraph("• Edwin Esneider Burbano Luna<br/>• Cristian Alexis Chantre Hurtado", style_body),
            Paragraph("• Luis Eduardo Hurtado Hormiga<br/>• Andrés Felipe Suaza Cerón", style_body)
        ]
    ]
    team_table = Table(team_data, colWidths=[1.8 * inch, 2.7 * inch, 2.6 * inch])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_box_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 6))

    # 1. Fundamentación Física y Modelo de Newton
    story.append(Paragraph("1. Fundamentación Física: Del Diagrama de Fuerzas al Modelo de Newton", style_h1))
    story.append(Paragraph(
        "Siguiendo la metodología de clase explicada por la docente en el tablero, consideramos un sistema masa-resorte-amortiguador "
        "con masa m, constante elástica k, constante de amortiguamiento c y posición de destino constante x_f.<br/>"
        "• <b>Fuerza restauradora (Ley de Hooke):</b> F_resorte = -k(x - x_f) (el resorte tira hacia el equilibrio x_f).<br/>"
        "• <b>Fuerza amortiguadora viscosa:</b> F_amortiguador = -c x' (el amortiguador frena proporcional a la velocidad).<br/>"
        "• <b>Segunda Ley de Newton (Inercia):</b> m x'' = Σ F = -c x' - k(x - x_f) ==> <b>m x'' + c x' + k(x - x_f) = 0</b>.<br/>"
        "Dividiendo entre m y aplicando las definiciones de clase: ω = √(k/m) y c/m = 2ζω (con ζ = c / c_cr):",
        style_body
    ))
    story.append(Paragraph("x''(t) + 2ζω x'(t) + ω² (x(t) - x_f) = 0", style_formula))
    story.append(Paragraph(
        "<b>Parámetros de la guía:</b> ω = 8 rad/s, destino x_f = 1 m, con reposo inicial x(0) = 0 m, x'(0) = 0 m/s.",
        style_body
    ))

    # 2. Los Dos Métodos de Solución
    story.append(Paragraph("2. Los Dos Métodos de Solución de Clase: Coeficientes Indeterminados vs Cambio de Variable", style_h1))
    story.append(Paragraph(
        "<b>Método A (Por Coeficientes Indeterminados x = x_h + x_p, visto en clase el 10/11/26):</b><br/>"
        "Reescribiendo la EDO como no homogénea: x'' + 2ζω x' + ω² x = ω² x_f.<br/>"
        "Como el término derecho g(t) = ω² x_f es constante, ensayamos una solución particular constante: x_p(t) = A.<br/>"
        "Derivando: x_p' = 0, x_p'' = 0 ==> 0 + 0 + ω² A = ω² x_f ==> A = x_f ==> <b>x_p(t) = x_f</b>.<br/>"
        "Por lo tanto, la solución general es: <b>x(t) = x_h(t) + x_f</b>.<br/><br/>"
        "<b>Método B (Por Cambio de Variable u = x - x_f, propuesto en la guía del proyecto):</b><br/>"
        "Definiendo el error u(t) = x(t) - x_f, como x_f es constante, u' = x' y u'' = x''.<br/>"
        "La ecuación se convierte en la EDO homogénea: <b>u'' + 2ζω u' + ω² u = 0</b>, con u(0) = -1 y u'(0) = 0.<br/>"
        "<i>Ambos métodos son matemáticamente equivalentes: u(t) es exactamente la solución homogénea x_h(t).</i>",
        style_body
    ))

    # 3. Ecuación Característica y los Tres Regímenes
    story.append(Paragraph("3. Ecuación Característica y Clasificación según el Tablero", style_h1))
    story.append(Paragraph("Proponiendo u(t) = e^(r t), obtenemos el polinomio característico:", style_body))
    story.append(Paragraph("r² + 2ζω r + ω² = 0   ===>   r = -ζω ± ω √(ζ² - 1)", style_formula))
    story.append(Paragraph(
        "El discriminante Δ = 4ω²(ζ² - 1) gobierna los tres regímenes anotados en el tablero de clase:<br/>"
        "1. <b>ζ &lt; 1 (Δ &lt; 0): Subamortiguado.</b> Raíces complejas conjugadas r = -α ± i β. Genera senos y cosenos reales (oscilación y rebote).<br/>"
        "2. <b>ζ = 1 (Δ = 0): Críticamente amortiguado.</b> Raíz real doble r = -ω. Regreso óptimo más rápido sin oscilación.<br/>"
        "3. <b>ζ &gt; 1 (Δ &gt; 0): Sobreamortiguado.</b> Dos raíces reales negativas distintas. Decaimiento lento y pesado sin rebote.",
        style_body
    ))

    # 4. Deducción Analítica para los Tres Casos
    story.append(Paragraph("4. Deducción Analítica para los Tres Valores de ζ (ω = 8, x_f = 1)", style_h1))

    # Caso 1
    story.append(Paragraph("Caso 1: ζ = 0.3 (Subamortiguado — Rebote Físico)", style_h2))
    story.append(Paragraph(
        "α = ζω = 2.4 s⁻¹  |  β = ω √(1 - 0.3²) = 8 √(0.91) ≈ 7.6315 rad/s ==> r = -2.4 ± 7.6315 i.<br/>"
        "u(t) = e^(-2.4 t) [ C1 cos(7.6315 t) + C2 sin(7.6315 t) ].<br/>"
        "Con u(0) = -1 ==> C1 = -1. Derivando y evaluando u'(0) = -2.4 C1 + 7.6315 C2 = 0 ==> C2 ≈ -0.3145.",
        style_body
    ))
    story.append(Paragraph("x(t) = 1 - e^(-2.4 t) [ cos(7.6315 t) + 0.3145 sin(7.6315 t) ]", style_formula))
    story.append(Paragraph(
        "• Sobreimpulso del primer pico: Mp = 100 · exp(-0.3 π / √0.91) ≈ <b>37.23%</b> en t_p = π / 7.6315 ≈ <b>0.4117 s</b>.<br/>"
        "• Tiempo de asentamiento al 2%: t_s ≈ <b>1.63 s</b>.",
        style_body
    ))

    # Caso 2
    story.append(Paragraph("Caso 2: ζ = 1.0 (Amortiguamiento Crítico — Más Rápido sin Rebote)", style_h2))
    story.append(Paragraph(
        "Raíz real doble r = -8. Solución general: u(t) = (C1 + C2 t) e^(-8 t).<br/>"
        "Con u(0) = -1 ==> C1 = -1. Derivando y evaluando u'(0) = C2 - 8 C1 = 0 ==> C2 = -8.",
        style_body
    ))
    story.append(Paragraph("x(t) = 1 - ( 1 + 8 t ) e^(-8 t)", style_formula))
    story.append(Paragraph(
        "• Sobreimpulso: Mp = <b>0%</b>. La función se acerca monótonamente por debajo sin cruzar jamás el destino.<br/>"
        "• Tiempo de asentamiento al 2%: t_s ≈ <b>0.73 s</b> (tiempo récord sin sobreimpulso).",
        style_body
    ))

    # Caso 3
    story.append(Paragraph("Caso 3: ζ = 2.0 (Sobreamortiguado — Pesado y sin Oscilar)", style_h2))
    story.append(Paragraph(
        "Raíces: r = -16 ± 8√3 ==> r1 ≈ -2.1436 s⁻¹, r2 ≈ -29.8564 s⁻¹.<br/>"
        "u(t) = C1 e^(r1 t) + C2 e^(r2 t). Con u(0) = -1 y u'(0) = 0 ==> C1 ≈ -1.07735, C2 ≈ +0.07735.",
        style_body
    ))
    story.append(Paragraph("x(t) = 1 - 1.07735 e^(-2.1436 t) + 0.07735 e^(-29.8564 t)", style_formula))
    story.append(Paragraph(
        "• Sobreimpulso: Mp = <b>0%</b>. Dominado por el polo lento r1: t_s ≈ <b>1.86 s</b> (sensación pesada).",
        style_body
    ))

    chart_regimes = "assets/slide_chart_regimes.png"
    if os.path.exists(chart_regimes):
        story.append(Spacer(1, 3))
        story.append(Image(chart_regimes, width=6.8 * inch, height=3.5 * inch))
        story.append(Paragraph("<i>Figura 1: Respuesta temporal comparando los tres regímenes analíticos con la banda de asentamiento al 2%.</i>", style_body))

    story.append(PageBreak())

    # 5. Demostración de por qué rebota
    story.append(Paragraph("5. Demostración Rigurosa: ¿Por qué ζ < 1 rebota y ζ ≥ 1 no?", style_h1))
    story.append(Paragraph(
        "• <b>Para ζ &lt; 1:</b> Las raíces tienen componente imaginaria no nula (r = -α ± i β). Por la <b>Fórmula de Euler</b> "
        "(e^(i β t) = cos βt + i sin βt), aparecen senos y cosenos reales. La velocidad x'(t) contiene sin(β t), la cual se anula cíclicamente "
        "en t_k = kπ/β. En esos instantes la velocidad cambia de signo; la masa cruza la meta y la fuerza del resorte la regresa, generando oscilación periódica.<br/>"
        "• <b>Para ζ ≥ 1:</b> Las raíces son puramente reales. La solución consiste exclusivamente en sumas de exponenciales monótonas e^(-λ t). "
        "Partiendo del reposo (x(0)=0, x'(0)=0), la velocidad x'(t) es estrictamente positiva para todo t &gt; 0; el objeto avanza siempre hacia adelante "
        "sin cruzar jamás la meta hacia el otro lado. El rebote es físicamente imposible.",
        style_body
    ))

    # 6. Comparación con Lerp
    story.append(Paragraph("6. Resorte (2º Orden) vs Interpolación Lineal Clásica (Lerp 1er Orden)", style_h1))
    story.append(Paragraph(
        "• <b>Lerp (x += (destino - x) * 0.1):</b> Corresponde a la EDO de 1er orden dx/dt = -λ(x - x_f). Carece de masa y aceleración; su velocidad "
        "es proporcional a la distancia restante, frenando de forma asintótica infinitesimal (efecto Zenón) y sin inercia ni rebote.<br/>"
        "• <b>Resorte de 2º Orden:</b> Posee aceleración x'' y almacena energía cinética (E_k = 1/2 m v²). Llega a la meta con velocidad real, "
        "generando elasticidad física orgánica y respuesta continua ante interrupciones.",
        style_body
    ))

    chart_lerp = "assets/slide_chart_lerp_vs_spring.png"
    if os.path.exists(chart_lerp):
        story.append(Image(chart_lerp, width=6.8 * inch, height=3.4 * inch))
        story.append(Paragraph("<i>Figura 2: Resorte dinámico de 2º orden con rebote vs interpolación lineal de 1er orden.</i>", style_body))

    # 7. Criterios de Selección en Videojuegos
    story.append(Paragraph("7. Criterios de Selección de Parámetros en Videojuegos e Interfaces", style_h1))
    table_data = [
        [Paragraph("<b>Elemento</b>", style_body), Paragraph("<b>ζ Elegido</b>", style_body), Paragraph("<b>Justificación de Ingeniería y Game Feel</b>", style_body)],
        [Paragraph("<b>Cámara de Videojuego</b>", style_body), Paragraph("<b>ζ = 1.0</b> (Crítico)", style_body), Paragraph("Seguimiento rápido sin sobreimpulso. Si ζ &lt; 1, la cámara oscilaría adelante y atrás causando mareo visual (<i>motion sickness</i>).", style_body)],
        [Paragraph("<b>Menús y Botones UI</b>", style_body), Paragraph("<b>ζ ≈ 0.5</b> (Subamortiguado)", style_body), Paragraph("Un rebote elástico (~16%) genera 'juiciness' y respuesta táctil reactiva, simulando plasticidad física (iOS / Material Design).", style_body)],
        [Paragraph("<b>Barra de Vida RPG</b>", style_body), Paragraph("<b>ζ ≈ 2.0</b> (Sobreamortiguado)", style_body), Paragraph("Descenso con peso y firmeza. Si rebotara hacia arriba, engañaría al jugador simulando que recuperó vida tras recibir daño.", style_body)]
    ]
    t_criteria = Table(table_data, colWidths=[1.8 * inch, 1.5 * inch, 3.8 * inch])
    t_criteria.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_box_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_box_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_criteria)
    story.append(Spacer(1, 4))

    chart_three = "assets/slide_chart_three_cases.png"
    if os.path.exists(chart_three):
        story.append(Image(chart_three, width=6.8 * inch, height=3.3 * inch))
        story.append(Paragraph("<i>Figura 3: Comportamiento dinámico de los tres casos reales exigidos por la guía.</i>", style_body))

    # 8. Verificación Numérica RK4
    story.append(Paragraph("8. Verificación Numérica mediante Runge-Kutta 4 (RK4)", style_h1))
    story.append(Paragraph(
        "Integramos el sistema de 1er orden Y = [x, v]^T con RK4 evaluando cuatro pendientes k1, k2, k3, k4 con paso h = 0.001 s.<br/>"
        "Al comparar numéricamente frente a la solución analítica exacta deducida a mano, el error absoluto residual es:<br/>"
        "<b>|x_num(t) - x_exacta(t)| &lt; 1.93 × 10^(-10) m</b>.<br/>"
        "Coincidencia matemática perfecta: el programa verifica rigurosamente los resultados analíticos a mano.",
        style_body
    ))

    chart_rk4 = "assets/slide_chart_rk4_verification.png"
    if os.path.exists(chart_rk4):
        story.append(Image(chart_rk4, width=6.8 * inch, height=3.5 * inch))
        story.append(Paragraph("<i>Figura 4: Verificación matemática de precisión con error residual inferior a 10⁻¹⁰ m.</i>", style_body))

    doc.build(story)

    if os.path.exists("Proyecto_4_Grupo_4"):
        import shutil
        shutil.copyfile(pdf_path_1, pdf_path_2)

    print("Updated PDF generated successfully!")


if __name__ == "__main__":
    build_pdf()
