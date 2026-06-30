/* ============================================
   VANTIA DIGITAL - MODAL CONTROLLER
   - Modales de detalle de servicio
   - Mini budget-modal por encima
   - Event delegation (compatible con componentes async)
   ============================================ */

(() => {
  'use strict';

  let activeModal = null;       // modal de servicio activo
  let activeBudget = null;       // budget modal activo
  let lastFocused = null;

  // Idioma activo (lo gestiona i18n.js). Fallback a 'es'.
  function lang() {
    return (window.VantiaI18n && window.VantiaI18n.get()) ||
           document.documentElement.getAttribute('lang') || 'es';
  }
  // Nombre del servicio en EN (los data-budget vienen en español, canónico)
  const SERVICE_EN = {
    'Optimización Web': 'Web Optimisation',
    'SEO Técnico / GEO': 'Technical SEO / GEO',
    'Campañas de anuncios': 'Ad Campaigns',
    'Gestión de Redes Sociales': 'Social Media Management',
    'Email Marketing': 'Email Marketing',
  };
  function serviceLabel(name) {
    return (lang() === 'en' && SERVICE_EN[name]) ? SERVICE_EN[name] : name;
  }

  function lockBody() {
    if (!document.body.classList.contains('modal-open')) {
      document.body.classList.add('modal-open');
      document.body.classList.remove('is-pillar-active');
      if (window.__lenis) window.__lenis.stop();
    }
  }

  function unlockBody() {
    // Solo desbloqueá si NADA está abierto
    if (!activeModal && !activeBudget) {
      document.body.classList.remove('modal-open');
      if (window.__lenis) window.__lenis.start();
    }
  }

  // -------- SERVICE MODAL --------
  function getServiceOverlay() {
    return document.querySelector('[data-modal-overlay]');
  }

  function openModal(id) {
    const overlay = getServiceOverlay();
    if (!overlay) return;
    const modal = document.getElementById(`modal-${id}`);
    if (!modal) return;

    lastFocused = document.activeElement;

    overlay.querySelectorAll('.modal').forEach((m) => {
      m.classList.remove('is-open');
      m.setAttribute('aria-hidden', 'true');
    });

    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');

    lockBody();

    requestAnimationFrame(() => {
      const focusable = modal.querySelector('.modal__close, a, button, input, textarea, select');
      if (focusable) focusable.focus();
    });

    activeModal = modal;
  }

  function closeModal() {
    const overlay = getServiceOverlay();
    if (!overlay || !activeModal) return;

    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    activeModal.classList.remove('is-open');
    activeModal.setAttribute('aria-hidden', 'true');
    activeModal = null;

    unlockBody();

    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  // -------- BUDGET MODAL --------
  function getBudgetOverlay() {
    return document.querySelector('[data-budget-overlay]');
  }

  function openBudgetModal(serviceName) {
    const overlay = getBudgetOverlay();
    if (!overlay) return;
    const modal = overlay.querySelector('.budget-modal');
    if (!modal) return;

    // Setear nombre del servicio (traducido para mostrar)
    modal.querySelectorAll('[data-budget-service-target]').forEach((el) => {
      el.textContent = serviceLabel(serviceName);
    });
    // Guardar el nombre canónico (español) en el form para el submit
    const form = modal.querySelector('form');
    if (form) form.dataset.service = serviceName;

    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');

    lockBody();

    requestAnimationFrame(() => {
      const firstInput = modal.querySelector('input, textarea');
      if (firstInput) firstInput.focus();
    });

    activeBudget = modal;
  }

  function closeBudgetModal() {
    const overlay = getBudgetOverlay();
    if (!overlay) return;
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    activeBudget = null;
    unlockBody();
  }

  // -------- EVENT DELEGATION (CLICKS) --------
  document.addEventListener('click', (e) => {
    // Budget close (botón X)
    if (e.target.closest('[data-budget-close]')) {
      e.preventDefault();
      closeBudgetModal();
      return;
    }
    // Click en el overlay del budget (fuera del modal)
    if (e.target.matches('[data-budget-overlay]')) {
      closeBudgetModal();
      return;
    }
    // Trigger del budget modal
    const budgetTrigger = e.target.closest('[data-budget]');
    if (budgetTrigger) {
      e.preventDefault();
      const serviceName = budgetTrigger.dataset.budget || 'Servicio';
      openBudgetModal(serviceName);
      return;
    }

    // Service modal trigger
    const serviceTrigger = e.target.closest('[data-modal-trigger]');
    if (serviceTrigger) {
      const id = serviceTrigger.dataset.modalTrigger;
      const modal = document.getElementById(`modal-${id}`);
      if (modal) {
        e.preventDefault();
        openModal(id);
      }
      return;
    }

    // Service modal close (X)
    if (e.target.closest('[data-modal-close]')) {
      e.preventDefault();
      closeModal();
      return;
    }
    // Click outside service modal
    if (e.target.matches('[data-modal-overlay]')) {
      closeModal();
    }
  });

  // -------- KEYBOARD (ESC + Enter/Space en cards) --------
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      // Cerrá primero el budget, después el de servicio
      if (activeBudget) {
        closeBudgetModal();
        return;
      }
      if (activeModal) {
        closeModal();
        return;
      }
    }
    if ((e.key === 'Enter' || e.key === ' ') && document.activeElement) {
      const trigger = document.activeElement.closest('[data-modal-trigger]');
      if (trigger) {
        e.preventDefault();
        openModal(trigger.dataset.modalTrigger);
      }
    }
  });

  // -------- FORM SUBMIT — abre mailto con servicio prerellenado --------
  document.addEventListener('submit', (e) => {
    const form = e.target.closest('.modal__form, .budget-modal__form');
    if (!form) return;
    e.preventDefault();

    const service = form.dataset.service || 'Servicio';
    const nameInput = form.querySelector('[name="name"]');
    const emailInput = form.querySelector('[name="email"]');
    const messageInput = form.querySelector('[name="message"]');

    if (nameInput && !nameInput.checkValidity()) { form.reportValidity(); return; }
    if (emailInput && !emailInput.checkValidity()) { form.reportValidity(); return; }

    const name = (nameInput?.value || '').trim();
    const email = (emailInput?.value || '').trim();
    const message = (messageInput?.value || '').trim();

    const svc = serviceLabel(service);
    const en = lang() === 'en';
    const subject = en
      ? `Quote request · ${svc}`
      : `Solicitud de presupuesto · ${svc}`;
    const body = en
      ? `Requested service: ${svc}\n` +
        `\n` +
        `Name: ${name}\n` +
        `Email: ${email}\n` +
        `\n` +
        `Message:\n${message || '(no additional message)'}`
      : `Servicio solicitado: ${svc}\n` +
        `\n` +
        `Nombre: ${name}\n` +
        `Email: ${email}\n` +
        `\n` +
        `Mensaje:\n${message || '(sin mensaje adicional)'}`;

    const mailto =
      `mailto:admin@vantia.digital` +
      `?subject=${encodeURIComponent(subject)}` +
      `&body=${encodeURIComponent(body)}`;

    window.location.href = mailto;
  });

  // -------- AUTO-OPEN POR HASH (ej: /index.html#ingenieria-web) --------
  function checkHashOnLoad() {
    const hash = window.location.hash.substring(1);
    if (!hash) return;
    const modal = document.getElementById(`modal-${hash}`);
    if (modal) setTimeout(() => openModal(hash), 250);
  }

  if (window.__componentsLoaded) {
    checkHashOnLoad();
  } else {
    document.addEventListener('components:loaded', checkHashOnLoad, { once: true });
  }

  // API global
  window.VantiaModal = {
    open: openModal,
    close: closeModal,
    openBudget: openBudgetModal,
    closeBudget: closeBudgetModal,
  };
})();
