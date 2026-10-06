"""Tool / integration logos (Simple Icons, CC0 paths) rendered as a per-page SVG sprite."""
import json, os, re

HERE = os.path.dirname(__file__)
ICONS = json.load(open(os.path.join(HERE, 'si', 'icons.json'), encoding='utf-8'))
HEX_FIX = {'amazonwebservices': 'FF9900', 'magento': 'EE672F', 'microsoft': '737373', 'microsoftazure': '0078D4', 'microsoftoutlook': '0078D4',
           'microsoftteams': '6264A7', 'openai': '000000', 'powerapps': '742774', 'powerautomate': '0066FF', 'salesforce': '00A1E0',
           'slack': '4A154B', 'sonarqube': '4E9BCD'}
LABEL = {'amazonwebservices': 'AWS', 'microsoftazure': 'Azure', 'googlecloud': 'Google Cloud', 'githubcopilot': 'GitHub Copilot',
         'modelcontextprotocol': 'MCP', 'microsoft': 'Microsoft 365', 'microsoftteams': 'Teams', 'microsoftoutlook': 'Outlook',
         'nodedotjs': 'Node.js', 'googlegemini': 'Gemini', 'githubactions': 'GitHub Actions', 'powerautomate': 'Power Automate',
         'powerapps': 'Power Apps', 'gmail': 'Gmail', 'googleads': 'Google Ads', 'huggingface': 'Hugging Face'}

USED = set()


def hexc(s):
    return '#' + (HEX_FIX.get(s) or ICONS[s].get('hex') or '0A1419')


def name(s):
    return LABEL.get(s) or ICONS[s]['title']


def logo(s, small=False):
    USED.add(s)
    return (f'<span class="logo{" logo--sm" if small else ""}" style="--c:{hexc(s)}"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-{s}"/></svg>'
            f'<span>{name(s)}</span></span>')


def sprite():
    sym = ''.join(f'<symbol id="i-{s}" viewBox="0 0 24 24"><path d="{ICONS[s]["d"]}"/></symbol>' for s in sorted(USED))
    USED.clear()
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">{sym}</svg>'


def row(slugs, small=False):
    return '<div class="logos">' + ''.join(logo(s, small) for s in slugs) + '</div>'


ENGINEERING = [
    ('Planning &amp; code', 'Specs, tickets and repositories', ['jira', 'linear', 'confluence', 'github', 'gitlab']),
    ('CI/CD &amp; quality gates', 'Builds, security scans, coverage, monitoring', ['githubactions', 'jenkins', 'sonarqube', 'snyk', 'sentry', 'datadog']),
    ('AI models &amp; assistants', 'The models and copilots your teams already use', ['claude', 'openai', 'googlegemini', 'githubcopilot', 'cursor', 'huggingface']),
    ('Agent frameworks', 'How agents reason, call tools and connect', ['modelcontextprotocol', 'langchain', 'n8n', 'powerautomate', 'powerapps']),
    ('Cloud &amp; runtime', 'Your tenancy, your infrastructure', ['amazonwebservices', 'microsoftazure', 'googlecloud', 'kubernetes', 'docker', 'terraform', 'vercel']),
    ('Languages &amp; data', 'What we build and ship in', ['python', 'typescript', 'nodedotjs', 'react', 'fastapi', 'postgresql']),
]
BUSINESS = [
    ('CRM &amp; sales', 'Where your pipeline lives', ['salesforce', 'hubspot', 'zoho']),
    ('Work &amp; collaboration', 'Email, chat and documents', ['microsoft', 'microsoftteams', 'microsoftoutlook', 'gmail', 'slack', 'notion']),
    ('Customer channels', 'Where your customers talk to you', ['whatsapp', 'telegram', 'zendesk']),
    ('Commerce &amp; marketing', 'Stores, catalogs and ad accounts', ['shopify', 'woocommerce', 'magento', 'googleads', 'meta']),
]
HOME = [
    ('Engineering &amp; delivery', 'Planning, code, CI/CD and quality gates', ['jira', 'linear', 'github', 'gitlab', 'githubactions', 'sonarqube', 'snyk', 'datadog']),
    ('AI models &amp; agents', 'Models, copilots and agent frameworks', ['claude', 'openai', 'googlegemini', 'githubcopilot', 'cursor', 'modelcontextprotocol', 'langchain', 'n8n']),
    ('Cloud &amp; runtime', 'Your tenancy, your infrastructure', ['amazonwebservices', 'microsoftazure', 'googlecloud', 'kubernetes', 'docker', 'terraform']),
    ('Business systems', 'CRM, collaboration, channels and commerce', ['salesforce', 'hubspot', 'zoho', 'microsoft', 'slack', 'whatsapp', 'shopify', 'zendesk']),
]
DISCLAIMER = 'Logos are trademarks of their respective owners and show integration compatibility, not partnership or endorsement. Where there is no off-the-shelf connector, we integrate through your systems&rsquo; APIs, email and documents.'


def stack(cats, eyebrow, h2, lead, sid='stack', alt=False):
    rows = ''.join(f'<div class="stack-row"><div class="stack-k"><h3>{k}</h3><p>{d}</p></div>{row(sl)}</div>' for k, d, sl in cats)
    cls = 'sec'
    return f'''<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">
<div class="sec-head sec-head--split"><div><div class="eyebrow" data-reveal>{eyebrow}</div><h2 id="{sid}-h" class="t-h2" data-reveal>{h2}</h2></div><p class="t-lead" data-reveal style="--d:1">{lead}</p></div>
<div class="stack" data-reveal>{rows}</div><p class="fine">{DISCLAIMER}</p></div></section>'''


def strip(slugs, label):
    return f'<div class="tool-strip" data-reveal><span class="t-mono">{label}</span>{row(slugs, small=True)}<p class="fine">Logos show integration compatibility, not partnership.</p></div>'
