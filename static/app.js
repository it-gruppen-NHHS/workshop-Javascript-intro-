const lessons = JSON.parse(document.getElementById('lessons-data').textContent);
const $ = (id) => document.getElementById(id);
let saved = {};
try { saved = JSON.parse(localStorage.getItem('kodeverkstad-v1')) || {}; } catch {}
if (typeof saved !== 'object' || Array.isArray(saved)) saved = {};
let current = 0;
let worker = null;
let timeout = null;
let preview = null;

function state() {
  const id = lessons[current].id;
  if (!saved[id] || typeof saved[id] !== 'object') saved[id] = {};
  return saved[id];
}
function persist() {
  try { localStorage.setItem('kodeverkstad-v1', JSON.stringify(saved)); } catch {}
}
function stop() {
  if (worker) worker.terminate();
  worker = null;
  clearTimeout(timeout);
  $('run').disabled = false;
}
function navigation() {
  $('lesson-nav').replaceChildren();
  lessons.forEach((lesson, index) => {
    if (index === 0 || lesson.level !== lessons[index - 1].level) {
      const heading = document.createElement('h3');
      heading.className = 'level-heading';
      heading.textContent = lesson.level;
      $('lesson-nav').append(heading);
    }
    const button = document.createElement('button');
    button.className = 'lesson-link';
    if (index === current) button.setAttribute('aria-current', 'step');
    const number = document.createElement('span');
    number.className = 'number';
    number.textContent = saved[lesson.id]?.done ? '✓' : String(index + 1).padStart(2, '0');
    const text = document.createElement('span');
    const title = document.createElement('strong');
    title.textContent = lesson.title;
    const topic = document.createElement('small');
    topic.textContent = lesson.topic + (saved[lesson.id]?.done ? ' · Fullført' : '');
    text.append(title, topic);
    button.append(number, text);
    button.addEventListener('click', () => { current = index; render(); });
    $('lesson-nav').append(button);
  });
  const count = lessons.filter((lesson) => saved[lesson.id]?.done).length;
  $('progress').value = count;
  $('progress-count').textContent = `${count} / ${lessons.length}`;
}
function hints() {
  const opened = Array.isArray(state().openHints) ? state().openHints :
    [0, 1, 2].filter(index => index < (Number(state().hints) || 0));
  $('hint-buttons').replaceChildren();
  $('hint-content').replaceChildren();
  ['1 · Litt hjelp', '2 · Meir hjelp', '3 · Fasiten'].forEach((label, index) => {
    const button = document.createElement('button');
    button.textContent = label;
    button.type = 'button';
    button.setAttribute('aria-expanded', String(opened.includes(index)));
    button.setAttribute('aria-controls', `hint-${index}`);
    button.addEventListener('click', () => {
      state().openHints = opened.includes(index) ? opened.filter(value => value !== index) : [...opened, index];
      persist();
      hints();
      $('hint-buttons').children[index].focus();
    });
    $('hint-buttons').append(button);
    const detail = document.createElement('div');
    detail.id = `hint-${index}`;
    detail.hidden = !opened.includes(index);
    detail.className = 'hint-detail' + (index === 2 ? ' solution' : '');
    detail.textContent = lessons[current].hints[index];
    $('hint-content').append(detail);
  });
}
function render() {
  stop();
  const lesson = lessons[current];
  preview = null;
  $('preview-host').replaceChildren();
  $('preview-panel').hidden = lesson.mode !== 'dom';
  $('html-panel').hidden = lesson.mode !== 'dom';
  $('html-panel').open = lesson.mode === 'dom';
  $('html-source').textContent = lesson.html || '';
  $('lesson-number').textContent = `OPPGÅVE ${String(current + 1).padStart(2, '0')} AV ${lessons.length}`;
  $('lesson-topic').textContent = lesson.topic;
  $('lesson-title').textContent = lesson.title;
  $('lesson-description').textContent = lesson.description;
  $('code').value = typeof state().code === 'string' ? state().code : lesson.starter;
  $('output').textContent = 'Resultatet av koden din dukkar opp her.';
  $('feedback').textContent = '';
  $('run-state').textContent = 'Klar når du er';
  $('lesson-position').textContent = `${current + 1} av ${lessons.length} oppgåver`;
  $('next').disabled = current === lessons.length - 1;
  navigation();
  hints();
}
$('code').addEventListener('input', () => { state().code = $('code').value; persist(); });
$('reset').addEventListener('click', () => {
  state().code = lessons[current].starter;
  state().hints = 0;
  state().openHints = [];
  persist();
  render();
});
$('next').addEventListener('click', () => { if (current < lessons.length - 1) { current++; render(); } });
$('code').addEventListener('keydown', (event) => {
  if (event.key === 'Tab' && !event.ctrlKey && !event.metaKey && !event.altKey) {
    event.preventDefault();
    const editor = event.currentTarget;
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    if (event.shiftKey) {
      const lineStart = editor.value.lastIndexOf('\n', start - 1) + 1;
      const indent = editor.value.slice(lineStart).match(/^( {1,2}|\t)/)?.[0].length || 0;
      if (indent) {
        editor.setRangeText('', lineStart, lineStart + indent, 'preserve');
      }
    } else {
      editor.setRangeText('  ', start, end, 'end');
    }
    editor.dispatchEvent(new Event('input', { bubbles: true }));
  }
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); run(); }
});

