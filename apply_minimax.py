#!/usr/bin/env python3
"""
apply_minimax.py — Implements MiniMax design language across Upcore website.
Dark charcoal → white canvas  |  Teal/8px buttons → black 9999px pills
Poppins → DM Sans  |  Dark card surfaces → white + hairline borders
Dark footer kept: #0a0a0a (MiniMax footer-region pattern)
"""

import os, re

BASE = r"C:\Users\saswa\Desktop\Upcore Website\upcore-website"
SKIP_DIRS = {'demos', '.git', '__pycache__', 'node_modules'}

# Flagship pages — root-level only; compared against RELATIVE path so kw/index.html is not caught
FLAGSHIP_RELPATHS = {'index.html', 'ai-engineering-governance.html', 'sdlc-agent.html',
                     'platform.html', 'about.html'}
# Interactive/utility pages — get :root/font/nav/footer only
UTILITY = {'agent-builder.html', 'assessment.html', 'build-your-demo.html', 'contact.html'}

# ── New :root (MiniMax-adapted) ───────────────────────────────────────────────
NEW_ROOT = """:root {
  --bg:     #ffffff;
  --bg2:    #f7f8fa;
  --bg3:    #f2f3f5;
  --card:   #ffffff;
  --card2:  #f7f8fa;
  --teal:   #0ABFCC;
  --teal2:  #089AAA;
  --mint:   #0ABFCC;
  --amber:  #C68B0A;
  --amber2: #F0A500;
  --green:  #22C55E;
  --red:    #EF4444;
  --txt:    #0a0a0a;
  --txt2:   #45515e;
  --txt3:   #8e8e93;
  --ink:    #0a0a0a;
  --ink-press: #222222;
  --border: #e5e7eb;
  --bh:     #d1d5db;
  --glow:   rgba(0,0,0,0.04);
  --grad:   linear-gradient(135deg,#0891b2,#0ABFCC);
  --grad-amber: linear-gradient(135deg,#C68B0A,#F0A500);
  --ff:     "DM Sans", sans-serif;
  --nav-h:  64px;
  --max:    1240px;
}"""

# ── Canonical nav (MiniMax-style white + black pill CTA) ─────────────────────
OLD_NAV = (
    'nav{width:100%;background:rgba(7,11,16,0.97);border-bottom:1px solid var(--border);'
    'padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;'
    'position:sticky;top:0;z-index:99;}\n'
    '.nav-logo a{display:flex;align-items:center;}\n'
    '.nav-logo img{height:44px;width:auto;}\n'
    '.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}\n'
    '.nav-links a{padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;'
    'color:var(--txt2);transition:color .2s,background .2s;text-decoration:none;}\n'
    '.nav-links a:hover{color:var(--txt);background:var(--glow);}\n'
    '.nav-links a.active{color:var(--teal);}\n'
    '.nav-cta{display:inline-flex;align-items:center;gap:8px;background:var(--teal);'
    'color:#070B10;font-size:14px;font-weight:700;padding:10px 22px;border-radius:8px;'
    'text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}\n'
    '.nav-cta:hover{background:var(--teal2);transform:translateY(-1px);}\n'
    '@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}'
)
NEW_NAV = (
    'nav{width:100%;background:#ffffff;border-bottom:1px solid #e5e7eb;'
    'padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;'
    'position:sticky;top:0;z-index:99;}\n'
    '.nav-logo a{display:flex;align-items:center;}\n'
    '.nav-logo img{height:44px;width:auto;}\n'
    '.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}\n'
    '.nav-links a{padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;'
    'color:#45515e;transition:color .2s,background .2s;text-decoration:none;}\n'
    '.nav-links a:hover{color:#0a0a0a;background:rgba(0,0,0,.04);}\n'
    '.nav-links a.active{color:#0a0a0a;font-weight:600;}\n'
    '.nav-cta{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;'
    'color:#ffffff;font-size:14px;font-weight:600;padding:10px 22px;border-radius:9999px;'
    'text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}\n'
    '.nav-cta:hover{background:#222222;transform:translateY(-1px);}\n'
    '@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}'
)


