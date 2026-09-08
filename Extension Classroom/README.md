# Extensión: paso de notas y devoluciones a Classroom

Rellena notas y comentarios privados en la ventana de calificación de Google
Classroom con los datos del calificador. Sirve para las tareas viejas
(creadas a mano, donde la API de Google bloquea la escritura) y para las
devoluciones, que no tienen endpoint en la API.

## Por qué existe

* La API de Classroom solo deja guardar notas en tareas creadas por la misma
  app, y no tiene endpoint de comentarios privados. Está verificado en la
  documentación oficial de Google.
* La extensión no usa la API: actúa en su navegador, sobre la página de
  Classroom, igual que si usted digitara. Por eso sí puede llenar notas y
  comentarios en cualquier tarea.
* La extensión nunca pulsa Guardar ni Devolver. Usted revisa y guarda.

## Instalación (Chrome o Edge, en su PC)

1. Abra `chrome://extensions` (o `edge://extensions`).
2. Active el **Modo de desarrollador**.
3. Pulse **Cargar descomprimida** y seleccione esta carpeta `Extension Classroom`.
4. Fije la extensión en la barra con el icono de rompecabezas.

## Uso

### Notas en la vista de lista (rápido, todos a la vez)

1. En el calificador, califique y pulse **Copiar para extensión**.
2. En Classroom, abra la tarea y entre a **Trabajo del estudiante**
   (la lista con la columna de notas `___/5`).
3. Abra la extensión, pegue el JSON y pulse **Detectar campos** para verificar
   (debe decir celdas por abrir).
4. Pulse **Rellenar notas y comentarios**. La extensión abre cada celda,
   escribe la nota y confirma, una por una. No cierre la pestaña.
5. Revise cada fila en pantalla y pulse **Guardar** o **Devolver** en Classroom.

### Sin casilla en lista (no entregaron): automático en vista individual

Las filas sin entrega no tienen casilla de nota. Al pulsar **Rellenar**,
esos estudiantes se abren solos uno por uno en su vista individual,
se califican ahí y se vuelve a la lista, sin que usted toque nada.
No cierre la pestaña hasta el resumen final. Si algo se atraviesa,
use el botón **Detener proceso automático** de la extensión.

### Comentarios (uno por uno, porque Classroom no los muestra en la lista)

1. Con el mismo JSON pegado, abra un estudiante (clic en su nombre).
2. Pulse **Rellenar**: se llenan su nota y su comentario privado.
3. Revise, siga con el siguiente estudiante y al final pulse
   **Guardar** o **Devolver**.

## Si algo no se rellena

Google cambia su página con frecuencia. Abra `content.js` y ajuste la
sección `SELECTORES` con las etiquetas actuales (use clic derecho,
Inspeccionar, sobre la casilla). Los reportes de la extensión le dicen
qué quedó pendiente.
