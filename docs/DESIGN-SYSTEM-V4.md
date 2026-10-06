# Upcore Design System V4.1 — "Enterprise Editorial"

Status: **live on dev** (2026-10-06) at `/`, `/ai-native-engineering`, `/who-we-help/*`. Supersedes `DESIGN-SYSTEM-V3.md` and the older V1/V2 docs for those pages.

> **V5 "Flow" layer (2026-10-06).** After review feedback ("too boxy, too many rounded rectangles, repetitive"), the V4 pages now load a second layer, [`css/upcore-v5.css`](../css/upcore-v5.css) + [`js/upcore-v5.js`](../js/upcore-v5.js), with components in [`tools/v4-build/flow.py`](../tools/v4-build/flow.py). Rules of the Flow layer:
> - **No boxes.** Containers have no background, border or radius; hairlines (`--hair`, ink top rules) carry structure. Radii are flattened globally (`--r-sm..--r-xl` = 4–10px). Only the primary CTA keeps its pill shape; avatars and nodes stay circular.
> - **One thread.** A cyan spine draws down the left margin with scroll (≥1360px); each section's eyebrow is a numbered stage (`01`, `02`…, a CSS counter) with a dot on the spine.
> - **No two sections share a layout.** Hero flowline (SVG pipeline with travelling tickets and a held-for-approval branch, decision log beneath), trust marquee, strike-through comparison (`.sk`), sticky scrollytelling pipeline with a big stage counter, horizontal timeline (`.tl`) + open pilot spec + pod line, proof rows with count-up numbers + crossfading pull quote (`.qc`), open framework stage (diagrams on canvas, no panels), logo streams (`.mq-row` marquees), typographic index rows with hover sweep (`.ix`), flagship line, open controls grid, sticky-side FAQ, CTA band with flowing lines.
> - **Dark bands are full-bleed** (`.band--flow`), never inset slabs, with a thin cyan seam at the top edge.
> - **Motion:** heading word-mask reveals, scroll-drawn spine, flowline tickets, marquees, count-ups, timeline draw, strike-through, quote crossfade, CTA line streams. Everything pauses off-screen, has a pause control where it loops, and is static under `prefers-reduced-motion`.
> - Where this file and the Flow layer disagree about layout or containers, the Flow layer wins; tokens, type, colour and framework visuals below still apply.

Source of truth for code: [`css/upcore-v4.css`](../css/upcore-v4.css) (one shared stylesheet) and [`js/upcore-v4.js`](../js/upcore-v4.js) (one vanilla motion layer). There is no per-page `:root` block any more. Pages link both files with a `?v=N` cache-buster, which must be bumped when either changes.

## Principles
1. **White editorial canvas, deep petrol bands.** Light sections carry reading; `.band` (petrol navy `#071A26`) carries product proof, controls and the final CTA.
2. **One accent: Upcore cyan.** `--cyan #21D2ED` for fills and glows, `--cyan-ink #0A6F82` for cyan text on white (5.6:1), `--cyan-2 #7DE6F6` for cyan text on dark. No second brand colour. Amber (human approval) and violet (AI step) appear only as tiny status dots.
3. **Enterprise type.** Geist for everything, Geist Mono for labels and data. Weights 400/500/600 only. No novelty display faces.
4. **Calm scale.** Hero tops out at 70px, H2 at 40px, body 16px.
5. **Motion explains, never decorates.** Every animation shows a process (work flowing, a loop running, autonomy being earned, waiting being removed). All motion stops under `prefers-reduced-motion`, and every visual has a text alternative.
6. **Every claim traceable.** Industry stats carry source links; frameworks cite their research lineage; client results are anonymized and from the engagement record.