def get_files():
    files = []
    for root, dirs, filenames in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))
    return sorted(files)


def replace_root(content):
    return re.sub(r':root\s*\{[^}]+\}', NEW_ROOT, content, count=1)


def replace_font(content):
    # Poppins → DM Sans
    for old in [
        'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap',
        'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&amp;display=swap',
    ]:
        content = content.replace(
            old,
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap'
        )
    return content


def replace_nav(content):
    if OLD_NAV in content:
        return content.replace(OLD_NAV, NEW_NAV)
    return content


def fix_footer(content):
    """Keep footer dark (MiniMax footer-region = #0a0a0a)."""
    # Footer background
    for old_bg in [
        'footer{background:var(--bg);border-top:1px solid var(--border);',
        'footer{background:var(--bg2);border-top:1px solid var(--border);',
    ]:
        content = content.replace(
            old_bg,
            'footer{background:#0a0a0a;border-top:1px solid rgba(255,255,255,.06);'
        )
    # Footer link text (--txt2 is now slate #45515e, too dark on black footer)
    content = content.replace(
        '.footer-links a{font-size:13px;color:var(--txt2);text-decoration:none;transition:color .15s;}',
        '.footer-links a{font-size:13px;color:rgba(255,255,255,.55);text-decoration:none;transition:color .15s;}'
    )
    # Some pages use slightly different footer link CSS
    content = content.replace(
        '.footer-links a{font-size:.875rem;color:var(--txt2);transition:color .2s;}',
        '.footer-links a{font-size:.875rem;color:rgba(255,255,255,.55);transition:color .2s;}'
    )
    # Footer tagline (--txt3 is now stone #8e8e93)
    content = content.replace(
        '.footer-tagline{font-size:13px;color:var(--txt3);line-height:1.7;margin-top:12px;max-width:220px;}',
        '.footer-tagline{font-size:13px;color:rgba(255,255,255,.4);line-height:1.7;margin-top:12px;max-width:220px;}'
    )
    content = content.replace(
        '.footer-tagline{font-size:.85rem;color:var(--txt3);line-height:1.6;margin-bottom:16px;}',
        '.footer-tagline{font-size:.85rem;color:rgba(255,255,255,.4);line-height:1.6;margin-bottom:16px;}'
    )
    # Footer copy
    content = content.replace(
        '.footer-copy{font-size:12px;color:var(--txt3);}',
        '.footer-copy{font-size:12px;color:rgba(255,255,255,.3);}'
    )
    content = content.replace(
        '.footer-copy a{color:var(--txt3);text-decoration:none;}',
        '.footer-copy a{color:rgba(255,255,255,.3);text-decoration:none;}'
    )
    content = content.replace(
        '.footer-copy{font-size:.8rem;color:var(--txt3);}',
        '.footer-copy{font-size:.8rem;color:rgba(255,255,255,.3);}'
    )
    content = content.replace(
        '.footer-copy a{color:var(--txt3);transition:color .2s;}',
        '.footer-copy a{color:rgba(255,255,255,.3);transition:color .2s;}'
    )
    # Footer col titles (--txt3 or --teal on dark footer is fine)
    content = content.replace(
        '.footer-col-title{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--txt3);margin-bottom:16px;}',
        '.footer-col-title{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.35);margin-bottom:16px;}'
    )
    # Color: teal for col titles was already correct on dark
    return content


