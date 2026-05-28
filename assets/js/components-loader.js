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

      // Los <script> insertados via innerHTML NO se ejecutan: hay que re-crearlos.
      const inertScripts = Array.from(fragment.querySelectorAll('script'));

      placeholder.replaceWith(fragment);

      // Re-crea cada <script> para forzar su ejecución (banner de cookies, etc.)
      inertScripts.forEach((old) => {
        const s = document.createElement('script');
        for (const attr of old.attributes) s.setAttribute(attr.name, attr.value);
        s.textContent = old.textContent;
        old.replaceWith(s);
      });
    } catch (err) {
      console.error('[components-loader]', url, err);
    }
  }

  // Lista canónica de componentes que cada página debería incluir.
  // Si alguno falta, se emite un warning para detectarlo en consola.
  const EXPECTED_COMPONENTS = ['header', 'footer', 'whatsapp', 'cookie-banner'];

  async function loadAll() {
    const base = getBase();
    const tasks = [];
    const foundNames = new Set();

    document.querySelectorAll('[data-component]').forEach((placeholder) => {
      const name = placeholder.dataset.component;
      foundNames.add(name);
      const url = `${base}/components/${name}.html`;
      tasks.push(loadInto(placeholder, url));
    });

    // Warning de componentes esperados que no están en esta página.
    EXPECTED_COMPONENTS.forEach((name) => {
      if (!foundNames.has(name)) {
        console.warn(`[components-loader] Falta placeholder esperado: data-component="${name}"`);
      }
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
