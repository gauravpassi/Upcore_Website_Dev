"""Upcore frameworks: custom visual models with their research lineage.
Each builder returns (copy_html, visual_html)."""

CITE = {
    'hw': ('Hayes &amp; Wheelwright, &ldquo;Link Manufacturing Process and Product Life Cycles&rdquo;, Harvard Business Review, 1979', 'https://hbr.org/1979/01/link-manufacturing-process-and-product-life-cycles'),
    'kc': ('Kephart &amp; Chess, &ldquo;The Vision of Autonomic Computing&rdquo;, IEEE Computer, 2003', 'https://doi.org/10.1109/MC.2003.1160055'),
    'psw': ('Parasuraman, Sheridan &amp; Wickens, &ldquo;A Model for Types and Levels of Human Interaction with Automation&rdquo;, IEEE Trans. SMC-A, 2000', 'https://doi.org/10.1109/3468.844354'),
    'ls': ('Lee &amp; See, &ldquo;Trust in Automation: Designing for Appropriate Reliance&rdquo;, Human Factors, 2004', 'https://doi.org/10.1518/hfes.46.1.50_30392'),
    'little': ('J. D. C. Little, &ldquo;A Proof for the Queuing Formula: L = &lambda;W&rdquo;, Operations Research, 1961', 'https://doi.org/10.1287/opre.9.3.383'),
    'dft': ('Dixon, Freeman &amp; Toman, &ldquo;Stop Trying to Delight Your Customers&rdquo;, Harvard Business Review, 2010', 'https://hbr.org/2010/07/stop-trying-to-delight-your-customers'),
}


def cite(*keys, prefix='Derived from'):
    parts = [f'<a href="{CITE[k][1]}" target="_blank" rel="noopener nofollow">{CITE[k][0]}</a>' for k in keys]
    return f'<p class="fw-cite">{prefix}: ' + '; '.join(parts) + '.</p>'


def copy(kicker, title, paras, bullets, cites):
    p = ''.join(f'<p>{x}</p>' for x in paras)
    b = '<ul>' + ''.join(f'<li>{x}</li>' for x in bullets) + '</ul>' if bullets else ''
    return f'<div class="fw-copy"><span class="t-mono">{kicker}</span><h3 class="t-h3">{title}</h3>{p}{b}{cites}</div>'


# ---------------------------------------------------------------- F1 Matrix
def matrix():
    dots = [  # (label, x%, y%, hot)
        ('Order-status replies', 88, 30, True), ('Document chasing', 75, 38, True), ('Bank reconciliation', 87, 44, True),
        ('Lead qualification', 63, 33, True), ('Claims &amp; exception triage', 38, 33, False), ('Contract first-pass review', 26, 42, False),
        ('Quarterly compliance pack', 72, 64, False), ('Pricing strategy', 28, 64, False),
    ]
    d = ''.join(f'<span class="mx-dot{" hot" if h else ""}" style="--x:{x}%;--y:{y}%;--i:{i}" title="{l}">{i+1}</span>' for i, (l, x, y, h) in enumerate(dots))
    leg = ''.join(f'<li><i class="{"hot" if h else ""}">{i+1}</i>{l}</li>' for i, (l, x, y, h) in enumerate(dots))
    vis = f'''<div class="fw-vis" role="img" aria-label="Automation Fit Matrix: volume against how rule-based a process is. High-volume, rule-based work is automated end to end; high-volume judgment work gets an agent that drafts for a person.">
<div class="cap"><span>Automation Fit Matrix</span><span>Illustrative placement</span></div>
<div class="mx"><div class="mx-y"><span>Low volume</span><span>High volume</span></div>
<div class="mx-plot">
<div class="mx-q q-tl"><b>Agent drafts, people decide</b><span>High volume, judgment-heavy</span></div>
<div class="mx-q q-auto"><b>Automate end to end</b><span>High volume, rule-based: start here</span></div>
<div class="mx-q q-bl"><b>Keep it human-led</b><span>Low volume, judgment-heavy</span></div>
<div class="mx-q q-br"><b>Schedule &amp; batch</b><span>Low volume, rule-based</span></div>
{d}</div>
<div class="mx-x"><span>Judgment-heavy</span><span>Rule-based</span></div></div>
<ul class="mx-legend">{leg}</ul></div>'''
    c = copy('Strategy', 'Automation Fit Matrix',
             ['Not every process should be automated, and not in the same way. We score each workflow on two axes: how much volume it carries and how rule-based its decisions are.',
              'Where a process lands decides how we automate it: end to end, as a draft for a person to approve, on a schedule, or not at all.'],
             ['Scored in discovery against your real volumes', 'High-volume, rule-based work goes first, because it pays back fastest', 'Judgment-heavy work gets an agent that drafts, never one that decides'],
             cite('hw', prefix='Adapted from the product&ndash;process matrix'))
    return c, vis


