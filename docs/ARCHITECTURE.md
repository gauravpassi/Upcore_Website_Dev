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
/                        → index.html  (V4.1, generated)
/ai-native-engineering   → ai-native-engineering.html  (V4.1 flagship, generated)
/who-we-help/<segment>   → who-we-help/{tech-software,ecommerce-retail,operations-heavy,professional-services}.html  (V4.1, generated)
/about                   → about.html
/platform                → platform.html
/contact                 → contact.html
/assessment              → assessment.html  (Discovery Call form, FormSubmit)
/build-your-demo         → build-your-demo.html  (calls /api/build-demo)
/agent-builder           → agent-builder.html
/sdlc-agent              → sdlc-agent.html
/industries              → industries/index.html + 11 older vertical pages
/insights                → insights/index.html + long-form articles
/demos/<slug>            → demos/<slug>.html  (generated, ephemeral)
```

Routing rules (all in [`vercel.json`](../vercel.json)):

- `cleanUrls: true` — internal links **must omit** `.html`.
- Permanent redirects: `/home → /`, `/blog → /insights`, `/blog/:slug → /insights/:slug`, `/contact-us → /contact`, `/about-us → /about`; `/industries/{cpa-firms,law-firms,legal-compliance} → /who-we-help/professional-services`, `/industries/insurance → /who-we-help/operations-heavy`; `/preview/home-v4 → /`, `/preview/ai-native-engineering → /ai-native-engineering`, `/preview/who-we-help-:slug → /who-we-help/:slug`.
- Temporary redirect: `/who-we-help → /#who-we-help` (no hub page; the home section is the hub).
- 2026-10-07 restructure: 35 more 301s for retired pages (Forge, Studio, FDE, `/platform/*`, `/solutions/*`, `/industries/*`, `/kw/*`, `/pricing`, `/ai-adoption-strategy` → `/fractional-ai-officer`, `/index-v2`). Full list: site map in [STRUCTURE.md](STRUCTURE.md). The `/industries/ecommerce` rewrite was replaced by a redirect. Unknown paths get `404.html`.
- One rewrite: `/industries/ecommerce → /industries/retail-d2c` (alias, not a redirect).

The chat widget (`<script src="/chat-widget.js" defer>`) is included on **every** non-demo page.

## 3. Serverless functions ([`api/`](../api/))

### 3.1 `/api/chat` and the website assistant (`chat-widget.js`)

`api/chat.js` answers the "Upcore AI" assistant ("Ask Upcore AI") through a free-tier OpenAI-compatible model (`GROQ_API_KEY`; it lists the models the key can use and falls back on errors). Without a key it returns `503 {fallback:true}` and `chat-widget.js` answers from its built-in FAQ. The site's facts live in its `SYSTEM_PROMPT`. Details: [FEATURES.md B3 and C2](FEATURES.md). `chat-widget.js` also holds the booking modal; its `?v=N` cache-buster is `CHAT_V` in `tools/v4-build/chrome.py` for generated pages and hard-coded on the hand-built ones (`/ai-operations`, `/build-your-demo`).

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

### 3.3 `/api/booking-intent` — booking attribution

