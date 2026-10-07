"""/contact (2026-10-07, calm rebuild): three ways to reach us + a short message form, what happens
next, where we are, three questions. The form posts to the same FormSubmit endpoint as before
(gaurav@, cc saswata@, subject "New Contact Form - name · company"); the visitor confirmation email
the old page sent through FormSubmit was dropped (FormSubmit asks unknown addresses to activate a form
instead of delivering, and the page promises no auto-replies). On success it pushes generate_lead
(lead_source: contact_form) with no personal data. Script: the "Contact" module in js/upcore-v5.js.
Run from the repo root: python tools/v4-build/build_contact.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K

MAIL = 'gaurav@upcoretechnologies.com'
WA = 'https://wa.me/919988135327?text=Hi%20Upcore%20team%2C%20I%27d%20like%20to%20talk%20about%20'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Bestech+Business+Tower+Sector+66+Mohali+Punjab+160062'

WAYS = [('book', 'Book a discovery call', '45 minutes on your situation. You leave with a written plan, whether or not we work together.', 'Recommended',
         C.btn('contact_ways', cls='btn btn--sm', label='Choose a time')),
        ('wa', 'WhatsApp', 'Best for quick questions and first conversations. We usually reply within 30 minutes during business hours.', '+91 99881 35327',
         f'<a class="link" href="{WA}" target="_blank" rel="noopener" data-gtm-cta="whatsapp" data-gtm-cta-type="secondary" data-gtm-cta-section="contact_ways">Open WhatsApp<span class="sr"> (opens in a new tab)</span></a>'),
        ('mail', 'Email', 'For detailed questions, partnerships or security reviews. We reply within 4 business hours.', MAIL,
         f'<a class="link" href="mailto:{MAIL}" data-gtm-cta="email" data-gtm-cta-type="secondary" data-gtm-cta-section="contact_ways">Write to us</a>')]
W_I = {'book': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8 14h3"/>',
       'wa': '<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-1.8-1.8l.8-1-1-2z"/>',
       'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>'}
ways = ''.join(f'<li class="ct-way{" is-main" if k == "book" else ""}" data-reveal style="--d:{i + 3}"><span class="ct-wi">{K.svg_icon(W_I[k])}</span>'
               f'<span class="ct-wc"><b>{t}</b><span>{d}</span><em>{m}</em></span><span class="ct-wa">{a}</span></li>' for i, (k, t, d, m, a) in enumerate(WAYS))

TOPICS = ['AI-Native Engineering', 'AI Governance', 'Process automation', 'Fractional AI Officer', 'Something else']
topics = ''.join(f'<label class="ct-chip"><input type="radio" name="topic" value="{t}"{" required" if i == 0 else ""} /><span>{t}</span></label>' for i, t in enumerate(TOPICS))
FORM = f'''<div class="ct-form-wrap" data-reveal="scale" style="--d:2">
<form class="ct-form" data-contact novalidate aria-labelledby="form-h">
<h2 id="form-h" class="ct-fh">Send us a message</h2>
<p class="ct-fs">Tell us what you&rsquo;re working on. A person reads every message.</p>
<div class="ct-grid">
<div class="ct-f"><input id="cf-name" name="name" type="text" autocomplete="name" placeholder=" " required /><label for="cf-name">Your name</label></div>
<div class="ct-f"><input id="cf-company" name="company" type="text" autocomplete="organization" placeholder=" " required /><label for="cf-company">Company</label></div>
<div class="ct-f ct-f--wide"><input id="cf-email" name="email" type="email" autocomplete="email" placeholder=" " required /><label for="cf-email">Work email</label></div>
</div>
<fieldset class="ct-topics"><legend>What can we help with?</legend><div>{topics}</div></fieldset>
<div class="ct-f ct-f--wide"><textarea id="cf-msg" name="message" rows="4" placeholder=" "></textarea><label for="cf-msg">What would you like to solve? (optional)</label></div>
<input class="ct-hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" />
<p class="ct-err" role="alert" hidden></p>
<button class="btn ct-send" type="submit"><span class="ct-send-t">Send message</span> <span class="btn-ico">{C.ARROW}</span></button>
<p class="ct-fine">We use your details only to reply. See our <a href="/privacy">privacy policy</a>.</p>
</form>
<div class="ct-done" hidden tabindex="-1" aria-live="polite">
<svg class="ct-tick" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle cx="26" cy="26" r="24"/><path d="m15 27 7.5 7.5L38 19"/></svg>
<h2 class="ct-fh">Message sent. Thank you.</h2>
<p class="ct-fs">A member of our team will reply to your email within 4 business hours, usually much sooner on business days.</p>
<ol class="ct-next"><li><b>Today</b><span>We read your message and check who is best placed to answer it.</span></li><li><b>Within 4 business hours</b><span>A reply from a person, with answers or a proposed time for a call.</span></li><li><b>On the call</b><span>45 minutes on your situation, and a written plan afterwards.</span></li></ol>
</div>
</div>'''

hero = f'''<section class="h-hero ct-hero" aria-labelledby="hero-h"><div class="hero-glow" aria-hidden="true"></div><div class="wrap ct-in">
<div>{K.crumb([(C.URL['home'], 'Home'), (None, 'Contact')])}
<p class="h-eyebrow" data-reveal>Contact</p>
<h1 id="hero-h" class="t-display" data-split>Talk to a person, <span class="hl">not a bot.</span></h1>
<p class="t-lead" data-reveal style="--d:2">Every message is read and answered by someone at Upcore. Pick whichever way suits you.</p>
<ul class="ct-ways">{ways}</ul></div>
{FORM}
</div></section>'''

where = f'''<section class="h-sec h-sec--alt" aria-labelledby="where-h"><div class="wrap ct-where">
<div>{K.eyebrow("Where we are")}<h2 id="where-h" class="h-h2 h-h2--sm" data-reveal>Mohali, India. Working with clients in six countries.</h2></div>
<dl class="ct-facts">
<div data-reveal><dt>Office</dt><dd>Upcore Technologies<br />Unit No. 625, 6th Floor, Tower-A<br />Bestech Business Tower, Sector 66<br />Mohali, Punjab 160062, India<br /><a class="link" href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps<span class="sr"> (opens in a new tab)</span></a></dd></div>
<div data-reveal style="--d:1"><dt>Business hours</dt><dd>Monday to Saturday<br />9:00 am to 7:00 pm IST<br /><span class="ct-mut">WhatsApp has extended hours. Pilot working hours are agreed with each client.</span></dd></div>
<div data-reveal style="--d:2"><dt>Phone &amp; WhatsApp</dt><dd><a href="tel:+919988135327">+91 99881 35327</a></dd><dt>Email</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd><dt>Elsewhere</dt><dd><a href="https://www.linkedin.com/company/upcoretech" target="_blank" rel="noopener">LinkedIn<span class="sr"> (opens in a new tab)</span></a> &middot; <a href="{C.URL['security']}">Security &amp; trust</a></dd></div>
</dl></div></section>'''

FAQ = [('What happens on a discovery call?', 'Forty-five minutes on where you are with AI and what you want to fix. We ask about your delivery process or your highest-volume workflows, then send a written plan: what to do first, in what order, and what it should return. You get the plan whether or not we work together.'),
       ('Can we sign an NDA before sharing details?', f'Yes. We sign a mutual NDA before any call where sensitive details are shared. Our contracts, data handling and certifications are on the <a class="link" href="{C.URL["security"]}">security page</a>.'),
       ('Which time zones do you work in?', 'Our delivery team is in India, with clients in the USA, UK, South Africa, Australia and Mauritius. Working hours are agreed in each pilot plan, and your team&rsquo;s analyst is your single point of contact.')]
faq = K.faq(FAQ, 'Before you get in touch.')

page = '\n'.join([hero, where, faq])
ld = C.graph('contact', [{'@type': 'ContactPage', 'name': 'Contact Upcore Technologies', 'url': C.SITE + C.FINAL_URL['contact'], 'about': {'@id': C.ORG_ID},
                          'mainEntity': {'@type': 'Organization', '@id': C.ORG_ID, 'email': MAIL, 'telephone': '+91-99881-35327',
                                         'address': {'@type': 'PostalAddress', 'streetAddress': 'Unit No. 625, 6th Floor, Tower-A, Bestech Business Tower, Sector 66',
                                                     'addressLocality': 'Mohali', 'addressRegion': 'Punjab', 'postalCode': '160062', 'addressCountry': 'IN'}}},
                         K.faq_ld(FAQ)], crumb='Contact')
print('contact', C.write('contact.html', 'contact', 'Contact Upcore: Book a Call, WhatsApp or Email | Upcore',
      'Talk to a person at Upcore: book a 45-minute discovery call, message us on WhatsApp or email. We reply within 4 business hours.',
      page, active='contact', ld=ld, group='company', spine=False, main_cls='is-calm'))