def fix_pg_template(content):
    """kw/, learn/, compare/, solutions/ pages — pg-template CSS."""

    # Badge: 6px → 9999px pill
    content = content.replace(
        '.pg-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.08);'
        'border:1px solid rgba(10,191,204,.18);color:var(--teal);font-size:11px;font-weight:700;'
        'padding:4px 12px;border-radius:6px;margin-bottom:24px;letter-spacing:2px;text-transform:uppercase;}',
        '.pg-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.1);'
        'border:1px solid rgba(10,191,204,.2);color:var(--teal);font-size:11px;font-weight:600;'
        'padding:4px 14px;border-radius:9999px;margin-bottom:24px;letter-spacing:.5px;text-transform:uppercase;}'
    )

    # H1 typography: 700 → 600, tighter spacing
    content = content.replace(
        '.pg-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:700;line-height:1.2;margin-bottom:20px;}',
        '.pg-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:600;line-height:1.1;letter-spacing:-1px;margin-bottom:20px;}'
    )

    # Primary button: teal → black pill (13px padding variant)
    content = content.replace(
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;'
        'font-weight:700;padding:13px 28px;border-radius:8px;font-size:15px;transition:background .2s,transform .2s;}',
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#ffffff;'
        'font-weight:600;padding:11px 24px;border-radius:9999px;font-size:14px;transition:background .2s,transform .2s;}'
    )
    # Primary button: teal → black pill (14px padding variant from kw/index.html)
    content = content.replace(
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;'
        'font-weight:700;padding:14px 28px;border-radius:8px;font-size:15px;transition:background .2s,transform .2s;}',
        '.btn-p{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#ffffff;'
        'font-weight:600;padding:11px 24px;border-radius:9999px;font-size:14px;transition:background .2s,transform .2s;}'
    )
    content = content.replace(
        '.btn-p:hover{background:var(--teal2);transform:translateY(-1px);}',
        '.btn-p:hover{background:#222222;transform:translateY(-1px);}'
    )

    # Secondary button: neutral → ink outline pill (13px variant)
    content = content.replace(
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bh);'
        'color:var(--txt);padding:13px 28px;border-radius:8px;font-size:15px;transition:border-color .2s,background .2s;}',
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1px solid #0a0a0a;'
        'color:#0a0a0a;padding:11px 24px;border-radius:9999px;font-size:14px;transition:border-color .2s,background .2s;}'
    )
    # 14px variant
    content = content.replace(
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--bh);'
        'color:var(--txt);padding:14px 28px;border-radius:8px;font-size:15px;transition:border-color .2s,background .2s;}',
        '.btn-o{display:inline-flex;align-items:center;gap:8px;border:1px solid #0a0a0a;'
        'color:#0a0a0a;padding:11px 24px;border-radius:9999px;font-size:14px;transition:border-color .2s,background .2s;}'
    )
    content = content.replace(
        '.btn-o:hover{border-color:rgba(255,255,255,.25);background:var(--glow);}',
        '.btn-o:hover{border-color:#222222;background:rgba(0,0,0,.04);}'
    )

    # Card: 10px → 16px, add shadow hover
    content = content.replace(
        '.pg-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:28px;transition:border-color .2s;}',
        '.pg-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;transition:border-color .2s,box-shadow .2s;}'
    )
    content = content.replace(
        '.pg-card:hover{border-color:var(--bh);}',
        '.pg-card:hover{border-color:var(--bh);box-shadow:rgba(0,0,0,.06) 0 4px 8px;}'
    )

    # Stat box: card bg → surface bg, no border
    content = content.replace(
        '.stat-box{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:24px;text-align:center;}',
        '.stat-box{background:var(--bg2);border:none;border-radius:16px;padding:24px;text-align:center;}'
    )
    content = content.replace(
        '.stat-num{font-size:2rem;font-weight:800;color:var(--teal);}',
        '.stat-num{font-size:2rem;font-weight:700;color:var(--teal);}'
    )

    # Timeline pill: 6px → 9999px
    content = content.replace(
        '.tl-pill{background:rgba(10,191,204,.08);color:var(--teal);font-size:.72rem;font-weight:600;padding:4px 10px;border-radius:6px;}',
        '.tl-pill{background:rgba(10,191,204,.1);color:var(--teal);font-size:.72rem;font-weight:600;padding:4px 10px;border-radius:9999px;}'
    )

    # CTA section: card bg → surface, no border, 10px → 24px
    content = content.replace(
        '.pg-cta{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:64px 48px;text-align:center;margin:0 0 64px;}',
        '.pg-cta{background:var(--bg2);border:none;border-radius:24px;padding:64px 48px;text-align:center;margin:0 0 64px;}'
    )
    content = content.replace(
        '.pg-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:700;margin-bottom:16px;}',
        '.pg-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:600;letter-spacing:-.5px;margin-bottom:16px;}'
    )

    # hub-cta on kw/index.html: same treatment
    content = content.replace(
        '.hub-cta{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:64px 48px;text-align:center;margin:0 0 64px;}',
        '.hub-cta{background:var(--bg2);border:none;border-radius:24px;padding:64px 48px;text-align:center;margin:0 0 64px;}'
    )
    content = content.replace(
        '.hub-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:700;margin-bottom:16px;}',
        '.hub-cta h2{font-size:clamp(1.5rem,2.5vw,2rem);font-weight:600;letter-spacing:-.5px;margin-bottom:16px;}'
    )

    # hub-badge on kw/index.html: 6px → 9999px
    content = content.replace(
        '.hub-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.08);'
        'border:1px solid rgba(10,191,204,.18);color:var(--teal);font-size:12px;font-weight:600;'
        'padding:4px 12px;border-radius:6px;margin-bottom:24px;letter-spacing:.5px;text-transform:uppercase;}',
        '.hub-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(10,191,204,.1);'
        'border:1px solid rgba(10,191,204,.2);color:var(--teal);font-size:12px;font-weight:600;'
        'padding:4px 14px;border-radius:9999px;margin-bottom:24px;letter-spacing:.3px;text-transform:uppercase;}'
    )

    # hub-h1 on kw/index.html: 700 → 600, tighter
    content = content.replace(
        '.hub-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:700;line-height:1.2;margin-bottom:20px;}',
        '.hub-h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:600;line-height:1.1;letter-spacing:-1px;margin-bottom:20px;}'
    )

    # res-card on kw/index.html: 10px → 16px, add shadow hover
    content = content.replace(
        '.res-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:24px;'
        'display:flex;flex-direction:column;gap:12px;transition:border-color .2s;position:relative;}',
        '.res-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;'
        'display:flex;flex-direction:column;gap:12px;transition:border-color .2s,box-shadow .2s;position:relative;}'
    )
    content = content.replace(
        '.res-card:hover{border-color:var(--bh);}',
        '.res-card:hover{border-color:var(--bh);box-shadow:rgba(0,0,0,.06) 0 4px 8px;}'
    )
    content = content.replace(
        '.res-card a.card-link{position:absolute;inset:0;z-index:1;border-radius:10px;}',
        '.res-card a.card-link{position:absolute;inset:0;z-index:1;border-radius:16px;}'
    )

    return content


