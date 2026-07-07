# Changelog

Append-only log of features, decisions, and non-obvious facts. Most-recent on top. Each entry is a date + a short stanza. Keep it terse — link to commits/PRs/files for detail.

Format:
```
## YYYY-MM-DD — short title
**Type:** feature | fix | decision | infra | content
**Files:** key paths touched
What changed and why (1–3 sentences). Anything future-Claude should know.
```

---

## 2026-07-03 — Governance CTAs open calendar modal; other CTAs stay on /assessment
**Type:** feature
**Files:** `chat-widget.js`, all `.html` files
AI-governance CTAs ("Book a Governance Review", "Start Your 72-Hour Onboarding") now open an inline iframe modal with the Google Calendar booking page — no external redirect. All other CTAs ("Book a Discovery Call", "Free AI Assessment", etc.) continue to link to /assessment. Modal built lazily on first click, closes on ×, backdrop click, or Escape. Added ?v=2 cache-bust to chat-widget.js script tag across all 65 pages so the new modal code loads immediately.

---

## 2026-07-03 — No em dashes, calendar CTAs, bigger logo (site-wide)
**Type:** fix
**Files:** all `.html` files (67+)
Removed all em dashes site-wide (replaced with ` - ` inline or `- ` for attributions). Changed all `href="/assessment"` CTA links (319 instances) to point directly to the Google Calendar booking link. Enlarged nav logo from 48px to 60px height across all pages.

---

## 2026-07-03 — Homepage design improvements — proof stats, Bridge CTA, connectors, addon icons
**Type:** feature
**Files:** `index.html`
Added 3-column crisis proof stats block to Problem section (45% exploitable / $4.7M breach cost / 0 named owners). Added "Book a Governance Review →" CTA with reassurance copy to Bridge section. Added teal `→` step connectors to How It Works cards (desktop only, inside top-right of each non-last card). Added emoji icons to agent add-on cards. Converted Gauntlet section to light theme (`var(--bg2)`) and added AIGOV Gauntlet section between FAO and Bridge.

---

## 2026-07-03 — FAO section redesign — dark theme, outcome bullets, 2-col layout
**Type:** fix
**Files:** `index.html`
Replaced the white "cutout" FAO section with a full dark `#070B10` treatment. Moved eyebrow + H2 inside the layout grid column (eliminated standalone section-title above the grid). Removed the generic 2×2 stat card grid and replaced with 4 outcome-specific bullet rows (fao-wins). Updated left-column CTA to "Book a Governance Review →" (primary, /assessment) and "See the Framework →" (ghost). New description copy focuses on the concrete problem: AI-generated code shipping unreviewed. Section is visually cohesive with the FAO Explorer accordion and ribbon already in place.

---

## 2026-07-03 — UI/UX audit quick wins — CTA standardization + design system fixes
**Type:** fix
**Files:** `index.html`, `about.html`, `contact.html`, `ai-engineering-governance.html`, 61 subdirectory pages
Implemented all 8 quick wins from the PART 4 UI/UX audit: (1) nav CTA standardized to "Book a Governance Review" across all 65 pages; (2) index.html hero primary CTA now "Book a Governance Review →" → /assessment; secondary becomes "See the Framework →"; (3) auto-expands first framework layer (Align) on governance page load; (4) removed banned `.grad-text` CSS and fixed `font-weight:900→700` in about.html; (5) added "See X Suite →" links to all 3 industry addon cards; (6) de-risking copy already present under governance page CTAs; (7) added attribution to hero hook quote — CTO, Series B Fintech; (8) added "–73% risk exposure" outcome label to ribbon SVG chart at Day 90 endpoint.

---

## 2026-07-03 — FAO section proper redesign — two-column accordion layout (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the 3-dark-block "Governance Intelligence Dashboard" (score ring + 3-pane command widget) with the site's canonical two-column layout. Left: prose + 5 layer pills + 4 stat cards (`var(--bg2)` light style, matching site) + CTAs. Right: `.fao-explorer` dark accordion with 5 expandable rows (L1–L5), each revealing capability bullets + timestamped log entry + compliance tags; L3 pre-opens on load; L2 amber REVIEW state; L3 red SCANNING/alert state. Pills on hover highlight matching accordion row via teal outline. Ribbon below unchanged (4 stats + SVG risk-decline chart). Removed all score-ring, layer-bar, and packet-animation JS; replaced with `toggleLayer()` accordion function + DOMContentLoaded pre-open + new pill hover. Zero console errors.

---

