---
version: alpha
name: Upcore-Instrument — dark design system (V2)
status: SPECIFICATION — not yet implemented. `docs/DESIGN-SYSTEM.md` still describes the live site.
description: |
  A dark, high-contrast, instrumentation-grade system for an AI-governance company. The page floor is a
  cool near-black (#0A0C10) and elevation is built entirely from a five-step surface ladder — never from
  shadows or glows. One voltage: Upcore teal (#0ABFCC), which finally reaches AAA contrast now that it
  sits on dark. DM Sans carries display at weight 700 with tight negative tracking; JetBrains Mono carries
  every technical register — eyebrows, stat numbers, scores, prices, log lines, table data. The signature
  visual is Upcore's own governance console (the FAO Risk Monitor / Portfolio Dashboard widgets) promoted
  from page decoration to page chrome, the way Raycast promotes its command palette. Red/amber/green are
  reserved strictly for RAG risk status — not decoration — because RAG status is the product's own language.
  There are no mesh gradients, no glass blur, no glow orbs, and no weight-300 display type anywhere.

colors:
  primary: "#0ABFCC"
  primary-bright: "#22D3E0"
  primary-pressed: "#089AAA"
  on-primary: "#04070B"
  primary-wash: "rgba(10,191,204,0.08)"
  primary-wash-strong: "rgba(10,191,204,0.14)"
  primary-line: "rgba(10,191,204,0.28)"
  primary-line-strong: "rgba(10,191,204,0.45)"

  canvas-deep: "#05070A"
  canvas: "#0A0C10"
  surface: "#0F1218"
  surface-raised: "#151922"
  surface-overlay: "#1C212B"

  hairline: "#1E232C"
  hairline-strong: "#2B3240"

  ink: "#F5F7FA"
  body: "#C3CAD5"
  muted: "#8B95A5"
  faint: "#5C6675"
  disabled: "#3F4855"

  ok: "#4ADE80"
  ok-wash: "rgba(74,222,128,0.10)"
  ok-line: "rgba(74,222,128,0.28)"
  warn: "#FBBF24"
  warn-wash: "rgba(251,191,36,0.10)"
  warn-line: "rgba(251,191,36,0.28)"
  risk: "#F87171"
  risk-wash: "rgba(248,113,113,0.10)"
  risk-line: "rgba(248,113,113,0.28)"
  insight: "#A78BFA"
  insight-wash: "rgba(167,139,250,0.10)"

  grid-line: "rgba(10,191,204,0.045)"
  hero-halo: "rgba(10,191,204,0.055)"

typography:
  display-hero:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: "clamp(40px, 5.4vw, 64px)"
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: "-0.025em"
  display-xl:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: "clamp(32px, 4vw, 48px)"
    fontWeight: 700
    lineHeight: 1.06
    letterSpacing: "-0.02em"
  display-lg:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: "clamp(27px, 3.2vw, 36px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  display-md:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  title-lg:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.005em"
  title-md:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 17px
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: 0
  title-sm:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  body-lg:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: 0
  body-md:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: 0
  body-sm:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 13.5px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  caption:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0
  eyebrow-mono:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.14em"
    textTransform: uppercase
  label-mono:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: "0.06em"
  data-xl:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: "clamp(34px, 4vw, 44px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  data-lg:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
  data-md:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0
  code:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: 12.5px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  button:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 14.5px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: 0
  nav-link:
    fontFamily: "'DM Sans', sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0

rounded:
  none: 0px
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  pill: 9999px

spacing:
  2xs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  section: 96px
  section-lg: 128px

components:
  nav-bar:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    typography: "{typography.nav-link}"
    borderColor: "{colors.hairline}"
    height: 64px
  nav-cta:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 9px 18px
    height: 38px
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 22px
    height: 44px
  button-primary-pressed:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 22px
    height: 44px
    borderColor: "{colors.hairline-strong}"
  button-ghost:
    backgroundColor: transparent
    textColor: "{colors.body}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 18px
    height: 44px
  button-disabled:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.disabled}"
    rounded: "{rounded.md}"
  eyebrow:
    backgroundColor: transparent
    textColor: "{colors.primary}"
    typography: "{typography.eyebrow-mono}"
  section-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.body}"
    padding: "{spacing.section} {spacing.lg}"
  section-band-alt:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    padding: "{spacing.section} {spacing.lg}"
  stat-tile:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    typography: "{typography.data-lg}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    borderColor: "{colors.hairline}"
  stat-band:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    rounded: "{rounded.lg}"
    borderColor: "{colors.hairline}"
  feature-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    borderColor: "{colors.hairline}"
  feature-card-featured:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    borderColor: "{colors.primary-line}"
  console-panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    rounded: "{rounded.xl}"
    padding: 0px
    borderColor: "{colors.hairline-strong}"
  console-header:
    backgroundColor: "{colors.canvas-deep}"
    textColor: "{colors.muted}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.none}"
    padding: 13px 18px
  console-row:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 11px 14px
    borderColor: "{colors.hairline}"
  console-row-alert:
    backgroundColor: "{colors.risk-wash}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 11px 14px
    borderColor: "{colors.risk-line}"
  status-pill-ok:
    backgroundColor: "{colors.ok-wash}"
    textColor: "{colors.ok}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.sm}"
    padding: 3px 9px
  status-pill-warn:
    backgroundColor: "{colors.warn-wash}"
    textColor: "{colors.warn}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.sm}"
    padding: 3px 9px
  status-pill-risk:
    backgroundColor: "{colors.risk-wash}"
    textColor: "{colors.risk}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.sm}"
    padding: 3px 9px
  log-block:
    backgroundColor: "{colors.canvas-deep}"
    textColor: "{colors.muted}"
    typography: "{typography.code}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
    borderColor: "{colors.hairline}"
  accordion-item:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    rounded: "{rounded.lg}"
    borderColor: "{colors.hairline}"
  accordion-trigger:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    padding: 20px 24px
  pricing-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
    borderColor: "{colors.hairline}"
  pricing-card-featured:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.xl}"
    borderColor: "{colors.primary-line-strong}"
  testimonial-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
    borderColor: "{colors.hairline}"
  input-text:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px 14px
    height: 46px
    borderColor: "{colors.hairline-strong}"
  input-text-focus:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    borderColor: "{colors.primary}"
  badge-solid:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.sm}"
    padding: 4px 10px
  badge-outline:
    backgroundColor: "{colors.primary-wash}"
    textColor: "{colors.primary}"
    typography: "{typography.eyebrow-mono}"
    rounded: "{rounded.sm}"
    padding: 4px 10px
    borderColor: "{colors.primary-line}"
  chip-mono:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.body}"
    typography: "{typography.label-mono}"
    rounded: "{rounded.xs}"
    padding: 4px 9px
    borderColor: "{colors.hairline}"
  data-table:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.lg}"
    borderColor: "{colors.hairline}"
  proof-strip:
    backgroundColor: "{colors.canvas-deep}"
    textColor: "{colors.muted}"
    typography: "{typography.label-mono}"
    padding: "{spacing.md} {spacing.lg}"
    borderColor: "{colors.hairline}"
  cta-band:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.display-xl}"
    padding: "{spacing.section} {spacing.lg}"
    borderColor: "{colors.hairline}"
  footer:
    backgroundColor: "{colors.canvas-deep}"
    textColor: "{colors.muted}"
    typography: "{typography.body-sm}"
    padding: "{spacing.3xl} {spacing.lg}"
    borderColor: "{colors.primary-line}"
  quiz-option:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 18px
    borderColor: "{colors.hairline-strong}"
  quiz-option-selected:
    backgroundColor: "{colors.primary-wash-strong}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 16px 18px
    borderColor: "{colors.primary}"
