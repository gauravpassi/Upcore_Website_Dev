"""
apply_design_system.py — Enforce upcore-design.md across all content pages.

Fixes:
  kw/ and learn/ pages (pg-* template):
    - .pg-badge:   border-radius 20px → 6px, neutral border
    - .pg-h1:      font-weight 800 → 700
    - .btn-p:      gradient fill → solid teal, border-radius 10px → 8px
    - .btn-o:      teal border/color → neutral
    - .pg-card:    border-radius 16px → 10px, hover no teal border
    - .stat-box:   border-radius 14px → 10px
    - .stat-num:   gradient text → solid var(--teal)
    - .pg-cta:     gradient bg + teal border → card bg, border-radius 24px → 10px
    - .tl-pill:    border-radius 20px → 6px
    - footer tagline: old → new

  industries/ pages (hub-* template):
    - .hub-eyebrow:      border-radius 100px → 6px, neutral border
    - .hub-status-live:  border-radius 100px → 6px
    - .hub-status-ready: border-radius 100px → 6px
    - .hub-hero h1:      font-weight 900 → 700
    - .hub-hero bg:      remove radial-gradient + grid overlay
    - .uc-card:          border-radius 20px → 10px, remove gradient top-bar ::before
    - .agent-pill-card:  border-radius 14px → 10px
    - .agent-tag:        border-radius 100px → 6px
    - .btn-cta:          gradient → solid teal, 100px → 8px, remove glow
    - .btn-ghost:        100px → 8px, teal → neutral
    - inline cta badge:  border-radius 100px → 6px

  All pages:
    - Remove teal box-shadow from any button/element
    - Footer tagline
    - Footer hover colors

Run from upcore-website/ directory.
"""
import re, glob, os

SKIP = {'index.html', 'ai-engineering-governance.html', 'sdlc-agent.html', 'platform.html', 'about.html'}
files = [f for f in sorted(glob.glob('**/*.html', recursive=True))
         if 'demos' not in f and os.path.basename(f) not in SKIP]

