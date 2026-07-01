"""
Comprehensive fix pass — runs AFTER propagate_design.py.

Fixes found by audit:
  1. Footer: old tagline + #00d4b4 hover color (all pages)
  2. grad-text spans in H1/H2 (secondary pages)
  3. insights/ articles: no :root, stray .@media line, old hardcoded colors
  4. Button class cleanup: btn-primary → btn btn-fill; bare btn-ghost → btn btn-ghost
  5. Various old inline color tokens

Run from upcore-website/ directory.
"""
import re, glob, os

SKIP_ROOT = {  # already have correct :root from manual redesign
    'index.html','ai-engineering-governance.html',
    'sdlc-agent.html','platform.html','about.html',
}

NEW_ROOT = """:root {
  --bg:     #070B10;
  --bg2:    #0C1018;
  --bg3:    #111722;
  --card:   #171E2B;
  --card2:  #1D2537;
  --teal:   #0ABFCC;
  --teal2:  #089AAA;
  --mint:   #0ABFCC;
  --amber:  #C68B0A;
  --amber2: #F0A500;
  --green:  #22C55E;
  --red:    #EF4444;
  --txt:    #E2E8F0;
  --txt2:   #64748B;
  --txt3:   #374151;
  --border: rgba(255,255,255,0.07);
  --bh:     rgba(255,255,255,0.14);
  --glow:   rgba(255,255,255,0.04);
  --grad:   linear-gradient(135deg,#0891b2,#0ABFCC);
  --grad-amber: linear-gradient(135deg,#C68B0A,#F0A500);
  --ff:     "Poppins", sans-serif;
  --nav-h:  64px;
  --max:    1240px;
}"""

ARTICLE_BASE_CSS = """/* ── Article base styles (charcoal design system) ─────────────── */
*,*::before,*::after { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Poppins', sans-serif; background: var(--bg); color: var(--txt2); line-height: 1.7; }
a { text-decoration: none; color: inherit; }
.page-container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
.logo img { height: 28px; width: auto; }
/* Article Header */
.article-header { padding: 40px 0; border-bottom: 1px solid var(--border); }
.breadcrumb { font-size: 13px; color: var(--txt3); margin-bottom: 16px; }
.breadcrumb a { color: var(--teal); text-decoration: none; }
.category-badge {
  display: inline-block; background: rgba(10,191,204,0.10);
  color: var(--teal); padding: 4px 12px; border-radius: 6px;
  font-size: 12px; font-weight: 600; margin-bottom: 20px;
  text-transform: uppercase; letter-spacing: 0.5px;
}
h1 { font-size: clamp(28px,5vw,42px); font-weight: 300; color: var(--txt); margin-bottom: 16px; line-height: 1.25; }
h1 strong { font-weight: 700; }
.byline { font-size: 13px; color: var(--txt3); margin-bottom: 20px; }
.byline strong { color: var(--txt2); }
/* Article Body */
.article-body { max-width: 760px; margin: 40px auto; padding: 0 20px; }
h2 { font-size: clamp(20px,3vw,28px); font-weight: 700; color: var(--txt); margin-top: 40px; margin-bottom: 16px; line-height: 1.3; }
h3 { font-size: 18px; font-weight: 600; color: var(--txt); margin-top: 28px; margin-bottom: 10px; }
p { margin-bottom: 18px; }
ul, ol { margin-bottom: 18px; padding-left: 24px; }
li { margin-bottom: 6px; }
/* Key Takeaway Box */
.key-takeaway {
  background: var(--card); border-left: 3px solid var(--teal);
  padding: 24px; margin: 40px 0; border-radius: 0 8px 8px 0;
  font-size: 16px; color: var(--txt); font-style: italic;
}
.key-takeaway strong { color: var(--teal); font-style: normal; }
/* Use Cases / Agent Cards */
.use-cases-section { max-width: 760px; margin: 60px auto; padding: 0 20px; }
.use-cases-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 20px; margin-top: 30px; }
.agent-card {
  background: var(--card); border: 1px solid var(--border);
  padding: 24px; border-radius: 10px; text-align: center;
  transition: border-color .2s; text-decoration: none; color: inherit;
}
.agent-card:hover { border-color: var(--bh); }
.agent-card h3 { font-size: 15px; color: var(--teal); margin: 10px 0 6px; }
.agent-card p { font-size: 13px; color: var(--txt2); margin: 0; }
.agent-icon { font-size: 28px; }
/* Article CTA */
.article-cta {
  background: var(--card2); border: 1px solid var(--border);
  border-radius: 10px; padding: 36px; text-align: center; margin: 48px auto;
  max-width: 760px;
}
.article-cta h2 { font-size: 22px; color: var(--txt); margin-bottom: 10px; margin-top: 0; }
.article-cta p { color: var(--txt2); margin-bottom: 24px; }
.article-cta .btn-cta {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--teal); color: #070B10; font-family: 'Poppins',sans-serif;
  font-size: 15px; font-weight: 700; padding: 14px 32px;
  border-radius: 8px; transition: background .2s, transform .2s;
  text-decoration: none;
}
.article-cta .btn-cta:hover { background: var(--teal2); transform: translateY(-1px); }
/* Stats / highlight boxes */
.stat-box, .highlight-box {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 24px; margin: 20px 0;
}
.stat-number { font-size: 36px; font-weight: 800; color: var(--teal); }
/* Related articles */
.related-section { max-width: 760px; margin: 60px auto 40px; padding: 0 20px; }
.related-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(200px,1fr)); gap: 16px; margin-top: 20px; }
.related-card {
  background: var(--card); border: 1px solid var(--border);
  padding: 20px; border-radius: 10px; transition: border-color .2s; text-decoration: none; color: inherit;
}
.related-card:hover { border-color: var(--bh); }
.related-card h4 { font-size: 14px; font-weight: 600; color: var(--txt); margin-bottom: 6px; }
.related-card p { font-size: 12px; color: var(--txt2); margin: 0; }
/* Responsive */
@media(max-width:768px) {
  .article-body, .use-cases-section, .related-section, .article-cta { padding: 0 16px; }
  h1 { font-size: 26px; }
}"""

