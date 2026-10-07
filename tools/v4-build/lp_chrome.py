"""Site chrome for the hand-maintained pages (2026-10-07). The generated pages get their nav and footer from
chrome.write(); these four keep hand-written bodies and scripts, and this script owns only their marked blocks:
  /lp/governance-index, /lp/ai-maturity-index  quiz landing pages (lp/lead-magnet-engine.js + inline NICHE_CONFIG)
  /build-your-demo                             agent demo builder (POSTs to /api/build-demo)
  /ai-operations                               $3 AI Operations Toolkit (Razorpay checkout)
Blocks:
  <!-- @chrome head --> Geist + stylesheets (before the page's inline <style>)
  <!-- @chrome nav -->  skip link + chrome.nav(), with the page's own CTA where it has one (no announcement bar)
  <!-- @chrome foot --> chrome.footer()
  <!-- @chrome js -->   js/upcore-v4.js + js/upcore-v5.js (no v4-analytics: these pages tag via gtag.js directly)
The quiz pages load the full css/upcore-v4.css + upcore-v5.css. The other two use generic class names
(.hero, .card, .step, .chip, .wrap ...) that the full stylesheets also style, so they load css/upcore-chrome.css
instead: the nav, footer, button and cookie-banner rules only, extracted here from the full stylesheets on every
run (never edit that file by hand).
The first run converted each page's own styles once to the calm light theme (marker "calm light theme" in its
<style>; the two product pages' colour tokens were renamed --bd-* / --ao-* so they can't collide with the site's).
Later runs only refresh the blocks and css/upcore-chrome.css.
Run from the repo root: python tools/v4-build/lp_chrome.py (build_all.py runs it)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" />'
HEAD = {'full': FONTS + '\n<link rel="stylesheet" href="/css/upcore-v4.css?v={V}" />\n<link rel="stylesheet" href="/css/upcore-v5.css?v={V}" />',
        'chrome': FONTS + '\n<link rel="stylesheet" href="/css/upcore-chrome.css?v={V}" />'}
JS = '<script src="/js/upcore-v4.js?v={V}" defer></script>\n<script src="/js/upcore-v5.js?v={V}" defer></script>'


# ---------------------------------------------------------------- css/upcore-chrome.css (generated)
def parse_css(css):
    """Tiny CSS reader: [('rule', selector, body) | ('at', prelude, children) | ('raw', prelude, body)]."""
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)
    n = len(css)

    def block(i):
        nodes = []
        while i < n:
            while i < n and css[i] in ' \t\r\n':
                i += 1
            if i >= n:
                break
            if css[i] == '}':
                return nodes, i + 1
            j, k = css.find('{', i), css.find(';', i)
            if k != -1 and (j == -1 or k < j):
                i = k + 1
                continue
            pre = css[i:j].strip()
            if pre.startswith(('@media', '@supports')):
                kids, i = block(j + 1)
                nodes.append(('at', pre, kids))
                continue
            d, m = 0, j
            while True:
                if css[m] == '{':
                    d += 1
                elif css[m] == '}':
                    d -= 1
                    if d == 0:
                        break
                m += 1
            nodes.append(('raw' if pre.startswith('@') else 'rule', pre, css[j + 1:m]))
            i = m + 1
        return nodes, i
    return block(0)[0]


def split_sel(sel):
    out, d, cur = [], 0, ''
    for ch in sel:
        if ch == '(':
            d += 1
        elif ch == ')':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    return out + [cur.strip()]


STATE = {'open', 'is-scrolled', 'is-compact', 'is-hidden', 'is-bump', 'menu-open', 'consent-open', 'js', 'fonts-ready', 'is-off', 'show'}


def chrome_css():
    """Every rule of css/upcore-v4.css + upcore-v5.css whose selectors only involve the chrome's own classes."""
    markup = C.nav('') + C.footer()
    own = set(re.findall(r'class="([^"]+)"', markup))
    own = {c for v in own for c in v.split()} | {'consent', 'consent-btns', 'skip', 'sr'}
    own.discard('wrap')
    cls = re.compile(r'\.([A-Za-z_][\w-]*)')

    def keep(sel):
        t = cls.findall(sel)
        return bool(t) and any(x in own for x in t) and all(x in own or x in STATE for x in t)

    def walk(nodes, root_ok):
        out, used = [], set()
        for kind, pre, body in nodes:
            if kind == 'rule':
                if pre == ':root' and root_ok:
                    out.append(f':root{{{body.strip()}}}')
                    continue
                sels = [s for s in split_sel(pre) if keep(s)]
                if sels:
                    out.append(f'{",".join(sels)}{{{body.strip()}}}')
                    used |= set(re.findall(r'animation(?:-name)?\s*:\s*([\w-]+)', body))
            elif kind == 'at':
                inner, u = walk(body, False)
                if inner:
                    out.append(f'{pre}{{\n' + '\n'.join('  ' + r for r in inner) + '\n}')
                    used |= u
        return out, used

    def keyframes(nodes):  # at any depth (the island's are inside its media query)
        for kind, pre, body in nodes:
            if kind == 'raw' and pre.startswith('@keyframes'):
                yield pre.split()[1], f'{pre}{{{body.strip()}}}'
            elif kind == 'at':
                yield from keyframes(body)

    rules, used, frames = [], set(), {}
    for name, root_ok in (('upcore-v4.css', True), ('upcore-v5.css', False)):
        nodes = parse_css(open(os.path.join(C.ROOT, 'css', name), encoding='utf-8').read())
        r, u = walk(nodes, root_ok)
        rules += r
        used |= u
        frames.update(keyframes(nodes))
    base = """/* GENERATED by tools/v4-build/lp_chrome.py from css/upcore-v4.css + css/upcore-v5.css. Do not edit.
   The site nav (island), footer, buttons and cookie banner for hand-built pages whose own class names
   clash with the full stylesheets (/ai-operations, /build-your-demo). */
:where(.nav,.foot,.consent),:where(.nav,.foot,.consent) :where(*,*::before,*::after){box-sizing:border-box;margin:0;padding:0;}
:where(.nav,.foot) :where(a){color:inherit;text-decoration:none;}
:where(.nav,.foot,.consent) :where(button){font:inherit;color:inherit;background:none;border:0;cursor:pointer;}
:where(.nav,.foot) :where(img,svg){display:block;max-width:100%;}
:where(.nav,.foot) :where(ul,ol){list-style:none;}
.nav,.foot,.consent,.skip{font-family:var(--f-sans);font-size:16px;line-height:1.6;letter-spacing:normal;-webkit-font-smoothing:antialiased;}
.foot .wrap{max-width:var(--wrap);margin:0 auto;padding:0 var(--gutter);}
"""
    css = base + '\n'.join(rules) + '\n' + '\n'.join(frames[k] for k in sorted(used) if k in frames) + '\n'
    open(os.path.join(C.ROOT, 'css', 'upcore-chrome.css'), 'w', encoding='utf-8', newline='\n').write(css)
    return len(css)


