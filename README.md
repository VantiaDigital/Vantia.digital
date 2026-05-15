# Vantia.digital

Web oficial de Vantia Digital - Agencia de marketing digital con precisión matemática.

## Stack

- HTML5 + CSS3 + JavaScript vanilla
- GSAP para animaciones
- Lenis para smooth scroll
- Deploy en Cloudflare Pages

## Estructura

- `index.html` - Home
- `pages/servicios.html` - Servicios
- `pages/casos.html` - Casos de éxito
- `pages/nosotros.html` - Sobre nosotros
- `pages/contacto.html` - Contacto

## Componentes compartidos

Los componentes (`header`, `footer`, `whatsapp`, `service-modals`) se cargan de forma dinámica con `fetch` desde `/components/` mediante el script `assets/js/components-loader.js`.

## Desarrollo local

```bash
python -m http.server 5500
```

Abrir en el navegador: http://localhost:5500/
