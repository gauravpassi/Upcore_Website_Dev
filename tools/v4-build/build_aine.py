"""AI-Native Engineering page (2026-10-07, calm rebuild). The deep page a CTO reads after the homepage:
leadership-view hero -> nine-stage explorer -> options compared -> the pod -> how we engage ->
engineering results -> FAQ -> CTA. Replaces the old build_v41.py.
Run from the repo root: python tools/v4-build/build_aine.py"""
import os, sys, re, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import tools as TL
import flow as FL
from v4parts import TESTIMONIALS

ARROW = C.ARROW


def eyebrow(t):
    return f'<p class="h-eyebrow" data-reveal>{t}</p>'


# ------------------------------------------------------------------ 1. hero + leadership view
DEV = [('#412', 'New endpoint skips your API versioning rule', 'hi', 'High', 'Stopped at the pull request, rebuilt under v2'),
       ('#188', 'Migration adds an optional column the schema marks required', 'md', 'Medium', 'Spec amended, decision recorded'),
       ('#77', 'Button style outside your design system', 'lo', 'Low', 'Fixed automatically, then merged'),
       ('#903', 'Fix touches a shared sign-in module outside the spec', 'hi', 'High', 'Held for approval, split into two changes')]
KPI = [('142', 'changes shipped'), ('61%', 'merged automatically'), ('9', 'held for a person'), ('4', 'rule deviations logged')]
kpis = ''.join(f'<div><b data-count>{v}</b><span>{l}</span></div>' for v, l in KPI)
rows = ''.join(f'<li class="dv-row" style="--i:{i}"><code>{a}</code><span class="dv-t">{b}</span><span class="dv-risk r-{c}">{d}</span><span class="dv-dec">{e}</span></li>' for i, (a, b, c, d, e) in enumerate(DEV))
DASH = f'''<figure class="dash" data-dash>
<p class="sr">Example leadership view with illustrative data: this week 142 changes shipped, 61% merged automatically, 9 held for a person and 4 deviations from your architecture rules logged, each with its risk and the decision taken.</p>
<div class="dash-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>Engineering delivery &middot; this week</span><span class="gate-pr">Leadership view</span></div>
<div class="dash-kpis">{kpis}</div>
<div class="dash-log"><div class="dash-log-h"><b>Deviation log</b><span>Every change that broke one of your rules, and what was decided</span></div><ol class="dv">{rows}</ol></div>
</div>
<figcaption><span>Example with illustrative data</span><button class="gate-toggle dash-toggle" type="button" aria-label="Pause animation">Pause</button></figcaption>
</figure>'''

PROOF_STRIP = '''<ul class="h-proof" aria-label="Certifications and ratings">
<li><img src="/images/accolades/light/iso27001.svg" alt="" width="26" height="26" /><span>ISO 27001</span></li>
<li><img src="/images/accolades/light/iso9001.svg" alt="" width="26" height="26" /><span>ISO 9001</span></li>
<li><img src="/images/accolades/light/cmmi.svg" alt="CMMI Level 3" width="46" height="26" /></li>
<li><a href="https://clutch.co/profile/upcore-technologies" target="_blank" rel="noopener"><span>Clutch 5.0&#9733;</span><span class="sr"> (opens in a new tab)</span></a></li>
<li><span>Claude Certified Architects</span></li>
</ul>'''

hero = f'''<section class="h-hero h-hero--long" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap h-hero-in">
<div class="h-hero-copy">
<nav class="crumb" aria-label="Breadcrumb" data-reveal><ol><li><a href="{C.URL["home"]}">Home</a></li><li aria-current="page">AI-Native Engineering</li></ol></nav>
<p class="h-eyebrow" data-reveal>AI-Native Engineering &middot; for CTOs and CIOs</p>
<h1 id="hero-h" class="t-hero" data-split>AI-native engineering, <span class="hl">governed from spec to production.</span></h1>
<p class="t-lead" data-reveal style="--d:3">We install a governed delivery pipeline inside your Jira or Linear, GitHub and CI/CD, and embed a Claude Certified Architect to run it with your team. You see every change that breaks one of your rules, why, and who decided.</p>
<div class="hero-ctas" data-reveal style="--d:4">{C.btn("hero", pulse=True)}<a class="link" href="#pipeline">See the nine stages</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes &middot; a written plan, whether or not we work together</p>
</div>
<div class="h-hero-vis" data-reveal="scale" style="--d:2"><div class="gate-stage" data-tilt>{DASH}</div></div>
</div>
<div class="wrap">{PROOF_STRIP}</div></section>'''