# ---------------------------------------------------------------- one-time light theme for the quiz pages
THEME = r'''
/* ── calm light theme (2026-10-07): chrome, Geist and tokens come from css/upcore-v4.css + v5 ── */
body{background:radial-gradient(ellipse 70% 460px at 50% 0%,rgba(33,210,237,.10),transparent 70%) no-repeat,var(--bg);background-size:auto;}
#lm-root{padding-top:clamp(36px,5vw,64px);}
.lm-h1{font-weight:600;letter-spacing:-.042em;line-height:1.05;color:var(--ink);text-wrap:balance;}
.lm-h2{font-weight:600;letter-spacing:-.03em;line-height:1.15;color:var(--ink);text-wrap:balance;}
.lm-question-text{font-weight:600;letter-spacing:-.028em;line-height:1.25;color:var(--ink);}
.lm-insight-copy{color:var(--ink);}
.lm-eyebrow{background:none;border:0;border-radius:0;padding:0;font-family:var(--f-mono);font-size:11.5px;font-weight:500;letter-spacing:.14em;line-height:1.5;color:var(--cyan-ink);}
.lm-eyebrow-dot{flex-shrink:0;width:7px;height:7px;border-radius:2px;background:var(--cyan);box-shadow:0 0 0 4px var(--cyan-wash);}
.lm-quiz-eyebrow,.lm-insight-badge,.lm-gate-done{font-family:var(--f-mono);font-weight:500;letter-spacing:.14em;color:var(--cyan-ink);}
.lm-hero-visual-label,.lm-sample-report-tag,.lm-sample-q-tag{font-family:var(--f-mono);font-weight:500;letter-spacing:.12em;color:var(--muted);}

.lm-btn{min-height:52px;font:500 16px/1 var(--f-sans);transition:transform .4s var(--ease-out),box-shadow .4s,background .2s,border-color .2s;}
.lm-btn-primary{background:var(--ink);color:#fff;padding:8px 8px 8px 26px;gap:14px;animation:none;}
.lm-btn-primary::after{content:'';flex-shrink:0;width:36px;height:36px;border-radius:50%;background:var(--cyan) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230A1419' stroke-width='2.2' stroke-linecap='round'%3E%3Cpath d='M5 12h14M13 6l6 6-6 6'/%3E%3C/svg%3E") center/15px no-repeat;}
.lm-btn-primary:disabled{opacity:.45;}
.lm-btn-ghost{color:var(--ink);border-color:var(--hair);}
.lm-link-secondary{min-height:52px;font:500 16px/1 var(--f-sans);color:var(--ink);border-color:var(--hair);}
.lm-continue-btn{justify-content:space-between;}

.lm-proof-icon{background:var(--cyan-wash);color:var(--cyan-ink);}
.lm-proof-cert,.lm-testimonial-badge{background:#fff;color:var(--ink-2);}
.lm-why-now,.lm-fw-preview-card,.lm-hero-visual-card,.lm-testimonial-card{border-radius:16px;background:var(--bg2);border-color:var(--hair-2);}
.lm-sample-report,.lm-sample-q,.lm-email-gate{border-radius:16px;background:#fff;border-color:var(--hair);box-shadow:0 40px 70px -48px rgba(7,26,38,.4),0 1px 2px rgba(7,26,38,.04);}
.lm-email-gate{background:#fff;}
.lm-icp-line{border-left-color:var(--cyan);color:var(--ink-2);}
.lm-weak-callout{background:var(--cyan-wash);border-left-color:var(--cyan-ink);}
.lm-testimonial-quote{color:var(--ink);}
.lm-testimonial-video{background:#fff;color:var(--ink);}
.lm-how-num{background:var(--ink);color:var(--cyan);font-family:var(--f-mono);font-weight:500;}

.lm-quiz-progress-track,.lm-sr-dim-track{background:var(--hair-2);}
.lm-quiz-back,.lm-quiz-exit{background:#fff;border-color:var(--hair);color:var(--ink-2);}
.lm-option,.lm-sample-q-opt{background:#fff;border-color:var(--hair);border-radius:12px;color:var(--ink);}
.lm-option-selected{background:var(--cyan-wash);border-color:var(--cyan-ink);}
.lm-opt-num{border-color:var(--hair);color:var(--muted);font-family:var(--f-mono);font-weight:500;}
.lm-option-selected .lm-opt-num{background:var(--ink);border-color:var(--ink);color:var(--cyan);}
.lm-opt-check{color:var(--cyan-ink);}

.lm-sr-score-num{color:var(--ink);font-weight:600;letter-spacing:-.05em;}
.lm-sr-tier{color:var(--cyan-ink);background:var(--cyan-wash);font-weight:600;}
.lm-score-blur{color:rgba(10,20,25,.32);font-family:var(--f-mono);}
.lm-radar-data{fill:rgba(33,210,237,.18);stroke:var(--cyan-ink);}
.lm-fw-badge-label{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(7,26,38,.08);}

.lm-faq-q{background:#fff;border-color:var(--hair);font-weight:500;color:var(--ink);border-radius:12px;}
.lm-faq-q[aria-expanded="true"]{background:#fff;border-color:var(--cyan-ink);border-radius:12px 12px 0 0;}
.lm-faq-q[aria-expanded="true"]+.lm-faq-a{border-color:var(--cyan-ink);border-radius:0 0 12px 12px;}
.lm-input{background:#fff;border-color:var(--hair);border-radius:10px;color:var(--ink);}
.lm-input:focus{border-color:var(--cyan-ink);box-shadow:0 0 0 3px rgba(33,210,237,.2);}
.lm-legal a{color:var(--ink-2);}
.lm-sticky-cta{background:rgba(255,255,255,.9);-webkit-backdrop-filter:saturate(1.4) blur(14px);backdrop-filter:saturate(1.4) blur(14px);border-top-color:var(--hair);box-shadow:0 -10px 30px -20px rgba(7,26,38,.35);}

@media (hover:hover) and (pointer:fine){
  .lm-btn-primary:hover{background:#16252C;transform:translateY(-1px);box-shadow:0 14px 30px -12px rgba(10,20,25,.5);}
  .lm-btn-ghost:hover,.lm-link-secondary:hover{background:rgba(10,20,25,.04);border-color:var(--ink);}
  .lm-option:hover,.lm-sample-q-opt:hover{border-color:var(--cyan-ink);background:var(--cyan-wash);}
  .lm-quiz-back:hover,.lm-quiz-exit:hover,.lm-faq-q:hover{border-color:var(--cyan-ink);color:var(--cyan-ink);}
}
@media (max-width:600px){
  .lm-eyebrow{font-size:10.5px;letter-spacing:.1em;}
  .lm-btn-primary{justify-content:space-between;}
}
/* @end calm light theme */
'''


