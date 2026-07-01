# Upcore Design System

> **This is the single source of truth.** Every visual decision on every page must trace back to a rule in this document.
> Canonical HTML source: `index.html`. Canonical script: `apply_design_system.py`.

---

## 1. Brand personality

Upcore is an enterprise AI company. The visual language is **Palantir/Anduril-adjacent** — charcoal-neutral, minimal decoration, maximum typography authority. Not a consumer SaaS product. Not "AI slop."

**What this means in practice:**
- No gradient fills on buttons
- No teal glow `box-shadow` anywhere
- No gradient text (`-webkit-text-fill-color: transparent`) on any heading
- No full-pill buttons (`border-radius: 100px`) outside of status indicator dots
- No animated grid overlays on hero sections
- Colour used to signal, not decorate

---

## 2. Colour tokens

Every page declares the same `:root`. Never use raw hex — always `var()`.

```css
:root {
  /* Backgrounds — charcoal, NOT navy blue */
  --bg:     #070B10;   /* Page base — near-black, minimal blue */
  --bg2:    #0C1018;   /* Lifted surface */
  --bg3:    #111722;   /* Section break — used sparingly */
  --card:   #171E2B;   /* Card surface */
  --card2:  #1D2537;   /* Elevated card */

  /* Brand teal — used selectively, not everywhere */
  --teal:   #0ABFCC;
  --teal2:  #089AAA;   /* Hover state */
  --mint:   #0ABFCC;   /* Alias */

  /* Governance accent — FAO / AI Governance page only */
  --amber:  #C68B0A;
  --amber2: #F0A500;

  /* Status — semantic only */
  --green:  #22C55E;
  --red:    #EF4444;

  /* Text */
  --txt:    #E2E8F0;   /* Warm near-white — headings */
  --txt2:   #64748B;   /* Muted slate — body (WCAG AA on --bg: 4.52:1) */
  --txt3:   #374151;   /* Tertiary labels */

  /* Borders — white-alpha, never teal-alpha */
  --border: rgba(255,255,255,0.07);
  --bh:     rgba(255,255,255,0.14);   /* Hover border */
  --glow:   rgba(255,255,255,0.04);   /* Hover surface tint */

  /* Gradients — restricted to one use: nav CTA gradient is also BANNED */
  --grad:       linear-gradient(135deg,#0891b2,#0ABFCC);   /* DO NOT USE on buttons */
  --grad-amber: linear-gradient(135deg,#C68B0A,#F0A500);   /* FAO page accent only */

  /* Layout */
  --ff:    "Poppins", sans-serif;
  --nav-h: 64px;
  --max:   1240px;
}
```

**Rules:**
- Borders use `rgba(255,255,255,…)` — never `rgba(10,191,204,…)` on neutral borders
- `--grad` is never used as a button background. Solid `var(--teal)` only.
- `--amber` used only on the AI Governance page CTA. Nowhere else.

---

## 3. Typography

### Flagship pages (index.html, ai-engineering-governance.html)
These pages use editorial, thin-weight heroes:
```css
h1 { font-size: clamp(56px,7vw,96px); font-weight: 300; color: var(--txt); }
h1 strong { font-weight: 700; }   /* emphasis WITHOUT gradient */
```

### Content pages (all other pages)
```css
h1 { font-size: clamp(28px,4vw,48px); font-weight: 700; color: var(--txt); line-height: 1.2; }
h2 { font-size: clamp(22px,3vw,36px); font-weight: 700; color: var(--txt); line-height: 1.3; }
h3 { font-size: 18px; font-weight: 600; color: var(--txt); }
body { font-size: 16px; font-weight: 400; color: var(--txt2); line-height: 1.7; }
```

### Rules
- **NO gradient text** (`-webkit-text-fill-color: transparent` / `background-clip: text`) on any heading, stat, or label.
- **NO `font-weight: 800` or 900** on content page H1. Max is 700.
- Use `<strong>` inside headings for emphasis — not `.grad-text` spans.
- Eyebrow labels: `font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase`

---

## 4. Buttons

### Canonical button system (3 classes only)

