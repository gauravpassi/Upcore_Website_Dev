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
- **Touches:** Cross-links to `ai-engineering-governance.html`, `agent-builder.html` (Studio) and `sdlc-agent.html` (Forge). If the product lineup changes, update this page **and** Kai's `SYSTEM_PROMPT` in `api/chat.js` together.

### A3b. AI Engineering Governance (FLAGSHIP)
- **What:** Flagship offering page — "The AI Code Crisis Is Already Inside Your Enterprise." Sells **AI Engineering Governance** delivered via a **Fractional AI Officer (FAO)**: governs the risk of AI-generated code (budget, security, compliance). Sections: crisis stats, documented incidents, the-gap comparison, FAO solution, 5-layer/19-capability framework, hire-vs-Big4-vs-FAO economics, 90-day journey, FAQ. Source of truth = the FAO decks.
- **Where:** [`ai-engineering-governance.html`](../ai-engineering-governance.html) (URL `/ai-engineering-governance`; redirects: `/fractional-ai-officer`, `/aigov`, `/ai-governance`)
- **Touches:** Standard nav (has its own top-level "AI Governance" link), chat widget, Service + FAQPage JSON-LD. No API calls. Featured as #1 product on `index.html` and first tab on `platform.html`; cross-linked from `sdlc-agent.html`, `industries/compliance-governance.html`, `learn/ai-data-governance.html`.
- **Extend by:** Inline edits. Buyers = CTO/CISO/CFO/Board. Keep stats' cited sources; keep pricing unpublished. If the offering changes, update Kai's `SYSTEM_PROMPT` too. "AIGOV" = internal shorthand only.

### A4. Studio (Agent Builder marketing)
- **What:** Marketing page for Upcore Studio — "Your Workflows. Now Run Themselves." Describes the plain-English-to-agent-logic flow.
- **Where:** [`agent-builder.html`](../agent-builder.html)
- **Touches:** Standard nav, chat widget. Does **not** call any API.
- **Extend by:** Inline edits. If Studio gains new capabilities, also update Kai's product description in `api/chat.js`.

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

### B3. Booking via chat (auto-emails)
- **What:** When Kai (the chat widget) detects user is ready to book, it embeds a `[BOOK_APPOINTMENT:{...json...}]` marker in its reply. The server strips it and fires two FormSubmit emails (one to Upcore, one to the prospect).
- **Where:** [`api/chat.js`](../api/chat.js) — see `sendBookingEmails()`. Marker contract documented in `SYSTEM_PROMPT`.
- **Touches:** FormSubmit, Anthropic API.
- **Extend by:** To change the data captured in a booking, update both the marker schema described in `SYSTEM_PROMPT` *and* the `sendBookingEmails()` payload. Keep them in sync.

---

## C. AI-powered features (Anthropic API)

### C1. Kai chatbot (chat widget)
- **What:** Floating chat widget on every non-demo page. Bot named **Kai**. Answers product questions, suggests demos, captures booking info via the marker protocol (B3).
- **Where:**
  - Frontend: [`chat-widget.js`](../chat-widget.js) (vanilla-JS IIFE, self-contained CSS).
  - Backend: [`api/chat.js`](../api/chat.js).
  - Loaded via `<script src="/chat-widget.js" defer></script>` — included on **all 37 non-demo pages**.
- **Touches:** Anthropic API (`claude-haiku-4-5-20251001`, `max_tokens: 600`, last 20 messages), FormSubmit (for booking emails). Env: `ANTHROPIC_API_KEY`.
- **Brand voice / product/industry list:** all in `SYSTEM_PROMPT` at the top of `api/chat.js` — that string is the source of truth for what Kai says about Upcore.
- **Extend by:**
  - To change voice/messaging: edit `SYSTEM_PROMPT`.
  - To change widget UI: edit `chat-widget.js`. Don't unify its CSS with the page's design tokens — see [DESIGN-SYSTEM.md §5](DESIGN-SYSTEM.md#5-chat-widget-styling).
  - To add a new conversational capability (e.g. capture a different kind of intent): introduce a new bracket-marker convention, document it in `SYSTEM_PROMPT`, parse it in `api/chat.js`.

### C2. Personalised Demo Builder
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

---

## E. Cross-cutting contracts

These are not features per se — they're invariants that span multiple features. Touching one means touching all listed places together.

| Contract | Places that depend on it |
|---|---|
| Anthropic model `claude-haiku-4-5-20251001` | `api/chat.js`, `api/build-demo.js` |
| Lead-notification email `gaurav@upcoretechnologies.com` | `assessment.html`, `contact.html`, `api/chat.js` `sendBookingEmails`, `api/build-demo.js` `NOTIFY_TO` |
| Industry list (Kai's knowledge) | `api/chat.js` `SYSTEM_PROMPT`, `industries/index.html`, individual `industries/*.html`, `INDUSTRY_CONFIG` (subset) |
| Product list (Kai's knowledge) | `api/chat.js` `SYSTEM_PROMPT`, `platform.html`, `agent-builder.html`, `sdlc-agent.html` |
| Booking marker `[BOOK_APPOINTMENT:{...}]` | `api/chat.js` `SYSTEM_PROMPT` (defines it), `api/chat.js` parser, `chat-widget.js` (must never display it) |
| Demo manifest schema `{ slug, expires, ... }` | `api/build-demo.js` (writer), `.github/workflows/*` (reader/cleaner) |
| Design tokens (`:root`) and nav block | All 37 non-demo HTML pages — see [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) |

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
