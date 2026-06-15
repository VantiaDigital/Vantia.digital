# Vantia · Marketing Digital — Handoff de contexto

> Documento de continuidad para retomar el proyecto en una nueva sesión de Claude Code.
> **Leer este archivo PRIMERO** antes de tocar cualquier cosa.

---

## TL;DR

Sitio estático para **Vantia Digital** (agencia técnica de marketing digital para PYMES y empresas medianas, Barcelona, fundador Facundo Goette). Web **bilingüe ES/EN**. Stack: HTML/CSS/JS vanilla + GSAP + Lenis. Deploy en Cloudflare Pages, dominio `vantia.digital`. Repo: `github.com/VantiaDigital/Vantia.digital`. Está LIVE y funcionando.

---

## ESTADO ACTUAL — 15 jun 2026 (este bloque MANDA sobre el resto del doc)

Partes de este handoff son de mayo y quedaron viejas. Lo vigente hoy:

- **Tono: tuteo de España** (tú/quieres/dime/coste/dinero), NUNCA voseo argentino. Sin emojis pictográficos. No inventar datos. Nunca menospreciar al cliente. Ver `memory/tone_spain_tuteo.md` y `memory/no_emoji_icons.md`. (Incluye el chat con Facu: también en tuteo España, NO voseo — corregido 2026-06-04.)
- **Naming: "Vantia Digital"** (sin punto medio en el wordmark). El "·" cobre es solo firma/acento externo. (La tarjeta de visita impresa legacy aún dice "Vantia · Marketing Digital" — no se toca.)
- **Servicios (nombres visibles):** Optimización Web + CRO · SEO Técnico + GEO · Campañas de anuncios. IDs internos sin cambiar (`ingenieria-web`, `seo-tecnico`, `paid-media`).
- **URLs limpias sin `/pages/`** (jun 2026): los archivos viven en la raíz (`servicios.html`, `nosotros.html`, `contacto.html`, `casos/index.html` → `/casos/`, `casos/<slug>.html`). `_redirects` hace `/pages/* -> /:splat 301`. Canónicas, og:url y sitemap usan las URLs limpias.
- **Header inlineado** en cada HTML (ya NO se fetchea). Fuente única `components/header.html`; tras editarlo, correr `python scripts/build_inline_header.py`. Footer/whatsapp/cookie-banner sí se cargan por fetch.
- **Web bilingüe ES/EN** con toggle sutil en cliente. ES = HTML base; EN en `assets/js/i18n.js` vía `data-i18n`. Ver `memory/i18n_system_vantia.md`.
- **WhatsApp:** +34 644 923 374, con saludo prerelleno en el wa.me. Se añadió **X** (x.com/vantiadigital) a contacto/footer.
- **SEO/indexación:** desajuste canónica/sitemap arreglado; sitemap limpio (11 URLs, sin legales noindex); 11 URLs con indexación solicitada. El aviso "Página con redirección" sobre variantes de la home (www/http/index.html) es ruido normal.
- **Cookies:** banner GDPR con botones de prominencia equitativa (aceptar = rechazar).
- **Stats hero:** ROAS **450%** (no 250%).

Donde el texto de abajo contradiga este bloque, **gana este bloque**. Los `HANDOFF-MAY-26.md` y `HANDOFF-MAY-29.md` son logs históricos por fecha — no los toques.

---

## Proyecto

| | |
|---|---|
| Local path | `C:\Users\facun\Documentos\Vantia Digital\Vantia Digital Web` |
| GitHub | https://github.com/VantiaDigital/Vantia.digital |
| Deploy | Cloudflare Pages (Worker `vantiadigital`) |
| URL workers.dev | `https://vantiadigital.wild-boat-af4c.workers.dev/` |
| URL pública | https://vantia.digital |
| Registrar dominio | Cloudflare Registrar |
| Auto-deploy | `git push` a `main` → Cloudflare rebuild ~30-60s |

---

## Identidad de marca

### Tagline
"Precisión matemática aplicada al marketing"

