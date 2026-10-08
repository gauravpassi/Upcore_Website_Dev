# Copy for the four "Who we help" segment pages (post-audit, US English).
# Rules: only Upcore results from the live site / pre-read; industry stats carry a source URL; no prices.
# Client names shown with Gaurav's approval (2026-10-07); the residential developer stays unnamed.

P_RETAIL = ('60%+', 'National food &amp; fashion retailer<br />900+ stores &middot; South Africa', 'Delivery-support tickets cut by more than 60% with a WhatsApp order-status agent, with 10,000+ queries automated every month.')
P_RE = ('~3 wks', 'Residential developer<br />India', 'Agents run bank and buyer document follow-ups on the client&rsquo;s own SOPs. Time to the first installment fell from 6&ndash;10 weeks to about 3.')
P_COMPLIANCE = ('&asymp;$210K/yr', 'Automotive compliance services firm<br />India', 'A compliance-check agent runs every check inside the team&rsquo;s own workflow, replacing roughly $210K (&#8377;2 crore) a year of licensed tooling.')
P_WEALTH = ('~800', 'FCA-regulated wealth management firm<br />United Kingdom', 'Client, portfolio and compliance data unified into one 360&deg; view, with financial operations automated for around 800 clients under FCA-appropriate controls.')
P_DENTAL = ('10', 'Dental implant network<br />9 states &middot; United States', 'Ten scheduling, intake and admin workflows automated across the network, plus a voice tool that turns clinicians&rsquo; dictation into notes and prescriptions. The client then hired us again.')
P_DENTAL_ENG = ('Rehired', 'Dental implant network<br />9 states &middot; United States', 'Hired us twice: first for ten automated operational workflows and a clinician voice tool, then to add test and DevOps agents to their software release pipeline.')
P_SAAS = ('In production', 'Field-service SaaS company<br />South Africa', 'The client belongs to a ServiceNow Elite partner group. Our delivery agents for requirements, user stories and developer onboarding are built into the team&rsquo;s product workflow.')
P_APP = ('4.9&#9733;', 'Booking &amp; payments app for barbers<br />United Kingdom', 'Built with AI-assisted engineering practices and live on both stores: 4.9&#9733; on the App Store (89 ratings), 4.5&#9733; on Google Play (5,000+ downloads).')
P_BRIEF = ('70% faster', 'Creator-marketing SaaS<br />Australia', 'A briefing agent turns scattered client material into structured, publishable campaign briefs. Brief creation became 70% faster.')

PATH_STD = [
    ('Discovery call', '45 minutes on your highest-volume workflows. You get a written plan: what to automate first, in what order, and what it should return.'),
    ('Pilot on one workflow', 'We build and run one agent on your own accounts, against real cases, with your people approving its output. You see the numbers before committing further. Duration and commercials are agreed on the discovery call.'),
    ('Scale and tune', 'Proven agents roll out to more teams and workflows on a monthly retainer, tuned as your volumes, rules and systems change.'),
]
FAQ_DATA = ('How is our data protected?', 'Agents run with scoped, revocable permissions, every action is logged and changes to records can be rolled back. Where your policies require it, we deploy into your own cloud, and model providers are configured so your data is not used to train their models. Our security management is certified to ISO 27001.')
FAQ_COST = ('What does it cost?', 'We don&rsquo;t publish a price list for this work. It depends on the workflows, volumes and systems involved. Pilot duration and commercials are agreed on the discovery call, based on your scope and requirements, and you get a written proposal with a fixed scope and price before any build starts.')
FAQ_SPEED = ('How fast can we see results?', 'Our standard is a first agent live within 30 days of design sign-off. Further agents reuse the same connections, so each one is faster than the last.')