```css
/* Base */
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--ff); font-size: 15px; font-weight: 700;
  padding: 13px 28px; border-radius: 8px;
  cursor: pointer; transition: background .2s, transform .2s, border-color .2s;
  text-decoration: none;
}

/* Primary — solid teal, dark text */
.btn.btn-fill { background: var(--teal); color: #070B10; border: none; }
.btn.btn-fill:hover { background: var(--teal2); transform: translateY(-1px); }

/* Secondary — transparent with border */
.btn.btn-ghost { background: transparent; color: var(--txt); border: 1px solid var(--bh); }
.btn.btn-ghost:hover { background: var(--glow); border-color: rgba(255,255,255,.25); }

/* Governance CTA — amber, FAO page only */
.btn.btn-amber { background: var(--amber2); color: #070B10; border: none; }
.btn.btn-amber:hover { background: var(--amber); transform: translateY(-1px); }
```

### Rules
- **NO `background: var(--grad)` on any button.** Solid `var(--teal)` only.
- **NO `border-radius: 100px` on any button.** Max is `8px`.
- **NO `box-shadow` teal glow** on any button or its hover state.
- **NO `transform: translateY(-2px)`** — max lift is `-1px`.
- Page-specific button classes (`.btn-p`, `.btn-cta`, `.btn-ind-pri`) are legacy — treat them as `.btn.btn-fill` equivalent.
- Page-specific ghost classes (`.btn-o`, `.btn-ghost`) are legacy — treat as `.btn.btn-ghost` equivalent.

### Nav CTA (exception — scoped to nav only)
```css
.nav-cta { background: var(--teal); color: #070B10; border-radius: 8px; padding: 10px 22px; }
.nav-cta:hover { background: var(--teal2); transform: translateY(-1px); }
```

---

## 5. Badges / eyebrows

One canonical badge. Used above hero H1 and section labels.

```css
.badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(10,191,204,0.08);
  border: 1px solid rgba(10,191,204,0.18);
  color: var(--teal);
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 6px;   /* flat rect, NOT pill */
}
```

**Rules:**
- `border-radius: 6px` — never `100px`, never `20px`
- Background is a very subtle teal tint — not full opacity
- Status indicators (Live/Coming soon) follow the same shape with green/teal fill
- **Inline status in hero** (replacing `.hub-status-live`):
  ```css
  background: rgba(74,222,128,0.08); border-color: rgba(74,222,128,0.2); color: #4ade80; border-radius: 6px;
  ```

---

## 6. Cards

One canonical card. All cards on all pages use this spec.

```css
/* Base card */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 24px 28px;
  transition: border-color .2s;
}
.card:hover { border-color: var(--bh); }

/* Semantic accent variant — for use-case / feature cards */
.card.accent-teal  { border-left: 3px solid var(--teal); }
.card.accent-amber { border-left: 3px solid var(--amber); }  /* FAO page only */
```

**Rules:**
- `border-radius: 10px` — never 14px, 16px, 18px, 20px, 24px
- Hover: `border-color: var(--bh)` — never teal glow, never `rgba(10,191,204,.3)`
- **NO gradient top-bar** `::before` with `background: var(--grad)` — banned
- **NO `box-shadow` on cards** of any kind
- **NO `transform: translateY()` on card hover** — max -1px if truly needed
- Elevated card (pricing featured): `background: var(--card2)` + `border-color: var(--bh)`

---

## 7. Stat display

Used in hero rows and proof sections.

```css
.stat-box {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 24px;
  text-align: center;
}
.stat-num {
  font-size: 2rem; font-weight: 800;
  color: var(--teal);   /* solid, NOT gradient */
}
.stat-lbl {
  font-size: .8rem; color: var(--txt2); margin-top: 4px;
}
```

**Rules:**
- Stat number colour: `var(--teal)` (solid) — never `background-clip: text` gradient
- Stat card `border-radius: 10px`

---

## 8. Navigation

Canonical 5-link nav. Identical across all 65 pages.

```css
nav {
  width: 100%; background: rgba(7,11,16,0.97);
  border-bottom: 1px solid var(--border);
  padding: 0 48px; height: var(--nav-h);
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 99;
}
.nav-logo img { height: 44px; }
.nav-links a { padding: 8px 16px; border-radius: 8px; font-size: 14px;
               font-weight: 500; color: var(--txt2); }
.nav-links a:hover { color: var(--txt); background: var(--glow); }
.nav-links a.active { color: var(--teal); }
.nav-cta { background: var(--teal); color: #070B10; padding: 10px 22px;
           border-radius: 8px; font-size: 14px; font-weight: 700; }
.nav-cta:hover { background: var(--teal2); transform: translateY(-1px); }
@media(max-width:768px) { nav { padding: 0 20px; } .nav-links { display: none; } }
```