### Naming
- Nombre: **"Vantia Digital"** (SIN punto medio en el wordmark). El `·` cobre es solo firma/acento externo, no va dentro del nombre. (La tarjeta de visita impresa legacy aún dice "Vantia · Marketing Digital" — no se toca.)
- Target: **PYMES y empresas medianas**
- Posicionamiento: agencia técnica, no creativa. *"La mayoría de agencias venden diseño. Nosotros construimos sistemas para ROI."*

### Tres pilares / servicios (nombres visibles)
1. **Optimización Web + CRO** — plataformas alta velocidad, PageSpeed 95+, conversión
2. **SEO Técnico + GEO** (Generative Engine Optimization, para búsqueda con IA)
3. **Campañas de anuncios** — Google Ads y Meta Ads

> IDs internos SIN cambiar (`ingenieria-web`, `seo-tecnico`, `paid-media`) para no romper tracking ni hashes.

### Paleta oficial
```
#1A1813 — Deep dark olive (hero bg, dark theme)
#3C3A2F — Olive (footer, mid)
#77431C — Brown (hover accent-hover)
#C1834B — Copper / Terracotta (CTAs, accents, copper "·" )
#A99B80 — Muted olive (secondary text)
#ECE8D8 — Cream (light theme, text on dark)
```

### Tipografía
- **Fraunces** (display serif) — titulares, brand name, hero
- **Inter** (sans) — body, contact data, navegación
- **Self-hosted** en `/assets/fonts/files/*.woff2` + `/assets/fonts/fonts.css`
- También hay `Fraunces-Regular.ttf` e `Inter-Variable.ttf` en `/assets/fonts/` (para script Python de PDFs)

### Logo
- V (cream sobre dark, o dark sobre light) + A (cobre `#C1834B`) interlocking
- En `/assets/images/logo.svg` (viewBox `0 0 1269 1012`)
- Favicon en `/assets/images/favicon.svg`
- **NUNCA** agregar strokes/contornos internos a las letras del logo — el usuario odia que se vea "hollow"

---

## Tech stack

- HTML/CSS/JS vanilla (sin framework)
- **GSAP 3.12.5 + ScrollTrigger** — animaciones, scroll-triggered reveals
- **Lenis 1.0.45** — smooth scroll (versión específica, API compatible con 1.0.42 original)
- **Web3Forms** — backend del form de contacto
- Todo el vendor JS está **self-hosted** en `/assets/js/vendor/`

---

## Estructura de archivos (relevante)

```
/
├─ index.html                    ← Home
├─ /pages/
│   ├─ servicios.html
│   ├─ casos.html                ← Portfolio con filtro Industria
│   ├─ nosotros.html
│   └─ contacto.html             ← Form Web3Forms + canales
├─ /components/                  ← Cargados via fetch
│   ├─ header.html
│   ├─ footer.html
│   ├─ whatsapp.html             ← FAB verde WhatsApp
│   └─ service-modals.html       ← 3 modales de servicios + budget modal
├─ /assets/
│   ├─ /css/
│   │   ├─ main.css              ← ~2400 líneas, TODOS los estilos del sitio
│   │   └─ animations.css        ← reveals, marquee, scroll progress, grain
│   ├─ /fonts/
│   │   ├─ fonts.css             ← @font-face self-host
│   │   ├─ Fraunces-Regular.ttf  ← Para script Python (PDFs)
│   │   ├─ Inter-Variable.ttf    ← Para script Python (PDFs)
│   │   └─ /files/*.woff2        ← 6 archivos (Fraunces+Inter, latin+latin-ext)
│   ├─ /images/
│   │   ├─ logo.svg              ← V+A oficial
│   │   ├─ favicon.svg           ← Favicon con bordes redondeados
│   │   ├─ gett-studio.jpg       ← Screenshot case study (con ?v=2 en casos.html)
│   │   ├─ mendieta.jpg
│   │   ├─ lulitas.jpg
│   │   ├─ estanteria.jpg
│   │   ├─ salamat.jpg
│   │   └─ parrilla.jpg
│   ├─ /js/
│   │   ├─ components-loader.js  ← Fetch + inject components
│   │   ├─ modal.js              ← Service modals + budget modal + hash auto-open
│   │   ├─ main.js               ← Lenis, header scroll, mobile nav, magnetic CTAs, WhatsApp, counters, page transitions, scroll-top
│   │   ├─ animations.js         ← GSAP hero intro, crystal mouse follow, parallax, pillars
│   │   └─ /vendor/
│   │       ├─ gsap.min.js
│   │       ├─ ScrollTrigger.min.js
│   │       └─ lenis.min.js
│   └─ /downloads/               ← Outputs del script de tarjeta
│       ├─ vantia-tarjeta-frente.pdf + .png
│       └─ vantia-tarjeta-reverso.pdf + .png
├─ /scripts/
│   └─ generate_business_card.py ← Genera la tarjeta empresarial
├─ _headers                      ← Cloudflare cache rules
├─ README.md
└─ HANDOFF.md                    ← Este archivo
```

