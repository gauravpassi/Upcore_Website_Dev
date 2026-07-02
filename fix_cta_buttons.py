"""
fix_cta_buttons.py
Standardize all primary CTA buttons to black pill across the entire site.
Target: background:#0a0a0a · color:#fff · padding:12px 26px · border-radius:9999px · font-size:15px · font-weight:600
"""
import os, glob

base = r'C:\Users\saswa\Desktop\Upcore Website\upcore-website'

# ─────────────────────────────────────────────────
# Replacement pairs — (old, new)
# ─────────────────────────────────────────────────

# Group 1 – standard industry pages — minified .btn-cta rule
IND_CTA_OLD = '.btn-cta{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;font-family:var(--ff);font-size:15px;font-weight:700;padding:13px 28px;border-radius:8px;transition:background .2s,transform .2s;}'
IND_CTA_NEW = '.btn-cta{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#fff;font-family:var(--ff);font-size:15px;font-weight:600;padding:12px 26px;border-radius:9999px;transition:background .2s,transform .2s;}'

# Group 2 – insights article pages — formatted .article-cta .btn-cta inner properties
ART_INNER_OLD = '  background: var(--teal); color: #070B10; font-family: var(--ff);\n  font-size: 15px; font-weight: 700; padding: 14px 32px;\n  border-radius: 8px; transition: background .2s, transform .2s;'
ART_INNER_NEW = '  background: #0a0a0a; color: #fff; font-family: var(--ff);\n  font-size: 15px; font-weight: 600; padding: 12px 26px;\n  border-radius: 9999px; transition: background .2s, transform .2s;'

ART_HOVER_OLD = '.article-cta .btn-cta:hover { background: var(--teal2); transform: translateY(-1px); }'
ART_HOVER_NEW = '.article-cta .btn-cta:hover { background: #333; transform: translateY(-1px); }'

# Group 3 – tech-sdlc / compliance-governance — teal .btn-p
TEAL_BTNP_OLD = '.btn-p{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;font-weight:700;padding:13px 28px;border-radius:8px;font-size:15px;transition:background .2s,transform .2s;}'
TEAL_BTNP_NEW = '.btn-p{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#fff;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;transition:background .2s,transform .2s;}'

# Group 4 – kw/ and platform/ sub-pages — small .btn-p (correct color, wrong size)
SMALL_BTNP_OLD = 'background:#0a0a0a;color:#ffffff;font-weight:600;padding:11px 24px;border-radius:9999px;font-size:14px;'
SMALL_BTNP_NEW = 'background:#0a0a0a;color:#ffffff;font-weight:600;padding:12px 26px;border-radius:9999px;font-size:15px;'

# Group 5 – industry pages — .btn-ghost secondary (8px squircle → 9999px pill)
IND_GHOST_OLD = '.btn-ghost{display:inline-flex;align-items:center;gap:8px;color:var(--txt);font-family:var(--ff);font-size:14px;font-weight:600;padding:13px 28px;border-radius:8px;border:1px solid var(--bh);transition:border-color .2s,background .2s;margin-left:16px;}'
IND_GHOST_NEW = '.btn-ghost{display:inline-flex;align-items:center;gap:8px;color:var(--txt);font-family:var(--ff);font-size:14px;font-weight:600;padding:12px 26px;border-radius:9999px;border:1px solid var(--bh);transition:border-color .2s,background .2s;margin-left:16px;}'

REPLACEMENTS_BY_GLOB = {
    # learn/, compare/, solutions/ — still have old undersized .btn-p
    os.path.join(base, 'learn', '*.html'): [
        (SMALL_BTNP_OLD, SMALL_BTNP_NEW),
    ],
    os.path.join(base, 'compare', '*.html'): [
        (SMALL_BTNP_OLD, SMALL_BTNP_NEW),
    ],
    os.path.join(base, 'solutions', '*.html'): [
        (SMALL_BTNP_OLD, SMALL_BTNP_NEW),
    ],
    # industries — fix secondary .btn-ghost to pill to match primary
    os.path.join(base, 'industries', '*.html'): [
        (IND_GHOST_OLD, IND_GHOST_NEW),
    ],
}

changed, unchanged = [], []

for pattern, pairs in REPLACEMENTS_BY_GLOB.items():
    for filepath in sorted(glob.glob(pattern)):
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()
        new_content = content
        for old, new in pairs:
            new_content = new_content.replace(old, new)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            changed.append(os.path.relpath(filepath, base))
        else:
            unchanged.append(os.path.relpath(filepath, base))

print(f'\nCHANGED ({len(changed)} files):')
for f in changed:
    print(f'   + {f}')
print(f'\nUNCHANGED ({len(unchanged)} files):')
for f in unchanged:
    print(f'   - {f}')
