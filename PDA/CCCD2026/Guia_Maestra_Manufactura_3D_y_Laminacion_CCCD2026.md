# GUÍA MAESTRA DE MANUFACTURA ADITIVA (3D) Y LAMINACIÓN FDM — CCCD 2026
**Misión:** Expediente Técnico de Cohetería Experimental y Deportiva  
**Institución:** I.E. José Antonio Galán (La Estrella, Antioquia)  
**Proyecto:** Concurso Colombiano de Cohetería Deportiva 2026 (CCCD 2026)  
**Equipos:** PDA Noctux (Cat 1) | PDA Stars (Cat 2) | PDA Rocketeers (Cat 3)  
**Fecha de consolidación:** 23 de Octubre de 2026

---

## 1. ÍNDICE MAESTRO Y DIRECTORIO DE SESIONES TÉCNICAS 3D

Para localizar, reabrir y retomar el contexto de cualquier desarrollo técnico en el entorno de desarrollo, utilice el identificador único de conversación (**Conversation ID / CID**):

| # | CID de Sesión | Fecha | Piezas / Hardware | Temas Técnicos Abordados |
| :---: | :--- | :---: | :--- | :--- |
| **01** | `b746dd93-aebd-4f44-9615-00973d788eb5` | 2026-10-23 | Aletas PETG, Ojiva Cat 2, Acople SIDERAL | Impresión vertical de aletas, calibración de flujo al 95% (-2 g), mitigación de costura en fuga, boquilla endurecida. |
| **02** | `4fe4fbb7-5403-4098-933d-c28b9bccea82` | 2026-10-21 | Acople con asa, Ojiva 102 mm, Ojivas Cat 1 y 2 | Parámetros definitivos Cura 4.13 en español, espesores 0.65 a 1.2 mm, generación de manual PDF oficial. |
| **03** | `067c23c6-b9e8-4f58-a1b8-fae1a2e489d9` | 2026-10-20 | Impresora Sunlu T3 (Cabina, Hotend) | Acondicionamiento para ASA: cabina térmica pasiva a 45 °C, garganta bimetálica all-metal, eliminación atasco Bowden. |
| **04** | `267e2c22-34ae-40c7-ba4e-2a147e6b09f2` | 2026-10-14 | Ojiva 102 mm ASA (Cat 3) | Fisuras interlaminares en ASA, descarte de modo jarrón, costura Z alineada vs aleatoria, postprocesado químico. |
| **05** | `9e1c963d-adf0-4c1e-8695-ecb4ae45a227` | 2026-10-17 | Acople SIDERAL 4" (Fusion 360) | Modelado CAD del asa de recuperación (12-15 G), hombros a presión, pilares para insertos M3 de latón. |
| **06** | `eb436f23-3dda-4ce0-aa9f-2ea01851caea` | 2026-10-01 | CanSat Cautivo, Anillos Roscados, Boquillas | Boquillas (0.4 vs 0.6 vs 0.8 mm), roscas trapezoidales Tr64x4 con holgura -0.20 mm, ventanas Stencil PDA. |
| **07** | `630bf9a6-837a-4133-ad8e-23ea8f4d9ad0` | 2026-09-22 | Ojiva Cat 3, Espuma Poliuretano | Carga de impacto a 6 m/s, inyección interna de espuma de poliuretano bicomponente en la punta como absorbedor. |
| **08** | `e6c3a321-44a4-45f3-bc9e-6bd2070a6064` | 2026-09-20 | PETG-CF vs PETG vs ASA | Rigidez frente a flutter vs Jaula de Faraday. Restricción crítica de filamentos con carbono en compartimentos de RF. |
| **09** | `cffeef9d-21fd-401e-a4cd-c19b0d3df8d9` | 2026-09-22 | Geometría Ojiva (OpenRocket -> Fusion) | Perfil supersónico Haack Series (factor C=0 / Von Kármán) para arrastre mínimo de onda (Cd), splines de control. |
| **10** | `3b0aaa3b-c53c-428e-9391-8e7ea0797304` | 2026-09-19 | CanSat, Aviónica LoRa, Aletas TTW | Límites de masa del CanSat (250-300 g), transparencia RF y fijación pasante Through-The-Wall (TTW). |
| **11** | `0cd0e954-1113-4f52-9e96-09f66c20b775` | 2026-10-18 | Resistencia Térmica, Portamotor | Límites HDT: descarte de PLA (55 °C) cerca al motor; PETG (75 °C) y ASA (100 °C) evaluados ante gases de combustión. |

