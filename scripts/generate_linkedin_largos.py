# -*- coding: utf-8 -*-
"""
Empaqueta los 9 posts long-form de LinkedIn LISTOS PARA SUBIR.
Por cada post crea  assets/downloads/linkedin/posts-largos/NN-slug/ con:
  - texto.txt   -> caption lista para copiar/pegar en LinkedIn (hook + cuerpo + hashtags)
  - imagen.png  -> foto de respaldo de marca (1080x1350), quote-card sobria, sin emojis
Y un README.md con el orden de publicacion y las notas de foto real.

Sistema visual: paleta Vantia + Fraunces/Inter. Tuteo Espana, cero emojis.
Correr: python scripts/generate_linkedin_largos.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "C:/Users/facun/Documentos/Vantia Digital/Vantia Digital Web"
FRAUNCES = f"{ROOT}/assets/fonts/Fraunces-Regular.ttf"
INTER = f"{ROOT}/assets/fonts/Inter-Variable.ttf"
OUT = f"{ROOT}/assets/downloads/linkedin/posts-largos"

DEEP = (26, 24, 19, 255)
OLIVE = (60, 58, 47, 255)
CREAM = (236, 232, 216, 255)
COPPER = (193, 131, 75, 255)
MUTED = (169, 155, 128, 255)
BG = {"dark": DEEP, "crema": CREAM}

W, H, PAD = 1080, 1350, 100
V_PATH = [(304.641, 155), (0, 155), (409.001, 877), (476.172, 877), (716, 476.054),
          (519.958, 599.613), (446.816, 725.157), (183.603, 255.236), (245.798, 255.236),
          (446.816, 605.568), (710.527, 155), (590.115, 155), (444.826, 407.08)]
A_PATH = [(796.957, 414.027), (525, 877), (651.053, 877), (796.957, 628.89),
          (932.935, 877), (1257, 877), (832.688, 155), (765.195, 155),
          (534.429, 548.006), (719.042, 444.296), (796.957, 313.294),
          (1068.91, 780.733), (1003.41, 780.733)]
VBOX_W, VBOX_H = 1269, 1012
_F = {}


def font(fam, size):
    k = (fam, size)
    if k not in _F:
        _F[k] = ImageFont.truetype(FRAUNCES if fam == "fraunces" else INTER, size)
    return _F[k]


def measure(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1], b


def draw_logo(d, x, y, h, v, a):
    s = h / VBOX_H
    d.polygon([(x + px * s, y + py * s) for px, py in V_PATH], fill=v)
    d.polygon([(x + px * s, y + py * s) for px, py in A_PATH], fill=a)


def footer(d, dark):
    logo_h = 46
    logo_w = VBOX_W * (logo_h / VBOX_H)
    text = "Vantia Digital"
    f = font("fraunces", 30)
    tw, th, b = measure(d, text, f)
    sx = (W - (logo_w + 18 + tw)) / 2
    y = H - 95
    col = CREAM if dark else DEEP
    draw_logo(d, sx, y - logo_h / 2, logo_h, col, COPPER)
    d.text((sx + logo_w + 18, y - th / 2 - b[1]), text, font=f, fill=col)


def render_card(post, path):
    dark = post["bg"] == "dark"
    fg = CREAM if dark else DEEP
    img = Image.new("RGBA", (W, H), BG[post["bg"]])
    d = ImageDraw.Draw(img)

    # eyebrow centrado + hairline cobre
    ey = font("inter", 24)
    label = " ".join(list(post["eyebrow"]))  # tracking
    lw, lh, lb = measure(d, label, ey)
    d.text(((W - lw) / 2, 210 - lb[1]), label, font=ey, fill=COPPER)
    d.rectangle([(W / 2 - 35, 210 + lh + 18), (W / 2 + 35, 210 + lh + 22)], fill=COPPER)

    # frase-tarjeta (auto-fit)
    lines, accent = post["lines"], post.get("accent")
    size = 92
    while size > 48:
        f = font("fraunces", size)
        if all(measure(d, ln, f)[0] <= W - 2 * PAD for ln in lines):
            break
        size -= 4
    f = font("fraunces", size)
    gap = int(size * 0.26)
    measured = [(ln, *measure(d, ln, f)) for ln in lines]
    total = sum(h for _, _, h, _ in measured) + gap * (len(lines) - 1)
    cy = (H - total) / 2 - 20
    for ln, lwd, lhd, lbd in measured:
        x0 = (W - lwd) / 2
        if accent and accent in ln:
            pre, post_ = ln.split(accent, 1)
            wpre = measure(d, pre, f)[0]
            wacc = measure(d, accent, f)[0]
            d.text((x0, cy - lbd[1]), pre, font=f, fill=fg)
            d.text((x0 + wpre, cy - lbd[1]), accent, font=f, fill=COPPER)
            d.text((x0 + wpre + wacc, cy - lbd[1]), post_, font=f, fill=fg)
        else:
            d.text((x0, cy - lbd[1]), ln, font=f, fill=fg)
        cy += lhd + gap

    footer(d, dark)
    img.save(path, "PNG", optimize=True)


# ─────────────────────────── DATA: 9 POSTS ───────────────────────────
POSTS = [
    dict(n=1, slug="quienes-somos", bg="dark", eyebrow="QUIENES SOMOS",
         lines=["No somos otra", "agencia creativa.", "Somos técnica."], accent="técnica",
         photo="Foto real recomendada: Facu trabajando o una pantalla con Looker Studio / GA4.",
         caption="""No somos otra agencia creativa. Somos técnica.

