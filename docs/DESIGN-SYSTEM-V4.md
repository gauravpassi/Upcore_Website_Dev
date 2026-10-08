# Upcore Design System V4.1 — "Enterprise Editorial"

Status: **live on dev** (2026-10-06) at `/`, `/ai-native-engineering`, `/who-we-help/*`. Supersedes `DESIGN-SYSTEM-V3.md` and the older V1/V2 docs for those pages.

> **V5 "Flow" layer (2026-10-06).** After review feedback ("too boxy, too many rounded rectangles, repetitive"), the V4 pages now load a second layer, [`css/upcore-v5.css`](../css/upcore-v5.css) + [`js/upcore-v5.js`](../js/upcore-v5.js), with components in [`tools/v4-build/flow.py`](../tools/v4-build/flow.py). Rules of the Flow layer:
> - **No boxes.** Containers have no background, border or radius; hairlines (`--hair`, ink top rules) carry structure. Radii are flattened globally (`--r-sm..--r-xl` = 4–10px). Only the primary CTA keeps its pill shape; avatars and nodes stay circular.
> - **One thread.** A cyan spine draws down the left margin with scroll (≥1360px); each section's eyebrow is a numbered stage (`01`, `02`…, a CSS counter) with a dot on the spine.
> - **No two sections share a layout.** Hero flowline (SVG pipeline with travelling tickets and a held-for-approval branch, decision log beneath), trust marquee, strike-through comparison (`.sk`), sticky scrollytelling pipeline with a big stage counter, horizontal timeline (`.tl`) + open pilot spec + pod line, proof rows with count-up numbers + crossfading pull quote (`.qc`), open framework stage (diagrams on canvas, no panels), logo streams (`.mq-row` marquees), typographic index rows with hover sweep (`.ix`), flagship line, open controls grid, sticky-side FAQ, CTA band with flowing lines.
> - **Dark bands are full-bleed** (`.band--flow`), never inset slabs, with a thin cyan seam at the top edge.
> - **Motion:** heading word-mask reveals, scroll-drawn spine, flowline tickets, marquees, count-ups, timeline draw, strike-through, quote crossfade, CTA line streams. Everything pauses off-screen, has a pause control where it loops, and is static under `prefers-reduced-motion`.
> - **Calm pages (homepage, /results):** after "information overload" feedback these drop the spine and stage numbers (`spine=False, main_cls='is-calm'` in `chrome.write`) and use the `h-`/`r-` block at the end of `upcore-v5.css`: at most 8 sections, about 120 words per section, one primary action, artifacts (the animated PR gate, mini checkpoint mockups) instead of paragraphs. New and rebuilt pages should follow the calm pattern.
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

**Navigation island (2026-10-07, calmer 2026-10-08). Desktop (≥1101px):** `.nav` is a near-opaque dark floating pill (`data-island`; no backdrop blur, which made scrolling heavy) that floats over the hero. At the top of a page it shows the full menu; after a deliberate scroll down (90px, or 140px back up to expand) it morphs into a compact pill with the logo, a reading-progress ring (`.nav-ring`), "Menu" and the CTA. It never shows section names. Scrolling up, hovering, focusing or clicking the pill expands it again; dropdowns grow out of it in the same dark style. **Below 1101px (phones and tablets)** it is a fixed-size floating pill, logo and menu button, that never changes size while scrolling, so the page can't jump. The menu button grows the island into a dark sheet from the button's corner (`clip-path` circle, page dimmed behind, chat launcher hidden): "On this page" chips for the page's titled sections (`.nav-here`, built by the script; current section highlighted; tapping one closes the sheet and scrolls there; hidden when a page has fewer than two), the menu with Solutions and Who we help expanding inline, then the page's CTA and Contact / Security / Email links (`.nav-sheet-foot`). `chrome.nav(active, cta=(href, label, slug))` sets the CTA in both the bar and the sheet for pages whose CTA isn't the booking modal (the quiz pages, /ai-operations). Scroll work runs once per frame and reads only a cached page height. CSS: the `island` block in `upcore-v5.css` (also copied into the generated `css/upcore-chrome.css`); JS: "Navigation island" in `upcore-v5.js`; markup: `chrome.nav()`. Sticky positioning needs the page's `html` overflow left visible (clip sections instead), or the island scrolls away.

**Scroll reveals (2026-10-08):** `[data-reveal]` content settles with a short fade and an 8px rise (the `smooth` block); section headings fade in like everything else instead of sliding in word by word.
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
V4 pages are generated by the Python files in [`tools/v4-build/`](../tools/v4-build/) (committed 2026-10-06, not deployed): `chrome.py` (shared head/nav/footer, URL map, tracking head, `LIVE` flag, cache-busters `V`/`CHAT_V`/`CTA_V`), `build_home.py` (homepage), `build_aine.py` (AI-Native Engineering), `build_results.py`, `build_about.py` (About), `build_security.py`, `build_contact.py`, `build_gov.py` (AI Governance), `build_bpa.py` (Business Process Automation, `/platform`), `build_fao.py` (Fractional AI Officer), `build_404.py`, `build_guide.py` + `build_compare.py` (article pages, layout in `article.py`), `build_insights.py` (the Insights hub), `build_all.py` (runs every builder), `calm.py` (shared calm-page parts: heroes, section heads, results band, FAQ, final CTA), `segments.py` + `segment_copy.py` (who-we-help pages), `v4parts.py` (trust strip, testimonials, FAQ, CTA band), `frameworks.py` (Upcore frameworks) and `tools.py` (tool logos from `si/icons.json`). Run from the repo root: `python tools/v4-build/build_home.py && python tools/v4-build/build_aine.py && python tools/v4-build/segments.py`. `LIVE = True` writes final paths with canonical/index and the GTM-only tracking head; `LIVE = False` writes noindex previews under `/preview/`. Never hand-edit the generated HTML.

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