---

## 2. SELECCIÓN TÉCNICA DE MATERIALES POR CATEGORÍA

### A. Categoría 1 — PDA Noctux (Baja Potencia / Model Rocketry)
*   **Restricción Oficial:** Prohibido el uso de compuestos laminados avanzados (fibra de carbono / aramida).
*   **Material FDM Aprobado:** **PLA+** o **PETG estándar** para la ojiva aerodinámica ultraligera.
*   **Espesor de pared:** $0.65\text{ mm}$ a $0.70\text{ mm}$ (1 perímetro continuo reforzado).
*   **Estructura de aletas:** Triplex Okume / Pino 2 mm con *papering* (Kraft + PVA prensado). FDM descartado para aletas en Cat 1 por peso.

### B. Categoría 2 — PDA Stars (Potencia Media / Motor F15-4)
*   **Requerimientos Operativos:** Salida de riel $\ge 55\text{ km/h}$, apogeo $250-350\text{ m}$, radio de impacto $\le 250\text{ m}$.
*   **Material FDM Aprobado:** **PETG estándar** o **ASA**.
*   **Ojiva Stellaris:** Espesor de pared $1.00\text{ mm}$ ($2$ a $3$ perímetros concéntricos).
*   **Aletas FDM (si aplica):** Impresión vertical, $100\%$ perímetros, boquilla endurecida, flujo calibrado al $95\%$ para ahorrar $2\text{ g}$ por aleta y preservar la posición adelantada del Centro de Gravedad ($CG$).

### C. Categoría 3 — PDA Rocketeers (Alta Potencia / Motor G80)
*   **Requerimientos Operativos:** Régimen transónico ($M \approx 0.65 - 0.85$), choque de apertura de paracaídas de $12\text{ a }15\text{ G}$, CanSat de $250-300\text{ g}$, telemetría LoRa $433/915\text{ MHz}$ y GPS activo.
*   **Materiales Aprobados y Restricciones:**
    1.  **ASA (Acrilonitrilo Estireno Acrilato):**
        *   *Piezas:* **Ojiva 102 mm** y **Acople SIDERAL 4" con Asa**.
        *   *Propiedades:* HDT $\approx 100^\circ\text{C}$, tenacidad dinámica ante impacto, **100% de transparencia electromagnética (sin blindaje de señal)**.
    2.  **PETG-CF (PETG Reforzado con Fibra de Carbono):**
        *   *Piezas permitidas:* Anillos de centrado portamotor y soportes mecánicos internos.
        *   *RESTRICCIÓN CRÍTICA:* **PROHIBIDO** en la ojiva, radomo o bahía del CanSat. Las fibras de carbono crean un apantallamiento de jaula de Faraday que atenúa drásticamente el enlace LoRa y satura la señal GPS.
    3.  **Poliuretano Rígido Bicomponente:**
        *   *Aplicación:* Inyección interna en el cono de la ojiva ($Z > 190\text{ mm}$).
        *   *Función:* Disipación de impacto de aterrizaje a $6\text{ m/s}$ sin densificar la pieza completa.

---

## 3. TABLA MAESTRA DE PARÁMETROS EN LAMINADOR (CURA 4.13 EN ESPAÑOL)

Configuraciones validadas para boquilla de **0.40 mm** en impresora **Sunlu T3**:

