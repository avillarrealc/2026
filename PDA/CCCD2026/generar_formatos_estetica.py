import os
import docx

def generar_documento_estetica(nombre_equipo, id_equipo, respuestas, output_path):
    template_path = r'Documentos_Oficiales_Globales\Plantilla_Formato_Estetica_Cohete.docx'
    doc = docx.Document(template_path)
    
    # P6: Nombre del Equipo
    doc.paragraphs[6].runs[1].text = nombre_equipo
    
    # P8: Institución Educativa
    doc.paragraphs[8].runs[1].text = 'I.E. José Antonio Galán (La Estrella, Antioquia)'
    
    # P9: ID del Equipo
    doc.paragraphs[9].runs[1].text = str(id_equipo)
    
    # P13: Respuesta 1
    doc.paragraphs[13].text = respuestas[0]
    
    # P15: Respuesta 2
    doc.paragraphs[15].text = respuestas[1]
    
    # P17: Respuesta 3
    doc.paragraphs[17].text = respuestas[2]
    
    # P19: Respuesta 4
    doc.paragraphs[19].text = respuestas[3]
    
    # P21: Respuesta 5
    doc.paragraphs[21].text = respuestas[4]
    
    doc.save(output_path)
    print(f"Generado exitosamente: {output_path}")

# --- CAT 3: PDA ROCKETEERS (ID: 310) ---
respuestas_cat3 = [
    # 1. Concepto e inspiración
    "El vehículo suborbital 'SIDERAL' (propulsado por motor clase G80-7T) se inspira en la estética funcional de los vectores de exploración y cohetes sonda de investigación atmosférica de alta velocidad. Simboliza el hito histórico de una institución educativa pública de La Estrella (Antioquia) compitiendo con solvencia técnica en la categoría universitaria contra prestigiosas facultades de ingeniería aeroespacial del país. La línea estética proyecta elegancia aerodinámica, esbeltez, disciplina ingenieril y confiabilidad operativa para alcanzar un apogeo proyectado de ~400 metros a una velocidad máxima calculada de 92.5 m/s.",
    
    # 2. Significado del diseño
    "El esquema cromático y los elementos gráficos cumplen un propósito tanto técnico como identitario:\n"
    "• Blanco Aeroespacial Puro (Fuselaje y bahía de carga útil): Representa el rigor y la neutralidad científica. Técnicamente, proporciona alta reflectancia térmica solar en rampa para proteger la instrumentación CanSat (sensores EKF, ESP32-S3 y telemetría LoRa 915 MHz) del sobrecalentamiento.\n"
    "• Azul Medianoche / Galán (Aletas y sección de transición): Representa el cielo estratosférico profundo y los colores institucionales distintivos de la I.E. José Antonio Galán.\n"
    "• Acentos Naranja Internacional y Plata: Aplicados en el perímetro de eyección y puntas de aletas para maximizar la detectabilidad visual durante el descenso en paracaídas dentro de la zona de recuperación de 400 m.\n"
    "• Simbología y Rótulos Técnicos: Incorpora el parche oficial de misión SIDERAL, el emblema PDA Rocketeers, la bandera de Colombia, la rotulación visible del ID de Misión '310' en disposición vertical reglamentaria, y las marcas de Centro de Gravedad (CG) y Centro de Presión (CP) certificando el margen estático obligatorio (≥ 2.0 calibres).",
    
    # 3. Materiales y pintura
    "Se utilizaron materiales de grado aeroespacial y automotriz compatibles con los sustratos estructurales:\n"
    "• Sustratos base: Tubo de fuselaje de fibra de vidrio/epoxi de pared delgada, ojiva ogival manufacturada en filamento ASA (imperativo por su permeabilidad al 100% a radiofrecuencia para telemetría sin efecto jaula de Faraday) y aletas en sándwich de balsa aligerada con velo de fibra de vidrio y resina epoxi.\n"
    "• Acabado: Masilla plástica poliéster ultraliviana para sellado micrométrico de poros, imprimación fondo/primer epóxico bicapa gris claro lijable, esmalte acrílico poliuretano bicapa automotriz (alta resistencia a esfuerzos cortantes de fricción del aire) y laca protectora transparente de poliuretano 2K con filtro UV.\n"
    "• Herramientas: Papeles abrasivos de lijado en húmedo (granos 240, 400, 600 y 1000), aerógrafo de precisión de doble acción, pistola HVLP de retoque a baja presión y balanza analítica digital con resolución de 0.01 g para control estricto de masa (incremento acotado a Delta m <= 2.8 g).",
    
    # 4. Técnicas artísticas
    "Se aplicaron técnicas de acabado aeronáutico y detalle de taller:\n"
    "• Nivelación micrométrica de superficie mediante lijado progresivo al agua para suprimir por completo cualquier vestigio de capa FDM en la ojiva o textura de tejido en el fuselaje, optimizando el coeficiente de fricción de capa límite.\n"
    "• Enmascaramiento de alta definición con cinta automotriz de perfilado fino (fine-line tape), garantizando líneas de corte limpias y afiladas entre los paneles blancos y las franjas azul medianoche, sin sangrado de pigmento ni bordes escalonados.\n"
    "• Rotulación técnica y gráficos vectoriales troquelados en vinilo polimérico ultrafino de 50 micras, sellados bajo la capa final de barniz de poliuretano para evitar desprendimientos causados por la corriente de flujo transónico.",
    
    # 5. Identidad del equipo
    "El diseño de SIDERAL sintetiza la identidad y el lema del semillero PDA (Pequeños Científicos Galanistas - Proyecto de Desarrollo Aeroespacial) de la I.E. José Antonio Galán: 'La educación pública alcanza las estrellas mediante la ciencia rigurosa y el trabajo en equipo'. Refleja la audacia, disciplina y capacidad de jóvenes antioqueños que han superado todas las revisiones técnicas (PDR, CDR) ocupando puestos de liderazgo nacional, demostrando que la pasión por la cohetería espacial transforma vidas y entornos comunitarios."
]