[`api/booking-intent.js`](../api/booking-intent.js) receives the email a visitor enters before the Google Calendar scheduler (booking modal in `chat-widget.js`, and the `/assessment` form), with first-touch attribution (`gclid`/`utm_*` from `localStorage.upc_attrib`), GA client/session IDs and consent state. It validates and clips the fields, then POSTs one `intent` row (plus `BOOKING_WEBHOOK_TOKEN`) to the booking Apps Script Web App (`BOOKING_SHEETS_WEBHOOK_URL`, source [`tools/booking-conversions.gs`](../tools/booking-conversions.gs)). That script later matches calendar bookings by attendee email and sends GA4 `booking_completed` + Google Ads offline-conversion rows. In-memory rate limit (8 per IP per 30 min). If the env var is unset it returns `202 {stored:false}` and the site keeps working. Deliberately separate from `/api/lead-magnet-submit` (different Sheet). Full flow and setup: [TRACKING.md §5](TRACKING.md#5-booking-conversions).

## 4. Cleanup cron ([`.github/workflows`](../.github/workflows))

- Schedule: daily at `30 20 * * *` UTC (02:00 IST). Manual trigger also available via `workflow_dispatch`.
- Reads `demos/manifest.json`, deletes any `demos/{slug}.html` whose `expires` is in the past, rewrites the manifest, commits as `Upcore Demo Bot <demo-bot@upcore.ai>` with message `chore: cleanup expired demos [automated]`.
- The bot needs `contents: write`. Don't change permissions without thinking through what else gets the same token.

## 5. Environment variables

Set in Vercel project settings:

| Var | Required by | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | `api/build-demo.js` | Anthropic Messages API |
| `GROQ_API_KEY` (optional) | `api/chat.js` | Website assistant model (Groq free tier). Alternative: `CHAT_API_KEY` + `CHAT_API_BASE` + `CHAT_MODEL` (+ `CHAT_FALLBACK_MODEL`) for any OpenAI-compatible provider. Unset: the assistant answers from its built-in FAQ. See FEATURES.md C2. |
| `GITHUB_PAT` | `api/build-demo.js` | Contents-API token to commit demos. Needs `contents:write` on the repo. |
| `GITHUB_REPO` | `api/build-demo.js` | Defaults to `gauravpassi/upcore-website`. |
| `SITE_BASE_URL` | `api/build-demo.js` | Used to build the demo URL returned to the caller. Defaults to `https://upcore.ai`. |
| `GOOGLE_SHEETS_WEBHOOK_URL` | `api/lead-magnet-submit.js` | Google Apps Script Web App URL (ends `/exec`) — the lead-magnet CRM **and** the peer-benchmark store. No service-account auth, no OAuth, no Vercel KV (this account has no Vercel Pro plan): the Apps Script appends one row per lead to a Google Sheet AND returns the niche's running aggregate (count/avgOverall/avgByDim) in the same response — the Sheet is the only data store this feature needs. Setup script + instructions in `lp/` (see FEATURES.md B4). If unset, the function logs a warning and returns `{sufficientData:false}` rather than failing the whole request. |

| `BOOKING_SHEETS_WEBHOOK_URL` | `api/booking-intent.js` | Apps Script Web App URL (ends `/exec`) for the booking Sheet — see [TRACKING.md §5](TRACKING.md#5-booking-conversions). Unset = intents are not stored (endpoint returns 202). |
| `BOOKING_WEBHOOK_TOKEN` | `api/booking-intent.js` | Shared secret sent with every intent; must equal the Apps Script property `WEBHOOK_TOKEN`. |

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
| Google Tag Manager | Tag/pixel management container. **V4 pages load all tags through it** (GA4, Ads, Conversion Linker, Clarity) behind the `{tagging:'gtm'}` flag; the container definition is [`tools/gtm-container-upcore-v4.json`](../tools/gtm-container-upcore-v4.json). See [TRACKING.md](TRACKING.md). | Container ID `GTM-MH5PB32L` hard-coded in two places per page: the loader `<script>` as the very first thing in `<head>` (above GA4/Clarity), and the `<noscript><iframe>` fallback immediately after the opening `<body>` tag. Both on all 70 non-demo pages. Bulk-replace both if the container changes. |
| Google Analytics 4 (`gtag.js`) | Pageview/traffic analytics | Legacy pages: property ID `G-TVRF5M70ES` hard-coded (script `src` + `gtag('config', ...)`) directly below the GTM block in `<head>`. V4 pages: via GTM only (never add `gtag.js` to them). Bulk-replace if the property changes. |
| Microsoft Clarity | Session recording / heatmaps | Legacy pages: project ID `xtvhi9nvqa` hard-coded in the inline snippet directly below the GA4 block. V4 pages: GTM Custom HTML tag, only after `analytics_storage` consent. Bulk-replace if the project changes. |
| Vercel | Hosting + deploy + cron-relay-via-GitHub-Actions | `vercel.json` |
| Google Apps Script (Web App) | Lead-magnet CRM **and** peer-benchmark store — `api/lead-magnet-submit.js` POSTs one row per submission to a Sheets-bound Apps Script webhook, which appends the row and returns the niche's running aggregate (count/avgOverall/avgByDim) computed from the sheet's own rows. No Vercel KV, no database — deliberately, since this account has no Vercel Pro plan. | Env var `GOOGLE_SHEETS_WEBHOOK_URL`; the Apps Script source lives outside this repo (given to the user directly, not committed — it's account-specific, not code this repo can own) |
| Google Apps Script (Web App) — bookings | Booking intents Sheet + calendar matching → GA4 Measurement Protocol `booking_completed` and Google Ads offline-conversion rows | Env vars `BOOKING_SHEETS_WEBHOOK_URL`, `BOOKING_WEBHOOK_TOKEN`; source committed at [`tools/booking-conversions.gs`](../tools/booking-conversions.gs) (secrets live in Script properties, never in the repo) |
| jsPDF (CDN) | Client-side PDF generation for the two lead-magnet pages | `<script>` tag, `cdnjs.cloudflare.com/ajax/libs/jspdf` |

## 8. Things that look broken but aren't

- **`demos/manifest.json` is `[]`** — that's the expected state when no demos are live. The cleanup workflow truncates it.
- **`<style>` blocks duplicated across 37 pages** — intentional. See [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) for how to keep them in sync.
- **In-memory rate limit "leaks" across cold starts** — by design; we accept some over-limit demos in exchange for not running a KV.
- **Chat widget hard-codes its own colors instead of using `:root`** — by design; widget must render correctly even if the host page didn't define `:root`.

## 9. Deploys (production blocked unless the commit author is Gaurav's GitHub account)

- **Dev:** `git push dev main` deploys `upcore-website-dev` (https://upcore-website-dev.vercel.app).
- **Production:** project `upcore-ai-workforces` (team `gauravpassis-projects`) serves www.upcoretech.com, Git-connected to `gauravpassi/upcore-website` `main`.
- **Git deploys on production are BLOCKED** (`seatBlock: COMMIT_AUTHOR_REQUIRED`) unless the head commit's author is the GitHub account `gauravpassi`. Commits authored as `Upcore <upcoretech@gmail.com>` are blocked, as happened on launch day.
- **Three ways to ship:**
  1. The head commit is authored by Gaurav's GitHub account.
  2. The account owner deploys from the CLI: export the commit with `git archive <sha>` into an empty folder (no `.git`, so no author check), then from that folder run `VERCEL_ORG_ID=team_u6ZGrna1j8I7c2K3KAHWZiTr VERCEL_PROJECT_ID=prj_jZXe1p8PuDNEaicVWNWRnUrE5uTa vercel deploy --prod --yes`. This is how the redesign launched on 2026-10-12.
  3. The Vercel plan or team allows the other committer.
- **A blocked deployment cannot be redeployed;** Vercel wants a fresh deployment.
- **The demo builder publishes by committing to `gauravpassi/upcore-website`** with `GITHUB_PAT`. Those deploys only succeed if the token belongs to the `gauravpassi` account.
