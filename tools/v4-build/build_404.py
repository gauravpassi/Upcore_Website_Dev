"""Branded 404 page (2026-10-07 restructure). Vercel serves /404.html for any unknown path.
Run from the repo root: python tools/v4-build/build_404.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C

ARROW = C.ARROW
LINKS = [(C.URL['aine'], 'AI-Native Engineering', 'Governed AI delivery, spec to production'),
         (C.URL['results'], 'Results', 'What our work has delivered in production'),
         (C.URL['tech-software'], 'Tech &amp; Software', 'For CTOs and CIOs shipping with AI'),
         (C.URL['ecommerce-retail'], 'Ecommerce &amp; Retail', 'Order status, returns, catalog and ad spend'),
         (C.URL['operations-heavy'], 'Operations-Heavy Businesses', 'Collections, documents and follow-ups'),
         (C.URL['professional-services'], 'Professional Services', 'Accounting, law, wealth and staffing'),
         ('/insights', 'Insights', 'Articles and guides'),
         ('/contact', 'Contact', 'Talk to the team')]
lk = ''.join(f'<li><a href="{h}"><b>{t}</b><span>{d}</span><i aria-hidden="true">{ARROW}</i></a></li>' for h, t, d in LINKS)
body = f'''<section class="h-hero h-hero--page" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<p class="h-eyebrow" data-reveal>Page not found</p>
<h1 id="hero-h" class="t-display" data-split>This page has moved <span class="hl">or no longer exists.</span></h1>
<p class="t-lead" data-reveal style="--d:3">We recently reorganised the site. These are the places most people are looking for.</p>
<div class="hero-ctas" data-reveal style="--d:4">{C.btn("404", pulse=True)}<a class="link" href="{C.URL["home"]}">Go to the homepage</a></div>
</div></section>
<section class="h-sec h-sec--tight" aria-label="Popular pages"><div class="wrap"><div class="h-router h-router--one"><ul>{lk}</ul></div></div></section>'''
print('404', C.write('404.html', '404', 'Page Not Found | Upcore Technologies', 'This page has moved or no longer exists. Find AI-Native Engineering, results and who we help.',
      body, spine=False, main_cls='is-calm', noindex=True))
