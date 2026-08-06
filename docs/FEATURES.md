# Feature Inventory

Every user-facing feature in the site, plus the contracts that hold them together. **When you ship a new feature, add it here in the relevant section and add a one-line entry to [CHANGELOG.md](CHANGELOG.md) — same change.** Last full audit: 2026-05-08.

How each entry is structured:
- **What** — the feature in one line
- **Where** — files involved
- **Touches** — other parts of the system this feature depends on (env vars, external services, other pages)
- **Extend by** — what to do when adding to / modifying this feature

---

## A. Brand & marketing pages (static, no API)

These are pure HTML. To add a new one, follow the page-add checklist in [CONVENTIONS.md §3](CONVENTIONS.md#3-adding-a-new-page-checklist).

### A1. Homepage
- **What:** Hero, trust strip (animated marquee of accolade logos), product overview, industry grid, social proof, CTAs to Discovery Call + Demo Builder.
- **Where:** [`index.html`](../index.html)
- **Touches:** `images/accolades/*.svg`, `chat-widget.js`. Hosts the **canonical** `:root` and `<nav>` blocks (see [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)).
- **Extend by:** Hero/CTA copy edits go inline. New trust-strip logos: drop SVG into `images/accolades/` and add to the marquee track.

### A2. About
- **What:** Company story / team / mission.
- **Where:** [`about.html`](../about.html)
- **Touches:** Standard nav, chat widget.
- **Extend by:** Inline edits.

### A3. Platform overview
- **What:** "Four Products. One AI Partner." — index page that introduces AI Engineering Governance, Studio, Forge, and the broader platform (tabbed).
- **Where:** [`platform.html`](../platform.html)
- **Touches:** Cross-links to `ai-engineering-governance.html`, `agent-builder.html` (Studio) and `sdlc-agent.html` (Forge). If the product lineup changes, update this page **and** the chat widget's FAQ answers (`chat-widget.js`) together.

### A3b. AI Engineering Governance (FLAGSHIP)
- **What:** Flagship offering page — "The AI Code Crisis Is Already Inside Your Enterprise." Sells **AI Engineering Governance** delivered via a **Fractional AI Officer (FAO)**: governs the risk of AI-generated code (budget, security, compliance). Sections: crisis stats, documented incidents, the-gap comparison, FAO solution, 5-layer/19-capability framework, hire-vs-Big4-vs-FAO economics, 90-day journey, FAQ. Source of truth = the FAO decks.
- **Where:** [`ai-engineering-governance.html`](../ai-engineering-governance.html) (URL `/ai-engineering-governance`; redirects: `/fractional-ai-officer`, `/aigov`, `/ai-governance`)
- **Touches:** Standard nav (has its own top-level "AI Governance" link), chat widget, Service + FAQPage JSON-LD. No API calls. Featured as #1 product on `index.html` and first tab on `platform.html`; cross-linked from `sdlc-agent.html`, `industries/compliance-governance.html`, `learn/ai-data-governance.html`.
- **Extend by:** Inline edits. Buyers = CTO/CISO/CFO/Board. Keep stats' cited sources. Pricing (starting from $1,999/month) is published on `pricing.html` — keep that page and this one's price-stack in sync. If the offering changes, update the chat widget's FAQ answers too. "AIGOV" = internal shorthand only.

### A3c. AI Adoption Strategy (FLAGSHIP)
- **What:** Flagship page for the Niche 2 offer — "From Twenty AI Pilots To Five That Matter. In 90 Days." Sells the same underlying **Fractional AI Officer (FAO)** product as A3b, reframed for **AI strategy & portfolio coordination** rather than code governance: turns scattered, ungoverned AI pilots into 2–3 owned, measurable implementations. Mirrors `ai-engineering-governance.html`'s section architecture (crisis stats, cost-of-inaction, the-gap comparison, FAO solution, 3-phase Diagnose/Design/Deploy framework, FAQ, hire-vs-consultancy-vs-FAO economics, anonymized client outcomes, engagement model, 90-day journey) but with a 3-phase framework instead of governance's 5-layer one, and no fabricated incidents/breach-cost stack (none exist for this niche — see the `docs/CHANGELOG.md` 2026-08-06 entry for the sourcing discipline followed). Buyers = COO (primary), CEO/CFO/CHRO (secondary); deliberately excludes CTO/CIO, who are A3b's buyers.
- **Where:** [`ai-adoption-strategy.html`](../ai-adoption-strategy.html) (URL `/ai-adoption-strategy`)
- **Touches:** Standard nav — as of 2026-08-06 it shares a top-level "Solutions" dropdown with A3b (`.nav-dropdown-wrap`, see `docs/DESIGN-SYSTEM.md` §4.1); its own page marks the dropdown trigger `class="nav-dropdown-trigger active"`, the same as A3b does on its own page. Chat widget, Service + FAQPage JSON-LD. All CTAs route into the existing Niche 2 lead-magnet funnel — `lp/ai-maturity-index.html` (quiz) and `lp/maturity-review.html` (booking), **not** `#book-governance` (that opens A3b's governance-framed Calendly modal). Cross-linked reciprocally with `ai-engineering-governance.html` (framework-section footnote), from `about.html`'s FAO Specialists team card and `platform.html`'s hero line, and from the footer Solutions column on 8 hub pages (`index.html`, `ai-engineering-governance.html`, `platform.html`, `pricing.html`, `fde-engineers.html`, `sdlc-agent.html`, `agent-builder.html`, `about.html`).
- **Extend by:** Inline edits. **Pricing must stay "starting from $1,999/month," in sync with A3b and `pricing.html`** — do not reintroduce the $5K–$195K figures that appeared in an early draft of the Niche 2 offer docs (see CHANGELOG 2026-08-06); the $400K–$750K figure on this page is the cost of the *alternative* (a full-time CAIO hire), not Upcore's own price. Keep `lp/ai-maturity-index.html`'s own pricing strings in sync too — they were previously out of sync (fixed same date).

### A4. Studio (Agent Builder marketing)
- **What:** Marketing page for Upcore Studio — "Your Workflows. Now Run Themselves." Describes the plain-English-to-agent-logic flow.
- **Where:** [`agent-builder.html`](../agent-builder.html)
- **Touches:** Standard nav, chat widget. Does **not** call any API.
- **Extend by:** Inline edits. If Studio gains new capabilities, also update the chat widget's FAQ answer for "How is Studio different from a no-code tool?" in `chat-widget.js`.

### A4b. FDE Engineers (Forward Deployed Engineering flagship)
- **What:** Flagship page for Studio's delivery model — "Your AI Agent Vendor Ships a Demo. We Ship an Engineer." Sells a **Forward Deployed Engineer (FDE)**: a dedicated engineer embedded in the client's workflow to build, integrate, deploy, and maintain custom agents against real systems (CRM/ERP/APIs), governed by the client's FAO from the first commit. Mirrors `ai-engineering-governance.html`'s section architecture (problem stats, failure patterns, cost-of-not-shipping, gap, solution pillars, 5-stage framework, FAQ, economics, client outcomes, engagement model). Single retainer price: starting from $2,499/month — no dual-tier pricing.
- **Where:** [`fde-engineers.html`](../fde-engineers.html) (URL `/fde-engineers`)
- **Touches:** Standard nav, chat widget, Service + FAQPage JSON-LD. Cross-linked from `about.html` (3rd team card), `agent-builder.html` (Investment-section callout), and `pricing.html` (3rd add-on card + footer Solutions link). Scoped to agent-building pages only — no homepage/nav changes (FAO remains the sitewide hero story).
- **Extend by:** Inline edits. Keep the single $2,499/mo retainer price — do not reintroduce a second FDE price point. Cited stats (RAND 80%, Gartner 40%+, S&P Global $7.2M) must stay attributed, not fabricated.

### A5. Forge (SDLC Agent marketing)
- **What:** Marketing page for Upcore Forge — "Build Software Without a Dev Team."
- **Where:** [`sdlc-agent.html`](../sdlc-agent.html)
- **Touches:** Standard nav, chat widget. No API calls.

### A6. Industries hub
- **What:** Directory of all 12 vertical pages.
- **Where:** [`industries/index.html`](../industries/index.html)
- **Touches:** Links to each `industries/<vertical>.html`. **Must** be updated when adding a new vertical.

### A7. Industry vertical pages (×12)
- **What:** One page per vertical: Banking & Finance, EdTech, Government, Healthcare, Legal & Compliance, Logistics, Manufacturing, Marketing Agencies, NBFC/Loans, Real Estate, Retail/D2C, SaaS/Technology.
- **Where:** [`industries/*.html`](../industries/)
- **Touches:** Each page typically links to: relevant insight articles, the demo builder (if supported), and the assessment page.
- **Note:** `/industries/ecommerce` is a rewrite to `retail-d2c` (see `vercel.json`).
- **Extend by:** See [CONVENTIONS.md §4](CONVENTIONS.md#4-adding-a-new-industry-to-the-demo-builder) for full add-an-industry flow (it spans pages + demo builder + chat prompt).

### A8. Insights hub + articles (×16)
- **What:** Long-form blog. 16 articles covering vertical-specific AI topics (banking WhatsApp service, healthcare no-shows, ecommerce cart recovery, real-estate lead conversion, NBFC KYC, manufacturing QC, logistics WISMO, etc.) plus framework pieces (human-in-the-loop, ROI business case, choosing your first agent).
- **Where:** [`insights/index.html`](../insights/index.html) + 16 article files.
- **Touches:** Editorial metadata (NOT loaded by pages) lives in `insights/ARTICLES-REFERENCE.md` and `BATCH-*.txt`.
- **Routing:** `/blog` and `/blog/:slug` redirect permanently to `/insights` and `/insights/:slug`.
- **Extend by:** Drop new article HTML in `insights/`, link it from `insights/index.html`, optionally add a record to `ARTICLES-REFERENCE.md`.

### A9. Learn hub — AI fundamentals education pages
- **What:** Educational long-form pages targeting technical executives and enterprise AI buyers. Covers foundational AI agent concepts with PAA-optimised FAQ sections and Article + FAQPage JSON-LD. Each page is 50–55KB of substantive HTML.
- **Where:** [`learn/`](../learn/) directory.
  - `learn/enterprise-ai-strategy.html` — 5 strategic decisions framework
  - `learn/how-ai-agents-work.html` — perception–reasoning–action architecture
  - `learn/ai-agent-vs-llm.html` — LLM vs agent capability comparison
  - `learn/ai-agent-memory.html` — 4 memory types (working, episodic, semantic, procedural)
  - `learn/ai-in-banking.html` — banking AI use cases, compliance architecture, and generic vs custom AI comparison
  - `learn/hipaa-compliant-ai.html` — HIPAA compliance for AI: architectural requirements, vendor evaluation checklist
  - `learn/ai-workforce-platform.html` — AI workforce platform category definition, architecture, and buyer's guide
- **Touches:** Standard nav, footer, chat widget. No API calls. Internal links to `/assessment`, `/platform/custom-ai-agents`, `/platform/on-premise-deployment`, `/kw`.
- **Extend by:** Drop new article HTML in `learn/`, add JSON-LD Article + FAQPage schemas, include 8 FAQ items targeting PAA queries. Follow the CSS/nav/footer pattern exactly from an existing `learn/` page — do NOT copy from `insights/` (different CSS component set).

---

## B. Lead-capture features (forms / FormSubmit)

### B1. Discovery Call ("Assessment") form
- **What:** "Let's Map Your AI Opportunity" form. Captures name, company, industry, challenge, contact info. Used as the primary booking surface.
- **Where:** [`assessment.html`](../assessment.html) — direct HTML form `POST` to `https://formsubmit.co/gaurav@upcoretechnologies.com`.
- **Touches:** FormSubmit.co (no backend, no env vars, no JS submit handler).
- **Extend by:** Add/remove fields in the form HTML. FormSubmit will email whatever you POST. If the destination email changes, also update [§E](#e-cross-cutting-contracts).

### B2. Contact form
- **What:** Contact form on `/contact`. Real `async handleSubmit()` — posts to FormSubmit.co via `fetch()` (matches B1's destination), shows a proper loading/error state.
- **Where:** [`contact.html`](../contact.html), `handleSubmit()` near the bottom.
- **Extend by:** Add/remove fields in the form HTML; FormSubmit will email whatever you POST. Note (2026-07-22 audit): unlike B1, this form has no inline privacy disclosure near the submit button and no CAPTCHA/honeypot — worth aligning with B1's pattern if spam becomes an issue.

### B3. Kai chat widget (one-click FAQ + lead capture)
- **What:** Floating chat widget on every non-demo page. Bot named **Kai**. As of 2026-07-24 this is a self-contained client-side FAQ menu, not a live AI conversation: a curated knowledge base (`FAQ` array, grouped into 6 categories) answers common questions in one click — click a popular question or drill into a category card, get the canned answer instantly, no network call. Anything typed into the free-text input is treated as a custom question: the bot collects name + email conversationally, then POSTs the question/name/email straight to FormSubmit (team notification, `_cc` to a second inbox) and shows a "Message Sent" confirmation — the team replies by email within 24 hours instead of the bot improvising an answer.
- **Where:** [`chat-widget.js`](../chat-widget.js) (vanilla-JS IIFE, self-contained CSS) — entirely frontend, no backend call. Loaded via `<script src="/chat-widget.js?v=N" defer></script>` on **all 70 non-demo pages**. The `?v=N` query is a manual cache-buster — bump it on every substantive edit to the file, across all pages, or browsers will keep serving a stale cached copy.
- **Touches:** FormSubmit.co (`gaurav@upcoretechnologies.com`, `_cc: saswata@upcoretechnologies.com`). The "📅 Book a Governance Review" chip re-dispatches a click on a synthetic `a[href="#book-governance"]` to open the same Google Calendar modal every nav CTA uses (bottom IIFE in the same file, unchanged).
- **Extend by:**
  - To add/edit a question: add an entry to the `FAQ` array (`id`, `cat`, `q`, `a`; set `popular: true` to also surface it in the initial 6-chip menu) or a new entry to `CATEGORIES`.
  - To change voice/copy: edit `INITIAL_MESSAGE` and the `a` strings directly — these are trusted, hand-authored HTML (inline `<a>` tags allowed), unlike user-typed text which is always escaped.
  - To change widget UI: edit `chat-widget.js` directly. Don't unify its CSS with the page's design tokens — see [DESIGN-SYSTEM.md §5](DESIGN-SYSTEM.md#5-chat-widget-styling).
  - To change what the lead-notification email contains: edit the payload in `submitLead()`.
- **Legacy:** `api/chat.js` (the previous Anthropic-backed implementation, with its `SYSTEM_PROMPT` and `[BOOK_APPOINTMENT:{...}]` marker protocol) is no longer called by `chat-widget.js` and is unused dead code — left in place rather than deleted in case AI-driven chat is reinstated later. Don't treat its `SYSTEM_PROMPT` as current brand voice; `chat-widget.js`'s `FAQ`/`INITIAL_MESSAGE` is the source of truth now.

### B4. Lead-magnet landing pages (Governance Index + AI Maturity Index)
- **What:** Two net-new, isolated, ad-only (`noindex,nofollow`) landing pages, unlinked from nav/footer/sitemap. Each is a 10-question scored quiz (Hero → Intro → Quiz → Teaser/email-gate → Full Result) that computes a 0–100 tier score client-side, gates the full breakdown behind an email, and immediately generates and downloads a branded PDF report in-browser (jsPDF via CDN — teal header bands, score card with tier badge, per-dimension bars with a peer-average marker, polished next-step CTA page; no transactional email service). `governance-index.html` targets CIO/CTO/VP Eng (dark "console" skin, 5-axis radar chart). `ai-maturity-index.html` targets COO/CEO/CFO/CHRO (light "scorecard" skin, 4-stage maturity curve + 10-axis radar). Neither page has a `<nav>` or the chat widget — a deliberate exception for paid landing pages (no competing interactive element).
- **Booking-page routing (2026-08-06):** each niche's "book a call" CTAs point at a *distinct* destination, set via `config.bookingHref` in that page's `NICHE_CONFIG` — never a shared page with swapped copy. Governance Index → `/assessment` (the site's general, nav-having governance booking page). AI Maturity Index → `/lp/maturity-review` (a dedicated, `/lp/`-convention page with portfolio-value/ROI copy matching the Maturity Index's own framing — no compliance-framework language). This split exists because the two funnels sell different things (governance vs. portfolio-value coordination) and a CRO audit found the Maturity Index's CTA routing to `/assessment`'s governance-framed copy was a direct message mismatch. If a third niche is ever added, give it its own booking destination the same way — don't retrofit `/assessment` or `/lp/maturity-review` to serve a second pitch.
- **Score/tier handoff to booking pages:** `lead-magnet-engine.js`'s `_bookingUrl()` (used only for the post-quiz Full Result CTA, not the pre-quiz "skip to booking" link, since no score exists yet) appends `?tier=<label>&score=<overall>` to `config.bookingHref`. Both `assessment.html` and `lp/maturity-review.html` run a small vanilla-JS IIFE on load that reads those params via `URLSearchParams` and, if present, shows a "Your [Index] score: **X (Y/100)** — we'll pick up from exactly there on the call" line above the form, plus populates a hidden form field so the value also reaches the team-notification email. Keeps the booking page personalized without a network round-trip.
- **Quiz UX:** Typeform-style — one question per screen (never grouped), thin animated progress bar + "N / total" counter, a `←` back button that re-shows the previous (editable) answer, numbered option rows (1–9), keyboard nav (number keys select, Enter confirms a multiselect + continues, Backspace goes back), fade/slide transition between questions. Insight interrupts render as their own centered full-screen interstitial at the same trigger point as the question that earns them.
- **Where:** [`lp/lead-magnet-engine.js`](../lp/lead-magnet-engine.js) — shared vanilla-JS IIFE (`window.LeadMagnetEngine.init(config)`) owning all mechanical logic: flow control, scoring, hand-rolled inline-SVG charts (no chart library), jsPDF generation (`_generatePdf`, with shared branding helpers `pdfHeaderBand`/`pdfFooter`/`pdfTierColor`), GTM events, UTM/gclid capture. [`lp/governance-index.html`](../lp/governance-index.html) and [`lp/ai-maturity-index.html`](../lp/ai-maturity-index.html) each own their own `<style>` block and an inline `NICHE_CONFIG` object (copy, question schema, tier table, chart config). `robots.txt` disallows `/lp/`. **`lead-magnet-engine.js?v=N` needs its cache-buster bumped on both pages whenever the file changes substantively** — same discipline `CLAUDE.md` documents for `chat-widget.js`; forgetting this once already shipped a fix that silently didn't reach visitors (2026-08-05).
- **Touches:** jsPDF (CDN `<script>`, `cdnjs.cloudflare.com/ajax/libs/jspdf`). [`api/lead-magnet-submit.js`](../api/lead-magnet-submit.js) is the real backend (both pages' `config.api.submit` points at `/api/lead-magnet-submit`): recomputes the score server-side (never trusts the client-submitted score/tier) and POSTs one row per lead to a Google Sheet via a Google Apps Script Web App webhook (`GOOGLE_SHEETS_WEBHOOK_URL` — **not Apollo, not Vercel KV**; this account has no Vercel Pro plan, so the Sheet is also the peer-benchmark store — the Apps Script computes and returns the niche's running aggregate, count/avgOverall/avgByDim, in its own response). If the sheet write fails the function still returns a valid score/tier response — a lead never gets stuck because of a CRM outage. The client (`_submitContact` in the engine) itself also degrades gracefully: if the fetch to `/api/lead-magnet-submit` fails outright (network error, 404, etc.), it falls back to the locally-computed score with `peer.sufficientData:false` rather than blocking the visitor.
- **Team notification email is sent client-side, deliberately.** `_sendTeamNotification()` in the engine fires a browser `fetch()` to FormSubmit.co (same service as every other lead form on this site) right after `_onSubmitResult`, using the API response's server-verified `tier`/`overallScore`/`dims`/`weakestDim` — **not** sent from `api/lead-magnet-submit.js` itself. Cloudflare (which fronts FormSubmit.co) returns a 403 bot-detection challenge to Vercel's serverless outbound IPs no matter what headers are set; only real-browser requests get through. Confirmed by direct testing 2026-08-05 — see CHANGELOG. If you're tempted to "simplify" this back onto the server, don't — it silently stops sending email again.
- **CIO/CTO cross-routing (not implemented):** the original spec described routing a Niche-2 (AI Maturity) submission to the Niche-1 (Governance) offer when the contact's title is CIO/CTO. The built email-gate form only collects firstName/email/company — no title field — so this routing rule was never wired up. Flagged here rather than silently dropped; would need a title field added to the teaser form before it could work.
- **Analytics — GA4 + Google Ads:** `pushEvent()` in the engine fires every funnel event two ways: `window.dataLayer.push(...)` (for anyone who later wants GTM-based triggers) AND a direct `gtag('event', eventName, params)` call — since both pages already load `gtag.js` straight for GA4 (`G-TVRF5M70ES`), the direct call lands in GA4 Realtime immediately with zero GTM configuration required. Event names, per niche (`index_*` for governance, `maturity_*` for maturity — swap the prefix, params are identical):

  | Event | Fires when | Params |
  |---|---|---|
  | `{prefix}_start` | Quiz begins (after Intro CTA) | — |
  | `{prefix}_question_answered` | Every question answered | `question_id`, `dimension` |
  | `{prefix}_teaser_view` | Score computed, email-gate shown | `tier` |
  | `{prefix}_email_captured` | Email-gate form submitted | `email_domain` |
  | `{prefix}_assessment_complete` | **Primary conversion** — same moment as `email_captured`, but named distinctly so it reads unambiguously as THE conversion event (not a generic form-fill) when marking it a GA4 key event | `tier` |
  | `{prefix}_result_view` | Full Result screen renders | `tier` |
  | `{prefix}_pdf_sent` | PDF download button clicked | — |
  | `{prefix}_call_booked` | "Book a review" CTA clicked on Full Result | — |

  Every event also carries `niche` (`governance-index` / `ai-maturity-index`) for segmentation. **Google Ads conversions (live):** two separate conversion actions, one per niche (user's choice — lets each ad campaign optimize toward its own niche's completion rate, matching the existing `index_*`/`maturity_*` event split). `config.googleAdsConversionLabel`/`Value`/`Currency` in each `NICHE_CONFIG` gate a `gtag('event','conversion',{send_to,value,currency})` call fired at the same `assessment_complete` moment — same pattern as `assessment.html`'s and `chat-widget.js`'s existing conversions, same `AW-16546427858` account. Governance Index → `AW-16546427858/ozjeCPjqqNwcENLn-dE9`; AI Maturity Index → `AW-16546427858/Aa1UCPvqqNwcENLn-dE9`; both `value:1.0, currency:'INR'`. Verified firing in-browser with the correct label/value/currency on both pages.
  - CTA click tracking (`cta_click` events, distinct from the funnel events above) already covers every button on these pages via the sitewide `cta-tracking.js` + the `data-gtm-cta`/`-type`/`-section` attributes the engine sets on every button — no extra wiring needed.
- **Extend by:**
  - To add/edit questions, copy, tiers, or chart config for a niche: edit that page's own `NICHE_CONFIG` object — never the shared engine.
  - To change flow mechanics, scoring math, chart rendering, or PDF layout for both niches at once: edit `lead-magnet-engine.js`.
  - The quiz always shows one question at a time (`state.qIndex` indexes the flat `allQuestions(config)` list, not `config.screens`). `config.screens` still exists purely as metadata: a screen's `chipLabel`/`theme` becomes the eyebrow label above its questions, and `screen.insightAfter.afterQuestionId` still controls exactly when an insight interrupt shows. There's no per-niche "grouping" setting anymore — `progressStyle`/`screensPerView` were removed as dead config.
  - A shared `el()` DOM-builder helper skips `null`/`false`/`undefined` attribute values entirely rather than calling `setAttribute` with them — needed because `setAttribute('disabled', null)` still sets the boolean `disabled` attribute (to the string `"null"`). Don't pass `attrs.disabled = null` expecting it to `setAttribute`-away; the helper already treats that as "omit the attribute."

---

## C. AI-powered features (Anthropic API)

*(No AI-powered chat feature is currently live — see B3's "Legacy" note. `api/chat.js` remains deployable but unused.)*

### C1. Personalised Demo Builder
- **What:** User picks an industry + describes pain point + agent name → in ~60s a live, personalised demo HTML is generated, committed to GitHub, deployed by Vercel, and the URL is returned. Lead notification email sent to Upcore.
- **Where:**
  - Frontend: [`build-your-demo.html`](../build-your-demo.html) (multi-step UI, POSTs to `/api/build-demo`).
  - Backend: [`api/build-demo.js`](../api/build-demo.js).
  - Output: `demos/<slug>.html` + entry in `demos/manifest.json`.
- **Touches:** Anthropic API, GitHub Contents API, Vercel auto-deploy, FormSubmit, daily cleanup cron.
- **Currently supported industries:** **manufacturing, ecommerce only** (driven by `INDUSTRY_CONFIG` in `api/build-demo.js`). The `build-your-demo.html` form only exposes those two as radio options.
- **Rate limits:** 3 demos / IP / 30min, 100 demos / day globally (in-memory, resets on cold start).
- **Env:** `ANTHROPIC_API_KEY`, `GITHUB_PAT`, `GITHUB_REPO`, `SITE_BASE_URL`.
- **Extend by:** See [CONVENTIONS.md §4](CONVENTIONS.md#4-adding-a-new-industry-to-the-demo-builder). Adding an industry is a 5-step flow that spans the API, the form, the chatbot prompt, and (optionally) a marketing page.
- **Pipeline diagram:** [ARCHITECTURE.md §3.2](ARCHITECTURE.md#32-apibuild-demo--demo-builder-pipeline).

---

## D. Operational / infrastructure features

### D1. Daily demo cleanup cron
- **What:** Reads `demos/manifest.json`, deletes `demos/<slug>.html` for any expired entries, rewrites the manifest, commits as the `Upcore Demo Bot`.
- **Where:** [`.github/workflows/`](../.github/workflows/) — runs at `30 20 * * *` UTC (02:00 IST). Manual trigger via `workflow_dispatch`.
- **Touches:** `demos/`, `demos/manifest.json`. Requires `contents: write` on the workflow.
- **Extend by:** If demo retention rules change, edit the inline Node script in the workflow. The manifest schema (`{ slug, expires, ... }`) is the contract — don't change it without updating `api/build-demo.js`.

### D2. Routing / cleanUrls / redirects
- **What:** All URL behavior — `cleanUrls: true`, permanent redirects (`/blog → /insights`, `/about-us → /about`, etc.), and the `/industries/ecommerce → /industries/retail-d2c` rewrite.
- **Where:** [`vercel.json`](../vercel.json).
- **Extend by:** Whenever you rename or move a page, add a redirect here. Never silently break inbound links.

### D3. HTTP headers / caching
- **What:** Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) on all responses; long immutable caching for static assets (`*.svg|*.png|*.jpg|*.ico`).
- **Where:** [`vercel.json`](../vercel.json) `headers` block.

### D4. Function timeouts & memory
- **What:** `api/build-demo.js` runs at 256MB / 60s; `api/chat.js` runs at 256MB / 15s.
- **Where:** [`vercel.json`](../vercel.json) `functions` block.
- **Note:** The 60s ceiling on `build-demo` is sized for a single Anthropic generation. If the prompt grows, watch latency.

### D5. Analytics stack (GTM + GA4 + Google Ads + Clarity) & CTA click tracking
- **What:** Tracking scripts in `<head>`/`<body>` on all 70 non-demo pages, in this order: Google Tag Manager (container `GTM-MH5PB32L`, loader script first in `<head>` + `<noscript><iframe>` fallback first in `<body>`), Google Analytics 4 (`gtag.js`, property `G-TVRF5M70ES`) — with a second `gtag('config', 'AW-16546427858')` call for the Google Ads account sharing the same `gtag.js` loader (per Google's own instructions for a site that already has a Google tag installed — no duplicate loader script), Microsoft Clarity (project `xtvhi9nvqa`). On top of that, every primary/secondary CTA `<a>` sitewide carries three `data-gtm-*` attributes, and [`cta-tracking.js`](../cta-tracking.js) listens for clicks on any `[data-gtm-cta]` element and pushes a structured `cta_click` event to `window.dataLayer`.
- **Google Ads conversions (two, primary + secondary — configured as such in the Google Ads dashboard, not in code):**
  - **Secondary — "Lead Tracking":** [`assessment.html`](../assessment.html) fires `gtag('event', 'conversion', {send_to: 'AW-16546427858/CN8BCPra5LsZENLn-dE9'})` — scoped to the existing `if(window.location.search.includes('submitted=true'))` block that already shows the success message post-submit (the FormSubmit `_next` redirect target), so it fires once per real completed Discovery Call *form submission*, never on a normal page view.
  - **Primary — "Book governance review":** the "Book a Governance Review" modal (bottom IIFE in [`chat-widget.js`](../chat-widget.js), triggered sitewide by any `a[href="#book-governance"]`) embeds **Calendly** (`https://calendly.com/saswata-upcoretechnologies/30min`), not Google Calendar's appointment scheduler — Calendly exposes a `postMessage` API with a genuine `calendly.event_scheduled` event when a visitor actually finishes booking a slot, which Google Calendar's embed does not. `chat-widget.js` listens for that message (checking `e.origin === 'https://calendly.com'` first) and fires `gtag('event', 'conversion', {send_to: 'AW-16546427858/_Q5SCO7LodgcENLn-dE9'})` only then — i.e. on a real completed *meeting booking*, not just a click on the CTA that opens the modal.
  - **Why two different signals for two conversions:** a form submission (assessment.html) is a real, verifiable completion event triggerable via a URL query param; a calendar booking inside a 3rd-party iframe is not observable at all without a provider that exposes a completion callback — Calendly does, Google Calendar's public appointment-scheduling embed doesn't. Switching booking providers was a deliberate decision (see CHANGELOG 2026-07-29) specifically to make the primary conversion accurate rather than click-based.
- **Where:**
  - GTM/GA4/Clarity snippets: inline in every page's `<head>`/`<body>` (no shared file — see D2/D3-style per-page duplication pattern already used for `:root`/nav).
  - CTA attributes: `data-gtm-cta="<slug>"` (derived from the button's own text, e.g. `"Book a Governance Review →"` → `book-a-governance-review`), `data-gtm-cta-type="primary"` or `"secondary"` (derived from the button's CSS class — see the allow-lists in the one-off tagging script's history, e.g. `btn-teal`/`btn-fill`/`btn-primary`/`nav-cta`/`btn-p`/etc. = primary, `btn-ghost`/`btn-o`/etc. = secondary), `data-gtm-cta-section="<context>"` (the nearest ancestor element's `id`, or a heuristic fallback: `nav`, `footer`, `hero`, `cta_final`, or `other`).
  - Tracking script: [`cta-tracking.js`](../cta-tracking.js) — a single vanilla-JS IIFE, same pattern as `chat-widget.js`. Loaded via `<script src="/cta-tracking.js?v=N" defer></script>` immediately after the `chat-widget.js` tag on every page.
- **Touches:** `window.dataLayer` (shared with GTM/GA4). No backend, no API calls.
- **cta_click event shape:** `{ event: 'cta_click', cta_id, cta_type, cta_section, cta_text, cta_url, page_path }`. `cta_text`/`cta_url`/`page_path` are read live from the DOM/location at click time, not baked into the HTML attributes.
- **GTM/GA4 configuration required (not done by this codebase — set up in the GTM/GA4 web UI):** a Custom Event trigger on `event == 'cta_click'`, Data Layer Variables for `cta_id`/`cta_type`/`cta_section`/`cta_text`/`cta_url`, and a GA4 Event tag (Event Name `cta_click`) mapping those as event parameters. Nobody in this repo can configure that from code — it's a one-time manual step in the GTM container.
- **Extend by:**
  - New CTA buttons: add the same three `data-gtm-cta*` attributes by hand, following the existing convention (`cta_id` = slugified button text, `cta_type` = primary/secondary by visual weight, `cta_section` = nearest semantic ancestor id or a sensible new heuristic label).
  - Changing the event shape: edit `cta-tracking.js`'s `dataLayer.push(...)` call, then update the GA4 Event tag's parameter mapping in GTM to match.
  - Bumping GTM/GA4/Clarity IDs: bulk-replace across all 70 pages in one commit (see CHANGELOG entries from 2026-07-29 for the exact pattern used).

---

## E. Cross-cutting contracts

These are not features per se — they're invariants that span multiple features. Touching one means touching all listed places together.

| Contract | Places that depend on it |
|---|---|
| Anthropic model `claude-haiku-4-5-20251001` | `api/build-demo.js` (live); `api/chat.js` (hardcoded but unused — see B3) |
| Lead-notification email `gaurav@upcoretechnologies.com` | `assessment.html`, `contact.html`, `chat-widget.js` `LEAD_EMAIL`/`submitLead()`, `api/build-demo.js` `NOTIFY_TO`; `api/chat.js` `sendBookingEmails` is unused legacy |
| Chat widget cache-buster `chat-widget.js?v=N` | One `<script>` tag per page, all 70 non-demo pages — bump the number everywhere in the same commit whenever `chat-widget.js` changes substantively |
| Industry list | `industries/index.html`, individual `industries/*.html`, `INDUSTRY_CONFIG` in `api/build-demo.js` (subset) — `chat-widget.js`'s FAQ links out to `/industries` rather than duplicating the list |
| Demo manifest schema `{ slug, expires, ... }` | `api/build-demo.js` (writer), `.github/workflows/*` (reader/cleaner) |
| Design tokens (`:root`) and nav block | All 70 non-demo HTML pages — see [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) |

---

## ⚠️ Known gaps / open items

These are documented so they're not rediscovered repeatedly. When a gap is closed, move it into the relevant feature section above.

- **Demo builder only supports 2 industries** ([C2](#c2-personalised-demo-builder)) despite 12 marketing pages existing. To expand: extend `INDUSTRY_CONFIG` and the radio options. See [CONVENTIONS.md §4](CONVENTIONS.md#4-adding-a-new-industry-to-the-demo-builder).
- **Two demo HTML files exist with empty manifest** ([STRUCTURE.md anomalies](STRUCTURE.md#anomalies-current-technical-debt)). Either stale samples or orphaned from a previous run. Cleanup cron won't touch them.
- **Duplicate `industries/upcore-logo.{png,svg}`** appear unused (pages reference root paths). Verify before deleting.
- **In-memory rate limit on `/api/build-demo`** resets on cold start — accepts some over-limit requests by design. If this becomes a problem, move to Vercel KV / Upstash.

---

## How to add a new feature (decision tree)

When you're about to build something new, walk this:

1. **Is it a static marketing/content page?** → New file in repo root or `industries/` or `insights/`. Follow [CONVENTIONS.md §3](CONVENTIONS.md#3-adding-a-new-page-checklist). Add to **Section A** above.
2. **Is it a form that collects info?** → Use FormSubmit (mirror `assessment.html`). Add to **Section B** above. Update [§E cross-cutting contracts](#e-cross-cutting-contracts) if it sends to the same email.
3. **Does it need an LLM?** → New serverless function in `api/`, add `functions[<path>]` to `vercel.json`, document in [ARCHITECTURE.md](ARCHITECTURE.md). Add to **Section C** above. Keep the Anthropic model id in sync with the existing files.
4. **Does it generate / persist content?** → Decide upfront whether it commits to git (like the demo builder) or uses a real DB/KV. Both are valid; the trade-offs are in [ARCHITECTURE.md](ARCHITECTURE.md). Add to **Section C** or **D**.
5. **Is it a scheduled job?** → New GitHub Actions workflow in `.github/workflows/`. Add to **Section D**.
6. **Does it change a URL or break an inbound link?** → Add a permanent redirect in `vercel.json`.
7. **Does it introduce a new design pattern, component, or token?** → Update [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) **first**, then propagate.
8. **Always:** add a [CHANGELOG.md](CHANGELOG.md) entry in the same change.
