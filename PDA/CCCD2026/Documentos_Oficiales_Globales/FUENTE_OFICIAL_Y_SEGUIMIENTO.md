# Fuente Oficial de Documentos CCCD 2026 y Seguimiento de Versiones

**Fuente oficial:** https://cccd.space/documentos
**Método de escaneo 2026-09-21:** sitio SPA React. `curl` a `https://cccd.space/documentos` retorna shell vacío + bundle `/assets/index-BVXGjl6K.js`. Listado real extraído de chunk `/assets/Documentos-BcOgGePm.js`. No se dispone de Chrome DevTools MCP en este entorno; se usó análisis estático del bundle + verificación `HEAD` por documento.
**Estado local verificado:** 2026-09-21. Los 8 `Content-Length` remotos coinciden byte a byte con los archivos en `Documentos_Oficiales_Globales/`. Sin actualizaciones pendientes.

## Tarea programada diaria (05:00 y 17:00)

- **Nombre:** `CCCD2026_Scan_Documentos` (Programador de tareas de Windows, estado Ready).
- **Disparadores:** diario 05:00 y diario 17:00. Proxima ejecucion verificada: 21/09/2026 17:00.
- **Script:** `scan_cccd_documentos.ps1` (misma carpeta). Clave de comparacion: `id` numerico del chunk remoto + `HEAD` (`Content-Length`, `ETag`) por PDF.
- **Log:** `seguimiento_diario.log`. Ante cambio: exit 2 + archivo `ALERTA_CAMBIO_YYYY-MM-DD_HH-mm.txt`.
- **Notificacion ante version nueva:** archivo `ALERTA_CAMBIO_YYYY-MM-DD_HH-mm.txt` en la misma carpeta (email a `alexvillarreal@jaga.edu.co` desactivado por decision del usuario 2026-09-21: solo archivo).
- **Nota de encoding:** el chunk JS remoto trae nombres con `ñ` corruptos (`�`); por eso la comparacion es por `id`, no por nombre.

## Tabla de seguimiento

| # | Documento local | Fecha publicación (remoto) | Versión (remoto) | Tamaño remoto (bytes) | ETag remoto | URL remota | Estado local |
|---|---|---|---|---|---|---|---|
| 1 | Reglamento General de Competencia CCCD 2026.pdf | 2026-04-02 | 1.0.0 | 995588 | e657442eb0e9a351ce28a88be22302dd | https://cccd.space/docs/Reglamento%20General%20de%20Competencia%20CCCD%202026.pdf | Sincronizado (995588 bytes, 2026-09-17 descarga) |
| 2 | Motores Permitidos.pdf | 2026-04-02 | 1.0.0 | 3325111 | ba334d8fdf554408bc4712507d50b30b | https://cccd.space/docs/Motores%20Permitidos.pdf | Sincronizado (3325111 bytes) |
| 3 | Diseño Construcción y Pruebas.pdf | 2026-04-02 | 1.0.0 | 1242574 | 305622807c0172d21d4494f3031e1aca | https://cccd.space/docs/Dise%C3%B1o%20Construcci%C3%B3n%20y%20Pruebas.pdf | Sincronizado (1242574 bytes) |
| 4 | Norma de Seguridad en Cohetería.pdf | 2026-04-02 | 1.0.0 | 1093234 | 3b0baf8a3fd721d1f99df2e968ce0758 | https://cccd.space/docs/Norma%20de%20Seguridad%20en%20Coheter%C3%ADa.pdf | Sincronizado (1093234 bytes) |
| 5 | Procedimientos de Inspección y Certificación.pdf | 2026-04-02 | 1.0.0 | 1014632 | 76d71af113f8f1235367aeb4ecdf09d5 | https://cccd.space/docs/Procedimientos%20de%20Inspecci%C3%B3n%20y%20Certificaci%C3%B3n.pdf | Sincronizado (1014632 bytes) |
| 6 | Cumplimiento y Evaluación.pdf | 2026-04-02 | 1.0.0 | 938997 | 4df23dbbb074d0794ebc0ce9608eca6d | https://cccd.space/docs/Cumplimiento%20y%20Evaluaci%C3%B3n.pdf | Sincronizado (938997 bytes) |
| 7 | Código de Conducta y Responsabilidad de las Delegaciones.pdf | 2026-04-02 | 1.0.0 | 985014 | 358909820b8782793ae2832edd9602f3 | https://cccd.space/docs/C%C3%B3digo%20de%20Conducta%20y%20Responsabilidad%20de%20las%20Delegaciones.pdf | Sincronizado (985014 bytes) |
| 8 | Guía CanSat.pdf | 2026-08-07 | 1.0.0 | 1336874 | ff566af226b19452f5313e43331c1935 | https://cccd.space/docs/Gu%C3%ADa%20CanSat.pdf | Sincronizado (1336874 bytes) |

## Procedimiento de seguimiento diario

1. `curl -sL https://cccd.space/assets/Documentos-BcOgGePm.js` y extraer bloques `{id, description, date, version, link}`. El nombre del chunk (`Documentos-*.js`) cambia en cada deploy; obtener nombre actual desde `index-*.js` con patrón `Documentos-*.js`.
2. Para cada `link` en `/docs/*.pdf`, ejecutar `curl -sI https://cccd.space/docs/<encode>` y comparar `Content-Length`, `ETag` y `version`/`date` contra esta tabla.
3. Criterio de actualización: cambio en `version`, `date`, `Content-Length` o `ETag` = descargar PDF, reemplazar en `Documentos_Oficiales_Globales/`, regenerar `txt_dumps/`, actualizar esta tabla con nueva fecha de verificación.
4. Verificar también formularios de entrega por categoría (no están en `/documentos`):
   - Cat1 Noctux Reporte Progreso 1: https://forms.gle/t2kAEV1NTeHhFJYW8 — **[COMPLETADO 2026-09-22, respuesta registrada verificada por captura]**
   - Cat2 Stars Reporte Progreso 1: https://forms.gle/1fq4DQ89jp4gdHe49
   - Cat3 Rocketeers Reporte Progreso 1: https://forms.gle/WRggMzyRChvw5qHR7
   - Plataforma educativa: https://academy.satelab.org/cccd/554e1756-bf1e-476a-88c8-49806d1acc21
