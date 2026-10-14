import os
import sys
import pymupdf

# Color Palette (RGB normalized 0 to 1)
NAVY = (0.05, 0.16, 0.36)       # Primary Brand Header
NAVY_LIGHT = (0.12, 0.32, 0.65) # Accent
BLUE_ACC = (0.12, 0.42, 0.78)   # Bright Blue for links/accents
SLATE = (0.35, 0.42, 0.52)      # Subtitles / Lines
LIGHT_BG = (0.95, 0.97, 1.0)    # Soft blue tint
WHITE = (1.0, 1.0, 1.0)
DARK = (0.1, 0.12, 0.15)        # Text body
GRAY_BORDER = (0.8, 0.84, 0.9)
ROW_ALT = (0.96, 0.98, 1.0)
WARN_BG = (1.0, 0.96, 0.88)
WARN_BORDER = (0.9, 0.55, 0.1)
ALERT_BG = (1.0, 0.92, 0.92)
ALERT_BORDER = (0.85, 0.2, 0.2)
GREEN_ACC = (0.08, 0.48, 0.22)
GREEN_BG = (0.90, 0.97, 0.92)
GREEN_BORDER = (0.15, 0.60, 0.28)
CARD_BG = (0.98, 0.99, 1.0)

def draw_header_footer(page, doc_title, page_num, total_pages):
    rect = page.rect
    page.draw_line((40, 42), (rect.width - 40, 42), color=SLATE, width=0.8)
    page.draw_line((40, rect.height - 38), (rect.width - 40, rect.height - 38), color=SLATE, width=0.8)
    
    # Header: Left text ends well before right text starts
    page.insert_text((40, 35), "CCCD 2026 | I.E. JOSÉ ANTONIO GALÁN", fontsize=7.5, fontname="helv", color=SLATE)
    page.insert_text((340, 35), doc_title[:45], fontsize=7.5, fontname="helv", color=SLATE)
    
    # Footer
    page.insert_text((40, rect.height - 26), "Expediente Técnico de Manufactura y Aerodinámica | Uso Exclusivo Delegación CCCD 2026", fontsize=7, fontname="helv", color=SLATE)
    page.insert_text((rect.width - 85, rect.height - 26), f"Página {page_num} de {total_pages}", fontsize=7.5, fontname="helv", color=SLATE)

def draw_banner(page, y_start, title, subtitle):
    page.draw_rect(pymupdf.Rect(40, y_start, 555, y_start + 42), color=NAVY, fill=NAVY, width=1)
    page.insert_text((55, y_start + 17), title, fontsize=11.5, fontname="helv", color=WHITE)
    page.insert_text((55, y_start + 32), subtitle, fontsize=8.2, fontname="helv", color=(0.85, 0.9, 1.0))
    return y_start + 48

def draw_section_title(page, y, title):
    page.draw_rect(pymupdf.Rect(40, y, 44, y + 14), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page.draw_line((46, y + 14), (555, y + 14), color=GRAY_BORDER, width=0.8)
    page.insert_text((48, y + 11), title, fontsize=9.2, fontname="helv", color=NAVY)
    return y + 18

def draw_callout(page, x, y, w, h, title, text, c_bg, c_border, c_title):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=c_border, fill=c_bg, width=1.0)
    page.insert_text((x + 8, y + 13), title, fontsize=8.2, fontname="helv", color=c_title)
    tb_rect = pymupdf.Rect(x + 8, y + 18, x + w - 8, y + h - 4)
    page.insert_textbox(tb_rect, text, fontsize=7.4, fontname="helv", color=DARK)

def draw_card_with_wa(page, x, y, w, h, title, subtitle, address, pbx_text, wa_number, wa_digits, items, notes=""):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + 16), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    
    page.insert_text((x + 8, y + 11.5), title, fontsize=8.2, fontname="helv", color=WHITE)
    page.insert_text((x + 8, y + 26), subtitle, fontsize=7.2, fontname="helv", color=NAVY_LIGHT)
    page.insert_text((x + 8, y + 36), f"Dirección: {address}", fontsize=7.0, fontname="helv", color=DARK)
    
    # Contact line + WhatsApp Button
    if pbx_text:
        page.insert_text((x + 8, y + 47), f"Contacto: {pbx_text} |", fontsize=7.0, fontname="helv", color=DARK)
        wa_btn_x = x + 8 + len(f"Contacto: {pbx_text} |") * 4.3 + 4
    else:
        page.insert_text((x + 8, y + 47), "Contacto:", fontsize=7.0, fontname="helv", color=DARK)
        wa_btn_x = x + 55
        
    wa_btn_w = 175
    wa_rect = pymupdf.Rect(wa_btn_x, y + 37, wa_btn_x + wa_btn_w, y + 51)
    page.draw_rect(wa_rect, color=GREEN_BORDER, fill=GREEN_BG, width=0.8)
    page.insert_text((wa_btn_x + 5, y + 47), f"Chat WhatsApp: {wa_number}", fontsize=6.8, fontname="helv", color=GREEN_ACC)
    page.insert_link({'kind': pymupdf.LINK_URI, 'from': wa_rect, 'uri': f"https://wa.me/{wa_digits}"})
    
    page.insert_text((x + 8, y + 59), f"Materiales: {items}", fontsize=7.0, fontname="helv", color=DARK)
    if notes:
        page.insert_text((x + 8, y + 70), f"Nota técnica: {notes}", fontsize=6.6, fontname="helv", color=SLATE)

