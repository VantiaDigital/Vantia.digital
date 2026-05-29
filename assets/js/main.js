/* ============================================
   VANTIA DIGITAL - MAIN JS
   Lenis smooth scroll + header + nav móvil
   ============================================ */

(() => {
  'use strict';

  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('has-js');

  // -------- LENIS SMOOTH SCROLL --------
  let lenis;

  function initLenis() {
    if (typeof Lenis === 'undefined') return;

    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    lenis = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      smoothTouch: false,
      touchMultiplier: 1.5,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Integración con GSAP ScrollTrigger
    if (window.gsap && window.ScrollTrigger) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    }

    window.__lenis = lenis;
  }

  // -------- HEADER ON SCROLL + SCROLL PROGRESS --------
  function initHeader() {
    const header = document.querySelector('.site-header');
    const progress = document.querySelector('.scroll-progress');

    const onScroll = () => {
      const y = window.scrollY;
      if (header) header.classList.toggle('is-scrolled', y > 8);

      if (progress) {
        const doc = document.documentElement;
        const max = doc.scrollHeight - window.innerHeight;
        const pct = max > 0 ? (y / max) * 100 : 0;
        progress.style.width = pct + '%';
      }
    };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // -------- MAGNETIC CTAs --------
  function initMagnetic() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    const targets = document.querySelectorAll('[data-magnetic]');
    if (!targets.length || !window.gsap) return;

    targets.forEach((el) => {
      const label = el.querySelector('.btn__label') || el;
      const strength = 0.32;
      const radius = 80;

      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = e.clientX - cx;
        const dy = e.clientY - cy;
        const dist = Math.hypot(dx, dy);
        if (dist > rect.width + radius) return;

        gsap.to(el, {
          x: dx * strength,
          y: dy * strength,
          duration: 0.5,
          ease: 'power3.out',
        });
        gsap.to(label, {
          x: dx * strength * 0.4,
          y: dy * strength * 0.4,
          duration: 0.5,
          ease: 'power3.out',
        });
      });

      el.addEventListener('mouseleave', () => {
        gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)' });
        gsap.to(label, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)' });
      });
    });
  }

  // -------- WHATSAPP FAB --------
  function initWhatsapp() {
    const fab = document.querySelector('.whatsapp-fab');
    if (!fab) return;
    setTimeout(() => fab.classList.add('is-visible'), 1600);
  }

  // -------- COUNTERS --------
  function initCounters() {
    const els = document.querySelectorAll('[data-count-to]');
    if (!els.length || !window.gsap || !window.ScrollTrigger) return;

    els.forEach((el) => {
      const target = parseFloat(el.dataset.countTo);
      if (isNaN(target)) return;
      const obj = { v: 0 };

      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        once: true,
        onEnter: () => {
          gsap.to(obj, {
            v: target,
            duration: 2.2,
            ease: 'power2.out',
            onUpdate: () => { el.textContent = Math.round(obj.v); },
          });
        },
      });
    });
  }

  // -------- MOBILE NAV --------
  function initMobileNav() {
    const toggle = document.querySelector('.nav__toggle');
    const nav = document.querySelector('.nav');
    if (!toggle || !nav) return;

    function closeNav() {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-nav-open');
      document.body.style.overflow = '';
    }

    function openNav() {
      nav.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      document.body.classList.add('is-nav-open');
      document.body.style.overflow = 'hidden';
    }

    toggle.addEventListener('click', () => {
      if (nav.classList.contains('is-open')) closeNav();
      else openNav();
    });

    // Click en un link cierra el menú
    nav.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', closeNav);
    });

    // Click en el overlay difuminado cierra el menú
    const dim = document.querySelector('.page-dim');
    if (dim) {
      dim.addEventListener('click', () => {
        if (document.body.classList.contains('is-nav-open')) closeNav();
      });
    }

    // ESC cierra el menú
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && document.body.classList.contains('is-nav-open')) {
        closeNav();
      }
    });
  }

  // Navegación 100% nativa del browser. Sin overlay, sin transición JS.
  // El elemento .page-transition fue eliminado del HTML — esta función es noop
  // de compatibilidad por si alguna pestaña vieja la invoca.
  function initPageTransitions() { /* noop */ }

  // -------- ACTIVE NAV LINK --------
  function markActiveNav() {
    // Toma el último segmento del path (sin .html). Comparación exacta para
    // evitar falsos positivos cuando un segmento contiene a otro como substring.
    const path = window.location.pathname;
    const segment = (path.split('/').filter(Boolean).pop() || '').replace(/\.html$/i, '');
    const current = segment || 'home';

    document.querySelectorAll('[data-nav]').forEach((link) => {
      if (link.dataset.nav === current) link.classList.add('is-active');
      else link.classList.remove('is-active');
    });
  }

  // -------- SCROLL TOP (footer "Volver al inicio") --------
  function initScrollTop() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('[data-scroll-top]');
      if (!link) return;
      e.preventDefault();
      if (window.__lenis) {
        window.__lenis.scrollTo(0, { duration: 1.4 });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  // -------- INIT --------
  function initInline() {
    // Cosas que no dependen de componentes (Lenis, counters)
    initLenis();
    initCounters();
    initScrollTop();
  }

  function initWithComponents() {
    // Cosas que SÍ dependen del header/footer/whatsapp/modales cargados
    initHeader();
    initMobileNav();
    initMagnetic();
    initWhatsapp();
    markActiveNav();
    requestAnimationFrame(initPageTransitions);
  }

  function init() {
    initInline();

    // Si hay placeholders [data-component] espera a que terminen de cargar
    const hasPlaceholders = !!document.querySelector('[data-component]');
    if (window.__componentsLoaded || !hasPlaceholders) {
      initWithComponents();
    } else {
      document.addEventListener('components:loaded', initWithComponents, { once: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // BFCACHE: si la página vuelve del back/forward cache del navegador,
  // resetear estado completo (overlay + body + GSAP) para evitar congelamientos
  // o tiempos de carga visuales fantasma.
  window.addEventListener('pageshow', (e) => {
    if (!e.persisted) return;

    // 1. Kill cualquier timeline de GSAP que haya quedado colgada
    if (window.gsap && window.gsap.globalTimeline) {
      try { window.gsap.globalTimeline.getChildren().forEach((tween) => tween.kill()); }
      catch (_) { /* noop */ }
    }

    // 2. Reset overlay del page-transition
    const ov = document.querySelector('.page-transition');
    if (ov) {
      ov.style.transform = 'scaleY(0)';
      ov.style.opacity = '0';
      ov.style.pointerEvents = 'none';
    }
    const ovLogo = document.querySelector('.page-transition__logo');
    if (ovLogo) ovLogo.style.opacity = '0';

    // 3. Reset body (por si quedó modal abierto o scroll bloqueado)
    document.body.classList.remove('modal-open', 'is-nav-open', 'is-pillar-active');
    document.body.style.overflow = '';

    // 4. Lenis re-init si está suspendido
    if (window.__lenis && typeof window.__lenis.start === 'function') {
      window.__lenis.start();
    }
  });
})();