Lo decimos en la primera frase porque es lo que más nos diferencia.

Hay muchas agencias que hacen cosas preciosas. Y está bien que existan.

Pero cuando un dueño de PYME nos pregunta "¿esto que pago, qué me devuelve?", la respuesta no puede ser un moodboard.

Tiene que ser un número.

Por eso lo nuestro empieza antes del diseño y termina después del lanzamiento.

Empieza en cómo se mide cada visita, cada contacto, cada venta.

Y termina en un informe donde tú, el dueño, ves qué euro trabajó y cuál se quedó por el camino.

No vendemos campañas bonitas para enseñar en una reunión.

Montamos sistemas que puedes auditar cuando quieras, sin tener que fiarte de nuestra palabra.

Somos una agencia técnica en Barcelona, trabajando con clientes dentro y fuera de España.

Y esta página va a ir de eso: cómo se hace el marketing cuando lo pones a rendir cuentas.

Casos reales, lo técnico explicado claro y alguna opinión que incomoda.

Empezamos por presentarnos. El resto, en los próximos.

¿Qué es para ti una agencia "técnica"? Te leemos en comentarios.

#MarketingDigital #PYMES #AgenciaDeMarketing #ROI #Barcelona"""),

    dict(n=2, slug="le-hablamos-al-dueno", bg="crema", eyebrow="A QUIEN LE HABLAMOS",
         lines=["Le hablamos al dueño.", "No a su departamento", "de marketing."], accent="dueño",
         photo="Foto real recomendada: un dueño de PYME en su negocio, o Facu en reunión/videollamada.",
         caption="""Le hablamos al dueño, no a su departamento de marketing.

Porque muchas PYMES no tienen departamento de marketing.

Tienen un dueño que ya hace de comercial, de jefe de obra, de atención al cliente y, en los ratos libres, de responsable de que la web no se caiga.

A esa persona no le sirve que le hablen en difícil.

No necesitas saber qué es un CTR, una tasa de rebote o una atribución multicanal para entender qué hace tu dinero.

Eso es trabajo nuestro, no tuyo.

Lo nuestro es coger lo técnico y traducirlo a algo que sí decide un negocio:

— cuánto te cuesta conseguir un cliente
— qué canal te lo trae
— qué pasa si inviertes más aquí y menos allá

Eso lo entiende cualquier dueño. Y con eso se toman decisiones.

Trabajamos así a propósito. Pensado para PYMES, no para corporaciones con un equipo de diez personas y su propio jefe de analítica.

Si alguna vez te han enseñado un informe y has asentido sin entender nada, esto va por ti.

¿Te ha pasado? ¿Has firmado un informe que no entendías del todo? Cuéntanoslo.

#PYMES #MarketingDigital #Emprender #MarketingParaPymes #Negocios"""),

    dict(n=3, slug="tu-web-no-es-folleto", bg="dark", eyebrow="EL PROBLEMA",
         lines=["Tu web no es", "un folleto.", "Es tu mejor comercial."], accent="comercial",
         photo="Foto real recomendada: un móvil con una web de cliente, o captura de PageSpeed / Core Web Vitals.",
         caption="""Tu web no es un folleto. Es tu mejor comercial.

Un folleto se enseña y se guarda.

Un comercial trabaja. Atiende, explica, convence y cierra. Incluso de madrugada, cuando tú ya has cerrado.

La mayoría de PYMES tratan su web como lo primero y la pagan como lo segundo.

Invierten en que se vea bien, la estrenan con ilusión y la dejan ahí, quieta, esperando que alguien aparezca.

Imagina que entra alguien a tu web a las 23 h, con ganas de comprar.

¿Encuentra rápido lo que busca? ¿Sabe cómo contactarte? ¿Cargó la página antes de que se aburriera y se fuera?

Si no lo sabes, no es culpa tuya. Es que nadie puso un número detrás para contártelo.

Una web que trabaja se mide como se mediría a un comercial:

cuánta gente atendió, a cuántos convenció y cuánto trajo a fin de mes.

Cuando empiezas a mirarla así, deja de ser un gasto en la cuenta de resultados.

Pasa a ser tu vendedor que no descansa nunca.

¿Tu web hoy es un folleto o un comercial? Sé sincero. Te leemos.

#MarketingDigital #PYMES #OptimizacionWeb #CRO #Negocios"""),

    dict(n=4, slug="que-hacemos", bg="crema", eyebrow="QUE HACEMOS",
         lines=["Cuatro cosas.", "Bien hechas."], accent="Bien hechas",
         photo="Imagen lista: la pieza de IG feed-04-que-hacemos.png. Alternativa real: escritorio con varias pantallas (web, GA4, gestor de anuncios).",
         caption="""Hacemos cuatro cosas. Y las hacemos bien.

No tenemos un catálogo de veinte servicios para que elijas a ciegas.

Tenemos cuatro. Encajan entre sí y se refuerzan.

1. Optimizar tu web para que venda.

No para que gane premios. Para que la gente que entra haga lo que querías que hiciera: comprar, reservar, escribirte.

2. Que te encuentren.

SEO técnico para Google, y GEO para que las IA como ChatGPT o Perplexity también te recomienden cuando alguien pregunta por tu sector.

3. Campañas de anuncios que rinden.

Las que se justifican con lo que devuelven, no con lo que gustan en una presentación.

4. Medición clara de cada resultado.

Esta es la que sostiene a las otras tres. Sin ella, las demás son intuición con presupuesto.

No hacemos de todo. Hacemos esto, y respondemos por cada euro que pasa por aquí.

Si necesitas algo que no está en esta lista, te lo decimos. Y si conocemos a quien lo hace bien, te lo presentamos.

De las cuatro, ¿cuál crees que más se descuida en las PYMES? Nos interesa tu opinión.

#MarketingDigital #SEO #CRO #PYMES #PublicidadOnline"""),

    dict(n=5, slug="primero-medir", bg="dark", eyebrow="NUESTRO PRINCIPIO",
         lines=["Primero medir.", "Después invertir."], accent="medir",
         photo="Foto real recomendada: pantalla con GA4 / Looker Studio antes-después, o libreta con el plan de medición junto al portátil.",
         caption="""Primero medir. Después invertir.

En ese orden. Siempre.

Suena obvio dicho así. En la práctica, casi todo el mundo lo hace al revés.

Primero se paga la web, primero se lanzan los anuncios, primero se gasta.

Y la medición, si llega, llega tarde y mal. Cuando el dinero ya voló.

Para nosotros es al contrario, y no es una manía. Es el principio que ordena todo lo demás.

Si mides antes de invertir, sabes desde qué punto partes.

Sabes qué euro funcionó y cuál no.

Y la próxima decisión la tomas con datos, no con la sensación de que "parece que va bien".

Invertir sin medir es apostar.

A veces sale. Pero no puedes repetirlo a propósito, porque no sabes qué fue lo que salió bien.

Medir primero no es más lento. Es lo que evita gastar meses sin enterarte de que estabas perdiendo.

Por eso, cuando entra un cliente, lo primero no es lanzar nada.

Es montar la forma de saber si lo que vamos a lanzar funciona.

¿Lo haces en este orden, o como casi todos, al revés? Sin juzgar. Te leemos.

#MarketingDigital #ROI #Analitica #PYMES #MarketingDeResultados"""),

    dict(n=6, slug="como-trabajamos", bg="crema", eyebrow="COMO TRABAJAMOS",
         lines=["Medición", "antes que tráfico."], accent="Medición",
         photo="Foto real recomendada: pantalla con Google Tag Manager o GA4 en montaje.",
         caption="""Montamos la medición antes de gastar un euro en tráfico.

Es lo primero que hacemos al entrar. Antes de tocar un anuncio.

Y al principio sorprende. Más de un cliente nos ha preguntado: "¿pero no empezamos ya a traer gente?".

Todavía no. Primero instrumentamos.

Eso quiere decir dejar listo el sistema que registra qué pasa en tu web: quién entra, qué hace, dónde se va y qué acaba en una venta.

GA4, Google Tag Manager, Consent Mode, Looker Studio, Clarity. Suenan a jerga, y por eso no tienes que saber qué es cada uno.

Lo que tienes que saber es lo que hacen juntos: convierten tu web en algo que se puede leer en números.

Cuando eso está montado, entonces sí, invertimos. Y cada euro que entra deja rastro.

Hay una parte que no todos dicen, y nosotros sí:

si algo no se puede medir bien, te lo decimos.

Preferimos ser claros a venderte una cifra bonita que luego no podemos sostener.

Esa transparencia, al principio, parece que nos resta.

A la larga es lo único que hace que confíes en el resto de números que te enseñamos.

¿Te han montado alguna vez la medición antes de empezar a gastar? Cuéntanoslo.

#MarketingDigital #Analitica #DataDriven #PYMES #Metodologia"""),

    dict(n=7, slug="en-que-creemos", bg="dark", eyebrow="EN QUE CREEMOS",
         lines=["Lo que", "no negociamos."], accent="no negociamos",
         photo="Imagen lista: la pieza de IG feed-07-nuestros-valores.png. Alternativa real: Facu de frente, plano sobrio.",
         caption="""Hay cosas que no negociamos. Estas son cuatro.

Cada agencia tiene su forma. Esta es la nuestra, y no la movemos ni cuando incomoda.

1. Decirte lo que no está funcionando.

Aunque sea algo que montamos nosotros. Si un canal no rinde, te lo decimos antes de que lo veas en la factura.

2. Hablar claro, sin jerga.

Si para explicarte algo necesitamos tres siglas y un anglicismo, es que no lo hemos entendido bien nosotros primero.

3. Datos antes que promesas.

No te decimos "esto va a funcionar". Te decimos "esto es lo que está pasando, mira el número".

4. Tu negocio por delante de todo.

Por delante de la campaña que nos gustaría enseñar. Por delante de lo que sería cómodo facturar.

Ninguna de estas cuatro es la opción más fácil de vender.

Decir lo que no funciona es más incómodo que enseñar solo lo bueno.

Hablar claro es más lento que esconderse detrás de palabras grandes.

Pero son las que hacen que, cuando te enseñamos un buen resultado, te lo puedas creer.

¿Qué es lo que tú no negociarías con una agencia? Nos interesa de verdad.

#MarketingDigital #PYMES #Transparencia #ROI #Negocios"""),

    dict(n=8, slug="paso-a-paso", bg="crema", eyebrow="PASO A PASO",
         lines=["Cuatro pasos.", "En orden."], accent="En orden",
         photo="Imagen lista: la pieza de IG feed-08-nuestra-metodologia.png. Alternativa real: pizarra o cuaderno con los 4 pasos a mano.",
         caption="""Cuatro pasos, en orden. Saltarse uno cuesta dinero.

Cuando empezamos con un cliente, no improvisamos. Seguimos siempre la misma secuencia.

Paso 1. Entender tu negocio.

Qué vendes, quién te compra y qué es un cliente bueno para ti. Sin esto, optimizar es optimizar a ciegas.

Paso 2. Medir el punto de partida.

Una foto de cómo estás hoy. Porque sin un "esto es lo que había", no hay forma de demostrar después que algo mejoró.

Paso 3. Construir y optimizar.

Aquí se trabaja la web, el SEO, las campañas. Pero recién aquí, con los dos pasos anteriores hechos.

Paso 4. Revisar con datos en la mano.

Nos sentamos contigo a mirar qué dicen los números y decidimos el siguiente movimiento sobre eso, no sobre corazonadas.

El orden importa más de lo que parece.

Casi todos quieren empezar por el paso 3, porque es el que se ve.

Pero saltarse el 1 y el 2 es lo que hace que, seis meses después, nadie sepa si la inversión sirvió de algo.

Lento al principio. Mucho más barato a la larga.

¿Por qué paso crees que suele empezar la mayoría? Te leemos.

#MarketingDigital #Metodologia #PYMES #Analitica #DataDriven"""),

    dict(n=9, slug="para-que", bg="dark", eyebrow="PARA QUE",
         lines=["Saber qué funciona.", "Decidir con claridad."], accent="claridad",
         photo="Foto real recomendada: un dueño de PYME tranquilo en su negocio, o Facu cerrando una reunión relajado.",
         caption="""Todo esto es para que, por fin, sepas qué funciona. Y decidas con claridad.

Hemos hablado de medición, de método, de no negociar ciertas cosas.

Pero nada de eso es el objetivo. Son el camino.

El objetivo es lo que te queda al final: tranquilidad.

La de abrir el informe a fin de mes y entenderlo entero.

La de saber qué euro trabajó y cuál no, sin que nadie te lo tenga que adornar.

La de decidir el próximo movimiento desde la calma, porque tienes los datos delante y no una corazonada.

Hacer marketing a ciegas cansa.

Pagas, esperas, y vives con la duda de si está sirviendo de algo. Esa duda pesa.

Lo que hacemos quita esa duda.

No te prometemos que todo vaya a funcionar siempre. Eso no lo puede prometer nadie honesto.

Te prometemos que vas a saber qué funciona y qué no. Y con eso, las decisiones dejan de dar miedo.

Eso es, al final, lo que vinimos a darte: control sobre tu dinero y claridad para decidir.

Si quieres ver cómo se vería esto en tu caso, escríbenos. Lo miramos juntos, sin compromiso.

#MarketingDigital #PYMES #ROI #MarketingDeResultados #Barcelona"""),
]


