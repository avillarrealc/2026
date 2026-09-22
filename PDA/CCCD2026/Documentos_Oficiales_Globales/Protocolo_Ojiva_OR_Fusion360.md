# Protocolo Técnico: Modelado de Ojiva desde OpenRocket a Fusion 360

**Proyecto:** CCCD 2026 - Categoría 3 (Avanzados)
**Aprobación:** Ingeniería Aeroespacial - Perfil de Mínimo Arrastre (Serie Haack / Von Kármán)

Este documento detalla el procedimiento validado paso a paso para extraer la geometría de una ojiva calculada en OpenRocket y convertirla en un modelo sólido 3D de alta precisión y calidad de manufactura en Autodesk Fusion 360.

---

## Fase 1: Extracción Directa desde OpenRocket

1. Abra su archivo de simulación (`.ork`) en OpenRocket.
2. En el árbol de componentes (esquina superior izquierda), haga clic derecho exclusivamente sobre el componente **Ojiva**.
3. Seleccione la opción **Exportar como OBJ (.obj)**.
4. En la ventana de configuración de exportación, marque obligatoriamente las siguientes casillas:
   * *Optimizar para impresión 3D*
   * *Eliminar desplazamiento del origen*
5. Despliegue el menú de *Opciones avanzadas* y **cambie el valor de Escala a 1000**. Este paso es crítico para que la conversión de metros a milímetros sea exacta.
6. Guarde el archivo `.obj` en su directorio de trabajo.

## Fase 2: Importación y Conversión en Fusion 360

1. Inicie un nuevo diseño en Autodesk Fusion 360 (Diseño de Piezas / Units: mm).
2. En la cinta superior, vaya a `Insertar` (Insert) -> `Insertar Malla` (Insert Mesh) y seleccione el archivo `.obj` exportado.
3. Cambie al espacio de trabajo **Malla** (Mesh) en la barra superior.
4. Vaya al menú `Modificar` (Modify) y seleccione **Convertir Malla** (Convert Mesh).
5. Seleccione el cuerpo de la ojiva en la pantalla.
6. En la ventana de configuración, asegúrese de que el método sea **Facetado** (Faceted) y la operación sea **Paramétrico**. Haga clic en Aceptar.

## Fase 3: Extracción del Perfil Bidimensional (Intersección)

1. Regrese al espacio de trabajo **Sólido** (Solid).
2. Seleccione `Crear Boceto` (Create Sketch) y elija uno de los planos verticales de origen (XY o XZ) que corte la ojiva exactamente por el centro longitudinal.
3. En el menú superior, vaya a `Crear` -> `Proyectar/Incluir` -> **`Intersecar`** (Intersect).
4. Seleccione el cuerpo sólido 3D de la ojiva y haga clic en Aceptar. Aparecerán unas líneas moradas que representan el contorno 2D exacto del modelo.
5. Vaya al árbol de operaciones (izquierda), expanda la carpeta "Cuerpos" (Bodies) y oculte el cuerpo 3D haciendo clic en el icono del ojo. Ahora solo trabajará con el boceto 2D.

## Fase 4: Trazado Analítico (Suavizado de Malla)

*Nota: La línea morada extraída es una polilínea facetada compuesta por cientos de segmentos rectos. Para evitar que la ojiva se imprima en "capas" o "escalones", debe trazarse una curva analítica perfecta.*

1. Dibuje una línea recta vertical desde el centro de la base hasta la punta para establecer el **eje central**. Presione `X` para convertirla en línea de construcción.
2. Elimine o convierta en línea de construcción (tecla `X`) el contorno de uno de los lados y el contorno interior para trabajar únicamente con **una mitad de la línea exterior**.
3. Seleccione `Crear` -> `Spline` -> **`Spline de puntos de ajuste`** (Fit Point Spline).
4. Haga un primer clic en la base de la línea morada exterior y comience a trazar la curva haciendo clics espaciados (aprox. cada 1 a 2 cm) a lo largo del contorno exterior hasta llegar a la punta superior. Termine con `Enter`.

## Fase 5: Estructura, Paredes y Macizado

1. **Grosor Uniforme:** Seleccione el nuevo Spline suave que acaba de dibujar. Presione la tecla `O` (Desfase / Offset) y aplique un valor de **-1.5 mm** (hacia el interior). Esto generará la pared estructural perfectamente paralela.
2. **Macizado de Punta:** Desplácese a la punta superior. A una distancia de 15 mm a 20 mm hacia abajo desde el vértice, trace una línea horizontal conectando la línea de desfase interior con el eje central. Use la tecla `T` (Recortar / Trim) para eliminar el pico interior sobrante. Esto garantiza una punta sólida 100% rellena para impresión 3D (resistencia térmica y de impacto).
3. **Refuerzo del Hombro:** Desplácese a la unión entre la ojiva y el acople (shoulder). Trace una línea recta o diagonal corta para "puentear" y rellenar el vértice agudo (concentrador de esfuerzos) en la cara interior.
4. **Cierre de Perfil:** Asegúrese de cerrar el espacio inferior de la base con una línea horizontal. El sistema sombreará todo el perfil (pared de 1.5 mm + bloque de punta) en un tono azul claro continuo.

## Fase 6: Solidificación (Revolución)

1. Haga clic en **Terminar boceto** (Finish Sketch).
2. Seleccione la herramienta **`Revolución`** (Revolve).
3. Seleccione el perfil topológico (sombreado azul).
4. Seleccione la línea recta de construcción vertical como **Eje** (Axis).
5. Defina un **Ángulo** de 360° y asegúrese de que la operación sea **Cuerpo nuevo** (New Body).
6. Haga clic en Aceptar.

El componente resultante es aerodinámicamente perfecto, estructuralmente optimizado para Categoría 3 (CCCD) y listo para ser exportado al laminador (Slicer).
