# Avisos y Documentos de Referencia - Categoría 3: PDA Rocketeers

**Equipo Delegado:** PDA Rocketeers  
**Competición:** Concurso Colombiano de Cohetería Deportiva (CCCD 2026) - Categoría Avanzados / 3  

---

## 📌 Comunicados y Avisos Oficiales

> [!WARNING]
> **⚠️ CONTRADICCIÓN NORMATIVA MASA CANSAT (ACCIÓN REQUERIDA)**
> Guía CanSat v1.0.0 §2.1 admite 250-350 g; Guía Categoría Avanzados exige 250-300 g. Criterio aplicado: máximo duro 300 g. Solicitar aclaración escrita al revisor (Fonseca) en asesorías 22 Sep-1 Oct.

> [!IMPORTANT]
> **MOTOR E ID DEFINITIVOS (circular 22-09-2026)**
> PDA Rocketeers: motor **G80-7T**, **ID de Misión 310**. Confirma lo registrado en memorias. Sin cambios.

> [!NOTE]
> **ID DE MISIÓN OBLIGATORIO**
> Se ha asignado oficialmente el Número de Equipo. Según la **Sección 3.2.8 del DCP**, este ID debe estar **físicamente grabado y visible** en la estructura exterior del cohete y la carga útil para los procesos de inspección técnica, validación de seguridad y operaciones en la zona de lanzamiento.

> [!TIP]
> **ACCESO Y PROGRESO EN LA PLATAFORMA EDUCATIVA**
> La plataforma ya está operativa 100%. Pueden ingresar utilizando las credenciales (usuario y contraseña) del líder del equipo.
> **Aclaración sobre el avance:** El porcentaje de progreso corresponde a la cuenta del equipo, no de manera individual. Si un integrante completa un contenido, aparecerá como completado para los demás. Esto no afecta el proceso; cualquier integrante puede entrar a revisarlo nuevamente. Se sugiere estudiarlo y discutirlo en equipo.

> [!WARNING]
> **ETAPA DE EVALUACIÓN Y CALENDARIO INICIADA**
> Con la publicación de la Rúbrica Oficial de Puntuación, el concurso ha comenzado su etapa de evaluación. Las primeras actividades y entregas hacen parte ya del desarrollo oficial. El calendario adjunto es **definitivo e inmodificable**.

