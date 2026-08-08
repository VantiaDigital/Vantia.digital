# -*- coding: utf-8 -*-
"""
Regenera la rejilla de "Tu web a medida": chips de filtro, tarjetas de modelo
y tarjetas de caso real.

Cada tarjeta NOMBRA los sectores que cubre. Sin eso, un visitante no sabe si
el modelo de despacho le sirve a su gestoria, y la seccion deja de vender.

Las tarjetas de caso real van visualmente diferenciadas y etiquetadas como
cliente real: son trabajo hecho, no maquetas, y no deben confundirse.

    python scripts/build_modelos_grid.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINA = os.path.join(ROOT, "tu-web-a-medida.html")
I18N = os.path.join(ROOT, "assets", "js", "i18n.js")

# --- Que esta publicado y donde ----------------------------------------
# Solo salen a la rejilla los modelos con URL aqui. Uno sin desplegar seria
# una tarjeta con la portada rota y un enlace muerto.
#
# Mientras Facu no asigne el dominio propio en el panel de Cloudflare, la
# tarjeta apunta al .pages.dev, que si responde. Al activar el dominio se
# cambia la linea por "https://<slug>.vantia.digital" y se vuelve a generar.
URLS = {
    "clinica-dental": "https://clinica-dental.vantia.digital",
    "fisioterapia":   "https://fisioterapia.vantia.digital",
    "yoga":           "https://yoga.vantia.digital",
    "construccion":   "https://construccion.vantia.digital",
    "reformas":       "https://reformas.vantia.digital",
    "despacho":       "https://despacho.vantia.digital",
    "logistica":      "https://logistica.vantia.digital",
    "distribucion":   "https://distribucion.vantia.digital",
    "formacion":      "https://formacion.vantia.digital",
    "inmobiliaria":   "https://inmobiliaria.vantia.digital",
    "automocion":     "https://automocion.vantia.digital",
    # Recien desplegados; pasan a <slug>.vantia.digital cuando tengan dominio.
    "turismo":        "https://turismo-ekc.pages.dev",
    "impresion3d":    "https://impresion3d-ewp.pages.dev",
    "tienda":         "https://tienda-9hc.pages.dev",
}

# --- Filtros -----------------------------------------------------------
CHIPS = [
    ("all",        "Todos",                    "All"),
    ("salud",      "Salud",                    "Health"),
    ("bienestar",  "Bienestar",                "Wellbeing"),
    ("obra",       "Obra y vivienda",          "Construction & housing"),
    ("profesional","Servicios profesionales",  "Professional services"),
    ("comercio",   "Comercio y distribución",  "Retail &amp; distribution"),
    ("transporte", "Logística y transporte",   "Logistics &amp; transport"),
    ("turismo",    "Turismo y hostelería",     "Tourism &amp; hospitality"),
    ("automocion", "Automoción",               "Automotive"),
    ("creativo",   "Diseño y fabricación",     "Design &amp; making"),
]

# --- Modelos -----------------------------------------------------------
# clave, sector-filtro, subdominio, nombre, sectores que cubre, 4 incluye
MODELOS = [
    ("dental", "salud", "clinica-dental", "Clínica y consulta privada",
     "dental · médica · psicología · nutrición · veterinaria",
     ["Cita online sin llamar, con recordatorio automático",
      "Tratamientos explicados sin tecnicismos",
      "Petición de reseña tras la visita",
      "Informe semanal a la dirección, por correo"]),

    ("fisio", "salud", "fisioterapia", "Fisioterapia y rehabilitación",
     "fisioterapia · osteopatía · podología · logopedia",
     ["Reserva de sesión y de bono desde el móvil",
      "Cada lesión con su explicación y su plazo",
      "Tarifas de sesión suelta y bono, sin permanencia",
      "Recordatorio para que no se pierda una sesión"]),

    ("yoga", "bienestar", "yoga", "Bienestar y actividad",
     "yoga · pilates · centro deportivo · estudio de danza",
     ["Horario de clases siempre al día",
      "Primera clase de prueba en dos toques",
      "Bonos y cuotas explicados sin letra pequeña",
      "Nivel de cada clase, para no venir con miedo"]),

    ("construccion", "obra", "construccion", "Construcción y obra",
     "constructoras · promotoras · arquitectura e ingeniería · rehabilitación",
     ["Cada obra con su ficha técnica y su plazo",
      "Las seis fases, con quién responde en cada una",
      "Solicitud de presupuesto con los datos que hacen falta",
      "Lo que sí se puede prometer, por escrito"]),

    ("reformas", "obra", "reformas", "Reformas e instalaciones",
     "reformas integrales · fontanería · electricidad · climatización",
     ["Horquilla de precio en diez segundos",
      "Calendario de obra firmado antes de empezar",
      "La distribución nueva, antes de tirar el primer tabique",
      "Obras contadas por lo que se decidió, no por la foto"]),

    ("despacho", "profesional", "despacho", "Despacho profesional",
     "abogados · asesorías fiscales y laborales · gestorías · administradores de fincas",
     ["Orientación por situación: área, coste y plazo legal",
      "Honorarios por modalidad, y qué gastos no cobra el despacho",
      "Equipo con número de colegiado comprobable",
      "Bloque propio para comunidades de propietarios"]),

    ("distribucion", "comercio", "distribucion", "Distribución y pedido B2B",
     "mayoristas de alimentación y bebidas a hostelería · imprentas y artes gráficas",
     ["Catálogo de referencias con formato y unidad de venta",
      "Pedido a cuenta, sin pasar por caja",
      "Zonas, días de reparto y hora de corte",
      "Alta de cliente con sus datos fiscales"]),

    ("logistica", "transporte", "logistica", "Logística y transporte",
     "operadores logísticos · transporte de mercancías · mensajería",
     ["Tiempo de tránsito por ruta, origen y destino",
      "Mapa de cobertura y horas de corte",
      "Seguimiento de envío por número de expedición",
      "Presupuesto con peso, medidas y tipo de carga"]),

    ("inmobiliaria", "obra", "inmobiliaria", "Inmobiliaria",
     "compraventa · alquiler · promoción de vivienda",
     ["Buscador con filtros de zona, precio y superficie",
      "Ficha con galería, plano y certificado energético",
      "Recorrido propio para el propietario que vende",
      "Solicitud de valoración de la vivienda"]),

    ("turismo", "turismo", "turismo", "Turismo y alojamiento",
     "hoteles pequeños · hostales · apartamentos turísticos · casas rurales",
     ["Calendario de disponibilidad y precio por noche",
      "Reserva directa, sin comisión de portal",
      "Tipos de habitación con su galería",
      "Qué hay cerca, para vender la estancia entera"]),

    ("automocion", "automocion", "automocion", "Automoción",
     "talleres mecánicos · chapa y pintura · neumáticos · pre-ITV",
     ["Cita pidiendo marca, modelo y matrícula",
      "Presupuesto aprobado antes de tocar nada",
      "Precios orientativos por servicio",
      "Qué hacer con las llaves fuera de horario"]),

    ("formacion", "profesional", "formacion", "Formación y academias",
     "idiomas · refuerzo escolar · formación profesional · autoescuelas",
     ["Horario semanal completo, no un PDF",
      "Convocatorias con fecha, plazas y estado",
      "Prueba de nivel que recomienda curso",
      "Matrícula online, con datos del tutor si es menor"]),

    ("tienda", "comercio", "tienda", "Tienda online",
     "comercio con venta y cobro en la propia web",
     ["Catálogo con filtros y stock a la vista",
      "Ficha con variantes de talla, color y formato",
      "Carrito y proceso de compra completo",
      "Envíos, devoluciones y seguimiento del pedido"]),

    ("impresion3d", "creativo", "impresion3d", "Diseño e impresión 3D",
     "modelos descargables · servicio de impresión · encargos a medida",
     ["El mismo diseño, como archivo o como pieza impresa",
      "Visor 3D que gira de verdad, sin librerías",
      "Presupuesto de impresión por material y acabado",
      "Licencia de uso personal y comercial, a la vista"]),
]

# --- Webs de clientes --------------------------------------------------
# Trabajo entregado. La tarjeta lleva a la web en vivo; debajo, el enlace al
# caso de exito. Van en su propia seccion al final, no mezcladas con los
# modelos: una cosa es lo que sabemos hacer y otra lo que ya hicimos.
# clave, web en vivo, ficha del caso, portada, nombre, sectores, resumen
CLIENTES = [
    ("mendieta", "https://mendieta.vantia.digital", "/casos/mendieta.html",
     "/assets/images/mendieta.jpg", "Mendieta",
     "alimentación con pedido y seguimiento · producto de importación",
     "Tienda de producto argentino en España. Catálogo, pedido y seguimiento."),

    ("parrilleros", "https://vantiadigital.github.io/Parrilla/", "/casos/parrilleros.html",
     "/assets/images/parrilla.jpg?v=2", "Los Hermanos Parrilleros",
     "eventos y catering · servicio a domicilio",
     "Asados a domicilio y para eventos, con reserva y presupuesto."),

    ("gett", "https://gett.vantia.digital", "/casos/gett.html",
     "/assets/images/gett-studio.jpg?v=2", "GeTT",
     "muebles y carpintería a medida · interiorismo",
     "Carpintería a medida, con el proyecto contado pieza a pieza."),

    ("lulitas", "https://lulitas.vantia.digital", "/casos/lulitas.html",
     "/assets/images/lulitas.jpg", "Lulitas",
     "catálogo sin tienda · venta por encargo",
     "Catálogo que enseña el producto y cierra la venta por mensaje."),

    ("salamat", "https://salamat.vantia.digital", "/casos/salamat.html",
     "/assets/images/salamat.jpg", "Salamat",
     "restaurante · carta y reserva",
     "Restaurante con carta, reserva de mesa y pedido para llevar."),

    ("estanteria", "https://vantiadigital.github.io/La-Estanter-a/", "/casos/estanteria.html",
     "/assets/images/estanteria.jpg?v=2", "La Estantería",
     "editorial y publicación digital · proyecto de autor",
     "Biblioteca de cuentos breves, con lectura en la propia web."),
]


def chips_html(sectores_vivos):
    """Un chip cuyo sector no tiene ninguna tarjeta publicada llevaria al
       estado vacio: mejor no sacarlo hasta que su modelo este en linea."""
    out = []
    for valor, es, _ in CHIPS:
        if valor != "all" and valor not in sectores_vivos:
            continue
        activa = ' is-active' if valor == 'all' else ''
        out.append(
            f'            <button class="filter-chip{activa}" type="button" '
            f'data-filter="sector" data-value="{valor}" '
            f'data-i18n="modelos.filter.{valor}">{es}</button>')
    return "\n".join(out)


def modelo_html(clave, sector, slug, nombre, cubre, incluye):
    url = URLS[slug]
    lis = "\n".join(
        f'                <li data-i18n="modelos.{clave}.inc{n+1}">{t}</li>'
        for n, t in enumerate(incluye))
    return f"""
          <!-- {nombre} -->
          <article class="case model model--{clave} case--live" data-caso-id="{slug}" data-caso-tipo="modelo" data-sector="{sector}">
            <a class="case__cover-link" href="{url}" target="_blank" rel="noopener"
               aria-label="Ver el modelo de web para {nombre.lower()} (se abre en una pestaña nueva)"></a>
            <div class="model__preview">
              <img class="model__preview-img" src="/assets/images/modelos/{slug}.webp"
                   alt="Portada del modelo de web para {nombre.lower()}"
                   width="1200" height="800" loading="lazy" decoding="async" />
            </div>
            <div class="case__body">
              <h3 class="case__name" data-i18n="modelos.{clave}.name">{nombre}</h3>
              <span class="case__sector" data-i18n="modelos.{clave}.sector">{cubre}</span>
              <ul class="model__includes">
{lis}
              </ul>
            </div>
            <div class="case__actions">
              <a class="case__action case__action--live" href="{url}" target="_blank" rel="noopener" data-i18n="modelos.cta.see">
                Ver el modelo
              </a>
              <a class="case__action case__action--secondary" href="/contacto" data-i18n="modelos.cta.want">
                Lo quiero para mi negocio
              </a>
            </div>
          </article>
