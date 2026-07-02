"""
fix_cta_teal.py
Change every solid/filled primary CTA button from black (#0a0a0a) to brand teal (#0ABFCC).
Text: #070B10 (dark). Hover: #089AAA (var(--teal2)).
Does NOT touch ghost/outline buttons, footers, nav, or non-button dark elements.
"""
import os, glob

base = r'C:\Users\saswa\Desktop\Upcore Website\upcore-website'

# ─────────────────────────────────────────────────────────────────────────────
# Helper: ordered list of (old, new) pairs applied to every file in the glob
# ─────────────────────────────────────────────────────────────────────────────

# ── .btn-fill variants (main site: index, about, platform, sdlc-agent,
#    ai-engineering-governance, insights/index, industries/index) ──────────────
BTN_FILL = [
    # spaced format (index, sdlc-agent, ai-engineering-governance)
    ('background:#0a0a0a; color:#ffffff; }',
     'background:#0ABFCC; color:#070B10; }'),
    ('background:#222222; transform:translateY(-1px); }',
     'background:#089AAA; transform:translateY(-1px); }'),
    # condensed with trailing semicolon (about)
    ('background:#0a0a0a;color:#ffffff;font-weight:600;}',
     'background:#0ABFCC;color:#070B10;font-weight:600;}'),
    ('background:#222222;transform:translateY(-1px);}',
     'background:#089AAA;transform:translateY(-1px);}'),
    # condensed without trailing semicolon (platform)
    ('background:#0a0a0a;color:#ffffff;font-weight:600}',
     'background:#0ABFCC;color:#070B10;font-weight:600}'),
    ('background:#222222;transform:translateY(-1px)}',
     'background:#089AAA;transform:translateY(-1px)}'),
    # industries/index plain (no font-weight)
    ('background:#0a0a0a;color:#ffffff;}',
     'background:#0ABFCC;color:#070B10;}'),
    # insights/index spaced with 8 spaces indent
    ('        .btn-fill { background:#0a0a0a; color:#ffffff; }',
     '        .btn-fill { background:#0ABFCC; color:#070B10; }'),
    ('        .btn-fill:hover { background:#222222; transform:translateY(-1px); }',
     '        .btn-fill:hover { background:#089AAA; transform:translateY(-1px); }'),
]

# ── .btn-primary (industries/index.html only) ─────────────────────────────────
BTN_PRIMARY_IND = [
    ('background:#0a0a0a;color:#ffffff;font-family:var(--ff);font-size:14px;font-weight:600;padding:12px 28px;border-radius:9999px;transition:background .2s,transform .2s;}',
     'background:#0ABFCC;color:#070B10;font-family:var(--ff);font-size:14px;font-weight:600;padding:12px 28px;border-radius:9999px;transition:background .2s,transform .2s;}'),
    ('background:#222222;transform:translateY(-1px);}',
     'background:#089AAA;transform:translateY(-1px);}'),
]

# ── .btn-p (kw/, platform/, learn/, compare/, solutions/, industries/tech-sdlc,
#    industries/compliance-governance) ─────────────────────────────────────────
BTN_P = [
    ('background:#0a0a0a;color:#ffffff;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;transition:background .2s,transform .2s;}',
     'background:#0ABFCC;color:#070B10;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;transition:background .2s,transform .2s;}'),
    # color:#fff variant (tech-sdlc, compliance-governance)
    ('background:#0a0a0a;color:#fff;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;transition:background .2s,transform .2s;}',
     'background:#0ABFCC;color:#070B10;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;transition:background .2s,transform .2s;}'),
    ('background:#222222;transform:translateY(-1px);}',
     'background:#089AAA;transform:translateY(-1px);}'),
]

# ── .btn-cta (12 standard industry pages, minified) ───────────────────────────
BTN_CTA = [
    ('background:#0a0a0a;color:#fff;font-family:var(--ff);font-size:15px;font-weight:600;padding:12px 26px;border-radius:9999px;transition:background .2s,transform .2s;}',
     'background:#0ABFCC;color:#070B10;font-family:var(--ff);font-size:15px;font-weight:600;padding:12px 26px;border-radius:9999px;transition:background .2s,transform .2s;}'),
    ('background:#222222;transform:translateY(-1px);}',
     'background:#089AAA;transform:translateY(-1px);}'),
]