## 2026-07-03 — FAO "Governance Intelligence Dashboard" full redesign (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the entire FAO section with a 3-layer visual dashboard. (1) Intro row: text/pills/CTAs left + dark governance score ring card right (CSS `@property` conic-gradient, animates to 94/100 on scroll, with 3 mini progress bars). (2) Full-width 3-pane dark command widget: layer coverage bars with IntersectionObserver fill animation; SVG architecture diagram with 5 nodes (L3 pulsing red via SMIL `<animate>`, 3 animated packets via `@keyframes`, scan sweep line); auto-scrolling live activity feed (CSS `feed-scroll` animation, 12 entries × 2 duplicated sets for seamless loop). (3) Dark ribbon: 4 stats (72h / Day 30 / 19 / 5, two count-up on scroll) + SVG risk-decline curve (stroke-dashoffset draw on scroll). Subtle teal dot-grid `::before` on section background. Zero console errors; all brand tokens preserved.

---

## 2026-07-03 — FAO section visual framework redesign (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the plain 3-stat card in the FAO section right column with a dark "FAO Governance Pipeline" widget — 5 connected layer nodes (L1–L5) with status badges, L3 Protect in active SCANNING state. Replaced 4 text bullets on the left with a 2×2 teal stat grid (5 / 72h / Day 30 / 19). Added vanilla JS: hovering a layer pill highlights the matching pipeline node. No new hex values; reuses `#0a0a0a` and `blink` keyframe from existing tokens.

---

## 2026-07-02 — CTA button standardization: all primary buttons now black pill site-wide
**Type:** fix
**Files:** 14 `learn/*.html`, `compare/*.html`, `solutions/*.html` pages (btn-p size); 12 `industries/*.html` (btn-ghost border-radius)
Primary CTA buttons were inconsistent across 5 class families (btn-fill, btn-p, btn-cta, btn-teal, btn-primary) with 3 distinct visual treatments: black pill on main pages, teal squircle on industry/insights, undersized pill on learn/compare/solutions. Industry+insights pages were already fixed in a prior pass. This pass normalizes: (1) `.btn-p` in 14 learn/compare/solutions pages from `padding:11px 24px; font-size:14px` → `padding:12px 26px; font-size:15px`. (2) `.btn-ghost` on all 12 standard industry pages from `border-radius:8px; padding:13px 28px` → `border-radius:9999px; padding:12px 26px` so secondary pills match the primary. Canonical standard: `background:#0a0a0a · color:#fff · padding:12px 26px · border-radius:9999px · font-size:15px · font-weight:600`. Script: `fix_cta_buttons.py`.

---

## 2026-07-02 — Full-site consistency audit: governance cross-links, content fixes, CTA standardization
**Type:** fix | content
**Files:** `about.html`, `platform.html`, `sdlc-agent.html`, `assessment.html`, `contact.html`, `kw/manufacturing-ai-agents.html`, `kw/index.html`, `platform/ai-agent-builder.html`, `platform/custom-ai-agents.html`, `platform/30-day-deployment.html`, `platform/on-premise-deployment.html`, `insights/banking-ai-customer-service.html`, `learn/enterprise-ai-strategy.html`, `learn/ai-data-governance.html`, all 12 `industries/*.html` pages
Multi-pass site-wide consistency audit. Key changes: (1) **about.html** — governance-first hero H1, added FAO as 4th product card in 2×2 grid, stats updated ("48hrs"→"72h", "3 Core Products"→"4 Products"), hero CTA "Work With Us"→"Book a Discovery Call", meta/schema updated. (2) **platform.html** — hero H1 updated to governance framing, Studio tab now has booking CTA. (3) **Governance cross-links** — teal callout box added before CTA on all 12 industry pages and 3 platform sub-pages; Decision 5 in enterprise-ai-strategy.html and ai-data-governance.html both now link to /ai-engineering-governance. (4) **CTA fixes** — manufacturing KW page CTAs changed /contact→/assessment; assessment.html button "Schedule My Assessment"→"Book My Discovery Call"; success message "You're on the list!"→"Request received."; placeholder names Rahul/Sharma→Alex/Smith; Studio Templates CTA label fixed. (5) **SEO** — banking article canonical URL changed from upcore.tech/insights/banking/ to upcoretech.com/insights/; ai-agent-builder meta description completed. (6) **Content fixes** — "48 hours"→"72 hours" throughout about.html; sdlc-agent "0 Developers Needed"→"0 Dev Handover Cycles"; sdlc schema offers.url /contact→/assessment; artefacts→artifacts in on-premise and ai-data-governance; contact response time inconsistency fixed; kw/index.html planning stats removed. (7) **Copyright** — 41 files updated 2025→2026.

