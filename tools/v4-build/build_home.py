"""Homepage (2026-10-06 rethink): one buyer, one story, one action.
CTO/CIO lens, competitor-informed: outcome hero with a real artifact -> proof strip -> problem ->
how it works (4 checkpoints, artifacts not paragraphs) -> number-led proof -> the pilot ->
compact router -> 4 objection FAQs -> final CTA with the people you'll meet.
Depth lives on /ai-native-engineering, /results and the segment pages.
Run from the repo root: python tools/v4-build/build_home.py"""
import os, sys, re, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import tools as TL
import flow as FL
from v4parts import TESTIMONIALS

ARROW = C.ARROW
CHECK = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def eyebrow(t):
    return f'<p class="h-eyebrow" data-reveal>{t}</p>'


# ------------------------------------------------------------------ 1. hero + artifact
GATE = f'''<div class="gate-stage" data-tilt>
<figure class="gate" data-gate>
<div class="gate-tabs" role="group" aria-label="Example scenario">
<button type="button" class="gate-tab" data-sc="0" aria-pressed="true">Routine change</button>
<button type="button" class="gate-tab" data-sc="1" aria-pressed="false">Risky change</button><span class="gate-ink" aria-hidden="true"></span></div>
<p class="sr">Example. A routine change passes every check and merges automatically because its risk score is under your limit. A risky change breaks one of your architecture rules, scores above your limit and is held for an architect. Both decisions are logged.</p>
<div class="gate-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span data-g="repo">Payments service</span><span class="gate-pr" data-g="pr">Pull request #418</span></div>
<div class="gate-title"><b data-g="title">Add partial refunds to checkout</b><span data-g="sub">Written with AI &middot; checked by your pipeline</span></div>
<ul class="gate-checks">
<li class="ok"><i class="st"></i><span class="k">Linked to its spec</span><span class="v" data-g="c0">Template complete</span></li>
<li class="ok"><i class="st"></i><span class="k">Architecture rules</span><span class="v" data-g="c1">Follows your API conventions</span></li>
<li class="ok"><i class="st"></i><span class="k">Security scan</span><span class="v" data-g="c2">No issues found</span></li>
<li class="ok"><i class="st"></i><span class="k">Test coverage</span><span class="v" data-g="c3">87% (minimum 80%)</span></li>
</ul>
<div class="gate-risk"><span class="k">Risk score</span><span class="meter"><i style="--v:12%"></i><b><em>Your limit</em></b></span><span class="v" data-g="risk">12 / 100</span></div>
<div class="gate-out ok" data-g="outwrap"><span class="tag" data-g="tag">Merged</span><span data-g="out">Under your risk limit, so it merged automatically</span></div>
</div>
<div class="gate-log" data-g="log" aria-hidden="true"><span class="gl-dot"></span><span class="gl-k">Decision log</span><span class="gl-t" data-g="logt">#418 merged automatically &middot; risk 12</span></div>
<figcaption><span>Example with illustrative data</span><button class="gate-toggle" type="button" aria-label="Pause animation">Pause</button></figcaption>
</figure></div>'''

PROOF_STRIP = '''<ul class="h-proof" aria-label="Certifications and ratings">
<li><img src="/images/accolades/light/iso27001.svg" alt="" width="26" height="26" /><span>ISO 27001</span></li>
<li><img src="/images/accolades/light/iso9001.svg" alt="" width="26" height="26" /><span>ISO 9001</span></li>
<li><img src="/images/accolades/light/cmmi.svg" alt="CMMI Level 3" width="46" height="26" /></li>
<li><a href="https://clutch.co/profile/upcore-technologies" target="_blank" rel="noopener"><span>Clutch 5.0&#9733;</span><span class="sr"> (opens in a new tab)</span></a></li>
<li><a href="https://www.designrush.com/agency/profile/upcore-technologies" target="_blank" rel="noopener"><span>DesignRush 5.0&#9733;</span><span class="sr"> (opens in a new tab)</span></a></li>
<li><span>Claude Certified Architects</span></li>
</ul>'''