# ------------------------------------------------------------------ 2. nine-stage explorer
WHO = {'auto': ('Automated check', 'auto'), 'ai': ('AI step', 'ai'), 'person': ('A person decides', 'person')}
STAGES = [
    ('Spec from a template', 'Every change, including bug fixes, starts as a written spec in Jira or Linear: scope, acceptance criteria, the services it touches and any data changes.',
     ['auto'], ['Scope written', 'Acceptance criteria you can test', 'Services and data changes listed'], ['jira', 'linear']),
    ('Architecture check', 'The spec is checked against the architecture rules you have agreed: your decision records, database schema, API conventions and design system. Conflicts show up before any code exists.',
     ['auto'], ['Your decision records', 'Database schema', 'API conventions and design system'], ['github', 'confluence']),
    ('Plan and architect sign-off', 'AI drafts an implementation plan covering files, interfaces, data migrations and tests. An architect approves the plan before any build starts.',
     ['ai', 'person'], ['Files and interfaces', 'Data migrations', 'Test plan'], ['claude', 'githubcopilot', 'cursor']),
    ('Build and test in a sandbox', 'Code is written and run in an isolated sandbox. AI writes tests from the acceptance criteria, and they must pass before a pull request is opened.',
     ['ai'], ['Isolated environment', 'Tests written from the spec', 'Tests pass first'], ['githubactions', 'gitlab', 'jenkins']),
    ('Pull-request checks', 'Each pull request is checked automatically: a clear description and linked ticket, your architecture rules, security scanning and minimum test coverage.',
     ['auto'], ['Your architecture rules', 'Security scanning', 'Minimum test coverage'], ['github', 'sonarqube', 'snyk']),
    ('Risk-scored merge', 'Every change gets a risk score based on how far it departs from your rules. Low-risk changes merge on their own; anything over your limit goes to a named approver.',
     ['auto', 'person'], ['A risk score for every change', 'The limit you set', 'A named approver above it'], ['github', 'gitlab']),
    ('Staging and scenario tests', 'The change runs in staging against a fixed set of known-good tasks and edge cases, not just unit tests.',
     ['auto'], ['Known-good tasks replayed', 'Edge cases', 'Results recorded'], ['githubactions', 'jenkins']),
    ('Feature-flagged release', 'The change goes to a small share of users behind a feature flag and is watched against your normal error rates, speed and cost before it is rolled out further or rolled back.',
     ['auto', 'person'], ['A small first rollout', 'Errors, speed and cost watched', 'Rolled out further or rolled back'], ['datadog', 'sentry']),
    ('Feedback loop', 'Tickets, decisions and incidents are linked automatically, so the next spec starts with the full history of what came before.',
     ['ai'], ['Decisions linked', 'Incidents linked', 'Context for the next spec'], ['jira', 'linear', 'confluence']),
]
tabs = ''.join(
    f'<button type="button" class="stx-tab{" is-on" if i == 0 else ""}" role="tab" id="stx-t{i}" aria-controls="stx-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
    f'<span class="stx-n">{i + 1:02d}</span><span class="stx-name">{t}</span><span class="stx-who">{"".join(f"<i class={chr(34)}w-{w}{chr(34)}></i>" for w in who)}</span></button>'
    for i, (t, d, who, chk, tl) in enumerate(STAGES))
panels = ''.join(
    f'<div class="stx-panel{" is-on" if i == 0 else ""}" role="tabpanel" id="stx-p{i}" aria-labelledby="stx-t{i}"{"" if i == 0 else " hidden"}>'
    f'<span class="stx-k">Stage {i + 1} of {len(STAGES)}</span><h3 class="stx-h">{t}</h3><p class="stx-d">{d}</p>'
    f'<div class="stx-meta"><div><span class="h-col">Who decides</span><ul class="stx-who-l">{"".join(f"<li class={chr(34)}w-{w}{chr(34)}><i></i>{WHO[w][0]}</li>" for w in who)}</ul></div>'
    f'<div><span class="h-col">What is checked</span><ul class="stx-chk">{"".join(f"<li>{c}</li>" for c in chk)}</ul></div>'
    f'<div><span class="h-col">Runs in</span><div class="logos">{"".join(TL.logo(x, small=True) for x in tl)}</div></div></div></div>'
    for i, (t, d, who, chk, tl) in enumerate(STAGES))