COPY = {
# ------------------------------------------------------------------ ECOMMERCE
'ecommerce-retail': dict(
    tools=['shopify', 'woocommerce', 'magento', 'zendesk', 'whatsapp', 'gmail', 'googleads', 'meta', 'slack', 'salesforce', 'hubspot'],
    fw=('effort', 'Upcore framework &middot; Consumer behavior', 'Less effort for customers means <span class="ul-draw">fewer tickets for you.</span>', 'Customers judge you on how easy it is to get a simple answer. We design every retail agent to remove steps, not just to reply faster.'),
    title='AI Agents for Ecommerce &amp; Retail Operations | Upcore',
    meta='AI agents that answer order and delivery questions on WhatsApp, email and chat, take returns and audit ad spend, connected to your store and carriers.',
    eyebrow='For ecommerce and customer-service leaders',
    h1='Stop answering <span class="hl">&ldquo;where is my order?&rdquo;</span> by hand.',
    lead='Upcore builds AI agents for ecommerce and retail brands that answer order and delivery questions, take returns and damage claims, keep product pages accurate and audit ad spend, connected to your store, ERP, carriers and helpdesk. Your team handles the exceptions.',
    chips=['60%+ fewer tickets at one retailer', 'WhatsApp, email &amp; chat', 'Shopify, ERP &amp; 3PL'],
    flow=dict(title='Order-status agent', aria='Example: an agent reads a customer message, finds the order, checks the carrier, applies your policy and replies, with refunds going to a person.',
              steps=[('Message received', 'WhatsApp', False), ('Order found', 'store / ERP', False), ('Carrier checked', 'tracking', False), ('Policy applied', 'your rules', False), ('Refund? To a person', 'approval', True), ('Reply sent &amp; logged', 'audit trail', False)],
              out=('Resolved', 'answered from live data, with the exception routed to your team')),
    pain=('Where margin leaks', 'Support queues and returns <span class="ul-draw">eat the margin.</span>', 'Especially for home goods, furniture and other bulky or made-to-order products, and for any brand where &ldquo;where is my order?&rdquo; dominates the queue.'),
    stats=[
        ('32', 'support tickets per 100 orders for Home &amp; Garden brands, against a 25 median across verticals', 'Gorgias Ecom Lab via Macha', 'https://www.getmacha.com/blog/support-tickets-per-order-by-ecommerce-vertical'),
        ('22.7%', 'online return rate for furniture, against 19.3% across all categories', 'NRF &amp; Happy Returns via eightx', 'https://eightx.co/blog/average-furniture-and-home-return-rate-benchmarks'),
        ('$55&ndash;108', 'cost to process one large-item return, often 50&ndash;100% of its gross margin', 'Optoro via eightx', 'https://eightx.co/blog/average-furniture-and-home-return-rate-benchmarks'),
        ('$1,127', 'average Google Ads spend wasted per account per month', 'WordStream via PPC Land', 'https://ppc.land/most-google-ads-accounts-waste-1-127-a-month-study-of-15k-accounts-finds/'),
    ],
    wf_h2='Five workflows, <span class="ul-draw">starting where the volume is.</span>',
    wf_lead='We start with the work that is high-volume and rules-based, where every hour saved shows up in your support costs or your margin.',
    workflows=[
        ('Order and delivery status', 'Answers &ldquo;where is my order?&rdquo; on WhatsApp, email and chat from live store, ERP and carrier data, including made-to-order production status and white-glove delivery windows.', 'Fewer tickets, faster replies at peak'),
        ('Returns and damage claims', 'Collects photos and order details, checks your returns policy, books collections and routes refunds above your threshold to a person.', 'Claims logged in minutes, not days'),
        ('Catalog and product-page accuracy', 'Checks every product page for missing dimensions, materials, care details and inconsistent specs, and drafts fixes for approval.', 'Fewer &ldquo;not as described&rdquo; returns'),
        ('Ad spend audits', 'Watches Google and Meta accounts daily for wasted search terms, budget pacing problems and falling ROAS, with plain-English alerts.', 'Spend moved to what converts'),
        ('Customer sentiment', 'Reads reviews, tickets and chats to flag product, delivery and service issues before they become a pattern.', 'Problems caught early'),
    ],
    ba_h2='What changes in a peak week.',
    ba=[
        ('Order status', 'Support staff copy tracking numbers from three systems into replies, and queues double in peak season.', 'Routine status questions are answered instantly from live data. Your team handles only real exceptions.'),
        ('Returns', 'Claims arrive as emails with missing photos, and each one takes several back-and-forths.', 'Every claim arrives complete, policy-checked and ready for a one-click decision.'),
        ('Product data', 'Missing dimensions and mismatched materials are found when a customer returns the item.', 'Gaps and inconsistencies are flagged and fixed before the product goes live.'),
        ('Ad spend', 'Wasted spend is found at the monthly review, after it has gone.', 'Problems are flagged the same day, with the fix suggested.'),
    ],
    proof_h2='Already live <span class="hl">in production.</span>', proof_lead='From retail and adjacent content work, measured in the client&rsquo;s own terms.',
    proof=[P_RETAIL, P_BRIEF],
    quotes='ops',
    path_h2='Start with one workflow. <span class="ul-draw">Scale what works.</span>', path_lead='Order status is the natural first workflow: high volume, clear rules and results you can measure in weeks.',
    path=PATH_STD,
    faq_h2='Questions <span class="ul-draw">retail teams ask.</span>',
    faq=[
        ('Do we have to replace our helpdesk?', 'No. Agents work alongside Gorgias, Zendesk, Freshdesk or your own inbox, and connect to Shopify, WooCommerce, Magento, your ERP and your carriers through their APIs. We confirm exactly what connects on the discovery call.'),
        ('Can it handle bulky, made-to-order or white-glove delivery?', 'Yes, and that is where off-the-shelf tracking tools fall short. We connect to your production schedule, 3PL and delivery partners, so customers get real answers about build and delivery dates, not just a parcel tracking link.'),
        ('Will customers know they are talking to an agent?', 'We recommend telling them, and some jurisdictions require it. The agent keeps your brand voice, and anything sensitive, such as refunds, complaints or high-value orders, goes to a person with the full context attached.'),
        ('Can we go live before peak season?', 'Usually, if we start now. Our standard is a first agent live within 30 days of design sign-off. We run it on a share of conversations first, tune it to your policies and tone, then scale it up before the peak arrives.'),
        FAQ_DATA, FAQ_COST,
    ],
    cta_h2='Be ready <span class="hl">before your next peak.</span>',
    cta_p='Book a 45-minute discovery call. We&rsquo;ll look at your ticket mix, returns and ad accounts, and send you a written plan for the first agents to build.',
),
# ------------------------------------------------------------------ OPERATIONS-HEAVY
'operations-heavy': dict(
    tools=['salesforce', 'hubspot', 'zoho', 'microsoft', 'microsoftteams', 'microsoftoutlook', 'gmail', 'whatsapp', 'slack', 'powerautomate', 'n8n'],
    fw=('compress', 'Upcore framework &middot; Operations research', 'The weeks are in the waiting, <span class="ul-draw">not the work.</span>', 'Most operational lead time is spent waiting on replies, documents and approvals. Agents remove the waiting; your people keep the decisions.'),
    title='AI Automation for Operations-Heavy Businesses | Upcore',
    meta='AI agents for mid-market firms that run on follow-ups: collections, document chasing, lead response and status updates, with people approving what matters.',
    eyebrow='For COOs of 100&ndash;1,000-person companies',
    h1='Your operations, <span class="hl">minus the chasing.</span>',
    lead='Where growth means more follow-ups, more documents and more status calls. Upcore deploys AI agents that do the chasing inside the systems you already run, so your team handles decisions instead of reminders.',
    chips=['Your CRM, ERP, email &amp; WhatsApp', 'Human approval built in', 'First agent live in 30 days, as standard'],
    flow=dict(title='Collections follow-up agent', aria='Example: an agent tracks a buyer payment milestone, chases documents from the buyer and bank, escalates exceptions and updates the CRM.',
              steps=[('Milestone due', 'CRM / ERP', False), ('Documents requested', 'buyer &amp; bank', False), ('Reminders sent', 'email &amp; WhatsApp', False), ('Documents checked', 'your SOP', False), ('Exception? To a person', 'approval', True), ('Payment tracked', 'CRM updated', False)],
              out=('~3 wks', 'to first installment for one developer, down from 6&ndash;10 weeks')),
    stats=None,
    wf_h2='The work that grows <span class="ul-draw">faster than headcount.</span>',
    wf_lead='Every operations team carries the same hidden load: chasing people, documents and payments, and telling everyone where things stand. That is exactly what agents are good at.',
    workflows=[
        ('Collections and payment follow-ups', 'Tracks every milestone and invoice, chases customers, banks and partners on your schedule, and escalates only the exceptions.', 'Cash in sooner'),
        ('Document collection and checks', 'Requests, chases, reads and checks documents against your SOPs, and files them in the right place.', 'Complete files without the back-and-forth'),
        ('Lead response and qualification', 'Answers every inquiry within minutes, qualifies it against your criteria and books the next step with the right person.', 'Every inquiry answered fast'),
        ('Customer and partner updates', 'Sends proactive status updates at every milestone and answers &ldquo;where are we?&rdquo; questions from live data.', 'Fewer status calls'),
        ('Scheduling and intake', 'Books, reschedules and confirms appointments, collects intake details and keeps calendars in sync across locations.', 'Fuller schedules, less admin'),
        ('Reporting and compliance packs', 'Pulls data from your systems into weekly operations reports and regulator-ready compliance packs.', 'Weekly reports assembled automatically'),
    ],
    ba_h2='What changes for your operations team.',
    ba=[
        ('Follow-ups', 'Coordinators keep spreadsheets of who owes what, and chase by phone when they find time.', 'Every follow-up runs on schedule. Coordinators see a live board and step in only when something is stuck.'),
        ('Documents', 'Files arrive incomplete, and someone checks each one by hand against the checklist.', 'Documents are chased until complete and checked against your SOP before anyone opens them.'),
        ('Status updates', 'Managers answer the same &ldquo;where are we?&rdquo; question all day.', 'Customers and partners get proactive updates from live data.'),
        ('Reporting', 'Someone spends Friday pulling numbers from four systems into a deck.', 'The weekly operations report is ready on Monday morning.'),
    ],
    proof_h2='Already running <span class="hl">on agents.</span>', proof_lead='From real estate, healthcare and compliance services.',
    proof=[P_RE, P_DENTAL, P_COMPLIANCE],
    quotes='ops',
    path_h2='Start with one workflow. <span class="ul-draw">Scale what works.</span>', path_lead='We pick the workflow with the most volume and the clearest rules, so the first result shows up quickly.',
    path=PATH_STD,
    faq_h2='Questions <span class="ul-draw">COOs ask.</span>',
    faq=[
        ('Which systems do you work with?', 'We build on what you already run: CRMs such as Salesforce, HubSpot and Zoho; ERPs; email; WhatsApp; shared drives and industry systems. Agents connect through APIs where they exist and through email and documents where they don&rsquo;t.'),
        ('Does the AI make decisions on its own?', 'Only within the limits you set. Agents handle the repetitive work; anything above your thresholds, such as write-offs, exceptions or customer disputes, goes to a named person. Every action is logged.'),
        ('We are not a tech company. Who runs this after go-live?', 'We do, with your team. A monthly retainer covers monitoring, tuning and new workflows, and your team is trained to understand and own what has been built.'),
        ('Which industries is this for?', 'Any business where growth means more follow-ups and documents. Our live work includes a residential developer, a multi-location dental network and a compliance services firm. Staffing or consulting firm? See Professional Services.'),
        FAQ_DATA, FAQ_SPEED, FAQ_COST,
    ],
    cta_h2='Find the three processes <span class="hl">worth automating first.</span>',
    cta_p='Book a 45-minute discovery call. We&rsquo;ll map your highest-volume workflows and send you a written plan: what to automate, in what order, and what it should return.',
),
# ------------------------------------------------------------------ PROFESSIONAL SERVICES
'professional-services': dict(
    tools=['microsoft', 'microsoftoutlook', 'microsoftteams', 'gmail', 'salesforce', 'hubspot', 'zoho', 'whatsapp', 'powerautomate', 'notion'],
    fw=('ladder', 'Upcore framework &middot; Behavioral science', 'Autonomy is earned, <span class="ul-draw">one level at a time.</span>', 'Professional firms cannot afford an agent that guesses. Every agent starts by drafting for your people to approve, and earns more autonomy only on measured evidence.'),
    controls=True,
    title='AI Agents for Accounting, Law, Wealth &amp; Staffing | Upcore',
    meta='AI agents for accounting, law, wealth and staffing firms: client intake, document chasing, review prep, deadlines and billing, approved by professionals.',
    eyebrow='For managing partners and practice leads',
    h1='More time with clients. <span class="hl">Less admin.</span>',
    lead='Upcore builds AI agents for accounting firms, law firms, wealth managers, and staffing and consulting firms. They take on intake, document chasing, review prep, deadlines and billing admin, so your professionals spend their time on clients.',
    chips=[('Accounting', 'acc'), ('Law', 'law'), ('Wealth &amp; advice', 'wealth'), ('Staffing &amp; consulting', 'staff')],
    flow=dict(title='Client document agent', aria='Example: an agent builds a client checklist, requests documents, chases until complete, files them and flags exceptions for a professional.',
              steps=[('Checklist built', 'per client', False), ('Request sent', 'portal &amp; email', False), ('Reminders', 'until complete', False), ('Documents filed', 'right folder', False), ('Exceptions reviewed', 'professional', True), ('Ready for work', 'summary sent', False)],
              out=('Complete', 'client files, without anyone writing a reminder')),
    pain=('Where the hours go', 'Admin is eating <span class="ul-draw">your client time.</span>', 'Firms that automate the admin around their experts win on capacity and client experience.'),
    stats=[
        ('33%', 'of a UK financial adviser&rsquo;s day is spent with clients; 51% is seen as ideal', 'Fidelity IFA DNA via IFA Magazine', 'https://ifamagazine.com/fidelity-research-shows-advisers-only-spend-one-third-of-their-day-with-clients-and-ai-could-unlock-the-ideal-workday/'),
        ('38%', 'of an adviser&rsquo;s day goes to reports, compliance and admin', 'Fidelity IFA DNA via IFA Magazine', 'https://ifamagazine.com/fidelity-research-shows-advisers-only-spend-one-third-of-their-day-with-clients-and-ai-could-unlock-the-ideal-workday/'),
        ('9% &rarr; 41%', 'accounting firms using AI, 2024 to 2025: competitors are moving', 'Wolters Kluwer via CPA Practice Advisor', 'https://www.cpapracticeadvisor.com/2025/10/09/accounting-firms-are-choosing-transformation-over-tactics-wolters-kluwer-report-says/170677/'),
        ('83%', 'Only 83% of ongoing advice reviews were actually delivered at the largest UK firms the FCA examined', 'FCA review via Regulation Tomorrow', 'https://www.regulationtomorrow.com/2025/02/fca-publishes-findings-from-review-of-ongoing-financial-advice-services/'),
    ],
    workflows=[],
    wf_h2='Workflows built for <span class="ul-draw">how your firm works.</span>',
    wf_lead='Choose your firm type. Every agent works inside your practice, case or client-management system, and a professional approves anything that matters.',
    ba_h2='What changes in a typical week.',
    ba=[
        ('Intake', 'New inquiries wait for someone to take notes, check conflicts or verify identity.', 'Intake details, checks and a summary are ready within minutes. The professional&rsquo;s first task is a decision.'),
        ('Documents', 'Staff chase the same clients three or four times and track replies in a spreadsheet.', 'One checklist per client and automatic reminders. Staff see who is complete and who needs a call.'),
        ('Reviews and deadlines', 'Review packs and deadlines depend on someone remembering and preparing them by hand.', 'Every deadline is tracked and every review pack is drafted in advance for the professional to finalize.'),
        ('Billing', 'Time and billing narratives are reconstructed from memory at month-end.', 'Draft entries come from real activity; professionals edit and approve.'),
    ],
    proof_h2='Our closest work, <span class="hl">already live.</span>', proof_lead='We haven&rsquo;t published an accounting or law case study yet. These are our closest engagements, and first firms in each sector get a pilot built around their own workflow.',
    proof=[P_WEALTH, P_RE, P_COMPLIANCE],
    quotes='ops',
    path_h2='Prove it on <span class="ul-draw">one workflow first.</span>', path_lead='Pilots are scoped around a single high-volume workflow, such as document collection or review prep, with success measures agreed up front.',
    path=PATH_STD,
    faq_h2='Questions <span class="ul-draw">firms ask.</span>',
    faq=[
        ('Does the AI give professional advice?', 'No. Agents capture, chase, draft, check and remind. Accounting judgments, legal advice and financial recommendations stay with your qualified people, who approve anything that reaches a client, a court or a regulator.'),
        ('How do you stop AI from making things up?', 'Agents work from your documents and records, not general knowledge. Every item they flag points to its source, outputs are logged, and anything they can&rsquo;t ground in a source is raised as a question, not an answer.'),
        ('Is client confidentiality protected?', 'Agents run with scoped, revocable permissions and every action is logged. Where your policies require it, we deploy into your own cloud. See the enterprise controls above for certifications and data handling.'),
        ('Will it work with our practice-management software?', 'We build on top of what you already run, connecting through APIs where they exist and through email, portals and shared folders where they don&rsquo;t. We confirm exactly what connects on the discovery call.'),
        ('UK advice firms: can it help with FCA Consumer Duty?', 'Yes. For advice firms we can assemble the client-outcome data your board report needs from your back-office system, and prepare review packs in advance of each client review.'),
        FAQ_COST,
    ],
    cta_h2='Give your people <span class="hl">their hours back.</span>',
    cta_p='Book a 45-minute discovery call. We&rsquo;ll map the workflows costing your firm the most non-billable time and send you a written automation plan.',
),
# ------------------------------------------------------------------ TECH & SOFTWARE
'tech-software': dict(
    tools=['jira', 'linear', 'github', 'gitlab', 'githubactions', 'claude', 'githubcopilot', 'cursor', 'sonarqube', 'snyk', 'sentry', 'datadog', 'amazonwebservices', 'microsoftazure', 'googlecloud'],
    fw=('loop', 'Upcore framework &middot; Computer science', 'Every agent runs <span class="ul-draw">a closed control loop.</span>', 'The same discipline you expect from production systems: sense, reason, act, verify and learn, with an approval gate whenever confidence is low.'),
    controls=True,
    ld_name='Governed AI software delivery for tech companies', ld_type='AI software delivery and governance',
    title='AI for Software Companies: Delivery, Spend &amp; Risk | Upcore',
    meta='For CTOs and CIOs: a governed AI delivery pipeline, AI spend and risk controls, and delivery agents built into Jira or Linear, GitHub and CI/CD.',
    eyebrow='For CTOs and CIOs of 50&ndash;500-engineer companies',
    h1='Ship AI-written code <span class="hl">your architects trust.</span>',
    lead='Your engineers already use Copilot, Cursor and Claude. Upcore adds what is missing: a governed delivery process with architecture guardrails and automated gates, visibility of AI spend and risk, and delivery agents built into the tools your teams already run.',
    hero_link='See how we help',
    chips=['Jira or Linear, GitHub, CI/CD', 'Claude Certified Architect-led'],
    flow=dict(title='Governed change pipeline', aria='Example: a change moves from spec through architecture checks, an architect-approved plan, sandbox build, automated gates and a monitored release.',
              steps=[('Spec from template', 'Jira / Linear', False), ('Guardrails checked', 'ADRs &amp; schema', False), ('Plan approved', 'architect', True), ('Built &amp; tested', 'sandbox', False), ('Gates passed', 'SAST &amp; coverage', False), ('Released safely', 'feature flag', False)],
              out=('Logged', 'every deviation, why it happened and who decided')),
    stats=None,
    wf_eyebrow='What we do',
    wf_h2='Three ways we help <span class="ul-draw">engineering teams.</span>',
    wf_lead='Each stands alone. Together they make AI-assisted delivery governed and visible to leadership. <a class="link" href="__AINE__">See the full AI-Native Engineering pipeline</a>',
    workflows=[
        ('AI governance and spend visibility', 'Dashboards for AI tool and token spend by team and user, where your tools expose usage data; controls that keep personal data out of AI tools; and review of the quality of AI-written code.', 'Know what AI costs and what it changes'),
        ('AI-Native Engineering pipeline', 'A governed spec-to-production process inside Jira or Linear, GitHub and your CI/CD: architecture guardrail checks, architect plan sign-off, AI-written tests, automated pull-request gates, risk-scored merge rules and feature-flagged releases.', 'Governed delivery without more review load'),
        ('Delivery agents and engineering pods', 'Agents for requirements, user stories, developer onboarding, testing and DevOps, plus lean pods (developer, Claude Certified Architect, analyst) embedded in your delivery.', 'More shipped per engineer'),
    ],
    ink=1,
    ba_cols=('Today', 'With Upcore'),
    ba_h2='What changes for your engineering leaders.',
    ba=[
        ('Review', 'Every AI-written pull request needs a senior engineer&rsquo;s full attention.', 'Automated architecture, security and coverage gates catch issues before a person reviews; people focus on what is genuinely risky.'),
        ('Visibility', 'Nobody can say what AI tools cost per team, or what they changed.', 'Spend, gate results and deviations are on one dashboard you can take to the board.'),
        ('Releases', 'AI-generated changes ship with the same risk as hand-written ones, or more.', 'Changes go out behind feature flags, monitored for errors, latency and cost, then promoted or rolled back.'),
        ('Knowledge', 'Decisions live in pull-request comments and are forgotten.', 'Tickets, decisions and incidents are linked automatically for the next spec.'),
    ],
    proof_h2='Already live <span class="hl">in production.</span>', proof_lead='Led by a Claude Certified Architect, with a Claude-certified engineering team.',
    proof=[P_SAAS, P_APP, P_DENTAL_ENG],
    quotes='eng',
    path_h2='Start with a pilot. <span class="ul-draw">Expand on results.</span>', path_lead='No price list: the model below is scoped to your organization after the discovery call.',
    path=[
        ('Pilot on one team', 'One team, one service, a real backlog. We install the pipeline end to end and measure it against your current process. Duration and commercials are agreed on the discovery call.'),
        ('One-time implementation', 'A fixed fee, scaled to the teams and repositories in scope: pipeline, gates, templates, dashboard and training.'),
        ('Monthly retainer', 'An embedded Claude Certified Architect who maintains your architecture rules, tunes gates and reviews high-risk deviations.'),
    ],
    faq_h2='Questions <span class="ul-draw">CTOs ask.</span>',
    faq_lead='Not covered here? Ask us on the discovery call.',
    faq=[
        ('Can you show us what our AI tools cost today?', 'Yes, where your AI tools expose usage and billing data. The governance dashboard breaks down AI tool and token spend by team and user, so you can see where spend produces output and where it doesn&rsquo;t.'),
        ('How is this different from giving developers Copilot or Cursor?', 'Those tools generate code. We install the delivery process around them: spec templates, architecture guardrails, plan sign-off, automated pull-request gates, merge rules, scenario testing, controlled releases and a decision record.'),
        ('Do we have to replace our tools?', 'No. Everything runs inside Jira or Linear, GitHub, your existing CI/CD and the AI assistants you have already approved.'),
        ('Who decides when AI-written code can merge?', 'You do. You set the thresholds; only low-risk changes that conform to your architecture rules auto-merge, and everything else goes to a named approver.'),
        ('How do you handle security and IP?', 'Code stays in your repositories and builds run in your environments. Security scanning is a mandatory gate. See the enterprise controls above for certifications and data handling.'),
        FAQ_COST,
    ],
    cta_h2='Trust every AI-written change <span class="hl">you ship.</span>',
    cta_p='Book a 45-minute discovery call. We&rsquo;ll review your current delivery process and outline what a pilot on one team would look like.',
),
}

