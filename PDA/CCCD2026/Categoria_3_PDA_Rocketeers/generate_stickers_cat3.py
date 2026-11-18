import os
import sys
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from PIL import Image

# Register Impact Font
IMPACT_PATH = "C:/Windows/Fonts/impact.ttf"
if os.path.exists(IMPACT_PATH):
    pdfmetrics.registerFont(TTFont("Impact", IMPACT_PATH))
    FONT_NAME = "Impact"
else:
    FONT_NAME = "Helvetica-Bold"

def draw_single_sticker(c, x0, y0, show_cut_guide=True, is_isolated=False):
    """
    Dibuja un sticker de 60x60 mm (6x6 cm) exactamente idéntico al referente físico.
    x0, y0: Coordenadas de la esquina inferior izquierda del sticker en pt.
    """
    size = 60.0 * mm
    pad = 4.5 * mm
    rect_w = size - 2 * pad
    rect_h = size - 2 * pad
    radius = 6.8 * mm
    
    # 1. Guía de corte perimetral de 60x60 mm
    if show_cut_guide:
        c.saveState()
        c.setStrokeColorRGB(0.75, 0.80, 0.85) # Gris suave delimitador
        c.setLineWidth(0.4)
        c.setDash([2.5, 2.0])
        c.rect(x0, y0, size, size, stroke=1, fill=0)
        c.restoreState()

    # Si es aislado, dibujar crucetas o esquinas de corte exteriores
    if is_isolated:
        c.saveState()
        c.setStrokeColorRGB(0.4, 0.4, 0.4)
        c.setLineWidth(0.5)
        mark_len = 4 * mm
        # 4 esquinas exteriores
        # BL
        c.line(x0 - mark_len, y0, x0, y0)
        c.line(x0, y0 - mark_len, x0, y0)
        # BR
        c.line(x0 + size, y0, x0 + size + mark_len, y0)
        c.line(x0 + size, y0 - mark_len, x0 + size, y0)
        # TL
        c.line(x0 - mark_len, y0 + size, x0, y0 + size)
        c.line(x0, y0 + size, x0, y0 + size + mark_len)
        # TR
        c.line(x0 + size, y0 + size, x0 + size + mark_len, y0 + size)
        c.line(x0 + size, y0 + size, x0 + size, y0 + size + mark_len)
        c.restoreState()
    
    # 2. Marco interior negro con bordes redondeados (1.6 mm / 4.5 pt)
    c.saveState()
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.setLineWidth(1.6 * mm)
    c.roundRect(x0 + pad, y0 + pad, rect_w, rect_h, radius, stroke=1, fill=0)
    c.restoreState()
    
    # 3. Tipografía y líneas de información oficiales
    c.setFillColorRGB(0.0, 0.0, 0.0)
    center_x = x0 + size / 2.0
    
    lines = [
        ("PDA ROCKETEERS - ID 310", 12.0),
        ("I.E. JOSÉ ANTONIO GALÁN", 11.5),
        ("COLOMBIA - LA ESTRELLA", 11.5),
        ("MOTOR: G80-7T (29 mm)", 11.5),
        ("AVANZADOS", 12.0),
        ("pdarocketeers@jaga.edu.co", 10.5),
        ("+57 313 7034500", 13.0)
    ]
    
    # Centro vertical exacto
    box_center_y = y0 + pad + rect_h / 2.0
    dy = 5.4 * mm # Paso entre líneas
    
    for i, (text, fsize) in enumerate(lines):
        line_offset = (3 - i) * dy
        # Ajuste óptico de línea de base para Impact
        target_y = box_center_y + line_offset - 0.35 * (fsize * 0.3528 * mm)
        c.setFont(FONT_NAME, fsize)
        c.drawCentredString(center_x, target_y, text)

