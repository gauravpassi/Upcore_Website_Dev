# Architecture

## 1. Stack at a glance

- **Static HTML site** — 37 hand-authored pages, each self-contained (its own `<style>` and `<script>` blocks). No bundler, no framework, no preprocessor, no `package.json`, no tests, no lint.
- **Hosting** — Vercel. `cleanUrls: true` means pages are served without `.html`. See [`vercel.json`](../vercel.json) for headers, redirects, rewrites, and per-function memory/timeout.
- **Two serverless functions** in [`api/`](../api/), invoked from the browser via `fetch`.
- **Forms** — Static HTML forms POST directly to FormSubmit.co. There is no server-side form handler in this repo.
- **Daily cron** — A GitHub Actions workflow cleans up expired demo files; see §4.

This stack is intentional. **Do not introduce React/Vue/Svelte, a bundler, Tailwind, a CSS-in-JS layer, or a CMS** without explicit approval — every one of those changes the deployment model.

## 2. Page layer

```
/                        → index.html
/about                   → about.html
/platform                → platform.html
/contact                 → contact.html
/assessment              → assessment.html  (Discovery Call form, FormSubmit)
/build-your-demo         → build-your-demo.html  (calls /api/build-demo)
/agent-builder           → agent-builder.html
/sdlc-agent              → sdlc-agent.html
/industries              → industries/index.html + 12 vertical pages
/insights                → insights/index.html + long-form articles
/demos/<slug>            → demos/<slug>.html  (generated, ephemeral)
```

Routing rules (all in [`vercel.json`](../vercel.json)):

- `cleanUrls: true` — internal links **must omit** `.html`.
- Permanent redirects: `/home → /`, `/blog → /insights`, `/blog/:slug → /insights/:slug`, `/contact-us → /contact`, `/about-us → /about`.
- One rewrite: `/industries/ecommerce → /industries/retail-d2c` (alias, not a redirect).

The chat widget (`<script src="/chat-widget.js" defer>`) is included on **every** non-demo page.

## 3. Serverless functions ([`api/`](../api/))

### 3.1 `/api/chat` — legacy, unused

[`api/chat.js`](../api/chat.js) is a Vercel function that calls the Anthropic Messages API (`model: claude-haiku-4-5-20251001`) with a hard-coded `SYSTEM_PROMPT` and a `[BOOK_APPOINTMENT:{...json...}]` marker protocol. **As of 2026-07-24, `chat-widget.js` no longer calls this endpoint** — the widget was rebuilt as a self-contained client-side FAQ menu (see below) that never hits the network for answers. `api/chat.js` still deploys and would still work if called directly, but nothing on the site calls it. Left in place rather than deleted in case AI-driven chat is reinstated; don't treat its `SYSTEM_PROMPT` as current brand voice.

### 3.1b Kai chat widget — one-click FAQ + email lead capture

