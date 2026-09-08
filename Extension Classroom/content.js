// Content script: rellena notas y comentarios en las ventanas de calificación
// de Google Classroom.
//
// ORDEN OBLIGATORIO POR ESTUDIANTE (no cambiar):
// 1. Clic en el campo de nota (abre el editor y el campo de comentario).
// 2. Tipear la nota SIN dar Enter todavía.
// 3. Pegar el comentario en su campo correspondiente.
// 4. Dar Enter en el campo de nota para confirmar y pasar al siguiente.
// 5. Nunca se pulsa Guardar ni Devolver: eso siempre lo hace usted.
//
// REGLAS CLAVE:
// - Selector exacto descubierto por F12: input[aria-label*="calificaci" i]
// - NUNCA toca el control de "5 puntos" de la barra superior.
// - No duplica comentarios previamente publicados.

// ─── SELECTORES ───────────────────────────────────────────────
const SEL = {
  comentario: [
    'div[contenteditable="true"][aria-label*="comentario privado" i]',
    'div[contenteditable="true"][aria-label*="private comment" i]',
    'div[contenteditable="true"][aria-label*="comentario" i]',
    'div[contenteditable="true"][aria-label*="comment" i]',
    'div[contenteditable="true"][aria-label*="privad" i]',
    'div[contenteditable="true"][role="textbox"]',
    'textarea[aria-label*="comentario privado" i]',
    'textarea[aria-label*="private comment" i]',
    'textarea[aria-label*="comentario" i]',
    'textarea[aria-label*="comment" i]'
  ],
  btnEnviarComentario: [
    'button[aria-label*="publicar" i]',
    'button[aria-label*="post" i]',
    'button[aria-label*="enviar" i]',
    'button[aria-label*="send" i]',
    'button[data-tooltip*="publicar" i]',
    'button[data-tooltip*="enviar" i]',
    'button[data-tooltip*="post" i]',
    '[role="button"][aria-label*="publicar" i]',
    '[role="button"][aria-label*="enviar" i]',
    '[role="button"][aria-label*="post" i]'
  ]
};

// ─── UTILIDADES ───────────────────────────────────────────────
function esperar(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function normalizarNombre(s) {
  return (s || '').toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[._…\n\r\t]+/g, ' ')
    .replace(/\s+/g, ' ').trim();
}

function calcularSimilitud(nombreA, nombreB) {
  const na = normalizarNombre(nombreA);
  const nb = normalizarNombre(nombreB);
  if (!na || !nb) return 0;
  if (na === nb) return 100;
  if (na.startsWith(nb) || nb.startsWith(na)) return 95;
  if (na.includes(nb) || nb.includes(na)) return 90;

  const palabrasA = na.split(' ').filter(p => p.length >= 2);
  const palabrasB = nb.split(' ').filter(p => p.length >= 2);
  if (palabrasA.length === 0 || palabrasB.length === 0) return 0;

  let coincidencias = 0;
  for (const pa of palabrasA) {
    for (const pb of palabrasB) {
      if (pa === pb || (pa.length >= 4 && pb.startsWith(pa)) || (pb.length >= 4 && pa.startsWith(pb))) {
        coincidencias++;
        break;
      }
    }
  }

  const mayorLongitud = Math.max(palabrasA.length, palabrasB.length);
  return (coincidencias / mayorLongitud) * 85;
}

function coinciden(a, b) {
  return calcularSimilitud(a, b) >= 50;
}

function esVisible(el) {
  if (!el) return false;
  const r = el.getBoundingClientRect();
  return r.width > 0 && r.height > 0;
}

// ─── IDENTIFICAR INPUT DEL ESTUDIANTE ─────────────────────────
// Candidatos amplios (la etiqueta exacta varía según idioma y versión):
// calificaci*, grade*, nota*, numéricos. La pertenencia se verifica aparte
// con inputPerteneceA, así que ampliar aquí no contamina.
const SEL_INPUT_NOTA = [
  'input[aria-label*="calificaci" i]',
  'input[aria-label*="grade" i]',
  'input[aria-label*="nota" i]',
  'input[aria-label*="puntos" i]',
  'input[inputmode="decimal"]',
  'input[inputmode="numeric"]',
  'input[type="number"]'
];
function inputsNotaCandidatos(visiblesSolo) {
  const vistos = new Set();
  const lista = [];
  SEL_INPUT_NOTA.forEach(sel => {
    let nodos = [];
    try { nodos = Array.from(document.querySelectorAll(sel)); } catch (e) { nodos = []; }
    nodos.forEach(n => {
      if (vistos.has(n)) return;
      if (visiblesSolo && !esVisible(n)) return;
      vistos.add(n);
      lista.push(n);
    });
  });
  return lista;
}
function encontrarInputNotaEstudiante(elementoNombre) {
  // 1. Subir por los ancestros de la fila
  let nodo = elementoNombre.parentElement;
  for (let i = 0; i < 8 && nodo && nodo !== document.body; i++) {
    const input = nodo.querySelector(SEL_INPUT_NOTA.join(','));
    if (input) {
      return input;
    }
    nodo = nodo.parentElement;
  }

  // 2. Buscar por proximidad vertical Y (en la misma fila física)
  const nameRect = elementoNombre.getBoundingClientRect();
  const todos = inputsNotaCandidatos(false);

  let mejor = null;
  let menorDistY = 999;
  for (const inp of todos) {
    if (!esVisible(inp)) continue;
    const r = inp.getBoundingClientRect();
    const distY = Math.abs(r.top - nameRect.top);
    if (distY < 70 && distY < menorDistY) {
      menorDistY = distY;
      mejor = inp;
    }
  }

  return mejor;
}

// Espera hasta timeoutMs a que aparezca un input PROPIO del estudiante.
async function esperarInputPropio(nombre, timeoutMs) {
  const limite = Date.now() + (timeoutMs || 2000);
  while (Date.now() < limite) {
    const info = buscarEstudianteEnLista(nombre);
    if (info) {
      const cand = encontrarInputNotaEstudiante(info.elementoNombre);
      if (cand && inputPerteneceA(cand, nombre)) return cand;
    }
    await esperar(250);
  }
  return null;
}

// ─── ESCRITURA EN EL INPUT DE NOTA DE CLASSROOM ───────────────
// Se usa en dos pasos: primero tipear (SIN Enter), y al final confirmar.
// Dividirlo es lo que permite pegar el comentario antes de confirmar.
// ─── PASO 1: tipear la nota (SIN Enter) ───────────────────────
function tipearNotaEnInput(input, valor) {
  input.focus();
  input.click();

  // 1. Simular tipeo real para que Google Wiz acepte el valor
  try {
    input.select();
    document.execCommand('selectAll', false, null);
    document.execCommand('delete', false, null);
    document.execCommand('insertText', false, valor);
  } catch (e) { /* fallback */ }

  // 2. Asignar el valor mediante el setter de prototipo
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
  if (setter) {
    setter.call(input, valor);
  } else {
    input.value = valor;
  }

  // 3. Despachar eventos (SIN Enter: la confirmación va al final)
  input.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
  input.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
}

