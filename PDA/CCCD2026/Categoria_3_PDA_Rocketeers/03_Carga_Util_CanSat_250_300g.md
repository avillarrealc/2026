# 03 Carga Útil CanSat 250 a 300 g - PDA Rocketeers Cat 3

**Regla oficial:** CanSat funcional tamaño lata, 250 a 300 g, diseñado y construido por el equipo. Se cuenta desde el primer diseño. Prohibidos animales vertebrados. Objetivos científicos, tecnológicos o de ingeniería.
**Contradicción normativa registrada:** Guía CanSat v1.0.0 §2.1 (gráfico p5) admite 250-350 g, pero Guía Categoría Avanzados exige 250-300 g. Criterio operativo sin ambigüedad: máximo duro **300 g** (cumple ambos documentos). Rango 300-350 g queda vedado hasta aclaración escrita del revisor. Dimensiones máximas: 115 x 66 mm.

---

## 1. Misión del CanSat, elijan una y no la cambien

- Opción A Clima vertical de La Estrella: temperatura, humedad, presión y altura para comparar con SIATA. Perfecta para enlazar con AeroBio.
- Opción B Calidad del aire en altura: partículas o gases más GPS y registro en MicroSD.
- Opción C Telemetría en vivo: ESP32 con LoRa mandando altura, posición y batería a la estación de tierra.

El CanSat es como una lonchera que se tira del bus en marcha: debe sobrevivir al golpe, seguir hablando y no romper nada del bus.

## 2. Arquitectura Estructural (Diseño CAD V2)

El diseño físico del CanSat está estandarizado paramétricamente en Fusion 360 bajo los siguientes constraints:
- **Dimensiones Máximas:** Altura de 115 mm x OD 66 mm (zona de agarre superior).
- **Mecanismo de Retención:** Roscas Trapezoidales (Tr64x4) sincronizadas arriba y abajo para anclaje a las matrices del cohete. Offset de -0.20 mm para tolerancia FDM.
- **Ventilación y Telemetría:** Corte tipográfico "PDA" usando fuente Stencil (para evitar colapso de islas centrales) y exoesqueleto matriz hexagonal (Honeycomb/Isogrid) para alivio térmico, reducción de masa e ingreso de flujo de aire al sensor BMP280.
- **Aviónica (PCB):** Ancho máximo interno admitido para electrónica es de **58 mm - 59 mm** (montaje vertical) fijado con encapsulado de espuma de poliuretano (Potting) para absorción de impactos.

## 3. Partes y peso controlado al gramo

| Parte | Ejemplo | Peso aprox |
| :--- | :--- | :---: |
| Estructura CanSat | Chasis celular hexagonal impreso en PETG/ASA | 40 a 60 g |
| Cerebro | ESP32 | 7 a 10 g |
| Sensores | BMP280 + GPS + gas o partículas | 20 a 40 g |
| Batería | 18650 Li-Ion cilíndrica permitida (LiPo prohibida, Guía CanSat §3.1); autonomía mínima 4 h | 40 a 70 g |
| Paracaídas propio del CanSat si aplica | Tela pequeña | 15 a 25 g |
| Tornillos, espuma (Potting), cables | | 20 g |
| **TOTAL CanSat** | **Debe dar 250 a 300 g** | **___ g** |

Si da menos de 250 g agreguen lastre útil: más batería o carcasa más fuerte. Si pasa de 300 g cambien batería y carcasa primero, nunca quiten sensores.

## 4. Conexión guía

```
Batería -> interruptor externo -> ESP32
BMP280 -> 3V3, GND, SCL, SDA
GPS -> TX, RX y antena al cielo
MicroSD -> SPI para guardar cada medio segundo
Buzzer + led -> para encontrarlo en el lote
Altímetro oficial -> fuera del CanSat, con su espuma propia
```

Código mínimo: prende, pita, lee sensores, guarda con tiempo, transmite si es telemetría, parpadea. Prueba de 30 minutos en mesa sin apagarse.

## 5. Guion de 5 minutos para jurados

1. Misión en 30 segundos y por qué sirve a La Estrella.
2. CanSat prendido leyendo en vivo en el PC.
3. Qué diseñamos nosotros: estructura, código, pruebas. Muestren algo fallado y cómo lo arreglaron.
4. Gráfica de prueba real: subida al segundo piso o caída con cuerda.
5. Peso exacto ___ g, sujeción en el cohete, no interfiere con recuperación ni altímetro.

Lleven impreso: esquema, código resumido, tabla de pruebas, peso con foto de balanza.

## 6. Tabla de pruebas

| Fecha | Prueba | Resultado | Arreglo |
| :--- | :--- | :--- | :--- |
| | Mesa 30 min | | |
| | Caída 10 m con cuerda | | |
| | Vibración y golpe | | |
| | Integración con cohete y altímetro | | |