## Tokens (see `:root`)
| Group | Tokens |
|---|---|
| Surfaces | `--canvas #FFF`, `--paper #F6F8F9`, `--stone #EEF2F4`, `--stone-2`, `--band #071A26`, `--band-2`, `--band-3` |
| Ink | `--ink #0A1419`, `--ink-2 #34434B`, `--muted #5D6B73` (5.2:1), `--hair`, `--hair-2`, `--on-band`, `--on-band-2` |
| Accent | `--cyan`, `--cyan-2`, `--cyan-ink`, `--cyan-wash`, `--cyan-glow` |
| Markers | `--amber` (human), `--violet` (AI) |
| Radius | `--r-sm 8`, `--r-md 14`, `--r-lg 20`, `--r-pill` |
| Motion | `--ease-out cubic-bezier(.16,1,.3,1)`, durations `.18 / .4 / .8s` |

## Type scale
`.t-hero` 38–70px · `.t-display` 32–52px · `.t-h2` 27–40px · `.t-h3` 18.5–21px · `.t-h4` 16.5px · `.t-lead` 16.5–18px · `.eyebrow` 11.5px mono uppercase. Headings use `text-wrap:balance`.

## Components
Chrome: `.progress` (scroll bar), `.annc`, `.nav` (+ `.drop` mega-menu, mobile `.menu-open`), `.foot`, `.mcta` (sticky mobile CTA, leaves room for the chat bubble).
Buttons: `.btn` (ink pill + cyan arrow disc), `.btn--cyan` (on dark), `.btn--sm`, `.btn-pulse`, `.link`, `.chip` (`--human`, `--ai`, `--auto`).
Sections: `.sec`, `.sec--paper`, `.sec-head` / `--split`, `.band` / `--rounded` with `.spot` (cursor spotlight) + `.grid-bg`.
Hero: `.hero` + `.hero-glow` (faded drifting cyan/blue gradient over a masked dot grid; replaced the particle canvas on 2026-10-06), `.badge` flagship pill, `[data-split]` word reveal (CSS animation on load, no observer, for fast LCP), `.hero-stage--eng` with `.run` (governed-change pipeline demo, `[data-flow]`) and `.dlog` (deviation-log mock, labelled Example view).
Content: `.rows/.row` (editorial outcome rows), `.cards/.card/.card--ink`, `.wf` (numbered workflows), `.ba` (before/after), `.stats/.stat` + `.sources`, `.path`, `.tabs/.tabpanel`, `.proc` (scroll-filled process), `.cred`, `.people`, `.ctrl` (enterprise controls grid), `.faq`, `.cta-band` + `.mesh`.
Segment hero: `.hero--split` + `.flow` (`[data-flow]` animated workflow steps).

## AI-Native Engineering components (flagship, 2026-10-06)
AI-Native Engineering is the primary offering: first item in the nav (`a.flag`), flagship tag in the Solutions menu, homepage hero, and a full-width `.flag-card` in the services grid (`.disc`).
`.vs` vibe-coding vs AI-native comparison table · `.pipe` nine-stage pipeline rail (`[data-pipe]`, fills on scroll; `.pipe--compact` on the homepage) · `.dlog` deviation log + risk pills `.risk.hi/.md/.lo` · `.pod` lean-pod cards · `.split` + `.ticks` · `.rows-label` grouped proof rows.

## Logos
- **Accolades:** light-surface variants live in `images/accolades/light/` (white text recoloured to ink, brand colours kept). Use these on white; the originals are for dark surfaces.
- **Tools and integrations:** brand marks from Simple Icons (CC0 paths). Each page embeds one hidden SVG sprite containing only the icons it uses (`<symbol id="i-slug">`), referenced by `<use>`. `.logo` tiles show monochrome and reveal the brand colour on hover; `.logo--sm` is used in strips and inside dark bands. `.stack` (categorised rows) and `.tool-strip` ("Connects to") are the two layouts. Every logo wall carries the trademark disclaimer: compatibility, not partnership.