---

## Cache headers (`_headers`)

```
/assets/fonts/* → max-age=31536000, immutable    (woff2 nunca cambian)
/assets/images/* → max-age=2592000               (30 días, sin immutable)
/assets/css/* → no-cache                         (revalidate ETag siempre)
/assets/js/* → no-cache
/components/* → max-age=300, must-revalidate
/*.html → no-cache
/ → no-cache
/* → security headers (X-Content-Type-Options, Referrer-Policy, etc.)
```

**Lecciones aprendidas**:
- NO usar `immutable` con URLs estables (como `/assets/css/main.css`) — el browser nunca revalida durante 1 año.
- Para imágenes que se reemplazan manteniendo el mismo nombre: usar **`?v=N`** cache-buster en `<img src>` para forzar refresh (ej. `gett-studio.jpg?v=2`).
- CSS links tienen `?v=2` aplicado una vez para escapar cache vieja con immutable.

---

## Sistema de componentes

- Cada HTML tiene placeholders: `<div data-component="header"></div>`
- `components-loader.js` los fetcha de `/components/*.html` e inyecta
- Dispara evento `components:loaded` al terminar
- `main.js` espera ese evento antes de inicializar header scroll, mobile nav, etc.

**Paths absolutos** en componentes (empiezan con `/`) para que funcionen desde cualquier nivel.

---

## Form de contacto (Web3Forms)

- URL: `https://api.web3forms.com/submit`
- **Access key**: `9fea70c9-7d29-427f-8e95-9de55c8491b5` (público y safe, está atado a admin@vantia.digital)
- Honeypot anti-spam: `<input name="botcheck">`
- Submit con fetch async, status visual de "Enviando…" / "Mensaje enviado" / error
- Subject preconfigurado: "Nuevo contacto · Vantia Digital"
- Recibe a: `admin@vantia.digital`

### Modal de presupuesto (en `/components/service-modals.html`)
- 3 modales detalle de servicio (data-modal-trigger=ingenieria-web / seo-tecnico / paid-media)
- Botón "Presupuesto de X" → abre **budget modal** sobre el service modal (z-index 8800 > 8500)
- Budget modal form → opens `mailto:admin@vantia.digital` con servicio prerellenado en subject

---

## Datos de contacto

| | |
|---|---|
| Email | admin@vantia.digital |
| WhatsApp | +34 644 923 374 |
| Calendly | https://calendly.com/admin-vantia/30min |
| TikTok | https://www.tiktok.com/@vantiadigital |
| Instagram | https://www.instagram.com/vantiadigital/ |
| YouTube | https://www.youtube.com/@Vantia.Digital |
| LinkedIn | https://www.linkedin.com/company/vantia-digital/ |
| Ubicación | Barcelona, España |
| Horario | Lun-Vie · 09:00–18:00 CET |

---

## Casos de éxito (`casos/index.html` → `/casos/`)

Filtro **single-dimension por Industria** (chips). 6 cases reales actualmente:

