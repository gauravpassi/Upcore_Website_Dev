"""Pre-publish checks for library articles (tools/v4-build/content/*.json) and their built pages.

    python tools/content/validate.py                      # every article, lenient for the pre-pipeline ones
    python tools/content/validate.py --strict FILE...     # full editorial checks (the content pipeline uses this)
    python tools/content/validate.py --built FILE...      # also check the generated HTML, sitemap and /insights hub

Strict mode applies automatically to articles with "ai_assisted": true. Exit code 1 if any ERROR.
House rules come from CLAUDE.md, docs/CONVENTIONS.md and docs/DESIGN-SYSTEM-V4.md; editorial rules from
tools/content/WRITER.md. Standard library only, like the rest of tools/."""
import datetime, glob, html as H, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CONTENT = os.path.join(ROOT, 'tools', 'v4-build', 'content')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'v4-build'))
import authors as AU  # noqa: E402

REQUIRED = {'file': str, 'path': str, 'title': str, 'meta': str, 'robots': str, 'published': str, 'faq': list,
            'related': list, 'stats': list, 'sections': list, 'lead': str, 'eyebrow': str, 'date_label': str,
            'kind': str, 'h1': str, 'aside': list}
OPTIONAL = {'author': str, 'reviewer': str, 'updated': str, 'ai_assisted': bool, 'sources': list, 'backlog_id': str}
KINDS = {'guide', 'comparison', 'framework', 'playbook'}
SECTIONS = {'insights', 'learn', 'compare'}
TAGS = {'p', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'br', 'a', 'div', 'span', 'table', 'thead', 'tbody',
        'tr', 'th', 'td', 'dl', 'dt', 'dd', 'code', 'pre', 'blockquote', 'cite'}
CLASS_OK = re.compile(r'^(lx-[a-z0-9-]+|ar-call|ar-call-k|is-hi|is-yes|is-no|is-part|hl)$')
BANNED = ['revolutionize', 'revolutionise', 'game-changer', 'game changer', 'unlock the', 'unleash', "in today's fast-paced",
          'in today’s fast-paced', 'delve', 'cutting-edge', 'synergy', 'paradigm shift', 'seamlessly']
UK = {'organisation': 'organization', 'optimise': 'optimize', 'optimisation': 'optimization', 'prioritise': 'prioritize',
      'analyse': 'analyze', 'behaviour': 'behavior', 'colour': 'color', 'favour': 'favor', 'licence': 'license',
      'catalogue': 'catalog', 'utilise': 'utilize', 'standardise': 'standardize', 'minimise': 'minimize',
      'maximise': 'maximize', 'recognise': 'recognize', 'authorise': 'authorize', 'judgement': 'judgment'}
REDIRECTED = None  # filled lazily from vercel.json


