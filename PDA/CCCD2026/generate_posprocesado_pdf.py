import os
import sys
import pymupdf

# ==============================================================================
# PALETA DE COLORES TÉCNICA (RGB normalizado 0 a 1)
# ==============================================================================
NAVY = (0.05, 0.16, 0.36)        # Azul marino institucional
NAVY_LIGHT = (0.12, 0.32, 0.65)  # Acento azul intermedio
BLUE_ACC = (0.12, 0.42, 0.78)    # Azul enlaces / detalles
BLUE_BG = (0.92, 0.95, 1.0)      # Fondo tenue para botones de enlace
BLUE_BORDER = (0.25, 0.50, 0.85)  # Borde botones de enlace
SLATE = (0.35, 0.42, 0.52)       # Gris técnico secundario
LIGHT_BG = (0.95, 0.97, 1.0)     # Fondo tenue azulado
WHITE = (1.0, 1.0, 1.0)
DARK = (0.1, 0.12, 0.15)         # Texto principal oscuro
GRAY_BORDER = (0.8, 0.84, 0.9)   # Bordes de tablas y cajas
ROW_ALT = (0.96, 0.98, 1.0)      # Alternado de filas
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
    page.draw_line((40, 38), (rect.width - 40, 38), color=SLATE, width=0.8)
    page.draw_line((40, rect.height - 32), (rect.width - 40, rect.height - 32), color=SLATE, width=0.8)
    
    # Header
    page.insert_text((40, 31), "CCCD 2026 | I.E. JOSÉ ANTONIO GALÁN | PDA ROCKETEERS & STARS", fontsize=7.2, fontname="helv", color=SLATE)
    page.insert_text((330, 31), doc_title[:45], fontsize=7.2, fontname="helv", color=SLATE)
    
    # Footer
    page.insert_text((40, rect.height - 22), "Manual Técnico de Taller: Posprocesado y Control de Masa (Delta m <= 2-3 g) | Uso Exclusivo Equipo Aeroespacial", fontsize=6.8, fontname="helv", color=SLATE)
    page.insert_text((rect.width - 85, rect.height - 22), f"Página {page_num} de {total_pages}", fontsize=7.2, fontname="helv", color=SLATE)

def draw_banner(page, y_start, title, subtitle):
    page.draw_rect(pymupdf.Rect(40, y_start, 555, y_start + 38), color=NAVY, fill=NAVY, width=1)
    page.insert_text((52, y_start + 15), title, fontsize=10.5, fontname="helv", color=WHITE)
    page.insert_text((52, y_start + 29), subtitle, fontsize=7.6, fontname="helv", color=(0.85, 0.92, 1.0))
    return y_start + 44

def draw_section_title(page, y, title):
    page.draw_rect(pymupdf.Rect(40, y, 44, y + 13), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page.draw_line((46, y + 13), (555, y + 13), color=GRAY_BORDER, width=0.8)
    page.insert_text((48, y + 10), title, fontsize=8.6, fontname="helv", color=NAVY)
    return y + 17

def draw_callout(page, x, y, w, h, title, text, c_bg, c_border, c_title):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=c_border, fill=c_bg, width=0.8)
    page.insert_text((x + 8, y + 11.5), title, fontsize=7.8, fontname="helv", color=c_title)
    tb_rect = pymupdf.Rect(x + 8, y + 15, x + w - 8, y + h - 2)
    rc = page.insert_textbox(tb_rect, text, fontsize=6.6, fontname="helv", color=DARK)
    if rc < 0:
        print(f"[WARN] Callout text overflow: {title} (rc={rc})")

