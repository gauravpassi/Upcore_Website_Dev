"""/results: brief client case studies (challenge, what we built, result) + testimonials.
Rebuilt 2026-10-07 from the case studies in cases.py (source: the Sierra Living Concepts pre-read).
Client names are withheld unless cases.SHOW_NAMES is switched on; results are as reported from our
engagements. Filter chips: the "Results: case filters" module in js/upcore-v5.js.
Run from the repo root: python tools/v4-build/build_results.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
from v4parts import TESTIMONIALS, QUOTE_LINKS
from cases import CASES, SHOW_NAMES, who

SEG_NAME = {'tech-software': 'Tech &amp; Software', 'ecommerce-retail': 'Ecommerce &amp; Retail', 'operations-heavy': 'Operations-heavy businesses', 'professional-services': 'Professional services'}
TAG = {'automation': 'Automation', 'engineering': 'Engineering'}
SERVICE = {'automation': ('bpa', 'Business Process Automation'), 'engineering': ('aine', 'AI-Native Engineering')}


def case(i, c):
    word = not any(ch.isdigit() for ch in c['n']) or len(c['n']) > 7
    tags = ''.join(f'<span class="h-tag">{TAG[t]}</span>' for t in c['tags'])
    svc = SERVICE[c['tags'][0]]
    return f'''<article class="cs" id="{c["key"]}" data-tags="{" ".join(c["tags"])}" data-reveal aria-labelledby="{c["key"]}-h">
<div class="cs-k"><div class="cs-tags">{tags}</div><b class="cs-n{" is-word" if word else ""}" data-count>{c["n"]}</b><span class="cs-what">{c["what"]}</span><h3 class="cs-who" id="{c["key"]}-h">{who(c)}</h3></div>
<dl class="cs-body"><div><dt>Challenge</dt><dd>{c["challenge"]}</dd></div><div><dt>What we built</dt><dd>{c["built"]}</dd></div><div class="cs-res"><dt>Result</dt><dd>{c["result"]}</dd></div></dl>
<p class="cs-links"><a class="link" href="{C.URL[svc[0]]}">{svc[1]}</a><a class="link" href="{C.URL[c["seg"]]}">{SEG_NAME[c["seg"]]}</a></p>
</article>'''


n_auto = sum('automation' in c['tags'] for c in CASES)
n_eng = sum('engineering' in c['tags'] for c in CASES)
chips = (f'<button type="button" class="hb-chip is-on" data-filter="all" aria-pressed="true">All <span>{len(CASES)}</span></button>'
         f'<button type="button" class="hb-chip" data-filter="automation" aria-pressed="false">Automation <span>{n_auto}</span></button>'
         f'<button type="button" class="hb-chip" data-filter="engineering" aria-pressed="false">Engineering <span>{n_eng}</span></button>')
names = 'Client context is from public sources; results are as reported from our engagements.' if SHOW_NAMES else 'Client names are withheld; ask us for a reference call.'
hero = K.hero_page([(C.URL['home'], 'Home'), (None, 'Results')], 'Results &amp; case studies',
                   'AI in production, <span class="hl">not in a slide deck.</span>',
                   f'Ten engagements in engineering and automation, for clients in the US, UK, South Africa, Australia, Mauritius and India. Each in brief: the challenge, what we built and the result. {names}')
cases = f'''<section class="h-sec cs-sec" aria-labelledby="cs-h"><div class="wrap" data-cases>
<div class="hb-bar"><h2 id="cs-h" class="h-h3">Case studies</h2><div class="hb-chips" role="group" aria-label="Filter case studies">{chips}</div></div>
<div class="cs-list">{"".join(case(i, c) for i, c in enumerate(CASES))}</div>
<p class="fine cs-fine">Results are as reported from our engagements. Where a figure is approximate it is marked with ~ or &asymp;. Detailed case studies and references are available on request.</p>
</div></section>'''

quotes = ''.join(f'<figure class="r-q" data-reveal><blockquote><p>&ldquo;{q}&rdquo;</p></blockquote><figcaption><span>{w}</span>'
                 + (f' <a href="{u}" target="_blank" rel="noopener">{s}<span class="sr"> (opens in a new tab)</span></a>' if s else '') + '</figcaption></figure>'
                 for q, w, s, u in TESTIMONIALS['eng'] + TESTIMONIALS['ops'])
words = f'''<section class="band h-sec" aria-labelledby="q-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
<p class="h-eyebrow">In their words</p><h2 id="q-h" class="h-h2" data-reveal>What clients say.</h2>
<div class="r-quotes">{quotes}</div>{QUOTE_LINKS}</div></section>'''
final = K.final('Want results like these <span class="hl">on your team?</span>',
                'Book a 45-minute discovery call with Gaurav or Saswata. You&rsquo;ll get a written plan, whether or not we work together.', lines=False)

ld = C.graph('results', [{'@type': 'ItemList', 'name': 'Upcore case studies', 'numberOfItems': len(CASES),
                          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': C.SITE + C.FINAL_URL['results'] + '#' + c['key'],
                                               'name': (c['name'] if SHOW_NAMES else c['anon'].replace('&middot;', '·').replace('&amp;', '&'))} for i, c in enumerate(CASES)]}], crumb='Results')
print('results', C.write('results.html', 'results', 'Results &amp; Case Studies: AI Engineering and Automation in Production | Upcore',
      'Ten brief case studies: 60%+ fewer support tickets, &asymp;$210K a year of tooling replaced, first installment in ~3 weeks instead of 6&ndash;10, a 4.9&#9733; app and more.',
      '\n'.join([hero, cases, words, final]), active='results', ld=ld, group='results', spine=False, main_cls='is-calm', annc_kind=C.ANNC_ENG))
