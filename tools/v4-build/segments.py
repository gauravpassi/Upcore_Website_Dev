"""Generate the four V4.1 'Who we help' segment pages (post-audit)."""
import re, os, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
import frameworks as F
import chrome as CH
import tools as TL
import flow as FL
from v4parts import head as sec_head, TRUST, quotes, faq_sec, cta

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


def page(slug, name, d):
    flow_steps = ''.join(
        f'<div class="step{" human" if h else ""}"><span class="st-i"></span><span class="st-t">{t}</span><em>{e}</em></div>'
        for t, e, h in d['flow']['steps'])
    chips = ''.join((f'<a class="chip" href="#workflows" data-tab="{c[1]}">{c[0]}</a>' if isinstance(c, tuple) else f'<span class="chip">{c}</span>') for c in d['chips'])
    run = SEG_RUN[slug]
    fl = FL.flowline(d['flow']['steps'], run['tickets'], d['flow']['title'], d['flow']['aria'], branch_label=run['branch'], end_label=run['end'])
    hero = f'''<section class="hero hero--flow hero--left" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<div class="hero-copy"><nav class="crumb" aria-label="Breadcrumb" data-reveal><ol><li><a href="{CH.URL['home']}">Home</a></li><li><a href="{CH.URL['home']}#segments">Who we help</a></li><li aria-current="page">{name}</li></ol></nav>
<div class="eyebrow" data-reveal>{d['eyebrow']}</div>
<h1 id="hero-h" class="t-display" data-split>{d['h1']}</h1>
<p class="t-lead" data-reveal style="--d:3">{d['lead']}</p>
<div class="hero-ctas" data-reveal style="--d:4">{CH.btn('hero', pulse=True)}<a class="link" href="#workflows">{d.get('hero_link', 'See what we automate')}</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes &middot; a written plan, whether or not we work together</p>
<div class="hero-proof" data-reveal style="--d:5">{chips}</div></div>
</div>{fl}</section>'''

    blocks = [hero, TRUST]
    if d.get('stats'):
        st = ''.join(f'<div class="stat" data-reveal><b data-count>{v}</b><p>{t}<sup>{i+1}</sup></p></div>' for i, (v, t, _, _) in enumerate(d['stats']))
        src = ' &middot; '.join(f'<sup>{i+1}</sup> <a href="{u}" rel="nofollow noopener" target="_blank">{n}<span class="sr"> (opens in a new tab)</span></a>' for i, (_, _, n, u) in enumerate(d['stats']))
        blocks.append(f'<section class="sec sec--tight" aria-labelledby="pain-h"><div class="wrap">{sec_head(d["pain"][0], d["pain"][1], d["pain"][2], hid="pain-h")}<div class="stats" data-reveal>{st}</div><p class="sources">Sources: {src}</p></div></section>')

    wf_inner = d['wf_custom'] if d.get('wf_custom') else FL.outcome_rows(d['workflows'])
    blocks.append(f'<section class="sec" id="workflows" aria-labelledby="wf-h"><div class="wrap">{sec_head(d.get("wf_eyebrow", "What we automate"), d["wf_h2"], d["wf_lead"], hid="wf-h")}{wf_inner}{TL.strip(d["tools"], "Connects to") if d.get("tools") else ""}</div></section>')

    c1, c2 = d.get('ba_cols', ('Today', 'With agents'))
    blocks.append(f'<section class="sec sec--gap" aria-labelledby="ba-h"><div class="wrap gap-grid"><div class="gap-side">{sec_head("Before and after", d["ba_h2"], hid="ba-h", split=False)}</div>{FL.strike(d["ba"], c1, c2)}</div></section>')

    if d.get('fw'):
        k, e, h2, lead = d['fw']
        blocks.append(F.single(k, e, h2, lead))
    rows = ''.join(f'<div class="row" data-reveal><div class="row-num" data-count>{n}</div><div class="row-who">{w}</div><div class="row-desc">{t}</div></div>' for n, w, t in d['proof'])
    blocks.append(f'''<section class="band band--flow sec sec--proof" aria-labelledby="proof-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
{sec_head("Proof", d["proof_h2"], d["proof_lead"], hid="proof-h")}
<div class="rows" data-reveal>{rows}</div><p class="fine" style="color:var(--on-band-2)">Client names are withheld. Results are as reported from our engagements. Ask us for a reference call.</p>
{quotes(d.get('quotes', 'ops'))}</div></section>''')

    blocks.append(f'<section class="sec sec--engage" id="engagement" aria-labelledby="path-h"><div class="wrap">{sec_head("How engagements work", d["path_h2"], d["path_lead"], hid="path-h")}{FL.timeline(d["path"])}</div></section>')

    if d.get('controls'):
        blocks.append(F.controls())
    blocks.append(faq_sec(d['faq'], d['faq_h2'], d.get('faq_lead', 'Not covered here? Ask Gaurav or Saswata on the discovery call; they&rsquo;ll tell you plainly whether automation will pay off for you.')))
    eng = slug == 'tech-software'
    blocks.append(cta(d['cta_h2'], d['cta_p'], '/lp/governance-index' if eng else '/lp/ai-maturity-index',
                      'Get your AI Governance Score in 2 minutes' if eng else 'Get your AI Maturity Score in 2 minutes', slug, leaders=eng))

    ld = CH.graph(slug, [
        {'@type': 'Service', 'name': d.get('ld_name', f'AI process automation for {H.unescape(name)}'), 'serviceType': d.get('ld_type', 'Business process automation'),
         'url': CH.SITE + CH.FINAL_URL[slug], 'provider': {'@id': CH.ORG_ID}, 'areaServed': CH.AREA, 'description': H.unescape(re.sub('<[^>]+>', '', d['meta']))},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': H.unescape(re.sub('<[^>]+>', '', q)), 'acceptedAnswer': {'@type': 'Answer', 'text': H.unescape(re.sub('<[^>]+>', '', a))}} for q, a in d['faq']]}],
        crumb=H.unescape(name))
    return CH.write(f'who-we-help/{slug}.html', slug, d['title'], d['meta'], chr(10).join(blocks), active=slug, ld=ld,
                    group='who-we-help', annc_kind=CH.ANNC_ENG if eng else CH.ANNC_OPS)


from segment_copy import COPY  # noqa: E402
for slug, name in SEGS:
    print(slug, page(slug, name, COPY[slug]))
