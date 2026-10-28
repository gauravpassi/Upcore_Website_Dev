"""Further-reading lists for the service, segment and home pages (2026-10-28, SEO audit issue #3: service and
segment pages linked to no library articles). Every list lives here, so a person or the content pipeline can
extend them without touching the page builders. Rendered by calm.further_reading(key) just before each page's
final CTA, with the same markup and classes as the library's "Keep reading" block (no new CSS).

ARTICLES     one row per library page: href -> [kicker, title, desc], plain text (escaped when rendered).
             href is root-relative without .html. kicker is the /insights hub type: Guide, Comparison,
             Framework or Industry playbook. desc is one short sentence (about 110 characters, two lines).
FURTHER_READING  page key (the chrome.URL key of the page showing the block) -> hrefs, most relevant first.
             An entry may also be a full [href, kicker, title, desc] list to override the ARTICLES row.
MAX_ITEMS    only the first four links render, so insert a new article where it should appear.

Anything missing (no ARTICLES row, or an empty field) is filled from the article's own content/*.json
(kind, title tag, meta), so the pipeline can publish an article and just add its href to a page list.
A link that matches no library page is skipped with a warning when the page is built, never rendered dead.
Copy rules as for the pages: US spelling, no em dashes, no figures the article itself doesn't state."""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
MAX_ITEMS = 4
KIND_LABEL = {'guide': 'Guide', 'comparison': 'Comparison', 'framework': 'Framework', 'playbook': 'Industry playbook'}
# Library pages built in Python (build_guide.py, build_compare.py) rather than from content/*.json.
PY_PAGES = {'/learn/what-is-ai-native-engineering', '/compare/ai-native-engineering-vs-ai-coding-tools', '/compare/upcore-vs-building-in-house'}

ARTICLES = {
    # AI-native engineering
    '/learn/what-is-ai-native-engineering': ['Guide', 'What is AI-native engineering?',
        'How it differs from AI-assisted coding, the building blocks of a governed delivery process and how to start.'],
    '/compare/ai-native-engineering-vs-ai-coding-tools': ['Comparison', 'AI-native engineering vs AI coding tools',
        'What Copilot, Cursor and Claude Code do well, where they stop, and when you need a delivery process around them.'],
    '/compare/upcore-vs-building-in-house': ['Comparison', 'Build it in-house, or bring in Upcore?',
        'What building the process yourself involves, when that is the right call, and where an outside team saves time.'],
    # Governance
    '/learn/ai-data-governance': ['Guide', 'AI Data Governance: Enterprise Checklist',
        'Data residency, access controls, audit logging and incident response, plus the questions every AI vendor must answer.'],
    '/learn/hipaa-compliant-ai': ['Guide', 'HIPAA-Compliant AI Agents for Healthcare',
        'What HIPAA requires of AI architecture: where data is processed, no training on PHI, audit logs and BAAs.'],
    '/compare/ai-agents-vs-copilot-financial-services': ['Comparison', 'AI Agents vs. Copilot for Financial Services',
        'Where Copilot pilots fall short on data sovereignty and compliance, compared side by side with custom AI agents.'],
    '/insights/human-in-the-loop': ['Framework', 'Human in the Loop Is Not a Feature',
        'Where people belong in AI decisions, why full autonomy fails in complex work, and how oversight lets AI scale.'],
    # Strategy and first agents
    '/learn/enterprise-ai-strategy': ['Guide', 'Enterprise AI Strategy Framework for Leaders',
        'The five decisions to make before deploying AI, such as build vs buy and cloud vs on-premise, plus a maturity model.'],
    '/insights/roi-business-case-ai-agents': ['Framework', 'How to Build the Business Case for AI Agents',
        'The three numbers a finance team needs to approve an AI project: hours saved, revenue uplift and risk cost avoided.'],
    '/insights/choosing-first-ai-agent': ['Framework', 'How to Choose Your First AI Agent',
        'Four criteria for a first agent that works, what to avoid, and how one success sets up the next.'],
    # AI agents
    '/learn/how-ai-agents-work': ['Guide', 'How AI Agents Work: A Plain-English Technical Guide',
        'The perception, reasoning and action loop, agent memory, and how an agent differs from a chatbot or workflow tool.'],
    '/learn/top-ai-agent-platforms': ['Guide', 'Top AI Agent Platforms Compared',
        'AutoGen, LangChain, Vertex AI Agents and Copilot Studio: where each fits, where each falls short and how to choose.'],
    '/learn/ai-agent-vs-llm': ['Guide', 'AI Agent vs. LLM: The Real Difference Explained',
        'An LLM is a reasoning engine. An agent wraps it with memory, tools and the ability to act. Why the difference matters.'],
    # Industry playbooks
    '/insights/ecommerce-cart-recovery-whatsapp': ['Industry playbook', 'The 78-Minute Window: WhatsApp Cart Recovery',
        'Why cart abandonment is a timing and channel problem, and how a WhatsApp agent reaches shoppers before intent fades.'],
    '/insights/logistics-wismo-ai-agents': ['Industry playbook', 'Eliminate WISMO Queries with AI Agents',
        'How agents answer order-status questions before customers have to ask, and what that does to support volume.'],
    '/insights/nbfc-kyc-automation': ['Industry playbook', 'How NBFCs Cut KYC TAT from 7 Days to 4 Hours',
        'Automating the KYC steps that don’t need human judgment, without skipping a compliance step.'],
    '/insights/manufacturing-ai-quality-control': ['Industry playbook', 'Why Manufacturing Teams Catch Defects Too Late',
        'Why quality problems surface in the field months after shipping, and how AI QC agents move detection earlier.'],
    '/insights/real-estate-lead-conversion': ['Industry playbook', 'Why Builders Lose 70% of Property Leads',
        'Buyers decide within 48 hours of an inquiry. Why builder CRMs fail at that speed, and what fast, personal follow-up looks like.'],
    '/insights/legal-ai-contract-review': ['Industry playbook', 'AI Contract Review: From 4 Hours to 20 Minutes',
        'First-pass review is pattern work: non-standard clauses, missing definitions and risk flags. How AI takes it on.'],
    '/insights/saas-churn-ai-early-warning': ['Industry playbook', 'SaaS Churn Early Warning with AI Agents',
        'Cancellation decisions are made 30 to 60 days before the request. How a health-score agent spots the signals and acts.'],
}