# --- CAT 2: PDA STARS (ID: 211) ---
respuestas_cat2 = [
    # 1. Concepto e inspiración
    "El concepto estético de 'PDA STARS' (propulsado por motor clase F15-4) se inspira en la orientación celestial, la navegación estelar y la constelación de Orión. Simboliza la búsqueda del conocimiento guiada por estrellas y el brillo del talento juvenil en ciencia y tecnología. Su geometría y acabado visual transmiten dinamismo, velocidad y precisión aerodinámica para cumplir holgadamente la ventana reglamentaria de vuelo (40 a 50 s) y apogeo de 300 metros.",
    
    # 2. Significado del diseño
    "Cada componente cromático y gráfico responde a una función técnica y de pertenencia:\n"
    "• Azul Galaxia Intenso: Evoca la inmensidad del firmamento nocturno y rinde tributo a la identidad corporativa de la I.E. José Antonio Galán, transmitiendo seriedad y vocación investigativa.\n"
    "• Blanco Brillante de Alto Contraste: Otorga pulcritud visual y refleja la radiación solar en rampa, destacando las líneas maestras del fuselaje de 29 mm.\n"
    "• Destellos Dorados y Ámbar: Representan el brillo de las estrellas y el empuje de propulsión del motor clase F, aportando una alta visibilidad en fase de descenso que optimiza el avistamiento dentro del radio límite de recuperación de 250 m.\n"
    "• Simbología Técnica: Incorpora el emblema PDA Stars, la estela estilizada de una constelación, el ID de Misión '211' rotulado verticalmente en tipografía aeronáutica de 10 cm, y marcas visibles de CG y CP para verificación del margen estático normativo (≥ 2.0 calibres).",
    
    # 3. Materiales y pintura
    "Se emplearon materiales livianos con rigurosa compatibilidad química y control de peso:\n"
    "• Sustratos base: Tubo de fuselaje de cartón kraft de alta densidad y precisión dimensional (alojamiento de motor de 29 mm), ojiva parabólica en filamento PLA+ de alta tenacidad mecánica, aletas estabilizadoras en madera balsa tratada con sellador tapaporos.\n"
    "• Acabado: Aparejo acrílico automotriz lijable en aerosol, esmalte acrílico brillante bicapa de secado rápido y laca transparente de poliuretano para protección superficial.\n"
    "• Herramientas: Tacos de lijado de espuma suave con lijas al agua granos 320, 500 y 800, plantillas de aerografía y espátulas plásticas de fijación vinílica.",
    
    # 4. Técnicas artísticas
    "El proceso artístico-técnico incluyó:\n"
    "• Sellado integral de la superficie porosa de la balsa y las espirales del tubo mediante tres manos de imprimación acrílica con lijado intermedio, logrando una superficie completamente lisa tipo espejo (glass finish).\n"
    "• Enmascarado de corte curvo para generar franjas estilizadas que representan estelas de movimiento a lo largo del cuerpo del cohete.\n"
    "• Rotulación en vinilo de corte de alta adherencia con bordes biselados y pulido final con cera automotriz sintética para reducir la resistencia aerodinámica por fricción superficial (Cf).",
    
    # 5. Identidad del equipo
    "El cohete PDA STARS encarna la constancia, el rigor y la energía positiva de los estudiantes de secundaria técnica de La Estrella. Refleja su posicionamiento en el podio nacional de la Categoría Intermedios (#3 Nacional con 140 pts), demostrando que con método científico, trabajo colaborativo y creatividad artística es posible sobresalir en certámenes tecnológicos de alto impacto."
]

