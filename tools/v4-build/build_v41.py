"""Build the V4.1 homepage (AI-Native Engineering flagship) and the AI-Native Engineering page.
Post-audit version (2026-10-06): CRO, copy, design/motion and GTM fixes applied."""
import os, sys, re, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import frameworks as F
import tools as TL
from v4parts import TRUST, TESTIMONIALS, quotes, faq_sec, LEADERS, cta

ARROW = C.ARROW
NB = lambda s: s.replace('AI-native', '<span class="nw">AI-native</span>')


def head(eyebrow, h2, lead='', split=True, hid=''):
    l = f'<p class="t-lead" data-reveal style="--d:1">{lead}</p>' if lead else ''
    i = f' id="{hid}"' if hid else ''
    if split and lead:
        return f'<div class="sec-head sec-head--split"><div><div class="eyebrow" data-reveal>{eyebrow}</div><h2{i} class="t-h2" data-reveal>{h2}</h2></div>{l}</div>'
    return f'<div class="sec-head"><div class="eyebrow" data-reveal>{eyebrow}</div><h2{i} class="t-h2" data-reveal>{h2}</h2>{l}</div>'


GATE = {'auto': 'chip--auto', 'human': 'chip--human', 'ai': 'chip--ai'}
STAGES = [
    ('Spec from template', 'A technical spec is written in Jira or Linear from a standard template: scope, acceptance criteria, affected services and data changes. Bugs follow the same path, so a fix is specified before it is coded.', [('auto', 'Template enforced')]),
    ('Architecture guardrail check', 'The spec is checked against your agreed architecture rules: architecture decision records (ADRs), the database schema, API conventions and the design system. Conflicts surface before a line of code exists.', [('auto', 'Automated check')]),
    ('Plan and architect sign-off', 'AI produces an implementation plan covering files, interfaces, migrations and tests. An architect signs off the plan before any build starts.', [('ai', 'AI plans'), ('human', 'Architect sign-off')]),
    ('Build and test in a sandbox', 'Code is generated and run in an isolated sandbox. The AI writes test cases from the acceptance criteria, and they must pass before a pull request exists.', [('ai', 'AI-written tests')]),
    ('Pull-request gates', 'Pull-request hygiene is checked first: description, linked ticket, scope. Then automated gates run: architecture fitness functions (automated tests that check code against your architecture rules), static application security testing (SAST) and test-coverage thresholds.', [('auto', 'Architecture fitness'), ('auto', 'SAST'), ('auto', 'Coverage')]),
    ('Risk-scored merge rules', 'Every change receives a risk score based on how far it departs from your rules. Low-risk changes that conform can auto-merge; anything above your threshold goes to a named approver.', [('auto', 'Auto-merge'), ('human', 'Named approver')]),
    ('Staging and scenario testing', 'The change deploys to staging, where an evaluation harness replays a fixed set of known-good tasks (golden tasks) and edge cases against the running system, not just unit tests.', [('auto', 'Golden tasks'), ('auto', 'Edge cases')]),
    ('Feature-flagged release', 'The release goes to a small share of traffic behind a feature flag. Errors, latency and cost are monitored against baseline, ending in promote or roll back.', [('auto', 'Monitored'), ('human', 'Promote or roll back')]),
    ('Feedback loop', 'Related tickets, decisions and incidents are linked automatically, so the next spec starts with the full context of everything before it.', [('ai', 'Auto-linked context')]),
]
PIPE_LOGOS = ['jira', 'linear', 'github', 'gitlab', 'githubactions', 'jenkins', 'claude', 'githubcopilot', 'cursor', 'powerautomate', 'sonarqube', 'snyk', 'sentry', 'datadog']


