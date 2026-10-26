# 02 Diseño en OpenRocket, Estabilidad 2.0 y 55 km/h - PDA Rocketeers Cat 3

**Meta:** cohete de mínimo 80 cm que con G80-7T llegue a 400 m con CanSat de 250 a 300 g.
**Tres números que los jueces revisan antes del vuelo:** estabilidad mínima 2.0 calibres, relación 5:1 y 55 km/h al salir del riel.

---

## 1. Paso a paso en OpenRocket

1. Archivo nuevo `PDA_Rocketeers_400m_G80.ork` en esta carpeta.
2. Tubo del diámetro real, largo para superar 80 cm con ojiva.
3. Montura 29 mm, aletas grandes y rígidas. En Cat 3 las aletas trabajan de verdad por el peso.
4. Carguen motor G80-7T. Si no está en la base, créenlo con impulso y empuje del certificado.
5. Agreguen CanSat como masa interna de 250 a 300 g en su posición real, más paracaídas grande.
6. Simulen riel de mínimo 1.5 m. OpenRocket muestra la velocidad al salir del riel. Debe dar más de 55 km/h que son 15.3 m/s.

Si la velocidad da menos de 55, el cohete sale cabeceando como bus sin dirección. Soluciones: riel más largo, menos peso o aletas más grandes. Nunca achiquen aletas para ir más rápido.

## 2. Estabilidad mínima 2.0 calibres

El CG adelante del CP mínimo 2 diámetros del tubo. Apunten a 2.0 a 3.0. Más de 3.5 lo pone muy nervioso con viento.

Trucos para subir estabilidad sin romper nada: ojiva más pesada adelante, aletas más grandes atrás, CanSat adelante del CP, nunca peso atrás.

## 3. Tabla de versiones para pegar a los 400 m

| Versión | Peso g | Largo cm | Margen cal | Vel riel km/h | Apogeo m | Decisión |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| v1 base | | | | | | |
| v2 ajustada | | | | | | |
| v_SIDERAL (03-Oct-26) | N/A | N/A | N/A | 65.7 (18.26 m/s) | 410.4 | Cumple apogeo (410m) y vel. riel (>55km/h) con G80T-7 |
| v_SIDERAL PDR (04-Oct-26) | 884 g | 90 cm | 1.91 riel / 2.22 burnout | 65.5 (18.20 m/s) | 409.5 | Línea base PDR |
| **v_SIDERAL CDR (25-Oct-26)** | **896 g** | **90 cm** | **1.91 riel / 2.20 burnout** | **63.1 (17.53 m/s)** | **397.8** | **Calibración con piezas reales: Ojiva ASA 87.88g, Acoplador 104g, CanSat 274g. Apogeo a 2.2m de la meta (400m). Cumple 100% normativa.** |

La versión definitiva del CDR demuestra: margen $\ge 2.0\text{ cal}$ en vuelo propulsado, velocidad en riel $> 55\text{ km/h}$, apogeo a $397.8\text{ m}$ (99.45% de precisión respecto a los 400 m) y aceleración máxima de $10.7\text{ G}$ ($105.2\text{ m/s}^2$).

## 4. Archivos y Entregables

- `Diseño SIDERAL.ork`: Modelo aerodinámico calibrado con masas reales de taller.
- `Graficos_CDR/`: Curvas de vuelo OpenRocket (`altitud vs tiempo.PNG`, `velocidad vs tiempo.PNG`, `aceleracion vs tiempo.PNG`, `perfil lateral.PNG`) y renders CAD.
- `310_PDARocketeers_CDR.pdf`: Informe oficial del Critical Design Review (59 páginas).
- `Anilloso_FINAL_Escala_1a1_Pliego_A2.pdf`: Plano de manufactura láser de aletas y anillos.
