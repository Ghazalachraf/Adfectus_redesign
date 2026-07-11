# -*- coding: utf-8 -*-
"""Générateur du site statique Adfectus — python build.py régénère les pages HTML."""
import os
import re

SITE = "https://www.adfectus-agency.com"
OUT = os.path.dirname(os.path.abspath(__file__))

# Version d'asset pour le cache-busting : change dès que style.css est modifié,
# ce qui force le navigateur à recharger la feuille de style (fini le cache figé).
try:
    ASSET_VERSION = int(os.path.getmtime(os.path.join(OUT, "assets", "css", "style.css")))
except OSError:
    ASSET_VERSION = 1

# Polices : locales (originales du site), voir assets/fonts + @font-face dans style.css
FONTS = ""

# Vidéos d'arrière-plan d'origine, compressées en local (dossier video/)
BG_VIDEOS = {
    "index.html": "bg_full_v.mp4",
    "consulting.html": "bg_full_v.mp4",
    "communication.html": "bg_img_5082.mp4",
    "production.html": "bg_664e94d021c44cbcaafd20e6b95dda31.mp4",
    "ntic.html": "bg_img_9932.mp4",
    "formation.html": "bg_c9651.mp4",
    "filiales.html": "bg_bubbles-2023-11-27-05-33-55-utc.mp4",
    "contact.html": "bg_7767537-uhd_4096_2160_25fps.mp4",
    "carriere.html": "bg_481a6240.mp4",
    "projets.html": "bg_5813069-uhd_4096_2160_25fps.mp4",
}

def bg_video(page):
    v = BG_VIDEOS.get(page)
    if not v:
        return ""
    return (f'<video class="bg-video" autoplay muted loop playsinline '
            f'src="video/{v}" aria-hidden="true"></video>\n<div class="bg-overlay"></div>\n')

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Adfectus",
  "legalName": "ADFECTUS sarl",
  "slogan": "We Made Tomorrow",
  "url": "%s",
  "logo": "%s/assets/img/t_adfectus-logo-06-400.png",
  "email": "Contact@adfectus-agency.com",
  "telephone": "+212535567583",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Hay Riad, Immeuble Bahji N35",
    "addressLocality": "Ifrane",
    "postalCode": "53000",
    "addressCountry": "MA"
  },
  "sameAs": [],
  "subOrganization": [
    {"@type": "Organization", "name": "Ad Retail"},
    {"@type": "Organization", "name": "Ad Facilities"},
    {"@type": "Organization", "name": "Ad Invest"}
  ]
}
</script>""" % (SITE, SITE)

def head(title, desc, page):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{page}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{page}">
<meta property="og:image" content="{SITE}/assets/img/t_adfectus-logo-06-400.png">
<meta property="og:locale" content="fr_FR">
<link rel="icon" type="image/png" href="assets/img/6_logo-adfectus-elements_plan-de-travail-1-184.png">
{FONTS}
<link rel="stylesheet" href="assets/css/style.css?v={ASSET_VERSION}">
{SCHEMA}
</head>
<body>
"""

HEADER = """<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="Adfectus — accueil">
      <img src="assets/img/8_adfectus-logo-05-368.png" alt="Adfectus — We Made Tomorrow">
    </a>
    <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>
    <ul class="nav-links">
      <li><a href="index.html">Accueil</a></li>
      <li class="has-sub"><a href="consulting.html">Services</a>
        <ul class="submenu">
          <li><a href="consulting.html">Consulting</a></li>
          <li><a href="communication.html">Communication &amp; Marketing</a></li>
          <li><a href="production.html">Production</a></li>
          <li><a href="ntic.html">NTIC</a></li>
          <li><a href="formation.html">Formation</a></li>
        </ul>
      </li>
      <li><a href="projets.html">Nos Projets</a></li>
      <li><a href="filiales.html">Filiales</a></li>
      <li><a href="carriere.html">Carrière</a></li>
      <li><a class="btn btn-primary" href="contact.html">Contact</a></li>
    </ul>
  </div>
</header>
"""

FOOTER = """<div class="footer-reveal">
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/img/t_adfectus-logo-06-400.png" alt="Adfectus">
        <p>Osez l'innovation, créez demain avec ambition.<br>We Made Tomorrow.</p>
      </div>
      <div>
        <h4>Navigation</h4>
        <ul>
          <li><a href="index.html">Accueil</a></li>
          <li><a href="projets.html">Nos Projets</a></li>
          <li><a href="filiales.html">Filiales</a></li>
          <li><a href="carriere.html">Carrière</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="consulting.html">Consulting</a></li>
          <li><a href="communication.html">Communication &amp; Marketing</a></li>
          <li><a href="production.html">Production</a></li>
          <li><a href="ntic.html">NTIC</a></li>
          <li><a href="formation.html">Formation</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><p>ADFECTUS sarl : Hay Riad, Immeuble Bahji N35 – Ifrane 53000 Maroc</p></li>
          <li><a href="mailto:Contact@adfectus-agency.com">Contact@adfectus-agency.com</a></li>
          <li><a href="tel:+212535567583">05.35.56.75.83</a></li>
          <li><a href="tel:+212661442647">06.61.44.26.47</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© Adfectus sarl — Tous droits réservés</span>
      <span>We Made Tomorrow</span>
    </div>
    <div class="footer-mega" aria-hidden="true">
      <span class="footer-mega-line">adfectus<span class="dot-red">.</span></span>
      <span class="footer-mega-sub">we made tomorrow</span>
    </div>
  </div>
</footer>
</div>
<script src="assets/js/main.js"></script>
</body>
</html>
"""