[`chat-widget.js`](../chat-widget.js) is a pure static asset with **no backend function of its own**. Two data structures at the top of the file (`CATEGORIES`, `FAQ`) drive the whole UI: clicking a popular question or a category card renders the matching canned answer instantly, client-side. Anything typed into the free-text input starts a short conversational capture (name → email) and then POSTs directly to `https://formsubmit.co/gaurav@upcoretechnologies.com` (same pattern as `assessment.html`/`contact.html`) with the question, name, email, and originating page — no serverless function involved. The "Book a Governance Review" chip reuses the existing Calendly booking modal (bottom IIFE in the same file — see FEATURES.md D5 for why it's Calendly and not Google Calendar) via a synthetic click on `a[href="#book-governance"]`.

The `<script src="/chat-widget.js?v=N" defer>` tag's `?v=N` query is a manual cache-buster. Browsers cache the script aggressively by exact URL; bump `N` across **all 70 non-demo pages** in the same commit whenever you change `chat-widget.js` substantively, or visitors keep getting the old version.

### 3.2 `/api/build-demo` — Demo Builder pipeline

[`api/build-demo.js`](../api/build-demo.js) is the most complex piece in the repo. End-to-end:

```
POST /api/build-demo
  ↓
1. Rate limit (in-memory)
   - per IP: 3 / 30 min
   - global: 100 / day
   - Resets on Vercel cold start; this is "good enough for MVP" by design.
  ↓
2. Anthropic call → generate demo data (rows, metrics, copy)
   - Driven by INDUSTRY_CONFIG (currently: manufacturing, ecommerce only)
   - To add an industry, extend INDUSTRY_CONFIG with: label, emoji, entityName,
     defaultAgentName, integrations[], metricsTemplate[], statusOptions[],
     systemPromptContext.
  ↓
3. Assemble standalone HTML (one large template-literal builder)
  ↓
4. GitHub Contents API
   - PUT /repos/{GITHUB_REPO}/contents/demos/{slug}.html       (new file)
   - PUT /repos/{GITHUB_REPO}/contents/demos/manifest.json     (append entry)
  ↓
5. Vercel auto-deploys the new commits → demo URL is live within seconds.
  ↓
6. FormSubmit lead notification email to gaurav@upcoretechnologies.com
  ↓
7. Return { url, slug } to caller
```

Vercel function: `memory: 256MB`, `maxDuration: 60s`. Slowest step is step 2.

**`demos/manifest.json`** is the contract between the builder and the cleanup workflow. It is an array of `{ slug, expires, ... }`. **Do not hand-edit it.** When no demos are live, `[]` is the correct state.

## 4. Cleanup cron ([`.github/workflows`](../.github/workflows))

- Schedule: daily at `30 20 * * *` UTC (02:00 IST). Manual trigger also available via `workflow_dispatch`.
- Reads `demos/manifest.json`, deletes any `demos/{slug}.html` whose `expires` is in the past, rewrites the manifest, commits as `Upcore Demo Bot <demo-bot@upcore.ai>` with message `chore: cleanup expired demos [automated]`.
- The bot needs `contents: write`. Don't change permissions without thinking through what else gets the same token.

## 5. Environment variables

Set in Vercel project settings:

| Var | Required by | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | `api/build-demo.js` (live); `api/chat.js` (unused legacy, see §3.1) | Anthropic Messages API |
| `GITHUB_PAT` | `api/build-demo.js` | Contents-API token to commit demos. Needs `contents:write` on the repo. |
| `GITHUB_REPO` | `api/build-demo.js` | Defaults to `gauravpassi/upcore-website`. |
| `SITE_BASE_URL` | `api/build-demo.js` | Used to build the demo URL returned to the caller. Defaults to `https://upcore.ai`. |
| `GOOGLE_SHEETS_WEBHOOK_URL` | `api/lead-magnet-submit.js` | Google Apps Script Web App URL (ends `/exec`) — the lead-magnet CRM **and** the peer-benchmark store. No service-account auth, no OAuth, no Vercel KV (this account has no Vercel Pro plan): the Apps Script appends one row per lead to a Google Sheet AND returns the niche's running aggregate (count/avgOverall/avgByDim) in the same response — the Sheet is the only data store this feature needs. Setup script + instructions in `lp/` (see FEATURES.md B4). If unset, the function logs a warning and returns `{sufficientData:false}` rather than failing the whole request. |

The Anthropic model id is **hard-coded in two places** (`claude-haiku-4-5-20251001`). If you bump it, bump it in both files and validate that the system prompt still produces the expected JSON / booking-marker shape.

## 6. Local development

- Run with `vercel dev` — required for the `api/` functions and for `cleanUrls`/redirects to behave like prod. Static-only previews (`python -m http.server`, `npx serve`, etc.) work for read-only browsing but break anything calling `/api/*`.
- No build step. Save → reload.

## 7. External services & destinations

| Service | Used for | How to change |
|---|---|---|
| Anthropic API | Demo generation (`api/build-demo.js`); `api/chat.js` also calls it but is unused | Env var + model string in both files |
| GitHub Contents API | Writing demo HTML + manifest | Env var `GITHUB_PAT`, `GITHUB_REPO` |
| FormSubmit.co | Static forms + chat lead capture + demo lead emails | Email is hard-coded as `gaurav@upcoretechnologies.com` in: `assessment.html`, `contact.html`, `chat-widget.js` (`LEAD_EMAIL`, client-side `submitLead()`), `api/build-demo.js` (`NOTIFY_TO`). Change all together. (`api/chat.js`'s `sendBookingEmails` is unused legacy.) |
| Google Fonts | Poppins | `<link>` on every page |
| Google Tag Manager | Tag/pixel management container | Container ID `GTM-MH5PB32L` hard-coded in two places per page: the loader `<script>` as the very first thing in `<head>` (above GA4/Clarity), and the `<noscript><iframe>` fallback immediately after the opening `<body>` tag. Both on all 70 non-demo pages. Bulk-replace both if the container changes. |
| Google Analytics 4 (`gtag.js`) | Pageview/traffic analytics | Property ID `G-TVRF5M70ES` hard-coded (script `src` + `gtag('config', ...)`) directly below the GTM block in `<head>` on all 70 non-demo pages. Bulk-replace if the property changes. |
| Microsoft Clarity | Session recording / heatmaps | Project ID `xtvhi9nvqa` hard-coded in the inline snippet directly below the GA4 block on all 70 non-demo pages. Bulk-replace if the project changes. |
| Vercel | Hosting + deploy + cron-relay-via-GitHub-Actions | `vercel.json` |
| Google Apps Script (Web App) | Lead-magnet CRM **and** peer-benchmark store — `api/lead-magnet-submit.js` POSTs one row per submission to a Sheets-bound Apps Script webhook, which appends the row and returns the niche's running aggregate (count/avgOverall/avgByDim) computed from the sheet's own rows. No Vercel KV, no database — deliberately, since this account has no Vercel Pro plan. | Env var `GOOGLE_SHEETS_WEBHOOK_URL`; the Apps Script source lives outside this repo (given to the user directly, not committed — it's account-specific, not code this repo can own) |
| jsPDF (CDN) | Client-side PDF generation for the two lead-magnet pages | `<script>` tag, `cdnjs.cloudflare.com/ajax/libs/jspdf` |

## 8. Things that look broken but aren't

- **`demos/manifest.json` is `[]`** — that's the expected state when no demos are live. The cleanup workflow truncates it.
- **`<style>` blocks duplicated across 37 pages** — intentional. See [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) for how to keep them in sync.
- **In-memory rate limit "leaks" across cold starts** — by design; we accept some over-limit demos in exchange for not running a KV.
- **Chat widget hard-codes its own colors instead of using `:root`** — by design; widget must render correctly even if the host page didn't define `:root`.
