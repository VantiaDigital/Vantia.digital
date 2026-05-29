# HANDOFF — sesión 2026-05-26

Estado al cierre. La próxima sesión empieza desde acá.

---

## 1 · Lo que se completó en sesiones anteriores

### Stack analítica profesional en 3 sitios
- **Vantia** (`vantia.digital`) — GA4 `G-SV13BVRDX9` · GTM `GTM-5H74KP28` · Clarity `wv202iqp3m`
- **Los Hermanos Parrilleros** (`loshermanosparrilleros.pages.dev`) — GA4 `G-ZZ8JT2WQHH` · GTM `GTM-KTJMHHCS` · Clarity (configurado en su GTM)
- **La Estantería** (`la-estanteria.pages.dev`) — GA4 `G-QSTQ5PHZYK` · GTM `GTM-KTGP8945` · Clarity `wv5ce1ogwy`

Cada sitio tiene: Consent Mode v2 + banner de cookies + eventos personalizados + páginas legales (privacidad/cookies/aviso-legal) + sitemap/robots + Search Console + Looker Studio dashboard.

### Template reusable para clientes
- Carpeta `C:\Users\facun\Documentos\Vantia Digital\Analitica\`
  - `GTM-template-vantia.json` — contenedor importable
  - `PLAYBOOK-ANALITICA.md` — proceso paso a paso

### Pendientes analítica (tareas del usuario)
- Marcar conversiones en GA4 con ⭐ cuando aparezcan los eventos (1-2 días):
  - Vantia: `enviar_formulario`, `click_agendar_llamada`
  - Parrilleros: `enviar_reserva`, `click_whatsapp`
  - La Estantería: `enviar_contacto`
- Verificar cada sitio: visitar + aceptar cookies + ver en GA4 Tiempo real

---

## 2 · Lo que se hizo HOY (26 mayo 2026)

### Brand kit completo en 3 lugares
**Notion · Brand Assets** (page id `311f806f-0267-80e8-a3c5-d81451b828f4`)
- Sección "Activos esenciales" arriba con todos los logos embebidos desde la web pública
- Sección "Brand Kit Social" con paleta, fonts, specs por plataforma
- Contenido viejo conservado abajo como "Recursos heredados"

**Canva** (Brand Kit id `kAHHmBYxiJg`)
- Logo configurado vía import desde web
- Carpeta "Vantia · Social" creada (id `FAHKwqry2DE`)
- Assets subidos (ver lista de IDs en sección 4)
- **Pendiente del lado del usuario:** cargar manualmente en el Brand Kit los 5 colores (`#1A1813 #3C3A2F #C1834B #ECE8D8 #A99B80`) y las fonts Fraunces + Inter, en el panel de Canva

**Web Vantia · nuevos archivos** (commiteados en `45b64d9` y `5e068e9`)
- `assets/images/logo-light-bg.svg` (V dark + A cobre, principal sobre claro)
- `assets/images/logo-dark-bg.svg` (V cream + A cobre, sobre oscuro)
- `assets/images/logo-mono-dark.svg` (todo dark)
- `assets/images/logo-mono-light.svg` (todo cream)
- `assets/images/logo-horizontal-claro.png` (logotipo con texto, 2938×530)
- `assets/images/logo-horizontal-oscuro.png` (2938×530)
- `assets/images/logo-vertical-claro.png` (apilado, 2047×1221)
- `assets/images/logo-vertical-oscuro.png` (2047×1221)
- `scripts/generate_logo_variants.py` — el script que los genera

---

## 3 · CORRECCIÓN IMPORTANTE PENDIENTE

**El texto de los logotipos PNG está mal.** Hoy se generaron con `"Vantia · Marketing Digital"`, pero el usuario aclaró:

> "El texto del logo es **Vantia Digital**, sin el marketing, eso era solo para las tarjetas de contacto."

**Acción requerida en la próxima sesión:**
1. Editar `scripts/generate_logo_variants.py` → cambiar:
   - `TEXT_LEFT = "Vantia "` y `TEXT_DOT = "·"` y `TEXT_RIGHT = " Marketing Digital"`
   - Por: `TEXT_LEFT = "Vantia "` y `TEXT_DOT = "·"` y `TEXT_RIGHT = " Digital"` (mantiene el · cobre) **OR** texto plano `"Vantia Digital"` sin punto. **Pendiente: confirmar formato con el usuario.**
2. Re-correr el script.
3. Re-subir los 4 PNGs a Canva (reemplazan los existentes o agregan nuevos — los IDs antiguos quedan obsoletos).
4. Actualizar Notion con los nuevos PNGs.
5. La tarjeta de visita (`scripts/generate_business_card.py`) **se queda como está** — para impresión sí va "Vantia · Marketing Digital".

---

## 4 · IDs y referencias clave

