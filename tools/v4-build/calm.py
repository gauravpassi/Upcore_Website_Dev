"""Shared parts for the calm (is-calm) pages built in phase 2 and 3 (2026-10-07):
eyebrows, breadcrumbs, heroes, section heads, results band, FAQ, final CTA and FAQ JSON-LD.
The homepage, AI-Native Engineering and About builders predate this module and keep their own copies."""
import re, html as H
import chrome as C

ARROW = C.ARROW

PROOF_STRIP = '''<ul class="h-proof" aria-label="Certifications and ratings">
<li><img src="/images/accolades/light/iso27001.svg" alt="" width="26" height="26" /><span>ISO 27001</span></li>
<li><img src="/images/accolades/light/iso9001.svg" alt="" width="26" height="26" /><span>ISO 9001</span></li>
<li><img src="/images/accolades/light/cmmi.svg" alt="CMMI Level 3" width="46" height="26" /></li>
<li><a href="https://clutch.co/profile/upcore-technologies" target="_blank" rel="noopener"><span>Clutch 5.0&#9733;</span><span class="sr"> (opens in a new tab)</span></a></li>
<li><span>Claude Certified Architects</span></li>
</ul>'''


def eyebrow(t):
    return f'<p class="h-eyebrow" data-reveal>{t}</p>'


def crumb(trail):
    """trail: [(href, label), ..., (None, current)]"""
    li = ''.join(f'<li><a href="{h}">{l}</a></li>' if h else f'<li aria-current="page">{l}</li>' for h, l in trail)
    return f'<nav class="crumb" aria-label="Breadcrumb" data-reveal><ol>{li}</ol></nav>'


def hero_split(trail, eb, h1, lead, ctas, vis, micro='45 minutes &middot; a written plan, whether or not we work together', proof=True, cls='h-hero--long'):
    m = f'<p class="hero-micro" data-reveal style="--d:4">{micro}</p>' if micro else ''
    return f'''<section class="h-hero {cls}" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap h-hero-in">
<div class="h-hero-copy">{crumb(trail)}
<p class="h-eyebrow" data-reveal>{eb}</p>
<h1 id="hero-h" class="t-hero" data-split>{h1}</h1>
<p class="t-lead" data-reveal style="--d:3">{lead}</p>
<div class="hero-ctas" data-reveal style="--d:4">{ctas}</div>{m}
</div>
<div class="h-hero-vis" data-reveal="scale" style="--d:2">{vis}</div>
</div>{f'<div class="wrap">{PROOF_STRIP}</div>' if proof else ''}</section>'''


def hero_page(trail, eb, h1, lead, extra=''):
    return f'''<section class="h-hero h-hero--page" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
{crumb(trail)}
<p class="h-eyebrow" data-reveal>{eb}</p>
<h1 id="hero-h" class="t-display" data-split>{h1}</h1>
{f'<p class="t-lead" data-reveal style="--d:3">{lead}</p>' if lead else ''}{extra}
</div></section>'''


def head(eb, h2, hid, lead='', sm=False):
    l = f'<p class="h-lead" data-reveal style="--d:1">{lead}</p>' if lead else ''
    return f'<div class="h-head"><div>{eyebrow(eb)}<h2 id="{hid}" class="h-h2{" h-h2--sm" if sm else ""}" data-reveal>{h2}</h2></div>{l}</div>'


def results_band(eb, h2, items, foot=True, quote=None, long=False, lead=None):
    """items: [(tag, number, what, who)]"""
    res = ''.join(f'<li data-reveal style="--d:{i}"><span class="h-tag">{tg}</span><b data-count{" class=is-word" if (not any(ch.isdigit() for ch in n) or len(H.unescape(n)) > 6) else ""}>{n}</b>'
                  f'<span class="what">{w}</span><span class="who">{who}</span></li>' for i, (tg, n, w, who) in enumerate(items))
    q = ''
    if quote:
        q = f'<figure class="h-quote" data-reveal><span class="h-qmark" aria-hidden="true">&ldquo;</span><blockquote><p>{quote[0]}</p></blockquote><figcaption>{quote[1]}</figcaption></figure>'
    f = (f'<div class="h-proof-foot"><a class="link" href="{C.URL["results"]}">See all results</a><span>Results as reported from our engagements. Ask us for a reference call.</span></div>') if foot else ''
    return f'''<section class="band h-sec h-proof-band" aria-labelledby="res-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
{eyebrow(eb)}
<h2 id="res-h" class="h-h2" data-reveal>{h2}</h2>{f'<p class="h-res-lead" data-reveal style="--d:1">{lead}</p>' if lead else ''}
<ul class="h-results{' h-results--long' if long else ''}">{res}</ul>{q}{f}
</div></section>'''


def faq(items, h2, eb='Questions'):
    fq = ''.join(f'<details><summary>{a}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{b}</p></div></details>' for a, b in items)
    return f'''<section class="h-sec" aria-labelledby="faq-h"><div class="wrap h-faq">
<div>{eyebrow(eb)}<h2 id="faq-h" class="h-h2 h-h2--sm" data-reveal>{h2}</h2></div>
<div class="faq">{fq}</div></div></section>'''


def faq_ld(items):
    clean = lambda s: re.sub(r'\s+', ' ', H.unescape(re.sub('<[^>]+>', '', s))).strip()
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': clean(a), 'acceptedAnswer': {'@type': 'Answer', 'text': clean(b)}} for a, b in items]}


def final(h2, p, alt='', btn_label='Book a Discovery Call', lines=True):
    import flow as FL
    a = f'<p class="cta-alt" data-reveal style="--d:3">{alt}</p>' if alt else ''
    return f'''<section class="band band--flow cta-band h-cta" aria-labelledby="cta-h">{FL.cta_lines() if lines else ''}<div class="spot" aria-hidden="true"></div><div class="wrap">
<h2 id="cta-h" class="t-display" data-reveal>{h2}</h2>
<p class="t-lead" data-reveal style="--d:1">{p}</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("cta_final", cls="btn btn--cyan", label=btn_label)}</div>{a}
</div></section>'''


def lp_alt(page, kind='gov'):
    if kind == 'gov':
        return f'Not ready for a call? <a href="/lp/governance-index?utm_source=website&amp;utm_medium={page}&amp;utm_campaign=cta_secondary">Get your AI Governance Score in 2 minutes <span aria-hidden="true">&rarr;</span></a>'
    return f'Not ready for a call? <a href="/lp/ai-maturity-index?utm_source=website&amp;utm_medium={page}&amp;utm_campaign=cta_secondary">Get your AI Maturity Score in 2 minutes <span aria-hidden="true">&rarr;</span></a>'


def svg_icon(paths, sw='1.6'):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>'
