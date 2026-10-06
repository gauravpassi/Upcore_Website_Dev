"""/results: every client result and testimonial in one place (2026-10-06 site consolidation).
Client names are withheld by default; results are as reported from our engagements.
Run from the repo root: python tools/v4-build/build_results.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
from v4parts import TESTIMONIALS, QUOTE_LINKS
import segment_copy as S

ENG = [S.P_APP, S.P_SAAS, S.P_DENTAL_ENG, S.P_BRIEF]
OPS = [S.P_RETAIL, S.P_RE, S.P_COMPLIANCE, S.P_WEALTH, S.P_DENTAL]
SEG = {id(S.P_APP): 'tech-software', id(S.P_SAAS): 'tech-software', id(S.P_DENTAL_ENG): 'tech-software', id(S.P_BRIEF): 'tech-software',
       id(S.P_RETAIL): 'ecommerce-retail', id(S.P_RE): 'operations-heavy', id(S.P_COMPLIANCE): 'operations-heavy',
       id(S.P_WEALTH): 'professional-services', id(S.P_DENTAL): 'operations-heavy'}
SEG_NAME = {'tech-software': 'Tech &amp; Software', 'ecommerce-retail': 'Ecommerce &amp; Retail', 'operations-heavy': 'Operations-heavy', 'professional-services': 'Professional services'}


def rows(items):
    out = ''
    for p in items:
        n, who, desc = p
        k = SEG[id(p)]
        out += (f'<li class="r-row" data-reveal><b class="r-n" data-count>{n}</b><span class="r-who">{who}</span>'
                f'<p class="r-d">{desc}</p><a class="r-seg" href="{C.URL[k]}">{SEG_NAME[k]} <span aria-hidden="true">&rarr;</span></a></li>')
    return f'<ol class="r-list">{out}</ol>'


quotes = ''.join(f'<figure class="r-q" data-reveal><blockquote><p>&ldquo;{q}&rdquo;</p></blockquote><figcaption><span>{w}</span>'
                 + (f' <a href="{u}" target="_blank" rel="noopener">{s}<span class="sr"> (opens in a new tab)</span></a>' if s else '') + '</figcaption></figure>'
                 for q, w, s, u in TESTIMONIALS['eng'] + TESTIMONIALS['ops'])

body = f'''<section class="h-hero h-hero--page" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<nav class="crumb" aria-label="Breadcrumb" data-reveal><ol><li><a href="{C.URL["home"]}">Home</a></li><li aria-current="page">Results</li></ol></nav>
<p class="h-eyebrow" data-reveal>Results</p>
<h1 id="hero-h" class="t-display" data-split>AI in production, <span class="hl">not in a slide deck.</span></h1>
<p class="t-lead" data-reveal style="--d:3">Engineering and automation work running for clients in the US, UK, South Africa, Australia and India. Client names are withheld; ask us for a reference call.</p>
</div></section>
<section class="h-sec h-sec--tight" aria-labelledby="eng-h"><div class="wrap">
<h2 id="eng-h" class="h-h3 r-h">AI-native engineering &amp; delivery</h2>{rows(ENG)}</div></section>
<section class="h-sec h-sec--tight" aria-labelledby="ops-h"><div class="wrap">
<h2 id="ops-h" class="h-h3 r-h">Business process automation</h2>{rows(OPS)}
<p class="fine">Results are as reported from our engagements. Where a figure is approximate it is marked with ~ or &asymp;.</p></div></section>
<section class="band h-sec" aria-labelledby="q-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
<p class="h-eyebrow">In their words</p><h2 id="q-h" class="h-h2" data-reveal>What clients say.</h2>
<div class="r-quotes">{quotes}</div>{QUOTE_LINKS}</div></section>
<section class="h-sec h-cta-light" aria-labelledby="cta-h"><div class="wrap">
<h2 id="cta-h" class="h-h2" data-reveal>Want results like these on your team?</h2>
<p class="h-lead" data-reveal style="--d:1">Book a 45-minute discovery call with Gaurav or Saswata. You&rsquo;ll get a written plan, whether or not we work together.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("results_cta")}</div></div></section>'''

ld = C.graph('results', [], crumb='Results')
print('results', C.write('results.html', 'results', 'Client Results: AI Engineering &amp; Automation | Upcore',
      'Anonymised results from AI-native engineering and automation work in production: 60%+ fewer support tickets, &asymp;$210K a year of tooling replaced, a 4.9&#9733; app.',
      body, active='results', ld=ld, group='results', spine=False, main_cls='is-calm', annc_kind=C.ANNC_ENG))
