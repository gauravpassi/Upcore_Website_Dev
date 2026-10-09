"""/ai-engineering-governance (2026-10-07, calm rebuild). AI Governance for CTOs, CISOs and CFOs:
spend/tools/risks view (hero) -> four gaps, struck through -> five-layer stack explorer ->
90-day plan + commitments -> who leads it -> FAQ -> CTA. Facts and commitments come from the previous
page; prices are not shown here (the only public price is on /fractional-ai-officer#economics).
Run from the repo root: python tools/v4-build/build_gov.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import flow as FL

# ------------------------------------------------------------------ 1. hero: spend, tools and risks (illustrative)
SPEND = [('Frontend', '$12.4k', 43, '&darr; 8%', 'dn'), ('Backend API', '$8.1k', 28, 'flat', 'eq'), ('Data pipeline', '$5.6k', 19, '&uarr; 3%', 'up'), ('Mobile', '$2.9k', 10, '&darr; 2%', 'dn')]
TOOLS = [('Claude', 'Approved', 'ok', 'Engineering, data'), ('GitHub Copilot', 'Approved', 'ok', 'Engineering'), ('Cursor', 'Approved', 'ok', 'Two product teams'),
         ('ChatGPT, personal accounts', 'Restricted', 'md', 'Moved to the company plan'), ('Unvetted browser extension', 'Blocked', 'hi', 'Under review')]
RISKS = [('#511', 'Hallucinated package in the checkout service', 'hi', 'Blocked before merge'),
         ('#498', 'Customer emails pasted into a personal chatbot account', 'hi', 'Blocked, owner told'),
         ('#476', 'AI-written change to payment rounding', 'md', 'Held for a named reviewer')]
spend = ''.join(f'<li><span class="gv-k">{k}</span><span class="gv-bar"><i style="--w:{p}%"></i></span><b>{v}</b><em class="gv-d gv-{c}">{d}</em></li>' for k, v, p, d, c in SPEND)
tools = ''.join(f'<li><span class="gv-k">{k}</span><span class="gv-st gv-{c}">{s}</span><em>{t}</em></li>' for k, s, c, t in TOOLS)
risks = ''.join(f'<li class="dv-row"><code>{a}</code><span class="dv-t">{b}</span><span class="dv-risk r-{c}">{"High" if c == "hi" else "Medium"}</span><span class="dv-dec">{d}</span></li>' for a, b, c, d in RISKS)
SEG = [('spend', 'Spend'), ('tools', 'Tools'), ('risks', 'Risks')]
seg_tabs = ''.join(f'<button type="button" role="tab" class="dp-tab{" is-on" if i == 0 else ""}" id="gv-t{i}" aria-controls="gv-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{l}</button>' for i, (k, l) in enumerate(SEG))
DASH = f'''<figure class="gv-dash" data-seg>
<p class="sr">Example leadership view with illustrative data: AI spend by team this month, the AI tools in use with their approval status, and AI risks caught with the decision taken.</p>
<div class="dash-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>AI governance &middot; this month</span><span class="gate-pr">Leadership view</span></div>
<div class="gv-head"><div class="dp-tabs" role="tablist" aria-label="View">{seg_tabs}</div><span class="gv-sum"><b>$29.0k</b> AI spend &middot; <em class="gv-dn">&darr; 11%</em></span></div>
<div class="gv-p is-on" id="gv-p0" role="tabpanel" aria-labelledby="gv-t0"><p class="gv-cap">AI tool and token spend by team</p><ul class="gv-spend">{spend}</ul></div>
<div class="gv-p" id="gv-p1" role="tabpanel" aria-labelledby="gv-t1" hidden><p class="gv-cap">Every AI tool in use, with an owner and a status</p><ul class="gv-tools">{tools}</ul></div>
<div class="gv-p" id="gv-p2" role="tabpanel" aria-labelledby="gv-t2" hidden><p class="gv-cap">Caught this week, and what was decided</p><ol class="dv">{risks}</ol></div>
</div>
<figcaption><span>Example with illustrative data</span></figcaption>
</figure>'''
hero = K.hero_split([(C.URL['home'], 'Home'), (None, 'AI Governance')], 'AI Governance &middot; for CTOs, CISOs and CFOs',
                    'Get your AI <span class="hl">under control.</span>',
                    'Your teams already use Copilot, Cursor and ChatGPT. Get every AI tool and its cost in one view, sensitive data kept out, AI-written code checked and an audit trail your board can rely on.',
                    C.btn('hero', pulse=True) + '<a class="link" href="#plan">See the 90-day plan</a>', DASH)

# ------------------------------------------------------------------ 2. four gaps, struck through
GAPS = [('Inventory', 'Nobody can say which AI tools are in use, by whom, or where.', 'Every AI tool, team and repository mapped to an accountable owner, within 72 hours of access.'),
        ('Spend', 'Invoices and license totals, with no link to teams, products or results.', 'AI spend by team and user, where your tools expose usage data, set against what it produced.'),
        ('Security', 'Scanners built for human-written code miss hallucinated packages and injection patterns.', 'AI-aware checks on every commit, with hallucinated packages blocked before they ship.'),
        ('Audit trail', 'The board or an auditor asks which code was AI-assisted and who reviewed it. There is no answer.', 'A record from prompt to deploy: what changed, which controls applied and who decided.')]
gaps = f'''<section class="h-sec" id="gaps" aria-labelledby="gap-h"><div class="wrap gap-grid gv-gaps">
<div class="gap-side">{K.eyebrow("The gap")}<h2 id="gap-h" class="h-h2 h-h2--sm" data-reveal>AI is already inside your org. Nobody owns it.</h2>
<p class="gv-side" data-reveal style="--d:1">The CTO is shipping product, the CISO is watching the perimeter and finance sees one invoice. The place where AI risk actually sits has no owner.</p>
<dl class="gv-stats" data-reveal style="--d:2"><div><dt>45%</dt><dd>of AI-generated code contains security flaws <span>Veracode GenAI Code Security Report, 2025</span></dd></div>
<div><dt>42%</dt><dd>of companies scrapped most of their AI initiatives in 2025, up from 17% <span>S&amp;P Global Market Intelligence, 2025</span></dd></div></dl></div>
{FL.strike(GAPS, "Today", "With AI Governance")}</div></section>'''

# ------------------------------------------------------------------ 3. five-layer stack
LAYERS = [('Align', 'Policy and standards', 'What AI may be used for, by whom, with which data.',
           ['An inventory of every AI tool, repository and workflow, each with an accountable owner', 'An executable AI policy: approved, restricted, prohibited and escalation-required use, live by Day 14', 'Shared rules files and context for your codebase, and the right model for each task on cost and capability']),
          ('Accelerate', 'Development governance', 'How AI-written work is produced and reviewed.',
           ['Prompt standards and a pattern library your teams reuse', 'Automated review of every pull request for logic inversions, invented APIs and authentication bypasses', 'Multi-step AI workflows with human checkpoints where judgment matters']),
          ('Protect', 'Security', 'Checks built for the mistakes AI makes.',
           ['AI-aware security scanning on every commit: injection, credential sprawl, insecure output', 'Supply-chain checks that block hallucinated packages, with SBOMs generated', 'Infrastructure-as-code checks for insecure defaults before anything is applied', 'Continuous adversarial testing of AI-written code']),
          ('Comply', 'Audit and regulation', 'Evidence produced as the work happens.',
           ['Mapping to the frameworks that apply to you: SOC 2, HIPAA, GDPR, PCI-DSS, the EU AI Act', 'Traceability from prompt to deploy, with every AI decision logged', 'Quality gates in CI/CD that cannot be bypassed', 'A reusable evidence pack for enterprise security questionnaires']),
          ('Optimize', 'Spend and return', 'What AI costs, and what it is worth.',
           ['AI spend by team and user, with burn-rate alerts and forecasts', 'A live dashboard for the CTO and CISO: AI code share by team and risk exposure', 'Quality measures: defect rates and cycle time for AI-written against human-written work', 'Production monitoring that links incidents back to the prompts and changes behind them'])]
# isometric plates, drawn bottom-up so upper plates overlap lower ones
plates = ''
for i in reversed(range(len(LAYERS))):
    y = 60 + i * 50
    plates += (f'<g class="gv-plate" data-i="{i}" style="--i:{i}"><path class="gv-side" d="M40 {y} L170 {y + 38} L170 {y + 46} L40 {y + 8}Z M300 {y} L170 {y + 38} L170 {y + 46} L300 {y + 8}Z"/>'
               f'<path class="gv-top" d="M40 {y} L170 {y - 38} L300 {y} L170 {y + 38}Z"/>'
               f'<text x="318" y="{y + 6}"><tspan class="gv-tn">L{i + 1}</tspan> {LAYERS[i][0]}</text></g>')
STACK = f'<svg class="gv-iso" viewBox="0 0 420 300" aria-hidden="true" focusable="false">{plates}</svg>'
acc = ''.join(
    f'<li class="gv-l{" is-on" if i == 0 else ""}" data-i="{i}"><button type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="gv-l{i}" id="gv-lb{i}">'
    f'<span class="gv-ln">L{i + 1}</span><span class="gv-lt"><b>{n}</b><span>{s}</span></span><span class="pm" aria-hidden="true"></span></button>'
    f'<div class="gv-lp" id="gv-l{i}" role="region" aria-labelledby="gv-lb{i}"{"" if i == 0 else " hidden"}><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div></li>'
    for i, (n, s, d, items) in enumerate(LAYERS))
stack = f'''<section class="h-sec h-sec--alt" id="framework" aria-labelledby="fw-h"><div class="wrap">
{K.head("What we install", "Five layers. One owner. Full control.", "fw-h", "Each layer runs inside the tools you already use: your IDEs, Git, CI/CD and monitoring. Choose a layer to see what it covers.")}
<div class="gv-fw" data-layers><div class="gv-fig" data-reveal="scale">{STACK}</div><ol class="gv-acc">{acc}</ol></div>
</div></section>'''

# ------------------------------------------------------------------ 4. 90-day plan + commitments
PLAN = [('Day 14: policy live', 'Stakeholders aligned, AI tools audited and your executable AI policy published and enforced.'),
        ('Day 30: risk report', 'Your actual AI risk, quantified and mapped, with a gap analysis and roadmap. You can stop here.'),
        ('Day 60: observe mode', 'IDE, Git, CI/CD and production monitoring connected. Baseline captured, policies tuned, nothing blocked yet.'),
        ('Day 90: enforced', 'Gates live on every pull request, incidents traced to their cause and a full return-on-investment model.')]
COMMIT = ['Your governance environment is visible within 72 hours of access being granted.', 'Your executable AI policy is live by Day 14.',
          'At Day 30 you get the risk report, gap analysis and roadmap, and can walk away owing only for work done to that date.',
          'If the agreed controls are not in place by Day 90 for reasons within our control, we keep working at no extra management fee.']
commit = ''.join(f'<li data-reveal style="--d:{i}">{c}</li>' for i, c in enumerate(COMMIT))
plan = f'''<section class="h-sec" id="plan" aria-labelledby="plan-h"><div class="wrap">
{K.head("The 90-day plan", "A plan your board, auditor and CTO can back.", "plan-h", "Ninety days with a walk-away checkpoint at Day 30. After Day 90 the work moves from implementation to monthly oversight: new tool approvals, quarterly compliance reports and board summaries.")}
{FL.timeline(PLAN)}
<div class="gv-commit"><div><p class="h-col">What we commit to</p><p class="gv-cnote">Each commitment depends on you giving us the access, decisions and feedback we ask for on time.</p></div>
<ol class="gv-clist">{commit}</ol>
<p class="gv-not"><b>What we don&rsquo;t guarantee:</b> certification, a regulator&rsquo;s or auditor&rsquo;s conclusion, legal compliance in every jurisdiction, or the removal of every vulnerability. Those depend on your systems and on factors outside any vendor&rsquo;s control.</p></div>
</div></section>'''

# ------------------------------------------------------------------ 5. who leads it
WHO = [('A person, not software', 'A senior governance specialist embedded in your engineering team: attends standups, reviews pull requests, writes policy and owns the outcome.'),
       ('Background', 'Eight or more years in software engineering, with AI and compliance expertise.'),
       ('Time', 'Eight to twelve hours a week, dedicated: enough to follow your sprints, review AI-written changes and report weekly.'),
       ('Named before you sign', 'You meet your specialist on the discovery call. If the fit isn&rsquo;t right, we find a better one.')]
who = ''.join(f'<div data-reveal style="--d:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(WHO))
lead = f'''<section class="h-sec h-sec--tight h-sec--alt" aria-labelledby="who-h"><div class="wrap h-pilot">
<div class="h-pilot-k">{K.eyebrow("Who leads it")}<h2 id="who-h" class="h-h2 h-h2--sm" data-reveal>One accountable owner for AI risk.</h2>
<p class="gv-side" data-reveal style="--d:1">Delivered as a <a class="link" href="{C.URL["fao"]}">Fractional AI Officer</a> engagement with a governance focus. Choose whether your team leads with our guidance, or we run it for you.</p></div>
<dl class="h-pilot-spec">{who}</dl></div></section>'''

FAQ = [('How is this different from the security scanners we already run?', 'SAST and SCA tools were built for human-written code. We add checks for the mistakes AI makes, such as hallucinated packages, inverted logic and credential handling, plus the layers scanners don&rsquo;t cover: an AI inventory, policy, spend visibility and an audit trail.'),
       ('How fast can it start?', 'Your governance environment is visible within 72 hours of access being granted. For regulated enterprises, procurement, legal review and contract signature usually add four to eight weeks first; the 72 hours run from signing. We tell you what to prepare on the discovery call.'),
       ('Do we have to change our tools or infrastructure?', 'No. We connect to your IDEs, Git, CI/CD and monitoring, start in observe mode so nothing is blocked while we tune, and there is no lock-in during the pilot.'),
       ('Can our team run it, or do you run it for us?', 'Either. Done with you: your team leads and we guide, train and co-design, with full knowledge transfer. Done for you: you give us access, your AI tool list and your compliance obligations, and we audit, install, observe and report. One person is accountable in both.'),
       ('How does this relate to AI-Native Engineering?', f'AI Governance controls the AI your teams already use, across engineering and beyond. <a class="link" href="{C.URL["aine"]}">AI-Native Engineering</a> installs a complete governed delivery pipeline, from spec to production, with these controls built in. You can start with either.'),
       ('What does it cost?', f'AI Governance runs as a Fractional AI Officer engagement on a monthly fee, scoped to your organization&rsquo;s size and how hands-on you want us to be. <a class="link" href="{C.URL["fao"]}#economics">See Fractional AI Officer pricing</a>. You get a written proposal before anything starts.')]
faq = K.faq(FAQ, 'Questions security leaders ask.')
final = K.final('Get AI spend, data and code <span class="hl">under control in 90 days.</span>',
                'Book a 45-minute discovery call. We&rsquo;ll map where AI is already used in your organization and send a written plan, whether or not we work together.',
                K.lp_alt('ai-governance', 'gov'))

page = '\n'.join([hero, gaps, stack, plan, lead, faq, final])
ld = C.graph('gov', [{'@type': 'Service', 'name': 'AI Governance', 'serviceType': 'AI governance and AI engineering governance', 'url': C.SITE + C.FINAL_URL['gov'], 'provider': {'@id': C.ORG_ID},
                      'description': 'An AI inventory, AI spend visibility, data controls, AI-aware security checks and an audit trail, installed in 90 days with a Day-30 walk-away checkpoint.', 'areaServed': C.AREA},
                     K.faq_ld(FAQ)], crumb='AI Governance')
print('gov', C.write('ai-engineering-governance.html', 'gov', 'AI Governance: AI Spend, Data Controls &amp; Audit Trails | Upcore',
      'An inventory of every AI tool, AI spend by team, data controls, security checks on AI-written code and an audit trail, installed in 90 days with a Day-30 walk-away.',
      page, active='gov', ld=ld, group='solution', spine=False, main_cls='is-calm'))