hero = f'''<section class="h-hero" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap h-hero-in">
<div class="h-hero-copy">
<p class="h-eyebrow" data-reveal>AI-Native Engineering &middot; for CTOs and CIOs</p>
<h1 id="hero-h" class="t-hero" data-split>AI writes the code. <span class="hl">Your architecture stays in charge.</span></h1>
<p class="t-lead" data-reveal style="--d:3">We install a governed delivery pipeline in your Jira or Linear, GitHub and CI/CD, so every AI-written change is checked, risk-scored and logged before it ships.</p>
<div class="hero-ctas" data-reveal style="--d:4">{C.btn("hero", pulse=True)}<a class="link" href="#pilot">See how a pilot works</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes with Gaurav or Saswata &middot; a written plan, whether or not we work together</p>
</div>
<div class="h-hero-vis" data-reveal="scale" style="--d:2">{GATE}</div>
</div>
<div class="wrap">{PROOF_STRIP}</div></section>'''

# ------------------------------------------------------------------ 2. problem
ICON = {
    'neck': '<path pathLength="1" d="M3 5h18l-7 8v6l-4 2v-8z"/>',
    'drift': '<path pathLength="1" d="M3 17h18"/><path pathLength="1" d="M3 17c5 0 8-1.5 11-5s4.5-6 7-7"/>',
    'blind': '<path pathLength="1" d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle pathLength="1" cx="12" cy="12" r="3"/><path pathLength="1" d="M4 4l16 16"/>',
}
PAINS = [('neck', 'Review becomes the bottleneck', 'Someone senior reads every AI-written line, so the speed you gained disappears in review.'),
         ('drift', 'Architecture drifts quietly', 'Models don&rsquo;t know your conventions. Small deviations pile up until they are expensive to unwind.'),
         ('blind', 'Leadership can&rsquo;t see the risk', 'Nobody can say what AI changed, why it changed, or who approved it.')]
pains = ''.join(f'<li data-reveal style="--d:{i}"><svg class="h-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICON[k]}</svg><span class="h-n">0{i + 1}</span><h3>{t}</h3><p>{p}</p></li>' for i, (k, t, p) in enumerate(PAINS))
problem = f'''<section class="h-sec" aria-labelledby="prob-h"><div class="wrap">
{eyebrow("The problem")}
<h2 id="prob-h" class="h-h2" data-reveal>Your team ships more AI-written code every week. <span class="mute">Review hasn&rsquo;t caught up.</span></h2>
<ol class="h-pains">{pains}</ol></div></section>'''

# ------------------------------------------------------------------ 3. how it works (4 checkpoints, each with a small artifact)
MINI = {
    'spec': '''<div class="mini" aria-hidden="true"><div class="mini-h"><b>Spec</b><span>Partial refunds</span></div>
<div class="mini-r ok"><i></i>Scope written</div><div class="mini-r ok"><i></i>Acceptance criteria</div><div class="mini-r ok"><i></i>Matches your architecture rules</div></div>''',
    'gate': '''<div class="mini" aria-hidden="true"><div class="mini-h"><b>Checks</b><span>Pull request #418</span></div>
<div class="mini-r ok"><i></i>Architecture rules</div><div class="mini-r ok"><i></i>Security scan</div><div class="mini-r ok"><i></i>Test coverage 87%</div></div>''',
    'merge': '''<div class="mini" aria-hidden="true"><div class="mini-h"><b>Risk score</b><span>Your limit: 30</span></div>
<div class="mini-meter"><i style="--v:12%"></i><b></b></div><div class="mini-r ok"><i></i>Low risk: merged automatically</div><div class="mini-r hold"><i></i>High risk: sent to a named approver</div></div>''',
    'release': '''<div class="mini" aria-hidden="true"><div class="mini-h"><b>Release</b><span>Behind a feature flag</span></div>
<div class="mini-steps"><span class="on">5%</span><span class="on">25%</span><span>100%</span></div><div class="mini-r ok"><i></i>Errors, speed and cost watched</div></div>''',
}
STEPS = [('spec', 'Spec', 'Every change starts from a standard spec in Jira or Linear, checked against your architecture rules before any code exists.'),
         ('gate', 'Gate', 'Automated checks run on every pull request: your architecture rules, security scanning and test coverage.'),
         ('merge', 'Merge', 'Each change gets a risk score. Low risk merges on its own; anything over your limit goes to a named approver.'),
         ('release', 'Release', 'Changes go out behind a feature flag, watched against your normal error rates, speed and cost, and every decision is logged for leadership.')]

