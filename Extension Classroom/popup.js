// Popup: lee el JSON pegado y pide al content script que detecte o rellene.
function mostrar(texto) {
  document.getElementById('estado').innerText = texto;
}

function leerDatos() {
  const crudo = document.getElementById('datos').value.trim();
  if (!crudo) throw new Error('Pegue primero el JSON copiado desde el calificador.');
  let datos;
  try {
    datos = JSON.parse(crudo);
  } catch (e) {
    throw new Error('El texto pegado no es JSON válido. Copie de nuevo desde el calificador.');
  }
  if (!Array.isArray(datos) || datos.length === 0) {
    throw new Error('El JSON debe ser una lista con al menos un estudiante.');
  }
  // Validar estructura mínima.
  const primero = datos[0];
  if (!primero.nombre) {
    throw new Error('El JSON no tiene la estructura correcta. Cada elemento debe tener "nombre".');
  }
  return datos;
}

function enviarAccion(accion) {
  let datos = [];
  if (accion === 'rellenar') {
    try {
      datos = leerDatos();
      mostrar('📋 ' + datos.length + ' estudiantes cargados. Procesando...');
    } catch (e) {
      mostrar('❌ ' + e.message);
      return;
    }
  } else {
    // Detectar también manda los datos si están pegados (para la radiografía),
    // pero no falla si el campo está vacío.
    try { datos = leerDatos(); } catch (e) { datos = []; }
    mostrar('🔍 Detectando campos...');
  }

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0] || !tabs[0].url || tabs[0].url.indexOf('classroom.google.com') === -1) {
      mostrar('⚠ Abra primero la página de calificación de la tarea en classroom.google.com.');
      return;
    }
    chrome.tabs.sendMessage(tabs[0].id, { accion: accion, datos: datos }, (resp) => {
      if (chrome.runtime.lastError) {
        mostrar('❌ No se pudo hablar con la página. Recárguela (F5) e intente de nuevo.\n' + chrome.runtime.lastError.message);
        return;
      }
      if (!resp) {
        mostrar('⚠ Sin respuesta de la página. Recárguela (F5) e intente de nuevo.');
        return;
      }
      mostrar(resp.reporte || '✅ Listo.');
    });
  });
}

document.getElementById('btn-leer').addEventListener('click', () => enviarAccion('detectar'));
document.getElementById('btn-rellenar').addEventListener('click', () => enviarAccion('rellenar'));
document.getElementById('btn-detener').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0]) return;
    chrome.tabs.sendMessage(tabs[0].id, { accion: 'detener' }, (resp) => {
      if (chrome.runtime.lastError) {
        mostrar('No se pudo contactar la página: ' + chrome.runtime.lastError.message);
        return;
      }
      mostrar((resp && resp.reporte) || 'Detenido.');
    });
  });
});
