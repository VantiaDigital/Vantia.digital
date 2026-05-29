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
        const ratio = max > 0 ? Math.min(1, y / max) : 0;
        // P1 perf: usar transform: scaleX en lugar de style.width.
        // scaleX es composite-only; width forzaría layout en cada frame.
        progress.style.transform = 'scaleX(' + ratio + ')';
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

  // -------- LOADER DINÁMICO "Vantia..." (solo si la carga tarda) --------
  // Política:
  // - Click en link interno → setTimeout 350ms.
  // - Si la nueva página termina de cargar antes → no se muestra nada.
  // - Si tarda más de 350ms → se crea el overlay dinámicamente y se muestra.
  // - El overlay se descarta automáticamente cuando el browser descarta la
  //   página vieja para mostrar la nueva. La nueva página no tiene loader
  //   (el HTML no lo contiene), entonces queda limpia.
  // - bfcache: pageshow + pagehide limpian el timer y el overlay.
  function initPageTransitions() {
    const LOADER_ID = '__vantia_loader__';
    let slowTimer = null;

    function createLoader() {
      let el = document.getElementById(LOADER_ID);
      if (el) return el;
      el = document.createElement('div');
      el.id = LOADER_ID;
      el.setAttribute('aria-hidden', 'true');
      el.innerHTML =
        '<div class="__vl-inner">Vantia' +
        '<span class="__vl-dots"><span>.</span><span>.</span><span>.</span></span>' +
        '</div>';
      el.style.cssText = [
        'position:fixed',
        'inset:0',
        'z-index:99999',
        'background:#1A1813',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'opacity:0',
        'transition:opacity 200ms ease-out',
        'pointer-events:none',
      ].join(';');

      const inner = el.querySelector('.__vl-inner');
      inner.style.cssText = [
        'font-family:"Fraunces",serif',
        'font-size:1.5rem',
        'color:#ECE8D8',
        'display:inline-flex',
        'align-items:baseline',
        'letter-spacing:-0.01em',
      ].join(';');

      // Estilo para los puntos animados
      const styleId = '__vl-style';
      if (!document.getElementById(styleId)) {
        const s = document.createElement('style');
        s.id = styleId;
        s.textContent =
          '.__vl-dots{display:inline-flex;margin-left:2px}' +
          '.__vl-dots span{display:inline-block;color:#C1834B;opacity:0;' +
          'animation:__vl-d 1.4s infinite ease-in-out both}' +
          '.__vl-dots span:nth-child(2){animation-delay:.18s}' +
          '.__vl-dots span:nth-child(3){animation-delay:.36s}' +
          '@keyframes __vl-d{0%{opacity:0;transform:translateY(0)}' +
          '20%{opacity:1;transform:translateY(-4px)}' +
          '40%{opacity:1;transform:translateY(0)}' +
          '100%{opacity:0;transform:translateY(0)}}';
        document.head.appendChild(s);
      }

      document.body.appendChild(el);
      // Forzar reflow para que la transición opacity funcione
      void el.offsetWidth;
      return el;
    }

    function showLoader() {
      const el = createLoader();
      el.style.opacity = '1';
      el.style.pointerEvents = 'auto';
    }

    function hideLoader() {
      const el = document.getElementById(LOADER_ID);
      if (el) {
        el.style.opacity = '0';
        el.style.pointerEvents = 'none';
      }
    }

    document.addEventListener('click', (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      const link = e.target.closest('a[href]');
      if (!link) return;
      if (link.target === '_blank' || link.hasAttribute('download')) return;

      const href = link.getAttribute('href');
      if (!href || href.startsWith('#')) return;
      if (/^(mailto:|tel:|javascript:)/.test(href)) return;

      const isInternal = href.includes('.html') ||
                         href === '/' ||
                         (href.startsWith('/') && !href.startsWith('//'));
      if (!isInternal) return;

      try {
        const u = new URL(link.href);
        if (u.pathname === window.location.pathname && u.hash) return;
      } catch (_) { /* noop */ }

      clearTimeout(slowTimer);
      slowTimer = setTimeout(showLoader, 350);
    });

    // bfcache: al volver con back, asegurar todo limpio
    window.addEventListener('pageshow', () => {
      clearTimeout(slowTimer);
      hideLoader();
    });
    window.addEventListener('pagehide', () => {
      clearTimeout(slowTimer);
    });

    // NOTA: ya NO mostramos el loader esperando a los componentes. El header
    // ahora está inline en el HTML (instantáneo) y el contenido se revela vía
    // IntersectionObserver nativo (instantáneo arriba). Los componentes que
    // quedan (footer, whatsapp, cookie-banner) están abajo o son overlays:
    // su carga no bloquea nada visible. El loader solo aparece en navegación
    // realmente lenta (el setTimeout de 350ms arriba).
  }

  // -------- REVEAL NATIVO (IntersectionObserver, sin GSAP) --------
  // Reemplaza el setupReveals de GSAP. El contenido nunca queda invisible
  // esperando que cargue una librería: arriba se revela al instante (el IO lo
  // ve en viewport al cargar), abajo al hacer scroll. Cero dependencia de GSAP.
  function initReveals() {
    const reveals = document.querySelectorAll('[data-reveal]');
    const childWraps = document.querySelectorAll('[data-reveal-children]');

    // Aplicar delays declarados (data-reveal-delay) como transition-delay
    reveals.forEach((el) => {
      const d = parseFloat(el.dataset.revealDelay || 0);
      if (d) el.style.transitionDelay = d + 's';
    });
    // Stagger de los hijos
    childWraps.forEach((parent) => {
      Array.from(parent.children).forEach((c, i) => {
        c.style.transitionDelay = (i * 0.08) + 's';
      });
    });

    const targets = [
      ...reveals,
      ...Array.from(childWraps).flatMap((p) => Array.from(p.children)),
    ];
    if (!targets.length) return;

    // Sin IntersectionObserver: mostrar todo de una (fallback seguro)
    if (!('IntersectionObserver' in window)) {
      targets.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    targets.forEach((el) => io.observe(el));
  }

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
    // Cosas que no dependen de componentes ni de GSAP. Corre siempre, primero.
    initReveals();          // reveal nativo IO — el contenido se muestra sí o sí
    initPageTransitions();  // loader de navegación lenta (no depende de componentes)
    initLenis();
    initCounters();
    initScrollTop();
  }

  function initWithComponents() {
    // Cosas que dependen del footer/whatsapp/modales cargados vía fetch.
    // (El header ahora es inline, pero initHeader/initMobileNav/markActiveNav
    // operan sobre él igual — está presente desde el inicio.)
    initHeader();
    initMobileNav();
    initMagnetic();
    initWhatsapp();
    markActiveNav();
    // initPageTransitions se movió a initInline (no depende de componentes).
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
