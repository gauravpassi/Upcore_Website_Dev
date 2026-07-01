# Design System

> **Canonical source:** the `:root` block and the `<nav>` block in [`index.html`](../index.html). Every other page **must** mirror these byte-for-byte. This document records the values; if you change them, update `index.html` first, then every other page via `apply_minimax.py`, then this file.
>
> **Current design system: MiniMax white-canvas** — applied 2026-07-01. Previous system was dark charcoal; see CHANGELOG for history.

## 1. Color tokens

Every page declares the same `:root`:

```css
:root {
  /* Backgrounds — white canvas */
  --bg:     #ffffff;   /* Page background */
  --bg2:    #f7f8fa;   /* Lifted surface / secondary sections */
  --bg3:    #f2f3f5;   /* Deliberate section break */
  --card:   #ffffff;   /* Card background */
  --card2:  #f7f8fa;   /* Elevated / featured card */

  /* Brand teal — used selectively for accents */
  --teal:   #0ABFCC;
  --teal2:  #089AAA;
  --mint:   #0ABFCC;   /* alias */

  /* Removed: amber accent tokens — replaced with teal site-wide (2025-07) */

  /* Status */
  --green:  #22C55E;
  --red:    #EF4444;

  /* Text — dark on white */
  --txt:    #0a0a0a;   /* Near-black — primary headings */
  --txt2:   #45515e;   /* Muted — body / secondary */
  --txt3:   #8e8e93;   /* Dimmer tertiary */
  --ink:    #0a0a0a;   /* Alias for button fill */
  --ink-press: #222222;

  /* Borders — light hairline */
  --border: #e5e7eb;
  --bh:     #d1d5db;
  --glow:   rgba(0,0,0,0.04);

  /* Gradients — for accents only, not buttons */
  --grad:       linear-gradient(135deg,#0891b2,#0ABFCC);
  /* --grad-amber removed (2025-07); use --grad for teal gradient */

  /* Layout */
  --ff:    "DM Sans", sans-serif;
  --nav-h: 64px;
  --max:   1240px;
}
```

**Rules**
- Don't introduce new hex values. Use a token or extend `:root` (propagate via `apply_minimax.py`).
- Backgrounds are white-canvas — never add dark/navy backgrounds to content sections.
- Borders use solid light hairlines (`#e5e7eb`), not white-alpha. White-alpha borders are only appropriate on the dark footer.
- **No amber tokens.** Amber was removed site-wide (2025-07); use `--teal` / `--teal2` for all accents.
- **Footer** is always dark (`background:#0a0a0a`) — MiniMax footer-region token. Footer text uses explicit `rgba(255,255,255,…)` overrides since `--txt` is now dark.

## 2. Typography

**Rules**

1. **Hero H1**: thin weight (`300–400`) + `<strong>` for emphasis. Large, spare. No gradient text.
2. **Hero H1 `<strong>`**: `font-weight:700; color:var(--txt)` — do NOT use `color:#fff` (page bg is now white).
3. **Section H2**: weight `600–700`, `letter-spacing:-0.5px`, color `var(--txt)`.
4. **Gradient text** (`.grad-text`): **BANNED** on headings.
5. **Body**: `17px`, weight `400`, `line-height: 1.75`, color `var(--txt2)`.
6. **Eyebrows**: `10–12px`, weight `600`, `letter-spacing: 0.5px`, uppercase. Shape: **9999px pill** (not 6px sharp).
7. **Stat numbers**: weight `700–800`, color `var(--teal)`. No gradient on numbers.

**Font loading:**
- Family: **DM Sans** from Google Fonts: `family=DM+Sans:wght@300;400;500;600;700`
- Use `var(--ff)` everywhere — never raw `font-family`.

**WCAG note:** `--txt2` (`#64748B`) on `--bg` (`#070B10`) yields contrast ratio ≈ 4.52:1 — passes WCAG AA (4.5:1 threshold). If lightened, keep above 4.5:1.

## 3. Spacing & layout

- Page horizontal padding: **48px desktop, 20px mobile** (≤768px). The nav uses the same.
- Standard section padding: `100px 48px` vertical/horizontal.
- Max content width: `var(--max)` = `1240px`, centered with `margin: 0 auto`.
- Border-radius scale: **`9999px`** (badge/pill/button CTA) · `16px` (card, panel) · `8px` (nav link hover, small chip).
- Cards: `box-shadow: rgba(0,0,0,.06) 0 4px 8px` on hover (replaces teal glow). No teal border accent on standard cards.

## 4. Components

### 4.1 Nav (most sensitive — pixel-perfect across all 65 pages)

This is the canonical nav. **Do not edit one page's nav in isolation.** Propagate via script.

**Nav is dark (`#0a0a0a`)** — the logo was designed for dark backgrounds; a white nav made logo elements invisible. The dark nav also reads as more authoritative for an enterprise governance product.

