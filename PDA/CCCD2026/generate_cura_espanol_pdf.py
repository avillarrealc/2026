import os
import sys
import pymupdf

# Paleta de Colores Técnicos (RGB normalizados 0 a 1)
NAVY = (0.05, 0.16, 0.36)        # Azul oscuro institucional
NAVY_LIGHT = (0.12, 0.32, 0.65)  # Azul medio acento
BLUE_ACC = (0.12, 0.42, 0.78)    # Azul vivo
SLATE = (0.35, 0.42, 0.52)       # Gris azulado para bordes y subtítulos
LIGHT_BG = (0.95, 0.97, 1.0)     # Fondo azul muy tenue
WHITE = (1.0, 1.0, 1.0)
DARK = (0.10, 0.12, 0.16)        # Texto principal muy oscuro y nítido
GRAY_BORDER = (0.80, 0.84, 0.90)
ROW_ALT = (0.96, 0.98, 1.0)
GREEN_ACC = (0.08, 0.48, 0.22)
CARD_BG = (0.98, 0.99, 1.0)

def draw_header_footer(page, page_num, total_pages, title_sub):
    rect = page.rect
    page.draw_line((40, 36), (rect.width - 40, 36), color=SLATE, width=0.8)
    page.draw_line((40, rect.height - 34), (rect.width - 40, rect.height - 34), color=SLATE, width=0.8)
    
    # Encabezado
    page.insert_text((40, 30), "CCCD 2026 | I.E. JOSÉ ANTONIO GALÁN", fontsize=8.0, fontname="helv", color=SLATE)
    page.insert_text((275, 30), title_sub, fontsize=8.0, fontname="helv", color=SLATE)
    
    # Pie de página
    page.insert_text((40, rect.height - 22), "Semillero PDA Rocketeers - Categoría 3 | Guía de Laminación para Cura 4.13 (Español)", fontsize=7.2, fontname="helv", color=SLATE)
    page.insert_text((rect.width - 95, rect.height - 22), f"Página {page_num} de {total_pages}", fontsize=7.5, fontname="helv", color=SLATE)

def draw_banner(page, y_start, title, subtitle):
    page.draw_rect(pymupdf.Rect(40, y_start, 555, y_start + 40), color=NAVY, fill=NAVY, width=1)
    page.insert_text((52, y_start + 17), title, fontsize=11.5, fontname="helv", color=WHITE)
    page.insert_text((52, y_start + 31), subtitle, fontsize=8.0, fontname="helv", color=(0.85, 0.92, 1.0))
    return y_start + 46

def draw_section_header(page, y, title):
    page.draw_rect(pymupdf.Rect(40, y, 555, y + 15), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page.insert_text((48, y + 11), title, fontsize=8.5, fontname="helv", color=WHITE)
    return y + 19

def safe_textbox(page, rect, text, fontsize, fontname="helv", color=DARK):
    rc = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname, color=color)
    if rc < 0:
        print(f"ADVERTENCIA: Desborde de texto en caja {rect}: faltaron {-rc:.1f} pt. Texto: {text[:30]}...")
    return rc

def draw_info_card(page, x, y, w, h, title, text, tag_color=BLUE_ACC):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page.draw_rect(pymupdf.Rect(x, y, x + 4, y + h), color=tag_color, fill=tag_color, width=0.5)
    page.insert_text((x + 12, y + 13), title, fontsize=8.2, fontname="helv", color=NAVY)
    tb_rect = pymupdf.Rect(x + 12, y + 18, x + w - 10, y + h - 4)
    safe_textbox(page, tb_rect, text, fontsize=7.2, color=DARK)

def draw_table_cura(page, y, rows):
    # Header tabla
    th_h = 16
    page.draw_rect(pymupdf.Rect(40, y, 555, y + th_h), color=NAVY, fill=NAVY, width=0.5)
    page.insert_text((46, y + 11.5), "Categoría / Ajuste en Cura (Español)", fontsize=7.8, fontname="helv", color=WHITE)
    page.insert_text((230, y + 11.5), "Valor Exacto a Digitar", fontsize=7.8, fontname="helv", color=WHITE)
    page.insert_text((375, y + 11.5), "Propósito Técnico para el Cohete", fontsize=7.8, fontname="helv", color=WHITE)
    y += th_h
    
    row_h = 14.0
    for i, (cat, campo, val, prop) in enumerate(rows):
        bg = ROW_ALT if i % 2 == 1 else WHITE
        page.draw_rect(pymupdf.Rect(40, y, 555, y + row_h), color=GRAY_BORDER, fill=bg, width=0.5)
        page.insert_text((46, y + 10.0), f"{cat}: {campo}", fontsize=6.8, fontname="helv", color=NAVY)
        page.insert_text((230, y + 10.0), val, fontsize=6.8, fontname="helv", color=DARK)
        page.insert_text((375, y + 10.0), prop, fontsize=6.7, fontname="helv", color=SLATE)
        y += row_h
    return y