def fix(content):
    # ── Footer tagline ──────────────────────────────────────────────────────
    for old, new in [
        ('Your AI Implementation Partner.<br/>We build agents that run your business  -  and stay until they do.',
         'Govern Your AI. Then Build With It.<br/>Enterprise-grade governance and agents, built for your org.'),
        ('Your AI Implementation Partner.<br/>We build agents that run your business — and stay until they do.',
         'Govern Your AI. Then Build With It.<br/>Enterprise-grade governance and agents, built for your org.'),
        ('Your AI Partner. Not Just Another AI Tool.',
         'Govern Your AI. Then Build With It.'),
    ]:
        content = content.replace(old, new)

    # ── PG-TEMPLATE (kw/ learn/ compare/ solutions/ platform-sub/) ─────────

    # pg-badge: 20px → 6px, teal border → subtle, font-size 12px → 11px
    content = content.replace(
        '.pg-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.1);border:1px solid rgba(10,191,204,.25);color:#0abfcc;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;margin-bottom:24px;letter-spacing:.5px;text-transform:uppercase;}',
        '.pg-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.08);border:1px solid rgba(10,191,204,.18);color:var(--teal);font-size:11px;font-weight:700;padding:4px 12px;border-radius:6px;margin-bottom:24px;letter-spacing:2px;text-transform:uppercase;}'
    )

    # pg-h1: font-weight 800 → 700
    content = content.replace(
        '.pg-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:800;line-height:1.2;margin-bottom:20px;}',
        '.pg-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:700;line-height:1.2;margin-bottom:20px;}'
    )

    # btn-p: gradient fill → solid teal, 10px → 8px
    content = content.replace(
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:var(--grad);color:#07101e;font-weight:700;padding:14px 28px;border-radius:10px;font-size:15px;transition:opacity .2s,transform .2s;}',
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;font-weight:700;padding:13px 28px;border-radius:8px;font-size:15px;transition:background .2s,transform .2s;}'
    )
    content = content.replace(
        '.btn-p:hover{opacity:.9;transform:translateY(-1px);}',
        '.btn-p:hover{background:var(--teal2);transform:translateY(-1px);}'
    )

    # btn-o: teal border/color → neutral
    content = content.replace(
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1.5px solid rgba(10,191,204,.4);color:var(--teal);padding:14px 28px;border-radius:10px;font-size:15px;transition:border-color .2s,background .2s;}',
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bh);color:var(--txt);padding:13px 28px;border-radius:8px;font-size:15px;transition:border-color .2s,background .2s;}'
    )
    content = content.replace(
        '.btn-o:hover{border-color:var(--teal);background:rgba(10,191,204,.06);}',
        '.btn-o:hover{border-color:rgba(255,255,255,.25);background:var(--glow);}'
    )

    # pg-card: 16px → 10px, hover teal border → neutral
    content = content.replace(
        '.pg-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px;transition:border-color .2s,transform .2s;}',
        '.pg-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:28px;transition:border-color .2s;}'
    )
    content = content.replace(
        '.pg-card:hover{border-color:rgba(10,191,204,.3);transform:translateY(-2px);}',
        '.pg-card:hover{border-color:var(--bh);}'
    )

    # stat-box: 14px → 10px
    content = content.replace(
        '.stat-box{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;text-align:center;}',
        '.stat-box{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:24px;text-align:center;}'
    )

    # stat-num: gradient text → solid teal
    content = content.replace(
        '.stat-num{font-size:2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}',
        '.stat-num{font-size:2rem;font-weight:800;color:var(--teal);}'
    )

    # pg-cta: gradient bg + teal border → card bg, 24px → 10px
    content = content.replace(
        '.pg-cta{background:linear-gradient(135deg,rgba(8,145,178,.12),rgba(61,221,196,.07));border:1px solid rgba(10,191,204,.2);border-radius:24px;padding:64px 48px;text-align:center;margin:0 0 64px;}',
        '.pg-cta{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:64px 48px;text-align:center;margin:0 0 64px;}'
    )
    content = content.replace(
        '.pg-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:800;margin-bottom:16px;}',
        '.pg-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:700;margin-bottom:16px;}'
    )

    # tl-pill: 20px → 6px
    content = content.replace(
        '.tl-pill{background:rgba(10,191,204,.1);color:var(--teal);font-size:.72rem;font-weight:600;padding:4px 10px;border-radius:20px;}',
        '.tl-pill{background:rgba(10,191,204,.08);color:var(--teal);font-size:.72rem;font-weight:600;padding:4px 10px;border-radius:6px;}'
    )

    # ── HUB-TEMPLATE (industries/) ──────────────────────────────────────────

    # hub-hero background: remove radial-gradient and grid overlay
    content = content.replace(
        '.hub-hero{padding:80px 48px 64px;background:radial-gradient(ellipse 80% 55% at 30% 0%,rgba(10,191,204,.08),transparent 65%),var(--bg);position:relative;overflow:hidden;}',
        '.hub-hero{padding:80px 48px 64px;background:var(--bg);}'
    )
    content = content.replace(
        ".hub-hero::before{content:'';position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(rgba(10,191,204,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(10,191,204,.03) 1px,transparent 1px);background-size:60px 60px;}",
        ''
    )

    # hub-eyebrow: 100px → 6px
    content = content.replace(
        '.hub-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.1);border:1px solid var(--border);border-radius:100px;padding:6px 14px;margin-bottom:16px;}',
        '.hub-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.08);border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:4px 12px;margin-bottom:16px;}'
    )

    # hub-status-live: 100px → 6px
    content = content.replace(
        '.hub-status-live{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:#4ade80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2);border-radius:100px;padding:5px 14px;margin-bottom:20px;}',
        '.hub-status-live{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:#4ade80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2);border-radius:6px;padding:4px 12px;margin-bottom:20px;}'
    )

    # hub-status-ready: 100px → 6px
    content = content.replace(
        '.hub-status-ready{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:var(--teal);background:rgba(10,191,204,.08);border:1px solid var(--border);border-radius:100px;padding:5px 14px;margin-bottom:20px;}',
        '.hub-status-ready{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;color:var(--teal);background:rgba(10,191,204,.08);border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:4px 12px;margin-bottom:20px;}'
    )

    # hub-hero h1: 900 → 700
    content = content.replace(
        '.hub-hero h1{font-size:clamp(28px,4vw,48px);font-weight:900;letter-spacing:-2px;line-height:1.1;margin-bottom:16px;}',
        '.hub-hero h1{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-1px;line-height:1.15;margin-bottom:16px;}'
    )

    # uc-card: 20px → 10px, remove gradient top-bar, add left border accent
    content = content.replace(
        '.uc-card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:36px;position:relative;overflow:hidden;}',
        '.uc-card{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--teal);border-radius:10px;padding:32px;}'
    )
    # Remove gradient top-bar ::before
    content = content.replace(
        ".uc-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--grad);}",
        ''
    )

    # agent-pill-card: 14px → 10px
    content = content.replace(
        '.agent-pill-card{background:rgba(10,191,204,.04);border:1px solid var(--border);border-radius:14px;padding:20px 24px;}',
        '.agent-pill-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px 24px;transition:border-color .2s;}'
    )

    # agent-tag: 100px → 6px, mint → teal
    content = content.replace(
        '.agent-tag{display:inline-flex;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--mint);background:rgba(61,221,196,.08);border:1px solid rgba(61,221,196,.2);border-radius:100px;padding:3px 10px;margin-bottom:10px;}',
        '.agent-tag{display:inline-flex;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.08);border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:3px 10px;margin-bottom:10px;}'
    )

    # btn-cta: gradient → solid teal, 100px → 8px, large padding → standard
    content = content.replace(
        '.btn-cta{display:inline-flex;align-items:center;gap:10px;background:var(--grad);color:#07101e;font-family:var(--ff);font-size:15px;font-weight:700;padding:16px 36px;border-radius:100px;transition:all .2s;}',
        '.btn-cta{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;font-family:var(--ff);font-size:15px;font-weight:700;padding:13px 28px;border-radius:8px;transition:background .2s,transform .2s;}'
    )
    content = content.replace(
        '.btn-cta:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(10,191,204,.4);}',
        '.btn-cta:hover{background:var(--teal2);transform:translateY(-1px);}'
    )

    # btn-ghost on industry: 100px → 8px, teal color → txt, margin-left stays
    content = content.replace(
        '.btn-ghost{display:inline-flex;align-items:center;gap:10px;color:var(--teal);font-family:var(--ff);font-size:14px;font-weight:600;padding:14px 28px;border-radius:100px;border:1px solid var(--border);transition:all .2s;margin-left:16px;}',
        '.btn-ghost{display:inline-flex;align-items:center;gap:8px;color:var(--txt);font-family:var(--ff);font-size:14px;font-weight:600;padding:13px 28px;border-radius:8px;border:1px solid var(--bh);transition:border-color .2s,background .2s;margin-left:16px;}'
    )
    content = content.replace(
        '.btn-ghost:hover{border-color:var(--teal);background:rgba(10,191,204,.05);}',
        '.btn-ghost:hover{border-color:rgba(255,255,255,.25);background:var(--glow);}'
    )

    # ── section-title on industry pages: 800 → 700 ─────────────────────────
    content = content.replace(
        '.section-title{font-size:clamp(22px,3vw,32px);font-weight:800;letter-spacing:-1px;margin-bottom:40px;}',
        '.section-title{font-size:clamp(22px,3vw,32px);font-weight:700;letter-spacing:-.5px;margin-bottom:40px;}'
    )

    # ── ALL PAGES: Remove teal box-shadows ─────────────────────────────────
    content = re.sub(r';?box-shadow:0 \d+px \d+px rgba\(10,191,204,[^)]+\)', '', content)
    content = re.sub(r';?box-shadow:0 \d+px \d+px rgba\(0,212,180,[^)]+\)', '', content)

    # ── ALL PAGES: Inline cta badge in industry pages with border-radius:100px ──
    # Match inline style attributes containing border-radius:100px (in CTA section div)
    content = re.sub(
        r'(style="[^"]*display:inline-flex[^"]*?)border-radius:100px([^"]*")',
        r'\g<1>border-radius:6px\2',
        content
    )

    # ── ALL PAGES: Form submit button cleanup ───────────────────────────────
    # assessment.html form submit glow
    content = content.replace(
        'box-shadow:0 4px 28px rgba(10,191,204,.28)',
        ''
    )

    return content

updated = 0
unchanged = 0

for fp in files:
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    orig = content
    content = fix(content)
    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'  updated: {fp}')
    else:
        unchanged += 1
        print(f'  no-op:   {fp}')

print(f'\n{"="*50}')
print(f'Updated:   {updated}')
print(f'Unchanged: {unchanged}')
print(f'Total:     {updated + unchanged}')