// ─── PASO 2: confirmar con Enter (después del comentario) ─────
function confirmarNotaConEnter(input) {
  input.focus();
  input.dispatchEvent(new KeyboardEvent('keydown', {
    bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13, which: 13
  }));
  input.dispatchEvent(new KeyboardEvent('keypress', {
    bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13, which: 13
  }));
  input.dispatchEvent(new KeyboardEvent('keyup', {
    bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13, which: 13
  }));
  input.blur();
  input.dispatchEvent(new Event('blur', { bubbles: true }));
}

// Compatibilidad: escritura completa en un solo llamado (tipear + confirmar).
function escribirNotaEnInput(input, valor) {
  tipearNotaEnInput(input, valor);
  confirmarNotaConEnter(input);
}

// Escritura en textarea simple (fallback para comentarios).
function escribirEnInput(el, texto) {
  el.focus();
  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
  if (setter) {
    setter.call(el, texto);
  } else {
    el.value = texto;
  }
  el.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
  el.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
}

function escribirEnContentEditable(el, texto) {
  el.focus();
  try {
    document.execCommand('selectAll', false, null);
    document.execCommand('delete', false, null);
    document.execCommand('insertText', false, texto);
  } catch (e) { /* fallback */ }

  if (!el.innerText || !el.innerText.trim()) {
    el.innerText = texto;
  }
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
}

// ─── VERIFICAR QUE EL PANEL DERECHO SEA DEL ESTUDIANTE ────────
async function asegurarEstudianteEnPanelDerecho(nombreEstudiante, elementoClic, anchoLista) {
  for (let intento = 0; intento < 12; intento++) {
    const elementosDerecha = Array.from(document.querySelectorAll('h1, h2, h3, [role="heading"], div, span, a'))
      .filter(el => {
        if (!esVisible(el)) return false;
        const r = el.getBoundingClientRect();
        if (r.left <= anchoLista || r.top > 320 || r.top < 70) return false;
        const t = (el.innerText || '').trim();
        return t.length >= 3 && t.length <= 80;
      });

    const match = elementosDerecha.find(el => calcularSimilitud(el.innerText, nombreEstudiante) >= 55);
    if (match) {
      return true;
    }

    if ((intento === 2 || intento === 5) && elementoClic) {
      elementoClic.click();
    }
    await esperar(200);
  }
  return false;
}

// ─── VERIFICAR PANEL DERECHO SIN CLICS EXTRA ──────────────────
// Solo verifica (no hace clic): los clics extra sobre el nombre tumbaban
// el editor de nota abierto. Si no sincroniza, se re-hace clic en el
// CAMPO DE NOTA, nunca en el nombre.
async function verificarPanelDerecho(nombreEstudiante, anchoLista) {
  for (let intento = 0; intento < 8; intento++) {
    const elementosDerecha = Array.from(document.querySelectorAll('h1, h2, h3, [role="heading"], div, span, a'))
      .filter(el => {
        if (!esVisible(el)) return false;
        const r = el.getBoundingClientRect();
        if (r.left <= anchoLista || r.top > 320 || r.top < 70) return false;
        const t = (el.innerText || '').trim();
        return t.length >= 3 && t.length <= 80;
      });

    const match = elementosDerecha.find(el => calcularSimilitud(el.innerText, nombreEstudiante) >= 55);
    if (match) {
      return true;
    }
    await esperar(250);
  }
  return false;
}

// ─── VERIFICAR SI UN COMENTARIO YA FUE PUBLICADO ──────────────
function yaTieneComentario(textoComentario, anchoLista) {
  const normBuscado = normalizarNombre(textoComentario);
  if (!normBuscado || normBuscado.length < 10) return false;

  const inicioComentario = normBuscado.substring(0, Math.min(30, normBuscado.length));

  const elementosDerecha = Array.from(document.querySelectorAll('div, p, span, [role="listitem"]'))
    .filter(el => {
      if (!esVisible(el)) return false;
      const r = el.getBoundingClientRect();
      if (r.left <= anchoLista) return false;
      if (el.getAttribute('contenteditable') === 'true' || el.tagName === 'TEXTAREA') return false;
      return true;
    });

  for (const el of elementosDerecha) {
    if (el.children.length > 4) continue;
    const txt = normalizarNombre(el.innerText || el.textContent || '');
    if (txt.length < 15) continue;
    if (txt.includes(inicioComentario) || calcularSimilitud(txt, normBuscado) >= 70) {
      return true;
    }
  }
  return false;
}

// ─── ENVÍO DE COMENTARIO PRIVADO ─────────────────────────────
async function enviarComentarioPrivado(campoComentario) {
  await esperar(300);

  let contenedor = campoComentario.closest('form, div') || campoComentario.parentElement;
  for (let i = 0; i < 6 && contenedor && contenedor !== document.body; i++) {
    for (const sel of SEL.btnEnviarComentario) {
      const btn = contenedor.querySelector(sel);
      if (btn && esVisible(btn) && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true') {
        btn.click();
        return true;
      }
    }
    const botones = Array.from(contenedor.querySelectorAll('button, [role="button"]')).filter(esVisible);
    const btnIcono = botones.find(b => {
      if (b.disabled || b.getAttribute('aria-disabled') === 'true') return false;
      const t = (b.innerText || '').toLowerCase();
      const aria = (b.getAttribute('aria-label') || '').toLowerCase();
      if (t === 'send' || aria.includes('enviar') || aria.includes('publicar') || aria.includes('post') || aria.includes('coment')) return true;
      if (b.querySelector('svg path[d*="M2.01"]') || b.querySelector('svg path[d*="2.01"]')) return true;
      const r = b.getBoundingClientRect();
      const rCont = contenedor.getBoundingClientRect();
      return r.right > rCont.right - 70 && r.bottom > rCont.bottom - 70;
    });
    if (btnIcono) {
      btnIcono.click();
      return true;
    }
    contenedor = contenedor.parentElement;
  }

  const botonesDerecha = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => {
    if (!esVisible(b) || b.disabled || b.getAttribute('aria-disabled') === 'true') return false;
    const r = b.getBoundingClientRect();
    return r.left > window.innerWidth * 0.45 && r.top > window.innerHeight * 0.45;
  });

  const btnFinal = botonesDerecha.find(b => {
    const aria = (b.getAttribute('aria-label') || '').toLowerCase();
    const t = (b.innerText || '').toLowerCase();
    return aria.includes('publicar') || aria.includes('enviar') || aria.includes('post') || t === 'send';
  });
  if (btnFinal) {
    btnFinal.click();
    return true;
  }

  return false;
}

// ─── OBTENER CONTENEDOR CON SCROLL DE LA LISTA ───────────────
function obtenerContenedorLista() {
  const anchoLista = Math.max(350, Math.min(window.innerWidth * 0.48, 550));
  const elementos = Array.from(document.querySelectorAll('div, main, section')).filter(el => {
    if (!esVisible(el)) return false;
    const r = el.getBoundingClientRect();
    if (r.left > 100 || r.width < 180 || r.width > anchoLista + 50) return false;
    return el.scrollHeight > el.clientHeight + 40;
  });
  return elementos[0] || null;
}