def build_pdf(output_path):
    doc = pymupdf.open()
    total_pages = 2
    
    # ==============================================================================
    # PÁGINA 1: ACOPLE SIDERAL 4 (CON ASA DE PARACAÍDAS)
    # ==============================================================================
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, 1, total_pages, "Cura 4.13 (Español) - Acople SIDERAL 4")
    
    y = draw_banner(page1, 44, "GUÍA CURA 4.13 (ESPAÑOL): ACOPLE SIDERAL 4 (CON ASA)",
                    "Parámetros con nombres exactos en español para Ultimaker Cura 4.13.2 | Impresora Sunlu T3 (ASA)")
    
    # Ficha del Acople
    fich_h = 68
    page1.draw_rect(pymupdf.Rect(40, y, 555, y + fich_h), color=NAVY_LIGHT, fill=LIGHT_BG, width=0.8)
    page1.insert_text((50, y + 13), "DATOS DE LA PIEZA: Acople SIDERAL 4.stl", fontsize=8.8, fontname="helv", color=NAVY)
    
    col1 = (
        "- Material: ASA (Acrilonitrilo Estireno Acrilato)\n"
        "- Boquilla instalada (Nozzle): 0.40 mm (Extrusor 1)\n"
        "- Altura total Z: 136.00 mm | Diámetro exterior: 99.00 mm\n"
        "- Anillo de tope exterior: 102.00 mm (Z de 30 a 42 mm)"
    )
    col2 = (
        "- Asa de anclaje: Perno cilíndrico de 8.0 mm a 45 grados\n"
        "- Empotramiento del asa: En pared vertical y piso horizontal\n"
        "- Función: Soporte del cordón de choque y paracaídas (12-15 Gs)\n"
        "- Posición en cama: Base cilíndrica abajo, asa en la parte alta"
    )
    safe_textbox(page1, pymupdf.Rect(50, y + 18, 290, y + fich_h - 2), col1, fontsize=7.2, color=DARK)
    safe_textbox(page1, pymupdf.Rect(300, y + 18, 545, y + fich_h - 2), col2, fontsize=7.2, color=DARK)
    y += fich_h + 8
    
    # Nota clave de Cura 4.13
    draw_info_card(page1, 40, y, 515, 54,
                   "CÓMO DESPLEGAR TODOS LOS AJUSTES EN CURA 4.13:",
                   "En la barra superior de ajustes, haz clic en las tres rayas horizontales al lado del buscador y selecciona 'Todos' (All). "
                   "Para 'Wall Ordering: Inside to Outside', en Cura 4.13 la casilla se llama 'Paredes exteriores antes que interiores' "
                   "y debe dejarse DESMARCADA (sin check) para que imprima primero los perímetros interiores.",
                   NAVY_LIGHT)
    y += 60
    
    # Tabla de Ajustes Acople
    y = draw_section_header(page1, y, "TABLA DE PARÁMETROS EN CURA (ESPAÑOL) — ACOPLE CON ASA")
    
    rows_acople = [
        ("Calidad", "Altura de capa", "0.16 mm", "Garantiza unión íntima y tenacidad en el asa a 45°"),
        ("Calidad", "Altura de capa inicial", "0.24 mm", "Aplastamiento reforzado para que el borde no despegue"),
        ("Calidad", "Ancho de línea de capa inicial", "120 %", "Mayor cordón en base para máxima fijación a la cama"),
        ("Paredes", "Recuento de líneas de pared", "5 líneas", "Convierte el asa de 8 mm en una barra 100% maciza"),
        ("Paredes", "Paredes exteriores antes que interiores", "Desmarcado (Sin check)", "Imprime de adentro hacia afuera; ancla el asa al núcleo"),
        ("Paredes", "Alternar pared adicional", "Marcado (Con check)", "Añade un perímetro alterno que amarra paredes al relleno"),
        ("Paredes", "Rellenar huecos entre paredes", "En todas partes", "Elimina cualquier micro-poro o fisura interna en el tubo"),
        ("Paredes", "Imprimir paredes finas", "Marcado (Con check)", "Asegura el copiado de bordes de 1.2 mm sin vacíos"),
        ("Capas", "Capas superiores / Capas inferiores", "6 superiores / 5 inferiores", "Piso de 1 mm macizo para que el asa no desgarre el mamparo"),
        ("Relleno", "Densidad / Patrón de relleno", "45 % a 50 % | Giroide", "Resistencia tridimensional sin crear bloque térmico pesado"),
        ("Material", "Temperatura de impresión", "245 °C a 250 °C (240 °C mín)", "Fusión molecular en el asa ante el tirón de recuperación"),
        ("Material", "Temperatura de placa de impresión", "100 °C continuo", "Supera la transición vítrea del ASA evitando despegues"),
        ("Velocidad", "Velocidad de impresión / Pared", "45 mm/s / 25 mm/s", "Velocidad moderada para garantizar tiempo de fusión"),
        ("Velocidad", "Velocidad de capa inicial", "20 mm/s", "Lentitud controlada para anclaje perfecto de primera capa"),
        ("Desplazamiento", "Habilitar retracción / Distancia", "Marcado / 5.0 mm a 40 mm/s", "Calibrado exacto para el extrusor Bowden de la Sunlu T3"),
        ("Desplazamiento", "Salto en Z al retraer / Altura", "Marcado / 0.20 mm", "Evita que la boquilla tropiece con el asa inclinada"),
        ("Refrigeración", "Habilitar refrigeración / Velocidad", "Marcado / 10 % a 15 % máx", "Enfriamiento casi nulo para que el ASA no se raje"),
        ("Refrigeración", "Velocidad regular en altura", "0.80 mm", "Permite que las primeras 4 capas fundan sin viento"),
        ("Soporte", "Generar soporte / Colocación", "Marcado / Tocando placa", "Soporta el anillo de 102 mm y el vientre inferior del asa"),
        ("Soporte", "Distancia Z del soporte", "0.20 mm a 0.22 mm", "Permite retirar el soporte del asa limpio sin romperlo"),
        ("Adherencia", "Tipo de adherencia / Ancho", "Borde (Brim) / 10.0 mm", "Fijación perimétrica obligatoria contra palanca"),
        ("Adherencia", "Borde solo en el exterior", "Desmarcado (Sin check)", "Genera borde por fuera Y por el agujero interior del cilindro")
    ]
    
    y = draw_table_cura(page1, y, rows_acople)
    y += 8
    
    # Card de advertencia del asa al final
    draw_info_card(page1, 40, y, 515, 58,
                   "REGLA DE TALLER: DESMOLDE DEL ASA DE ANCLAJE:",
                   "Al retirar el material de soporte debajo del asa, utilice pinzas de punta fina o bisturí con cuidado. "
                   "No use alicates de corte que muerdan o rayen el cuerpo cilíndrico del asa. Cualquier incisión en el plástico "
                   "se convertirá en un concentrador de esfuerzos que podría quebrar el asa bajo el impacto del paracaídas.",
                   GREEN_ACC)
    
    # ==============================================================================
    # PÁGINA 2: OJIVA 102 mm + PROTOCOLO DE IMPRESIÓN SUNLU T3
    # ==============================================================================
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, 2, total_pages, "Cura 4.13 (Español) - Ojiva 102 mm")
    
    y = draw_banner(page2, 44, "GUÍA CURA 4.13 (ESPAÑOL): OJIVA 102 mm AERODINÁMICA",
                    "Parámetros con nombres exactos en español para Ultimaker Cura 4.13.2 | Impresora Sunlu T3 (ASA)")
    
    # Ficha de la Ojiva
    fich_h = 68
    page2.draw_rect(pymupdf.Rect(40, y, 555, y + fich_h), color=NAVY_LIGHT, fill=LIGHT_BG, width=0.8)
    page2.insert_text((50, y + 13), "DATOS DE LA PIEZA: 2026-10-20 Ojiva 102 mm punta ok.stl", fontsize=8.8, fontname="helv", color=NAVY)
    
    col1_oj = (
        "- Material: ASA (Acrilonitrilo Estireno Acrilato)\n"
        "- Boquilla: 0.40 mm | Altura total Z: 225.45 mm\n"
        "- Diámetro exterior máximo: 102.00 mm\n"
        "- Diámetro hombro inferior: 99.00 mm (Z de 0 a 44 mm)"
    )
    col2_oj = (
        "- Espesor de cáscara: 1.20 mm en cono (100% perimetral)\n"
        "- Escalón exterior: 1.50 mm plano a 90 grados a Z = 45 mm\n"
        "- Cavidad interior: Cónica auto-portante (sin soporte adentro)\n"
        "- Orientación en cama: Base abajo, punta hacia arriba"
    )
    safe_textbox(page2, pymupdf.Rect(50, y + 18, 290, y + fich_h - 2), col1_oj, fontsize=7.2, color=DARK)
    safe_textbox(page2, pymupdf.Rect(300, y + 18, 545, y + fich_h - 2), col2_oj, fontsize=7.2, color=DARK)
    y += fich_h + 8
    
    # Tabla de Ajustes Ojiva
    y = draw_section_header(page2, y, "TABLA DE PARÁMETROS EN CURA (ESPAÑOL) — OJIVA 102 mm")
    
    rows_ojiva = [
        ("Calidad", "Altura de capa", "0.16 mm", "Acabado superficial liso en la ojiva y resistencia axial"),
        ("Calidad", "Altura de capa inicial", "0.24 mm", "Fijación reforzada del hombro inferior contra la cama"),
        ("Calidad", "Ancho de línea de capa inicial", "120 %", "Máximo sellado perimétrico de la primera capa"),
        ("Paredes", "Recuento de líneas de pared", "4 líneas (ancho 0.45)", "La pared de 1.2 mm se hace 100% sólida concéntrica"),
        ("Paredes", "Paredes exteriores antes que interiores", "Desmarcado (Sin check)", "Asegura fidelidad dimensional exterior y buena unión"),
        ("Paredes", "Alineación de la costura en Z", "Alineada o Atrás", "Costura en línea recta vertical; NUNCA aleatoria"),
        ("Paredes", "Preferencia de costura en Z", "Ocultar costura", "Ubica la costura en el cuadrante trasero para facilitar pulido"),
        ("Paredes", "Rellenar huecos entre paredes", "En todas partes", "Garantiza hermeticidad y cero poros en la cáscara"),
        ("Relleno", "Densidad / Patrón de relleno", "40 % a 50 % | Giroide", "Actúa en la punta maciza (Z > 200 mm) sin crear bloque pesado"),
        ("Material", "Temperatura de impresión", "245 °C a 250 °C", "Fusión estructural para soportar presión aerodinámica"),
        ("Material", "Temperatura de placa de impresión", "100 °C continuo", "Previene levantamiento de la base por contracción"),
        ("Velocidad", "Velocidad de impresión / Pared", "45 mm/s / 25 mm/s", "Garantiza precisión y redondez en los 102 mm de diámetro"),
        ("Desplazamiento", "Habilitar retracción / Distancia", "Marcado / 5.0 mm a 40 mm/s", "Configuración estándar para bowden de Sunlu T3"),
        ("Desplazamiento", "Salto en Z al retraer", "Marcado / 0.20 mm", "Evita cicatrices o golpes en la superficie del cono"),
        ("Refrigeración", "Velocidad del ventilador", "0 % a 10 % (30 % escalón)", "Casi apagado; solo sube al 30% en el puente del escalón exterior"),
        ("Soporte", "Generar soporte / Colocación", "Marcado / Tocando placa", "Soporta únicamente el escalón exterior de 1.5 mm a Z = 45 mm"),
        ("Soporte", "Bloqueador de soporte (Herramienta E)", "Cilindro dentro del hueco", "Obligatorio: impide que Cura meta soporte dentro de la ojiva"),
        ("Soporte", "Distancia Z del soporte", "0.20 mm a 0.22 mm", "Desmolde limpio del escalón plano a 90 grados"),
        ("Adherencia", "Tipo de adherencia / Ancho", "Borde (Brim) / 10.0 mm", "Sustenta la pieza alta (22.5 cm) ante la palanca del cabezal"),
        ("Adherencia", "Borde solo en el exterior", "Desmarcado (Sin check)", "Crea borde por fuera y por dentro del anillo del hombro")
    ]
    
    y = draw_table_cura(page2, y, rows_ojiva)
    y += 8
    
    # Protocolo de Impresión en Sunlu T3
    y = draw_section_header(page2, y, "PROTOCOLO OBLIGATORIO DE TALLER: SUNLU T3 + FILAMENTO ASA")
    
    t3_text = (
        "1. CERRAMIENTO TÉRMICO (CABINA): La Sunlu T3 es una impresora abierta. El ASA exige cámara caliente para no rajarse. "
        "Coloque la impresora dentro de una carpa ignífuga, cabina o caja cerrada. Queda prohibido imprimir con la impresora destapada.\n"
        "2. PRECALENTAMIENTO DE CABINA: Encienda la cama a 100 °C con la cabina cerrada durante 15 a 20 minutos ANTES de iniciar "
        "la impresión. El aire interno debe estabilizarse entre 40 °C y 50 °C para suprimir corrientes térmicas convectivas.\n"
        "3. FIJACIÓN DE BASE PEI: Limpie la lámina PEI con alcohol isopropílico y aplique una capa uniforme de adhesivo fijador "
        "(Dimafix, Magigoo o laca extrafuerte). No retire la pieza de la cama hasta que se enfríe naturalmente por debajo de 40 °C."
    )
    draw_info_card(page2, 40, y, 515, 86,
                   "RECOMENDACIONES DE OPERACIÓN TÉCNICA (SUNLU T3):",
                   t3_text,
                   NAVY_LIGHT)

    doc.save(output_path)
    doc.close()
    print(f"PDF generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_pdf = r"d:\Documentos\IEJAGA\2026\PDA\CCCD2026\Guia_Cura_Espanol_Acople_y_Ojiva_ASA.pdf"
    build_pdf(out_pdf)