pipeline = f'''<section class="h-sec h-sec--alt" id="pipeline" aria-labelledby="pipe-h"><div class="wrap">
{eyebrow("What gets installed")}
<div class="h-head"><h2 id="pipe-h" class="h-h2" data-reveal>Nine stages from spec to production, inside your own tools.</h2>
<p class="h-lead" data-reveal style="--d:1">Checks are automated where your rules are clear and handed to a person where judgment matters. <span class="stx-hint">Choose a stage to see what happens in it.</span></p></div>
<div class="stx" data-stages data-reveal><div class="stx-tabs" role="tablist" aria-label="Pipeline stages">{tabs}<span class="stx-rail" aria-hidden="true"><i></i></span></div>
<div class="stx-stage">{panels}</div></div>
<div class="stx-legend" aria-hidden="true"><span><i class="w-auto"></i>Automated check</span><span><i class="w-ai"></i>AI step</span><span><i class="w-person"></i>A person decides</span></div>
<p class="stx-note">Autonomy is earned, not assumed: merge limits start strict and loosen only as the pipeline proves itself on your own work.</p>
</div></section>'''

# ------------------------------------------------------------------ 3. options compared
CMP = [('What you get', 'Code suggestions in each developer&rsquo;s editor', 'Whatever your platform team has time to build', 'The full pipeline: specs, rules, checks, merge limits, releases and a decision log'),
       ('Who reviews AI-written code', 'Senior engineers, line by line', 'Depends on the checks you build', 'Automated checks first; people review what is risky'),
       ('Your architecture rules', 'Not checked', 'Checked if you build and maintain the checks', 'Checked at the spec, the plan and every pull request'),
       ('What leadership sees', 'Usage statistics, not what changed or why', 'Dashboards you build and maintain', 'A deviation log and dashboard from the first pilot'),
       ('Who maintains the rules', 'Each team, informally', 'Your platform team, alongside its roadmap', 'An embedded Claude Certified Architect, with your team')]
COLS = ['AI coding tools alone', 'Build it yourself', 'With Upcore']
cmp_rows = ''.join(
    f'<div class="cmp-row" role="row" data-reveal style="--d:{i % 3}"><div class="cmp-k" role="rowheader">{k}</div>'
    + ''.join(f'<div class="cmp-c{" is-us" if j == 2 else ""}" role="cell"><span class="cmp-l">{COLS[j]}</span>{v}</div>' for j, v in enumerate((a, b, c)))
    + '</div>' for i, (k, a, b, c) in enumerate(CMP))
compare = f'''<section class="h-sec" id="compare" aria-labelledby="cmp-h"><div class="wrap">
{eyebrow("Your options")}
<h2 id="cmp-h" class="h-h2" data-reveal>AI tools write the code. Something has to govern it.</h2>
<div class="cmp" role="table" aria-label="AI coding tools alone, building it yourself, and Upcore compared">
<div class="cmp-row cmp-head" role="row"><div role="columnheader"><span class="sr">Question</span></div>{"".join(f'<div class="cmp-c{" is-us" if j == 2 else ""}" role="columnheader">{c}</div>' for j, c in enumerate(COLS))}</div>
{cmp_rows}</div>
<p class="cmp-note">Many of the tools are ones you already run. What we add is the installed process from day one, and the people who keep it working. A pilot measures it against your current process before you commit.</p>
<p class="cmp-more"><a class="link" href="{C.URL["cmp-tools"]}">AI-native engineering vs AI coding tools</a><a class="link" href="{C.URL["cmp-inhouse"]}">Build it in-house, or bring in Upcore?</a><a class="link" href="{C.URL["guide-aine"]}">What is AI-native engineering?</a></p>
</div></section>'''

