# 📋 GUÍA DOCENTE Y PUBLICACIÓN EN CLASSROOM
## Actividad de Recuperación · Grado 9°02 · I.E. José Antonio Galán (La Estrella, Antioquia)

---

### 1. DATOS DE CONFIGURACIÓN EN GOOGLE CLASSROOM

- **Título de la tarea:** `Recuperación 9°02: Fundamentos de Programación en Python (Google Colab)`
- **Tema (Categoría):** `Recuperaciones y Nivelaciones`
- **Puntuación:** `5.0` (o `100` según configuración de la rúbrica)
- **Fecha de entrega:** `[Definida por el docente según cronograma institucional]`
- **Material adjunto:** Subir el archivo `Recuperacion_0902_Python_Colab.ipynb` desde Google Drive seleccionando la opción: **"Hacer una copia para cada alumno"** (o compartir el enlace del cuaderno como plantilla).

---

### 2. TEXTO LITERAL PARA PEGAR EN "INSTRUCCIONES" DE CLASSROOM

*(Copia y pega este texto directamente en la descripción de la tarea)*

```markdown
¡Hola, muchachos de 9°02! 👋

Esta es su actividad de recuperación para nivelar y consolidar los aprendizajes del período en Tecnología e Informática. La actividad está diseñada para que la resuelvan paso a paso de manera 100% guiada utilizando **Google Colab**.

---

### 📌 ¿EN QUÉ CONSISTE LA ACTIVIDAD?
El cuaderno de trabajo contiene:
1. **2 Ejemplos Guiados:** Explicaciones sencillas con código listo sobre mensajes en pantalla (`print`), captura de texto (`input`), cantidades numéricas (`int(input)`) y operaciones matemáticas (`*`, `+`, `-`). Solo deben leer la explicación y darle al botón de **Play (▶️)** para probarlos.
2. **3 Ejercicios Prácticos (Solo 3):** Situaciones cotidianas de nuestro municipio (la tienda del colegio, el puesto de comidas rápidas en el parque y la tienda del barrio) donde deberán aplicar lo aprendido completando las celdas de código.

---

### 🚀 PASOS PARA REALIZAR LA ACTIVIDAD:
1. Abre el cuaderno adjunto en esta tarea (se abrirá en **Google Colab**).
2. En la primera celda, escribe tu **Nombre Completo**.
3. Lee con atención los **2 ejemplos guiados** y ejecútalos dando clic en el botón de **Play (▶️)**.
4. Resuelve los **3 ejercicios prácticos** en sus respectivas celdas de código. Pruébalos ingresando datos de prueba y asegurándote de que no salgan errores en rojo.
5. **¡Ojo a esto!** No borres los ejemplos; el cuaderno se debe entregar completo con ejemplos y ejercicios resueltos.

---

### 📤 CÓMO ENTREGAR TU TRABAJO:
Puedes entregarlo de cualquiera de estas dos formas:
- **Opción A (Recomendada - Enlace compartido):**
  1. En la esquina superior derecha de Colab, haz clic en **Compartir**.
  2. En *Acceso general*, cambia a **"Cualquier persona con el enlace"** (rol: **Lector**).
  3. Haz clic en **Copiar enlace**.
  4. Aquí en Classroom, da clic en **+ Añadir o crear** ➡️ **Enlace**, pega el link y dale a **Entregar**.
- **Opción B (Descargar archivo):**
  1. En Colab, ve al menú: `Archivo` ➡️ `Descargar` ➡️ `Descargar .ipynb`.
  2. Aquí en Classroom, haz clic en **+ Añadir o crear** ➡️ **Archivo**, sube el archivo descargado y dale a **Entregar**.

---

¡Muchos éxitos! Lean con calma las pistas en el código. Si siguen el paso a paso, su nota quedará en Nivel Superior.
```

---

### 3. ESTRUCTURA Y CONTENIDO DEL CUADERNO (CELDA POR CELDA)

El cuaderno generado (`Recuperacion_0902_Python_Colab.ipynb`) cuenta con la siguiente arquitectura pedagógica:

```
[Celda 1: Markdown] Encabezado institucional, datos del estudiante y propósito del taller.
[Celda 2: Markdown] Concepto 1: print() e input() para salidas y entradas de texto.
[Celda 3: Código]   EJEMPLO 1: Saludo y bienvenida en la cafetería El Parque (La Estrella).
[Celda 4: Markdown] Concepto 2: int(input()), operaciones matemáticas (*, +, -) y variables.
[Celda 5: Código]   EJEMPLO 2: Caja registradora sencilla de empanadas (cálculo de 1 producto).
[Celda 6: Markdown] Enunciado del EJERCICIO 1: La Tienda Escolar del Galán (IEJAGA).
[Celda 7: Código]   Plantilla guiada para el EJERCICIO 1.
[Celda 8: Markdown] Enunciado del EJERCICIO 2: Comidas Rápidas en el Parque Principal.
[Celda 9: Código]   Plantilla guiada para el EJERCICIO 2.
[Celda 10: Markdown] Enunciado del EJERCICIO 3: La Tienda del Barrio y Cálculo de Vueltas (Cambio).
[Celda 11: Código]  Plantilla guiada para el EJERCICIO 3.
[Celda 12: Markdown] Instrucciones de guardado y entrega en Google Classroom.
```

