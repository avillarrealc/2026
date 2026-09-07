/**
 * DASHBOARD MAESTRO DOCENTE MULTIGRADO (9°, 10° Y 11°) - IEJAGA 2026
 * Una sola aplicación web para controlar todos los grupos de la institución.
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Dashboard')
    .setTitle('Panel Docente IEJAGA 2026 · Control de Clases')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Cargar datos de todos los grados desde la nube
function loadAllGradesData() {
  var props = PropertiesService.getUserProperties();
  var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_2026');
  
  if (!raw) {
    // Datos iniciales por defecto si es la primera vez
    var initialData = {
      g9: {
        nombre: "Grado 9°",
        materia: "Fundamentos de Programación (Python)",
        claseActual: 9,
        temaClase: "Clase 9: Listas en Python: Indexación y Corchetes",
        fechaBase: "08-09-2026",
        grupos: [
          { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "08-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Programada para martes 08-09" },
          { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Programada para miércoles 09-09" },
          { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Programada para jueves 10-09" }
        ]
      },
      g10: {
        nombre: "Grado 10°",
        materia: "El Proyecto Arduino y Circuitos en Tinkercad",
        claseActual: 9,
        temaClase: "Clase 9: Entradas Digitales con Pulsadores en Arduino",
        fechaBase: "08-09-2026",
        grupos: [
          { grupo: "10°1", horario: "Lunes (3° y 4° hora)", fecha: "07-09-2026", impartida: false, classroom: "Borrador", entregas: "0/32", obs: "Programada para lunes 07-09" },
          { grupo: "10°2", horario: "Miércoles (1° y 2° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/31", obs: "Programada para miércoles 09-09" },
          { grupo: "10°3", horario: "Viernes (3° y 4° hora)", fecha: "11-09-2026", impartida: false, classroom: "Borrador", entregas: "0/30", obs: "Programada para viernes 11-09" }
        ]
      },
      g11: {
        nombre: "Grado 11°",
        materia: "Producción Audiovisual y Página de Ventas",
        claseActual: 11,
        temaClase: "Clase 11: Guion Técnico y Storyboard para Video Comercial",
        fechaBase: "07-09-2026",
        grupos: [
          { grupo: "11°1", horario: "Lunes (1° y 2° hora)", fecha: "07-09-2026", impartida: false, classroom: "Borrador", entregas: "0/28", obs: "Programada para lunes 07-09" },
          { grupo: "11°2", horario: "Jueves (3° y 4° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/29", obs: "Programada para jueves 10-09" }
        ]
      }
    };
    return initialData;
  }
  
  return JSON.parse(raw);
}

// Guardar los datos de un grado específico en la nube y actualizar el CSV correspondiente en Drive
function saveGradeData(gradeKey, gradeData) {
  var props = PropertiesService.getUserProperties();
  var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_2026');
  var allData = raw ? JSON.parse(raw) : {};
  
  allData[gradeKey] = gradeData;
  props.setProperty('IEJAGA_CONTROL_MULTIGRADO_2026', JSON.stringify(allData));

  // Generar / actualizar archivo CSV del grado en Google Drive
  try {
    var fileName = "Control_" + gradeKey.toUpperCase() + "_2026.csv";
    var csvContent = "Grupo,Horario,Fecha de Clase,¿Impartida?,Classroom,Entregas,Observaciones / Novedades\n";
    gradeData.grupos.forEach(function(g) {
      var cleanObs = (g.obs || '').replace(/"/g, '""');
      csvContent += g.grupo + ',"' + g.horario + '",' + g.fecha + ',' + (g.impartida ? 'TRUE' : 'FALSE') + ',' + g.classroom + ',' + g.entregas + ',"' + cleanObs + '"\n';
    });

    var files = DriveApp.getFilesByName(fileName);
    if (files.hasNext()) {
      var file = files.next();
      file.setContent(csvContent);
    } else {
      DriveApp.createFile(fileName, csvContent, MimeType.PLAIN_TEXT);
    }
  } catch(e) {
    Logger.log("Error al escribir CSV: " + e.message);
  }

  return { success: true, hora: new Date().toLocaleTimeString() };
}