CTA = """<section class="cta-band">
  <div class="container reveal">
    <p class="eyebrow" style="justify-content:center">Keep in Touch</p>
    <h2>Osez l'innovation, créez demain avec ambition.</h2>
    <a class="btn btn-primary" href="contact.html">Contactez-Nous</a>
  </div>
</section>
"""

def page_hero(eyebrow, title, lead=""):
    lead_html = f'<p class="lead reveal">{lead}</p>' if lead else ""
    return f"""<section class="page-hero">
  <div class="container">
    <p class="eyebrow reveal">{eyebrow}</p>
    <h1 class="reveal">{title}</h1>
    {lead_html}
  </div>
</section>
"""

def domain_cards(heading, cards):
    items = ""
    for i, (t, bullets) in enumerate(cards, 1):
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        items += f'<article class="card reveal"><span class="num">0{i}</span><h3>{t}</h3><ul>{lis}</ul></article>\n'
    return f"""<section class="section">
  <div class="container">
    <div class="section-head reveal"><h2>{heading}</h2></div>
    <div class="grid grid-2">
{items}    </div>
  </div>
</section>
"""

pages = {}

# ---------------------------------------------------------------- ACCUEIL
pages["index.html"] = {
    "title": "Adfectus — Agence Consulting, Communication & Production | We Made Tomorrow",
    "desc": "Adfectus sarl, agence de consulting, communication, marketing, production audiovisuelle, NTIC et formation au Maroc. Osez l'innovation, créez demain avec ambition.",
    "body": """<section class="hero hero-center">
  <div class="container">
    <h1 class="reveal visible">Osez <span class="subtitle-gendy accent">l'innovation,</span><br>créez demain avec ambition</h1>
    <p class="lead hero-tagline reveal visible">Consulting · Communication &amp; Marketing · Production · NTIC · Formation</p>
    <div class="hero-actions reveal visible">
      <a class="btn btn-primary" href="contact.html">Contactez-Nous</a>
    </div>
    <div class="hero-badges reveal visible">
      <a href="consulting.html" title="Consulting"><img src="assets/img/0_logo-adfectus-elements-04-194.png" alt="ad Consulting"></a>
      <a href="ntic.html" title="NTIC"><img src="assets/img/t_logo-adfectus-elements-03-186.png" alt="ad it"></a>
      <a href="communication.html" title="Communication &amp; Marketing"><img src="assets/img/e_logo-adfectus-elements-02-188.png" alt="ad Com's Marketing"></a>
      <a href="production.html" title="Production"><img src="assets/img/6_logo-adfectus-elements_plan-de-travail-1-184.png" alt="ad Prod"></a>
    </div>
    <div class="audio-player reveal visible" data-src="audio/ads-audio-spot-adfectus-short.mp3">
      <button class="audio-toggle" aria-label="Écouter le spot Adfectus"></button>
      <div class="audio-track"><div class="audio-bar"></div></div>
      <span class="audio-time">0:00</span>
    </div>
  </div>
</section>


<section class="section section-dark">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Nos Services</p>
      <h2>Une approche 360°, de la stratégie à la production</h2>
    </div>
    <div class="grid grid-3">
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/0_logo-adfectus-elements-04-194.png" alt="" aria-hidden="true"></span>
          <h3>Consulting</h3>
        </div>
        <p>Le pôle consulting d'Adfectus propose un accompagnement stratégique, opérationnel et créatif dans les domaines du marketing, de la communication, du management organisationnel et de l'innovation numérique (NTIC).</p>
        <a class="card-link" href="consulting.html">En savoir plus</a>
      </article>
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/e_logo-adfectus-elements-02-188.png" alt="" aria-hidden="true"></span>
          <h3>Communication &amp; Marketing</h3>
        </div>
        <p>Nous vous offrons un accompagnement d'exception dans l'art du marketing et de la communication, avec une attention minutieuse portée à chaque détail.</p>
        <a class="card-link" href="communication.html">En savoir plus</a>
      </article>
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/6_logo-adfectus-elements_plan-de-travail-1-184.png" alt="" aria-hidden="true"></span>
          <h3>Production</h3>
        </div>
        <p>Le pôle audiovisuel d'Adfectus combine créativité, expertise terrain et technologie de pointe pour produire des contenus professionnels qui inspirent, mobilisent et valorisent vos actions.</p>
        <a class="card-link" href="production.html">En savoir plus</a>
      </article>
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/t_logo-adfectus-elements-03-186.png" alt="" aria-hidden="true"></span>
          <h3>NTIC</h3>
        </div>
        <p>Chez Adfectus, nous croyons que l'innovation digitale est la clé pour construire dès aujourd'hui les solutions de demain.</p>
        <a class="card-link" href="ntic.html">En savoir plus</a>
      </article>
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/h_logo-adfectus-elements_plan-de-travail-1-436.png" alt="" aria-hidden="true"></span>
          <h3>Formation</h3>
        </div>
        <p>Former des esprits, bâtir des projets, faire naître l'avenir. Nous révélons des potentiels, catalysons des idées et transformons des intentions en actions durables.</p>
        <a class="card-link" href="formation.html">En savoir plus</a>
      </article>
      <article class="card svc reveal">
        <div class="svc-head">
          <span class="card-mark"><img src="assets/img/c_logo-adfectus-elements-02-780.png" alt="" aria-hidden="true"></span>
          <h3>Nos Projets</h3>
        </div>
        <p>Films institutionnels, capsules, spots publicitaires, couvertures d'événements : découvrez une sélection de nos réalisations audiovisuelles.</p>
        <a class="card-link" href="projets.html">Voir la galerie</a>
      </article>
    </div>
  </div>
</section>

<section class="partners logo-wall">
  <div class="container">
    <p class="eyebrow reveal" style="justify-content:center">Ils nous ont fait confiance</p>
    <div class="logo-row reveal">
      <div class="logo-item"><img src="assets/img/partners/myserrena.png" alt="Myserrena" loading="lazy"></div>
      <div class="logo-item"><img src="assets/img/partners/al-akhawayn.png" alt="Al Akhawayn University" loading="lazy"></div>
      <div class="logo-item"><img src="assets/img/partners/terroir-pni.png" alt="Produits de Terroir — Parc National d'Ifrane" loading="lazy"></div>
      <div class="logo-item logo-text"><span>Mobadara</span></div>
      <div class="logo-item logo-text"><span>Acadimia</span></div>
    </div>
  </div>
</section>

<section class="section section-alt section-dark">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Filiales</p>
      <h2>Adfectus élargit ses horizons avec trois nouvelles filiales stratégiques</h2>
      <p>Dans le cadre de sa vision innovante et de son expansion continue, Adfectus s'apprête à lancer trois filiales complémentaires qui renforceront son positionnement sur le marché.</p>
    </div>
    <div class="grid grid-3">
      <article class="card reveal">
        <h3><span class="ad-script">ad</span> Retail<span class="dot-red">.</span></h3>
        <p>Dédiée au développement de concepts commerciaux innovants, à l'accompagnement des marques, ainsi qu'aux activités d'import-export.</p>
      </article>
      <article class="card reveal">
        <h3><span class="ad-script">ad</span> Facilities<span class="dot-red">.</span></h3>
        <p>Spécialisée dans la gestion des installations, des espaces professionnels, et des services de support aux entreprises.</p>
      </article>
      <article class="card reveal">
        <h3><span class="ad-script">ad</span> Invest<span class="dot-red">.</span></h3>
        <p>Pensée comme un catalyseur d'opportunités : investissement, accompagnement de startups et projets à fort impact.</p>
      </article>
    </div>
    <div class="filiales-foot reveal">
      <a class="btn btn-ghost" href="filiales.html">Découvrir les filiales &amp; l'édito</a>
      <span class="script-note" aria-hidden="true">we made tomorrow</span>
    </div>
  </div>
</section>

<section class="cta-band cta-script">
  <div class="container reveal">
    <h2>Osez l'innovation, créez demain avec ambition.</h2>
    <a class="btn btn-primary" href="contact.html">Contactez-Nous</a>
  </div>
</section>
""",
}