---

## 2026-07-01 — Full design overhaul: MiniMax white-canvas system (65 pages)
**Type:** feature | fix
**Files:** all 65 HTML pages, `apply_minimax.py` (new), `fix_flagships.py` (new), `docs/DESIGN-SYSTEM.md`
Flipped the entire site from dark charcoal to a MiniMax-adapted white-canvas system. Key changes: (1) **Colors**: `--bg:#ffffff`, `--txt:#0a0a0a`, `--border:#e5e7eb` — fully light. (2) **Font**: Poppins → DM Sans (weights 300/400/500/600/700). (3) **Nav**: dark-glass `rgba(7,11,16,0.97)` → white `#ffffff`; CTA teal/8px → black `#0a0a0a`/9999px pill. (4) **Buttons**: `.btn-fill` teal → black, `.btn-ghost` white-alpha → ink outline, all `8px` → `9999px` pill. (5) **Cards**: `10px` → `16px`, `rgba(0,0,0,.06)` shadow hover, teal left-borders removed. (6) **Badges/pills**: `6px` → `9999px` site-wide. (7) **Footer**: kept dark `#0a0a0a`; text forced to `rgba(255,255,255,…)` since `--txt` is now dark. (8) **Hero strong**: `color:#fff` → `color:var(--txt)` on 3 flagship pages (was invisible on white bg). `apply_minimax.py` handles 60 template pages idempotently; `fix_flagships.py` patches the 5 uniquely-formatted flagship pages. Both scripts re-runnable safely.

---

## 2026-07-01 — Design system enforcement: upcore-design.md + apply_design_system.py
**Type:** fix | infra
**Files:** `upcore-design.md` (new), `apply_design_system.py` (new), 45+ HTML pages, `industries/index.html`, `kw/index.html`, `platform/custom-ai-agents.html`, `platform/on-premise-deployment.html`, `kw/real-estate-ai-workforce.html`, `docs/DESIGN-SYSTEM.md`
Defined a comprehensive 15-section design system in `upcore-design.md` (single source of truth) and enforced it site-wide. `apply_design_system.py` patched 42 content pages (kw/, learn/, industries/, compare/, solutions/) in one pass. Key changes: badge border-radius 20px/100px → 6px; button gradient fills → solid `var(--teal)`; button border-radius 100px → 8px; card border-radius 16-20px → 10px; card hover teal glow → `border-color:var(--bh)`; gradient `::before` top-bars removed → left-border accent; stat number gradient text → `color:var(--teal)`; hero radial-gradient + grid overlay removed; teal box-shadows removed. Manual patches: `industries/index.html` (unique `.eyebrow`/`.hub-card`/`.btn-primary` template), `kw/index.html` (unique `.hub-badge`/`.hub-stat-num`/`.res-card` template), `platform/custom-ai-agents.html` (`.step-num`), `platform/on-premise-deployment.html` (`.arch-card::before`), `kw/real-estate-ai-workforce.html` (`.case-metric-num`). Final state: 0 gradient fills on buttons, 0 pill badges, 0 teal glow shadows on any content page.

---

## 2026-07-01 — Full site visual redesign: Palantir/Anduril aesthetic (charcoal-neutral system)
**Type:** feature | fix
**Files:** all 65 HTML pages, `docs/DESIGN-SYSTEM.md`, `propagate_design.py`, `fix_all.py`
Overhauled the entire site from "AI slop" navy/teal-glow to a Palantir/Anduril-inspired charcoal-neutral dark mode. Changes propagated to all 65 HTML files via Python scripts with zero manual per-page edits. Key changes: (1) **Color system**: backgrounds shifted from blue-navy (`#07101e`) to charcoal-neutral (`#070B10`); borders switched from teal-alpha to white-alpha (`rgba(255,255,255,0.07)`); amber governance accent added (`--amber`/`--amber2`); text lightened to warm `#E2E8F0`. (2) **Typography**: gradient text (`.grad-text`) banned on all H1/H2 — replaced with `font-weight:300` H1 + `<strong>` for emphasis; 14 `grad-text` instances removed across secondary pages. (3) **Nav**: 7 links → 5 links (`AI Governance`, `Products`, `Industries`, `Resources`, `About`); `backdrop-filter:blur` removed; height 72px → 64px; CTA changed from gradient to solid teal. (4) **Buttons**: 6+ old classes collapsed to 3 — `.btn.btn-fill`, `.btn.btn-ghost`, `.btn.btn-amber`. (5) **Cards**: border-radius 20px → 10px; teal glow shadows removed; gradient top-bars removed; left-border accent adopted for semantic cards. (6) **Insights articles**: all 15 article files had no `:root` block — injected canonical tokens + `ARTICLE_BASE_CSS`. (7) **Footer**: tagline updated to "Govern Your AI. Then Build With It." across all pages. Final audit: ALL CLEAR — 0 issues across 65 files.