# ------------------------------------------------------------------ 4. the pod
POD_ICONS = {'dev': '<path d="m8 7-5 5 5 5M16 7l5 5-5 5"/>', 'arch': '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>', 'ba': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c1.8.8 3 2.6 3.5 5.2"/>'}
POD = [('dev', 'Full-stack developer', 'Runs the pipeline day to day: drafts specs with your team, supervises what AI builds and keeps the checks green.'),
       ('arch', 'Claude Certified Architect', 'Maintains your architecture rules with your team, signs off plans, tunes the merge limits you set and reviews every high-risk deviation.'),
       ('ba', 'Analyst &amp; client lead', 'Turns business requests into specs, runs acceptance with your stakeholders and is your single point of contact.')]
pod = ''.join(f'<li class="pod-p{" is-lead" if k == "arch" else ""}" data-reveal style="--d:{j}"><span class="pod-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{POD_ICONS[k]}</svg></span><h3 class="t-h3">{t}</h3><p>{p}</p></li>' for j, (k, t, p) in enumerate(POD))
team = f'''<section class="h-sec h-sec--tight" id="team" aria-labelledby="pod-h"><div class="wrap">
{eyebrow("Who does the work")}
<div class="h-head"><h2 id="pod-h" class="h-h2" data-reveal>Three people, embedded in your delivery.</h2>
<p class="h-lead" data-reveal style="--d:1">Every Upcore architect is Claude certified. To scale, we add pods rather than enlarging one, so each team gets the pipeline, the rules and the judgment.</p></div>
<div class="pod-line"><span class="pod-wire" aria-hidden="true"></span><ol>{pod}</ol></div></div></section>'''

# ------------------------------------------------------------------ 5. how we engage
STEPS = [('Pilot on one team', 'One team, one service, a real backlog. Prove it on real work before you commit further.'),
         ('One-time implementation', 'A fixed fee scaled to the teams and repositories in scope: pipeline, checks, templates, dashboard and training.'),
         ('Monthly retainer', 'An embedded Claude Certified Architect maintains your rules, tunes checks and limits, and reviews high-risk deviations as your system evolves.')]
SPEC = [('Your pod', 'A full-stack developer, a Claude Certified Architect and an analyst who is your single point of contact.'),
        ('Measured against', 'Success measures agreed up front against your current delivery process.'),
        ('You get', 'The pipeline installed end to end, then a results review with you before any wider rollout.'),
        ('Duration &amp; commercials', 'Agreed on the discovery call, based on your scope and requirements.')]
spec = ''.join(f'<div data-reveal style="--d:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(SPEC))
engage = f'''<section class="h-sec" id="engagement" aria-labelledby="eng-h"><div class="wrap">
{eyebrow("How we engage")}
<div class="h-head"><h2 id="eng-h" class="h-h2" data-reveal>Start with a pilot. Scale on evidence.</h2>
<p class="h-lead" data-reveal style="--d:1">No price list. Every engagement is scoped after the discovery call, and you get a written proposal with a fixed scope and price before any build starts.</p></div>
{FL.timeline(STEPS)}
<div class="h-pilot h-pilot--eng"><div class="h-pilot-k"><p class="h-col">The pilot, specified</p><div class="hero-ctas" data-reveal>{C.btn("engagement")}</div></div><dl class="h-pilot-spec">{spec}</dl></div>
</div></section>'''

# ------------------------------------------------------------------ 6. results
RES = [('Engineering', 'In production', 'delivery agents inside a product team', 'Field-service SaaS platform, part of a ServiceNow Elite partner group', 'South Africa'),
       ('Engineering', '4.9&#9733;', 'App Store rating, 89 ratings', 'Booking and payments app built with AI-assisted engineering', 'United Kingdom'),
       ('Engineering', 'Rehired', 'to add test and DevOps agents to their release pipeline', 'Dental implant network across nine states', 'United States')]
res = ''.join(f'<li data-reveal style="--d:{i}"><span class="h-tag">{tg}</span><b data-count{" class=is-word" if not any(ch.isdigit() for ch in n) else ""}>{n}</b><span class="what">{w}</span><span class="who">{who} &middot; {geo}</span></li>' for i, (tg, n, w, who, geo) in enumerate(RES))
q = TESTIMONIALS['eng'][0]
proof = f'''<section class="band h-sec h-proof-band" aria-labelledby="res-h"><div class="spot" aria-hidden="true"></div><div class="wrap">
{eyebrow("Results")}
<h2 id="res-h" class="h-h2" data-reveal>Engineering work in production.</h2>
<ul class="h-results">{res}</ul>
<figure class="h-quote" data-reveal><span class="h-qmark" aria-hidden="true">&ldquo;</span><blockquote><p>I have worked with Upcore many times on projects big and small. Their expertise, network, and professionalism is second to none.</p></blockquote><figcaption>{q[1]}</figcaption></figure>
<div class="h-proof-foot"><a class="link" href="{C.URL["results"]}">See all results</a><span>Client names withheld. Results as reported from our engagements; ask us for a reference call.</span></div>
</div></section>'''

# ------------------------------------------------------------------ 7. FAQ
FAQ = [
    ('How is this different from giving developers Copilot or Cursor?', 'Those tools generate code. AI-native engineering is the delivery process around them: the spec template, the architecture checks, the plan sign-off, the automated pull-request checks, the merge rules, the scenario tests, the controlled release and the decision record. Without that process, AI-written code still depends on manual review to be trusted.'),
    ('Couldn&rsquo;t our platform team build this ourselves?', 'You could, and many of the tools are ones you already run. What we add is the installed process from day one: spec templates, architecture checks, the plan sign-off, merge limits and the deviation log, plus an embedded Claude Certified Architect who maintains your architecture rules and tunes the checks as your system evolves. The pilot measures it against your current process before you commit.'),
    ('Do we have to replace our tools?', 'No. We install the process inside what you already run: Jira or Linear, GitHub, your existing CI/CD and the AI assistants you have approved, such as Claude, GitHub Copilot or Cursor.'),
    ('Who decides when AI-written code can merge?', 'You do. You set the merge limits. Only low-risk changes that follow your architecture rules merge on their own; everything above the limit goes to a named approver, and every decision is recorded on the dashboard.'),
    ('What happens to our engineers&rsquo; roles?', 'They stop hand-writing routine code and prompts and move up a level: writing and reviewing specs, approving plans, owning architecture rules and handling the changes that genuinely need human judgment.'),
    ('How do you handle security and intellectual property?', f'Code stays in your repositories and builds run in your environments. Security scanning is a mandatory check and builds run in sandboxes. Our security and quality management are certified to ISO 27001 and ISO 9001. <a class="link" href="/security">Security details</a>'),
    ('Where is your team, and how do you work across time zones?', 'Our delivery team is in India, with clients in the USA, UK, South Africa, Australia and Mauritius. Your pod&rsquo;s analyst is your single point of contact, and working hours are agreed in the pilot plan.'),
    ('What does it cost?', 'We don&rsquo;t publish a price list. You start with a pilot on one team, then a one-time implementation fee scaled to the teams and repositories in scope, then a monthly retainer for your embedded Claude Certified Architect. Duration and commercials are agreed on the discovery call, and you get a written proposal with a fixed scope and price before any build starts.'),
]
fq = ''.join(f'<details><summary>{a}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{b}</p></div></details>' for a, b in FAQ)
faq = f'''<section class="h-sec" aria-labelledby="faq-h"><div class="wrap h-faq">
<div>{eyebrow("Questions")}<h2 id="faq-h" class="h-h2 h-h2--sm" data-reveal>Before you book a call.</h2></div>
<div class="faq">{fq}</div></div></section>'''

# ------------------------------------------------------------------ 8. CTA
final = f'''<section class="band band--flow cta-band h-cta" aria-labelledby="cta-h">{FL.cta_lines()}<div class="spot" aria-hidden="true"></div><div class="wrap">
<h2 id="cta-h" class="t-display" data-reveal>Put AI-written code <span class="hl">under your architecture&rsquo;s control.</span></h2>
<p class="t-lead" data-reveal style="--d:1">Book a 45-minute discovery call. We&rsquo;ll review your delivery process and send a written plan for a pilot on one team, whether or not we work together.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("cta_final", cls="btn btn--cyan")}</div>
<p class="cta-alt" data-reveal style="--d:3">Not ready for a call? <a href="/lp/governance-index?utm_source=website&amp;utm_medium=ai-native-engineering&amp;utm_campaign=cta_secondary">Get your AI Governance Score in 2 minutes <span aria-hidden="true">&rarr;</span></a></p>
</div></section>'''

page = '\n'.join([hero, pipeline, compare, team, engage, proof, faq, final])
ld = C.graph('aine', [
    {'@type': 'Service', 'name': 'AI-Native Engineering', 'serviceType': 'Governed AI software delivery', 'url': C.SITE + C.FINAL_URL['aine'], 'provider': {'@id': C.ORG_ID},
     'description': 'Installation of a governed, end-to-end AI-native software delivery pipeline inside existing engineering tools, with architecture checks, automated pull-request checks, risk-scored merges, controlled releases and a leadership dashboard.',
     'audience': {'@type': 'Audience', 'audienceType': 'CTOs and CIOs'}, 'areaServed': C.AREA},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': H.unescape(a), 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', H.unescape(b))}} for a, b in FAQ]}],
    crumb='AI-Native Engineering')
print('aine', C.write('ai-native-engineering.html', 'aine', 'AI-Native Engineering: Governed Software Delivery | Upcore',
      'A governed spec-to-production AI pipeline inside Jira or Linear, GitHub and CI/CD, with architecture checks, controlled releases and a leadership view.',
      page, active='aine', ld=ld, group='solution', spine=False, main_cls='is-calm'))