> [!IMPORTANT]
> **REPORTE DE PROGRESO 1 (Universitarios / Avanzados)**
> **[COMPLETADO: 2026-09-21 12:32:34]**
> Diligenciar el formulario correspondiente a la categoría: [https://forms.gle/WRggMzyRChvw5qHR7](https://forms.gle/WRggMzyRChvw5qHR7)

> [!SUCCESS]
> **MODELADO 3D Y PROTOCOLO DE OJIVA [COMPLETADO]**
> Se completó el diseño de la Ojiva (Perfil Serie Haack, C=0) para vuelo transónico. Geometría extraída de OpenRocket (escala x1000) e importada a Fusion 360 como sólido. Se generó un protocolo técnico en `Documentos_Oficiales_Globales/Protocolo_Ojiva_OR_Fusion360.md`.

> [!SUCCESS]
> **VIDEO DEL EQUIPO [COMPLETADO: 2026-10-10 11:30]**
> Material audiovisual oficial entregado y cargado en plataforma/Drive bajo la nomenclatura reglamentaria: `310_PDARocketeers_VideoEquipo.mp4` (o `310_PDA_Rocketeers_VideoEquipo.mp4`), cumpliendo las especificaciones de la Rúbrica §3.4 (máximo 2 min, formato 16:9, subtítulos en español sincronizados, límite 200 MB). Evaluado sobre 100 puntos.

> [!SUCCESS]
> **SEGUNDA REVISIÓN TÉCNICA VIRTUAL (CAT. 3 - PDA ROCKETEERS) [COMPLETADA Y APROBADA: 2026-10-19]**
> El equipo sustentó ante el evaluador técnico oficial (Juan Sebastián Fonseca — TRA #36180 L1) la segunda revisión técnica virtual de control:
> - **Dictamen oficial:** **Aprobado con éxito / Evaluación técnica sobresaliente.**
> - **Aspectos auditados y certificados:** Avance físico y funcional superior al 80% del vehículo SIDERAL, integridad de fuselaje de 102 mm, ojiva Haack manufacturada en filamento ASA, aletas sándwich balso / PETG-CF, montura de motor 29 mm para AeroTech G80-7T, margen estático $\ge 2.0\text{ cal}$, velocidad en riel $\ge 55\text{ km/h}$, integración de bahía de aviónica y CanSat (250–300 g) con batería 18650, y sistema de recuperación calibrado a $\sim 6.95\text{ m/s}$ para aterrizaje dentro del radio de 400 m.
> - **Próximo hito:** Entrega del documento oficial CDR (`310_PDARocketeers_CDR.pdf`, domingo 25 de octubre).



> [!CAUTION]
> **REGLAS SOBRE SISTEMAS DE CONTROL (Cat. 3 - Avanzados)**
> En esta categoría el uso de sistemas de control es **opcional** y no afecta el puntaje. En caso de implementarse, debe cumplir:
> - Vuelo nominal totalmente posible con el sistema desactivado.
> - Cohete estable por sí mismo sin depender del mecanismo.
> - Activación exclusiva posterior al apagado del motor.
> - **Prohibido** control activo de *pitch* o *yaw* (solo aplicaciones de *roll*).
> - Todo sistema (roll, air brakes, doble paracaídas, etc.) exige **aprobación previa** por la organización (contacto: Juan Sebastián Fonseca, secretario Tripoli).

> [!WARNING]
> **⚠️ CONTRADICCIÓN NORMATIVA DETECTADA (ACCIÓN REQUERIDA)**
> El **DCP Oficial (Sección 3.3.1)** prohíbe explícitamente sistemas de eyección distintos al motor y controles activos de recuperación. Aunque el reciente comunicado en Telegram autoriza "mecanismos de doble paracaídas" y "air brakes", **es imperativo solicitar a la Organización un aval técnico por escrito** que los exima formalmente de la Sección 3.3.1 para blindar el diseño y evitar descalificaciones en la inspección.

> [!TIP]
> **ESTRATEGIA DE PUNTUACIÓN CANSAT (CARGA ÚTIL)**
> Según la revisión de la *Guía CanSat*, el uso de módulos comerciales pre-fabricados (COTS) no está prohibido, pero **reducirá la calificación** en el ítem de innovación y desarrollo. Para asegurar el máximo puntaje, se recomienda el desarrollo de electrónica propia (diseño y fabricación de PCBs).

> [!CAUTION]
> **⚠️ ZONAS DE RECUPERACIÓN Y RADIO LÍMITE DE 400 M [CIRCULAR OFICIAL 10-OCT-2026]**
> El Comité Técnico emitió el documento oficial `ZONAS DE RECUPERACIÓN CCCD2026 CAT 3.pdf`:
> - **Regla de oro:** Todo cohete que aterrice fuera del **radio de 400 metros** será considerado **IRRECUPERABLE A EFECTOS DE LA COMPETENCIA**, anulando el puntaje del vuelo.
> - La condición se determina en el instante exacto del aterrizaje, sin importar localización posterior.
> - **Criterio de diseño para SIDERAL (409,5 m apogeo):** Con velocidad terminal de 6,95 m/s, ante viento máximo de 5 m/s la deriva estimada es de 288 m (margen positivo de 112 m). **Prohibido usar paracaídas que reduzcan el descenso a < 5,5 m/s**, pues con vientos superiores a 3,5 m/s el cohete sobrepasaría los 400 m.

> [!TIP]
> **SOFTWARE OFICIAL DE DISEÑO DE PARACAÍDAS (ALAS / SATELAB) [09-OCT-2026]**
> Carlos Pineda (Corporación ALAS) facilitó a los equipos el software de dimensionamiento aerodinámico de paracaídas: [https://paracaidas.satelab.org](https://paracaidas.satelab.org).
> - **Utilidad técnica:** Permite modelar el dosel (diámetro plano vs. inflado), área efectiva, líneas de suspensión, orificio de derrame (*spill hole*) y velocidad terminal ($V_t$). Utilizado para contrastar con OpenRocket y asegurar que SIDERAL mantenga una velocidad de descenso entre 6.0 y 7.0 m/s para no exceder los 400 m de radio límite.

> [!NOTE]
> **TABLERO DE CALIFICACIONES EN VIVO (CCCD PUNTOS)**
> Resultados oficiales consultables en: [https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21](https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21)
> - **Posición actual PDA Rocketeers:** **Puesto #4 Nacional (Categoría Universitarios / Avanzados)** con **188 puntos** acumulados:
>   - Reporte Progreso 1: **45 / 50 pts**.
>   - Video del Equipo: **95 / 100 pts** (Puntaje élite nacional).
>   - PDR (*Preliminary Design Review*): **48 / 50 pts** (Evaluación sobresaliente de ingeniería).
> - Diferencial competitivo: A solo 3 puntos del 1° puesto (Spectro Rocket Team UdeA: 191 pts), superando a facultades de ingeniería de la Universidad Nacional, UPB, EMAVI y EIA-Hermes. Próximo hito: CDR (25-Oct).

> [!CAUTION]
> **⚠️ CATO (Catastrophe At Take Off) Y PROTOCOLO DE SEGUNDO VUELO [CIRCULAR OFICIAL OCT-2026]**
> El Comité Técnico emitió la directriz oficial sobre fallas catastróficas del motor en rampa:
> - **Definición y deslinde:** Ruptura del motor y daño estructural al vehículo. Corporación ALAS no asume responsabilidad civil ni técnica por defectos del motor atribuibles al fabricante.
> - **Procedimiento de seguridad (Motor Clase G):** Suspensión inmediata de lanzamientos por el RSO para salvaguarda de vidas humanas. Perímetro de seguridad estricto de 20 m y espera mínima de 60 segundos antes de aproximación.
> - **Posibilidad de segundo vuelo:** El equipo podrá solicitar un segundo intento siempre que:
>   1. El vehículo sea inspeccionado y declarado 100% apto y estructuralmente seguro por los técnicos (Juan Sebastián Fonseca - TRA #36180 L1).
>   2. Se cumpla la totalidad de los requisitos de estabilidad ($\ge 2.0\text{ cal}$), integridad del CanSat (250–300 g) y velocidad en riel ($\ge 55\text{ km/h}$).
>   3. Exista disponibilidad física de un motor compatible de reemplazo (AeroTech G80).
>   4. La autorización no es automática ni obligatoria; prima la decisión técnica del RSO.
> - Documento oficial de consulta: `Documentos_Oficiales_Globales/CATO - CONSIDERACIONES TÉCNICAS Y DE SEGURIDAD.pdf`.

> [!IMPORTANT]
> **ENTREGABLE CRÍTICO: CRITICAL DESIGN REVIEW (CDR) CAT 3 [25-OCT-2026]**
> Se recibió la plantilla oficial `Plantilla CDR Avanzados.docx` y el equipo consolidó el informe técnico formal `310_PDARocketeers_CDR.pdf` (59 páginas, formato AIAA / LaTeX).
> - **Fecha límite de entrega:** Domingo 25 de octubre de 2026, 11:59 p. m. (0 pts de penalización).
> - **Penalizaciones por extemporaneidad:** Lunes 26-Oct (-15 pts), Martes 27-Oct (-30 pts). Posterior al martes 27-Oct la plataforma cierra y el puntaje es 0.
> - **Nomenclatura obligatoria:** `310_PDARocketeers_CDR.pdf`.
> - **Estructura oficial exigida (13 secciones):**
>   1. Parche de Misión
>   2. Equipo de Misión
>   3. Objetivos de Misión
>   4. Requerimientos y Restricciones
>   5. Cronograma de Trabajo
>   6. Análisis de Diseño del Cohete (SIDERAL)
>   7. Simulación de Vuelo (OpenRocket)
>   8. Construcción y Manufactura
>   9. Paracaídas y Sistema de Recuperación
>   10. Carga Útil (CanSat AeroBio / EKF / Sensores / Baterías Ni-MH 3.6V / LoRa)
>   11. Pruebas en Tierra
>   12. Seguridad y Mitigación de Riesgos
>   13. Referencias (Formato AIAA)

---

## 📂 Archivos de Referencia Anexos en esta Carpeta

1. `1_Terminos_CCCD.pdf` — Términos generales firmados.
2. `2_Paso_a_paso_Plataforma.pdf` — Guía de acceso a la plataforma virtual CCCD2026.
3. `3_Asignacion_ID_Mision.pdf` — Comunicado oficial sobre el uso del Número de Equipo.
4. `4_Rubrica_Sistema_Puntuacion.pdf` — Rúbrica detallada con los aspectos, distribución de puntajes y criterios de evaluación de la competencia.
5. `5_Calendario_Oficial.jpg` — Cronograma oficial inmodificable de entregables y actividades del certamen.
6. `6_Guia_Categoria_Avanzados.pdf` — **[ESPECÍFICO CAT 3]** Requisitos, retos, medidas y restricciones oficiales para la categoría Universitarios / Avanzados.
7. `ZONAS DE RECUPERACIÓN CCCD2026 CAT 3.pdf` — **[NUEVO 10-OCT-2026]** Documento oficial con modelos de deriva por viento y radio límite de 400 m.
8. `CATO - CONSIDERACIONES TÉCNICAS Y DE SEGURIDAD.pdf` — **[NORMA GLOBAL OCT-2026]** Protocolo oficial ante fallas de motor y condiciones para solicitar segundo vuelo (custodiado en `Documentos_Oficiales_Globales/`).
9. `Plantilla CDR Avanzados.docx` — **[PLANTILLA OFICIAL CDR 25-OCT-2026]** Estructura y lineamientos institucionales para el Critical Design Review.
10. `310_PDARocketeers_CDR.pdf` — **[BORRADOR TÉCNICO CDR]** Documento de 59 páginas desarrollado por el equipo para la entrega final.
11. `Anilloso FINAL.dxf` / `Anilloso_FINAL_Escala_1a1_Pliego_A2.pdf` — Planos de manufactura 1:1 de aletas y anillos de centrado en pliego A2.
12. `Diseño SIDERAL.ork` — Modelo OpenRocket actualizado y calibrado con pesos reales de manufactura.

---

## 📌 Sesión Informativa 1 (22-09-2026, grupo WhatsApp)

Fuente: `Documentos_Oficiales_Globales/Sesion_Informativa_1_CCCD2026.md`.

- **Calendario Cat. 3:** Reporte Progreso 1 (23 Sep) · Asesorías (22 Sep-1 Oct) · PDR (4 Oct) · Video Equipo (10 Oct) · Revisiones Técnicas Virtuales (12-22 Oct) · CDR (25 Oct) · Fotos Cohete (28 Oct) · Divulgación (1 Nov) · Concurso (6-8 Nov). Sin aplazamientos.
- **Revisión técnica virtual:** exige mínimo 80% de avance físico/funcional; verificación en vivo de fuselaje, aletas, recuperación, carga útil, materiales y simulación. Revisor Cat. 3: Juan Sebastián Fonseca — TRA #36180 L1 (mismo contacto de aprobación de sistemas de control).
- **Sistemas de control:** la sesión confirma permitido en Cat. 3 con los requisitos ya registrados arriba. Se mantiene la exigencia de aval escrito frente a DCP §3.3.1.
- **Baterías CanSat:** prohibidas LiPo y Li-Ion rectangular; permitidas AA/AAA no recargables, 18650, Li-Ion cilíndricas, botón; autonomía mínima 4 h (Guía CanSat §3.1). Memoria `03` ya corregida a 18650.
- **Acopladores:** 1 calibre mínimo a cada lado del punto de separación (ver `04`).
- **ID y marcaciones:** etiqueta obligatoria (equipo, ID, institución, país, ciudad, contacto); etiqueta adicional vertical entre aletas con ID visible en contraste; longitud mínima 25 cm + sticker del concurso. Archivos: `Id_NombreDelEquipo_Entregable`.