## Page build
V4 pages are generated by the Python files in [`tools/v4-build/`](../tools/v4-build/) (committed 2026-10-06, not deployed): `chrome.py` (shared head/nav/footer, URL map, tracking head, `LIVE` flag, cache-busters `V`/`CHAT_V`/`CTA_V`), `build_v41.py` (home + AI-Native Engineering), `segments.py` + `segment_copy.py` (who-we-help pages), `v4parts.py` (trust strip, testimonials, FAQ, CTA band), `frameworks.py` (Upcore frameworks) and `tools.py` (tool logos from `si/icons.json`). Run from the repo root: `python tools/v4-build/build_v41.py && python tools/v4-build/segments.py`. `LIVE = True` writes final paths with canonical/index and the GTM-only tracking head; `LIVE = False` writes noindex previews under `/preview/`. Never hand-edit the generated HTML.

**Consent banner & Cookie settings:** `.consent` (bottom-left card, Decline/Accept equal width) and the footer `.foot-link[data-consent-open]` button; script at the end of `js/upcore-v4.js`. Behaviour: [TRACKING.md §4](TRACKING.md#4-consent-consent-mode-v2).

**Copy facts used across V4 pages:** pod role "Claude Certified Architect" (every Upcore architect holds the certification); pilot duration and commercials are agreed on the discovery call; discovery calls are led by Gaurav or Saswata (no title or surname published for Saswata until confirmed).

## Upcore frameworks (custom visuals)
Built by `frameworks.py` (generator, kept outside the repo) into static HTML; animated by `js/upcore-v4.js` via a `.play` class.
| Framework | Discipline | Visual | Lineage cited on page |
|---|---|---|---|
| Automation Fit Matrix | Strategy | `.mx` 2x2, volume × rule-clarity, dots fly to position | Hayes & Wheelwright, HBR 1979 |
| Agent Control Loop | Computer science | `.lp` sense→reason→act→verify→learn ring with human gate | Kephart & Chess, IEEE Computer 2003 |
| Autonomy Ladder | Behavioural science | `.ld` L0–L4 bars; evidence meter promotes the agent | Parasuraman, Sheridan & Wickens 2000; Lee & See 2004 |
| Lead-time Compression | Operations science | `.cp` work vs waiting bars collapse to the reported result | Little, Operations Research 1961 |
| The effort principle | Consumer behaviour | `.ef` customer steps before/after + effort meter | Dixon, Freeman & Toman, HBR 2010 |
Homepage shows four as an auto-advancing tab suite (`[data-fw]`, pauses on hover, stops on click). Segment pages show one each (`.fw-single`): ecommerce → effort, operations-heavy → compression, professional services → ladder, tech → loop.

## Motion rules (post-audit)
- State class for running steps is `is-run` (never `run`; `.run` is the hero panel).
- Every looping region pauses off-screen (`.is-off`), when the tab is hidden, and via its Pause button (`.run-toggle`). Loops settle: CTA pulse twice, then rest.
- Animate `transform`/`opacity`/`clip-path` only. The spotlight moves via `translate3d`, the pipeline fill via `scaleY(--pp)`, the ladder meter via `scaleX(--ev)`.
- Framework panels are stacked in one grid cell (`.fw-stage`) so tab changes never shift the page; autoplay is off on touch and stops on focus.
- Reveal travel 14px, 0.7s, `--ease-out`. Hero items animate on load (no opacity fade) so the LCP is not delayed. The headline word reveal waits for fonts (`.fonts-ready`, 700ms cap).
- Surfaces: one dark color (`--band`) for bands, footer, announcement and flagship card. Rounded bands float with equal inset. Consecutive white sections share a hairline (no paper/grey sections).

## Accessibility & performance checklist
- Contrast: all text tokens ≥ 4.5:1 on their surface; focus ring `--focus`.
- Each animated visual has `role="img"` + `aria-label`; tabs are real `role="tab"` with arrow-key support.
- Canvas pauses off-screen and on hidden tabs; DPR capped at 2.
- Reduced motion: transitions/animations disabled, canvas hidden, all states shown final.
- Two font families from Google Fonts (Geist, Geist Mono), `display=swap`.
