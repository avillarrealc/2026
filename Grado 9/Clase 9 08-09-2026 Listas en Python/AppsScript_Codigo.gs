/**
 * CONTROL DE CLASES EN LA NUBE - I.E. JOSÉ ANTONIO GALÁN
 * Este script corre 100% en Google Drive / Google Apps Script.
 * Sirve la interfaz bonita y guarda los datos en la nube cada vez que marcas una casilla.
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Control de Grupos · Clase 9 (IEJAGA)')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Carga los datos guardados en la nube de Google
function loadData() {
  var props = PropertiesService.getUserProperties();
  var raw = props.getProperty('CONTROL_CLASE_9_GRUPOS');
  
  if (!raw) {
    // Datos iniciales si es la primera vez que se abre
    return [
      { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "08-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Programada para martes 08-09" },
      { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Programada para miércoles 09-09" },
      { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Programada para jueves 10-09" }
    ];
  }
  
  return JSON.parse(raw);
}

// Guarda los datos en la nube y actualiza automáticamente el CSV en Google Drive
function saveData(data) {
  // 1. Guardar en la memoria permanente de la cuenta de Google
  var props = PropertiesService.getUserProperties();
  props.setProperty('CONTROL_CLASE_9_GRUPOS', JSON.stringify(data));

  // 2. Actualizar o crear automáticamente el archivo CSV en tu Google Drive
  try {
    var csvContent = "Grupo,Horario Habitual,Fecha de Clase,¿Impartida?,Classroom,Entregas,Observaciones / Novedades\n";
    data.forEach(function(g) {
      var obsClean = (g.obs || '').replace(/"/g, '""');
      csvContent += g.grupo + ',"' + g.horario + '",' + g.fecha + ',' + (g.impartida ? 'TRUE' : 'FALSE') + ',' + g.classroom + ',' + g.entregas + ',"' + obsClean + '"\n';
    });

    var files = DriveApp.getFilesByName('Control_Grupos_Clase_9_08-09-2026.csv');
    if (files.hasNext()) {
      var file = files.next();
      file.setContent(csvContent);
    } else {
      DriveApp.createFile('Control_Grupos_Clase_9_08-09-2026.csv', csvContent, MimeType.PLAIN_TEXT);
    }
  } catch (e) {
    Logger.log("Error al escribir CSV en Drive: " + e.message);
  }

  return { success: true, hora: new Date().toLocaleTimeString() };
}