def theme(css):
    """One-time conversion of the old dark inline quiz styles (idempotent: skipped once converted)."""
    if 'calm light theme' in css:
        return css
    a = css.index('/* ── Navigation (sitewide)')
    b = css.index('*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}')
    css = css[:a] + css[b:]
    css = css[:css.index('/* == PRIMARY CTA GLOW')]
    css = re.sub(r':root\{[^}]*\}', ':root{--teal:#21D2ED;--bg:#FFFFFF;--bg2:#F6F8F9;--card:#FFFFFF;--txt:#0A1419;--txt2:#34434B;--txt3:#5D6B73;--border:#DFE5E8;}', css, count=1)
    css = re.sub(r"h1,h2,h3\{font-family:'Space Grotesk'[^}]*\}\n?", '', css, count=1)
    css = re.sub(r'body\{font-family:"DM Sans",sans-serif;color:var\(--txt\);line-height:1\.6;overflow-x:hidden;[\s\S]*?\n\}',
                 'body{font-family:var(--f-sans);color:var(--txt);line-height:1.6;overflow-x:hidden;}', css, count=1)
    css = css.replace('"DM Sans",sans-serif', 'var(--f-sans)').replace('"JetBrains Mono",monospace', 'var(--f-mono)')
    css = css.replace('color:#3ee1f5', 'color:var(--cyan-ink)').replace('rgba(255,255,255,.15)', 'var(--hair)')
    css = css.replace(':focus-visible{outline:2px solid var(--teal);outline-offset:2px;}', ':focus-visible{outline:2px solid var(--focus);outline-offset:2px;}')
    css = css.replace('.lm-btn-ghost:hover{background:rgba(255,255,255,.04);}', '').replace('.lm-link-secondary:hover{background:rgba(255,255,255,.05);transform:translateY(-1px);}', '')
    return css.rstrip() + '\n' + THEME


