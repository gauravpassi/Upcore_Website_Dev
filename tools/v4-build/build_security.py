"""/security (2026-10-07, calm rebuild). For the CISO and procurement reader:
data-path explorer hero -> six short answers + certifications -> how code and data are handled ->
AI in our delivery (controls) -> frameworks we produce evidence for -> documents before you sign ->
entity and jurisdiction questions -> CTA. Facts come from the previous security page; per founder
direction the page names the certifications held and makes no claim either way about SOC 2.
Run from the repo root: python tools/v4-build/build_security.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K

MAIL = 'gaurav@upcoretechnologies.com'
PACK = (f'mailto:{MAIL}?subject=Security%20Review%20Pack%20Request&amp;body=Please%20send%20the%20Upcore%20Security%20Review%20Pack'
        '%20(ISO%2027001%2C%20CMMI%2C%20subprocessor%20list%2C%20security%20questionnaire).')


def pack_link(section, cls='link', label='Request the Security Review Pack'):
    return (f'<a class="{cls}" href="{PACK}" data-gtm-cta="request-security-pack" data-gtm-cta-type="secondary" '
            f'data-gtm-cta-section="{section}">{label}</a>')


# ------------------------------------------------------------------ 1. hero: where your code and data go
MODES = [('std', 'Standard'), ('eu', 'EU personal data'), ('prem', 'On-premise model')]


def alt(std, eu, prem):
    return f'data-std="{std}" data-eu="{eu}" data-prem="{prem}"'


ENV_I = K.svg_icon('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 14h3"/>')
POD_I = K.svg_icon('<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.8-3.2 3.2-5 6-5s5.2 1.8 6 5"/><path d="M16 4.6a3.2 3.2 0 0 1 0 6.4M18.5 14c1.5.8 2.4 2.4 2.8 5"/>')
MOD_I = K.svg_icon('<path d="M12 3 4 7.5v9L12 21l8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>')
tabs = ''.join(f'<button type="button" role="tab" class="dp-tab{" is-on" if i == 0 else ""}" data-mode="{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{l}</button>' for i, (k, l) in enumerate(MODES))
L1 = ('OAuth access, scoped to the branches in your SOW',) * 3
L2 = ('Prompts sent to an enterprise model API', 'Routed to an EU-region endpoint', 'Stays inside your network')
M_T = ('Model provider', 'Model provider, EU region', 'Open-weight model, in your infrastructure')
M_D = ('Covered by a data processing agreement, with no training on your data. Named in your SOW before you sign.',
       'EU-region endpoints are the default for EU clients. Transfers to our India team run under Standard Contractual Clauses.',
       'For air-gapped requirements: nothing goes to an external API. Adds about two weeks to the first deployment.')
M_G = ('No training', 'EU region', 'Inside your walls')
DPATH = f'''<figure class="dp" data-dpath>
<div class="dp-win">
<div class="gate-top"><span class="gate-dots"><i></i><i></i><i></i></span><span>Where your code and data go</span><span class="gate-pr">Data path</span></div>
<div class="dp-tabs" role="tablist" aria-label="Choose a setup">{tabs}</div>
<ol class="dp-path" aria-live="polite">
<li class="dp-n dp-env"><span class="dp-i">{ENV_I}</span><span class="dp-c"><b>Your environment</b><span>Repositories, CI/CD and business systems. Builds run here.</span></span><em class="dp-g">Stays yours</em></li>
<li class="dp-l"><i aria-hidden="true"></i><span {alt(*L1)}>{L1[0]}</span></li>
<li class="dp-n dp-pod"><span class="dp-i">{POD_I}</span><span class="dp-c"><b>Your Upcore team</b><span>Named people only. Access is revoked at the end of the engagement, or whenever you ask.</span></span><em class="dp-g">Named</em></li>
<li class="dp-l dp-l--m"><i aria-hidden="true"></i><span {alt(*L2)}>{L2[0]}</span></li>
<li class="dp-n dp-mod"><span class="dp-i">{MOD_I}</span><span class="dp-c"><b {alt(*M_T)}>{M_T[0]}</b><span {alt(*M_D)}>{M_D[0]}</span></span><em class="dp-g" {alt(*M_G)}>{M_G[0]}</em></li>
</ol>
<dl class="dp-facts"><div><dt>Code copied to Upcore servers</dt><dd>No</dd></div><div><dt>Training on your data</dt><dd>No</dd></div><div><dt>Provider named</dt><dd>Before you sign</dd></div></dl>
</div>
<figcaption>Choose a setup to see how the path changes</figcaption>
</figure>'''

hero = K.hero_split([(C.URL['home'], 'Home'), (None, 'Security')], 'Security &amp; trust',
                    'The questions your CISO will ask, <span class="hl">answered before you sign.</span>',
                    'How Upcore handles your code and data, which AI providers process it, and the contracts available before any engagement starts. Our information security management is certified to ISO 27001:2022.',
                    C.btn('hero', pulse=True) + pack_link('hero'), DPATH, micro='Security questions? We respond within 24 hours')

# ------------------------------------------------------------------ 2. six short answers + certifications
QA = [('Yes', 'Is Upcore ISO 27001 certified?', 'Yes. Upcore Technologies Pvt. Ltd. holds ISO 27001:2022 certification at organization level, covering information security management across all delivery functions.'),
      ('Only with your permission', 'Does our code leave our environment?', 'Work happens in your repositories through OAuth-scoped access. No code is copied to Upcore servers, and snippets shared for analysis are not kept after the session.'),
      ('Named in your contract', 'Which AI providers process our data?', 'They are named in your Statement of Work and Data Processing Agreement before the engagement starts. We use enterprise-tier API agreements, and no provider we use trains on customer data.'),
      ('Yes', 'Can you sign a Business Associate Agreement?', 'Yes, for any engagement where protected health information may be in scope. Raise it on the discovery call and it is added to your contract package.'),
      ('Yes', 'Can we use our own model, on-premise or in a private cloud?', 'Yes. For air-gapped requirements we deploy open-weight models on your infrastructure. It adds about two weeks to the initial deployment.'),
      ('On request', 'What is your compliance and audit posture?', f'We hold ISO 27001, ISO 9001 and a CMMI Level 3 appraisal. Scope, data handling and subprocessors are covered in a Security Review Pack, available on request during procurement from <a class="link" href="mailto:{MAIL}">{MAIL}</a>. Our governance work also produces the AI evidence clients need for their own SOC 2, HIPAA and EU AI Act audits.')]
qa = ''.join(f'<details class="sc-q" data-reveal style="--d:{i % 3}"><summary><span class="sc-st">{s}</span><span class="sc-qt">{q}</span><span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for i, (s, q, a) in enumerate(QA))
CERTS = [('/images/accolades/light/iso27001.svg', 26, 'ISO 27001:2022', 'Information security management, covering client data handling, access control and incident response.', 'Certified, active'),
         ('/images/accolades/light/iso9001.svg', 26, 'ISO 9001:2015', 'Quality management: planning, monitoring and continual improvement across client delivery.', 'Certified, active'),
         ('/images/accolades/light/cmmi.svg', 46, 'CMMI Level 3', 'Delivery processes are documented, standardized and applied the same way on every engagement.', 'Appraised, active')]
certs = ''.join(f'<li data-reveal style="--d:{i}"><img src="{src}" alt="" width="{w}" height="26" /><b>{n}</b><p>{d}</p><span class="sc-ok">{st}</span></li>' for i, (src, w, n, d, st) in enumerate(CERTS))
answers = f'''<section class="h-sec" id="answers" aria-labelledby="qa-h"><div class="wrap">
{K.head("Quick reference", "Six questions from every CISO.", "qa-h", "Short answers first. Open any question for the detail.")}
<div class="faq sc-qa">{qa}</div>
<div class="sc-certs-wrap"><p class="h-col">Certifications &middot; certificates are shared with enterprise clients during procurement</p><ul class="sc-certs">{certs}</ul></div>
</div></section>'''

# ------------------------------------------------------------------ 3. how code and data are handled
HANDLE = [('<path d="M4 7h16v12H4z"/><path d="M8 7V5h8v2"/><path d="m9 13 2 2 4-4"/>', 'Repository access', 'OAuth with the minimum permissions: read access to the branches in your SOW. Write access only if you opt in to automated pull-request comments. Revoked at the end of the engagement or whenever you ask.'),
          ('<path d="M6 3h9l3 3v15H6z"/><path d="M9 12h6M9 16h4"/>', 'Code retention', 'No code is copied to Upcore systems. Snippets shared for AI-assisted review are processed in context and not stored after the session. Audit-log entries are kept for the engagement and handed to you when it ends.'),
          ('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>', 'Data residency', 'Analysis uses the model provider&rsquo;s regional endpoint nearest your data. EU clients get EU-region endpoints by default; US-only residency is configured at onboarding. The specifics are written into your DPA.'),
          ('<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>', 'Access controls', 'Only the named people on your engagement can reach your environment, unless you approve someone else. Credentials are held in an ISO 27001-compliant credential management system.'),
          ('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>', 'Subprocessors', 'The full list, including model providers, credential management and communication tools, is in your DPA. New subprocessors come with 30 days&rsquo; notice and the right to object.'),
          ('<path d="M12 3 2.5 20h19z"/><path d="M12 10v4M12 17.5v.01"/>', 'Incident notification', 'If a security incident affects your data, we notify you within 72 hours of becoming aware, in line with ISO 27001 incident management and GDPR Article 33.')]
hitems = ''.join(f'<li data-reveal style="--d:{i % 2}">{K.svg_icon(ic, "1.5")}<b>{t}</b><p>{d}</p></li>' for i, (ic, t, d) in enumerate(HANDLE))
handling = f'''<section class="h-sec h-sec--alt" id="data" aria-labelledby="data-h"><div class="wrap h-security">
<div>{K.eyebrow("Data handling")}<h2 id="data-h" class="h-h2 h-h2--sm" data-reveal>How your code and data are handled.</h2>
<p class="sc-side" data-reveal style="--d:1">The specifics your procurement team will ask for. Need it as a formal document? Ask for our Data Processing Appendix.</p></div>
<ul class="h-sec-list">{hitems}</ul></div></section>'''

# ------------------------------------------------------------------ 4. AI in our delivery
CTL = [('Model providers train on your data', 'No'), ('Data processing agreement', 'Yes, with every MSA'), ('Provider named in your SOW', 'Yes, before you sign'),
       ('On-premise model option', 'Available'), ('Code sent to Upcore servers', 'No'), ('EU-region endpoints for EU clients', 'Default'), ('Prompt audit logging', 'Included')]
ctl = ''.join(f'<div class="sc-row" data-reveal style="--d:{i % 3}"><dt>{k}</dt><dd class="{"is-no" if v == "No" else ""}">{v}</dd></div>' for i, (k, v) in enumerate(CTL))
ai = f'''<section class="h-sec" id="ai" aria-labelledby="ai-h"><div class="wrap ab-split">
<div>{K.eyebrow("AI in our delivery")}<h2 id="ai-h" class="h-h2 h-h2--sm" data-reveal>Which AI touches your code, and on what terms.</h2>
<p class="sc-side" data-reveal style="--d:1">We use enterprise-tier model APIs for assisted work, the same way your engineers use Copilot or Cursor, but under documented access controls and data processing agreements. Clients who cannot send code to any external API can run open-weight models on their own infrastructure.</p></div>
<dl class="sc-ctl">{ctl}</dl></div></section>'''

# ------------------------------------------------------------------ 5. frameworks (reuses the stage explorer)
FW = [('EU AI Act', 'High-risk classification and documentation', 'We map your AI systems to the Act&rsquo;s high-risk categories, produce the conformity documentation and keep an AI system register aligned to Annex III. General obligations apply from 2 August 2026; high-risk obligations are due 2 December 2027.'),
      ('HIPAA', 'AI-written code near protected health information', 'Reviews make sure AI-written code doesn&rsquo;t open access-control or encryption gaps under &sect;164.312 in systems that touch PHI. A Business Associate Agreement is available.'),
      ('SOX', 'Audit trails for AI in financial systems', 'For public companies, our governance work produces the AI code audit trail your external auditors need under PCAOB AS 2201, so gaps are closed before the audit cycle.'),
      ('GDPR', 'AI processing and data flows', 'AI-written code that processes personal data is reviewed for DPIA triggers, data minimization and purpose limitation. EU client data is processed under Standard Contractual Clauses.'),
      ('ISO 42001', 'AI management systems', 'We align your AI governance with the international standard for AI management systems, useful if you are preparing for formal certification.'),
      ('OWASP LLM Top 10', 'Code-level controls', 'AI code reviews check against the OWASP Top 10 for LLM applications, including prompt injection, insecure output handling and supply-chain risks, with controls recorded per pull request.')]
fw_tabs = ''.join(
    f'<button type="button" class="stx-tab{" is-on" if i == 0 else ""}" role="tab" id="fw-t{i}" aria-controls="fw-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
    f'<span class="stx-n">{i + 1:02d}</span><span class="stx-name">{n}</span><span class="stx-who"></span></button>' for i, (n, s, d) in enumerate(FW))
fw_panels = ''.join(
    f'<div class="stx-panel{" is-on" if i == 0 else ""}" role="tabpanel" id="fw-p{i}" aria-labelledby="fw-t{i}"{"" if i == 0 else " hidden"}>'
    f'<span class="stx-k">{n}</span><h3 class="stx-h">{s}</h3><p class="stx-d">{d}</p></div>' for i, (n, s, d) in enumerate(FW))
frameworks = f'''<section class="h-sec h-sec--alt" id="frameworks" aria-labelledby="fw-h"><div class="wrap">
{K.head("Compliance support", "Audit evidence, produced as the work happens.", "fw-h", "We don&rsquo;t give legal or audit opinions. Our governance work generates the records and audit trail that show adherence to these frameworks.")}
<div class="stx stx--short" data-stages data-reveal><div class="stx-tabs" role="tablist" aria-label="Frameworks">{fw_tabs}<span class="stx-rail" aria-hidden="true"><i></i></span></div>
<div class="stx-stage">{fw_panels}</div></div>
</div></section>'''

# ------------------------------------------------------------------ 6. documents before you sign
DOCS = [('Master Services Agreement', 'Liability, indemnification, IP ownership, confidentiality and termination rights. Your legal team can redline it.', 'Standard contract'),
        ('Data Processing Agreement', 'Every data flow between your environment and ours: subprocessors, retention, deletion and breach notification. Required for every engagement.', 'Included with the MSA'),
        ('Business Associate Agreement', 'Our obligations as a Business Associate under HIPAA, with the safeguards your compliance team requires.', 'On request, healthcare'),
        ('Mutual NDA', 'Covers your code and business information, and our methods. Signed before any call where sensitive details are shared.', 'Before the discovery call'),
        ('Standard Contractual Clauses', 'The EU-approved mechanism for transferring personal data to our India-based team.', 'Standard for EU clients'),
        ('Security Review Pack', 'ISO 27001 certificate, CMMI attestation, subprocessor list and security questionnaire responses.', 'On request, under NDA')]
DOC_I = K.svg_icon('<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>', '1.5')
docs = ''.join(f'<li data-reveal style="--d:{i % 3}"><span class="sc-doc-i">{DOC_I}</span><span class="sc-doc-c"><b>{n}</b><span>{d}</span></span><em>{s}</em></li>' for i, (n, d, s) in enumerate(DOCS))
contracts = f'''<section class="h-sec" id="contracts" aria-labelledby="doc-h"><div class="wrap">
{K.head("Contracts &amp; protections", "Everything your legal team needs, before you sign.", "doc-h", "Every document is shared at the discovery-call stage, before any engagement starts.")}
<ul class="sc-docs">{docs}</ul>
<p class="sc-pack" data-reveal>{pack_link("contracts")}</p>
</div></section>'''

# ------------------------------------------------------------------ 7. entity and jurisdiction
JUR = [('GDPR: India is not an EU adequacy country. How does data transfer work?', 'EU personal data transferred to Upcore is governed by Standard Contractual Clauses, the European Commission&rsquo;s approved mechanism for transfers to non-adequacy countries. Our DPA, included with every MSA, specifies the SCC module, subprocessor list and breach-notification timeline. No EU personal data is processed outside the executed SCCs.'),
       ('HIPAA: can an Indian private limited company sign a Business Associate Agreement?', 'Yes. HIPAA&rsquo;s Business Associate requirements depend on the data handled, not where the vendor is incorporated. If PHI may be in scope, we execute a BAA that meets the 45 CFR &sect;164.308&ndash;314 safeguard requirements, reviewed by your compliance team before any engagement starts.'),
       ('SOX: how does an Indian vendor fit into a SOX-scoped audit chain?', 'SOX Section 404 requires controls over financial reporting to be documented and tested, including third-party vendors with access to financial data or systems. Upcore is treated as a third-party vendor under your vendor-management controls, and our governance work delivers documentation (control inventories, change logs and risk assessments) your internal audit team can present to your external auditor.'),
       ('EU AI Act: does the Act apply to an Indian provider serving EU clients?', 'Yes. Under the Act&rsquo;s extraterritorial scope (Article 2), providers placing AI systems on the EU market, or whose outputs are used in the EU, are covered wherever they are established. Our governance work includes EU AI Act mapping: risk classification, transparency obligations and conformity documentation.')]
jur = K.faq(JUR, 'Procurement questions about working with an Indian company.', eb='Entity &amp; jurisdiction')

final = K.final('Bring your security questionnaire <span class="hl">to the first call.</span>',
                'Book a 45-minute discovery call and we&rsquo;ll answer your CISO&rsquo;s questions before you commit to anything. Or request the Security Review Pack first.',
                f'Security questions? Email <a href="mailto:{MAIL}">{MAIL}</a>. We respond within 24 hours.')

page = '\n'.join([hero, answers, handling, ai, frameworks, contracts, jur, final])
ld = C.graph('security', [{'@type': 'WebPage', 'name': 'Security & Trust Center', 'url': C.SITE + C.FINAL_URL['security'], 'about': {'@id': C.ORG_ID}},
                          K.faq_ld([(q, a) for s, q, a in QA] + JUR)], crumb='Security')
print('security', C.write('security.html', 'security', 'Security &amp; Trust: Data Handling and Certifications | Upcore',
      'How Upcore handles your code and data, which AI providers process it, our ISO 27001 and CMMI Level 3 certifications, and the contracts available before you sign.',
      page, active='security', ld=ld, group='company', spine=False, main_cls='is-calm'))
