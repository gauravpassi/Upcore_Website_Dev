"""/platform: Business Process Automation (2026-10-07, calm rebuild; replaces the old Studio/Forge/
Workforce services overview). For COOs and operations leaders: live work-queue view (hero) ->
what we automate, by function -> the Autonomy Ladder -> results -> how engagements work ->
controls -> who we help -> FAQ -> CTA. Workflows, results and FAQs reuse segment_copy.py.
Run from the repo root: python tools/v4-build/build_bpa.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import flow as FL
import tools as TL
import segment_copy as S
from frameworks import CONTROLS
from v4parts import TESTIMONIALS

# ------------------------------------------------------------------ 1. hero: the agent work queue (illustrative)
KPI = [('1284', 'tasks handled'), ('91%', 'without a person'), ('117', 'sent for approval'), ('2 min', 'median first reply')]
ROWS = [('#2207', 'Where is my order? (WhatsApp)', 'lo', 'Handled', 'Answered from live carrier tracking'),
        ('#118', 'Bank sanction letter still missing', 'md', 'Chased', 'Reminder sent by email and WhatsApp'),
        ('#3302', 'Invoice 45 days overdue', 'md', 'Chased', 'Second reminder sent, CRM updated'),
        ('#091', 'Refund above your threshold', 'hi', 'To a person', 'Sent to your team with the full context')]
kpis = ''.join(f'<div><b data-count>{v}</b><span>{l}</span></div>' for v, l in KPI)
rows = ''.join(f'<li class="dv-row" style="--i:{i}"><code>{a}</code><span class="dv-t">{b}</span><span class="dv-risk r-{c}">{d}</span><span class="dv-dec">{e}</span></li>' for i, (a, b, c, d, e) in enumerate(ROWS))
QUEUE = f'''<figure class="dash" data-dash>
<p class="sr">Example operations view with illustrative data: this week agents handled 1,284 tasks, 91% without a person; 117 were sent to a person for approval, and the median first reply took two minutes.</p>
<div class="dash-win" aria-hidden="true">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>Operations agents &middot; this week</span><span class="gate-pr">Work queue</span></div>
<div class="dash-kpis">{kpis}</div>
<div class="dash-log"><div class="dash-log-h"><b>Latest work</b><span>What each agent did, and what went to a person</span></div><ol class="dv">{rows}</ol></div>
</div>
<figcaption><span>Example with illustrative data</span><button class="gate-toggle dash-toggle" type="button" aria-label="Pause animation">Pause</button></figcaption>
</figure>'''
hero = K.hero_split([(C.URL['home'], 'Home'), (None, 'Business Process Automation')], 'Business Process Automation &middot; for COOs and operations leaders',
                    'Let AI do <span class="hl">the busywork.</span>',
                    'Agents that run the repetitive work in support, operations and finance: answering status questions, chasing documents and payments, and checking files against your rules, inside the systems you already use.',
                    C.btn('hero', pulse=True) + '<a class="link" href="#workflows">See what we automate</a>', QUEUE,
                    micro='Our standard: a first agent live within 30 days of design sign-off')

# ------------------------------------------------------------------ 2. what we automate, by function
FUNCS = [('Customer support', [
            ('Order and delivery status', 'Answers &ldquo;where is my order?&rdquo; on WhatsApp, email and chat from live store, ERP and carrier data.', 'Fewer tickets, faster replies at peak'),
            ('Returns and damage claims', 'Collects photos and order details, checks your returns policy and routes refunds above your threshold to a person.', 'Claims logged in minutes, not days'),
            ('Customer sentiment', 'Reads reviews, tickets and chats to flag product, delivery and service issues before they become a pattern.', 'Problems caught early')]),
         ('Operations', [
            ('Document collection and checks', 'Requests, chases, reads and checks documents against your SOPs, and files them in the right place.', 'Complete files without the back-and-forth'),
            ('Customer and partner updates', 'Sends proactive status updates at every milestone and answers &ldquo;where are we?&rdquo; from live data.', 'Fewer status calls'),
            ('Scheduling and intake', 'Books, reschedules and confirms appointments, collects intake details and keeps calendars in sync.', 'Fuller schedules, less admin')]),
         ('Finance', [
            ('Collections and payment follow-ups', 'Tracks every milestone and invoice, chases customers, banks and partners on your schedule and escalates only the exceptions.', 'Cash in sooner'),
            ('Bank and card reconciliation', 'Transactions categorized and matched; only mismatches reach a person, with the reason.', 'Hours of manual matching removed'),
            ('Timesheets and billing', 'Timesheets chased and checked, and invoices drafted from approved hours.', 'Invoices out on time')]),
         ('Sales', [
            ('Lead response and qualification', 'Answers every inquiry within minutes, qualifies it against your criteria and books the next step with the right person.', 'Every inquiry answered fast'),
            ('CRM hygiene', 'Keeps records, stages and follow-ups current without anyone updating them by hand.', 'A pipeline you can trust'),
            ('Ad spend audits', 'Watches Google and Meta accounts daily for wasted spend, pacing problems and falling returns, with plain-English alerts.', 'Spend moved to what converts')]),
         ('Compliance &amp; reporting', [
            ('Compliance checks in your workflow', 'Runs each check inside your team&rsquo;s own process and records the result, instead of a separate licensed tool.', 'Checks done, evidence kept'),
            ('Reporting and compliance packs', 'Pulls data from your systems into weekly operations reports and regulator-ready packs.', 'Reports ready on Monday morning'),
            ('Review preparation', 'Data pulls and draft review packs prepared before every client or board review.', 'Packs ready before each meeting')])]
ftabs = ''.join(f'<button type="button" role="tab" class="dp-tab{" is-on" if i == 0 else ""}" id="fn-t{i}" aria-controls="fn-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>' for i, (n, w) in enumerate(FUNCS))
fpanels = ''.join(f'<div class="bp-fp{" is-on" if i == 0 else ""}" data-seg-panel id="fn-p{i}" role="tabpanel" aria-labelledby="fn-t{i}"{"" if i == 0 else " hidden"}>{FL.outcome_rows(w)}</div>' for i, (n, w) in enumerate(FUNCS))
TOOLS = ['salesforce', 'hubspot', 'zoho', 'shopify', 'zendesk', 'microsoft', 'microsoftoutlook', 'microsoftteams', 'gmail', 'whatsapp', 'slack', 'powerautomate', 'n8n']
work = f'''<section class="h-sec" id="workflows" aria-labelledby="wf-h"><div class="wrap">
{K.head("What we automate", "The work that grows faster than headcount.", "wf-h", "We start where the volume is high and the rules are clear, so every hour saved shows up in your costs or your service. Choose a function.")}
<div class="bp-fn" data-seg><div class="dp-tabs bp-tabs" role="tablist" aria-label="Business function">{ftabs}</div>{fpanels}</div>
{TL.strip(TOOLS, "Connects to")}
</div></section>'''

# ------------------------------------------------------------------ 3. the Autonomy Ladder
LEVELS = [('L0', 'Manual', 'People do the work.', 'Everything', 'Nothing yet'),
          ('L1', 'Assist', 'The agent suggests; people act.', 'Every action', 'Suggestions and lookups'),
          ('L2', 'Draft &amp; approve', 'The agent drafts; a person approves each item.', 'Approves each item', 'Drafts every item'),
          ('L3', 'Act within limits', 'The agent acts under your thresholds; exceptions go to people.', 'Handles the exceptions', 'Everything under your limits'),
          ('L4', 'Autonomous', 'The agent acts; people audit samples.', 'Audits samples', 'The whole workflow')]
lv_btn = ''.join(f'<button type="button" class="bp-lv{" is-on" if i == 2 else ""}" role="tab" id="lv-t{i}" aria-controls="lv-p" aria-selected="{"true" if i == 2 else "false"}" tabindex="{0 if i == 2 else -1}" data-i="{i}" style="--h:{20 + i * 19}%">'
                 f'<span class="bp-bar"><i></i></span><span class="bp-lk">{k}</span><b>{t}</b>{"<em>Start here</em>" if i == 2 else ""}</button>' for i, (k, t, d, p, a) in enumerate(LEVELS))
lv_data = ''.join(f'<template data-lv="{i}"><span class="bp-dk">{k} &middot; {t}</span><p class="bp-dd">{d}</p><dl><div><dt>The agent</dt><dd>{a}</dd></div><div><dt>Your people</dt><dd>{p}</dd></div></dl></template>' for i, (k, t, d, p, a) in enumerate(LEVELS))
k, t, d, p, a = LEVELS[2]
ladder = f'''<section class="h-sec h-sec--alt" id="autonomy" aria-labelledby="lad-h"><div class="wrap bp-lad-wrap">
<div>{K.eyebrow("How much the agent does")}<h2 id="lad-h" class="h-h2 h-h2--sm" data-reveal>Autonomy is earned, one level at a time.</h2>
<p class="bp-side" data-reveal style="--d:1">Every agent starts at Level 2, drafting work for a person to approve. It moves up only when its measured accuracy on your real work justifies it, and you approve every promotion. Any agent can be stepped back down at any time.</p></div>
<div class="bp-lad" data-ladder data-reveal><div class="bp-lvs" role="tablist" aria-label="Autonomy levels">{lv_btn}</div>
<div class="bp-det" id="lv-p" role="tabpanel" aria-live="polite"><span class="bp-dk">{k} &middot; {t}</span><p class="bp-dd">{d}</p><dl><div><dt>The agent</dt><dd>{a}</dd></div><div><dt>Your people</dt><dd>{p}</dd></div></dl></div>{lv_data}</div>
</div></section>'''

# ------------------------------------------------------------------ 4. results
strip = lambda s: s.replace('<br />', ' &middot; ')
RES = [('Automation', S.P_RETAIL[0], 'fewer delivery-support tickets, with 10,000+ queries automated a month', strip(S.P_RETAIL[1])),
       ('Automation', S.P_RE[0], 'to the first installment, down from 6&ndash;10 weeks', strip(S.P_RE[1])),
       ('Automation', S.P_COMPLIANCE[0], 'of licensed compliance tooling replaced by an agent', strip(S.P_COMPLIANCE[1]))]
q = TESTIMONIALS['ops'][0]
results = K.results_band('Results', 'Already running on agents.', RES, quote=(q[0], q[1]))

# ------------------------------------------------------------------ 5. how engagements work
engage = f'''<section class="h-sec" id="engagement" aria-labelledby="eng-h"><div class="wrap">
{K.head("How engagements work", "Start with one workflow. Scale what works.", "eng-h", "We pick the workflow with the most volume and the clearest rules, so the first result shows up quickly. Our standard is a first agent live within 30 days of design sign-off, and each further agent reuses the same connections.")}
{FL.timeline(S.PATH_STD)}
</div></section>'''

# ------------------------------------------------------------------ 6. controls
ctl = ''.join(f'<li data-reveal style="--d:{i % 2}">{K.svg_icon(ic, "1.5")}<b>{t}</b><p>{p}</p></li>' for i, (ic, t, p) in enumerate(CONTROLS))
controls = f'''<section class="h-sec h-sec--tight h-sec--alt" aria-labelledby="ctl-h"><div class="wrap h-security">
<div>{K.eyebrow("Controls")}<h2 id="ctl-h" class="h-h2 h-h2--sm" data-reveal>Built to pass your security review.</h2>
<a class="link" href="{C.URL["security"]}" data-reveal style="--d:1">Read the security details</a></div>
<ul class="h-sec-list">{ctl}</ul></div></section>'''

# ------------------------------------------------------------------ 7. who we help
SEGS = [('ecommerce-retail', 'Ecommerce &amp; Retail', 'Order status, returns, catalog accuracy and ad spend'),
        ('operations-heavy', 'Operations-Heavy Businesses', 'Collections, documents, follow-ups and status updates'),
        ('professional-services', 'Professional Services', 'Accounting, law, wealth and staffing firms'),
        ('tech-software', 'Tech &amp; Software', 'Governed AI delivery for engineering teams')]
segs = ''.join(f'<li><a href="{C.URL[k]}"><b>{t}</b><span>{d}</span><i aria-hidden="true">{C.ARROW}</i></a></li>' for k, t, d in SEGS)
who = f'''<section class="h-sec h-sec--tight" aria-labelledby="who-h"><div class="wrap ab-split">
<div>{K.eyebrow("Who we help")}<h2 id="who-h" class="h-h2 h-h2--sm" data-reveal>Find the workflows for your industry.</h2></div>
<div class="h-router h-router--one"><ul>{segs}</ul></div></div></section>'''

FAQ = [('Which systems do you work with?', 'We build on what you already run: CRMs such as Salesforce, HubSpot and Zoho; ERPs; helpdesks; email; WhatsApp; shared drives and industry systems. Agents connect through APIs where they exist and through email and documents where they don&rsquo;t.'),
       ('Does the AI make decisions on its own?', 'Only within the limits you set. Agents handle the repetitive work; anything above your thresholds, such as write-offs, exceptions or customer disputes, goes to a named person. Every action is logged.'),
       ('Who runs this after go-live?', 'We do, with your team. A monthly retainer covers monitoring, tuning and new workflows, and your team is trained to understand and own what has been built.'),
       S.FAQ_DATA, S.FAQ_SPEED, S.FAQ_COST]
faq = K.faq(FAQ, 'Questions operations leaders ask.')
final = K.final('Find the three processes <span class="hl">worth automating first.</span>',
                'Book a 45-minute discovery call. We&rsquo;ll map your highest-volume workflows and send a written plan: what to automate, in what order, and what it should return.',
                K.lp_alt('platform', 'maturity'))

page = '\n'.join([hero, work, ladder, results, engage, controls, who, faq, final])
ld = C.graph('bpa', [{'@type': 'Service', 'name': 'Business Process Automation', 'serviceType': 'AI agents for business process automation', 'url': C.SITE + C.FINAL_URL['bpa'], 'provider': {'@id': C.ORG_ID},
                      'description': 'AI agents that run repetitive support, operations, finance, sales and compliance work inside existing systems, with human approval thresholds and a full audit trail.', 'areaServed': C.AREA},
                     K.faq_ld(FAQ)], crumb='Business Process Automation')
print('bpa', C.write('platform.html', 'bpa', 'Business Process Automation with AI Agents | Upcore',
      'AI agents that chase documents and payments, answer status questions and keep records current in your systems, with people approving what matters.',
      page, active='bpa', ld=ld, group='solution', spine=False, main_cls='is-calm', annc_kind=C.ANNC_OPS))