# ---------------------------------------------------------------- F2 Control loop
def loop():
    # Nodes on a circle r=40 around (50,50), clockwise from the top.
    nodes = [('Sense', 'inputs change', 50, 10, '4.2s'), ('Reason', 'against your rules', 88.0, 37.6, '5.4s'),
             ('Act', 'in your systems', 73.5, 82.4, '.6s'), ('Verify', 'checks &amp; confidence', 26.5, 82.4, '1.8s'),
             ('Learn', 'log &amp; improve', 12.0, 37.6, '3.0s')]
    n = ''.join(f'<div class="lp-node" style="left:{x}%;top:{y}%;--dl:{dl}"><div><b>{t}</b><small>{s}</small></div></div>' for t, s, x, y, dl in nodes)
    vis = f'''<div class="fw-vis fw-vis--dark" role="img" aria-label="Agent Control Loop: sense, reason, act, verify, learn, around a core of your rules, code and data, with an approval gate when confidence is low.">
<div class="cap"><span>Agent Control Loop</span><span>Runs on every agent</span></div>
<div class="lp">
<svg viewBox="0 0 100 100" aria-hidden="true">
<circle class="ring" cx="50" cy="50" r="40"/>
<circle class="ring-run" cx="50" cy="50" r="40"/>
<circle class="pk" r="1.3"><animateMotion dur="6s" repeatCount="indefinite" path="M90 50 A40 40 0 1 1 10 50 A40 40 0 1 1 90 50"/></circle>
<circle class="pk-h" cx="88.05" cy="62.4" r="1.5"/>
</svg>
<div class="lp-core"><div><b>Your knowledge</b><small>rules &middot; code &middot; data &middot; history</small></div></div>
{n}
<span class="lp-human" style="left:79%;top:61%">Approval gate &middot; low confidence</span>
</div>
<div class="lp-key"><span><i></i>Agent step</span><span><i class="h"></i>Person approves</span></div></div>'''
    c = copy('Computer science', 'Agent Control Loop',
             ['Every Upcore agent runs the same closed loop: sense what changed, reason against your rules, act in your systems, verify the result and learn from the outcome.',
              'When confidence falls below the threshold you set, the loop stops at an approval gate instead of guessing.'],
             ['Grounded in your rules, code and data, not general knowledge', 'Every action verified and written to an audit log', 'Low-confidence decisions routed to a named person'],
             cite('kc', prefix='Adapted from the autonomic-computing control loop (monitor, analyze, plan, execute over shared knowledge)'))
    return c, vis


# ---------------------------------------------------------------- F3 Autonomy ladder
def ladder():
    levels = [('L0', 'Manual', 20, 'People do the work'), ('L1', 'Assist', 37, 'Agent suggests; people act'),
              ('L2', 'Draft &amp; approve', 55, 'Agent drafts; a person approves each item'),
              ('L3', 'Act within limits', 75, 'Agent acts under thresholds; exceptions go to people'),
              ('L4', 'Autonomous', 95, 'Agent acts; people audit samples')]
    cols = ''.join(f'<div class="ld-col{" cur" if i == 2 else (" done" if i < 2 else "")}" style="--h:{h}%;--i:{i}"><span class="ld-tag">{"Start here" if i == 2 else "Earned"}</span><div class="ld-bar"><span class="lv">{lv}</span><b>{t}</b></div></div>'
                   for i, (lv, t, h, d) in enumerate(levels))
    desc = ''.join(f'<li>{d}</li>' for lv, t, h, d in levels)
    vis = f'''<div class="fw-vis" role="img" aria-label="Autonomy Ladder: five levels from manual to autonomous. Agents start at level 2, drafting for approval, and move up only as measured accuracy on your real work builds evidence.">
<div class="cap"><span>Autonomy Ladder</span><span>Promotion on evidence</span></div>
<div class="ld">{cols}</div>
<ul class="ld-desc">{desc}</ul>
<div class="ld-meter"><span>Evidence: accuracy on your real work</span><div class="track"><div class="fill"></div></div><span class="next">earns L3</span></div></div>'''
    c = copy('Behavioral science', 'Autonomy Ladder',
             ['Trust in automation should be earned, not assumed. Too little and people redo the agent&rsquo;s work; too much and errors slip through.',
              'Every agent starts at Level 2, drafting work for a person to approve. It moves up only when its measured accuracy on your real work justifies it, and you approve every promotion.'],
             ['Five levels, from manual to autonomous with sampled audit', 'Promotion on measured accuracy, never by default', 'Any agent can be stepped back down at any time'],
             cite('psw', 'ls'))
    return c, vis