---

## 2026-07-01 — Pivot: AI Engineering Governance (Fractional AI Officer) as new flagship
**Type:** feature | content | decision
**Files:** `ai-engineering-governance.html` (new), `index.html`, `platform.html`, `api/chat.js`, `chat-widget.js`, `sitemap.xml`, `vercel.json`, all ~65 non-demo pages (nav), `sdlc-agent.html`, `industries/compliance-governance.html`, `learn/ai-data-governance.html`
Positioned **AI Engineering Governance** — delivered via a **Fractional AI Officer (FAO)** — as Upcore's new flagship offering, added *alongside* the kept agent-building business (softer pivot, all existing SEO pages retained). Source of truth = the FAO decks (V8b latest). What shipped: (1) New flagship page `/ai-engineering-governance` (built from `sdlc-agent.html` shell) — crisis stats, documented incidents (Moltbook, CVE-2025-48757, Amazon), the-gap two-column, the FAO solution, 5-layer/19-capability framework, hire-vs-Big4-vs-FAO economics, 90-day journey, FAQ; Service + FAQPage JSON-LD. (2) Homepage: FAO added as first product card in `#products` + crisis stat panel, hero "New" announcement link, title/meta/OG rewritten, Organization `knowsAbout` expanded. (3) Nav: added top-level **AI Governance** link (before Industries) — propagated to all ~65 non-demo pages via script, in sync per DESIGN-SYSTEM rule. (4) `platform.html`: added AI Governance as first product tab ("Four Products"), retitled. (5) Kai (`api/chat.js` SYSTEM_PROMPT): AIGOV/FAO added as lead offering with CTO/CISO/CFO framing; `chat-widget.js` suggested prompt added. (6) SEO: sitemap entry (0.9); redirects `/fractional-ai-officer`, `/aigov`, `/ai-governance` → `/ai-engineering-governance`. (7) Funnel-in cross-links from Forge + compliance-governance + ai-data-governance. Note: "AIGOV" is internal shorthand; market-facing names are "AI Engineering Governance" + "Fractional AI Officer". Stats carry deck sources (Gartner/Veracode/IBM/GitClear 2025, CVE-2025-48757). All pricing kept unpublished per convention.

---

## 2026-05-12 — Full SEO audit and remediation (61 pages)
**Type:** fix
**Files:** all 61 HTML pages, `docs/CHANGELOG.md`
Comprehensive site-wide SEO fix across two commits (19d4c1c, da15db8): (1) Fixed 24 broken internal links across 13 pages (wrong industry slugs, nested insight paths). (2) Added complete OG + Twitter meta tags to all 14 industries/ pages which had zero social meta. (3) Added og:image to 10 pages and twitter:card to 11 pages. (4) Trimmed all 50 meta descriptions that exceeded 160 chars (word-boundary trim + ellipsis). (5) Trimmed 16 page titles to ≤65 chars (keyword-preserving rewrites). (6) Added hreflang en + x-default to 5 pages. (7) Added JSON-LD to 19 pages with none: about (AboutPage), contact (ContactPage), assessment (WebPage), platform (WebPage), insights/index (CollectionPage), all 12 original industries/ pages (Service schema). (8) Added og:site_name to 17 pages. (9) Trimmed og:description to ≤155 chars on 33 pages. (10) Synced og:title + twitter:title with updated page titles. (11) Removed SVG `<title>Layer 1</title>` from index.html body. Final state: 61/61 pages pass all checks.

---

