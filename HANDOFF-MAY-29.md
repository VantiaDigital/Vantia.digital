# HANDOFF — sesión 2026-05-29

Estado al cierre. La próxima sesión empieza desde acá. Continúa del HANDOFF-MAY-26.md.

---

## 0 · Reglas del usuario (SIEMPRE vigentes — leer primero)

- **Tono: tuteo de España** (tú/tienes/quieres/dime/elige/dinero/coste) en TODO output visible de Vantia (web, posts, copys, scripts que generan PNGs, bios). NUNCA voseo argentino. Esto REEMPLAZA la regla vieja de "voseo" de handoffs anteriores. Ver `memory/tone_spain_tuteo.md`. La conversación interna del agente con el usuario SÍ es en voseo (él es argentino).
- **Sin emojis pictográficos** (📍🕒🌐✅⚠️🚀 etc.) en nada visible de Vantia. Usar · — → y jerarquía tipográfica. Ver `memory/no_emoji_icons.md`.
- **No inventar datos.** Esta sesión se cazaron 2 veces métricas fabricadas en gett.html (PageSpeed 98, LCP 1.2s) y se quitaron. Nada de cifras inventadas (ni de Vantia ni stats genéricas dudosas).
- **No modificar lo visual sin preguntar.**
- **Tarjeta de visita** (`scripts/generate_business_card.py`) se queda con "Vantia · Marketing Digital" — es para impresión, NO se toca.
- **Honestidad operativa:** decir qué se puede y qué no desde la sesión.

---

## 1 · Lo que se hizo esta sesión

### Logo (tarea original)
- Texto del logotipo cambiado a "Vantia Digital" PLANO (sin punto medio ·, un solo color). `scripts/generate_logo_variants.py` simplificado.
- 4 PNG regenerados (horizontal/vertical, claro/oscuro) + commit + push.
- Re-subidos a Canva. **IDs Canva NUEVOS** (carpeta "Vantia · Social", id `FAHKwqry2DE`):
  - Horizontal claro: `MAHKwlenRtQ`
  - Horizontal oscuro: `MAHKwqNKal0`
  - Vertical claro: `MAHKwpJhWLo`
  - Vertical oscuro: `MAHKwtSPadY`
- IDs viejos OBSOLETOS (`MAHKwg_VV0A`, `MAHKwtq770E`, `MAHKwpLxItY`, `MAHKwlG6ivU`) — el usuario los borra a mano en Canva si quiere.
- Notion "Brand Assets" (`311f806f-0267-80e8-a3c5-d81451b828f4`) actualizado con los IDs nuevos.

### Web — cambios grandes (todo commiteado y pusheado a main)
- ROAS del hero: 250% → **450%** (index.html).
- Rename de servicios en texto VISIBLE: "Paid Media" → **"Campañas de anuncios"**; "Ingeniería Web" → **"Optimización Web"**. Los IDs internos (`paid-media`, `ingenieria-web`, `data-modal-trigger`) se MANTIENEN para no romper tracking ni hashes.
- `pages/servicios.html` reescrita a **long-form educativo** (3 servicios, secciones largas tipo artículo) + cross-link a un caso por servicio (Optimización→GeTT, SEO+GEO→Estantería, Campañas→Mendieta).
- Hero del index: figura geométrica cambiada de pentágono (5 puntas) a **hexágono (6 puntas)** con estrella de David interior.
- **6 páginas de caso de éxito** nuevas en `pages/casos/`: gett, mendieta, salamat, parrilleros, lulitas, estanteria. Cada una con UNA acción destacada única (NO genéricas):
  - GeTT → Performance + mobile-first
  - Mendieta → Tracking de conversiones por WhatsApp
  - Salamat → SEO local + nicho dietético
  - Parrilleros → Lead generation B2B para eventos
  - Lulitas → Catálogo digital sin e-commerce
  - Estantería → SEO Técnico + GEO editorial
- `pages/casos.html`: cards clickeables en toda la superficie (`.case__cover-link`) → abren la página del caso. Cada card con tag de acción + 2 botones al pie ("Ver sitio en vivo" → subdominio, "Pedir presupuesto similar" → contacto).
- **TODO el sitio pasado a tuteo España** (se cazó voseo en varias pasadas; última: "aplicás" en servicios). 404 también.
- **Todos los emojis quitados** de web + scripts + handoffs.
- Accesibilidad (recomendado por skill ui-ux-pro-max): **skip-link** + **focus-visible** en las 15 páginas. Contraste de `.footer__location` corregido.