**Active class per URL prefix:**

| URL prefix | Active link |
|---|---|
| `/ai-engineering-governance` | AI Governance |
| `/platform` | Products |
| `/industries` | Industries |
| `/insights`, `/kw/`, `/learn/`, `/compare/`, `/solutions/` | Resources |
| `/about` | About |

---

## 9. Sections & layout

```css
.section { padding: 80px 48px; }
.section + .section { border-top: 1px solid var(--border); }
.wrap { max-width: var(--max); margin: 0 auto; }

/* Section backgrounds — only 2 states per page */
/* Primary: var(--bg) */
/* Secondary: var(--bg3) — used ONCE per page for CTA or highlight section */
```

**Rules:**
- Max content width: `var(--max)` = `1240px`
- Section backgrounds alternate between `var(--bg)` and `var(--bg3)` — not `var(--bg2)` (too subtle to read)
- No radial-gradient overlays in hero sections
- No animated grid overlays (`::before` with `background-image: linear-gradient`)
- Footer background: `var(--bg)` — NOT `var(--bg2)` (looks too different on some pages)

---

## 10. CTA sections

End-of-page CTA block:

```css
.cta-section {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 64px 48px;
  text-align: center;
  margin: 64px 0;
}
.cta-section h2 { font-size: clamp(22px,3vw,36px); font-weight: 700; margin-bottom: 12px; }
.cta-section p  { color: var(--txt2); max-width: 540px; margin: 0 auto 28px; }
```

**Rules:**
- Background: `var(--card)` — NOT `linear-gradient(rgba(teal))` or `var(--bg2)`
- Border: `var(--border)` — NOT `rgba(10,191,204,.2)`
- Border-radius: `10px` — NOT `24px`

---

## 11. Footer

**Tagline (canonical):** `Govern Your AI. Then Build With It.`
**Sub-line:** `Enterprise-grade governance and agents, built for your org.`

```css
.footer-links a:hover { color: var(--teal); }
.footer-soc-btn:hover { background: rgba(10,191,204,0.10); border-color: rgba(10,191,204,0.28); color: var(--teal); }
.footer-copy a:hover  { color: var(--teal); }
```

---

## 12. Hero sections (content pages)

Pattern for all non-flagship hero sections (industry, kw, learn, compare, solutions):

```css
.hero { padding: 72px 48px 56px; border-bottom: 1px solid var(--border); }
/* No radial-gradient background */
/* No ::before grid overlay */
/* Badge above H1, H1 at weight 700, subtext in var(--txt2) */
```

---

## 13. Spacing & radius scale

| Use | Value |
|---|---|
| Button | `8px` |
| Badge/tag | `6px` |
| Card, panel | `10px` |
| Input field | `8px` |
| Status dot | `50%` (circle) |
| Pill — BANNED except status dot | — |

---

## 14. What is banned

These patterns existed in the old design and must NOT be reintroduced:

| Pattern | Why banned |
|---|---|
| `background: var(--grad)` on buttons | Gradient buttons = AI slop |
| `-webkit-background-clip: text` on headings | Gradient heading text = AI slop |
| `border-radius: 100px` on buttons | Consumer-grade pill = not enterprise |
| `border-radius: 20px+` on cards | Over-rounded = template-feel |
| `box-shadow: 0 Xpx Ypx rgba(10,191,204,…)` | Teal glow = AI slop |
| `::before` gradient top-bar on cards | Garish decoration |
| `background-image: linear-gradient(rgba(teal) 1px…)` grid overlay | Overused hero pattern |
| `radial-gradient(ellipse…rgba(teal))` in hero | Glowy = not authoritative |
| `transform: translateY(-2px)` card hover | Too dramatic |
| `border-color: rgba(10,191,204,.3)` on card hover | Teal glow via border |

---

## 15. Propagation scripts

| Script | Purpose |
|---|---|
| `propagate_design.py` | `:root`, nav CSS, nav HTML across all 65 pages |
| `fix_all.py` | Footer, grad-text, buttons, insights CSS injection |
| `apply_design_system.py` | Component-level consistency (badges, buttons, cards, stat numbers) across kw/, learn/, industries/ |

Run all three from `upcore-website/` after any system-level change.
