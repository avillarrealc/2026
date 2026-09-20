# 📋 Ficha de Categoría — El Huevonauta
**Plataforma:** SateLab Academy — CCCD 2026  
**Equipo:** PDA Noctux (2026)  
**Categoría:** 1 · Principiantes  
**Extraído:** 18-09-2026 | Fuente: https://academy.satelab.org/cccd/554e1756-bf1e-476a-88c8-49806d1acc21

---

## 🎯 Misión General

> **"Construye, junto con tu equipo, un cohete capaz de llevar un huevo de gallina crudo durante todo el vuelo y lograr que regrese a tierra completamente intacto."**

---

## ✅ Resumen de Objetivos (Pestaña: Resumen)

| Objetivo | Descripción |
| :--- | :--- |
| Construir | Un cohete pequeño, liviano y estable |
| Apogeo | Superar los **100 metros** de altura |
| Recuperación | Que el paracaídas funcione correctamente |
| Carga útil | Proteger el **huevo** de gallina durante todo el vuelo |
| Altímetro | Registrar el vuelo con altímetro **Jolly Logic** o **Estes** |
| Aterrizaje | Conseguir que el cohete regrese a tierra de forma segura |

### 🎁 Lo que provee la Organización
- **Un huevo de gallina crudo**, con una masa entre 55 y **60 gramos**.
- **Un motor comercial de combustible sólido D12-5** (Estes).
- **Altímetro (Jolly Logic o Estes)** — ✅ Incluido por la organización del concurso. **No requiere compra por parte del equipo.**

---

## 🔧 Ficha Técnica y Evaluación (Pestaña: Ficha técnica y evaluación)

| Parámetro | Valor |
| :--- | :--- |
| **Longitud mínima** | 40 cm |
| **Masa máxima** | 300 g |
| **Altímetro requerido** | Jolly Logic o Estes |
| **Sistema de recuperación** | Mediante paracaídas |

### Criterios de Evaluación Visual (Barras de calificación)

**Recuperación:**
- 🟢 **Apertura óptima:** El paracaídas abre completamente y cumple correctamente su función.
- 🟡 **Apertura parcial:** El paracaídas abre de manera incompleta o enredada, pero ayuda a disminuir la velocidad de descenso.
- 🔴 **Sin apertura:** El paracaídas no abre y no cumple su función.

**Estabilidad:**
- 🟢 **Muy estable:** El cohete asciende de manera recta y controlada.
- 🟡 **Medianamente estable:** El cohete comienza a desviarse o torcerse durante el vuelo.
- 🔴 **Inestable:** El cohete se desvía considerablemente o pierde estabilidad durante el ascenso.

---

## 📜 Reglamento Completo (Pestaña: Reglamento completo)

### En qué consiste el reto
- La misión principal es salvar el **huevo**: si se rompe, el vuelo queda fuera de clasificación, sin importar la altura alcanzada.
- El **huevo** debe sobrevivir al despegue, ascenso, descenso y aterrizaje.
- Solo si el **huevo** llega intacto el equipo puede competir por la clasificación de altura.
- El cohete debe superar una altura mínima de **100 metros** para que el vuelo sea válido; a partir de ahí, entre más alto mejor el resultado — siempre que el huevo llegue sano y salvo.

### Altímetro
- **Dimensiones de referencia:** aproximadamente 15 × 20 × 55 mm.
- **Peso de referencia:** aproximadamente 10–12 g.

### Criterios de Puntuación
- El **huevo** llega intacto a tierra (requisito de clasificación).
- Altura alcanzada por encima de los **100 metros** mínimos.
- Desempeño del sistema de recuperación (**paracaídas**).
- **Estabilidad** del cohete durante el ascenso.

---

## 📁 Documentos (Pestaña: Documentos)

> ⚠️ **"Todavía no hay documentos disponibles para tu categoría."**
> La plataforma aún no ha publicado documentos oficiales descargables para la Categoría 1.

---

## 📚 Cursos de la Plataforma — Semillero PDA Noctux

| Nº | Curso | URL |
| :--- | :--- | :--- |
| 1 | Fundamentos del Modelismo Espacial | https://academy.satelab.org/courses/fundamentos-del-modelismo-espacial |
| 2 | Clasificación de Motores Cohete en Modelismo Espacial | https://academy.satelab.org/courses/clasificacion-de-motores-cohete-en-modelismo-espacial |
| 3 | Fundamentos de Estabilidad en Cohetes | https://academy.satelab.org/courses/fundamentos-de-estabilidad-en-cohetes |
| 4 | Introducción a OpenRocket | https://academy.satelab.org/courses/introduccion-a-openrocket |
| 5 | Fundamentos de los Motores en Modelismo Espacial | https://academy.satelab.org/courses/fundamentos-motores-modelismo-espacial |

---

## ⚠️ Implicaciones Técnicas para el Diseño del PDA Noctux

### Restricciones de diseño
1. **Masa máxima total: 300 g** — Incluyendo el huevo (55-60 g), el altímetro (~12 g), el tubo BT65, paracaídas, motor y todos los componentes. El presupuesto de masa es muy ajustado.
2. **Longitud mínima: 40 cm** — El BT65 debe garantizar al menos esta longitud total del cohete ensamblado.
3. **Motor D12-5:** Este motor ya lo provee la organización. Impulso total aprox. 17.6 N·s. Retardo de 5 segundos antes de la eyección del paracaídas.

### ⚡ Factores clave para ganar (en orden de prioridad)
1. **El huevo llega intacto** → Sin esto no hay clasificación (descalificación automática).
2. **Máxima altura posible** → En un motor D12-5 con masa máxima de 300g, es posible alcanzar entre 120 y 200 metros con un buen diseño aerodinámico.
3. **Paracaídas de apertura óptima** → Calcular el diámetro para bajar a menos de 11 m/s.
4. **Estabilidad "Muy estable"** → Margen de estabilidad ≥ 1.5 calibres (preferiblemente 2.0), verificado en OpenRocket.