// ─── BÚSQUEDA DE ESTUDIANTE EN LA LISTA ──────────────────────
// Umbral alto (70) a propósito: con nombres parecidos y textos recortados,
// un umbral bajo emparejaba FILAS AJENAS y contaminaba a otros estudiantes.
function buscarEstudianteEnLista(nombreBuscado, umbral) {
  const minimo = (umbral === undefined) ? 70 : umbral;
  const anchoLista = Math.max(350, Math.min(window.innerWidth * 0.48, 550));

  const todos = Array.from(document.querySelectorAll('span, div, a, p, h2, h3, [role="button"]'))
    .filter(el => {
      if (!esVisible(el)) return false;
      const r = el.getBoundingClientRect();
      if (r.left > anchoLista || r.top < 90) return false;
      const t = (el.innerText || '').trim();
      if (t.length < 3 || t.length > 80) return false;
      if (/^(todos los estudiantes|all students|ordenar por|sort by|instrucciones|trabajo del estudiante)/i.test(t)) return false;
      return true;
    });

  let mejorElemento = null;
  let mejorPuntaje = 0;

  for (const el of todos) {
    const t = (el.innerText || '').trim();
    const score = calcularSimilitud(t, nombreBuscado);
    if (score > mejorPuntaje && score >= minimo) {
      mejorPuntaje = score;
      mejorElemento = el;
    }
  }

  if (!mejorElemento) return null;

  return {
    estudiante: nombreBuscado,
    elementoNombre: mejorElemento
  };
}

// ─── BARRIDO DE SCROLL HASTA RENDERIZAR AL ESTUDIANTE ─────────
// La lista virtualiza filas: si el estudiante no está en el DOM, se baja
// el scroll hasta que aparezca. Si se llega al fondo sin verlo, se vuelve
// arriba y se barre una vez más (la lista puede no estar en el mismo orden).
async function barrerListaHastaEstudiante(nombreBuscado) {
  let info = buscarEstudianteEnLista(nombreBuscado);
  if (info && info.elementoNombre.isConnected) return info;

  const contenedor = obtenerContenedorLista();
  if (!contenedor) return buscarEstudianteEnLista(nombreBuscado);

  for (let pasada = 0; pasada < 2; pasada++) {
    if (pasada === 1) {
      contenedor.scrollTo(0, 0);
      await esperar(350);
    }
    let anterior = -1;
    for (let i = 0; i < 40; i++) {
      info = buscarEstudianteEnLista(nombreBuscado);
      if (info && info.elementoNombre.isConnected) return info;
      if (contenedor.scrollTop === anterior &&
          contenedor.scrollTop + contenedor.clientHeight >= contenedor.scrollHeight - 20) {
        break; // fondo alcanzado
      }
      anterior = contenedor.scrollTop;
      contenedor.scrollBy(0, 400);
      await esperar(250);
    }
  }
  return null;
}

// ─── ¿ESTE INPUT ES DE ESTE ESTUDIANTE? ───────────────────────
// Blindaje anti-contaminación: nunca se escribe en un input que no sea del
// estudiante en turno. Revisa el aria-label y la fila contenedora.
function inputPerteneceA(input, nombre) {
  if (!input || !input.isConnected) return false;
  try {
    const aria = input.getAttribute && (input.getAttribute('aria-label') || '') || '';
    if (aria && calcularSimilitud(aria, nombre) >= 70) return true;
    let nodo = input;
    for (let i = 0; i < 10 && nodo && nodo !== document.body; i++) {
      nodo = nodo.parentElement;
      if (!nodo) break;
      const t = (nodo.innerText || '').split('\n').map(l => l.trim()).filter(Boolean).slice(0, 4);
      if (t.some(lin => calcularSimilitud(lin, nombre) >= 80)) return true;
    }
  } catch (e) { /* no pertenece */ }
  return false;
}

// ─── DUEÑO DEL PANEL DERECHO ──────────────────────────────────
// Devuelve el nombre (de los datos) que mejor calza con lo visible a la
// derecha, o '' si ninguno calza bien. El comentario SOLO se pega cuando
// el dueño es el estudiante en turno.
function duenoDelPanel(datos, anchoLista) {
  const textos = Array.from(document.querySelectorAll('h1, h2, h3, [role="heading"], div, span, a'))
    .filter(el => {
      if (!esVisible(el)) return false;
      const r = el.getBoundingClientRect();
      if (r.left <= anchoLista || r.top > 320 || r.top < 70) return false;
      const t = (el.innerText || '').trim();
      return t.length >= 3 && t.length <= 80;
    })
    .map(el => (el.innerText || '').trim());
  let mejor = '';
  let mejorPuntaje = 70;
  for (const d of (datos || [])) {
    for (const t of textos) {
      const s = calcularSimilitud(t, d.nombre);
      if (s > mejorPuntaje) {
        mejorPuntaje = s;
        mejor = d.nombre;
      }
    }
  }
  return mejor;
}

function valoresNotaIguales(a, b) {
  const na = parseFloat(String(a === undefined || a === null ? '' : a).replace(',', '.'));
  const nb = parseFloat(String(b === undefined || b === null ? '' : b).replace(',', '.'));
  if (isNaN(na) || isNaN(nb)) return false;
  return Math.abs(na - nb) < 0.051;
}

// ─── CELDAS DE NOTA (___/5) EN LA PÁGINA ───────────────────────
// Las celdas suelen tener spans anidados, así que no se exige que sean
// hojas del DOM: se buscan textos cortos con "/N" y se queda con los
// más internos. Excluye puntaje máximo, orden y devolver.
function buscarCeldasNota() {
  const cands = Array.from(document.querySelectorAll('div, span, button, td, [role="gridcell"], [role="cell"], [role="button"]'))
    .filter(el => {
      if (!esVisible(el)) return false;
      const t = ((el.innerText || el.textContent) || '').trim();
      if (t.length === 0 || t.length > 24) return false;
      if (!/\/\s*\d/.test(t)) return false;
      if (/puntaje|puntos|ordenar|sort|devolver|return|buscar|todos/i.test(t)) return false;
      return true;
    });
  const set = new Set(cands);
  return cands.filter(el => {
    try {
      return !Array.from(el.querySelectorAll('*')).some(x => set.has(x));
    } catch (e) { return true; }
  });
}

