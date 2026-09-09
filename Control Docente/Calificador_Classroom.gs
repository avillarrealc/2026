/**
/**
 * =========================================================================
 * CALIFICADOR INTELIGENTE DE GOOGLE CLASSROOM CON IA (GEMINI API)
 * I.E. JOSÉ ANTONIO GALÁN - LA ESTRELLA (ANTIOQUIA) - 2026
 * =========================================================================
 * 
 * Requisitos en Google Apps Script:
 * 1. En el menú lateral izquierdo, en "Servicios" (+), activar:
 *    - Google Classroom API (identificador: Classroom)
 *    - Google Drive API (identificador: Drive)
 * 2. Ingresar la API Key gratuita de Gemini (Google AI Studio) desde la interfaz.
 */

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('Calificador_Classroom')
    .setTitle('Calificador IA Classroom · IEJAGA 2026')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// --------------------------------------------------------------------------
// 1. CONEXIÓN GEMINI PARA USO DOCENTE (calificar trabajos, no es app de estudiantes)
// --------------------------------------------------------------------------

var MODELO_POR_DEFECTO = 'gemini-3.6-flash';
var ENDPOINT_POR_DEFECTO = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent';

/**
 * Normaliza el techo de nota para trabajos de seguimiento guiado.
 * Rango permitido: 4.0 a 5.0. Devuelve 5.0 si viene vacío o inválido (sin techo).
 */
function normalizarTecho(valor) {
  var n = Number(valor);
  if (isNaN(n)) return 5.0;
  if (n < 4.0) return 4.0;
  if (n > 5.0) return 5.0;
  return Math.round(n * 10) / 10;
}

/**
 * Nivel del Decreto 1290 con escala fija. El techo no cambia esta escala:
 * Bajo 1.0 a 2.9, Básico 3.0 a 3.9, Alto 4.0 a 4.5, Superior 4.6 a 5.0.
 */
function nivel1290(nota) {
  var n = Number(nota);
  if (n >= 4.6) return 'Superior';
  if (n >= 4.0) return 'Alto';
  if (n >= 3.0) return 'Básico';
  return 'Bajo';
}

/**
 * Aplica el techo a la nota sugerida por la IA.
 * Solo recorta la nota hacia abajo, nunca hacia arriba.
 * El nivel se asigna después con la escala fija del Decreto 1290, sin reescalar.
 */
function aplicarTecho(notaIA, techo) {
  var t = normalizarTecho(techo);
  var nIA = Number(notaIA);
  if (isNaN(nIA)) nIA = 1.0;
  var recortada = false;
  var nFinal = nIA;
  if (t < 5.0 && nIA > t) {
    nFinal = t;
    recortada = true;
  }
  nFinal = Math.round(nFinal * 10) / 10;
  return { notaFinal: nFinal, nivelFinal: nivel1290(nFinal), recortada: recortada, notaIA: Math.round(nIA * 10) / 10, techo: t };
}

/**
 * Descubre dinámicamente qué modelo de Gemini está activo y disponible
 * para la API Key del docente usando la llamada oficial ListModels.
 */
function autoDescubrirEndpoint(key) {
  if (!key) return { success: false, error: 'La clave de API está vacía.' };
  var cleanKey = key.trim();
  
  // 1. Consultar a Google AI Studio la lista de modelos activos en v1beta
  var listUrl = "https://generativelanguage.googleapis.com/v1beta/models?key=" + cleanKey;
  try {
    var resp = UrlFetchApp.fetch(listUrl, {
      method: "get",
      muteHttpExceptions: true
    });
    var code = resp.getResponseCode();
    var respText = resp.getContentText();
    
    if (code === 200) {
      var data = JSON.parse(respText);
      if (data.models && data.models.length > 0) {
        var compatibles = data.models.filter(function(m) {
          return m.supportedGenerationMethods && m.supportedGenerationMethods.indexOf("generateContent") !== -1;
        });
        
        if (compatibles.length > 0) {
          // Ordenar priorizando la serie 3.x Flash
          compatibles.sort(function(a, b) {
            return puntajeModelo(b.name) - puntajeModelo(a.name);
          });
          
          for (var c = 0; c < Math.min(compatibles.length, 6); c++) {
            var modelName = compatibles[c].name; // ej: "models/gemini-3.8-flash"
            var testEndpoint = "https://generativelanguage.googleapis.com/v1beta/" + modelName + ":generateContent";
            var pingTest = probarEndpointDirecto(testEndpoint, cleanKey);
            if (pingTest.ok) {
              PropertiesService.getUserProperties().setProperty('GEMINI_WORKING_ENDPOINT', testEndpoint);
              var cleanName = modelName.replace('models/', '');
              PropertiesService.getUserProperties().setProperty('GEMINI_MODEL_NAME', cleanName);
              return { success: true, endpoint: testEndpoint, model: cleanName };
            }
          }
        }
      }
    } else if (code === 403 || respText.indexOf("denied access") !== -1) {
      return {
        success: false,
        error: "Google rechazó la clave (Error 403: Your project has been denied access).\n\n" +
               "💡 MOTIVO: Google Cloud bloqueó ese proyecto específico por filtros automatizados de seguridad en cuentas sin verificación completa.\n\n" +
               "🚀 SOLUCIÓN EN 1 MINUTO:\n" +
               "1. En aistudio.google.com/app/apikey, haz clic en 'Create API key'.\n" +
               "2. Selecciona 'Create API key in new project' (Crear en proyecto nuevo, ¡no reutilices el anterior!).\n" +
               "3. Si persiste, verifica que tu cuenta de Google tenga teléfono y verificación en dos pasos en myaccount.google.com/security."
      };
    }
  } catch(errList) {
    Logger.log("Error consultando ListModels (v1beta): " + errList.message);
  }
  
  // 2. Si ListModels falló, probar endpoints modernos (v1beta solamente).
  // Ojo: 1.5-flash y 2.5-flash ya fueron retirados para usuarios nuevos (404 / no longer available).
  // Google recomienda 3.6-flash como base compatible. No usar v1 ni 1.5 ni 2.5.
  var endpointsFijos = [
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent"
  ];
  
  var ultimoError = "";
  for (var i = 0; i < endpointsFijos.length; i++) {
    var ep = endpointsFijos[i];
    var test = probarEndpointDirecto(ep, cleanKey);
    if (test.ok) {
      PropertiesService.getUserProperties().setProperty('GEMINI_WORKING_ENDPOINT', ep);
      var modelTag = ep.split('/models/')[1].split(':')[0];
      PropertiesService.getUserProperties().setProperty('GEMINI_MODEL_NAME', modelTag);
      return { success: true, endpoint: ep, model: modelTag };
    } else {
      ultimoError = test.error;
      if (test.code === 403 || (test.error && test.error.indexOf("denied access") !== -1)) {
        return {
          success: false,
          error: "Google rechazó la clave (Error 403: Your project has been denied access).\n\n" +
                 "💡 MOTIVO: El proyecto de Google donde se creó esta clave está bloqueado por filtros de seguridad.\n\n" +
                 "🚀 CÓMO RESOLVERLO:\n" +
                 "Crea una nueva clave en aistudio.google.com seleccionando 'Create API key in new project' (un proyecto nuevo limpio)."
        };
      }
    }
  }
  
  return { 
    success: false, 
    error: "No se pudo validar la conexión con Google Gemini (" + (ultimoError || 'Error de autenticación') + "). Por favor verifica tu clave en aistudio.google.com." 
  };
}

function puntajeModelo(nombre) {
  var s = (nombre || "").toLowerCase();

  // Modelos retirados por Google: nunca usar.
  // 1.5-flash, 1.0 y 2.5-flash dan 404 o "no longer available to new users".
  if (s.indexOf("1.5-flash") !== -1 || s.indexOf("1.0") !== -1 || s.indexOf("1-5") !== -1) {
    return -500;
  }
  if (s.indexOf("2.5-flash") !== -1 || s.indexOf("2.0-flash") !== -1) {
    return -400;
  }
  if (s.indexOf("embedding") !== -1 || s.indexOf("aqa") !== -1 || s.indexOf("tts") !== -1 || s.indexOf("image") !== -1) {
    return -500;
  }
  
  var match = s.match(/gemini-(\d+)(?:\.(\d+))?/);
  var mayor = 1;
  var menor = 0;
  if (match) {
    mayor = parseInt(match[1], 10) || 1;
    menor = match[2] ? parseInt(match[2], 10) : 0;
  }
  
  var score = (mayor * 100) + (menor * 10);
  
  if (s.indexOf("flash") !== -1) score += 50;
  if (s.indexOf("high") !== -1) score += 15;
  if (s.indexOf("preview") !== -1 || s.indexOf("exp") !== -1) score -= 30;
  if (s.indexOf("pro") !== -1) score += 20;
  if (s.indexOf("lite") !== -1) score -= 10;
  // Modelos 2.x quedan como último respaldo, los 3.x primero.
  if (mayor <= 2) score -= 40;
  
  return score;
}

/**
 * Detecta si un endpoint guardado es obsoleto (v1 sola o modelo retirado).
 * Incluye 2.5-flash porque Google ya dice "no longer available to new users".
 */
function esEndpointObsoleto(endpoint) {
  if (!endpoint) return true;
  var e = endpoint.toLowerCase();
  if (e.indexOf("1.5-flash") !== -1 || e.indexOf("1.0-pro") !== -1) return true;
  if (e.indexOf("2.5-flash") !== -1 || e.indexOf("2.0-flash") !== -1) return true;
  // /v1/ sin "v1beta" ya no sirve para flash retirados. Forzar v1beta.
  if (e.indexOf("/v1/") !== -1 && e.indexOf("v1beta") === -1) return true;
  return false;
}

/**
 * Borra la configuración vieja de Gemini (llave + modelo + endpoint).
 * Ejecútala una vez en Apps Script si quedaste pegado en 1.5-flash:
 * Menú Ejecutar > limpiarConfigGemini > Ejecutar.
 */
function limpiarConfigGemini() {
  var props = PropertiesService.getUserProperties();
  props.deleteProperty('GEMINI_API_KEY');
  props.deleteProperty('GEMINI_MODEL_NAME');
  props.deleteProperty('GEMINI_WORKING_ENDPOINT');
  return { success: true, mensaje: 'Configuración borrada. Vuelve a pegar una llave nueva creada en proyecto nuevo.' };
}

function probarEndpointDirecto(endpointUrl, key) {
  try {
    var url = endpointUrl + "?key=" + key;
    var resp = UrlFetchApp.fetch(url, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify({
        contents: [{ parts: [{ text: "hola" }] }]
      }),
      muteHttpExceptions: true
    });
    var code = resp.getResponseCode();
    var text = resp.getContentText();
    var isOk = (code === 200);
    var err = "";
    if (!isOk) {
      try {
        var parsed = JSON.parse(text);
        err = parsed.error ? parsed.error.message : text;
      } catch(e) {
        err = text;
      }
    }
    return { ok: isOk, code: code, error: err };
  } catch(e) {
    return { ok: false, code: 0, error: e.message };
  }
}

function probarClaveGemini(key) {
  if (!key) return { success: false, error: 'La clave está vacía.' };
  var res = autoDescubrirEndpoint(key);
  if (res.success) {
    var nombreDisplay = res.model ? res.model.replace('models/', '') : MODELO_POR_DEFECTO;
    return { success: true, endpoint: res.endpoint, modelo: nombreDisplay };
  } else {
    return { success: false, error: res.error };
  }
}

/**
 * Guarda la clave de Gemini sin bloquear el uso.
 * Solo valida que no esté vacía o incompleta.
 * La elección del modelo se hace después, desde la lista real de Google.
 */
