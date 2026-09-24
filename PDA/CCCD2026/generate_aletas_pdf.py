import sys
sys.path.append(r'C:\Users\SERVIDOR\AppData\Roaming\Python\Python314\site-packages')
from fpdf import FPDF

# Datos para la tabla
data = [
    {
        "categoria": "Categoria 1",
        "material": "Triplex Okume / Pino (2mm) + Laminado con Papel Kraft (Papering)",
        "aplicacion": "Coheteria de baja potencia. Sin uso de composites.",
        "tienda": "La Tienda del Triplex\nhttps://latiendadeltriplex.com",
        "montaje": "Cortar aleta en triplex, lijar perfil aerodinamico. Aplicar pegamento PVA (Colbon) diluido y adherir papel Kraft/cartulina prensando entre superficies planas."
    },
    {
        "categoria": "Categoria 2",
        "material": "Triplex Okume / Pino (4mm) - Madera Sellada",
        "aplicacion": "Coheteria de potencia Categoría 2 (Motor F). Restriccion: Sin fibras de refuerzo.",
        "tienda": "La Tienda del Triplex\nMonomerados",
        "montaje": "Cortar en triplex calibre 4mm. Lijar perfil aerodinamico. Sellar madera con resina pura o laca (sin tela) y pegar con filetes epoxicos al fuselaje."
    },
    {
        "categoria": "Categoria 3",
        "material": "Nucleo de Balso Aeromodelismo (2-3mm) + Pieles Fibra de Carbono",
        "aplicacion": "Coheteria de potencia Categoría 3 (Motor G). Maxima rigidez requerida.",
        "tienda": "Manolos Hobbies\nhttps://manoloshobbies.com\nKYM RC Models",
        "montaje": "Lijar perfil aerodinamico en balso crudo. Pegar al tubo. Laminado tip-to-tip envolvente usando tela de fibra de carbono para crear un sandwich estructural ligero."
    }
]

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 153)
        self.cell(0, 10, 'REPORTE TECNICO DE ALETAS - CCCD 2026', 0, 1, 'C')
        self.ln(5)
        
        # Table Header
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(0, 51, 153)
        self.set_text_color(255, 255, 255)
        self.cell(25, 10, 'Categoria', 1, 0, 'C', 1)
        self.cell(55, 10, 'Material', 1, 0, 'C', 1)
        self.cell(50, 10, 'Aplicacion', 1, 0, 'C', 1)
        self.cell(45, 10, 'Tienda (URL)', 1, 0, 'C', 1)
        self.cell(100, 10, 'Descripcion de Montaje', 1, 0, 'C', 1)
        self.ln()

pdf = PDF('L', 'mm', 'A4')  # Landscape
pdf.add_page()
pdf.set_font('Arial', '', 9)

# Draw rows
pdf.set_fill_color(240, 248, 255)
fill = False
pdf.set_text_color(0, 0, 0)

col_widths = [25, 55, 50, 45, 100]

def draw_row(row_data, fill):
    # Calculate row height based on the maximum number of lines in multi_cell
    # We create a dummy pdf just to count lines
    lines = 1
    for i, text in enumerate(row_data):
        # fpdf get_string_width doesn't easily translate to lines, so we estimate
        text_length = pdf.get_string_width(text)
        est_lines = int(text_length / (col_widths[i] - 2)) + 1
        # count explicit newlines
        est_lines += text.count('\n')
        if est_lines > lines:
            lines = est_lines
            
    row_height = lines * 5 + 4
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    
    for i, text in enumerate(row_data):
        pdf.set_xy(x_start, y_start)
        pdf.rect(x_start, y_start, col_widths[i], row_height, 'DF' if fill else 'D')
        pdf.set_xy(x_start, y_start + 2)
        pdf.multi_cell(col_widths[i], 5, text, 0, 'L')
        x_start += col_widths[i]
        
    pdf.set_xy(10, y_start + row_height)

for item in data:
    row = [
        item["categoria"],
        item["material"],
        item["aplicacion"],
        item["tienda"],
        item["montaje"]
    ]
    draw_row(row, fill)
    fill = not fill

output_file = 'd:/Documentos/IEJAGA/2026/PDA/CCCD2026/Aletas.pdf'
pdf.output(output_file)
print(f"PDF generado: {output_file}")
