# Avisos y Documentos de Referencia - Categoría 2: PDA Stars (Intermedios)

**Equipo Delegado:** PDA Stars  
**Competición:** Concurso Colombiano de Cohetería Deportiva (CCCD 2026) - Categoría Intermedios  

---

## 📌 Comunicados y Avisos Oficiales

> [!IMPORTANT]
> **ACTUALIZACIÓN OFICIAL: GUÍA CARGA ÚTIL INTERMEDIOS 2026 [25-OCT-2026]**
> El Comité Técnico emitió el documento oficial `Guia_Carga_Util_Intermedios_2026.pdf` (Versión 1.0.0, ALAS - SateLab):
> - **Masa máxima permitida:** **$\mathbf{\le 60\text{ g}}$** para la carga útil completamente ensamblada (estructura, electrónica, sensores y batería).
> - **Autonomía eléctrica obligatoria:** Cálculo y duración mínima de **$\mathbf{\ge 4\text{ horas}}$** continuas de operación.
> - **Baterías permitidas vs prohibidas:** Prohibidas celdas LiPo y Li-Ion planas rectangulares. Permitidas AA/AAA no recargables, 18650, Li-Ion cilíndricas, 9V y pilas de botón. *(Nota técnica: 18650 y 9V pesan ~45 g, por lo que se recomienda 2xAAA alcalinas de ~23 g o celda Li-Ion cilíndrica 14500 de ~19.5 g para no violar el techo de 60 g).*
> - **Sistema de Switches:** Switch externo mandatorio para activación en rampa de lanzamiento sin desmontar componentes.
> - **Sistema de Retención:** Prohibición estricta de separación total o eyección libre. La carga útil debe permanecer mecánicamente unida al cohete en todas las fases de vuelo y recuperación.
> - **Materiales autorizados:** PLA, PETG, ABS y Fibra de vidrio.

> [!IMPORTANT]
> **ACTUALIZACIÓN OFICIAL: GUÍA DE LANZAMIENTO CAT. 2 Y VARILLA Ø 6.5 MM [OCTUBRE 2026]**
> El Comité Técnico emitió el documento oficial `Guia_de_Lanzamiento_Categoria_2.pdf`:
> - **Motivo de seguridad:** Se rediseñó la plataforma de lanzamiento de Categoría 2, actualizando la varilla cilíndrica de lanzamiento (*launch rod*).
> - **Nuevas especificaciones oficiales obligatorias:**
>   - **Diámetro de la varilla:** **$\varnothing 6.5\text{ mm}$** (tolerancia dimensional precisa).
>   - **Longitud de la varilla:** **$1500\text{ mm}$** ($1.5\text{ metros}$).
> - **Acción técnica mandatoria para PDA Stars:**
>   - Todo soporte o guía de lanzamiento (*launch lug*) instalado en el fuselaje debe poseer un **diámetro interno mínimo de $\mathbf{7.0\text{ mm}}$** (radio interno $\ge 3.5\text{ mm}$) para garantizar que el cohete deslice suavemente por gravedad sin fricción ni riesgo de atascamiento (*rod binding*) en rampa.
>   - En las simulaciones de OpenRocket, configurar la longitud de varilla en $1.5\text{ m}$.

> [!IMPORTANT]
> **ACTUALIZACIÓN OFICIAL: GUÍA CATEGORÍA INTERMEDIOS Y TIEMPO DE VUELO MOTOR F**
> El Comité Técnico emitió la versión actualizada del documento oficial "Requisitos y retos – Categoría Intermedios" (`6_Guia_Categoria_Intermedios.pdf`).
> - **Ajuste técnico crítico (p4 y p7):** Se especifica formalmente que el cohete deberá mantener un tiempo total de vuelo entre **40 a 50 segundos para motor F** (manteniendo 30 a 40 segundos exclusivamente para motor E).
> - **Criterio de evaluación:** La precisión no altera la tabla de puntuaciones, pero define la ventana reglamentaria de descenso para PDA Stars (motor F15-4, altura objetivo 300 m). Permite dimensionar el paracaídas para una velocidad de descenso de 7.0 a 8.0 m/s sin riesgo de descalificación por aterrizar antes de 40 s ni exceder 50 s.

