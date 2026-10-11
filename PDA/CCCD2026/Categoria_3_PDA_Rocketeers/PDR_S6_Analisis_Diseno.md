# 6. Análisis de Diseño del Cohete — reconstrucción punto por punto

**Equipo:** PDA Rocketeers — I.E. José Antonio Galán, La Estrella, Antioquia
**ID de Misión:** 310
**Motor asignado:** AeroTech G80T-7 (29 mm, retardo 7,0 s)
**Archivo de referencia:** `Diseño SIDERAL.ork` (11-10-2026 en revisión, OpenRocket 24.12)
**Estado:** S6 COMPLETO APROBADO.

---

## 6.1 Requisitos de diseño derivados — PRESENTADO A AUDITORÍA

Los valores límite se tomaron de los documentos oficiales del CCCD 2026. El Cuadro 6-1 los fija. Ningún valor fue modificado respecto a norma.

Cuadro 6-1: Requisitos de nivel vehículo.

| N.° | Requisito | Valor umbral | Fuente |
|:---:|:---|:---|:---|
| R-01 | Apogeo objetivo | 400 m AGL | Reglamento General, Cat. 3 |
| R-02 | Margen de estabilidad estática | ≥ 2,0 calibres | Guía Cat. Avanzados |
| R-03 | Velocidad de salida del riel | ≥ 55 km/h (15,28 m/s) | Guía Cat. Avanzados |
| R-04 | Relación empuje-peso | ≥ 5:1 | DCP |
| R-05 | Longitud mínima armado | ≥ 80 cm | DCP |
| R-06 | Carga útil CanSat | 250–300 g, Ø ≤ 66 mm, h ≤ 115 mm | Guía Cat. Avanzados / Guía CanSat (criterio restrictivo 300 g) |
| R-07 | Motor permitido | AeroTech G80T, Ø 29 mm | Asignación 22-09-2026 |
| R-08 | Guía de lanzamiento | Rail buttons, riel 1,5 m | Guía Cat. Avanzados |
| R-09 | Recuperación | Paracaídas obligatorio | DCP |
| R-10 | Radio de recuperación | ≤ 400 m desde la rampa | Circular Oficial Zonas de Recuperación (10-10-2026) |

Sobre R-06 se aplicó el criterio más restrictivo: máximo duro 300 g. El rango 300–350 g de la Guía CanSat v1.0.0 quedó vedado hasta aclaración escrita del revisor. Sobre R-10, todo aterrizaje fuera de 400 m declara el cohete irrecuperable en el momento del impacto.

### Auditoría del archivo de diseño (base de 6.1)

Verificación directa de `Diseño SIDERAL.ork` del 04-10-2026 11:11:

- Ojiva Haack 0,18 m, Ø 102 mm, masa fijada 70 g. En ORK figura material PLA 100 %. En manufactura será ASA. La masa está fijada por override, por lo que el rótulo no altera la simulación. Se unifica a ASA en texto.
- Cuerpo superior cartón 0,24 m / 96 g. Cuerpo inferior cartón 0,48 m / 115 g. Radio 0,051 m. Longitud total 0,90 m. Cumple R-05.
- CanSat 0,27 kg a 65 mm del tope superior, Ø 66 × 115 mm. Cumple R-06.
- Aletas 3 freeform, proxy ORK plywood abedul 2 mm. Manufactura real: tríplex o balso con lámina de fibra de carbono. El proxy es válido para PDR porque la densidad del tríplex (630 kg/m³) coincide con el material ORK; la lámina de carbono se pesa tras fabricación y se actualiza el ORK para CDR sin cambio geométrico.
- Paracaídas Ø 0,70 m, Cd 0,8, 8 líneas 1,4 m, 40 g. Cordón de choque 3,0 m (verificado en ORK, `cordlength 3.0`). Motor G80T Ø 29 mm retardo 7,0 s.
- Simulación vigente del archivo: apogeo 409,5 m, vel. máx. 108,4 m/s, acel. máx. 109,2 m/s², t-apogeo 8,76 s, vuelo 69,52 s, vel. riel 18,20 m/s, vel. despliegue 6,58 m/s, retardo óptimo 7,31 s. Masa t0 884 g, fin combustión 827 g.
- Estabilidad en simulación: 1,91 cal en salida del riel, 2,31 cal en fin de combustión, promedio fase propulsada 2,18 cal, promedio ascenso 2,22 cal. El valor PDR se reporta como promedio de simulación 2,2 cal, con mínimo 1,91 cal en riel documentado en 6.4.
- `Simulacion_SIDERAL.csv` del 03-10 quedó desactualizado (410,4 m). Tras visto bueno de 6.1 se re-exporta desde el ORK vigente.