---

### 4. SOLUCIONARIO TÉCNICO PARA EL DOCENTE

#### Solución Ejercicio 1 (Tienda Escolar IEJAGA):
```python
# 1. Precio fijo del jugo
precio_jugo = 3000

# 2. Mensaje de bienvenida institucional
print("--- BIENVENIDO A LA TIENDA ESCOLAR IEJAGA ---")

# 3. Pedir el nombre del estudiante
nombre_estudiante = input("Ingresa tu nombre: ")

# 4. Pedir cantidad de jugos
cantidad_jugos = int(input("¿Cuántos vasos de jugo vas a comprar?: "))

# 5. Cálculo matemático
total_pagar = cantidad_jugos * precio_jugo

# 6. Salida de resultados
print("---------------------------------------------")
print(nombre_estudiante, ", el total a pagar por tus jugos es: $", total_pagar)
```

#### Solución Ejercicio 2 (Comidas Rápidas en el Parque Principal):
```python
# 1. Precios fijos
precio_empanada = 2500
precio_gaseosa = 3500

# 2. Mensaje de bienvenida
print("=== COMIDAS RÁPIDAS EL PARQUE · LA ESTRELLA ===")

# 3. Nombre del cliente
cliente = input("¿Cuál es tu nombre?: ")

# 4. Cantidades
cant_empanadas = int(input("¿Cuántas empanadas de carne deseas?: "))
cant_gaseosas = int(input("¿Cuántas gaseosas deseas?: "))

# 5 y 6. Subtotales
total_empanadas = cant_empanadas * precio_empanada
total_gaseosas = cant_gaseosas * precio_gaseosa

# 7. Total general (Suma con +)
total_pedido = total_empanadas + total_gaseosas

# 8. Resumen ordenado
print("-----------------------------------------------")
print("Cliente:", cliente)
print("Subtotal empanadas: $", total_empanadas)
print("Subtotal gaseosas:  $", total_gaseosas)
print("TOTAL A PAGAR:      $", total_pedido)
print("¡Gracias por apoyar el comercio siderense!")
```

#### Solución Ejercicio 3 (Tienda del Barrio y Vueltas):
```python
# 1. Precios fijos
precio_galleta = 1800
precio_jugo_caja = 2200

# 2. Mensaje del minimercado
print("--- MINIMERCADO SIDERENSE · CONTROL DE CAJA ---")

# 3. Pedir cantidades
cant_galletas = int(input("¿Cuántos paquetes de galletas lleva?: "))
cant_jugos = int(input("¿Cuántos jugos en caja lleva?: "))

# 4. Cálculo del total de la compra
total_galletas = cant_galletas * precio_galleta
total_jugos = cant_jugos * precio_jugo_caja
total_compra = total_galletas + total_jugos

# 5. Mostrar total a pagar
print("Total a pagar por la compra: $", total_compra)

# 6. Preguntar con cuánto paga
pago_cliente = int(input("¿Con cuánto dinero en efectivo paga el cliente?: "))

# 7. Cálculo de las vueltas
vueltas = pago_cliente - total_compra

# 8. Recibo final
print("================ RECIBO DE PAGO ================")
print("Total de la compra:   $", total_compra)
print("Dinero recibido:      $", pago_cliente)
print("Vueltas a devolver:   $", vueltas)
print("================================================")
```

---

### 5. RÚBRICA SIMPLIFICADA (DECRETO 1290)

| Nivel de Desempeño | Rango de Nota | Criterio de Evaluación |
| :--- | :---: | :--- |
| **Superior** | `4.6 - 5.0` | Entrega el cuaderno completo con los 2 ejemplos ejecutados y los 3 ejercicios resueltos a la perfección. Convierte correctamente las entradas numéricas con `int()`, realiza las operaciones de multiplicación, suma y resta de manera exacta, y muestra resúmenes claros en consola sin errores. |
| **Alto** | `4.0 - 4.5` | Resuelve los 3 ejercicios de forma funcional. Presenta pequeños detalles de formato o presentación en los mensajes finales, pero la lógica de cálculo (precios, cantidades, totales y vueltas) es correcta y el código se ejecuta sin fallas. |
| **Básico** | `3.0 - 3.9` | Resuelve adecuadamente al menos 2 de los 3 ejercicios, o comete errores leves en la fórmula matemática final (ejemplo: olvida restar las vueltas o confunde una suma con multiplicación), pero demuestra comprensión del uso de variables, `input()` y `print()`. |
| **Bajo** | `1.0 - 2.9` | No resuelve los ejercicios propuestos, solo entrega los ejemplos sin modificarlos, o el código presenta errores graves de sintaxis no corregidos que impiden su ejecución. |
