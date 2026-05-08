# Design System

> **Canonical source:** the `:root` block and the `<nav>` block in [`index.html`](../index.html). Every other page **must** mirror these byte-for-byte. This document records the values; if you change them, update `index.html` first, then every other page, then this file.

## 1. Color tokens

Every page declares the same `:root`:

```css
:root {
  --bg:    #07101e;     /* page background (deepest) */
  --bg2:   #0a1628;     /* section break / trust strip */
  --bg3:   #0d1c34;     /* layered surface */
  --card:  #0f2040;     /* card / panel surface */

  --teal:  #0abfcc;     /* primary brand */
  --mint:  #3dddc4;     /* highlight / success accent */
  --teal3: #0891b2;     /* gradient start */
  --green: #4ade80;     /* "live" / status dot */

  --txt:   #ffffff;     /* primary text */
  --txt2:  #8bbed4;     /* secondary text (body) */
  --txt3:  #3a6080;     /* tertiary text (labels, captions) */

  --border: rgba(10, 191, 204, 0.13);   /* default border */
  --bh:     rgba(10, 191, 204, 0.38);   /* hover/active border */
  --glow:   rgba(10, 191, 204, 0.08);   /* hover background tint */

  --grad:  linear-gradient(135deg, #0891b2, #0abfcc, #3dddc4);  /* THE brand gradient */
  --ff:    "Poppins", sans-serif;
}
```

**Rules**
- Don't introduce new hex values. Either use a token or extend `:root` (and propagate to every page).
- `--grad` is the only gradient that appears on primary CTAs and gradient text. Don't invent alt gradients.
- Status colors used in cards/visualizations: `#ff6b6b` (red dot), `#fbbf24` (amber dot), `#4ade80` (green dot / `--green`). These are the only allowed semantic accents outside the teal palette.

## 2. Typography

- Family: **Poppins** loaded once per page from Google Fonts, weights `300;400;500;600;700;800;900`. Use `var(--ff)` everywhere — never raw `font-family`.
- Body: `font-size: 16px` implicit, `line-height: 1.6`, `color: var(--txt)` on `var(--bg)`.
- Heading scale (extracted from index hero + section heads):

| Use | Size | Weight | Letter-spacing | Notes |
|---|---|---|---|---|
| Hero H1 | `clamp(44px, 5.8vw, 76px)` | 800 | `-2px` | `line-height: 1.04` |
| Section H2 | `clamp(32px, 4vw, 52px)` | 800 | — | — |
| Card / sub-section | 18px–24px | 600–700 | — | — |
| Body | 17–18px | 400 | — | `color: var(--txt2)`, `line-height: 1.78` for hero sub |
| Eyebrow / label | 11–13px | 600–700 | `0.3–2px` | `text-transform: uppercase` for trust headers |
| Stat number | 36px | 800 | — | `color: var(--teal)` |

- Gradient text uses `.grad-text` (background-clip pattern). Don't reinvent it.

## 3. Spacing & layout

- Page horizontal padding: **48px desktop, 20px mobile** (≤768px). The nav uses the same.
- Hero inner: `padding: 100px 48px 80px`.
- Standard section padding lives inline per page; common pattern is `80–120px` vertical, `48px` horizontal.
- Border-radius scale: `8` (small chip) · `10` (CTA pill) · `12` (button) · `14` (large button) · `16` (card row) · `20` (hero card) · `100px` (full pill).
- Box-shadows for primary CTA: `0 4px 28px rgba(10,191,204,0.3)` resting → `0 8px 44px rgba(10,191,204,0.48)` hover.

## 4. Components

### 4.1 Nav (most sensitive — pixel-perfect across all 37 pages)

Recent commits in this repo had to repair nav damage caused by per-page edits. **Do not edit one page's nav in isolation.** Locked specs:

```css
nav {
  width: 100%;
  background: rgba(7, 16, 30, 0.96);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(10, 191, 204, 0.13);
  padding: 0 48px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 99;
}
.nav-logo img { height: 68px; width: auto; }
.nav-links     { display: flex; gap: 4px; list-style: none; }
.nav-links a   { padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; color: rgba(139,190,212,1); }
.nav-links a:hover  { color: #fff; background: rgba(10,191,204,0.08); }
.nav-links a.active { color: #0abfcc; }
.nav-cta {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #0891b2, #0abfcc, #3dddc4);
  color: #07101e; font-size: 14px; font-weight: 700;
  padding: 10px 22px; border-radius: 10px;
}
@media (max-width: 768px) {
  nav { padding: 0 20px; }
  .nav-links { display: none; }   /* mobile: hide link list */
}
```

**When editing the nav:**
1. Edit `index.html` first.
2. Diff every other page's `<nav>` block against the new one. (Quick check: `grep -A 30 '<nav' *.html industries/*.html insights/*.html` and compare.)
3. Add the active-state highlight on the page that owns it: `<a href="..." class="active">`.
4. Update this section if the spec changes.

### 4.2 Buttons

```css
.btn      { padding: 15px 30px; border-radius: 12px; font-size: 15px; font-weight: 600; gap: 8px; transition: all 0.22s; font-family: var(--ff); }
.btn-lg   { padding: 17px 38px; font-size: 16px; border-radius: 14px; }
.btn-primary { background: var(--grad); color: #07101e; box-shadow: 0 4px 28px rgba(10,191,204,0.3); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 44px rgba(10,191,204,0.48); }
.btn-outline { background: transparent; color: var(--txt); border: 1.5px solid var(--bh); }
.btn-outline:hover { background: var(--glow); border-color: var(--teal); }
```

- Primary CTAs use `.btn-primary` with the brand gradient. Outline buttons are the secondary action.
- The chat widget overrides these with its own scoped CSS — that's intentional, don't unify.

### 4.3 Cards / surfaces

```css
.card-like {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
}
```
Hover state: bump border to `var(--bh)` and add `box-shadow: 0 4px 28px rgba(10,191,204,0.18)` if interactive.

### 4.4 Tag / pill (eyebrow above hero)

```css
.hero-tag {
  display: inline-flex; align-items: center; gap: 10px;
  background: linear-gradient(135deg, rgba(10,191,204,0.15), rgba(61,221,196,0.10));
  border: 1px solid rgba(10,191,204,0.35);
  border-radius: 100px; padding: 10px 22px;
  font-size: 13px; font-weight: 700; letter-spacing: 0.3px;
}
.tag-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--mint); animation: pulse 2s infinite; }
```

### 4.5 Stat / proof row

3-column grid, 1px borders between cells, 16px outer radius. Stat number = 36px / 800 / `--teal`; label = 12px / `--txt3`.

### 4.6 Background atmospherics

- `.hero-glow` — two stacked `radial-gradient` ellipses on `pointer-events: none`. Subtle teal/mint glows at low opacity (4–7%).
- `.hero-grid` — 60×60 grid drawn with two crossed `linear-gradient`s at `rgba(10,191,204,0.04)`.
- Trust strip uses `keyframes marquee` (28s linear infinite) on a doubled track. `:hover` pauses it.

## 5. Chat widget styling

The chat widget (`/chat-widget.js`) ships its own scoped CSS prefixed with `#upcore-chat-*`. It echoes the brand gradient (`#00d4b4 → #0099cc` — note: a **different** gradient from `--grad`). When updating widget colors, edit them in [chat-widget.js](../chat-widget.js); they intentionally don't read CSS variables (the widget must work even on pages that didn't load `:root`).

## 6. Do / don't

**Do**
- Use existing tokens. Reach for `var(--card)` before typing `#0f2040`.
- Mirror nav/`:root`/font-load changes across every page in the same commit.
- Keep page-specific styles inline in that page's `<style>` block — that's the architecture.

**Don't**
- Introduce a CSS framework, preprocessor, or shared stylesheet. The trade-off (duplication for zero build complexity) is intentional — see [ARCHITECTURE.md](ARCHITECTURE.md).
- Add new colors without extending `:root` everywhere.
- Edit one page's `<nav>` to "fix" it locally. That's how the previous nav damage happened.
- Change Poppins to a different family without updating every `<link>` and the `--ff` token.