### Web — fixes de carga/performance (MUCHA iteración, leer con atención)
Causa raíz de los problemas: el sitio escondía todo el contenido (opacity:0) y dependía de GSAP (125KB) para revelarlo, + el header se cargaba por fetch JS. Soluciones aplicadas:
- **page-transition overlay ELIMINADO** por completo (HTML/CSS/JS). Causaba traba y doble-aparición. Quedó un loader "Vantia..." dinámico que solo aparece si la navegación tarda >350ms.
- **Reveals con IntersectionObserver nativo** (`main.js` → `initReveals`), reemplaza el `setupReveals` de GSAP. Above-the-fold instantáneo, below-fold al scroll, cero dependencia de GSAP. CSS en animations.css (`.is-visible`).
- **Header INLINEADO** en las 15 páginas (`scripts/build_inline_header.py`). Ya NO se carga por fetch. **Fuente única: `components/header.html`. Si cambia el header, editar ese archivo y RE-CORRER el script.** Bloque marcado con comentarios `BUILD:header:start/end`.
- **Hero del index:** se quitó el gateo GSAP que dejaba los botones invisibles. Ahora el texto del hero se ve por defecto + fade CSS. `--fs-hero` reducido para que el CTA entre arriba del pliegue en notebooks. Valor final: `clamp(2.65rem, 5.9vw, 6rem)`.
- **Bug del loader pegado** (footer "Optimización Web" abre modal y el loader quedaba tapando): arreglado — el loader no se dispara en links que abren modal/presupuesto/scroll-top ni en la misma página.
- **Preload de fuentes** críticas (Fraunces 600, Fraunces italic, Inter 400) en todas las páginas.

### LECCIÓN CRÍTICA DE CACHE (no repetir el error)
- Puse `_headers` de `/assets/css/*` y `/assets/js/*` en `immutable` (cache 1 año). **Eso causó que el navegador sirviera CSS/JS viejo** y el usuario veía "se ve igual" en cada cambio. Varios fixes fueron invisibles por esto.
- REVERTIDO a `public, no-cache` (revalida con ETag, siempre fresco).
- Bump de versión a `?v=6` en TODAS las refs CSS/JS de las 15 páginas. Importante: `main.js`, `animations.js`, `modal.js` antes NO tenían `?v` — ahora sí (`?v=6`).
- **REGLA:** mientras CSS/JS estén en `no-cache`, no hace falta bumpear (revalida solo). Si alguien vuelve a poner `immutable`, DEBE bumpear `?v` en cada cambio o el usuario no ve nada.

### Analítica (GTM/GA4)
- Evento nuevo `ver_caso_detalle` (dispara al abrir una página de caso). Configurado por el usuario en GTM.
- `click_caso` ahora lleva parámetro `accion` (`ver_detalle` / `ver_sitio_vivo` / `pedir_presupuesto`). `analytics-events.js` actualizado.
- Dimensión GA4 `caso` YA EXISTÍA (se reusa, no duplicar). Dimensión `accion` pendiente/opcional.
- IDs: GA4 `G-SV13BVRDX9`, GTM `GTM-5H74KP28`, Clarity `wv202iqp3m`.

### Contenido de redes generado (en `assets/downloads/`)
LinkedIn (`linkedin/`):
- `empresa-foto-perfil.png` (400×400, logo sobre cream)
- `empresa-banner.png` (1584×268, solo tipografía)
- `personal-banner.png` (1584×396)
- `posts/`: empresa-01-bienvenida-corta, empresa-02-portfolio, empresa-03-tesis-hubspot, personal-01-anuncio, personal-02-tecnico
- `screenshots/`: gett, parrilleros, estanteria (capturas reales vía Microlink)

Instagram (`instagram/`):
- `stories/`: 01-bienvenida-empresa, 02-poll-ga4
- `carruseles/ga4/`: 8 slides (3 errores GA4)
- `carruseles/proceso/`: 6 slides (proceso Vantia)
- `feed/`: feed-01 a feed-07 (citas, tips, checklist — generados esta sesión)

Scripts generadores: `generate_logo_variants.py`, `generate_linkedin_assets.py`, `generate_linkedin_posts.py`, `generate_ig_assets.py`, `generate_ig_feed.py`, `fetch_client_screenshots.py`.

Copys (textos para pegar): About empresa, About personal, headlines personales (3 opciones), tagline, bios IG, captions de posts empresa/personal — TODOS redactados en chat, en tuteo. **PENDIENTE: faltan escribir los captions de los 7 posts feed-01..07 de IG** (el usuario los pidió justo al cierre).

### Otros
- **Research de competencia** hecho: 6 agencias (Convertiam, Elabs, InboundCycle, Cyberclick, Adrenalina, Webpositer). Hueco que Vantia puede ocupar: hablarle al DUEÑO de PYME, no a marketers. Clasificación skill: "B2B Service" (trust & authority).
- **Security review:** sitio limpio (estático, sin superficie real de ataque).
- **Skill ui-ux-pro-max** instalado en `~/.claude/skills/ui-ux-pro-max/` (este entorno NO lo auto-carga como Skill; se usa leyendo su contenido directo).
- **Plugins en OpenCode:** el usuario instaló el ecosistema superpowers en OpenCode (herramienta SEPARADA, no este entorno). No sirven acá. Se limpiaron los artefactos de plugins de OpenCode (sin tocar su núcleo).

---

## 2 · Problema Zscaler / bloqueo corporativo (CONTEXTO IMPORTANTE)