# ==============================================================================
# DOCUMENTO 1: DIRECTORIO DE PROVEEDORES
# ==============================================================================
def build_directorio_pdf(filepath):
    doc = pymupdf.open()
    total_pages = 2
    
    # ---------------- PAGE 1 ----------------
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, "Directorio Técnico de Proveedores - CCCD 2026", 1, total_pages)
    
    y = draw_banner(page1, 50, "DIRECTORIO TÉCNICO DE PROVEEDORES DE MATERIALES E INSUMOS",
                    "Maderas, Fibras Compuestas y Químicos Estructurales | Medellín y Valle de Aburrá Sur")
    
    draw_callout(page1, 40, y, 515, 62,
                 "RESUMEN TÉCNICO DE ESPESORES Y MATERIALES APROBADOS (OCTUBRE 2026):",
                 "• CATEGORÍA 1 (PDA Noctux): Triplex Okume / Pino de 2 mm + refuerzo con Papel Kraft y PVA (Papering). Prohibido composites.\n"
                 "• CATEGORÍA 2 (PDA Stars - Motor F15-4): Triplex Okume / Pino de 3 mm - Madera Sellada con laca/resina pura (sin fibras de tela).\n"
                 "• CATEGORÍA 3 (PDA Rocketeers - Motor G80): Núcleo de Balso o Triplex fino (2 mm a 3 mm) + Pieles de Fibra de Carbono Twill 3K (200 g/m²).",
                 LIGHT_BG, NAVY_LIGHT, NAVY)
    y += 70
    
    y = draw_section_title(page1, y, "1. PROVEEDORES EN EL VALLE DE ABURRÁ SUR (ITAGÜÍ, SABANETA, ENVIGADO)")
    
    # Card 1: La Tienda del Triplex Villa Paula
    draw_card_with_wa(page1, 40, y, 515, 78,
                      "LA TIENDA DEL TRIPLEX — Sede Itagüí (Villa Paula)",
                      "Distribuidor Oficial de Tableros Contrachapados y Laminados",
                      "Calle 47 # 49-35, Villa Paula, Itagüí",
                      "PBX: (604) 448 1844 Ext. 1201",
                      "+57 314 750 1447", "573147501447",
                      "Triplex Okume (2 mm y 3 mm), Triplex de Pino selecto sin nudos. Placas delgadas de alta densidad.",
                      "Solicitar servicio de corte en escuadra para piezas preliminares. Verificar planitud de la lámina.")
    y += 84
    
    # Card 2: La Tienda del Triplex Autopista Sur
    draw_card_with_wa(page1, 40, y, 515, 78,
                      "LA TIENDA DEL TRIPLEX — Bodega Autopista Sur",
                      "Centro de Distribución Mayorista y Transformación de Madera",
                      "Carrera 42 # 46-317, Itagüí (sobre la Autopista Sur)",
                      "PBX: (604) 448 1844 Ext. 1901",
                      "+57 311 362 8901", "573113628901",
                      "Láminas completas de Triplex Okume y Pino estructural (2 mm y 3 mm).",
                      "Ideal para abastecimiento de material bruto para los 3 cohetes de la delegación.")
    y += 84

    # Card 3: Servicomercial Triplex
    draw_card_with_wa(page1, 40, y, 515, 78,
                      "SERVICOMERCIAL TRÍPLEX Y MADERAS",
                      "Distribuidora Industrial de Maderas y Aglomerados de Precisión",
                      "Calle 88 # 47-41 (Sector San Fernando) / Carrera 65 # 35-70, Itagüí",
                      "Tel: (604) 322 7029",
                      "+57 310 411 0531", "573104110531",
                      "Tableros de pino calibrado 3 mm, aglomerados rígidos y triplex para carpintería técnica.",
                      "Excelente opción de respaldo para la madera de 3 mm de Categoría 2.")
    y += 84

    # Card 4: Carbon Fiber Stocks
    draw_card_with_wa(page1, 40, y, 515, 78,
                      "CARBON FIBER STOCKS (CFS) — Sede Sabaneta",
                      "Especialistas en Fibras Compuestas, Telas Técnicas y Resinas Epóxicas",
                      "Sabaneta, Antioquia (Valle de Aburrá Sur) | Despachos locales y asesoría técnica",
                      "IG: @carbonfiberstock",
                      "+57 302 378 5380", "573023785380",
                      "Tela de Fibra de Carbono Twill 3K 2x2 (200 g/m²), cintas unidireccionales, resinas epóxicas de baja viscosidad.",
                      "Proveedor primario para Categoría 3. Asesoran en relaciones de mezcla para infusión y laminado manual.")
    y += 84

    # Card 5: Area Hobbies
    draw_card_with_wa(page1, 40, y, 515, 78,
                      "ÁREA HOBBIES — Mall Plaza Mayorca (Envigado / Sabaneta)",
                      "Tienda Especializada de Modelismo y Suministros para Aeromodelismo",
                      "Carrera 43A # 49D Sur 22, Mall Plaza Mayorca, Envigado",
                      "Suministros RC",
                      "+57 305 227 0009", "573052270009",
                      "Madera balso en láminas calibradas de 2 mm y 3 mm (Balsa de Colombia / KYM RC Models). Densidad uniforme C-grain.",
                      "Material ideal para el núcleo sándwich de aletas Cat 3 y núcleo ligero Cat 1.")

    # ---------------- PAGE 2 ----------------
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, "Directorio Técnico de Proveedores - CCCD 2026", 2, total_pages)
    
    y = 50
    y = draw_section_title(page2, y, "2. PROVEEDORES ESTRATÉGICOS EN MEDELLÍN (CORREDOR INDUSTRIAL GUAYABAL)")
    
    # Card 6: Sumiglas
    draw_card_with_wa(page2, 40, y, 515, 78,
                      "SUMIGLAS S.A.S. — Sede Medellín (Eje Guayabal)",
                      "Mayorista y Minorista de Materias Primas para Materiales Compuestos",
                      "Calle 14 # 51-26 (Contiguo al Centro Empresarial Olaya Herrera, Medellín)",
                      "PBX: (604) 448 9922",
                      "+57 313 684 2173", "573136842173",
                      "Resinas epóxicas de laminación estructural, tejido de fibra de carbono, tela de pelado (Peel-ply), película microperforada.",
                      "Proveedor integral para insumos de vacío: manta absorbedora (breather), cinta de sellado (tacky tape) y cera PVA.")
    y += 84

    # Card 7: HobbyCol
    draw_card_with_wa(page2, 40, y, 515, 78,
                      "HOBBYCOL — Medellín (Guayabal)",
                      "Materiales Estructurales para Aeromodelismo y Radiocontrol",
                      "Calle 25 # 52-96, Medellín (Acceso directo desde el sur por Av. Guayabal)",
                      "Web: hobbycol.com",
                      "+57 318 497 7695", "573184977695",
                      "Láminas seleccionadas de madera balsa 2 mm y 3 mm con veta recta de alta resistencia al cizallamiento.",
                      "Disponen además de cianoacrilato de grado técnico para endurecimiento instantáneo de cantos.")
    y += 84

    # Card 8: S-Hobbies
    draw_card_with_wa(page2, 40, y, 515, 78,
                      "S-HOBBIES AEROMODELISMO — Medellín (Belén)",
                      "Taller y Almacén de Aeromodelismo Estructural",
                      "Calle 31 # 65F-11, Medellín (Belén / Fátima)",
                      "Taller Aeromodelismo",
                      "+57 312 283 3657", "573122833657",
                      "Balso técnico, pegamentos epóxicos bicomponentes de 15 y 30 minutos, y perfiles de refuerzo.",
                      "Surtido constante de láminas delgadas de balso libres de humedad.")
    y += 86

    y = draw_section_title(page2, y, "3. INSUMOS AUXILIARES, QUÍMICOS Y SEGURIDAD INDUSTRIAL")
    
    # Table of Auxiliary Supplies
    page2.draw_rect(pymupdf.Rect(40, y, 555, y + 15), color=NAVY, fill=NAVY, width=0.5)
    page2.insert_text((48, y + 10.5), "INSUMO", fontsize=7.5, fontname="helv", color=WHITE)
    page2.insert_text((150, y + 10.5), "FUNCIÓN EN PROYECTO", fontsize=7.5, fontname="helv", color=WHITE)
    page2.insert_text((345, y + 10.5), "DONDE COMPRAR", fontsize=7.5, fontname="helv", color=WHITE)
    page2.insert_text((465, y + 10.5), "ESPECIFICACIÓN", fontsize=7.5, fontname="helv", color=WHITE)
    y += 16
    
    aux_rows = [
        ("Resina Epóxica", "Matriz del laminado de carbono (Cat 3)", "CFS / Sumiglas", "Baja viscosidad 2:1"),
        ("Peel-Ply (Pelable)", "Drenaje de exceso y textura mate", "Sumiglas / CFS", "Tejido poliéster técnico"),
        ("Película Perforada", "Control de flujo de resina al vacío", "Sumiglas", "Microperforada P3"),
        ("Manta Breather", "Evacuación de aire en bolsa de vacío", "Sumiglas", "Fieltro poliéster 150g"),
        ("Pegamento PVA", "Laminado Kraft (Papering en Cat 1)", "Ferreterías Itagüí", "Colbón Madera profesional"),
        ("Papel Kraft 120g", "Piel exterior para aletas Cat 1", "Papelerías técnicas", "Sin encerar / poroso"),
        ("Lijas de Agua", "Perfilado y acabado aerodinámico", "Ferreterías del Sur", "Granos 120, 240, 400, 600"),
        ("EPP Obligatorio", "Protección contra partículas y vapores", "Ferreterías industriales", "Mascarilla N95 + Nitrilo")
    ]
    
    for item, func, shop, spec in aux_rows:
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + 13), color=GRAY_BORDER, fill=WHITE, width=0.5)
        page2.insert_text((45, y + 9), item, fontsize=7.1, fontname="helv", color=DARK)
        page2.insert_text((150, y + 9), func, fontsize=7.1, fontname="helv", color=DARK)
        page2.insert_text((345, y + 9), shop, fontsize=7.1, fontname="helv", color=DARK)
        page2.insert_text((465, y + 9), spec, fontsize=7.1, fontname="helv", color=SLATE)
        y += 13.5
        
    y += 8
    y = draw_section_title(page2, y, "4. CHECKLIST TÉCNICO DE INSPECCIÓN EN MOSTRADOR")
    
    draw_callout(page2, 40, y, 515, 66,
                 "CRITERIOS DE RECHAZO INMEDIATO AL RECIBIR MATERIALES EN EL ALMACÉN:",
                 "1. Triplex: Colocar la lámina de canto sobre un mesón plano. Si presenta alabeo (warp) mayor a 1 mm, RECHAZARLA.\n"
                 "2. Balso: Verificar que la veta sea recta y paralela. Evitar láminas algodonosas o esponjosas al tacto.\n"
                 "3. Fibra de Carbono: Inspeccionar visualmente que el tejido Twill 3K no tenga hilos jalados ni deformaciones de trama.\n"
                 "4. Resina Epóxica: Exigir formulación para laminado/infusión. NO aceptar resinas densas para artesanías o porcelanato.",
                 ALERT_BG, ALERT_BORDER, (0.7, 0.1, 0.1))

    doc.save(filepath)
    doc.close()
    print(f"Directorio generado y corregido: {filepath}")