## 2026-05-12 — Three new learn/ pages: ai-in-banking, hipaa-compliant-ai, ai-workforce-platform
**Type:** content
**Files:** `learn/ai-in-banking.html`, `learn/hipaa-compliant-ai.html`, `learn/ai-workforce-platform.html`, `docs/FEATURES.md`
Added three substantive industry/compliance/category guide pages (50–57KB each). ai-in-banking covers front/middle/back office use cases, compliance architecture problem, and 8-row generic vs. custom AI comparison table. hipaa-compliant-ai covers 4 HIPAA rules applied to AI, 3-card failure modes, 4-step compliant architecture, 6 use cases, and an 8-item vendor checklist. ai-workforce-platform defines the category, 4-layer architecture, 8-row comparison table, 3-step Upcore methodology, and 4-audience buyer profiles. All include 8-question FAQ with Article + FAQPage JSON-LD, datePublished 2025-01-01, dateModified 2025-05-12.

## 2026-05-12 — Three new learn/ education pages: how-ai-agents-work, ai-agent-vs-llm, ai-agent-memory
**Type:** content
**Files:** `learn/how-ai-agents-work.html`, `learn/ai-agent-vs-llm.html`, `learn/ai-agent-memory.html`, `docs/FEATURES.md`
Added three substantive AI fundamentals pages (50–55KB each) targeting PAA queries: perception–reasoning–action architecture, LLM vs agent capability comparison (10-row table), and 4-type memory architecture (episodic/semantic/procedural/working). Each page has 8-question FAQ with Article + FAQPage JSON-LD, full internal link graph between learn/ pages and /platform/ destinations, and cross-links back to /assessment and /kw. Added A9 section to FEATURES.md documenting the learn/ hub pattern.

## 2026-05-08 — Directory structure + feature inventory added to docs
**Type:** infra
**Files:** `docs/STRUCTURE.md` (new), `docs/FEATURES.md` (new), `docs/README.md`, `CLAUDE.md`
Added two new source-of-truth docs: `STRUCTURE.md` (annotated directory tree + "where do new things go" map) and `FEATURES.md` (categorised feature inventory grouped A: static pages / B: forms / C: AI features / D: infra, plus cross-cutting contracts and a "how to add a new feature" decision tree). Documented current known gaps: contact form is inert, demo builder only supports 2 of 12 industries, two stale demo HTMLs exist while manifest is empty, duplicated `industries/upcore-logo.*` likely unused.

## 2026-05-08 — Source-of-truth docs introduced
**Type:** infra
**Files:** `docs/README.md`, `docs/DESIGN-SYSTEM.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/CHANGELOG.md`, `CLAUDE.md`
Created a `docs/` folder as the canonical reference for design tokens, architecture, and conventions. `CLAUDE.md` now points at this folder and instructs future Claude Code sessions to read it first and update it on any change.

## 2026-05-08 (pre-doc baseline) — State of the repo as captured
**Type:** decision
**Files:** repo-wide

Recorded for future reference; not new changes. The state below is what the docs were written against:

- **37 hand-authored HTML pages.** No build step, no framework, no `package.json`, no tests.
- **Design system duplicated across every page** (`:root` block + `<nav>` block). Recent commits (`Enforce pixel-perfect nav consistency across all 37 pages`, `Fix nav CSS damage from previous stripping pass`) had to repair drift — this is the known-fragile surface.
- **Two Vercel functions:** `api/chat.js` (Kai chatbot, model `claude-haiku-4-5-20251001`, max_tokens 600, 15s timeout) and `api/build-demo.js` (demo generator, 60s timeout, writes to `demos/` via the GitHub Contents API).
- **Demo Builder pipeline:** request → Anthropic → assemble HTML → commit to GitHub → Vercel auto-deploys → return URL → email lead notification via FormSubmit.
- **Daily cleanup cron** at 20:30 UTC (`.github/workflows/`) deletes expired demos based on `demos/manifest.json`. Bot user: `Upcore Demo Bot <demo-bot@upcore.ai>`.
- **`INDUSTRY_CONFIG` in `api/build-demo.js` currently supports only `manufacturing` and `ecommerce`.** Other industries have marketing pages but cannot be selected in the demo builder yet.
- **All forms + lead notifications go to `gaurav@upcoretechnologies.com`** via FormSubmit.co. No server-side form handler.
- **Chat widget (`chat-widget.js`)** is a single self-contained vanilla-JS IIFE included on all 37 non-demo pages.
- **Routing:** `cleanUrls: true`, plus redirects (`/blog → /insights`, `/about-us → /about`, `/contact-us → /contact`, `/home → /`) and rewrite `/industries/ecommerce → /industries/retail-d2c`. All in `vercel.json`.
- **Brand voice + product/industry list lives in `SYSTEM_PROMPT`** at the top of `api/chat.js` — the source of truth for what Kai says about Upcore.

---

<!-- Add new entries above this line. Do not delete old entries. -->
