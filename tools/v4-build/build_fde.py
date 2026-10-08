"""/forward-deployed-engineer (2026-10-08): Fractional FDE, the fifth solution. A Forward Deployed Engineer embedded
part of every week to take AI pilots and agents into production against the client's real systems, and stay on.
delivery log (hero) -> why pilots stall -> what a fractional FDE is -> five stages, one owner -> when it fits ->
proof -> FAQ -> CTA. Facts: the retired /fde-engineers page (lifecycle, ownership model, governed from the first
commit), the site's own standards and stats. No public price (the FAO is the only published price) and no
"48 hours" claim. Reuses the FAO page's components (.fo-*) plus the small `fde` CSS block.
Run from the repo root: python tools/v4-build/build_fde.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import segment_copy as S
from v4parts import TESTIMONIALS

# ------------------------------------------------------------------ 1. hero: delivery log (illustrative)
LOG = [('Discover', 'Workflow mapped, blueprint signed off', 'scale', 'Done'),
       ('Build', 'Agent built and tested on your real data', 'scale', 'Done'),
       ('Integrate', 'Connected to your CRM and help desk', 'acc', 'In progress'),
       ('Deploy', 'Released to Slack and web, with a rollback path', 'con', 'Next'),
       ('Iterate', 'Your engineer stays on to monitor and improve', 'acc', 'Ongoing')]
rows = ''.join(f'<li style="--i:{i}"><span class="fo-pi"><b>{n}</b><span>{d}</span></span><em class="fo-v fo-{c}">{v}</em></li>' for i, (n, d, c, v) in enumerate(LOG))
DELIVERY = f'''<figure class="fo-port" data-portfolio>
<p class="sr">Example delivery log with illustrative data: one engineer takes an agent through five stages, discover, build, integrate, deploy and iterate, and stays on after launch.</p>
<div class="dash-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>Order triage agent &middot; delivery log</span><span class="gate-pr">Your FDE</span></div>
<div class="fo-sum"><div><b>1</b><span>named engineer</span></div><div><b>5</b><span>stages, one owner</span></div><div><b>0</b><span>hand-offs to a new team</span></div><div><b>Day 1</b><span>under your governance</span></div></div>
<ol class="fo-list">{rows}</ol>
</div>
<figcaption><span>Example with illustrative data</span><button class="gate-toggle fo-toggle" type="button" aria-label="Replay animation">Replay</button></figcaption>
</figure>'''
hero = K.hero_split([(C.URL['home'], 'Home'), (None, 'Fractional FDE')], 'Fractional Forward Deployed Engineer',
                    'Your AI pilot, <span class="hl">live in production.</span>',
                    'A senior engineer joins your team part of every week, builds against your real systems and data, ships the agent and stays to keep it working. It&rsquo;s the role AI companies such as OpenAI and Anthropic hire to get their technology working inside customers, without you hiring one full-time.',
                    C.btn('hero', pulse=True) + '<a class="link" href="#stages">See how it works</a>', DELIVERY)

# ------------------------------------------------------------------ 2. why pilots stall
PAINS = [('Demo data', '&ldquo;It worked in the demo.&rdquo;', 'Demos run on clean sample data. Real data is messy, and the agent breaks on the first live ticket.', 'Built and tested on your real data from day one'),
         ('No owner', '&ldquo;Whose job is the integration?&rdquo;', 'The vendor configured the tool. Wiring it into your CRM, help desk and APIs fell to a team that already has a full-time job.', 'One named engineer owns build, integration and release'),
         ('No scale', '&ldquo;It works for one team. Now what?&rdquo;', 'A pilot solved one problem. Taking it to five teams needs someone to own the roadmap and the next integration.', 'The same engineer takes it across teams'),
         ('Nobody stays', '&ldquo;The agency shipped and left.&rdquo;', 'Workflows change, edge cases pile up and quality drifts. Without an owner, the agent quietly stops being used.', 'Monitored, fixed and improved on the same retainer')]
pains = ''.join(f'<li data-reveal style="--d:{i % 2}"><span class="fo-pk">{k}</span><blockquote>{q}</blockquote><p>{d}</p><span class="fo-fix">{f}</span></li>' for i, (k, q, d, f) in enumerate(PAINS))
gaps = f'''<section class="h-sec" aria-labelledby="gap-h"><div class="wrap">
<div class="h-head"><div>{K.eyebrow("Why pilots stall")}<h2 id="gap-h" class="h-h2" data-reveal>Great demo. Never shipped.</h2></div>
<dl class="gv-stats fo-stats" data-reveal style="--d:1"><div><dt>95%</dt><dd>of enterprise generative AI pilots fail to deliver measurable return <span>MIT NANDA Initiative, 2025</span></dd></div>
<div><dt>42%</dt><dd>of companies scrapped most of their AI initiatives in 2025, up from 17% <span>S&amp;P Global Market Intelligence, 2025</span></dd></div></dl></div>
<ul class="fo-pains">{pains}</ul></div></section>'''

# ------------------------------------------------------------------ 3. what a fractional FDE is
WHO = [('Who they are', 'A senior engineer fluent in Python, cloud infrastructure and AI orchestration (retrieval, agent frameworks, evaluation) who also owns the business outcome.'),
       ('How they work', 'Inside your tools and your team&rsquo;s rhythm, not a ticket queue. They build against your real systems, data and constraints.'),
       ('What they own', 'The build, the integration, the release and everything after launch: monitoring, fixes and the next workflow.'),
       ('Why fractional', 'Part of every week on a monthly retainer, for as long as it pays off. No recruitment cycle, and you meet your engineer before you sign.')]
who = ''.join(f'<div data-reveal style="--d:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(WHO))
role = f'''<section class="h-sec h-sec--alt" id="engagement" aria-labelledby="who-h"><div class="wrap">
<div class="h-pilot"><div class="h-pilot-k">{K.eyebrow("What you get")}<h2 id="who-h" class="h-h2 h-h2--sm" data-reveal>One engineer. Start to finish.</h2>
<p class="fo-side" data-reveal style="--d:1">Not a consultant who leaves after the demo, and not a no-code tool you configure yourself. Every design is reviewed by a Claude Certified Architect, and every Upcore architect is Claude certified.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("engagement")}</div></div>
<dl class="h-pilot-spec">{who}</dl></div>
</div></section>'''

# ------------------------------------------------------------------ 4. five stages, one owner
STAGES = [('01', 'Discover', ['Maps how the work is really done, step by step', 'Picks the workflow with the most impact, not the easiest demo', 'Writes a blueprint of what gets built and what &ldquo;done&rdquo; means, signed off before any code']),
          ('02', 'Build', ['Uses your terminology and decision rules', 'Built and tested on your real data, not samples', 'Your team reviews at every milestone']),
          ('03', 'Integrate', ['Connects to the CRM, ERP, APIs and databases you already run', 'Respects your existing access and permissions', 'Lives inside your stack, not in another dashboard']),
          ('04', 'Deploy', ['Released where your team works: Slack, WhatsApp, web or an API', 'Checked against your governance rules before go-live', 'Team trained, with a clear rollback path']),
          ('05', 'Iterate', ['The engineer who built it maintains it', 'Tracks accuracy, edge cases and drift, and fixes them early', 'Adds the next workflow on the same retainer'])]
st = ''.join(f'<li class="fo-ph" data-reveal style="--d:{i}"><span class="fo-node" aria-hidden="true"></span><span class="fo-days">Stage {n}</span><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></li>' for i, (n, t, items) in enumerate(STAGES))
stages = f'''<section class="h-sec" id="stages" aria-labelledby="st-h"><div class="wrap">
{K.head("How it works", "Five stages. One owner.", "st-h", "Most AI projects skip the last stage. Yours doesn&rsquo;t: the engineer who ships it stays to keep it working.")}
<ol class="fo-phases fd-phases" data-reveal><span class="fo-rail" aria-hidden="true"><i></i></span>{st}</ol>
</div></section>'''

# ------------------------------------------------------------------ 5. when it fits
FIT = [('It fits when', ['You have a pilot or a clear workflow, but nobody to take it to production.', 'Your engineers are at capacity and integration keeps slipping.', 'The work needs real connections to your CRM, ERP or internal APIs.', 'You want one accountable person, not a vendor ticket queue.'], None),
       ('Choose something else when', [f'You need a whole delivery team changing how software ships: start with <a class="link" href="{C.URL["aine"]}">AI-Native Engineering</a>.',
                                        f'You haven&rsquo;t decided where AI should go yet: start with a <a class="link" href="{C.URL["fao"]}">Fractional AI Officer</a>.',
                                        f'You want agents run for you across operations: see <a class="link" href="{C.URL["bpa"]}">Business Process Automation</a>.'], None)]
fit = ''.join(f'<li data-reveal style="--d:{i}"><span class="fo-fn">0{i + 1}</span><h3>{t}</h3><ul class="fd-list">{"".join(f"<li>{x}</li>" for x in items)}</ul></li>' for i, (t, items, _) in enumerate(FIT))
fits = f'''<section class="h-sec h-sec--tight h-sec--alt" aria-labelledby="fit-h"><div class="wrap ab-split">
<div>{K.eyebrow("Is it right for you?")}<h2 id="fit-h" class="h-h2 h-h2--sm" data-reveal>The right fit, honestly.</h2>
<p class="fo-side" data-reveal style="--d:1">If another Upcore service suits you better, we&rsquo;ll say so on the first call. Every engagement ships under your security and governance rules: see <a class="link" href="{C.URL["security"]}">Security</a>.</p></div>
<ul class="fo-focus">{fit}</ul></div></section>'''

# ------------------------------------------------------------------ 6. proof
strip = lambda s: s.replace('<br />', ' &middot; ')
RES = [('Engineering', S.P_SAAS[0], 'delivery agents inside a product team', strip(S.P_SAAS[1])),
       ('Engineering', S.P_DENTAL_ENG[0], 'to add test and DevOps agents to their release pipeline', strip(S.P_DENTAL_ENG[1])),
       ('Automation', S.P_RETAIL[0], 'fewer delivery-support tickets, with 10,000+ queries automated a month', strip(S.P_RETAIL[1]))]
q = TESTIMONIALS['eng'][1]
proof = K.results_band('Results', 'Shipped. Still running.', RES, quote=(q[0], q[1]))

# ------------------------------------------------------------------ 7. FAQ + CTA
FAQ = [('What is a Forward Deployed Engineer?', 'A senior software engineer who works inside a customer&rsquo;s team to build and ship production AI against their real systems, rather than handing over a tool and leaving. The role is common at AI companies such as OpenAI and Anthropic.'),
       ('What does &ldquo;fractional&rdquo; mean here?', 'Your engineer works with you part of every week on a monthly retainer, instead of a full-time hire. You get the same ownership without the recruitment cycle, and new workflows are added to the same retainer.'),
       ('What will our engineer build?', 'Usually AI agents and automations that sit inside your existing tools: triage and routing, document and data extraction, customer and internal assistants, and the integrations that connect them to your CRM, ERP and APIs.'),
       ('How is this different from an agency or a contractor?', 'An agency ships a project and moves on. A contractor builds what the ticket says. Your FDE owns the outcome across all five stages and stays after launch to monitor, fix and extend what they built.'),
       ('How do you handle our code and data?', f'Your engineer works with the access you grant, in your tools and environment. Which AI providers are used, on what terms, and how code and data are handled is set out on our <a class="link" href="{C.URL["security"]}">security page</a>. We sign a mutual NDA before any call where sensitive details are shared.'),
       ('What does it cost?', 'A monthly retainer scoped to the work after a 45-minute discovery call. You get a written proposal with a fixed scope before anything starts.')]
faq = K.faq(FAQ, 'Questions before you start.')
final = K.final('Get your AI out of the pilot. <span class="hl">Into production.</span>',
                'Book a 45-minute discovery call. We&rsquo;ll look at the pilot or workflow you want live and send a written plan, whether or not we work together.')

page = '\n'.join([hero, gaps, role, stages, fits, proof, faq, final])
ld = C.graph('fde', [{'@type': 'Service', 'name': 'Fractional Forward Deployed Engineer', 'serviceType': 'Forward deployed engineering', 'url': C.SITE + C.FINAL_URL['fde'], 'provider': {'@id': C.ORG_ID},
                      'description': 'A senior engineer embedded part-time to build AI agents against your real systems, ship them to production and stay on to maintain and extend them.', 'areaServed': C.AREA},
                     K.faq_ld(FAQ)], crumb='Fractional FDE')
print('fde', C.write('forward-deployed-engineer.html', 'fde', 'Fractional Forward Deployed Engineer (FDE) for AI | Upcore',
      'A senior engineer embedded part of every week to take your AI pilot into production against your real systems, and stay on to keep it working.',
      page, active='fde', ld=ld, group='solution', spine=False, main_cls='is-calm', annc_kind=C.ANNC_OPS))