# ==============================================================================
# DOCUMENTO 2: PROCEDIMIENTO DE PERFILADO AERODINÁMICO
# ==============================================================================
def build_perfilado_pdf(filepath):
    doc = pymupdf.open()
    total_pages = 2
    
    # ---------------- PAGE 1 ----------------
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, "Procedimiento de Perfilado de Aletas - CCCD 2026", 1, total_pages)
    
    y = draw_banner(page1, 50, "PROCEDIMIENTO TÉCNICO: ELABORACIÓN DE PERFILES AERODINÁMICOS",
                    "Mecanizado de Precisión en Aletas para Reducción de Arrastre y Control de Capa Límite")
    
    draw_callout(page1, 40, y, 515, 54,
                 "FUNDAMENTACIÓN AERODINÁMICA DEL PERFILADO (AIRFOIL SHAPING)",
                 "Una aleta con bordes planos de sección cuadrada presenta un coeficiente de arrastre Cd ≈ 0.82 debido al desprendimiento turbulento masivo en el borde de ataque. El biselado y redondeo aerodinámico reduce el Cd a ≈ 0.18–0.22, disminuyendo las pérdidas por fricción, aumentando el apogeo hasta un 18% y estabilizando la trayectoria en la salida del riel.",
                 LIGHT_BG, NAVY_LIGHT, NAVY)
    y += 62
    
    y = draw_section_title(page1, y, "1. ANATOMÍA Y GEOMETRÍA NOMINAL DEL PERFIL SIMÉTRICO")
    
    anat_text = (
        "• Borde de Ataque (Leading Edge): Radio parabólico continuo (r ≈ t/2). Desvía el flujo de aire suavemente sin vórtices.\n"
        "• Zona Media (Mid-Chord): Espesor nominal constante (2 mm o 3 mm según categoría). Conserva la inercia a flexión.\n"
        "• Borde de Fuga (Trailing Edge): Ahusado en cuña cónica (5° a 8°) comenzando al 35%-40% de la cuerda.\n"
        "• Talón de Seguridad en Fuga: Se debe dejar un espesor residual plano de 0.5 mm. Prohibido afilar a filo de navaja (0 mm),\n"
        "  ya que la madera colapsaría por cizallamiento durante el vuelo o sufriría rotura por impacto en el aterrizaje.\n"
        "• Borde de Raíz (Root): Canto plano a 90° con tolerancia estricta para el anclaje pasante (Through-The-Wall - TTW)."
    )
    page1.insert_textbox(pymupdf.Rect(40, y, 555, y + 60), anat_text, fontsize=7.6, fontname="helv", color=DARK)
    y += 64
    
    y = draw_section_title(page1, y, "2. ESQUEMA TÉCNICO VECTORIAL DEL PERFIL DE VUELO (SECCIÓN TRANSVERSAL)")
    
    # DRAW VECTOR AIRFOIL DIAGRAM
    diag_y = y + 2
    diag_h = 130
    page1.draw_rect(pymupdf.Rect(40, diag_y, 555, diag_y + diag_h), color=GRAY_BORDER, fill=WHITE, width=0.8)
    
    yc = diag_y + 55
    x_le = 90
    x_mid1 = 130
    x_mid2 = 280
    x_te = 460
    t_half = 14
    
    # Centerline
    page1.draw_line((x_le - 20, yc), (x_te + 20, yc), color=(0.85, 0.88, 0.92), width=0.6)
    
    # Top contour
    page1.draw_bezier((x_le, yc), (x_le, yc - t_half * 0.8), (x_mid1 - 20, yc - t_half), (x_mid1, yc - t_half), color=NAVY, width=1.5)
    page1.draw_line((x_mid1, yc - t_half), (x_mid2, yc - t_half), color=NAVY, width=1.5)
    page1.draw_line((x_mid2, yc - t_half), (x_te, yc - 2.5), color=NAVY, width=1.5)
    # Trailing step
    page1.draw_line((x_te, yc - 2.5), (x_te, yc + 2.5), color=NAVY, width=1.5)
    # Bottom contour
    page1.draw_line((x_te, yc + 2.5), (x_mid2, yc + t_half), color=NAVY, width=1.5)
    page1.draw_line((x_mid2, yc + t_half), (x_mid1, yc + t_half), color=NAVY, width=1.5)
    page1.draw_bezier((x_mid1, yc + t_half), (x_mid1 - 20, yc + t_half), (x_le, yc + t_half * 0.8), (x_le, yc), color=NAVY, width=1.5)
    
    # Guide / dimension lines
    page1.draw_line((x_mid1 + 40, yc - t_half), (x_mid1 + 40, yc + t_half), color=BLUE_ACC, width=1.0)
    page1.draw_line((x_mid1 + 35, yc - t_half), (x_mid1 + 45, yc - t_half), color=BLUE_ACC, width=1.0)
    page1.draw_line((x_mid1 + 35, yc + t_half), (x_mid1 + 45, yc + t_half), color=BLUE_ACC, width=1.0)
    page1.draw_line((x_mid2, yc - t_half - 12), (x_mid2, yc + t_half + 12), color=SLATE, width=0.8)
    page1.draw_line((x_te + 15, yc + 25), (x_te + 2, yc + 5), color=ALERT_BORDER, width=1.0)
    
    # Diagram Labels (Positioned without overlap)
    page1.insert_text((x_le - 40, yc - 35), "Borde de Ataque Elíptico / Radio (r = t/2)", fontsize=7.5, fontname="helv", color=BLUE_ACC)
    page1.insert_text((x_mid1 + 10, yc - t_half - 6), "Espesor Nominal (t = 2 mm ó 3 mm)", fontsize=7.5, fontname="helv", color=NAVY)
    page1.insert_text((x_mid2 - 40, yc + t_half + 22), "Línea de Hombro (Comienzo del Ahusado)", fontsize=7.2, fontname="helv", color=SLATE)
    page1.insert_text((x_te - 100, yc - 20), "Bisel Ahusado (5° - 8°)", fontsize=7.2, fontname="helv", color=DARK)
    page1.insert_text((x_te - 15, yc + 35), "Talón Ciego: 0.5 mm Plano", fontsize=7.5, fontname="helv", color=ALERT_BORDER)
    page1.insert_text((55, diag_y + diag_h - 10), "Nota: La simetría bilateral entre la cara superior e inferior es mandatoria para evitar cabeceo o rolido inducido.", fontsize=6.8, fontname="helv", color=SLATE)
    
    y += diag_h + 12
    y = draw_section_title(page1, y, "3. HERRAMIENTAS Y EQUIPOS DE CONTROL DIMENSIONAL")
    
    tools_text = (
        "1. Taco de Lija Rígido: Bloque de aluminio extruido o madera cepillada con lija adherida (evita que la lija copie ondulaciones con los dedos).\n"
        "2. Papeles Abrasivos de Óxido de Aluminio: Grano 120 (desbaste rápido), Grano 240 (conformado de forma) y Grano 400 (alisado final).\n"
        "3. Galga / Plantilla Negativa: Recorte en chapa de aluminio o acrílico con la curva exacta del perfil para contrastar contra luz.\n"
        "4. Calibrador Pie de Rey Digital: Para verificar el espesor de la raíz (t), la simetría y el escalón de fuga (0.5 mm)."
    )
    page1.insert_textbox(pymupdf.Rect(40, y, 555, y + 45), tools_text, fontsize=7.6, fontname="helv", color=DARK)
    
    # ---------------- PAGE 2 ----------------
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, "Procedimiento de Perfilado de Aletas - CCCD 2026", 2, total_pages)
    
    y = 50
    y = draw_section_title(page2, y, "4. MÉTODO DE LAS TRES FACETAS PARA REDONDEO DEL BORDE DE ATAQUE")
    
    f_y = y + 2
    page2.draw_rect(pymupdf.Rect(40, f_y, 515, f_y + 82), color=GRAY_BORDER, fill=WHITE, width=0.8)
    
    # Step 1: Square
    page2.draw_rect(pymupdf.Rect(60, f_y + 24, 110, f_y + 54), color=NAVY, fill=(0.94, 0.96, 1.0), width=1.0)
    # Step 2: 45 degree facet
    page2.draw_line((200, f_y + 34), (210, f_y + 24), color=NAVY, width=1.0)
    page2.draw_line((210, f_y + 24), (250, f_y + 24), color=NAVY, width=1.0)
    page2.draw_line((250, f_y + 24), (250, f_y + 54), color=NAVY, width=1.0)
    page2.draw_line((250, f_y + 54), (210, f_y + 54), color=NAVY, width=1.0)
    page2.draw_line((210, f_y + 54), (200, f_y + 44), color=NAVY, width=1.0)
    page2.draw_line((200, f_y + 44), (200, f_y + 34), color=NAVY, width=1.0)
    # Step 3: Rounded
    page2.draw_bezier((340, f_y + 39), (340, f_y + 27), (352, f_y + 24), (360, f_y + 24), color=NAVY, width=1.0)
    page2.draw_line((360, f_y + 24), (395, f_y + 24), color=NAVY, width=1.0)
    page2.draw_line((395, f_y + 24), (395, f_y + 54), color=NAVY, width=1.0)
    page2.draw_line((395, f_y + 54), (360, f_y + 54), color=NAVY, width=1.0)
    page2.draw_bezier((360, f_y + 54), (352, f_y + 54), (340, f_y + 51), (340, f_y + 39), color=NAVY, width=1.0)
    
    # Step arrows
    page2.draw_line((125, f_y + 39), (185, f_y + 39), color=BLUE_ACC, width=1.2)
    page2.draw_line((180, f_y + 35), (185, f_y + 39), color=BLUE_ACC, width=1.2)
    page2.draw_line((180, f_y + 43), (185, f_y + 39), color=BLUE_ACC, width=1.2)
    page2.draw_line((265, f_y + 39), (325, f_y + 39), color=BLUE_ACC, width=1.2)
    page2.draw_line((320, f_y + 35), (325, f_y + 39), color=BLUE_ACC, width=1.2)
    page2.draw_line((320, f_y + 43), (325, f_y + 39), color=BLUE_ACC, width=1.2)
    
    page2.insert_text((55, f_y + 15), "Paso A: Canto Escuadrado (Bruto)", fontsize=7.2, fontname="helv", color=SLATE)
    page2.insert_text((195, f_y + 15), "Paso B: Chaflán a 45° en Esquinas", fontsize=7.2, fontname="helv", color=SLATE)
    page2.insert_text((335, f_y + 15), "Paso C: Lijado Orbital Continuo", fontsize=7.2, fontname="helv", color=BLUE_ACC)
    page2.insert_text((420, f_y + 33), "Regla Técnica:", fontsize=7.5, fontname="helv", color=NAVY)
    page2.insert_text((420, f_y + 45), "Desbastar primero en facetas", fontsize=7.2, fontname="helv", color=DARK)
    page2.insert_text((420, f_y + 55), "evita crear bordes planos", fontsize=7.2, fontname="helv", color=DARK)
    page2.insert_text((420, f_y + 65), "desiguales o asimétricos.", fontsize=7.2, fontname="helv", color=DARK)
    
    y += 94
    y = draw_section_title(page2, y, "5. PROCEDIMIENTO OPERATIVO PASO A PASO (TALLER)")
    
    steps = [
        ("Paso 1: Trazado de Referencias", "Con lápiz duro 2H y regla metálica, trazar la 'línea de hombro' paralela al borde de fuga (a una distancia equivalente al 35% de la cuerda). En el canto de fuga, marcar la línea central con calibre a t/2."),
        ("Paso 2: Fijación y Desbaste del Borde de Fuga", "Fijar la aleta al borde del banco con prensa suave protegida por cartón. Con taco rígido a 5° y lija 120, desbastar desde la línea de hombro hasta la línea media del canto, deteniéndose estrictamente al alcanzar el espesor de 0.5 mm. Voltear y repetir."),
        ("Paso 3: Mecanizado del Borde de Ataque", "Lijar las dos esquinas a 45° (Paso B del diagrama). Posteriormente, aplicar movimientos semicirculares envolventes de 180° con lija 240 hasta fundir las facetas en un radio elíptico uniforme."),
        ("Paso 4: Control de Calidad Simétrica", "Colocar la galga contra la aleta a contraluz. Si se filtra luz en zonas asimétricas, rectificar con lija 400. Pesar las aletas en gramera digital para asegurar que la variación de masa entre ellas no supere 0.5 gramos."),
        ("Paso 5: Sellado y Rigidización de Bordes", "Aplicar cianoacrilato líquido o una película delgada de resina epóxica pura sobre el borde de fuga y de ataque para endurecer las fibras expuestas de madera antes de pintura o laminado.")
    ]
    
    for title_s, desc_s in steps:
        page2.insert_text((42, y), title_s, fontsize=8, fontname="helv", color=NAVY)
        y += 10
        tb = pymupdf.Rect(42, y, 555, y + 18)
        page2.insert_textbox(tb, desc_s, fontsize=7.3, fontname="helv", color=DARK)
        y += 22

    y += 2
    y = draw_section_title(page2, y, "6. VIDEOTUTORIALES Y RECURSOS TÉCNICOS RECOMENDADOS")
    
    tutorials = [
        ("Apogee Components: 'Mini-Copter 10 - Airfoil the Rocket Fins'", 
         "Muestra la técnica exacta de biselado con taco de madera y redondeo de borde de ataque en aletas de cohetería.",
         "https://www.youtube.com/watch?v=AUZIYQFIQBIrMB1E_51q2f-hVqKQ5kAaRKZ7ofgHEqf4z-slsbSGnsjr6dX9GaW1OttLmt0vtNhmau9lNooPG1JYa4CP0O8rWb8iWvgafmG7wb8teRpHps9dO7lMarG-sR5_f2YE"),
        ("Apogee Components: 'FAI Parachute Duration - 7: Sealing and Airfoiling'",
         "Técnica de aletas de competencia FAI: perfilado fino, verificación con galga y sellado superficial.",
         "https://www.youtube.com/watch?v=AUZIYQHNl8NuCvDy0Qlg6uDYJzkjNMhfczW4e2AnzqewRCc5XAqYImGlUgePmc8ilSuspql2-3F3RTzqTlzPgAmcFS072EBB53n7c2rUFbZjM8QCzES7zduw4XlOkpqRhLvD5OSTRAOAWSM"),
        ("Apogee Components: 'Sealing & Smoothing Balsa Fins'",
         "Guía de preparación del grano de la madera, aplicación de sellador y lijado al agua para acabado de espejo.",
         "https://www.youtube.com/watch?v=AUZIYQHQhma11rFYjZdARqU0Te69x1hzD3_ghnAvhivoOyoIZHKL3mkTJSWLbHGMmaeI5iyfcey_Z6DclTdg0AkETtozSOZji6S76CdvSAY5ChtpoAfpJCo72iauHgcPY7J-UvVH")
    ]
    
    for v_title, v_desc, v_url in tutorials:
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + 26), color=GRAY_BORDER, fill=ROW_ALT, width=0.5)
        link_rect = pymupdf.Rect(40, y, 555, y + 26)
        page2.insert_link({'kind': pymupdf.LINK_URI, 'from': link_rect, 'uri': v_url})
        
        page2.insert_text((48, y + 10), v_title + "  [Ver Video en YouTube ->]", fontsize=7.8, fontname="helv", color=BLUE_ACC)
        page2.insert_text((48, y + 20), v_desc, fontsize=7, fontname="helv", color=SLATE)
        y += 30

    doc.save(filepath)
    doc.close()
    print(f"Manual de Perfilado generado y corregido: {filepath}")