function guardarGeminiApiKey(apiKey) {
  var cleanKey = apiKey ? apiKey.trim() : '';
  if (!cleanKey) {
    return { success: false, error: 'Por favor ingresa una clave de API válida.' };
  }
  if (cleanKey.length < 20) {
    return { success: false, error: 'Esa llave parece incompleta. Cópiala completa de aistudio.google.com.' };
  }
  
  var props = PropertiesService.getUserProperties();
  props.setProperty('GEMINI_API_KEY', cleanKey);
  
  // No se valida aquí para no bloquear. Solo se deja un valor sano si había uno obsoleto.
  var modeloGuardado = props.getProperty('GEMINI_MODEL_NAME') || '';
  var endpointGuardado = props.getProperty('GEMINI_WORKING_ENDPOINT') || '';
  if (!modeloGuardado || !endpointGuardado || esEndpointObsoleto(endpointGuardado) || esEndpointObsoleto(modeloGuardado)) {
    props.setProperty('GEMINI_MODEL_NAME', MODELO_POR_DEFECTO);
    props.setProperty('GEMINI_WORKING_ENDPOINT', ENDPOINT_POR_DEFECTO);
  }
  
  return {
    success: true,
    mensaje: 'Llave guardada. Ahora escoge tu modelo de la lista.',
    modelo: props.getProperty('GEMINI_MODEL_NAME')
  };
}

/**
 * Prueba el modelo que el docente eligió de la lista (sin imponer ninguno).
 * Se usa desde el botón Probar / al cambiar el selector.
 */
function probarModeloElegido(modelId) {
  var props = PropertiesService.getUserProperties();
  var key = props.getProperty('GEMINI_API_KEY');
  if (!key) return { success: false, error: 'Primero guarda tu API Key.' };
  if (!modelId) return { success: false, error: 'Escoge un modelo de la lista.' };
  var endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + modelId + ":generateContent";
  var test = probarEndpointDirecto(endpoint, key.trim());
  if (test.ok) {
    props.setProperty('GEMINI_MODEL_NAME', modelId);
    props.setProperty('GEMINI_WORKING_ENDPOINT', endpoint);
    return { success: true, modelo: modelId, endpoint: endpoint };
  } else {
    return { success: false, error: test.error || ('No se pudo usar ' + modelId + '. Prueba con otro de la lista.') };
  }
}

function verificarGeminiApiKey() {
  var props = PropertiesService.getUserProperties();
  var key = props.getProperty('GEMINI_API_KEY');
  var modelo = props.getProperty('GEMINI_MODEL_NAME') || '';
  var endpoint = props.getProperty('GEMINI_WORKING_ENDPOINT') || '';
  // Si quedó un modelo retirado, se migra al valor por defecto sin borrar la llave.
  if (!modelo || !endpoint || esEndpointObsoleto(endpoint) || esEndpointObsoleto(modelo)) {
    modelo = MODELO_POR_DEFECTO;
    endpoint = ENDPOINT_POR_DEFECTO;
    if (key) {
      props.setProperty('GEMINI_MODEL_NAME', modelo);
      props.setProperty('GEMINI_WORKING_ENDPOINT', endpoint);
    }
  }
  return { 
    hasKey: !!key, 
    preview: key ? (key.substring(0, 6) + '...' + key.substring(key.length - 4)) : '',
    modelo: modelo.replace('models/', '')
  };
}

/**
 * Lista todos los modelos de Gemini disponibles para que EL DOCENTE ESCOJA.
 * No impone ninguno: trae la lista real de Google con ListModels.
 * Si ListModels falla, devuelve el error real + lista de respaldo moderna (sin 1.5 ni 2.5).
 */