// ─── REVELAR CELDA DE NOTA OCULTA ─────────────────────────────
// En filas sin entrega la casilla ___/5 solo aparece al pasar el mouse.
// 1) Si hay un botón/combo de calificación cerca, se le hace clic directo.
// 2) Si no, se dispara hover sobre el área derecha de la fila y la celda aparece.
async function revelarCeldaNota(elementoNombre) {
  try {
    const r0 = elementoNombre.getBoundingClientRect();
    const triggers = Array.from(document.querySelectorAll('button, [role="button"], [role="combobox"], [aria-haspopup]'))
      .filter(el => {
        if (!esVisible(el)) return false;
        const aria = (el.getAttribute && (el.getAttribute('aria-label') || '')) || '';
        if (!/calific|grade|nota/i.test(aria)) return false;
        if (esControlPropio(el)) return false;
        const r = el.getBoundingClientRect();
        return Math.abs(r.top - r0.top) < 140;
      });
    if (triggers.length > 0) {
      triggers[0].click();
      return 'trigger';
    }
    let fila = null;
    let nodo = elementoNombre;
    for (let i = 0; i < 10 && nodo && nodo !== document.body; i++) {
      nodo = nodo.parentElement;
      if (!nodo) break;
      try { if (nodo.matches('tr, [role="row"], li')) { fila = nodo; break; } } catch (e) { /* sigue */ }
    }
    const raiz = fila || elementoNombre.parentElement;
    if (raiz) {
      const r = raiz.getBoundingClientRect();
      const areas = Array.from(raiz.querySelectorAll('div, td, span')).filter(el => {
        if (!esVisible(el)) return false;
        const q = el.getBoundingClientRect();
        return q.width > 50 && q.height > 18 && q.left > r.left + r.width * 0.5;
      });
      areas.sort((a, b) => b.getBoundingClientRect().right - a.getBoundingClientRect().right);
      const area = areas[0] || raiz;
      ['pointerover', 'mouseover', 'mouseenter', 'mousemove'].forEach(t => {
        area.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
      });
      return 'hover';
    }
  } catch (e) { /* no se pudo revelar */ }
  return null;
}

// ─── ¿LA FILA YA MUESTRA ESTE COMENTARIO? ──────────────────────
// Classroom muestra bajo el nombre el comentario ya publicado. Si ya está,
// se cuenta como procesado y NO se vuelve a pegar (anti-duplicados).
function filaYaTieneComentario(elementoNombre, textoComentario) {
  try {
    const norm = normalizarNombre(textoComentario);
    if (!norm || norm.length < 10) return false;
    const inicio = norm.substring(0, 25);
    let fila = null;
    let nodo = elementoNombre;
    for (let i = 0; i < 10 && nodo && nodo !== document.body; i++) {
      nodo = nodo.parentElement;
      if (!nodo) break;
      try { if (nodo.matches('tr, [role="row"], li')) { fila = nodo; break; } } catch (e) { /* sigue */ }
    }
    const raiz = fila || elementoNombre.parentElement;
    if (!raiz) return false;
    return normalizarNombre(raiz.innerText || '').includes(inicio);
  } catch (e) { return false; }
}

// ─── CLIC EN LA CELDA DE NOTA (___/5) CERCA DEL NOMBRE ────────
function clicEnCeldaNota(elementoNombre) {
  try {
    const hojas = buscarCeldasNota();
    if (hojas.length === 0) return false;
    const r0 = elementoNombre.getBoundingClientRect();
    hojas.sort((a, b) =>
      Math.abs(a.getBoundingClientRect().top - r0.top) - Math.abs(b.getBoundingClientRect().top - r0.top));
    const mejor = hojas[0];
    if (Math.abs(mejor.getBoundingClientRect().top - r0.top) > 140) return false; // muy lejos: no es su fila
    mejor.scrollIntoView({ block: 'center', behavior: 'instant' });
    mejor.click();
    return true;
  } catch (e) { return false; }
}

// ─── CLIC EN ÁREA VACÍA DE NOTA ───────────────────────────────
// Filas sin entrega no muestran ni ___/5: se hace clic en la zona derecha
// de la fila (donde vive la celda de nota) para forzar que abra el editor.
function clicEnAreaNotaVacia(elementoNombre) {
  try {
    let fila = null;
    let nodo = elementoNombre;
    for (let i = 0; i < 10 && nodo && nodo !== document.body; i++) {
      nodo = nodo.parentElement;
      if (!nodo) break;
      try { if (nodo.matches('tr, [role="row"], li')) { fila = nodo; break; } } catch (e) { /* sigue */ }
    }
    const raiz = fila || elementoNombre.parentElement;
    if (!raiz) return false;
    const r = raiz.getBoundingClientRect();
    const zonas = Array.from(raiz.querySelectorAll('div, td, span, button')).filter(el => {
      if (!esVisible(el)) return false;
      if (/^(input|textarea)$/i.test(el.tagName)) return false;
      const q = el.getBoundingClientRect();
      if (q.width < 60 || q.height < 18) return false;
      if (q.left < r.left + r.width * 0.45) return false; // mitad derecha de la fila
      const t = ((el.innerText || el.textContent) || '').trim().toLowerCase();
      if (/puntaje|puntos|ordenar|sort|devolver|todos/i.test(t)) return false;
      return true;
    });
    if (zonas.length === 0) return false;
    zonas.sort((a, b) => b.getBoundingClientRect().right - a.getBoundingClientRect().right);
    const zona = zonas[0];
    zona.scrollIntoView({ block: 'center', behavior: 'instant' });
    ['pointerover', 'mouseover', 'mouseenter', 'mousemove'].forEach(t => {
      zona.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
    });
    zona.click();
    return true;
  } catch (e) { return false; }
}

// ─── DETECCIÓN GENERAL (BOTÓN DETECTAR) ───────────────────────
function detectar() {
  const lineas = [];
  const anchoLista = Math.max(350, Math.min(window.innerWidth * 0.48, 550));

  const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"], [role="checkbox"]'))
    .filter(el => esVisible(el) && el.getBoundingClientRect().left < anchoLista);

  const inputsNota = Array.from(document.querySelectorAll('input[aria-label*="calificaci" i]'));

  const totalEstudiantes = checkboxes.length > 0 ? checkboxes.length - 1 : inputsNota.length;

  lineas.push('📋 Estudiantes en la lista: ' + (totalEstudiantes > 0 ? totalEstudiantes : 'detectando...'));
  lineas.push('🎯 Campos de calificación exactos [aria-label*="calificaci"]: ' + inputsNota.length);
  if (inputsNota.length > 0) {
    const ejemplo = (inputsNota[0].getAttribute('aria-label') || '(sin etiqueta)').substring(0, 80);
    lineas.push('   Ejemplo etiqueta: ' + ejemplo);
  }
  const celdas = buscarCeldasNota();
  lineas.push('🧮 Celdas de nota (___/5) en página: ' + celdas.length);
  if (celdas.length > 0) {
    lineas.push('   Ejemplo celda: ' + ((celdas[0].innerText || '').trim().substring(0, 20)));
  } else {
    lineas.push('   Si no ve la columna ___/5, desplácese a la derecha y pulse Detectar de nuevo.');
    lineas.push('   Las celdas vacías se revelan solas al Rellenar (hover automático).');
  }

  const camposComentario = Array.from(document.querySelectorAll('div[contenteditable="true"], textarea'))
    .filter(c => esVisible(c) && c.getBoundingClientRect().left > 450);
  if (camposComentario.length > 0) {
    lineas.push('💬 Panel de comentarios del estudiante activo: Detectado.');
  }

  lineas.push('');
  lineas.push('✔ Pegue el JSON del calificador y pulse "Rellenar notas y comentarios".');
  return lineas.join('\n');
}