| Industria | Cliente | URL |
|---|---|---|
| Comercio · Retail | GeTT Studio | https://vantiadigital.github.io/Gett/ |
| Gastronomía | Mendieta | https://vantiadigital.github.io/Mendieta/ |
| Gastronomía | Salamat Clot | https://vantiadigital.github.io/Salamat/ |
| Gastronomía | Los Hermanos Parrilleros | https://vantiadigital.github.io/Parrilla/index.html |
| Diseño · Creativo | Lulitas Designs | https://vantiadigital.github.io/LulitasDesign/ |
| Editorial · Cultural | La Estantería del Horizonte | https://vantiadigital.github.io/La-Estanter-a/index.html |

### Implementación del filtro
- Cada `<article class="case case--live">` tiene `data-industry="..."`
- Chips `.filter-chip` con `data-filter="industry"` `data-value="..."`
- JS inline al final de `casos.html` (~30 líneas)
- `.case[hidden] { display: none; }` — fix de especificidad para que `hidden` gane sobre `.case { display: flex }`
- Empty state cuando ningún case matchea

### "Stretched link" — toda la tarjeta clickable
```css
.case--live { cursor: pointer; }
.case--live .case__link::after {
  content: ''; position: absolute; inset: 0; z-index: 2;
}
```
El link real está en su posición, su `::after` cubre toda la tarjeta capturando clicks.

### Indicador LIVE
`.case--live .case__name::before` → puntito verde pulsante (`#4ADE80`) junto al nombre.

### Para agregar un caso nuevo
1. Descargar screenshot (Microlink o thum.io). Pattern:
   ```bash
   curl -sL -A "Mozilla/5.0" "https://api.microlink.io/?url=URL_ENCODED&screenshot=true&meta=false&embed=screenshot.url&viewport.width=1440&viewport.height=900&waitForTimeout=4000" -o raw.png
   ```
2. Optimizar con PIL: resize 1200x750, JPEG q90, save como `/assets/images/[client].jpg`
3. Agregar `<article class="case case--live" data-industry="...">` en `casos.html`
4. Si la industria es nueva: agregar chip al filter-group
5. Si quiere fallback gradient único: agregar `.mockup--N` en el `<style>` block

---

## Conceptos / contenido clave

### Home (`index.html`)
- Hero: cristal SVG con mouse parallax (GSAP) + autorrotación
- Marquee inferior con 5 citas (Proverbio chino, George Box, Aristóteles, Saint-Exupéry, Da Vinci)
- 3 pilares clickables → abren modales de servicio
- Stats con counters (99 PageSpeed, 450% ROAS, 100% código a medida)
- CTA "Sesión gratis" → Calendly

### Filosofía de la marca (`/pages/nosotros.html`)
> "Vantia Digital nace de algo evidente que el mercado prefiere ignorar: **la mayoría de agencias venden diseño**. Webs preciosas que no convierten. Campañas creativas sin tracking. Estrategias virales sin retorno medible."

> "Construimos sistemas digitales que funcionan para el ROI. Donde cada decisión se justifica con datos y cada acción tiene una métrica al lado."

Sección **"¿Te suena familiar?"** con 6 pain-points para que el cliente se identifique.

### Sobre Facundo Goette (fundador)
SECCIÓN ELIMINADA — el usuario decidió quitarla. Si la querés agregar de vuelta, fue la sección 06 de nosotros.html con foto placeholder y bio breve.

---

## Tono / voz

- **Tuteo de España** (tú/quieres/dime/coste/dinero) en TODO output visible de Vantia. NUNCA voseo argentino. Ver `memory/tone_spain_tuteo.md`. (Incluye el chat con Facu: también tuteo España.)
- **Sin emojis pictográficos**; usar · — → y jerarquía tipográfica. Ver `memory/no_emoji_icons.md`.
- **No inventar datos** (ni métricas ni stats dudosas). La transparencia es el moat.
- **Nunca menospreciar al cliente**: si pierde dinero es por falta de información, no por "tonto".
- Mezcla técnico-sobrio + accesible. Posición de marca: agencia **técnica**, NO creativa.
- Diferencia: **honestidad, datos, métricas verificables**. Frase clave: "Precisión matemática".

---

## REGLAS DEL USUARIO (NO violar)

