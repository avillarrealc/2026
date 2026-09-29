import sys
import subprocess

try:
    from fpdf import FPDF
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 13)
        self.cell(0, 10, 'Protocolo CAD - Carga Util Cautiva CanSat (CCCD Cat 3)', 0, 1, 'C')
        self.ln(3)

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 10)

text = """
FASE 1: Modelado del Nucleo (Perfil Escalonado)

1. Boceto 2D Maestro (Plano Frontal XZ/YZ):
   * Dibuje una linea vertical de 115 mm partiendo del origen (Sera el Eje Z).
   * Trace el perfil derecho (la mitad) del CanSat anclado a ese eje. Asegure las 
     siguientes cotas (Altura "Y" y Radio "X"):
     - Tope de Agarre: Altura = 15 mm. Radio = 33 mm (Generara OD 66 mm).
     - Pista Rosca Sup: Altura = 10 mm. Radio = 32 mm (Generara OD 64 mm).
     - Cuello Central: Altura = 80 mm. Radio = 29 mm (Generara OD 58 mm).
     - Pista Rosca Inf: Altura = 10 mm. Radio = 32 mm (Generara OD 64 mm).
   * Verifique que el contorno este cerrado y finalice el boceto (Finish Sketch).

2. Revolucion Base:
   * Vaya a Create > Revolve. Seleccione el perfil escalonado.
   * Seleccione la linea de 115 mm como Eje (Axis). 
   * Configurado a 360 grados, Operacion: New Body. Presione OK.

3. Inyeccion de Roscas (Sincronizadas):
   * Vaya a Create > Thread.
   * Seleccione UNICAMENTE las dos caras cilindricas de 64 mm de diametro.
   * Marque la casilla "Modeled" (Obligatorio).
   * Thread Type: ISO Metric Trapezoidal Threads.
   * Tamano: 64.0 mm. Designacion: Tr64x4 (Paso de 4mm). Presione OK.

4. Vaciado Estructural (Shell):
   * Vaya a Modify > Shell. Seleccione la cara circular plana de arriba y la de abajo.
   * Ingrese el grosor de pared: 1.5 mm. (El CanSat quedara hueco internamente).


FASE 2: Matrices de Acople (Sustraccion Booleana)

1. Extrusion de Anillos Base (Evasion de Proyeccion):
   * Vaya a Construct > Offset Plane. Haga clic en la cara plana donde finaliza la rosca superior y mueva el plano 5 mm hacia arriba (alejandose de la rosca). OK.
   * Cree un boceto en este nuevo plano flotante (asi evita que el CAD contamine el dibujo).
   * Dibuje el diametro interior de 58 mm (obligatorio) y el diametro exterior de su tubo contenedor del cohete.
   * Ejecute Extrude por 15 mm (bajando hasta cubrir la pista roscada). Operacion: New Component.
   * Repita el proceso para el anillo inferior.

2. Transferencia de Hilos (Combine Cut):
   * Vaya a Modify > Combine.
   * Target Body: Seleccione el Anillo Superior.
   * Tool Body: Seleccione el CanSat.
   * Operation: Elija Cut.
   * REQUISITO INELUDIBLE: Marque "Keep Tools". Presione OK. 
   * Repita la operacion exacta para el Anillo Inferior.


FASE 3: Tolerancias de Ensamblaje FDM

1. Holgura de Friccion (Offset Face):
   * Oculte los anillos de centrado en su arbol de trabajo.
   * Vaya a Modify > Offset Face.
   * Seleccione TODAS las caras helicoidales (flancos y valles) de ambas roscas 
     externas del CanSat.
   * Ingrese el valor: -0.20 mm. Esto garantiza el deslizamiento suave del polimero.

2. Guias de Rampa (Chamfer):
   * Vaya a Modify > Chamfer. Aplique un chaflan de 1.5 mm a los inicios de los hilos.

FASE 4: Esqueletizacion y Ventilacion (Corte Tipografico PDA)

1. Plano de Proyeccion:
   * Vaya a Construct > Tangent Plane.
   * Haga clic en el cuello liso central del CanSat. Deje el Angulo en 0.0 y presione OK.

2. Trazado de Ventanas:
   * Vaya a Create > Create Sketch y seleccione el nuevo plano tangente naranja.
   * Vaya a Create > Text y dibuje un cuadro a lo largo de la zona lisa.
   * En el cuadro de texto, digite 'P' (Enter), 'D' (Enter), 'A'.
   * OBLIGATORIO: Cambie la fuente a una tipo 'Stencil' (Ej. Black Ops One, Allerta Stencil, Army) para garantizar que las islas centrales no colapsen al imprimir.
   * Ajuste la altura (ej. 15mm) para que el texto encaje en el area libre. Termine el boceto.

3. Sustraccion Radial (Emboss Cut):
   * Vaya a Create > Emboss.
   * Profiles: Seleccione el texto PDA.
   * Faces: Seleccione la cara cilindrica lisa del CanSat.
   * Effect: Seleccione el SEGUNDO icono 'Deboss' (Hacia adentro / Grabado).
   * Depth: Digite -2.0 mm (Garantiza que la cuchilla atraviese la pared de 1.5 mm).
   * Presione OK.

FASE 5: Exoesqueleto Estructural (Matriz Hexagonal Panal de Abejas)

1. Corte Semilla (Seed Cut):
   * Cree un boceto en un plano de origen lateral (YZ o XY) para mirar el CanSat de lado.
   * Vaya a Create > Polygon > Circumscribed Polygon. Dibuje un hexagono (ej. 12mm de diametro).
   * Presione 'E' (Extrude), seleccione el hexagono y ejecute un corte (Cut) que atraviese SOLO la pared del CanSat que tiene al frente (sin pasar de lado a lado).

2. Matriz Radial Inteligente (Circular Pattern):
   * Vaya a Create > Pattern > Circular Pattern.
   * Type: Cambie el parametro a 'Features' (Operaciones).
   * Objects: Haga clic en la extrusion del hexagono en su linea de tiempo inferior.
   * Axis: Seleccione la pared curva del CanSat. 
   * Quantity: Aumente el numero (ej. 10) hasta rodear el cilindro.
   * TRUCO DE SUPRESION: Apague (haciendo clic) los cuadros de verificacion (checkmarks) sobre los hexagonos fantasmas que colisionen o toquen su texto PDA. Presione OK.

3. Multiplicacion en Altura (Rectangular Pattern):
   * Vaya a Create > Pattern > Rectangular Pattern.
   * Type: 'Features'. Seleccione el Patron Circular en su linea de tiempo.
   * Axis: Seleccione el Eje Z (la linea vertical azul del origen).
   * Jale la flecha hacia arriba/abajo. Configure la Cantidad de pisos (niveles) y ajuste la Distancia para llenar el area lisa libre. Presione OK.
"""

pdf.multi_cell(0, 5, text.encode('latin-1', 'replace').decode('latin-1'))

output_file = 'd:/Documentos/IEJAGA/2026/PDA/CCCD2026/Categoria_3_PDA_Rocketeers/Protocolo_CAD_CanSat.pdf'
pdf.output(output_file)
print(f"PDF successfully generated at: {output_file}")