// A separate worker keeps an accidental infinite loop from freezing the page.
// This is a local learning playground, not a sandbox for untrusted third-party code.
function run() {
  stop();
  if (lessons[current].mode === 'dom') { runDOM(); return; }
  $('run').disabled = true;
  $('feedback').textContent = '';
  $('run-state').textContent = 'Køyrer …';
  $('output').textContent = '';
  const source = `
    self.onmessage = async ({data: {code}}) => {
      const lines = [];
      let hasError = false;
      const format = value => typeof value === 'string' ? value :
        (typeof value === 'object' && value !== null ? JSON.stringify(value) : String(value));
      const log = (...args) => {
        if (lines.length >= 100) throw new Error('For mange utskrifter. Prøv ei kortare løkke.');
        const line = args.map(format).join(' ');
        if (line.length > 10000) throw new Error('Resultatet er for langt.');
        lines.push(line);
        self.postMessage({lines, pending: true});
      };
      try {
        const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
        const result = await new AsyncFunction('console', code)(
          { log, info: log, warn: log, error: (...args) => { hasError = true; log(...args); } });
        if (result !== undefined) log(result);
        self.postMessage({lines, hasError});
      } catch (error) { self.postMessage({lines, error: error.name + ': ' + error.message}); }
    };
  `;
  const url = URL.createObjectURL(new Blob([source], {type: 'text/javascript'}));
  try { worker = new Worker(url); }
  catch { URL.revokeObjectURL(url); fail('Nettlesaren kunne ikkje starte koden. Prøv ein oppdatert nettlesar.'); return; }
  URL.revokeObjectURL(url);
  worker.onmessage = ({data}) => {
    if (!data || !Array.isArray(data.lines)) { fail('Uventa resultat frå koden.'); return; }
    $('output').textContent = data.lines.join('\n') || '(Ingen utskrift enno)';
    if (data.pending) return;
    stop();
    if (data.error) { fail(data.error, true); return; }
    complete(!data.hasError);
  };
  worker.onerror = () => fail('Koden kunne ikkje køyrast. Sjå etter skrivefeil og prøv igjen.');
  timeout = setTimeout(() => fail('Koden brukte for lang tid og vart stoppa. Sjekk at løkka di tek slutt.', true), 2000);
  worker.postMessage({code: $('code').value});
}
function fail(message, append = false) {
  stop();
  $('run-state').textContent = 'Prøv igjen';
  $('output').textContent = (append ? $('output').textContent + '\n' : '') + message;
  $('feedback').className = 'error';
  $('feedback').textContent = 'Det er noko feil. Sjå feilmeldinga i resultatfeltet.';
}
$('run').addEventListener('click', run);
render();

function complete(correct) {
  $('run-state').textContent = correct ? '✓ Koden er køyrd' : 'Det er noko feil';
  $('feedback').className = correct ? 'success' : 'error';
  $('feedback').textContent = correct
    ? 'Koden køyrde utan feil. Resultatet er vist over.'
    : 'Det er noko feil. Sjå feilmeldinga i resultatfeltet.';
  if (correct) {
    state().done = true;
    persist();
    navigation();
  }
}
function runDOM() {
  const lesson = lessons[current];
  $('run').disabled = true;
  $('run-state').textContent = 'Køyrer …';
  $('feedback').textContent = '';
  $('output').textContent = '';
  preview = document.createElement('iframe');
  preview.title = 'Resultatet av JavaScript-oppgåva';
  preview.setAttribute('sandbox', 'allow-scripts');
  const config = JSON.stringify({code: $('code').value,
    api: new URL('/api/users', location.href).href}).replace(/</g, '\\u003c');
  const runner = `
    const config = ${config};
    const lines = [];
    let hasError = false;
    const send = parent.postMessage.bind(parent);
    const log = (...args) => {
      if (lines.length < 100) lines.push(args.map(value => typeof value === 'object' && value !== null ? JSON.stringify(value) : String(value)).join(' ').slice(0, 10000));
      send({kind:'lesson', lines, pending:true, hasError}, '*');
    };
    window.addEventListener('error', e => send({kind:'lesson', error:e.message, lines}, '*'));
    window.addEventListener('unhandledrejection', e => send({kind:'lesson', error:String(e.reason), lines}, '*'));
    (async () => {
      try {
        const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
        const result = await new AsyncFunction('API_URL', 'console', config.code)(config.api,
          {log, info:log, warn:log, error:(...args) => { hasError = true; log(...args); }});
        if (result !== undefined) log(result);
        send({kind:'lesson', lines, hasError}, '*');
      } catch (error) { send({kind:'lesson', error:error.message, lines}, '*'); }
    })();
  `;
  preview.srcdoc = '<!doctype html><html lang="nn"><meta charset="utf-8"><style>body{font:15px system-ui;padding:16px;color:#192e2a}button{padding:8px 14px;cursor:pointer}td,th{padding:8px;text-align:left;border-bottom:1px solid #ddd}table{border-collapse:collapse}</style>'
    + lesson.html + '<script>' + runner + '</scr' + 'ipt></html>';
  $('preview-host').replaceChildren(preview);
  timeout = setTimeout(() => {
    preview = null;
    $('preview-host').replaceChildren();
    fail('Kontrollen tok for lang tid. Sjekk API-kallet og om løkker tek slutt.');
  }, 10000);
}
window.addEventListener('message', event => {
  if (!preview || event.source !== preview.contentWindow || event.data?.kind !== 'lesson') return;
  $('output').textContent = Array.isArray(event.data.lines) ? event.data.lines.join('\n') : '';
  if (event.data.pending) {
    if (event.data.hasError) complete(false);
    return;
  }
  stop();
  if (event.data.error) { fail(event.data.error, true); return; }
  $('output').textContent ||= '(Ingen utskrift. Sjå førehandsvisinga under.)';
  complete(!event.data.hasError);
});