def draw_supplier_card(page, x, y, w, h, title, subtitle, address, tel_text, wa_digits, wa_label, catalog_items, links=None):
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + h), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page.draw_rect(pymupdf.Rect(x, y, x + w, y + 14), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    
    page.insert_text((x + 6, y + 10), title, fontsize=7.8, fontname="helv", color=WHITE)
    page.insert_text((x + 6, y + 23), subtitle, fontsize=6.8, fontname="helv", color=NAVY_LIGHT)
    page.insert_text((x + 6, y + 32), f"Ubicación: {address}", fontsize=6.6, fontname="helv", color=DARK)
    
    # Phone + WA button
    page.insert_text((x + 6, y + 42), f"Contacto: {tel_text}", fontsize=6.6, fontname="helv", color=DARK)
    
    if wa_digits:
        btn_w = 125
        btn_x = x + w - btn_w - 6
        wa_rect = pymupdf.Rect(btn_x, y + 32, btn_x + btn_w, y + 44)
        page.draw_rect(wa_rect, color=GREEN_BORDER, fill=GREEN_BG, width=0.6)
        page.insert_text((btn_x + 5, y + 41), f"WhatsApp: {wa_label}", fontsize=6.3, fontname="helv", color=GREEN_ACC)
        page.insert_link({'kind': pymupdf.LINK_URI, 'from': wa_rect, 'uri': f"https://wa.me/{wa_digits}"})
        
    page.insert_text((x + 6, y + 53), f"Insumos clave: {catalog_items}", fontsize=6.4, fontname="helv", color=DARK)

    # Interactive Links Bar if provided
    if links:
        link_x = x + 6
        link_y = y + 58
        for btn_label, btn_url in links:
            # Measure width
            btn_width = len(btn_label) * 4.6 + 10
            btn_rect = pymupdf.Rect(link_x, link_y, link_x + btn_width, link_y + 11.5)
            page.draw_rect(btn_rect, color=BLUE_BORDER, fill=BLUE_BG, width=0.5)
            page.insert_text((link_x + 4, link_y + 8.5), btn_label, fontsize=5.8, fontname="helv", color=NAVY)
            page.insert_link({'kind': pymupdf.LINK_URI, 'from': btn_rect, 'uri': btn_url})
            link_x += btn_width + 6

# ==============================================================================
# GENERADOR DEL MANUAL COMPLETO
# ==============================================================================
def build_manual_posprocesado(filepath):
    doc = pymupdf.open()
    total_pages = 4
    
    # ==========================================================================
    # PÁGINA 1: MARCO DE MASA, PROVEEDORES E INSUMOS DE LIJADO
    # ==========================================================================
    page1 = doc.new_page(width=595, height=842)
    draw_header_footer(page1, "Manual Posprocesado y Acabado Aeronáutico", 1, total_pages)
    
    y = draw_banner(page1, 46, "MANUAL DE POSPROCESADO Y ACABADO AERONÁUTICO",
                    "Protocolo de Lijado, Sellado Químico y Pintura con Restricción Estricta de Masa (Delta m <= 2 a 3 g)")
    
    # Callout de masa
    draw_callout(page1, 40, y, 515, 52,
                 "PRESUPUESTO ESTRICTO DE MASA SECA (DELTA M <= 2.0 A 3.0 GRAMOS POR COMPONENTE):",
                 "En cohetería de alta y media potencia (Cat 3 motor G80 y Cat 2 motor F15), el acabado superficial debe reducir la fricción aerodinámica (Cd) sin alterar el balance de masa. Cada gramo añadido en aletas desplaza el Centro de Gravedad (CG) hacia popa, reduciendo el margen de estabilidad (>= 2.0 cal). Se prohíbe el masillado pesado de carrocería (Bondo) o resinas densas aplicadas a brocha.",
                 WARN_BG, WARN_BORDER, (0.8, 0.4, 0.0))
    y += 58
    
    # Sección 1: Proveedores
    y = draw_section_title(page1, y, "1. DIRECTORIO DE PROVEEDORES Y ENLACES DIRECTOS A PRODUCTO")
    
    # Card 1: Homecenter (con enlaces directos de producto)
    homecenter_links = [
        ("Ver MTN PRO Plásticos (SKU: 393972)", "https://www.homecenter.com.co/homecenter-co/product/393972/aerosol-imprimacion-plasticos-y-metales-400-ml/393972/"),
        ("Ver MTN PRO Fondo Blanco (SKU: 393974)", "https://www.homecenter.com.co/homecenter-co/product/393974/aerosol-imprimacion-fondo-blanco-400-ml/393974/"),
        ("Ver Base Truper 9'' (SKU: 620849)", "https://www.homecenter.com.co/homecenter-co/product/620849/lijadora-manual-de-9-1-3-de-hoja-para-acabados-finos/620849/")
    ]
    draw_supplier_card(page1, 40, y, 515, 72,
                       "HOMECENTER (Sodimac Las Vegas / Envigado / San Juan)",
                       "Líneas Técnicas Montana Colors (MTN PRO) y Herramientas de Lijado",
                       "Av. Las Vegas (Envigado / Poblado) | Tienda en Línea Homecenter.com.co",
                       "PBX: (604) 444 4455 / Web", "", "",
                       "Montana Colors MTN PRO Imprimación Plásticos ($52.900), MTN PRO Fondo Blanco ($52.900), Base Truper ($33.900), Lijas Abracol.",
                       links=homecenter_links)
    y += 76
    
    # Card 2: Sumiglas (con enlaces a catálogo y fichas)
    sumiglas_links = [
        ("Catálogo Resinas Sumiglas", "https://sumiglas.com/resinas-epoxicas/"),
        ("Fichas Técnicas Oficiales", "https://sumiglas.com/fichas-tecnicas/")
    ]
    draw_supplier_card(page1, 40, y, 515, 72,
                       "SUMIGLAS S.A.S. — Sede Guayabal (Medellín)",
                       "Distribuidor de Materias Primas para Compuestos y Resinas de Grado Aeronáutico",
                       "Calle 14 # 51-26 (Contiguo al Centro Empresarial Olaya Herrera)",
                       "(604) 448 9922", "573136842173", "+57 313 684 2173",
                       "Resina Epóxica Rígida de Baja Viscosidad (Glas 04 / Sistema 1840 con endurecedor 2:1), fraccionada para sellado micrónico de madera.",
                       links=sumiglas_links)
    y += 76

    # Card 3: Poliuretanos y Químicos
    poli_links = [
        ("Directorio y Contacto Guayabal", "https://directoriomedellin.com.co/item/poliuretanos-y-quimicos-sas/")
    ]
    draw_supplier_card(page1, 40, y, 515, 70,
                       "POLIURETANOS Y QUÍMICOS S.A.S. — Eje Guayabal",
                       "Especialistas en Sistemas de Resinas, Poliuretanos Industriales y Solventes",
                       "Carrera 52 # 25-66 (Avenida Guayabal, sector Plaza Mayorista / Olaya Herrera)",
                       "(604) 444 4421 / (604) 235 7788", "", "",
                       "Resinas epoxi y poliéster, sistemas de poliuretano bicomponente, alcohol isopropílico de alta pureza y agentes desengrasantes.",
                       links=poli_links)
    y += 74

    # Card 4: HobbyCol y Área Hobbies
    hobby_links = [
        ("Portal HobbyCol Medellín", "https://hobbycol.com/"),
        ("Portal Área Hobbies Mayorca", "https://areahobbies.com/"),
        ("Tamiya Primer en Colombia", "https://listado.mercadolibre.com.co/tamiya-surface-primer")
    ]
    draw_supplier_card(page1, 40, y, 515, 72,
                       "HOBBYCOL (Guayabal) & ÁREA HOBBIES (Mall Plaza Mayorca)",
                       "Tiendas Técnicas de Aeromodelismo, Maquetismo de Escala y Resinas Estructurales",
                       "HobbyCol: Cra 52 # 25-96 | Área Hobbies: Cra 43A # 49D Sur 22, Mayorca Envigado",
                       "HobbyCol: 318 497 7695", "573052270009", "305 227 0009 (Mayorca)",
                       "Imprimante Tamiya Surface Primer (capa ultraligera de 15 micras), epóxico de 30 min para filetes exteriores de aletas y tacos de balsa.",
                       links=hobby_links)
    y += 76

    # Sección 2: Herramientas de Lijado
    y = draw_section_title(page1, y, "2. CATÁLOGO DE TACOS DE LIJADO Y ACCESORIOS HOMOLOGADOS")
    
    # Tabla de Tacos con enlaces interactivos en cada fila
    page1.draw_rect(pymupdf.Rect(40, y, 555, y + 14), color=NAVY, fill=NAVY, width=0.5)
    page1.insert_text((45, y + 10), "HERRAMIENTA", fontsize=7.2, fontname="helv", color=WHITE)
    page1.insert_text((150, y + 10), "TIPO Y SISTEMA", fontsize=7.2, fontname="helv", color=WHITE)
    page1.insert_text((275, y + 10), "PROVEEDOR / COSTO", fontsize=7.2, fontname="helv", color=WHITE)
    page1.insert_text((400, y + 10), "APLICACIÓN EN EL COHETE", fontsize=7.2, fontname="helv", color=WHITE)
    y += 15
    
    tacos_rows = [
        ("Base Truper 9'' (SKU 620849)", "Plana rígida con mordazas metálicas", "Homecenter ($33.900) [Ver Link]", "Aplanado de Triplex Okume y aletas PETG-CF.", "https://www.homecenter.com.co/homecenter-co/product/620849/lijadora-manual-de-9-1-3-de-hoja-para-acabados-finos/620849/"),
        ("Taco Lijador Mastder", "Goma automotriz semirrígida", "Homecenter ($38.900) [Ver Link]", "Asentado húmedo de transición cónica en ojivas.", "https://www.homecenter.com.co/homecenter-co/search?Ntt=taco+lijador"),
        ("Taco de Goma Automotriz", "Caucho compacto 90x60 mm", "Ferreterías Itagüí ($8.000 - $12.000)", "Desbaste plano de cantos y bordes de fuga en madera.", ""),
        ("Taco de Espuma Flexible", "Esponja abrasiva / bloque EVA fino", "Ferreterías / Tiendas de pintura", "Lijado de ojivas curvas (Haack/Cónica) sin marcas.", "https://www.homecenter.com.co/homecenter-co/search?Ntt=esponja+lijadora"),
        ("Lubricante de Lijado", "Agua + 3 gotas jabón neutro (1%)", "Taller escolar (preparación propia)", "Refrigera, evita empastar lija y deformar plástico.", "")
    ]
    
    for item, mec, shop, uso, url_link in tacos_rows:
        row_rect = pymupdf.Rect(40, y, 555, y + 13.5)
        page1.draw_rect(row_rect, color=GRAY_BORDER, fill=WHITE, width=0.4)
        page1.insert_text((45, y + 9.5), item, fontsize=6.8, fontname="helv", color=DARK)
        page1.insert_text((150, y + 9.5), mec, fontsize=6.6, fontname="helv", color=DARK)
        
        if url_link:
            page1.insert_text((275, y + 9.5), shop, fontsize=6.6, fontname="helv", color=NAVY_LIGHT)
            page1.insert_link({'kind': pymupdf.LINK_URI, 'from': pymupdf.Rect(275, y + 1, 395, y + 12), 'uri': url_link})
        else:
            page1.insert_text((275, y + 9.5), shop, fontsize=6.6, fontname="helv", color=DARK)
            
        page1.insert_text((400, y + 9.5), uso, fontsize=6.6, fontname="helv", color=SLATE)
        y += 14.0


    # ==========================================================================
    # PÁGINA 2: PROTOCOLO TÉCNICO DE ALETAS (CAT 3 Y CAT 2)
    # ==========================================================================
    page2 = doc.new_page(width=595, height=842)
    draw_header_footer(page2, "Manual Posprocesado y Acabado Aeronáutico", 2, total_pages)
    
    y = 46
    y = draw_section_title(page2, y, "3. PROTOCOLO ALETAS CAT 3: TRIPLEX OKUME (SIN FIBRA DE CARBONO)")
    
    draw_callout(page2, 40, y, 515, 42,
                 "DIAGNÓSTICO TÉCNICO DE LA MADERA DE OKUME FRENTE AL CONTROL DE MASA:",
                 "El Triplex Okume es contrachapado de grano abierto. Si se aplica resina a brocha o pintura líquida directa, absorbe entre 12 y 20 g de solvente/resina. Se exige la 'Técnica de Sellado Micrónico por Raspado' para limitar el incremento a máximo 2.0 - 2.5 g en toda la aleta.",
                 LIGHT_BG, NAVY_LIGHT, NAVY)
    y += 48
    
    fases_aletas_cat3 = [
        ("Fase 1: Perfilado Aerodinámico Substractivo",
         "- Herramienta: Base rígida Truper o taco plano de madera con lija en seco grano 180 y 240.\n"
         "- Procedimiento: Redondear el borde de ataque con radio continuo (~1 mm) y afilar el borde de fuga en cuña cónica suave.\n"
         "- Balance de masa: Esta operación remueve entre 2.0 y 3.0 g de aserrín de la pieza bruta. Limpiar el polvillo con brocha seca.",
         52, NAVY),
        ("Fase 2: Sellado Micrónico de Poro por Raspado con Tarjeta (Insumo: Resina Glas 04 de Sumiglas)",
         "- Mezcla: Catalizar 5 g de resina epóxica de baja viscosidad en relación 2:1 por peso en una copa de dosificación.\n"
         "- Aplicación: Verter únicamente 6 a 8 gotas de epoxi catalizado sobre el centro de cada cara de la aleta de Triplex.\n"
         "- Técnica de raspado: Con una tarjeta plástica rígida (o espátula japonesa), extender y raspar con fuerza a 45° retirando TODO el exceso exterior. La resina debe quedar forzada dentro de los microporos celulares sin formar capa líquida en superficie.\n"
         "- Ganancia de masa: El epóxico atrapado en los poros pesa menos de 0.8 a 1.0 g por aleta. Dejar curar 18 a 24 horas.",
         68, DARK),
        ("Fase 3: Asentado al Agua e Imprimación de Guía",
         "- Asentado: Frotar suavemente con taco plano y lija grano 400 al agua jabonosa para nivelar la superficie vitrificada.\n"
         "- Imprimación: Rociar una sola neblina pulverizada rápida a 30 cm de distancia con Montana Colors MTN PRO Fondo Blanco.\n"
         "- Lijado fino: Dejar secar 20 min y dar una pasada muy leve con lija 600 al agua. El aporte seco de aparejo es de solo ~0.6 g.",
         52, DARK),
        ("Fase 4: Acabado Final y Enmascarado Crítico de la Raíz",
         "- ENMASCARADO OBLIGATORIO: Colocar cinta de carrocero de 5 mm cubriendo toda la arista de la raíz que hace contacto con el fuselaje. ESTÁ PROHIBIDO PINTAR LA RAÍZ; el adhesivo estructural debe fijarse madera virgen contra fuselaje.\n"
         "- Color: 1 mano fina de esmalte MTN PRO o Rust-Oleum 2X (aporte: ~0.8 g). Masa total agregada final: 2.2 a 2.5 g.",
         52, ALERT_BORDER)
    ]
    
    for t_f, d_f, h_box, c_col in fases_aletas_cat3:
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + h_box), color=GRAY_BORDER, fill=CARD_BG, width=0.6)
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + 13), color=LIGHT_BG, fill=LIGHT_BG, width=0.4)
        page2.insert_text((46, y + 9.5), t_f, fontsize=7.2, fontname="helv", color=c_col)
        rc = page2.insert_textbox(pymupdf.Rect(46, y + 15, 550, y + h_box - 2), d_f, fontsize=6.6, fontname="helv", color=DARK)
        if rc < 0:
            print(f"[WARN] Overflow en Fase Aletas Cat 3: {t_f} (rc={rc})")
        y += h_box + 4

    y += 4
    y = draw_section_title(page2, y, "4. PROTOCOLO ALETAS CAT 2: PETG-CF (MONTAJE SUPERFICIAL EXTERIOR / NO TTW)")
    
    draw_callout(page2, 40, y, 515, 42,
                 "REGLA CRÍTICA DE MONTAJE SUPERFICIAL EN FUSELAJE KRAFT BT-80:",
                 "Al no ser aletas pasantes (Through-The-Wall), el 100% de la resistencia al flutter y desprendimiento depende del filete adhesivo exterior. Si se pinta la raíz de la aleta, el epóxico se pegará sobre la pintura y la aleta se arrancará en el despegue.",
                 ALERT_BG, ALERT_BORDER, (0.7, 0.1, 0.1))
    y += 48

    fases_aletas_cat2 = [
        ("Paso 1: Preparación Mecánica y Desengrase",
         "Las aletas impresas en PETG-CF plano sobre cama ya tienen una cara lisa y textura mate de carbono. No requiere masilla.\n"
         "Lijar con taco semirrígido y lija al agua grano 400 únicamente los radios de ataque y fuga. Limpiar con alcohol isopropílico.", 38),
        ("Paso 2: Enmascarado de la Arista de Raíz",
         "Aplicar cinta azul 3M cubriendo la franja inferior de la raíz (arista plana de contacto con el tubo BT-80). Debe quedar plástico virgen.", 28),
        ("Paso 3: Imprimación de Anclaje y Color de Visibilidad",
         "Aplicar 1 pasada relámpago de Montana Colors MTN PRO Plásticos (espesor seco < 5 micras, masa < 0.3 g).\n"
         "Aplicar 1 mano delgada de color de alta visibilidad (blanco o flúor) a 25 cm. Masa seca total añadida: 1.2 a 1.5 g por aleta.", 38),
        ("Paso 4: Montaje y Filetes Estructurales",
         "Retirar la cinta de la raíz. Lijar suavemente la zona del fuselaje BT-80 con lija 180 (quitar brillo). Adherir la aleta con epóxico estructural de 30 min (Área Hobbies / Sumiglas) y conformar un filete curvo exterior con radio de 4 a 5 mm.", 38)
    ]
    
    for t_f, d_f, h_box in fases_aletas_cat2:
        page2.draw_rect(pymupdf.Rect(40, y, 555, y + h_box), color=GRAY_BORDER, fill=WHITE, width=0.6)
        page2.insert_text((46, y + 10), t_f, fontsize=7.2, fontname="helv", color=NAVY)
        rc = page2.insert_textbox(pymupdf.Rect(46, y + 13, 550, y + h_box - 2), d_f, fontsize=6.6, fontname="helv", color=DARK)
        if rc < 0:
            print(f"[WARN] Overflow en Aletas Cat 2: {t_f} (rc={rc})")
        y += h_box + 3


    # ==========================================================================
    # PÁGINA 3: PROTOCOLO DE OJIVAS Y REGLA ESTRICTA DE ACOPLES
    # ==========================================================================
    page3 = doc.new_page(width=595, height=842)
    draw_header_footer(page3, "Manual Posprocesado y Acabado Aeronáutico", 3, total_pages)
    
    y = 46
    y = draw_section_title(page3, y, "5. PROTOCOLO DE OJIVAS FDM: CAT 2 (PETG-CF) Y CAT 3 (ASA 102 MM)")
    
    draw_callout(page3, 40, y, 515, 42,
                 "CONFIRMACIÓN DE COMPATIBILIDAD ELECTRÓNICA:",
                 "Se confirma que la ojiva de Categoría 2 NO aloja aviónica interna con antena de radiofrecuencia. En consecuencia, el uso de filamento PETG-CF es totalmente válido y seguro. Proporciona máxima resistencia al impacto en la punta sin riesgo operativo.",
                 GREEN_BG, GREEN_BORDER, GREEN_ACC)
    y += 48

    # Ojiva Cat 2
    page3.draw_rect(pymupdf.Rect(40, y, 555, y + 120), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page3.draw_rect(pymupdf.Rect(40, y, 555, y + 14), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page3.insert_text((46, y + 10), "OJIVA CAT 2 — PETG-CF (FUSILAMIENTO AERODINÁMICO DE BAJO PESO)", fontsize=7.8, fontname="helv", color=WHITE)
    
    cat2_steps = (
        "1. Desbaste inicial al agua (Lija 240 + agua jabonosa):\n"
        "   Lijar con taco de espuma flexible en sentido longitudinal (desde la punta hacia la base) para desvanecer las líneas de capa Z.\n"
        "   No lijar en seco (el calor derrite microfibras de PETG). Esta operación remueve ~1.5 g de plástico FDM. Secar con paño limpio.\n"
        "2. Anclaje químico (Montana Colors MTN PRO Imprimación Plásticos):\n"
        "   Aplicar 1 pasada uniforme a 25 cm. La resina promotora rompe la tensión superficial del PETG. Tiempo de evaporación: 10 min (masa < 0.4 g).\n"
        "3. Aparejo y técnica de 'Lijar hasta transparentar' (MTN PRO Fondo Blanco / Aparejo):\n"
        "   Aplicar 1 capa fina de aparejo blanco. Dejar secar 45 min. Lijar con lija al agua grano 600 hasta que las crestas del plástico negro\n"
        "   vuelvan a verse transparentes. El aparejo solo permanece dentro de las hendiduras microscópicas (masa retenida: ~0.8 g).\n"
        "4. Acabado de color de visibilidad:\n"
        "   1 capa rápida de esmalte de color (blanco/flúor). Incremento neto total de masa seca: 2.2 a 2.5 gramos."
    )
    rc = page3.insert_textbox(pymupdf.Rect(46, y + 16, 550, y + 118), cat2_steps, fontsize=6.6, fontname="helv", color=DARK)
    if rc < 0:
        print(f"[WARN] Overflow Ojiva Cat 2: rc={rc}")
    y += 126

    # Ojiva Cat 3
    page3.draw_rect(pymupdf.Rect(40, y, 555, y + 120), color=GRAY_BORDER, fill=CARD_BG, width=0.8)
    page3.draw_rect(pymupdf.Rect(40, y, 555, y + 14), color=NAVY, fill=NAVY, width=0.5)
    page3.insert_text((46, y + 10), "OJIVA CAT 3 — FILAMENTO ASA 102 MM (VEHÍCULO SIDERAL)", fontsize=7.8, fontname="helv", color=WHITE)
    
    cat3_steps = (
        "1. Desbaste en seco (Lija 180 y 240 con taco rígido/flexible):\n"
        "   El ASA es un polímero duro y altamente mecanizable. Lijar en seco la costura Z y las estrías superiores de la ojiva cónica.\n"
        "   Remover ~2.5 a 3.5 g de crestas plásticas. Luego dar una pasada con lija al agua grano 320 para suavizar arañazos del grano grueso.\n"
        "2. Imprimación técnica:\n"
        "   Limpiar el polvillo con alcohol isopropílico. Aplicar 1 capa ligera de MTN PRO Plásticos o directamente MTN PRO Fondo Blanco.\n"
        "3. Asentado al agua (Grano 400 y 600 húmedo):\n"
        "   Lijar el aparejo blanco hasta obtener una superficie sedosa de acabado aeronáutico. Comprobar tacto con la yema de los dedos.\n"
        "4. Capa de sellado térmico y visual:\n"
        "   1 capa corrida de esmalte blanco brillante (para minimizar absorción de calor solar en rampa de lanzamiento).\n"
        "   Incremento neto final de masa seca: 2.5 a 2.8 gramos (cumple con holgura el límite <= 3.0 g)."
    )
    rc = page3.insert_textbox(pymupdf.Rect(46, y + 16, 550, y + 118), cat3_steps, fontsize=6.6, fontname="helv", color=DARK)
    if rc < 0:
        print(f"[WARN] Overflow Ojiva Cat 3: rc={rc}")
    y += 126

    y = draw_section_title(page3, y, "6. REGLA ESTRICTA: ACOPLES DESLIZANTES (CAT 2 PETG TRANSP. Y CAT 3 ASA INTERIOR)")
    
    draw_callout(page3, 40, y, 515, 78,
                 "PROHIBICIÓN TOTAL DE PINTURA, IMPRIMANTE O MASILLA EN ZONAS DE ACOPLE:",
                 "1. Justificación Normativa (DCP 2026 Secc. 3.2.5): El acoplador debe penetrar al menos 1.0 calibre (102 mm en Cat 3) y deslizar suavemente bajo una fuerza de eyección calibrada.\n"
                 "2. Mecánica de Fluidos: Una capa de primer + pintura agrega entre 150 y 250 micras (0.15 - 0.25 mm) de espesor irregular y alta rugosidad estática. Esto produce atascamiento del émbolo de separación en vuelo, causando falla catastrófica de recuperación.\n"
                 "3. Procedimiento Obligatorio: Enmascarar herméticamente con cinta azul 3M toda la longitud de inserción deslizante de los acoples antes de pintar las piezas vecinas. Deben conservar la textura plástica virgen de fábrica.",
                 ALERT_BG, ALERT_BORDER, (0.8, 0.1, 0.1))
    y += 84

    # Card adicional: Verificación de Deslizamiento
    draw_callout(page3, 40, y, 515, 62,
                 "CHECKLIST DE CALIBRACIÓN MECÁNICA DE ACOPLADORES:",
                 "- Prueba de Gravedad Invertida: El acoplador insertado debe sostener el peso de la ojiva invertida pero deslizarse libremente al sacudir el fuselaje hacia abajo con la mano (fuerza de tracción ~5 a 15 N).\n"
                 "- Limpieza: Desengrasar con alcohol isopropílico para retirar polvo de lija antes de empacar el paracaídas y la manta Nomex.\n"
                 "- Prohibición de Lubricantes: Prohibido usar aceites o grasas (atrapan polvo en rampa y degradan la tela del paracaídas).",
                 LIGHT_BG, NAVY_LIGHT, NAVY)


    # ==========================================================================
    # PÁGINA 4: TIEMPOS DE TALLER, METROLOGÍA Y CHECKLIST DE CONTROL
    # ==========================================================================
    page4 = doc.new_page(width=595, height=842)
    draw_header_footer(page4, "Manual Posprocesado y Acabado Aeronáutico", 4, total_pages)
    
    y = 46
    y = draw_section_title(page4, y, "7. MATRIZ DE TIEMPOS DE SECADO Y CURADO QUÍMICO EN TALLER (VALLE DE ABURRÁ)")
    
    # Tabla de tiempos
    page4.draw_rect(pymupdf.Rect(40, y, 555, y + 14), color=NAVY, fill=NAVY, width=0.5)
    page4.insert_text((48, y + 10), "PRODUCTO QUÍMICO", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((180, y + 10), "SECADO AL TACTO", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((285, y + 10), "TIEMPO PARA LIJADO", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((405, y + 10), "CURADO TOTAL (LISTO PARA VUELO)", fontsize=7.2, fontname="helv", color=WHITE)
    y += 15
    
    tiempos_rows = [
        ("Resina Epóxica Glas 04 (Raspado Okume)", "4 a 6 horas (estado gel)", "18 a 24 horas (curado duro)", "48 horas a temperatura ambiente (22-25 °C)"),
        ("Montana Colors MTN PRO Plásticos", "10 a 15 minutos", "No se lija (capa micrónica)", "2 horas (anclaje polimérico completo)"),
        ("MTN PRO Fondo Blanco / Aparejo", "15 a 20 minutos", "45 a 60 minutos (al agua)", "12 horas (polimerización acrílica estable)"),
        ("Esmaltes Acrílicos Rust-Oleum / MTN", "20 a 30 minutos", "24 horas (si requiere pulir)", "24 a 48 horas (dureza mecánica de vuelo)"),
        ("Epóxico Estructural 30 min (Raíz aletas)", "30 a 45 minutos", "3 horas", "24 horas (resistencia a tracción > 25 MPa)")
    ]
    
    for prod, t_tacto, t_lija, t_vuelo in tiempos_rows:
        page4.draw_rect(pymupdf.Rect(40, y, 555, y + 13.5), color=GRAY_BORDER, fill=WHITE, width=0.4)
        page4.insert_text((45, y + 9.5), prod, fontsize=6.6, fontname="helv", color=DARK)
        page4.insert_text((180, y + 9.5), t_tacto, fontsize=6.5, fontname="helv", color=DARK)
        page4.insert_text((285, y + 9.5), t_lija, fontsize=6.5, fontname="helv", color=DARK)
        page4.insert_text((405, y + 9.5), t_vuelo, fontsize=6.4, fontname="helv", color=SLATE)
        y += 14

    y += 8
    y = draw_section_title(page4, y, "8. HOJA DE CONTROL METROLÓGICO PRE/POST PINTURA (CHECKLIST EN GRAMERA)")
    
    draw_callout(page4, 40, y, 515, 42,
                 "INSTRUCCIÓN OBLIGATORIA DE PESAJE EN TALLER:",
                 "Toda pieza debe registrarse en la báscula de precisión digital (0.01 g) antes de iniciar y después del secado final de 24 h. Si una pieza supera los 3.0 gramos de peso añadido, debe asentarse con lija al agua 600 para retirar excedente de película seca.",
                 LIGHT_BG, NAVY_LIGHT, NAVY)
    y += 48

    # Tabla de Control de Masa
    page4.draw_rect(pymupdf.Rect(40, y, 555, y + 14), color=NAVY_LIGHT, fill=NAVY_LIGHT, width=0.5)
    page4.insert_text((48, y + 10), "COMPONENTE", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((160, y + 10), "PESO BRUTO (m0)", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((255, y + 10), "TRAS DESBASTE (m1)", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((355, y + 10), "FINAL PINTADO (m2)", fontsize=7.2, fontname="helv", color=WHITE)
    page4.insert_text((455, y + 10), "DELTA M MÁXIMO", fontsize=7.2, fontname="helv", color=WHITE)
    y += 15

    check_rows = [
        ("Ojiva Cat 2 (PETG-CF)", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "<= +2.5 g (Aprobado)"),
        ("Ojiva Cat 3 (ASA 102 mm)", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "<= +2.8 g (Aprobado)"),
        ("Aletas Cat 2 (PETG-CF x3)", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "<= +1.5 g / pieza"),
        ("Aletas Cat 3 (Okume x4)", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "Anotar gramos: [     ]", "<= +2.2 g / pieza"),
        ("Acoples deslizantes", "Peso fijo sin pintar", "No aplica", "Peso original invariable", "+0.0 g (Estricto)")
    ]

    for comp, m0, m1, m2, dmax in check_rows:
        page4.draw_rect(pymupdf.Rect(40, y, 555, y + 13.5), color=GRAY_BORDER, fill=WHITE, width=0.4)
        page4.insert_text((45, y + 9.5), comp, fontsize=6.8, fontname="helv", color=DARK)
        page4.insert_text((160, y + 9.5), m0, fontsize=6.4, fontname="helv", color=SLATE)
        page4.insert_text((255, y + 9.5), m1, fontsize=6.4, fontname="helv", color=SLATE)
        page4.insert_text((355, y + 9.5), m2, fontsize=6.4, fontname="helv", color=SLATE)
        page4.insert_text((455, y + 9.5), dmax, fontsize=6.6, fontname="helv", color=GREEN_ACC)
        y += 14

    y += 8
    y = draw_section_title(page4, y, "9. PLAN DE CONTINGENCIA Y CORRECCIÓN DE DEFECTOS EN TALLER")
    
    contingencia_text = (
        "- Sobrepeso (Delta m > 3.0 g): Lijar al agua con grano 600 y 1000 con movimientos suaves hasta rebajar el exceso de película seca.\n"
        "- Pintura accidental en raíz o acople: Raspar con cuchilla de precisión o lija 180 en seco hasta reexponer el sustrato plástico o madera virgen.\n"
        "- Falta de adherencia / Descascarado en PETG o ASA: Ocurre por omisión del promotor MTN PRO Plásticos o grasa dactilar. Limpiar con alcohol isopropílico y aplicar 1 pasada rápida de promotor antes de retocar con color.\n"
        "- Alabeo en Triplex Okume: Si la madera absorbe humedad ambiental durante el lijado, prensar la aleta entre dos tablas planas de madera rígida con peso uniforme de 5 kg encima durante 12 horas hasta estabilización completa."
    )
    draw_callout(page4, 40, y, 515, 78,
                 "ACCIONES CORRECTIVAS INMEDIATAS ANTE ANOMALÍAS EN TALLER:",
                 contingencia_text, ALERT_BG, ALERT_BORDER, (0.7, 0.1, 0.1))

    doc.save(filepath)
    doc.close()
    print(f"Manual generado con éxito: {filepath}")

if __name__ == "__main__":
    out_dir = r"d:\Documentos\IEJAGA\2026\PDA\CCCD2026"
    pdf_path = os.path.join(out_dir, "Manual_Posprocesado_y_Acabado_Aeronautico_CCCD2026.pdf")
    build_manual_posprocesado(pdf_path)