def pipeline(compact, link=False):
    st = ''.join(
        f'<li class="pipe-stage{" is-human" if any(k == "human" for k, _ in g) else ""}"><span class="pipe-dot" aria-hidden="true"></span><div class="pipe-body"><h3><span class="sr">Stage {i}: </span>{t}</h3>'
        + ('' if compact else f'<p>{d}</p>')
        + '<div class="pipe-gates">' + ''.join(f'<span class="chip {GATE[k]}"><span class="dot"></span>{l}</span>' for k, l in g) + '</div></div></li>'
        for i, (t, d, g) in enumerate(STAGES, 1))
    logos = TL.row(PIPE_LOGOS, small=True)[:-6] + '<span class="logo logo--sm"><span>Feature flags</span></span></div>'
    more = f'<p style="margin-top:26px"><a class="link" href="{C.URL["aine"]}#pipeline">See every stage in detail</a></p>' if link else ''
    return f'''<section class="band band--rounded sec" id="pipeline" aria-labelledby="pipe-h"><div class="spot" aria-hidden="true"></div><div class="grid-bg" aria-hidden="true"></div><div class="wrap">
<div class="pipe-wrap"><div class="pipe-intro"><div class="eyebrow">The pipeline</div><h2 id="pipe-h" class="t-h2">Spec to production in <span class="hl">nine governed stages.</span></h2>
<p class="t-lead" style="margin-top:18px">Every stage runs inside the tools your teams already use. Gates are automated where the rules are clear and human where judgment matters.</p>
<div class="pipe-tools">{logos}</div>
<div class="pipe-legend"><span><i class="auto"></i>Automated gate</span><span><i class="human"></i>Human decision</span><span><i class="ai"></i>AI step</span></div>{more}</div>
<ol class="pipe{" pipe--compact" if compact else ""}" data-pipe>{st}</ol></div></div></section>'''


VS = [
    ('Requirements', 'Prompts in a chat window nobody can audit', 'Specs from a standard template in Jira or Linear'),
    ('Architecture', 'Whatever the model suggests', 'Checked against your architecture decision records (ADRs), schema, API conventions and design system'),
    ('Review', 'A senior engineer reads every AI-written line', 'Automated architecture, security and coverage gates; people review what is risky'),
    ('Merging', 'Decided by feel in a pull-request comment', 'A risk score checked against thresholds you set'),
    ('Release', 'Ship and hope', 'Feature-flagged and monitored for errors, latency and cost; promote or roll back'),
    ('Record', 'Decisions lost in pull-request threads', 'Every deviation from your rules logged with its reasoning and decision'),
]


def vs_table():
    rows = '<div class="vs-row head" aria-hidden="true"><div class="k"></div><div class="a">Vibe coding</div><div class="b">AI-native engineering</div></div>' + ''.join(
        f'<div class="vs-row"><div class="k">{k}</div><div class="a"><span class="sr">Vibe coding</span>{a}</div><div class="b"><span class="sr">AI-native engineering</span>{b}</div></div>' for k, a, b in VS)
    return f'<div class="vs" data-reveal>{rows}</div>'


DLOG = [
    ('PAY-412', 'New endpoint bypasses the /v2 API versioning convention', 'hi', 'High', 'Rejected at PR gate &middot; rebuilt under /v2'),
    ('ORD-188', 'Migration adds a nullable column the schema record marks required', 'md', 'Med', 'Spec amended &middot; decision record updated'),
    ('UI-77', 'Button variant outside the design system', 'lo', 'Low', 'Auto-fixed to the system component &middot; auto-merged'),
    ('BUG-903', 'Fix touches a shared auth module outside the spec&rsquo;s scope', 'hi', 'High', 'Held for approval &middot; split into two tickets'),
]


def dlog(n=4, hero=False):
    rows = ''.join(f'<div class="dlog-row"><code>{a}</code><p>{b}</p><div class="dec"><span class="risk {c}">{d}</span>{e}</div></div>' for a, b, c, d, e in DLOG[:n])
    return (f'<figure class="dlog{" dlog--hero" if hero else ""}" data-reveal="scale" style="--d:2" aria-label="Example deviation log: each change that departs from your architecture rules, its risk and the decision taken.">'
            f'<div class="dlog-head"><span>Deviation log</span><span>Example view</span></div><div class="dlog-rows">{rows}</div>'
            f'<figcaption class="t-small">A deviation is any change that departs from your architecture rules. Each one is logged with where it was caught, why it happened, its risk and who decided.</figcaption>'
            f'<div class="dlog-foot"><div><span class="risk hi">High</span><span>Held or rejected</span></div><div><span class="risk md">Med</span><span>Spec amended</span></div><div><span class="risk lo">Low</span><span>Auto-merged</span></div></div></figure>')