def fix_hub_template(content):
    """industries/*.html pages — hub-template CSS."""

    # Eyebrow badge: 6px → 9999px
    content = content.replace(
        '.hub-eyebrow{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;'
        'letter-spacing:2px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.08);'
        'border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:4px 12px;}',
        '.hub-eyebrow{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;'
        'letter-spacing:.5px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.1);'
        'border:1px solid rgba(10,191,204,.2);border-radius:9999px;padding:4px 14px;}'
    )

    # Hub hero H1: 700 → 600, tighter leading
    content = content.replace(
        '.hub-hero h1{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-1px;line-height:1.15;}',
        '.hub-hero h1{font-size:clamp(28px,4vw,48px);font-weight:600;letter-spacing:-1.5px;line-height:1.1;}'
    )

    # Status badge live: 6px → 9999px, MiniMax success-bg green
    content = content.replace(
        '.hub-status-live{color:#4ade80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2);'
        'border-radius:6px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:1px;'
        'text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;}',
        '.hub-status-live{color:#1ba673;background:#e8ffea;border:1px solid rgba(27,166,115,.2);'
        'border-radius:9999px;padding:4px 12px;font-size:11px;font-weight:600;letter-spacing:.3px;'
        'text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;}'
    )

    # Status badge ready: 6px → 9999px
    content = content.replace(
        '.hub-status-ready{color:var(--teal);background:rgba(10,191,204,.08);border:1px solid rgba(10,191,204,.18);'
        'border-radius:6px;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:1px;'
        'text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;}',
        '.hub-status-ready{color:var(--teal);background:rgba(10,191,204,.1);border:1px solid rgba(10,191,204,.2);'
        'border-radius:9999px;padding:4px 12px;font-size:11px;font-weight:600;letter-spacing:.3px;'
        'text-transform:uppercase;display:inline-flex;align-items:center;gap:6px;}'
    )

    # UC card: remove left-border, 10px → 16px, shadow on hover
    content = content.replace(
        '.uc-card{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--teal);'
        'padding:24px;border-radius:10px;position:relative;transition:border-color .2s;}',
        '.uc-card{background:var(--card);border:1px solid var(--border);'
        'padding:24px;border-radius:16px;position:relative;transition:border-color .2s,box-shadow .2s;}'
    )
    content = content.replace(
        '.uc-card:hover{border-color:var(--bh);}',
        '.uc-card:hover{border-color:var(--bh);box-shadow:rgba(0,0,0,.06) 0 4px 8px;}'
    )

    # Agent pill card: 10px → 16px, surface bg
    content = content.replace(
        '.agent-pill-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;transition:border-color .2s;}',
        '.agent-pill-card{background:var(--bg2);border:none;border-radius:16px;padding:20px;}'
    )

    # Agent tag: 6px → 9999px
    content = content.replace(
        '.agent-tag{font-size:10px;font-weight:700;color:var(--teal);background:rgba(10,191,204,.08);'
        'border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:3px 9px;letter-spacing:.5px;text-transform:uppercase;}',
        '.agent-tag{font-size:10px;font-weight:600;color:var(--teal);background:rgba(10,191,204,.1);'
        'border:1px solid rgba(10,191,204,.2);border-radius:9999px;padding:3px 10px;letter-spacing:.3px;text-transform:uppercase;}'
    )

    # CTA button: teal → black pill
    content = content.replace(
        '.btn-cta{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#070B10;'
        'font-family:var(--ff);font-size:15px;font-weight:700;padding:14px 28px;border-radius:8px;'
        'text-decoration:none;transition:background .2s,transform .2s;}',
        '.btn-cta{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;color:#ffffff;'
        'font-family:var(--ff);font-size:14px;font-weight:600;padding:11px 24px;border-radius:9999px;'
        'text-decoration:none;transition:background .2s,transform .2s;}'
    )
    content = content.replace(
        '.btn-cta:hover{background:var(--teal2);transform:translateY(-1px);}',
        '.btn-cta:hover{background:#222222;transform:translateY(-1px);}'
    )

    # Ghost button: → ink outline pill
    content = content.replace(
        '.btn-ghost{display:inline-flex;align-items:center;gap:8px;color:var(--txt);border-radius:8px;'
        'border:1px solid var(--bh);font-family:var(--ff);font-size:15px;font-weight:600;padding:14px 28px;'
        'text-decoration:none;transition:border-color .2s,background .2s;}',
        '.btn-ghost{display:inline-flex;align-items:center;gap:8px;color:#0a0a0a;border-radius:9999px;'
        'border:1px solid #0a0a0a;font-family:var(--ff);font-size:14px;font-weight:600;padding:11px 24px;'
        'text-decoration:none;transition:border-color .2s,background .2s;}'
    )
    content = content.replace(
        '.btn-ghost:hover{background:var(--glow);}',
        '.btn-ghost:hover{background:rgba(0,0,0,.04);}'
    )

    # Section title: 700 → 600, tighter
    content = content.replace(
        '.section-title{font-size:clamp(22px,3vw,34px);font-weight:700;margin-bottom:8px;}',
        '.section-title{font-size:clamp(22px,3vw,34px);font-weight:600;letter-spacing:-.5px;margin-bottom:8px;}'
    )

    return content


