/* ============================================
   VANTIA DIGITAL — I18N (ES / EN)
   ----------------------------------------------------------------
   Estrategia: el español es el HTML base (indexable por buscadores).
   El inglés se aplica en cliente desde el diccionario de abajo, sin
   recargar la página. La preferencia se guarda en localStorage.

   Marcado en el HTML:
     <h2 data-i18n="home.method.title">…español…</h2>
       → reemplaza innerHTML por DICT.en["home.method.title"] en EN.
     <input data-i18n-placeholder="cont.form.name_ph">
     <meta data-i18n-content="home.meta.desc">
     <button data-i18n-aria-label="nav.toggle">
     <a data-i18n-title="…">

   Regla de oro: nunca pongas data-i18n en un elemento que CONTENGA
   otro elemento con data-i18n (el swap de innerHTML borraría el hijo).
   Usá el elemento-hoja más pequeño que envuelva solo el texto.
   ============================================ */
(() => {
  'use strict';

  const STORAGE_KEY = 'vantia-lang';
  const DEFAULT_LANG = 'es';
  const SUPPORTED = ['es', 'en'];

  // ====================================================================
  // DICCIONARIO — solo EN (ES = HTML original)
  // ====================================================================
  const DICT = { en: {} };

  // ---- GLOBAL / COMPARTIDO (header, footer, modales, cookies, etc.) ----
  Object.assign(DICT.en, {
    // Accesibilidad
    'a11y.skip': 'Skip to content',

    // Header / nav
    'nav.aria': 'Main',
    'nav.casos': 'Case studies',
    'nav.servicios': 'Services',
    'nav.nosotros': 'About',
    'nav.contacto': 'Contact',
    'nav.toggle': 'Open menu',
    'nav.logo_aria': 'Vantia Digital — Home',
    'lang.aria': 'Language',

    // Footer
    'foot.tagline': 'Web ecosystems and Digital Marketing with mathematical precision.',
    'foot.explore': 'Explore',
    'foot.back_top': 'Back to top',
    'foot.casos': 'Case studies',
    'foot.servicios': 'Services',
    'foot.nosotros': 'About',
    'foot.contacto': 'Contact',
    'foot.free_session': 'Free session',
    'foot.services_h': 'Services',
    'foot.svc_web': 'Web Optimisation',
    'foot.svc_seo': 'Technical SEO / GEO',
    'foot.svc_ads': 'Ad Campaigns',
    'foot.contact_h': 'Contact',
    'foot.location': 'Barcelona, Spain',
    'foot.social_aria': 'Social media',
    'foot.copyright': '© 2026 Vantia Digital. All rights reserved.',
    'foot.legal_aria': 'Legal links',
    'foot.privacy': 'Privacy',
    'foot.cookies': 'Cookies',
    'foot.legal_notice': 'Legal notice',
    'foot.cookie_prefs': 'Cookie preferences',

    // WhatsApp FAB
    'wa.aria': 'Contact via WhatsApp',

    // ---- Cookie banner ----
    'cc.banner_aria': 'Cookie notice',
    'cc.title': 'We use cookies',
    'cc.text': 'We use necessary cookies for the site to work and, with your consent, analytics cookies to measure traffic. See our <a href="/cookies">Cookie Policy</a>.',
    'cc.configure': 'Configure',
    'cc.reject': 'Reject',
    'cc.accept': 'Accept',
    'cc.modal_title': 'Cookie preferences',
    'cc.modal_intro': 'Manage your consent by category. You can change these preferences at any time from the footer.',
    'cc.cat_necessary': 'Necessary',
    'cc.necessary_aria': 'Necessary cookies (always on)',
    'cc.necessary_desc': 'Essential for the site to work (navigation, security). <span class="vc-cat__locked">Always on.</span>',
    'cc.cat_analytics': 'Analytics',
    'cc.analytics_aria': 'Analytics cookies',
    'cc.analytics_desc': 'Google Analytics 4 with anonymized IP. They help us understand which content is most useful. No remarketing or advertising profiles.',
    'cc.reject_all': 'Reject all',
    'cc.save': 'Save preferences',

    // ---- Service modals ----
    'mod.web.num': '01 · Pillar',
    'mod.web.title': 'Web Optimisation',
    'mod.web.subtitle': 'Platforms that turn visitors into customers.',
    'mod.web.what_h': 'What we do',
    'mod.web.what_p': 'We design and build high-performance web ecosystems. Every line of code is built to maximise conversion and speed. We apply CRO (conversion rate optimisation) so every visit performs better.',
    'mod.web.how_h': 'How we do it',
    'mod.web.how_1': 'Full technical audit of your current website',
    'mod.web.how_2': 'Information architecture optimised for conversion',
    'mod.web.how_3': 'Premium UX/UI design adapted to your brand',
    'mod.web.how_4': 'Frontend development with clean, optimised code',
    'mod.web.how_5': 'Integrations with CMS, CRM and analytics tools',
    'mod.web.how_6': 'Performance testing until reaching PageSpeed 95+',
    'mod.web.how_cro': 'CRO: heatmaps, A/B tests and friction reduction at the conversion points',
    'mod.web.res_h': 'Expected results',
    'mod.web.res_1': 'Load time under 2 seconds',
    'mod.web.res_2': 'PageSpeed Insights 95+ on mobile and desktop',
    'mod.web.res_3': 'Measurable improvement in conversion rate',
    'mod.web.res_4': 'A website ready to scale',
    'mod.web.cta': 'Web quote',

    'mod.seo.num': '02 · Pillar',
    'mod.seo.title': 'Technical SEO <span class="modal__title-slash">/</span> GEO',
    'mod.seo.subtitle': 'Technical SEO combined with GEO (Generative Engine Optimization), adapted to the new AI-powered search.',
    'mod.seo.what_h': 'What we do',
    'mod.seo.what_p': 'We optimise your digital ecosystem for traditional search engines and for the new AI-based answer engines. We combine classic technical SEO with GEO to capture qualified demand across both channels.',
    'mod.seo.how_h': 'How we do it',
    'mod.seo.how_1': 'Full technical SEO audit',
    'mod.seo.how_2': 'Core Web Vitals and internal architecture optimisation',
    'mod.seo.how_3': 'Advanced schema markup and structured data',
    'mod.seo.how_4': 'Content strategy optimised for SEO and GEO',
    'mod.seo.how_5': 'Citation engineering to position the brand as a trusted source',
    'mod.seo.how_6': 'Continuous monitoring and monthly adjustments',
    'mod.seo.res_h': 'Expected results',
    'mod.seo.res_1': 'Organic ranking in top positions',
    'mod.seo.res_2': 'Visibility in AI engines',
    'mod.seo.res_3': 'Increase in qualified traffic',
    'mod.seo.res_4': 'Sustainable month-over-month growth',
    'mod.seo.cta': 'SEO / GEO quote',

    'mod.ads.num': '03 · Pillar',
    'mod.ads.title': 'Ad Campaigns',
    'mod.ads.subtitle': 'Campaigns on <em>Google Ads</em> and <em>Meta Ads</em>. Predictable traffic, based on pure data.',
    'mod.ads.what_h': 'What we do',
    'mod.ads.what_p': 'We design and manage paid traffic campaigns on Google Ads (Search, Performance Max, YouTube) and Meta Ads (Facebook and Instagram). Every euro invested has a measured, attributed return.',
    'mod.ads.how_h': 'How we do it',
    'mod.ads.how_1': 'Deep analysis of your market and competition',
    'mod.ads.how_2': 'Definition of buyer personas and customer journey',
    'mod.ads.how_3': 'Advanced tracking setup (GA4, Meta Pixel, Conversions API)',
    'mod.ads.how_4': 'Campaigns on Google Ads and Meta Ads with surgical targeting',
    'mod.ads.how_5': 'Continuous optimisation of funnels and creatives',
    'mod.ads.how_6': 'Systematic A/B testing at every funnel stage',
    'mod.ads.res_h': 'Expected results',
    'mod.ads.res_1': 'Maximised, predictable ROAS',
    'mod.ads.res_2': 'CAC reduced month over month',
    'mod.ads.res_3': 'Controlled budget scalability',
    'mod.ads.res_4': 'Clear attribution of every conversion',
    'mod.ads.cta': 'Ad Campaigns quote',

    // Budget mini-modal
    'mod.budget.eyebrow': 'Request a quote',
    'mod.budget.title': 'Service',
    'mod.budget.sub': 'Fill in the form and an email will open with the details. We reply within 24 business hours.',
    'mod.budget.name_ph': 'Name',
    'mod.budget.email_ph': 'Email',
    'mod.budget.msg_ph': 'Tell us briefly about your project (optional)',
    'mod.budget.name_aria': 'Name',
    'mod.budget.email_aria': 'Email',
    'mod.budget.msg_aria': 'Message about your project',
    'mod.budget.send': 'Send request',
  });

  // ---- HOME (index.html) ----
  Object.assign(DICT.en, {
    'home.meta.title': 'Vantia · Digital Marketing',
    'home.meta.desc': 'Technical digital marketing agency for SMEs and mid-sized companies. Web Optimisation, Technical SEO + GEO and Ad Campaigns with measurable ROI.',

    'home.hero.l1': 'Web ecosystems',
    'home.hero.l2': 'and Digital Marketing',
    'home.hero.l3': 'with <em>mathematical precision</em>.',
    'home.hero.sub': "We're experts at scaling your company's revenue. Book your first free session to assess your case and structure your next project.",
    'home.hero.cta1': 'Free session',
    'home.hero.cta2': 'View services',

    // Marquee quotes
    'home.q1': '&ldquo;The best time to plant a tree was 20 years ago. The second best time is now&rdquo;',
    'home.q1a': 'Chinese proverb',
    'home.q2': '&ldquo;All models are wrong. Some are useful&rdquo;',
    'home.q2a': 'George Box',
    'home.q3': '&ldquo;Patience is bitter, but its fruit is sweet&rdquo;',
    'home.q3a': 'Aristotle',
    'home.q4': '&ldquo;What is essential is invisible to the eye&rdquo;',
    'home.q4a': 'Antoine de Saint-Exupéry',
    'home.q5': '&ldquo;Simplicity is the ultimate sophistication&rdquo;',
    'home.q5a': 'Leonardo da Vinci',

    // Methodology
    'home.method.eyebrow': 'Our methodology',
    'home.method.line': 'Three technical pillars:',
    'home.method.em': 'One single conversion ecosystem.',

    'home.p1.num': '01 / Pillar',
    'home.p1.title': 'Web Optimisation',
    'home.p1.body': 'High-speed platforms and CRO (conversion optimisation). Architecture built to convert, with clean code and a 99/100 PageSpeed.',
    'home.p1.aria': 'Open Web Optimisation details',
    'home.p2.num': '02 / Pillar',
    'home.p2.title': 'Technical SEO <span style="color: var(--color-olive); font-weight: 400;">/</span> GEO',
    'home.p2.body': 'Technical SEO combined with GEO (Generative Engine Optimization), adapted to the new AI-powered search.',
    'home.p2.aria': 'Open Technical SEO and GEO details',
    'home.p3.num': '03 / Pillar',
    'home.p3.title': 'Ad Campaigns',
    'home.p3.body': 'Campaigns on <span class="brand-em">Google Ads</span> and <span class="brand-em">Meta Ads</span>. Predictable traffic based on pure data, maximising ROAS and lowering cost per acquisition.',
    'home.p3.aria': 'Open Ad Campaigns details',
    'home.method.cta': 'See service details',

    // Stats
    'home.stats.sr': 'Key metrics',
    'home.stat1.label': 'Average PageSpeed',
    'home.stat1.desc': 'Core Web Vitals in the green on every project we deliver.',
    'home.stat2.label': 'ROAS growth',
    'home.stat2.desc': 'Average over 9 months on the initial ad spend.',
    'home.stat3.label': 'Custom code',
    'home.stat3.desc': 'Zero templates. Every line belongs to the client.',
  });

  // ==== I18N:PAGE-CHUNKS:START (no borrar — aquí se insertan las páginas) ====

  // ---- SERVICIOS ----
  Object.assign(DICT.en, {
    "serv.title": "Services · Vantia · Digital Marketing",
    "serv.meta.desc": "Vantia services · Digital Marketing — Web Optimisation, Technical SEO + GEO and Ad Campaigns, plus Social Media Management and Email Marketing. The complete system to scale your business.",
    "serv.hero.eyebrow": "Services in detail",
    "serv.hero.title": "Three <em>technical</em> services.<br/>\n          One single ecosystem.",
    "serv.hero.subtitle": "Each service is designed to integrate with the others. We don't sell loose parts: we build complete systems where the web, SEO and campaigns work in unison. Scroll down and read in detail what we do in each one, why it matters for your SME and what we deliver.",
    "serv.s1.num": "01 — Service",
    "serv.s1.title": "Web Optimisation",
    "serv.s1.lead": "The website is the foundation against which everything else is measured. If it loads slowly, if it doesn't display properly on mobile, if Google flags it as insecure, no other marketing effort will perform. Before investing in ads or SEO, we optimise the website: technical speed and CRO (conversion rate optimisation). Because a fast website that doesn't convert is still wasted money.",
    "serv.s1.h3a": "What does \"web optimisation\" mean in practice?",
    "serv.s1.p1": "It is the set of technical and conversion improvements that make your site load fast, display correctly on any device, be understood by search engines and AI engines, and turn more visits into customers. On one hand, the three metrics Google looks at to decide whether your website is up to scratch are <strong>Core Web Vitals</strong>: how long it takes for the main content to appear (LCP), how quickly it reacts to a click (INP), and whether elements shift while loading (CLS). On the other, <strong>CRO</strong> (conversion rate optimisation) works on what happens once the page has loaded: what stops the user, where they drop off, and which version of a headline or a form converts better.",
    "serv.s1.p2": "The reality: 70% of SMEs have at least one of these metrics in the red. That means Google lowers their ranking, users leave before the page finishes loading, and the ads you pay for cost more because the quality of the destination is low.",
    "serv.s1.h3b": "Why it matters for your SME",
    "serv.s1.p3": "For every extra 100 milliseconds your website takes to load, you lose between 1% and 2% of conversions. A website that takes 4 seconds to load loses roughly half its visitors before showing anything. And since each visit came from a paid click or hard-won SEO, that is real money wasted.",
    "serv.s1.p4": "On top of that: Google rewards fast websites with better organic rankings, and AI engines (ChatGPT, Perplexity, Gemini) only cite sources that load properly. If your website is slow or has technical errors, neither Google nor AI will recommend you.",
    "serv.s1.h3c": "How we do it at Vantia",
    "serv.s1.li1": "<strong>Technical audit with Lighthouse and PageSpeed Insights.</strong> We get the real diagnosis of your current website: Core Web Vitals, accessibility, technical SEO, best practices. If you already have a site, we start from there. If not, we build it from scratch.",
    "serv.s1.li2": "<strong>Performance budget.</strong> We define a technical budget: how much each page can weigh, how many requests it can make, how many KB of JavaScript are acceptable. Without this, websites bloat with every change.",
    "serv.s1.li3": "<strong>Selective refactor or rebuild.</strong> We rewrite only what is necessary: image optimisation (WebP/AVIF), lazy loading, critical inline CSS, non-blocking JavaScript, fonts with display:swap, correct cache headers.",
    "serv.s1.li4": "<strong>Accessibility (WCAG 2.2).</strong> Meeting accessibility standards is not just a legal requirement in Europe (Directive 2025) — it also broadens your market: correct contrast, keyboard navigation, semantic tags, alt text on images.",
    "serv.s1.li5": "<strong>Base technical SEO.</strong> Schema markup, XML sitemap, robots.txt, canonical tags, hreflang if you operate in multiple languages, Open Graph meta tags so your link looks good when someone shares it.",
    "serv.s1.li6": "<strong>Continuous monitoring.</strong> We set up a dashboard that monitors performance, JS errors, uptime and the speed of each page. If something breaks, we know before you do.",
    "serv.s1.li_cro": "<strong>CRO (conversion rate optimisation).</strong> We analyse real behaviour with heatmaps and session recordings (Microsoft Clarity), identify friction and drop-off points, and run A/B tests on headlines, calls to action and forms. We don't assume what converts — we measure it.",
    "serv.s1.h3d": "What we deliver",
    "serv.s1.del1": "Website with PageSpeed Insights 95+ on mobile and desktop.",
    "serv.s1.del2": "Core Web Vitals in the green (LCP &lt; 2.5s, INP &lt; 200ms, CLS &lt; 0.1).",
    "serv.s1.del3": "WCAG 2.2 level AA accessibility validated.",
    "serv.s1.del4": "Analytics stack installed: GA4, GTM, Consent Mode v2, Microsoft Clarity.",
    "serv.s1.del_cro": "CRO roadmap with prioritised hypotheses, documented A/B tests, and heatmap and session-recording analysis.",
    "serv.s1.del5": "Monitoring dashboard in Looker Studio that you can read yourself.",
    "serv.s1.del6": "Technical project documentation (what was done, why, and how to maintain it).",
    "serv.s1.cta": "Request a quote · Web Optimisation",
    "serv.s1.case.eyebrow": "Real case · Web Optimisation",
    "serv.s1.case.title": "GeTT Studio — performance and mobile-first",
    "serv.s2.num": "02 — Service",
    "serv.s2.title": "Technical SEO <span class=\"service-article__title-slash\">/</span> GEO",
    "serv.s2.lead": "SEO is no longer just about \"ranking first on Google\". It is about appearing in the answers from ChatGPT, Perplexity, Gemini and the new AI engines. We combine traditional technical SEO with GEO (Generative Engine Optimization) so your brand is cited in both channels.",
    "serv.s2.h3a": "What is technical SEO and what is GEO?",
    "serv.s2.p1": "<strong>Technical SEO</strong> is the part of SEO that deals with how Google understands your website: site structure, clean code, schema markup, speed, indexing, sitemap. It is the foundation on which content SEO (articles, keywords) is then built.",
    "serv.s2.p2": "<strong>GEO (Generative Engine Optimization)</strong> is the new discipline, which emerged in 2024–2025, that deals with how generative AI engines cite and incorporate your content in their responses. When someone asks ChatGPT \"what is the best technical agency in Barcelona\", the model chooses which sources to cite based on signals very different from Google's.",
    "serv.s2.p3": "The two disciplines overlap at the technical foundation (fast website, correct schema, clear content) but diverge in tactics: classic SEO looks at backlinks and domain authority, GEO looks at the \"citability\" of content (clarity, verifiable data, thematic authority).",
    "serv.s2.h3b": "Why it matters for your SME",
    "serv.s2.p4": "Search behaviour is changing fast: Gartner estimates that by 2026 traditional organic traffic will fall by 25% while AI search grows. If your SEO strategy only targets Google, you will gradually lose relevance without noticing.",
    "serv.s2.p5": "And the good news is that GEO is still in its early years — whoever optimises now captures an advantage that is hard to reverse. SMEs that position themselves as citable sources in ChatGPT today will have an authority that is very hard to compete with in 2027.",
    "serv.s2.h3c": "How we do it at Vantia",
    "serv.s2.li1": "<strong>Full technical SEO audit.</strong> Screaming Frog + Google Search Console + Ahrefs: we detect indexing problems, duplicate content, misconfigured schema, broken canonical URLs, redirect chains.",
    "serv.s2.li2": "<strong>Core Web Vitals optimisation.</strong> As with Web Optimisation — performance is also an SEO signal.",
    "serv.s2.li3": "<strong>Advanced schema markup.</strong> Structured data for Organization, LocalBusiness, Service, FAQPage, Article, BreadcrumbList. This makes Google and AI engines understand exactly what your business does.",
    "serv.s2.li4": "<strong>Dual content strategy.</strong> Every article or page is planned with two objectives: ranking on Google (keywords, intent) and being cited by AI (clarity, data, authority). These are not separate exercises.",
    "serv.s2.li5": "<strong>Citation engineering.</strong> We position your brand as a reliable source: consistent profiles (Google Business, LinkedIn, Wikipedia if applicable), mentions in sector media, participation in datasets that AI models use for training.",
    "serv.s2.li6": "<strong>Monthly monitoring.</strong> Google ranking report + regular checks in ChatGPT/Perplexity/Gemini for your niche's key keywords. If the brand does not appear, we adjust strategy.",
    "serv.s2.h3d": "What we deliver",
    "serv.s2.del1": "Technical audit with issue prioritisation (P0 to P3).",
    "serv.s2.del2": "Schema markup implemented across all relevant pages.",
    "serv.s2.del3": "Content strategy with quarterly editorial calendar.",
    "serv.s2.del4": "Improved organic ranking (Google) and citability (AI).",
    "serv.s2.del5": "Monthly keyword dashboard + visibility in AI engines.",
    "serv.s2.del6": "Actionable recommendations every month, not just passive reports.",
    "serv.s2.cta": "Request a quote · SEO + GEO",
    "serv.s2.case.eyebrow": "Real case · Technical SEO + GEO",
    "serv.s2.case.title": "La Estantería — ranking on Google and in AI",
    "serv.s3.num": "03 — Service",
    "serv.s3.title": "Ad Campaigns",
    "serv.s3.lead": "Paid campaigns are the fastest shortcut to generating qualified traffic. But they only work if the website loads properly, if tracking is clean and if you measure which click converts into a real customer. Without that foundation, you spend money without knowing where it goes.",
    "serv.s3.h3a": "What does a well-run ad campaign include?",
    "serv.s3.p1": "A campaign is not just \"putting an ad live on Google or Meta\". There are five layers that need to be well coordinated: <strong>tracking</strong> (measuring what happens), <strong>audience</strong> (who you are talking to), <strong>creative</strong> (what you show them), <strong>landing</strong> (where you send them) and <strong>optimisation</strong> (what you do with the incoming data).",
    "serv.s3.p2": "Most SMEs have problems with the first layer: tracking is misconfigured, so the Google and Meta algorithms do not learn which clicks convert. Without that feedback, campaigns optimise towards cheap clicks instead of real customers. Money spent on visits that never buy.",
    "serv.s3.h3b": "Why it matters for your SME",
    "serv.s3.p3": "Done properly, campaigns are the most measurable and predictable channel available. With clean tracking you can know exactly how much a customer costs you, what your ROAS per channel is, which creatives work and which do not. But done poorly, they are the fastest black hole in digital marketing.",
    "serv.s3.p4": "Vantia always starts from tracking: before spending a single euro on ads, we configure GA4 + GTM + Conversions API (Meta) + Enhanced Conversions (Google). Only once data reaches the algorithm cleanly do we start investing.",
    "serv.s3.h3c": "How we do it at Vantia",
    "serv.s3.li1": "<strong>Technical setup before creative setup.</strong> GA4 with custom events, marked conversions, Conversions API on Meta, Enhanced Conversions on Google. We validate that every conversion is measured correctly before launching.",
    "serv.s3.li2": "<strong>Audience research.</strong> Analysis of your real customer (not a generic avatar): who buys, how much they are worth, where they come from, what they do before and after buying. This defines who the campaigns target.",
    "serv.s3.li3": "<strong>Campaign structure by intent.</strong> We do not mix cold audiences with remarketing. Each funnel level has its own campaign, budget and KPI. This is called an \"ABC structure\" and is what allows you to scale without losing efficiency.",
    "serv.s3.li4": "<strong>Tested creatives.</strong> Systematic A/B testing at every level: copy, image, video, CTA. We do not assume what works — we verify it with data.",
    "serv.s3.li5": "<strong>Weekly optimisation with clean data.</strong> Every Monday we review performance, cut what is not working, scale what is. No \"set and forget\" — campaigns left running on their own degrade fast.",
    "serv.s3.li6": "<strong>Monthly report with real numbers.</strong> No vanity metrics (\"impressions\", \"reach\") — only useful numbers: CPL, CAC, ROAS, projected LTV. You know exactly what each euro invested is delivering.",
    "serv.s3.h3d": "What we deliver",
    "serv.s3.del1": "End-to-end validated tracking (website → GA4 → algorithm → report).",
    "serv.s3.del2": "Campaigns on Google Ads (Search, PMax, YouTube) and Meta Ads (Facebook, Instagram).",
    "serv.s3.del3": "Custom audiences + intelligent remarketing.",
    "serv.s3.del4": "Library of creatives tested with real data.",
    "serv.s3.del5": "Campaign dashboard in Looker Studio with CAC, ROAS and attribution.",
    "serv.s3.del6": "Weekly optimisation with actionable recommendations.",
    "serv.s3.cta": "Request a quote · Campaigns",
    "serv.s3.case.eyebrow": "Real case · Measurement and conversion",
    "serv.s3.case.title": "Mendieta — WhatsApp conversion tracking",
    "serv.cta.title": "Ready to <em>scale</em>?",
    "serv.cta.subtitle": "Book a 30-minute session. We audit your case and design a concrete plan.",
    "serv.cta.btn": "Book a free session",

    "serv.grupo2.eyebrow": "The layer that holds the system together",
    "serv.grupo2.title": "Acquiring is good.<br/>\n          <em>Coming back</em> is better.",
    "serv.grupo2.intro": "The three services above put your business where people are searching and measure every visit. These two make sure those people don't leave and come back: social media keeps you present where your audience already spends the day, and email turns a one-off visit into a relationship that buys again. Without this layer, every customer you win has to be won again from scratch. With it, what you measure starts to compound: the system performs, and keeps performing.",

    "serv.s4.num": "04 — Service",
    "serv.s4.title": "Social Media Management",
    "serv.s4.lead": "Being on social media is easy; making that presence bring you customers, less so. The difference lies in what you publish for. We don't manage social media just \"to be there\": we use it to keep you present where your audience already hangs out and to drive qualified traffic to your website, with every visit tagged so we know which post brought whom. A consistent presence, yes, but one that leaves a trail and can be measured.",
    "serv.s4.h3a": "What does \"social media management\" done right actually mean?",
    "serv.s4.p1": "It means taking care of your presence on the channels that genuinely matter for your business, from start to finish: the month's strategy and calendar, the assets and copy in the correct dimensions for each channel, the scheduling, and the day-to-day conversation (replying to comments and messages within the first few hours). It's not posting content and looking away: it's a presence designed to support the rest of your marketing.",
    "serv.s4.p2": "The key is the approach. Most social media management is measured in likes and followers — numbers that look good in a screenshot but don't tell you whether the business is growing. We treat social media as another traffic source: every link we publish carries its tag (UTM) and connects to your analytics, so we know which post brought visits and which of those visits converted. The pretty stuff supports the work; what counts is who you bring in.",
    "serv.s4.h3b": "Why it matters for your SME",
    "serv.s4.p3": "Your audience already spends hours on social media. Being there, consistently, is what makes them remember you when the moment to buy arrives, and it's the social proof your customer checks before deciding: a living profile builds trust, an abandoned one takes it away. Imagine someone discovers you through an ad or through Google and, before messaging you, goes to look at your Instagram. What they find there carries weight.",
    "serv.s4.p4": "And as with everything at Vantia, this doesn't rest on a hunch. Social media feeds the rest of the system: it sends traffic to the website (which converts and measures it), provides brand signals for SEO, and creates audiences your campaigns can reuse. When you know which channel and which type of asset bring you real customers, you stop posting blindly and start investing your time where it pays off.",
    "serv.s4.h3c": "How we do it at Vantia",
    "serv.s4.li1": "<strong>Monthly strategy and editorial calendar.</strong> We define which channels make sense for your business (you don't need all of them) and put together the month's plan: what gets published, when and in what format. Every piece has a reason — we don't fill the calendar just to fill it.",
    "serv.s4.li2": "<strong>Production of assets and copy.</strong> The Designer prepares the assets and the Copywriter writes the copy, in the correct dimensions and tone for each channel. Your brand looks consistent wherever it publishes.",
    "serv.s4.li3": "<strong>Measurement from the very first link.</strong> Every link that goes out to social media carries its tag (UTM) and connects to GA4. So, from day one, we know which post brings traffic and which traffic converts. This is what separates Vantia's social media management from the decorative kind.",
    "serv.s4.li4": "<strong>Scheduling and conversation.</strong> We leave the month scheduled and handle comments and messages within the first few hours, which is when they matter. You validate the final publishing: social platforms penalise full automation, so the last click is human.",
    "serv.s4.li5": "<strong>Organic growth and social proof.</strong> We work on growing qualified followers (not number by number) and the signals your sales side can use to close: an active profile with movement is a selling point.",
    "serv.s4.li6": "<strong>Monthly report that connects social media and business.</strong> Each month we report reach, engagement and growth, yes, but above all the traffic that converts: which post brought visits that ended up as customers. If a channel or a format isn't contributing, we change it.",
    "serv.s4.h3d": "What we deliver",
    "serv.s4.del1": "Monthly editorial calendar, approved by you before we start.",
    "serv.s4.del2": "The month's assets and the push stories, ready and scheduled.",
    "serv.s4.del3": "Copy per channel, in your tone and in the correct dimensions.",
    "serv.s4.del4": "Tagged links (UTMs) connected to GA4 to measure real traffic.",
    "serv.s4.del5": "Management of comments and messages within the first few hours, on business days.",
    "serv.s4.del6": "Monthly report that ties social media to business: from reach to the traffic that converts.",
    "serv.s4.cta": "Request a quote · Social Media",
    "serv.s4.case.eyebrow": "Real case · Social Media",
    "serv.s4.case.title": "Mendieta — Instagram management",

    "serv.s5.num": "05 — Service",
    "serv.s5.title": "Email Marketing",
    "serv.s5.lead": "Email is the most measurable channel there is: you know who opened, who clicked and who bought. We're not talking about \"sending a newsletter now and then\", but about sequences and campaigns that move a concrete metric of your business: getting the customer to buy again, book again, or come back after months of silence. It's the layer that turns a single visit into a relationship that lasts.",
    "serv.s5.h3a": "What is the email marketing we're talking about?",
    "serv.s5.p1": "It's communicating with your customers by email, but designed to build loyalty and measure, not to make noise. On one hand there are the automations: emails that send themselves at the right moment (a welcome message when someone signs up, a reminder if they left a purchase halfway, a nudge to re-engage someone who hasn't been back in a while). On the other, the month's campaigns: the one-off sends with an offer, a piece of news or a story, always with an A/B test on the subject line to learn what works.",
    "serv.s5.p2": "And it's all done on your own list, with permission. No buying databases or emailing people who didn't ask for it: that's spam and, in Europe, a legal risk. The list grows from your website, with sign-up forms and double confirmation. It takes a little more work, but the difference is huge: you write to people who want to hear from you.",
    "serv.s5.h3b": "Why it matters for your SME",
    "serv.s5.p3": "Without email, every customer you win has to be won again: you pay once more to bring them back from an ad or a search. With email, you speak to them directly, with no intermediaries or algorithms in between, and you raise the value each customer leaves over time. Imagine someone who bought from you once six months ago and forgot about you; an email at the right moment brings them back without you having to pay again for their attention.",
    "serv.s5.p4": "It's also where our promise to measure shows more clearly than anywhere else. Every campaign and every automation tells you how many people opened, how many clicked and how much revenue it brought in. We're not talking about \"awareness\" or fuzzy figures: we're talking about euros attributed to a specific send. And GDPR done right, far from being a hurdle, is a trust signal: the customer knows you respect their inbox.",
    "serv.s5.h3c": "How we do it at Vantia",
    "serv.s5.li1": "<strong>Platform and measurement first.</strong> We choose and configure the sending tool (by default Brevo, a European company that respects the GDPR), connect it to your website and leave measurement ready: events and tags (UTMs) linked to GA4. As with campaigns, measuring comes before sending.",
    "serv.s5.li2": "<strong>Clean acquisition from your website.</strong> We set up forms with double confirmation (double opt-in) so your list grows with people who genuinely want to hear from you. It's the foundation for everything else working and for complying with the law without thinking about it.",
    "serv.s5.li3": "<strong>Template and segmentation.</strong> We create a master template with your brand identity and organise the list into segments (customers, prospects, inactive), because you don't write the same thing to everyone.",
    "serv.s5.li4": "<strong>Automations that work on their own.</strong> We build the sequences that move the business even while you're busy with something else: welcome, post-purchase and loyalty, re-engagement of dormant customers and, if your business calls for it, a reminder for a halfway purchase or appointment.",
    "serv.s5.li5": "<strong>Monthly campaigns with A/B testing.</strong> We write, design, segment and send the month's emails, testing two versions of the subject line to keep the one with the best open rate. We don't assume what works: we check it.",
    "serv.s5.li6": "<strong>List health and revenue report.</strong> We keep the list clean (sign-ups, unsubscribes, bounces) and GDPR-compliant, and each month we deliver a report with what matters: opens, clicks, conversions and revenue attributed to each send.",
    "serv.s5.h3d": "What we deliver",
    "serv.s5.del1": "Sending platform configured, with your brand template and sign-up forms on the website.",
    "serv.s5.del2": "Acquisition with double confirmation (double opt-in) and GDPR in order from day one.",
    "serv.s5.del3": "The agreed automations, live and measuring (welcome, loyalty, re-engagement…).",
    "serv.s5.del4": "The month's campaigns, sent, with an A/B test on the subject line.",
    "serv.s5.del5": "A segmented, healthy list, with its consent documented.",
    "serv.s5.del6": "Monthly report with business numbers: opens, clicks, conversions and attributed revenue.",
    "serv.s5.cta": "Request a quote · Email Marketing"
  });

  // ---- NOSOTROS ----
  Object.assign(DICT.en, {
    "nos.meta.title": "About Us · Vantia · Digital Marketing",
    "nos.meta.desc": "About Vantia · Digital Marketing — Technical agency for SMEs and mid-sized companies. Systems that generate ROI, not design.",
    "nos.hero.eyebrow": "About Vantia Digital",
    "nos.hero.title": "We build <em>systems</em> that generate ROI. Not pretty design.",
    "nos.hero.subtitle": "Digital marketing agency specialising in <strong>SMEs and mid-sized companies</strong>. We combine technical architecture, AI and GEO so your business grows in a measurable and sustainable way.",
    "nos.s1.title": "Origins",
    "nos.s1.p1": "Vantia Digital was born from something obvious that the market prefers to ignore: <strong>most agencies sell design</strong>. Beautiful websites that do not convert. Creative campaigns without tracking. Viral strategies with no measurable return. Results impossible to audit.",
    "nos.s1.p2": "Founded in Barcelona, Vantia was built as the antithesis: <strong>we build digital systems that work for ROI</strong>. Where every decision is justified with data and every action has a metric alongside it.",
    "nos.s2.title": "Philosophy",
    "nos.s2.p1": "Digital marketing has changed. Search is no longer just Google: it is <strong>ChatGPT, Perplexity, Gemini</strong>. Purchase decisions are no longer linear: they are fragmented, multi-channel, AI-assisted. And most agencies are still selling what worked five years ago.",
    "nos.s2.p2": "Our philosophy is to build for this new reality. We work with <strong>SMEs and mid-sized companies</strong> that understand sustainable growth is built with <strong>technical architecture + AI + data</strong>. Not with creativity without measurement. Not with shortcuts.",
    "nos.s3.title": "Does this sound <em>familiar</em>?",
    "nos.s3.subtitle": "If any of these statements describes your situation, you are in the right place.",
    "nos.pain1": "\"I have a beautiful website but it does not convert.\"",
    "nos.pain2": "\"I invest in ads but I do not know if they are working.\"",
    "nos.pain3": "\"My competitors appear in ChatGPT and I do not.\"",
    "nos.pain4": "\"I have an agency, but their reports tell me nothing useful.\"",
    "nos.pain5": "\"My business works, but it does not scale. And I do not know why.\"",
    "nos.pain6": "\"I want to grow with technology, but I do not know where to start.\"",
    "nos.s4.title": "Methodology",
    "nos.s4.subtitle": "Four sequential phases. No skips, no shortcuts.",
    "nos.step1.label": "Audit",
    "nos.step1.title": "Diagnosis",
    "nos.step1.desc": "We analyse every metric, every funnel, every leak point.",
    "nos.step2.label": "Strategy",
    "nos.step2.title": "Plan",
    "nos.step2.desc": "We design a plan with measurable objectives and realistic timelines.",
    "nos.step3.label": "Implementation",
    "nos.step3.title": "Execution",
    "nos.step3.desc": "We execute with technical precision and transparent reporting.",
    "nos.step4.label": "Optimisation",
    "nos.step4.title": "Iteration",
    "nos.step4.desc": "Continuous improvement based on real data, not on gut feeling.",
    "nos.s5.title": "Values",
    "nos.value1.title": "Radical transparency",
    "nos.value1.desc": "Every euro invested has full traceability. No black boxes.",
    "nos.value2.title": "Precision over speed",
    "nos.value2.desc": "We prefer to do less, better. Speed without direction is noise.",
    "nos.value3.title": "Results over appearances",
    "nos.value3.desc": "Metrics speak louder than words. And our metrics are auditable.",
    "nos.value4.title": "Long-term partnership",
    "nos.value4.desc": "We do not look for clients, we look for partners. The relationship is the foundation of compounding.",
    "nos.cta.title": "Let's talk about your <em>project</em>.",
    "nos.cta.subtitle": "If our way of working resonates with you, book a no-commitment session.",
    "nos.cta.btn": "Book a free session"
  });

  // ---- CASOS (listado) + 404 ----
  Object.assign(DICT.en, {
    "cases.meta.description": "Vantia · Marketing Digital success stories — Proven real results in E-commerce, SaaS, professional services and retail.",
    "cases.title": "Success stories · Vantia · Marketing Digital",
    "cases.hero.eyebrow": "Success stories",
    "cases.hero.title": "Proven <em>real</em> results.",
    "cases.hero.subtitle": "Selection by sector.",
    "cases.filter.label": "Industry",
    "cases.filter.all": "All",
    "cases.filter.comercio": "Commerce · Retail",
    "cases.filter.gastronomia": "Food & Drink",
    "cases.filter.diseno": "Design · Creative",
    "cases.filter.editorial": "Editorial · Cultural",
    "cases.card.gett.cover_aria": "Read the GeTT Studio success story",
    "cases.card.gett.mockup_aria": "Preview of GeTT Studio",
    "cases.card.gett.sector": "Furniture and noble-wood objects studio",
    "cases.card.gett.action_tag": "Performance + mobile-first →",
    "cases.card.mendieta.cover_aria": "Read the Mendieta success story",
    "cases.card.mendieta.mockup_aria": "Preview of Mendieta",
    "cases.card.mendieta.sector": "Argentine patisserie in Barcelona · online orders",
    "cases.card.mendieta.action_tag": "WhatsApp conversion tracking →",
    "cases.card.salamat.cover_aria": "Read the Salamat Clot success story",
    "cases.card.salamat.mockup_aria": "Preview of Salamat Clot",
    "cases.card.salamat.sector": "100% gluten-free restaurant in el Clot, Barcelona",
    "cases.card.salamat.action_tag": "Local SEO + dietary niche →",
    "cases.card.parrilleros.cover_aria": "Read the Los Hermanos Parrilleros success story",
    "cases.card.parrilleros.mockup_aria": "Preview of Los Hermanos Parrilleros",
    "cases.card.parrilleros.sector": "Argentine barbecue catering in Barcelona · private events",
    "cases.card.parrilleros.action_tag": "Lead gen + qualification →",
    "cases.card.lulitas.cover_aria": "Read the Lulitas Designs success story",
    "cases.card.lulitas.mockup_aria": "Preview of Lulitas Designs",
    "cases.card.lulitas.sector": "Digital and printable stationery · personal brand",
    "cases.card.lulitas.action_tag": "Simple digital catalogue →",
    "cases.card.estanteria.cover_aria": "Read the La Estantería success story",
    "cases.card.estanteria.mockup_aria": "Preview of La Estantería",
    "cases.card.estanteria.sector": "Digital library of short stories",
    "cases.card.estanteria.action_tag": "Technical SEO + GEO →",
    "cases.tag.mobiliario": "Furniture",
    "cases.tag.estudio_diseno": "Design studio",
    "cases.tag.landing": "Landing",
    "cases.tag.gastronomia": "Food & Drink",
    "cases.tag.pedidos_whatsapp": "WhatsApp orders",
    "cases.tag.landing_custom": "Custom landing",
    "cases.tag.sin_gluten": "Gluten-free · vegan",
    "cases.tag.catering_asado": "Catering · barbecue",
    "cases.tag.marca_personal": "Personal brand",
    "cases.tag.mostrar_productos": "Product showcase",
    "cases.tag.catalogo": "Catalogue",
    "cases.tag.editorial_cultural": "Editorial · cultural",
    "cases.tag.lectura_online": "Online reading",
    "cases.tag.sitio_editorial": "Editorial site",
    "cases.live": "View live site <svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M7 17 17 7\"/><path d=\"M7 7h10v10\"/></svg>",
    "cases.quote": "Request a similar quote",
    "cases.empty.text": "No cases match those filters.",
    "cases.empty.reset": "Clear filters",
    "cases.cta.title": "I want <em>results</em> like these.",
    "cases.cta.subtitle": "Book a 30-minute session. We'll tell you straight whether your case is a fit.",
    "cases.cta.btn": "Book a free session",
    "e404.meta.description": "Page not found — Vantia · Marketing Digital.",
    "e404.title": "404 · Page not found — Vantia · Marketing Digital",
    "e404.hero.eyebrow": "Error 404",
    "e404.hero.title": "This page does not <em>exist</em>.",
    "e404.hero.subtitle": "The link may be broken or the page has moved. Return to the home page or keep exploring the site.",
    "e404.btn.home": "Back to home",
    "e404.nav.links": "Or go straight to <a href=\"/servicios\" style=\"text-decoration: underline; text-underline-offset: 3px;\">Services</a>, <a href=\"/casos/\" style=\"text-decoration: underline; text-underline-offset: 3px;\">Success stories</a> or <a href=\"/contacto\" style=\"text-decoration: underline; text-underline-offset: 3px;\">Contact</a>."
  });

  // ---- CONTACTO ----
  Object.assign(DICT.en, {
    "cont.meta.desc": "Contact Vantia · Digital Marketing — Form, WhatsApp, email, Calendly and social media.",
    "cont.title": "Contact · Vantia · Digital Marketing",
    "cont.hero.eyebrow": "Contact",
    "cont.hero.title": "I want to <em>grow</em> my business.",
    "cont.hero.subtitle": "Choose the channel you prefer. We respond within 24 business hours.",
    "cont.form.name": "Full name <span class=\"req\">*</span>",
    "cont.form.company": "Company",
    "cont.form.email": "Email <span class=\"req\">*</span>",
    "cont.form.phone": "Phone",
    "cont.form.inquiry": "Subject <span class=\"req\">*</span>",
    "cont.form.inquiry_ph": "What's this about?",
    "cont.form.opt1": "I want a free audit",
    "cont.form.opt2": "I have a project in mind",
    "cont.form.opt3": "I'm looking for advice, not sure what I need yet",
    "cont.form.opt4": "Other",
    "cont.form.opt5": "Other",
    "cont.form.message": "Message <span class=\"req\">*</span>",
    "cont.form.submit": "Send message",
    "cont.form.services": "Which services are you interested in?",
    "cont.form.svc_web": "Web Optimization",
    "cont.form.svc_seo": "Technical SEO + GEO",
    "cont.form.svc_ads": "Ad campaigns",
    "cont.form.svc_email": "Email marketing",
    "cont.form.svc_social": "Social media management",
    "cont.form.budget": "Advertising budget <span class=\"req\">*</span>",
    "cont.form.budget_ph": "E.g. 500",
    "cont.form.budget_hint": "Approx. €/month. Enter 0 if you're not investing yet.",
    "cont.aside.h1": "Response time",
    "cont.aside.p1": "We respond to every message within 24 business hours. If your case is urgent, use WhatsApp.",
    "cont.aside.h2": "Before you write",
    "cont.aside.p2": "The more context you give us about your project, the better our first response will be. If you have current metrics, links or documentation, include them in the message.",
    "cont.aside.li1": "Barcelona, Spain",
    "cont.aside.li2": "Mon to Fri · 09:00–18:00 CET",
    "cont.aside.li3": "We work remotely with global clients",
    "cont.ch.eyebrow": "— Or",
    "cont.ch.title": "Contact us <em>directly</em>",
    "cont.ch.calendly.label": "Calendly · featured",
    "cont.ch.calendly.title": "Book a free 30-min session",
    "cont.ch.calendly.desc": "The fastest way to find out if we are a good fit. No commitment, no sales filter.",
    "cont.ch.wa.desc": "Direct reply within a few hours.",
    "cont.ch.email.desc": "Ideal for messages with attached documentation.",
    "cont.ch.x.desc": "News, ideas and debate on technical marketing.",
    "cont.ch.tiktok.desc": "Content on scaling and digital architecture.",
    "cont.ch.ig.desc": "Behind the scenes of the studio.",
    "cont.ch.yt.desc": "Technical analyses and case studies in video format.",
    "cont.ch.li.desc": "Professional content and B2B networking."
  });

  // ---- CASO: GeTT + La Estantería ----
  Object.assign(DICT.en, {
    "cs_gett.page.title": "GeTT Studio — Performance + mobile-first · Vantia · Marketing Digital",
    "cs_gett.meta.description": "Case study · GeTT Studio — Performance and mobile-first for a fine-wood furniture studio.",
    "cs_gett.breadcrumb.casos": "Case studies",
    "cs_gett.hero.eyebrow": "Featured service · Performance and mobile-first",
    "cs_gett.hero.title": "A <em>visual</em> landing page that doesn't sacrifice speed.",
    "cs_gett.hero.lead": "GeTT Studio crafts fine wood furniture piece by piece. Their website had to showcase the detail of the material without sacrificing speed. Performance not as decoration, but as a condition.",
    "cs_gett.meta.client_l": "Client",
    "cs_gett.meta.sector_l": "Sector",
    "cs_gett.meta.sector_v": "Furniture · Design",
    "cs_gett.meta.year_l": "Year",
    "cs_gett.meta.action_l": "Featured service",
    "cs_gett.meta.action_v": "Web Optimisation",
    "cs_gett.meta.stack_l": "Stack",
    "cs_gett.s1.h2": "The challenge",
    "cs_gett.s1.p1": "When the product is handcrafted, photography is heavy. Every piece needs to be seen in detail, in high resolution, with the grain of the wood clearly defined. The obvious problem: heavy images kill performance, and slow sites kill conversion. In design studios this is felt more acutely: someone looking for unique furniture arrives on mobile, waits 3 seconds at most, and leaves.",
    "cs_gett.s1.p2": "The technical challenge was clear. Show the piece with real visual weight, load the site fast on a typical 4G connection, and have Google reward it with good organic rankings.",
    "cs_gett.s2.h2": "Our approach",
    "cs_gett.s2.p1": "Mobile-first for real, not as a sales label. We designed the entire experience from the mobile viewport upwards. This shifts decisions from the outset: bundle weight, visual hierarchy, what information appears in the first scroll, what gets deferred.",
    "cs_gett.s2.p2": "Every image goes through an optimisation pipeline before being uploaded. Modern formats (WebP and AVIF with a JPG fallback), responsive sizes served with <code>srcset</code>, native lazy loading for everything not above the fold. The browser downloads only what it needs, at the exact resolution for the user's screen.",
    "cs_gett.s3.h2": "What was done in detail",
    "cs_gett.s3.li1": "<strong>Optimised image pipeline.</strong> WebP compression with visually indistinguishable quality, dimensions served according to viewport, native lazy loading. Images that previously weighed 2 MB dropped to 180 KB with no perceptible loss.",
    "cs_gett.s3.li2": "<strong>Inline critical CSS.</strong> The CSS required to render the first view is inlined in the HTML. The browser does not wait for external CSS before painting. Result: First Contentful Paint under 800 ms.",
    "cs_gett.s3.li3": "<strong>Fonts with display:swap.</strong> Custom typography does not block rendering. Text appears with a system fallback and is swapped when the real font loads, with no Cumulative Layout Shift.",
    "cs_gett.s3.li4": "<strong>Non-blocking JavaScript.</strong> All non-essential JS is loaded with <code>defer</code>. Animations execute after the main content is visible, not before.",
    "cs_gett.s3.li5": "<strong>Cloudflare cache headers configured.</strong> Static assets cached to the maximum, HTML with a short cache. The second visit is practically instantaneous.",
    "cs_gett.s4.h2": "What was optimised and how it is measured",
    "cs_gett.s4.p1": "Performance is not promised — it is verified. The site is built targeting the three metrics Google uses to evaluate user experience (Core Web Vitals):",
    "cs_gett.s4.li1": "<strong>LCP (loading speed of the main content):</strong> optimised images, inline critical CSS, and non-blocking fonts so content appears as quickly as possible.",
    "cs_gett.s4.li2": "<strong>CLS (visual stability):</strong> reserved dimensions for every image and block, with no layout shifts while loading.",
    "cs_gett.s4.li3": "<strong>INP (interaction responsiveness):</strong> deferred, non-blocking JavaScript so the site responds instantly to the first tap.",
    "cs_gett.s4.li4": "<strong>Accessibility:</strong> contrast, keyboard navigation, and semantic markup following WCAG guidelines.",
    "cs_gett.s4.p2": "Anyone can check the current state of the site in real time with <a href=\"https://pagespeed.web.dev/\" target=\"_blank\" rel=\"noopener noreferrer\">PageSpeed Insights</a> from Google. Transparency is part of the work: the numbers are whatever the tool shows, not whatever we claim.",
    "cs_gett.cta.live": "View live site",
    "cs_gett.cta.contact": "I want something like this",
    "cs_gett.nav.back": "Back to all case studies",
    "cs_est.page.title": "La Estantería — Technical SEO + GEO for editorial sites · Vantia · Marketing Digital",
    "cs_est.meta.description": "Case study · La Estantería — Technical SEO + GEO for a digital library of short stories.",
    "cs_est.breadcrumb.casos": "Case studies",
    "cs_est.hero.eyebrow": "Featured service · Technical SEO + GEO in editorial content",
    "cs_est.hero.title": "Ranking an editorial site on <em>Google and in AI</em>.",
    "cs_est.hero.lead": "La Estantería is a digital library of short stories. To grow, it needs to appear in two distinct places: in Google search results and in the answers from ChatGPT, Perplexity, and Gemini. Two disciplines that share the same foundation but diverge in tactics.",
    "cs_est.meta.client_l": "Client",
    "cs_est.meta.sector_l": "Sector",
    "cs_est.meta.sector_v": "Editorial · Cultural",
    "cs_est.meta.year_l": "Year",
    "cs_est.meta.action_l": "Featured service",
    "cs_est.meta.action_v": "Technical SEO + GEO",
    "cs_est.meta.stack_l": "Stack",
    "cs_est.s1.h2": "The challenge",
    "cs_est.s1.p1": "An editorial site lives or dies by its ability to be found when someone searches for similar content. Five years ago that meant ranking on Google. Today it means ranking on Google <strong>and</strong> being cited by generative AI engines (ChatGPT, Perplexity, Gemini, Claude). Search behaviour is changing fast: a portion of traditional organic traffic is shifting to conversational AI search.",
    "cs_est.s1.p2": "The challenge: build the site from the ground up with both disciplines in mind. Classic Technical SEO for Google and GEO (Generative Engine Optimization) for the new engines.",
    "cs_est.s2.h2": "Our approach",
    "cs_est.s2.p1": "SEO and GEO overlap at the technical foundation (fast site, clear semantic structure, correct schema) but diverge in tactics. SEO looks at backlinks, domain authority, and keywords. GEO looks at the <strong>citability</strong> of the content: how easily an AI model can extract a verifiable statement and correctly attribute it to your site.",
    "cs_est.s2.p2": "The strategy was to work both layers in parallel without sacrificing either. What serves one rarely harms the other when the technical foundation is solid.",
    "cs_est.s3.h2": "What was done in detail",
    "cs_est.s3.li1": "<strong>Advanced editorial schema markup.</strong> Every story implements <code>Article</code> schema with author, publication date, modification date, and thematic keywords. Category pages use <code>BreadcrumbList</code> and <code>CollectionPage</code>. Pages with frequently asked questions implement <code>FAQPage</code>. This gives Google and AI engines a clear structure for what to read and how to cite it.",
    "cs_est.s3.li2": "<strong>Clean, semantic URLs.</strong> A <code>/category/story-slug</code> structure that communicates hierarchy without ambiguity. No tracking parameters in the base URL. Correct canonical tags on every page.",
    "cs_est.s3.li3": "<strong>XML sitemap by section.</strong> Master sitemap plus per-category sitemaps. Change frequency correctly indicated. This speeds up the indexing of new content and gives Google a clear view of the site architecture.",
    "cs_est.s3.li4": "<strong>Content format designed for citability.</strong> Every story opens with a clear, verifiable summary paragraph. Relevant data (author, date, context) appears at the top. This makes it straightforward for an AI model to cite the site without having to infer or guess.",
    "cs_est.s3.li5": "<strong>Core Web Vitals in the green.</strong> Performance is not optional. Google and AI engines penalise slow sites heavily. Lighthouse 95+ from day one.",
    "cs_est.s3.li6": "<strong>Open Graph and meta tags optimised.</strong> When someone shares a story on social media, the preview looks perfect: title, description, image. This increases CTR on social networks and brand recognition.",
    "cs_est.s4.h2": "Setup results",
    "cs_est.s4.p1": "The site has been correctly indexed in Google since day one. Initial manual tests on ChatGPT and Perplexity for topics related to the editorial catalogue are showing that the model finds and cites the content when asked about short stories or specific authors published on La Estantería.",
    "cs_est.s4.p2": "The next step is sustained editorial content to accumulate thematic authority in the niche. Citability in AI engines is not built in days — it is built over months of consistent publications that the model learns to recognise as a reliable source.",
    "cs_est.cta.live": "View live site",
    "cs_est.cta.contact": "I want something like this",
    "cs_est.nav.back": "Back to all case studies"
  });

  // ---- CASO: Lulitas + Mendieta ----
  Object.assign(DICT.en, {
    "cs_lul.meta_desc": "Case study · Lulitas Designs — A digital stationery catalogue without the complexity of a full e-commerce platform.",
    "cs_lul.page_title": "Lulitas Designs — Digital catalogue + personal brand · Vantia · Digital Marketing",
    "cs_lul.breadcrumb_cases": "Case studies",
    "cs_lul.eyebrow": "Featured action · Digital catalogue without a full e-commerce platform",
    "cs_lul.h1": "Selling products without <em>burdening</em> yourself with a full shop.",
    "cs_lul.lead": "Lulitas Designs creates digital and printable stationery. She does not need a shopping cart, a complex payment gateway, or physical stock management. She only needs to showcase, attract, and sell through direct contact.",
    "cs_lul.meta.client_l": "Client",
    "cs_lul.meta.sector_l": "Sector",
    "cs_lul.meta.sector_v": "Digital stationery · Personal brand",
    "cs_lul.meta.year_l": "Year",
    "cs_lul.meta.action_l": "Featured action",
    "cs_lul.meta.action_v": "Simple digital catalogue",
    "cs_lul.meta.stack_l": "Stack",
    "cs_lul.meta.stack_v": "Static HTML · Responsive grid · Lazy loading",
    "cs_lul.s1.h2": "The challenge",
    "cs_lul.s1.p1": "The trap that catches entrepreneurs selling digital products: believing they need Shopify, WooCommerce, or some other robust e-commerce platform. For Lulitas, that would have been overkill. Every platform comes with a monthly cost, a learning curve, and ongoing maintenance. And most importantly: it slows the site down and breaks the personal-brand aesthetic.",
    "cs_lul.s1.p2": "The challenge was to build a powerful visual showcase that communicated quality, made it clear what was on sale and how to buy it, and allowed the sale to close through a direct channel (email or social), bypassing any platform entirely.",
    "cs_lul.s2.h2": "How we approached it",
    "cs_lul.s2.p1": "A pure static site: HTML, CSS, zero heavy dependencies. The catalogue is organised as a visual grid where every product has its place, its description, and its price. When a customer wants to buy, they go straight through their preferred channel: WhatsApp, Instagram DM, or email. No complicated forms, no login, no checkout.",
    "cs_lul.s2.p2": "The personal brand carries more weight than the product itself. Typography, colour palette, and tone of communication all have to reflect the person behind the studio. That visual consistency is what turns visits into customers.",
    "cs_lul.s3.h2": "What was done in practice",
    "cs_lul.s3.li1": "<strong>Product grid with a strong visual identity.</strong> Every product is presented with a quality photograph, a concise description, and a clear price. No distractions, no promotional badges cluttering the layout.",
    "cs_lul.s3.li2": "<strong>Zero e-commerce platform.</strong> No Shopify, no WooCommerce, no Stripe. The customer shows interest, clicks “Order”, and goes straight to WhatsApp or email. The sale closes in the channel that converts best for low-price, high-personalisation products.",
    "cs_lul.s3.li3": "<strong>Aggressive lazy loading + WebP images.</strong> The catalogue can grow to 50 + products without the site slowing down. Each image loads only when it enters the viewport.",
    "cs_lul.s3.li4": "<strong>Cross-channel brand consistency.</strong> The site’s palette, typography, and tone match exactly with Instagram, the email signature, and the printable PDFs. The same visual universe across every touchpoint.",
    "cs_lul.s3.li5": "<strong>Basic SEO done properly.</strong> Schema Product on every item, meta tags per category, Open Graph optimised so that when the catalogue is shared on social media it looks right.",
    "cs_lul.s4.h2": "Setup results",
    "cs_lul.s4.p1": "The site fulfils its purpose at the lowest possible operational cost: zero euros per month on platforms, simple maintenance (adding or changing products means editing HTML), and load speed that outperforms any CMS- or e-commerce-based solution.",
    "cs_lul.s4.p2": "Closing via direct channel (WhatsApp or email) achieves a higher conversion rate than a typical e-commerce cart for products in the “personalisation + emotional decision” category, such as artistic stationery.",
    "cs_lul.cta.live": "View live site",
    "cs_lul.cta.contact": "I want something like this",
    "cs_lul.nav_back": "Back to all case studies",
    "cs_men.meta_desc": "Case study · Mendieta — How to measure a conversion that happens over WhatsApp. Offline-online tracking.",
    "cs_men.page_title": "Mendieta — WhatsApp orders + tracking · Vantia · Digital Marketing",
    "cs_men.breadcrumb_cases": "Case studies",
    "cs_men.eyebrow": "Featured action · WhatsApp conversion tracking",
    "cs_men.h1": "How to measure a <em>conversion</em> that happens over WhatsApp.",
    "cs_men.lead": "Mendieta sells Argentine pastries in Barcelona. The customer visits the website, browses the catalogue, and ends up ordering over WhatsApp. The close is offline, but the data cannot be lost.",
    "cs_men.meta.client_l": "Client",
    "cs_men.meta.sector_l": "Sector",
    "cs_men.meta.sector_v": "Food & beverage · Bakery",
    "cs_men.meta.year_l": "Year",
    "cs_men.meta.action_l": "Featured action",
    "cs_men.meta.action_v": "Offline-online measurement",
    "cs_men.meta.stack_l": "Stack",
    "cs_men.s1.h2": "The challenge",
    "cs_men.s1.p1": "In the food and beverage sector, traditional e-commerce does not always fit. Many small businesses close their sales over WhatsApp: the customer asks, adjusts the order, confirms a date, and collects in person. But the usual problem is that when the customer leaves the site to open WhatsApp, the data breaks. How many of those clicks ended in a sale? What is the cost per order? Which acquisition channel performs best? Without tracking, these questions have no answer.",
    "cs_men.s2.h2": "How we approached it",
    "cs_men.s2.p1": "We designed a measurement system that connects the click on “Order via WhatsApp” with the full funnel: from the acquisition channel all the way to the final conversion. The key insight is that the click is the <strong>measurable conversion</strong>: everything that happens afterwards inside WhatsApp is the operator’s responsibility, but the lead’s origin and qualification are tracked at 100%.",
    "cs_men.s3.h2": "What was done in practice",
    "cs_men.s3.li1": "<strong>Click-to-Chat with a pre-filled message.</strong> Every “Order via WhatsApp” button opens the conversation with a message that already includes the product or section of interest. This qualifies the lead before they type a single word.",
    "cs_men.s3.li2": "<strong>Custom event in GA4 on click.</strong> Every click on “Order via WhatsApp” fires a <code>click_whatsapp</code> event with parameters: product, position on the page, device, and source. That event is marked as a conversion in GA4.",
    "cs_men.s3.li3": "<strong>UTM tags on every inbound channel.</strong> Instagram posts, Google Business Profile links, mailings: every outbound link carries unique UTMs. We know exactly where each customer who ended up on WhatsApp came from.",
    "cs_men.s3.li4": "<strong>Looker Studio dashboard with the full funnel.</strong> Visits → Product views → WhatsApp clicks → Cost per WhatsApp click (calculated against spend on each channel). The business owner reads the report without needing any marketing knowledge.",
    "cs_men.s3.li5": "<strong>Consent Mode v2 correctly integrated.</strong> Tracking respects the user’s choice in the cookie banner without losing signal in GA4 (thanks to Google’s data modelling).",
    "cs_men.s4.h2": "Setup results",
    "cs_men.s4.p1": "What was once a black box is now a measurable funnel. The business owner can answer with data questions that previously relied on intuition: which catalogue product generates the most enquiries, which acquisition channel converts best, which days of the week see the highest demand. That information drives real decisions: where to invest in advertising, which product to feature on the homepage, which opening hours are critical.",
    "cs_men.s4.p2": "The dashboard has been live since the very first order received. Every WhatsApp click is recorded and attributed by channel and time of day. The operator can read the weekly reports and make commercial decisions with data that previously did not exist.",
    "cs_men.cta.live": "View live site",
    "cs_men.cta.contact": "I want something like this",
    "cs_men.nav_back": "Back to all case studies"
  });

  // ---- CASO: Parrilleros + Salamat ----
  Object.assign(DICT.en, {
    "cs_par.meta.description": "Case study · Los Hermanos Parrilleros — Lead generation landing for private B2B events.",
    "cs_par.page.title": "Los Hermanos Parrilleros — Lead generation for events · Vantia · Marketing Digital",
    "cs_par.breadcrumb.aria": "Breadcrumb navigation",
    "cs_par.breadcrumb.casos": "Case studies",
    "cs_par.hero.eyebrow": "Featured work · Lead generation for consultative sales",
    "cs_par.hero.h1": "Capturing <em>qualified</em> leads for private events.",
    "cs_par.hero.lead": "Los Hermanos Parrilleros provide Argentine asado catering for premium private events. Every lead is worth a 30-minute conversation. The website had to filter prospects before that conversation even begins.",
    "cs_par.meta.label.client": "Client",
    "cs_par.meta.label.sector": "Sector",
    "cs_par.meta.value.sector": "Catering · Premium events",
    "cs_par.meta.label.year": "Year",
    "cs_par.meta.label.action": "Featured work",
    "cs_par.meta.value.action": "Lead gen + qualification",
    "cs_par.meta.label.stack": "Stack",
    "cs_par.meta.value.stack": "Custom landing · Forms · WhatsApp pre-filled",
    "cs_par.s1.h2": "The challenge",
    "cs_par.s1.p1": "Catering for private events is pure consultative sales. A wedding, a company with 80 guests, a birthday with a bespoke menu: every lead requires a conversation. The classic mistake is placing a bare \"Contact us\" form with no further context. Leads that arrive that way are cold, poorly informed, and consume the operator's time before filtering the ones that are worth pursuing.",
    "cs_par.s1.p2": "The challenge: to have the website itself handle the first layer of qualification. So that when an enquiry arrives, the operator already knows what type of event it is, approximately how many guests, what date, and what kind of service is needed.",
    "cs_par.s2.h2": "How we approached it",
    "cs_par.s2.p1": "We structured the landing page as a stepped conversation. Each section answers a question the prospective client is asking themselves mentally, in the order they ask it. By the time they reach the form, they already understand which type of service fits them and are ready to provide the information the operator needs to respond well.",
    "cs_par.s3.h2": "What was done in practice",
    "cs_par.s3.li1": "<strong>Visual storytelling of the experience.</strong> The homepage explains what a premium Argentine asado for events is: who does it, how the service works, what is delivered. This acts as a pre-filter: anyone looking for cheap catering quickly realises this is not the right place.",
    "cs_par.s3.li2": "<strong>Menu section with clearly defined formats.</strong> Three differentiated service formats: intimate event, corporate event, large-format event. Each with a description of what is included, guest numbers, and the type of customisation available.",
    "cs_par.s3.li3": "<strong>Qualifying form with structured fields.</strong> Not just name and email: event type, approximate date, number of guests, location, indicative budget. This filters out enquiries that are not a fit before any time is spent on a response.",
    "cs_par.s3.li4": "<strong>\"Request a quote via WhatsApp\" button with a pre-filled message.</strong> For those who prefer direct chat, the message already includes the key fields the operator needs. Same principle as the form, different interface.",
    "cs_par.s3.li5": "<strong>Tracking every completed form submission in GA4.</strong> The <code>enviar_reserva</code> event is marked as a conversion. We know what percentage of visitors reach the form, complete it, and become a qualified lead.",
    "cs_par.s4.h2": "Setup results",
    "cs_par.s4.p1": "The qualifying structure changes the type of leads that come in. The operator receives fewer enquiries in volume but more qualified ones, which reduces the time to close and increases the conversion rate from lead to contracted event. The integrated measurement makes it possible to iterate on which parts of the landing convert best and where the funnel drops off.",
    "cs_par.s4.p2": "The most useful feedback comes from the operator after each closed event: how many back-and-forths the close required, which form fields saved time, which types of events convert best. That information feeds subsequent iterations on the landing page.",
    "cs_par.cta.live": "View live site",
    "cs_par.cta.contact": "I want something like this",
    "cs_par.backnav.aria": "Navigation between case studies",
    "cs_par.backnav.label": "Back to all case studies",
    "cs_sal.meta.description": "Case study · Salamat Clot — Local SEO for a niche gluten-free restaurant in Barcelona.",
    "cs_sal.page.title": "Salamat Clot — Local SEO + dietary niche · Vantia · Marketing Digital",
    "cs_sal.breadcrumb.aria": "Breadcrumb navigation",
    "cs_sal.breadcrumb.casos": "Case studies",
    "cs_sal.hero.eyebrow": "Featured work · Local SEO and dietary niche",
    "cs_sal.hero.h1": "<em>Local</em> SEO for a 100% gluten-free restaurant.",
    "cs_sal.hero.lead": "Salamat Clot combines two very specific filters: neighbourhood (el Clot, Barcelona) and diet (gluten-free, vegan options). Searches are long-tail and local. Technical SEO here is not optional — it is the difference between existing or not on Google.",
    "cs_sal.meta.label.client": "Client",
    "cs_sal.meta.label.sector": "Sector",
    "cs_sal.meta.value.sector": "Food & drink · Gluten-free",
    "cs_sal.meta.label.year": "Year",
    "cs_sal.meta.label.action": "Featured work",
    "cs_sal.meta.value.action": "Local technical SEO",
    "cs_sal.meta.label.stack": "Stack",
    "cs_sal.s1.h2": "The challenge",
    "cs_sal.s1.p1": "When someone searches for \"gluten-free restaurant Clot\" on Google, there are literally five possible options. Appearing in that list is not optional: if you do not appear, you do not exist. The technical challenge is threefold: geographic (a specific neighbourhood in Barcelona), dietary (strict gluten-free filter plus vegan options), and intentional (people who want to book a table, not read a blog).",
    "cs_sal.s1.p2": "And all of this with no advertising budget. Well-executed local SEO has to outperform a Google Maps ad.",
    "cs_sal.s2.h2": "How we approached it",
    "cs_sal.s2.p1": "Niche local SEO operates by different rules to generic SEO. The strongest signal for Google is <strong>consistency across sources</strong>: name, address, phone number, opening hours, specialities. If the website, Google Business Profile, TripAdvisor, social channels, and aggregators all say the same thing in the same structure, Google understands the business is real and prioritises it.",
    "cs_sal.s3.h2": "What was done in practice",
    "cs_sal.s3.li1": "<strong>Advanced schema markup.</strong> Implementation of <code>Restaurant</code> + <code>LocalBusiness</code> + <code>FoodEstablishment</code> schema with all relevant fields: opening hours, georeferenced address, menu with prices, cuisine type, dietary options (glutenFreeOption, veganOption). This allows Google to understand exactly what the restaurant offers.",
    "cs_sal.s3.li2": "<strong>Optimised Google Business Profile.</strong> Correct primary and secondary categories, description with natural local keywords (\"sin gluten Clot Barcelona\"), weekly photos, regular posts. GMB is the highest source of local traffic.",
    "cs_sal.s3.li3": "<strong>Content targeting long-tail searches.</strong> Each section of the website targets real queries: \"gluten-free menu Barcelona\", \"coeliac restaurant Clot\", \"vegan gluten-free food\". No keyword stuffing — written naturally.",
    "cs_sal.s3.li4": "<strong>Performance + accessibility as an SEO factor.</strong> Google uses Core Web Vitals as a ranking signal. Fast site, validated WCAG accessibility, impeccable mobile-first implementation.",
    "cs_sal.s3.li5": "<strong>Tracking local searches with GA4 + Search Console.</strong> We know exactly which queries bring visitors, which ones convert into a booking or a call, and where to optimise the content.",
    "cs_sal.s4.h2": "Setup results",
    "cs_sal.s4.p1": "The site has been correctly indexed from day one, with all local signals in order. The first long-tail searches related to gluten-free + Clot are already ranking on the first page. The next objective is to gain positions for more competitive searches (gluten-free Barcelona in general) with sustained editorial content.",
    "cs_sal.s4.p2": "Search Console is already showing the first impressions for neighbourhood searches (Clot + gluten-free + restaurant). The initial CTR is high because there is little direct competition in the cross-filtered niche. The next objective is to expand the geographic radius without losing position in the neighbourhood.",
    "cs_sal.cta.live": "View live site",
    "cs_sal.cta.contact": "I want something like this",
    "cs_sal.backnav.aria": "Navigation between case studies",
    "cs_sal.backnav.label": "Back to all case studies"
  });

  // ---- LEGALES: Privacidad + Cookies + Aviso legal ----
  Object.assign(DICT.en, {
    "leg_priv.meta_desc": "Privacy Policy of Vantia Digital. Processing of personal data in accordance with the GDPR and the LOPDGDD.",
    "leg_priv.title": "Privacy Policy · Vantia Digital",
    "leg_priv.eyebrow": "Legal document",
    "leg_priv.h1": "Privacy <em>Policy</em>.",
    "leg_priv.subtitle": "How we process your personal data in accordance with the GDPR and the LOPDGDD.",
    "leg_priv.meta": "Last updated: 20 May 2026",
    "leg_priv.s1.h2": "1. Data controller",
    "leg_priv.s1.p1": "In accordance with Regulation (EU) 2016/679 on the General Data Protection Regulation (GDPR) and Organic Law 3/2018 on the Protection of Personal Data and Guarantee of Digital Rights (LOPDGDD), we provide the following details of the data controller:",
    "leg_priv.s1.li1": "<strong>Name / Company:</strong> [TO BE COMPLETED — Full name / Company name]",
    "leg_priv.s1.li2": "<strong>Tax ID (NIF):</strong> [TO BE COMPLETED]",
    "leg_priv.s1.li3": "<strong>Address:</strong> [TO BE COMPLETED — Full registered address], Barcelona, Spain",
    "leg_priv.s1.li4": "<strong>Email:</strong> <a href=\"mailto:admin@vantia.digital\">admin@vantia.digital</a>",
    "leg_priv.s1.li5": "<strong>Website:</strong> <a href=\"https://vantia.digital\">https://vantia.digital</a>",
    "leg_priv.s2.h2": "2. Data we collect",
    "leg_priv.s2.p1": "We process personal data that you voluntarily provide through the site's contact forms and channels, as well as data generated automatically through analytical cookies (subject to prior consent).",
    "leg_priv.s2.th1": "Source",
    "leg_priv.s2.th2": "Data",
    "leg_priv.s2.th3": "Purpose",
    "leg_priv.s2.td1a": "Contact form",
    "leg_priv.s2.td1b": "Name, email, phone (optional), company, message",
    "leg_priv.s2.td1c": "Handling the commercial enquiry or request",
    "leg_priv.s2.td2a": "Direct email or WhatsApp",
    "leg_priv.s2.td2b": "Data the user chooses to provide",
    "leg_priv.s2.td2c": "Maintaining communication",
    "leg_priv.s2.td3a": "Google Analytics 4 (with consent)",
    "leg_priv.s2.td3b": "Pseudonymised browsing data, anonymised IP address",
    "leg_priv.s2.td3c": "Aggregated statistical analysis of the site",
    "leg_priv.s3.h2": "3. Legal basis for processing",
    "leg_priv.s3.li1": "<strong>Consent</strong> (Art. 6.1.a GDPR): for sending commercial communications and for non-essential cookies.",
    "leg_priv.s3.li2": "<strong>Performance of a contract or pre-contractual measures</strong> (Art. 6.1.b GDPR): for handling enquiries and providing the requested services.",
    "leg_priv.s3.li3": "<strong>Legitimate interest</strong> (Art. 6.1.f GDPR): for maintaining site security.",
    "leg_priv.s3.li4": "<strong>Legal obligation</strong> (Art. 6.1.c GDPR): for compliance with tax and commercial obligations.",
    "leg_priv.s4.h2": "4. Retention period",
    "leg_priv.s4.p1": "We will retain your data for the period strictly necessary for the purpose of the processing and, where applicable, for the legally required retention periods (Commercial Code, tax regulations). Analytical data is retained for a maximum of <strong>14 months</strong>. Commercial contact data is retained for as long as the relationship exists or until you request its deletion.",
    "leg_priv.s5.h2": "5. Recipients and data processors",
    "leg_priv.s5.p1": "We do not transfer your data to third parties except where legally required. We work with the following data processors, all of which provide adequate safeguards in accordance with the GDPR:",
    "leg_priv.s5.li1": "<strong>Google Ireland Limited</strong> (Google Analytics 4) — pseudonymised analytical data. International transfers covered by Standard Contractual Clauses (SCCs) and the EU-U.S. Data Privacy Framework.",
    "leg_priv.s5.li2": "<strong>Cloudflare, Inc.</strong> — hosting (Cloudflare Pages) and CDN. Transfer covered by SCCs.",
    "leg_priv.s5.li3": "<strong>Google Workspace</strong> — corporate email.",
    "leg_priv.s6.h2": "6. Your rights",
    "leg_priv.s6.p1": "As the data subject, you may exercise the following rights at any time:",
    "leg_priv.s6.li1": "<strong>Access, rectification and erasure</strong> of your data.",
    "leg_priv.s6.li2": "<strong>Objection</strong> to processing and <strong>restriction</strong> thereof.",
    "leg_priv.s6.li3": "<strong>Data portability</strong>.",
    "leg_priv.s6.li4": "<strong>Withdrawal of consent</strong> at any time without affecting the lawfulness of processing carried out prior to withdrawal.",
    "leg_priv.s6.li5": "<strong>Lodge a complaint with the Spanish Data Protection Agency (Agencia Española de Protección de Datos)</strong> (<a href=\"https://www.aepd.es\" target=\"_blank\" rel=\"noopener noreferrer\">www.aepd.es</a>).",
    "leg_priv.s6.p2": "To exercise these rights, please send an email to <a href=\"mailto:admin@vantia.digital\">admin@vantia.digital</a> stating the right you wish to exercise and attaching a copy of an identity document.",
    "leg_priv.s7.h2": "7. Security measures",
    "leg_priv.s7.p1": "We apply appropriate technical and organisational measures to ensure a level of security appropriate to the risk of the processing, including encryption in transit (HTTPS/TLS), access controls and activity logging.",
    "leg_priv.s8.h2": "8. Cookies",
    "leg_priv.s8.p1": "For detailed information about the cookies we use, please consult our <a href=\"/cookies\">Cookie Policy</a>.",
    "leg_priv.s9.h2": "9. Amendments",
    "leg_priv.s9.p1": "We reserve the right to amend this policy in order to adapt it to legislative or case-law developments. In such cases, the changes will be published on this page with an updated date.",
    "leg_cook.meta_desc": "Cookie Policy of Vantia Digital. Types of cookies used and consent management.",
    "leg_cook.title": "Cookie Policy · Vantia Digital",
    "leg_cook.eyebrow": "Legal document",
    "leg_cook.h1": "Cookie <em>Policy</em>.",
    "leg_cook.subtitle": "Information about the cookies we use and how to manage your consent.",
    "leg_cook.meta": "Last updated: 20 May 2026",
    "leg_cook.s1.h2": "1. What are cookies?",
    "leg_cook.s1.p1": "A cookie is a small text file that a website stores in the user's browser when they visit it. It allows information about the visit to be remembered and the experience to be improved. This policy describes the cookies used by <a href=\"https://vantia.digital\">vantia.digital</a>, in accordance with Article 22.2 of the LSSI-CE and the guidelines of the AEPD.",
    "leg_cook.s2.h2": "2. Types of cookies we use",
    "leg_cook.s2.h3a": "Necessary cookies (always active)",
    "leg_cook.s2.p1": "These are essential for the site to function. They do not require consent.",
    "leg_cook.th_nombre": "Name",
    "leg_cook.th_titular": "Provider",
    "leg_cook.th_finalidad": "Purpose",
    "leg_cook.th_duracion": "Duration",
    "leg_cook.s2.td1c": "Store the user's consent preferences.",
    "leg_cook.s2.td1d": "12 months",
    "leg_cook.s2.td2c": "Security, bot mitigation and CDN performance.",
    "leg_cook.s2.td2d": "Session / 30 days",
    "leg_cook.s2.h3b": "Analytical cookies (prior consent required)",
    "leg_cook.s2.p2": "They help us understand how visitors interact with the site by collecting information in an aggregated and pseudonymised form. <strong>They are only activated if you accept.</strong>",
    "leg_cook.s2.td3c": "Distinguish users in a pseudonymised manner.",
    "leg_cook.s2.td3d": "2 years",
    "leg_cook.s2.td4c": "Persist the session state for GA4.",
    "leg_cook.s2.td4d": "2 years",
    "leg_cook.s2.p3": "We configure Google Analytics with <strong>anonymised IP</strong>, without Google Signals and without data sharing for advertising personalisation.",
    "leg_cook.s2.h3c": "Cloudflare Web Analytics cookies",
    "leg_cook.s2.p4": "We also use <strong>Cloudflare Web Analytics</strong>, a solution that <strong>does not install any cookies in your browser</strong> and does not perform fingerprinting. It therefore does not require consent under Art. 22.2 LSSI.",
    "leg_cook.s3.h2": "3. Consent management",
    "leg_cook.s3.p1": "When you access the site for the first time, a banner is displayed allowing you to accept, reject or configure cookies by category. You can change your choice at any time using the button below:",
    "leg_cook.s3.btn": "Change my cookie preferences",
    "leg_cook.s4.h2": "4. How to disable cookies from your browser",
    "leg_cook.s4.p1": "In addition to the site's preference panel, you can block or delete cookies from your browser settings:",
    "leg_cook.s4.p2": "Please note that disabling some cookies may affect the functioning of the site.",
    "leg_cook.s5.h2": "5. International transfers",
    "leg_cook.s5.p1": "The providers Google and Cloudflare may transfer data to the United States. Such transfers are covered by the Standard Contractual Clauses (SCCs) approved by the European Commission and, in the case of Google, also by the EU-U.S. Data Privacy Framework.",
    "leg_cook.s6.h2": "6. Further information",
    "leg_cook.s6.p1": "For further information on the general processing of your data, please consult our <a href=\"/privacidad\">Privacy Policy</a>. For any queries, write to us at <a href=\"mailto:admin@vantia.digital\">admin@vantia.digital</a>.",
    "leg_aviso.meta_desc": "Legal Notice of Vantia Digital. Mandatory information pursuant to the LSSI-CE.",
    "leg_aviso.title": "Legal Notice · Vantia Digital",
    "leg_aviso.eyebrow": "Legal document",
    "leg_aviso.h1": "Legal <em>Notice</em>.",
    "leg_aviso.subtitle": "Mandatory information pursuant to Law 34/2002 on Information Society Services.",
    "leg_aviso.meta": "Last updated: 20 May 2026",
    "leg_aviso.s1.h2": "1. Identifying details of the owner",
    "leg_aviso.s1.p1": "In compliance with Article 10 of Law 34/2002, of 11 July, on Information Society Services and Electronic Commerce (LSSI-CE), users are informed of the identifying details of the website owner:",
    "leg_aviso.s1.li1": "<strong>Name / Company:</strong> [TO BE COMPLETED — Full name / Company name]",
    "leg_aviso.s1.li2": "<strong>Tax ID (NIF):</strong> [TO BE COMPLETED]",
    "leg_aviso.s1.li3": "<strong>Address:</strong> [TO BE COMPLETED — Full registered address], Barcelona, Spain",
    "leg_aviso.s1.li4": "<strong>Email:</strong> <a href=\"mailto:admin@vantia.digital\">admin@vantia.digital</a>",
    "leg_aviso.s1.li5": "<strong>Phone:</strong> +34 644 923 374",
    "leg_aviso.s1.li6": "<strong>Website:</strong> <a href=\"https://vantia.digital\">https://vantia.digital</a>",
    "leg_aviso.s2.h2": "2. Purpose",
    "leg_aviso.s2.p1": "This legal notice governs the use of the website <a href=\"https://vantia.digital\">vantia.digital</a> (hereinafter, \"the Site\"), owned by Vantia Digital. Browsing the Site constitutes the status of user and implies full acceptance of the terms set out herein.",
    "leg_aviso.s3.h2": "3. Services provided",
    "leg_aviso.s3.p1": "The Site provides information about Vantia Digital's professional services in the areas of web development, technical SEO, GEO (Generative Engine Optimization) and paid advertising campaign management (Paid Media).",
    "leg_aviso.s4.h2": "4. Terms of use",
    "leg_aviso.s4.p1": "The user undertakes to make appropriate use of the contents and services of the Site and not to use them to:",
    "leg_aviso.s4.li1": "Engage in unlawful, illegal activities or activities contrary to good faith and public order.",
    "leg_aviso.s4.li2": "Disseminate content of a racist, xenophobic, illegal nature or content that violates human rights.",
    "leg_aviso.s4.li3": "Cause damage to the physical and logical systems of the Site owner or third parties, introduce computer viruses or any other system capable of causing damage.",
    "leg_aviso.s4.li4": "Attempt to access, and where applicable use, other users' email accounts and to modify or tamper with their messages.",
    "leg_aviso.s5.h2": "5. Intellectual and industrial property",
    "leg_aviso.s5.p1": "All content on the Site (texts, photographs, graphics, images, icons, source code, trademarks, logos, trade names and other distinctive signs) is the exclusive property of the owner or of third parties with whom the corresponding agreements exist. Any reproduction, distribution, public communication, transformation or any other form of exploitation, in whole or in part, without the prior written authorisation of the owner is strictly prohibited.",
    "leg_aviso.s6.h2": "6. Third-party links",
    "leg_aviso.s6.p1": "The Site may contain links to third-party websites. The owner accepts no responsibility for the content, accuracy or truthfulness of the linked sites or for the services or opinions offered therein.",
    "leg_aviso.s7.h2": "7. Limitation of liability",
    "leg_aviso.s7.p1": "The owner shall not be liable, in any event, for damages of any nature that may arise, by way of example: errors or omissions in the content, unavailability of the portal, or the transmission of viruses or malicious programmes in the content, despite having adopted all necessary technological measures to prevent this.",
    "leg_aviso.s8.h2": "8. Amendments",
    "leg_aviso.s8.p1": "The owner reserves the right to make, without prior notice, such amendments as it deems appropriate to the Site, being able to change, remove or add both the contents and services provided through it and the way in which they are presented or located.",
    "leg_aviso.s9.h2": "9. Applicable law and jurisdiction",
    "leg_aviso.s9.p1": "The relationship between the owner and the user shall be governed by current Spanish law. For the resolution of any dispute, the parties submit to the Courts and Tribunals of the owner's domicile, expressly waiving any other jurisdiction that may apply to them.",
    "leg_aviso.s10.h2": "10. Data protection",
    "leg_aviso.s10.p1": "The processing of personal data is governed by our <a href=\"/privacidad\">Privacy Policy</a> and our <a href=\"/cookies\">Cookie Policy</a>."
  });

  // ==== I18N:PAGE-CHUNKS:END ====

  // ====================================================================
  // MOTOR
  // ====================================================================
  function getStoredLang() {
    try {
      const s = localStorage.getItem(STORAGE_KEY);
      if (s && SUPPORTED.indexOf(s) !== -1) return s;
    } catch (_) { /* noop */ }
    return DEFAULT_LANG;
  }

  function storeLang(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (_) { /* noop */ }
  }

  const ATTR_MAP = [
    ['data-i18n-content', 'content'],
    ['data-i18n-placeholder', 'placeholder'],
    ['data-i18n-aria-label', 'aria-label'],
    ['data-i18n-title', 'title'],
  ];

  function applyTo(root, lang) {
    // innerHTML
    root.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (el.__i18nEs === undefined) el.__i18nEs = el.innerHTML;
      if (lang === 'en') {
        const v = DICT.en[key];
        el.innerHTML = (v !== undefined) ? v : el.__i18nEs;
      } else {
        el.innerHTML = el.__i18nEs;
      }
    });
    // atributos
    ATTR_MAP.forEach((pair) => {
      const dataAttr = pair[0], target = pair[1];
      root.querySelectorAll('[' + dataAttr + ']').forEach((el) => {
        const key = el.getAttribute(dataAttr);
        const store = '__i18nEs_' + target;
        if (el[store] === undefined) el[store] = el.getAttribute(target) || '';
        if (lang === 'en') {
          const v = DICT.en[key];
          el.setAttribute(target, (v !== undefined) ? v : el[store]);
        } else {
          el.setAttribute(target, el[store]);
        }
      });
    });
  }

  function updateToggles(lang) {
    document.querySelectorAll('[data-lang-set]').forEach((btn) => {
      const active = btn.getAttribute('data-lang-set') === lang;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  let current = DEFAULT_LANG;

  function setLang(lang, opts) {
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT_LANG;
    current = lang;
    try { document.documentElement.setAttribute('lang', lang); } catch (_) {}
    applyTo(document, lang);
    updateToggles(lang);
    if (!opts || opts.persist !== false) storeLang(lang);
  }

  function reapply() {
    applyTo(document, current);
    updateToggles(current);
  }

  // Toggle (delegación — funciona con el header inline)
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-lang-set]');
    if (!btn) return;
    e.preventDefault();
    const lang = btn.getAttribute('data-lang-set');
    if (lang !== current) setLang(lang);
  });

  function init() {
    setLang(getStoredLang(), { persist: false });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Footer / cookie-banner / modales / whatsapp se inyectan async vía fetch.
  document.addEventListener('components:loaded', reapply);

  // API pública (modal.js la usa para el idioma del email de presupuesto)
  window.VantiaI18n = {
    set: setLang,
    get: () => current,
    t: (key) => (current === 'en' && DICT.en[key] !== undefined) ? DICT.en[key] : null,
    reapply: reapply,
  };
})();
