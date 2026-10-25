import os
import sys
import ezdxf
from ezdxf import path
import pymupdf as fitz

MM_TO_PT = 72.0 / 25.4  # 1 mm = 2.834645669... pt

def dxf_to_pdf_single_page(dxf_path, output_pdf_path):
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
    
    geom_w = max_x - min_x
    geom_h = max_y - min_y
    print(f"Dimensiones DXF detectadas: {geom_w:.2f} mm x {geom_h:.2f} mm")
    print(f"Bounds: X=[{min_x:.2f}, {max_x:.2f}], Y=[{min_y:.2f}, {max_y:.2f}]")
    
    # Formato A2 estándar (420 x 594 mm)
    page_w_mm = 420.0
    page_h_mm = 594.0
    
    page_w_pt = page_w_mm * MM_TO_PT
    page_h_pt = page_h_mm * MM_TO_PT
    
    # Centrar horizontalmente y dejar espacio inferior para rótulo y regla
    offset_x = (page_w_mm - geom_w) / 2.0 - min_x
    offset_y = 70.0 - min_y
    
    def to_pdf_pt(x_mm, y_mm):
        px = (x_mm + offset_x) * MM_TO_PT
        py = (page_h_mm - (y_mm + offset_y)) * MM_TO_PT
        return fitz.Point(px, py)

    pdf_doc = fitz.open()
    page = pdf_doc.new_page(width=page_w_pt, height=page_h_pt)
    
    # Trazo vectorial del dibujo
    shape = page.new_shape()
    for p in all_paths:
        curr = p.start
        for cmd in p:
            if 'LineTo' in str(type(cmd)):
                p0 = to_pdf_pt(curr.x, curr.y)
                p1 = to_pdf_pt(cmd.end.x, cmd.end.y)
                shape.draw_line(p0, p1)
                curr = cmd.end
            elif 'Curve4To' in str(type(cmd)):
                p0 = to_pdf_pt(curr.x, curr.y)
                p1 = to_pdf_pt(cmd.ctrl1.x, cmd.ctrl1.y)
                p2 = to_pdf_pt(cmd.ctrl2.x, cmd.ctrl2.y)
                p3 = to_pdf_pt(cmd.end.x, cmd.end.y)
                shape.draw_bezier(p0, p1, p2, p3)
                curr = cmd.end
                
    shape.finish(color=(0, 0, 0), width=0.6, stroke_opacity=1.0)
    shape.commit()
    
    # Rótulo técnico, marco y regla de verificación
    annot = page.new_shape()
    # Marco exterior (margen 10 mm)
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
                     f"Plano de Corte 1:1 - Anillos y Componentes Finales | Hoja: A2 ({page_w_mm:.0f} x {page_h_mm:.0f} mm)",
                     fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - (rotulo_y - 11)) * MM_TO_PT),
                     f"Dimensiones de conjunto: {geom_w:.1f} x {geom_h:.1f} mm | Escala estricta: 1:1",
                     fontsize=8.5, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(fitz.Point(rotulo_x * MM_TO_PT, (page_h_mm - (rotulo_y - 16)) * MM_TO_PT),
                     "AVISO: Imprimir al 100% / Tamaño real. NO usar 'Ajustar a página'.",
                     fontsize=8, fontname="hebo", color=(0.8, 0.1, 0.1))
                     
    pdf_doc.save(output_pdf_path)
    pdf_doc.close()
    print(f"[OK] Generado PDF en una sola hoja (A2 1:1): {output_pdf_path}")

if __name__ == "__main__":
    dxf_input = r"D:\Descargas\Anilloso FINAL.dxf"
    pdf_output = r"D:\Descargas\Anilloso_FINAL_Escala_1a1_Pliego_A2.pdf"
    dxf_to_pdf_single_page(dxf_input, pdf_output)