def fix_industries_index(content):
    """industries/index.html — unique template."""

    # Eyebrow badge: 6px → 9999px
    content = content.replace(
        '.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:700;'
        'letter-spacing:2px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.08);'
        'border:1px solid rgba(10,191,204,.18);border-radius:6px;padding:4px 12px;margin-bottom:24px;}',
        '.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:600;'
        'letter-spacing:.5px;text-transform:uppercase;color:var(--teal);background:rgba(10,191,204,.1);'
        'border:1px solid rgba(10,191,204,.2);border-radius:9999px;padding:4px 14px;margin-bottom:24px;}'
    )

    # Hero H1: 700 → 600
    content = content.replace(
        '.page-hero h1{font-size:clamp(30px,4.5vw,52px);font-weight:700;letter-spacing:-1px;line-height:1.15;margin-bottom:18px;}',
        '.page-hero h1{font-size:clamp(30px,4.5vw,52px);font-weight:600;letter-spacing:-1.5px;line-height:1.1;margin-bottom:18px;}'
    )

    # Hub card: remove left-border, 10px → 16px, shadow hover
    content = content.replace(
        '.hub-card{\n  background:var(--card);border:1px solid var(--border);border-left:3px solid var(--teal);border-radius:10px;\n'
        '  padding:28px;cursor:pointer;transition:border-color .2s;position:relative;\n'
        '  display:flex;flex-direction:column;\n}',
        '.hub-card{\n  background:var(--card);border:1px solid var(--border);border-radius:16px;\n'
        '  padding:28px;cursor:pointer;transition:border-color .2s,box-shadow .2s;\n'
        '  display:flex;flex-direction:column;\n}'
    )
    content = content.replace(
        '.hub-card:hover{border-color:var(--bh);}',
        '.hub-card:hover{border-color:var(--bh);box-shadow:rgba(0,0,0,.06) 0 4px 8px;}'
    )

    # Hub status: 6px → 9999px
    content = content.replace(
        '.hub-status{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:700;'
        'letter-spacing:.1em;text-transform:uppercase;border-radius:6px;padding:4px 12px;margin-bottom:12px;}',
        '.hub-status{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:600;'
        'letter-spacing:.05em;text-transform:uppercase;border-radius:9999px;padding:4px 12px;margin-bottom:12px;}'
    )
    # Status live color: update to MiniMax success-bg
    content = content.replace(
        '.hub-status.live{color:#4ade80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.2);}',
        '.hub-status.live{color:#1ba673;background:#e8ffea;border:1px solid rgba(27,166,115,.2);}'
    )

    # Hub pill: 6px → 9999px
    content = content.replace(
        '.hub-pill{font-size:10px;font-weight:600;color:var(--txt2);background:rgba(255,255,255,.04);'
        'border:1px solid rgba(255,255,255,.06);border-radius:6px;padding:3px 9px;}',
        '.hub-pill{font-size:10px;font-weight:500;color:var(--txt2);background:var(--bg2);'
        'border:1px solid var(--border);border-radius:9999px;padding:3px 10px;}'
    )

    # Filter button: 6px → 9999px
    content = content.replace(
        '.filter-btn{font-family:var(--ff);font-size:12px;font-weight:600;padding:8px 18px;border-radius:6px;'
        'border:1px solid var(--border);background:transparent;color:var(--txt2);cursor:pointer;transition:all .2s;}',
        '.filter-btn{font-family:var(--ff);font-size:12px;font-weight:500;padding:8px 18px;border-radius:9999px;'
        'border:1px solid var(--border);background:transparent;color:var(--txt2);cursor:pointer;transition:all .2s;}'
    )
    content = content.replace(
        '.filter-btn:hover,.filter-btn.active{background:var(--glow);border-color:var(--teal);color:var(--teal);}',
        '.filter-btn:hover,.filter-btn.active{background:var(--bg2);border-color:var(--txt2);color:var(--txt);}'
    )

    # Primary button: teal → black pill
    content = content.replace(
        '.btn-primary{display:inline-flex;align-items:center;gap:10px;background:var(--teal);color:#070B10;'
        'font-family:var(--ff);font-size:15px;font-weight:700;padding:16px 36px;border-radius:8px;'
        'transition:background .2s,transform .2s;}',
        '.btn-primary{display:inline-flex;align-items:center;gap:10px;background:#0a0a0a;color:#ffffff;'
        'font-family:var(--ff);font-size:14px;font-weight:600;padding:12px 28px;border-radius:9999px;'
        'transition:background .2s,transform .2s;}'
    )
    content = content.replace(
        '.btn-primary:hover{background:var(--teal2);transform:translateY(-1px);}',
        '.btn-primary:hover{background:#222222;transform:translateY(-1px);}'
    )

    # Page CTA h2: 700 → 600
    content = content.replace(
        '.page-cta h2{font-size:clamp(22px,3vw,34px);font-weight:700;letter-spacing:-1px;margin-bottom:12px;}',
        '.page-cta h2{font-size:clamp(22px,3vw,34px);font-weight:600;letter-spacing:-1px;margin-bottom:12px;}'
    )

    # Page CTA background
    content = content.replace(
        '.page-cta{padding:64px 48px;background:var(--bg2);border-top:1px solid var(--border);text-align:center;}',
        '.page-cta{padding:64px 48px;background:var(--bg3);border-top:1px solid var(--border);text-align:center;}'
    )

    return content


