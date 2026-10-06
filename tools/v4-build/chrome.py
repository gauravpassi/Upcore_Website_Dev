"""Shared V4.1 chrome: head, announcement, nav, footer, sticky CTA, scripts, JSON-LD.
LIVE=False builds noindex previews under /preview/; LIVE=True switches to final URLs, canonical,
index/follow and the production analytics tags (rollout only)."""
import json, os
import tools as TL

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))  # repo root
SITE = 'https://www.upcoretech.com'
V = 6          # cache-buster for css/js/upcore-v4 + v4-analytics
CHAT_V = 17    # chat-widget.js (bump sitewide when it changes)
CTA_V = 3      # cta-tracking.js (bump sitewide when it changes)
LIVE = True
OG_IMAGE = SITE + '/images/og/upcore-v4.png'

PREVIEW_URL = {
    'home': '/preview/home-v4', 'aine': '/preview/ai-native-engineering',
    'tech-software': '/preview/who-we-help-tech-software', 'ecommerce-retail': '/preview/who-we-help-ecommerce-retail',
    'operations-heavy': '/preview/who-we-help-operations-heavy', 'professional-services': '/preview/who-we-help-professional-services',
}
FINAL_URL = {
    'home': '/', 'aine': '/ai-native-engineering',
    'tech-software': '/who-we-help/tech-software', 'ecommerce-retail': '/who-we-help/ecommerce-retail',
    'operations-heavy': '/who-we-help/operations-heavy', 'professional-services': '/who-we-help/professional-services',
}
URL = dict(FINAL_URL if LIVE else PREVIEW_URL)
URL.update({'gov': '/ai-engineering-governance', 'bpa': '/platform', 'fao': '/ai-adoption-strategy'})

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON = {
    'aine': '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    'gov': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'bpa': '<path d="M4 7h10M4 12h16M4 17h7"/><circle cx="18" cy="7" r="2"/><circle cx="14" cy="17" r="2"/>',
    'fao': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'tech-software': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'ecommerce-retail': '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/>',
    'operations-heavy': '<path d="M4 20V10l5-3v13M9 20V5l6-2v17M15 20V9l5 2v9"/>',
    'professional-services': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
}
SOLUTIONS = [('aine', 'AI-Native Engineering', 'Governed AI delivery, spec to production', True),
             ('gov', 'AI Governance', 'Spend visibility, data controls, audit trails', False),
             ('bpa', 'Business Process Automation', 'Agents that run repetitive operations work', False),
             ('fao', 'Fractional AI Officer', 'An embedded AI lead on retainer', False)]
SEGMENTS = [('tech-software', 'Tech &amp; Software', 'For CTOs and CIOs shipping with AI'),
            ('ecommerce-retail', 'Ecommerce &amp; Retail', 'Support, returns, catalog, ad spend'),
            ('operations-heavy', 'Operations-Heavy Businesses', 'Follow-ups, documents, collections'),
            ('professional-services', 'Professional Services', 'Accounting, law, wealth, staffing')]


def svg(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICON[k]}</svg>'


def btn(section, cls='btn', label='Book a Discovery Call', pulse=False, magnetic=True):
    return (f'<a class="{cls}{" btn-pulse" if pulse else ""}" href="#book-governance"{" data-magnetic" if magnetic else ""} data-gtm-cta="book-a-discovery-call" '
            f'data-gtm-cta-type="primary" data-gtm-cta-section="{section}">{label} <span class="btn-ico">{ARROW}</span></a>')


CHEV = '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><path d="M2.5 4.5 6 8l3.5-3.5"/></svg>'