# ---------------------------------------------------------------- F4 Lead-time compression
def compress():
    before = [('work', 6), ('wait', 16), ('work', 5), ('wait', 22), ('work', 6), ('wait', 20), ('work', 5), ('wait', 20)]
    w2 = iter([3.5, 4.5, 4, 3.5])
    seg = lambda rows, after: ''.join(
        f'<span class="cp-seg {k}" style="--w:{w}{";--w2:" + str(next(w2)) if (after and k == "wait") else ""}"></span>' for k, w in rows)
    vis = f'''<div class="fw-vis" role="img" aria-label="Lead-time compression: before, 6 to 10 weeks of mostly waiting between short bursts of work; with agents chasing documents and replies, about 3 weeks, with the same work and far less waiting.">
<div class="cap"><span>Lead-Time Compression</span><span>Residential developer &middot; reported result</span></div>
<div class="cp">
<div class="cp-row"><div class="lbl"><span>Before: booking to first installment</span><b>6&ndash;10 wks</b></div><div class="cp-track">{seg(before, False)}</div></div>
<div class="cp-row after"><div class="lbl"><span>With agents chasing documents and replies</span><b>~3 wks</b></div><div class="cp-track">{seg(before, True)}</div></div>
<div class="cp-legend"><span><i></i>Work: checking, deciding</span><span><i class="w"></i>Waiting: on buyers, banks, documents</span></div>
<div><span class="cp-formula">Lead time <em>W</em> = work in progress <em>L</em> &divide; throughput <em>&lambda;</em></span></div>
<p class="fine" style="margin-top:0">Segment lengths are illustrative; the totals are the client&rsquo;s reported result.</p>
</div></div>'''
    c = copy('Operations research', 'Lead-Time Compression',
             ['Most process time is not work, it is waiting: for a reply, a document, a signature, a bank. Agents don&rsquo;t make your people work faster; they remove the waiting between the steps.',
              'That is where weeks come back. For one residential developer, time from booking to first installment fell from 6&ndash;10 weeks to about 3.'],
             ['Work stays with people; chasing goes to agents', 'Measured end to end, not task by task', 'Less work in progress means faster cash and fewer status calls'],
             cite('little', prefix='Grounded in Little&rsquo;s Law'))
    return c, vis


# ---------------------------------------------------------------- F5 Customer effort
def effort():
    before = ['Find the order email', 'Copy the order number', 'Open the courier site', 'No useful update', 'Fill in a contact form', 'Wait for a reply']
    after = ['Ask on WhatsApp', 'Live status and delivery window']
    lane = lambda steps, cls: ''.join(
        (f'<span class="ef-arrow" style="--i:{i}" aria-hidden="true">&rarr;</span>' if i else '') + f'<span class="ef-step{" ok" if (cls and i == len(steps) - 1) else ""}" style="--i:{i}">{s}</span>' for i, s in enumerate(steps))
    vis = f'''<div class="fw-vis" role="img" aria-label="Customer effort: six steps for a customer to find out where their order is, versus two steps with an order-status agent.">
<div class="cap"><span>Customer Effort Principle</span><span>Illustrative journey</span></div>
<div class="ef">
<div class="ef-lane"><div class="lbl"><b>Today</b><span>6 steps, 1&ndash;2 channels, a wait</span></div><div class="ef-steps">{lane(before, False)}</div></div>
<div class="ef-meter"><span>Customer effort</span><div class="track"><div class="fill" style="--v:92%"></div></div></div>
<div class="ef-lane after"><div class="lbl"><b>With an order-status agent</b><span>2 steps, 1 channel, instant</span></div><div class="ef-steps">{lane(after, True)}</div></div>
<div class="ef-meter after"><span>Customer effort</span><div class="track"><div class="fill" style="--v:16%"></div></div></div>
</div></div>'''
    c = copy('Consumer behavior', 'Customer Effort Principle',
             ['Customers don&rsquo;t stay loyal because you delighted them once. They leave when getting a simple answer takes too much effort.',
              'So we design agents to remove steps: the answer comes to the customer, on the channel they already use, with live data behind it.'],
             ['Fewer steps for the customer, fewer tickets for your team', 'Answers from live store, ERP and carrier data', 'Exceptions handed to a person with the full context'],
             cite('dft', prefix='Grounded in customer-effort research'))
    return c, vis