# ---------------------------------------------------------------- one-time light themes for the two product pages
def tokens(s, prefix):
    """Rename the page's own :root custom properties (--x -> --<prefix>x) everywhere in the page."""
    css = re.search(r'<style>([\s\S]*?)</style>', s).group(1)
    names = re.findall(r'--([\w-]+)\s*:', re.search(r':root\s*\{([^}]*)\}', css).group(1))
    for nm in sorted(set(names), key=len, reverse=True):
        s = re.sub(r'--' + re.escape(nm) + r'(?![\w-])', '--' + prefix + nm, s)
    return s


def cut(css, start, end):
    a = css.index(start)
    return css[:a] + css[css.index(end, a):]


THEME_DEMO = r'''
/* ── calm light theme (2026-10-07): site nav, footer and Geist come from css/upcore-chrome.css ── */
:root{--bd-bg:#FFFFFF;--bd-bg2:#F6F8F9;--bd-bg3:#EEF2F4;--bd-card:#FFFFFF;--bd-card2:#F6F8F9;--bd-teal:#21D2ED;--bd-teal2:#3EE1F5;--bd-mint:#0ABFCC;--bd-green:#15803D;--bd-red:#C2361F;--bd-txt:#0A1419;--bd-txt2:#34434B;--bd-txt3:#5D6B73;--bd-ink:#0A1419;--bd-ink-press:#000;--bd-border:#DFE5E8;--bd-bh:#9FB0B8;--bd-glow:rgba(33,210,237,.14);--bd-grad:linear-gradient(135deg,#0ea5b5,#21D2ED);--bd-ff:var(--f-sans);--bd-max:1240px;}
body{background:#fff;}
.demo-banner{background:#FFF7E3;border-bottom-color:#F1DDAE;color:#7A5A12;font-weight:500;}
.demo-banner span{font-weight:600;}
.demo-banner{display:block;text-align:center;line-height:1.5;}
.demo-banner svg{display:inline-block;}
.field-label{flex-wrap:wrap;}
.page{min-height:0;padding:clamp(40px,5vw,72px) 24px clamp(64px,7vw,104px);background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(33,210,237,.10),transparent 60%),#fff;}
.page::before{background-image:radial-gradient(circle,rgba(10,20,25,.08) 1px,transparent 1.3px);background-size:22px 22px;-webkit-mask-image:linear-gradient(#000,transparent 70%);mask-image:linear-gradient(#000,transparent 70%);}
.demo-card{border-radius:20px;box-shadow:0 50px 90px -60px rgba(7,26,38,.45),0 2px 6px -2px rgba(7,26,38,.05);}
.card-header{background:var(--bd-bg2);}
.ch-icon{background:var(--ink);color:var(--cyan);}
.ch-title{font-weight:600;color:var(--ink);}
.ch-sub{color:var(--cyan-ink);}
.step-dot{background:var(--hair);}
.eyebrow{font-family:var(--f-mono);font-weight:500;letter-spacing:.14em;color:var(--cyan-ink);}
.state-title{font-weight:600;letter-spacing:-.035em;line-height:1.12;color:var(--ink);}
.state-title strong{font-weight:600;color:var(--cyan-ink);}
.field-label{font-family:var(--f-mono);font-size:10.5px;font-weight:500;color:var(--ink-2);}
.field-label .opt{font-family:var(--f-sans);font-size:11.5px;}
.ind-option{background:#fff;border-color:var(--hair);}
.ind-option:hover{border-color:var(--ink);}
.ind-option.selected{background:var(--cyan-wash);border-color:var(--cyan-ink);}
.ind-icon{color:var(--cyan-ink);}
.ind-label{font-weight:600;color:var(--ink);}
input[type="text"],input[type="email"],input[type="tel"],textarea,select{background:#fff!important;border-color:var(--hair)!important;color:var(--ink)!important;font-size:16px!important;}
input[type="tel"]{width:100%;border:1px solid var(--hair);border-radius:12px;padding:13px 16px;font-family:var(--f-sans);outline:none;}
input:focus,textarea:focus,select:focus{border-color:var(--cyan-ink)!important;box-shadow:0 0 0 3px rgba(33,210,237,.18);}
.chip{background:#fff;border-color:var(--hair);color:var(--ink-2);font-weight:500;}
.chip:hover{border-color:var(--ink);color:var(--ink);}
.chip.selected{background:var(--ink);border-color:var(--ink);color:#fff;}
.btn-primary,.btn-open{background:var(--ink);color:#fff;font-weight:500;letter-spacing:-.01em;animation:none;box-shadow:none;}
.btn-primary:hover:not(:disabled),.btn-open:hover{background:#16252C;box-shadow:0 14px 30px -12px rgba(10,20,25,.5);}
.btn-ghost{color:var(--ink-2);border-color:var(--hair);font-weight:500;}
.btn-ghost:hover{border-color:var(--ink);color:var(--ink);}
.build-step.bs-active{background:var(--cyan-wash);border-color:rgba(10,111,130,.18);}
.bs-active .bs-badge,.progress-msg{color:var(--cyan-ink);}
.bs-done .bs-icon,.bs-done .bs-badge{color:#15803D;}
.progress-bar-wrap{background:var(--hair-2);}
.progress-agent-name,.done-title{font-weight:600;letter-spacing:-.03em;color:var(--ink);}
.done-pulse{background:var(--cyan-wash);}
.url-box{background:var(--bd-bg2);border-color:var(--cyan-ink);}
.url-text{color:var(--cyan-ink);font-family:var(--f-mono);}
.copy-btn{background:#fff;border-color:var(--hair);color:var(--ink);}
.copy-btn:hover{background:var(--cyan-wash);}
.done-actions .btn-ghost{margin-top:0;}
/* @end calm light theme */
'''


