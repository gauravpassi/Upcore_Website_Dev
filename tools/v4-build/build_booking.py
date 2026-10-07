"""Booking pages for the two self-assessment funnels (2026-10-07, calm rebuild of the old hand-built pages):
/assessment (AI Governance Review, after the Governance Index) and /lp/maturity-review (AI Portfolio
Value Review, after the AI Maturity Index). The form is unchanged in substance: native POST to FormSubmit
(gaurav@, cc saswata@) with the same field names and subject, _next back to ?submitted=true, where the
Google Calendar scheduler appears. On submit: /api/booking-intent (booking attribution, as before). On the
?submitted=true view: generate_lead {lead_source} to GA4 and the "Lead Tracking" Google Ads conversion
(AW-16546427858/CN8BCPra5LsZENLn-dE9) as a gtag command through the Google tag GTM loads.
?tier=&score= from the quiz show a personal line and travel in a hidden field. Script: inline, below.
Run from the repo root: python tools/v4-build/build_booking.py"""
import os, sys, html as H
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K

CAL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ1_obz6QaD_10QlHvG7azfJ3015e7AdPmNiUtAgdK99p_9msqj5vR6pEnHV4KsEzNBRevBOFtPn?gv=true'
CONV = 'AW-16546427858/CN8BCPra5LsZENLn-dE9'

PAGES = [
    dict(key='assessment', file='assessment.html', path='/assessment', index='Governance Index', noindex=False, lead_source='assessment_form',
         title='Book an AI Governance Review | Upcore', meta='A free 45-minute AI Governance Review: your AI risk surface, compliance gaps and a Day-30 roadmap, with an honest view on fit.',
         eyebrow='Free AI Governance Review', h1='Book your <span class="hl">AI Governance Review.</span>',
         lead='In 45 minutes, a governance specialist maps where AI is already used across your engineering, checks it against the frameworks that matter to you, and gives you a concrete Day-30 roadmap. No pitch, no pressure.',
         cover=[('AI risk surface', 'Every AI tool in use, every ungoverned code path and every gap in how AI-written changes are reviewed today.'),
                ('Compliance gaps', 'Your current position against the frameworks that matter to you: EU AI Act, HIPAA, SOX, SOC 2 or GDPR.'),
                ('A Day-30 roadmap', 'What to govern first, in what order, and what you can show your board or auditor at 30 days.'),
                ('An honest view on fit', 'If governance work isn&rsquo;t the right move for you yet, we&rsquo;ll say so on the call.')],
         subject='New AI Governance Review Request via Upcore Website', next='https://www.upcoretech.com/assessment?submitted=true',
         selects=[('role', 'Role', 'Your role', True, ['CTO / VP Engineering', 'CISO / Security', 'CEO / Founder', 'COO / Operations', 'CFO / Finance', 'Other']),
                  ('ai-tools', 'AI Tools in Use', 'AI tools in use today', True, ['0 — evaluating options', '1–3 tools (early stage)', '4–10 tools (scaling)', '10+ tools (complex AI stack)']),
                  ('compliance', 'Compliance Framework', 'Main compliance requirement', False, ['None / not sure yet', 'GDPR', 'HIPAA', 'SOC 2', 'SOX', 'EU AI Act', 'Multiple frameworks'])],
         text=('challenge', 'What Is Driving This', 'What&rsquo;s driving this conversation? (optional)', 'e.g. The board asked for an AI risk report; our CISO flagged Copilot in code review.'),
         button='Book my governance review',
         facts=[('45 min', 'one focused call'), ('Free', 'no commitment'), ('Day-30', 'roadmap you keep')],
         meet='The call introduces the governance specialist who would work with your team. No surprise assignments: you decide whether the fit is right.',
         call=['We walk through your current AI tool stack and where the governance gaps actually are, not a generic checklist.',
               'You see a live example of how we review an AI-generated commit or flag a risky package.',
               'We map out what a Day-30 governance report would look like for your organisation.',
               'No slide deck and no sales pitch. If it isn&rsquo;t a fit, we say so on the call, not after.']),
    dict(key='maturity-review', file='lp/maturity-review.html', path='/lp/maturity-review', index='Maturity Index', noindex=True, lead_source='maturity_review_form',
         title='Book an AI Portfolio Value Review | Upcore', meta='A free 45-minute review of the AI pilots, tools and spend across your company, and which two or three initiatives are worth funding next.',
         eyebrow='Free AI Portfolio Value Review', h1='Book your <span class="hl">AI Portfolio Value Review.</span>',
         lead='In 45 minutes, an AI strategy specialist walks through the AI activity already running across your company, where it costs you, and whether two or three initiatives are worth funding in the next 90 days. No pitch, no pressure.',
         cover=[('Pilot and spend inventory', 'Every AI tool, pilot, vendor and employee-built automation running across departments, and what it costs.'),
                ('Ownership gaps', 'Where accountability for AI results is missing, duplicated or nobody&rsquo;s job.'),
                ('Fastest-value workflows', 'Which of your existing pilots or ideas could show measurable value first.'),
                ('An honest view on fit', 'If a coordination engagement isn&rsquo;t the right move for you yet, we&rsquo;ll say so directly.')],
         subject='New AI Portfolio Value Review Request via Maturity Index', next='https://www.upcoretech.com/lp/maturity-review?submitted=true',
         selects=[('role', 'Role', 'Your role', True, ['CEO / Founder', 'COO / Operations', 'CFO / Finance', 'CHRO / People', 'CTO / CIO', 'Other']),
                  ('ai-tools', 'AI Tools/Pilots Running Today', 'AI tools or pilots running today', True, ['0 — evaluating options', '1–3 tools (early stage)', '4–10 tools (scaling)', '10+ tools (complex AI stack)']),
                  ('driver', 'What\'s Driving This Now', 'What&rsquo;s driving this now?', False, ['Upcoming board meeting', 'Annual planning or budget cycle', 'AI tool renewal', 'Margin or cost pressure', 'Pilot(s) not showing ROI', 'Just exploring'])],
         text=('challenge', 'Anything Specific To Look At', 'Anything specific you want us to look at? (optional)', 'e.g. We have five pilots across marketing and ops and no idea which to keep.'),
         button='Book my portfolio review',
         facts=[('45 min', 'one focused call'), ('Free', 'no commitment'), ('2&ndash;3', 'initiatives worth funding')],
         meet='The call introduces the specialist who would coordinate your AI initiatives. No surprise assignments: you decide whether the fit is right.',
         call=['We walk through the AI pilots and spend you already have across departments, not a generic framework.',
               'You leave with a rough read on which two or three initiatives are worth funding next quarter.',
               'We show you what a 90-day coordination plan would look like for your company.',
               'No slide deck and no sales pitch. If your Index score is already strong, we tell you so.']),
]


