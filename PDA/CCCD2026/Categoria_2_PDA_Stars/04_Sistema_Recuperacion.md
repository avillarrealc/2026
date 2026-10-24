# 04 Sistema de Recuperación con Paracaídas - PDA Stars Cat 2

**Regla oficial:** paracaídas obligatorio. Puntaje: apertura óptima abre completo, parcial abre enredado pero frena, sin apertura cero puntos.
**Meta de vuelo total:** **40 a 50 segundos** para motor F (especificación oficial en guía Cat. 2 p4 y p7; 30 a 40 s exclusivo para motor E).
**Resolución técnica clase F:** La actualización oficial de la guía resuelve la discrepancia técnica previa: con apogeo de 300 m y tiempo hasta apogeo/eyección de ~7.5 s, el tiempo de descenso disponible para situarse en la ventana reglamentaria es de **32.5 a 42.5 segundos**, lo que corresponde a una velocidad de descenso nominal de **7.0 a 8.5 m/s**.

---

## 1. Directriz Oficial: Zonas de Recuperación y Deriva (Circular 10-Oct-2026)

> [!CAUTION]
> **REGLA ESTRICTA DE ZONA DE RECUPERACIÓN (RADIO ≤ 250 M EN CAT 2)**
> Según el documento oficial `ZONAS DE RECUPERACIÓN CCCD2026 CAT 2.pdf` emitido por el Comité Técnico del CCCD:
> - Todo cohete de Categoría 2 que aterrice **fuera del radio de 250 metros** desde la zona de lanzamiento será considerado **IRRECUPERABLE A EFECTOS DE LA COMPETENCIA**, anulando el puntaje del vuelo.
> - La condición se evalúa en el instante del aterrizaje, sin considerar si es recuperado físicamente con posterioridad.

### Modelo de Deriva por Viento (Apogeo 300 m con motor F15-4):
La distancia radial de caída $R$ está gobernada por:
$$R = \frac{H_{\text{apogeo}} \cdot V_{\text{viento}}}{V_{\text{descenso}}}$$

Matriz de radio de impacto para **Apogeo = 300 m** (documento oficial CCCD Cat 2):

| Velocidad de Descenso | Viento 1 m/s | Viento 2 m/s | Viento 3 m/s | Viento 4 m/s | Viento 5 m/s | Estado frente al límite (250 m) |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2 m/s** | 150 m | 300 m | 450 m | 600 m | 750 m | ❌ **CRÍTICO:** Viento ≥ 2 m/s descalifica |
| **4 m/s** | 75 m | 150 m | 225 m | 300 m | 375 m | ❌ **CRÍTICO:** Viento ≥ 3.5 m/s descalifica |
| **6 m/s** | 50 m | 100 m | 150 m | 200 m | 250 m | ⚠️ **AL LÍMITE:** A 5 m/s queda exacto en 250 m (T. total ~57 s, excede 50 s) |
| **7.5 a 8.0 m/s (LÍNEA BASE REVISADA)** | **38 m** | **75 m** | **113 m** | **150 m** | **188 m** | ✅ **ÓPTIMO:** Margen de 62 m ante viento 5 m/s + Tiempo total ~45 s (centro de ventana 40–50 s) |
| **9.0 a 9.5 m/s** | **32 m** | **63 m** | **95 m** | **126 m** | **158 m** | ✅ **SEGURO:** Margen de 92 m + Tiempo total ~39–41 s |

### Conclusión Técnica y Blindaje de Diseño:
Con la ventana oficial de **40 a 50 segundos** para motor F:
1. Un paracaídas sobredimensionado (> 70 cm) que descienda a < 6 m/s causa **descalificación por tiempo** (toma > 55 s) y riesgo crítico de deriva fuera de los 250 m con viento moderado.
2. Un descenso a > 10 m/s aterrizaría en < 38 s, quedando **descalificado por aterrizaje prematuro** (por debajo de los 40 s reglamentarios).
3. **Configuración definitiva obligatoria:**
   - Paracaídas de **Ø 45 a 50 cm** (nylon ripstop con cuerdas trenzadas).
   - Velocidad de descenso objetivo: **7.5 a 8.2 m/s**.
   - Tiempo de vuelo total proyectado: **44 a 47 segundos** (centrado con holgura dentro de los 40–50 s).
   - Deriva máxima calculada ante viento de 5 m/s: **180 a 190 metros** (margen seguro de 60 a 70 m dentro del radio de 250 m).

## 2. Armado que sí abre

- Manta Nomex entre motor y paracaídas siempre. Sin manta el flamazo quema la tela.
- Cordón de choque Kevlar de mínimo 2 metros, doblado en Z sin nudos duros.
- Paracaídas doblado en rollo, no en bola. Las líneas estiradas sin enredos.
- Carga de eyección del F15-4 con retardo 4 s. No la toquen ni la cambien.
- Prueba en tierra: metan todo, soplen por el tubo de montura o tiren del cordón. Debe salir suave en menos de 2 segundos.
- Acopladores (DCP, Sesión Informativa 1 §05): los que se separan en recuperación exigen extensión mínima de 1 calibre (diámetro del fuselaje) a cada lado del punto de separación. Los que no se separan van con extensión máxima posible o 1 calibre, fijados con uniones mecánicas o adhesivos permanentes. Verificar con regla antes de cada vuelo.

Es como doblar una sombrilla mojada: si la meten a la brava se traba. Si la enrollan con calma abre de una.

## 3. Tabla de pruebas de eyección y descenso

| Fecha | Prueba | Paracaídas | Resultado | Tiempo medido | Arreglo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | Eyección en mesa | 75 cm | Salió / se trabó | ___ s en salir | |
| | Caída desde 2° piso | 75 cm | Abrió completo / parcial | ___ s | |
| | Vuelo bajo de prueba | 75 cm | Óptima / parcial / sin apertura | ___ s total | |
| | Vuelo oficial simulado | Final | | ___ s, altura ___ m | |

## 4. Qué guardar en esta carpeta

- Foto del paracaídas extendido con metro.
- Foto del doblez en Z paso a paso.
- Video de cada prueba de eyección.
- Factura del paracaídas, Kevlar y Nomex para el presupuesto.