function listarModelosGemini(apiKey) {
  var props = PropertiesService.getUserProperties();
  var key = apiKey || props.getProperty('GEMINI_API_KEY');
  var modeloActual = props.getProperty('GEMINI_MODEL_NAME') || MODELO_POR_DEFECTO;
  if (esEndpointObsoleto(modeloActual)) {
    modeloActual = MODELO_POR_DEFECTO;
  }
  
  var fallbackModelos = [
    { id: "gemini-3.6-flash", nombre: "Gemini 3.6 Flash (recomendado por Google)", endpoint: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent" },
    { id: "gemini-3.8-flash", nombre: "Gemini 3.8 Flash (más reciente)", endpoint: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent" },
    { id: "gemini-3.7-flash", nombre: "Gemini 3.7 Flash", endpoint: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent" },
    { id: "gemini-3.5-flash", nombre: "Gemini 3.5 Flash", endpoint: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent" }
  ];
  
  if (!key) {
    if (!modeloActual || esEndpointObsoleto(modeloActual)) {
      modeloActual = MODELO_POR_DEFECTO;
      props.setProperty('GEMINI_MODEL_NAME', modeloActual);
      props.setProperty('GEMINI_WORKING_ENDPOINT', ENDPOINT_POR_DEFECTO);
    }
    return {
      success: true,
      modelos: fallbackModelos,
      modeloSeleccionado: modeloActual,
      fechaConsulta: new Date().toISOString(),
      fuente: 'respaldo-sin-llave'
    };
  }

  var cleanKey = key.trim();
  var lista = [];
  var vistos = {};
  var errorLista = '';
  
  // Consultar a Google AI Studio la lista real de modelos activos en v1beta.
  // No imponemos ninguno: mostramos lo que Google diga que sirve con generateContent.
  var listUrl = "https://generativelanguage.googleapis.com/v1beta/models?key=" + cleanKey;
  try {
    var resp = UrlFetchApp.fetch(listUrl, { method: "get", muteHttpExceptions: true });
    var codeLista = resp.getResponseCode();
    var textLista = resp.getContentText();
    if (codeLista === 200) {
      var data = JSON.parse(textLista);
      if (data.models && data.models.length > 0) {
        data.models.forEach(function(m) {
          if (m.supportedGenerationMethods && m.supportedGenerationMethods.indexOf("generateContent") !== -1) {
            var cleanId = m.name.replace('models/', '');
            if (!vistos[cleanId]) {
              vistos[cleanId] = true;
              var endpoint = "https://generativelanguage.googleapis.com/v1beta/" + m.name + ":generateContent";
              var displayName = m.displayName || cleanId;
              lista.push({
                id: cleanId,
                nombre: displayName,
                endpoint: endpoint,
                version: "v1beta",
                score: puntajeModelo(cleanId)
              });
            }
          }
        });
      }
    } else {
      try {
        var parsedErr = JSON.parse(textLista);
        errorLista = parsedErr.error ? parsedErr.error.message : textLista;
      } catch(eParse) {
        errorLista = textLista;
      }
      errorLista = 'Google (' + codeLista + '): ' + errorLista;
    }
  } catch(err) {
    errorLista = err.message;
    Logger.log("Error listando modelos (v1beta): " + err.message);
  }

  // Filtrar retirados: puntaje negativo = no mostrar (1.5, 2.5, embeddings).
  lista = lista.filter(function(item) { return item.score > 0; });

  if (lista.length > 0) {
    lista.sort(function(a, b) {
      return b.score - a.score;
    });
    
    // Se respeta la elección del docente. Solo se sugiere el primero si el guardado no existe.
    var existe = lista.some(function(item) { return item.id === modeloActual; });
    if (!existe) {
      modeloActual = lista[0].id;
    }
    
    return {
      success: true,
      modelos: lista,
      modeloSeleccionado: modeloActual,
      fechaConsulta: new Date().toISOString(),
      fuente: 'google-listmodels',
      nota: 'Lista real de Google. Usted escoge.'
    };
  }

  // Sin lista en vivo: respaldo moderno más motivo real.
  var enFallback = fallbackModelos.some(function(item) { return item.id === modeloActual; });
  if (!enFallback || esEndpointObsoleto(modeloActual)) {
    modeloActual = MODELO_POR_DEFECTO;
    props.setProperty('GEMINI_MODEL_NAME', modeloActual);
    props.setProperty('GEMINI_WORKING_ENDPOINT', ENDPOINT_POR_DEFECTO);
  }

  return {
    success: true,
    modelos: fallbackModelos,
    modeloSeleccionado: modeloActual,
    fechaConsulta: new Date().toISOString(),
    fuente: 'respaldo',
    advertenciaLista: errorLista || 'No se pudo traer la lista en vivo. Se muestra respaldo. Revise la llave.'
  };
}

/**
 * Guarda el modelo de IA seleccionado por el docente
 */
function guardarModeloSeleccionado(modelId, endpoint) {
  var props = PropertiesService.getUserProperties();
  props.setProperty('GEMINI_MODEL_NAME', modelId);
  var ep = endpoint || ("https://generativelanguage.googleapis.com/v1beta/models/" + modelId + ":generateContent");
  props.setProperty('GEMINI_WORKING_ENDPOINT', ep);
  return { success: true, modelo: modelId, endpoint: ep };
}

// --------------------------------------------------------------------------
// 2. CONEXIÓN CON GOOGLE CLASSROOM API
// --------------------------------------------------------------------------

/**
 * Obtiene todos los cursos activos donde el usuario es docente
 */
function obtenerCursosDocente() {
  try {
    var response = Classroom.Courses.list({
      teacherId: 'me',
      courseStates: ['ACTIVE'],
      pageSize: 50
    });
    
    var cursos = (response.courses || []).map(function(c) {
      return {
        id: c.id,
        nombre: c.name,
        seccion: c.section || '',
        materia: c.descriptionHeading || ''
      };
    });
    
    // Ordenar alfabéticamente por nombre
    cursos.sort(function(a, b) {
      return a.nombre.localeCompare(b.nombre);
    });
    
    return { success: true, cursos: cursos };
  } catch(error) {
    return { success: false, error: 'Error al listar cursos: ' + error.message };
  }
}

/**
 * Obtiene todas las actividades/tareas publicadas de un curso específico.
 * Versión liviana para el selector: trae lo necesario para listar.
 * El detalle completo (materiales y rúbrica) se trae con obtenerDetalleActividad.
 */
function obtenerActividadesCurso(courseId) {
  try {
    var response = Classroom.Courses.CourseWork.list(courseId, {
      courseWorkStates: ['PUBLISHED'],
      pageSize: 100
    });
    
    var actividades = (response.courseWork || []).map(function(w) {
      return {
        id: w.id,
        titulo: w.title,
        descripcion: w.description || '',
        descripcionCorta: (w.description || '').substring(0, 220),
        tieneDescripcion: !!(w.description && w.description.trim() !== ''),
        puntosMaximos: w.maxPoints || 5.0,
        tipoTrabajo: w.workType || '',
        enlace: w.alternateLink,
        fechaCreacion: w.creationTime
      };
    });
    
    // Ordenar por fecha de creación (más recientes primero)
    actividades.sort(function(a, b) {
      return new Date(b.fechaCreacion) - new Date(a.fechaCreacion);
    });
    
    return { success: true, actividades: actividades };
  } catch(error) {
    return { success: false, error: 'Error al listar actividades: ' + error.message };
  }
}

/**
 * Resume los materiales de una tarea en texto corto para el panel docente.
 */
function resumirMateriales(materiales) {
  if (!materiales || materiales.length === 0) return '';
  var lineas = [];
  materiales.forEach(function(m, idx) {
    if (m.driveFile) {
      lineas.push('- Archivo Drive: ' + (m.driveFile.driveFile ? m.driveFile.driveFile.title : (m.driveFile.title || 'adjunto'))); 
    } else if (m.link) {
      lineas.push('- Enlace: ' + (m.link.title || m.link.url) + ' (' + m.link.url + ')');
    } else if (m.youtubeVideo) {
      lineas.push('- Video YouTube: https://youtu.be/' + (m.youtubeVideo.id || ''));
    } else if (m.form) {
      lineas.push('- Formulario: ' + (m.form.formUrl || '') + ' ' + (m.form.title || ''));
    } else {
      lineas.push('- Material ' + (idx + 1));
    }
  });
  return lineas.join('\n');
}

/**
 * Intenta leer la rúbrica asociada a una tarea. No es vinculante, solo referencia.
 * Devuelve { tieneRubrica, texto, criterios } sin lanzar error si no existe.
 */
function obtenerRubricaActividad(courseId, courseWorkId) {
  var resultado = { tieneRubrica: false, texto: '', criterios: [] };
  try {
    var rubricas = null;
    // Recurso Rubrics del servicio avanzado de Classroom (puede no existir según versión).
    if (Classroom.Courses && Classroom.Courses.CourseWork && Classroom.Courses.CourseWork.Rubrics) {
      try {
        rubricas = Classroom.Courses.CourseWork.Rubrics.list(courseId, courseWorkId, { pageSize: 10 });
      } catch(eList) {
        Logger.log('Rubrics.list no disponible: ' + eList.message);
      }
      var items = (rubricas && (rubricas.rubrics || rubricas.items)) || [];
      if (items.length > 0) {
        var r = items[0];
        // Si solo viene el id, intentar traer el detalle.
        if ((!r.criteria || r.criteria.length === 0) && r.courseId && r.courseWorkId && r.id) {
          try {
            r = Classroom.Courses.CourseWork.Rubrics.get(r.courseId, r.courseWorkId, r.id) || r;
          } catch(eGet) {
            Logger.log('Rubrics.get falló: ' + eGet.message);
          }
        }
        var lineas = [];
        if (r.title) lineas.push('Rúbrica: ' + r.title);
        (r.criteria || []).forEach(function(c) {
          var nombreCriterio = c.title || c.name || 'Criterio';
          var niveles = (c.levels || []).map(function(l) {
            return (l.title || l.name || '') + ' (' + (l.points !== undefined ? l.points + ' pts' : '') + '): ' + (l.description || '');
          }).join(' | ');
          lineas.push('- ' + nombreCriterio + (niveles ? ' -> ' + niveles : ''));
          resultado.criterios.push({ criterio: nombreCriterio, niveles: niveles });
        });
        resultado.texto = lineas.join('\n');
        resultado.tieneRubrica = resultado.texto.trim() !== '';
      }
    }
  } catch(e) {
    Logger.log('Sin rúbrica o no soportada: ' + e.message);
  }
  return resultado;
}

/**
 * Trae el detalle completo de una actividad para el panel docente:
 * instrucciones, materiales y rúbrica asociada (si existe, no vinculante).
 * Lo manual que escriba el docente después tiene prelación sobre esto.
 */
function obtenerDetalleActividad(courseId, courseWorkId) {
  try {
    var w = Classroom.Courses.CourseWork.get(courseId, courseWorkId);
    if (!w) return { success: false, error: 'No se encontró la actividad en Classroom.' };
    var instrucciones = w.description || '';
    var materialesTexto = resumirMateriales(w.materials || []);
    var rubrica = obtenerRubricaActividad(courseId, courseWorkId);
    return {
      success: true,
      detalle: {
        id: w.id,
        titulo: w.title || '',
        instrucciones: instrucciones,
        instruccionesCortas: instrucciones.substring(0, 3000),
        materiales: materialesTexto,
        puntosMaximos: w.maxPoints || 5.0,
        tipoTrabajo: w.workType || '',
        enlace: w.alternateLink || '',
        tieneInstrucciones: !!(instrucciones && instrucciones.trim() !== ''),
        tieneRubrica: rubrica.tieneRubrica,
        rubricaTexto: rubrica.texto || '',
        rubricaCorta: (rubrica.texto || '').substring(0, 2500),
        rubricaCriterios: rubrica.criterios
      }
    };
  } catch(error) {
    return { success: false, error: 'Error al traer detalle de la actividad: ' + error.message };
  }
}

/**
 * Dice si un archivo adjunto es una imagen (foto o captura, como la de Tinkercad).
 */
function esArchivoImagen(titulo, mimeType) {
  var t = (titulo || '').toLowerCase();
  var m = (mimeType || '').toLowerCase();
  if (m.indexOf('image/') === 0) return true;
  return (/\.(png|jpe?g|gif|webp|bmp)$/.test(t));
}

/**
 * Lee hasta 2 imágenes de Drive y las deja listas para visión de Gemini.
 * Límite de 3.5 MB por imagen para no exceder la cuota. Devuelve texto de aviso si alguna no se pudo leer.
 */
function leerImagenesParaIA(imagenIds) {
  var imagenes = [];
  var avisos = [];
  var lista = imagenIds || [];
  for (var i = 0; i < Math.min(lista.length, 2); i++) {
    try {
      var file = DriveApp.getFileById(lista[i].id);
      var blob = file.getBlob();
      var bytes = blob.getBytes();
      if (bytes.length > 3670016) {
        avisos.push('La imagen ' + (lista[i].titulo || '') + ' pesa mucho y no se pudo revisar a simple vista.');
        continue;
      }
      var mime = blob.getContentType() || 'image/png';
      imagenes.push({ titulo: lista[i].titulo || 'imagen', mimeType: mime, base64: Utilities.base64Encode(bytes) });
    } catch(eImg) {
      avisos.push('No se pudo abrir la imagen ' + ((lista[i] && lista[i].titulo) || '') + '.');
      Logger.log('No se pudo leer imagen ' + ((lista[i] && lista[i].id) || '') + ': ' + eImg.message);
    }
  }
  if (lista.length > 2) {
    avisos.push('Se revisaron las 2 primeras imágenes.');
  }
  return { imagenes: imagenes, aviso: avisos.join(' ') };
}

/**
 * Dice si una URL es un enlace de Drive o de Docs/Sheets/Slides de Google.
 */
function esEnlaceDrive(url) {
  var u = (url || '').toLowerCase();
  return (u.indexOf('drive.google.com') !== -1 || u.indexOf('docs.google.com') !== -1);
}

/**
 * Saca el ID de archivo de un enlace de Drive/Docs/Sheets/Slides.
 * Soporta /file/d/ID, open?id=ID, /document/d/ID, /spreadsheets/d/ID, etc.
 */
function extraerIdDrive(url) {
  try {
    var m = String(url || '').match(/\/file\/d\/([-\w]+)/)
      || String(url || '').match(/[?&]id=([-\w]+)/)
      || String(url || '').match(/\/(document|spreadsheets|presentation|drawings|forms)\/d\/([-\w]+)/);
    if (!m) return '';
    return m[2] !== undefined && m[1].length < 20 ? m[2] : m[1];
  } catch (e) {
    return '';
  }
}
/**
 * Intenta abrir enlaces de Drive/Docs compartidos como enlace (no adjuntos).
 * Lee Docs como texto e imágenes para visión. Nunca responde en vacío:
 * si no se puede abrir, deja aviso claro para pedir revisión de permisos.
 * Máximo 2 enlaces por estudiante.
 */
function resolverEnlacesDrive(driveLinks) {
  var textos = [];
  var imagenes = [];
  var avisos = [];
  var lista = driveLinks || [];
  for (var i = 0; i < Math.min(lista.length, 2); i++) {
    var url = lista[i].url || '';
    var titulo = lista[i].titulo || url;
    var id = extraerIdDrive(url);
    if (!id) {
      avisos.push('El enlace ' + titulo + ' no trae un ID de archivo reconocible.');
      continue;
    }
    try {
      var file = DriveApp.getFileById(id);
      var blob = file.getBlob();
      var mime = blob.getContentType() || '';
      var nombreReal = titulo;
      try { nombreReal = file.getName() || titulo; } catch (eN) { /* conserva título */ }
      if (mime.indexOf('image/') === 0 || esArchivoImagen(nombreReal, mime)) {
        var bytes = blob.getBytes();
        if (bytes.length > 3670016) {
          avisos.push('La imagen del enlace ' + nombreReal + ' pesa mucho y no se pudo revisar.');
        } else {
          imagenes.push({ titulo: nombreReal, mimeType: mime || 'image/png', base64: Utilities.base64Encode(bytes) });
          textos.push('[Imagen abierta desde enlace de Drive: ' + nombreReal + ' - se revisa a simple vista]');
        }
      } else if (mime.indexOf('google-apps.document') !== -1) {
        try {
          var doc = DocumentApp.openById(id);
          var t = doc.getBody().getText() || '';
          if (t.trim() !== '') {
            textos.push('[Documento de Drive abierto desde enlace: ' + nombreReal + ']\n' + t.substring(0, 4000));
          } else {
            avisos.push('El documento ' + nombreReal + ' se abrió pero está vacío.');
          }
        } catch (eDoc) {
          avisos.push('El documento ' + nombreReal + ' no se pudo abrir (revise que esté compartido).');
        }
      } else if (nombreReal.toLowerCase().indexOf('.brd') !== -1 || (mime.indexOf('text/') === 0 && blob.getDataAsString().indexOf('<eagle') !== -1)) {
        try {
          var extractoBrd = extraerCircuitoBrd(blob.getDataAsString(), nombreReal);
          if (extractoBrd) {
            textos.push(extractoBrd);
          } else {
            avisos.push('El archivo .brd ' + nombreReal + ' no contiene componentes reconocibles.');
          }
        } catch (eBrd) {
          avisos.push('El archivo .brd ' + nombreReal + ' no se pudo interpretar.');
        }
      } else if (mime.indexOf('text/') === 0 || mime.indexOf('csv') !== -1 || mime.indexOf('json') !== -1) {
        try {
          var plano = blob.getDataAsString().substring(0, 4000);
          if (plano.trim() !== '') {
            textos.push('[Archivo de texto abierto desde enlace: ' + nombreReal + ']\n' + plano);
          } else {
            avisos.push('El archivo ' + nombreReal + ' se abrió pero está vacío.');
          }
        } catch (eTxt) {
          avisos.push('El archivo ' + nombreReal + ' no se pudo leer como texto.');
        }
      } else if (mime.indexOf('pdf') !== -1) {
        avisos.push('El enlace ' + nombreReal + ' es un PDF y no se pudo extraer su texto automáticamente; pida al estudiante el contenido en Docs o imagen.');
      } else if (mime.indexOf('spreadsheet') !== -1 || mime.indexOf('presentation') !== -1) {
        avisos.push('El enlace ' + nombreReal + ' es hoja de cálculo o presentación y no se pudo leer automáticamente; pida captura o exportación.');
      } else {
        avisos.push('El enlace ' + nombreReal + ' (' + mime + ') no se pudo interpretar; pida otro formato.');
      }
    } catch (eOpen) {
      avisos.push('El enlace ' + titulo + ' no se pudo abrir (revise que esté compartido con usted).');
      Logger.log('Enlace Drive no abrible ' + url + ': ' + eOpen.message);
    }
  }
  if (lista.length > 2) {
    avisos.push('Se revisaron los 2 primeros enlaces de Drive.');
  }
  return { texto: textos.join('\n'), imagenes: imagenes, aviso: avisos.join(' ') };
}

/**
 * Extrae el código de un cuaderno .ipynb leído como texto (para Colab públicos).
 */
function extraerCodigoIpynb(rawJson, titulo) {
  try {
    var nb = JSON.parse(rawJson);
    var celdasCodigo = (nb.cells || []).filter(function(c) { return c.cell_type === 'code'; });
    if (celdasCodigo.length === 0) return '';
    var extracto = celdasCodigo.map(function(c, idx) {
      var src = Array.isArray(c.source) ? c.source.join('') : (c.source || '');
      var outs = (c.outputs || []).map(function(o) {
        if (o.text) return Array.isArray(o.text) ? o.text.join('') : o.text;
        if (o.evalue) return 'Error: ' + o.evalue;
        return '';
      }).join('\n');
      return 'Celda ' + (idx + 1) + ':\n' + src + (outs ? '\nSalida:\n' + outs : '');
    }).join('\n---\n');
    return '[Cuaderno Colab abierto desde enlace: ' + titulo + ']\n' + extracto.substring(0, 5000);
  } catch (e) {
    return '';
  }
}

/**
 * Extrae un resumen limpio de componentes y conexiones eléctricas (netlist)
 * de un archivo de circuito exportado desde Tinkercad en formato Autodesk EAGLE (.brd).
 * Reduce un archivo XML de 25KB a un extracto ultraligero de ~200 tokens.
 */
function extraerCircuitoBrd(rawXml, titulo) {
  try {
    if (!rawXml) return '';
    var lineas = ['[Circuito Tinkercad / EAGLE (.brd): ' + (titulo || 'circuito.brd') + ']'];
    
    // 1. Extraer elementos / componentes
    var mElements = rawXml.match(/<elements>([\s\S]*?)<\/elements>/i);
    lineas.push('\nCOMPONENTES INSTALADOS:');
    if (mElements && mElements[1]) {
      var elemMatches = mElements[1].match(/<element\b[^>]*\/?>/gi) || [];
      elemMatches.forEach(function(elStr) {
        var nameMatch = elStr.match(/\bname="([^"]*)"/i);
        var valMatch = elStr.match(/\bvalue="([^"]*)"/i);
        var pkgMatch = elStr.match(/\bpackage="([^"]*)"/i);
        var name = nameMatch ? nameMatch[1] : 'Componente';
        var val = valMatch ? valMatch[1] : '';
        var pkg = pkgMatch ? pkgMatch[1] : '';
        lineas.push('- ' + name + (val ? ': valor="' + val + '"' : '') + (pkg ? ' (paquete: ' + pkg + ')' : ''));
      });
      if (elemMatches.length === 0) lineas.push('(No se detectaron componentes en <elements>)');
    } else {
      lineas.push('(Sin sección de componentes)');
    }
    
    // 2. Extraer señales / conexiones (Netlist)
    var mSignals = rawXml.match(/<signals>([\s\S]*?)<\/signals>/i);
    lineas.push('\nCONEXIONES Y CABLES ELÉCTRICOS (NETLIST):');
    if (mSignals && mSignals[1]) {
      var sigBlocks = mSignals[1].match(/<signal\b[\s\S]*?<\/signal>/gi) || [];
      sigBlocks.forEach(function(sigStr) {
        var sigNameMatch = sigStr.match(/<signal\b[^>]*\bname="([^"]*)"/i);
        var sigName = sigNameMatch ? sigNameMatch[1] : 'Red';
        var conns = [];
        var refMatches = sigStr.match(/<contactref\b[^>]*\/?>/gi) || [];
        refMatches.forEach(function(refStr) {
          var elM = refStr.match(/\belement="([^"]*)"/i);
          var padM = refStr.match(/\bpad="([^"]*)"/i);
          if (elM && padM) {
            conns.push(elM[1] + '.pad(' + padM[1] + ')');
          }
        });
        if (conns.length > 0) {
          lineas.push('- Red ' + sigName + ': ' + conns.join(' <--> '));
        }
      });
      if (sigBlocks.length === 0) lineas.push('(No se detectaron cables o conexiones en <signals>)');
    } else {
      lineas.push('(Sin sección de conexiones)');
    }
    
    return lineas.join('\n');
  } catch (e) {
    Logger.log('Error parseando .brd: ' + e.message);
    return '[Archivo .brd: ' + (titulo || '') + ' - no se pudo interpretar el esquema XML]';
  }
}

