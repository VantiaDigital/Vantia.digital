/* ============================================
   VANTIA DIGITAL - CONSENT MANAGER
   Google Consent Mode v2 + GA4
   Cumple RGPD / LOPD-DDD (AEPD España)
   ============================================ */

(() => {
  'use strict';

  const GA_ID = 'G-SV13BVRDX9';
  const STORAGE_KEY = 'vantia_consent_v1';
  const CONSENT_VERSION = 1; // bump para forzar re-consent en cambios mayores

  // -------- gtag base (debe ejecutarse ANTES de cargar gtag.js) --------
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  // Consent default: TODO denegado hasta decisión del usuario (modelo opt-in EU)
  gtag('consent', 'default', {
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'analytics_storage': 'denied',
    'functionality_storage': 'granted',  // necesarias siempre
    'security_storage': 'granted',
    'wait_for_update': 500
  });

  gtag('set', 'ads_data_redaction', true);
  gtag('set', 'url_passthrough', false);

  // -------- Estado y persistencia --------
  function readConsent() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (data.version !== CONSENT_VERSION) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  function saveConsent(prefs) {
    const data = {
      version: CONSENT_VERSION,
      timestamp: new Date().toISOString(),
      analytics: !!prefs.analytics
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.warn('[consent] localStorage unavailable');
    }
    return data;
  }

  function applyConsent(prefs) {
    const analytics = prefs.analytics ? 'granted' : 'denied';
    gtag('consent', 'update', {
      'analytics_storage': analytics,
      // Mantenemos ads denegados — no usamos remarketing
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied'
    });

    if (prefs.analytics) {
      loadGA();
    }
  }

  // -------- Carga GA4 (solo si hay consent analytics) --------
  let gaLoaded = false;
  function loadGA() {
    if (gaLoaded) return;
    gaLoaded = true;

    const s = document.createElement('script');
    s.async = true;
    s.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(s);

    gtag('js', new Date());
    gtag('config', GA_ID, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
  }

  // -------- API pública (la usa el banner) --------
  window.VantiaConsent = {
    get: readConsent,

    acceptAll() {
      const data = saveConsent({ analytics: true });
      applyConsent(data);
      document.dispatchEvent(new CustomEvent('consent:updated', { detail: data }));
    },

    rejectAll() {
      const data = saveConsent({ analytics: false });
      applyConsent(data);
      document.dispatchEvent(new CustomEvent('consent:updated', { detail: data }));
    },

    save(prefs) {
      const data = saveConsent(prefs);
      applyConsent(data);
      document.dispatchEvent(new CustomEvent('consent:updated', { detail: data }));
    },

    reset() {
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      location.reload();
    },

    hasDecision() {
      return readConsent() !== null;
    }
  };

  // -------- Re-aplicar consent en navegaciones --------
  const existing = readConsent();
  if (existing) {
    applyConsent(existing);
  }
})();