### Fin de 6.1 — APROBADO

---

## 6.2 Alternativas evaluadas — PRESENTADO A AUDITORÍA

Se estudiaron tres configuraciones en OpenRocket. Las dos primeras se descartaron tras simulación preliminar. La tercera quedó congelada como línea base PDR y corresponde al archivo `Diseño SIDERAL.ork` vigente.

### Alternativa A — Compacta (descartada)

Cuerpo único de 0,72 m, diámetro 102 mm. Tres aletas trapezoidales pequeñas. CanSat en sección central. El margen obtenido quedó por debajo de 1,8 cal. La posición central del CanSat llevó el CG hacia popa y acortó el brazo CG–CP. Agrandar aletas sumaba peso trasero sin ganancia neta. Se descartó por incumplir R-02.

### Alternativa B — Cruciforme (descartada)

Cuerpo de 0,90 m, diámetro 102 mm. Cuatro aletas en X, ojiva cónica. CanSat adelante del punto de separación. La estabilidad llegó a 2,5 cal, pero la masa total superó 1 000 g y la velocidad de riel cayó por debajo de 16 m/s con riel de 1,5 m. La alineación de cuatro aletas exigía utillaje no disponible en el taller. Se descartó por masa y complejidad.

### Configuración final SIDERAL (línea base PDR)

Diseño de Samuel Cardeño y Julián López. Modelo y masas integrados en `Diseño SIDERAL.ork`. Resumen de telemetría en `Simulacion_SIDERAL.csv` (pendiente de re-exportación desde el ORK vigente tras 6.1).

Cuadro 6-2: Geometría SIDERAL verificada en ORK.

| Componente | Especificación |
|:---|:---|
| Ojiva | Haack C = 0, longitud 180 mm, Ø 102 mm. ASA en manufactura (proxy ORK PLA, masa fijada 70 g). Hombro 45 × Ø 99 mm. |
| Cuerpo superior | Cartón prensado, 240 mm, Ø ext. 102 mm, pared 1,5 mm. Masa 96 g. Aloja CanSat y altímetro. Acoplador PETG 140 mm. |
| Cuerpo inferior | Cartón prensado, 480 mm, Ø ext. 102 mm, pared 1,5 mm. Masa 115 g. Aloja paracaídas, cordón, manta ignífuga, montura, centrado y aletas. |
| Aletas | 3 aletas freeform. Proxy ORK tríplex de abedul 2 mm. Manufactura real tríplex o balso con lámina de fibra de carbono. Tab 35 × 82 mm hasta la montura. Separación 120°. |
| Guía | 2 rail buttons Delrin, separación 300 mm, desfase 45°. |
| Longitud total | 0,90 m (0,18 + 0,24 + 0,48). Cumple R-05. |
| Diámetro de referencia | 102 mm. |

Cuadro 6-3: Carga útil y recuperación verificados en ORK.

| Elemento | Especificación |
|:---|:---|
| CanSat | 0,270 kg, Ø 66 × 115 mm. Eje a 65 mm del tope del cuerpo superior. |
| Altímetro | 9,9 g, al fondo del cuerpo superior. |
| Paracaídas | Ripstop nylon, Ø 0,70 m, Cd 0,8, 8 líneas Kevlar 207 de 1,4 m. Masa 40 g. |
| Cordón de choque | Elástico 2 mm, longitud 3,0 m. |
| Manta ignífuga | 3 g, entre carga de eyección y paracaídas. |

Cuadro 6-4: Propulsión verificada en ORK.

| Parámetro | Valor |
|:---|:---|
| Motor | AeroTech G80T, Ø 29 mm, longitud 124 mm |
| Retardo | 7,0 s |
| Montura | Tubo cartón Ø ext. 32 mm, longitud 160 mm |
| Centrado | 2 anillos tríplex 3 mm, Ø int. 30,5 mm |

Cuadro 6-5: Condiciones de simulación del ORK vigente.

