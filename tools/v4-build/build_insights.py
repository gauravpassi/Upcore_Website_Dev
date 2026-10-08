"""/insights (2026-10-07): the single hub for every guide, comparison, framework and industry playbook
(insights/*, learn/*, compare/*). Titles, descriptions and reading times are read from the pages at build
time, so re-run this after adding or renaming an article. Filter chips + search (JS module "Insights hub");
everything is visible without JS. The newsletter form keeps the previous endpoint and subject.
Run from the repo root (after the guide and comparison builders): python tools/v4-build/build_insights.py"""
import os, sys, re, glob, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K

FEATURED = ['learn/what-is-ai-native-engineering.html', 'compare/ai-native-engineering-vs-ai-coding-tools.html', 'compare/upcore-vs-building-in-house.html']
DISPLAY = {'learn/what-is-ai-native-engineering.html': 'What is AI-native engineering?',
           'compare/ai-native-engineering-vs-ai-coding-tools.html': 'AI-native engineering vs AI coding tools',
           'compare/upcore-vs-building-in-house.html': 'Build it in-house, or bring in Upcore?'}
FRAMEWORKS = {'insights/human-in-the-loop.html', 'insights/roi-business-case-ai-agents.html', 'insights/choosing-first-ai-agent.html'}
TYPES = [('guide', 'Guides'), ('comparison', 'Comparisons'), ('framework', 'Frameworks'), ('playbook', 'Industry playbooks')]
TYPE_LABEL = dict(TYPES)


def kind(f):
    f = f.replace(os.sep, '/')
    if f.startswith('learn/'):
        return 'guide'
    if f.startswith('compare/'):
        return 'comparison'
    return 'framework' if f in FRAMEWORKS else 'playbook'


def read(f):
    s = open(os.path.join(C.ROOT, f), encoding='utf-8').read()
    title = H.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1)).strip()
    title = re.sub(r'\s*\|\s*Upcore.*$', '', title)
    title = DISPLAY.get(f.replace(os.sep, '/'), title)
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = H.unescape(m.group(1)).strip() if m else ''
    main = re.search(r'<main[^>]*>(.*)</main>', s, re.S)
    body = main.group(1) if main else s
    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', body, flags=re.S)
    mins = max(3, round(len(re.sub(r'<[^>]+>', ' ', body).split()) / 230))
    url = '/' + f.replace(os.sep, '/')[:-5]
    return dict(f=f.replace(os.sep, '/'), title=title, desc=desc, mins=mins, url=url, kind=kind(f))


files = sorted(set(glob.glob(os.path.join(C.ROOT, 'learn', '*.html')) + glob.glob(os.path.join(C.ROOT, 'compare', '*.html'))
                   + [p for p in glob.glob(os.path.join(C.ROOT, 'insights', '*.html')) if not p.endswith('index.html')]))
items = [read(os.path.relpath(p, C.ROOT)) for p in files]
by_f = {i['f']: i for i in items}
order = {k: n for n, (k, _) in enumerate(TYPES)}
rest = sorted(items, key=lambda i: (order[i['kind']], i['title'].lower()))

e = lambda s: H.escape(s, quote=True)
feat = ''.join(f'<li data-reveal style="--d:{n}" data-type="{i["kind"]}"><a href="{i["url"]}"><span class="hb-k">{TYPE_LABEL[i["kind"]].rstrip("s")}</span><b>{e(i["title"])}</b><span class="hb-d">{e(i["desc"])}</span><span class="hb-m">{i["mins"]} min read</span><i aria-hidden="true">{C.ARROW}</i></a></li>'
               for n, i in enumerate(by_f[f] for f in FEATURED if f in by_f))
rows = ''.join(f'<li data-type="{i["kind"]}"{" data-feat" if i["f"] in FEATURED else ""}><a href="{i["url"]}"><span class="hb-k">{TYPE_LABEL[i["kind"]].rstrip("s")}</span><span class="hb-t"><b>{e(i["title"])}</b><span class="hb-d">{e(i["desc"])}</span></span><span class="hb-m">{i["mins"]} min</span><i aria-hidden="true">{C.ARROW}</i></a></li>' for i in rest)
counts = {k: sum(1 for i in items if i['kind'] == k) for k, _ in TYPES}
chips = (f'<button type="button" class="hb-chip is-on" data-filter="all" aria-pressed="true">All <span>{len(items)}</span></button>'
         + ''.join(f'<button type="button" class="hb-chip" data-filter="{k}" aria-pressed="false">{l} <span>{counts[k]}</span></button>' for k, l in TYPES))

hero = K.hero_page([(C.URL['home'], 'Home'), (None, 'Insights')], 'Insights',
                   'Practical AI guides <span class="hl">for business leaders.</span>',
                   'Plain-English guides to AI-native engineering, AI governance and automation, honest comparisons, and playbooks by industry.',
                   extra=f'<div class="hb-tools" data-reveal style="--d:4"><label class="hb-search"><span class="sr">Search insights</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input type="search" placeholder="Search {len(items)} articles" data-hb-search autocomplete="off" /></label></div>')
featured = f'''<section class="h-sec h-sec--tight hb-feat-sec" aria-labelledby="start-h"><div class="wrap">
<p class="h-col" id="start-h">Start here</p><ul class="hb-feat">{feat}</ul></div></section>'''
listing = f'''<section class="h-sec hb-list-sec" id="all" aria-labelledby="all-h"><div class="wrap" data-hub>
<div class="hb-bar"><h2 id="all-h" class="h-h3">Everything we&rsquo;ve published</h2><div class="hb-chips" role="group" aria-label="Filter by type">{chips}</div></div>
<ul class="hb-list">{rows}</ul>
<p class="hb-empty" hidden>No matches. Try a different word, or <button type="button" class="hb-reset">show everything</button>.</p>
</div></section>'''
news = f'''<section class="h-sec h-sec--tight h-sec--alt" aria-labelledby="nl-h"><div class="wrap hb-news">
<div>{K.eyebrow("New guides by email")}<h2 id="nl-h" class="h-h2 h-h2--sm" data-reveal>Get the next guide first.</h2>
<p class="hb-side" data-reveal style="--d:1">An occasional email when we publish something new. No sales sequences.</p></div>
<form class="hb-form" data-newsletter novalidate><label class="ct-f"><input type="email" name="email" autocomplete="email" placeholder=" " required /><span class="hb-fl">Work email</span></label>
<input class="ct-hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" />
<button class="btn" type="submit"><span class="hb-send">Subscribe</span> <span class="btn-ico">{C.ARROW}</span></button>
<p class="hb-msg" role="status" aria-live="polite"></p></form></div></section>'''
final = K.final('Want this applied <span class="hl">to your teams?</span>',
                'Book a 45-minute discovery call. We&rsquo;ll look at where you are with AI and send a written plan, whether or not we work together.')

page = '\n'.join([hero, featured, listing, news, final])
ld = C.graph('insights', [{'@type': 'CollectionPage', 'name': 'Upcore Insights', 'url': C.SITE + C.FINAL_URL['insights'],
                           'hasPart': [{'@type': 'Article', 'headline': i['title'], 'url': C.SITE + i['url']} for i in rest]}], crumb='Insights')
print('insights', len(items), 'items', C.write('insights/index.html', 'insights', 'Insights: AI-Native Engineering, Governance &amp; Automation | Upcore',
      'Plain-English guides to AI-native engineering, AI governance and automation, honest comparisons, and AI playbooks by industry.',
      page, active='insights', ld=ld, group='insights', spine=False, main_cls='is-calm'))
