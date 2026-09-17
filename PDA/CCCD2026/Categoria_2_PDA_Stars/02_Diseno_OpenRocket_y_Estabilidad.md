# 02 Diseño en OpenRocket y Estabilidad - PDA Stars Cat 2

**Meta:** cohete de mínimo 60 cm y máximo 480 g con E12-4 que llegue a 200 m y vuele 30 a 40 s en total.
**Programa:** OpenRocket gratis en los PC del colegio. Curso base: Introducción a OpenRocket y Fundamentos de Estabilidad del Dashboard.

---

## 1. Paso a paso para simular, sin perderse

1. Abran OpenRocket, archivo nuevo, pónganle nombre `PDA_Stars_200m_E12-4.ork` y guárdenlo en esta carpeta.
2. Creen el tubo principal con el diámetro real que compramos y largo para que el cohete total dé más de 60 cm.
3. Agreguen ojiva parabólica o cónica, montura de motor 24 mm y 3 o 4 aletas trapezoidales.
4. En motores elijan Estes E12-4. Si no aparece, cárguenlo manual: impulso total 27 a 30 N-s, retardo 4 s.
5. Agreguen paracaídas con el diámetro real que vamos a comprar y el peso total medido en la ficha 01.
6. Corran la simulación sin viento primero y anoten. Luego prueben con viento 3 m/s y 5 m/s.

Ojo muchachos: simular es como ensayar la ruta del integrado en un mapa antes de salir. Si en el mapa ya se estrella, en la calle también.

## 2. CG y CP explicado en una frase

El CG es donde se equilibra el cohete en un dedo. El CP es donde empuja el aire. El CG debe ir adelante del CP mínimo un diámetro del tubo. Eso es 1 calibre. Lo ideal para nosotros es entre 1.5 y 2.5 calibres.

Si el margen da menos de 1, el cohete sale loco como trompo. Si da más de 3, va muy rígido y el viento lo acuesta. Apunten a 1.5 a 2.5.

## 3. Tabla de resultados que exige el jurado

Llenen una fila por cada versión del diseño. La versión que vuela es la que dé cerca de 200 m.

| Versión | Peso sim (g) | Largo (cm) | CG (cm) | CP (cm) | Margen (cal) | Apogeo sim (m) | Tiempo sim (s) | Velocidad máx (m/s) | Decisión |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| v1 base | | | | | | | | | |
| v2 más liviana | | | | | | | | | |
| v3 final a 200 m | | | | | | | | | |

Criterio para decir muy estable el día del vuelo: ascenso recto y controlado. Si se tuerce un poco es medianamente estable. Si cabecea o gira es inestable y perdemos esos puntos.

## 4. Trucos para pegar a los 200 m sin pasarse

- Si la simulación da más de 220 m, no cambien el motor. Suban un poco de peso útil o usen paracaídas un poco más grande para frenar y alargar el tiempo hacia 35 s.
- Si da menos de 180 m, bajen peso: lijen pintura, acorten tornillos, batería más liviana.
- Si el tiempo da menos de 30 s, el paracaídas está muy pequeño o abre tarde. Si da más de 40 s, el paracaídas es muy grande y nos pasamos del tiempo.
- Guarden pantallazo de cada simulación: ventana de diseño con CG-CP visible y gráfica de altura contra tiempo.

## 5. Qué guardar en esta carpeta

- Archivo `PDA_Stars_200m_E12-4.ork` versión final y una copia v1.
- 3 pantallazos: diseño lateral con CG-CP, tabla de simulación, curva de vuelo.
- Foto del cohete real al lado del metro para comparar con el diseño.
