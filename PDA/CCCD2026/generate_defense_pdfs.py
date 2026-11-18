import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B365D"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, self.doc_title)
            self.setFont("Helvetica", 8)
            self.drawRightString(letter[0] - 54, 750, self.team_subtitle)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, letter[0] - 54, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "CCCD 2026 | I.E. José Antonio Galán — La Estrella, Antioquia")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_cat2_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    primary_color = colors.HexColor("#1B365D")
    secondary_color = colors.HexColor("#2B547E")
    dark_neutral = colors.HexColor("#1E293B")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    story = []

    # Title & Banner
    story.append(Paragraph("DOSSIER TÉCNICO DE DEFENSA ANTE JURADOS", title_style))
    story.append(Paragraph("CATEGORÍA 2: INTERMEDIOS — VEHÍCULO PDA STARS (ID DE MISIÓN 211)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=8))

    # Context Box
    context_text = """<b>CIRCULAR OFICIAL INMEDIATA:</b> Presentación ante jurados y revisión técnica presencial el viernes 6 de noviembre. 
    <b>Requisitos mandatorios de rampa:</b> 1) Computador con OpenRocket actualizado con masas reales y posición real del CG. 
    2) Marcación física indeleble visible en fuselaje de <b>CP</b> y <b>CG SIN MOTOR</b>. (El CG con motor será auditado por los jueces en campo el día del lanzamiento)."""
    
    callout_data = [[Paragraph(context_text, callout_style)]]
    callout_table = Table(callout_data, colWidths=[letter[0]-108])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # SECTION 1: MARCADAS FÍSICAS Y SIMULACIÓN
    story.append(Paragraph("1. Directriz Operativa: Marcación Física y Parámetros OpenRocket", h1_style))
    
    summary_data = [
        [Paragraph("Parámetro Aerodinámico / Físico", table_header), Paragraph("Valor Oficial PDA Stars", table_header), Paragraph("Criterio Normativo / Inspección", table_header)],
        [Paragraph("Longitud total ensamblado", table_cell_bold), Paragraph("68.5 cm (685 mm)", table_cell), Paragraph("Mínimo 60.0 cm requerido (Cumple)", table_cell)],
        [Paragraph("Diámetro exterior fuselaje (D)", table_cell_bold), Paragraph("6.6 cm (66.0 mm - Kraft BT-80)", table_cell), Paragraph("Calibre de referencia Barrowman", table_cell)],
        [Paragraph("Masa en rampa (con motor F15-4)", table_cell_bold), Paragraph("444.0 g (pesaje real de taller)", table_cell), Paragraph("Máximo 650.0 g (Holgura: 206 g)", table_cell)],
        [Paragraph("Masa sin motor (en seco)", table_cell_bold), Paragraph("341.4 g (descontados 102.6 g motor)", table_cell), Paragraph("Configuración para pesaje previo", table_cell)],
        [Paragraph("MARCA FÍSICA: CP (Centro de Presión)", table_cell_bold), Paragraph("<b>51.4 cm</b> desde vértice ojiva", table_cell), Paragraph("Símbolo diana aerodinámica (⊙)", table_cell)],
        [Paragraph("MARCA FÍSICA: CG SIN MOTOR", table_cell_bold), Paragraph("<b>31.2 cm</b> desde vértice ojiva", table_cell), Paragraph("Símbolo cuadrantes bicolores (⊕)", table_cell)],
        [Paragraph("CG en rampa (con motor F15-4)", table_cell_bold), Paragraph("38.2 cm desde vértice ojiva", table_cell), Paragraph("Auditable en rampa de lanzamiento", table_cell)],
        [Paragraph("CG en fin de combustión (Burnout)", table_cell_bold), Paragraph("37.8 cm (consumidos 60 g grano)", table_cell), Paragraph("Adelantamiento dinámico por masa", table_cell)],
        [Paragraph("Margen Estático en Salida de Riel", table_cell_bold), Paragraph("<b>2.00 calibres</b> (Δx = 13.2 cm)", table_cell), Paragraph("Norma estricta: ≥ 2.00 calibres (Cumple)", table_cell)],
        [Paragraph("Margen Estático al Burnout", table_cell_bold), Paragraph("<b>2.05 calibres</b> (Δx = 13.6 cm)", table_cell), Paragraph("Vuelo propulsado estable", table_cell)],
        [Paragraph("Guía de Lanzamiento (Launch Lugs)", table_cell_bold), Paragraph("Ø interior <b>7.2 mm</b>", table_cell), Paragraph("Para varilla oficial de Ø 6.5 mm x 1.5 m", table_cell)],
        [Paragraph("Relación Empuje/Peso (T/W pico)", table_cell_bold), Paragraph("<b>5.70:1</b> (a_max = 46.13 m/s²)", table_cell), Paragraph("Cumple y supera regla 5:1 (4.7G + 1G)", table_cell)],
        [Paragraph("Apogeo simulado (Stellaris)", table_cell_bold), Paragraph("<b>287.5 m</b> (Meta: 300 m)", table_cell), Paragraph("Precisión aerodinámica 95.8%", table_cell)],
        [Paragraph("Tiempo total de vuelo", table_cell_bold), Paragraph("<b>44.57 s</b>", table_cell), Paragraph("Centro exacto ventana motor F (40-50 s)", table_cell)],
        [Paragraph("Velocidad en varilla (1.5 m)", table_cell_bold), Paragraph("10.84 m/s (39.0 km/h)", table_cell), Paragraph("Salida guiada estable sin cabeceo", table_cell)],
        [Paragraph("Velocidad de llegada a tierra", table_cell_bold), Paragraph("8.14 m/s (Paracaídas Ø 42 cm)", table_cell), Paragraph("Aterrizaje seguro, deriva ≤ 250 m", table_cell)],
    ]
    t1 = Table(summary_data, colWidths=[150, 160, 194])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # SECTION 2: JURADOS DE PROYECTO
    story.append(Paragraph("2. Banco de Preguntas y Respuestas: Jurados de Proyecto", h1_style))
    
    # Georfrey Acevedo
    story.append(Paragraph("Jurado: Georfrey Acevedo (Director Pregrado Ing. Mecatrónica — Universidad EIA)", h2_style))
    q1 = """<b>P1: ¿Por qué emplearon filamento PETG-CF en aletas y cómo garantizan que no fallen por cortante en vuelo?</b><br/>
    <i>R:</i> Empleamos PETG reforzado con fibra de carbono por su rigidez flexural y resistencia térmica (HDT ~80 °C). Para eliminar la concentración de esfuerzos en la unión con el tubo Kraft, las aletas tienen fijación Through-The-Wall (TTW): atraviesan el fuselaje y se adhieren mecánicamente con resina epoxi estructural tanto al tubo portamotor de 29 mm como a los anillos de centrado, formando una viga monolítica integrada."""
    story.append(Paragraph(q1, body_style))

    q2 = """<b>P2: ¿Cómo demuestran que el cohete cumple con la relación empuje-peso de 5:1 con el motor Estes F15-4?</b><br/>
    <i>R:</i> Conforme a la simulación oficial (simulacion_stellaris.csv), la aceleración máxima al despegue alcanza <b>46.13 m/s²</b> (4.70 G netos). Al sumar la gravedad (1 G), la relación empuje-peso instantánea en rampa es: <b>(T/W)_pico = a_max / g + 1 = 4.70 + 1 = 5.70:1</b>, superando holgadamente el criterio de seguridad de 5:1. Además, la velocidad al abandonar la varilla de 1.5 m es de 10.84 m/s (39.0 km/h), asegurando autoridad aerodinámica inmediata de las aletas para evitar el cabeceo por viento cruzado. Reglamentariamente, la Guía de Intermedios establece masa máxima de 650 g (estamos en 444–456 g), reservando la fórmula F_prom/(5*g) para motores Clase G."""
    story.append(Paragraph(q2, body_style))

    # Diego Robledo
    story.append(Paragraph("Jurado: Diego Fernando Robledo (EAFIT / UPB — Arquitecto de Datos y Telemetría)", h2_style))
    q3 = """<b>P3: ¿A qué frecuencia muestrea el sensor BMP280 y cómo evitan la pérdida de datos en la MicroSD?</b><br/>
    <i>R:</i> Muestreamos a 20 Hz (cada 50 ms) vía I2C a 400 kHz con sobremuestreo x4 en presión. Para mitigar la latencia no determinista de escritura de la MicroSD en bus SPI, creamos un buffer circular en la memoria RAM del microcontrolador. Los datos se vacían en bloques cerrados de 512 bytes, evitando llamadas continuas de apertura de archivo en el sistema FAT32."""
    story.append(Paragraph(q3, body_style))

    story.append(Spacer(1, 6))

    # SECTION 3: JURADO CARGA ÚTIL
    story.append(Paragraph("3. Banco de Preguntas y Respuestas: Jurado de Carga Útil", h1_style))
    story.append(Paragraph("Jurado: Daniel Felipe Angarita (UPTC — Física de Radiaciones, CanSat UNAM, Misión ALUNA)", h2_style))
    q4 = """<b>P1: La guía exige masa ≤ 60.0 g, autonomía ≥ 4 h y prohíbe celdas LiPo planas. ¿Cuál es su presupuesto de potencia y masa?</b><br/>
    <i>R:</i> La carga útil pesa exactamente 56.7 g (holgura de 3.3 g). Descartamos celdas 18650 y 9V por su excesiva masa (~45 g, 75% del presupuesto). Usamos un pack de 2 pilas AAA alcalinas en serie (3.0 V, 23.0 g, ~1100 mAh). Con un consumo medido de 42 mA del circuito, la autonomía teórica es de 26.2 horas, y certificamos en banco 6.5 horas de operación continua ininterrumpida."""
    story.append(Paragraph(q4, body_style))

    q5 = """<b>P2: ¿Cómo garantizan la retención estructural sin separación total y la conmutación en rampa?</b><br/>
    <i>R:</i> En cumplimiento de la Sección 5 de la Guía, la bahía tiene un cáncamo estructural en PETG integrado al CAD (resistió 250 N de tracción) anclado permanentemente a la línea principal de Kevlar con eslabón rápido de acero (quick-link). Para la conmutación segura en rampa sin desarmar la ojiva, cuenta con un micro-switch deslizante empotrado en el fuselaje con LED de estado visible exterior."""
    story.append(Paragraph(q5, body_style))

    story.append(Spacer(1, 6))

    # SECTION 4: INSPECCIÓN DE SEGURIDAD
    story.append(Paragraph("4. Auditoría de Seguridad y Aprobación de Vuelo", h1_style))
    story.append(Paragraph("Inspector Oficial: Víctor Marín (Corporación ALAS)", h2_style))
    
    insp_text = """<b>Checklist Mandatorio que auditará el inspector en mesa:</b><br/>
    1. <b>Masa e Integridad:</b> Cohete físico en balanza (444 g ≤ 650 g); Longitud medida con cinta (68.5 cm ≥ 60 cm).<br/>
    2. <b>Launch Lugs Oficiales:</b> Verificación física con varilla de 6.5 mm. El diámetro interior es de 7.2 mm con caída suave por gravedad.<br/>
    3. <b>Marcación Exterior:</b> Inspección visual de marcas indelebles de CP (51.4 cm) y CG sin motor (31.2 cm).<br/>
    4. <b>Retención del Motor F15:</b> Platina mecánica de acero galvanizado con tornillos de sujeción positiva bidireccional.<br/>
    5. <b>Línea de Recuperación:</b> Tren ininterrumpido ojiva-shock cord-bahía-fuselaje. Manta ignífuga Nomex 15x15 cm instalada.<br/>
    6. <b>Tiempo de Vuelo y Deriva:</b> Paracaídas de 42 cm dimensionado para 7.42 m/s, asegurando descenso de 39 s (vuelo total ~46 s, centro de la ventana 40–50 s) y deriva de 185 m ante viento de 5 m/s (radio reglamentario: ≤ 250 m)."""
    story.append(Paragraph(insp_text, body_style))

    # Build PDF
    canvas_maker = NumberedCanvas
    canvas_maker.doc_title = "CCCD 2026 — Dossier de Defensa: Categoría 2 (PDA Stars ID 211)"
    canvas_maker.team_subtitle = "I.E. José Antonio Galán"
    doc.build(story, canvasmaker=canvas_maker)

def build_cat3_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0B2545")
    secondary_color = colors.HexColor("#134074")
    dark_neutral = colors.HexColor("#1E293B")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    story = []

    # Title & Banner
    story.append(Paragraph("DOSSIER TÉCNICO DE DEFENSA ANTE JURADOS", title_style))
    story.append(Paragraph("CATEGORÍA 3: AVANZADOS — VEHÍCULO SIDERAL (ID DE MISIÓN 310)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=8))

    # Context Box
    context_text = """<b>CIRCULAR OFICIAL INMEDIATA:</b> Presentación ante jurados e inspección técnica presencial el viernes 6 de noviembre. 
    <b>Requisitos mandatorios:</b> 1) OpenRocket actualizado en laptop con masas reales y CG exacto. 
    2) Marcación física visible en fuselaje de <b>CP</b> y <b>CG SIN MOTOR</b>. (El CG con motor AeroTech G80T será certificado por Tripoli/ALAS en campo)."""
    
    callout_data = [[Paragraph(context_text, callout_style)]]
    callout_table = Table(callout_data, colWidths=[letter[0]-108])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF4F8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#B0C4DE")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # SECTION 1: MARCADAS FÍSICAS Y SIMULACIÓN
    story.append(Paragraph("1. Directriz Operativa: Marcación Física y Parámetros OpenRocket", h1_style))
    
    summary_data = [
        [Paragraph("Parámetro Aerodinámico / Físico", table_header), Paragraph("Valor Oficial SIDERAL", table_header), Paragraph("Criterio Normativo / Inspección", table_header)],
        [Paragraph("Longitud total armado (L)", table_cell_bold), Paragraph("90.0 cm (900 mm)", table_cell), Paragraph("Mínimo 80.0 cm requerido (Cumple)", table_cell)],
        [Paragraph("Diámetro exterior fuselaje (D)", table_cell_bold), Paragraph("10.2 cm (102.0 mm - 4 pulgadas)", table_cell), Paragraph("Calibre de referencia Barrowman", table_cell)],
        [Paragraph("Masa al despegue (con motor G80T)", table_cell_bold), Paragraph("896.0 g (medición real CDR)", table_cell), Paragraph("Relación 5:1 admite hasta 1580 g (Cumple)", table_cell)],
        [Paragraph("Masa en seco (sin motor G80T)", table_cell_bold), Paragraph("791.0 g (descontados 105.0 g)", table_cell), Paragraph("Configuración para pesaje previo", table_cell)],
        [Paragraph("MARCA FÍSICA: CP (Centro de Presión)", table_cell_bold), Paragraph("<b>68.1 cm</b> desde vértice ojiva", table_cell), Paragraph("Símbolo diana aerodinámica (⊙)", table_cell)],
        [Paragraph("MARCA FÍSICA: CG SIN MOTOR", table_cell_bold), Paragraph("<b>45.0 cm</b> desde vértice ojiva", table_cell), Paragraph("Símbolo cuadrantes bicolores (⊕)", table_cell)],
        [Paragraph("CG en rampa (con motor G80T)", table_cell_bold), Paragraph("49.5 cm desde vértice ojiva", table_cell), Paragraph("Verificado en banco con filo delgado", table_cell)],
        [Paragraph("CG al fin de combustión (Burnout)", table_cell_bold), Paragraph("47.2 cm (consumidos 48 g grano)", table_cell), Paragraph("CP se sitúa en 70.4 cm", table_cell)],
        [Paragraph("Margen Estático en Salida de Riel", table_cell_bold), Paragraph("<b>2.04 calibres</b> (Δx = 18.6 cm)", table_cell), Paragraph("Norma estricta: ≥ 2.00 calibres (Cumple)", table_cell)],
        [Paragraph("Margen Estático al Burnout", table_cell_bold), Paragraph("<b>2.27 calibres</b> (Δx = 23.2 cm)", table_cell), Paragraph("Estabilidad intrínseca en ascenso", table_cell)],
        [Paragraph("Velocidad al salir del riel (1.5 m)", table_cell_bold), Paragraph("<b>61.6 km/h (17.11 m/s)</b>", table_cell), Paragraph("Exigido: > 55.0 km/h (Cumple +12%)", table_cell)],
        [Paragraph("Relación Empuje / Peso (T/W)", table_cell_bold), Paragraph("8.82:1 promedio / 10.7:1 en riel", table_cell), Paragraph("Norma de seguridad: ≥ 5:1 (Cumple holgado)", table_cell)],
        [Paragraph("Apogeo simulado / Altura meta", table_cell_bold), Paragraph("390.9 m (Meta: 400.0 m)", table_cell), Paragraph("Precisión aerodinámica 97.7%", table_cell)],
        [Paragraph("Tiempo al apogeo / Retardo", table_cell_bold), Paragraph("8.70 s (Retardo motor: 7.0 s)", table_cell), Paragraph("Eyección 0.20 s antes del apogeo", table_cell)],
        [Paragraph("Carga Útil CanSat calibrada", table_cell_bold), Paragraph("<b>250.0 g exactos</b>", table_cell), Paragraph("Rango restrictivo: 250.0 a 300.0 g", table_cell)],
        [Paragraph("Descenso terminal / Paracaídas", table_cell_bold), Paragraph("7.18 m/s (Ø 70 cm hemisférico)", table_cell), Paragraph("Deriva 288 m ante viento 5 m/s (≤ 400 m)", table_cell)],
    ]
    t1 = Table(summary_data, colWidths=[150, 160, 194])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # SECTION 2: JURADOS DE PROYECTO
    story.append(Paragraph("2. Banco de Preguntas y Respuestas: Jurados de Proyecto", h1_style))
    
    # Raul Gutierrez
    story.append(Paragraph("Jurado: Cnel. (r) Raúl Gutiérrez (FAC / Octant Aerospace / NSS Colombia)", h2_style))
    q1 = """<b>P1: Explíqueme los márgenes de seguridad en la salida del riel y la estabilidad aeroelástica del SIDERAL.</b><br/>
    <i>R:</i> Mi Coronel, el cohete sale del riel de 1.5 m a 17.11 m/s (61.6 km/h), superando en un 12% los 55 km/h normativos para neutralizar el weathercocking. En ese instante, el margen estático es de 2.04 calibres (Δx = 18.6 cm), cumpliendo la norma estricta ≥ 2.0 calibres. La relación empuje-peso inicial de 10.7:1 (frente al umbral de 5:1) garantiza un vuelo directriz sin cabeceo transitorio."""
    story.append(Paragraph(q1, body_style))

    q2 = """<b>P2: ¿Cuál es el protocolo de seguridad ante una falla de ignición o CATO?</b><br/>
    <i>R:</i> Operamos bajo estándar Tripoli/ALAS: ante falla de ignición rige un tiempo de espera de 60 segundos antes del despeje. En caso de CATO, se activa el perímetro de exclusión de 20 m. El tubo de fibra de vidrio de 29 mm y los anillos de tríplex de 3 mm aíslan la presión radial. Tras inspección del RSO, si la bahía superior y el CanSat están intactos y la estabilidad se preserva, podemos solicitar un segundo vuelo oficial disponiendo de motor de repuesto."""
    story.append(Paragraph(q2, body_style))

    # Luis Lema
    story.append(Paragraph("Jurado: Luis Lema (AVIANCA — Director de Gestión y Proyectos de Mantenimiento, MRO Rionegro)", h2_style))
    q3 = """<b>P3: En MRO auditamos tolerancias e interfaces de desacople. ¿Cómo garantizan la separación sin atascamientos ni holguras?</b><br/>
    <i>R:</i> Ingeniero, el acoplador de ASA tiene una penetración de 105 mm (1.03 calibres) en el fuselaje móvil inferior, superando el requisito DCP 3.2.7 (≥ 1.0 calibre = 102 mm). Hacia el tubo superior la unión es fija y rígida: cuatro tornillos avellanados M3 fijados a insertos moleteados de latón (heat-set inserts) termosellados en el acoplador, soportando cortante y dejando el interior liso para proteger los arneses."""
    story.append(Paragraph(q3, body_style))

    # Daniela Suarez
    story.append(Paragraph("Jurado: Daniela Suárez Cárdenas (ASTCOL — Ingeniera Química, Comandante Misión ALUNA)", h2_style))
    q4 = """<b>P4: ¿Por qué la ojiva es en filamento ASA y no en fibra de carbono? ¿Cuál es la carga biológica secundaria?</b><br/>
    <i>R:</i> Ingeniera, el ASA posee un HDT de ~100 °C y tenacidad al impacto, pero la causa crítica es de telecomunicaciones: el PETG-CF genera un apantallamiento de jaula de Faraday sobre las antenas LoRa (915 MHz) y GPS u-blox alojadas en la proa; el ASA es 100% permeable a RF. La misión biológica secundaria porta 7.5 g de semillas nativas de La Estrella en cápsulas hidrófilas para evaluar el efecto de una aceleración de 10.5 G sobre la tasa de germinación."""
    story.append(Paragraph(q4, body_style))

    story.append(Spacer(1, 6))

    # SECTION 3: JURADOS DE CARGA ÚTIL
    story.append(Paragraph("3. Banco de Preguntas y Respuestas: Jurados de Carga Útil", h1_style))
    story.append(Paragraph("Jurados: Raúl Joya & Iván Luna (Satélite Libertad 1, Sequoia Space, MinCiencias)", h2_style))
    q5 = """<b>P1: En sistemas espaciales masa y EPS son sagrados. ¿Cómo resolvieron la masa del CanSat, la batería y el enlace LoRa?</b><br/>
    <i>R:</i> Ingenieros, calibramos el CanSat en 250.0 g exactos (límite inferior restrictivo de la norma 250–300 g). En potencia descartamos LiPo e implementamos 3 celdas Ni-MH cilíndricas en serie (3.6 V, 2200 mAh, 88.5 g) con regulador DC-DC a 5.0 V y filtrado capacitivo pi para suprimir rizado. La Heltec ESP32-S3 transmite paquetes de telemetría en 915 MHz a +14 dBm con el indicativo táctico oficial PDA310-SAT hacia la estación terrena."""
    story.append(Paragraph(q5, body_style))

    q6 = """<b>P2: ¿Cómo garantizan que la vibración o choque de 10.5 G no desactive la electrónica?</b><br/>
    <i>R:</i> Suprimimos los conmutadores mecánicos estándar que sufren micro-cortes por inercia bajo 10 G. Instalamos un conector jack 3.5 mm configurado como pin 'Remove Before Flight' (RBF). El pin se retira físicamente 2 minutos antes del lanzamiento, cerrando el circuito de forma limpia y permanente con confirmación sonora y telemetría de rampa."""
    story.append(Paragraph(q6, body_style))

    story.append(Spacer(1, 6))

    # SECTION 4: INSPECCIÓN DE SEGURIDAD
    story.append(Paragraph("4. Auditoría de Seguridad y Aprobación de Vuelo", h1_style))
    story.append(Paragraph("Inspector Oficial: Juan Sebastián Fonseca (Secretario de Trípoli Rocketry Association)", h2_style))
    
    insp_text = """<b>Puntos Técnicos Invariables auditados por Tripoli:</b><br/>
    1. <b>Margen Estático Obligatorio:</b> 2.04 calibres medidos en rampa con motor (CP: 68.1 cm, CG: 49.5 cm, D: 10.2 cm). Marcación física de CP y CG sin motor (45.0 cm) rotulada en fuselaje.<br/>
    2. <b>Velocidad de Riel y Empuje/Peso:</b> 61.6 km/h al salir del riel de 1.5 m (> 55 km/h). Relación T/W de 10.7:1 pico / 8.82:1 promedio (supera umbral 5:1).<br/>
    3. <b>Penetración de Acoplador (DCP 3.2.7):</b> Acoplador ASA inserta 105 mm en tubo inferior (1.03 calibres ≥ 1.0 calibre requerido).<br/>
    4. <b>Retención Mecánica de Motor (DCP 3.2.9):</b> Tapa roscada de retención mecánica en tubo portamotor de fibra de vidrio.<br/>
    5. <b>Línea de Recuperación:</b> Cordón de Kevlar plano de 3.40 m útiles (3.78x longitud total, supera norma ≥ 2x). Manta Nomex 15x15 cm y funda ignífuga tubular. Paracaídas Ø 70 cm con descenso de 7.18 m/s (deriva de 288 m ante viento de 5 m/s, dentro del perímetro legal de 400 m).<br/>
    6. <b>Orificio Barométrico:</b> Orificio estático de Ø 2.5 mm a 90° de los botones de riel para el altímetro oficial Jolly Logic."""
    story.append(Paragraph(insp_text, body_style))

    # Build PDF
    canvas_maker = NumberedCanvas
    canvas_maker.doc_title = "CCCD 2026 — Dossier de Defensa: Categoría 3 (PDA Rocketeers ID 310)"
    canvas_maker.team_subtitle = "I.E. José Antonio Galán"
    doc.build(story, canvasmaker=canvas_maker)

if __name__ == '__main__':
    cat2_out = os.path.abspath('Categoria_2_PDA_Stars/Defensa_Jurados_e_Inspeccion_Cat2_PDAStars.pdf')
    cat3_out = os.path.abspath('Categoria_3_PDA_Rocketeers/Defensa_Jurados_e_Inspeccion_Cat3_PDARocketeers.pdf')
    
    print('Generando PDF Cat 2...')
    build_cat2_pdf(cat2_out)
    print('PDF Cat 2 generado exitosamente en:', cat2_out)
    
    print('Generando PDF Cat 3...')
    build_cat3_pdf(cat3_out)
    print('PDF Cat 3 generado exitosamente en:', cat3_out)