ROW = lambda c, k, v: f'<div class="sv-row {c}"><i class="st"></i><span class="k">{k}</span><span class="v">{v}</span></div>'
PANELS = [
    ROW('ok', 'Scope', 'Partial refunds for card payments') + ROW('ok', 'Acceptance criteria', 'Three, written and testable') + ROW('ok', 'Services affected', 'Payments and orders') + ROW('ok', 'Architecture rules', 'No conflicts found'),
    ROW('ok', 'Architecture rules', 'Follows your API conventions') + ROW('ok', 'Security scan', 'No issues found') + ROW('ok', 'Test coverage', '87% (minimum 80%)') + ROW('ok', 'Linked to its spec', 'Template complete'),
    '<div class="sv-meter"><div class="sv-meter-h"><span>Risk score</span><b>12 / 100</b></div><span class="meter"><i style="--v:12%"></i><b><em>Your limit: 30</em></b></span></div>'
    + '<div class="sv-lane is-hot"><span class="tag">Under your limit</span>Merged automatically</div><div class="sv-lane"><span class="tag tag--hold">Over your limit</span>Sent to a named approver</div>',
    '<div class="sv-roll"><span class="sv-roll-k">Rollout</span><div class="sv-bars"><span style="--w:5%"><em>5%</em></span><span style="--w:25%"><em>25%</em></span><span style="--w:100%"><em>100%</em></span></div></div>'
    + ROW('ok', 'Error rate', 'Normal') + ROW('ok', 'Speed', 'Normal') + ROW('ok', 'Cost per request', 'Normal')
    + '<div class="sv-logged"><i class="st st--ok"></i>Decision logged for leadership</div>',
]
story_steps = ''.join(
    f'<li class="story-step{" is-on" if i == 0 else ""}" data-step="{i}"><button type="button" class="story-btn" aria-label="Show step {i + 1}: {t}"><span class="h-n">0{i + 1}</span><span class="story-t">{t}</span></button><p>{p}</p><div class="story-mini" data-reveal>{MINI[k]}</div></li>'
    for i, (k, t, p) in enumerate(STEPS))
pips = ''.join(f'<span class="sv-pip{" on" if i == 0 else ""}">{t}</span>' for i, (_, t, _) in enumerate(STEPS))
panels = ''.join(f'<div class="sv-panel{" on" if i == 0 else ""}" data-p="{i}">{pn}</div>' for i, pn in enumerate(PANELS))
STORY = f'''<div class="story" data-story><ol class="story-steps">{story_steps}</ol>
<div class="story-vis" aria-hidden="true"><div class="story-sticky"><div class="sv">
<div class="sv-top"><span class="gate-dots"><i></i><i></i><i></i></span><b>Add partial refunds to checkout</b><span>Pull request #418</span></div>
<div class="sv-pips">{pips}<span class="sv-track"><i></i></span></div>
<div class="sv-body">{panels}</div></div></div></div></div>'''
works_logos = ''.join(TL.logo(s, small=True) for s in ['jira', 'linear', 'github', 'gitlab', 'githubactions', 'claude', 'githubcopilot', 'cursor'])
how = f'''<section class="h-sec h-sec--alt" id="how" aria-labelledby="how-h"><div class="wrap">
{eyebrow("How it works")}
<div class="h-head"><h2 id="how-h" class="h-h2" data-reveal>Every AI-written change passes four checkpoints.</h2>
<p class="h-lead" data-reveal style="--d:1">Installed inside the tools your teams already use. You set the rules; the pipeline enforces them and a Claude Certified Architect keeps them current.</p></div>
{STORY}
<div class="h-works"><span>Works with</span><div class="logos">{works_logos}</div><a class="link" href="{C.URL["aine"]}#pipeline">See all nine stages</a></div>
</div></section>'''