> [!TIP]
> **SOFTWARE OFICIAL DE DISEÑO DE PARACAÍDAS (ALAS / SATELAB) [09-OCT-2026]**
> Carlos Pineda (Corporación ALAS) puso a disposición de los equipos el software web oficial de dimensionamiento de sistemas de recuperación: [https://paracaidas.satelab.org](https://paracaidas.satelab.org).
> - **Utilidad técnica:** Permite calcular el diámetro plano e inflado, área superficial, longitud de líneas de suspensión, orificio de derrame (*spill hole*) y velocidad terminal de descenso ($V_t$) a partir de la masa de aterrizaje del cohete. Utilizado para contrastar con OpenRocket y asegurar el aterrizaje dentro del radio de 250 m y la ventana de 40–50 s.

> [!IMPORTANT]
> **MOTOR E ID DEFINITIVOS (circular 22-09-2026)**
> PDA - Stars: motor **F15-4**, **ID de Misión 211**. Esta circular reemplaza la del sábado y es la oficialmente establecida. Memorias 01, 02, 03, 04, 05 y 06 migradas de E12-4 a F15-4 (montura 29 mm, masa máxima 650 g, objetivo 300 m).
> Discrepancia abierta: DMP v1.0.0 y guía Cat. 2 tabulan F15-6, no F15-4. Prevalece la circular por ser posterior y definitiva. Confirmar especificaciones del empaque al recibir el motor.

> [!IMPORTANT]
> **REPORTE DE PROGRESO 1 (Categoría Intermedios)**
> Se debe diligenciar el Reporte de Progreso 1 **una sola vez por equipo** a través de: [https://forms.gle/1fq4DQ89jp4gdHe49](https://forms.gle/1fq4DQ89jp4gdHe49). 
> **Requisito:** Adjuntar archivo inicial de OpenRocket. Los parámetros no definidos pueden indicarse como "pendientes" o estimados.

> [!IMPORTANT]
> **RESTRICCIÓN DE SISTEMAS DE CONTROL (Cat. 1 y 2)**
> Está **estrictamente prohibido** el uso de cualquier sistema de control o mecanismo de actuación durante el vuelo (frenos aerodinámicos/air brakes, aletas móviles, canards móviles). El cohete debe mantener una configuración pasiva y estable.

> [!NOTE]
> **ID DE MISIÓN OBLIGATORIO**
> Se ha asignado oficialmente el Número de Equipo. Según la **Sección 3.2.8 del DCP**, este ID debe estar **físicamente grabado y visible** en la estructura exterior del cohete y la carga útil para inspección técnica.

> [!TIP]
> **ACCESO Y PROGRESO EN LA PLATAFORMA EDUCATIVA**
> La plataforma ya está operativa. Pueden ingresar utilizando las credenciales (usuario y contraseña) del líder del equipo.
> **Aclaración sobre el avance:** El porcentaje de progreso corresponde a la cuenta del equipo, no de manera individual. Si un integrante completa un contenido, aparecerá como completado para los demás. Esto no afecta el proceso; cualquier integrante puede entrar a revisarlo nuevamente. Se sugiere estudiarlo y discutirlo en equipo.

> [!SUCCESS]
> **VIDEO DEL EQUIPO (CAT. 2 - PDA STARS) [COMPLETADO: 2026-10-10 23:10]**
> Material audiovisual oficial entregado y cargado en plataforma/Drive bajo la nomenclatura reglamentaria: `211_PDAStars_VideoEquipo.mp4` (o `211_PDA_Stars_VideoEquipo.mp4`), cumpliendo especificaciones de la Rúbrica §3.4 (máx. 2 min, 16:9, subtítulos en español sincronizados, límite 200 MB). Evaluado sobre 100 puntos.

> [!SUCCESS]
> **SEGUNDA REVISIÓN TÉCNICA VIRTUAL (CAT. 2 - PDA STARS) [COMPLETADA Y APROBADA: 2026-10-23]**
> El equipo sustentó ante el evaluador técnico oficial (Juan Guillermo Cano — TRA #41662 L1) la segunda revisión técnica virtual de control y verificación de diseño:
> - **Dictamen oficial:** **Aprobado con éxito / Evaluación técnica satisfactoria.**
> - **Aspectos auditados y certificados:** Cumplimiento de avance físico y funcional (>80%), integridad del fuselaje ($\ge 60\text{ cm}$), montura 29 mm para motor Estes F15-4, aletas trapezoidales, masa total ($\le 650\text{ g}$), margen estático de estabilidad ($\ge 2.0\text{ cal}$), adaptación de guías para varilla de $\varnothing 6.5\text{ mm}$ y sistema de recuperación dimensionado para la ventana de 40 a 50 segundos.
> - **Próximo hito:** Entrega del documento oficial CDR (`211_PDAStars_CDR.pdf`, domingo 25 de octubre).


> [!CAUTION]
> **⚠️ ZONAS DE RECUPERACIÓN Y RADIO LÍMITE DE 250 M [CIRCULAR OFICIAL 10-OCT-2026]**
> El Comité Técnico emitió el documento oficial `ZONAS DE RECUPERACIÓN CCCD2026 CAT 2.pdf`:
> - **Regla de oro:** Todo cohete que aterrice fuera del **radio de 250 metros** será considerado **IRRECUPERABLE A EFECTOS DE LA COMPETENCIA**, anulando el puntaje del vuelo.
> - La condición se juzga en el instante del aterrizaje, sin importar localización posterior.
> - **Impacto crítico para PDA Stars (300 m apogeo con F15-4):**
>   - Con descenso lento (4 a 5 m/s): Vientos de 3.5 a 5 m/s derivan el cohete entre 260 y 375 m (**DESCALIFICADO**).
>   - Con nuestra línea base revisada (7.5 a 8.2 m/s para ventana oficial de 40–50 s): La deriva máxima a 5 m/s de viento es de **180 a 190 m** (margen seguro de 60 a 70 m dentro del radio de 250 m), garantizando además un aterrizaje mucho más suave sin descalificación por tiempo ni por zona.

> [!WARNING]
> **REPORTE TÉCNICO OFICIAL DE INSPECCIÓN (PDA STARS ID 211) — DICTAMEN: APTO CON CORRECCIONES [04-NOV-2026]**
> Archivo respaldado: [`Reporte técnico PDA Stars (ID 211).pdf`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Categoria_2_PDA_Stars/Reporte%20t%C3%A9cnico%20PDA%20Stars%20(ID%20211).pdf)
> - **Estado oficial:** **APTO CON CORRECCIONES**. El cohete tiene masas reales y buen diseño aerodinámico. Podrá recibir la autorización final de vuelo una vez subsanada la lista de chequeo en taller.
> - **Parámetros verificados conformes:**
>   - Masa total con motor F15-4: **444 g** (masas reales) vs. máx. 650 g (**CUMPLE**).
>   - Longitud total: **68.5 cm** vs. mín. 60 cm (**CUMPLE**).
>   - Masa de la carga útil: **56.7 g** vs. máx. 60 g (**CUMPLE**).
>   - Materiales: **Cero piezas en PLA** (**CUMPLE**). El Comité confirmó formalmente que **las aletas impresas en 3D (PETG-CF) SÍ están permitidas**, condicionadas a excelente impresión sin microfisuras y pegado estructural robusto.
>   - Altímetro: Espacio y orificio de ventilación previstos (**CUMPLE**).
>   - Simulación: Desarrollada bajo condiciones reales de vuelo (**CUMPLE**).
>   - Retención de motor: Platina de acero galvanizado (**CUMPLE**, se sugiere anillo retenedor de respaldo).
> - **Condiciones obligatorias para autorización final de vuelo en rampa:**
>   1. **[CRÍTICA] Launch lugs incompatibles:** Los tubos guía instalados tienen diámetro interno de 6 mm y la nueva varilla oficial de lanzamiento mide 6.5 mm. **No entran en la varilla**. Deben sustituirse por guías con diámetro interno $\ge 7.0\text{ mm}$ alineadas al eje longitudinal del fuselaje y verificadas con varilla física.
>   2. **[CRÍTICA] Paracaídas y cordón incompleto:** Paracaídas no terminado y partes sin conectar al cordón de choque. Riesgo de piezas sueltas y 0 pts en recuperación. Terminar confección (color visible, descenso calibrado a 7.5–8.0 m/s) y anclar sólidamente cuerpo, nariz y carga útil.
>   3. **[ALTA] Fijación de aletas:** Pegar aletas de PETG-CF al cuerpo con resina epóxica de alta resistencia y filetes estructurales de refuerzo en la raíz.
>   4. **[ALTA] Acople de ojiva:** Ajustar la fricción del hombro de la nariz para que no se separe durante el ascenso por presión dinámica, pero deslice libremente con la deflagración de eyección.
>   5. **[ALTA] Switch externo:** Instalar interruptor exterior accesible con el cohete montado en rampa y protegido contra conmutación accidental.
>   6. **[ALERTA DE ESTABILIDAD]:** El margen verificado es de **2.05 calibres** (límite reglamentario $\ge 2.0\text{ cal}$). Al pegar las aletas, instalar switch y ensamblar paracaídas completo, es mandatorio recalcular y verificar físicamente que el $CG$ no se desplace hacia popa dejando el margen en $< 2.0\text{ cal}$.

> [!SUCCESS]
> **DEVOLUCIONES OFICIALES RECIBIDAS: VIDEO Y ESTÉTICA (PDA STARS ID 211) [04-NOV-2026]**
> 1. **Calificación del Video de Equipo:** **90 / 100** (Archivo respaldado: [`211 - PDA Stars.pdf`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Categoria_2_PDA_Stars/211%20-%20PDA%20Stars.pdf)).
>    - *Claridad y narrativa (18/20):* Estructura clara presentando a los 6 integrantes en primera persona con sus roles específicos.
>    - *Calidad técnica (18/20):* Muy buena edición, logo constante, subtítulos legibles y audio nítido.
>    - *Contenido técnico (16/20):* Buen vocabulario técnico (CG, CP, margen, simulación). Recomendación: incluir capturas visuales de pantalla del software de simulación.
>    - *Creatividad y originalidad (18/20):* Cuidada identidad visual, justificación del parche y narrativa consistente.
>    - *Identidad del equipo (20/20 - PUNTUACIÓN PERFECTA):* Los 6 integrantes hablando a cámara con roles específicos (ingeniera, diseñadora, comunicaciones, contador y dos líderes).
>    - Requisitos de entrega: Todos cumplidos al 100% (1:34.9, 16:9, a tiempo).
> 2. **Calificación del Reto Estética del Cohete:** **84 / 100** (Archivo respaldado: [`10_PDA_Stars_Estetica.pdf`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Categoria_2_PDA_Stars/10_PDA_Stars_Estetica.pdf)).
>    - *Diseño y apariencia general (17/20):* Concepto geométrico con estrella de 6 puntas y franjas en V. Recomendación: dar más presencia al nombre STELLARIS y logo del equipo.
>    - *Esquema de colores (18/20):* Paleta azul, blanco y negro bien distribuida con sensación de movimiento.
>    - *Identidad y originalidad (18/20):* Estrella de 6 puntas representa a la mascota y a los 6 integrantes.
>    - *Justificación del diseño (18/20):* Explicación sólida del azul y blanco. Recomendación: justificar el negro como color predominante.
>    - *Calidad de los acabados (13/20):* Bordes definidos en franjas. Recomendación crítica de taller: lograr acabado negro más uniforme sin rayones ni marcas claras, limpiar la raíz de las aletas con el fuselaje y asegurar iluminación neutra y enfoque nítido en el registro fotográfico.

> [!NOTE]
> **TABLERO DE CALIFICACIONES EN VIVO (CCCD PUNTOS) [ACTUALIZADO: 05-NOV-2026]**
> Resultados oficiales consultables en: [https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21](https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21)
> - **Posición actual PDA Stars:** **Puesto #2 Nacional (Zona de Podio / Subcampeón Transitorio)** con **409 puntos** acumulados (5 de 11 parámetros evaluados):
>   - Reporte Progreso 1: **50 / 50 pts** (Puntaje perfecto).
>   - Divulgación Científica: **100 / 100 pts** (**¡Puntaje perfecto!**).
>   - Video del Equipo: **90 / 100 pts** (Calificación sobresaliente).
>   - Critical Design Review (CDR): **85 / 100 pts** (Computa penalización de -15 pts por entrega 26-Oct).
>   - Reto Estética del Cohete: **84 / 100 pts**.
> - Diferencial de punta: A solo 2 puntos del líder nacional (Malok Space - Cosmo School: 411 pts) y superando a Orión 25 (400 pts) y AstroComercial (397 pts). Pendientes por calificar en campo: Presentación ante jurados, Altitud de Vuelo (Motor F), Carga Útil, Paracaídas y Estado Final.

> [!CAUTION]
> **⚠️ CATO (Catastrophe At Take Off) Y PROTOCOLO DE SEGUNDO VUELO [CIRCULAR OFICIAL OCT-2026]**
> El Comité Técnico emitió la directriz oficial sobre fallas catastróficas del motor en rampa:
> - **Definición y deslinde:** Ruptura del motor y daño estructural al vehículo. Corporación ALAS no asume responsabilidad civil ni técnica por defectos del motor atribuibles al fabricante.
> - **Procedimiento de seguridad:** Suspensión inmediata de lanzamientos por el Oficial de Seguridad (RSO) para salvaguarda de personas.
> - **Posibilidad de segundo vuelo:** El equipo podrá solicitar un segundo intento siempre que:
>   1. El vehículo sea inspeccionado y declarado 100% apto y seguro por los técnicos.
>   2. Se cumpla la totalidad de los requisitos de estabilidad y masa reglamentaria ($\le 650\text{ g}$, margen $\ge 2.0\text{ cal}$).
>   3. Exista disponibilidad física de un motor compatible de reemplazo (F15-4).
>   4. La autorización no es automática ni obligatoria; prima la decisión técnica del RSO.
> - Documento oficial de consulta: `Documentos_Oficiales_Globales/CATO - CONSIDERACIONES TÉCNICAS Y DE SEGURIDAD.pdf`.

> [!IMPORTANT]
> **📋 PLANTILLA OFICIAL Y DIRECTRICES DE ENTREGA: CDR (CRITICAL DESIGN REVIEW) [OCT-2026]**
> El Comité Técnico emitió la plantilla oficial del documento CDR para Categoría Intermedios:
> - **Archivo plantilla:** `Plantilla CDR Intermedios.docx` (resguardada en la carpeta del equipo).
> - **Reglas de integridad de la plantilla (Penalizaciones por incumplimiento):**
>   - En la portada, sustituir estrictamente "000" por el **ID de Misión oficial: 211**.
>   - **Prohibido** modificar los colores institucionales, fuentes, tamaños de encabezados, títulos o diseño general.
>   - **Obligatorio** conservar sin excepción la totalidad de los 13 apartados originales de la tabla de contenidos. Se permite agregar tablas, subsecciones y diagramas complementarios sin alterar la estructura base.
> - **Nomenclatura reglamentaria:** `211_PDAStars_CDR.pdf` (o `211_PDA_Stars_CDR.pdf`).
> - **Plazos límite de entrega y escala de penalización:**
>   - **Domingo 25 de octubre, hasta las 11:59 p. m.:** Entrega a tiempo, **sin penalización**.
>   - **Lunes 26 de octubre, hasta las 11:59 p. m.:** Penalización de **-15 puntos**.
>   - **Martes 27 de octubre, hasta las 11:59 p. m.:** Penalización de **-30 puntos**.
>   - **Miércoles 28 de octubre en adelante:** **Plataforma cerrada**, no se admiten entregas extemporáneas (0 puntos en CDR).

> [!IMPORTANT]
> **🎨 RETO ESTÉTICA DEL COHETE (CAT. 2 - PDA STARS) [30-OCT-2026 23:59]**
> - **Plazo oficial ampliado:** Viernes 30 de octubre de 2026 a las 11:59 p. m.
> - **Ubicación de radicación:** Drive institucional (`I.E. José Antonio Galán`) → Subcarpeta: **`Reto Estética Visual`**.
> - **Entregables:**
>   1. **5 a 7 fotografías de alta resolución** (enfoque nítido, iluminación neutra, fondo limpio) del cohete PDA STARS completamente terminado (vista de conjunto + detalles de ojiva PLA+, fuselaje de 29 mm, aletas en balsa sellada, ID `211` y marcas de $CG/CP$).
>   2. **Formato oficial diligenciado:** [`211_PDAStars_Estetica.docx`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Categoria_2_PDA_Stars/211_PDAStars_Estetica.docx).
> - **Evaluación:** Hasta 100 puntos (Rúbrica SPP §3.5) + Elegibilidad automática al **Premio STEAM en Artes**.

---

## 📂 Archivos de Referencia Anexos en esta Carpeta

1. `1_Terminos_CCCD.pdf` — Términos generales firmados.
2. `2_Paso_a_paso_Plataforma.pdf` — Guía de acceso a la plataforma virtual CCCD2026.
3. `3_Asignacion_ID_Mision.pdf` — Comunicado oficial sobre el uso del Número de Equipo.
4. `4_Rubrica_Sistema_Puntuacion.pdf` — Rúbrica detallada con los aspectos y criterios de evaluación.
5. `5_Calendario_Oficial.jpg` — Cronograma de entregables inmodificable.
6. `6_Guia_Categoria_Intermedios.pdf` — **[ESPECÍFICO CAT 2]** Requisitos, retos, medidas y restricciones oficiales para la categoría.
7. `ZONAS DE RECUPERACIÓN CCCD2026 CAT 2.pdf` — **[NUEVO 10-OCT-2026]** Documento oficial con modelos de deriva por viento y radio límite de 250 m.
8. `Guia_de_Lanzamiento_Categoria_2.pdf` — **[NUEVO OCT-2026]** Especificación técnica oficial de la varilla de lanzamiento (Ø 6.5 mm x 1500 mm) y requerimiento de ajuste de guías.
9. `CATO - CONSIDERACIONES TÉCNICAS Y DE SEGURIDAD.pdf` — **[NORMA GLOBAL OCT-2026]** Protocolo oficial ante fallas de motor y condiciones para solicitar segundo vuelo (custodiado en `Documentos_Oficiales_Globales/`).
10. `Plantilla CDR Intermedios.docx` — **[PLANTILLA OFICIAL CDR]** Formato Word inalterable con la estructura obligatoria de 13 secciones para el Critical Design Review.
11. `Guia_Carga_Util_Intermedios_2026.pdf` — **[NUEVO 25-OCT-2026]** Especificación técnica oficial de carga útil (masa $\le 60\text{ g}$, autonomía $\ge 4\text{ h}$, switch externo y retención estructural obligatoria).
12. `Plantilla_Formato_Estetica_Cohete.docx` — Plantilla oficial Word de la organización para el Reto Estética Visual.
13. `211_PDAStars_Estetica.docx` — Formato oficial diligenciado con fundamentación técnica y estética de PDA STARS (Cat 2).
14. `Consentimiento_Participacion_CCCD2026.pdf` — Formato obligatorio de exoneración, tratamiento de datos y póliza SATELAB (subir firmado a Drive `Documentos`).

---

## 📌 Sesión Informativa y Circulares Técnicas (WhatsApp ALAS)

Fuente: `Documentos_Oficiales_Globales/Sesion_Informativa_1_CCCD2026.md` y circulares oficiales del certamen.

- **Calendario Cat. 2:** Reporte Progreso 1 (23 Sep) · Asesorías (22 Sep-1 Oct) · Video Equipo (10 Oct) · Revisiones Técnicas Virtuales (12-22 Oct) · CDR (25 Oct) · Estética Visual (30 Oct) · Divulgación (1 Nov) · Concurso (6-8 Nov). Cat. 2 no presenta PDR.
- **Revisión técnica virtual:** exige mínimo 80% de avance físico/funcional; verificación en vivo de fuselaje, aletas, recuperación, carga útil, materiales y simulación. Revisor Cat. 1 y 2: Juan Guillermo Cano — TRA #41662 L1.
- **Baterías carga útil:** prohibidas LiPo y Li-Ion rectangular; permitidas AA/AAA no recargables, 18650, Li-Ion cilíndricas, botón. Memoria `03` ya corregida a 18650/2xAAA.
- **Acopladores:** 1 calibre mínimo a cada lado del punto de separación (ver `04`).
- **ID y marcaciones (Circular 27-Oct):** ID vertical en fuselaje con longitud mínima **$\ge 15\text{ cm}$** en alto contraste; etiqueta en aleta con medidas libres (imagen referencial) conteniendo: ID (211), Nombre de equipo, Institución (I.E. José Antonio Galán), País/Ciudad (Colombia - La Estrella) y Contacto.
- **Consentimiento de Participación (Circular 28-Oct):** Obligatorio para todos los integrantes. Menores de edad con firma de acudiente en Sección 6. Cargar escaneado/digital en Drive de la institución → subcarpeta `Documentos`. Cobertura de póliza: 6-Nov (inauguración) y 7-Nov (lanzamiento).
