"""Shared V4.1 page parts: trust strip, testimonials, FAQ section, final CTA band."""
import chrome as C
import flow as FL


def head(eyebrow, h2, lead='', split=True, hid=''):
    l = f'<p class="t-lead" data-reveal style="--d:1">{lead}</p>' if lead else ''
    i = f' id="{hid}"' if hid else ''
    if split and lead:
        return f'<div class="sec-head sec-head--split"><div><div class="eyebrow" data-reveal>{eyebrow}</div><h2{i} class="t-h2" data-reveal>{h2}</h2></div>{l}</div>'
    return f'<div class="sec-head"><div class="eyebrow" data-reveal>{eyebrow}</div><h2{i} class="t-h2" data-reveal>{h2}</h2>{l}</div>'


_TRUST_ITEMS = (
    '<li class="trust-item"><img src="/images/accolades/light/iso27001.svg" alt="ISO 27001 certified" width="30" height="30" /><b>ISO 27001</b></li>'
    '<li class="trust-item"><img src="/images/accolades/light/iso9001.svg" alt="ISO 9001 certified" width="30" height="30" /><b>ISO 9001</b></li>'
    '<li class="trust-item"><img src="/images/accolades/light/cmmi.svg" alt="CMMI Level 3" width="54" height="30" /></li>'
    '<li class="trust-item"><img src="/images/accolades/light/nasscom.svg" alt="Nasscom member" width="110" height="18" /></li>'
    '<li class="trust-item"><a href="https://clutch.co/profile/upcore-technologies" target="_blank" rel="noopener"><img src="/images/accolades/light/clutch.svg" alt="Clutch" width="80" height="30" /><b>5.0&#9733;</b><span class="sr"> rating on Clutch (opens in a new tab)</span></a></li>'
    '<li class="trust-item"><a href="https://www.designrush.com/agency/profile/upcore-technologies" target="_blank" rel="noopener"><b>DesignRush 5.0&#9733;</b><span class="sr"> (opens in a new tab)</span></a></li>'
    '<li class="trust-item"><b>Claude Certified Architects</b></li>'
)
TRUST = ('<section class="trust trust--flow" aria-label="Certifications and ratings"><div class="wrap trust-in">'
         '<p>Certified processes. Verified reviews. Delivering since 2020 for clients in six countries.</p>'
         + FL.marquee('<ul class="trust-row">' + _TRUST_ITEMS + '</ul>', dur=38) + '</div></section>')

TESTIMONIALS = {
    'eng': [("I have worked with Upcore many times on projects big and small. Their expertise, network, and professionalism is second to none. Their technical understanding combined with project management skills enables them to provide strategic guidance and direction while also managing a team of development resources.", 'Josh Fitheringham, CEO, Oragen USA', '', ''),
            ('Their ability to simplify difficult AI concepts for both our business and technical teams was particularly impressive.', 'Co-Founder, Real Estate &middot; AI consulting engagement', 'DesignRush', 'https://www.designrush.com/agency/profile/upcore-technologies')],
    'ops': [('They stuck to the timetable, completing each milestone on time, with clear, measurable results throughout.', 'Client review, Real Estate &middot; AI consulting engagement', 'DesignRush', 'https://www.designrush.com/agency/profile/upcore-technologies'),
            ('Upcore Technologies delivered a solution using machine learning and NLP that showed significant, measurable improvement.', 'Managing Director, Healthcare &middot; Generative AI engagement', 'DesignRush', 'https://www.designrush.com/agency/profile/upcore-technologies')],
}


QUOTE_LINKS = ('<div class="quote-links"><a class="link" href="https://vimeo.com/960114218" target="_blank" rel="noopener">Watch a client testimonial<span class="sr"> (opens in a new tab)</span></a>'
               '<a class="link" href="https://clutch.co/profile/upcore-technologies" target="_blank" rel="noopener">Clutch 5.0<span class="sr"> (opens in a new tab)</span></a>'
               '<a class="link" href="https://www.designrush.com/agency/profile/upcore-technologies" target="_blank" rel="noopener">DesignRush 5.0, 16 reviews<span class="sr"> (opens in a new tab)</span></a></div>')


def quotes(kind):
    return FL.quote_carousel(TESTIMONIALS[kind], QUOTE_LINKS)


def faq_sec(items, h2, lead):
    fq = ''.join(f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in items)
    return f'<section class="sec sec--faq" aria-labelledby="faq-h"><div class="wrap faq-grid"><div class="faq-side">{head("FAQs", h2, lead, split=False, hid="faq-h")}</div><div class="faq">{fq}</div></div></section>'


LEADERS = '''<div class="leaders" data-reveal style="--d:3"><span class="t-mono">Leadership</span>
<div class="person"><span class="avatar">GP</span><div><b>Gaurav Passi</b><span>Co-Founder &amp; CEO &middot; Claude Certified Architect</span></div></div>
<div class="person"><span class="avatar">SM</span><div><b>Shrikant Maniar</b><span>Executive Director &middot; former MD, Accenture</span></div></div>
<div class="person"><span class="avatar">SD</span><div><b>Shanker Dhand</b><span>Technical Head</span></div></div></div>'''


def cta(h2, p, alt_href, alt_label, page, leaders=False):
    pts = ''.join(f'<span>{x}</span>' for x in ['A 45-minute discovery call', 'A written plan, whether or not we work together', 'Pilot on one team before you commit'])
    alt = f'<p class="cta-alt" data-reveal style="--d:3">Not ready for a call? <a href="{alt_href}?utm_source=website&amp;utm_medium={page}&amp;utm_campaign=cta_secondary">{alt_label} <span aria-hidden="true">&rarr;</span></a></p>'
    return f'''<section class="band band--flow cta-band" aria-labelledby="cta-h">{FL.cta_lines()}<div class="spot" aria-hidden="true"></div><div class="wrap">
<div class="eyebrow" data-reveal>Next step</div><h2 id="cta-h" class="t-display" data-reveal>{h2}</h2><p class="t-lead" data-reveal style="--d:1">{p}</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("cta_final", cls="btn btn--cyan")}</div><div class="cta-points" data-reveal style="--d:3">{pts}</div>{alt}{LEADERS if leaders else ""}</div></section>'''