def run_panel(handoff=False):
    steps = [('Spec from template', 'Linear', False), ('Guardrails checked', 'ADRs &middot; schema &middot; API', False), ('Plan approved', 'architect', True),
             ('Built in sandbox', 'AI-written tests', False), ('Gates passed', 'fitness &middot; SAST &middot; coverage', False),
             ('Merged', 'risk score: low', False), ('Released', 'feature flag &middot; monitored', False)]
    st = ''.join(f'<div class="step{" human" if h else ""}"><span class="st-i"></span><span class="st-t">{t}</span><em>{e}</em></div>' for t, e, h in steps)
    mode = ' data-flow="handoff"' if handoff else ' data-flow'
    return f'''<div class="run"{mode} role="img" aria-label="Example: one change moving through the governed pipeline, from spec to a monitored release, with an architect approving the plan and the decision logged for leadership.">
<div class="con-head"><span><b>Governed change</b> &middot; example run</span><span class="live">Running</span><button class="run-toggle" type="button" aria-label="Pause animation">Pause</button></div>
<div class="run-pr"><div><code>PAY-418</code><b>Add partial refunds to checkout</b></div><span>main &larr; feat/refunds</span></div>
<div class="steps" aria-hidden="true">{st}</div>
<div class="flow-out" aria-hidden="true"><b>Logged</b><span>Decision, reasoning and gate results recorded for leadership</span></div></div>'''


ENG_PROOF = [
    ('In production', 'Field-service SaaS platform<br />South Africa', 'The client belongs to a ServiceNow Elite partner group. Our software-delivery agents for requirements, user stories and developer onboarding are built into the team&rsquo;s product workflow, from client need to development-ready work.'),
    ('4.9&#9733;', 'Booking &amp; payments app<br />United Kingdom', 'Built with AI-assisted engineering practices and live on both stores: 4.9&#9733; on the App Store (89 ratings) and 4.5&#9733; on Google Play (5,000+ downloads).'),
    ('Rehired', 'Dental implant network, 9 states<br />United States', 'Hired us twice: first for ten automated operational workflows and a clinician voice tool, then to add test and DevOps agents to their software release pipeline.'),
]
OPS_PROOF = [
    ('60%+', 'Food &amp; fashion retailer, ~960 stores<br />South Africa', 'Delivery-support tickets cut by more than 60% with a WhatsApp order-status agent, with 10,000+ queries automated every month.'),
    ('~3 wks', 'Residential developer<br />India', 'Agents run bank and buyer document follow-ups on the client&rsquo;s own SOPs. Time to the first installment fell from 6&ndash;10 weeks to about 3.'),
    ('&asymp;$210K/yr', 'Automotive compliance firm<br />India', 'A compliance-check agent replaced roughly $210K (&#8377;2 crore) a year of licensed tooling.'),
]

def proof_band(groups, h2, lead, q='eng'):
    r = ''
    for label, rows in groups:
        if label:
            r += f'<div class="rows-label">{label}</div>'
        r += ''.join(f'<div class="row"><div class="row-num">{n}</div><div class="row-who">{w}</div><div class="row-desc">{t}</div></div>' for n, w, t in rows)
    return f'''<section class="band band--rounded sec" aria-labelledby="proof-h"><div class="spot" aria-hidden="true"></div><div class="grid-bg" aria-hidden="true"></div><div class="wrap">
{head("Proof", h2, lead, hid="proof-h")}<div class="rows" data-reveal>{r}</div>
<p class="fine" style="color:var(--on-band-2)">Client names are withheld. Results are as reported from our engagements. Ask us for a reference call.</p>
{quotes(q)}</div></section>'''