files = [f for f in sorted(glob.glob('**/*.html', recursive=True)) if 'demos' not in f]
updated = 0
unchanged = 0

for fp in files:
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    orig = content
    basename = os.path.basename(fp)
    is_insight_article = (
        fp.startswith('insights\\') and
        basename != 'index.html' and
        ':root' not in content
    )

    # ── 1. Footer tagline ────────────────────────────────────────────────
    content = content.replace(
        'Your AI Partner. Not Just Another AI Tool.<br/>We build agents that actually run your business.',
        'Govern Your AI. Then Build With It.<br/>Enterprise-grade governance and agents, built for your org.'
    )
    content = content.replace(
        "Your AI Partner. Not Just Another AI Tool.",
        "Govern Your AI. Then Build With It."
    )

    # ── 2. Footer hover colors ────────────────────────────────────────────
    content = content.replace(
        '.footer-soc-btn:hover{background:rgba(0,212,180,0.12);border-color:rgba(0,212,180,0.35);color:#00d4b4;}',
        '.footer-soc-btn:hover{background:rgba(10,191,204,0.10);border-color:rgba(10,191,204,0.28);color:var(--teal);}'
    )
    content = content.replace(
        '.footer-links a:hover{color:#00d4b4;}',
        '.footer-links a:hover{color:var(--teal);}'
    )
    content = content.replace(
        '.footer-copy a:hover{color:#00d4b4;}',
        '.footer-copy a:hover{color:var(--teal);}'
    )

    # ── 3. grad-text spans inside heading elements ────────────────────────
    # Replace <span class="grad-text">X</span> within H1/H2 with <strong>X</strong>
    def replace_grad_in_h(m):
        heading = m.group(0)
        heading = re.sub(r'<span class="grad-text">(.*?)</span>', r'<strong>\1</strong>', heading, flags=re.DOTALL)
        return heading
    content = re.sub(r'<h[12][^>]*>.*?</h[12]>', replace_grad_in_h, content, flags=re.DOTALL)

    # ── 4. Button classes ─────────────────────────────────────────────────
    # a. class="btn-primary" and class="btn-hero-primary" → class="btn btn-fill"
    content = re.sub(r'class="btn-primary"', 'class="btn btn-fill"', content)
    content = re.sub(r'class="btn-hero-primary"', 'class="btn btn-fill"', content)
    content = re.sub(r'class="btn-demo-primary"', 'class="btn btn-fill"', content)
    content = re.sub(r'class="btn-ind-pri"', 'class="btn btn-fill"', content)
    content = re.sub(r'class="btn-outline"', 'class="btn btn-ghost"', content)

    # b. bare class="btn-ghost" → class="btn btn-ghost"
    # Only match if it's NOT already "btn btn-ghost"
    content = re.sub(
        r'class="(?!btn )([^"]*\b)btn-ghost([^"]*)"',
        lambda m: f'class="btn {m.group(1)}btn-ghost{m.group(2)}"'.replace('class="btn btn-ghost"','class="btn btn-ghost"'),
        content
    )
    # Cleaner: just fix the specific pattern "class="btn-ghost""
    content = re.sub(r'\bclass="btn-ghost"', 'class="btn btn-ghost"', content)
    # Remove double spaces that might arise
    content = content.replace('class="btn  btn-ghost"', 'class="btn btn-ghost"')

    # ── 5. insights/ articles: inject :root + replace article CSS ────────
    if is_insight_article:
        # Remove stray .@media line
        content = re.sub(r'\n\.@media[^\n]*\n', '\n', content)

        # Inject :root + article base CSS right after the nav CSS block
        # (after the line that ends the nav mobile media query)
        nav_css_end = '@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}'
        if nav_css_end in content and ':root' not in content:
            content = content.replace(
                nav_css_end,
                nav_css_end + '\n\n' + NEW_ROOT + '\n\n' + ARTICLE_BASE_CSS
            )

        # Now replace old hardcoded body rule
        content = re.sub(
            r'body\s*\{\s*\n[^}]*font-family[^}]*background-color[^}]*\n[^}]*color[^}]*\n[^}]*line-height[^}]*\n[^}]*\}',
            '/* body styled by design system tokens above */',
            content, flags=re.DOTALL
        )
        # Simpler fallback: replace the specific hardcoded body values
        content = re.sub(
            r'(body\s*\{[^}]*background-color\s*:)\s*#07101e',
            r'\1 var(--bg)',
            content
        )
        content = re.sub(
            r'(body\s*\{[^}]*\bcolor\s*:)\s*#8bbed4',
            r'\1 var(--txt2)',
            content
        )

    # ── 6. insights/index.html: fix grad-text in h2 ──────────────────────
    # (already handled by step 3 above)

    # ── 7. Remove any lingering stray .@media line (non-insights too) ────
    content = re.sub(r'\n\.@media[^\n]+\n', '\n', content)

    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'  updated: {fp}')
    else:
        unchanged += 1

print(f'\n{"="*50}')
print(f'Updated:   {updated}')
print(f'Unchanged: {unchanged}')
print(f'Total:     {updated + unchanged}')
