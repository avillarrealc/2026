import os
import sys
import ezdxf
from ezdxf import path
import pymupdf as fitz

MM_TO_PT = 72.0 / 25.4  # 1 mm = 2.834645669... pt

def get_dxf_geometry(dxf_path):
    doc_dxf = ezdxf.readfile(dxf_path)
    msp = doc_dxf.modelspace()
    
    all_paths = []
    for e in msp:
        try:
            p = path.make_path(e)
            if len(p) > 0:
                all_paths.append(p)
        except Exception as ex:
            print(f"Ignorando entidad {e.dxftype()}: {ex}")
            
    bboxes = [p.bbox() for p in all_paths]
    min_x = min(b.extmin[0] for b in bboxes)
    min_y = min(b.extmin[1] for b in bboxes)
    max_x = max(b.extmax[0] for b in bboxes)
    max_y = max(b.extmax[1] for b in bboxes)
    
    return all_paths, min_x, min_y, max_x, max_y

def render_paths_to_shape(shape, all_paths, to_pdf_pt_fn):
    for p in all_paths:
        curr = p.start
        for cmd in p:
            if 'LineTo' in str(type(cmd)):
                p0 = to_pdf_pt_fn(curr.x, curr.y)
                p1 = to_pdf_pt_fn(cmd.end.x, cmd.end.y)
                shape.draw_line(p0, p1)
                curr = cmd.end
            elif 'Curve4To' in str(type(cmd)):
                p0 = to_pdf_pt_fn(curr.x, curr.y)
                p1 = to_pdf_pt_fn(cmd.ctrl1.x, cmd.ctrl1.y)
                p2 = to_pdf_pt_fn(cmd.ctrl2.x, cmd.ctrl2.y)
                p3 = to_pdf_pt_fn(cmd.end.x, cmd.end.y)
                shape.draw_bezier(p0, p1, p2, p3)
                curr = cmd.end

def generate_pliego_a2(all_paths, min_x, min_y, max_x, max_y, output_pdf_path):
    geom_w = max_x - min_x
    geom_h = max_y - min_y
    
    page_w_mm = 420.0  # A2
    page_h_mm = 594.0
    
    page_w_pt = page_w_mm * MM_TO_PT
    page_h_pt = page_h_mm * MM_TO_PT
    
    # Centrar horizontalmente y dejar espacio inferior para rótulo
    offset_x = (page_w_mm - geom_w) / 2.0 - min_x
    offset_y = 70.0 - min_y
    
    def to_pdf_pt(x_mm, y_mm):
        px = (x_mm + offset_x) * MM_TO_PT
        py = (page_h_mm - (y_mm + offset_y)) * MM_TO_PT
        return fitz.Point(px, py)

    pdf_doc = fitz.open()
    page = pdf_doc.new_page(width=page_w_pt, height=page_h_pt)
    
    # Geometría DXF en trazo fino de corte (0.6 pt)
    shape = page.new_shape()
    render_paths_to_shape(shape, all_paths, to_pdf_pt)
    shape.finish(color=(0, 0, 0), width=0.6, stroke_opacity=1.0)
    shape.commit()
    
    # Rótulos y regla de calibración
    annot = page.new_shape()
    # Marco exterior
    annot.draw_rect(fitz.Rect(10.0 * MM_TO_PT, 10.0 * MM_TO_PT, (page_w_mm - 10.0) * MM_TO_PT, (page_h_mm - 10.0) * MM_TO_PT))
    
    # Regla 100 mm
    ruler_x0_mm = 30.0
    ruler_y0_mm = 30.0
    r0 = fitz.Point(ruler_x0_mm * MM_TO_PT, (page_h_mm - ruler_y0_mm) * MM_TO_PT)
    r1 = fitz.Point((ruler_x0_mm + 100.0) * MM_TO_PT, (page_h_mm - ruler_y0_mm) * MM_TO_PT)
    annot.draw_line(r0, r1)
    for i in range(11):
        tx = ruler_x0_mm + i * 10.0
        th = 5.0 if i in (0, 5, 10) else 3.0
        annot.draw_line(fitz.Point(tx * MM_TO_PT, (page_h_mm - ruler_y0_mm) * MM_TO_PT),
                        fitz.Point(tx * MM_TO_PT, (page_h_mm - (ruler_y0_mm + th)) * MM_TO_PT))
    
    annot.finish(color=(0.1, 0.2, 0.5), width=0.8)
    annot.commit()
    
    for i in range(11):
        tx = ruler_x0_mm + i * 10.0
        page.insert_text(fitz.Point((tx - 1.5) * MM_TO_PT, (page_h_mm - (ruler_y0_mm - 4.0)) * MM_TO_PT),
                         f"{i}", fontsize=7, color=(0.1, 0.2, 0.5))
                         
    page.insert_text(fitz.Point(ruler_x0_mm * MM_TO_PT, (page_h_mm - (ruler_y0_mm + 8.5)) * MM_TO_PT),
                     "REGLA DE CALIBRACIÓN: ESTE SEGMENTO DEBE MEDIR EXACTAMENTE 100 mm (10.0 cm)",
                     fontsize=8, fontname="helv", color=(0.1, 0.2, 0.5))
                     
    rotulo_x = 180.0
    rotulo_y = 48.0
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - rotulo_y) * MM_TO_PT),
                     "CCCD 2026 | PDA ROCKETEERS (CAT 3) - COHETE SIDERAL",
                     fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - (rotulo_y - 6)) * MM_TO_PT),
                     f"Plano de Corte 1:1 - Aletas y Anillos | Hoja: A2 ({page_w_mm:.0f} x {page_h_mm:.0f} mm)",
                     fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - (rotulo_y - 11)) * MM_TO_PT),
                     f"Dimensiones de conjunto: {geom_w:.1f} x {geom_h:.1f} mm | Escala estricta: 1:1",
                     fontsize=8.5, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - (rotulo_y - 16)) * MM_TO_PT),
                     "AVISO: Imprimir al 100% / Tamaño real. NO usar 'Ajustar a página'.",
                     fontsize=8, fontname="hebo", color=(0.8, 0.1, 0.1))
                     
    pdf_doc.save(output_pdf_path)
    pdf_doc.close()
    print(f"[OK] Generado Pliego A2: {output_pdf_path}")
    return offset_x, offset_y, page_w_mm, page_h_mm