# ==============================================================================
# DOCUMENTO 3: PROCEDIMIENTO DE CHAPEADO CON FIBRA DE CARBONO
# ==============================================================================
def build_chapeado_pdf(filepath):
    doc = pymupdf.open()
    total_pages = 2
    
    # ---------------- PAGE 1 ----------------
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, "Procedimiento de Chapeado con Fibra de Carbono - CCCD 2026", 1, total_pages)
    
    y = draw_banner(page1, 50, "PROCEDIMIENTO TÉCNICO: CHAPEADO Y LAMINADO EN FIBRA DE CARBONO",
                    "Estructura Compuesta en Sándwich y Refuerzo Tip-to-Tip para Aletas de Alta Potencia (Cat 3)")
    
    draw_callout(page1, 40, y, 515, 54,
                 "REGLA CRÍTICA DE FABRICACIÓN EN MATERIALES COMPUESTOS:",
                 "El núcleo de madera de balso o triplex (2 mm o 3 mm) DEBE PERFILARSE AERODINÁMICAMENTE ANTES DE LAMINAR. Si se lamina una placa plana y luego se pretende lijar el perfil aerodinámico, se destruyen las fibras continuas de carbono en los bordes de ataque y fuga, dejando la madera expuesta y cancelando las propiedades mecánicas frente al flutter transónico.",
                 ALERT_BG, ALERT_BORDER, (0.7, 0.1, 0.1))
    y += 62
    
    y = draw_section_title(page1, y, "1. ESPECIFICACIÓN TÉCNICA DE LOS COMPONENTES DEL COMPUESTO")
    
    comp_text = (
        "• Núcleo (Core): Madera de Balso de grado aeromodelismo (2 mm o 3 mm) o Triplex fino. Actúa como separador de cortante,\n"
        "  aumentando el momento de inercia y la rigidez a flexión (I = b*h^3 / 12) con una penalización de peso mínima.\n"
        "• Refuerzo (Pieles): Tela de Fibra de Carbono Twill 3K 2x2 (200 g/m²). El ligamento sarga (Twill) ofrece máxima conformabilidad\n"
        "  bidireccional, adaptándose al bisel cónico y al radio del borde de ataque sin generar pliegues ni deshilacharse.\n"
        "• Matriz (Resina): Resina Epóxica de laminación estructural de baja viscosidad. Prohibida terminantemente la resina de poliéster\n"
        "  (sufre contracción del 8%, mala adherencia a la fibra de carbono y disuelve la hemicelulosa superficial del balso).\n"
        "• Relación de Mezcla: Se busca alcanzar una fracción volumétrica óptima de 60% fibra / 40% resina en peso para máxima ligereza."
    )
    page1.insert_textbox(pymupdf.Rect(40, y, 555, y + 68), comp_text, fontsize=7.6, fontname="helv", color=DARK)
    y += 74
    
    y = draw_section_title(page1, y, "2. PROCEDIMIENTO DE TALLER: PREPARACIÓN E IMPREGNACIÓN")
    
    phases_p1 = [
        ("Fase 1: Pre-Sellado del Núcleo (Evacuación de Porosidad)", 
         "El balso tiene una porosidad celular abierta muy alta. Si se aplica la resina directamente con la tela de carbono seca, el balso absorberá la resina como esponja, dejando la fibra seca ('resin starvation') y acumulando peso muerto. Solución técnica: Aplicar con espátula de goma una película micrónica de resina epóxica pura sobre el núcleo perfilado y dejar curar hasta estado de gel pegajoso (tacky)."),
        ("Fase 2: Corte y Orientación de la Fibra de Carbono (Corte a ±45°)",
         "Para resistir las fuerzas combinadas de torsión y flutter causadas por la aceleración del motor G80, cortar los paños de tela orientando los filamentos a ±45° respecto al borde de ataque. Colocar cinta de carrocero delgada sobre la línea de corte y cortar con tijera para fibras de alto desempeño a través de la cinta para evitar que la trama se deshilache."),
        ("Fase 3: Impregnación Manual Controlada",
         "Colocar el núcleo sobre una superficie limpia con plástico de polietileno. Aplicar resina con técnica de estarcido (punteado con brocha corta) desde el centro hacia afuera. La tela debe verse totalmente translúcida y negra brillante, sin pozos de resina ni zonas blanquecinas secas.")
    ]
    
    for t_ph, d_ph in phases_p1:
        page1.insert_text((42, y), t_ph, fontsize=8, fontname="helv", color=NAVY)
        y += 10
        tb = pymupdf.Rect(42, y, 555, y + 22)
        page1.insert_textbox(tb, d_ph, fontsize=7.3, fontname="helv", color=DARK)
        y += 26

    # ---------------- PAGE 2 ----------------
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, "Procedimiento de Chapeado con Fibra de Carbono - CCCD 2026", 2, total_pages)
    
    y = 50
    y = draw_section_title(page2, y, "3. ESQUEMA TÉCNICO DEL PAQUETE DE COMPACTACIÓN POR VACÍO (VACUUM BAGGING)")
    
    v_y = y + 2
    v_h = 98
    page2.draw_rect(pymupdf.Rect(40, v_y, 555, v_y + v_h), color=GRAY_BORDER, fill=WHITE, width=0.8)
    
    stack_w = 400
    stack_x = 70
    layers = [
        ("Bolsa de Vacío (Vacuum Bag Film 50 micras)", (0.9, 0.95, 1.0), (0.1, 0.3, 0.6), 5),
        ("Manta Respiradora / Absorbente (Breather / Bleeder)", (0.95, 0.95, 0.95), SLATE, 8),
        ("Película Microperforada de Liberación (Release Film)", (0.85, 0.92, 0.85), GREEN_ACC, 4),
        ("Tela de Pelado Técnico (Peel-Ply)", (0.98, 0.92, 0.82), WARN_BORDER, 4),
        ("Piel de Fibra de Carbono Twill 3K Superior", (0.2, 0.2, 0.2), DARK, 4),
        ("NÚCLEO PERFILADO (Balso o Triplex 2-3 mm)", (0.95, 0.88, 0.72), (0.6, 0.4, 0.1), 12),
        ("Piel de Fibra de Carbono Twill 3K Inferior", (0.2, 0.2, 0.2), DARK, 4),
        ("Tela de Pelado Técnico (Peel-Ply)", (0.98, 0.92, 0.82), WARN_BORDER, 4),
        ("Placa Base Rígida Encerada / Vidrio de Soporte", (0.85, 0.9, 0.95), NAVY, 6)
    ]
    
    curr_ly = v_y + 12
    for name, c_fill, c_line, lh in layers:
        page2.draw_rect(pymupdf.Rect(stack_x, curr_ly, stack_x + stack_w, curr_ly + lh), color=c_line, fill=c_fill, width=0.8)
        curr_ly += lh + 1.2
    
    # Tacky tape seals on sides
    page2.draw_rect(pymupdf.Rect(stack_x - 18, v_y + 25, stack_x - 4, v_y + 65), color=WARN_BORDER, fill=(1.0, 0.8, 0.2), width=1.0)
    page2.draw_rect(pymupdf.Rect(stack_x + stack_w + 4, v_y + 25, stack_x + stack_w + 18, v_y + 65), color=WARN_BORDER, fill=(1.0, 0.8, 0.2), width=1.0)
    page2.draw_circle((stack_x + 340, v_y + 8), 6, color=ALERT_BORDER, fill=(1.0, 0.9, 0.9), width=1.2)
    
    # Labels for layers
    page2.insert_text((stack_x + 10, v_y + 10), "Tacky Tape (Sello) <", fontsize=6.8, fontname="helv", color=WARN_BORDER)
    page2.insert_text((stack_x + 355, v_y + 10), "Válvula de Vacío (-0.6 a -0.7 bar)", fontsize=7.2, fontname="helv", color=ALERT_BORDER)
    page2.insert_text((stack_x + 10, v_y + 26), "Manta de Sangrado (Extrae resina excedente)", fontsize=6.8, fontname="helv", color=SLATE)
    page2.insert_text((stack_x + 10, v_y + 44), "Peel-Ply (Deja textura rugosa para adherencia)", fontsize=6.8, fontname="helv", color=DARK)
    page2.insert_text((stack_x + 130, v_y + 60), "NÚCLEO PERFILADO DE BALSO / TRIPLEX", fontsize=7.5, fontname="helv", color=(0.4, 0.25, 0.0))
    page2.insert_text((55, v_y + v_h - 6), "Método Alternativo sin bomba: Prensar entre placas con almohadilla de espuma de EVA / neopreno de 12 mm forrada en polietileno.", fontsize=6.8, fontname="helv", color=SLATE)
    
    y += v_h + 10
    y = draw_section_title(page2, y, "4. CURADO, DESMOLDEO Y RECORTE DE BORDES (FLASHING)")
    
    phases_p2 = [
        ("Fase 4: Consolidación y Curado Térmico",
         "Mantener la presión de vacío continua entre -0.6 y -0.7 bar durante mínimo 8 horas. Dejar curar 24 horas a temperatura ambiente (>22 °C). Si la temperatura nocturna desciende de 20 °C, aplicar calor radiante suave o manta térmica a 35-40 °C para acelerar la polimerización sin deformar el núcleo."),
        ("Fase 5: Desprendimiento del Peel-Ply y Recorte Perimetral",
         "Tirar del Peel-ply en un ángulo cerrado de 180° hacia atrás; este proceso despega limpiamente la manta absorbente con toda la resina sobrante. Para recortar las rebabas duras de carbono de los bordes, usar minitorno (Dremel) con disco de corte de diamante o bloque con lija de metales al agua. Prohibido usar tijeras (se arruinaría el borde de fuga)."),
        ("Fase 6: Montaje Pasante Through-The-Wall (TTW) y Refuerzo Tip-to-Tip (T2T)",
         "Insertar las aletas en las ranuras del fuselaje hasta tocar el tubo motor. Aplicar filetes epóxicos reforzados con microbalones o sílice en la raíz interior y exterior. Finalmente, laminar una capa continua de tela de carbono que abrace la aleta, copie la curva del tubo fuselaje y continúe hacia la aleta adyacente (Tip-to-Tip) para consolidar una estructura monolítica indestructible.")
    ]
    
    for t_ph, d_ph in phases_p2:
        page2.insert_text((42, y), t_ph, fontsize=8, fontname="helv", color=NAVY)
        y += 10
        tb = pymupdf.Rect(42, y, 555, y + 22)
        page2.insert_textbox(tb, d_ph, fontsize=7.3, fontname="helv", color=DARK)
        y += 26

    y += 2
    y = draw_section_title(page2, y, "5. VIDEOTUTORIALES Y RECURSOS DIDÁCTICOS RECOMENDADOS")
    
    tutorials_cf = [
        ("Easy Composites Ltd: 'How to Hand Laminate & Vacuum Bag a Simple Carbon Fibre Part'",
         "Guía técnica exhaustiva de bolsa de vacío: estratificación de peel-ply, manta absorbente, sello hermético y nivel de vacío.",
         "https://www.youtube.com/watch?v=AUZIYQFlb4wlZ84-5B7UfU5INj0qdyC9SWhTU91qEqiFw81HILwkL2HbMM0u4EWFPTc2Z6jBNfdyRwru4Hn2r2xoRYAKoQ13-U0IEc4fUv0GDWPd-JzYAlK7BPJa1Qyx2JVcW-I="),
        ("West System Epoxy: 'Vacuum Bagging Basics: How to Get Started (Complete Guide)'",
         "Fundamentos mecánicos de compactación de composites, control de presión atmosférica y proporciones resina/refuerzo.",
         "https://www.youtube.com/watch?v=AUZIYQGL64SjY6ABWFslXgghEHWYCYzZ_LJK-8HVTtHFwhMwrETcIgX1TSSNoi_i15f4Yl5fmeefxZLyrUUgRzdR1gBjaRez2BOXIMoqqTUD3zgGTl-a6YBEA9Y7heaG6ZY2gmE="),
        ("Making Carbon Fiber Rocket Fins (Amateur Rocketry / BPS.space & High Power)",
         "Tutorial práctico enfocado exclusivamente en manufactura de aletas de cohetería de alta potencia con fibra de carbono y núcleo.",
         "https://www.youtube.com/watch?v=AUZIYQECLhMeaDYVtwc2mIr9Z3y7_pn2o_JSwPd1UT_C0YPFzYw2gtar9_UYEVwT7vg-dtFpHvO0NWubSWr8SV-QHBmZLNuhsCKRymNievcg4HctbJwf27MKZb2g3g6dVCW4YGc=")
    ]
    
    for v_title, v_desc, v_url in tutorials_cf:
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + 26), color=GRAY_BORDER, fill=ROW_ALT, width=0.5)
        link_rect = pymupdf.Rect(40, y, 555, y + 26)
        page2.insert_link({'kind': pymupdf.LINK_URI, 'from': link_rect, 'uri': v_url})
        
        page2.insert_text((48, y + 10), v_title + "  [Ver Video en YouTube ->]", fontsize=7.8, fontname="helv", color=BLUE_ACC)
        page2.insert_text((48, y + 20), v_desc, fontsize=7, fontname="helv", color=SLATE)
        y += 30

    doc.save(filepath)
    doc.close()
    print(f"Manual de Chapeado generado y corregido: {filepath}")

# ==============================================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    out_dir = r"d:\Documentos\IEJAGA\2026\PDA\CCCD2026"
    
    f1 = os.path.join(out_dir, "Directorio_Proveedores_Materiales_CCCD2026.pdf")
    f2 = os.path.join(out_dir, "Procedimiento_Perfilado_Aletas_CCCD2026.pdf")
    f3 = os.path.join(out_dir, "Procedimiento_Chapeado_Fibra_Carbono_CCCD2026.pdf")
    
    build_directorio_pdf(f1)
    build_perfilado_pdf(f2)
    build_chapeado_pdf(f3)
    
    print("\n--- REGENERACIÓN EXITOSA ---")
    print(f"1. {f1}")
    print(f"2. {f2}")
    print(f"3. {f3}")
