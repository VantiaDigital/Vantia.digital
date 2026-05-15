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

    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    nav.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  // -------- PAGE TRANSITIONS --------
  function initPageTransitions() {
    const overlay = document.querySelector('.page-transition');
    if (!overlay || !window.gsap) return;

    // Entrada (overlay sale al cargar)
    gsap.set(overlay, { scaleY: 1, transformOrigin: 'top' });
    gsap.set('.page-transition__logo', { opacity: 1 });

    const tlIn = gsap.timeline({ delay: 0.1 });
    tlIn
      .to('.page-transition__logo', { opacity: 0, duration: 0.3, ease: 'power2.out' }, 0.2)
      .to(overlay, {
        scaleY: 0,
        duration: 0.9,
        ease: 'expo.inOut',
        transformOrigin: 'top',
      }, 0.3);

    // Salida (al hacer click en link interno)
    document.querySelectorAll('a[href]').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;
      // Saltar anchors-only (#algo) y links con hash al mismo path
      if (href.startsWith('#')) return;
      // Saltar mailto, tel, javascript:, etc.
      if (/^(mailto:|tel:|javascript:)/.test(href)) return;
      // Solo navegamos en links que apuntan a otro .html
      const isInternal = href.includes('.html') ||
                         href === '/' ||
                         (href.startsWith('/') && !href.startsWith('//'));
      if (!isInternal) return;
      if (link.target === '_blank' || link.hasAttribute('download')) return;

      // Si el link es a la página actual (mismo pathname), saltar también
      try {
        const u = new URL(link.href);
        if (u.pathname === window.location.pathname && u.hash) return;
      } catch (_) { /* noop */ }

      link.addEventListener('click', (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey) return;
        e.preventDefault();
        const url = link.href;

        gsap.set(overlay, { scaleY: 0, transformOrigin: 'bottom' });
        const tlOut = gsap.timeline({
          onComplete: () => { window.location.href = url; },
        });
        tlOut
          .to(overlay, {
            scaleY: 1,
            duration: 0.7,
            ease: 'expo.inOut',
            transformOrigin: 'bottom',
          })
          .to('.page-transition__logo', { opacity: 1, duration: 0.3, ease: 'power2.out' }, 0.4);
      });
    });
  }

  // -------- ACTIVE NAV LINK --------
  function markActiveNav() {
    // Detecta la página actual a partir del path
    const path = window.location.pathname;
    let current = 'home';
    if (path.includes('casos')) current = 'casos';
    else if (path.includes('servicios')) current = 'servicios';
    else if (path.includes('nosotros')) current = 'nosotros';
    else if (path.includes('contacto')) current = 'contacto';
    else if (path.includes('sesion')) current = 'sesion';

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
})();
