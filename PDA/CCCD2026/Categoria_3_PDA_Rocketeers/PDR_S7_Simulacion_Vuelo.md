# 7. Simulación de Vuelo — reconstrucción punto por punto

**Equipo:** PDA Rocketeers — ID 310 — Motor G80T-7
**Archivo de referencia:** `Diseño SIDERAL.ork` (OpenRocket 24.12)
**Resumen:** `Simulacion_SIDERAL.csv` actualizado al ORK vigente el 04-10-2026
**Estado:** 7.1 APROBADO. 7.2 APROBADO. 7.3 APROBADO. S7 COMPLETO.

---

## 7.1 Configuración de simulación y resultados generales — APROBADO

Simulación `Simulation 1`, integrador RK4 paso 0,05 s, atmósfera ISA, riel 1,5 m, sitio 550 m s.n.m. 6,5586° N 75,8256° W, viento 1,94 m/s turbulencia 10 %.

Cuadro 7-1: Resultados generales verificados en ORK y CSV.

| Parámetro | Valor |
|:---|:---:|
| Apogeo | 409,5 m |
| Velocidad máxima | 108,4 m/s (Mach 0,32) |
| Aceleración máxima | 109,2 m/s² |
| Tiempo a apogeo | 8,76 s |
| Duración de vuelo | 69,5 s |
| Vel. salida del riel | 18,20 m/s (65,5 km/h) |
| Vel. despliegue | 6,58 m/s |
| Vel. llegada a tierra | 6,95 m/s |
| Retardo óptimo | 7,31 s (motor 7,0 s) |

Eventos: despegue 0,023 s, salida del riel 0,181 s, fin de combustión 1,5 s, eyección 8,5 s, apogeo 8,76 s, despliegue 9,5 s, impacto 69,52 s.

### Fin de 7.1 — APROBADO

---

## 7.2 Curvas de vuelo y estabilidad — APROBADO

Cuadro 7-2: Puntos característicos verificados en simulación.

| Tiempo (s) | Altitud (m) | Vel. total (m/s) | Acel. total (m/s2) | Margen (cal) |
|:---:|:---:|:---:|:---:|:---:|
| 0,00 | 0,0 | 0,0 | 0,0 | — |
| 0,18 riel | 1,7 | 18,2 | 97,8 | 1,91 |
| 0,50 | 12,5 | 49,4 | 95,7 | 2,12 |
| 1,00 | 48,7 | 91,9 | 67,9 | 2,25 |
| 1,50 burnout | 99,8 | 105,9 | 30,5 | 2,31 |
| 3,00 | 229,7 | 70,3 | 18,6 | 2,29 |
| 5,00 | 338,1 | 40,0 | 12,6 | 2,27 |
| 8,76 apogeo | 409,5 | 2,4 | 9,2 | 1,63 |
| 9,50 despliegue | 407,2 | 6,6 | 6,9 | — |
| 69,52 suelo | 0,0 | 6,9 | 0,3 | — |

Altura contra tiempo: ascenso propulsado hasta 99,8 m a 1,5 s, costa hasta 409,5 m a 8,76 s, descenso con paracaídas a 6,6-6,9 m/s durante 60 s. Velocidad máxima 108,4 m/s. Aceleración máxima 109,2 m/s2. Tras el despliegue el margen deja de ser representativo por vuelo colgado.

Estabilidad: 1,91 cal en riel, 2,31 cal en fin de combustión, promedio propulsada 2,18 cal y ascenso 2,22 cal. Valor PDR 2,2 cal promedio con mínimo documentado. Comparativa contra R-02, R-01 y R-03 en Cuadro 7-3 de 7.3.

Fig. 7-1: Perfil lateral de vuelo OpenRocket.
Fig. 7-2: Altitud contra tiempo.
Fig. 7-3: Velocidad contra tiempo.
Fig. 7-4: Aceleración contra tiempo.

### Fin de 7.2 — APROBADO

---

## 7.3 Comparativa contra requisitos — APROBADO

Cuadro 7-3: Simulación contra requisitos.

| Parámetro | Simulado | Requisito | Estado |
|:---|:---:|:---:|:---:|
| Apogeo | 409,5 m | 400 m | +2,4 % |
| Vel. riel | 18,20 m/s | 15,28 m/s | Cumple |
| Margen promedio | 2,2 cal | 2,0 cal | Cumple |
| T/W | 11,1 | 5,0 | Cumple |
| Retardo | 7,0 s vs óptimo 7,31 s | — | Delta 0,31 s aceptado |
| Radio de recuperación | 288 m (con viento 5 m/s) | ≤ 400 m | Cumple (Circular 10-10-2026) |

El diseño preliminar presenta comportamiento acorde con objetivos y requisitos de la misión.

### Fin de 7.3 — S7 COMPLETO APROBADO