"""


def cliente_html(clave, web, caso, portada, nombre, cubre, resumen):
    """Tarjeta de web de cliente: la portada lleva a la web en vivo y debajo
       va el enlace a su caso de exito."""
    return f"""
          <!-- {nombre} -->
          <article class="case client" data-caso-id="{clave}" data-caso-tipo="caso">
            <a class="case__cover-link" href="{web}" target="_blank" rel="noopener"
               aria-label="Ver la web de {nombre} (se abre en una pestaña nueva)"></a>
            <div class="model__preview">
              <img class="model__preview-img" src="{portada}"
                   alt="Portada de la web de {nombre}"
                   width="1200" height="800" loading="lazy" decoding="async" />
            </div>
            <div class="case__body">
              <h3 class="case__name">{nombre}</h3>
              <span class="case__sector">{cubre}</span>
              <p class="case__real-text">{resumen}</p>
            </div>
            <div class="case__actions">
              <a class="case__action case__action--live" href="{web}" target="_blank" rel="noopener">
                Ver la web
              </a>
              <a class="case__action case__action--secondary" href="{caso}">
                Ver el caso
              </a>
            </div>
          </article>
"""


def main():
    h = io.open(PAGINA, encoding="utf-8").read()

    vivos = [m for m in MODELOS if m[2] in URLS]
    pendientes = [m[2] for m in MODELOS if m[2] not in URLS]
    sectores_vivos = {m[1] for m in vivos}

    # 1 · chips
    ini = h.index('<button class="filter-chip is-active"')
    fin = h.index("</div>", h.rindex('data-i18n="modelos.filter.', ini))
    h = h[:ini].rstrip("\n ") + "\n" + chips_html(sectores_vivos) + "\n          " + h[fin:]

    # 2 · rejilla de modelos, entera
    g0 = h.index('<div class="case-grid"')
    g0 = h.index(">", g0) + 1
    g1 = h.index('<!-- Empty state', g0)
    g1 = h.rindex("</div>", g0, g1)

    portadas = os.path.join(ROOT, "assets", "images", "modelos")
    sin_portada = [m[2] for m in vivos
                   if not os.path.exists(os.path.join(portadas, m[2] + ".webp"))]
    if sin_portada:
        raise SystemExit("faltan portadas: " + ", ".join(sin_portada))

    rejilla = "".join(modelo_html(*m) for m in vivos)
    h = h[:g0] + "\n" + rejilla + "\n        " + h[g1:]

    # 3 · seccion propia de webs de clientes, al final
    marca_ini = "<!-- CLIENTES:start -->"
    marca_fin = "<!-- CLIENTES:end -->"
    seccion = f"""{marca_ini}
    <section class="sector section--white" id="clientes">
      <div class="container">
        <div class="section__head">
          <span class="section__eyebrow" data-reveal data-i18n="modelos.clientes.eyebrow">Trabajo entregado</span>
          <h2 class="section__title" data-reveal data-i18n="modelos.clientes.title">Webs de clientes</h2>
          <p class="section__subtitle" data-reveal data-i18n="modelos.clientes.sub">
            Estas sí están en marcha, con su negocio detrás. Entra a verlas o lee
            qué se decidió en cada una.
          </p>
        </div>

        <div class="case-grid" data-reveal-children>
{"".join(cliente_html(*c) for c in CLIENTES)}        </div>
      </div>
    </section>
    {marca_fin}"""

    if marca_ini in h:
        h = h[:h.index(marca_ini)] + seccion + h[h.index(marca_fin) + len(marca_fin):]
    else:
        ancla = h.index('<section class="cta-banner">')
        h = h[:ancla] + seccion + "\n\n    " + h[ancla:]

    io.open(PAGINA, "w", encoding="utf-8", newline="\n").write(h)
    print(f"tu-web-a-medida.html: {len(vivos)} modelos publicados, "
          f"{len(pendientes)} pendientes + {len(CLIENTES)} webs de clientes")

    # 3 · claves EN
    dic = io.open(I18N, encoding="utf-8").read()
    nuevas = []
    for valor, es, en in CHIPS:
        nuevas.append((f"modelos.filter.{valor}", en))
    nuevas += [
        ("modelos.clientes.eyebrow", "Delivered work"),
        ("modelos.clientes.title", "Client websites"),
        ("modelos.clientes.sub", "These ones are live, with a real business behind them. "
                                 "Go and see them, or read what was decided in each."),
    ]
    faltan = [k for k, _ in nuevas if f'"{k}"' not in dic]
    print(f"claves EN por anadir: {len(faltan)} -> {', '.join(faltan) if faltan else 'ninguna'}")
    return faltan


if __name__ == "__main__":
    main()
