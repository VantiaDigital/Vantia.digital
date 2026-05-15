/* ============================================
   VANTIA DIGITAL - COMPONENTS LOADER
   Inyecta header/footer/modales/whatsapp via fetch
   Dispara 'components:loaded' al terminar
   ============================================ */

(() => {
  'use strict';

  // Detecta el path base: si estamos en /pages/x.html, base = ..; si en /index.html, base = '.'
  function getBase() {
    const path = window.location.pathname.replace(/\\/g, '/');
    if (path.includes('/pages/')) return '..';
    return '.';
  }

  async function loadInto(placeholder, url) {
    try {
      const res = await fetch(url, { cache: 'no-cache' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      let html = await res.text();

      // Reescribe paths relativos a la página actual
      const base = getBase();
      // href="/..." y src="/..." ya son absolutos, ok
      // href="index.html" o "pages/x.html" → re-prefijar con base si estamos en /pages/
      // Más simple: usar siempre paths absolutos en los componentes (con "/")

      placeholder.innerHTML = html;
      // Mueve los hijos al nivel del placeholder (para no romper estilos)
      const fragment = document.createDocumentFragment();
      while (placeholder.firstChild) fragment.appendChild(placeholder.firstChild);
      placeholder.replaceWith(fragment);
    } catch (err) {
      console.error('[components-loader]', url, err);
    }
  }

  async function loadAll() {
    const base = getBase();
    const tasks = [];

    document.querySelectorAll('[data-component]').forEach((placeholder) => {
      const name = placeholder.dataset.component;
      const url = `${base}/components/${name}.html`;
      tasks.push(loadInto(placeholder, url));
    });

    await Promise.all(tasks);
    window.__componentsLoaded = true;
    document.dispatchEvent(new CustomEvent('components:loaded'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadAll);
  } else {
    loadAll();
  }
})();