POD_ICONS = {'dev': '<path d="m8 7-5 5 5 5M16 7l5 5-5 5"/>', 'arch': '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>', 'ba': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c1.8.8 3 2.6 3.5 5.2"/>'}
POD = [('dev', 'Full-stack developer', 'Operates the pipeline day to day: drafts specs with your team, supervises AI build output and keeps the gates green.'),
       ('arch', 'Claude Certified Architect', 'Maintains your architecture rules with your team, signs off plans, tunes the merge thresholds you set and reviews every high-risk deviation.'),
       ('ba', 'Analyst &amp; client lead', 'Turns business requests into specs, runs acceptance with your stakeholders and is your single point of contact.')]
PILOT = [('Scope', 'One team, one service, a real backlog.'),
         ('Your pod', 'A full-stack developer, a Claude Certified Architect and an analyst who is your single point of contact.'),
         ('Measured against', 'Success measures agreed up front against your current delivery process.'),
         ('You get', 'The pipeline installed end to end, then a results review with you before any wider rollout.'),
         ('Duration &amp; commercials', 'Agreed on the discovery call, based on your scope and requirements.')]
PATH = [('One-time implementation', 'A fixed fee, scaled to your company size and the teams and repositories in scope: pipeline, gates, templates, dashboard and training.'),
        ('Monthly retainer', 'An embedded Claude Certified Architect who maintains your architecture rules, tunes gates and thresholds, and reviews high-risk deviations as your system evolves.')]


def engage(sid='engagement'):
    pod = ''.join(f'<div class="card{" card--feature" if k == "arch" else ""}" data-reveal style="--d:{j}"><span class="role"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{POD_ICONS[k]}</svg></span><h3 class="t-h3">{t}</h3><p>{p}</p></div>' for j, (k, t, p) in enumerate(POD))
    spec = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in PILOT)
    path = ''.join(f'<div class="card" data-reveal style="--d:{j+1}"><span class="k">Step {j+2:02d}</span><h3 class="t-h3">{t}</h3><p>{p}</p></div>' for j, (t, p) in enumerate(PATH))
    return f'''<section class="sec" id="{sid}" aria-labelledby="eng-h"><div class="wrap">
{head("How we engage", 'Start with a pilot. <span class="ul-draw">Scale on evidence.</span>', 'No price list: every engagement is scoped after the discovery call, and you get a written proposal with a fixed scope and price before any build starts.', hid="eng-h")}
<div class="pilot" data-reveal><div class="pilot-k"><span class="k">Step 01</span><h3 class="t-h3">Pilot on one team</h3><p>Prove it on real work before you commit further.</p>{C.btn("engagement", cls="btn btn--sm")}</div><dl class="pilot-spec">{spec}</dl></div>
<div class="path path--2">{path}</div>
<div class="subhead"><h3 class="t-h3">Your pod: three people, embedded in your delivery.</h3><p>To scale, we add pods rather than enlarging one. Each pod brings the pipeline, the rules and the judgment.</p></div>
<div class="pod">{pod}</div></div></section>'''


COST_FAQ = ('What does it cost?', 'We don&rsquo;t publish a price list. AI-Native Engineering starts with a pilot on one team, then a one-time implementation fee scaled to the teams and repositories in scope, then a monthly retainer for your embedded Claude Certified Architect. Pilot duration and commercials are agreed on the discovery call, based on your scope and requirements. Automation work is scoped per workflow. After the discovery call you get a written proposal with a fixed scope and price before any build starts.')
ENG_FAQ = [
    ('How is this different from giving developers Copilot or Cursor?', 'Those tools generate code. AI-native engineering is the delivery process around them: the spec template, the architecture guardrails, the plan sign-off, the automated pull-request gates, the merge rules, the scenario testing, the controlled release and the decision record. Without that process, AI-written code still depends on manual review to be trusted.'),
    ('Couldn&rsquo;t our platform team build this ourselves?', 'You could, and many of the tools are ones you already run. What we add is the installed process from day one: spec templates, architecture guardrails, the plan sign-off, merge thresholds and the deviation log, plus an embedded Claude Certified Architect who maintains your architecture rules and tunes the gates as your system evolves. The pilot measures it against your current process before you commit.'),
    ('Do we have to replace our tools?', 'No. We install the process inside what you already run: Jira or Linear, GitHub, your existing CI/CD and the AI assistants you have approved, such as Claude, GitHub Copilot or Microsoft Power Platform for low-code teams.'),
    ('Who decides when AI-written code can merge?', 'You do. You set the merge thresholds. Only low-risk changes that conform to your architecture rules auto-merge; everything above the threshold goes to a named approver, and every decision is recorded on the dashboard.'),
    ('What happens to our engineers&rsquo; roles?', 'They stop hand-writing routine code and prompts and move up a level: writing and reviewing specs, approving plans, owning architecture rules and handling the changes that genuinely need human judgment.'),
    ('How do you handle security and intellectual property?', 'Code stays in your repositories and builds run in your environments. Security scanning is a mandatory gate and builds run in sandboxes. See the enterprise controls above for certifications and data handling.'),
    ('Where is your team, and how do you work across time zones?', 'Our delivery team is in India, with clients in the USA, UK, South Africa, Australia and Mauritius. Your pod&rsquo;s analyst is your single point of contact, and working hours are agreed in the pilot plan.'),
    COST_FAQ,
]
HOME_FAQ = [ENG_FAQ[0], ENG_FAQ[1], ENG_FAQ[3], COST_FAQ,
            ('How does a pilot work?', 'We pick one team and one service with a real backlog, agree success measures against your current process up front, install the pipeline end to end, and review the results with you before any wider rollout.'),
            ('Do you also automate business operations?', f'Yes. The same governed approach runs our <a class="link" href="{C.URL["bpa"]}">Business Process Automation</a> work: AI agents for follow-ups, documents, reconciliations and customer updates, with people approving what matters. Some clients start there: a US dental implant network hired us for ten operational workflows first, then to add test and DevOps agents to its release pipeline.')]