def theme_demo(s):
    s = tokens(s, 'bd-')
    s = s.replace('<a href="/assessment" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;color:var(--bd-teal);font-family:var(--bd-ff);font-size:14px;font-weight:600;padding:14px;border-radius:6px;border:1px solid var(--bd-border);transition:all .2s;text-align:center;" onmouseover="this.style.borderColor=\'var(--bd-teal)\'" onmouseout="this.style.borderColor=\'var(--bd-border)\'">',
                  '<a class="btn-ghost" href="#book-governance" data-gtm-cta="book-a-discovery-call" data-gtm-cta-type="secondary" data-gtm-cta-section="state-done">')

    def css(c):
        c = cut(c, '/* ── Navigation', ':root {')
        c = cut(c, 'footer{background:radial-gradient', '/* == PRIMARY CTA GLOW')
        c = c[:c.index('/* == PRIMARY CTA GLOW')]
        c = re.sub(r"h1,h2,h3\{font-family:'Space Grotesk'[^}]*\}\n?", '', c, count=1)
        return c.rstrip() + '\n' + THEME_DEMO
    return re.sub(r'<style>([\s\S]*?)</style>', lambda m: '<style>' + css(m.group(1)) + '</style>', s, count=1)


THEME_OPS = r'''
/* ── calm light theme (2026-10-07): site nav, footer and Geist come from css/upcore-chrome.css ── */
:root{--ao-bg:#FFFFFF;--ao-ink:#0A1419;--ao-card:#FFFFFF;--ao-panel:#F6F8F9;--ao-panel-2:#EEF2F4;--ao-fg:#0A1419;--ao-muted:#34434B;--ao-faint:#5D6B73;--ao-primary:#0A6F82;--ao-primary-soft:rgba(33,210,237,.14);--ao-primary-glow:rgba(33,210,237,.35);--ao-border:#DFE5E8;--ao-radius:16px;}
body{background:#fff radial-gradient(1200px 700px at 50% 0%,rgba(33,210,237,.09),transparent 70%) no-repeat;}
#main :is(h1,h2,h3,h4){font-weight:600;letter-spacing:-.035em;color:var(--ink);}
.hero{padding:clamp(40px,5vw,72px) 0 4rem;}
.accent{color:var(--cyan-ink);text-shadow:none;}
.pill{font-weight:500;}
.pill .dot,.svc-list .dot,.chip .dot{background:var(--cyan);box-shadow:0 0 0 4px var(--cyan-wash);border-radius:2px;}
.cta{background:var(--ink);color:#fff;font-weight:500;border-radius:999px;padding:.4rem .4rem .4rem 1.5rem;gap:.85rem;box-shadow:none;animation:none;}
.cta svg{box-sizing:content-box;width:.95rem;height:.95rem;padding:.6rem;border-radius:50%;background:var(--cyan);color:var(--ink);}
.cta:hover{box-shadow:0 14px 30px -12px rgba(10,20,25,.5);}
.cta.sm{padding:.3rem .3rem .3rem 1.1rem;}
.cta-ghost{background:#fff;color:var(--ink);border-color:var(--hair);border-radius:999px;}
.cta-ghost:hover{background:#fff;border-color:var(--ink);}
.card{box-shadow:0 1px 2px rgba(7,26,38,.04);}
.grid-bg{background-image:radial-gradient(circle,rgba(10,20,25,.08) 1px,transparent 1.3px);background-size:22px 22px;background-color:var(--paper);}
.hero-art{background:#0B1B29;box-shadow:0 40px 80px -40px rgba(7,26,38,.55);border-color:transparent;}
.stat-tile{background:rgba(255,255,255,.94);box-shadow:0 20px 40px -26px rgba(7,26,38,.4);}
.stat-tile .n,.price-box .big,.price-inline .now{color:var(--ink);}
.check-dot{background:var(--cyan-wash);}
.qcard .ghost,.kit .ghost{color:rgba(10,20,25,.06);}
.x-dot{background:rgba(10,20,25,.05);}
.yes-card{box-shadow:0 30px 60px -40px rgba(7,26,38,.35);}
.yes-card .check-big,.vcard .tier-badge{background:var(--ink);color:var(--cyan);}
.vcard:hover{border-color:var(--cyan-ink);box-shadow:0 24px 50px -30px rgba(7,26,38,.35);}
.vcard.selected{border-color:var(--cyan-ink);box-shadow:0 0 0 3px rgba(33,210,237,.25);}
.price-box{background:linear-gradient(165deg,rgba(33,210,237,.16),rgba(33,210,237,.04));border-color:rgba(10,111,130,.35);box-shadow:0 40px 70px -40px rgba(7,26,38,.35);}
.bar{background:rgba(10,20,25,.07);}
.bar i{background:var(--cyan);}
.get-card{background:linear-gradient(180deg,rgba(33,210,237,.09),rgba(255,255,255,0) 70%),#fff;border-color:rgba(10,111,130,.3);box-shadow:0 50px 90px -60px rgba(7,26,38,.45);}
.rzp-input{background:#fff;border-color:var(--hair);font-size:16px;}
.rzp-input:focus{background:#fff;border-color:var(--cyan-ink);box-shadow:0 0 0 3px rgba(33,210,237,.18);}
.rzp-success-icon{color:#15803D;}
.glow-blob{opacity:.6;}
html{overflow-x:visible;}
#main>section{overflow-x:clip;}
@media (max-width:640px){.hero{padding-top:28px;}}
/* @end calm light theme */
'''