- `vantia.digital` fue bloqueado por **Zscaler** (WAF corporativo de HPE) como "Malware". Causa: guilt-by-association — había 6 links a `*.pages.dev` en casos.html, y `*.pages.dev` está en blacklist de WAFs corporativos.
- **Fix aplicado:** se quitaron los 6 links a `.pages.dev` de casos.html. VirusTotal y Cisco Talos dan vantia.digital LIMPIO. Es solo Zscaler con política conservadora.
- Esperar re-crawl de Zscaler (7-30 días). Verificable en sitereview.zscaler.com (lookup público, sin cuenta).
- El usuario dijo: **"Zscaler dalo por olvidado, lo chequearé luego."**
- Los sitios de cliente viven en `.pages.dev` (bloqueados en redes corporativas). Los botones "Ver sitio en vivo" de casos.html apuntan a subdominios `*.vantia.digital` que **NO están configurados** (gett.vantia.digital, etc.). El usuario dijo **"subdominios no va a pasar"** (no los configura ahora). Mientras tanto esos botones llevan a 404 — tenerlo presente.
- Cuentas Cloudflare: la principal de **Vantia** (tiene vantia.digital + proyectos gett, mendieta, salamat-7hx, lulitasdesign) y una **personal** (tiene loshermanosparrilleros + la-estanteria). Si algún día se hacen los subdominios, parrilleros y estanteria requieren cross-account (Camino B con TXT de verificación).

---

## 3 · EL PLAN ACTUAL (actualizado por el usuario al cierre)

Fase 1 (lo inmediato):
```
Instagram                          LinkedIn (en paralelo)
1. Armar contenido base (HECHO)    1. Armar perfil empresa + personal
2. Seguir amigos → seguidores      2. Conectar con contactos
3. Ads IG con poco presupuesto     3. Pedir recomendaciones a amigos
```
Luego: plan de contenido a la par de **lead gen** (después de la fase 1).

### Pendientes concretos para arrancar la próxima sesión
1. **Escribir los 7 captions de IG** (feed-01..07) con hashtags — quedó pendiente, el usuario lo pidió.
2. **Subir contenido a IG:** perfil (foto + bio) + grid de 9 + stories. Checklist de orden ya dado en el chat (orden sugerido: feed-01, carrusel ga4, feed-04, portfolio, feed-06, feed-02, carrusel proceso, feed-05, feed-03).
3. **Subir contenido a LinkedIn** empresa + personal (paquete listo, copys dados).
4. **Ads IG** (después de grid + primeros seguidores): definir post a promocionar, segmentación Barcelona+PYMES, presupuesto mínimo, medición con UTMs/GA4.
5. El usuario NO puede automatizar subidas a IG/LinkedIn de forma confiable (detección de bots + acciones que requieren su OK). El agente arma todo y el usuario sube. La extensión Claude in Chrome falló con permisos de dominio en intentos previos.

### Diferido (no ahora)
- Subdominios `*.vantia.digital` (Camino B).
- Zscaler (chequear luego).
- Dimensión GA4 `accion` (opcional).
- Lead gen (fase 2).
- Brand Kit Canva: cargar manualmente los 5 hexes + fonts + logos (pendiente del lado del usuario, de antes).

---

## 4 · Referencias clave

| Ítem | Valor |
|---|---|
| Repo | github.com/VantiaDigital/Vantia.digital |
| Local | C:\Users\facun\Documentos\Vantia Digital\Vantia Digital Web |
| Deploy | Cloudflare Pages (auto on push to main) |
| Dominio | vantia.digital |
| GA4 | G-SV13BVRDX9 |
| GTM | GTM-5H74KP28 |
| Clarity | wv202iqp3m |
| Canva Brand Kit | kAHHmBYxiJg |
| Canva carpeta Social | FAHKwqry2DE |
| Notion Brand Assets | 311f806f-0267-80e8-a3c5-d81451b828f4 |
| Email | admin@vantia.digital |
| WhatsApp | +34 645 720 420 |
| Calendly | calendly.com/admin-vantia/30min |

### Paleta (sin cambios)
```
#1A1813 Dark espresso · fondo principal
#3C3A2F Olive · fondos secundarios
#C1834B Copper · acento + punto medio ·
#ECE8D8 Cream · texto sobre dark
#A99B80 Muted · texto secundario
#77431C Brown · hover del cobre (solo en CSS)
```
### Fonts
- Fraunces (serif) — títulos. `Fraunces-Regular.ttf`
- Inter (sans) — body. `Inter-Variable.ttf` (OJO: `Inter-Regular.ttf` está ROTO, renderiza tofu — usar siempre la Variable)

### Memory files creados esta sesión
- `memory/tone_spain_tuteo.md` — tuteo España, reemplaza voseo
- `memory/no_emoji_icons.md` — prohibido emojis

---

## 5 · Para arrancar la próxima sesión

1. Leer reglas (§0) — tuteo España + no emojis + no inventar datos.
2. Escribir los 7 captions de IG (§3.1) — es lo primero pendiente.
3. Seguir el plan fase 1 (§3): subir contenido IG + LinkedIn.
4. NO tocar: subdominios, Zscaler (diferidos por el usuario).
5. Cache CSS/JS está en `no-cache` — los cambios se ven con reload normal/Ctrl+F5. No volver a `immutable` sin sistema de bump de `?v`.

*Última actualización: 29 mayo 2026.*