```css
nav{width:100%;background:#0a0a0a;border-bottom:1px solid rgba(255,255,255,.08);padding:0 48px;height:var(--nav-h);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:99;}
.nav-logo a{display:flex;align-items:center;}
.nav-logo img{height:40px;width:auto;}
.nav-links{display:flex;gap:4px;list-style:none;padding:0;margin:0;}
.nav-links a{padding:8px 16px;border-radius:6px;font-size:14px;font-weight:500;color:rgba(255,255,255,.65);transition:color .2s,background .2s;text-decoration:none;}
.nav-links a:hover{color:#ffffff;background:rgba(255,255,255,.07);}
.nav-links a.active{color:#ffffff;font-weight:600;}
.nav-cta{display:inline-flex;align-items:center;gap:8px;background:#ffffff;color:#0a0a0a;font-size:14px;font-weight:600;padding:10px 22px;border-radius:9999px;text-decoration:none;white-space:nowrap;transition:background .2s,transform .2s;}
.nav-cta:hover{background:#f2f2f2;transform:translateY(-1px);}
@media(max-width:768px){nav{padding:0 20px;}.nav-links{display:none;}}
```

```html
<!-- Canonical 5-link nav — active class varies per page -->
<nav>
  <div class="nav-logo"><a href="/"><img src="/upcore-logo.png" alt="Upcore Technologies"/></a></div>
  <ul class="nav-links">
    <li><a href="/ai-engineering-governance">AI Governance</a></li>
    <li><a href="/platform">Products</a></li>
    <li><a href="/industries">Industries</a></li>
    <li><a href="/insights">Resources</a></li>
    <li><a href="/about">About</a></li>
  </ul>
  <a href="/assessment" class="nav-cta">Book a Call</a>
</nav>
```

**Active class mapping:**
| URL prefix | Active link |
|---|---|
| `/ai-engineering-governance` | AI Governance |
| `/platform` | Products |
| `/industries` | Industries |
| `/insights` | Resources |
| `/kw/` | Resources |
| `/about` | About |

**When editing the nav:**
1. Edit `index.html` first.
2. Run `python propagate_design.py` from `upcore-website/` to propagate to all 65 pages.
3. Update this section if the spec changes.

### 4.2 Buttons — 3 classes

```css
/* Base — pill shape */
.btn       { font: 600 15px/1 var(--ff); padding: 12px 26px; border-radius: 9999px;
             cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; border: none; }
/* Primary — black pill */
.btn-fill  { background: #0a0a0a; color: #ffffff; }
.btn-fill:hover  { background: #222222; transform: translateY(-1px); }
/* Secondary — ink outline pill */
.btn-ghost { background: transparent; color: #0a0a0a; border: 1px solid #0a0a0a; }
.btn-ghost:hover { background: rgba(0,0,0,.04); border-color: #222222; }
/* Teal accent */
.btn-teal { background: var(--teal); color: #070B10; border-radius: 9999px; }
.btn-teal:hover { background: var(--teal2); transform: translateY(-1px); }
```

Usage:
- `.btn.btn-fill` — primary CTA (black pill). Used everywhere for the main action.
- `.btn.btn-ghost` — secondary action (ink outline pill).
- `.btn.btn-teal` — teal accent CTA, available site-wide.
- **Never use teal fills on buttons** — black pill is the MiniMax CTA pattern.
- The nav CTA (`.nav-cta`) keeps its own scoped CSS and is NOT part of the `.btn` system.

### 4.3 Cards / surfaces

```css
/* Standard card */
background: var(--card);      /* #ffffff */
border: 1px solid var(--border);   /* #e5e7eb */
border-radius: 16px;
padding: 24px 28px;
transition: border-color 0.2s, box-shadow 0.2s;

/* Hover */
border-color: var(--bh);     /* #d1d5db */
box-shadow: rgba(0,0,0,.06) 0 4px 8px;
```

**Removed patterns — do not re-introduce:**
- Teal left-border accent on standard cards (`.hub-card`, `.uc-card`) — removed in MiniMax pass
- Gradient top-bar on hover (`::before` with gradient background)
- Teal glow `box-shadow`: `0 4px 28px rgba(10,191,204,0.3)` — BANNED
- Small border-radius (6–10px) on cards — use 16px
- `transform: translateY(-4px)` on card hover — too dramatic; use `-1px` max

### 4.4 Eyebrow / badge tag

```css
.badge-tag {
  display: inline-flex;
  align-items: center;
  background: rgba(10,191,204,0.1);
  border: 1px solid rgba(10,191,204,0.2);
  border-radius: 9999px;              /* pill — MiniMax style */
  padding: 4px 14px;
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: var(--teal);
}
```

Eyebrow/badge tags are **always pill-shaped** (`9999px`). The old sharp `6px` badges have been replaced site-wide.

### 4.5 Stat / proof row

