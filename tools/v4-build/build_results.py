"""/results: client case studies + testimonials (rebuilt 2026-10-07).
Each case is its own full-width chapter (alternating bands, zig-zag layout): client name and context,
headline figure with its own animated result visual, then challenge -> what we built -> result on a
drawn thread. An index of client names at the top doubles as the filter (Automation / Engineering).
Data: cases.py. Styles .cx-*, .cv-*; script "Results: case index + filters" in js/upcore-v5.js.
Run from the repo root: python tools/v4-build/build_results.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
from v4parts import TESTIMONIALS, QUOTE_LINKS
from cases import CASES, SHOW_NAMES, who

SEG_NAME = {'tech-software': 'Tech &amp; Software', 'ecommerce-retail': 'Ecommerce &amp; Retail', 'operations-heavy': 'Operations-heavy businesses', 'professional-services': 'Professional services'}
TAG = {'automation': 'Automation', 'engineering': 'Engineering'}
SERVICE = {'automation': ('bpa', 'Business Process Automation'), 'engineering': ('aine', 'AI-Native Engineering')}


# ------------------------------------------------------------------ result visuals (decorative; every fact is also in the text)
def viz(v):
    k = v['kind']
    if k == 'bars':
        rows = ''.join(f'<div class="cv-row{" is-after" if i else ""}" style="--i:{i}"><span class="cv-l">{l}</span><span class="cv-bar"><i style="--w:{w}%"></i></span><span class="cv-v">{t}</span></div>'
                       for i, (l, t, w) in enumerate(v['rows']))
        return f'<div class="cv cv--bars">{rows}</div>'
    if k == 'ring':
        ticks = ''.join(f'<line x1="60" y1="8" x2="60" y2="{15 if h % 6 else 19}" transform="rotate({h * 15} 60 60)" style="--i:{h}"/>' for h in range(24))
        chips = ''.join(f'<span style="--i:{i}">{x}</span>' for i, x in enumerate(v['items']))
        return f'<div class="cv cv--ring"><svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><circle cx="60" cy="60" r="52"/><g class="cv-ticks">{ticks}</g><line class="cv-hand" x1="60" y1="60" x2="60" y2="20"/><circle class="cv-hub" cx="60" cy="60" r="4"/></svg><div class="cv-chips">{chips}</div></div>'
    if k == 'tiles':
        tiles = ''.join(f'<i style="--i:{i}"></i>' for i in range(v['n']))
        wave = ''.join(f'<i style="--i:{i}"></i>' for i in range(18))
        return f'<div class="cv cv--tiles"><div class="cv-tiles">{tiles}</div><span class="cv-cap">{v["label"]}</span><div class="cv-wave">{wave}</div><span class="cv-cap">{v["voice"]}</span></div>'
    if k == 'converge':
        n = len(v['sources'])
        ys = [20 + i * (120 / (n - 1)) for i in range(n)]
        paths = ''.join(f'<path d="M96 {y:.0f} C 170 {y:.0f}, 170 80, 236 80" style="--i:{i}" pathLength="1"/>' for i, y in enumerate(ys))
        nodes = ''.join(f'<g style="--i:{i}"><circle cx="90" cy="{y:.0f}" r="5"/><text x="80" y="{y + 4:.0f}" text-anchor="end">{s}</text></g>' for i, (s, y) in enumerate(zip(v['sources'], ys)))
        return f'<div class="cv cv--converge"><svg viewBox="0 0 330 160" aria-hidden="true" focusable="false"><g class="cv-paths">{paths}</g>{nodes}<circle class="cv-core" cx="252" cy="80" r="16"/><circle class="cv-core-ring" cx="252" cy="80" r="24"/><text class="cv-tgt" x="252" y="122" text-anchor="middle">{v["target"]}</text></svg></div>'
    if k == 'engines':
        rows = ''.join(f'<div class="cv-eng" style="--i:{i}"><span class="cv-l">{x}</span><span class="cv-track"><i></i><i></i><i></i></span><em>Automated</em></div>' for i, x in enumerate(v['items']))
        return f'<div class="cv cv--engines">{rows}</div>'
    if k == 'flow':
        steps = ''.join(f'<li style="--i:{i}"><span></span>{s}</li>' for i, s in enumerate(v['steps']))
        return f'<div class="cv cv--flow"><ol>{steps}</ol><span class="cv-side">+ {v["side"]}</span></div>'
    if k == 'rating':
        rows = ''.join(f'<div class="cv-rate" style="--i:{i}"><span class="cv-l">{s}</span><span class="cv-stars" style="--r:{r / 5 * 100:.0f}%"><b>&#9733;&#9733;&#9733;&#9733;&#9733;</b><i>&#9733;&#9733;&#9733;&#9733;&#9733;</i></span><span class="cv-v"><b>{r}</b> &middot; {c}</span></div>' for i, (s, r, c) in enumerate(v['rows']))
        return f'<div class="cv cv--rating">{rows}</div>'
    return ''


def case(i, c):
    word = not any(ch.isdigit() for ch in c['n']) or len(c['n']) > 7
    tags = ''.join(f'<span>{TAG[t]}</span>' for t in c['tags']) + f'<span>{SEG_NAME[c["seg"]]}</span>'
    svc = SERVICE[c['tags'][0]]
    alt = i % 2 == 1
    return f'''<section class="cx{" cx--alt" if alt else ""}" id="{c["key"]}" data-no="{i + 1:02d}" data-tags="{" ".join(c["tags"])}" aria-labelledby="{c["key"]}-h"><div class="wrap">
<header class="cx-head" data-reveal><span class="cx-no"><b>{i + 1:02d}</b><span>Case {i + 1} of {len(CASES)}</span></span><div class="cx-tags">{tags}</div></header>
<div class="cx-grid">
<div class="cx-fig" data-reveal style="--d:1">
<h3 class="cx-name" id="{c["key"]}-h">{who(c)}</h3><p class="cx-meta">{c["meta"]}</p>
<div class="cx-num"><b class="{"is-word" if word else ""}" data-count>{c["n"]}</b><span>{c["what"]}</span></div>
{viz(c["viz"])}
</div>
<ol class="cx-story" data-reveal style="--d:2">
<li><span class="cx-k">Challenge</span><p>{c["challenge"]}</p></li>
<li><span class="cx-k">What we built</span><p>{c["built"]}</p></li>
<li class="is-res"><span class="cx-k">Result</span><p>{c["result"]}</p></li>
<li class="cx-links"><a class="link" href="{C.URL[svc[0]]}">{svc[1]}</a><a class="link" href="{C.URL[c["seg"]]}">{SEG_NAME[c["seg"]]}</a></li>
</ol>
</div></div></section>'''


n_auto = sum('automation' in c['tags'] for c in CASES)
n_eng = sum('engineering' in c['tags'] for c in CASES)
chips = (f'<button type="button" class="hb-chip is-on" data-filter="all" aria-pressed="true">All <span>{len(CASES)}</span></button>'
         f'<button type="button" class="hb-chip" data-filter="automation" aria-pressed="false">Automation <span>{n_auto}</span></button>'
         f'<button type="button" class="hb-chip" data-filter="engineering" aria-pressed="false">Engineering <span>{n_eng}</span></button>')
index = ''.join(f'<li data-tags="{" ".join(c["tags"])}"><a href="#{c["key"]}"><span class="cx-ix-n">{i + 1:02d}</span><b>{c["short"]}</b><em>{c["n"]}</em></a></li>' for i, c in enumerate(CASES))
names = 'Client names are withheld; ask us for a reference call.'
hero = K.hero_page([(C.URL['home'], 'Home'), (None, 'Results')], 'Results &amp; case studies',
                   'Real AI. <span class="hl">Real results.</span>',
                   f'Ten engagements in engineering and automation, for clients in the US, UK, South Africa, Australia, Mauritius and India. {names}')
idx = f'''<section class="h-sec h-sec--tight cx-index-sec" aria-labelledby="ix-h"><div class="wrap" data-cases>
<div class="hb-bar"><h2 id="ix-h" class="h-h3">Ten case studies</h2><div class="hb-chips" role="group" aria-label="Filter case studies">{chips}</div></div>
<ol class="cx-index">{index}</ol>
</div></section>'''
cases = '\n'.join(case(i, c) for i, c in enumerate(CASES))
fine = '<section class="cx-fine"><div class="wrap"><p class="fine">Results are as reported from our engagements. Where a figure is approximate it is marked with ~ or &asymp;. Detailed case studies and references are available on request.</p></div></section>'

quotes = ''.join(f'<figure class="cx-q" data-reveal style="--d:{i % 2}"><span class="cx-qm" aria-hidden="true">&ldquo;</span><blockquote><p>{q}</p></blockquote><figcaption><span>{w}</span>'
                 + (f' <a href="{u}" target="_blank" rel="noopener">{s}<span class="sr"> (opens in a new tab)</span></a>' if s else '') + '</figcaption></figure>'
                 for i, (q, w, s, u) in enumerate(TESTIMONIALS['eng'] + TESTIMONIALS['ops']))
words = f'''<section class="h-sec cx-words" aria-labelledby="q-h"><div class="wrap">
{K.eyebrow("In their words")}<h2 id="q-h" class="h-h2" data-reveal>What clients say.</h2>
<div class="cx-quotes">{quotes}</div>{QUOTE_LINKS}</div></section>'''
final = K.final('Want results <span class="hl">like these?</span>',
                'Book a 45-minute discovery call. You&rsquo;ll get a written plan, whether or not we work together.')

ld = C.graph('results', [{'@type': 'ItemList', 'name': 'Upcore case studies', 'numberOfItems': len(CASES),
                          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': C.SITE + C.FINAL_URL['results'] + '#' + c['key'],
                                               'name': c['name'].replace('&amp;', '&')} for i, c in enumerate(CASES)]}], crumb='Results')
print('results', C.write('results.html', 'results', 'Case Studies: AI Engineering &amp; Automation | Upcore',
      'Ten client case studies, from a national retailer and a US dental network to a UK wealth firm: the challenge, what we built and the result.',
      '\n'.join([hero, idx, cases, fine, words, final]), active='results', ld=ld, group='results', spine=False, main_cls='is-calm', annc_kind=C.ANNC_ENG))
