/**
 * DASHBOARD MAESTRO DOCENTE MULTIGRADO (9°, 10° Y 11°) - IEJAGA 2026
 * Soporta creación dinámica de nuevas clases y clases de práctica sin tocar código.
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Dashboard')
    .setTitle('Panel Docente IEJAGA 2026 · Control de Clases y Prácticas')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Cargar todos los datos de los grados desde la nube
function loadAllGradesData() {
  var props = PropertiesService.getUserProperties();
  var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_V2');
  
  if (!raw) {
    // Estructura inicial con soporte para múltiples clases y sesiones de práctica
    var initialData = {
      g9: {
        nombre: "Grado 9°",
        materia: "Fundamentos de Programación (Python)",
        gruposBase: ["9°1", "9°2", "9°3"],
        horariosBase: {
          "9°1": "Martes (1° y 2° hora)",
          "9°2": "Miércoles (3° y 4° hora)",
          "9°3": "Jueves (5° y 6° hora)"
        },
        sesiones: [
          {
            id: "g9-c8",
            tipo: "regular",
            numero: 8,
            titulo: "Clase 8: Introducción a Colecciones de Datos",
            fechaBase: "01-09-2026",
            grupos: [
              { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "01-09-2026", impartida: true, classroom: "Calificada", entregas: "34/34", obs: "Completada" },
              { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "02-09-2026", impartida: true, classroom: "Calificada", entregas: "33/33", obs: "Completada" },
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "03-09-2026", impartida: true, classroom: "Calificada", entregas: "35/35", obs: "Completada" }
            ]
          },
          {
            id: "g9-c9",
            tipo: "regular",
            numero: 9,
            titulo: "Clase 9: Listas en Python: Indexación y Corchetes",
            fechaBase: "08-09-2026",
            grupos: [
              { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "08-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Lista para impartir" },
              { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Lista para impartir" },
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Lista para impartir" }
            ]
          },
          {
            id: "g9-p1",
            tipo: "practica",
            numero: "P1",
            titulo: "Práctica en Sala 1: Retos de Listas en Google Colab",
            fechaBase: "11-09-2026",
            grupos: [
              { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "15-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Ejercicios de refuerzo" },
              { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "16-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Ejercicios de refuerzo" },
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "17-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Ejercicios de refuerzo" }
            ]
          }
        ]
      },
      g10: {
        nombre: "Grado 10°",
        materia: "El Proyecto Arduino y Circuitos en Tinkercad",
        gruposBase: ["10°1", "10°2", "10°3"],
        horariosBase: {
          "10°1": "Lunes (3° y 4° hora)",
          "10°2": "Miércoles (1° y 2° hora)",
          "10°3": "Viernes (3° y 4° hora)"
        },
        sesiones: [
          {
            id: "g10-c9",
            tipo: "regular",
            numero: 9,
            titulo: "Clase 9: Entradas Digitales con Pulsadores en Arduino",
            fechaBase: "08-09-2026",
            grupos: [
              { grupo: "10°1", horario: "Lunes (3° y 4° hora)", fecha: "07-09-2026", impartida: false, classroom: "Borrador", entregas: "0/32", obs: "Programada" },
              { grupo: "10°2", horario: "Miércoles (1° y 2° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/31", obs: "Programada" },
              { grupo: "10°3", horario: "Viernes (3° y 4° hora)", fecha: "11-09-2026", impartida: false, classroom: "Borrador", entregas: "0/30", obs: "Programada" }
            ]
          }
        ]
      },
      g11: {
        nombre: "Grado 11°",
        materia: "Producción Audiovisual y Página de Ventas",
        gruposBase: ["11°1", "11°2"],
        horariosBase: {
          "11°1": "Lunes (1° y 2° hora)",
          "11°2": "Jueves (3° y 4° hora)"
        },
        sesiones: [
          {
            id: "g11-c11",
            tipo: "regular",
            numero: 11,
            titulo: "Clase 11: Guion Técnico y Storyboard para Video Comercial",
            fechaBase: "07-09-2026",
            grupos: [
              { grupo: "11°1", horario: "Lunes (1° y 2° hora)", fecha: "07-09-2026", impartida: false, classroom: "Borrador", entregas: "0/28", obs: "Programada" },
              { grupo: "11°2", horario: "Jueves (3° y 4° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/29", obs: "Programada" }
            ]
          }
        ]
      }
    };
    return initialData;
  }
  
  return JSON.parse(raw);
}

// Guardar los datos completos del grado (incluyendo nuevas clases o prácticas)
function saveAllGradeData(gradeKey, gradeData) {
  var props = PropertiesService.getUserProperties();
  var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_V2');
  var allData = raw ? JSON.parse(raw) : {};
  
  allData[gradeKey] = gradeData;
  props.setProperty('IEJAGA_CONTROL_MULTIGRADO_V2', JSON.stringify(allData));

  // Generar CSV consolidado de todas las clases de ese grado en Google Drive
  try {
    var fileName = "Control_" + gradeKey.toUpperCase() + "_2026.csv";
    var csvContent = "Tipo Sesión,Clase / Práctica,Fecha Base,Grupo,Horario,Fecha Impartida,¿Impartida?,Classroom,Entregas,Observaciones\n";
    
    gradeData.sesiones.forEach(function(s) {
      var tipoTag = s.tipo === 'practica' ? '[PRÁCTICA]' : '[REGULAR]';
      var tituloClean = '"' + s.titulo.replace(/"/g, '""') + '"';
      
      s.grupos.forEach(function(g) {
        var cleanObs = '"' + (g.obs || '').replace(/"/g, '""') + '"';
        csvContent += tipoTag + ',' + tituloClean + ',' + s.fechaBase + ',' + g.grupo + ',"' + g.horario + '",' + g.fecha + ',' + (g.impartida ? 'TRUE' : 'FALSE') + ',' + g.classroom + ',' + g.entregas + ',' + cleanObs + '\n';
      });
    });

    var files = DriveApp.getFilesByName(fileName);
    if (files.hasNext()) {
      var file = files.next();
      file.setContent(csvContent);
    } else {
      DriveApp.createFile(fileName, csvContent, MimeType.PLAIN_TEXT);
    }
  } catch(e) {
    Logger.log("Error CSV: " + e.message);
  }

  return { success: true, hora: new Date().toLocaleTimeString() };
}