# ── .article-cta .btn-cta (insights article pages, formatted) ─────────────────
ART_BTN_CTA = [
    ('  background: #0a0a0a; color: #fff; font-family: var(--ff);',
     '  background: #0ABFCC; color: #070B10; font-family: var(--ff);'),
    ('.article-cta .btn-cta:hover { background: #333; transform: translateY(-1px); }',
     '.article-cta .btn-cta:hover { background: #089AAA; transform: translateY(-1px); }'),
]

# ── .toc-cta (insights article sidebar CTA) ───────────────────────────────────
TOC_CTA = [
    ('  display:block; padding:11px 14px; background:#0a0a0a; color:#ffffff;\n  font-size:12.5px; font-weight:700; text-decoration:none;\n  border-radius:8px;',
     '  display:block; padding:11px 14px; background:#0ABFCC; color:#070B10;\n  font-size:12.5px; font-weight:700; text-decoration:none;\n  border-radius:9999px;'),
    ('.toc-cta:hover { background:#222222; }',
     '.toc-cta:hover { background:#089AAA; }'),
]

# ── .cta-section a (insights article bottom CTA) ──────────────────────────────
CTA_SECTION_A = [
    ('  display:inline-block; background:#0a0a0a; color:#ffffff;',
     '  display:inline-block; background:#0ABFCC; color:#070B10;'),
    ('.cta-section a:hover { background:#222222; transform:translateY(-1px); }',
     '.cta-section a:hover { background:#089AAA; transform:translateY(-1px); }'),
]

# ─────────────────────────────────────────────────────────────────────────────
# File groups → which replacement sets to apply
# ─────────────────────────────────────────────────────────────────────────────
GROUPS = [
    # Root-level flagship pages
    ([os.path.join(base, f) for f in [
        'index.html', 'about.html', 'platform.html', 'sdlc-agent.html',
        'ai-engineering-governance.html', 'assessment.html', 'contact.html',
    ]], BTN_FILL),

    # Industries hub index (has both btn-fill and btn-primary)
    ([os.path.join(base, 'industries', 'index.html')], BTN_FILL + BTN_PRIMARY_IND),

    # Insights hub index
    ([os.path.join(base, 'insights', 'index.html')], BTN_FILL),

    # kw/, platform/, learn/, compare/, solutions/ — use .btn-p
    (glob.glob(os.path.join(base, 'kw', '*.html')) +
     glob.glob(os.path.join(base, 'platform', '*.html')) +
     glob.glob(os.path.join(base, 'learn', '*.html')) +
     glob.glob(os.path.join(base, 'compare', '*.html')) +
     glob.glob(os.path.join(base, 'solutions', '*.html')),
     BTN_P),

    # 12 standard industry pages — use .btn-cta
    (glob.glob(os.path.join(base, 'industries', '*.html')), BTN_CTA + BTN_P),

    # Insights articles — .article-cta, .toc-cta, .cta-section a
    (glob.glob(os.path.join(base, 'insights', '*.html')), ART_BTN_CTA + TOC_CTA + CTA_SECTION_A),
]

changed, unchanged = [], []

for files, pairs in GROUPS:
    for filepath in sorted(set(files)):  # dedup in case of overlap
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()
        new_content = content
        for old, new in pairs:
            new_content = new_content.replace(old, new)
        relpath = os.path.relpath(filepath, base)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            changed.append(relpath)
        else:
            unchanged.append(relpath)

# Deduplicate (files appear in multiple groups may be counted twice)
changed = sorted(set(changed))
unchanged = [f for f in sorted(set(unchanged)) if f not in changed]

print(f'CHANGED ({len(changed)} files):')
for f in changed:
    print(f'   + {f}')
print(f'\nUNCHANGED ({len(unchanged)} files):')
for f in unchanged:
    print(f'   - {f}')
