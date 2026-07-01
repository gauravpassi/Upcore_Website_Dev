"""
Propagate new :root tokens, nav CSS, and nav HTML to all HTML pages.
Run from the upcore-website directory.

Pages already manually redesigned are in SKIP — they won't be touched.
"""
import re, glob, os, sys

SKIP = {
    'index.html',
    'ai-engineering-governance.html',
    'sdlc-agent.html',
    'platform.html',
    'about.html',
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

NEW_NAV_CSS = """/* ── Navigation ──────────────────────────────────────────────── */
nav{width:100%;background:rgba(7,11,16,0.97);border-bottom:1px solid var(--border);padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:99;}
.nav-logo a{display:flex;align-items:center;}
.nav-logo img{height:44px;width:auto;}
.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}
.nav-links a{padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;color:var(--txt2);transition:color .2s,background .2s;text-decoration:none;}
.nav-links a:hover{color:var(--txt);background:var(--glow);}
.nav-links a.active{color:var(--teal);}
.nav-cta{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;font-size:14px;font-weight:700;padding:10px 22px;border-radius:8px;text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}
.nav-cta:hover{background:var(--teal2);transform:translateY(-1px);}
@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}"""

NEW_NAV_HTML = """<nav>
  <div class="nav-logo"><a href="/"><img src="/upcore-logo.png" alt="Upcore Technologies"/></a></div>
  <ul class="nav-links">
    <li><a href="/ai-engineering-governance">AI Governance</a></li>
    <li><a href="/platform">Products</a></li>
    <li><a href="/industries">Industries</a></li>
    <li><a href="/insights">Resources</a></li>
    <li><a href="/about">About</a></li>
  </ul>
  <a href="/assessment" class="nav-cta">Book a Call</a>
</nav>"""

# ─── active-class map ─────────────────────────────────────────────────────────
# Map path prefixes → which nav link should get class="active"
ACTIVE_MAP = [
    ('/ai-engineering-governance', 'AI Governance'),
    ('/platform',                  'Products'),
    ('/industries',                'Industries'),
    ('/insights',                  'Resources'),
    ('/about',                     'About'),
    ('/kw/',                       'Resources'),
]

def nav_with_active(filepath):
    """Return nav HTML with the correct active class for this file's URL."""
    # Convert Windows path to URL-like slug
    path = filepath.replace('\\', '/')
    # Remove trailing index.html or .html
    path = path.replace('.html', '').replace('/index', '')
    if not path.startswith('/'):
        path = '/' + path

    for prefix, label in ACTIVE_MAP:
        if path.startswith(prefix.rstrip('/')):
            # Inject active class on the matching <a>
            return NEW_NAV_HTML.replace(
                f'>{label}</a>',
                f' class="active">{label}</a>'
            )
    return NEW_NAV_HTML


def replace_root(content):
    """Replace the :root { ... } block."""
    return re.sub(r':root\s*\{[^}]+\}', NEW_ROOT, content, count=1)


def replace_nav_css(content):
    """
    Replace the nav CSS block.
    Strategy: find the nav CSS comment (or just 'nav{width:100%')
    through to the mobile media query closing '}'.
    Uses line-by-line scanning for robustness.
    """
    lines = content.split('\n')
    start = None
    end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Look for nav CSS comment or start of nav rule
        if start is None:
            if '/* ── Navigation' in stripped or stripped.startswith('nav{width:100%'):
                start = i
        else:
            # Look for the closing mobile media query
            if 'nav-links' in stripped and 'display:none' in stripped:
                end = i
                break

    if start is None or end is None:
        return content, False  # pattern not found

    new_lines = lines[:start] + [NEW_NAV_CSS] + lines[end + 1:]
    return '\n'.join(new_lines), True


def replace_nav_html(content, filepath):
    """Replace the <nav>...</nav> HTML block."""
    nav_html = nav_with_active(filepath)
    new_content = re.sub(r'<nav>.*?</nav>', nav_html, content, count=1, flags=re.DOTALL)
    return new_content


# ─── main ─────────────────────────────────────────────────────────────────────
files = [f for f in glob.glob('**/*.html', recursive=True) if 'demos' not in f]

updated = 0
skipped_manual = 0
skipped_no_match = 0

for filepath in sorted(files):
    basename = os.path.basename(filepath)

    if basename in SKIP:
        skipped_manual += 1
        continue

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # 1. Replace :root
    content = replace_root(content)

    # 2. Replace nav CSS
    content, css_found = replace_nav_css(content)

    # 3. Replace nav HTML
    content = replace_nav_html(content, filepath)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'  updated: {filepath}')
    else:
        skipped_no_match += 1
        print(f'  no-op:   {filepath}')

print(f'\n{"="*50}')
print(f'Updated:        {updated}')
print(f'Skipped (done): {skipped_manual}')
print(f'No-op:          {skipped_no_match}')