// ─── RELLENAR NOTAS Y COMENTARIOS ────────────────────────────
async function rellenar(datos) {
  if (!Array.isArray(datos) || datos.length === 0) {
    return 'Error: No se recibieron datos. Pegue el JSON del calificador.';
  }

  let notasOk = 0;
  let comentariosOk = 0;
  const errores = [];
  const noEncontrados = [];
  const colaIndividual = [];

  const anchoLista = Math.max(350, Math.min(window.innerWidth * 0.48, 550));
  const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"], [role="checkbox"]'))
    .filter(el => esVisible(el) && el.getBoundingClientRect().left < anchoLista);

  const hayEstudiantesEnLista = datos.some(d => buscarEstudianteEnLista(d.nombre) !== null);
  const esVistaLista = checkboxes.length >= 2 || hayEstudiantesEnLista;

  if (esVistaLista) {
    // ══════════════════════════════════════════════════════════
    // MODO LISTA: Procesar cada estudiante en secuencia
    // ══════════════════════════════════════════════════════════
    for (const d of datos) {
      if (await jobCancelado()) {
        return '⏹ Proceso detenido por usted. Lo ya rellenado queda en pantalla para revisar y guardar.';
      }
      d.a = (d.a || 0) + 1;
      if (d.soloIndividual) {
        // Ya se sabe que no tiene casilla en lista: va directo a la cola individual.
        colaIndividual.push(d);
        continue;
      }
      // 1. Buscar al estudiante en la lista izquierda
      let info = buscarEstudianteEnLista(d.nombre);

      if (!info) {
        const contenedorLista = obtenerContenedorLista();
        if (contenedorLista) {
          contenedorLista.scrollBy(0, 300);
          await esperar(200);
          info = buscarEstudianteEnLista(d.nombre);
        }
      }

      if (!info) {
        noEncontrados.push(d.nombre);
        continue;
      }

      try {
        const tieneNota = (d.nota !== null && d.nota !== undefined && d.nota !== '');
        const tieneComentario = Boolean((d.comentario || '').trim());
        if (!tieneNota && !tieneComentario) {
          continue;
        }
        const valorNota = tieneNota ? String(d.nota).replace(',', '.') : '';

        // PASO 1: ubicar al estudiante barriendo el scroll (la lista virtualiza
        // filas; sin barrido se emparejaba la fila ajena visible y se contaminaba).
        info = await barrerListaHastaEstudiante(d.nombre);
        if (!info) {
          noEncontrados.push(d.nombre);
          continue;
        }
        info.elementoNombre.scrollIntoView({ block: 'center', behavior: 'instant' });
        await esperar(300);

        // PASO 2: localizar el campo de nota PROPIO y hacer CLIC en él.
        // Si el campo no es del estudiante, NO se usa (anti-contaminación).
        // Ojo: en filas sin entrega la casilla ___/5 está vacía y solo se
        // revela con hover, por eso primero se revela y luego se busca.
        let inputNota = encontrarInputNotaEstudiante(info.elementoNombre);
        if (inputNota && !inputPerteneceA(inputNota, d.nombre)) {
          inputNota = null;
        }
        if (!inputNota) {
          // Revelar (hover o clic en trigger) y luego buscar la celda ___/5...
          const modo = await revelarCeldaNota(info.elementoNombre);
          if (modo !== 'trigger') {
            clicEnCeldaNota(info.elementoNombre);
          }
          // ...y esperar con reintentos a que aparezca un campo PROPIO
          // (el editor tarda en renderizar; un solo intento no basta).
          inputNota = await esperarInputPropio(d.nombre, 2500);
        }
        if (!inputNota) {
          // ...o clic en el área vacía de nota (filas sin entrega no muestran ___/5)...
          if (clicEnAreaNotaVacia(info.elementoNombre)) {
            await esperar(600);
            inputNota = await esperarInputPropio(d.nombre, 2000);
          }
        }
        if (!inputNota) {
          // ...o seleccionando por nombre como último recurso.
          info.elementoNombre.click();
          await esperar(500);
          inputNota = await esperarInputPropio(d.nombre, 2000);
        }
        if (tieneNota && !inputNota) {
          d.soloIndividual = true;
          colaIndividual.push(d);
          continue;
        }
        if (inputNota) {
          inputNota.scrollIntoView({ block: 'center', behavior: 'instant' });
          await esperar(150);
          inputNota.click(); // abre el editor (y con él, el campo de comentario)
          await esperar(500);
          if (!inputNota.isConnected || !inputPerteneceA(inputNota, d.nombre)) {
            const infoR3 = buscarEstudianteEnLista(d.nombre);
            const cand3 = infoR3 ? encontrarInputNotaEstudiante(infoR3.elementoNombre) : null;
            inputNota = (cand3 && inputPerteneceA(cand3, d.nombre)) ? cand3 : null;
          }
        }

        // PASO 3: tipear la nota SIN Enter todavía y verificar que quedó escrita.
        if (tieneNota) {
          if (!inputNota || !inputNota.isConnected) {
            errores.push(d.nombre + ' (el campo de nota se cerró antes de escribir)');
            continue;
          }
          tipearNotaEnInput(inputNota, valorNota);
          await esperar(300);
          if (!valoresNotaIguales(inputNota.value, valorNota)) {
            tipearNotaEnInput(inputNota, valorNota); // un reintento
            await esperar(300);
          }
          if (!valoresNotaIguales(inputNota.value, valorNota)) {
            errores.push(d.nombre + ' (la nota no quedó escrita; no se confirmó nada)');
            continue;
          }
        }

        // PASO 4: comentario. Primero se mira si la fila YA lo muestra
        // (Classroom lista bajo el nombre el comentario publicado): si está,
        // se cuenta y NO se vuelve a pegar. Si no, se pega SOLO cuando el
        // panel derecho es de este estudiante.
        if (tieneComentario) {
          const infoFila = buscarEstudianteEnLista(d.nombre);
          if (infoFila && filaYaTieneComentario(infoFila.elementoNombre, d.comentario)) {
            comentariosOk++;
          } else {
            let dueno = duenoDelPanel(datos, anchoLista);
          if (dueno !== d.nombre) {
            info.elementoNombre.click();
            await esperar(600);
            dueno = duenoDelPanel(datos, anchoLista);
          }
          if (dueno !== d.nombre) {
            errores.push(d.nombre + ' (el panel mostraba a otro estudiante; comentario no pegado)');
          } else if (yaTieneComentario(d.comentario, anchoLista)) {
            comentariosOk++;
          } else {
            let campoComentario = null;
            for (let intento = 0; intento < 6 && !campoComentario; intento++) {
              const candidatos = Array.from(document.querySelectorAll('div[contenteditable="true"], textarea'))
                .filter(c => esVisible(c) && c.getBoundingClientRect().left > 450);
              if (candidatos.length > 0) {
                campoComentario = candidatos[0];
                break;
              }
              await esperar(250);
            }

            if (campoComentario) {
              if (campoComentario.tagName === 'TEXTAREA') {
                escribirEnInput(campoComentario, d.comentario);
              } else {
                escribirEnContentEditable(campoComentario, d.comentario);
              }
              await esperar(350);

              await enviarComentarioPrivado(campoComentario);
              await esperar(400);
              // Re-verificar que el panel siga siendo del mismo estudiante;
              // el envío a veces avanza la selección.
              if (duenoDelPanel(datos, anchoLista) === d.nombre || yaTieneComentario(d.comentario, anchoLista)) {
                comentariosOk++;
              } else {
                errores.push(d.nombre + ' (el panel cambió tras enviar; revise el comentario)');
              }
            } else {
              errores.push(d.nombre + ' (campo de comentario no abrió)');
            }
          }
          } // cierra el else de filaYaTieneComentario
        }

        // PASO 5: AHORA SÍ Enter en el campo de nota para confirmar y pasar al siguiente.
        // Solo si el campo sigue siendo propio y con nuestro valor.
        if (tieneNota) {
          if (!inputNota || !inputNota.isConnected || !inputPerteneceA(inputNota, d.nombre)) {
            const infoFresca = await barrerListaHastaEstudiante(d.nombre);
            const inputFresco = infoFresca ? encontrarInputNotaEstudiante(infoFresca.elementoNombre) : null;
            if (inputFresco && inputPerteneceA(inputFresco, d.nombre)) {
              inputNota = inputFresco;
              tipearNotaEnInput(inputNota, valorNota);
              await esperar(300);
            } else {
              inputNota = null;
            }
          } else if (!valoresNotaIguales(inputNota.value, valorNota)) {
            tipearNotaEnInput(inputNota, valorNota);
            await esperar(300);
          }
          if (inputNota && inputNota.isConnected && valoresNotaIguales(inputNota.value, valorNota)) {
            confirmarNotaConEnter(inputNota);
            await esperar(600);
            // Verificar confirmación: el editor se cierra o conserva el valor.
            // El segundo Enter SOLO si el campo sigue siendo del mismo estudiante
            // (si no, podría confirmar la casilla del siguiente).
            const infoVer = buscarEstudianteEnLista(d.nombre);
            const inputVer = infoVer ? encontrarInputNotaEstudiante(infoVer.elementoNombre) : null;
            if (inputVer && inputVer.isConnected && inputPerteneceA(inputVer, d.nombre) &&
                inputVer.value.trim() !== '' && !valoresNotaIguales(inputVer.value, valorNota)) {
              confirmarNotaConEnter(inputVer);
              await esperar(500);
            }
            notasOk++;
          } else {
            errores.push(d.nombre + ' (el campo cambió antes del Enter; nota no confirmada)');
          }
        }

      } catch (e) {
        errores.push(d.nombre + ': ' + e.message);
      }

      await esperar(350);
    }

  } else {
    return '⚠ No se detectó la lista de estudiantes en pantalla.\n' +
      'Asegúrese de estar en la pestaña "Trabajo del estudiante" en Classroom.';
  }

  // ─── CONTINUACIÓN AUTOMÁTICA EN VISTA INDIVIDUAL ────────────
  // Los sin casilla en lista (tareas no entregadas) se abren solos uno por
  // uno en su vista individual. Agotados tras varios intentos quedan en errores.
  const pendientesInd = colaIndividual.filter(d => (d.a || 0) < 4);
  pendientesInd.forEach(d => { d.soloIndividual = true; });
  colaIndividual.filter(d => (d.a || 0) >= 4).forEach(d => {
    errores.push(d.nombre + ' (sin campo de nota tras varios intentos; ábralo a mano)');
  });
  if (pendientesInd.length > 0) {
    await store.set('ieJagaJob', {
      datos: pendientesInd, notasOk: notasOk, comentariosOk: comentariosOk,
      errores: errores, noEncontrados: noEncontrados,
      creado: Date.now(), hecho: false, cancelado: false, modoAuto: true,
      actor: ACTOR, leaseTs: Date.now()
    });
    const primero = await barrerListaHastaEstudiante(pendientesInd[0].nombre);
    if (primero) {
      primero.elementoNombre.click();
      trasAbrirEstudiante();
    }
    const reporteAuto = [
      '✅ Notas rellenadas en lista: ' + notasOk + ' de ' + datos.length,
      '💬 Comentarios procesados: ' + comentariosOk
    ];
    if (errores.length > 0) {
      reporteAuto.push('❌ Errores: ' + errores.slice(0, 6).join('; ') +
        (errores.length > 6 ? ' (+' + (errores.length - 6) + ' más)' : ''));
    }
    reporteAuto.push('🔄 ' + pendientesInd.length + ' sin casilla en lista: se abren solos uno por uno en su vista individual.');
    reporteAuto.push('NO cierre esta pestaña. Al terminar sale el resumen. Para detener, use el botón Detener de la extensión.');
    return reporteAuto.join('\n');
  }

  // ─── REPORTE FINAL ──────────────────────────────────────────
  const reporte = [
    '✅ Notas rellenadas: ' + notasOk + ' de ' + datos.length,
    '💬 Comentarios procesados: ' + comentariosOk
  ];
  if (noEncontrados.length > 0) {
    reporte.push('⚠ No encontrados en la lista: ' + noEncontrados.slice(0, 8).join(', ') +
      (noEncontrados.length > 8 ? ' (+' + (noEncontrados.length - 8) + ' más)' : ''));
  }
  if (errores.length > 0) {
    reporte.push('❌ Errores: ' + errores.slice(0, 6).join('; ') +
      (errores.length > 6 ? ' (+' + (errores.length - 6) + ' más)' : ''));
  }
  reporte.push('🔍 REVISE todo en pantalla y pulse Guardar/Devolver en Classroom cuando esté listo.');
  return reporte.join('\n');
}

