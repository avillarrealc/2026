# Presupuesto y Relación de Gastos — CCCD 2026
**Concurso Colombiano de Cohetería Deportiva 2026**  
**Equipos / Delegación:** PDA Noctux (Cat. 1), PDA Stars (Cat. 2), PDA Rocketeers (Cat. 3)  
**Institución Educativa:** I.E. José Antonio Galán (La Estrella, Antioquia)  
**Asesor Docente:** Alexander Villarreal  
**Archivo de Cálculo Vinculado:** [`Presupuesto_y_Relacion_de_Gastos_CCCD2026.xlsx`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Presupuesto_y_Relacion_de_Gastos_CCCD2026.xlsx)

---

## 📊 1. Resumen Ejecutivo y Propuesta de Presupuesto

Este presupuesto detalla los costos proyectados y diferenciados para los 3 equipos de la delegación de La Estrella que participarán en el Concurso Colombiano de Cohetería Deportiva (CCCD 2026). Se ha implementado un sistema de **asignación por categoría** para identificar a qué equipo pertenece cada rubro de inversión, así como rubros compartidos.

> [!TIP]
> **ESTRATEGIA FINANCIERA DE LA DELEGACIÓN**
> - **Cat 1 (Noctux):** Es el equipo más económico, enfocado en balística pura y aerodinámica, sin desarrollo electrónico.
> - **Cat 2 (Stars):** Requiere inversión intermedia. Su mayor reto es la inscripción pendiente ($ 900.000) y la adquisición del altímetro reglamentario Jolly Logic.
> - **Cat 3 (Rocketeers):** Absorbe la mayor carga de ingeniería. Requiere altímetro redundante, telemetría y construcción del módulo Cansat y una estructura mayor.
> - **Gastos Globales:** Se consolidan el hospedaje en finca ($ 3.000.000) y los consumibles generales compartidos (PLA, Ripstop, Nylon).

---

## 🎯 2. Presupuesto Proyectado Detallado (Matriz de Ítems)

### 🚀 Categoría 1: PDA Noctux
*Presupuesto proyectado sin componentes electrónicos, priorizando la estructura y estabilidad.*
- **Estructura Aerodinámica:** Tubo BT65 ➔ **$ 70.000**.
- **Sistema de Recuperación:** Cordón de choque ➔ **$ 10.000**.

### 🌟 Categoría 2: PDA Stars
*Inversión enfocada en la telemetría, altimetría obligatoria y el pago pendiente de inscripción.*
- **Inscripción CCCD:** Inscripción equipo PDA Stars ➔ **$ 900.000**.
- **Aviónica Obligatoria:** Altímetro Jolly Logic AltimeterOne ➔ **$ 250.000**.
- **Desarrollo Electrónica Base:** Componentes y placas ➔ **$ 300.000**.
- **Estructura Aerodinámica:** Tubo BT80 ➔ **$ 90.000**.
- **Sistema de Recuperación:** Cordón de choque ➔ **$ 10.000**.

### 👨‍🚀 Categoría 3: PDA Rocketeers
*Máxima inversión en cohetería de alta potencia (HPR) y el desarrollo de carga útil CanSat.*
- **Estructura HPR:** Tubo cartón 4 pulgadas (2 unid x $ 100.000) ➔ **$ 200.000**.
- **Estructura HPR (Desarrollos extras):** Tubo porta motor ($50.000), Madera para aletas ($120.000), Molde para ojiva ($300.000), Guías de lanzamiento ($20.000).
- **Aviónica:** Altímetro Jolly Logic AltimeterOne ➔ **$ 250.000**.
- **Desarrollo Electrónica y Carga Útil:** Módulo Cansat y redundancia ➔ **$ 500.000**.
- **Sistema de Recuperación:** Cordón de choque ➔ **$ 60.000**.
- **Consumibles:** Herrajes y tornillos ➔ **$ 50.000**.

