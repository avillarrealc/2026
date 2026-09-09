/**
 * DASHBOARD MAESTRO DOCENTE MULTIGRADO (9°, 10° Y 11°) - IEJAGA 2026
 * Grado 9: 4 grupos (9°1, 9°2, 9°3, 9°4)
 * Grado 10: 4 grupos (10°1, 10°2, 10°3, 10°4) - Sin clases programadas aún
 * Grado 11: 3 grupos (11°1, 11°2, 11°3)
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
  var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_V3');
  
  if (!raw) {
    var initialData = {
      g9: {
        nombre: "Grado 9°",
        materia: "Fundamentos de Programación (Python)",
        gruposBase: ["9°1", "9°2", "9°3", "9°4"],
        horariosBase: {
          "9°1": "Martes (1° y 2° hora)",
          "9°2": "Miércoles (3° y 4° hora)",
          "9°3": "Jueves (5° y 6° hora)",
          "9°4": "Viernes (1° y 2° hora)"
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
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "03-09-2026", impartida: true, classroom: "Calificada", entregas: "35/35", obs: "Completada" },
              { grupo: "9°4", horario: "Viernes (1° y 2° hora)", fecha: "04-09-2026", impartida: true, classroom: "Calificada", entregas: "32/32", obs: "Completada" }
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
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Lista para impartir" },
              { grupo: "9°4", horario: "Viernes (1° y 2° hora)", fecha: "11-09-2026", impartida: false, classroom: "Borrador", entregas: "0/32", obs: "Lista para impartir" }
            ]
          },
          {
            id: "g9-p1",
            tipo: "practica",
            numero: "P1",
            titulo: "Práctica en Sala 1: Retos de Listas en Google Colab",
            fechaBase: "11-09-2026",
            grupos: [
              { grupo: "9°1", horario: "Martes (1° y 2° hora)", fecha: "15-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Programada" },
              { grupo: "9°2", horario: "Miércoles (3° y 4° hora)", fecha: "16-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Programada" },
              { grupo: "9°3", horario: "Jueves (5° y 6° hora)", fecha: "17-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Programada" },
              { grupo: "9°4", horario: "Viernes (1° y 2° hora)", fecha: "18-09-2026", impartida: false, classroom: "Borrador", entregas: "0/32", obs: "Programada" }
            ]
          }
        ]
      },
      g10: {
        nombre: "Grado 10°",
        materia: "El Proyecto Arduino y Circuitos en Tinkercad",
        gruposBase: ["10°1", "10°2", "10°3", "10°4"],
        horariosBase: {
          "10°1": "Lunes (3° y 4° hora)",
          "10°2": "Miércoles (1° y 2° hora)",
          "10°3": "Jueves (3° y 4° hora)",
          "10°4": "Viernes (3° y 4° hora)"
        },
        sesiones: [
          {
            id: "g10-c10",
            tipo: "regular",
            numero: 10,
            titulo: "Clase 10: Ejercicios de Ley de Ohm en Tinkercad",
            fechaBase: "09-09-2026",
            grupos: [
              { grupo: "10°2", horario: "Miércoles (1° y 2° hora)", fecha: "09-09-2026", impartida: false, classroom: "Borrador", entregas: "0/34", obs: "Programada" },
              { grupo: "10°3", horario: "Jueves (3° y 4° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/33", obs: "Programada" },
              { grupo: "10°4", horario: "Viernes (3° y 4° hora)", fecha: "11-09-2026", impartida: false, classroom: "Borrador", entregas: "0/32", obs: "Programada" },
              { grupo: "10°1", horario: "Lunes (3° y 4° hora)", fecha: "14-09-2026", impartida: false, classroom: "Borrador", entregas: "0/35", obs: "Programada" }
            ]
          }
        ]
      },
      g11: {
        nombre: "Grado 11°",
        materia: "Producción Audiovisual y Página de Ventas",
        gruposBase: ["11°1", "11°2", "11°3"],
        horariosBase: {
          "11°1": "Lunes (1° y 2° hora)",
          "11°2": "Jueves (3° y 4° hora)",
          "11°3": "Viernes (5° y 6° hora)"
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
              { grupo: "11°2", horario: "Jueves (3° y 4° hora)", fecha: "10-09-2026", impartida: false, classroom: "Borrador", entregas: "0/29", obs: "Programada" },
              { grupo: "11°3", horario: "Viernes (5° y 6° hora)", fecha: "11-09-2026", impartida: false, classroom: "Borrador", entregas: "0/30", obs: "Programada" }
            ]
          }
        ]
      }
    };
    props.setProperty('IEJAGA_CONTROL_MULTIGRADO_V3', JSON.stringify(initialData));
    return initialData;
  }
  
  try {
    var data = JSON.parse(raw);
    return sanitizeGradesOnServer(data);
  } catch(e) {
    Logger.log("Error parseando datos: " + e.message);
    return sanitizeGradesOnServer({});
  }
}

// Asegurar que cada grado tenga sus gruposBase y sesiones
function sanitizeGradesOnServer(data) {
  if (!data) data = {};
  
  var defaults = {
    g9: {
      nombre: "Grado 9°",
      materia: "Fundamentos de Programación (Python)",
      gruposBase: ["9°1", "9°2", "9°3", "9°4"],
      horariosBase: {
        "9°1": "Martes (1° y 2° hora)",
        "9°2": "Miércoles (3° y 4° hora)",
        "9°3": "Jueves (5° y 6° hora)",
        "9°4": "Viernes (1° y 2° hora)"
      }
    },
    g10: {
      nombre: "Grado 10°",
      materia: "El Proyecto Arduino y Circuitos en Tinkercad",
      gruposBase: ["10°1", "10°2", "10°3", "10°4"],
      horariosBase: {
        "10°1": "Lunes (3° y 4° hora)",
        "10°2": "Miércoles (1° y 2° hora)",
        "10°3": "Jueves (3° y 4° hora)",
        "10°4": "Viernes (3° y 4° hora)"
      }
    },
    g11: {
      nombre: "Grado 11°",
      materia: "Producción Audiovisual y Página de Ventas",
      gruposBase: ["11°1", "11°2", "11°3"],
      horariosBase: {
        "11°1": "Lunes (1° y 2° hora)",
        "11°2": "Jueves (3° y 4° hora)",
        "11°3": "Viernes (5° y 6° hora)"
      }
    }
  };

  ['g9', 'g10', 'g11'].forEach(function(k) {
    if (!data[k]) data[k] = defaults[k];
    if (!data[k].nombre) data[k].nombre = defaults[k].nombre;
    if (!data[k].materia) data[k].materia = defaults[k].materia;
    if (!data[k].gruposBase || !Array.isArray(data[k].gruposBase) || data[k].gruposBase.length === 0) {
      data[k].gruposBase = defaults[k].gruposBase;
    }
    if (!data[k].horariosBase) {
      data[k].horariosBase = defaults[k].horariosBase;
    }
    if (!data[k].sesiones || !Array.isArray(data[k].sesiones)) {
      data[k].sesiones = [];
    }
  });

  return data;
}

// Guardar los datos completos del grado en la nube de Google
function saveAllGradeData(gradeKey, gradeData) {
  try {
    var props = PropertiesService.getUserProperties();
    var raw = props.getProperty('IEJAGA_CONTROL_MULTIGRADO_V3');
    var allData = raw ? JSON.parse(raw) : {};
    
    allData[gradeKey] = gradeData;
    props.setProperty('IEJAGA_CONTROL_MULTIGRADO_V3', JSON.stringify(allData));

    // Generar CSV consolidado de ese grado en Google Drive (no bloqueante)
    try {
      var fileName = "Control_" + gradeKey.toUpperCase() + "_2026.csv";
      var csvContent = "Tipo Sesión,Clase / Práctica,Fecha Base,Grupo,Horario,Fecha Impartida,¿Impartida?,Classroom,Entregas,Observaciones\n";
      
      if (gradeData.sesiones && gradeData.sesiones.length > 0) {
        gradeData.sesiones.forEach(function(s) {
          var tipoTag = s.tipo === 'practica' ? '[PRÁCTICA]' : '[REGULAR]';
          var tituloClean = '"' + (s.titulo || '').replace(/"/g, '""') + '"';
          
          if (s.grupos && s.grupos.length > 0) {
            s.grupos.forEach(function(g) {
              var cleanObs = '"' + (g.obs || '').replace(/"/g, '""') + '"';
              csvContent += tipoTag + ',' + tituloClean + ',' + s.fechaBase + ',' + g.grupo + ',"' + g.horario + '",' + g.fecha + ',' + (g.impartida ? 'TRUE' : 'FALSE') + ',' + g.classroom + ',' + g.entregas + ',' + cleanObs + '\n';
            });
          }
        });
      }

      var files = DriveApp.getFilesByName(fileName);
      if (files.hasNext()) {
        var file = files.next();
        file.setContent(csvContent);
      } else {
        DriveApp.createFile(fileName, csvContent, MimeType.PLAIN_TEXT);
      }
    } catch(eDrive) {
      Logger.log("Aviso CSV Drive: " + eDrive.message);
    }

    return { success: true, hora: new Date().toLocaleTimeString() };
  } catch(err) {
    Logger.log("Error saveAllGradeData: " + err.message);
    return { success: false, error: err.message, hora: new Date().toLocaleTimeString() };
  }
}
