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
REC_BG = (0.96, 0.98, 1.0)       # Fondo suave para recomendaciones
REC_BORDER = (0.25, 0.45, 0.75)  # Borde azul suave
GREEN_ACC = (0.08, 0.48, 0.22)
CARD_BG = (0.98, 0.99, 1.0)

def draw_header_footer(page, page_num, total_pages):
    rect = page.rect
    page.draw_line((40, 36), (rect.width - 40, 36), color=SLATE, width=0.8)
    page.draw_line((40, rect.height - 34), (rect.width - 40, rect.height - 34), color=SLATE, width=0.8)
    
    # Encabezado
    page.insert_text((40, 30), "CCCD 2026 | I.E. JOSÉ ANTONIO GALÁN", fontsize=8.0, fontname="helv", color=SLATE)
    page.insert_text((315, 30), "Guía Técnica de Laminación: Ojiva 102 mm (ASA)", fontsize=8.0, fontname="helv", color=SLATE)
    
    # Pie de página
    page.insert_text((40, rect.height - 22), "Semillero PDA Rocketeers - Categoría 3 | Recomendaciones de Manufactura Aditiva", fontsize=7.2, fontname="helv", color=SLATE)
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

def draw_item_box(page, x, y, w, h, title, param_val, justification, tag_color=BLUE_ACC):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page.draw_rect(pymupdf.Rect(x, y, x + 4, y + h), color=tag_color, fill=tag_color, width=0.5)
    
    page.insert_text((x + 12, y + 13), title, fontsize=8.5, fontname="helv", color=NAVY)
    page.insert_text((x + 12, y + 25), f"Sugerencia en laminador: {param_val}", fontsize=8.0, fontname="helv", color=NAVY_LIGHT)
    
    tb_rect = pymupdf.Rect(x + 12, y + 30, x + w - 10, y + h - 4)
    safe_textbox(page, tb_rect, f"Justificación técnica: {justification}", fontsize=7.2, color=DARK)