1. **NUNCA modificar visual o comportamiento sin permiso explícito**. Preguntar primero con opciones claras.
2. **No inventar datos en portfolio**. La transparencia es el moat competitivo de la marca. No agregar métricas falsas a casos sin números reales.
3. **Mantener punto medio** `·` (no punto bajo `.`) en "Vantia · Marketing Digital"
4. **No tocar el logo** — son polígonos simples sin strokes internos. Las versiones con stroke se ven "hollow" y al usuario no le gustan.
5. Si una "optimización" puede afectar visual → preguntar y testear antes
6. Aplicar cambios safe (sin efectos visuales) directamente. Para todo lo demás: pregunto.

---

## Quirks / bugs resueltos

| Issue | Fix |
|---|---|
| Inter TTF extraído de woff2 solo tenía "A" | Reemplazado con `Inter-Variable.ttf` de google/fonts repo |
| `_headers` con `immutable` en CSS rompía updates | Cambiado a `no-cache` para CSS/JS, con `?v=N` cache-bust único |
| Mobile nav usaba `inset: var(--header-h) 0 auto 0` (incompatible Safari mobile) | Cambiado a `top/left/right` explícitos |
| `[hidden]` no ganaba contra `.case { display: flex }` | Agregado `.case[hidden] { display: none; }` |
| Components no cargaban si HTML cacheaba con immutable | Cache rules nuevas resuelven |
| GeTT screenshot no se actualizaba | Cache-buster `?v=2` en src del img |
| iPhone notch tapaba header | `env(safe-area-inset-top)` + `viewport-fit=cover` |
| Empresa de fonts: Inter latin subset .woff2 muy pequeño en TTF | Para script Python: usar Inter-Variable completo |

---

## Cómo hacer tareas comunes

### Cambiar texto en un componente
Editar `/components/<file>.html` → commit + push → ~60s online (cache no-cache en `/*.html`).

### Cambiar CSS
Editar `/assets/css/main.css` → commit + push → browser revalida ETag automático (no-cache).

### Agregar caso de éxito
Ver sección "Para agregar un caso nuevo" arriba.

### Regenerar la tarjeta de contacto PDF
```bash
python scripts/generate_business_card.py
```
Output: 4 archivos en `/assets/downloads/`.

### Deploy
Auto. Solo `git push origin main`. Cloudflare detecta el push y redeploya en 30-60s.

### Ver el deploy en Cloudflare
Dashboard → Workers & Pages → vantiadigital → Deployments.

---

## Open TODOs / ideas para más adelante

- Desactivar la URL `*.workers.dev` para que solo `vantia.digital` sea pública (SEO duplicate)
- Reemplazar screenshots de mshots por capturas propias de mejor calidad
- Si crecen los casos: volver a multi-dimension filter (Industria + Necesidad + Tipo)
- Cuando haya casos con métricas reales: migrar de filtro por industria a vista por servicio
- Considerar agregar sección "Sobre el fundador" si el usuario quiere
- Optimizaciones PageSpeed adicionales: inline critical CSS, defer animations.css (CUIDADO: animations.css tiene estados iniciales críticos como `[data-reveal] { opacity: 0 }` — deferirlo causa FOUC)

---

## Archivos importantes para preservar

Si necesitás revisar diseños / estilos pasados:
- `/scripts/generate_business_card.py` — script PDF tarjeta empresarial
- `_headers` — cache rules
- `/assets/css/main.css` — todos los estilos
- `/components/*` — componentes compartidos

---

## Datos para una nueva sesión de Claude Code

```
Proyecto: Vantia · Marketing Digital
Path: C:\Users\facun\Documentos\Vantia Digital\Vantia Digital Web
Repo: github.com/VantiaDigital/Vantia.digital
Stack: HTML + CSS + JS vanilla + GSAP + Lenis + Cloudflare Pages
Deploy: auto on git push to main
Domain: vantia.digital (live)
User: VantiaDigital, fundador Facundo Goette
Email: admin@vantia.digital
Tone: técnico-sobrio, TUTEO DE ESPAÑA (no voseo), sin emojis, no inventar datos
Regla principal: preguntar antes de cualquier cambio visual o de comportamiento
```

---

_Última actualización: handoff antes de cambio de sesión por context window full. Estado del proyecto: estable, en producción, ajustes incrementales._
