/* ============================================
   VANTIA DIGITAL - EVENTOS PERSONALIZADOS (dataLayer)
   Mide clics de botones clave para analizarlos por separado.

   Empuja eventos al dataLayer. Google Tag Manager los lee
   con triggers de "Evento personalizado" y dispara los tags
   de GA4. El Consent Mode (consent.js) controla si GA4 los
   envía — este archivo no depende del consentimiento.

   Delegación en document → funciona también con elementos
   inyectados por componentes (header, footer, whatsapp, modales).
   ============================================ */

(() => {
  'use strict';

  function track(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params || {}));
  }

  function clean(txt) {
    return (txt || '').replace(/\s+/g, ' ').trim().slice(0, 90);
  }

  // Nombre de la página actual para el parámetro 'ubicacion'
  function pageName() {
    const p = window.location.pathname;
    if (p === '/' || p.endsWith('/index.html')) return 'home';
    // Páginas de detalle de caso: /casos/<slug> → "caso_<slug>"
    const casoMatch = p.match(/\/casos\/([^\/]+)$/);
    if (casoMatch) return 'caso_' + casoMatch[1];
    const m = p.match(/\/([^\/]+)\/?$/);
    return m ? m[1] : 'otra';
  }

  // Si estamos en una página de detalle de caso, disparar ver_caso_detalle
  // una vez al cargar (complementa el page_view automático de GA4).
  (function fireCaseDetailView() {
    const m = window.location.pathname.match(/\/casos\/([^\/]+)$/);
    if (m && m[1]) {
      track('ver_caso_detalle', { caso: m[1] });
    }
  })();

  function socialNet(href) {
    if (!href) return null;
    if (href.indexOf('instagram.com') > -1) return 'instagram';
    if (href.indexOf('tiktok.com') > -1) return 'tiktok';
    if (href.indexOf('youtube.com') > -1) return 'youtube';
    if (href.indexOf('linkedin.com') > -1) return 'linkedin';
    return null;
  }

  // -------- Clics (fase de captura: corre antes de navegar) --------
  document.addEventListener('click', (e) => {
    const t = e.target;
    if (!t || !t.closest) return;

    // WhatsApp (botón flotante o tarjeta de contacto)
    const wa = t.closest('.whatsapp-fab, a[href*="wa.me"], .channel--whatsapp');
    if (wa) {
      track('click_whatsapp', {
        ubicacion: wa.classList.contains('whatsapp-fab') ? 'boton_flotante' : pageName()
      });
      return;
    }

    // Agendar llamada (Calendly)
    const cal = t.closest('a[href*="calendly.com"]');
    if (cal) {
      track('click_agendar_llamada', { ubicacion: pageName() });
      return;
    }

    // Pedir presupuesto (abre el modal de presupuesto)
    const budget = t.closest('[data-budget]');
    if (budget) {
      track('abrir_presupuesto', { servicio: clean(budget.dataset.budget) });
      return;
    }

    // Abrir detalle de un servicio (pilares / modales)
    const svc = t.closest('[data-modal-trigger]');
    if (svc) {
      track('abrir_servicio', { servicio: clean(svc.dataset.modalTrigger) });
      return;
    }

    // Email
    const mail = t.closest('a[href^="mailto:"]');
    if (mail) {
      track('click_email', { ubicacion: pageName() });
      return;
    }

    // Caso de éxito (3 acciones distintas dentro de la card):
    //   - cover-link → abre página de detalle del caso
    //   - case__action a *.vantia.digital → ver sitio en vivo del cliente
    //   - case__action a /contacto → pedir presupuesto similar
    const caso = t.closest('article.case');
    if (caso) {
      let accion = 'ver_detalle';
      const action = t.closest('.case__action');
      if (action) {
        if (action.href && action.href.indexOf('/contacto') > -1) {
          accion = 'pedir_presupuesto';
        } else {
          accion = 'ver_sitio_vivo';
        }
      }
      const name = caso.querySelector('.case__name');
      track('click_caso', {
        caso: clean(name && name.textContent) || 'desconocido',
        accion: accion
      });
      return;
    }

    // Redes sociales
    const link = t.closest('a[href]');
    if (link) {
      const red = socialNet(link.href);
      if (red) {
        track('click_red_social', { red: red, ubicacion: pageName() });
        return;
      }
    }

    // Navegación del header
    const nav = t.closest('a.nav__link[data-nav]');
    if (nav) {
      track('click_navegacion', { destino: clean(nav.dataset.nav) });
      return;
    }
  }, true);

  // -------- Envío de formularios --------
  document.addEventListener('submit', (e) => {
    const f = e.target;
    if (!f || !f.checkValidity) return;

    // Formulario de contacto (solo si pasa la validación HTML5)
    if (f.id === 'contactForm' && f.checkValidity()) {
      const asunto = f.querySelector('#cf-inquiry');
      track('enviar_formulario', { asunto: asunto ? clean(asunto.value) : '' });
      return;
    }

    // Solicitud de presupuesto (formularios de los modales)
    if (f.matches && f.matches('.budget-modal__form, .modal__form') && f.checkValidity()) {
      track('enviar_presupuesto', { servicio: clean(f.dataset.service || '') });
    }
  }, true);

  // -------- Inicio del formulario de contacto (embudo) --------
  // Dispara una sola vez, cuando el usuario interactúa por primera vez.
  let formStartFired = false;
  document.addEventListener('focusin', (e) => {
    if (formStartFired) return;
    const t = e.target;
    if (t && t.closest && t.closest('#contactForm')) {
      formStartFired = true;
      track('form_start', { ubicacion: pageName() });
    }
  }, true);

  // -------- Secciones vistas al hacer scroll --------
  // Dispara una vez por sección cuando entra al 50% en pantalla.
  function initSectionTracking() {
    if (!('IntersectionObserver' in window)) return;
    const seen = {};
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const sec = entry.target;
        const name = clean(sec.dataset.section || (sec.className || '').split(' ')[0] || 'seccion');
        if (!seen[name]) {
          seen[name] = true;
          track('ver_seccion', { seccion: name });
        }
        obs.unobserve(sec);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('section').forEach((s) => obs.observe(s));
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSectionTracking);
  } else {
    initSectionTracking();
  }
})();