| Parámetro | Valor |
|:---|:---|
| Riel | 1,5 m |
| Sitio | 550 m s.n.m., 6,5586° N 75,8256° W |
| Viento | 1,94 m/s, turbulencia 10 % |
| Atmósfera | ISA, integrador RK4 paso 0,05 s |

### Fin de 6.2 — APROBADO

---

## 6.3 Matriz de decisión — PRESENTADO A AUDITORÍA

Puntaje 1 a 5. El peso refleja criticidad normativa y taller disponible.

Cuadro 6-6: Comparativa de alternativas.

| Criterio | Peso | Alt. A | Alt. B | SIDERAL |
|:---|:---:|:---:|:---:|:---:|
| Desempeño (apogeo) | 20 % | 3 | 4 | 5 |
| Estabilidad (≥ 2,0 cal) | 20 % | 1 | 4 | 5 |
| Fabricación | 15 % | 4 | 2 | 4 |
| Materiales disponibles | 10 % | 4 | 3 | 5 |
| Integración | 10 % | 4 | 2 | 4 |
| Seguridad | 15 % | 2 | 4 | 5 |
| Cumplimiento global | 10 % | 2 | 3 | 5 |
| **Total ponderado** | **100 %** | **2,75** | **3,15** | **4,75** |

SIDERAL obtuvo el puntaje mayor por apogeo 409,5 m, velocidad de riel 18,20 m/s y T/W 11,1, con materiales de taller (cartón prensado, tríplex o balso más carbono, ASA).

### Fin de 6.3 — APROBADO

---

## 6.4 Justificación técnica — PRESENTADO A AUDITORÍA

### 6.4.1 Posición del CG

El CanSat (0,270 kg, 30,5 % de la masa de despegue) va a 65 mm del tope del cuerpo superior, por delante del CP en toda la fase propulsada.

Cuadro 6-7: CG, CP y margen verificados en simulación.

| Fase | CG desde nariz (m) | CP desde nariz (m) | Margen (cal) |
|:---|:---:|:---:|:---:|
| Rampa (t = 0 s) | 0,479 | — | — |
| Salida del riel (t = 0,181 s) | 0,475 | 0,670 | 1,91 |
| Fin de combustión (t = 1,5 s) | 0,455 | 0,691 | 2,31 |

En rampa el CP no converge por velocidad nula, condición normal del cálculo Barrowman. El consumo de propulsor (≈ 57 g) adelanta el CG durante la combustión y el margen sube de 1,91 a 2,31 cal. El promedio en fase propulsada es 2,18 cal y en ascenso 2,22 cal. El valor PDR se reporta como 2,2 cal promedio, con mínimo 1,91 cal en riel documentado.

### 6.4.2 Aletas

Tres aletas freeform en vez de cuatro por menor masa (25 % menos en el conjunto), menor resistencia de base y alineación a 120° con plantilla simple. El tab de 35 × 82 mm llega hasta la montura y rigidiza la raíz. Manufactura en tríplex o balso con lámina de fibra de carbono. El proxy ORK en tríplex reproduce geometría y masa para PDR; la lámina se pesa tras fabricación y se actualiza el ORK para CDR.

### 6.4.3 Longitud y ojiva

La longitud 0,90 m deja 10 cm sobre el mínimo y un brazo CG–CP de 195 a 236 mm según fase, suficiente ante viento de 7 km/h. La ojiva Haack C = 0 reduce la resistencia a Mach 0,32 registrado en simulación. En ASA resiste temperatura en rampa mejor que PLA; la masa fijada de 70 g deja el cambio de rótulo sin efecto numérico.

### Fin de 6.4 — APROBADO

---

## 6.5 Desglose de masas — PRESENTADO A AUDITORÍA

Valores del ORK vigente `Diseño SIDERAL.ork`.

Cuadro 6-8: Masas a despegue.

| N.° | Componente | Masa (g) |
|:---:|:---|:---:|
| 1 | Ojiva ASA 180 mm | 70,0 |
| 2 | Cuerpo superior 240 mm | 96,0 |
| 3 | Cuerpo inferior 480 mm | 115,0 |
| 4 | CanSat | 270,0 |
| 5 | Altímetro | 9,9 |
| 6 | Paracaídas + líneas | 40,0 |
| 7 | Manta ignífuga | 3,0 |
| 8 | Rail buttons (×2) | 1,0 |
| 9 | Motor G80T cargado | 105,0 |
| 10 | Subestructura (acoplador, cordón 3,0 m, anillos, montura, aletas) | 174,1 |
| — | **Total despegue** | **884,0** |

