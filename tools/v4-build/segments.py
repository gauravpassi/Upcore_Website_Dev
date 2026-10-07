"""Generate the four 'Who we help' segment pages (2026-10-07, calm rebuild; copy in segment_copy.py).
Section order: hero with the example-run flowline -> where it hurts (sourced stats, where we have them)
-> what we automate -> before and after -> results -> how engagements work -> FAQ -> CTA.
The trust marquee, framework diagrams and enterprise-controls grid from V4.1 were dropped to cut
length; security is one link away in every FAQ and in the footer.
Run from the repo root: python tools/v4-build/segments.py"""
import re, os, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as CH
import calm as K
import tools as TL
import flow as FL
from v4parts import TESTIMONIALS

# Example runs for the hero flowline (illustrative, labelled "example run" on the page).
SEG_RUN = {
    'ecommerce-retail': dict(branch='Refund &middot; to your team', end='Resolved &middot; logged', tickets=[
        dict(id='#10482', title='Where is my order?', risk='lo', out='Answered from live carrier tracking'),
        dict(id='#10519', title='Change of delivery address', risk='lo', out='Updated under your policy, customer told'),
        dict(id='#10533', title='Damaged item, refund request', risk='hi', branch=True, out='Refund routed to your team to approve')]),
    'operations-heavy': dict(branch='Exception &middot; to a person', end='Payment tracked', tickets=[
        dict(id='B-1204', title='First installment due', risk='lo', out='Documents complete, payment tracked in the CRM'),
        dict(id='C-0807', title='Bank sanction letter pending', risk='md', out='Chased by email and WhatsApp until received'),
        dict(id='A-0311', title='Name mismatch on the agreement', risk='hi', branch=True, out='Exception sent to your team with the reason')]),
    'professional-services': dict(branch='Exception &middot; to a professional', end='Ready for work', tickets=[
        dict(id='CL-2291', title='Year-end documents', risk='lo', out='File complete and filed, ready for work'),
        dict(id='CL-1874', title='Missing bank statements', risk='md', out='Chased until complete, no one wrote a reminder'),
        dict(id='CL-3022', title='Unsigned engagement letter', risk='hi', branch=True, out='Flagged for a professional to review')]),
    'tech-software': dict(branch='Held &middot; architect review', end='Released &middot; logged', tickets=[
        dict(id='PAY-418', title='Add partial refunds to checkout', risk='lo', out='Low risk &middot; auto-merged, released behind a flag'),
        dict(id='ORD-190', title='Add delivery-window field to orders', risk='md', out='Medium risk &middot; spec amended, then approved'),
        dict(id='AUTH-77', title='Refactor session handling', risk='hi', branch=True, out='High risk &middot; held at plan sign-off for an architect')]),
}

SEGS = [('ecommerce-retail', 'Ecommerce &amp; Retail'), ('operations-heavy', 'Operations-Heavy Businesses'),
        ('professional-services', 'Professional Services'), ('tech-software', 'Tech &amp; Software')]
TAG = {'tech-software': 'Engineering'}


def plain(s):
    return re.sub(r'<span class="(ul-draw|hl)">(.*?)</span>', r'\2', s)