SEG_CARDS = [('tech-software', 'Tech &amp; Software', 'Ship AI-written code you can trust', ['Governed delivery pipeline', 'AI spend and risk controls', 'Delivery agents and pods'], 'For CTOs and CIOs'),
             ('ecommerce-retail', 'Ecommerce &amp; Retail', 'Fewer tickets, fewer returns', ['Order and delivery status', 'Returns and damage claims', 'Catalog and ad spend audits'], 'For ecommerce leaders'),
             ('operations-heavy', 'Operations-Heavy Businesses', 'Less chasing, faster cash', ['Collections and follow-ups', 'Document collection', 'Customer and partner updates'], 'For COOs'),
             ('professional-services', 'Professional Services', 'More time with clients', ['Client intake and documents', 'Reviews, deadlines and billing', 'Accounting, law, wealth, staffing'], 'For managing partners')]


def beyond():
    flag = f'''<a class="card card--ink flag-card" href="{C.URL["aine"]}" data-reveal><div><span class="badge-f">Flagship</span><span class="k">Engineer</span><h3 class="t-h3">AI-Native Engineering</h3>
<p>A governed spec-to-production pipeline installed inside the tools your engineering teams already use, with an embedded Claude Certified Architect.</p>
<span class="more">Explore the pipeline {ARROW}</span></div>
<ul class="feat"><li>Spec templates and architecture guardrails</li><li>Plan signed off by an architect</li><li>Automated architecture, security and coverage gates</li><li>Risk-scored merges against your thresholds</li><li>Feature-flagged, monitored releases</li><li>A deviation log for leadership</li></ul></a>'''
    others = [('gov', 'Govern', 'AI Governance', 'Spend visibility, data controls and audit trails for the AI tools already in use across your business.', 'Explore AI governance'),
              ('bpa', 'Automate', 'Business Process Automation', 'Pre-built and custom agents that run follow-ups, documents, reconciliations and customer updates inside your systems.', 'Explore the agent library'),
              ('fao', 'Lead', 'Fractional AI Officer', 'An embedded AI lead on retainer who owns the roadmap and reports results to leadership.', 'Meet the Fractional AI Officer')]
    rest = ''.join(f'<a class="card" href="{C.URL[k]}" data-reveal style="--d:{i+1}"><span class="k">{kk}</span><h3 class="t-h3">{t}</h3><p>{p}</p><span class="more">{l} {ARROW}</span></a>' for i, (k, kk, t, p, l) in enumerate(others))
    segs = ''.join(f'<a class="card" href="{C.URL[k]}" data-reveal style="--d:{i}"><span class="k">{who}</span><h3 class="t-h3">{n}</h3><p class="seg-h">{h}</p><ul>{"".join(f"<li>{x}</li>" for x in ls)}</ul><span class="more">{short} {ARROW}</span></a>' for i, (k, n, h, ls, who, short) in enumerate([c + ({'tech-software': 'See the engineering page', 'ecommerce-retail': 'See the retail page', 'operations-heavy': 'See the operations page', 'professional-services': 'See the firms page'}[c[0]],) for c in SEG_CARDS]))
    return f'''<section class="sec" id="who-we-help" aria-labelledby="disc-h"><div class="wrap">
{head("Beyond engineering", 'Engineering leads. <span class="ul-draw">Everything around it, governed.</span>', 'Engineering is where we lead. The same governed discipline extends to the AI already in your business and to the operations around your product.', hid="disc-h")}
<div class="disc">{flag}{rest}</div>
<div class="subhead" id="segments"><h3 class="t-h3">Who we help</h3><p>Four kinds of business, one governed approach. Each page shows the workflows, proof and model that fit.</p></div>
<div class="cards cards--4">{segs}</div></div></section>'''