def fix_insights(content):
    """insights/ article pages."""
    # Category badge: 6px → 9999px
    content = content.replace(
        '.category-badge{background:rgba(10,191,204,.10);color:var(--teal);border-radius:6px;',
        '.category-badge{background:rgba(10,191,204,.1);color:var(--teal);border-radius:9999px;'
    )
    # Article CTA button: teal → black pill
    content = content.replace(
        '.article-cta .btn-cta{background:var(--teal);color:#070B10;border-radius:8px;',
        '.article-cta .btn-cta{background:#0a0a0a;color:#ffffff;border-radius:9999px;'
    )
    return content


def process_file(path):
    rel = os.path.relpath(path, BASE).replace('\\', '/')
    filename = os.path.basename(path)
    parts = rel.split('/')
    dirpart = parts[0] if len(parts) > 1 else ''

    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # ── Shared: root / font / nav / footer ───────────────────────────────────
    content = replace_root(content)
    content = replace_font(content)
    content = replace_nav(content)
    content = fix_footer(content)

    # ── Component-level: skip flagship & utility ──────────────────────────────
    # Compare rel (full relative path) for flagship so kw/index.html is not skipped
    if rel not in FLAGSHIP_RELPATHS and filename not in UTILITY:
        if dirpart in ('kw', 'learn', 'compare', 'solutions'):
            content = fix_pg_template(content)
        elif dirpart == 'industries':
            if filename == 'index.html':
                content = fix_industries_index(content)
            else:
                content = fix_hub_template(content)
        elif dirpart == 'platform':
            content = fix_pg_template(content)
        elif dirpart == 'insights':
            content = fix_insights(content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 'updated'
    return 'unchanged'


if __name__ == '__main__':
    files = get_files()
    updated, unchanged = 0, 0
    for f in files:
        result = process_file(f)
        rel = os.path.relpath(f, BASE)
        if result == 'updated':
            updated += 1
            print(f'  [+] {rel}')
        else:
            unchanged += 1
            print(f'  [-] {rel}')
    print(f'\nDone: {updated} updated, {unchanged} unchanged / {len(files)} total')