| Categoría / Ajuste en Cura | Ojiva 102 mm (ASA - Cat 3) | Acople SIDERAL (ASA - Cat 3) | Ojiva 1.0 mm (PETG - Cat 2) | Ojiva 0.65 mm (PLA+ - Cat 1) |
| :--- | :---: | :---: | :---: | :---: |
| **Altura de capa** | 0.16 mm | 0.16 mm | 0.16 mm | 0.20 mm |
| **Altura de capa inicial** | 0.24 mm | 0.24 mm | 0.24 mm | 0.24 mm |
| **Ancho de línea inicial** | 120 % | 120 % | 115 % | 120 % |
| **Recuento líneas de pared** | 4 líneas (ancho 0.45 mm) | 5 líneas (asa maciza 8 mm) | 2 a 3 líneas | 1 línea (ancho 0.65 mm) |
| **Paredes ext. antes que int.** | Desmarcado (Interior primero) | Desmarcado (Interior primero) | Desmarcado | Desmarcado |
| **Alinear costura en Z** | Alineada o Atrás | Alineada o Atrás | Alineada | Alineada |
| **Preferencia de costura Z** | Ocultar costura | Ocultar costura | Ocultar costura | Ocultar costura |
| **Rellenar huecos e/paredes** | En todas partes | En todas partes | En todas partes | No aplica |
| **Capas sup. / Capas inf.** | 5 sup / 5 inf | 6 sup / 5 inf (piso 1 mm) | 4 sup / 4 inf | 3 sup / 3 inf |
| **Densidad de relleno** | 40-50% (solo punta Z>200) | 45 % a 50 % | 15 % (si aplica punta) | 0 % (cuerpo hueco) |
| **Patrón de relleno** | Giroide | Giroide | Giroide | Líneas |
| **Temperatura de impresión** | 245 °C - 250 °C | 245 °C - 250 °C | 235 °C - 240 °C | 205 °C - 210 °C |
| **Temperatura placa (cama)** | 100 °C continuo | 100 °C continuo | 75 °C - 80 °C | 60 °C continuo |
| **Flujo de filamento** | 100 % | 100 % | 95 % a 100 % | 105 % (sobreextrusión) |
| **Velocidad de impresión** | 45 mm/s (Pared: 25 mm/s) | 45 mm/s (Pared: 25 mm/s) | 40 mm/s | 35 mm/s |
| **Retracción (Garganta Bimetálica)**| 2.5 mm a 40 mm/s | 2.5 mm a 40 mm/s | 2.5 mm a 35 mm/s | 2.0 mm a 40 mm/s |
| **Salto en Z al retraer** | Marcado (0.20 mm) | Marcado (0.20 mm) | Desmarcado | Desmarcado |
| **Velocidad de ventilador** | 0-10% (30% escalón Z=45) | 10 % a 15 % máx | 20 % a 30 % | 50 % a 100 % |
| **Generar soporte** | Tocando placa (escalón Z=45) | Tocando placa (vientre asa) | No requerido | No requerido |
| **Bloqueador de soporte** | Cilíndrico (hueco interior) | No aplica | No aplica | No aplica |
| **Distancia Z del soporte** | 0.20 mm a 0.22 mm | 0.20 mm a 0.22 mm | N/A | N/A |
| **Tipo de adherencia (Build)** | Borde (Brim) 10.0 mm | Borde (Brim) 10.0 mm | Borde 8.0 mm | Borde 10.0 mm |
| **Borde solo en el exterior** | Desmarcado (int. y ext.) | Desmarcado (int. y ext.) | Desmarcado | Marcado |

---

## 4. DIRECTIVAS OBLIGATORIAS DE TALLER (SUNLU T3)
1.  **Cabina Térmica:** Queda prohibido imprimir piezas de ASA con la Sunlu T3 destapada. Se debe usar cabina cerrada y precalentar la cama a $100^\circ\text{C}$ durante $15-20\text{ minutos}$ antes de iniciar para estabilizar la cámara entre $40^\circ\text{C}$ y $50^\circ\text{C}$.
2.  **Garganta Bimetálica (*All-Metal*):** Requerida para sostener de forma segura los $245-250^\circ\text{C}$ de extrusión sin degradar el tubo de teflón interno. **Restricción de retracción:** Reducir estrictamente la distancia de retracción en Cura a un rango de $2.0 - 2.8\text{ mm}$ (límite crítico $\le 3.0\text{ mm}$) a $35-45\text{ mm/s}$. Retracciones $\ge 4.0\text{ mm}$ arrastran polímero fundido al cuello frío de metal, generando taponamiento irreversible (*heat creep clog*), especialmente severo en PLA+.
3.  **Desmolde de Soportes en el Asa:** Retirar los soportes inferiores del asa de anclaje con bisturí o pinza fina. Prohibido el uso de alicates de corte que muerdan o rayen el cuerpo cilíndrico de $8\text{ mm}$ (evita concentradores de esfuerzo en eyección).
