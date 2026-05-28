/* ============================================
   VANTIA DIGITAL - COMPONENTS LOADER
   Inyecta header/footer/modales/whatsapp via fetch
   Dispara 'components:loaded' al terminar
   ============================================ */

(() => {
  'use strict';

  // Detecta el path base contando cuántos niveles de profundidad estamos
  // desde la raíz del sitio. Soporta:
  //   /index.html              → '.'    (raíz)
  //   /pages/casos.html        → '..'   (1 nivel)
  //   /pages/casos/gett.html   → '../..' (2 niveles)
  //   etc.
  function getBase() {
    const path = window.location.pathname.replace(/\\/g, '/');
    // Quitar query string si lo hubiera (no aplica a pathname, pero por seguridad)
    const cleanPath = path.split('?')[0];
    // Segmentos del path, sin el archivo final (los que terminan en .html o son vacíos)
    const segments = cleanPath.split('/').filter((s) => s && !/\.html?$/i.test(s));
    if (segments.length === 0) return '.';
    return new Array(segments.length).fill('..').join('/');
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