def generate_mosaico_carta_from_pliego(pliego_pdf_path, min_x, min_y, max_x, max_y, offset_x, offset_y, page_h_mm, output_pdf_path):
    doc_pliego = fitz.open(pliego_pdf_path)
    
    geom_w = max_x - min_x
    geom_h = max_y - min_y
    
    pliego_geom_x0_pt = (min_x + offset_x) * MM_TO_PT
    pliego_geom_y0_pt = (page_h_mm - (max_y + offset_y)) * MM_TO_PT
    
    carta_w_mm = 215.9
    carta_h_mm = 279.4
    
    carta_w_pt = carta_w_mm * MM_TO_PT
    carta_h_pt = carta_h_mm * MM_TO_PT
    
    overlap_mm = 18.0
    overlap_pt = overlap_mm * MM_TO_PT
    
    tile_w_mm = 176.0
    tile_w_pt = tile_w_mm * MM_TO_PT
    step_x_pt = tile_w_pt - overlap_pt
    
    tile_h_mm = 224.0
    tile_h_pt = tile_h_mm * MM_TO_PT
    step_y_pt = tile_h_pt - overlap_pt
    
    target_x0 = (carta_w_pt - tile_w_pt) / 2.0
    target_y0 = (carta_h_pt - tile_h_pt) / 2.0
    target_rect = fitz.Rect(target_x0, target_y0, target_x0 + tile_w_pt, target_y0 + tile_h_pt)
    
    doc_carta = fitz.open()
    
    page_configs = [
        {"row": 0, "col": 0, "name": "Hoja 1 de 4 [Superior Izquierda]"},
        {"row": 0, "col": 1, "name": "Hoja 2 de 4 [Superior Derecha]"},
        {"row": 1, "col": 0, "name": "Hoja 3 de 4 [Inferior Izquierda]"},
        {"row": 1, "col": 1, "name": "Hoja 4 de 4 [Inferior Derecha]"},
    ]
    
    for cfg in page_configs:
        page = doc_carta.new_page(width=carta_w_pt, height=carta_h_pt)
        
        r = cfg["row"]
        c = cfg["col"]
        
        src_x0 = pliego_geom_x0_pt + c * step_x_pt
        src_y0 = pliego_geom_y0_pt + r * step_y_pt
        src_rect = fitz.Rect(src_x0, src_y0, src_x0 + tile_w_pt, src_y0 + tile_h_pt)
        
        page.show_pdf_page(target_rect, doc_pliego, 0, clip=src_rect)
        
        guides = page.new_shape()
        guides.draw_rect(target_rect)
        
        # Línea de solape vertical
        if c == 0:
            cut_x = target_rect.x1 - overlap_pt
            guides.draw_line(fitz.Point(cut_x, target_rect.y0), fitz.Point(cut_x, target_rect.y1))
        else:
            cut_x = target_rect.x0 + overlap_pt
            guides.draw_line(fitz.Point(cut_x, target_rect.y0), fitz.Point(cut_x, target_rect.y1))
            
        # Línea de solape horizontal
        if r == 0:
            cut_y = target_rect.y1 - overlap_pt
            guides.draw_line(fitz.Point(target_rect.x0, cut_y), fitz.Point(target_rect.x1, cut_y))
        else:
            cut_y = target_rect.y0 + overlap_pt
            guides.draw_line(fitz.Point(target_rect.x0, cut_y), fitz.Point(target_rect.x1, cut_y))
            
        guides.finish(color=(0.2, 0.3, 0.7), dashes="[4 3] 0", width=0.6)
        guides.commit()
        
        # Regla de prueba de 50 mm
        ruler = page.new_shape()
        rx0_pt = 20.0 * MM_TO_PT
        ry0_pt = carta_h_pt - (10.0 * MM_TO_PT)
        ruler.draw_line(fitz.Point(rx0_pt, ry0_pt), fitz.Point(rx0_pt + 50.0 * MM_TO_PT, ry0_pt))
        for i in range(6):
            tx = rx0_pt + i * 10.0 * MM_TO_PT
            th = 4.0 * MM_TO_PT if i in (0, 5) else 2.5 * MM_TO_PT
            ruler.draw_line(fitz.Point(tx, ry0_pt), fitz.Point(tx, ry0_pt - th))
        ruler.finish(color=(0.8, 0.1, 0.1), width=0.7)
        ruler.commit()
        
        page.insert_text(fitz.Point(rx0_pt, ry0_pt - 5.0 * MM_TO_PT),
                         "TEST 50 mm (5.0 cm) - Medir con regla tras imprimir",
                         fontsize=6.5, fontname="hebo", color=(0.8, 0.1, 0.1))
                         
        # Encabezado limpio
        page.insert_text(fitz.Point(18.0 * MM_TO_PT, 14.0 * MM_TO_PT),
                         f"CCCD 2026 SIDERAL | {cfg['name']} - Escala 1:1",
                         fontsize=8, fontname="hebo", color=(0.1, 0.1, 0.1))
        page.insert_text(fitz.Point(carta_w_pt - 180.0, 14.0 * MM_TO_PT),
                         "IMPRIMIR EN 'TAMAÑO REAL' (100%)",
                         fontsize=7.5, fontname="hebo", color=(0.8, 0.1, 0.1))
                         
        # Textos de solape en el centro del margen de unión
        mid_y = (target_rect.y0 + target_rect.y1) / 2.0
        if c == 0:
            page.insert_text(fitz.Point(target_rect.x1 - overlap_pt + 4, mid_y + 40),
                             "Línea de unión (Solapar con Hoja 2) ->",
                             fontsize=6, fontname="helv", color=(0.2, 0.3, 0.7), rotate=90)
        else:
            page.insert_text(fitz.Point(target_rect.x0 + 4, mid_y + 40),
                             "<- Borde de unión con Hoja 1",
                             fontsize=6, fontname="helv", color=(0.2, 0.3, 0.7), rotate=90)
                             
        if r == 0:
            page.insert_text(fitz.Point(target_rect.x0 + 40, target_rect.y1 - overlap_pt + 11),
                             "v Línea de solape (Unir con fila inferior) v",
                             fontsize=6, fontname="helv", color=(0.2, 0.3, 0.7))
        else:
            page.insert_text(fitz.Point(target_rect.x0 + 40, target_rect.y0 + 11),
                             "^ Borde de solape (Unir con fila superior) ^",
                             fontsize=6, fontname="helv", color=(0.2, 0.3, 0.7))
                             
    doc_carta.save(output_pdf_path)
    doc_carta.close()
    doc_pliego.close()
    print(f"[OK] Generado Mosaico Carta optimizado: {output_pdf_path}")

if __name__ == "__main__":
    dxf_input = r"D:\Descargas\Aletas y anillos.dxf"
    pdf_pliego = r"D:\Descargas\Aletas_y_anillos_Escala_1a1_Pliego_A2.pdf"
    pdf_mosaico = r"D:\Descargas\Aletas_y_anillos_Escala_1a1_Mosaico_Carta_4_Hojas.pdf"
    
    paths, min_x, min_y, max_x, max_y = get_dxf_geometry(dxf_input)
    print(f"Dimensiones DXF detectadas: {max_x - min_x:.2f} mm x {max_y - min_y:.2f} mm")
    
    off_x, off_y, pw, ph = generate_pliego_a2(paths, min_x, min_y, max_x, max_y, pdf_pliego)
    generate_mosaico_carta_from_pliego(pdf_pliego, min_x, min_y, max_x, max_y, off_x, off_y, ph, pdf_mosaico)