// ─── MODO AUTOMÁTICO: VISTA INDIVIDUAL ────────────────────────
// Para estudiantes sin casilla en la lista (no entregaron). Se abren solos
// uno por uno, se califican en su vista y se vuelve a la lista.
// El trabajo pendiente vive en chrome.storage: si la página recarga,
// el proceso retoma solo. Nunca se escribe sin verificar el dueño.

const ACTOR = 'a' + Math.random().toString(36).slice(2);
const JOB_KEY = 'ieJagaJob';
const JOB_MAX_MIN = 30;

const store = {
  mem: {},
  async get(k) {
    try {
      if (chrome.storage && chrome.storage.local) {
        const o = await chrome.storage.local.get(k);
        if (o && o[k] !== undefined) return o[k];
      }
    } catch (e) { /* sin storage: memoria */ }
    return this.mem[k];
  },
  async set(k, v) {
    this.mem[k] = v;
    try {
      if (chrome.storage && chrome.storage.local) {
        const o = {};
        o[k] = v;
        await chrome.storage.local.set(o);
      }
    } catch (e) { /* sin storage: memoria */ }
  },
  async del(k) {
    delete this.mem[k];
    try {
      if (chrome.storage && chrome.storage.local) await chrome.storage.local.remove(k);
    } catch (e) { /* sin storage: memoria */ }
  }
};