### ⛺ Gastos Logísticos y Materiales Globales (Toda la Delegación)
*Estos rubros cubren y benefician a los tres equipos en conjunto durante el diseño, manufactura y la campaña de lanzamiento.*
- **Hospedaje en Finca:** Santa Fe de Antioquia (Fin de semana) ➔ **$ 3.000.000** *(Alojamiento delegación)*.
- **Transporte Terrestre:** Bus/busetas ida y regreso (La Estrella - Santa Fe de Ant.) ➔ **$ 900.000**.
- **Impresión 3D:** Filamento PLA ➔ **$ 100.000**.
- **Impresión 3D Avanzada:** Filamento PETG + CF (Fibra de Carbono) ➔ **$ 120.000**.
- **Impresión 3D (Consumibles):** Boquilla de acero endurecido ➔ **$ 80.000**.
- **Recuperación Textil:** Tela Ripstop para paracaídas (Lote general) ➔ **$ 100.000**.
- **Recuperación (Costuras):** Nylon trenzado ➔ **$ 25.000**.
- **Pinturas de Acabado:** ➔ **$ 160.000**.
- **Estructura y Pegantes:** Resina Epóxica ➔ **$ 175.000**.
- **Estética y Marcación:** Vinilo adhesivo ➔ **$ 80.000**.
- **Misión e Imagen:** Adhesivos para letras y parches de misión impresos ➔ **$ 70.000**.

---

## 🧾 3. Estructura de la Hoja de Relación de Gastos Reales

En el libro de cálculo [`Presupuesto_y_Relacion_de_Gastos_CCCD2026.xlsx`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Presupuesto_y_Relacion_de_Gastos_CCCD2026.xlsx), se ha actualizado la hoja **`PRESUPUESTO`** y **`RELACION_GASTOS`** integrando la columna **ASIGNACIÓN (CAT)** y adaptando las filas a los materiales de construcción estipulados (tubos BT, impresión en PETG-CF, cortes textiles, etc). 

Aquellos rubros con **[Valor por definir]** han sido declarados en el inventario con costo cero (0 COP) de manera temporal, permitiendo ser ajustados en el documento de Excel a medida que se consigan las cotizaciones oficiales.

---

## 🖨️ 4. Automatización de Reportes (PDF)

Para fines logísticos y de presentación, se ha desarrollado un script de extracción y generación automática de PDF:
- **Script:** [`generate_pdf.py`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/generate_pdf.py) - Lee el archivo Excel maestro y extrae estrictamente las columnas *Ítem, Descripción, Cantidad y Total*.
- **Reporte de Salida:** [`Presupuesto_Resumido.pdf`](file:///d:/Documentos/IEJAGA/2026/PDA/CCCD2026/Presupuesto_Resumido.pdf) - Documento en PDF con estética del "PDA CLUB", que suma automáticamente el Gran Total y formatea la descripción para los tres equipos.

---

## 🏛️ 5. Fuentes de Financiación Identificadas

| Fuente de Financiación | Tipo de Recurso | Monto Estimado (COP) | Estado Actual |
| :--- | :--- | :---: | :---: |
| **Convocatoria Generación Estrella / YCAF** | Subsidio proyecto ambiental (AeroBio) | $ 3.000.000 | Aprobado / Asignado |
| **Fondo de Servicios Educativos - IEJAGA** | Apoyo institucional | $ 1.200.000 | En trámite |
| **Patrocinios Comerciales / Industria Local** | Donación de insumos o aporte económico | $ 1.500.000 | Cartas radicadas |
| **Actividades Pro-Fondos Delegación PDA** | Recaudo de eventos de ciencia | $ 800.000 | En ejecución |

---

## 📌 6. Recomendaciones de Jorge Londoño / Asesoría Financiera

1. **Gestión Inmediata de Inscripción:** Priorizar el desembolso de los $ 900.000 de la categoría 2 (Stars) para garantizar su cupo oficial ante la organización.
2. **Reserva de Finca:** Abonar al alquiler de la Finca en Santa Fe de Antioquia para congelar el precio de $ 3.000.000.
3. **Cotización de Electrónica (Cat 2 y Cat 3):** Es prioritario establecer los requerimientos de PCB, sensores y transmisores LoRa para reemplazar los rubros "Por definir" y conocer el costo real de desarrollo en aviónica.
