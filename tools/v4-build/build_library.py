"""The content library (2026-10-07): the 15 insights articles, 10 learn guides, the original financial-services
comparison, the privacy policy and the terms, rendered in the calm article layout from JSON files in
tools/v4-build/content/ (one per page: title, meta, hero, sections as HTML, FAQ, related reading).
Those JSON files are now the source of truth for these pages; edit them, then re-run this script.
They were imported once from the old hand-built pages, with their components mapped to .lx-* classes
(cards, tables, steps, checklists, stats) and .ar-call callouts; links to retired pages were rewritten.
Run from the repo root: python tools/v4-build/build_library.py"""
import os, sys, re, json, glob, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import article as A

CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content')
KIND = {'guide': 'Guide', 'comparison': 'Comparison', 'framework': 'Framework', 'playbook': 'Industry playbook', 'legal': 'Legal'}
GROUP = {'guide': 'guide', 'comparison': 'comparison', 'framework': 'insights', 'playbook': 'insights', 'legal': 'legal'}


def plain(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def related_block(items):
    rows = ''.join(f'<li><a href="{h}"><span class="hb-k">{t or "Read next"}</span><span class="hb-t"><b>{H.escape(ti)}</b>'
                   f'{f"<span class=hb-d>{H.escape(d)}</span>" if d else ""}</span><i aria-hidden="true">{C.ARROW}</i></a></li>' for h, t, ti, d in items)
    return f'''<section class="h-sec h-sec--tight lx-rel" aria-labelledby="rel-h"><div class="wrap">
<div class="hb-bar"><h2 id="rel-h" class="h-h3">Keep reading</h2><a class="link" href="{C.URL["insights"]}">All insights</a></div>
<ul class="hb-list lx-rel-list">{rows}</ul></div></section>'''


def build(path):
    d = json.load(open(path, encoding='utf-8'))
    key = 'lib:' + d['path']
    C.FINAL_URL[key] = d['path']
    C.PREVIEW_URL[key] = '/preview/' + d['path'].strip('/').replace('/', '-')
    C.URL[key] = d['path']
    legal = d['kind'] == 'legal'
    name = plain(d['h1'])
    crumb = name if len(name) <= 48 else name[:46].rsplit(' ', 1)[0] + '…'
    trail = [(C.URL['home'], 'Home')] + ([] if legal else [(C.URL['insights'], 'Insights')]) + [(None, H.escape(crumb))]
    eb = H.escape(d['eyebrow']) if d['eyebrow'] and not legal else ''
    eyebrow = eb if KIND[d['kind']].lower() in eb.lower() else ((eb + ' &middot; ') if eb else '') + KIND[d['kind']]
    meta_line = f'<span>{H.escape(d["date_label"])}</span>' if legal and d['date_label'] else (f'<span>Published {H.escape(d["date_label"])}</span>' if d.get('date_label') else '')
    stats = ''
    if d['stats']:
        stats = '<dl class="lx-stats lx-stats--hero" data-reveal style="--d:4">' + ''.join(f'<div><dt>{H.escape(n)}</dt><dd>{H.escape(l)}</dd></div>' for n, l in d['stats']) + '</dl>'
    aside = ''
    if d.get('aside'):
        aside = f'<div class="ar-aside-cta"><p class="h-col">Put it into practice</p><a class="link" href="{d["aside"][1]}">{d["aside"][0]}</a></div>'
    sections = [(i, h, b) for i, h, b in d['sections']]
    hero, body, mins = A.page(trail, eyebrow, d['h1'], d['lead'], sections, meta_line=meta_line, aside=aside, extra=stats, show_time=not legal)
    parts = [hero, body]
    if d['faq']:
        parts.append(K.faq(d['faq'], 'Common questions.'))
    if d['related']:
        parts.append(related_block(d['related']))
    if not legal:
        parts.append(K.final('Want this applied <span class="hl">to your business?</span>',
                             'Book a 45-minute discovery call. We&rsquo;ll look at where you are with AI and send a written plan, whether or not we work together.'))
    if legal:
        ld = C.graph(key, [{'@type': 'WebPage', 'name': name, 'url': C.SITE + d['path'], 'about': {'@id': C.ORG_ID}, 'dateModified': '2026-10-07'}], crumb=name)
    else:
        ld = C.graph(key, A.ld_article(key, name, plain(d['meta']), mins, d['faq'] or None, published=d.get('published') or None), crumb=name)
    noindex = 'noindex' in (d.get('robots') or '')
    return C.write(d['file'], key, H.escape(d['title'], quote=False), H.escape(d['meta']), '\n'.join(parts),
                   active='' if legal else 'insights', ld=ld, group=GROUP[d['kind']], spine=False, main_cls='is-calm lx-page', noindex=noindex)


for f in sorted(glob.glob(os.path.join(CONTENT, '*.json'))):
    print(os.path.basename(f)[:-5].replace('__', '/'), build(f))