def theme_ops(s):
    s = tokens(s, 'ao-')
    s = s.replace("/* header scroll state */\nconst hdr=document.getElementById('hdr');\naddEventListener('scroll',()=>hdr.classList.toggle('scrolled',scrollY>10),{passive:true});\n\n", '')

    def css(c):
        c = cut(c, '/* ---------- header ---------- */', '/* ---------- buttons ---------- */')
        c = cut(c, '/* ---------- footer ---------- */', '.glow-blob{')
        c = re.sub(r"'Space Grotesk'[^;}]*", 'var(--f-sans)', c)
        c = re.sub(r"'DM Sans'[^;}]*", 'var(--f-sans)', c)
        c = re.sub(r"'JetBrains Mono'[^;}]*", 'var(--f-mono)', c)
        c = c.replace('rgba(255,255,255,.025)', 'rgba(10,20,25,.04)').replace('rgba(255,255,255,.12)', 'var(--hair)')
        return c.rstrip() + '\n' + THEME_OPS
    return re.sub(r'<style>([\s\S]*?)</style>', lambda m: '<style>' + css(m.group(1)) + '</style>', s, count=1)


def theme_lp(s):
    return re.sub(r'<style>([\s\S]*?)</style>', lambda m: '<style>' + theme(m.group(1)) + '</style>', s, count=1)