def run():
    os.makedirs(OUT, exist_ok=True)
    readme = ["# LinkedIn · Posts long-form LISTOS PARA SUBIR — Vantia Digital",
              "",
              "Carta de presentación de marca (adaptada de Instagram) en formato long-form.",
              "Cada carpeta NN-slug tiene `texto.txt` (copiar/pegar) + `imagen.png` (adjuntar).",
              "Orden de publicación = numeración. Cadencia sugerida: 2/semana (martes y jueves, media mañana).",
              "Tuteo España, cero emojis. La subida final la hace Facu.",
              "",
              "La `imagen.png` es una foto de respaldo de marca lista para usar. En 6 posts (1,2,3,5,6,9)",
              "una FOTO REAL tuya rinde más (cara, pantalla con datos): cuando la tengas, reemplaza imagen.png.",
              ""]
    for p in POSTS:
        folder = f"{OUT}/{p['n']:02d}-{p['slug']}"
        os.makedirs(folder, exist_ok=True)
        render_card(p, f"{folder}/imagen.png")
        with open(f"{folder}/texto.txt", "w", encoding="utf-8") as f:
            f.write(p["caption"].strip() + "\n")
        readme.append(f"- **{p['n']:02d} · {p['eyebrow'].title()}** — `{p['n']:02d}-{p['slug']}/` · {p['photo']}")
    with open(f"{OUT}/README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme) + "\n")
    print(f"Paquete generado en {OUT}")
    for p in POSTS:
        print(f"  {p['n']:02d}-{p['slug']}/  (texto.txt + imagen.png)")


run()
