# 03 Carga Útil Electrónica y Evaluación en Tierra - PDA Stars (Cat. 2)

**Normativa Oficial de Referencia:** `Guia_Carga_Util_Intermedios_2026.pdf` (Versión 1.0.0, SateLab - ALAS)  
**ID de Misión Oficial:** 211 | **Vehículo:** PDA Stars | **Motor Asignado:** Estes F15-4 (29 mm)  
**Evaluación Oficial:** Evaluación presencial en tierra previa al vuelo (Rúbrica SPP §3.8, escala de 0 a 100 puntos). Sin evaluación técnica aprobada en tierra no se autoriza el lanzamiento.

---

## 1. Requisitos Técnicos y Restricciones Obligatorias (Guía Oficial 2026)

Conforme a la **Guía Carga Útil Intermedios 2026**, la carga útil de PDA Stars debe cumplir estrictamente con los siguientes parámetros de ingeniería:

| Parámetro | Límite Reglamentario Obligatorio | Referencia Normativa | Impacto en el Diseño PDA Stars |
| :--- | :--- | :--- | :--- |
| **Masa Máxima** | **$\mathbf{\le 60\text{ g}}$** (sistema ensamblado completo) | Guía §2.1 y §2.2 | Masa estricta total: estructura, electrónica, sensores y batería. |
| **Materiales Permitidos** | PLA, PETG, ABS, Fibra de vidrio | Guía §2.3 | Carcasa modelada e impresa en PETG o PLA liviano. |
| **Autonomía Eléctrica** | **Mínimo 4 horas** continuas de operación | Guía §3.1 | Cálculo obligatorio de consumo ($I_{\text{prom}} \times 4\text{ h} \le C_{\text{bat}}$). |
| **Baterías Prohibidas** | **LiPo** y **Li-Ion en empaque plano rectangular** | Guía §3.1.1 | Totalmente descartadas por riesgo de ignición por shock dinámico. |
| **Baterías Permitidas** | AA/AAA no recargables, 18650, Li-Ion cilíndricas, 9V, botón | Guía §3.1.2 | Selección orientada por balance de masa ($\le 60\text{ g}$). |
| **Sistema de Switches** | **Interruptor accesible externamente** | Guía §3.2 | Activación segura en rampa sin abrir ni desarmar el cohete. |
| **Sistema de Retención** | **Unión estructural obligatoria permanente** | Guía §5 | Prohibida la liberación/separación total; sujeción al cordón de choque. |
| **Computadora de Vuelo** | Control embebido autónomo | Guía §3.3 | Adquisición, procesamiento y registro de datos en microcontrolador. |
| **Sensores** | Selección libre según objetivo de misión | Guía §3.4 | BMP280 (presión, temperatura y altitud barométrica). |
| **Telecomunicaciones** | Opcional (normativa Mintic / bandas permitidas) | Guía §3.5 | Telemetría LoRa 915 MHz opcional o registro a bordo en MicroSD. |

---

## 2. Balance de Masa y Selección del Sistema de Alimentación

El límite reglamentario de **$60\text{ g}$** restringe drásticamente la masa de la fuente de poder:
* **Descarte técnico de celda 18650:** Una batería 18650 estándar pesa entre **$45\text{ y }48\text{ g}$**, lo cual consumiría el **75–80%** de la masa total permitida, dejando únicamente $12\text{ a }15\text{ g}$ para la estructura, cables, microcontrolador y sensores (riesgo crítico de sobrepeso).
* **Descarte técnico de batería 9V:** Masa promedio de **$45\text{ g}$** con baja densidad de energía útil.
* **Configuración seleccionada (Línea Base PDA Stars):**
  * **Opción A (Recomendada):** Pack de **$2 \times \text{AAA}$ alcalinas no recargables en serie** ($3.0\text{ V}$ nominales, peso total: **$23.0\text{ g}$**, capacidad: $\approx 1000\text{–}1200\text{ mAh}$). Proporciona $>15\text{ horas}$ de autonomía a un microcontrolador de bajo consumo.
  * **Opción B (Alternativa compacta):** Celda **Li-Ion cilíndrica 14500** ($3.7\text{ V}$, peso: **$19.5\text{ g}$**, capacidad: $800\text{ mAh}$) con regulador LDO de $3.3\text{ V}$.

### Desglose de Masa de la Carga Útil (Tolerancia: $\le 60.0\text{ g}$)

