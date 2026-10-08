"""Client case studies (2026-10-07), from Upcore's client pre-read deck
(September 2026, "What we've built"). Results are as reported from our engagements; client context is
from public sources. No real client names anywhere on the site (decision 2026-10-08): `name` and `short` are
descriptors, and keys are neutral (they become #anchors on /results).
Each case: key, name, short (for the index), meta, tags, seg, n, what, challenge, built, result, viz.
viz kinds (rendered in build_results.py): bars, ring, tiles, converge, engines, flow, rating."""

SHOW_NAMES = False  # kept for callers; names are descriptors either way

CASES = [
    dict(key='retail-orders', name='National food &amp; fashion retailer', short='National retailer', meta='Food &amp; fashion retail, 900+ stores &middot; South Africa',
         tags=['automation'], seg='ecommerce-retail', n='60%+', what='fewer delivery-support tickets',
         challenge='Online is one of the retailer&rsquo;s fastest-growing channels. At that scale, every order can turn into a &ldquo;where is my order?&rdquo; support question.',
         built='Alongside leading four of their mobile and ecommerce technology teams (2021&ndash;2023), we built a WhatsApp order-status and post-purchase agent that answers delivery questions automatically.',
         result='Delivery-support tickets fell by more than 60%, with 10,000+ customer queries automated every month.',
         viz=dict(kind='bars', rows=[('Before', 'Every delivery question answered by a person', 100), ('After', '60%+ fewer tickets, 10,000+ queries a month automated', 38)])),
    dict(key='compliance-checks', name='Automotive compliance services firm', short='Compliance services firm', meta='Product compliance services for automotive suppliers &middot; India',
         tags=['automation'], seg='operations-heavy', n='&asymp;$210K', what='a year of licensed tooling replaced',
         challenge='Suppliers need an approved IMDS material data sheet before parts are accepted, so every sheet must be checked for wrong classifications, missing codes and restricted substances. The checking tools cost about &#8377;2 crore a year in licenses.',
         built='An automated quality and compliance-check agent that runs those checks inside the team&rsquo;s own workflow.',
         result='The checks now run through the agent, and the &#8377;2 crore (&asymp;$210K) annual license spend is gone.',
         viz=dict(kind='bars', rows=[('Before', '&#8377;2 crore a year on licensed checking tools', 100), ('After', 'Checks run by the agent, no license spend', 3)])),
    dict(key='residential-developer', name='Residential developer, India', short='Residential developer', meta='Homes sold under construction &middot; India',
         tags=['automation'], seg='operations-heavy', n='~3 wks', what='to the first installment, from 6&ndash;10 weeks',
         challenge='After a sale, the first installment waits on registration, the buyer&rsquo;s contribution, loan sanction and disbursement paperwork. Every hand-off between builder, buyer and bank needed chasing.',
         built='A team of agents built around the developer&rsquo;s existing SOPs, running bank and buyer follow-ups on behalf of the operations team.',
         result='Time to receive the first installment fell from 6&ndash;10 weeks to about 3.',
         viz=dict(kind='bars', rows=[('Before', '6&ndash;10 weeks to the first installment', 100), ('After', 'About 3 weeks', 37)])),
    dict(key='creator-briefs', name='Creator-marketing platform', short='Creator-marketing SaaS', meta='AI creator-marketing platform for brands and agencies &middot; Australia',
         tags=['automation'], seg='ecommerce-retail', n='70% faster', what='campaign brief creation',
         challenge='Every campaign on the platform needs a brief built from scattered client material (goals, products, brand guidelines) before creators can start work.',
         built='A campaign briefing and activation agent that turns raw client material into structured, publishable briefs creators can act on.',
         result='Brief creation became 70% faster.',
         viz=dict(kind='bars', rows=[('Before', 'Each brief assembled by hand', 100), ('After', '70% faster', 30)])),
    dict(key='hospitality', name='Luxury real estate &amp; short-stay group', short='Short-stay group', meta='Luxury real estate and short-stay rentals &middot; Mauritius',
         tags=['automation', 'engineering'], seg='operations-heavy', n='24/7', what='check-in, payments and guest help desk',
         challenge='Guests from many countries and time zones expect instant answers and self check-in, while check-ins, payments and questions were handled by hand.',
         built='An end-to-end hospitality agent connected to the booking platform, WhatsApp, smart locks and payments, inside a platform we built: staff and owner portals, a staff operations app and a guest app.',
         result='The agent handles check-in and check-out (including door codes), payments, in-stay requests and help-desk conversations around the clock.',
         viz=dict(kind='ring', items=['Check-in', 'Payments', 'In-stay requests', 'Help desk'])),
    dict(key='dental-network', name='Multi-state dental implant network', short='Dental network', meta='Oral surgery and dental implant centers &middot; 9 states, USA',
         tags=['automation', 'engineering'], seg='operations-heavy', n='10', what='workflows automated, plus voice AI for doctors',
         challenge='Running scheduling, intake and admin the same way across clinics in nine states took heavy manual effort, and note-writing weighed on clinicians.',
         built='Ten workflows for scheduling, intake and admin with patient-sentiment tracking, and a voice tool: doctors speak instead of writing notes, speakers are separated automatically and prescriptions are generated.',
         result='Staff are freed from repetitive admin and patient sentiment is tracked. They hired us again to add test and DevOps agents to their release pipeline.',
         viz=dict(kind='tiles', n=10, label='Workflows for scheduling, intake and admin', voice='Doctors dictate; notes and prescriptions are generated')),
    dict(key='wealth-firm', name='FCA-regulated wealth management firm', short='Wealth firm', meta='Chartered financial planning &middot; United Kingdom',
         tags=['automation'], seg='professional-services', n='~800', what='clients in one operational view',
         challenge='Client, portfolio and compliance data sat on disconnected platforms, and the FCA&rsquo;s Consumer Duty requires proof that ongoing reviews happen.',
         built='Claude agents, n8n and Microsoft Power Platform connecting CRM, client, portfolio and compliance workflows.',
         result='A single 360&deg; view of every client, with financial operations automated for around 800 clients under FCA-appropriate controls.',
         viz=dict(kind='converge', sources=['CRM', 'Client data', 'Portfolios', 'Compliance'], target='One client view')),
    dict(key='staffing', name='Employer-of-record staffing firm', short='Staffing firm', meta='Remote staffing for UK businesses &middot; UK &amp; India',
         tags=['automation'], seg='professional-services', n='100+', what='person team on automated HR and sales operations',
         challenge='The firm recruits, employs and manages talent in India for UK businesses, from CVs and interviews to payroll and HR, and growth depends on answering leads fast.',
         built='Two automation engines: one for HR operations, one for lead and sales operations.',
         result='HR, lead and sales operations now run on automated workflows.',
         viz=dict(kind='engines', items=['HR operations', 'Lead &amp; sales operations'])),
    dict(key='field-service-saas', name='Field-service SaaS company', short='Field-service SaaS', meta='Field-service software from a ServiceNow Elite partner group &middot; South Africa',
         tags=['engineering'], seg='tech-software', n='In production', what='delivery agents inside a product team',
         challenge='Serving field teams across many industries means a steady flow of new requirements that must become clear user stories, with new developers productive quickly.',
         built='Delivery agents for requirements, user stories and developer onboarding, built into the team&rsquo;s product workflow.',
         result='Work moves from client need to development-ready stories with AI agents inside the delivery process.',
         viz=dict(kind='flow', steps=['Client need', 'Requirements', 'User stories', 'Ready for development'], side='Developer onboarding')),
    dict(key='barber-app', name='Booking &amp; payments app for barbers', short='Barber booking app', meta='Booking, payments and growth app for independent barbers &middot; United Kingdom',
         tags=['engineering'], seg='tech-software', n='4.9&#9733;', what='on the App Store, 89 ratings',
         challenge='Independent barbers run their chair as a business, juggling bookings, payments and marketing on their own.',
         built='The app itself, built with AI-first engineering practices: booking links, online payments, no-show protection, reviews and analytics.',
         result='Live on both stores: 4.9&#9733; on the App Store (89 ratings) and 4.5&#9733; on Google Play (5,000+ downloads).',
         viz=dict(kind='rating', rows=[('App Store', 4.9, '89 ratings'), ('Google Play', 4.5, '5,000+ downloads')])),
]


def who(c):
    return c['name']