# ---------------------------------------------------------------- CONSULTING
pages["consulting.html"] = {
    "title": "Consulting — Adfectus | Accompagnement stratégique 360°",
    "desc": "Le pôle consulting d'Adfectus : marketing stratégique, communication 360°, management & leadership, NTIC et transformation digitale.",
    "body": page_hero("Nos Services", "Consulting",
        "Le pôle consulting d'Adfectus propose un accompagnement stratégique, opérationnel et créatif dans les domaines du marketing, de la communication, du management organisationnel et de l'innovation numérique (NTIC). Notre approche se distingue par sa dimension 360°, sa créativité méthodique, et son alignement avec les meilleures pratiques internationales, combinant expertise terrain et référentiels certifiants.")
    + domain_cards("Nos domaines de consulting", [
        ("Marketing Stratégique &amp; Digital", [
            "Études de marché, positionnement et branding",
            "Plans marketing intégrés (B2C / B2B / territorial)",
            "Transformation digitale des canaux marketing (réseaux sociaux, e-mailing, automation)"]),
        ("Communication 360° &amp; Influence", [
            "Stratégies de communication institutionnelle et de contenu",
            "Campagnes créatives et multimédia (print, vidéo, réseaux sociaux)",
            "Relations presse, communication de crise, visibilité impact"]),
        ("Management &amp; Leadership", [
            "Organisation agile et gestion par projet",
            "Développement du leadership, gouvernance participative",
            "Accompagnement au changement et dynamiques collectives"]),
        ("NTIC &amp; Transformation Digitale", [
            "Diagnostic numérique et feuille de route IT",
            "Déploiement d'outils collaboratifs, ERP, CRM, intranet",
            "Intégration d'outils de formation en ligne, plateformes LMS, gamification"]),
    ]) + CTA,
}

