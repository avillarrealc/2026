# Cronograma y Estado de Entregables - CCCD 2026

**Última actualización:** 5 de Noviembre de 2026 (15:35)

## Categorías y Equipos IEJAGA
- **Categoría 1 (Principiantes):** PDA Noctux (Baja potencia)
- **Categoría 2 (Intermedios):** PDA Stars (Motor F)
- **Categoría 3 (Avanzados):** PDA Rocketeers (Motor G, Carga Útil CanSat 250-300g, Apogeo proyectado ~400m)

---

## Cronograma Oficial CCCD 2026 y Calificaciones Registradas

**Plataforma oficial de puntuación en vivo:** [https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21](https://puntos.cccd.space/public/live/554e1756-bf1e-476a-88c8-49806d1acc21)

| Fecha límite | Entregable / Actividad | Cat 1 (Noctux) | Cat 2 (Stars) | Cat 3 (Rocketeers) | Estado y Calificación Oficial |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **23 de Septiembre** | Reporte de Progreso 1 | Aplica (**40 pts**) | Aplica (**50 pts**) | Aplica (**45 pts**) | *Evaluado en plataforma* |
| **25 Sep - 3 Oct** | Asesorías Virtuales | Aplica | Aplica | Aplica | *Cerrado* |
| **4 de Octubre** | Preliminary Design Review (PDR) | - | - | **Aplica (48 pts)** | *Evaluado en plataforma (48/50)* |
| **10 de Octubre** | Video del Equipo | Aplica (**87 pts**) | Aplica (**90 pts**) | Aplica (**95 pts**) | *Evaluado en plataforma. Devoluciones formales archivadas para Cat 2 (90/100) y Cat 3 (95/100)* |
| **12 - 23 de Octubre** | Revisiones Técnicas Virtuales | **Aprobada (23-Oct)** | **Apto con Correcciones (23-Oct)** | **Aprobada (19-Oct)** | *Completadas. Cat 2 con reporte oficial de correcciones obligatorias (launch lugs, paracaídas, switch, aletas)* |
| **25 de Octubre** | Reporte Técnico | **Aplica (75 pts)** (25-Oct) | - | - | *Evaluado en plataforma* |
| **25 de Octubre** | Critical Design Review (CDR) | - | **Aplica (85 pts)** (26-Oct, con -15 pts penalización) | **Aplica (50 pts)** (25-Oct, 310_PDARocketeers_CDR.pdf) | *Evaluado en plataforma. Cat 3 obtiene puntaje perfecto (50/50, 100% de la fase CDR)* |
| **30 de Octubre** | Reto “Estética del Cohete” | **Aplica (96 pts)** | **Aplica (84 pts)** | **Aplica (89 pts)** | *Evaluado en plataforma. Devoluciones archivadas para Cat 2 (84/100) y Cat 3 (89/100)* |
| **1 de Noviembre** | Divulgación (Redes Sociales) | **Aplica (100 pts)** | **Aplica (100 pts)** | **Aplica (100 pts)** | *Evaluado en plataforma. ¡Pleno perfecto de 100/100 para los 3 equipos de la IEJAGA!* |
| **6 - 8 de Noviembre**| Concurso Colombiano de Cohetería | Aplica | Aplica | Aplica | **Evento Presencial (Santa Fe de Antioquia)** |

### 🏆 Posiciones Actuales en Tabla General en Vivo (Top Pre-Lanzamiento al 05-Nov):
- **Categoría 3 (Universitarios / Avanzados):** **Puesto #4 Nacional** — `PDA Rocketeers` con **427 pts** (Progreso 1: 45, PDR: 48, CDR: 50, Video: 95, Estética: 89, Divulgación: 100). A solo 5 puntos del líder universitario nacional (Deméter EIA: 432 pts), a 4 puntos de Spectro UdeA (431 pts) y a 2 puntos de SpaceTech Pollux UniAndes (429 pts). ¡Fase previa virtual completada al 100% con 427 de 450 puntos posibles (94.9%)!
- **Categoría 2 (Intermedios):** **Puesto #2 Nacional (Zona de Podio y Subcampeonato Transitorio)** — `PDA - Stars` con **409 pts** (Progreso 1: 50, Video: 90, CDR: 85, Estética: 84, Divulgación: 100). A solo 2 puntos del líder (Malok Space: 411 pts).
- **Categoría 1 (Principiantes):** **Puesto #2 Nacional (Zona de Podio y Subcampeonato Transitorio)** — `PDA Noctux` con **398 pts** (Progreso 1: 40, Video: 87, Informe Técnico: 75, Estética: 96, Divulgación: 100). A 15 puntos del líder (Copetonautas: 413 pts).

*Nota: No se aplazará ninguna actividad ni fecha límite establecida sin previo aviso al Comité Técnico.*

---

## Requisitos Técnicos Críticos para Revisiones (PDR / CDR)

### Categoría 3 (PDA Rocketeers)
- **Estabilidad:** Margen estático mínimo de 2.0 calibres entre CG y CP (1.91 cal al despegue, 2.20 cal en burnout).
- **Relación Empuje/Peso:** Mínimo 5:1 (G80-7T: 80 N / [0.896 kg * 9.81 m/s²] = 9.1:1, cumple holgadamente).
- **Velocidad de salida (riel):** Mínimo 55 km/h (15.3 m/s) -> Verificado en OpenRocket a **63.1 km/h (17.53 m/s)** en riel de 1.5 m.
- **Carga Útil:** CanSat funcional cautivo de **274.0 g** (rango reglamentario 250 g a 300 g) con ESP32-S3, telemetría LoRa 915 MHz y filtro EKF.
- **Zona de Recuperación (Circular 10-Oct):** Radio de impacto **≤ 400 m** (fuera = irrecuperable / anula vuelo). Paracaídas Ø 70 cm con derrame de 7 cm, velocidad de impacto 7.06 m/s, deriva estimada a 5 m/s de viento: 281 m (margen seguro de 119 m).
- **Estado Actual de Diseño:** `Diseño SIDERAL.ork` calibrado con masas de manufactura FDM y balso (Apogeo **397.81 m** con motor Aerotech G80-7T, error de sólo 0.55% frente a los 400 m).
- **Documento CDR:** Informe formal `310_PDARocketeers_CDR.pdf` de 59 páginas bajo formato AIAA / LaTeX. **Completado y radicado a tiempo el 25 de Octubre (0 pts penalización)**.

### Categoría 2 (PDA Stars)
- **Motor asignado:** Motor F (Estes F15-4, 29 mm, ID 211).
- **Entregable crítico CDR (Critical Design Review):**
  - **Fecha límite oficial:** Domingo 25 de octubre, 11:59 p. m. (0 pts penalización).
  - **Penalizaciones por extemporaneidad:** Lunes 26-Oct (-15 pts), Martes 27-Oct (-30 pts). Cierre definitivo posterior al martes 27-Oct.
  - **Estado oficial de radicación:** **Completado el 26 de octubre (1 día de retraso)**. Aplica penalización reglamentaria oficial de **-15 puntos** en la evaluación del CDR.
  - **Nomenclatura oficial radicada:** `211_PDAStars_CDR.pdf` (33 páginas, respaldado en repositorio local).
  - **Plantilla oficial:** `Plantilla CDR Intermedios.docx`. Prohibido alterar colores, tipografías, encabezados o estructura base. Obligatorio conservar todos los apartados originales y reemplazar "000" por ID "211".
- **Plataforma y Rampa (Circular Oct-2026):** Varilla cilíndrica de **$\varnothing 6.5\text{ mm} \times 1500\text{ mm}$**. Guías de lanzamiento (*launch lugs*) con diámetro interior $\ge 7.0\text{ mm}$ (modelo `.ork` actualizado a radio $3.6\text{ mm} = \varnothing 7.2\text{ mm}$).
- **Zona de Recuperación (Circular 10-Oct):** Radio de impacto **≤ 250 m** (fuera = irrecuperable / anula vuelo).
- **Tiempo de vuelo:** Ventana estricta de **40 a 50 s** para motor F (actualización oficial de guía Intermedios p4 y p7).
- **Estrategia de Descenso:** Descenso a **7.5–8.2 m/s** (paracaídas Ø 45–50 cm). Garantiza deriva ≤ 190 m a 5 m/s viento (margen seguro dentro del radio de 250 m) y tiempo total de vuelo en ~44 a 47 s (centro de la ventana reglamentaria).
- **Carga Útil (Guía Oficial 25-Oct):** Masa máxima $\mathbf{\le 60\text{ g}}$, autonomía $\mathbf{\ge 4\text{ h}}$, switch accesible externamente en rampa y retención estructural obligatoria (prohibida eyección libre).

### Categoría 1 (PDA Noctux)
- **Nivel:** Baja potencia.
- **Reporte Técnico:** **Completado y radicado a tiempo el 25 de Octubre (0 pts penalización)**. Sin requisito de CDR formal.

---

## Requisitos de Seguridad, Marcación e Ingreso al Concurso Presencial (6-8 Nov)

### 🏷️ Marcación y Rotulación de Vehículos (Circular Oficial 27-Oct)
- **ID vertical en el fuselaje:** Ubicado entre dos aletas, visible y en contraste cromático neto:
  - **Categoría 1 (PDA Noctux - ID 104):** Longitud mínima **$\ge 10\text{ cm}$**.
  - **Categoría 2 (PDA Stars - ID 211):** Longitud mínima **$\ge 15\text{ cm}$**.
  - **Categoría 3 (PDA Rocketeers - ID 310):** Longitud mínima **$\ge 25\text{ cm}$**.
- **Etiqueta informativa en la aleta:** No exige medidas específicas fijas (la infografía oficial es referencial). Debe ser visible, contrastar con la aleta e incluir estrictamente 5 campos:
  1. ID del equipo (`104`, `211` o `310`)
  2. Nombre del equipo (`PDA Noctux`, `PDA - Stars` o `PDA Rocketeers`)
  3. Institución educativa (`I.E. José Antonio Galán`)
  4. País y ciudad (`Colombia - La Estrella, Antioquia`)
  5. Forma de contacto (correo del docente / asesor técnico)
- **Referencia gráfica:** [`Documentos_Oficiales_Globales/Rotulacion_ID_y_Etiqueta_Aleta.jpg`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Documentos_Oficiales_Globales/Rotulacion_ID_y_Etiqueta_Aleta.jpg).

### 📄 Consentimiento de Participación y Póliza de Seguro (Circular Oficial 28-Oct)
- **Documento base:** [`Documentos_Oficiales_Globales/Consentimiento_Participacion_CCCD2026.pdf`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Documentos_Oficiales_Globales/Consentimiento_Participacion_CCCD2026.pdf).
- **Ubicación obligatoria en Google Drive:** Carpeta institucional `I.E. José Antonio Galán` → Subcarpeta **`Documentos`**.
- **Carácter obligatorio:** Aplica al **100% de los participantes** de cada equipo (estudiantes y docentes/mentores). La cantidad de documentos cargados (firmados digitalmente o escaneados) debe coincidir con el total de acreditados.
- **Instrucciones de diligenciamiento:**
  - *Mayores de edad:* Diligencian y firman Secciones 1 a 5 (Sección 6 se deja en blanco).
  - *Menores de 18 años:* Diligencian Secciones 1 a 5 y **obligatoriamente la Sección 6** firmada por padre, madre o representante legal.
- **Alcance de la Póliza Colectiva de Accidentes Personales (SATELAB):**
  - **Viernes 6 de noviembre (Inauguración Aburrá Sur):** Cobertura activa para todos los participantes acreditados.
  - **Sábado 7 de noviembre (Lanzamientos Santa Fe de Antioquia):** Cobertura activa exclusivamente para competidores de **Categoría 1 y Categoría 2**.
  - **Domingo 8 de noviembre (Lanzamientos Santa Fe de Antioquia):** Cobertura activa exclusivamente para competidores de **Categoría 3**.
  - *Condición de público general:* Quienes asistan en días distintos a la fecha de lanzamiento de su categoría lo hacen en calidad de observadores, debiendo respaldarse en su afiliación a EPS o póliza estudiantil institucional.
