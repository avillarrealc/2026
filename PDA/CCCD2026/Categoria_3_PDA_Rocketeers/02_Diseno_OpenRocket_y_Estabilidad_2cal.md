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
| v3 final 400 m | | | | | | |

La v3 final debe mostrar en pantallazo: margen mayor a 2.0, velocidad mayor a 55, apogeo cerca de 400, relación 5:1 cumplida.

## 4. Qué guardar

- `PDA_Rocketeers_400m_G80.ork` final más copia v1.
- Pantallazos: diseño con CG-CP, tabla de simulación con velocidad de riel, curva de vuelo.
- Foto del cohete real junto al metro.
