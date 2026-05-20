/* ============================================
   VANTIA DIGITAL - EVENTOS GA4 PERSONALIZADOS
   Mide clics de botones clave para analizarlos por separado.

   Respeta el consentimiento: gtag() siempre existe (shim de
   dataLayer en consent.js). Si el usuario aceptó analíticas,
   GA4 envía el evento; si no, queda en dataLayer sin enviarse.

   Delegación en document → funciona también con elementos
   inyectados por componentes (header, footer, whatsapp, modales).
   ============================================ */

(() => {
  'use strict';

  function track(name, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, params || {});
  }

  function clean(txt) {
    return (txt || '').replace(/\s+/g, ' ').trim().slice(0, 90);
  }

  // Nombre de la página actual para el parámetro 'ubicacion'
  function pageName() {
    const p = window.location.pathname;
    if (p === '/' || p.endsWith('/index.html')) return 'home';
    const m = p.match(/\/([^\/]+)\.html$/);
    return m ? m[1] : 'otra';
  }

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

    // Caso de éxito
    const caso = t.closest('article.case');
    if (caso) {
      const name = caso.querySelector('.case__name');
      track('click_caso', { caso: clean(name && name.textContent) || 'desconocido' });
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

  // -------- Envío del formulario de contacto --------
  document.addEventListener('submit', (e) => {
    if (e.target && e.target.id === 'contactForm') {
      const asunto = e.target.querySelector('#cf-inquiry');
      track('enviar_formulario', {
        asunto: asunto ? clean(asunto.value) : ''
      });
    }
  }, true);
})();
