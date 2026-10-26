# 06 Bitácora de Vuelos y Presupuesto Cat 3 - PDA Rocketeers

**Uso:** una fila por prueba y por gasto. Todo gasto se copia al Excel general en su categoría 1 a 7.

---

## 1. Bitácora de pruebas

| Fecha | Lugar | Versión | Peso g / techo | Altura m / 400 | Vel riel | Recuperación | Estabilidad | Aprendimos |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| 03-Oct-26 | Simulación | v_SIDERAL | N/A | 410.4 m | 65.7 km/h | 6.55 m/s | N/A | CSV anterior, reemplazado el 04-10-2026 |
| 04-Oct-26 | Simulación | v_SIDERAL línea base PDR | 884 g | 409.5 m | 65.5 km/h (18.20 m/s) | 6.58 m/s despliegue, 6.95 suelo | 2.2 cal prom (1.91 riel) | Línea base PDR S6+S7, cordón 3.0 m |
| 25-Oct-26 | Simulación | v_SIDERAL calibrada CDR (`Diseño SIDERAL.ork`) | 896 g (despegue) / 824 g (descenso) | 397.8 m | 63.1 km/h (17.53 m/s) | 7.65 m/s despliegue, 7.06 suelo | 2.20 cal burnout (1.91 salida riel) | Calibración final con componentes físicos (ojiva ASA 87.88g, acoplador 104g, CanSat 274g, motor G80-7T). Apogeo a solo 2.2 m del objetivo (400 m). |
| | | v1 | | | | | | |
| | | v2 | | | | | | |
| | | v3 final | | | | | | |

Cada fila con pantallazo, foto de balanza, video y lectura de altímetro.

### 1.1 Hitos y Revisiones Técnicas Oficiales (Staff CCCD)

| Fecha | Hito / Instancia | Revisor Oficial | Estado / Resultado | Observaciones Técnicas Principales |
| :---: | :--- | :--- | :---: | :--- |
| **19-Oct-2026** | **Segunda Revisión Técnica Virtual** | Juan Sebastián Fonseca (TRA #36180 L1) | **Aprobada (Sobresaliente)** | Avance físico y funcional >80% de SIDERAL. Validación de fuselaje 102 mm, ojiva Haack ASA, aletas sándwich balso / PETG-CF, montura de motor 29 mm para AeroTech G80-7T, estabilidad estática $\ge 2.0\text{ cal}$, velocidad en riel $\ge 55\text{ km/h}$, aviónica/CanSat (250–300 g) con batería 18650 y paracaídas calibrado a $\sim 6.95\text{ m/s}$ para radio de 400 m. Habilitado para CDR (25-Oct). |
| **25-Oct-2026** | **Critical Design Review (CDR)** | Staff Técnico CCCD / Plataforma | **Desarrollado (59 págs)** | Documento formal `310_PDARocketeers_CDR.pdf` consolidado bajo formato AIAA / LaTeX. Cubre diseño definitivo, calibración de masas, telemetría LoRa 915 MHz, filtro EKF, paracaídas Ø 70 cm con derrame de 7 cm, análisis de seguridad y pruebas en tierra. |

## 2. Gastos propios Rocketeers

| Fecha | Factura | Qué compramos | Cant | Valor COP | Categoría 1-7 | Responsable |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| | | Motor Aerotech G80-7T | | | 1 Propulsión | |
| | | Altímetro Jolly Logic o Estes | | | 4 Aviónica | |
| | | Tubo, ojiva, aletas 29 mm | | | 2 Estructura | |
| | | Paracaídas 110+ cm + Kevlar + Nomex | | | 3 Recuperación | |
| | | CanSat ESP32 + sensores + GPS + batería | | | 4 Aviónica | |
| | | Riel y retén 29 mm | | | 5 Taller | |
| | | Transporte campo grande | | | 6 Logística | |

Total Rocketeers: ___ COP. Foto de cada factura a Drive con enlace en el Excel general.

## 3. Pendientes

- [ ] Comprar altímetro y reservar G80 con la organización
- [ ] Copiar datos reales del motor y calcular techo 5:1
- [ ] Cerrar v3 a 400 m con 2.0 calibres y 55 km/h
- [ ] Pasar los 7 cursos del Dashboard y guardar certificados
- [ ] 2 pruebas antes del oficial
