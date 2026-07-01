#!/usr/bin/env python3
"""fix_flagships.py — Fix nav, buttons, hero text, footer on 5 flagship pages.

Pages:
  index.html                    — multi-line nav/btn/footer, hero strong
  ai-engineering-governance.html — multi-line nav/footer, single-line btn, hero strong
  sdlc-agent.html               — multi-line nav/footer, single-line btn, hero strong
  platform.html                 — nav+footer already done; only buttons
  about.html                    — nav+footer already done; only buttons
"""

import os

BASE = r"C:\Users\saswa\Desktop\Upcore Website\upcore-website"

# ── Canonical new nav block ───────────────────────────────────────────────────
NEW_NAV = (
    "/* ── NAV ───────────────────────────────────────────────────── */\n"
    "nav{width:100%;background:#ffffff;border-bottom:1px solid #e5e7eb;"
    "padding:0 48px;height:var(--nav-h);display:flex;align-items:center;"
    "justify-content:space-between;position:sticky;top:0;z-index:99;}\n"
    ".nav-logo a{display:flex;align-items:center;}\n"
    ".nav-logo img{height:44px;width:auto;}\n"
    ".nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}\n"
    ".nav-links a{padding:8px 16px;border-radius:8px;font-size:14px;font-weight:500;"
    "color:#45515e;transition:color .2s,background .2s;text-decoration:none;}\n"
    ".nav-links a:hover{color:#0a0a0a;background:rgba(0,0,0,.04);}\n"
    ".nav-links a.active{color:#0a0a0a;font-weight:600;}\n"
    ".nav-cta{display:inline-flex;align-items:center;gap:8px;background:#0a0a0a;"
    "color:#ffffff;font-size:14px;font-weight:600;padding:10px 22px;border-radius:9999px;"
    "text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}\n"
    ".nav-cta:hover{background:#222222;transform:translateY(-1px);}\n"
    "@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}"
)

# ── Multi-line nav block shared by index / ai-gov / sdlc ─────────────────────
OLD_NAV_MULTILINE_START = (
    "/* ── NAV ───────────────────────────────────────────────────── */\n"
    "nav {\n"
    "  width:100%; background:rgba(7,11,16,0.97);\n"
    "  border-bottom:1px solid var(--border);\n"
    "  padding:0 48px; height:64px;\n"
    "  display:flex; align-items:center; justify-content:space-between;\n"
    "  position:sticky; top:0; z-index:99;\n"
    "}\n"
    ".nav-logo a { display:flex; align-items:center; }\n"
    ".nav-logo img { height:58px; width:auto; }\n"
    ".nav-links { display:flex; gap:2px; list-style:none; padding:0; margin:0; }\n"
)
OLD_NAV_MEDIAEND = "@media(max-width:768px){ nav{padding:0 20px;} .nav-links{display:none;} }"