# --- CAT 1: PDA NOCTUX (ID: 104) ---
respuestas_cat1 = [
    # 1. Concepto e inspiración
    "El diseño de 'PDA NOCTUX' surge de la integración entre la figura mítica del búho nocturno (Noctua, símbolo de sabiduría, visión estratégica y sigilo) y la misión biológica de salvaguardar la vida en el certamen (reto 'El Huevonauta'). La inspiración visual combina la biología y la astronáutica infantil/juvenil, transformando un cohete de modelismo en una cápsula protectora con personalidad propia.",
    
    # 2. Significado del diseño
    "La distribución cromática y sus detalles gráficos comunican la esencia de la misión:\n"
    "• Negro Grafito / Espacial: Representa el vuelo nocturno y el cielo profundo, sirviendo de base sobria y técnica.\n"
    "• Verde Neón Bio-Tecnológico: Representa la vida del 'Huevonauta' que viaja en el módulo frontal. Este color fluorescente proporciona además una máxima visibilidad óptica para la rápida localización y rescate del cohete en tierra.\n"
    "• Blanco Puro: Destinado a las aletas estabilizadoras y rótulos para generar contraste y facilitar la lectura técnica en inspección de rampa.\n"
    "• Elementos Gráficos: Ojos de búho geométricos y estilizados en la transición de la ojiva/cápsula biológica, el emblema 'Huevonauta a Salvo', el ID reglamentario '104' en posición vertical contrastada y las marcas de Centro de Gravedad (CG).",
    
    # 3. Materiales y pintura
    "Se priorizó la ligereza para no sobrecargar el empuje de motores de modelismo:\n"
    "• Sustratos base: Fuselaje cilíndrico de cartón kraft espiralizado ultraliviano, ojiva hueca termoformada/impresa con compartimento acolchado para el huevo, aletas en madera balsa liviana.\n"
    "• Acabado: Imprimación ligera base agua para no atacar el cartón, pintura acrílica en spray de secado rápido aplicada en capas pulverizadas muy delgadas, y sellador satinado transparente.\n"
    "• Herramientas: Bloques de lija de grano fino (400 y 600), cintas de carrocero delicadas para enmascarado y balanza de precisión para monitorear cada capa de pintura aplicada.",
    
    # 4. Técnicas artísticas
    "Las técnicas aplicadas fueron:\n"
    "• Lijado suave y pulido de cantos en las aletas de balsa con perfil de borde de ataque redondeado y borde de fuga afilado.\n"
    "• Estarcido (stencil) para la rotulación artística de los ojos de búho y patrones geométricos en el fuselaje.\n"
    "• Aplicación de vinilos reflectivos de alta visibilidad en los bordes de aletas y rotulación adhesiva del ID '104' con corte computarizado.",
    
    # 5. Identidad del equipo
    "PDA NOCTUX representa el semillero inicial de la I.E. José Antonio Galán: niños y jóvenes principiantes que descubren el fascinante mundo de la ingeniería aeroespacial. La estética del cohete refleja su curiosidad, dedicación, ternura y sentido de responsabilidad al proteger su carga útil biológica, llevando en alto el nombre de su colegio y su municipio en el CCCD 2026."
]

def main():
    os.makedirs('Categoria_1_PDA_Noctux', exist_ok=True)
    os.makedirs('Categoria_2_PDA_Stars', exist_ok=True)
    os.makedirs('Categoria_3_PDA_Rocketeers', exist_ok=True)
    
    # Generar los 3 archivos Word oficiales
    generar_documento_estetica('PDA Noctux', 104, respuestas_cat1, r'Categoria_1_PDA_Noctux\104_PDANoctux_Estetica.docx')
    generar_documento_estetica('PDA - Stars', 211, respuestas_cat2, r'Categoria_2_PDA_Stars\211_PDAStars_Estetica.docx')
    generar_documento_estetica('PDA Rocketeers', 310, respuestas_cat3, r'Categoria_3_PDA_Rocketeers\310_PDARocketeers_Estetica.docx')
    
    # Copiar también la plantilla base a cada carpeta de categoría para referencia
    import shutil
    shutil.copyfile(r'Documentos_Oficiales_Globales\Plantilla_Formato_Estetica_Cohete.docx', r'Categoria_1_PDA_Noctux\Plantilla_Formato_Estetica_Cohete.docx')
    shutil.copyfile(r'Documentos_Oficiales_Globales\Plantilla_Formato_Estetica_Cohete.docx', r'Categoria_2_PDA_Stars\Plantilla_Formato_Estetica_Cohete.docx')
    shutil.copyfile(r'Documentos_Oficiales_Globales\Plantilla_Formato_Estetica_Cohete.docx', r'Categoria_3_PDA_Rocketeers\Plantilla_Formato_Estetica_Cohete.docx')
    print("Plantillas base copiadas a carpetas de categoría.")

if __name__ == '__main__':
    main()