def build_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    page_w, page_h = letter
    
    sticker_size = 60.0 * mm
    cols = 3
    rows = 4
    
    grid_w = cols * sticker_size
    grid_h = rows * sticker_size
    
    margin_x = (page_w - grid_w) / 2.0
    margin_y = (page_h - grid_h) / 2.0
    
    # -------------------------------------------------------------
    # PÁGINA 1: Planilla Completa (12 stickers: 3 cols x 4 filas)
    # -------------------------------------------------------------
    # Encabezado técnico exterior a la cuadrícula de corte
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(0.3, 0.35, 0.4)
    header_text = "CCCD 2026 | CAT 3: PDA ROCKETEERS (ID 310) — PLANILLA DE 12 STICKERS (6x6 cm)"
    c.drawString(margin_x, page_h - margin_y + 4 * mm, header_text)
    
    c.setFont("Helvetica", 6.8)
    instruc = "Configuración de impresión: Hoja Carta (Letter) | Escala 100% / Tamaño Real (No ajustar a página)"
    c.drawRightString(margin_x + grid_w, page_h - margin_y + 4 * mm, instruc)
    
    for r in range(rows):
        for col in range(cols):
            x = margin_x + col * sticker_size
            # r=0 es la fila superior
            y = margin_y + (rows - 1 - r) * sticker_size
            draw_single_sticker(c, x, y, show_cut_guide=True, is_isolated=False)
            
    c.showPage()
    
    # -------------------------------------------------------------
    # PÁGINA 2: Planilla Media (6 stickers: 3 cols x 2 filas)
    # -------------------------------------------------------------
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColorRGB(0.3, 0.35, 0.4)
    c.drawString(margin_x, page_h - margin_y + 4 * mm, "CCCD 2026 | CAT 3: PDA ROCKETEERS (ID 310) — MEDIA HOJA (6 STICKERS 6x6 cm)")
    c.setFont("Helvetica", 6.8)
    c.drawRightString(margin_x + grid_w, page_h - margin_y + 4 * mm, instruc)
    
    for r in range(2): # Solo 2 filas superiores
        for col in range(cols):
            x = margin_x + col * sticker_size
            y = margin_y + (rows - 1 - r) * sticker_size
            draw_single_sticker(c, x, y, show_cut_guide=True, is_isolated=False)
            
    c.showPage()

    # -------------------------------------------------------------
    # PÁGINA 3: Sticker Individual 6x6 cm Centrado con marcas de corte
    # -------------------------------------------------------------
    single_x = (page_w - sticker_size) / 2.0
    single_y = (page_h - sticker_size) / 2.0
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(0.2, 0.25, 0.3)
    c.drawCentredString(page_w / 2.0, single_y + sticker_size + 12 * mm, "STICKER INDIVIDUAL OFICIAL CAT 3 (6 x 6 cm)")
    
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(0.4, 0.45, 0.5)
    c.drawCentredString(page_w / 2.0, single_y + sticker_size + 7 * mm, "Dimensiones exactas: 60.0 x 60.0 mm | Imprimir al 100% en hoja adhesiva Carta")
    
    draw_single_sticker(c, single_x, single_y, show_cut_guide=True, is_isolated=True)
    
    c.showPage()
    c.save()
    print(f"PDF generado exitosamente en: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.abspath("Categoria_3_PDA_Rocketeers/Stickers_Cat3_PDA_Rocketeers_6x6cm.pdf")
    build_pdf(out_pdf)
    
    # Generar renders PNG para validación gráfica inmediata
    doc = fitz.open(out_pdf)
    
    # 1. Render de la página completa de 12 stickers (150 DPI para visualización ágil)
    pix_sheet = doc[0].get_pixmap(dpi=150)
    pix_sheet.save("Categoria_3_PDA_Rocketeers/Hoja_Impresion_Stickers_Cat3_12x.png")
    
    # 2. Render de alta resolución del sticker individual (300 DPI nítido para uso directo)
    # Extraemos el sticker individual de la página 3 recortando el área
    p3 = doc[2]
    # Bounding box del sticker centrado en pt
    page_w, page_h = letter
    size_pt = 60.0 * mm
    sx = (page_w - size_pt) / 2.0
    sy = (page_h - size_pt) / 2.0
    # En PyMuPDF el origen Y es arriba
    rect = fitz.Rect(sx - 15, page_h - (sy + size_pt) - 15, sx + size_pt + 15, page_h - sy + 15)
    pix_single = p3.get_pixmap(dpi=300, clip=rect)
    pix_single.save("Categoria_3_PDA_Rocketeers/Sticker_Individual_Cat3_6x6cm.png")
    
    print("Renders de validación PNG generados con éxito.")