def nav(active=''):
    cur = lambda k: ' aria-current="page"' if k == active else ''
    sol = ''.join(f'<a href="{URL[k]}"{cur(k)}><span class="di">{svg(k)}</span><span><b>{t}{"<span class=tag>Flagship</span>" if f else ""}</b><span>{d}</span></span></a>' for k, t, d, f in SOLUTIONS)
    seg = ''.join(f'<a href="{URL[k]}"{cur(k)}><span class="di">{svg(k)}</span><span><b>{t}</b><span>{d}</span></span></a>' for k, t, d in SEGMENTS)
    return f'''<header class="nav">
  <div class="nav-in">
    <a class="nav-logo" href="{URL['home']}" aria-label="Upcore home"><img src="/images/upcore-logo-ink.png" alt="Upcore" width="102" height="26" /></a>
    <nav aria-label="Primary"><ul class="nav-menu" role="list">
      <li><a class="flag" href="{URL['aine']}"{cur('aine')}>AI-Native Engineering</a></li>
      <li><button type="button" aria-expanded="false" aria-controls="drop-solutions">Solutions {CHEV}</button><div class="drop" id="drop-solutions">{sol}</div></li>
      <li><button type="button" aria-expanded="false" aria-controls="drop-who">Who we help {CHEV}</button><div class="drop" id="drop-who">{seg}</div></li>
      <li><a href="{URL['aine']}#engagement">How we engage</a></li>
      <li><a href="/about">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      {btn('nav', cls='btn btn--sm')}
      <button class="nav-burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>'''


def footer():
    sol = ''.join(f'<li><a href="{URL[k]}">{t}</a></li>' for k, t, d, f in SOLUTIONS)
    seg = ''.join(f'<li><a href="{URL[k]}">{t}</a></li>' for k, t, d in SEGMENTS)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand"><img src="/images/upcore-logo-ops-toolkit.png" alt="Upcore" width="102" height="26" loading="lazy" /><p>AI-native engineering, governed from spec to production, and the automation that runs around it.</p></div>
      <nav class="foot-nav" aria-label="Footer">
        <div><h2 class="foot-h">Solutions</h2><ul>{sol}</ul></div>
        <div><h2 class="foot-h">Who we help</h2><ul>{seg}</ul></div>
        <div><h2 class="foot-h">Company</h2><ul><li><a href="/about">About</a></li><li><a href="/insights">Insights</a></li><li><a href="/contact">Contact</a></li><li><a href="/security">Security</a></li></ul></div>
        <div><h2 class="foot-h">Legal</h2><ul><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><button type="button" class="foot-link" data-consent-open>Cookie settings</button></li></ul></div>
      </nav>
    </div>
    <div class="foot-word" aria-hidden="true">upcore</div>
    <div class="foot-bot"><span>&copy; 2026 Upcore Technologies</span><ul class="foot-certs" aria-label="Certifications"><li>ISO 27001</li><li>ISO 9001</li><li>CMMI Level 3</li><li>Nasscom member</li></ul></div>
  </div>
