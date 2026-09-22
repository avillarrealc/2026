import sys
sys.path.append(r'C:\Users\SERVIDOR\AppData\Roaming\Python\Python314\site-packages')
import pandas as pd
from fpdf import FPDF

file_path = 'd:/Documentos/IEJAGA/2026/PDA/CCCD2026/Presupuesto_y_Relacion_de_Gastos_CCCD2026.xlsx'

df = pd.read_excel(file_path, sheet_name='PRESUPUESTO', header=3)

# Find columns
cols = df.columns.astype(str).tolist()

item_col = next((c for c in cols if 'item' in c.lower() or 'ítem' in c.lower() or 'tem' in c.lower()), None)
detalle_col = next((c for c in cols if 'descrip' in c.lower() or 'detalle' in c.lower() or 'art' in c.lower()), None)
cantidad_col = next((c for c in cols if 'cant' in c.lower()), None)
total_col = next((c for c in cols if 'total' in c.lower()), None)

# Fallbacks if not found
if not detalle_col:
    detalle_col = cols[1] if len(cols) > 1 else None
if not cantidad_col:
    cantidad_col = cols[2] if len(cols) > 2 else None
if not total_col:
    total_col = next((c for c in cols if 'valor' in c.lower() and 'total' not in c.lower()), None)
    
if not all([item_col, detalle_col, cantidad_col, total_col]):
    print(f"Error finding columns. Found: {item_col}, {detalle_col}, {cantidad_col}, {total_col}")
    print(f"All columns: {cols}")
    sys.exit(1)

# Drop rows where 'Detalle' or 'Total' is NaN, or 'Total' is not a number
df = df.dropna(subset=[detalle_col])
# Convert 'Total' to numeric, errors='coerce' to turn text into NaN, then drop NaNs
df[total_col] = pd.to_numeric(df[total_col], errors='coerce')
df = df.dropna(subset=[total_col])

# Create PDF
class PDF(FPDF):
    def header(self):
        # Logo / Club Identification
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 153) # Dark Blue
        self.cell(0, 10, 'PDA CLUB', 0, 1, 'C')
        
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'CCCD 2026', 0, 1, 'C')
        self.ln(2)
        
        self.set_font('Arial', '', 10)
        intro_text = "Este presupuesto está diseñado para cubrir los gastos de participación de la delegación en el Concurso Colombiano de Cohetería Deportiva (CCCD 2026), evento que se llevará a cabo en Santa Fe de Antioquia del 6 al 8 de Noviembre de 2026. Cubre la logística y desarrollo de los tres equipos: PDA Noctux, PDA Stars y PDA Rocketeers."
        # Encoding for FPDF compatibility with accents
        intro_text = intro_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 5, intro_text, 0, 'J')
        self.ln(5)
        
        # Header Row
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(0, 51, 153) # Dark Blue background
        self.set_text_color(255, 255, 255) # White text
        self.cell(15, 10, 'Item', 1, 0, 'C', 1)
        self.cell(105, 10, 'Detalle', 1, 0, 'C', 1)
        self.cell(20, 10, 'Cant', 1, 0, 'C', 1)
        self.cell(50, 10, 'Total', 1, 0, 'C', 1)
        self.ln()

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 9)

fill = False
pdf.set_fill_color(240, 248, 255) # Alice Blue for alternating rows
pdf.set_text_color(0, 0, 0)

grand_total = 0.0

for index, row in df.iterrows():
    item = str(row[item_col]) if not pd.isna(row[item_col]) else ""
    detalle = str(row[detalle_col])[:60] # Truncate if too long
    cant = str(row[cantidad_col]) if not pd.isna(row[cantidad_col]) else ""
    
    # Format total as currency
    try:
        total_val = float(row[total_col])
        total = f"${total_val:,.0f}"
        grand_total += total_val
    except:
        total = str(row[total_col])
    
    pdf.cell(15, 8, item, 1, 0, 'C', fill)
    pdf.cell(105, 8, detalle, 1, 0, 'L', fill)
    pdf.cell(20, 8, cant, 1, 0, 'C', fill)
    pdf.cell(50, 8, total, 1, 0, 'R', fill)
    pdf.ln()
    fill = not fill

# Print Grand Total Row
pdf.set_font('Arial', 'B', 10)
pdf.set_fill_color(200, 200, 200)
pdf.cell(140, 10, 'GRAN TOTAL', 1, 0, 'R', 1)
pdf.cell(50, 10, f"${grand_total:,.0f}", 1, 0, 'R', 1)
pdf.ln()

output_file = 'd:/Documentos/IEJAGA/2026/PDA/CCCD2026/Presupuesto_Resumido.pdf'
pdf.output(output_file)
print(f"PDF successfully generated at: {output_file}")