| Componente | Especificación Técnica | Masa Nominal | Subtotal Acumulado |
| :--- | :--- | :---: | :---: |
| **Microcontrolador** | ESP32-WROOM-32D DevKit (o Arduino Nano Every) | $8.5\text{ g}$ | $8.5\text{ g}$ |
| **Sensor Ambiental** | Módulo BMP280 (I2C / SPI, presión + temperatura) | $1.8\text{ g}$ | $10.3\text{ g}$ |
| **Almacenamiento** | Módulo MicroSD SPI + Memoria 16 GB | $2.5\text{ g}$ | $12.8\text{ g}$ |
| **Fuente de Poder** | $2 \times$ Pilas AAA alcalinas con portapilas liviano | $24.5\text{ g}$ | $37.3\text{ g}$ |
| **Switch Externo** | Conmutador deslizante mini con seguro mecánico | $1.2\text{ g}$ | $38.5\text{ g}$ |
| **Cableado y Soldadura** | Cable siliconado AWG 28 y conectores micro JST | $3.5\text{ g}$ | $42.0\text{ g}$ |
| **Carcasa Estructural** | Bahía cilíndrica impresa en PETG (pared 1.2 mm) | $12.0\text{ g}$ | **$54.0\text{ g}$** |
| **Margen de Seguridad** | Colchón de tolerancia para calibración oficial | **$6.0\text{ g}$** | **$60.0\text{ g}$ / Máx 60.0 g** |

---

## 3. Arquitectura del Sistema de Encendido Externo (Guía §3.2)

1. **Requerimiento en rampa:** El cohete se instala en la plataforma con el motor F15-4 preparado. La carga útil debe encenderse en los últimos 2 minutos antes del despeje de la zona sin desmontar la ojiva ni desacoplar el fuselaje.
2. **Implementación:**
   * Interruptor micro-deslizante montado a ras del fuselaje en un receso (*bezel*) protegido contra ramas o viento.
   * Alternativa redundante: Clavija tipo "Remove Before Flight" (pin jack tipo puente normalmente cerrado extraíble mediante cordón).
   * LED de estado superficial visible desde el exterior para confirmar adquisición e inicialización del sensor antes del encendido del motor.

---

## 4. Retención Estructural y Sistema de Recuperación (Guía §5)

> [!CRITICAL]
> **PROHIBICIÓN TOTAL DE DESPRENDIMIENTO O EYECCIÓN LIBRE:**  
> La Guía de Carga Útil Intermedios §5 dictamina: *"La separación total de la carga útil respecto al vehículo será considerada una falla crítica de recuperación y podrá derivar en penalizaciones o invalidación de la misión."*

* **Anclaje mecánico:** La carcasa de la carga útil cuenta con un ojal estructural macizo integrado en el modelado 3D (PETG con 5 perímetros, probado a carga de tracción $\ge 250\text{ N}$).
* **Integración al tren de recuperación:** El ojal se conecta directamente al cordón de choque principal de Kevlar mediante un eslabón rápido (*quick-link*) de acero inoxidable, ubicándose amortiguada entre la ojiva y el paracaídas principal.

---

## 5. Misión Científica: Perfil Barométrico y Microclimático PDA Stars

* **Objetivo de Misión:** Mapeo de gradiente vertical de presión, temperatura y aceleración barométrica en ascenso hacia los $300\text{ m}$ de apogeo nominal, correlacionando la curva barométrica del sensor a bordo con la lectura oficial del altímetro Jolly Logic / Estes de la competencia.
* **Criterios de Éxito:**
  1. Adquisición continua a frecuencia $\ge 10\text{ Hz}$.
  2. Almacenamiento no volátil en formato CSV dentro de la MicroSD (`TIME, PRESS, TEMP, ALT_EST`).
  3. Integridad física estructural y retención al fuselaje sin desprendimiento tras el choque de aterrizaje.
  4. Entrega de informe gráfico a los jurados en la sustentación presencial de tierra.

---

## 6. Protocolo de Evaluación en Tierra Frente a Jurados (100 Puntos)

La evaluación de la carga útil se realiza en la mesa técnica antes de pista:

1. **Inspección de Masa Oficial:** Verificación en balanza de calibración del concurso: registro $\le 60.0\text{ g}$.
2. **Inspección de Batería:** Certificación visual de celda autorizada (cilíndrica / alcalina; ausencia de celdas LiPo planas).
3. **Prueba Operacional en Vivo:**
   * Accionamiento del switch externo.
   * Lectura de datos en tiempo real mediante telemetría LoRa o volcado de prueba de MicroSD en la estación terrena / PC de campo.
4. **Demostración de Desarrollo Propio:** Sustentación del esquema electrónico, código fuente desarrollado por el equipo (en C++/Arduino/MicroPython) y diseño CAD de la bahía. Prohibido el uso de kits prearmados.
5. **Simulación de Retención:** Verificación de resistencia del anclaje al cordón de recuperación.
