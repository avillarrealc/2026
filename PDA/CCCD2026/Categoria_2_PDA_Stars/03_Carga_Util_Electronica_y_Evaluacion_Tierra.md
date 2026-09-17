# 03 Carga Útil Electrónica y Evaluación en Tierra - PDA Stars Cat 2

**Regla oficial:** la carga la diseñamos y construimos nosotros. Los jurados la evalúan en tierra antes del vuelo. Sin esa evaluación no hay puntos de carga ni vuelo válido.
**Tamaño guía del altímetro oficial:** 15 x 20 x 55 mm y 10 a 12 g. Nuestra carga debe caber con el altímetro sin apretar cables.

---

## 1. Misión de nuestra carga, en sencillo

Elijan UNA misión y no la cambien a mitad de camino. Tres opciones que sí podemos hacer en el colegio:

- Opción A Clima de La Tablaza: temperatura, humedad y presión durante el vuelo. Sirve para comparar con datos del SIATA.
- Opción B Calidad del aire: sensor de partículas o gases liviano más temperatura. Sirve para el proyecto AeroBio.
- Opción C Telemetría viva: ESP32 con LoRa que manda altura y posición en vivo a un celular en tierra.

Piensen en la carga como el pasajero del bus: debe ir amarrado, no gritar, no mover el bus y bajarse sano.

## 2. Lista de partes y presupuesto guía

| Parte | Ejemplo | Peso aprox | Para qué sirve |
| :--- | :--- | :---: | :--- |
| Cerebro | ESP32 o Arduino Nano | 7 a 10 g | Lee sensores y guarda datos |
| Sensor clima | BMP280 o DHT22 | 2 a 5 g | Temperatura, humedad, presión |
| Guardado | MicroSD o memoria interna | 2 g | No perder datos si se apaga |
| Batería | LiPo 1S 300 a 500 mAh | 8 a 14 g | Energía de a bordo |
| Cables y cinta | Jumpers cortos | 5 g | Conexiones sin enredos |
| Estructura | Tubo o cajita impresa | 15 a 25 g | Que no se mueva en el vuelo |
| Altímetro oficial | Jolly Logic o Estes | 10 a 12 g | Prueba oficial de 200 m |

Todo esto sumado no puede pasar el total de 480 g del cohete completo. Pésenlo junto en la ficha 01.

## 3. Esquema de conexión para copiar

```
Batería LiPo -> Cerebro ESP32 (VIN y GND)
BMP280 -> ESP32 (VCC 3V3, GND, SCL, SDA)
MicroSD -> ESP32 (SPI)
Altímetro Jolly Logic o Estes -> aparte con su espuma, sin cables compartidos
Interruptor externo -> para prender sin abrir el cohete
Buzzer -> para encontrar la carga en el pasto
```

Código mínimo que debe hacer: prender, pitar una vez, leer sensores cada medio segundo, guardar con hora, parpadear un led. Si no guarda en MicroSD, no sirve.

## 4. Guion literal para la evaluación en tierra frente a jurados

Practíquenlo en el salón como una exposición de 5 minutos. Cada uno dice su parte:

1. Saludo y misión en 30 segundos: somos PDA Stars de La Estrella, nuestra carga mide tal cosa para tal objetivo.
2. Muestren la carga prendida y el sensor leyendo en vivo en el PC o celular.
3. Expliquen qué diseñaron ustedes: estructura, código, pruebas. Nada comprado ya armado vale como diseño propio.
4. Muestren gráfica de una prueba en tierra: déjenla caer 10 m con una cuerda o súbanla al segundo piso y grafiquen.
5. Cierren con peso y seguridad: pesa tantos gramos, va sujeta así, no interfiere con el paracaídas ni el altímetro.

Lleven impreso: esquema, código de una página, tabla de pruebas y peso. Eso enamora jurados de NASA y SpaceX más que palabras.

## 5. Tabla de pruebas de la carga

| Fecha | Prueba | Qué medimos | Resultado | Falla y arreglo |
| :--- | :--- | :--- | :--- | :--- |
| | Banco en mesa 10 min | Si guarda sin apagarse | | |
| | Caída suave 10 m | Si sigue leyendo | | |
| | Vibración y golpe leve | Si no se suelta nada | | |
| | Prueba completa con altímetro | Si conviven sin interferir | | |

## 6. Qué guardar en esta carpeta

- Foto de la carga armada con regla al lado.
- Esquema a mano o en Tinkercad con nombres.
- Código con fecha y nombre del archivo.
- Video de 1 minuto de la carga leyendo en vivo.
- Hoja impresa que se lleva a jurados.
