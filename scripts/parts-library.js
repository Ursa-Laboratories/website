const byId = id => document.getElementById(id);
const canvas = byId('part-canvas');
const status = byId('model-status');
const list = byId('parts-list');
const fields = {
  q: byId('parts-search'), configuration: byId('configuration'),
  category: byId('category'), format: byId('format'), availability: byId('availability'),
};
let parts = [];
let selected = null;
let selectionVersion = 0;
let preview;
let previewPromise;
let hasModel = false;

function modelStatus(message) {
  status.textContent = message;
  status.hidden = !message;
}

function controlsEnabled(enabled) {
  hasModel = enabled;
  document.querySelectorAll('.view-toolbar button').forEach(button => { button.disabled = !enabled; });
}

function updateUrl(push = false) {
  const url = new URL(location.href);
  for (const [key, element] of Object.entries(fields)) {
    if (element.value.trim()) url.searchParams.set(key, element.value.trim());
    else url.searchParams.delete(key);
  }
  if (selected) url.searchParams.set('part', selected.id);
  else url.searchParams.delete('part');
  history[push ? 'pushState' : 'replaceState'](null, '', url);
}

function readFilters() {
  const params = new URLSearchParams(location.search);
  for (const [key, element] of Object.entries(fields)) element.value = params.get(key) || '';
}

function formatBytes(bytes) {
  return bytes >= 1e6 ? `${(bytes / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1000))} KB`;
}

function matches(part) {
  const terms = fields.q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const text = `${part.label} ${part.subgroup} ${part.sources.join(' ')} ${part.summary} ${part.configuration} ${part.category}`.toLowerCase();
  if (!terms.every(term => text.includes(term))) return false;
  for (const key of ['configuration', 'category']) if (fields[key].value && part[key] !== fields[key].value) return false;
  if (fields.format.value && !part.formats.includes(fields.format.value)) return false;
  switch (fields.availability.value) {
    case 'preview': return Boolean(part.file);
    case 'missing': return !part.file;
    case 'notes': return Boolean(part.readme);
    case 'local': return part.local_changes;
    default: return true;
  }
}

function renderList() {
  const visible = parts.filter(matches);
  const fragment = document.createDocumentFragment();
  for (const part of visible) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'part-option';
    button.dataset.part = part.id;
    button.setAttribute('aria-pressed', String(selected?.id === part.id));
    const title = document.createElement('strong');
    title.textContent = part.label;
    const folder = document.createElement('small');
    folder.textContent = part.subgroup;
    const meta = document.createElement('small');
    meta.className = 'option-meta';
    meta.textContent = `${part.formats.join(' · ')}${part.file ? '' : ' · No 3D preview'}`;
    button.append(title, folder, meta);
    button.addEventListener('click', () => {
      selectPart(part, true);
      if (matchMedia('(max-width: 760px)').matches) {
        document.querySelector('.inspector-heading').scrollIntoView({ behavior: 'instant', block: 'start' });
      }
    });
    fragment.append(button);
  }
  list.replaceChildren(fragment);
  list.hidden = !visible.length;
  byId('empty-results').hidden = Boolean(visible.length);
  byId('result-count').textContent = `${visible.length} of ${parts.length} parts`;
}

async function selectPart(part, push = false, writeUrl = true) {
  const version = ++selectionVersion;
  selected = part;
  preview?.clear();
  controlsEnabled(false);
  byId('part-dimensions').textContent = '';
  byId('part-title').textContent = part.label;
  byId('part-location').textContent = part.subgroup;
  byId('part-summary').textContent = part.summary || 'Open the source files to inspect or modify this part.';
  byId('part-notice').textContent = part.desc;
  byId('local-notice').hidden = !part.local_changes;
  byId('part-formats').textContent = `${part.configuration} / ${part.category} · ${part.formats.join(', ')}`;
  canvas.setAttribute('aria-label', `3D preview of ${part.label}. Arrow keys rotate; plus and minus zoom.`);
  const notes = byId('part-notes');
  notes.hidden = !part.readme;
  if (part.readme) {
    notes.href = part.readme.url || part.readme.download;
    notes.textContent = part.readme.url ? 'Part notes ↗' : 'Snapshot notes ↗';
  } else notes.removeAttribute('href');
  byId('part-files').replaceChildren(...part.source_files.map(source => {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = source.download;
    link.download = source.name;
    const name = document.createElement('span');
    name.className = 'file-name';
    name.textContent = source.name;
    const size = document.createElement('span');
    size.className = 'file-size';
    size.textContent = `${formatBytes(source.bytes)} ↓`;
    link.append(name, size);
    li.append(link);
    return li;
  }));
  const download = byId('preview-download');
  download.hidden = !part.file;
  if (part.file) {
    download.href = part.file;
    download.download = `${part.id}${part.file.endsWith('.glb') ? '.glb' : '.stl'}`;
  } else download.removeAttribute('href');
  byId('share-part').disabled = false;
  byId('share-part').textContent = 'Copy link';
  list.querySelectorAll('.part-option').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.part === part.id)));
  if (writeUrl) updateUrl(push);
  if (!part.file) {
    modelStatus(part.preview_error || 'No 3D preview yet. The original source files are available below.');
    return;
  }
  modelStatus('Loading 3D preview…');
  try {
    // Catalog, filtering, and downloads remain useful if WebGL or the CDN fails.
    previewPromise ||= import('./part-preview.js').then(module => {
      preview = module.createPreview(canvas, message => { controlsEnabled(false); modelStatus(message); });
      return preview;
    });
    const viewer = await previewPromise;
    if (version !== selectionVersion) return;
    const dimensions = await viewer.load(part);
    if (version !== selectionVersion || !dimensions) return;
    byId('part-dimensions').textContent = `${dimensions.map(n => n.toLocaleString(undefined, { maximumFractionDigits: 1 })).join(' × ')} model units`;
    byId('part-dimensions').title = 'X × Y × Z bounding box. STL does not encode a physical unit; confirm units in the source CAD.';
    controlsEnabled(true);
    modelStatus('');
  } catch (error) {
    if (version !== selectionVersion || error.name === 'AbortError') return;
    modelStatus('3D preview unavailable. You can still download the source files below. Reload to try again.');
  }
}