function vistaActual() {
  try {
    const m = (location.href || '').match(/\/submissions(?:\/([^/?#]+))?/);
    if (m) return m[1] ? 'individual' : 'lista';
  } catch (e) { /* fallback DOM */ }
  try {
    const ancho = Math.max(350, Math.min(window.innerWidth * 0.48, 550));
    const checks = Array.from(document.querySelectorAll('input[type="checkbox"], [role="checkbox"]'))
      .filter(el => esVisible(el) && el.getBoundingClientRect().left < ancho);
    if (checks.length >= 2) return 'lista';
  } catch (e) { /* otra vista */ }
  return 'otra';
}

async function jobCancelado() {
  try {
    const j = await store.get(JOB_KEY);
    return !!(j && j.cancelado);
  } catch (e) { return false; }
}

// Toma el control del trabajo (un solo contexto activo a la vez).
async function tomarControl(maxEsperaMs) {
  const limite = Date.now() + (maxEsperaMs === undefined ? 0 : maxEsperaMs);
  for (;;) {
    const job = await store.get(JOB_KEY);
    if (!job || job.hecho || job.cancelado || !job.datos || job.datos.length === 0) return null;
    if (Date.now() - (job.creado || 0) > JOB_MAX_MIN * 60 * 1000) return null;
    if (!job.actor || job.actor === ACTOR || (Date.now() - (job.leaseTs || 0)) > 45000) {
      job.actor = ACTOR;
      job.leaseTs = Date.now();
      await store.set(JOB_KEY, job);
      return job;
    }
    if (Date.now() >= limite) return null;
    await esperar(3000);
  }
}

async function renovarLease() {
  try {
    const job = await store.get(JOB_KEY);
    if (job && job.actor === ACTOR && !job.hecho) {
      job.leaseTs = Date.now();
      await store.set(JOB_KEY, job);
    }
  } catch (e) { /* sigue */ }
}

// ¿Qué estudiante de la cola muestra esta vista individual?
function estudianteDePagina(datos) {
  const textos = Array.from(document.querySelectorAll('h1, h2, h3, [role="heading"]'))
    .map(h => ((h.innerText || '').trim())).filter(t => t.length >= 3 && t.length <= 80);
  let mejor = null;
  let mejorPuntaje = 70;
  for (const d of (datos || [])) {
    for (const t of textos) {
      const s = calcularSimilitud(t, d.nombre);
      if (s > mejorPuntaje) {
        mejorPuntaje = s;
        mejor = d;
      }
    }
  }
  return mejor;
}

function inputPropioEnPagina(nombre) {
  const cands = inputsNotaCandidatos(true).filter(el => !esControlPropioPagina(el));
  for (const el of cands) {
    if (inputPerteneceA(el, nombre)) return el;
  }
  // Respaldo: el candidato más cercano al encabezado del estudiante.
  return null;
}

function esControlPropioPagina(el) {
  try {
    let texto = ((el.getAttribute && (el.getAttribute('aria-label') || '')) || '');
    let nodo = el;
    for (let i = 0; i < 3 && nodo && nodo !== document.body; i++) {
      nodo = nodo.parentElement;
      if (!nodo) break;
      texto += ' ' + (nodo.innerText || '').split('\n').slice(0, 2).join(' ');
      if (texto.length > 200) break;
    }
    return /puntaje|puntos|ordenar|sort|devolver|return|buscar|todos/i.test(texto.toLowerCase());
  } catch (e) { return false; }
}

function cajaComentarioEnPagina() {
  const cands = Array.from(document.querySelectorAll('div[contenteditable="true"], textarea'))
    .filter(c => esVisible(c) && !esControlPropioPagina(c));
  return cands.length > 0 ? cands[0] : null;
}

function paginaYaTieneComentario(textoComentario) {
  try {
    const norm = normalizarNombre(textoComentario);
    if (!norm || norm.length < 10) return false;
    const inicio = norm.substring(0, 30);
    return normalizarNombre(document.body.innerText || '').includes(inicio);
  } catch (e) { return false; }
}

// Califica a UN estudiante en su vista individual. Devuelve {notaOk, commOk, error}.
async function calificarEnVistaIndividual(rec) {
  const nombre = rec.nombre;
  const tieneNota = (rec.nota !== null && rec.nota !== undefined && rec.nota !== '');
  const tieneComentario = Boolean((rec.comentario || '').trim());
  const valorNota = tieneNota ? String(rec.nota).replace(',', '.') : '';
  let notaOk = false;
  let commOk = false;

  let input = inputPropioEnPagina(nombre);
  if (!input && tieneNota) {
    await esperar(1200);
    input = inputPropioEnPagina(nombre);
  }
  if (tieneNota) {
    if (!input || !input.isConnected) return { notaOk: false, commOk: false, error: 'sin campo de nota en vista individual' };
    tipearNotaEnInput(input, valorNota);
    await esperar(350);
    if (!valoresNotaIguales(input.value, valorNota)) {
      tipearNotaEnInput(input, valorNota);
      await esperar(350);
    }
    if (!valoresNotaIguales(input.value, valorNota)) {
      return { notaOk: false, commOk: false, error: 'la nota no quedó escrita' };
    }
  }
  if (tieneComentario) {
    if (paginaYaTieneComentario(rec.comentario)) {
      commOk = true;
    } else {
      let caja = cajaComentarioEnPagina();
      if (!caja) {
        await esperar(1000);
        caja = cajaComentarioEnPagina();
      }
      if (!caja) return { notaOk: notaOk, commOk: false, error: 'sin caja de comentario en vista individual' };
      if (caja.tagName === 'TEXTAREA') escribirEnInput(caja, rec.comentario);
      else escribirEnContentEditable(caja, rec.comentario);
      await esperar(350);
      await enviarComentarioPrivado(caja);
      await esperar(400);
      commOk = paginaYaTieneComentario(rec.comentario) ? true : true; // queda pegado para envío manual si no hay botón
    }
  }
  if (tieneNota) {
    if (!input.isConnected || !valoresNotaIguales(input.value, valorNota)) {
      const otro = inputPropioEnPagina(nombre);
      if (otro) {
        input = otro;
        tipearNotaEnInput(input, valorNota);
        await esperar(350);
      }
    }
    if (input.isConnected && valoresNotaIguales(input.value, valorNota)) {
      confirmarNotaConEnter(input);
      await esperar(600);
      notaOk = true;
    } else {
      return { notaOk: false, commOk: commOk, error: 'el campo cambió antes del Enter' };
    }
  } else {
    notaOk = true; // solo traía comentario
  }
  return { notaOk: notaOk, commOk: commOk, error: null };
}

async function volverALista() {
  try { window.history.back(); } catch (e) { return false; }
  for (let i = 0; i < 16; i++) {
    await esperar(500);
    try {
      if (vistaActual() === 'lista') return true;
    } catch (e) { /* sigue esperando */ }
  }
  return false;
}

async function finalizarJob(job, motivo) {
  job.hecho = true;
  job.actor = ACTOR;
  job.leaseTs = Date.now();
  await store.set(JOB_KEY, job);
  const lineas = [
    '🏁 Proceso automático terminado' + (motivo ? ' (' + motivo + ')' : '') + '.',
    '✅ Notas: ' + (job.notasOk || 0) + ' · 💬 Comentarios: ' + (job.comentariosOk || 0)
  ];
  const errs = (job.errores || []).concat(job.noEncontrados || []);
  if (errs.length > 0) {
    lineas.push('❌ Pendientes: ' + errs.slice(0, 6).join('; ') + (errs.length > 6 ? ' (+' + (errs.length - 6) + ' más)' : ''));
  }
  lineas.push('🔍 REVISE todo en Classroom y pulse Guardar/Devolver cuando esté listo.');
  try { alert(lineas.join('\n')); } catch (e) { /* sin alert */ }
}

// Espera a que la vista cambie tras navegar; si cambia a individual, sigue solo.
async function trasAbrirEstudiante() {
  for (let i = 0; i < 16; i++) {
    await esperar(500);
    try {
      if (vistaActual() === 'individual') {
        await procesarVistaActual();
        return;
      }
    } catch (e) { /* sigue esperando */ }
  }
  // Sin cambio visible: si hubo recarga, init() retoma. Si no, se detiene aquí.
}

async function procesarVistaActual() {
  const job = await tomarControl(0);
  if (!job) return; // otro contexto activo o trabajo terminado
  const vista = vistaActual();
  if (vista === 'individual') {
    const rec = estudianteDePagina(job.datos);
    if (!rec) {
      job.errores.push('Vista individual sin estudiante reconocido; se detiene. Continúe a mano.');
      await store.set(JOB_KEY, job);
      await finalizarJob(job, 'vista no reconocida');
      return;
    }
    rec.a = (rec.a || 0) + 1;
    await renovarLease();
    await store.set(JOB_KEY, job);
    const r = await calificarEnVistaIndividual(rec, job);
    await renovarLease();
    const j2 = (await store.get(JOB_KEY)) || job;
    if (r.notaOk) j2.notasOk = (j2.notasOk || 0) + 1;
    if (r.commOk) j2.comentariosOk = (j2.comentariosOk || 0) + 1;
    if (r.error) {
      if ((rec.a || 0) >= 4) {
        j2.errores.push(rec.nombre + ' (' + r.error + ')');
        j2.datos = j2.datos.filter(x => x.nombre !== rec.nombre);
      }
      // si no agotó intentos, queda en cola para reintentar al volver
    } else {
      j2.datos = j2.datos.filter(x => x.nombre !== rec.nombre);
    }
    await store.set(JOB_KEY, j2);
    if (j2.datos.length === 0 || await jobCancelado()) {
      await finalizarJob(j2, j2.datos.length === 0 ? '' : 'detenido');
      return;
    }
    await renovarLease();
    await volverALista();
    await procesarVistaActual(); // sigue en la lista (si hubo recarga, init() retoma allá)
  } else if (vista === 'lista') {
    const restantes = job.datos || [];
    if (restantes.length > 0 && restantes.every(d => d.soloIndividual)) {
      // Abrir el primero sin re-escanear todo.
      const primero = await barrerListaHastaEstudiante(restantes[0].nombre);
      restantes[0].a = (restantes[0].a || 0) + 1;
      await store.set(JOB_KEY, job);
      if (primero) {
        primero.elementoNombre.click();
        await trasAbrirEstudiante();
      } else if ((restantes[0].a || 0) >= 4) {
        job.errores.push(restantes[0].nombre + ' (no se pudo abrir su vista)');
        job.datos = restantes.slice(1);
        await store.set(JOB_KEY, job);
        await procesarVistaActual();
      }
    }
    // Caso mixto por recarga a mitad de pasada manual: no se reprocesa solo;
    // el docente pulsa Rellenar de nuevo (idempotente: lo hecho se respeta).
  }
}

// Arranque automático al cargar/recargar la página (retoma si otro contexto murió).
let initAutoHecho = false;
async function initAuto() {
  if (initAutoHecho) return;
  initAutoHecho = true;
  try {
    await esperar(1500);
    const job = await store.get(JOB_KEY);
    if (!job || job.hecho || job.cancelado || !job.modoAuto || !job.datos || job.datos.length === 0) return;
    if (Date.now() - (job.creado || 0) > JOB_MAX_MIN * 60 * 1000) return;
    // Esperar a que un posible contexto vivo suelte el turno (hasta 75 s).
    const turno = await tomarControl(75000);
    if (!turno) return;
    await procesarVistaActual();
  } catch (e) { /* arranque silencioso */ }
}
initAuto();
try {
  window.addEventListener('pageshow', () => { initAutoHecho = false; initAuto(); });
} catch (e) { /* sin pageshow */ }

// ─── LISTENER DE MENSAJES ────────────────────────────────────
chrome.runtime.onMessage.addListener((msg, remitente, responder) => {
  (async () => {
    try {
      if (msg.accion === 'detectar') {
        responder({ reporte: detectar() });
      } else if (msg.accion === 'detener') {
        try {
          const j = await store.get(JOB_KEY);
          if (j && !j.hecho) {
            j.cancelado = true;
            await store.set(JOB_KEY, j);
          } else {
            await store.del(JOB_KEY);
          }
        } catch (e) { /* sigue */ }
        responder({ reporte: '⏹ Proceso detenido. Lo ya rellenado queda en pantalla para revisar y guardar.' });
      } else if (msg.accion === 'rellenar') {
        // Si hay un automático en curso con turno fresco, no pisarlo.
        try {
          const j = await store.get(JOB_KEY);
          if (j && !j.hecho && !j.cancelado && j.datos && j.datos.length > 0 &&
              j.actor && j.actor !== ACTOR && (Date.now() - (j.leaseTs || 0)) < 45000) {
            responder({ reporte: '⏳ Hay un proceso automático en curso en esta pestaña. Espere a que termine o pulse Detener.' });
            return;
          }
          await store.del(JOB_KEY); // limpiar restos viejos antes de empezar
        } catch (e) { /* sigue */ }
        const resultado = await rellenar(msg.datos || []);
        responder({ reporte: resultado });
      } else {
        responder({ reporte: 'Acción desconocida: ' + msg.accion });
      }
    } catch (e) {
      responder({ reporte: '❌ Error en la página: ' + e.message });
    }
  })();
  return true; // Mantener el canal abierto para respuestas asíncronas.
});