def page(slug, name, d):
    eng = slug == 'tech-software'
    run = SEG_RUN[slug]
    fl = FL.flowline(d['flow']['steps'], run['tickets'], d['flow']['title'], d['flow']['aria'], branch_label=run['branch'], end_label=run['end'])
    chips = ''.join((f'<a class="chip" href="#workflows" data-tab="{c[1]}">{c[0]}</a>' if isinstance(c, tuple) else f'<span class="chip">{c}</span>') for c in d['chips'])
    hero = f'''<section class="h-hero h-hero--seg hero--flow" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
{K.crumb([(CH.URL['home'], 'Home'), (CH.URL['home'] + '#segments', 'Who we help'), (None, name)])}
<p class="h-eyebrow" data-reveal>{d['eyebrow']}</p>
<h1 id="hero-h" class="t-hero" data-split>{d['h1']}</h1>
<p class="t-lead" data-reveal style="--d:3">{d['lead']}</p>
<div class="hero-ctas" data-reveal style="--d:4">{CH.btn('hero', pulse=True)}<a class="link" href="#workflows">{d.get('hero_link', 'See what we automate')}</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes &middot; a written plan, whether or not we work together</p>
<div class="hero-proof" data-reveal style="--d:5">{chips}</div>
</div>{fl}<div class="wrap">{K.PROOF_STRIP}</div></section>'''
    blocks = [hero]

    if d.get('stats'):
        st = ''.join(f'<div class="stat" data-reveal style="--d:{i}"><b data-count>{v}</b><p>{t}<sup>{i + 1}</sup></p></div>' for i, (v, t, _, _) in enumerate(d['stats']))
        src = ' &middot; '.join(f'<sup>{i + 1}</sup> <a href="{u}" rel="nofollow noopener" target="_blank">{n}<span class="sr"> (opens in a new tab)</span></a>' for i, (_, _, n, u) in enumerate(d['stats']))
        blocks.append(f'''<section class="h-sec h-sec--tight" aria-labelledby="pain-h"><div class="wrap">
{K.head(d["pain"][0], plain(d["pain"][1]), "pain-h", d["pain"][2])}
<div class="stats" data-reveal>{st}</div><p class="sources">Sources: {src}</p></div></section>''')

    wf_inner = d['wf_custom'] if d.get('wf_custom') else FL.outcome_rows(d['workflows'])
    blocks.append(f'''<section class="h-sec{" h-sec--alt" if d.get("stats") else ""}" id="workflows" aria-labelledby="wf-h"><div class="wrap">
{K.head(d.get("wf_eyebrow", "What we automate"), plain(d["wf_h2"]), "wf-h", d["wf_lead"])}
{wf_inner}{TL.strip(d["tools"], "Connects to") if d.get("tools") else ""}</div></section>''')

    c1, c2 = d.get('ba_cols', ('Today', 'With agents'))
    blocks.append(f'''<section class="h-sec{"" if d.get("stats") else " h-sec--alt"}" aria-labelledby="ba-h"><div class="wrap gap-grid">
<div class="gap-side">{K.eyebrow("Before and after")}<h2 id="ba-h" class="h-h2 h-h2--sm" data-reveal>{d["ba_h2"]}</h2></div>
{FL.strike(d["ba"], c1, c2)}</div></section>''')

    tag = TAG.get(slug, 'Automation')
    res = [(tag, n, t, re.sub(r'<br\s*/?>', ' &middot; ', w)) for n, w, t in d['proof']]
    q = TESTIMONIALS[d.get('quotes', 'ops')][0]
    qt = q[0] if len(q[0]) < 200 else 'I have worked with Upcore many times on projects big and small. Their expertise, network, and professionalism is second to none.'
    blocks.append(K.results_band('Results', plain(d['proof_h2']), res, quote=(qt, q[1]), long=True, lead=d.get('proof_lead')))

    blocks.append(f'''<section class="h-sec" id="engagement" aria-labelledby="path-h"><div class="wrap">
{K.head("How engagements work", plain(d["path_h2"]), "path-h", d["path_lead"])}
{FL.timeline(d["path"])}</div></section>''')

    blocks.append(K.faq(d['faq'], plain(d['faq_h2'])))
    blocks.append(K.final(d['cta_h2'], d['cta_p'], K.lp_alt(slug, 'gov' if eng else 'maturity')))

    ld = CH.graph(slug, [
        {'@type': 'Service', 'name': d.get('ld_name', f'AI process automation for {H.unescape(name)}'), 'serviceType': d.get('ld_type', 'Business process automation'),
         'url': CH.SITE + CH.FINAL_URL[slug], 'provider': {'@id': CH.ORG_ID}, 'areaServed': CH.AREA, 'description': H.unescape(re.sub('<[^>]+>', '', d['meta']))},
        K.faq_ld(d['faq'])], crumb=H.unescape(name))
    return CH.write(f'who-we-help/{slug}.html', slug, d['title'], d['meta'], chr(10).join(blocks), active=slug, ld=ld,
                    group='who-we-help', annc_kind=CH.ANNC_ENG if eng else CH.ANNC_OPS, spine=False, main_cls='is-calm')


from segment_copy import COPY  # noqa: E402
for slug, name in SEGS:
    print(slug, page(slug, name, COPY[slug]))