for (const element of Object.values(fields)) {
  element.addEventListener(element.type === 'search' ? 'input' : 'change', () => { renderList(); updateUrl(); });
}
byId('clear-filters').addEventListener('click', () => {
  Object.values(fields).forEach(element => { element.value = ''; });
  renderList();
  updateUrl();
  fields.q.focus();
});
document.querySelectorAll('[data-view]').forEach(button => {
  button.addEventListener('click', () => { if (hasModel) preview.setView(button.dataset.view); });
});
byId('wireframe').addEventListener('click', event => {
  const enabled = event.currentTarget.getAttribute('aria-pressed') !== 'true';
  event.currentTarget.setAttribute('aria-pressed', String(enabled));
  preview?.setWireframe(enabled);
});
byId('reset-view').addEventListener('click', () => {
  byId('wireframe').setAttribute('aria-pressed', 'false');
  preview?.setWireframe(false);
  preview?.setView('iso');
});
byId('share-part').addEventListener('click', async () => {
  const url = new URL(location.href);
  url.search = '';
  url.searchParams.set('part', selected.id);
  try {
    await navigator.clipboard.writeText(url.href);
    byId('share-part').textContent = 'Copied';
    byId('share-status').textContent = 'Part link copied to clipboard.';
  } catch {
    byId('share-status').textContent = 'Copy the part URL from the address bar.';
    byId('share-part').textContent = 'Use address bar';
  }
});
window.addEventListener('popstate', () => {
  readFilters();
  const id = new URLSearchParams(location.search).get('part');
  const part = parts.find(item => item.id === id);
  renderList();
  if (part) selectPart(part, false, false);
});

try {
  const response = await fetch('assets/cad/catalog.json');
  if (!response.ok) throw new Error('Catalog request failed');
  const catalog = await response.json();
  parts = catalog.parts;
  byId('total-parts').textContent = parts.length;
  byId('total-files').textContent = parts.reduce((sum, part) => sum + part.sources.length, 0);
  byId('total-previews').textContent = parts.filter(part => part.file).length;
  for (const key of ['configuration', 'category', 'format']) {
    const options = [...new Set(parts.flatMap(part => key === 'format' ? part.formats : [part[key]]))].sort();
    for (const value of options) fields[key].add(new Option(value, value));
  }
  readFilters();
  const stamp = new Date(catalog.generated_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  const local = parts.filter(part => part.local_changes).length;
  byId('catalog-snapshot').textContent = `Snapshot ${stamp} · Cubware ${catalog.source_revision.slice(0, 7)} · ${local} entries with local changes`;
  const requested = new URLSearchParams(location.search).get('part');
  const first = parts.find(part => part.id === requested)
    || parts.find(part => part.source.endsWith('ForceSensorMountFront.stl')) || parts[0];
  renderList();
  if (first) {
    await selectPart(first);
    const active = list.querySelector('[aria-pressed="true"]');
    if (active) list.scrollTop = active.offsetTop - list.offsetTop;
    if (requested && requested !== first.id) {
      byId('share-status').classList.remove('visually-hidden');
      byId('share-status').textContent = 'That part is no longer in the snapshot. Showing an available part.';
    }
  } else {
    modelStatus('No CAD parts are included in this snapshot.');
  }
} catch {
  byId('result-count').textContent = 'Catalog unavailable';
  modelStatus('Could not load the parts library. Please reload or browse the repository above.');
}