def draw_recommendation_box(page, x, y, w, h, title, text):
    # Caja sobria y elegante con acento azul/marino sin tonos de alarma
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=REC_BORDER, fill=REC_BG, width=0.8)
    page.draw_rect(pymupdf.Rect(x, y, x + 4, y + h), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page.insert_text((x + 12, y + 13), title, fontsize=8.2, fontname="helv", color=NAVY)
    tb_rect = pymupdf.Rect(x + 12, y + 19, x + w - 10, y + h - 5)
    safe_textbox(page, tb_rect, text, fontsize=7.3, color=DARK)

def build_pdf(output_path):
    doc = pymupdf.open()
    total_pages = 2
    
    # ==============================================================================
    # PÁGINA 1: IDENTIFICACIÓN, TEMPERATURAS Y ESTRUCTURA
    # ==============================================================================
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, 1, total_pages)
    
    y = draw_banner(page1, 44, "GUÍA TÉCNICA DE LAMINACIÓN: OJIVA 102 mm (ASA)",
                    "Recomendaciones técnicas para el operador de impresión y justificación de ingeniería")
    
    # 1. Identificación y geometría
    fich_h = 76
    page1.draw_rect(pymupdf.Rect(40, y, 555, y + fich_h), color=NAVY_LIGHT, fill=LIGHT_BG, width=0.8)
    page1.insert_text((50, y + 14), "1. IDENTIFICACIÓN Y GEOMETRÍA DE LA PIEZA (STL)", fontsize=8.8, fontname="helv", color=NAVY)
    
    col1_text = (
        "- Archivo: 2026-10-08 Ojiva 102 mm punta ok.stl\n"
        "- Material: ASA (Acrilonitrilo Estireno Acrilato)\n"
        "- Boquilla instalada (Nozzle): 0.40 mm\n"
        "- Altura total de pieza en Z: 225.45 mm"
    )
    col2_text = (
        "- Diámetro exterior máximo: 102.00 mm\n"
        "- Diámetro del acople / hombro: 99.00 mm (Z = 0 a 45 mm)\n"
        "- Saliente del escalón exterior: 1.50 mm plano a 90 grados\n"
        "- Posición en cama: Base cilíndrica abajo, punta arriba"
    )
    safe_textbox(page1, pymupdf.Rect(50, y + 22, 290, y + fich_h - 4), col1_text, fontsize=7.5, color=DARK)
    safe_textbox(page1, pymupdf.Rect(300, y + 22, 545, y + fich_h - 4), col2_text, fontsize=7.5, color=DARK)
    y += fich_h + 8
    
    # 2. Gestión térmica y enfriamiento
    y = draw_section_header(page1, y, "2. GESTIÓN TÉRMICA Y ENFRIAMIENTO (FILAMENTO ASA)")
    
    draw_item_box(page1, 40, y, 515, 68,
                  "Temperatura de Boquilla (Extrusor)",
                  "250 °C a 255 °C continuos",
                  "El plástico ASA requiere buena temperatura para que las capas se fundan químicamente entre sí por difusión molecular. Si se imprime por debajo de 245 °C, las capas se pegan solo superficialmente y la pieza pierde tenacidad frente a las vibraciones o la apertura del paracaídas.",
                  NAVY_LIGHT)
    y += 73
    
    draw_item_box(page1, 40, y, 515, 78,
                  "Temperatura de Cama y Cabina (Enclosure)",
                  "Cama a 100 °C - 105 °C | Impresora CERRADA (Cabina sugerida: 45 °C a 55 °C)",
                  "El ASA tiene tendencia a contraerse con el enfriamiento. En una pieza de 22.5 cm de altura, mantener la cabina cerrada previene corrientes de aire frío que generan contracciones desiguales y fisuras horizontales. Se aconseja precalentar la cama a 100 °C con la puerta cerrada durante 15 minutos antes de iniciar.",
                  NAVY_LIGHT)
    y += 83
    
    draw_item_box(page1, 40, y, 515, 72,
                  "Ventilador de Capa (Part Cooling Fan)",
                  "0% (apagado) a máximo 10% en el cuerpo | 25% a 30% solo en el escalón exterior",
                  "El flujo excesivo de aire enfría el hilo antes de unirse firmemente a la capa anterior. Se recomienda imprimir la ojiva prácticamente sin ventilación de capa, activando solo un flujo moderado (25% a 30%) durante el trazado del escalón exterior para que el puente no descuelgue.",
                  NAVY_LIGHT)
    y += 78
    
    # 3. Altura de capa y estructura
    y = draw_section_header(page1, y, "3. ALTURA DE CAPA Y ESTRUCTURA DE PAREDES")
    
    draw_item_box(page1, 40, y, 515, 76,
                  "Altura de Capa (Sugerencia por Zonas)",
                  "0.20 mm en la base del acople (Z: 0 a 45 mm) | 0.16 mm en la ojiva (Z > 45 mm)",
                  "En la base cilíndrica de inserción (de 0 a 45 mm) se recomienda 0.20 mm para optimizar el tiempo de impresión en una sección puramente recta. A partir de los 45 mm, al iniciar la curvatura aerodinámica de la ojiva, se recomienda pasar a 0.16 mm para suavizar el escalonado superficial, mejorar el acabado y maximizar la unión entre capas.",
                  BLUE_ACC)
    y += 81
    
    draw_item_box(page1, 40, y, 515, 70,
                  "Perímetros y Espesor de Pared",
                  "4 bucles de pared | Ancho de línea en 0.45 mm | Orden: Paredes internas primero",
                  "El espesor modelado de la ojiva es de 1.50 mm. Con 4 perímetros a 0.45 mm, la pared queda 100% sólida y concéntrica en todo el perfil, eliminando microporosidades y evitando rellenos débiles en zigzag, lo que otorga rigidez ante la presión dinámica del vuelo.",
                  BLUE_ACC)
    y += 75
    
    draw_item_box(page1, 40, y, 515, 58,
                  "Adhesión a la Base (Brim / Borde Exterior)",
                  "Borde exterior de 8 mm a 10 mm pegado a la pieza (separación 0.0 mm)",
                  "Brinda sustentación contra el momento de inercia a medida que la pieza crece a 22.5 cm de altura sobre la plataforma, evitando que la base se levante. Se recomienda aplicar adhesivo fijador sobre lámina PEI.",
                  GREEN_ACC)
    
    # ==============================================================================
    # PÁGINA 2: COSTURAS, SOPORTES Y TABLA RESUMEN
    # ==============================================================================
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, 2, total_pages)
    
    y = 44
    y = draw_section_header(page2, y, "4. CONTROL DE COSTURAS (Z-SEAM) Y AERODINÁMICA")
    
    draw_recommendation_box(page2, 40, y, 515, 58,
                            "RECOMENDACIÓN: EVITAR LA COSTURA ALEATORIA (RANDOM SEAM)",
                            "Se aconseja no utilizar costura aleatoria. En un componente aerodinámico a velocidad subsónica alta, los puntos de inicio aleatorios dejan pequeñas marcas en los 360 grados de la piel exterior. Esto incrementa la fricción con el aire y exige un lijado perimetral completo, con riesgo de desbastar despareja la forma redonda de la ojiva.")
    y += 64
    
    draw_item_box(page2, 40, y, 515, 76,
                  "Configuración Sugerida de Costura",
                  "Costura Alineada (Aligned) o Atrás (Rear) en una sola línea recta vertical",
                  "Al alinear los cambios de capa en un único meridiano vertical (preferiblemente en la cara posterior): 1) El 98% del contorno exterior queda con superficie virgen y acabado uniforme. 2) La labor de acabado se reduce a pasar una lija suave al agua sobre esa única línea, logrando una superficie suave en pocos minutos sin alterar la redondez del cono.",
                  NAVY_LIGHT)
    y += 82
    
    y = draw_section_header(page2, y, "5. CONFIGURACIÓN DE SOPORTES (EL VOLADIZO EXTERNO)")
    
    draw_recommendation_box(page2, 40, y, 515, 60,
                            "RECOMENDACIÓN: OMITIR SOPORTES EN LA CAVIDAD INTERNA",
                            "La cavidad interior de la ojiva es cónica y termina en punta maciza; su ángulo es auto-portante y no requiere soporte. Si el laminador coloca soporte adentro, quedará atrapado a 20 cm de profundidad y será difícil de retirar, agregando peso innecesario. Se recomienda activar 'Solo en placa' y usar un Bloqueador de Soporte interno.")
    y += 66
    
    draw_item_box(page2, 40, y, 515, 68,
                  "Ubicación y Tipo de Soporte Exterior",
                  "Normal Ceñido (Snug) o Árbol (Tree) apoyado únicamente desde la base",
                  "El único punto geométrico que requiere apoyo es el escalón horizontal de 1.50 mm situado a 45 mm de altura (transición del hombro de 99 mm al fuselaje de 102 mm). Este escalón hace de tope plano contra el tubo del cohete y conviene imprimirlo perpendicular a 90 grados exactos.",
                  NAVY_LIGHT)
    y += 73
    
    draw_item_box(page2, 40, y, 515, 72,
                  "Distancia Vertical Z de Contacto con el Soporte",
                  "0.20 mm a 0.22 mm (Distancia Z superior / Top Z Contact Distance)",
                  "El filamento ASA caliente tiene alta adhesión entre hilos contiguos. Una distancia Z de 0.20 mm a 0.22 mm permite que la interfaz sostenga el escalón plano sin fundirse con él, logrando que el soporte se retire con facilidad y deje la cara inferior del escalón limpia.",
                  NAVY_LIGHT)
    y += 77
    
    draw_item_box(page2, 40, y, 515, 64,
                  "Separación Horizontal XY del Soporte",
                  "0.70 mm a 0.80 mm de separación respecto a la pared vertical",
                  "Evita que la torre de soporte toque lateralmente el cilindro del hombro (diámetro 99 mm). Este acople debe entrar suave y con ajuste preciso dentro del tubo del cohete, por lo que su superficie exterior cilíndrica debe conservarse sin rebabas.",
                  NAVY_LIGHT)
    y += 70
    
    # 6. Tabla resumen rápido
    y = draw_section_header(page2, y, "6. TABLA RESUMEN DE PARÁMETROS RÁPIDOS PARA EL LAMINADOR")
    
    th_h = 16
    page2.draw_rect(pymupdf.Rect(40, y, 555, y + th_h), color=NAVY, fill=NAVY, width=0.5)
    page2.insert_text((48, y + 11.5), "Parámetro en el Slicer", fontsize=8.0, fontname="helv", color=WHITE)
    page2.insert_text((220, y + 11.5), "Valor Sugerido a Digitar", fontsize=8.0, fontname="helv", color=WHITE)
    page2.insert_text((390, y + 11.5), "Objetivo Principal", fontsize=8.0, fontname="helv", color=WHITE)
    y += th_h
    
    table_rows = [
        ("Temperatura Boquilla", "250 °C a 255 °C", "Fusión molecular entre capas sin fisuras"),
        ("Temperatura Cama", "100 °C a 105 °C", "Evitar levantamiento de base (warping)"),
        ("Encerramiento / Cabina", "CERRADA (Precalentar 15 min)", "Eliminar corrientes de aire frío"),
        ("Ventilador de Capa", "0% a 10% (30% en escalón)", "Impedir que el plástico se raje"),
        ("Altura de Capa", "0.20 mm base / 0.16 mm ojiva", "Agilidad en base y suavidad en la curva"),
        ("Paredes / Perímetros", "4 bucles (ancho 0.45 mm)", "Pared 100% maciza (sin relleno zig-zag)"),
        ("Alineación de Costura", "Alineada o Atrás (Línea recta)", "Aerodinámica limpia, evitar aleatoria"),
        ("Soportes", "Solo escalón exterior (bloqueo interno)", "Evitar soporte atrapado en el interior"),
        ("Distancia Z al Soporte", "0.20 mm a 0.22 mm", "Facilidad de desprendimiento limpio"),
        ("Borde de Sujeción (Brim)", "8 mm a 10 mm exterior pegado", "Anclar la pieza alta a la cama caliente")
    ]
    
    row_h = 14
    for i, (param, val, obj) in enumerate(table_rows):
        bg = ROW_ALT if i % 2 == 1 else WHITE
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + row_h), color=GRAY_BORDER, fill=bg, width=0.5)
        page2.insert_text((48, y + 10), param, fontsize=7.2, fontname="helv", color=NAVY)
        page2.insert_text((220, y + 10), val, fontsize=7.2, fontname="helv", color=DARK)
        page2.insert_text((390, y + 10), obj, fontsize=7.0, fontname="helv", color=SLATE)
        y += row_h

    doc.save(output_path)
    doc.close()
    print(f"PDF generado exitosamente en: {output_path}")

if __name__ == "__main__":
    out_pdf = r"d:\Documentos\IEJAGA\2026\PDA\CCCD2026\Guia_Laminacion_Ojiva_102mm_ASA.pdf"
    build_pdf(out_pdf)
