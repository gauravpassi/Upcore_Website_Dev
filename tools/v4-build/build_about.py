"""/about (2026-10-07, calm rebuild). Who Upcore is, for a buyer checking us out:
hero + key facts -> why we exist (scroll-lit statement) -> what we do -> what we believe ->
leadership (initials, no headshots) -> where we are (client map) + credentials -> CTA.
Every fact here already appears elsewhere on the site; nothing new is claimed.
Run from the repo root: python tools/v4-build/build_about.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C

ARROW = C.ARROW


def eyebrow(t):
    return f'<p class="h-eyebrow" data-reveal>{t}</p>'


# ------------------------------------------------------------------ 1. hero
FACTS = [('2020', 'Delivering for clients since'), ('6', 'Countries where clients run our work'), ('5.0&#9733;', 'Rated on Clutch and DesignRush')]
facts = ''.join(f'<div data-reveal style="--d:{i + 3}"><dt>{v}</dt><dd>{l}</dd></div>' for i, (v, l) in enumerate(FACTS))
hero = f'''<section class="h-hero h-hero--page" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<nav class="crumb" aria-label="Breadcrumb" data-reveal><ol><li><a href="{C.URL["home"]}">Home</a></li><li aria-current="page">About</li></ol></nav>
<p class="h-eyebrow" data-reveal>About Upcore</p>
<h1 id="hero-h" class="t-display" data-split>We put AI to work <span class="hl">under your rules.</span></h1>
<p class="t-lead" data-reveal style="--d:3">Upcore installs governed AI-native delivery for engineering teams, builds agents that run repetitive operations work, and embeds AI leadership where a company needs it.</p>
<dl class="ab-facts">{facts}</dl>
</div></section>'''

# ------------------------------------------------------------------ 2. why we exist
LIT = ('So that is what we build: written specs, your architecture rules, checks on every change, '
       'limits on what merges on its own and a record of every decision. Then we stay and run it with your team.')
why = f'''<section class="h-sec" aria-labelledby="why-h"><div class="wrap">
<div class="ab-split"><div>{eyebrow("Why we exist")}<h2 id="why-h" class="h-h2 h-h2--sm" data-reveal>AI made software faster to write. Not easier to trust.</h2></div>
<div class="ab-prose"><p data-reveal>Teams adopted AI coding tools faster than any review process could keep up. Code shipped that no one had properly reviewed, AI-suggested packages reached production without security checks, and when compliance asked for an audit trail there wasn&rsquo;t one. Nobody owned what the AI produced.</p>
<p data-reveal style="--d:1">The tools were never the problem. What was missing was the process around them, and someone accountable for running it.</p></div></div>
<p class="ab-lit" data-lit>{LIT}</p>
</div></section>'''

# ------------------------------------------------------------------ 3. what we do
SERV = [('aine', 'AI-Native Engineering', 'A governed delivery pipeline from spec to production, run with your engineering team.', True),
        ('gov', 'AI Governance', 'Visibility of AI spend, data controls and audit trails across the company.', False),
        ('bpa', 'Business Process Automation', 'Agents that run repetitive operations work, with a person approving what matters.', False),
        ('fao', 'Fractional AI Officer', 'An embedded AI lead on retainer, accountable for your AI roadmap.', False)]
serv = ''.join(f'<li><a href="{C.URL[k]}"><b>{t}{"<span class=ab-flag>Flagship</span>" if f else ""}</b><span>{d}</span><i aria-hidden="true">{ARROW}</i></a></li>' for k, t, d, f in SERV)
what = f'''<section class="h-sec h-sec--tight h-sec--alt" aria-labelledby="what-h"><div class="wrap ab-split">
<div>{eyebrow("What we do")}<h2 id="what-h" class="h-h2 h-h2--sm" data-reveal>One way of working, applied where you need it.</h2>
<p class="ab-side" data-reveal style="--d:1">Every service runs on the same idea: AI does the routine work inside limits you set, and people decide what is risky.</p></div>
<div class="h-router h-router--one ab-serv"><ul>{serv}</ul></div></div></section>'''

# ------------------------------------------------------------------ 4. what we believe
BELIEFS = [('Control comes before autonomy.', 'AI works inside guardrails you define, and nothing runs at scale without approval where it matters. Autonomy is earned on your own work, not assumed.'),
           ('Context beats model size.', 'An AI that doesn&rsquo;t know your architecture, terminology or edge cases is a prototype, not a production tool. We encode your rules before we automate anything.'),
           ('Prove it on real work.', 'Every engagement starts with a pilot on one team or one workflow, measured against how you work today, before you commit further.'),
           ('Amplify people. Keep the judgment human.', 'AI takes the repetitive, high-volume work. People keep judgment, relationships and exceptions. That division is what makes the results reliable.')]
bel = ''.join(f'<li data-reveal style="--d:{i % 2}"><span class="ab-n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(BELIEFS))
believe = f'''<section class="h-sec" aria-labelledby="bel-h"><div class="wrap">
{eyebrow("What we believe")}
<h2 id="bel-h" class="h-h2" data-reveal>Four convictions behind every engagement.</h2>
<ol class="ab-beliefs" data-beliefs>{bel}</ol>
</div></section>'''

# ------------------------------------------------------------------ 5. leadership (initials avatars, no headshots)
LI_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.77 2.65 4.77 6.1V21h-4v-4.95c0-1.18-.02-2.7-1.65-2.7-1.65 0-1.9 1.29-1.9 2.62V21h-4z"/></svg>'
TEAM = [('GP', 'Gaurav Passi', 'Co-Founder &amp; CEO &middot; Claude Certified Architect',
         'Leads client engagements and delivery quality. Every engagement plan goes through him before it reaches your team.', 'https://linkedin.com/in/gauravusa'),
        ('SM', 'Shrikant Maniar', 'Executive Director &middot; former MD, Accenture',
         'Sits across the engagement portfolio: scope, commercial terms and whether an engagement is the right fit before it starts. If you want to talk to someone other than your delivery lead about how an engagement is run, it&rsquo;s him.', 'https://www.linkedin.com/in/shrikantmaniar/'),
        ('SD', 'Shanker Dhand', 'Technical Head',
         'Owns the technical side of delivery: the review standards, the checks wired into your pipeline and the architecture decisions behind anything Upcore ships into your environment.', 'https://www.linkedin.com/in/shankerdhand/')]
team_li = ''.join(
    f'<li class="ab-p" data-reveal style="--d:{i}"><span class="ab-av" aria-hidden="true"><span>{ini}</span></span>'
    f'<h3>{n}</h3><p class="ab-role">{r}</p><p class="ab-bio">{b}</p>'
    f'<a class="ab-li" href="{u}" target="_blank" rel="noopener">{LI_ICON}<span>LinkedIn<span class="sr">: {n} (opens in a new tab)</span></span></a></li>'
    for i, (ini, n, r, b, u) in enumerate(TEAM))
team = f'''<section class="h-sec h-sec--alt" id="team" aria-labelledby="team-h"><div class="wrap">
<div class="h-head"><div>{eyebrow("Leadership")}<h2 id="team-h" class="h-h2" data-reveal>The people accountable for your work.</h2></div>
<p class="h-lead" data-reveal style="--d:1">Before you hand us part of your delivery, you should know who is responsible for it.</p></div>
<ol class="ab-team">{team_li}</ol>
<p class="ab-pods" data-reveal>Day to day, your work is run by a pod of three: a full-stack developer, a Claude Certified Architect and an analyst who is your single point of contact. Every Upcore architect is Claude certified. <a class="link" href="{C.URL["aine"]}#team">How a pod works</a></p>
</div></section>'''

# ------------------------------------------------------------------ 6. where we are: dot map with arcs from the delivery team
# Rough continent outlines (lon, lat); a 3-degree dot grid is filled where a point falls inside one.
LAND = [
    [(-168, 66), (-140, 70), (-95, 72), (-80, 68), (-62, 60), (-55, 50), (-66, 44), (-76, 35), (-81, 25), (-97, 26), (-97, 18), (-88, 15), (-83, 9),
     (-78, 8), (-85, 12), (-92, 15), (-105, 20), (-112, 30), (-118, 33), (-124, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-52, 82), (-22, 82), (-18, 72), (-42, 60), (-56, 70)],
    [(-80, 10), (-62, 11), (-50, 0), (-35, -7), (-40, -22), (-48, -28), (-58, -38), (-65, -55), (-73, -50), (-72, -30), (-70, -18), (-81, -5)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (2, 51), (8, 54), (5, 58), (10, 63), (20, 70), (30, 71), (40, 67), (45, 55), (40, 45), (28, 41), (22, 37), (15, 38), (10, 44), (3, 42)],
    [(-6, 50), (1, 51), (2, 53), (-2, 56), (-3, 59), (-7, 57)],
    [(-17, 21), (-10, 32), (10, 37), (32, 31), (35, 28), (43, 12), (51, 12), (40, -2), (40, -15), (35, -25), (27, -34), (18, -34), (12, -17), (9, -1), (5, 5), (-8, 4), (-17, 14)],
    [(26, 40), (36, 36), (35, 30), (44, 13), (52, 15), (58, 22), (66, 25), (72, 21), (77, 8), (80, 15), (88, 22), (92, 22), (98, 16), (100, 5), (104, 1), (106, 10),
     (109, 15), (108, 21), (117, 23), (122, 31), (121, 40), (128, 38), (130, 43), (140, 48), (142, 55), (135, 55), (160, 60), (170, 65), (180, 68), (180, 72),
     (140, 73), (110, 77), (80, 73), (68, 70), (55, 68), (45, 55), (40, 45)],
    [(130, 31), (135, 34), (141, 38), (142, 45), (140, 42), (136, 36)],
    [(95, 5), (104, -6), (115, -8), (125, -9), (130, -4), (119, 1), (119, 6), (110, 3)],
    [(131, -1), (141, -3), (150, -10), (141, -9)],
    [(114, -22), (114, -34), (123, -34), (131, -31.5), (138, -35), (146, -39), (150, -37), (153, -28), (153, -25), (146, -19), (142, -11), (136, -12), (131, -12), (125, -15)],
    [(172, -34), (178, -38), (174, -42), (167, -46), (170, -44)],
    [(44, -25), (48, -25), (50, -15), (49, -12), (44, -17)],
]
LON0, LAT0, SC = -170, 78, 2  # viewBox x = (lon + 170) * 2, y = (78 - lat) * 2
W, H = 700, 256


def xy(lon, lat):
    return (lon - LON0) * SC, (LAT0 - lat) * SC


def inside(pt, poly):
    x, y = pt
    hit = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit


dots = []
for lat in range(75, -50, -3):
    for lon in range(-168, 181, 3):
        if any(inside((lon, lat), p) for p in LAND):
            x, y = xy(lon, lat)
            dots.append(f'M{x:g} {y:g}h0')
land = ''.join(dots)

HUB = (76.7, 30.7)  # Mohali, India
PLACES = [('us', 'United States', (-96, 37), 'middle', 0, 22), ('uk', 'United Kingdom', (-1, 52), 'end', -10, -8),
          ('za', 'South Africa', (28, -26), 'end', -10, 16), ('mu', 'Mauritius', (57.5, -20.2), 'start', 10, 16),
          ('au', 'Australia', (151, -34), 'end', -10, 18)]
hx, hy = xy(*HUB)
arcs, nodes = '', ''
for i, (k, name, (lon, lat), anchor, dx, dy) in enumerate(PLACES):
    x, y = xy(lon, lat)
    mx, my = (hx + x) / 2, (hy + y) / 2
    d = math.hypot(x - hx, y - hy)
    nx, ny = -(y - hy) / d, (x - hx) / d  # unit normal; flip so the arc bows upward
    if ny > 0:
        nx, ny = -nx, -ny
    lift = min(d * 0.28, 72)
    path = f'M{hx:.1f} {hy:.1f}Q{mx + nx * lift:.1f} {my + ny * lift:.1f} {x:.1f} {y:.1f}'
    arcs += f'<path class="ab-arc c-{k}" style="--i:{i}" d="{path}" pathLength="1"/><path class="ab-comet c-{k}" style="--i:{i}" d="{path}" pathLength="1"/>'
    nodes += (f'<g class="ab-node c-{k}" style="--i:{i}"><circle class="ab-ping" cx="{x:.1f}" cy="{y:.1f}" r="9"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3.6"/>'
              f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{name}</text></g>')
MAP = f'''<figure class="ab-map" data-map data-reveal style="--d:1"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Map: the delivery team in India works with clients in the United States, the United Kingdom, South Africa, Mauritius and Australia" focusable="false">
<path class="ab-land" d="{land}"/>{arcs}{nodes}
<g class="ab-hub"><circle class="ab-ping" cx="{hx:.1f}" cy="{hy:.1f}" r="12"/><circle cx="{hx:.1f}" cy="{hy:.1f}" r="5.5"/><text x="{hx + 12:.1f}" y="{hy - 12:.1f}">Delivery team &middot; India</text></g>
</svg></figure>'''

PL = [('in', 'India', 'Delivery team, Mohali')] + [(k, n, 'Clients') for k, n, *_ in PLACES]
places = ''.join(f'<li data-c="{k}"><i aria-hidden="true"></i><b>{n}</b><span>{s}</span></li>' for k, n, s in PL)
CREDS = [('<img src="/images/accolades/light/iso27001.svg" alt="" width="26" height="26" />', 'ISO 27001', 'Information security management', ''),
         ('<img src="/images/accolades/light/iso9001.svg" alt="" width="26" height="26" />', 'ISO 9001', 'Quality management', ''),
         ('<img src="/images/accolades/light/cmmi.svg" alt="" width="46" height="26" />', 'CMMI Level 3', 'Delivery processes', ''),
         ('<img src="/images/accolades/light/nasscom.svg" alt="" width="92" height="15" />', 'Nasscom', 'Member', ''),
         ('', 'Clutch 5.0&#9733;', 'Verified client reviews', 'https://clutch.co/profile/upcore-technologies'),
         ('', 'DesignRush 5.0&#9733;', '16 client reviews', 'https://www.designrush.com/agency/profile/upcore-technologies')]


def cred(img, t, d, u):
    img = img or '<span class="ab-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
    inner = f'<span class="ab-cred-i">{img}</span><b>{t}</b><span>{d}</span>'
    if u:
        return f'<li><a href="{u}" target="_blank" rel="noopener">{inner}<span class="sr"> (opens in a new tab)</span></a></li>'
    return f'<li>{inner}</li>'


creds = ''.join(cred(*c) for c in CREDS)
where = f'''<section class="h-sec" id="where" aria-labelledby="where-h"><div class="wrap">
<div class="ab-where"><div>
{eyebrow("Where we are")}<h2 id="where-h" class="h-h2 h-h2--sm" data-reveal>One delivery team in India. Clients in six countries.</h2>
<p class="ab-side" data-reveal style="--d:1">Working hours are agreed in each pilot plan, and your pod&rsquo;s analyst is your single point of contact.</p>
<ul class="ab-places" data-reveal style="--d:2">{places}</ul>
<address class="ab-addr" data-reveal style="--d:3"><span class="h-col">Office</span>Upcore Technologies, Unit No. 625, 6th Floor, Tower-A, Bestech Business Tower, Sector 66, Mohali, Punjab 160062, India</address>
</div>{MAP}</div>
<div class="ab-creds-wrap"><p class="h-col">Credentials</p><ul class="ab-creds">{creds}</ul>
<a class="link" href="/security">How we handle security</a></div>
</div></section>'''

# ------------------------------------------------------------------ 7. CTA
final = f'''<section class="band band--flow cta-band h-cta" aria-labelledby="cta-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
<h2 id="cta-h" class="t-display" data-reveal>Talk to the people <span class="hl">who will do the work.</span></h2>
<p class="t-lead" data-reveal style="--d:1">Book a 45-minute discovery call with Gaurav or Saswata. You&rsquo;ll get a written plan, whether or not we work together.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("cta_final", cls="btn btn--cyan")}</div>
<p class="cta-alt" data-reveal style="--d:3">Prefer to write first? <a href="/contact">Contact us <span aria-hidden="true">&rarr;</span></a></p>
</div></section>'''

page = '\n'.join([hero, why, what, believe, team, where, final])
people = [{'@type': 'Person', 'name': n, 'jobTitle': r.split(' &middot; ')[0].replace('&amp;', '&'), 'sameAs': [u], 'worksFor': {'@id': C.ORG_ID}} for ini, n, r, b, u in TEAM]
ld = C.graph('about', [{'@type': 'AboutPage', 'name': 'About Upcore Technologies', 'url': C.SITE + C.FINAL_URL['about'], 'about': {'@id': C.ORG_ID}}] + people, crumb='About')
print('about', C.write('about.html', 'about', 'About Upcore: Leadership, Convictions &amp; Credentials | Upcore',
      'Upcore builds governed AI-native engineering and automation for clients in six countries. Meet the leadership, what we believe and our credentials.',
      page, active='about', ld=ld, group='company', spine=False, main_cls='is-calm'))