</footer>'''


ANNC_ENG = ('Now booking AI-Native Engineering pilots: one team, one service, a real backlog.', 'Pilots now booking', 'How a pilot works', 'aine#engagement')
ANNC_OPS = ('Now booking one-workflow pilots. Our standard: a first agent live within 30 days of design sign-off.', 'One-workflow pilots now booking', 'How it works', 'self#engagement')


def annc(kind, self_key):
    full, short, link, target = kind
    href = (URL['aine'] + '#engagement') if target.startswith('aine') else (URL[self_key] + '#engagement')
    return f'<div class="annc"><span class="annc-full">{full}</span><span class="annc-short">{short}.</span> <a href="{href}">{link} <span aria-hidden="true">&rarr;</span></a></div>'


# V4 pages load every tag through GTM (container import: tools/gtm-container-upcore-v4.json).
# Consent Mode v2 defaults run first: denied in the UK/EEA/Switzerland until the visitor accepts,
# granted elsewhere; a stored choice is re-applied. gtag stays a local function so the site
# scripts push to dataLayer (window.upcGTM), and {tagging:'gtm'} is the flag every GTM trigger
# checks, so legacy pages that still load gtag.js directly are never double counted.
TRACKING = '''<script>window.dataLayer=window.dataLayer||[];window.upcGTM=true;(function(){function g(){dataLayer.push(arguments)}g('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',region:[__EEA__],wait_for_update:500});g('consent','default',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});g('set','ads_data_redaction',true);try{var c=localStorage.getItem('upc_consent');if(c==='granted'||c==='denied')g('consent','update',{ad_storage:c,ad_user_data:c,ad_personalization:c,analytics_storage:c})}catch(e){}})();dataLayer.push({tagging:'gtm',content_group:'__GROUP__'});</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-MH5PB32L');</script>
<!-- End Google Tag Manager -->'''.replace('__EEA__', "'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'")

ORG_ID = SITE + '/#organization'
ORG = {'@type': 'Organization', '@id': ORG_ID, 'name': 'Upcore Technologies', 'url': SITE, 'logo': SITE + '/upcore-logo.png',
       'description': 'Upcore Technologies installs governed, AI-native software delivery pipelines for engineering teams and builds AI agents that automate business processes, with AI governance and a Fractional AI Officer service.',
       'knowsAbout': ['AI-native engineering', 'AI software delivery governance', 'AI governance', 'Business process automation', 'AI agents'],
       'sameAs': ['https://www.linkedin.com/company/upcoretech', 'https://clutch.co/profile/upcore-technologies', 'https://www.designrush.com/agency/profile/upcore-technologies']}
AREA = ['US', 'GB', 'AE', 'AU', 'NZ', 'ZA', 'IN']


def graph(key, nodes, crumb=None):
    url = SITE + FINAL_URL[key]
    g = [ORG] + nodes
    if crumb:
        g.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url}]})
    return {'@context': 'https://schema.org', '@graph': g}


def write(fname, key, title, meta, body, active='', ld=None, og=None, group='page', annc_kind=ANNC_ENG):
    canon = SITE + FINAL_URL[key]
    ld_tag = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' if ld else ''
    robots = '<meta name="robots" content="index, follow, max-image-preview:large" />\n<link rel="canonical" href="' + canon + '" />' if LIVE else '<meta name="robots" content="noindex, nofollow" />'
    track = TRACKING.replace('__GROUP__', group) if LIVE else ''
    noscript = '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MH5PB32L" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n' if LIVE else ''
    body_html = body  # sprite must be generated after body is built
    html = f'''<!DOCTYPE html>
<html lang="en" class="no-js v4">
<head>
<meta charset="UTF-8" />
<script>document.documentElement.classList.replace('no-js','js');setTimeout(function(){{if(!window.__v4)document.documentElement.classList.add('reveal-all')}},4000)</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
{track}
<title>{title}</title>
<meta name="description" content="{meta}" />
{robots}
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Upcore Technologies" />
<meta property="og:url" content="{canon}" />
<meta property="og:title" content="{og or title}" />
<meta property="og:description" content="{meta}" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Upcore: AI-native engineering, governed from spec to production." />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{OG_IMAGE}" />
<meta name="theme-color" content="#FFFFFF" />
<link rel="icon" href="/favicon.ico" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/upcore-v4.css?v={V}" />
{ld_tag}</head>
<body>
{noscript}<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
{annc(annc_kind, key)}
{nav(active)}
<main id="main">
{body_html}
</main>
{footer()}
<div class="mcta">{btn('mobile_sticky', magnetic=False)}</div>
{TL.sprite()}
<script src="/js/upcore-v4.js?v={V}" defer></script>
<script src="/js/v4-analytics.js?v={V}" defer></script>
<script src="/cta-tracking.js?v={CTA_V}" defer></script>
<script src="/chat-widget.js?v={CHAT_V}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, fname) if LIVE else os.path.join(ROOT, 'preview', PREVIEW_URL[key].rsplit('/', 1)[1] + '.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    return len(html)