# ------------------------------------------------------------------ 4. proof (number-led, anonymised)
RESULTS = [('4.9&#9733;', 'App Store rating, 89 ratings', 'Booking and payments app built with AI-assisted engineering', 'United Kingdom'),
           ('60%+', 'fewer delivery-support tickets', 'WhatsApp order-status agent for a 960-store retailer', 'South Africa'),
           ('&asymp;$210K', 'a year of licensed tooling replaced', 'Compliance-check agent for an automotive compliance firm', 'India')]
res = ''.join(f'<li data-reveal style="--d:{i}"><b data-count>{n}</b><span class="what">{w}</span><span class="who">{who} &middot; {geo}</span></li>' for i, (n, w, who, geo) in enumerate(RESULTS))
q = TESTIMONIALS['eng'][0]
quote_txt = 'I have worked with Upcore many times on projects big and small. Their expertise, network, and professionalism is second to none.'
proof = f'''<section class="band h-sec h-proof-band" aria-labelledby="res-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
{eyebrow("Results")}
<h2 id="res-h" class="h-h2" data-reveal>Already running in production.</h2>
<ul class="h-results">{res}</ul>
<figure class="h-quote" data-reveal><span class="h-qmark" aria-hidden="true">&ldquo;</span><blockquote><p>{quote_txt}</p></blockquote><figcaption>{q[1]}</figcaption></figure>
<div class="h-proof-foot"><a class="link" href="/results">See all results</a><span>Client names withheld. Results as reported from our engagements; ask us for a reference call.</span></div>
</div></section>'''

# ------------------------------------------------------------------ 5. pilot
PILOT = [('Scope', 'One team, one service, a real backlog.'),
         ('Your pod', 'A Claude Certified Architect, a full-stack developer and an analyst who is your single point of contact.'),
         ('You get', 'The pipeline installed end to end, measured against your current process, then a results review before any wider rollout.')]