---

## Overview

**Upcore-Instrument** is a dark, high-contrast system for a company that sells governance over other people's AI. Its central conceit: *the marketing site should look like the instrument panel the product produces.* Upcore already builds the right assets for this — the FAO Risk Monitor, the Governance Dashboard, the Portfolio Dashboard, the 10-dimension radar, the scored PDF report. In the current light system those are decorations parked in a hero's right column. In V2 they become the page's chrome, the way Raycast's command palette is Raycast's chrome.

The system has **one surface mode: dark.** The page floor is a cool near-black `{colors.canvas}` (#0A0C10) and elevation is built from a five-step surface ladder rather than shadows — on a dark canvas there is no luminance headroom *below* a surface, so a drop shadow has almost nothing to cast into. Every reference system that ships a serious dark mode (Raycast, Composio) reaches the same conclusion independently, and so does Material's dark-theme guidance: on dark, **elevation is brightness, not shadow.**

There is **one voltage**: Upcore teal `{colors.primary}` (#0ABFCC). This is the single most important finding behind V2 — see *The contrast case for dark* below.

Type runs **DM Sans at weight 700** for display with tight negative tracking, and **JetBrains Mono for the entire technical register**: eyebrows, stat numbers, scores, prices, table data, log lines. Putting numbers in mono is the highest-leverage "reads engineered, not AI-generated" move in the system, and it costs one font file Upcore already loads on `/lp/governance-index`.

Red / amber / green appear only as **RAG risk status**. This is not a decorative choice — RAG severity coding *is* the product's language, the same vocabulary a CISO reads all day in Wiz, Datadog, and Snyk. Because the risk colors are earned, the system can stay otherwise monochrome-plus-teal without feeling starved.

**Key characteristics**
- Five-step surface ladder (`canvas-deep` → `canvas` → `surface` → `surface-raised` → `surface-overlay`); zero drop shadows except one overlay tier for menus and modals.
- Brand teal reaches **8.80:1** on the dark canvas — AAA for body text. It reaches **2.25:1** on white, which is why the current light system needs a compromise teal.
- DM Sans 700 display with −1.5% to −2.5% tracking. **Weight 300 display type is banned** — it is the current site's single strongest "generic AI startup" tell.
- JetBrains Mono carries every number and every technical label.
- CTAs are **8px squares, not pills.** Pills are for badges only.
- The governance console is the hero chrome. No mesh gradients, no glassmorphism, no glow orbs, no isometric illustration, no emoji icons.
- One restrained atmospheric element: a 72px teal blueprint grid at 4.5% alpha, plus a single ≤5.5% teal halo behind hero console mockups. Nothing else.

---

## The contrast case for dark

This is the research finding that should drive the decision, not taste.

| Pairing | Ratio | WCAG |
|---|---|---|
| `#0ABFCC` on `#FFFFFF` (**today's brand teal on today's canvas**) | **2.25:1** | ✗ fails everything |
| `#077F8C` on `#FFFFFF` (today's compromise teal-text token) | 4.75:1 | ✓ AA small text, ✗ AAA |
| **`#0ABFCC` on `#0A0C10`** (V2) | **8.80:1** | ✓✓ AAA small text |
| `#04070B` on `#0ABFCC` (V2 primary button) | 8.77:1 | ✓✓ AAA |

The live site cannot use its own brand color as text. `docs/DESIGN-SYSTEM.md` already documents `--teal-text: #077F8C` as an "AA-compliant darker teal for text on white" — a muddier, greener, off-brand color that exists purely to work around the failure in row 1. Every teal headline, link, and label on the site today is either that compromise color or an accessibility violation.

Inverting the canvas resolves this at the root. **Dark is not a restyle here; it is the first background on which Upcore's brand color is legally usable as text.**

Verified text-ladder ratios against `{colors.canvas}` (#0A0C10):

| Token | Hex | Ratio | Permitted use |
|---|---|---|---|
| `{colors.ink}` | #F5F7FA | ~17.1:1 | Headlines, high-emphasis |
| `{colors.body}` | #C3CAD5 | **11.86:1** | Default running text |
| `{colors.muted}` | #8B95A5 | **6.47:1** | Captions, metadata, labels — **lowest tier allowed for small text** |
| `{colors.faint}` | #5C6675 | **3.37:1** | ✗ Not for body copy. Large text (≥24px), dividers, decorative rules, disabled affordances only |
| `{colors.ok}` | #4ADE80 | 11.23:1 | Status |
| `{colors.warn}` | #FBBF24 | 11.73:1 | Status |
| `{colors.risk}` | #F87171 | 6.83:1 | Status |

`{colors.faint}` is deliberately kept in the palette despite failing AA for small text, because a five-step text ladder is needed for dense console UI — but **its constraint is a rule, not a suggestion.** Any small-text use of `faint` is a bug.

**Note on pure white.** `{colors.ink}` is #F5F7FA, not #FFFFFF. Pure white on near-black produces halation — the perceived bleed of light glyphs into a dark field — which measurably degrades reading comfort and is significantly worse for readers with astigmatism. Raycast (#f4f4f6) and Composio (#ffffff for display only, #a8a8a8 for body) both back off pure white for sustained reading. Do not "fix" the off-white to #fff.

---

## Colors

### Brand voltage
- **Upcore Teal** (`{colors.primary}` — #0ABFCC) — primary CTA fill, eyebrows, active states, data-viz strokes, focus rings. The only chromatic color permitted on chrome.
- **Teal Bright** (`{colors.primary-bright}` — #22D3E0) — hover/active lift on dark. One notch up, never a second brand color.
- **Teal Pressed** (`{colors.primary-pressed}` — #089AAA) — pressed state; carried over unchanged from V1.
- **On Primary** (`{colors.on-primary}` — #04070B) — near-black text on teal fills. Never white-on-teal: white on #0ABFCC is 2.4:1 and fails.
- **Washes and lines** — `{colors.primary-wash}` (8%) for tinted card fills, `{colors.primary-wash-strong}` (14%) for selected states, `{colors.primary-line}` (28%) for tinted borders, `{colors.primary-line-strong}` (45%) for featured-card rings.

### Surface ladder
Elevation runs one direction only: **up**. A surface never gets darker to signal lift.

| Token | Hex | Role |
|---|---|---|
| `{colors.canvas-deep}` | #05070A | Inset wells — log blocks, code, console headers, footer, proof strip |
| `{colors.canvas}` | #0A0C10 | Page floor |
| `{colors.surface}` | #0F1218 | Cards, alternating section bands |
| `{colors.surface-raised}` | #151922 | Nested panels, inputs, secondary buttons, console rows |
| `{colors.surface-overlay}` | #1C212B | Menus, dropdowns, tooltips, active table rows |

The canvas is a *cool* near-black (a touch of blue), not neutral gray-black. Teal is a cool hue; a warm or perfectly neutral dark fights it and reads cheaper. The blue cast is subtle enough to never register as "blue," but it makes the teal sit correctly.

### Hairlines
- `{colors.hairline}` (#1E232C) — the structural workhorse. Every card edge, every divider.
- `{colors.hairline-strong}` (#2B3240) — inputs, secondary buttons, console panel outer edge, table rules.

### Semantic — RAG risk status
These are **product vocabulary, not decoration.** They may appear on status pills, console rows, severity indicators, and data visualization. They may never be used as a general accent, a section background, or a CTA.

- **OK / Governed** — `{colors.ok}` #4ADE80 + `{colors.ok-wash}` + `{colors.ok-line}`
- **Review / Warning** — `{colors.warn}` #FBBF24 + washes
- **Risk / Blocked / Critical** — `{colors.risk}` #F87171 + washes
- **Insight / Optimisation** — `{colors.insight}` #A78BFA + wash. Preserves V1's documented violet-is-insight semantic, distinct from risk severity.

These are the dark-tuned counterparts of V1's `--green` / `--amber` / `--red` / `--violet`. **The existing dark widgets on the live site already use almost exactly these values** (`#4ade80` / `#fbbf24` / `#f87171` in the FAO Explorer) — meaning the site's dark components already speak V2's semantic palette and survive migration nearly untouched.

### Atmospheric
Two tokens, both deliberately near-invisible:
- `{colors.grid-line}` — rgba(10,191,204,0.045). A 72px blueprint grid. Reads as schematic paper, not as decoration.
- `{colors.hero-halo}` — rgba(10,191,204,0.055). A single soft radial behind hero console mockups. **Capped at 5.5% alpha and permitted once per page.**

That's the entire decorative system. If a third atmospheric effect seems necessary, the layout is the problem.

---

## Typography

### Families
**DM Sans** — display, headings, body, UI. Retained from V1 deliberately: the current site's typographic problem is not the typeface, it is that the typeface is set at **weight 300 at 40–66px**, which is the most-copied hero treatment in AI-SaaS marketing and the single loudest generic signal on the site. DM Sans at 700 with tight tracking reads confident and editorial. Keeping it also preserves brand continuity and costs zero migration risk.

**JetBrains Mono** — the technical register. Already loaded on `/lp/governance-index`, so this is a font Upcore ships today.

> **The one open brand question.** If Upcore wants to go further than V2, the move is DM Sans → **Inter** or **Geist** for a harder engineering register (wider weight range, better small-size hinting, true tabular figures). That is a brand-identity decision, not a design-system decision, and it should be made deliberately and separately. V2 is specified to work either way — swapping the display family is a one-line `--ff` change if the weights and tracking are preserved.

### Hierarchy

| Token | Size | Weight | LH | Tracking | Use |
|---|---|---|---|---|---|
| `{typography.display-hero}` | clamp(40→64) | 700 | 1.04 | −0.025em | Hero H1 — one per page |
| `{typography.display-xl}` | clamp(32→48) | 700 | 1.06 | −0.02em | Section titles, CTA band |
| `{typography.display-lg}` | clamp(27→36) | 700 | 1.10 | −0.015em | Sub-section titles |
| `{typography.display-md}` | 28 | 700 | 1.15 | −0.01em | Card-group heads |
| `{typography.title-lg}` | 20 | 700 | 1.30 | −0.005em | Panel titles |
| `{typography.title-md}` | 17 | 700 | 1.35 | 0 | Card titles, accordion triggers |
| `{typography.title-sm}` | 15 | 600 | 1.40 | 0 | List labels, form labels |
| `{typography.body-lg}` | 17 | 400 | 1.65 | 0 | Hero subhead, lead paragraphs |
| `{typography.body-md}` | 15 | 400 | 1.65 | 0 | Default body |
| `{typography.body-sm}` | 13.5 | 400 | 1.60 | 0 | Card body, console rows |
| `{typography.caption}` | 12 | 500 | 1.50 | 0 | Footnotes, disclaimers |
| `{typography.eyebrow-mono}` | 11 | 600 | 1.40 | 0.14em ᴜᴘ | **Section eyebrows, status pills, badges** |
| `{typography.label-mono}` | 12 | 500 | 1.50 | 0.06em | Chips, table headers, metadata |
| `{typography.data-xl}` | clamp(34→44) | 700 | 1.00 | −0.02em | Headline stat numbers, scores |
| `{typography.data-lg}` | 28 | 700 | 1.00 | −0.01em | Stat-tile numbers, prices |
| `{typography.data-md}` | 16 | 600 | 1.40 | 0 | Inline data, table figures |
| `{typography.code}` | 12.5 | 400 | 1.60 | 0 | Log lines, code, terminal |
| `{typography.button}` | 14.5 | 600 | 1.00 | 0 | Button labels |
| `{typography.nav-link}` | 14 | 500 | 1.40 | 0 | Nav |

### Principles

1. **Display is always 700.** No 300, no 400, no 800. One confident weight.
2. **Tracking tightens as size grows** — −0.025em at hero, −0.01em at 28px, 0 at body. Every reference system does this; it is what separates "designed" from "default."
3. **Every number is mono.** Scores, percentages, prices, counts, dates, durations, dimension values. If a user could compare it to another number, it is `data-*` or `label-mono`. This is the system's defining texture.
4. **Eyebrows are mono, uppercase, 0.14em tracked, teal.** They label sections like a spec sheet. They replace V1's `.eyebrow` DM Sans treatment.
5. **Enable `font-variant-numeric: tabular-nums`** on every `data-*` token so figures align in columns and don't jitter during count-up animation.

---

## Layout

### Spacing
Base unit 4px. `{spacing.2xs}` 4 · `{spacing.xs}` 8 · `{spacing.sm}` 12 · `{spacing.md}` 16 · `{spacing.lg}` 24 · `{spacing.xl}` 32 · `{spacing.2xl}` 48 · `{spacing.3xl}` 64 · `{spacing.section}` 96 · `{spacing.section-lg}` 128.

Section bands run `{spacing.section}` (96px) vertical — down from V1's 100px, aligning to the 4px grid and matching all four reference systems, which independently converged on 96px. Flagship hero and final CTA bands may use `{spacing.section-lg}` (128px).

### Grid & container
- Content max-width **1240px**, gutters 24px mobile / 48px desktop. Carried from V1 unchanged.
- Console mockups may run wider (~1080px) inside a full-bleed band.
- Card grids: 4-up → 2-up (1024px) → 1-up (768px). Feature grids 3-up → 1-up.
- Footer 5-col → 2-col (1024px) → 1-col (768px).

### Band rhythm
The page alternates `{component.section-band}` (canvas) and `{component.section-band-alt}` (surface) — a **two-tone rhythm**, not a light/dark whiplash. Sections are separated by the tone step plus a `{colors.hairline}` rule, never by a decorative divider. The blueprint grid runs continuously across every band so the page reads as one continuous instrument surface.

---

## Elevation & depth

| Level | Treatment | Use |
|---|---|---|
| −1 Recessed | `{colors.canvas-deep}` | Log blocks, code, console headers, footer, proof strip |
| 0 Floor | `{colors.canvas}` | Page background |
| 1 Card | `{colors.surface}` + 1px `{colors.hairline}` | Every standard card |
| 2 Raised | `{colors.surface-raised}` + 1px `{colors.hairline-strong}` | Inputs, secondary buttons, console rows, nested panels |
| 3 Overlay | `{colors.surface-overlay}` + `0 16px 40px rgba(0,0,0,0.55)` | **Only** menus, dropdowns, modals, tooltips |
| Featured | Level 1 or 2 + 1px `{colors.primary-line-strong}` ring | Featured pricing tier, selected quiz option |

**Level 3 is the only shadow in the system.** Everything else is brightness. A card that needs to "pop" gets a teal ring, not a glow.

**Explicitly banned:** teal-tinted drop shadows, `box-shadow` glows on buttons, `backdrop-filter: blur()` glassmorphism, and multi-stop mesh gradients. All four are the visual signature of template-built AI marketing sites and all four are what the brief means by "AI-looking."

> This bans the teal glow-shadow that was added to `/ai-operations` buttons. That page is V2's closest ancestor but predates this spec; when it migrates, the glow comes off and the pill CTAs square down to 8px.

---

## Shapes

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | 0 | Full-bleed bands, nav, footer, console header |
| `{rounded.xs}` | 4 | Mono chips, inline tags |
| `{rounded.sm}` | 6 | Status pills, badges, table cells |
| `{rounded.md}` | **8** | **All buttons**, inputs, small cards, quiz options |
| `{rounded.lg}` | 12 | Feature cards, pricing cards, accordions, stat bands |
| `{rounded.xl}` | 16 | Console panels, hero mockup containers |
| `{rounded.pill}` | 9999 | **Badges only — never CTAs** |

### The pill decision
V1 sets every CTA at `border-radius: 9999px`. V2 moves them to **8px**, and this is the second-largest visual change in the system after the canvas inversion.

The reasoning is consistent across the reference set: Expo — *"Don't use full pills on CTAs — pills are for badges only."* Composio — *"Compact pill geometry: CTAs sit at 8px, not full pills — developer-tool dialect."* Raycast ships 8px buttons. Vercel is the lone exception, using pills for marketing CTAs while keeping 6px squares for app chrome — and explicitly treats the shape difference as *"a deliberate signal of which surface you're on."*

Fully-rounded CTAs read consumer/friendly; tight-radius CTAs read tool/engineered. For a company selling audit trails to CISOs, the tight radius is the correct register. **This change touches every button on ~70 pages** and should be sequenced as its own commit.

---

## Components

> Hover states are documented where they carry meaning; otherwise only default and pressed/active are specified, matching the reference-set convention.

### Navigation

**`nav-bar`** — `{colors.canvas}`, 64px, 1px bottom `{colors.hairline}`, sticky. Logo left; `{typography.nav-link}` links in `{colors.body}` (→ `{colors.ink}` on hover); `{component.nav-cta}` right. Structurally unchanged from V1 — the current nav is already dark and already correct. **This is the single biggest migration win: the nav and footer blocks that are duplicated across all ~70 pages barely change.**

**`nav-cta`** — teal fill, `{colors.on-primary}` text, 8px radius, 38px. The one solid teal element above the fold on every page.

### Buttons

**`button-primary`** — `{colors.primary}` fill, `{colors.on-primary}` text, `{rounded.md}`, 44px height, 12×22 padding. Pressed → `{colors.primary-pressed}`. **No shadow, no glow.** Max one per viewport fold.

**`button-secondary`** — `{colors.surface-raised}` fill, `{colors.ink}` text, 1px `{colors.hairline-strong}`. The paired action next to primary.

**`button-ghost`** — transparent, `{colors.body}` text, no border. Tertiary/inline actions.

**`button-disabled`** — `{colors.surface-raised}` fill, `{colors.disabled}` text.

### Eyebrow

**`eyebrow`** — `{typography.eyebrow-mono}` in `{colors.primary}`. Uppercase, 0.14em tracked, monospace. Optionally prefixed with a 6px teal square (not a dot — squares read schematic, dots read decorative). Every major section opens with one.

### Console — the signature component

The system's load-bearing visual. Promotes V1's `.gov-dash` / `.fao-explorer` / `.rm-*` widgets from hero garnish to page chrome.

**`console-panel`** — `{colors.surface}`, 1px `{colors.hairline-strong}`, `{rounded.xl}`, padding 0. Composed of a header strip, a row stack, and an optional footer bar.

**`console-header`** — `{colors.canvas-deep}` strip, `{typography.eyebrow-mono}` in `{colors.muted}`, 13×18 padding, square corners against the panel's rounded top. Carries a label plus a status dot. **The dot is static, never animated, and the label always reads "— EXAMPLE"** — V1 already fixed a credibility bug where static mockups claimed "Live"; that fix is now a system rule.

**`console-row`** — `{colors.surface-raised}`, 1px `{colors.hairline}`, `{rounded.md}`, 11×14. Layout: icon + name + `{typography.body-sm}` detail on the left, `{component.status-pill-*}` on the right. **`console-row-alert`** swaps fill to `{colors.risk-wash}` and border to `{colors.risk-line}`.

**`status-pill-ok` / `-warn` / `-risk`** — wash fill, semantic text color, `{typography.eyebrow-mono}`, `{rounded.sm}`. Labels are terse and uppercase: `ACTIVE` · `REVIEW` · `BLOCKED` · `SCANNING`.

**`log-block`** — `{colors.canvas-deep}`, 1px `{colors.hairline}`, `{typography.code}` in `{colors.muted}`, `{rounded.md}`. Carries the timestamped operational log lines already written for the FAO Explorer. Timestamps in `{colors.faint}` (large-enough, decorative — permitted).

### Data display

**`stat-tile`** — `{colors.surface}`, 1px `{colors.hairline}`, `{rounded.lg}`, 24px. Number in `{typography.data-lg}` `{colors.primary}`, label in `{typography.body-sm}` `{colors.muted}`. **`stat-band`** joins 3–4 tiles into one rounded container divided by `{colors.hairline}` rules — the treatment already prototyped on `/ai-operations`.

**`data-table`** — `{colors.surface}`, `{rounded.lg}`, header row in `{typography.label-mono}` `{colors.muted}` on `{colors.canvas-deep}`, body rows separated by `{colors.hairline}`, numeric cells in `{typography.data-md}` with tabular figures. Active row lifts to `{colors.surface-overlay}`. Used for pricing comparison and framework matrices.

**Data visualization** — the radar chart, score dials, and dimension bars inherit `{colors.primary}` stroke at full opacity, `{colors.primary-wash}` fill, `{colors.hairline-strong}` grid rings, and `{colors.muted}` axis labels. Peer-average markers use `{colors.faint}` (decorative — permitted). **On dark, the existing radar becomes substantially more legible than it is on white** — its teal-on-white fill is currently the weakest element on both landing pages.

### Cards

**`feature-card`** — `{colors.surface}`, 1px `{colors.hairline}`, `{rounded.lg}`, 24px. Optional 3px `{colors.primary}` left accent bar. **`feature-card-featured`** steps to `{colors.surface-raised}` with a `{colors.primary-line}` border.

**`pricing-card`** / **`pricing-card-featured`** — 32px padding, `{rounded.lg}`. Prices in `{typography.data-lg}`. Struck comparison rows use `{colors.faint}` with line-through; the Upcore row uses `{colors.primary}`. Featured tier is distinguished by the `{colors.primary-line-strong}` ring **and nothing else** — no scale transform, no shadow, no ribbon.

**`testimonial-card`** — `{colors.surface}`, 1px `{colors.hairline}`, `{rounded.lg}`. Quote in `{typography.body-md}` `{colors.body}`, attribution in `{typography.caption}` `{colors.muted}`, source link in `{colors.primary}`. Retains V1's 6-line clamp + Read more toggle.

**`accordion-item`** — `{colors.surface}`, 1px `{colors.hairline}`, `{rounded.lg}`. Trigger in `{typography.title-md}` `{colors.ink}` with a teal `+` that rotates 45° when open. Open item's border brightens to `{colors.hairline-strong}`. Used for the 5-layer framework and every FAQ.

### Forms

**`input-text`** — `{colors.surface-raised}`, 1px `{colors.hairline-strong}`, `{rounded.md}`, 46px, `{colors.ink}` text, `{colors.faint}` placeholder. **`input-text-focus`** — border becomes `{colors.primary}` plus a 3px `{colors.primary-wash}` outer ring. Focus is always visible and always teal; never remove the outline.

**`quiz-option` / `quiz-option-selected`** — the landing-page quiz answer buttons. Selected state fills `{colors.primary-wash-strong}` with a full `{colors.primary}` border. 44px+ tap target guaranteed.

### Badges & chips

**`badge-solid`** — teal fill, near-black mono text. High emphasis, sparingly.
**`badge-outline`** — `{colors.primary-wash}` fill, teal text, teal-line border. The default badge.
**`chip-mono`** — `{colors.surface-raised}`, `{colors.body}`, `{typography.label-mono}`, `{rounded.xs}`. Tool names, tech tags, kit contents.

### Bands

**`proof-strip`** — `{colors.canvas-deep}`, `{typography.label-mono}` `{colors.muted}`, hairline top and bottom. Certifications and ratings, dot-separated.

**`cta-band`** — `{colors.surface}` with hairline top, `{typography.display-xl}` in `{colors.ink}`, one `{component.button-primary}`, reassurance line in `{typography.caption}` `{colors.muted}`.

**`footer`** — `{colors.canvas-deep}` with a 3px `{colors.primary-line}` top rule (carried from V1). Column heads in `{typography.eyebrow-mono}` `{colors.muted}`; links in `{colors.muted}` → `{colors.ink}` on hover.

---

## Long-form reading surface

**This is the system's one honest concession, and it should not be hand-waved.**

The evidence on dark mode and reading is genuinely mixed and ambient-light-dependent: dark mode measurably helps readers with astigmatism and in low light, and measurably *hurts* sustained reading performance for readers without astigmatism in bright ambient light — which describes a CFO reading a 2,000-word article on a corporate laptop in a lit office. Upcore has ~30 long-form pages (`insights/`, `learn/`, `kw/`, `compare/`, plus `privacy` and `terms`) where sustained reading is the entire job.

Two defensible options:

**Option A — Reading surface (recommended).** Long-form pages keep the dark chrome (nav, footer, proof strip) but set the article body in a `{colors.surface}` well with `{typography.body-lg}` at `{colors.body}` on a 68ch measure. Same system, one tuned context. Legal pages use the same treatment.

**Option B — Dark-only.** Simpler and more striking; matches Raycast and Composio, both of which are dark-only marketing sites — but note that both keep their *documentation* on a separate surface. Accept a real readability cost on the article corpus.

Recommendation: **A.** The marketing spine gets the full dark instrument treatment; the reading corpus gets the same system at a reading-tuned contrast. Decide this before migration starts, because it changes the page inventory.

---

## Do's and Don'ts

### Do
- Build elevation from the surface ladder. Brightness up, never shadow down.
- Use `{colors.primary}` for exactly one solid CTA per fold.
- Set every number in `{typography.data-*}` or `{typography.label-mono}` with tabular figures.
- Open every section with a mono uppercase `{component.eyebrow}`.
- Anchor heroes with a `{component.console-panel}` showing real Upcore output.
- Label every mockup "— EXAMPLE" with a static status dot.
- Keep display type at weight 700 with negative tracking.
- Reserve RAG colors for genuine severity states.
- Keep focus rings teal, visible, and never removed.

### Don't
- Don't set display type at weight 300. This is the current site's loudest generic tell.
- Don't use full pills on CTAs. Pills are badges only.
- Don't add drop shadows, teal glows, or `backdrop-filter` blur.
- Don't introduce a mesh gradient or a second atmospheric effect.
- Don't use RAG colors as decoration, section fills, or CTAs.
- Don't put white text on teal (2.4:1 — fails). Teal fills take `{colors.on-primary}`.
- Don't use `{colors.faint}` for small body text (3.37:1).
- Don't set `{colors.ink}` to pure #FFFFFF — halation is a real cost.
- Don't animate status dots or claim "Live" on static mockups.
- Don't add a second brand color. If the page feels flat, the fix is contrast and layout, not hue.

---

## Responsive behavior

| Breakpoint | Width | Changes |
|---|---|---|
| Ultrawide | 1440px+ | Container caps 1240px; gutters grow to 64px |
| Desktop | 1240px | Full grids, horizontal nav |
| Laptop | 1024px | 4-up → 2-up; console panel narrows, stays intact |
| Tablet | 768px | Nav → drawer; all grids 1-up; section padding 96 → 64px |
| Mobile | 480px | Hero clamps to 40px; console collapses to 3 representative rows; padding → 48px |

- **Touch targets:** buttons 44px, inputs 46px, quiz options 56px+ — all at or above WCAG AAA.
- **Console on mobile:** truncate to three rows plus a mono summary line. Do not shrink to illegibility; do not hide entirely (V1 hid its dashboard below 768px and lost its strongest trust signal on ~60% of traffic).
- **Tables:** horizontal scroll at tablet, one-card-per-column stack at mobile.
- **Blueprint grid:** fixed 72px at every breakpoint — it should not scale.

---

## Migration path

Realistic sequencing for a static, no-build repo where `:root`, `<nav>`, and `<footer>` are duplicated across ~70 pages.

1. **North-star page.** Build V2 on one flagship — `ai-engineering-governance.html` is the right candidate (it exercises nearly every component: console, accordion, stat band, pricing, case-study cards, FAQ). Sign off on the real thing before any propagation.
2. **Codify tokens** in the canonical `:root` in `index.html`, keeping V1 token names as aliases so nothing breaks mid-migration.
3. **Wave 1 — spine:** `index`, `ai-engineering-governance`, `ai-adoption-strategy`, `platform`, `pricing`, `about`, `contact`.
4. **Wave 2 — secondary product:** `sdlc-agent`, `agent-builder`, `fde-engineers`, `security`, `assessment`, `industries/*`.
5. **Wave 3 — long-form** under the reading-surface decision above.
6. **Wave 4 — landing pages.** ⚠️ **`lp/governance-index` and `lp/ai-maturity-index` carry live paid ad spend.** Migrate them last, deliberately, with full quiz-flow QA and a `lead-magnet-engine.js` cache-buster bump. A broken email gate here costs real money per hour, unlike a broken marketing page.
7. **Contrast audit.** Automated pass over every token pairing actually used, against the ratios table above. Every `faint`-on-small-text instance is a bug.
8. **Doc sync.** `DESIGN-SYSTEM.md` → superseded pointer; `CHANGELOG.md`; add V2-migrated pages to the `propagate_design.py` SKIP set as they land.

**Effort:** the token layer is a day. The north-star page is 2–3 days. Propagation is mechanical but wide — the real cost is per-page QA, not per-page CSS.

---

## Known gaps

- **Not implemented.** This is a specification; no page renders it yet. Every ratio in this document is computed from the WCAG 2.x relative-luminance formula, not measured in a browser. Re-verify in-browser during the north-star build.
- **DM Sans vs. Inter/Geist** is deliberately left open as a brand decision (see Typography).
- **Reading-surface Option A vs. B** must be decided before migration starts.
- **Motion** is out of scope. V1's count-up and SVG draw-in animations are assumed to carry over; they need a `prefers-reduced-motion` audit that V1 never had.
- **Illustration** is undefined beyond console mockups and data-viz. If Upcore ever needs a non-console visual, the system has no answer yet — and inventing one casually is exactly how the "AI-looking" problem returns.
- **Light mode does not exist** and is not planned. Email templates and the generated PDF report remain light and are governed separately — the PDF's teal-on-white is a *print* surface where the contrast math differs.