# ─────────────────────────────────────────────────────────────────────────────
# Helper: replace footer on multi-line formatted flagship pages
# ─────────────────────────────────────────────────────────────────────────────
def fix_footer_multiline(content):
    content = content.replace(
        "footer { background:var(--bg); border-top:1px solid var(--border); padding:60px 48px 0; }",
        "footer { background:#0a0a0a; border-top:1px solid rgba(255,255,255,.06); padding:60px 48px 0; }"
    )
    content = content.replace(
        ".footer-tagline { font-size:13px; color:var(--txt2); line-height:1.7; margin-top:12px; max-width:200px; }",
        ".footer-tagline { font-size:13px; color:rgba(255,255,255,.4); line-height:1.7; margin-top:12px; max-width:200px; }"
    )
    content = content.replace(
        ".footer-links a { font-size:13px; color:var(--txt2); transition:color .15s; }",
        ".footer-links a { font-size:13px; color:rgba(255,255,255,.55); transition:color .15s; }"
    )
    content = content.replace(
        ".footer-col-title { font-size:10px; font-weight:700; letter-spacing:2px; "
        "text-transform:uppercase; color:var(--txt3); margin-bottom:16px; }",
        ".footer-col-title { font-size:10px; font-weight:700; letter-spacing:2px; "
        "text-transform:uppercase; color:rgba(255,255,255,.35); margin-bottom:16px; }"
    )
    content = content.replace(
        ".footer-copy { font-size:12px; color:var(--txt3); }",
        ".footer-copy { font-size:12px; color:rgba(255,255,255,.3); }"
    )
    content = content.replace(
        ".footer-copy a { color:var(--txt3); }",
        ".footer-copy a { color:rgba(255,255,255,.3); }"
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# index.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_index(content):
    # NAV — multi-line with multi-line nav-links a and multi-line nav-cta
    old_nav = (
        OLD_NAV_MULTILINE_START
        + ".nav-links a {\n"
        + "  padding:8px 15px; border-radius:6px;\n"
        + "  font-size:14px; font-weight:500; color:var(--txt2);\n"
        + "  transition:color .2s,background .2s;\n"
        + "}\n"
        + ".nav-links a:hover { color:var(--txt); background:var(--glow); }\n"
        + ".nav-links a.active { color:var(--txt); }\n"
        + ".nav-cta {\n"
        + "  display:inline-flex; align-items:center; gap:6px;\n"
        + "  background:var(--teal); color:#070B10;\n"
        + "  font-size:14px; font-weight:700;\n"
        + "  padding:9px 20px; border-radius:8px;\n"
        + "  white-space:nowrap; transition:background .2s,transform .2s;\n"
        + "}\n"
        + ".nav-cta:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        + OLD_NAV_MEDIAEND
    )
    content = content.replace(old_nav, NEW_NAV)

    # BUTTONS — multi-line .btn block
    content = content.replace(
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn {\n"
        "  display:inline-flex; align-items:center; gap:8px;\n"
        "  font:600 15px/1 var(--ff); padding:14px 28px;\n"
        "  border-radius:8px; cursor:pointer;\n"
        "  transition:all .2s; border:none; text-decoration:none;\n"
        "}\n"
        ".btn-fill { background:var(--teal); color:#070B10; }\n"
        ".btn-fill:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:var(--txt); border:1px solid var(--bh); }\n"
        ".btn-ghost:hover { background:var(--glow); border-color:rgba(255,255,255,.25); }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }",
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn {\n"
        "  display:inline-flex; align-items:center; gap:8px;\n"
        "  font:600 15px/1 var(--ff); padding:12px 26px;\n"
        "  border-radius:9999px; cursor:pointer;\n"
        "  transition:all .2s; border:none; text-decoration:none;\n"
        "}\n"
        ".btn-fill { background:#0a0a0a; color:#ffffff; }\n"
        ".btn-fill:hover { background:#222222; transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:#0a0a0a; border:1px solid #0a0a0a; }\n"
        ".btn-ghost:hover { background:rgba(0,0,0,.04); border-color:#222222; }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; border-radius:9999px; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }"
    )

    # HERO strong text — invisible on white bg
    content = content.replace(
        ".hero-h1 strong { font-weight:800; color:#fff; }",
        ".hero-h1 strong { font-weight:700; color:var(--txt); }"
    )

    # FOOTER
    content = fix_footer_multiline(content)
    return content


# ─────────────────────────────────────────────────────────────────────────────
# ai-engineering-governance.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_aigov(content):
    # NAV — multi-line nav, single-line links, active = var(--txt)
    old_nav = (
        OLD_NAV_MULTILINE_START
        + ".nav-links a { padding:8px 15px; border-radius:6px; font-size:14px; font-weight:500; "
        + "color:var(--txt2); transition:color .2s,background .2s; }\n"
        + ".nav-links a:hover { color:var(--txt); background:var(--glow); }\n"
        + ".nav-links a.active { color:var(--txt); }\n"
        + ".nav-cta { display:inline-flex; align-items:center; gap:6px; background:var(--teal); "
        + "color:#070B10; font-size:14px; font-weight:700; padding:9px 20px; border-radius:8px; "
        + "white-space:nowrap; transition:background .2s,transform .2s; }\n"
        + ".nav-cta:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        + OLD_NAV_MEDIAEND
    )
    content = content.replace(old_nav, NEW_NAV)

    # BUTTONS — single-line .btn with text-decoration:none
    content = content.replace(
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn { display:inline-flex; align-items:center; gap:8px; font:600 15px/1 var(--ff); "
        "padding:14px 28px; border-radius:8px; cursor:pointer; transition:all .2s; border:none; text-decoration:none; }\n"
        ".btn-fill { background:var(--teal); color:#070B10; }\n"
        ".btn-fill:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:var(--txt); border:1px solid var(--bh); }\n"
        ".btn-ghost:hover { background:var(--glow); border-color:rgba(255,255,255,.25); }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }",
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn { display:inline-flex; align-items:center; gap:8px; font:600 15px/1 var(--ff); "
        "padding:12px 26px; border-radius:9999px; cursor:pointer; transition:all .2s; border:none; text-decoration:none; }\n"
        ".btn-fill { background:#0a0a0a; color:#ffffff; }\n"
        ".btn-fill:hover { background:#222222; transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:#0a0a0a; border:1px solid #0a0a0a; }\n"
        ".btn-ghost:hover { background:rgba(0,0,0,.04); border-color:#222222; }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; border-radius:9999px; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }"
    )

    # HERO strong
    content = content.replace(
        ".hero-h1 strong { font-weight:800; color:#fff; }",
        ".hero-h1 strong { font-weight:700; color:var(--txt); }"
    )

    # FOOTER
    content = fix_footer_multiline(content)
    return content


# ─────────────────────────────────────────────────────────────────────────────
# sdlc-agent.html
# ─────────────────────────────────────────────────────────────────────────────
def fix_sdlc(content):
    # NAV — multi-line nav, single-line links, active = var(--teal)
    old_nav = (
        OLD_NAV_MULTILINE_START
        + ".nav-links a { padding:8px 15px; border-radius:6px; font-size:14px; font-weight:500; "
        + "color:var(--txt2); transition:color .2s,background .2s; }\n"
        + ".nav-links a:hover { color:var(--txt); background:var(--glow); }\n"
        + ".nav-links a.active { color:var(--teal); }\n"
        + ".nav-cta { display:inline-flex; align-items:center; gap:6px; background:var(--teal); "
        + "color:#070B10; font-size:14px; font-weight:700; padding:9px 20px; border-radius:8px; "
        + "white-space:nowrap; transition:background .2s,transform .2s; }\n"
        + ".nav-cta:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        + OLD_NAV_MEDIAEND
    )
    content = content.replace(old_nav, NEW_NAV)

    # BUTTONS — single-line .btn WITHOUT text-decoration:none
    content = content.replace(
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn { display:inline-flex; align-items:center; gap:8px; font:600 15px/1 var(--ff); "
        "padding:14px 28px; border-radius:8px; cursor:pointer; transition:all .2s; border:none; }\n"
        ".btn-fill { background:var(--teal); color:#070B10; }\n"
        ".btn-fill:hover { background:var(--teal2); transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:var(--txt); border:1px solid var(--bh); }\n"
        ".btn-ghost:hover { background:var(--glow); border-color:rgba(255,255,255,.25); }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }",
        "/* ── BUTTONS ───────────────────────────────────────────────── */\n"
        ".btn { display:inline-flex; align-items:center; gap:8px; font:600 15px/1 var(--ff); "
        "padding:12px 26px; border-radius:9999px; cursor:pointer; transition:all .2s; border:none; }\n"
        ".btn-fill { background:#0a0a0a; color:#ffffff; }\n"
        ".btn-fill:hover { background:#222222; transform:translateY(-1px); }\n"
        ".btn-ghost { background:transparent; color:#0a0a0a; border:1px solid #0a0a0a; }\n"
        ".btn-ghost:hover { background:rgba(0,0,0,.04); border-color:#222222; }\n"
        ".btn-amber { background:var(--amber2); color:#070B10; border-radius:9999px; }\n"
        ".btn-amber:hover { background:var(--amber); transform:translateY(-1px); }"
    )

    # HERO strong
    content = content.replace(
        ".hero-h1 strong { font-weight:800; color:#fff; }",
        ".hero-h1 strong { font-weight:700; color:var(--txt); }"
    )

    # FOOTER
    content = fix_footer_multiline(content)
    return content


# ─────────────────────────────────────────────────────────────────────────────
# platform.html — nav+footer already done; fix buttons only
# ─────────────────────────────────────────────────────────────────────────────
def fix_platform(content):
    # .btn base (no trailing semicolons in this page's CSS)
    content = content.replace(
        ".btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--ff);"
        "font-size:.92rem;font-weight:600;padding:13px 28px;border-radius:8px;"
        "border:none;cursor:pointer;transition:all .2s;text-decoration:none}",
        ".btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--ff);"
        "font-size:.92rem;font-weight:600;padding:11px 24px;border-radius:9999px;"
        "border:none;cursor:pointer;transition:all .2s;text-decoration:none}"
    )
    content = content.replace(
        ".btn-fill{background:var(--teal);color:#070B10;font-weight:700}",
        ".btn-fill{background:#0a0a0a;color:#ffffff;font-weight:600}"
    )
    content = content.replace(
        ".btn-fill:hover{background:var(--teal2);transform:translateY(-1px)}",
        ".btn-fill:hover{background:#222222;transform:translateY(-1px)}"
    )
    content = content.replace(
        ".btn-ghost{background:transparent;color:var(--txt);border:1px solid var(--bh)}",
        ".btn-ghost{background:transparent;color:#0a0a0a;border:1px solid #0a0a0a}"
    )
    content = content.replace(
        ".btn-ghost:hover{background:var(--glow);border-color:rgba(255,255,255,.25)}",
        ".btn-ghost:hover{background:rgba(0,0,0,.04);border-color:#222222}"
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# about.html — nav+footer already done; fix buttons only
# ─────────────────────────────────────────────────────────────────────────────
def fix_about(content):
    # .btn base (with trailing semicolons)
    content = content.replace(
        ".btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--ff);"
        "font-size:15px;font-weight:600;padding:14px 30px;border-radius:8px;"
        "border:none;cursor:pointer;transition:all .2s;text-decoration:none;}",
        ".btn{display:inline-flex;align-items:center;gap:10px;font-family:var(--ff);"
        "font-size:15px;font-weight:600;padding:12px 26px;border-radius:9999px;"
        "border:none;cursor:pointer;transition:all .2s;text-decoration:none;}"
    )
    content = content.replace(
        ".btn-fill{background:var(--teal);color:#070B10;font-weight:700;}",
        ".btn-fill{background:#0a0a0a;color:#ffffff;font-weight:600;}"
    )
    content = content.replace(
        ".btn-fill:hover{background:var(--teal2);transform:translateY(-1px);}",
        ".btn-fill:hover{background:#222222;transform:translateY(-1px);}"
    )
    content = content.replace(
        ".btn-ghost{background:transparent;color:var(--txt);border:1px solid var(--bh);}",
        ".btn-ghost{background:transparent;color:#0a0a0a;border:1px solid #0a0a0a;}"
    )
    content = content.replace(
        ".btn-ghost:hover{background:var(--glow);border-color:rgba(255,255,255,.25);}",
        ".btn-ghost:hover{background:rgba(0,0,0,.04);border-color:#222222;}"
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────────────────────────────────────
def process(filepath, fix_fn):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    content = fix_fn(original)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 'updated'
    return 'unchanged'


if __name__ == '__main__':
    tasks = [
        ('index.html',                    fix_index),
        ('ai-engineering-governance.html', fix_aigov),
        ('sdlc-agent.html',               fix_sdlc),
        ('platform.html',                 fix_platform),
        ('about.html',                    fix_about),
    ]
    for filename, fix_fn in tasks:
        filepath = os.path.join(BASE, filename)
        result = process(filepath, fix_fn)
        print(f"  [{'+'if result=='updated'else'-'}] {filename} — {result}")
