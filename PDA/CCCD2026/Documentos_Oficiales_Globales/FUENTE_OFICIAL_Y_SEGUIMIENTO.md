# Fuente Oficial de Documentos CCCD 2026 y Seguimiento de Versiones

**Fuente oficial:** https://cccd.space/documentos  
**Método de escaneo:** Sitio SPA React (Vite). El bundle principal `/assets/index-Ds75TG7j.js` carga de forma diferida el chunk de documentos `/assets/Documentos-_zf7UjRB.js`. Los documentos se extraen analizando el bundle y verificando las cabeceras HTTP `HEAD` (`Content-Length`, `ETag`) y sumas de verificación MD5 de cada archivo PDF.  
**Estado local verificado:** **2026-10-23 (22:52)**. Los 8 documentos PDF oficiales remotos coinciden byte a byte y en hash MD5 con los archivos locales en `Documentos_Oficiales_Globales/`. **No hay versiones nuevas de los reglamentos o guías técnicas.**

---

## Tarea Programada Diaria (05:00 y 17:00)

- **Nombre:** `CCCD2026_Scan_Documentos` (Programador de tareas de Windows, estado: Ready).
- **Disparadores:** Diario a las 05:00 y a las 17:00.
- **Script:** `scan_cccd_documentos.ps1` (ubicado en esta misma carpeta).
- **Mecanismo de comparación:** Extrae los enlaces `/docs/*.pdf` y fechas declaradas en el chunk JS remoto `Documentos-*.js` mediante decodificación UTF-8 y normalización de caracteres, ejecutando luego una consulta `HEAD` para validar `Content-Length` y `ETag` contra la línea base.
- **Log de ejecución:** `seguimiento_diario.log`.
- **Notificación ante cambio detectado:** Genera un archivo de alerta `ALERTA_CAMBIO_YYYY-MM-DD_HH-mm.txt` con código de salida `2` (notificación local en disco; envío de correo desactivado por directiva técnica).

---

## Tabla de Seguimiento de Documentos Oficiales

| # | Documento local | Fecha publicación (remoto) | Versión (remoto) | Tamaño (bytes) | Hash MD5 | ETag remoto | Estado local |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `Reglamento General de Competencia CCCD 2026.pdf` | 2026-04-02 | 1.0.0 | 995.588 | `6bf71ef90226373e2a78e85fc91aaeaf` | `e657442eb0e9a351ce28a88be22302dd` | Sincronizado |
| 2 | `Motores Permitidos.pdf` | 2026-04-02 | 1.0.0 | 3.325.111 | `2f3e38d578385ef9a16e993081d0bcd1` | `ba334d8fdf554408bc4712507d50b30b` | Sincronizado |
| 3 | `Diseño Construcción y Pruebas.pdf` | 2026-04-02 | 1.0.0 | 1.242.574 | `8b1832f29ba08e6fe0450c21adb88162` | `305622807c0172d21d4494f3031e1aca` | Sincronizado |
| 4 | `Norma de Seguridad en Cohetería.pdf` | 2026-04-02 | 1.0.0 | 1.093.234 | `fc97339cbc008ee65d263ddd675e6733` | `3b0baf8a3fd721d1f99df2e968ce0758` | Sincronizado |
| 5 | `Procedimientos de Inspección y Certificación.pdf` | 2026-04-02 | 1.0.0 | 1.014.632 | `294238271679b72d842db39204939bd5` | `76d71af113f8f1235367aeb4ecdf09d5` | Sincronizado |
| 6 | `Cumplimiento y Evaluación.pdf` | 2026-04-02 | 1.0.0 | 938.997 | `1bfec45c93b4a2c659e610d4da33972f` | `4df23dbbb074d0794ebc0ce9608eca6d` | Sincronizado |
| 7 | `Código de Conducta y Responsabilidad de las Delegaciones.pdf` | 2026-04-02 | 1.0.0 | 985.014 | `ec9c3048ebb6b4e87c9b1013b494d5fc` | `358909820b8782793ae2832edd9602f3` | Sincronizado |
| 8 | `Guía CanSat.pdf` | 2026-08-07 | 1.0.0 | 1.336.874 | `633e47cb90f8cd95bca4f0d0e95c5ffa` | `ff566af226b19452f5313e43331c1935` | Sincronizado |

---

## Actualizaciones Técnicas y Novedades del Sitio Web Oficial (2026-10-23)

1. **Reestructuración del Frontend Web (Vite / React):**
   - El sitio actualizó sus artefactos compilados (`index-Ds75TG7j.js` y `Documentos-_zf7UjRB.js`).
   - El script de monitoreo local (`scan_cccd_documentos.ps1`) fue actualizado para soportar el nuevo esquema de objetos del frontend, decodificación UTF-8 e interoperabilidad con nombres de archivo tildados.

2. **Cronograma Oficial de Lanzamientos (Santa Fe de Antioquia):**
   - **Día 1 (Viernes 6 de noviembre):** Inauguración. De 7:00 a. m. a 10:00 a. m. ingreso privado exclusivo para concursantes. Posteriormente se abre el ingreso a padres de familia y acompañantes.
   - **Día 2 (Sábado 7 de noviembre):** Lanzamientos Categoría 1 (PDA Noctux) y Categoría 2 (PDA Stars). Todo el día. Acceso abierto al público general.
   - **Día 3 (Domingo 8 de noviembre):** Lanzamientos Categoría 3 (PDA Rocketeers). Todo el día. Acceso abierto al público general.
   - **Estado oficial de inscripciones:** "Las inscripciones al CCCD 2026 ya cerraron. Estamos en la etapa de verificación de la información entregada por los equipos, de cara a la inauguración presencial de los lanzamientos el 6 de noviembre. Esta verificación es un proceso interno del staff - los equipos inscritos no necesitan realizar ninguna acción adicional."

3. **Módulo de Escrutinio Técnico en Plataforma (`TechnicalScrutinyPage`):**
   - Se detectó la integración del panel de escrutinio técnico en el dashboard de equipos para la verificación automática de archivos `.ork` (OpenRocket).
   - Valida: longitud total, masa máxima, estabilidad estática (rango de referencia en plataforma 1.50 - 2.50 cal; norma estricta CCCD ≥ 2.0 cal), motor asignado y parámetros de carga útil.

---

## Canales y Enlaces Externos Asociados

- **Formularios de Progreso:**
  - Cat 1 Noctux: `https://forms.gle/t2kAEV1NTeHhFJYW8` *(Completado)*
  - Cat 2 Stars: `https://forms.gle/1fq4DQ89jp4gdHe49`
  - Cat 3 Rocketeers: `https://forms.gle/WRggMzyRChvw5qHR7`
- **Plataforma Educativa SateLab Academy:** `https://academy.satelab.org/cccd/554e1756-bf1e-476a-88c8-49806d1acc21`
- **Software Oficial de Diseño de Paracaídas (ALAS / SateLab):** `https://paracaidas.satelab.org`
- **Credenciales y usuarios:** Custodiados en `PDA/CCCD2026/.credenciales_satelab.json` (Cat 1 Noctux, Cat 2 Stars ID 211, Cat 3 Rocketeers ID 310).