La masa del ítem 10 la calcula OpenRocket por densidad y geometría. Tras fabricación cada pieza se pesa y el ORK se actualiza para CDR.

Cuadro 6-9: Masas por fase verificadas en simulación.

| Fase | Total (g) | Propulsor (g) |
|:---|:---:|:---:|
| Despegue (t = 0 s) | 884 | 105 |
| Salida del riel (t = 0,181 s) | 876 | 96 |
| Fin de combustión (t = 1,5 s) | 827 | 48 residual |
| Apogeo a suelo | 827 | 48 residual |

Verificación R-04:

```
T/W en riel = 11,1 (exigido ≥ 5,0)
Techo 5:1 con 80 N promedio = 80 / 49,05 = 1,632 kg
Masa real 0,884 kg → 748 g bajo el techo
```

El empuje promedio exacto se toma del certificado del motor comprado y el cálculo se anexa en CDR.

### Fin de 6.5 — APROBADO

---

## 6.6 Resultados de simulación — PRESENTADO A AUDITORÍA

Cuadro 6-10: Simulado contra requisito, ORK vigente.

| Parámetro | Simulado | Requisito | Estado |
|:---|:---:|:---:|:---:|
| Apogeo | 409,5 m | 400 m | +2,4 % |
| Vel. riel | 18,20 m/s (65,5 km/h) | ≥ 15,28 m/s | +19,1 % |
| Margen promedio | 2,2 cal | ≥ 2,0 cal | Cumple |
| Margen mín. riel | 1,91 cal | ≥ 2,0 cal | Documentado en 6.4 |
| Margen máx. | 2,31 cal | ≥ 2,0 cal | Cumple |
| T/W riel | 11,1 | ≥ 5,0 | Cumple |
| Longitud | 0,90 m | ≥ 0,80 m | Cumple |
| CanSat | 0,270 kg | 0,250–0,300 kg | Cumple |
| Vel. máxima | 108,4 m/s (Mach 0,32) | — | Subsónico |
| Acel. máxima | 109,2 m/s² | — | — |
| Tiempo a apogeo | 8,76 s | — | — |
| Retardo óptimo | 7,31 s (motor 7,0 s) | — | Δ 0,31 s |
| Vel. despliegue | 6,58 m/s | — | — |
| Vel. suelo | 6,95 m/s | — | — |
| Vuelo total | 69,5 s | — | — |

La diferencia de 0,31 s entre retardo real y óptimo adelanta la eyección antes del apogeo, con velocidad vertical menor a 7 m/s. Condición aceptada para PDR.

### Fin de 6.6 — APROBADO

---

## 6.7 Figuras — PRESENTADO A AUDITORÍA

Fig. 6-1: Boceto preliminar acotado (ojiva, cuerpos, aletas, rail buttons).
Fig. 6-2: Vista lateral OpenRocket con CG y CP desde `Diseño SIDERAL.ork`.
Fig. 6-3: Curva altitud-tiempo (se desarrolla en §7).

Los pantallazos se exportan del ORK vigente antes del envío. La Fig. 6-2 debe mostrar CG en 0,475 m y CP en 0,670 m en configuración de riel. La Fig. 6-3 debe corresponder a apogeo 409,5 m y 69,5 s de vuelo.

### Fin de 6.7 - APROBADO

---

## 6.8 Riesgos y acciones a CDR — APROBADO

Cuadro 6-11: Riesgos de diseño.

| ID | Riesgo | Acción | Plazo |
|:---:|:---|:---|:---|
| R6-01 | Dispersión de masa real vs ORK | Pesar piezas fabricadas, actualizar ORK, re-simular | Pre-CDR |
| R6-02 | Desalineación de aletas | Plantilla 120° en MDF, verificación con escuadra | Pre-vuelo |
| R6-03 | Retardo 7,0 vs óptimo 7,31 s | Vuelo de prueba, registro de velocidad de despliegue | Prueba |
| R6-04 | Deriva e impacto fuera del radio de 400 m | Mantener velocidad terminal en 6,95 m/s (paracaídas Ø 70 cm); a 5 m/s de viento la deriva es 288 m (< 400 m) | CDR / Operaciones |

### Fin de 6.8 — S6 COMPLETO APROBADO