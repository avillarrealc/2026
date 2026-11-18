import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 2,
    "metadata": {
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🚀 TALLER DE RECUPERACIÓN · TECNOLOGÍA E INFORMÁTICA\n",
                "### Institución Educativa José Antonio Galán · La Estrella (Antioquia)\n",
                "**Grado:** 9°02 | **Tema:** Fundamentos de Programación en Python (Google Colab)\n",
                "**Estudiante:** `[Escribe aquí tu nombre completo]` | **Fecha:** Noviembre 2026\n",
                "\n",
                "> 💡 **¿En qué consiste esta recuperación?**\n",
                "> ¡Hola! Esta es tu oportunidad para ponerte al día y demostrar todo lo que has aprendido.\n",
                "> Este taller es **100% guiado**: primero vas a repasar los conceptos clave con **2 ejemplos listos** que vas a probar dándole al botón de **Play (▶️)**.\n",
                "> Luego, resolverás **solo 3 ejercicios prácticos** aplicando exactamente la misma lógica de los ejemplos.\n",
                ">\n",
                "> 📌 **Regla importante:** No borres los ejemplos guiados. Tu entrega en Classroom debe incluir **los 2 ejemplos ejecutados y tus 3 ejercicios resueltos y probados**."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "## 📘 PARTE 1: REPASO GUIADO CON EJEMPLOS\n",
                "\n",
                "### 🔹 Concepto 1: Mostrar mensajes y pedir datos con `print()` e `input()`\n",
                "- **`print(\"texto\")`**: Muestra información o mensajes en la pantalla.\n",
                "- **`input(\"pregunta\")`**: Le pide un dato al usuario por teclado y lo guarda dentro de una **variable** (como una cajita con nombre).\n",
                "- Para combinar textos fijos con variables dentro de un `print()`, los separamos con comas: `print(\"Hola\", nombre, \"bienvenido\")`.\n",
                "\n",
                "👇 **Ejecuta el siguiente código dando clic en el botón de Play (▶️) a la izquierda y escribe tu nombre cuando te lo pida:**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ======================================================\n",
                "# EJEMPLO 1: SALUDO Y BIENVENIDA EN EL PARQUE DE LA ESTRELLA\n",
                "# ======================================================\n",
                "\n",
                "# 1. Mostramos mensajes institucionales y de bienvenida\n",
                "print(\"==================================================\")\n",
                "print(\"  BIENVENIDOS A LA CAFETERÍA EL PARQUE - LA ESTRELLA\")\n",
                "print(\"==================================================\")\n",
                "\n",
                "# 2. Le preguntamos el nombre a la persona y lo guardamos en una variable\n",
                "nombre_cliente = input(\"¿Cuál es tu nombre?: \")\n",
                "\n",
                "# 3. Saludamos a la persona usando su nombre\n",
                "print(\"¡Mucho gusto en atenderte,\", nombre_cliente, \"! Pasa adelante y mira la carta.\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 🔹 Concepto 2: Números, conversión con `int()` y operaciones matemáticas\n",
                "- **¡Ojo a esto!** En Python, todo lo que entra por `input()` llega en formato de texto.\n",
                "- Si vas a hacer operaciones matemáticas (calcular precios, cantidades o vueltas), debes usar `int(input(...))` para convertirlo a **número entero**.\n",
                "- **Operaciones matemáticas básicas en Python:**\n",
                "  - Multiplicación: `*` (ejemplo: `total = precio * cantidad`)\n",
                "  - Suma: `+` (ejemplo: `total = total_empanadas + total_gaseosas`)\n",
                "  - Resta: `-` (ejemplo: `vueltas = dinero_entregado - total_pagar`)\n",
                "\n",
                "👇 **Ejecuta este segundo ejemplo para ver cómo calcula la cuenta de una compra automáticamente:**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ======================================================\n",
                "# EJEMPLO 2: CAJA REGISTRADORA SENCILLA (UN PRODUCTO)\n",
                "# ======================================================\n",
                "\n",
                "# 1. Fijamos el precio de una empanada (variable numérica)\n",
                "precio_empanada = 2500\n",
                "\n",
                "print(\"--- PUESTO DE ANTOJITOS SIDERENSES ---\")\n",
                "print(\"Precio por unidad de empanada: $\", precio_empanada)\n",
                "\n",
                "# 2. Pedimos la cantidad que va a llevar el cliente (usamos int para que sea número)\n",
                "cantidad = int(input(\"¿Cuántas empanadas vas a llevar?: \"))\n",
                "\n",
                "# 3. Hacemos el cálculo matemático (multiplicación)\n",
                "total_pagar = cantidad * precio_empanada\n",
                "\n",
                "# 4. Mostramos el resultado claro en la pantalla\n",
                "print(\"--------------------------------------------------\")\n",
                "print(\"Cantidad pedida:\", cantidad, \"empanadas\")\n",
                "print(\"Total a pagar en caja: $\", total_pagar)\n",
                "print(\"¡Gracias por tu compra en La Estrella!\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "## 🛠️ PARTE 2: EJERCICIOS PARA EL ESTUDIANTE (SOLO 3)\n",
                "> Lee atentamente cada situación y escribe tu código en la celda correspondiente. Recuerda darle al botón Play (▶️) para verificar que funcione sin errores.\n",
                "\n",
                "---\n",
                "### 📝 EJERCICIO 1: La Tienda Escolar del Galán (IEJAGA)\n",
                "**Situación:**\n",
                "En la cafetería de nuestro colegio, el vaso de jugo natural de mango cuesta **$3.000**.\n",
                "Debes crear un programa en Python que realice los siguientes pasos:\n",
                "1. Muestre un mensaje de bienvenida: `\"--- BIENVENIDO A LA TIENDA ESCOLAR IEJAGA ---\"`.\n",
                "2. Le pregunte al estudiante su **nombre** (usando `input`).\n",
                "3. Le pregunte **cuántos vasos de jugo** va a comprar (usando `int(input(...))` para que sea número entero).\n",
                "4. Calcule el valor total multiplicando la cantidad pedida por el precio ($3.000).\n",
                "5. Muestre en consola un mensaje final con el nombre del estudiante y el total a pagar.\n",
                "\n",
                "*Ejemplo de salida esperada:* Si Dylan pide 3 jugos, debe mostrar: `Dylan, el total a pagar por tus jugos es: $ 9000`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ======================================================\n",
                "# EJERCICIO 1: TIENDA ESCOLAR DEL GALÁN\n",
                "# Estudiante: [Escribe aquí tu nombre completo]\n",
                "# ======================================================\n",
                "\n",
                "# 1. Precio fijo del jugo (No modificar)\n",
                "precio_jugo = 3000\n",
                "\n",
                "# 2. Escribe aquí el mensaje de bienvenida institucional con print()\n",
                "\n",
                "\n",
                "# 3. Pide el nombre del estudiante con input()\n",
                "\n",
                "\n",
                "# 4. Pide cuántos vasos de jugo va a llevar usando int(input(...))\n",
                "\n",
                "\n",
                "# 5. Calcula el total a pagar (multiplica cantidad por precio_jugo)\n",
                "\n",
                "\n",
                "# 6. Muestra el resumen final con el nombre del estudiante y el total a pagar\n",
                "\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "### 📝 EJERCICIO 2: Puesto de Comidas Rápidas en el Parque Principal\n",
                "**Situación:**\n",
                "En el Parque Principal de La Estrella tienes un puesto de comidas rápidas con dos productos:\n",
                "- Empanada de carne: **$2.500** cada una.\n",
                "- Gaseosa personal: **$3.500** cada una.\n",
                "\n",
                "Debes crear un programa en Python que realice los siguientes pasos:\n",
                "1. Muestre el saludo del negocio: `\"=== COMIDAS RÁPIDAS EL PARQUE · LA ESTRELLA ===\"`.\n",
                "2. Pida el nombre del cliente con `input()`.\n",
                "3. Pida cuántas empanadas desea llevar con `int(input(...))`.\n",
                "4. Pida cuántas gaseosas desea llevar con `int(input(...))`.\n",
                "5. Calcule el subtotal de empanadas (`empanadas * 2500`).\n",
                "6. Calcule el subtotal de gaseosas (`gaseosas * 3500`).\n",
                "7. Calcule el total general del pedido **sumando (+) ambos subtotales**. *(¡Ojo! Es una suma con `+`, nunca multiplicación)*.\n",
                "8. Muestre un resumen ordenado en pantalla con el nombre del cliente, las cantidades pedidas y el total final a pagar.\n",
                "\n",
                "*Ejemplo de salida esperada:* Si Sofía pide 2 empanadas y 1 gaseosa, el cálculo es `(2*2500) + (1*3500) = 5000 + 3500 = $8500`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ======================================================\n",
                "# EJERCICIO 2: COMIDAS RÁPIDAS EN EL PARQUE PRINCIPAL\n",
                "# Estudiante: [Escribe aquí tu nombre completo]\n",
                "# ======================================================\n",
                "\n",
                "# 1. Precios fijos de los productos (No modificar)\n",
                "precio_empanada = 2500\n",
                "precio_gaseosa = 3500\n",
                "\n",
                "# 2. Mensaje de bienvenida al negocio con print()\n",
                "\n",
                "\n",
                "# 3. Pedir el nombre del cliente con input()\n",
                "\n",
                "\n",
                "# 4. Pedir la cantidad de empanadas con int(input(...))\n",
                "\n",
                "\n",
                "# 5. Pedir la cantidad de gaseosas con int(input(...))\n",
                "\n",
                "\n",
                "# 6. Calcular los dos subtotales (empanadas y gaseosas)\n",
                "\n",
                "\n",
                "# 7. Calcular el total del pedido sumando (+) los dos subtotales\n",
                "\n",
                "\n",
                "# 8. Mostrar el resumen completo del pedido con prints ordenados\n",
                "\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "### 📝 EJERCICIO 3: La Tienda del Barrio y el Cálculo de las Vueltas (Cambio)\n",
                "**Situación:**\n",
                "En un minimercado del barrio San Agustín o La Ferrería en La Estrella, un cliente compra dos productos para las onces:\n",
                "- Paquete de galletas: **$1.800** cada uno.\n",
                "- Jugo de caja: **$2.200** cada uno.\n",
                "\n",
                "El cliente paga con un billete de denominación mayor (por ejemplo, $10.000 o $20.000) y el cajero necesita que el sistema calcule exactamente cuánto dinero devolverle de cambio (\"las vueltas\").\n",
                "\n",
                "Debes crear un programa en Python que realice los siguientes pasos:\n",
                "1. Muestre el saludo: `\"--- MINIMERCADO SIDERENSE · CONTROL DE CAJA ---\"`.\n",
                "2. Pida la cantidad de galletas que va a llevar con `int(input(...))`.\n",
                "3. Pida la cantidad de jugos en caja que va a llevar con `int(input(...))`.\n",
                "4. Calcule el valor total de la compra sumando galletas y jugos.\n",
                "5. Muestre en pantalla el total que debe pagar el cliente.\n",
                "6. Pregunte con cuánto dinero paga el cliente usando: `pago = int(input(\"¿Con cuánto dinero paga el cliente?: \"))`.\n",
                "7. Calcule las vueltas con una resta: `vueltas = pago - total_compra`.\n",
                "8. Muestre en pantalla un recibo final claro con: Total a pagar, Dinero entregado y Vueltas a devolver.\n",
                "\n",
                "*Ejemplo de salida esperada:* Si lleva 2 galletas ($3.600) y 1 jugo ($2.200), el total es $5.800. Si paga con un billete de $10.000, el sistema debe imprimir: `Vueltas a devolver al cliente: $ 4200`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# ======================================================\n",
                "# EJERCICIO 3: TIENDA DEL BARRIO Y CÁLCULO DE VUELTAS\n",
                "# Estudiante: [Escribe aquí tu nombre completo]\n",
                "# ======================================================\n",
                "\n",
                "# 1. Precios fijos de los productos (No modificar)\n",
                "precio_galleta = 1800\n",
                "precio_jugo_caja = 2200\n",
                "\n",
                "# 2. Mensaje de bienvenida del minimercado con print()\n",
                "\n",
                "\n",
                "# 3. Pedir cantidad de galletas (int) y cantidad de jugos (int)\n",
                "\n",
                "\n",
                "# 4. Calcular el subtotal de galletas, subtotal de jugos y total de la compra\n",
                "\n",
                "\n",
                "# 5. Mostrar en pantalla el total a pagar\n",
                "\n",
                "\n",
                "# 6. Preguntar con cuánto dinero paga el cliente usando int(input(...))\n",
                "\n",
                "\n",
                "# 7. Calcular las vueltas restando: dinero_pago - total_compra\n",
                "\n",
                "\n",
                "# 8. Mostrar el recibo final completo (Total, Pago y Vueltas)\n",
                "\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "## 📤 CÓMO ENTREGAR TU CUADERNO EN GOOGLE CLASSROOM\n",
                "\n",
                "Sigue estos pasos sencillos para que tu entrega quede registrada correctamente:\n",
                "\n",
                "1. **Verificación técnica:** Asegúrate de haber ejecutado (botón Play ▶️) los **2 ejemplos guiados** y tus **3 ejercicios**. Comprueba que no aparezca ningún error en rojo.\n",
                "2. **Renombrar el cuaderno:** En la esquina superior izquierda de Google Colab, cambia el nombre del archivo por: `Recuperacion_0902_TuNombre.ipynb`.\n",
                "3. **Elige una de las dos formas de entrega:**\n",
                "   - **Opción A (Recomendada - Compartir enlace):**\n",
                "     - Clic en el botón azul **Compartir** (arriba a la derecha).\n",
                "     - En \"Acceso general\", cambia de \"Restringido\" a **\"Cualquier persona con el enlace\"** (rol: **Lector**).\n",
                "     - Clic en **Copiar enlace**.\n",
                "     - Ve a Google Classroom, entra a la tarea de Recuperación, haz clic en **+ Añadir o crear** -> **Enlace**, pega el enlace copiado y pulsa **Entregar**.\n",
                "   - **Opción B (Descargar y adjuntar archivo .ipynb):**\n",
                "     - En Colab, ve al menú superior: `Archivo` -> `Descargar` -> `Descargar .ipynb`.\n",
                "     - En Google Classroom, en la tarea, haz clic en **+ Añadir o crear** -> **Archivo**, selecciona el archivo descargado y pulsa **Entregar**.\n",
                "\n",
                "¡Muchos éxitos! Si seguiste la guía paso a paso, vas a recuperar tu nota sin ningún problema."
            ]
        }
    ]
}

with open(r"Grado 9\Recuperación 0902 - Fundamentos de Python\Recuperacion_0902_Python_Colab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("¡Notebook generado exitosamente!")