FURTHER_READING = {
    # Homepage: the AI-native engineering cluster, plus the CTO/CIO governance checklist
    'home': ['/learn/what-is-ai-native-engineering', '/compare/ai-native-engineering-vs-ai-coding-tools',
             '/compare/upcore-vs-building-in-house', '/learn/ai-data-governance'],
    # Services
    'aine': ['/learn/what-is-ai-native-engineering', '/compare/ai-native-engineering-vs-ai-coding-tools',
             '/compare/upcore-vs-building-in-house'],
    'gov': ['/learn/ai-data-governance', '/learn/hipaa-compliant-ai', '/compare/ai-agents-vs-copilot-financial-services',
            '/insights/human-in-the-loop'],
    'bpa': ['/insights/choosing-first-ai-agent', '/insights/human-in-the-loop', '/learn/how-ai-agents-work',
            '/learn/ai-agent-vs-llm'],
    'fao': ['/learn/enterprise-ai-strategy', '/insights/roi-business-case-ai-agents', '/insights/choosing-first-ai-agent'],
    'fde': ['/learn/how-ai-agents-work', '/learn/top-ai-agent-platforms', '/insights/choosing-first-ai-agent',
            '/insights/human-in-the-loop'],
    # Who we help
    'tech-software': ['/learn/what-is-ai-native-engineering', '/compare/ai-native-engineering-vs-ai-coding-tools',
                      '/insights/saas-churn-ai-early-warning'],
    'ecommerce-retail': ['/insights/logistics-wismo-ai-agents', '/insights/ecommerce-cart-recovery-whatsapp',
                         '/insights/choosing-first-ai-agent'],
    'operations-heavy': ['/insights/real-estate-lead-conversion', '/insights/nbfc-kyc-automation',
                         '/insights/manufacturing-ai-quality-control'],
    'professional-services': ['/insights/legal-ai-contract-review', '/insights/roi-business-case-ai-agents',
                              '/insights/human-in-the-loop'],
}


def _library_json(href):
    path = os.path.join(CONTENT, href.strip('/').replace('/', '__') + '.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    return None


def resolve(entry):
    """An href or [href, kicker, title, desc] -> (href, kicker, title, desc), or None when no library page matches."""
    row = [entry] if isinstance(entry, str) else list(entry)
    href = row[0]
    row = (row + ['', '', ''])[1:4]
    known = ARTICLES.get(href, ['', '', ''])
    kicker, title, desc = (row[i] or known[i] for i in range(3))
    d = _library_json(href)
    if d is None and href not in PY_PAGES:
        return None
    if d:
        kicker = kicker or KIND_LABEL.get(d.get('kind'), 'Read next')
        title = title or re.sub(r'\s*\|\s*Upcore.*$', '', d.get('title', '')).strip()
        desc = desc or d.get('meta', '')
    return href, kicker or 'Read next', title or href, desc


def items(key):
    """The resolved links for one page, at most MAX_ITEMS; unknown links are reported on stderr and left out."""
    out = []
    for entry in FURTHER_READING.get(key, []):
        r = resolve(entry)
        if r is None:
            print(f'reading.py: no library page for {entry if isinstance(entry, str) else entry[0]} (page {key}); link skipped', file=sys.stderr)
        else:
            out.append(r)
    return out[:MAX_ITEMS]
