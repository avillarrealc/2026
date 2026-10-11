# 04 Sistema de Recuperación - PDA Rocketeers Cat 3

**Regla oficial:** paracaídas obligatorio. Puntaje óptima, parcial o sin apertura. Aquí el cohete pesa más de 1 kg, el paracaídas manda.

---

## 1. Directriz Oficial: Zonas de Recuperación y Deriva (Circular 10-Oct-2026)

> [!CAUTION]
> **REGLA ESTRICTA DE ZONA DE RECUPERACIÓN (RADIO ≤ 400 M)**
> Según el documento oficial `ZONAS DE RECUPERACIÓN CCCD2026 CAT 3.pdf` emitido por el Comité Técnico del CCCD:
> - Todo cohete que aterrice **fuera del radio de 400 metros** desde la zona de lanzamiento será declarado **IRRECUPERABLE A EFECTOS DE LA COMPETENCIA**, anulando el puntaje del vuelo, independientemente de que se localice físicamente con posterioridad.
> - La condición se juzga estrictamente en el momento del impacto contra el suelo.

### Modelo de Deriva por Viento (Apogeo 400 m nominal):
La distancia radial de caída $R$ está gobernada por:
$$R = \frac{H_{\text{apogeo}} \cdot V_{\text{viento}}}{V_{\text{descenso}}}$$

Matriz de radio de impacto para **Apogeo = 400 m** (documento oficial CCCD Cat 3):

| Velocidad de Descenso | Viento 1 m/s | Viento 2 m/s | Viento 3 m/s | Viento 4 m/s | Viento 5 m/s | Estado frente al límite (400 m) |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2 m/s** | 200 m | 400 m | 600 m | 800 m | 1000 m | ❌ **CRÍTICO:** Viento > 2 m/s descalifica |
| **4 m/s** | 100 m | 200 m | 300 m | 400 m | 500 m | ⚠️ **RIESGOSO:** Viento > 4 m/s descalifica |
| **6 m/s** | 66 m | 133 m | 200 m | 266 m | 333 m | ✅ **SEGURO:** Se mantiene dentro del radio a 5 m/s |
| **6.95 m/s (SIDERAL)** | **57 m** | **115 m** | **172 m** | **230 m** | **288 m** | ✅ **LÍNEA BASE SIDERAL:** Margen de seguridad 112 m |
| **8 m/s** | 50 m | 100 m | 150 m | 200 m | 250 m | ✅ **SEGURO:** Margen amplio |
| **10 m/s** | 40 m | 80 m | 120 m | 160 m | 200 m | ⚠️ Riesgo de sobreaceleración al CanSat |

### Conclusión de Diseño para SIDERAL:
1. **Ventana óptima de descenso:** **6.0 a 7.0 m/s**.
   - Menos de 5.5 m/s: Con ráfagas térmicas de 4 a 5 m/s en Santa Fe de Antioquia, el cohete deriva fuera de los 400 m (descalificación).
   - Más de 7.5 m/s: Puede comprometer la estructura de la carga útil CanSat.
2. **Dimensionamiento del Paracaídas:**
   - Paracaídas semiesférico de **Ø 70 cm** ($C_d = 0.8$, verificado en `Diseño SIDERAL.ork`).
   - Masa total al toque de suelo: 827 g.
   - Velocidad terminal verificada: **6.95 m/s**.
   - Deriva máxima calculada con viento límite de 5 m/s (18 km/h): **288 metros** (holgura de 112 m dentro del perímetro legal de 400 m).

## 2. Armado y Enlace Mecánico con Motor G80T

- **Protección Térmica:** Manta ignífuga Nomex de alta densidad ($15 \times 15\text{ cm}$) entre montura del motor y paracaídas. El AeroTech G80T libera una carga eyectora de alta energía.
- **Línea de Choque:** Cordón Kevlar de 3,0 m (longitud verificada en ORK, factor de amortiguamiento contra shock de eyección). Doblado en patrón en Z, sin nudos restrictivos.
- **Plegado:** Paracaídas empacado cilíndricamente en rollo, líneas de suspensión desrejadas y peinadas.
- **Eyección del G80-7T:** Retardo nominal de 7.0 s (OpenRocket calcula retardo óptimo en 7.31 s; delta de 0.31 s plenamente tolerable a 6.58 m/s de velocidad de despliegue).
- **Inspección en Tierra:** Prueba de deslizamiento por gravedad: la carga de recuperación debe desalojar el fuselaje superior en menos de 2 s ante tracción manual moderada.
- **Acopladores (DCP §05 / Sesión Informativa 1):**
  - Acoplador de separación: Inserción mínima de **1 calibre** (102 mm) a cada lado del plano de corte.
  - Acopladores fijos: Inserción mínima de 1 calibre fijada con adhesivo estructural epóxico.

## 3. Tabla de pruebas

| Fecha | Prueba | Resultado | Tiempo | Arreglo |
| :--- | :--- | :--- | :---: | :--- |
| | Eyección en mesa | Salió / se trabó | ___ s | |
| | Caída piso alto | Óptima / parcial | ___ s | |
| | Vuelo de prueba | Óptima / parcial / sin | ___ s, ___ m | |
