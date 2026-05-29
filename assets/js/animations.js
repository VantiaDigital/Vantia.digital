/* ============================================
   VANTIA DIGITAL - ANIMATIONS (GSAP)
   Hero parallax + scroll-triggered reveals
   ============================================ */

(() => {
  'use strict';

  if (typeof gsap === 'undefined') return;
  if (window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // -------- PRELOADER --------
  function runPreloader() {
    const preloader = document.querySelector('.preloader');
    if (!preloader) return Promise.resolve();

    return new Promise((resolve) => {
      const tl = gsap.timeline({
        onComplete: () => {
          preloader.classList.add('is-hidden');
          gsap.set(preloader, { display: 'none' });
          resolve();
        },
      });

      tl.to('.preloader__bar::after', { duration: 0.1 }) // placeholder, no css var anim
        .fromTo(
          '.preloader__bar',
          { '--prog': '0%' },
          { duration: 1.1, ease: 'power2.inOut' },
          0
        )
        .to(
          '.preloader',
          { yPercent: -100, duration: 0.9, ease: 'expo.inOut' },
          '+=0.1'
        )
        .to(
          '.preloader__mark',
          { opacity: 0, y: -20, duration: 0.6, ease: 'power2.out' },
          '<0.1'
        );
    });
  }

  // -------- HERO INTRO --------
  // IMPORTANTE: el TEXTO del hero (título, subtítulo, CTAs) ya NO se anima con
  // GSAP. Antes GSAP los ponía en opacity:0 y los revelaba; si GSAP tardaba o
  // fallaba, los botones quedaban INVISIBLES. Ahora el texto se muestra siempre
  // (visible por defecto + un fade suave por CSS, ver animations.css). Acá GSAP
  // sólo anima el cristal y la grilla, que son decorativos y tienen opacity
  // segura por defecto en CSS.
  function heroIntro() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    gsap.set('.hero__grid', { opacity: 0 });
    const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
    tl.to('.hero__grid', { opacity: 1, duration: 1.2, ease: 'power2.out' }, 0)
      .from('.hero__crystal', {
        opacity: 0,
        scale: 0.7,
        rotate: -18,
        duration: 2.0,
        ease: 'expo.out',
      }, 0);
  }

  // -------- HERO PARALLAX (scroll) --------
  function heroParallax() {
    if (!window.ScrollTrigger) return;
    if (prefersReduced) return;

    const hero = document.querySelector('.hero');
    if (!hero) return;

    gsap.to('.hero__crystal', {
      yPercent: 45,
      rotate: 18,
      scale: 1.18,
      ease: 'none',
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: 'bottom top',
        scrub: 0.6,
      },
    });

    gsap.to('.hero__grid', {
      yPercent: 25,
      opacity: 0.4,
      ease: 'none',
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: 'bottom top',
        scrub: 0.4,
      },
    });

    gsap.to('.hero__inner', {
      yPercent: -18,
      opacity: 0.3,
      ease: 'none',
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: 'bottom 30%',
        scrub: 0.6,
      },
    });
  }

  // -------- HERO CRYSTAL + GRID — REACTIVO AL CURSOR --------
  // Aplica el efecto al WRAPPER (.hero__crystal-wrap) para no chocar con GSAP
  // que controla .hero__crystal (intro + scroll parallax).
  // Pausa cuando el hero no está en viewport o la pestaña está oculta para ahorrar CPU.
  function crystalMouseFollow() {
    if (prefersReduced) return;

    const hero = document.querySelector('.hero');
    const wrap = document.querySelector('.hero__crystal-wrap');
    const grid = document.querySelector('.hero__grid');
    const bg = document.querySelector('.hero__bg');
    if (!hero || !wrap) return;

    const target = { x: 0, y: 0 };
    const current = { x: 0, y: 0 };
    let t0 = performance.now();
    let mouseInside = false;
    let isVisible = true;
    let isTabActive = true;
    let rafId = null;

    hero.addEventListener('mouseenter', () => { mouseInside = true; });
    hero.addEventListener('mousemove', (e) => {
      const rect = hero.getBoundingClientRect();
      target.x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      target.y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
      mouseInside = true;
    });
    hero.addEventListener('mouseleave', () => {
      mouseInside = false;
      target.x = 0;
      target.y = 0;
    });

    if (bg) bg.style.perspective = '1400px';
    wrap.style.transformStyle = 'preserve-3d';

    function tick(now) {
      if (!isVisible || !isTabActive) {
        rafId = requestAnimationFrame(tick);
        return;
      }

      // P1 perf: skip frames when fully idle (no mouse, lerp converged).
      // Ahorra ~1-3 ms/frame en desktop, 5-10 ms/frame en mobile.
      const dx = target.x - current.x;
      const dy = target.y - current.y;
      if (!mouseInside && Math.abs(dx) < 0.0005 && Math.abs(dy) < 0.0005) {
        rafId = requestAnimationFrame(tick);
        return;
      }

      const t = (now - t0) / 1000;

      // Lerp del objetivo del cursor
      current.x += (target.x - current.x) * 0.085;
      current.y += (target.y - current.y) * 0.085;

      // Autorrotación + flotación constante (más viva cuando no hay cursor encima)
      const idleAmp = mouseInside ? 0.35 : 1;
      const autoRot = Math.sin(t * 0.35) * 4 * idleAmp;        // rotZ suave
      const autoFloatX = Math.sin(t * 0.6) * 12 * idleAmp;
      const autoFloatY = Math.cos(t * 0.45) * 10 * idleAmp;
      const autoBreath = 1 + Math.sin(t * 0.8) * 0.025 * idleAmp;

      // Efecto cursor — más exagerado
      const rotY = current.x * 28;
      const rotX = -current.y * 22;
      const tx = current.x * 95 + autoFloatX;
      const ty = current.y * 65 + autoFloatY;
      const dist = Math.min(1, Math.hypot(current.x, current.y));
      const cursorScale = 1 + dist * 0.12;
      const totalScale = cursorScale * autoBreath;

      wrap.style.transform =
        `translate3d(${tx}px, ${ty}px, 0)` +
        ` rotateX(${rotX}deg) rotateY(${rotY}deg) rotateZ(${autoRot}deg)` +
        ` scale(${totalScale})`;

      if (grid) {
        grid.style.transform =
          `translate3d(${-current.x * 24 + autoFloatX * 0.3}px, ${-current.y * 18 + autoFloatY * 0.3}px, 0)`;
      }

      rafId = requestAnimationFrame(tick);
    }
    rafId = requestAnimationFrame(tick);

    // Pausa cuando el hero sale del viewport (ahorra CPU)
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => { isVisible = entry.isIntersecting; });
      }, { threshold: 0 });
      io.observe(hero);
    }

    // Pausa cuando la pestaña no está activa
    document.addEventListener('visibilitychange', () => {
      isTabActive = document.visibilityState === 'visible';
    });
  }

  // -------- GENERIC REVEALS --------
  function setupReveals() {
    if (!window.ScrollTrigger) return;

    // Elementos simples
    document.querySelectorAll('[data-reveal]').forEach((el) => {
      const delay = parseFloat(el.dataset.revealDelay || 0);
      gsap.fromTo(
        el,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 1,
          ease: 'expo.out',
          delay,
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Stagger children
    document.querySelectorAll('[data-reveal-children]').forEach((parent) => {
      const children = parent.children;
      gsap.fromTo(
        children,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 1,
          ease: 'expo.out',
          stagger: 0.12,
          scrollTrigger: {
            trigger: parent,
            start: 'top 80%',
            toggleActions: 'play none none none',
          },
        }
      );
    });
  }

  // -------- PILLARS HOVER ENRICHMENT --------
  function pillarsInteraction() {
    const pillars = document.querySelectorAll('.pillar');
    if (!pillars.length) return;

    const isCoarse = window.matchMedia('(pointer: coarse)').matches;

    pillars.forEach((pillar) => {
      const icon = pillar.querySelector('.pillar__icon');

      pillar.addEventListener('mouseenter', () => {
        if (!isCoarse) document.body.classList.add('is-pillar-active');
        if (icon) gsap.to(icon, { rotate: -10, scale: 1.1, duration: 0.4, ease: 'power3.out' });
      });

      pillar.addEventListener('mouseleave', () => {
        document.body.classList.remove('is-pillar-active');
        if (icon) gsap.to(icon, { rotate: 0, scale: 1, duration: 0.5, ease: 'power3.out' });
      });
    });
  }

  // -------- FOOTER MARK PARALLAX --------
  function footerParallax() {
    if (!window.ScrollTrigger) return;
    if (prefersReduced) return;

    const mark = document.querySelector('.footer__brand-mark');
    if (!mark) return;

    gsap.fromTo(
      mark,
      { yPercent: 20, opacity: 0.6 },
      {
        yPercent: 0,
        opacity: 1,
        ease: 'none',
        scrollTrigger: {
          trigger: mark,
          start: 'top 95%',
          end: 'top 40%',
          scrub: true,
        },
      }
    );
  }

  // -------- INIT --------
  function init() {
    heroIntro();
    heroParallax();
    crystalMouseFollow();
    // setupReveals() eliminado: los reveals ahora los maneja un
    // IntersectionObserver nativo en main.js (initReveals), independiente de
    // GSAP. Así el contenido nunca queda invisible esperando que cargue GSAP.
    pillarsInteraction();
    footerParallax();

    // Re-cálculo después de fuentes / imágenes
    window.addEventListener('load', () => {
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