pil = ''.join(f'<div data-reveal style="--d:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(PILOT))
pilot = f'''<section class="h-sec" id="pilot" aria-labelledby="pilot-h"><div class="wrap h-pilot">
<div class="h-pilot-k">{eyebrow("Start small")}
<h2 id="pilot-h" class="h-h2" data-reveal>Prove it on one team before you commit.</h2>
<p class="h-lead" data-reveal style="--d:1">No price list and no long contract up front. Duration and commercials are agreed on the discovery call, based on your scope.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("pilot")}<a class="link" href="{C.URL["aine"]}#engagement">How engagements work</a></div></div>
<dl class="h-pilot-spec">{pil}</dl></div></section>'''

# ------------------------------------------------------------------ 6. router
SEGS = [('tech-software', 'Tech &amp; Software', 'Governed AI delivery for engineering teams'),
        ('ecommerce-retail', 'Ecommerce &amp; Retail', 'Order status, returns, catalog and ad spend'),
        ('operations-heavy', 'Operations-Heavy Businesses', 'Collections, documents and follow-ups'),
        ('professional-services', 'Professional Services', 'Accounting, law, wealth and staffing')]
SOLS = [('gov', 'AI Governance', 'Spend, data controls and audit trails'),
        ('bpa', 'Business Process Automation', 'Agents for repetitive operations work'),
        ('fao', 'Fractional AI Officer', 'An embedded AI lead on retainer')]
lk = lambda k, t, d: f'<li><a href="{C.URL[k]}"><b>{t}</b><span>{d}</span><i aria-hidden="true">{ARROW}</i></a></li>'
router = f'''<section class="h-sec h-sec--tight" id="who-we-help" aria-labelledby="who-h"><div class="wrap">
<div class="h-router-head"><h2 id="who-h" class="h-h3">Not leading an engineering team?</h2><p>The same governed approach runs AI across the rest of the business.</p></div>
<div class="h-router" id="segments"><div><p class="h-col">Who we help</p><ul>{"".join(lk(*s) for s in SEGS)}</ul></div>
<div><p class="h-col">Also from Upcore</p><ul>{"".join(lk(*s) for s in SOLS)}</ul></div></div></div></section>'''

# ------------------------------------------------------------------ 7. objections
FAQ = [('How is this different from giving developers Copilot or Cursor?', 'Those tools generate code. We install the delivery process around them: spec templates, architecture guardrails, plan sign-off, automated pull-request gates, risk-scored merges, controlled releases and a decision record. Without that process, AI-written code still depends on manual review to be trusted.'),
       ('Is our code and data safe with you?', 'Code stays in your repositories and builds run in your environments, with security scanning as a mandatory gate. Model providers are configured so your data is not used to train their models. Our security and quality management are certified to ISO 27001 and ISO 9001. <a class="link" href="/security">Security details</a>'),
       ('Where is your team, and how do you handle time zones?', 'Our delivery team is in India, with clients in the USA, UK, South Africa, Australia and Mauritius. Your pod&rsquo;s analyst is your single point of contact, and working hours are agreed in the pilot plan.'),
       ('What does it cost?', 'We don&rsquo;t publish a price list. You start with a pilot on one team; duration and commercials are agreed on the discovery call. After the call you get a written proposal with a fixed scope and price before any build starts.')]
fq = ''.join(f'<details><summary>{a}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{b}</p></div></details>' for a, b in FAQ)
faq = f'''<section class="h-sec" aria-labelledby="faq-h"><div class="wrap h-faq">
<div>{eyebrow("Questions")}<h2 id="faq-h" class="h-h2 h-h2--sm" data-reveal>What CTOs ask us first.</h2></div>
<div class="faq">{fq}</div></div></section>'''

# ------------------------------------------------------------------ 8. final CTA
final = f'''<section class="band band--flow cta-band h-cta" aria-labelledby="cta-h">{FL.cta_lines()}<div class="spot" aria-hidden="true"></div><div class="wrap">
<h2 id="cta-h" class="t-display" data-reveal>Make AI-written code something <span class="hl">your architects can sign off on.</span></h2>
<p class="t-lead" data-reveal style="--d:1">Book a 45-minute discovery call. We&rsquo;ll review your delivery process and send a written plan for a pilot on one team, whether or not we work together.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("cta_final", cls="btn btn--cyan")}</div>
<p class="cta-alt" data-reveal style="--d:3">Not ready for a call? <a href="/lp/governance-index?utm_source=website&amp;utm_medium=home&amp;utm_campaign=cta_secondary">Get your AI Governance Score in 2 minutes <span aria-hidden="true">&rarr;</span></a></p>
</div></section>'''

home = '\n'.join([hero, problem, how, proof, pilot, router, faq, final])
ld = C.graph('home', [{'@type': 'WebSite', '@id': C.SITE + '/#website', 'url': C.SITE + '/', 'name': 'Upcore Technologies', 'publisher': {'@id': C.ORG_ID}},
                      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': H.unescape(a), 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', H.unescape(b))}} for a, b in FAQ]}])
print('home', C.write('index.html', 'home', 'AI-Native Engineering &amp; Automation | Upcore Technologies',
      'Governed AI-native software delivery inside Jira or Linear, GitHub and CI/CD: every AI-written change checked, risk-scored and logged. Start with a pilot.',
      home, active='home', ld=ld, group='home', spine=False, main_cls='is-calm'))