### Canva assets de Vantia (carpeta "Vantia · Social", id `FAHKwqry2DE`)
| Asset | ID Canva |
|---|---|
| Logo favicon (V+A cuadrado redondeado) | `MAHKwvDDyPM` |
| Logo SVG sobre claro (V dark + A cobre) | `MAHKwlbWK_A` |
| Logo SVG sobre oscuro (V cream + A cobre) | `MAHKwrN0dC8` |
| Logo monocromo oscuro | `MAHKwgoJtxE` |
| Logo monocromo claro | `MAHKwgbX7v4` |
| Logotipo horizontal claro **(texto a corregir)** | `MAHKwg_VV0A` |
| Logotipo horizontal oscuro **(texto a corregir)** | `MAHKwtq770E` |
| Logotipo vertical claro **(texto a corregir)** | `MAHKwpLxItY` |
| Logotipo vertical oscuro **(texto a corregir)** | `MAHKwlG6ivU` |
| Tarjeta de visita frente | `MAHKwo0fIGo` |
| Tarjeta de visita reverso | `MAHKwjnU0Wk` |
| Logo (versión inicial extraída de web) | `MAHKwvDDyPM` |

### Notion · páginas relevantes
- **Brand Assets:** `311f806f-0267-80e8-a3c5-d81451b828f4`
- **Plan Operativo Maestro (en Google Docs):** `1psunNefW6VYaZfeY2L4qoEPFyT43ivctyHRuMEKjwXk` — referencia estratégica, NO ejecutar ciegamente

### Paleta Vantia (los 5 hexes oficiales)
```
#1A1813  Dark      — fondo principal
#3C3A2F  Olive     — fondos secundarios
#C1834B  Copper    — acento, punto medio "·"
#ECE8D8  Cream     — texto sobre dark, isotipo V
#A99B80  Muted     — texto secundario
```

### Fonts
- **Fraunces** (serif) — display/títulos · `assets/fonts/Fraunces-Regular.ttf`
- **Inter** (sans) — body · `assets/fonts/Inter-Variable.ttf`

---

## 5 · Otros pendientes abiertos (del usuario en este turno)

### Pedidos sin completar
1. **Revisar LinkedIn personal del usuario** — `https://www.linkedin.com/in/facundo-goette/` — el usuario pidió sugerencias para que "venda junto con Vantia". Pendiente: el browser tool no llegó a entrar. Próxima sesión: intentar acceder vía Claude in Chrome, o pedirle al usuario que copie el contenido del perfil para revisarlo.

2. **Archivo Figma local** — `C:\Users\facun\Downloads\Logo Vantia Main.svg` (3.2MB, no se llegó a leer). El usuario aclaró que igualmente está desactualizado. Probablemente no haga falta abrirlo.

3. **Generar plantillas de contenido en Canva** — el siguiente paso natural: usar `generate-design` con `brand_kit_id="kAHHmBYxiJg"` para producir:
   - Banner LinkedIn (empresa 1128×191, personal 1584×396)
   - Banner YouTube (2560×1440, safe area 1546×423)
   - Post cuadrado IG/LinkedIn (1080×1350)
   - Story/Reel/TikTok (1080×1920)
   - Thumbnail YouTube (1280×720)

### Pendientes "filosóficos" abiertos
- **Decisión:** Figma Pro vs solo Canva Pro vs híbrido. Hoy quedó: Canva Pro como herramienta operativa. Figma free para masters si hace falta.
- **(a)** Blindaje de los 3 selectores frágiles del tracking de Vantia (`.case`, `.whatsapp-fab`, `<section>` para `ver_seccion`) — no urgente, sólo si se rediseña la web.
- **(b)** Sumar "Analítica y Medición" como **servicio** en la web de Vantia (4° pilar, dentro de Ingeniería Web, o en página Servicios). Decisión pendiente.

---

## 6 · Reglas del usuario (siempre vigentes)

- **No modificar la página si va a verse distinto** sin preguntar antes (las marcas de marca son sagradas).
- **No inventar datos de portfolio** — los demos son demos, los clientes reales son reales.
- **Voseo argentino** ("vos", "tenés", "decime") en todo lo que se escribe.
- **El "·" punto medio (no período)** es la firma de marca en cobre. Salvo que ahora con "Vantia Digital" se redefina (ver pendiente §3).
- **Plan Operativo Maestro como referencia, no como instrucciones a auto-ejecutar.**
- **Honestidad operativa:** decir qué se puede y qué no se puede hacer desde la sesión (no soy abogado, no puedo loguear en paneles, etc.).

---

## 7 · Para arrancar la próxima sesión

1. Resolver el pendiente §3 (texto del logotipo).
2. Continuar con generación de plantillas en Canva (§5.3).
3. Revisar LinkedIn (§5.1).

La carpeta `Analitica` con el playbook + template GTM **no se toca** — está cerrada.

---
*Última actualización: 26 mayo 2026.*