Number: `font-size: clamp(32px,4vw,48px)`, weight `800`, color `var(--teal)`.
Label: `12–13px`, color `var(--txt3)`.
No card border around individual stats — use whitespace separation only.

### 4.6 Hero sections

**Removed:**
- Radial-gradient grid overlay `::before` on every hero — banned
- `backdrop-filter: blur(20px)` on nav — replaced with solid rgba background
- Animated pulse on every badge dot — keep only on the homepage hero badge

**New hero pattern:**
```css
.hero { padding: 100px 48px 80px; background: var(--bg); }
.hero h1 { font-size: clamp(48px,6vw,80px); font-weight: 300; color: var(--txt); }
.hero h1 strong { font-weight: 700; }
```

### 4.7 Insights article pages

Article pages under `insights/` use the `ARTICLE_BASE_CSS` canonical stylesheet injected via `fix_all.py`. Key elements:

```css
body { font-family: 'Poppins', sans-serif; background: var(--bg); color: var(--txt2); }
h1 { font-size: clamp(28px,5vw,42px); font-weight: 300; color: var(--txt); }
h1 strong { font-weight: 700; }
.category-badge { background: rgba(10,191,204,0.10); color: var(--teal); border-radius: 6px; }
.agent-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; }
.article-cta .btn-cta { background: var(--teal); color: #070B10; border-radius: 8px; }
```

## 5. Footer

**Background:** `#0a0a0a` (always dark — footer is a deliberate dark region on the white-canvas body)
**Top accent:** `border-top: 3px solid rgba(10,191,204,.2)` — thin teal line separates footer from content
**Canonical tagline:** `Govern Your AI. Then Build With It.` — `font-weight:600; color:rgba(255,255,255,.75)`
**Sub-line:** `Enterprise AI governance and agents, built for your org.` — `color:rgba(255,255,255,.35)`

**Key rule: never use `var(--txt)`, `var(--txt2)`, or `var(--txt3)` inside footer CSS.** These are now light-canvas values (`#0a0a0a`, `#45515e`, `#8e8e93`) — all invisible on the dark footer. Always use explicit `rgba(255,255,255,…)` values.

Footer color scale:
- Link text: `rgba(255,255,255,.52)` → hover `#ffffff`
- Social icon buttons: circular (`border-radius:50%`), `color:rgba(255,255,255,.55)` → hover `#ffffff`
- Review badges: `color:rgba(255,255,255,.45)` → hover `rgba(255,255,255,.85)`
- Column titles: `rgba(255,255,255,.4)`, `letter-spacing:2px`, uppercase, 10px
- Tagline: `rgba(255,255,255,.75)`, weight 600
- Sub-tagline: `rgba(255,255,255,.35)`
- Cert strip (footer-bottom left): `rgba(255,255,255,.28)`
- Copyright (footer-bottom right): `rgba(255,255,255,.25)`
- Divider (footer-bottom border-top): `rgba(255,255,255,.09)`

**Footer bottom** shows certifications on the left (`CMMI Level 3 · ISO 27001 · ISO 9001 · Nasscom Member`) and copyright on the right. No italic tagline.

## 6. Chat widget styling

The chat widget (`/chat-widget.js`) ships its own scoped CSS prefixed with `#upcore-chat-*`. It uses its own hardcoded colors intentionally — the widget must work even on pages that haven't loaded `:root`. When updating widget colors, edit `chat-widget.js` directly.

## 7. Propagation scripts

Two Python scripts in `upcore-website/`:

- **`propagate_design.py`** — replaces `:root`, nav CSS, and nav HTML on all 65 pages. Run after any change to the canonical nav or root tokens. SKIP set: `index.html`, `ai-engineering-governance.html`, `sdlc-agent.html`, `platform.html`, `about.html` (manually redesigned).
- **`fix_all.py`** — comprehensive fix pass: footer tagline/hover, grad-text → `<strong>`, button class migration, insights article CSS injection.

## 8. Do / don't

**Do**
- Use existing tokens. Reach for `var(--card)` before typing `#171E2B`.
- Mirror nav/`:root` changes across every page via `propagate_design.py` in the same pass.
- Keep page-specific styles inline in that page's `<style>` block — that's the architecture.
- Use `border-left: 3px solid var(--teal)` for semantic accent on cards (not gradient top-bars).
- Use `<strong>` for emphasis in headings (not `.grad-text`).

**Don't**
- Introduce `.grad-text` spans in H1/H2 elements — banned. One-time exception allowed only for a single stat number on a flagship page if critically needed.
- Add teal glow box-shadows to cards or interactive elements.
- Use large border-radius (>10px on cards, >8px on buttons).
- Use `backdrop-filter: blur()` on the nav — replaced with solid background.
- Edit one page's `<nav>` or `:root` locally. Run the propagation script.
- Introduce a CSS framework, preprocessor, or shared stylesheet.
- Add new colors without extending `:root` everywhere (and updating this doc).
