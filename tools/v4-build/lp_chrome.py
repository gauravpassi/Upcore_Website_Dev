"""Site chrome for the two self-assessment landing pages (2026-10-07): /lp/governance-index and
/lp/ai-maturity-index. Their quiz (lp/lead-magnet-engine.js + the inline NICHE_CONFIG), the inline
quiz styles and their direct gtag.js tracking stay hand-maintained in the HTML; this script owns
only the marked blocks, so the pages share the island nav, footer, Geist type and stylesheets with
the generated pages:
  <!-- @chrome head --> fonts + css/upcore-v4.css + css/upcore-v5.css (before the inline <style>)
  <!-- @chrome nav -->  skip link + chrome.nav() with the page's own CTA (no announcement bar)
  <!-- @chrome foot --> chrome.footer()
  <!-- @chrome js -->   js/upcore-v4.js + js/upcore-v5.js (no v4-analytics: these pages tag via gtag.js)
The first run also converted the inline quiz styles to the calm light theme (marker
"calm light theme" in the <style>); later runs only refresh the blocks.
Run from the repo root: python tools/v4-build/lp_chrome.py (build_all.py runs it)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C

PAGES = [('lp/governance-index.html', 'Governance Index', ('/assessment', 'Book a Governance Review', 'book-a-governance-review')),
         ('lp/ai-maturity-index.html', 'AI Maturity Index', ('/lp/maturity-review', 'Book an AI Strategy Review', 'book-an-ai-strategy-review'))]

HEAD = '''<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/upcore-v4.css?v={V}" />
<link rel="stylesheet" href="/css/upcore-v5.css?v={V}" />'''
JS = '''<script src="/js/upcore-v4.js?v={V}" defer></script>
<script src="/js/upcore-v5.js?v={V}" defer></script>'''

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


def run(fname, label, cta):
    p = os.path.join(C.ROOT, fname)
    s = open(p, encoding='utf-8-sig').read()
    href, text, slug = cta
    nav = C.nav('').replace(C.btn('nav', cls='btn btn--sm'),
                            f'<a class="btn btn--sm" href="{href}" data-gtm-cta="{slug}" data-gtm-cta-type="primary" data-gtm-cta-section="nav">{text} <span class="btn-ico">{C.ARROW}</span></a>')
    s = block(s, 'head', HEAD.replace('{V}', str(C.V)), find=r'<link href="https://fonts\.googleapis\.com/css2\?family=Space\+Grotesk[^>]*>')
    s = block(s, 'nav', '<a class="skip" href="#main">Skip to content</a>\n' + nav, find=r'<nav>\n  <div class="nav-logo">[\s\S]*?\n</nav>')
    s = block(s, 'foot', C.footer(), find=r'<footer>[\s\S]*?\n</footer>')
    s = block(s, 'js', JS.replace('{V}', str(C.V)), before='</body>')
    if '<main id="main"' not in s:
        s = s.replace('<div id="lm-root">', f'<main id="main" class="lp-main" data-island-label="{label}">\n<div id="lm-root">', 1)
        s = s.replace('\n<!-- @chrome foot -->', '\n</main>\n<!-- @chrome foot -->', 1)
    s = re.sub(r'<style>([\s\S]*?)</style>', lambda m: '<style>' + theme(m.group(1)) + '</style>', s, count=1)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return len(s)


for f, l, c in PAGES:
    print(f, run(f, l, c))
