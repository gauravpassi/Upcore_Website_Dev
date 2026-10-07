"""Brief client case studies (2026-10-07), from the Upcore x Sierra Living Concepts pre-read
(September 2026, "What we've built"). Results are as reported from our engagements.
Client names are withheld by default, the site-wide rule; set SHOW_NAMES = True only once Gaurav
confirms each client may be named publicly (the pre-read names them for a prospect, not the public).
Each case: key, name, anonymous descriptor, tags, segment, number, what the number means,
challenge, what we built, result."""

SHOW_NAMES = False

CASES = [
    dict(key='retail-order-status', name='Woolworths South Africa', anon='Food &amp; fashion retailer &middot; ~960 stores &middot; South Africa',
         tags=['automation'], seg='ecommerce-retail', n='60%+', what='fewer delivery-support tickets',
         challenge='Online is one of the retailer&rsquo;s fastest-growing channels. At that scale, every order can turn into a &ldquo;where is my order?&rdquo; support question.',
         built='Alongside leading four of the retailer&rsquo;s mobile and ecommerce technology teams (2021&ndash;2023), we built a WhatsApp order-status and post-purchase agent that answers delivery questions automatically.',
         result='Delivery-support tickets fell by more than 60%, with 10,000+ customer queries automated every month.'),
    dict(key='compliance-checks', name='Global PCCS', anon='Automotive product-compliance firm &middot; India',
         tags=['automation'], seg='operations-heavy', n='&asymp;$210K', what='a year of licensed tooling replaced',
         challenge='Suppliers need an approved IMDS material data sheet before parts are accepted, so every sheet must be checked for wrong classifications, missing codes and restricted substances. The checking tools cost about &#8377;2 crore a year in licenses.',
         built='An automated quality and compliance-check agent that runs those checks inside the team&rsquo;s own workflow.',
         result='The checks now run through the agent, and the &#8377;2 crore (&asymp;$210K) annual license spend is gone.'),
    dict(key='developer-follow-ups', name='Residential developer', anon='Residential developer &middot; India',
         tags=['automation'], seg='operations-heavy', n='~3 wks', what='to the first installment, from 6&ndash;10 weeks',
         challenge='After a sale, the first installment waits on registration, the buyer&rsquo;s contribution, loan sanction and disbursement paperwork. Every hand-off between builder, buyer and bank needed chasing.',
         built='A team of agents built around the developer&rsquo;s existing SOPs, running bank and buyer follow-ups on behalf of the operations team.',
         result='Time to receive the first installment fell from 6&ndash;10 weeks to about 3.'),
    dict(key='campaign-briefs', name='Fabulate', anon='AI creator-marketing platform &middot; Australia',
         tags=['automation'], seg='ecommerce-retail', n='70% faster', what='campaign brief creation',
         challenge='Every campaign on the platform needs a brief built from scattered client material (goals, products, brand guidelines) before creators can start work.',
         built='A campaign briefing and activation agent that turns raw client material into structured, publishable briefs creators can act on.',
         result='Brief creation became 70% faster.'),
    dict(key='hospitality-agent', name='First Grand Group', anon='Luxury short-stay and property group &middot; Mauritius',
         tags=['automation', 'engineering'], seg='operations-heavy', n='24/7', what='check-in, payments and guest help desk',
         challenge='Guests from many countries and time zones expect instant answers and self check-in, while check-ins, payments and questions were handled by hand.',
         built='An end-to-end hospitality agent connected to the booking platform, WhatsApp, smart locks and payments, inside a platform we built: staff and owner portals, a staff operations app and a guest app.',
         result='The agent handles check-in and check-out (including door codes), payments, in-stay requests and help-desk conversations around the clock.'),
    dict(key='dental-network', name='Rain Dental Implant Centers', anon='Dental implant network &middot; 9 states &middot; United States',
         tags=['automation', 'engineering'], seg='operations-heavy', n='10', what='workflows automated, plus voice AI for doctors',
         challenge='Running scheduling, intake and admin the same way across clinics in nine states took heavy manual effort, and note-writing weighed on clinicians.',
         built='Ten workflows for scheduling, intake and admin with patient-sentiment tracking, and a voice tool: doctors speak instead of writing notes, speakers are separated automatically and prescriptions are generated.',
         result='Staff are freed from repetitive admin and patient sentiment is tracked. The client hired us again to add test and DevOps agents to its release pipeline.'),
    dict(key='wealth-client-view', name='Mercury Wealth Management', anon='FCA-regulated financial planner &middot; United Kingdom',
         tags=['automation'], seg='professional-services', n='~800', what='clients in one operational view',
         challenge='Client, portfolio and compliance data sat on disconnected platforms, and the FCA&rsquo;s Consumer Duty requires proof that ongoing reviews happen.',
         built='Claude agents, n8n and Microsoft Power Platform connecting CRM, client, portfolio and compliance workflows.',
         result='A single 360&deg; view of every client, with financial operations automated for around 800 clients under FCA-appropriate controls.'),
    dict(key='staffing-operations', name='Black Piano', anon='Employer-of-record and remote staffing firm &middot; UK &amp; India',
         tags=['automation'], seg='professional-services', n='100+', what='person team on automated HR and sales operations',
         challenge='The firm recruits, employs and manages talent in India for UK businesses, from CVs and interviews to payroll and HR, and growth depends on answering leads fast.',
         built='Two automation engines: one for HR operations, one for lead and sales operations.',
         result='HR, lead and sales operations now run on automated workflows.'),
    dict(key='field-service-delivery', name='WorkWide by Quintica', anon='Field-service SaaS platform, part of a ServiceNow Elite partner group &middot; South Africa',
         tags=['engineering'], seg='tech-software', n='In production', what='delivery agents inside a product team',
         challenge='Serving field teams across many industries means a steady flow of new requirements that must become clear user stories, with new developers productive quickly.',
         built='Delivery agents for requirements, user stories and developer onboarding, built into the team&rsquo;s product workflow.',
         result='Work moves from client need to development-ready stories with AI agents inside the delivery process.'),
    dict(key='booking-app', name='Barbr', anon='Booking and payments app for barbers &middot; United Kingdom',
         tags=['engineering'], seg='tech-software', n='4.9&#9733;', what='on the App Store, 89 ratings',
         challenge='Independent barbers run their chair as a business, juggling bookings, payments and marketing on their own.',
         built='The app itself, built with AI-first engineering practices: booking links, online payments, no-show protection, reviews and analytics.',
         result='Live on both stores: 4.9&#9733; on the App Store (89 ratings) and 4.5&#9733; on Google Play (5,000+ downloads).'),
]


def who(c):
    if SHOW_NAMES and c['name'] != 'Residential developer':
        return f"{c['name']} &middot; {c['anon'].split(' &middot; ')[-1]}"
    return c['anon']
