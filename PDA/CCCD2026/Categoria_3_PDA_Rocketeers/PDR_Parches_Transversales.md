# Parches transversales PDR — valores congelados 04-10-2026

**Fuente única:** `Diseño SIDERAL.ork` vigente + `Simulacion_SIDERAL.csv` actualizado.
Aplica a §4, §8 y texto CanSat donde corresponda. Redacción lista para pegar en LaTeX.

---

## P-01 §4.3 Características estructurales

- Diámetro: 102 mm. Longitud total: 0,90 m (0,18 + 0,24 + 0,48).
- Masa despegue: 884 g con motor. Fin de combustión: 827 g.
- Fuselaje cartón prensado. Aletas tríplex o balso con lámina de fibra de carbono (proxy ORK tríplex 2 mm). Ojiva ASA (proxy ORK PLA con masa fijada 70 g).

## P-02 §4.4 Propulsión

- Motor AeroTech G80T-7, 29 mm, retardo 7,0 s. T/W en riel 11,1. Techo 5:1 con 80 N = 1,632 kg. Margen 748 g.

## P-03 §4.2 / §7 Estabilidad

- Riel 1,91 cal, fin combustión 2,31 cal, promedio propulsada 2,18 cal, promedio ascenso 2,22 cal. Valor PDR 2,2 cal promedio con mínimo documentado.

## P-04 §8 Recuperación

- Paracaídas Ø 0,70 m, Cd 0,8, 8 líneas 1,4 m, 40 g.
- Cordón de choque 3,0 m (verificado ORK). Manta ignífuga 3 g.
- Despliegue 9,5 s a 6,58 m/s. Suelo 6,95 m/s. Vuelo 69,5 s.

## P-05 CanSat masa

- Texto 250–350 g → corregir a 250–300 g en todo el PDR. Diseño 270 g vigente.

## P-06 CSV

- `Simulacion_SIDERAL.csv` regenerado: 18,20 / 409,503 / 6,576 / 7,31 / 108,45 / 109,211 / 8,76 / 69,524 / 6,947.

---

## Pendientes GUI antes del envío (2 min)

1. Abrir `Diseño SIDERAL.ork`, ejecutar Simulation 1, guardar.
2. Exportar CSV y verificar coincide con P-06.
3. Capturar Fig. 6-2 (CG 0,475 / CP 0,670 en riel), Fig. 7-1 a 7-4.