PAGES = [
    dict(file='lp/governance-index.html', label='Governance Index', css='full', theme=theme_lp, main='<div id="lm-root">',
         cta=('/assessment', 'Book a Governance Review', 'book-a-governance-review'),
         font=r'<link href="https://fonts\.googleapis\.com/css2\?family=Space\+Grotesk[^>]*>', nav=r'<nav>\n  <div class="nav-logo">[\s\S]*?\n</nav>'),
    dict(file='lp/ai-maturity-index.html', label='AI Maturity Index', css='full', theme=theme_lp, main='<div id="lm-root">',
         cta=('/lp/maturity-review', 'Book an AI Strategy Review', 'book-an-ai-strategy-review'),
         font=r'<link href="https://fonts\.googleapis\.com/css2\?family=Space\+Grotesk[^>]*>', nav=r'<nav>\n  <div class="nav-logo">[\s\S]*?\n</nav>'),
    dict(file='build-your-demo.html', label='Agent demo builder', css='chrome', theme=theme_demo, main='<div class="demo-banner">', cta=None,
         font=r'<link href="https://fonts\.googleapis\.com/css2\?family=Space\+Grotesk[^>]*>', nav=r'<nav>\n  <div class="nav-logo">[\s\S]*?\n</nav>'),
    dict(file='ai-operations.html', label='AI Operations Toolkit', css='chrome', theme=theme_ops, main='<!-- ============ HERO ============ -->',
         cta=('#get', 'Get it for $3', 'get-it-for-3'),
         font=r'<link href="https://fonts\.googleapis\.com/css2\?family=DM\+Sans[^>]*>', nav=r'<!-- =+ HEADER =+ -->\n<header id="hdr">[\s\S]*?</header>'),
]