# Professional services: tabbed workflows by firm type
_TABS = [
    ('acc', 'Accounting', [('Client document collection', 'Per-client checklists, portal requests and reminders until the file is complete.', 'Files complete before busy season'), ('Bank and card reconciliation', 'Transactions categorized and matched; only mismatches reach a person, with reasons.', 'Hours of manual matching removed'), ('Deadlines and engagement letters', 'Filing and extension deadlines per client and entity; letters issued and tracked to signature.', 'Every deadline tracked and reminded')]),
    ('law', 'Law', [('Intake and conflict checks', 'Inquiries captured, parties extracted and conflict searches run before an attorney spends time on the call.', 'Faster yes or no to new matters'), ('Docketing and deadlines', 'Dates extracted from filings and orders, calendared against your rules, with escalating reminders.', 'Deadlines never depend on one person'), ('Time capture and billing', 'Draft time entries and narratives built from real email, document and calendar activity.', 'Unbilled time recovered')]),
    ('wealth', 'Wealth &amp; advice', [('Client 360 and onboarding', 'Client, portfolio and compliance data in one view; onboarding and AML documents chased until complete.', 'Proven for ~800 clients'), ('Review preparation', 'Fact-find refresh, data pulls and draft review packs ready before every client review.', 'Review packs ready before each meeting'), ('Consumer Duty reporting', 'Client-outcome data assembled from your back office for board reporting.', 'Board-ready evidence')]),
    ('staff', 'Staffing &amp; consulting', [('Candidate and employee admin', 'Onboarding documents, contracts and compliance checks chased and verified.', 'Faster starts'), ('Lead and sales operations', 'Every inquiry answered, qualified and followed up, with CRM hygiene handled automatically.', 'Pipeline kept current'), ('Timesheets and billing', 'Timesheets chased and checked, and invoices drafted from approved hours.', 'Invoices out on time')]),
]
_tablist = '<div class="tabs" role="tablist" aria-label="Firm type">' + ''.join(
    f'<button class="tab" role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>' for i, (k, n, _) in enumerate(_TABS)) + '</div>'
import flow as _FL  # noqa: E402
_panels = ''.join(
    f'<div class="tabpanel{" on" if i == 0 else ""}" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}">' + _FL.outcome_rows(ws) + '</div>'
    for i, (k, n, ws) in enumerate(_TABS))
COPY['professional-services']['wf_custom'] = _tablist + _panels

import chrome as _C  # noqa: E402
COPY['tech-software']['wf_lead'] = COPY['tech-software']['wf_lead'].replace('__AINE__', _C.URL['aine'])