class Body(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problems, self.links, self.text = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in TAGS:
            self.problems.append(f'tag <{tag}> is not allowed in article HTML')
        if 'style' in a:
            self.problems.append(f'inline style on <{tag}>')
        for c in (a.get('class') or '').split():
            if not CLASS_OK.match(c):
                self.problems.append(f'class "{c}" is not an article component (.lx-*, .ar-call*)')
        if tag == 'a':
            self.links.append(a.get('href') or '')

    def handle_data(self, data):
        self.text.append(data)


def redirect_sources():
    global REDIRECTED
    if REDIRECTED is None:
        v = json.load(open(os.path.join(ROOT, 'vercel.json'), encoding='utf-8'))
        REDIRECTED = {r['source'] for r in v.get('redirects', []) if not r.get('has')}
    return REDIRECTED


def page_exists(path):
    path = path.split('#')[0].split('?')[0].rstrip('/') or '/'
    if path == '/':
        return os.path.exists(os.path.join(ROOT, 'index.html'))
    rel = path.lstrip('/')
    return os.path.exists(os.path.join(ROOT, rel + '.html')) or os.path.exists(os.path.join(ROOT, rel, 'index.html'))


def words(s):
    return len(re.sub(r'<[^>]+>', ' ', s).split())


def plain(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def check(fn, strict_flag, built, all_paths, pending):
    errs, warns = [], []
    E, W = errs.append, warns.append
    try:
        d = json.load(open(fn, encoding='utf-8'))
    except Exception as e:  # noqa: BLE001
        return [f'not valid JSON: {e}'], []
    strict = strict_flag or bool(d.get('ai_assisted'))
    for k, t in REQUIRED.items():
        if k not in d:
            E(f'missing key "{k}"')
        elif not isinstance(d[k], t):
            E(f'"{k}" should be {t.__name__}')
    for k, t in OPTIONAL.items():
        if k in d and not isinstance(d[k], t):
            E(f'"{k}" should be {t.__name__}')
    unknown = set(d) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        E(f'unknown keys {sorted(unknown)}')
    if errs:
        return errs, warns

    # identity
    sec = d['path'].strip('/').split('/')[0]
    slug = d['path'].rstrip('/').rsplit('/', 1)[-1]
    if sec not in SECTIONS or d['path'] != f'/{sec}/{slug}' or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug):
        E(f'path "{d["path"]}" must be /insights|learn|compare/<lowercase-hyphen-slug>')
    if os.path.basename(fn) != f'{sec}__{slug}.json':
        E(f'filename should be {sec}__{slug}.json')
    if d['file'] != d['path'].lstrip('/') + '.html':
        E(f'"file" should be {d["path"].lstrip("/")}.html')
    if all_paths.count(d['path']) > 1:
        E('another content file uses the same path')
    if d['path'] in redirect_sources():
        E('path is a redirect source in vercel.json (a retired URL)')
    if d['kind'] not in KINDS:
        E(f'kind must be one of {sorted(KINDS)}')

    # head
    t = d['title']
    if not t.endswith(' | Upcore'):
        E('title must end with " | Upcore"')
    if len(t) > 60:
        (E if strict else W)(f'title is {len(t)} chars (max 60)')
    m = d['meta']
    lo = 140 if strict else 120
    if not lo <= len(m) <= 158:
        (E if strict else W)(f'meta description is {len(m)} chars (want {lo}-158)')
    if m.rstrip().endswith(('…', '...')):
        E('meta description is truncated (ends with an ellipsis)')
    if re.search(r'<|&[a-z]+;|&#\d+;', t + m):
        E('title/meta must be plain text without tags or entities (the generator HTML-escapes them)')

    # dates and people
    today = datetime.date.today().isoformat()
    for k in ('published', 'updated'):
        v = d.get(k) or ''
        if v and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
            E(f'"{k}" must be YYYY-MM-DD')
    if strict and not d['published']:
        E('"published" is required')
    if d.get('updated') and d['published'] and d['updated'] < d['published']:
        E('"updated" is earlier than "published"')
    if d['published'] > today:
        W(f'published date {d["published"]} is in the future')
    for k in ('author', 'reviewer'):
        if d.get(k) and d[k] not in AU.PEOPLE:
            E(f'{k} "{d[k]}" is not in tools/v4-build/authors.py')
    if strict and not d.get('author'):
        E('strict: a named author is required')
    if strict and d.get('ai_assisted') and not d.get('reviewer'):
        E('strict: AI-assisted articles need a named reviewer')

    # body
    body = Body()
    all_html = d['h1'] + d['lead'] + ''.join(s[2] for s in d['sections']) + ''.join(a for _, a in d['faq'])
    body.feed(all_html)
    for p in sorted(set(body.problems)):
        E(p)
    ids = [s[0] for s in d['sections']]
    for s in d['sections']:
        if len(s) != 3:
            E('each section must be [id, h2, html]')
            continue
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', s[0]):
            (E if strict else W)(f'section id "{s[0]}" should be lowercase-hyphenated without a trailing hyphen')
        if re.search(r'<h[12][ >]', s[2]):
            E(f'section "{s[0]}" contains an <h1>/<h2>; the section title is the h2')
    if len(ids) != len(set(ids)):
        E('duplicate section ids')
    text = ' '.join([plain(all_html), t, m] + [plain(x) for r in d['related'] for x in r[2:]])
    if '—' in json.dumps(d, ensure_ascii=False):
        E('em dash found (house rule: none; use " - ", "&ndash;" or rephrase)')
    low = text.lower()
    for b in BANNED:
        if b in low:
            (E if strict else W)(f'banned phrase "{b}"')
    for uk, us in UK.items():
        if re.search(rf'\b{uk}', low):
            W(f'UK spelling "{uk}" (US: {us})')
    n = sum(words(s[2]) for s in d['sections'])
    if strict and n < 1000:
        E(f'body is {n} words (strict minimum 1000)')
    elif n < 600:
        W(f'body is only {n} words')

    # links
    internal = [h for h in body.links if h.startswith('/')]
    external = [h for h in body.links if h.startswith('http')]
    for h in body.links:
        if h.startswith('/'):
            if h.split('#')[0].endswith('.html'):
                E(f'link {h} uses .html (cleanUrls)')
            elif not page_exists(h) and h not in pending:
                E(f'internal link {h} does not resolve to a page')
        elif h.startswith('http://'):
            E(f'insecure link {h}')
        elif h.startswith('https://www.upcoretech.com') or h.startswith('https://upcoretech.com'):
            E(f'use a root-relative link instead of {h}')
        elif not (h.startswith('https://') or h.startswith('#') or h.startswith('mailto:')):
            E(f'odd link "{h}"')
    if strict:
        if len(internal) < 3:
            E(f'strict: {len(internal)} internal links in the body (want 3+, one to a service page)')
        if not any(h.split('#')[0] in ('/ai-native-engineering', '/ai-engineering-governance', '/platform', '/fractional-ai-officer',
                                       '/forward-deployed-engineer') for h in internal):
            E('strict: no link to a service page in the body')
        stat_like = re.findall(r'\b\d+(?:\.\d+)?\s?%|\$\s?\d', plain(''.join(s[2] for s in d['sections'])))
        if stat_like and not external:
            E(f'strict: {len(stat_like)} figures (%/$) but no external source links')
        if not 4 <= len(d['faq']) <= 6:
            E(f'strict: {len(d["faq"])} FAQs (want 4-6)')
        for q, a in d['faq']:
            if not 25 <= words(a) <= 90:
                W(f'FAQ answer for "{q[:40]}" is {words(a)} words (aim for 40-70)')
        if not d.get('sources'):
            W('no "sources" list (the URLs the facts came from)')
        listed = {u.rstrip('/') for u in d.get('sources') or []}
        linked = {u.rstrip('/') for u in external}
        for u in sorted(linked - listed):
            W(f'external link not in "sources": {u}')
        for u in sorted(listed - linked):
            W(f'source never linked in the article: {u}')
    for r in d['related']:
        if len(r) != 4:
            E('related entries must be [href, kicker, title, desc]')
            continue
        if not (page_exists(r[0]) or r[0] in pending):
            E(f'related link {r[0]} does not resolve')
        if '<' in r[2] + r[3]:
            E('related title/desc must be plain text')
    if strict and not 2 <= len(d['related']) <= 4:
        E(f'strict: {len(d["related"])} related links (want 2-4)')
    if d['aside'] and (len(d['aside']) != 2 or not page_exists(d['aside'][1])):
        E('aside must be [label, existing href]')

    # built output
    if built:
        out = os.path.join(ROOT, d['file'])
        if not os.path.exists(out):
            E(f'{d["file"]} has not been built (run tools/v4-build/build_all.py)')
        else:
            s = open(out, encoding='utf-8').read()
            if f'<link rel="canonical" href="https://www.upcoretech.com{d["path"]}" />' not in s:
                E('built page has no matching canonical')
            for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                try:
                    g = json.loads(blob)['@graph']
                    art = next((x for x in g if x.get('@type') == 'Article'), None)
                    if art and art['dateModified'] < art['datePublished']:
                        E('JSON-LD dateModified is earlier than datePublished')
                except Exception as e:  # noqa: BLE001
                    E(f'JSON-LD does not parse: {e}')
            if '—' in s:
                W('built page contains an em dash (probably from shared chrome)')
        if f'<loc>https://www.upcoretech.com{d["path"]}</loc>' not in open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read():
            E('not in sitemap.xml (build_sitemap.py should add it)')
        if f'href="{d["path"]}"' not in open(os.path.join(ROOT, 'insights', 'index.html'), encoding='utf-8').read():
            E('not listed on /insights (run build_insights.py)')
    return errs, warns


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    strict, built = '--strict' in sys.argv, '--built' in sys.argv
    every = sorted(f for f in glob.glob(os.path.join(CONTENT, '*.json')) if os.path.basename(f) not in ('privacy.json', 'terms.json'))
    files = [os.path.abspath(a) for a in args] or every
    all_paths = [json.load(open(f, encoding='utf-8')).get('path') for f in every]
    pending = set()  # paths of other drafts in this run may be linked before they exist
    for f in files:
        try:
            pending.add(json.load(open(f, encoding='utf-8'))['path'])
        except Exception:  # noqa: BLE001
            pass
    total_e = 0
    for f in files:
        errs, warns = check(f, strict, built, all_paths, pending)
        total_e += len(errs)
        tag = 'FAIL' if errs else ('WARN' if warns else ' OK ')
        print(f'[{tag}] {os.path.relpath(f, ROOT)}')
        for e in errs:
            print(f'   ERROR  {e}')
        for w in warns:
            print(f'   warn   {w}')
    print(f'\n{len(files)} file(s), {total_e} error(s)')
    sys.exit(1 if total_e else 0)


if __name__ == '__main__':
    main()