def block(s, name, html, find=None, before=None):
    start, end = f'<!-- @chrome {name} -->', f'<!-- @end {name} -->'
    blk = f'{start}\n{html}\n{end}'
    if start in s:
        return re.sub(re.escape(start) + r'[\s\S]*?' + re.escape(end), lambda m: blk, s, count=1)
    if find:
        m = re.search(find, s)
        assert m, (name, find)
        return s[:m.start()] + blk + s[m.end():]
    i = s.index(before)
    return s[:i] + blk + '\n' + s[i:]


def run(p):
    path = os.path.join(C.ROOT, p['file'])
    s = open(path, encoding='utf-8-sig').read()
    nav = C.nav('', cta=p['cta'])
    if 'calm light theme' not in s:
        s = p['theme'](s)
    s = block(s, 'head', HEAD[p['css']].replace('{V}', str(C.V)), find=p['font'])
    s = block(s, 'nav', '<a class="skip" href="#main">Skip to content</a>\n' + nav, find=p['nav'])
    s = block(s, 'foot', C.footer(), find=r'<footer>[\s\S]*?\n</footer>')
    s = block(s, 'js', JS.replace('{V}', str(C.V)), before='</body>')
    if '<main id="main"' not in s:
        s = s.replace(p['main'], f'<main id="main" class="lp-main" data-island-label="{p["label"]}">\n' + p['main'], 1)
        s = s.replace('\n<!-- @chrome foot -->', '\n</main>\n<!-- @chrome foot -->', 1)
    open(path, 'w', encoding='utf-8', newline='\n').write(s)
    return len(s)


print('css/upcore-chrome.css', chrome_css())
for p in PAGES:
    print(p['file'], run(p))
