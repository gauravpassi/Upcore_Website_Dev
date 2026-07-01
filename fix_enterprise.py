"""
Enterprise upgrade pass:
1. Dark nav across all 65 pages (logo now visible, enterprise authority)
2. Footer border fixes (var(--border) = light gray on dark bg = bad)
3. Better footer social/review button styling
"""
import glob, re

files = [f for f in glob.glob('**/*.html', recursive=True) if 'demos' not in f]

# ── NAV: exact match across all 65 pages ─────────────────────────────────────

OLD_NAV_LINES = [
    'nav{width:100%;background:#ffffff;border-bottom:1px solid #e5e7eb;padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:99;}',
    '.nav-logo a{display:flex;align-items:center;}',
    '.nav-logo img{height:44px;width:auto;}',
    '.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}',
    '.nav-links a{padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;color:#45515e;transition:color .2s,background .2s;text-decoration:none;}',
    '.nav-links a:hover{color:#0a0a0a;background:rgba(0,0,0,.04);}',
    '.nav-links a.active{color:#0a0a0a;font-weight:600;}',
    '.nav-cta{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#ffffff;font-size:14px;font-weight:600;padding:10px 22px;border-radius:9999px;text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}',
    '.nav-cta:hover{background:#222222;transform:translateY(-1px);}',
    '@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}',
]

NEW_NAV_LINES = [
    'nav{width:100%;background:#0a0a0a;border-bottom:1px solid rgba(255,255,255,.08);padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:99;}',
    '.nav-logo a{display:flex;align-items:center;}',
    '.nav-logo img{height:40px;width:auto;}',
    '.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}',
    '.nav-links a{padding:8px 16px;border-radius:6px;font-size:14px;font-weight:500;color:rgba(255,255,255,.65);transition:color .2s,background .2s;text-decoration:none;}',
    '.nav-links a:hover{color:#ffffff;background:rgba(255,255,255,.07);}',
    '.nav-links a.active{color:#ffffff;font-weight:600;}',
    '.nav-cta{display:inline-flex;align-items:center;gap:8px;background:#ffffff;color:#0a0a0a;font-size:14px;font-weight:600;padding:10px 22px;border-radius:9999px;text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}',
    '.nav-cta:hover{background:#f2f2f2;transform:translateY(-1px);}',
    '@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}',
]

OLD_NAV = '\n'.join(OLD_NAV_LINES)
NEW_NAV = '\n'.join(NEW_NAV_LINES)

nav_updated = 0
footer_updated = 0
no_nav_match = []

for f in sorted(files):
    content = orig = open(f, encoding='utf-8').read()

    # ── NAV CSS replacement ───────────────────────────────────────────────────
    if OLD_NAV in content:
        content = content.replace(OLD_NAV, NEW_NAV)
        nav_updated += 1
    else:
        no_nav_match.append(f)

    # ── FOOTER border fixes: line-by-line ───────────────────────────────────
    # Process line by line to catch both single-line and multi-line CSS formats
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # footer-bottom: fix var(--border) → white-alpha
        if 'footer-bottom' in line and 'var(--border)' in line:
            line = line.replace('var(--border)', 'rgba(255,255,255,.09)')
        # footer-soc-btn: fix var(--border) → white-alpha
        elif 'footer-soc-btn' in line and 'var(--border)' in line:
            line = line.replace('var(--border)', 'rgba(255,255,255,.1)')
        # footer-review-btn: fix var(--border) → white-alpha
        elif 'footer-review-btn' in line and 'var(--border)' in line:
            line = line.replace('var(--border)', 'rgba(255,255,255,.1)')
        # footer-review-btn hover: fix var(--bh) → white-alpha
        elif 'footer-review-btn' in line and 'var(--bh)' in line:
            line = line.replace('var(--bh)', 'rgba(255,255,255,.22)')
        # Multi-line format: standalone border line inside footer CSS block
        # These appear as sub-lines of a .footer-* { ... } block
        # We handle them by checking if it's a border inside a footer context
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # ── FOOTER social button: fix multi-line format in index.html style ──────
    # index.html has multi-line .footer-soc-btn { ... border:1px solid var(--border) ... }
    # This might not have been caught by the line-by-line above if border is on its own line
    # within a .footer-soc-btn block. Let's do a regex pass for that case.
    # Pattern: inside .footer-soc-btn { ... } block, fix border lines
    # We use a regex that specifically targets the footer-soc-btn block
    content = re.sub(
        r'(\.footer-soc-btn\s*\{[^}]*?)border:\s*1px\s+solid\s+var\(--border\)',
        r'\1border:1px solid rgba(255,255,255,.1)',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'(\.footer-review-btn\s*\{[^}]*?)border:\s*1px\s+solid\s+var\(--border\)',
        r'\1border:1px solid rgba(255,255,255,.1)',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'(\.footer-review-btn\s*:\s*hover\s*\{[^}]*?)border-color:\s*var\(--bh\)',
        r'\1border-color:rgba(255,255,255,.22)',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'(\.footer-bottom\s*\{[^}]*?)border-top:\s*1px\s+solid\s+var\(--border\)',
        r'\1border-top:1px solid rgba(255,255,255,.09)',
        content, flags=re.DOTALL
    )

    if content != orig:
        open(f, 'w', encoding='utf-8').write(content)
        if content.replace(orig.replace(OLD_NAV, NEW_NAV), '') != orig.replace(OLD_NAV, NEW_NAV):
            footer_updated += 1

print(f'Nav updated:    {nav_updated}/65 pages')
print(f'No nav match:   {len(no_nav_match)} pages')
if no_nav_match:
    for f in no_nav_match: print(f'  MISSING: {f}')
print()
print('Footer border fixes applied.')

# Verify: no remaining light borders in dark footer context
border_issues = []
for f in files:
    content = open(f, encoding='utf-8').read()
    lines_c = content.split('\n')
    for i, line in enumerate(lines_c):
        if ('footer-bottom' in line or 'footer-soc-btn' in line or 'footer-review-btn' in line):
            if 'var(--border)' in line or 'var(--bh)' in line:
                border_issues.append(f'{f}:{i+1}')
if not border_issues:
    print('Footer border check: ALL CLEAR')
else:
    print('Footer border issues remaining:')
    for x in border_issues: print(f'  {x}')