/**
 * Limpia HTML a texto visible corto (título, descripción y contenido).
 */
function textoVisibleDeHtml(html) {
  try {
    var titulo = '';
    var mTitle = html.match(/<title[^>]*>([^<]*)<\/title>/i);
    if (mTitle) titulo = mTitle[1].trim();
    var desc = extraerMeta(html, 'og:description') || extraerMeta(html, 'description');
    var cuerpo = html.replace(/<script[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style[\s\S]*?<\/style>/gi, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ').trim();
    var partes = [];
    if (titulo) partes.push('Título de la página: ' + titulo.substring(0, 200));
    if (desc) partes.push('Descripción: ' + desc.substring(0, 400));
    if (cuerpo) partes.push('Contenido visible: ' + cuerpo.substring(0, 1200));
    return partes.join('\n');
  } catch (e) {
    return '';
  }
}

/**
 * Intenta ABRIR enlaces públicos entregados (Colab, código, páginas).
 * Un enlace público de Colab o de código SÍ se puede leer: se trae su
 * contenido y va a la IA. Solo si de verdad no abre se deja aviso puntual,
 * sin regaños y sin pedir otro formato por defecto.
 * Máximo 2 enlaces por estudiante.
 */
function resolverEnlacesPublicos(links) {
  var textos = [];
  var imagenes = [];
  var avisos = [];
  var lista = links || [];
  for (var i = 0; i < Math.min(lista.length, 2); i++) {
    var url = (lista[i].url || '').trim();
    var titulo = lista[i].titulo || url;
    if (!url || url.toLowerCase().indexOf('http') !== 0) {
      continue;
    }
    var bajo = url.toLowerCase();
    try {
      // 1. Colab público con ID de Drive: se lee el cuaderno directamente.
      var mColab = url.match(/colab\.research\.google\.com\/drive\/([-\w]+)/i);
      if (mColab) {
        try {
          var rawColab = DriveApp.getFileById(mColab[1]).getBlob().getDataAsString();
          var codigo = extraerCodigoIpynb(rawColab, titulo);
          if (codigo) {
            textos.push(codigo);
            continue;
          }
          avisos.push('El Colab ' + titulo + ' abrió pero no se pudo interpretar su código (revise que el enlace sea público).');
        } catch (eColab) {
          avisos.push('El Colab ' + titulo + ' no se pudo abrir (revise que el enlace sea público).');
        }
        continue;
      }
      // 2. Archivos binarios que no se pueden calificar como texto.
      if (/\.(mp4|avi|mov|zip|rar|mp3|wav|exe|apk)(\?|#|$)/i.test(bajo)) {
        avisos.push('El enlace ' + titulo + ' es un archivo multimedia o comprimido y no se pudo revisar su contenido.');
        continue;
      }
      // 3. Imágenes directas: van a visión.
      if (/\.(png|jpe?g|gif|webp|bmp)(\?|#|$)/i.test(bajo)) {
        try {
          var respImg = UrlFetchApp.fetch(url, { method: 'get', muteHttpExceptions: true, followRedirects: true });
          if (respImg.getResponseCode() >= 200 && respImg.getResponseCode() < 400) {
            var blobImg = respImg.getBlob();
            var bytesImg = blobImg.getBytes();
            if (bytesImg.length > 0 && bytesImg.length <= 3670016) {
              imagenes.push({ titulo: titulo, mimeType: blobImg.getContentType() || 'image/png', base64: Utilities.base64Encode(bytesImg) });
              textos.push('[Imagen abierta desde enlace: ' + titulo + ' - se revisa a simple vista]');
              continue;
            }
          }
          avisos.push('La imagen del enlace ' + titulo + ' no se pudo descargar.');
        } catch (eImg) {
          avisos.push('La imagen del enlace ' + titulo + ' no se pudo descargar.');
        }
        continue;
      }
      // 4. GitHub blob -> raw, y textos planos directos.
      var urlFetch = url;
      var mGh = bajo.match(/github\.com\/([^\/]+\/[^\/]+)\/blob\/(.+)/);
      if (mGh) {
        urlFetch = 'https://raw.githubusercontent.com/' + mGh[1] + '/' + mGh[2];
      }
      var resp = UrlFetchApp.fetch(urlFetch, { method: 'get', muteHttpExceptions: true, followRedirects: true });
      var code = resp.getResponseCode();
      if (code < 200 || code >= 400) {
        avisos.push('El enlace ' + titulo + ' no abrió (HTTP ' + code + ').');
        continue;
      }
      var mime = '';
      try { mime = resp.getBlob().getContentType() || ''; } catch (eMime) { mime = ''; }
      var contenido = '';
      try { contenido = resp.getContentText().substring(0, 6000); } catch (eTxt) { contenido = ''; }
      if (!contenido || contenido.trim() === '') {
        avisos.push('El enlace ' + titulo + ' abrió pero no trajo contenido legible.');
        continue;
      }
      if (mime.indexOf('text/') === 0 || mime.indexOf('json') !== -1 || mime.indexOf('javascript') !== -1 ||
          /\.(py|js|java|c|cpp|txt|csv|md|ipynb)(\?|#|$)/i.test(bajo) || bajo.indexOf('raw.githubusercontent') !== -1 ||
          bajo.indexOf('gist.githubusercontent') !== -1 || bajo.indexOf('pastebin') !== -1) {
        if (/\.ipynb(\?|#|$)/i.test(bajo) || contenido.trim().charAt(0) === '{') {
          var codNb = extraerCodigoIpynb(contenido, titulo);
          textos.push(codNb !== '' ? codNb : '[Código abierto desde enlace: ' + titulo + ']\n' + contenido.substring(0, 5000));
        } else {
          textos.push('[Contenido abierto desde enlace: ' + titulo + ']\n' + contenido.substring(0, 5000));
        }
      } else {
        var visible = textoVisibleDeHtml(contenido);
        if (visible) {
          textos.push('[Página abierta desde enlace: ' + titulo + ']\n' + visible);
        } else {
          avisos.push('El enlace ' + titulo + ' abrió pero no trajo texto aprovechable.');
        }
      }
    } catch (eGen) {
      avisos.push('El enlace ' + titulo + ' no se pudo abrir en este intento.');
      Logger.log('Enlace público no abrible ' + url + ': ' + eGen.message);
    }
  }
  if (lista.length > 2) {
    avisos.push('Se revisaron los 2 primeros enlaces.');
  }
  return { texto: textos.join('\n'), imagenes: imagenes, aviso: avisos.join(' ') };
}

function esUrlSimulacion(url) {
  var u = (url || '').toLowerCase();
  return (u.indexOf('tinkercad') !== -1 || u.indexOf('falstad') !== -1 || u.indexOf('circuit') !== -1);
}

/**
 * Extrae una etiqueta meta (og:title, og:description, og:image) de un HTML.
 */
function extraerMeta(html, propiedad) {
  try {
    var re = new RegExp('<meta[^>]+property=["\']' + propiedad + '["\'][^>]*>', 'i');
    var m = html.match(re);
    if (!m) {
      re = new RegExp('<meta[^>]+name=["\']' + propiedad + '["\'][^>]*>', 'i');
      m = html.match(re);
    }
    if (!m) return '';
    var tag = m[0];
    var c = tag.match(/content=["']([^"']*)["']/i);
    return c ? c[1] : '';
  } catch(e) {
    return '';
  }
}

/**
 * Intenta leer los datos públicos de un enlace de simulación (título, descripción, miniatura).
 * Las simulaciones interactivas exigen inicio de sesión y no se pueden abrir ni correr
 * desde Apps Script, así que esto es solo contexto de apoyo, no verificación del circuito.
 */
function enriquecerEnlaceSimulacion(url) {
  var info = { accesible: false, titulo: '', descripcion: '', miniaturaUrl: '', nota: '' };
  try {
    if (!url || url.toLowerCase().indexOf('http') !== 0) {
      info.nota = 'Enlace no válido.';
      return info;
    }
    var resp = UrlFetchApp.fetch(url, { method: 'get', muteHttpExceptions: true, followRedirects: true });
    var code = resp.getResponseCode();
    if (code < 200 || code >= 400) {
      info.nota = 'El enlace no abrió (HTTP ' + code + '). Puede ser privado o exigir inicio de sesión.';
      return info;
    }
    var html = '';
    try { html = resp.getContentText().substring(0, 12000); } catch(eT) { html = ''; }
    if (!html) {
      info.nota = 'El enlace abrió pero no devolvió texto legible.';
      return info;
    }
    var bajo = html.toLowerCase();
    if (bajo.indexOf('login') !== -1 && bajo.indexOf('og:title') === -1 && html.length < 3000) {
      info.nota = 'El enlace parece exigir inicio de sesión. No se pudo ver el contenido.';
      return info;
    }
    info.titulo = extraerMeta(html, 'og:title') || (function() { var t = html.match(/<title[^>]*>([^<]*)<\/title>/i); return t ? t[1] : ''; })();
    info.descripcion = extraerMeta(html, 'og:description') || extraerMeta(html, 'description');
    info.miniaturaUrl = extraerMeta(html, 'og:image');
    info.accesible = !!(info.titulo || info.descripcion || info.miniaturaUrl);
    if (!info.accesible) {
      info.nota = 'El enlace abrió pero no trajo datos públicos para revisar.';
    }
  } catch(e) {
    info.nota = 'No se pudo leer el enlace: ' + e.message;
    Logger.log('Enriquecer enlace falló: ' + e.message);
  }
  return info;
}

/**
 * Descarga una miniatura pública (og:image) para análisis visual. Máximo 2 MB.
 */
function descargarMiniaturaComoImagen(urlMiniatura) {
  try {
    if (!urlMiniatura || urlMiniatura.toLowerCase().indexOf('http') !== 0) return null;
    var resp = UrlFetchApp.fetch(urlMiniatura, { method: 'get', muteHttpExceptions: true, followRedirects: true });
    if (resp.getResponseCode() < 200 || resp.getResponseCode() >= 400) return null;
    var blob = resp.getBlob();
    var bytes = blob.getBytes();
    if (!bytes || bytes.length === 0 || bytes.length > 2097152) return null;
    var mime = blob.getContentType() || 'image/png';
    if (mime.toLowerCase().indexOf('image/') !== 0) return null;
    return { titulo: 'miniatura del enlace', mimeType: mime, base64: Utilities.base64Encode(bytes) };
  } catch(e) {
    Logger.log('Miniatura no descargable: ' + e.message);
    return null;
  }
}

/**
 * Obtiene las entregas de los estudiantes para una tarea dada
 * e inspecciona el contenido de los archivos adjuntos (Docs, .ipynb, imágenes, etc.)
 */
function obtenerEntregasDetalladas(courseId, courseWorkId) {
  try {
    // 1. Mapear usuarios (IDs -> Nombres completos de estudiantes activos con paginación)
    var mapaEstudiantes = {};
    var idsActivos = {};
    try {
      var pageToken = null;
      do {
        var roster = Classroom.Courses.Students.list(courseId, { 
          pageSize: 100,
          pageToken: pageToken
        });
        if (roster.students) {
          roster.students.forEach(function(st) {
            idsActivos[st.userId] = true;
            mapaEstudiantes[st.userId] = {
              nombre: st.profile.name.fullName,
              nombrePila: st.profile.name.givenName || st.profile.name.fullName.split(' ')[0],
              apellido: st.profile.name.familyName || st.profile.name.fullName.split(' ').slice(1).join(' '),
              email: st.profile.emailAddress,
              foto: st.profile.photoUrl,
              matriculado: true
            };
          });
        }
        pageToken = roster.nextPageToken;
      } while (pageToken);
    } catch(e) {
      Logger.log("No se pudo obtener roster completo: " + e.message);
    }
    
    // 2. Obtener entregas
    var subsResponse = Classroom.Courses.CourseWork.StudentSubmissions.list(courseId, courseWorkId, {
      pageSize: 100
    });
    
    var submissions = subsResponse.studentSubmissions || [];
    var entregasProcesadas = [];
    
    submissions.forEach(function(sub) {
      var esMatriculado = !!idsActivos[sub.userId];
      var perfil = mapaEstudiantes[sub.userId];
      
      // Si el estudiante no está en la lista activa (ej: fue cambiado de grupo o retirado),
      // consultar su nombre real directamente en la API de Classroom
      if (!perfil) {
        var nombreReal = 'Estudiante (' + sub.userId + ')';
        var nombrePilaReal = '';
        var apellidoReal = '';
        var emailReal = '';
        var fotoReal = '';
        try {
          var uProfile = Classroom.UserProfiles.get(sub.userId);
          if (uProfile && uProfile.name) {
            nombreReal = (uProfile.name.fullName || ('Usuario ' + sub.userId)) + ' [Desvinculado / Otro Grupo]';
            nombrePilaReal = uProfile.name.givenName || '';
            apellidoReal = uProfile.name.familyName || '';
            emailReal = uProfile.emailAddress || '';
            fotoReal = uProfile.photoUrl || '';
          }
        } catch(errProf) {
          Logger.log("No se pudo consultar perfil de " + sub.userId + ": " + errProf.message);
        }
        
        perfil = {
          nombre: nombreReal,
          nombrePila: nombrePilaReal,
          apellido: apellidoReal,
          email: emailReal,
          foto: fotoReal,
          matriculado: false
        };
        mapaEstudiantes[sub.userId] = perfil;
      }
      
      var estado = sub.state; // NEW, CREATED, TURNED_IN, RETURNED
      var notaBorrador = sub.draftGrade || null;
      var notaAsignada = sub.assignedGrade || null;
      
      // Inspeccionar adjuntos
      var archivos = [];
      var contenidoTexto = '';
      var tipoContenido = 'none';
      var imagenIds = [];
      var driveLinks = [];
      var enlacesPublicos = [];
      
      if (sub.assignmentSubmission && sub.assignmentSubmission.attachments) {
        sub.assignmentSubmission.attachments.forEach(function(att) {
          if (att.driveFile) {
            var f = att.driveFile;
            var fileData = {
              id: f.id,
              titulo: f.title,
              enlace: f.alternateLink,
              tipo: 'drive'
            };
            
            // Intentar extraer contenido para la IA
            try {
              var mimePrevio = '';
              try { mimePrevio = DriveApp.getFileById(f.id).getBlob().getContentType() || ''; } catch(eMime) {}
              if (esArchivoImagen(f.title, mimePrevio)) {
                // Imagen (foto o captura de Tinkercad): no se manda el peso al panel,
                // solo se guarda el id para leerla al calificar con visión.
                fileData.tipo = 'imagen';
                fileData.mimeType = mimePrevio;
                tipoContenido = (tipoContenido === 'none' || tipoContenido === 'imagen') ? 'imagen' : tipoContenido + '+imagen';
                imagenIds.push({ id: f.id, titulo: f.title });
                contenidoTexto += '\n[Imagen adjunta: ' + f.title + ' - se revisará a simple vista en la calificación]';
              } else if (f.title.toLowerCase().indexOf('.ipynb') !== -1) {
                // Cuaderno Colab
                fileData.tipo = 'colab';
                tipoContenido = 'colab';
                var rawJson = DriveApp.getFileById(f.id).getBlob().getDataAsString();
                var nb = JSON.parse(rawJson);
                var celdasCodigo = (nb.cells || []).filter(function(c) { return c.cell_type === 'code'; });
                var extracto = celdasCodigo.map(function(c, idx) {
                  var src = Array.isArray(c.source) ? c.source.join('') : (c.source || '');
                  var outs = (c.outputs || []).map(function(o) {
                    if (o.text) return Array.isArray(o.text) ? o.text.join('') : o.text;
                    if (o.evalue) return 'Error: ' + o.evalue;
                    return '';
                  }).join('\n');
                  return 'Celda ' + (idx + 1) + ':\n' + src + (outs ? '\nSalida:\n' + outs : '');
                }).join('\n---\n');
                
                contenidoTexto += '\n[Cuaderno Colab: ' + f.title + ']\n' + extracto;
              } else if (f.title.toLowerCase().indexOf('.brd') !== -1) {
                // Circuito Tinkercad / EAGLE (.brd)
                fileData.tipo = 'circuito_brd';
                tipoContenido = (tipoContenido === 'none') ? 'circuito_brd' : tipoContenido + '+brd';
                try {
                  var rawBrd = DriveApp.getFileById(f.id).getBlob().getDataAsString();
                  var extractoBrd = extraerCircuitoBrd(rawBrd, f.title);
                  contenidoTexto += '\n' + extractoBrd;
                } catch(eBrd) {
                  contenidoTexto += '\n[Archivo .brd: ' + f.title + ' - no se pudo extraer el esquema]';
                }
              } else {
                // Intentar leer como Google Doc
                try {
                  var doc = DocumentApp.openById(f.id);
                  fileData.tipo = 'doc';
                  tipoContenido = 'doc';
                  var textoDoc = doc.getBody().getText();
                  contenidoTexto += '\n[Documento Google Docs: ' + f.title + ']\n' + textoDoc.substring(0, 4000);
                } catch(docErr) {
                  // Si no es Google Doc, leer texto plano (o .brd no nombrado)
                  var blobText = DriveApp.getFileById(f.id).getBlob().getDataAsString();
                  if (f.title.toLowerCase().indexOf('.brd') !== -1 || (blobText && blobText.indexOf('<eagle') !== -1)) {
                    fileData.tipo = 'circuito_brd';
                    tipoContenido = (tipoContenido === 'none') ? 'circuito_brd' : tipoContenido + '+brd';
                    contenidoTexto += '\n' + extraerCircuitoBrd(blobText, f.title);
                  } else if (blobText && blobText.length < 5000) {
                    contenidoTexto += '\n[Archivo: ' + f.title + ']\n' + blobText;
                    tipoContenido = 'text';
                  }
                }
              }
            } catch(readErr) {
              Logger.log("No se pudo leer archivo " + f.id + ": " + readErr.message);
            }
            
            archivos.push(fileData);
          } else if (att.link) {
            var urlLink = att.link.url || '';
            var esTinkercad = urlLink.toLowerCase().indexOf('tinkercad') !== -1;
            var esDrive = !esTinkercad && esEnlaceDrive(urlLink);
            archivos.push({
              id: '',
              titulo: att.link.title || urlLink,
              enlace: urlLink,
              tipo: esTinkercad ? 'tinkercad' : (esDrive ? 'drivelink' : 'link')
            });
            if (esTinkercad) {
              contenidoTexto += '\n[Enlace de simulación entregado]: ' + urlLink + ' (se intentará leer datos públicos de apoyo; la simulación no se puede abrir ni probar, pida captura si falta)';
            } else if (esDrive) {
              driveLinks.push({ url: urlLink, titulo: att.link.title || urlLink });
              contenidoTexto += '\n[Enlace de Drive entregado]: ' + urlLink + ' (se abrirá e intentará leer al calificar)';
            } else {
              enlacesPublicos.push({ url: urlLink, titulo: att.link.title || urlLink });
              contenidoTexto += '\n[Enlace entregado]: ' + urlLink + ' (se abrirá e intentará leer al calificar)';
            }
            if (tipoContenido === 'none') tipoContenido = esTinkercad ? 'tinkercad' : (esDrive ? 'drivelink' : 'link');
          }
        });
      }
      
      // Si fue respuesta corta textual directa en Classroom
      if (sub.shortAnswerSubmission && sub.shortAnswerSubmission.answer) {
        contenidoTexto += '\n[Respuesta corta]: ' + sub.shortAnswerSubmission.answer;
        tipoContenido = 'shortAnswer';
      }
      
      entregasProcesadas.push({
        submissionId: sub.id,
        userId: sub.userId,
        nombre: perfil.nombre,
        nombrePila: perfil.nombrePila || '',
        apellido: perfil.apellido || '',
        email: perfil.email,
        foto: perfil.foto,
        estado: estado,
        entregado: (estado === 'TURNED_IN' || estado === 'RETURNED' || archivos.length > 0),
        notaBorrador: notaBorrador,
        notaAsignada: notaAsignada,
        matriculado: esMatriculado,
        archivos: archivos,
        tipoContenido: tipoContenido,
        contenidoTexto: contenidoTexto.trim(),
        imagenIds: imagenIds,
        tieneImagen: imagenIds.length > 0,
        driveLinks: driveLinks,
        tieneDriveLink: driveLinks.length > 0,
        enlacesPublicos: enlacesPublicos,
        tieneEnlacePublico: enlacesPublicos.length > 0,
        // Campos que llenará la IA
        calificacionSugerida: notaBorrador || null,
        nivel1290: '',
        comentarioIA: '',
        evaluado: false
      });
    });
    
    // Ordenar alfabéticamente por nombre de estudiante
    entregasProcesadas.sort(function(a, b) {
      return a.nombre.localeCompare(b.nombre);
    });
    
    return { success: true, entregas: entregasProcesadas };
  } catch(error) {
    return { success: false, error: 'Error al obtener entregas: ' + error.message };
  }
}

// --------------------------------------------------------------------------
// 3. MOTOR DE EVALUACIÓN CON IA (GEMINI API)
// --------------------------------------------------------------------------

/**
 * Evalúa un lote de entregas. Si la IA falla con un estudiante, continúa con los demás
 * y reporta el fallo al final. Nunca asigna 1.0 por un error técnico.
 * Prelación: lo manual que escriba el docente va por encima de lo traído de Classroom.
 * Techo: en trabajos de seguimiento guiado, la nota final se recorta al techo indicado.
 */
function evaluarLoteEstudiantes(apiKey, actividadTitulo, consignaManual, entregasAEnviar, contextoTarea, techoNota) {
  // Compatibilidad con llamadas anteriores de 4 argumentos.
  if (!entregasAEnviar && contextoTarea && Object.prototype.toString.call(contextoTarea) === '[object Array]') {
    entregasAEnviar = contextoTarea;
    contextoTarea = {};
  }
  contextoTarea = contextoTarea || {};
  // El techo puede venir como sexto argumento o dentro del contexto.
  var techo = normalizarTecho(techoNota !== undefined ? techoNota : contextoTarea.techo);
  var props = PropertiesService.getUserProperties();
  var key = apiKey || props.getProperty('GEMINI_API_KEY');
  
  if (!key) {
    return { success: false, error: 'No se ha configurado la API Key de Gemini. Por favor ingrésala arriba.' };
  }

  var modeloEnUso = props.getProperty('GEMINI_MODEL_NAME') || MODELO_POR_DEFECTO;
  var manualLimpio = (consignaManual || '').trim();
  var instruccionesAuto = (contextoTarea.instrucciones || '').substring(0, 3000);
  var rubricaAuto = (contextoTarea.rubricaTexto || '').substring(0, 2500);
  var fuenteCriterios = manualLimpio ? 'manual' : ((instruccionesAuto.trim() !== '' || rubricaAuto.trim() !== '') ? 'classroom' : 'generico');
  
  var resultados = [];
  var fallos = [];
  
  for (var i = 0; i < entregasAEnviar.length; i++) {
    var e = entregasAEnviar[i];
    var primerNombre = e.nombre ? e.nombre.split(' ')[0] : 'estudiante';
    // Formatear primer nombre (ej: "MATEO" -> "Mateo")
    primerNombre = primerNombre.charAt(0).toUpperCase() + primerNombre.slice(1).toLowerCase();
    
    var tieneTexto = (e.contenidoTexto && e.contenidoTexto.trim() !== '');
    var tieneImagen = !!(e.tieneImagen || (e.imagenIds && e.imagenIds.length > 0));
    var tieneContenido = tieneTexto || tieneImagen;
    var marcoEntregado = (e.estado === 'TURNED_IN' || e.estado === 'RETURNED');
    
    // -----------------------------------------------------------------------
    // REGLA 1: Marcó la tarea como entregada pero SIN archivos adjuntos
    // Nota = 1.0 (Bajo), mensaje recordándole que olvidó adjuntar y puede volver a hacerlo
    // -----------------------------------------------------------------------
    if (marcoEntregado && !tieneContenido) {
      resultados.push({
        submissionId: e.submissionId,
        nota: 1.0,
        nivel: 'Bajo',
        diagnostico: 'Marcó la tarea como entregada pero sin ningún archivo adjunto.',
        comentario: '¡Hola ' + primerNombre + '! Al parecer marcaste la tarea, pero no se adjuntó ningún archivo. Vuelve a subir tu trabajo para poder revisarlo y ponerte la nota. Aún puedes entregarlo.'
      });
      continue;
    }
    
    // Sin entrega y sin archivo
    if (!marcoEntregado && !tieneContenido) {
      resultados.push({
        submissionId: e.submissionId,
        nota: 1.0,
        nivel: 'Bajo',
        diagnostico: 'No se evidencia entrega de la actividad ni archivos adjuntos.',
        comentario: '¡Hola ' + primerNombre + '! No veo tu trabajo entregado. Ponte al día y súbelo en Classroom para poder calificarte.'
      });
      continue;
    }
    
    // -----------------------------------------------------------------------
    // REGLA 2: Tiene archivo adjunto (sea que haya marcado o no "Entregar")
    // Se evalúa con la IA. Si no marcó "Entregar", se le suma el llamado de atención
    // -----------------------------------------------------------------------
    try {
      // Si hay imágenes, se leen de Drive en este momento para análisis visual.
      var vision = leerImagenesParaIA(e.imagenIds || []);
      var textoParaIA = e.contenidoTexto || '';
      if (vision.aviso) {
        textoParaIA += '\n[Nota sobre imágenes]: ' + vision.aviso;
      }
      // Si hay enlaces de Drive, se ABREN e intentan leer (Docs, texto, imágenes).
      // Nada de respuesta genérica: lo que se pudo leer va a la IA y lo que no,
      // queda avisado para pedir revisión de permisos.
      if (e.driveLinks && e.driveLinks.length > 0) {
        try {
          var resDrive = resolverEnlacesDrive(e.driveLinks);
          if (resDrive.texto) {
            textoParaIA += '\n' + resDrive.texto;
          }
          if (resDrive.imagenes && resDrive.imagenes.length > 0) {
            for (var di = 0; di < resDrive.imagenes.length && vision.imagenes.length < 2; di++) {
              vision.imagenes.push(resDrive.imagenes[di]);
            }
          }
          if (resDrive.aviso) {
            textoParaIA += '\n[Nota sobre enlaces de Drive]: ' + resDrive.aviso;
          }
        } catch (eDrive) {
          textoParaIA += '\n[Nota sobre enlaces de Drive]: no se pudieron revisar en este intento.';
          Logger.log('Resolver Drive falló para ' + e.nombre + ': ' + eDrive.message);
        }
      }
      // Si hay enlaces públicos (Colab, código, páginas), se ABREN e intentan leer.
      // Un enlace público SÍ se puede leer: su contenido va a la IA y solo si de
      // verdad no abre se deja aviso puntual, sin regaños ni pedidos genéricos.
      if (e.enlacesPublicos && e.enlacesPublicos.length > 0) {
        try {
          var resPub = resolverEnlacesPublicos(e.enlacesPublicos);
          if (resPub.texto) {
            textoParaIA += '\n' + resPub.texto;
          }
          if (resPub.imagenes && resPub.imagenes.length > 0) {
            for (var pi = 0; pi < resPub.imagenes.length && vision.imagenes.length < 2; pi++) {
              vision.imagenes.push(resPub.imagenes[pi]);
            }
          }
          if (resPub.aviso) {
            textoParaIA += '\n[Nota sobre enlaces entregados]: ' + resPub.aviso;
          }
        } catch (ePub) {
          textoParaIA += '\n[Nota sobre enlaces entregados]: no se pudieron revisar en este intento.';
          Logger.log('Resolver enlaces falló para ' + e.nombre + ': ' + ePub.message);
        }
      }
      // Si hay enlaces de simulación (Tinkercad u otra), se intenta leer datos públicos de apoyo.
      // La simulación interactiva no se puede abrir ni correr: solo es contexto, no verificación.
      var urlsSimulacion = [];
      try {
        (e.archivos || []).forEach(function(a) {
          if (a && a.enlace && (a.tipo === 'tinkercad' || esUrlSimulacion(a.enlace))) {
            if (urlsSimulacion.indexOf(a.enlace) === -1) urlsSimulacion.push(a.enlace);
          }
        });
      } catch(eLinks) {}
      if (urlsSimulacion.length > 0) {
        try {
          var infoSim = enriquecerEnlaceSimulacion(urlsSimulacion[0]);
          if (infoSim.accesible) {
            textoParaIA += '\n[Datos públicos del enlace de simulación]: ' +
              (infoSim.titulo ? 'Título: ' + infoSim.titulo + '. ' : '') +
              (infoSim.descripcion ? infoSim.descripcion.substring(0, 600) : '');
            if (vision.imagenes.length === 0 && infoSim.miniaturaUrl) {
              var mini = descargarMiniaturaComoImagen(infoSim.miniaturaUrl);
              if (mini) {
                vision.imagenes.push(mini);
                textoParaIA += '\n[Nota]: se adjuntó la miniatura pública del enlace para revisión a simple vista.';
              }
            }
          } else if (infoSim.nota) {
            textoParaIA += '\n[Nota sobre el enlace de simulación]: ' + infoSim.nota;
          }
        } catch(eEnr) {
          Logger.log('Enriquecer simulación falló para ' + e.nombre + ': ' + eEnr.message);
        }
      }
      var evaluacion = consultarGemini(key, actividadTitulo, manualLimpio, e.nombre, textoParaIA, {
        instrucciones: instruccionesAuto,
        rubricaTexto: rubricaAuto,
        tieneRubrica: !!contextoTarea.tieneRubrica,
        tieneInstrucciones: !!(instruccionesAuto && instruccionesAuto.trim() !== ''),
        materiales: (contextoTarea.materiales || '').substring(0, 1500),
        puntosMaximos: contextoTarea.puntosMaximos || 5.0,
        fuenteCriterios: fuenteCriterios,
        techo: techo,
        tieneImagen: vision.imagenes.length > 0
      }, vision.imagenes);
      var comentarioFinal = evaluacion.comentario;
      var diagFinal = evaluacion.diagnostico;
      var notaFinal = evaluacion.nota;
      var nivelFinal = evaluacion.nivel;
      var notaIARaw = evaluacion.nota;
      var conTecho = false;
      if (techo < 5.0) {
        var recorte = aplicarTecho(evaluacion.nota, techo);
        notaFinal = recorte.notaFinal;
        nivelFinal = recorte.nivelFinal;
        conTecho = recorte.recortada;
        if (recorte.recortada) {
          diagFinal = '[Techo seguimiento ' + recorte.techo.toFixed(1) + ': IA sugirió ' + recorte.notaIA.toFixed(1) + '] ' + diagFinal;
        }
      }
      
      // Si tenía archivo pero no había marcado "Entregar"
      if (!marcoEntregado && tieneContenido) {
        diagFinal = '[Archivo evaluado - Pendiente marcar como entregada] ' + diagFinal;
        comentarioFinal += ' (Recuerda darle clic en "Entregar" en Classroom para que no quede pendiente).';
      }
      
      resultados.push({
        submissionId: e.submissionId,
        nota: notaFinal,
        nivel: nivelFinal,
        diagnostico: diagFinal,
        comentario: comentarioFinal,
        fuenteCriterios: fuenteCriterios,
        notaIA: notaIARaw,
        conTecho: conTecho,
        techo: techo
      });
    } catch(err) {
      Logger.log("Error evaluando a " + e.nombre + ": " + err.message);
      var errMsg = err.message || '';
      // No se detiene el lote. Se registra el fallo para aviso manual del docente.
      fallos.push({ submissionId: e.submissionId, nombre: e.nombre, error: errMsg });
    }
    
    // Pequeña pausa para no saturar la cuota gratuita (más larga si hubo visión).
    Utilities.sleep(vision.imagenes.length > 0 ? 1000 : 400);
  }
  
  return { success: true, resultados: resultados, fallos: fallos, modeloEnUso: modeloEnUso, fuenteCriterios: fuenteCriterios, techoAplicado: techo };
}

/**
 * Consulta puntual a Gemini para evaluar a un estudiante bajo el Decreto 1290.
 * Prelación: criterios manuales del docente > instrucciones de Classroom > rúbrica referencial.
 */
function consultarGemini(apiKey, tituloTarea, consignaManual, nombreEstudiante, contenidoEntrega, contexto, imagenes) {
  var props = PropertiesService.getUserProperties();
  var key = apiKey || props.getProperty('GEMINI_API_KEY');
  
  if (!key) {
    throw new Error("No se ha configurado la API Key de Gemini.");
  }
  contexto = contexto || {};
  imagenes = imagenes || [];
  var manual = (consignaManual || '').trim();
  var instruccionesClassroom = (contexto.instrucciones || '').substring(0, 3000);
  var rubricaRef = (contexto.rubricaTexto || '').substring(0, 2500);
  var materialesCtx = (contexto.materiales || '').substring(0, 1200);
  var puntosMax = contexto.puntosMaximos || 5.0;
  var fuente = contexto.fuenteCriterios || (manual ? 'manual' : ((instruccionesClassroom.trim() !== '' || rubricaRef.trim() !== '') ? 'classroom' : 'generico'));
  var techoPrompt = normalizarTecho(contexto.techo);
  var reglaPrelacion = manual
    ? "REGLA DE PRELACIÓN: el docente escribió criterios manuales. Úsalos como base principal de la nota. Las instrucciones de Classroom y la rúbrica solo sirven de contexto secundario."
    : "No hay criterios manuales. Usa las instrucciones de Classroom como base. Si hay rúbrica, úsala solo como referencia no vinculante.";
  if (techoPrompt < 5.0) {
    reglaPrelacion += " TECHO DE SEGUIMIENTO: es un trabajo guiado paso a paso, la nota máxima es " + techoPrompt.toFixed(1) + ". Califica con exigencia acorde y no superes ese techo en la nota que propongas.";
  }
  
  var prompt = 
    "Eres un docente de Tecnología e Informática que ayuda a calificar trabajos de Classroom bajo el Decreto 1290 (Superior: 4.6 a 5.0, Alto: 4.0 a 4.5, Básico: 3.0 a 3.9, Bajo: 1.0 a 2.9).\n\n" +
    "ACTIVIDAD: " + (tituloTarea || 'Actividad de clase') + " (Puntos Classroom: " + puntosMax + ", se califica en escala 1.0 a 5.0" + (techoPrompt < 5.0 ? ", techo de seguimiento: " + techoPrompt.toFixed(1) : "") + ").\n\n" +
    "INSTRUCCIONES PUBLICADAS EN CLASSROOM:\n" + (instruccionesClassroom.trim() !== '' ? instruccionesClassroom : 'Sin instrucciones publicadas.') + "\n\n" +
    (materialesCtx.trim() !== '' ? "MATERIALES DE LA TAREA:\n" + materialesCtx + "\n\n" : "") +
    "RÚBRICA ASOCIADA EN CLASSROOM (solo referencia, no vinculante):\n" + (rubricaRef.trim() !== '' ? rubricaRef : 'Sin rúbrica asociada.') + "\n\n" +
    "CRITERIOS MANUALES DEL DOCENTE (tienen prelación si existen):\n" + (manual !== '' ? manual : 'Sin criterios manuales.') + "\n\n" +
    reglaPrelacion + "\n\n" +
    (imagenes.length > 0
      ? "HAY " + imagenes.length + " IMAGEN" + (imagenes.length > 1 ? "ES" : "") + " ADJUNTA" + (imagenes.length > 1 ? "S" : "") + " (foto, captura o imagen abierta desde un enlace). Mírala" + (imagenes.length > 1 ? "s" : "") + " con cuidado.\n\n"
      : "No hay imágenes adjuntas. Si ves contenido abierto desde enlaces (código, documento o página incluida arriba), califícalo como parte de la entrega. Solo las simulaciones interactivas no se pueden correr: de esas usa los datos de apoyo incluidos.\n\n") +
    "REGLAS SOBRE ENLACES (obligatorias): los enlaces públicos entregados YA fueron abiertos cuando fue posible y su contenido está incluido arriba: califícalo con normalidad. JAMÁS digas que no puedes abrir enlaces si arriba hay contenido de un enlace. JAMÁS regañes al estudiante por entregar un enlace ni le exijas reenviar en otro formato por defecto. Solo si arriba dice expresamente que un enlace no abrió Y no hay otro contenido para calificar, agrega al final del comentario UNA frase amable pidiendo que revise el permiso del enlace o adjunte el código o una captura la próxima vez.\n\n" +
    "ESTUDIANTE: " + nombreEstudiante + "\n\n" +
    "CONTENIDO ENTREGADO POR EL ESTUDIANTE (texto):\n" +
    (contenidoEntrega ? contenidoEntrega.substring(0, 4500) : 'Sin texto, solo imagen o enlace') + "\n\n" +
    "INSTRUCCIONES DE EVALUACIÓN:\n" +
    "1. Revisa el trabajo: si funciona, si cumple lo pedido y si se entiende.\n" +
    "2. Si hay esquema de circuito Tinkercad / EAGLE (.brd) incluido en el texto: revisa la lista de COMPONENTES (valores en ohmios, voltajes, tipos) y las CONEXIONES (netlist de cables). Evalúa si el circuito está bien armado según lo pedido (ej: polaridad de pilas y LEDs, resistencias de protección adecuadas, circuito cerrado en serie o paralelo según el reto). Si hay imagen de un circuito (Tinkercad o foto real): describe en palabras sencillas lo que se ve a simple vista y califica conexiones visibles.\n" +
    "3. Si hay contenido abierto desde un enlace de Drive (documento o texto incluido arriba), califícalo como parte de la entrega, nunca lo ignores ni respondas en genérico. Si arriba dice que el enlace no se pudo abrir, dilo en palabras sencillas y pide al estudiante que revise los permisos para compartir, pero califica lo demás que sí se vea.\n" +
    "4. Pon una nota de 1.0 a 5.0 (con un decimal) y su nivel fijo: Bajo 1.0 a 2.9, Básico 3.0 a 3.9, Alto 4.0 a 4.5, Superior 4.6 a 5.0. El techo no cambia estos rangos.\n" +
    "5. Para el campo diagnostico escribe un resumen corto para el docente, con palabras normales. Si revisaste imagen, di qué se vio bien y qué conexión falló. Si leíste un enlace de Drive, di qué contenía.\n" +
    "6. Para el campo comentario escribe el mensaje para el estudiante: máximo 3 líneas cortas, con palabras sencillas de todos los días. Empieza con '¡Hola [Nombre]!'. Di una cosa buena y una por mejorar con un ejemplo claro. No uses palabras difíciles como sintaxis, lógica, particularidades, pedagógico o retroalimentación. Di en cambio 'error en el código', 'se entiende bien', 'te faltó', 'el cable va en...'. Frases cortas que un joven de 13 a 17 años entienda a la primera.\n\n" +
    "Responde EXCLUSIVAMENTE con este formato JSON:\n" +
    "{\n" +
    '  "nota": 4.8,\n' +
    '  "nivel": "Superior",\n' +
    '  "diagnostico": "Resumen corto para el docente, en palabras sencillas",\n' +
    '  "comentario": "Mensaje corto para el estudiante, en palabras sencillas"\n' +
    "}";
    
  var baseEndpoint = props.getProperty('GEMINI_WORKING_ENDPOINT');
  var modeloGuardado = props.getProperty('GEMINI_MODEL_NAME') || MODELO_POR_DEFECTO;
  // Si quedó un endpoint retirado, se redescubre una vez. Si no hay éxito, se usa el valor por defecto
  // y el error real se muestra al docente para aviso manual, sin cambio silencioso posterior.
  if (!baseEndpoint || esEndpointObsoleto(baseEndpoint)) {
    var disc = autoDescubrirEndpoint(key);
    if (disc.success) {
      baseEndpoint = disc.endpoint;
      modeloGuardado = disc.model;
    } else {
      baseEndpoint = ENDPOINT_POR_DEFECTO;
    }
  }
  
  // Multimodal: texto más hasta 2 imágenes (inlineData) para revisión a simple vista.
  var partesFinales = [{ text: prompt }];
  imagenes.forEach(function(img) {
    if (img && img.base64) {
      partesFinales.push({ inlineData: { mimeType: img.mimeType || 'image/png', data: img.base64 } });
    }
  });

  var payload = {
    contents: [
      {
        parts: partesFinales
      }
    ],
    generationConfig: {
      temperature: 0.2
    }
  };
  
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  
  var url = baseEndpoint + "?key=" + key;
  var response = UrlFetchApp.fetch(url, options);
  var statusCode = response.getResponseCode();
  var rawText = response.getContentText();
  var json = {};
  
  try {
    json = JSON.parse(rawText);
  } catch(e) {
    throw new Error("Respuesta no JSON de Gemini (HTTP " + statusCode + "): " + rawText.substring(0, 300));
  }
  
  // Si el modelo guardado fue retirado, avisar para elección manual. No cambiar en silencio.
  if (json.error && (statusCode === 400 || statusCode === 404 || json.error.message.indexOf("not found") !== -1 || json.error.message.indexOf("not supported") !== -1 || json.error.message.indexOf("no longer available") !== -1 || json.error.message.indexOf("not found for API version") !== -1)) {
    throw new Error("El modelo " + modeloGuardado + " ya no responde en Google (" + statusCode + "): " + json.error.message + ". Actualice la lista con el botón Actualizar y escoja otro modelo de la lista real.");
  }

  if (json.error) {
    var errorMsg = json.error.message || JSON.stringify(json.error);
    throw new Error("Google Gemini (" + statusCode + "): " + errorMsg);
  }
  
  if (!json.candidates || json.candidates.length === 0) {
    throw new Error("Gemini no devolvió candidatos de respuesta (HTTP " + statusCode + ")");
  }
  
  var firstCand = json.candidates[0];
  if (firstCand.finishReason && firstCand.finishReason === "SAFETY") {
    throw new Error("La entrega fue bloqueada por filtros de seguridad de Gemini");
  }
  
  // Extraer texto de todas las partes posibles
  var partes = (firstCand.content && firstCand.content.parts) ? firstCand.content.parts : [];
  var textoRespuesta = "";
  for (var p = 0; p < partes.length; p++) {
    if (partes[p].text) {
      textoRespuesta += partes[p].text + "\n";
    }
  }
  textoRespuesta = textoRespuesta.trim();
  
  if (!textoRespuesta) {
    throw new Error("Gemini devolvió una respuesta vacía. FinishReason: " + (firstCand.finishReason || 'N/A'));
  }
  
  // Parsear JSON con el motor tolerante a fallos
  var parsed = parsearRespuestaGemini(textoRespuesta);
  if (!parsed) {
    Logger.log("Texto devuelto por Gemini que no se pudo parsear:\n" + textoRespuesta);
    throw new Error("No se pudo interpretar el formato JSON devuelto por Gemini:\n" + textoRespuesta.substring(0, 200));
  }
  
  return {
    nota: Number(parsed.nota) || 4.0,
    nivel: parsed.nivel || 'Alto',
    diagnostico: parsed.diagnostico || '',
    comentario: parsed.comentario || ''
  };
}

/**
 * Parsea respuestas JSON de Gemini con tolerancia a markdown, comillas y saltos de línea
 */
function parsearRespuestaGemini(rawText) {
  if (!rawText) return null;
  
  // 1. Limpieza básica de bloques markdown
  var cleaned = rawText.replace(/```json/gi, '').replace(/```/g, '').trim();
  
  // 2. Extraer el bloque JSON más externo {...}
  var start = cleaned.indexOf('{');
  var end = cleaned.lastIndexOf('}');
  if (start !== -1 && end !== -1 && end > start) {
    var jsonStr = cleaned.substring(start, end + 1);
    
    // Intento 1: parseo directo
    try {
      var obj = JSON.parse(jsonStr);
      if (obj && (obj.nota !== undefined || obj.calificacion !== undefined)) {
        return normalizarObjetoEvaluacion(obj);
      }
    } catch(e1) {}
    
    // Intento 2: sanitizando saltos de línea literales dentro de strings
    try {
      var sanitizado = jsonStr.replace(/\r?\n/g, "\\n");
      var obj2 = JSON.parse(sanitizado);
      if (obj2) return normalizarObjetoEvaluacion(obj2);
    } catch(e2) {}
  }

  // 3. Extracción robusta con Expresiones Regulares campo por campo (acepta coma o punto decimal)
  var notaMatch = rawText.match(/"?nota"?\s*:\s*([0-9]+(?:[.,][0-9]+)?)/i);
  var nivelMatch = rawText.match(/"?nivel"?\s*:\s*"([^"\r\n]+)"/i);
  var diagMatch = rawText.match(/"?diagnostico"?\s*:\s*"([\s\S]*?)"(?=\s*,\s*"?comentario"?|\s*\})/i);
  var commMatch = rawText.match(/"?comentario"?\s*:\s*"([\s\S]*?)"(?=\s*\})/i);

  if (notaMatch) {
    return {
      nota: parseFloat(String(notaMatch[1]).replace(',', '.')),
      nivel: nivelMatch ? nivelMatch[1] : 'Alto',
      diagnostico: diagMatch ? diagMatch[1].replace(/\\n/g, ' ').replace(/"/g, '') : '',
      comentario: commMatch ? commMatch[1].replace(/\\n/g, '\n').replace(/\\"/g, '"') : ''
    };
  }

  return null;
}

function normalizarObjetoEvaluacion(obj) {
  var notaRaw = obj.nota || obj.calificacion || obj.score || 4.0;
  var nota = Number(String(notaRaw).trim().replace(',', '.'));
  var nivel = obj.nivel || obj.desempeno || 'Alto';
  var diag = obj.diagnostico || obj.resumen || '';
  var comm = obj.comentario || obj.retroalimentacion || obj.feedback || '';
  return {
    nota: nota,
    nivel: nivel,
    diagnostico: diag,
    comentario: comm
  };
}

// --------------------------------------------------------------------------
// 4. GUARDAR NOTAS EN CLASSROOM (ESTADO BORRADOR) + HOJA DE NOTAS
// --------------------------------------------------------------------------
//
// Nota del docente: todas sus tareas valen 5, así que la nota se envía tal cual,
// como número con punto decimal y máximo 2 decimales (lo que acepta Classroom).
// Límites de la API (documentación oficial de Google, no del calificador):
// 1. patch solo acepta draftGrade y assignedGrade. No existe endpoint de comentarios.
// 2. patch solo funciona en tareas creadas por el mismo proyecto de la app.
//    En tareas creadas a mano, Google responde PERMISSION_DENIED.

/**
 * Convierte cualquier formato de nota a número con punto decimal y 2 decimales.
 * Acepta coma decimal ("4,5") y la pasa a punto (4.5), que es lo que exige el JSON de la API.
 */
function normalizarNotaEnvio(valor) {
  if (valor === null || valor === undefined || valor === '') return null;
  var texto = String(valor).trim().replace(',', '.');
  var n = Number(texto);
  if (isNaN(n) || n < 0) return null;
  return Math.round(n * 100) / 100;
}

/**
 * Guarda las notas en Google Classroom como borrador y crea/actualiza la hoja
 * de notas con notas y comentarios para revisión.
 * Si soloHoja es true, no intenta el patch y solo genera la hoja.
 */
function guardarNotasEnClassroom(courseId, courseWorkId, notasArray, soloHoja) {
  try {
    var actualizadas = 0;
    var errores = [];
    var notas = notasArray || [];

    var tituloTarea = 'Actividad';
    try {
      var trabajo = Classroom.Courses.CourseWork.get(courseId, courseWorkId);
      if (trabajo && trabajo.title) tituloTarea = trabajo.title;
    } catch(eGet) {
      Logger.log('No se pudo leer el título de la tarea: ' + eGet.message);
    }

    if (!soloHoja) {
      var permiso = puedeEscribirNotas(courseId, courseWorkId);
      if (!permiso.editable) {
        errores.push('Classroom: ' + permiso.motivo);
      } else {
        notas.forEach(function(item) {
        if (!item.submissionId) return;
        var notaEnviar = normalizarNotaEnvio(item.nota);
        if (notaEnviar === null) {
          errores.push(item.nombre + ': nota vacía o inválida, no se envió.');
          return;
        }
        try {
          Classroom.Courses.CourseWork.StudentSubmissions.patch(
            { draftGrade: notaEnviar },
            courseId,
            courseWorkId,
            item.submissionId,
            { updateMask: 'draftGrade' }
          );
          actualizadas++;
        } catch(err) {
          var msg = err.message || '';
          if (msg.indexOf('PERMISSION_DENIED') !== -1 || msg.indexOf('did not create') !== -1 || msg.indexOf('not permitted to make this request') !== -1) {
            errores.push(item.nombre + ': Google bloqueó el envío (tarea creada a mano en Classroom, la API solo deja calificar tareas creadas por la app). La nota quedó en la hoja.');
          } else if (msg.indexOf('scope') !== -1 || msg.indexOf('Scope') !== -1 || msg.indexOf('insufficient') !== -1) {
            errores.push(item.nombre + ': faltan permisos en Apps Script (scope classroom.coursework.students). Reautorice el proyecto.');
          } else {
            errores.push(item.nombre + ': ' + msg);
          }
        }
      });
      }
    }

    var hoja = { url: '', nombre: '' };
    var avisoHoja = '';
    try {
      hoja = crearHojaNotas(tituloTarea, notas);
    } catch(errHoja) {
      var msgHoja = errHoja.message || '';
      Logger.log('No se pudo crear la hoja de notas: ' + msgHoja);
      if (msgHoja.indexOf('auth/spreadsheets') !== -1 || msgHoja.indexOf('permiso para llamar a SpreadsheetApp') !== -1) {
        avisoHoja = 'La hoja de notas no se creó porque falta autorizar el permiso de hojas de cálculo. Para activarlo: en Apps Script abra Configuración del proyecto, active "Mostrar el archivo appsscript.json", agregue https://www.googleapis.com/auth/spreadsheets a oauthScopes, guarde y vuelva a ejecutar para autorizar. Las notas de Classroom no se vieron afectadas.';
      } else {
        avisoHoja = 'La hoja de notas no se creó: ' + msgHoja;
      }
    }

    return {
      success: soloHoja ? (hoja.url !== '') : (errores.length === 0),
      error: (soloHoja && hoja.url === '') ? (avisoHoja || 'No se pudo crear la hoja.') : undefined,
      actualizadas: actualizadas,
      total: notas.length,
      errores: errores,
      tituloTarea: tituloTarea,
      sheetUrl: hoja.url,
      sheetNombre: hoja.nombre,
      avisoHoja: avisoHoja,
      mensaje: soloHoja
        ? 'Hoja de notas creada sin tocar Classroom.'
        : (actualizadas + ' de ' + notas.length + ' notas en borrador.'
          + (errores.length > 0 ? ' Hubo ' + errores.length + ' fallos: revise el detalle.' : ''))
    };
  } catch(error) {
    return { success: false, error: 'Error general al guardar notas: ' + error.message };
  }
}

/**
 * Crea o actualiza la hoja de notas con nota, nivel y comentario por estudiante.
 */
function crearHojaNotas(tituloTarea, notasArray) {
  var nombreArchivo = 'Calificador IA - Notas IEJAGA';
  var libro = null;
  var archivos = DriveApp.getFilesByName(nombreArchivo);
  if (archivos.hasNext()) {
    var idLibro = archivos.next().getId();
    libro = SpreadsheetApp.openById(idLibro);
  } else {
    libro = SpreadsheetApp.create(nombreArchivo);
  }
  var base = (tituloTarea || 'Actividad').replace(/["':*?\/\\\[\]]/g, '').substring(0, 28);
  var nombreHoja = base;
  var hoja = libro.getSheetByName(nombreHoja);
  if (!hoja) {
    hoja = libro.insertSheet(nombreHoja);
  }
  hoja.clearContents();
  var filas = [['N.º', 'Estudiante', 'Nota (1.0-5.0)', 'Nivel 1290', 'Comentario para Classroom']];
  (notasArray || []).forEach(function(item, idx) {
    var n = normalizarNotaEnvio(item.nota);
    filas.push([idx + 1, item.nombre || '', (n === null ? '' : n), item.nivel || '', item.comentario || '']);
  });
  hoja.getRange(1, 1, filas.length, filas[0].length).setValues(filas);
  hoja.setFrozenRows(1);
  try { hoja.autoResizeColumns(1, filas[0].length); } catch(eCols) {}
  return { url: libro.getUrl(), nombre: nombreArchivo + ' > ' + nombreHoja };
}

// --------------------------------------------------------------------------
// 5. CREAR TAREAS EN CLASSROOM DESDE EL CALIFICADOR
// --------------------------------------------------------------------------
//
// Las tareas creadas aquí quedan asociadas al proyecto de la app y por eso
// Google sí permite guardarles notas en borrador por API. Las tareas creadas
// a mano en Classroom no aceptan escritura por API (regla de Google).

/**
 * Crea una tarea de tipo ASSIGNMENT publicada en el curso indicado.
 * datos: { titulo, descripcion, maxPoints, fechaEntrega (yyyy-mm-dd opcional) }.
 */
function crearTareaClassroom(courseId, datos) {
  try {
    if (!courseId) return { success: false, error: 'Seleccione un curso.' };
    datos = datos || {};
    var titulo = (datos.titulo || '').trim();
    if (!titulo) return { success: false, error: 'Escriba el título de la tarea.' };
    var cuerpo = {
      title: titulo,
      description: (datos.descripcion || '').substring(0, 30000),
      maxPoints: 5,
      workType: 'ASSIGNMENT',
      state: 'PUBLISHED'
    };
    if (datos.maxPoints !== undefined && datos.maxPoints !== null && datos.maxPoints !== '') {
      var mp = Number(String(datos.maxPoints).replace(',', '.'));
      if (!isNaN(mp) && mp >= 1 && mp <= 1000) cuerpo.maxPoints = mp;
    }
    if (datos.fechaEntrega) {
      var partes = String(datos.fechaEntrega).split('-');
      if (partes.length === 3) {
        cuerpo.dueDate = { year: Number(partes[0]), month: Number(partes[1]), day: Number(partes[2]) };
        cuerpo.dueTime = { hours: 23, minutes: 59 };
      }
    }
    var creada = Classroom.Courses.CourseWork.create(cuerpo, courseId);
    return {
      success: true,
      actividad: {
        id: creada.id,
        titulo: creada.title,
        descripcion: creada.description || '',
        puntosMaximos: creada.maxPoints || cuerpo.maxPoints,
        enlace: creada.alternateLink || '',
        fechaCreacion: creada.creationTime || ''
      },
      mensaje: 'Tarea publicada en Classroom. Como fue creada por la app, las notas sí se guardan solas en borrador.'
    };
  } catch(error) {
    var msg = error.message || '';
    if (msg.indexOf('scope') !== -1 || msg.indexOf('Scope') !== -1 || msg.indexOf('insufficient') !== -1) {
      return { success: false, error: 'Faltan permisos: reautorice el proyecto en Apps Script (scope classroom.coursework.students). Detalle: ' + msg };
    }
    return { success: false, error: 'No se pudo crear la tarea: ' + msg };
  }
}

/**
 * Revisa si la app puede escribir notas en una tarea (solo si la creó el mismo proyecto).
 * Devuelve { editable, motivo }. No lanza error.
 */
function puedeEscribirNotas(courseId, courseWorkId) {
  try {
    var lista = Classroom.Courses.CourseWork.StudentSubmissions.list(courseId, courseWorkId, { pageSize: 1 });
    var subs = (lista && lista.studentSubmissions) || [];
    if (subs.length === 0) return { editable: true, motivo: 'Sin entregas para verificar, se intentará el guardado.' };
    var sub = Classroom.Courses.CourseWork.StudentSubmissions.get(courseId, courseWorkId, subs[0].id);
    if (sub && sub.associatedWithDeveloper === true) {
      return { editable: true, motivo: 'Tarea creada por la app: escritura permitida.' };
    }
    return { editable: false, motivo: 'Tarea creada a mano en Classroom: Google bloquea la escritura por API (PERMISSION_DENIED). Use la hoja o la extensión.' };
  } catch(e) {
    return { editable: true, motivo: 'No se pudo verificar, se intentará el guardado. Detalle: ' + e.message };
  }
}