# ---------------------------------------------------------------- COMMUNICATION
pages["communication.html"] = {
    "title": "Communication & Marketing — Adfectus",
    "desc": "Identité visuelle, packaging, supports imprimés, stratégies publicitaires et campagnes digitales : l'accompagnement marketing d'exception d'Adfectus.",
    "body": page_hero("Nos Services", "Communication &amp; Marketing",
        "Nous vous offrons un accompagnement d'exception dans l'art du marketing et de la communication, avec une attention minutieuse portée à chaque détail.")
    + """<section class="section">
  <div class="container">
    <div class="prose reveal">
      <p>Nos créations d'emballages se distinguent par leur originalité et leur ingéniosité, conçues pour éblouir et captiver dès le premier regard. De plus, l'identité visuelle que nous façonnons pour votre marque incarne à la fois son essence et sa singularité, grâce à des logos raffinés et des chartes graphiques harmonieuses qui marquent les esprits.</p>
      <p>Par ailleurs, nous transformons vos idées en supports imprimés d'une rare élégance, qu'il s'agisse de brochures sophistiquées ou de dépliants audacieux, sublimant ainsi chaque message que vous souhaitez véhiculer. Mais ce n'est pas tout : notre expertise se prolonge également dans l'élaboration de stratégies publicitaires sur mesure, pensées pour optimiser votre impact après une analyse rigoureuse de votre audience et de vos concurrents.</p>
      <p>De plus, nous mettons en place des campagnes digitales innovantes sur l'ensemble des plateformes, maximisant votre présence en ligne et renforçant votre visibilité à chaque étape du parcours client. Enfin, nos campagnes publicitaires, qu'elles soient traditionnelles ou digitales, se distinguent par leur créativité vibrante et leur force narrative, captant l'attention de votre audience et inscrivant durablement votre marque dans leur mémoire.</p>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><h2>Les créatifs, toutes formes</h2></div>
    <ol class="roadmap">
      <li class="roadmap-step reveal">
        <span class="rm-node">01</span>
        <div class="rm-body">
          <h3>Études</h3>
          <p>Analyse du marché, de l'audience et de la concurrence pour cadrer chaque prise de parole.</p>
        </div>
      </li>
      <li class="roadmap-step reveal">
        <span class="rm-node">02</span>
        <div class="rm-body">
          <h3>Stratégie Marketing &amp; Communication</h3>
          <p>Le plan directeur : positionnement, messages clés et plan média.</p>
        </div>
      </li>
      <li class="roadmap-step reveal">
        <span class="rm-node">03</span>
        <div class="rm-body">
          <h3>Book institutionnel</h3>
          <p>L'entreprise racontée : histoire, valeurs et savoir-faire réunis en un objet de référence.</p>
        </div>
      </li>
      <li class="roadmap-step reveal">
        <span class="rm-node">04</span>
        <div class="rm-body">
          <h3>Catalogue</h3>
          <p>Vos produits mis en scène et structurés, prêts à convaincre.</p>
        </div>
      </li>
      <li class="roadmap-step reveal">
        <span class="rm-node">05</span>
        <div class="rm-body">
          <h3>Lookbook</h3>
          <p>La collection sublimée, image par image, pour installer l'univers de la marque.</p>
        </div>
      </li>
      <li class="roadmap-step reveal">
        <span class="rm-node">06</span>
        <div class="rm-body">
          <h3>Packaging</h3>
          <p>L'emballage qui capte le regard dès le premier coup d'œil.</p>
        </div>
      </li>
    </ol>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- PRODUCTION
pages["production.html"] = {
    "title": "Production audiovisuelle — Adfectus | Contenus créatifs à fort impact",
    "desc": "Vidéos, photos et expériences immersives sur mesure : le pôle audiovisuel d'Adfectus, technologies immersives et storytelling.",
    "body": page_hero("Contenus créatifs à fort impact — Technologies immersives &amp; storytelling", "Production",
        "Le pôle audiovisuel d'Adfectus combine créativité, expertise terrain et technologie de pointe pour produire des contenus professionnels qui inspirent, mobilisent et valorisent vos actions. Nous créons des vidéos, des photos et des expériences immersives sur mesure, pour renforcer votre image, votre message, et votre impact.")
    + domain_cards("Nos domaines de Production", [
        ("Production avec technologies de pointe", [
            "Caméras HD/4K, drones, GoPro, stabilisateurs, micros HF",
            "Éclairage professionnel dernière génération (LED, lumière continue, softbox…)",
            "Prises de vue multi-caméras et captation dynamique",
            "Tournage 360° immersif avec casques ou export web",
            "Création de visites virtuelles interactives (locaux, lieux historiques, expositions…)"]),
        ("Production vidéo &amp; storytelling", [
            "Films institutionnels et reportages de terrain",
            "Capsules événementielles et teasers",
            "Vidéos pédagogiques et formats courts pour réseaux sociaux",
            "Vidéos témoignages et capsules d'impact"]),
        ("Photographie professionnelle", [
            "Reportages sur le vif ou shootings en studio",
            "Portraits institutionnels ou ambiance terrain",
            "Photographie de produits et branding visuel"]),
        ("Création &amp; post-production", [
            "Écriture de scénarios et storyboards",
            "Direction artistique, voice-over, habillage graphique",
            "Motion design, animation typographique et effets spéciaux",
            "Montage optimisé pour tous formats (YouTube, Instagram, TikTok, TV…)"]),
    ])
    + """<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><h2>L'art de raconter des histoires captivantes</h2></div>
    <div class="prose reveal">
      <p>Une production audiovisuelle de pointe incarne la fusion parfaite entre créativité et innovation, donnant vie à vos idées les plus audacieuses. Passionnés par l'art de raconter des histoires captivantes, nous transformons les médias visuels et sonores en véritables œuvres qui touchent et émeuvent.</p>
      <p>Notre équipe est composée de professionnels chevronnés, parmi lesquels des talents créatifs, réalisateurs, producteurs, scénaristes et techniciens expérimentés, tous animés par une même ambition : produire des œuvres audiovisuelles de qualité exceptionnelle, capables de susciter des émotions profondes et de marquer durablement votre public.</p>
      <p>Que vous soyez une entreprise désireuse de promouvoir vos produits ou services, un artiste cherchant à créer un clip vidéo mémorable, ou une organisation voulant transmettre un message puissant, nous sommes à vos côtés pour vous aider à atteindre vos objectifs. Quelle que soit la nature ou la complexité de votre projet, nous vous garantissons un service sur-mesure, parfaitement adapté à vos besoins et à votre budget.</p>
      <p>De la conception initiale à la post-production, chaque étape de notre collaboration est guidée par l'excellence et l'attention au détail, afin que votre vision prenne vie de la manière la plus éclatante. Chez Adfectus, nous avons hâte de collaborer avec vous et de vous accompagner tout au long de votre projet audiovisuel. Faites-nous confiance pour réaliser vos idées avec brio et distinction.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.5rem">
      <article class="card reveal"><h3>Production Sport publicitaire</h3></article>
      <article class="card reveal"><h3>Capsules</h3></article>
      <article class="card reveal"><h3>Interviews</h3></article>
      <article class="card reveal"><h3>Film institutionnel</h3></article>
      <article class="card reveal"><h3>Couverture évents</h3></article>
      <article class="card reveal"><h3>Shooting</h3></article>
    </div>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- NTIC
pages["ntic.html"] = {
    "title": "NTIC & Transformation digitale — Adfectus",
    "desc": "Plateformes web et mobiles, transformation digitale, formation numérique : Adfectus digitalise l'impact. We Made Tomorrow.",
    "body": page_hero("Nos Services", "NTIC",
        "Chez Adfectus, nous croyons que l'innovation digitale est la clé pour construire dès aujourd'hui les solutions de demain.")
    + """<section class="section">
  <div class="container">
    <div class="prose reveal">
      <p>À travers notre service NTIC, nous accompagnons les institutions, associations et jeunes entrepreneurs dans leur transition numérique intelligente, en créant des outils technologiques sur mesure, accessibles, durables et ancrés dans les réalités sociales du terrain.</p>
      <p>Qu'il s'agisse de plateformes web, d'applications mobiles, de systèmes collaboratifs ou de formations digitales, nous concevons des solutions qui transforment le potentiel local en puissance digitale.</p>
      <p>Avec une approche agile, créative et centrée sur l'humain, nous digitalisons l'impact avec une vision claire : <strong>We Made Tomorrow</strong>.</p>
    </div>
  </div>
</section>
"""
    + domain_cards("Nos domaines NTIC", [
        ("Développement de solutions sur mesure", [
            "Création de plateformes web et mobiles (formations, e-commerce, e-learning, gestion…)",
            "Applications métiers pour associations, incubateurs, coopératives",
            "Systèmes de pointage QR code, bases de données, tableaux de bord interactifs"]),
        ("Transformation digitale", [
            "Audit numérique, diagnostic de maturité digitale",
            "Accompagnement à la mise en place de solutions digitales",
            "Digitalisation des processus internes (RH, gestion de projet, CRM…)"]),
        ("Formation et montée en compétences", [
            "Modules de formation certifiants",
            "Ateliers « coding for beginners » – pensée algorithmique et logique informatique",
            "Sensibilisation à l'IA, au web3, à la protection des données"]),
        ("Communication digitale &amp; outils collaboratifs", [
            "Mise en place d'écosystèmes collaboratifs",
            "Outils de communication intégrée : newsletters, CRM, automation, analytics",
            "Stratégies de visibilité numérique pour les projets d'impact (SEO, ADS, réseaux)"]),
    ])
    + """<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><h2>Sur le terrain</h2></div>
    <div class="photo-mosaic">
      <img class="reveal" src="assets/img/a_img_9681-600.jpg" alt="Atelier NTIC Adfectus" loading="lazy">
      <img class="reveal" src="assets/img/t_img_9684-450.jpg" alt="Formation numérique" loading="lazy">
      <img class="reveal" src="assets/img/e_img_3465-600.jpg" alt="Session de travail" loading="lazy">
      <img class="reveal" src="assets/img/l_161c60e1-e252-4be8-9bae-2f8646b2c29e-600.jpg" alt="Accompagnement digital" loading="lazy">
      <img class="reveal" src="assets/img/6_img_3182-600.jpg" alt="Atelier coding" loading="lazy">
      <img class="reveal" src="assets/img/p_d6650477-eea1-43d0-9e73-a7a547973a7d-600.jpg" alt="Équipe Adfectus en action" loading="lazy">
    </div>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- FORMATION
pages["formation.html"] = {
    "title": "Formation & Accompagnement — Adfectus | We Made Tomorrow",
    "desc": "Former des esprits, bâtir des projets, faire naître l'avenir : l'approche pédagogique complète et innovante d'Adfectus.",
    "body": page_hero("We Made Tomorrow", "Former des esprits, bâtir des projets, faire naître l'avenir",
        "Chez Adfectus, nous ne nous contentons pas de transmettre des compétences : nous révélons des potentiels, catalysons des idées et transformons des intentions en actions durables.")
    + """<section class="section">
  <div class="container">
    <div class="prose reveal">
      <p>À travers notre service de formation et d'accompagnement, nous proposons une approche complète et innovante qui allie montée en compétences, stimulation de l'esprit entrepreneurial et soutien stratégique à toutes les étapes du projet — de l'idéation à la consolidation post-création.</p>
      <p>Parce que l'avenir appartient à ceux qui le construisent, nous plaçons l'humain, l'innovation et l'impact au cœur de chaque parcours.</p>
      <p><strong>Former aujourd'hui ceux qui feront demain, c'est notre promesse. We Made Tomorrow.</strong></p>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><h2>Notre approche pédagogique</h2></div>
    <div class="grid grid-2">
      <article class="card reveal"><span class="num">01</span><h3>Méthodologies actives</h3><p>Learning by doing, pédagogie inversée, co-construction</p></article>
      <article class="card reveal"><span class="num">02</span><h3>Expériences immersives</h3><p>Serious games, simulation d'entreprise, hackathons</p></article>
      <article class="card reveal"><span class="num">03</span><h3>Techniques certifiées</h3><p>Google Ventures (Design Sprint), Startup Lab, Design Thinking</p></article>
      <article class="card reveal"><span class="num">04</span><h3>Digitalisation de la formation</h3><p>E-learning, blended learning, plateformes interactives</p></article>
      <article class="card reveal"><span class="num">05</span><h3>Adaptation aux profils variés</h3><p>Jeunes sans diplôme, entrepreneurs, porteurs d'idées, cadres</p></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal"><h2>En images</h2></div>
    <div class="photo-mosaic">
      <img class="reveal" src="assets/img/l_methodes-01-664.png" alt="Nos méthodes pédagogiques" loading="lazy">
      <img class="reveal" src="assets/img/l_image-collee-406.png" alt="Session de formation Adfectus" loading="lazy">
      <img class="reveal" src="assets/img/8_image-collee-442.png" alt="Atelier de formation" loading="lazy">
      <img class="reveal" src="assets/img/p_image-collee-316.png" alt="Accompagnement de projets" loading="lazy">
    </div>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- FILIALES
pages["filiales.html"] = {
    "title": "Filiales — Ad Retail, Ad Facilities, Ad Invest | Adfectus",
    "desc": "Adfectus élargit ses horizons avec le lancement de trois nouvelles filiales stratégiques : Ad Retail, Ad Facilities et Ad Invest.",
    "body": page_hero("Filiales", "Adfectus élargit ses horizons avec le lancement de trois nouvelles filiales stratégiques",
        "Dans le cadre de sa vision innovante et de son expansion continue, Adfectus s'apprête à lancer trois filiales complémentaires qui renforceront son positionnement sur le marché et répondront à des besoins spécifiques dans des secteurs clés.")
    + """<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <article class="card reveal">
        <span class="num">01</span><h3><span class="ad-script">ad</span> Retail<span class="dot-red">.</span></h3>
        <p>Dédiée au développement de concepts commerciaux innovants, à l'accompagnement des marques, ainsi qu'aux activités d'import-export, en valorisant les produits à fort potentiel local et international. Elle transforme l'expérience client à travers le digital et les tendances de consommation émergentes.</p>
      </article>
      <article class="card reveal">
        <span class="num">02</span><h3><span class="ad-script">ad</span> Facilities<span class="dot-red">.</span></h3>
        <p>Spécialisée dans la gestion des installations, des espaces professionnels, et des services de support aux entreprises avec une approche durable, technologique et orientée qualité de vie au travail.</p>
      </article>
      <article class="card reveal">
        <span class="num">03</span><h3><span class="ad-script">ad</span> Invest<span class="dot-red">.</span></h3>
        <p>Pensée comme un catalyseur d'opportunités, cette filiale portera les activités liées à l'investissement, à l'accompagnement de startups, et aux projets à fort impact dans les domaines de l'innovation, de l'économie verte et de l'entrepreneuriat social.</p>
      </article>
    </div>
    <p class="lead reveal" style="margin-top:2.5rem">Avec cette nouvelle dynamique, Adfectus réaffirme son engagement : <strong>« We Made Tomorrow »</strong> — en construisant dès aujourd'hui les solutions de demain.</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal" style="text-align:center;margin-inline:auto">
      <p class="eyebrow" style="justify-content:center">Édito</p>
      <h2>Le mot du Directeur Général</h2>
    </div>
    <div class="agenda-wrap reveal">
      <div class="agenda">
        <figure class="agenda-photo">
          <img src="assets/img/a_5n4a0970-412.jpg" alt="Mohammed Khalil Ghazal, Directeur Général d'Adfectus">
          <figcaption>Mohammed Khalil Ghazal</figcaption>
        </figure>
        <p class="agenda-date">Édito — Adfectus, We Made Tomorrow</p>
        <p>Depuis sa création, Adfectus est née d'une conviction forte : celle que l'innovation, lorsqu'elle est ancrée dans la réalité des besoins humains, peut transformer durablement notre manière de créer, d'apprendre, de consommer et de bâtir le futur.</p>
        <p>Notre mission a toujours été claire : accompagner les individus, les entreprises et les territoires vers une transformation durable, inclusive et tournée vers l'avenir. À travers nos pôles de formation, de consulting stratégique, de développement entrepreneurial et d'innovation sociale, nous avons su bâtir un écosystème agile, où les idées prennent forme et les projets deviennent concrets.</p>
        <p>Aujourd'hui, Adfectus franchit une nouvelle étape dans son développement. Forts de notre expertise multisectorielle et de notre ancrage sur le terrain, nous annonçons avec fierté la création de trois filiales spécialisées, conçues comme des extensions naturelles de notre savoir-faire :</p>
        <p><strong>Ad Retail</strong> : dédiée aux concepts commerciaux innovants, à l'accompagnement des marques locales et à l'activité d'import-export, pour connecter les talents et produits du Sud aux marchés mondiaux.</p>
        <p><strong>Ad Facilities</strong> : experte en gestion d'infrastructures, de services généraux et de qualité de vie au travail, dans une logique durable et efficiente.</p>
        <p><strong>Ad Invest</strong> : bras armé d'Adfectus pour l'investissement à impact, l'accompagnement de startups, et le soutien aux projets générateurs de valeur, notamment dans les secteurs du digital, de l'économie verte et de l'innovation sociale.</p>
        <p>Ce plan d'expansion s'inscrit dans une vision long terme. Nous ne cherchons pas simplement à croître : nous voulons bâtir un modèle économique porteur de sens, capable de créer de la valeur économique, sociale et environnementale.</p>
        <p>À tous nos partenaires, collaborateurs, bénéficiaires, clients et amis : merci de croire en cette aventure collective. Ensemble, We Made Tomorrow n'est pas seulement un slogan. C'est une promesse. Une responsabilité. Et un cap que nous continuerons à suivre avec engagement, audace et humanité.</p>
        <div class="agenda-signature">
          <img src="assets/img/4_signe_plan-de-travail-1-400.png" alt="Signature de Mohammed Khalil Ghazal">
          <p class="signature">Mohammed Khalil Ghazal<small>Directeur Général d'Adfectus</small></p>
        </div>
      </div>
    </div>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- PROJETS
VIDEOS = [
    ("adfectus-20ads-20officielle-20.mp4", "Adfectus — Film officiel"),
    ("ads-20ord-20.mp4", "ADS — Ord"),
    ("ads-20formation.mp4", "ADS — Formation"),
    ("ads-20fashion-20.mp4", "ADS — Fashion"),
    ("myserrena-20ads_1.mp4", "Myserrena — ADS"),
    ("jingle2024-20mobadara.mp4", "Jingle 2024 — Mobadara"),
    ("vid-20mobadara-20poadcast-201.mp4", "Mobadara — Podcast"),
    ("telerealite-20ep1-20vf.mp4", "Téléréalité — Épisode 1"),
    ("akhawayen-20commune-20vid2o-20.mp4", "Akhawayn — Commune"),
    ("315328882_3298060573784007_34085888068704038_n.mp4", "Capsule événementielle"),
    ("autisme-20vid-20bleu-20-20vf-20.mp4", "Spot — Journée de l'autisme"),
    ("ads-20ord-20-1.mp4", "ADS — Ord II"),
    ("showroom-20artisanat-20terroir.mp4", "Showroom — Artisanat & Terroir"),
    ("fairy-house-in-flowers-2023-11-27-05-02-25-utc.mp4", "Capsule créative"),
    ("acadimia-20ads-20vf-20.mp4", "Acadimia — ADS"),
    ("day3.mp4", "Couverture d'événement — Day 3"),
    ("audio-20spot-20video-20va-20adfectus.mp4", "Spot audio-vidéo — Adfectus"),
]
video_cards = "".join(
    f'''<figure class="video-card reveal" data-video="{SITE}/video/{f}" data-title="{t}" tabindex="0" role="button" aria-label="Lire : {t}">
  <div class="video-thumb">
    <img src="assets/img/posters/{f.rsplit('.', 1)[0]}.jpg" alt="{t}" loading="lazy">
    <span class="play-btn" aria-hidden="true"></span>
  </div>
  <figcaption>{t}</figcaption>
</figure>
''' for f, t in VIDEOS)

pages["projets.html"] = {
    "title": "Nos Projets — Réalisations audiovisuelles | Adfectus",
    "desc": "Films institutionnels, spots publicitaires, capsules, jingles et couvertures d'événements réalisés par Adfectus.",
    "body": page_hero("Portfolio", "Nos Projets",
        "Une sélection de nos réalisations audiovisuelles : films institutionnels, spots, capsules et couvertures d'événements.")
    + f"""<section class="section">
  <div class="container">
    <div class="video-grid">
{video_cards}    </div>
  </div>
</section>
""" + CTA,
}

# ---------------------------------------------------------------- CONTACT
pages["contact.html"] = {
    "title": "Contact — Adfectus | Ifrane, Maroc",
    "desc": "Contactez Adfectus sarl : Hay Riad, Immeuble Bahji N35 – Ifrane 53000 Maroc. Tél : 05.35.56.75.83 / 06.61.44.26.47.",
    "body": page_hero("Mail US", "Contactez-Nous",
        "Une idée, un projet, une question ? Écrivez-nous, nous serions ravis d'échanger avec vous.")
    + """<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items:start">
      <form class="form-grid reveal" action="https://formspree.io/f/VOTRE_ID_FORMSPREE" method="POST">
        <div>
          <label for="nom">Votre Nom complet :</label>
          <input id="nom" type="text" name="nom" required>
        </div>
        <div>
          <label for="email">Votre adresse mail :</label>
          <input id="email" type="email" name="email" required>
        </div>
        <div>
          <label for="tel">Votre numéro de téléphone :</label>
          <input id="tel" type="tel" name="telephone">
        </div>
        <div>
          <label for="objet">Objet :</label>
          <input id="objet" type="text" name="objet" required>
        </div>
        <div class="full">
          <label for="message">Message :</label>
          <textarea id="message" name="message" required></textarea>
        </div>
        <div class="full">
          <button class="btn btn-primary" type="submit">Envoyez</button>
        </div>
      </form>
      <div class="contact-info reveal">
        <div>
          <span class="label">Adresse</span><br>
          <span style="color:var(--text)">ADFECTUS sarl : Hay Riad, Immeuble Bahji N35 – Ifrane 53000 Maroc</span>
        </div>
        <div>
          <span class="label">Email</span><br>
          <a href="mailto:Contact@adfectus-agency.com">Contact@adfectus-agency.com</a>
        </div>
        <div>
          <span class="label">Téléphone</span><br>
          <a href="tel:+212535567583">05.35.56.75.83</a> — <a href="tel:+212661442647">06.61.44.26.47</a>
        </div>
      </div>
    </div>
  </div>
</section>
""",
}

# ---------------------------------------------------------------- CARRIERE
pages["carriere.html"] = {
    "title": "Carrière — Rejoignez l'équipe Adfectus",
    "desc": "L'un des meilleurs et des plus innovants endroits où travailler. Rejoignez l'équipe Adfectus à Ifrane, Maroc.",
    "body": page_hero("Join Our Team", "Carrière",
        "Les personnes qui travaillent ici sont uniques, motivées et authentiques. Elles se soucient profondément les unes des autres et de ce qu'elles accomplissent. On nous a dit que nous sommes l'un des meilleurs et des plus innovants endroits où travailler, et nous en sommes très fiers.")
    + """<section class="cta-band">
  <div class="container reveal">
    <h2>Cela ressemble à l'endroit où vous aimeriez être ?<br>Nous serions ravis de vous rencontrer.</h2>
    <a class="btn btn-primary" href="mailto:Contact@adfectus-agency.com?subject=Candidature">Contact US</a>
  </div>
</section>
""",
}

# ---------------------------------------------------------------- GÉNÉRATION
# Signature typographique façon studio : un mot par grand titre passe en Gendy.
# Appliqué aux <h1>/<h2> à la génération, sans modifier le contenu textuel.
EMPH_WORDS = [
    "l'innovation", "360°", "filiales", "consulting", "créatifs", "Production",
    "histoires", "NTIC", "terrain", "pédagogique", "images",
    "Directeur Général", "Projets", "Contactez-Nous", "rencontrer", "l'avenir",
]

def emphasize(m):
    inner = m.group(2)
    if "emph" in inner or "subtitle-gendy" in inner:
        return m.group(0)
    for w in EMPH_WORDS:
        if w in inner:
            inner = inner.replace(w, f'<em class="emph">{w}</em>', 1)
            break
    return m.group(1) + inner + m.group(3)

for fname, p in pages.items():
    # La vidéo de fond couvre toute la page (élément fixe derrière le contenu)
    body = re.sub(r'(<h[12][^>]*>)(.*?)(</h[12]>)', emphasize, p["body"], flags=re.S)
    html = (head(p["title"], p["desc"], "" if fname == "index.html" else fname)
            + bg_video(fname) + HEADER + "<main>\n" + body + "</main>\n" + FOOTER)
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("OK", fname)

# sitemap.xml + robots.txt
urls = "".join(f"<url><loc>{SITE}/{'' if f=='index.html' else f}</loc></url>\n" for f in pages)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nDisallow:\n\nSitemap: {SITE}/sitemap.xml\n")
print("OK sitemap.xml + robots.txt")
