"""/fractional-ai-officer (2026-10-07, calm rebuild). An embedded AI lead on retainer, for COOs, CFOs
and CEOs: portfolio-verdict view (hero) -> four gaps -> 90 days in three phases -> two focuses ->
economics (#economics: the only public price on the site, from $1,999/month; /pricing redirects here)
-> who you get + commitments -> FAQ -> CTA. Facts and figures come from the previous page.
Run from the repo root: python tools/v4-build/build_fao.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K

# ------------------------------------------------------------------ 1. hero: portfolio verdicts (illustrative)
PORT = [('Content &amp; marketing agent', '12% cost reduction, proven', 'scale', 'Scale'),
        ('Sales proposal drafting', '64% adoption, return unproven', 'acc', 'Accelerate'),
        ('Expense anomaly detection', 'Early pilot, promising signal', 'acc', 'Accelerate'),
        ('Vendor contract review', 'Three overlapping pilots, no baseline', 'con', 'Consolidate'),
        ('Support ticket triage', 'Manual, no clear owner', 'stop', 'Stop')]
prow = ''.join(f'<li style="--i:{i}"><span class="fo-pi"><b>{n}</b><span>{d}</span></span><em class="fo-v fo-{c}">{v}</em></li>' for i, (n, d, c, v) in enumerate(PORT))
PORTFOLIO = f'''<figure class="fo-port" data-portfolio>
<p class="sr">Example portfolio review with illustrative data: five AI initiatives reviewed. One is recommended to scale, two to accelerate, one to consolidate and one to stop.</p>
<div class="dash-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>AI portfolio &middot; Day-30 decision</span><span class="gate-pr">Portfolio view</span></div>
<div class="fo-sum"><div><b>5</b><span>initiatives reviewed</span></div><div><b>1</b><span>to scale</span></div><div><b>2</b><span>to accelerate</span></div><div><b>2</b><span>to consolidate or stop</span></div></div>
<ol class="fo-list">{prow}</ol>
</div>
<figcaption><span>Example with illustrative data</span><button class="gate-toggle fo-toggle" type="button" aria-label="Replay animation">Replay</button></figcaption>
</figure>'''
hero = K.hero_split([(C.URL['home'], 'Home'), (None, 'Fractional AI Officer')], 'Fractional AI Officer &middot; for COOs, CFOs and CEOs',
                    'One accountable owner for your AI, <span class="hl">without a full-time hire.</span>',
                    'An embedded AI lead on retainer. Your Fractional AI Officer inventories every AI pilot and tool, picks the two or three worth scaling and stays accountable until they are live and used. From $1,999 a month.',
                    C.btn('hero', pulse=True) + '<a class="link" href="#economics">See the economics</a>', PORTFOLIO,
                    micro=f'Not ready for a call? <a href="/lp/ai-maturity-index?utm_source=website&amp;utm_medium=fractional-ai-officer&amp;utm_campaign=hero_secondary">Get your AI Maturity Score in 2 minutes</a>')

# ------------------------------------------------------------------ 2. four gaps
PAINS = [('No owner', '&ldquo;Everyone&rsquo;s job touches AI. Nobody&rsquo;s job is AI working.&rdquo;', 'Operations owns the process, technology the platform, finance the budget. Nobody owns whether an initiative succeeds.', 'One accountable owner across the portfolio'),
         ('No baseline', '&ldquo;We think it&rsquo;s working. We can&rsquo;t prove it.&rdquo;', 'Teams say their tools save time, but nobody set a baseline, priced the saving or checked people actually use it.', 'A baseline and KPI agreed before real spend'),
         ('Strategy that never ships', '&ldquo;We have the slide deck. We don&rsquo;t have the workflow.&rdquo;', 'The workshop happened. The work stalls when someone has to redesign the process, connect the systems and win adoption.', 'Implementations live with real users in 90 days'),
         ('Tool sprawl', '&ldquo;We have twenty logins. We don&rsquo;t have one strategy.&rdquo;', 'Departments buy overlapping subscriptions and engage different vendors for the same problem.', 'Duplicates consolidated, one owner per tool')]
pains = ''.join(f'<li data-reveal style="--d:{i % 2}"><span class="fo-pk">{k}</span><blockquote>{q}</blockquote><p>{d}</p><span class="fo-fix">{f}</span></li>' for i, (k, q, d, f) in enumerate(PAINS))
gaps = f'''<section class="h-sec" aria-labelledby="gap-h"><div class="wrap">
<div class="h-head"><div>{K.eyebrow("The gap")}<h2 id="gap-h" class="h-h2" data-reveal>Twenty AI pilots. Nobody owns the outcome.</h2></div>
<dl class="gv-stats fo-stats" data-reveal style="--d:1"><div><dt>95%</dt><dd>of enterprise generative AI pilots fail to deliver measurable return <span>MIT NANDA Initiative, 2025</span></dd></div>
<div><dt>42%</dt><dd>of companies scrapped most of their AI initiatives in 2025, up from 17% <span>S&amp;P Global Market Intelligence, 2025</span></dd></div></dl></div>
<ul class="fo-pains">{pains}</ul></div></section>'''

# ------------------------------------------------------------------ 3. 90 days, three phases
PHASES = [('Days 1&ndash;30', 'Diagnose &amp; decide', ['Every AI pilot, tool, vendor and owner inventoried in ten business days', 'Every opportunity ranked by financial impact, feasibility and risk', 'Process, data and adoption gaps found before budget is committed', 'Day-30 decision: two initiatives to build, one conditional, stop or consolidate the rest']),
          ('Days 31&ndash;60', 'Design &amp; de-risk', ['A baseline, financial case and KPI for every selected initiative', 'Named business, technical and financial owners, with a steering committee', 'The fastest responsible route for each: custom agent, existing platform or vendor', 'Testing, adoption and launch plans approved before build']),
          ('Days 61&ndash;90+', 'Deploy &amp; prove', ['The first initiative live with real users and real data', 'The second live, with usage and quality tracked against its KPI', 'Results compared with the baseline, and a 6&ndash;12 month plan for what scales next', 'Then monthly: portfolio management, adoption coaching and quarterly board reporting'])]
ph = ''.join(f'<li class="fo-ph" data-reveal style="--d:{i}"><span class="fo-node" aria-hidden="true"></span><span class="fo-days">{d}</span><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></li>' for i, (d, t, items) in enumerate(PHASES))
phases = f'''<section class="h-sec h-sec--alt" id="framework" aria-labelledby="ph-h"><div class="wrap">
{K.head("What your AI Officer does", "From twenty pilots to the few that matter, in 90 days.", "ph-h", "Three phases, with a walk-away checkpoint at Day 30. Your AI Officer runs it with a coordinated Upcore team behind them: financial modelling, solution architecture and adoption.")}
<ol class="fo-phases" data-reveal><span class="fo-rail" aria-hidden="true"><i></i></span>{ph}</ol>
</div></section>'''

# ------------------------------------------------------------------ 4. two focuses
FOCUS = [('Strategy &amp; adoption', 'For COOs and CFOs with scattered pilots and no answer for the board. Portfolio, priorities, business cases and adoption: everything on this page.', None),
         ('AI engineering governance', 'For CTOs and CISOs whose teams ship AI-written code. Inventory, policy, security checks, spend visibility and an audit trail.', (C.URL['gov'], 'See AI Governance'))]
foc = ''.join(f'<li data-reveal style="--d:{i}"><span class="fo-fn">0{i + 1}</span><h3>{t}</h3><p>{d}</p>{f"<a class=link href={u[0]}>{u[1]}</a>" if u else ""}</li>' for i, (t, d, u) in enumerate(FOCUS))
focus = f'''<section class="h-sec h-sec--tight" aria-labelledby="foc-h"><div class="wrap ab-split">
<div>{K.eyebrow("One role, two focuses")}<h2 id="foc-h" class="h-h2 h-h2--sm" data-reveal>Choose where your AI Officer starts.</h2>
<p class="fo-side" data-reveal style="--d:1">Some organisations need both at once. One AI Officer can run either, or both.</p></div>
<ul class="fo-focus">{foc}</ul></div></section>'''

# ------------------------------------------------------------------ 5. economics (#economics)
COST = [('Full-time Chief AI Officer', '$400,000&ndash;$750,000+', 'a year, plus 6&ndash;12 months to recruit and a team to build underneath them', 400, 750),
        ('Strategy consultancy', '$500,000+', 'a project: a report, then they leave', 500, 500),
        ('Fractional AI Officer', 'From $1,999', 'a month, from $23,988 a year', 24, 24)]
bars = ''.join(f'<li class="fo-c{" is-us" if i == 2 else ""}" data-reveal style="--d:{i}"><span class="fo-cn">{n}</span><span class="fo-cb"><i style="--s:{a / b * 100:.1f}%;--b:{max(b / 750 * 100, 3.2):.1f}%"></i></span><span class="fo-cv"><b>{v}</b> {s}</span></li>' for i, (n, v, s, a, b) in enumerate(COST))
CMP = [('Time to value', 'Six to twelve months to recruit, then build a team', 'A report, then they leave', 'First inventory in ten business days'),
       ('Accountability', 'One person, one context, no delivery team', 'Resets with every engagement', 'Owns portfolio outcomes, not a report'),
       ('Longevity', 'Salary, equity and benefits, indefinitely', 'Recommendations die when the contract ends', 'Embedded in your organisation, through adoption'),
       ('Track record', 'Hard to vet at the point of hire', 'Generalist advice, not accountable for delivery', 'A specialist in AI strategy and coordination')]
COLS = ['Full-time hire', 'Consultancy', 'Fractional AI Officer']
cmp_rows = ''.join(f'<div class="cmp-row" role="row" data-reveal style="--d:{i % 3}"><div class="cmp-k" role="rowheader">{k}</div>'
                   + ''.join(f'<div class="cmp-c{" is-us" if j == 2 else ""}" role="cell"><span class="cmp-l">{COLS[j]}</span>{v}</div>' for j, v in enumerate((a, b, c))) + '</div>'
                   for i, (k, a, b, c) in enumerate(CMP))
econ = f'''<section class="h-sec" id="economics" aria-labelledby="eco-h"><div class="wrap">
{K.head("The economics", "The role your organisation is missing, without the cost or the wait.", "eco-h", "The only price we publish. Exact pricing depends on your organisation&rsquo;s size and scope, and is confirmed in a written proposal after the discovery call.")}
<ul class="fo-cost" data-reveal>{bars}</ul>
<p class="fo-axis" aria-hidden="true"><span>Annual cost</span><span><span>$0</span><span>$750K+</span></span><span></span></p>
<div class="cmp" role="table" aria-label="Full-time hire, consultancy and Fractional AI Officer compared">
<div class="cmp-row cmp-head" role="row"><div role="columnheader"><span class="sr">Question</span></div>{"".join(f'<div class="cmp-c{" is-us" if j == 2 else ""}" role="columnheader">{c}</div>' for j, c in enumerate(COLS))}</div>
{cmp_rows}</div>
</div></section>'''

# ------------------------------------------------------------------ 6. who you get + commitments
WHO = [('A person, not a slide deck', 'A senior AI strategy specialist embedded across your organisation: runs the steering committee, owns the roadmap and coaches adoption.'),
       ('Background', 'Eight or more years in operations or delivery leadership, with AI implementation expertise, backed by a coordinated Upcore team.'),
       ('Time', 'Eight to twelve hours a week, dedicated: enough to run your steering cadence, track every initiative and report weekly.'),
       ('Named before you sign', 'You meet your AI Officer on the discovery call. If the fit isn&rsquo;t right, we find a better one.')]
who = ''.join(f'<div data-reveal style="--d:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(WHO))
COMMIT = ['Your enterprise AI inventory is delivered within ten business days.',
          'At Day 30 you get the full decision package (inventory, maturity assessment, value heatmap and ROI baselines) and can walk away owing only for work done to that date.',
          'If agreed implementation milestones are not reached by Day 90 for reasons within our control, we keep working at no extra management fee.']
commit = ''.join(f'<li data-reveal style="--d:{i}">{c}</li>' for i, c in enumerate(COMMIT))
engage = f'''<section class="h-sec h-sec--alt" id="engagement" aria-labelledby="who-h"><div class="wrap">
<div class="h-pilot"><div class="h-pilot-k">{K.eyebrow("Who you get")}<h2 id="who-h" class="h-h2 h-h2--sm" data-reveal>A person who owns the result.</h2>
<p class="fo-side" data-reveal style="--d:1">Done with you: your team leads and your AI Officer guides, trains and co-designs, with full knowledge transfer. Done for you: you give us stakeholder access and pilot data, and we run the portfolio.</p>
<div class="hero-ctas" data-reveal style="--d:2">{C.btn("engagement")}</div></div>
<dl class="h-pilot-spec">{who}</dl></div>
<div class="gv-commit"><div><p class="h-col">What we commit to</p><p class="gv-cnote">Each commitment depends on you giving us the access and decisions we ask for on time.</p></div>
<ol class="gv-clist">{commit}</ol>
<p class="gv-not"><b>What we don&rsquo;t guarantee:</b> a specific revenue increase, workforce reductions, perfect employee adoption or a vendor&rsquo;s own performance.</p></div>
</div></section>'''

FAQ = [('What is a Fractional AI Officer?', 'A specialist embedded in your organisation part-time, accountable for turning scattered AI pilots into two or three owned, measurable implementations. They run your steering committee, own the roadmap and stay accountable for adoption, without the cost or timeline of a full-time Chief AI Officer.'),
       ('How fast can this start?', 'Ten business days to your first enterprise AI inventory. We interview your stakeholders and inventory every pilot, tool and vendor already in motion, with no recruitment cycle and no ramp period.'),
       ('What is in the 90 days?', 'By Day 30, a complete inventory, a value heatmap and a decision-grade portfolio report, and you may walk away. By Day 60, business cases, named owners and an approved architecture for each selected initiative. By Day 90, at least two implementations at their agreed milestones with real users and visible measurement.'),
       ('How is this different from hiring a Chief AI Officer or a consultancy?', 'A full-time Chief AI Officer costs $400,000&ndash;$750,000+ a year, plus the time to recruit and to build a delivery function underneath them. A consultancy delivers a report and leaves. A Fractional AI Officer runs the portfolio, gets the implementations built and stays accountable for adoption.'),
       ('Can the AI Officer govern our engineering teams&rsquo; use of AI too?', f'Yes. One AI Officer can focus on strategy and adoption, on AI engineering governance, or both. <a class="link" href="{C.URL["gov"]}">See AI Governance</a>.'),
       ('What does it cost?', 'From $1,999 a month ($23,988 a year). The exact fee depends on your organisation&rsquo;s size and the scope of the portfolio, and is confirmed in a written proposal before anything starts.')]
faq = K.faq(FAQ, 'What leaders ask before they hire one.')
final = K.final('Find the two AI initiatives <span class="hl">worth scaling.</span>',
                'Book a 45-minute discovery call. We&rsquo;ll look at what AI is already running in your organisation and send a written plan, whether or not we work together.',
                K.lp_alt('fractional-ai-officer', 'maturity'))

page = '\n'.join([hero, gaps, phases, focus, econ, engage, faq, final])
ld = C.graph('fao', [{'@type': 'Service', 'name': 'Fractional AI Officer', 'serviceType': 'Fractional Chief AI Officer', 'url': C.SITE + C.FINAL_URL['fao'], 'provider': {'@id': C.ORG_ID},
                      'description': 'An embedded AI lead on retainer who inventories AI pilots and tools, selects the initiatives worth scaling and stays accountable for implementation and adoption.', 'areaServed': C.AREA,
                      'offers': {'@type': 'Offer', 'priceCurrency': 'USD', 'price': '1999', 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': '1999', 'priceCurrency': 'USD', 'unitText': 'MONTH', 'description': 'Starting price per month'}}},
                     K.faq_ld(FAQ)], crumb='Fractional AI Officer')
print('fao', C.write('fractional-ai-officer.html', 'fao', 'Fractional AI Officer: An Embedded AI Lead from $1,999/month | Upcore',
      'An embedded AI lead on retainer: inventory every AI pilot, pick the two or three worth scaling and see them live in 90 days, with a Day-30 walk-away. From $1,999 a month.',
      page, active='fao', ld=ld, group='solution', spine=False, main_cls='is-calm', annc_kind=C.ANNC_OPS))