def page(p):
    C.FINAL_URL[p['key']] = p['path']; C.PREVIEW_URL[p['key']] = '/preview/' + p['key']; C.URL[p['key']] = p['path']
    cover = ''.join(f'<li data-reveal style="--d:{i}"><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate(p['cover']))
    call = ''.join(f'<li>{x}</li>' for x in p['call'])
    facts = ''.join(f'<li><b>{n}</b><span>{l}</span></li>' for n, l in p['facts'])
    sel = ''
    for fid, name, label, req, opts in p['selects']:
        o = ''.join(f'<option>{H.escape(x)}</option>' for x in opts)
        sel += (f'<div class="bk-f"><label for="{fid}">{label}{" <i aria-hidden=true>*</i>" if req else ""}</label>'
                f'<select id="{fid}" name="{H.escape(name)}"{" required" if req else ""}><option value="" disabled selected>Select one</option>{o}</select></div>')
    tid, tname, tlabel, tph = p['text']
    form = f'''<div class="bk-card" data-reveal="scale" style="--d:2">
<div class="bk-form" id="form-wrap">
<h2 class="ct-fh" id="form-h">Request your review</h2>
<p class="ct-fs">Two minutes. You pick a time on the next screen; no waiting for a reply.</p>
<p class="bk-personal" id="personalized-line" hidden></p>
<form id="booking-form" action="https://formsubmit.co/gaurav@upcoretechnologies.com" method="POST" aria-labelledby="form-h">
<input type="hidden" name="_subject" value="{H.escape(p['subject'])}" />
<input type="hidden" name="_template" value="table" />
<input type="hidden" name="_captcha" value="false" />
<input type="text" name="_honey" class="ct-hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
<input type="hidden" name="_cc" value="saswata@upcoretechnologies.com" />
<input type="hidden" name="_next" value="{p['next']}" />
<input type="hidden" name="Index Score Context" id="index-score-field" value="" />
<div class="bk-grid">
<div class="bk-f"><label for="fname">First name <i aria-hidden="true">*</i></label><input type="text" id="fname" name="First Name" autocomplete="given-name" required /></div>
<div class="bk-f"><label for="lname">Last name <i aria-hidden="true">*</i></label><input type="text" id="lname" name="Last Name" autocomplete="family-name" required /></div>
<div class="bk-f bk-wide"><label for="email">Work email <i aria-hidden="true">*</i></label><input type="email" id="email" name="Email" autocomplete="email" required /></div>
<div class="bk-f bk-wide"><label for="company">Company <i aria-hidden="true">*</i></label><input type="text" id="company" name="Company" autocomplete="organization" required /></div>
{sel}
<div class="bk-f bk-wide"><label for="{tid}">{tlabel}</label><textarea id="{tid}" name="{H.escape(tname)}" rows="2" placeholder="{H.escape(tph)}"></textarea></div>
</div>
<button class="btn ct-send" type="submit" id="submit-btn"><span class="bk-send-t">{p['button']}</span> <span class="btn-ico">{C.ARROW}</span></button>
<p class="ct-fine">No commitment. Your details go to our team inbox through FormSubmit.co and are used only to arrange your call. <a href="/privacy">Privacy policy</a></p>
</form></div>
<div class="bk-done" id="success-msg" hidden>
<svg class="ct-tick" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle cx="26" cy="26" r="24"/><path d="m15 27 7.5 7.5L38 19"/></svg>
<h2 class="ct-fh">Request received. Now pick a time.</h2>
<p class="ct-fs">Your call is confirmed as soon as you choose a slot below.</p>
<iframe class="bk-cal" title="Choose a time: Google Calendar scheduling" data-src="{CAL}" loading="lazy"></iframe>
</div>
</div>'''
    hero = f'''<section class="h-hero bk-hero" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap bk-in">
<div class="bk-intro"><p class="h-eyebrow" data-reveal>{p['eyebrow']}</p>
<h1 id="hero-h" class="t-display" data-split>{p['h1']}</h1>
<p class="t-lead" data-reveal style="--d:2">{p['lead']}</p>
<ul class="bk-facts" data-reveal style="--d:3">{facts}</ul></div>
{form}
<div class="bk-more"><p class="h-col bk-k">What we cover</p>
<ol class="bk-cover">{cover}</ol>
<p class="h-col bk-k">On the call</p>
<ul class="bk-call">{call}</ul>
<p class="bk-meet"><b>You meet your specialist before committing.</b> {p['meet']}</p>
{K.PROOF_STRIP}</div>
</div></section>'''
    script = '''<script>
(function () {
  var q = new URLSearchParams(location.search), tier = q.get('tier'), score = q.get('score');
  if (tier) {
    var line = document.getElementById('personalized-line'), v = tier + (score ? ' (' + score + '/100)' : '');
    line.hidden = false; line.innerHTML = 'Your __INDEX__ score: <strong></strong>. We will pick up from exactly there on the call.';
    line.querySelector('strong').textContent = v;
    var f = document.getElementById('index-score-field'); if (f) f.value = v;
  }
  if (q.get('submitted') === 'true') {
    document.getElementById('form-wrap').hidden = true;
    var done = document.getElementById('success-msg'), cal = done.querySelector('iframe');
    done.hidden = false; done.parentNode.classList.add('is-done'); cal.src = cal.getAttribute('data-src');
    if (window.innerWidth <= 1000) setTimeout(function () { done.parentNode.scrollIntoView({ block: 'start' }); }, 60);
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event_params: null });
    window.dataLayer.push({ event: 'generate_lead', event_params: { lead_source: '__SOURCE__' } });
    (function () { window.dataLayer.push(arguments); })('event', 'conversion', { send_to: '__CONV__' });
    return;
  }
  var form = document.getElementById('booking-form');
  form.addEventListener('submit', function () {
    var btn = document.getElementById('submit-btn'), email = document.getElementById('email').value.trim();
    btn.disabled = true; btn.querySelector('.bk-send-t').textContent = 'Submitting\\u2026';
    if (!email || email.indexOf('@') < 0) return;
    try {
      var a = {}; try { a = JSON.parse(localStorage.getItem('upc_attrib') || '{}') || {}; } catch (e) {}
      var ck = function (re) { var m = document.cookie.match(re); return m ? m[1] : ''; };
      var cs = ''; try { cs = localStorage.getItem('upc_consent') || ''; } catch (e) {}
      if (cs !== 'granted' && cs !== 'denied') { var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {} cs = /^Europe\\//.test(tz) ? 'unknown_eu' : 'default_granted'; }
      fetch('/api/booking-intent', { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, page: location.pathname, cta_id: '__CTA__', cta_section: '__SECTION__', attrib: a,
          ga_client_id: ck(/(?:^|;\\s*)_ga=GA\\d\\.\\d\\.(\\d+\\.\\d+)/), ga_session_id: ck(/(?:^|;\\s*)_ga_TVRF5M70ES=GS\\d\\.\\d\\.s?(\\d+)/), consent: cs, referrer: document.referrer || '' }) }).catch(function () {});
    } catch (e) {}
  });
})();
</script>'''.replace('__INDEX__', p['index']).replace('__SOURCE__', p['lead_source']).replace('__CONV__', CONV) \
        .replace('__CTA__', 'assessment-form' if p['key'] == 'assessment' else 'review-form').replace('__SECTION__', 'assessment_page' if p['key'] == 'assessment' else 'maturity_review_page')
    ld = C.graph(p['key'], [{'@type': 'WebPage', 'name': H.unescape(p['title'].split(' | ')[0]), 'url': C.SITE + p['path'], 'about': {'@id': C.ORG_ID}}])
    return C.write(p['file'], p['key'], p['title'], p['meta'], hero + '\n' + script, active='', ld=ld, group='booking', spine=False, main_cls='is-calm bk-page', noindex=p['noindex'])


for p in PAGES:
    print(p['key'], page(p))