BUILDERS = {'matrix': matrix, 'loop': loop, 'ladder': ladder, 'compress': compress, 'effort': effort}


def single(key, eyebrow, h2, lead, alt=False):
    c, v = BUILDERS[key]()
    import re as _re
    c = _re.sub(r'<span class="t-mono">.*?</span>', '', c, count=1)
    cls = 'sec'
    return f'''<section class="{cls}" aria-labelledby="fw-{key}-h"><div class="wrap">
<div class="sec-head"><div class="eyebrow" data-reveal>{eyebrow}</div><h2 id="fw-{key}-h" class="t-h2" data-reveal>{h2}</h2><p class="t-lead" data-reveal style="--d:1">{lead}</p></div>
<div class="fw-single"><div class="fw-panel">{c}{v}</div></div></div></section>'''


def suite(order=None, eyebrow='Upcore frameworks', h2='The thinking behind <span class="ul-draw">every engagement.</span>', lead=None):
    meta = {'matrix': ('Strategy', 'Automation Fit Matrix'), 'loop': ('Computer science', 'Agent Control Loop'),
            'ladder': ('Behavioral science', 'Autonomy Ladder'), 'compress': ('Operations research', 'Lead-Time Compression'),
            'effort': ('Consumer behavior', 'Customer Effort Principle')}
    order = order or ['matrix', 'loop', 'ladder', 'compress']
    lead = lead or 'Four working models we apply with every client, each grounded in established research.'
    tabs = ''.join(f'<button class="fw-tab" role="tab" id="fwt-{k}" aria-controls="fwp-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="n">{i+1:02d}</span><span class="d">{meta[k][0]}</span><b>{meta[k][1]}</b><span class="bar" aria-hidden="true"></span></button>'
                   for i, k in enumerate(order))
    panels = ''
    for i, k in enumerate(order):
        c, v = BUILDERS[k]()
        panels += f'<div class="fw-panel{" on" if i == 0 else ""}" id="fwp-{k}" role="tabpanel" aria-labelledby="fwt-{k}">{c}{v}</div>'
    cols = f' style="--fw-cols:{len(order)}"'
    return f'''<section class="sec" id="frameworks" aria-labelledby="fw-h"><div class="wrap">
<div class="sec-head sec-head--split"><div><div class="eyebrow" data-reveal>{eyebrow}</div><h2 id="fw-h" class="t-h2" data-reveal>{h2}</h2></div>
<p class="t-lead" data-reveal style="--d:1">{lead}</p></div>
<div class="fw" data-fw{cols}><div class="fw-tabs" role="tablist" aria-label="{eyebrow}">{tabs}</div><div class="fw-stage">{panels}</div></div>
</div></section>'''


CONTROLS = [
    ('<path d="M3 15a4 4 0 0 0 4 4h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 6.1 9.6 4 4 0 0 0 3 15z"/>', 'Your cloud or ours', 'Where your policies require it, agents are deployed into your own cloud tenancy.'),
    ('<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>', 'Scoped, revocable access', 'Agents get only the permissions a workflow needs, and you can revoke them at any time.'),
    ('<path d="M4 5h16M4 10h16M4 15h10M4 20h7"/>', 'Every action logged', 'A complete audit trail of what each agent saw, decided and did. Changes to records can be rolled back.'),
    ('<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>', 'Human approval thresholds', 'You set what agents may do alone. Everything above goes to a named person.'),
    ('<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>', 'Your data stays yours', 'Model providers are configured so your data is not used to train their models.'),
    ('<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>', 'Certified delivery', 'Our information security and quality management are certified to ISO 27001 and ISO 9001, and every engagement runs on CMMI Level 3 processes.'),
]


def controls():
    cells = ''.join(f'<div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ic}</svg><b>{t}</b><p>{p}</p></div>' for i, (ic, t, p) in enumerate(CONTROLS))
    return f'''<section class="sec" aria-labelledby="ctrl-h"><div class="wrap">
<div class="sec-head sec-head--split"><div><div class="eyebrow" data-reveal>Enterprise controls</div><h2 id="ctrl-h" class="t-h2" data-reveal>Built for <span class="ul-draw">your security review.</span></h2></div>
<p class="t-lead" data-reveal style="--d:1">The controls your CISO, compliance team and auditors will ask about are part of every deployment, not an upgrade. <a class="link" href="/security">See how we handle security</a></p></div>
<div class="ctrl" data-reveal>{cells}</div></div></section>'''