def vs_section(h2, eyebrow='The gap'):
    return f'<section class="sec" aria-labelledby="gap-h"><div class="wrap">{head(eyebrow, h2, "Most teams use AI as a faster keyboard: prompts in an editor, then a senior engineer reviews everything by hand because nothing else can be trusted. The speed gain disappears in review, and the risk moves to production.", hid="gap-h")}{vs_table()}</div></section>'


ROUTER = ('<p class="router" data-reveal style="--d:5">Not leading an engineering team? See how we help '
          f'<a href="{C.URL["ecommerce-retail"]}">ecommerce &amp; retail</a>, <a href="{C.URL["operations-heavy"]}">operations-heavy businesses</a> '
          f'and <a href="{C.URL["professional-services"]}">professional services firms</a>.</p>')

# ===================================================================== HOME
home = '\n'.join([
    f'''<section class="hero" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<p class="badge" data-reveal><i aria-hidden="true"></i><span><b>AI-Native Engineering</b><span class="opt"> for CTOs and CIOs</span></span></p>
<h1 id="hero-h" class="t-hero" data-split>AI writes the code. <span class="hl">Your architecture stays in charge.</span></h1>
<p class="t-lead" data-reveal style="--d:3">Upcore installs a governed delivery pipeline inside your Jira or Linear, GitHub and CI/CD, and embeds a Claude Certified Architect to run it with your team. Every AI-written change is checked against your architecture, gated and risk-scored. Start with a pilot on one team.</p>
<div class="hero-ctas" data-reveal style="--d:4">{C.btn("hero", pulse=True)}<a class="link" href="#pipeline">See the pipeline</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes &middot; a written plan, whether or not we work together</p>
{ROUTER}
<div class="hero-stage hero-stage--eng">{run_panel(handoff=True)}{dlog(4, hero=True)}</div>
</div></section>''',
    TRUST,
    vs_section(NB('Vibe coding is not <span class="ul-draw">AI-native engineering.</span>')),
    pipeline(compact=True, link=True),
    engage(),
    proof_band([('AI-Native Engineering', ENG_PROOF), ('Business Process Automation', OPS_PROOF)], 'Shipped, <span class="hl">and still running.</span>', 'Engineering and automation work in production for clients in the US, UK, South Africa and India.'),
    F.suite(order=['loop', 'ladder', 'matrix', 'compress'], lead='Four working models behind every engagement, each grounded in established research. They govern how agents behave, how much autonomy they earn, what we automate and where the time comes back.'),
    TL.stack(TL.HOME, 'Integrations', 'Runs inside the stack <span class="ul-draw">you have today.</span>', 'Pipelines and agents connect to your planning, code, CI/CD, cloud and business systems, and to the AI models your teams already use. No rip-and-replace.', sid='integrations'),
    beyond(),
    F.controls(),
    faq_sec(HOME_FAQ, 'What engineering leaders <span class="ul-draw">want to know.</span>', 'Not covered here? Ask Gaurav or Saswata on the discovery call.'),
    cta('Make AI-written code something <span class="hl">your architects can sign off on.</span>', 'Book a 45-minute discovery call. We&rsquo;ll review your current delivery process and outline what a pilot on one team would look like.',
        '/lp/governance-index', 'Get your AI Governance Score in 2 minutes', 'home', leaders=True),
])
ld = C.graph('home', [{'@type': 'WebSite', '@id': C.SITE + '/#website', 'url': C.SITE + '/', 'name': 'Upcore Technologies', 'publisher': {'@id': C.ORG_ID}}])
print('home', C.write('index.html', 'home', 'AI-Native Engineering &amp; Automation | Upcore Technologies',
      'Governed AI-native software delivery inside Jira or Linear, GitHub and CI/CD, plus AI agents for the operations around your product. ISO 27001 certified.',
      home, active='home', ld=ld, group='home'))

