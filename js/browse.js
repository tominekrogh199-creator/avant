/* Static results remain readable without JS. The URL keeps your search when you return. */
(() => {
  'use strict';
  const root = document.querySelector('[data-browser]');
  if (!root) return;
  const input = root.querySelector('input[type="search"]');
  const entries = [...root.querySelectorAll('[data-entry]')];
  const buttons = [...root.querySelectorAll('[data-filter]')];
  const clear = root.querySelector('[data-clear]');
  let category = 'all';
  const normalize = value => value.toLocaleLowerCase('nb').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ø/g, 'o').replace(/æ/g, 'ae');
  const index = entries.map(el => ({el, text: normalize(el.dataset.search)}));
  function update(save = true) {
    const query = input.value.trim();
    const terms = normalize(query).split(/\s+/).filter(Boolean);
    let visible = 0;
    index.forEach(({el, text}) => {
      const show = (category === 'all' || el.dataset.category === category) && terms.every(term => text.includes(term));
      el.hidden = !show;
      if (show) visible++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    const noun = root.dataset.noun === 'saker' ? (visible === 1 ? 'sak' : 'saker') : (visible === 1 ? 'merke' : 'merker');
    root.querySelector('[data-count]').textContent = `${visible} ${noun}` + ((query || category !== 'all') ? ` av ${entries.length}` : '');
    root.querySelector('[data-empty]').hidden = visible > 0;
    clear.hidden = !query && category === 'all';
    if (save) {
      try {
        const url = new URL(location.href);
        query ? url.searchParams.set('q', query) : url.searchParams.delete('q');
        category !== 'all' ? url.searchParams.set('type', category) : url.searchParams.delete('type');
        url.hash = '';
        history.replaceState(null, '', url);
      } catch (_) { /* file:// and restricted browser contexts still work */ }
    }
  }
  function restore() {
    const params = new URLSearchParams(location.search);
    input.value = params.get('q') || '';
    const requested = params.get('type');
    category = buttons.some(b => b.dataset.filter === requested) ? requested : 'all';
    let target = null;
    try { target = entries.find(el => el.id && el.id === decodeURIComponent(location.hash.slice(1))); } catch (_) {}
    if (target) { input.value = ''; category = 'all'; }
    update(false);
  }
  function reset() { input.value = ''; category = 'all'; update(); input.focus(); }
  input.addEventListener('input', () => update());
  input.addEventListener('search', () => update());
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  root.querySelector('[data-reset]').addEventListener('click', reset);
  clear.addEventListener('click', reset);
  window.addEventListener('pageshow', restore);
  window.addEventListener('popstate', restore);
  window.addEventListener('hashchange', restore);
  root.querySelector('[data-controls]').hidden = false;
  restore();
})();