# ===================================================================== AINE PAGE
aine = '\n'.join([
    f'''<section class="hero hero--split" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap">
<div><nav class="crumb" aria-label="Breadcrumb" data-reveal><ol><li><a href="{C.URL["home"]}">Home</a></li><li aria-current="page">AI-Native Engineering</li></ol></nav>
<div class="eyebrow" data-reveal>AI-Native Engineering &middot; For CTOs and CIOs</div>
<h1 id="hero-h" class="t-display" data-split>AI-native engineering, <span class="hl">governed from spec to production.</span></h1>
<p class="t-lead" data-reveal style="--d:3">We install a governed delivery pipeline inside your Jira or Linear, GitHub and CI/CD and embed a Claude Certified Architect to run it with your team. Every deviation from your architecture is recorded, explained and decided. Start with a pilot on one team.</p>
<div class="hero-ctas" data-reveal style="--d:4">{C.btn("hero", pulse=True)}<a class="link" href="#pipeline">See the pipeline</a></div>
<p class="hero-micro" data-reveal style="--d:4">45 minutes &middot; a written plan, whether or not we work together</p></div>
{run_panel()}</div></section>''',
    TRUST,
    vs_section('AI writes more of your code every quarter. <span class="ul-draw">Your review process hasn&rsquo;t changed.</span>', eyebrow='Vibe coding vs AI-native engineering'),
    pipeline(compact=False),
    engage(),
    f'''<section class="sec" aria-labelledby="dash-h"><div class="wrap"><div class="split">
<div><div class="eyebrow" data-reveal>Leadership visibility</div><h2 id="dash-h" class="t-h2" data-reveal>Know delivery is under control <span class="ul-draw">without reading pull requests.</span></h2>
<p class="t-lead" data-reveal style="--d:1;margin-top:18px">The CTO/CIO dashboard records every deviation from your architecture rules: where it was caught, why it happened, its risk score and who decided what to do about it.</p>
<ul class="ticks" data-reveal style="--d:2"><li>A deviation log with the reasoning and decision for each one</li><li>Gate pass and fail trends by team and service</li><li>The share of changes auto-merged versus approved by a person</li><li>Release outcomes, promoted or rolled back, and why</li><li>One view you can take to a board, an auditor or a customer&rsquo;s security review</li></ul></div>
{dlog(4)}</div></div></section>''',
    proof_band([('', ENG_PROOF)], 'Engineering work <span class="hl">in production.</span>', 'AI-Native Engineering starts as a pilot. These engagements are the engineering work it builds on, led by a Claude Certified Architect.'),
    F.suite(order=['loop', 'ladder'], eyebrow='Engineering principles', h2='Two models <span class="ul-draw">behind every merge.</span>', lead='Every change runs a closed control loop, and autonomy is earned on evidence, never assumed.'),
    TL.stack(TL.ENGINEERING, 'Engineering stack', 'Installed inside <span class="ul-draw">your toolchain.</span>', 'The governed pipeline runs in the planning, code, CI/CD and cloud tools you already have, with the AI assistants and models your teams have approved.'),
    F.controls(),
    faq_sec(ENG_FAQ, 'Before you <span class="ul-draw">book a call.</span>', 'Not covered here? Ask Gaurav or Saswata on the discovery call.'),
    cta('Put AI-written code <span class="hl">under your architecture&rsquo;s control.</span>', 'Book a 45-minute discovery call. We&rsquo;ll review your current delivery process and outline what a pilot on one team would look like.',
        '/lp/governance-index', 'Get your AI Governance Score in 2 minutes', 'ai-native-engineering', leaders=True),
])
ld = C.graph('aine', [
    {'@type': 'Service', 'name': 'AI-Native Engineering', 'serviceType': 'Governed AI software delivery', 'url': C.SITE + C.FINAL_URL['aine'], 'provider': {'@id': C.ORG_ID},
     'description': 'Installation of a governed, end-to-end AI-native software delivery pipeline inside existing engineering tools, with architecture guardrails, automated gates, controlled releases and a leadership dashboard.',
     'audience': {'@type': 'Audience', 'audienceType': 'CTOs and CIOs'}, 'areaServed': C.AREA},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': H.unescape(q), 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', H.unescape(a))}} for q, a in ENG_FAQ]}],
    crumb='AI-Native Engineering')
print('aine', C.write('ai-native-engineering.html', 'aine', 'AI-Native Engineering: Governed Software Delivery | Upcore',
      'A governed spec-to-production AI pipeline inside Jira or Linear, GitHub and CI/CD, with architecture gates, controlled releases and a CTO dashboard.',
      aine, active='aine', ld=ld, group='solution'))
