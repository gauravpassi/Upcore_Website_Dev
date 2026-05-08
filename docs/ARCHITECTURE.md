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

### 3.1 `/api/chat` — Kai chatbot

[`api/chat.js`](../api/chat.js)

- **Brand voice + product/industry list lives in the `SYSTEM_PROMPT` string** at the top of the file. To change what Kai says about Upcore, edit that string.
- Calls Anthropic Messages API: `model: claude-haiku-4-5-20251001`, `max_tokens: 600`, last 20 messages forwarded.
- Response can include a `[BOOK_APPOINTMENT:{...json...}]` marker. Server **strips the marker before returning to the client** and fires fire-and-forget FormSubmit emails (notification to Upcore + confirmation to prospect).
- Vercel function: `memory: 256MB`, `maxDuration: 15s`.

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
| `ANTHROPIC_API_KEY` | `api/chat.js`, `api/build-demo.js` | Anthropic Messages API |
| `GITHUB_PAT` | `api/build-demo.js` | Contents-API token to commit demos. Needs `contents:write` on the repo. |
| `GITHUB_REPO` | `api/build-demo.js` | Defaults to `gauravpassi/upcore-website`. |
| `SITE_BASE_URL` | `api/build-demo.js` | Used to build the demo URL returned to the caller. Defaults to `https://upcore.ai`. |

The Anthropic model id is **hard-coded in two places** (`claude-haiku-4-5-20251001`). If you bump it, bump it in both files and validate that the system prompt still produces the expected JSON / booking-marker shape.

## 6. Local development

- Run with `vercel dev` — required for the `api/` functions and for `cleanUrls`/redirects to behave like prod. Static-only previews (`python -m http.server`, `npx serve`, etc.) work for read-only browsing but break anything calling `/api/*`.
- No build step. Save → reload.

## 7. External services & destinations

| Service | Used for | How to change |
|---|---|---|
| Anthropic API | Chat + demo generation | Env var + model string in two files |
| GitHub Contents API | Writing demo HTML + manifest | Env var `GITHUB_PAT`, `GITHUB_REPO` |
| FormSubmit.co | Static forms + chat booking + demo lead emails | Email is hard-coded as `gaurav@upcoretechnologies.com` in: `assessment.html`, `contact.html`, `api/chat.js` (`sendBookingEmails`), `api/build-demo.js` (`NOTIFY_TO`). Change all together. |
| Google Fonts | Poppins | `<link>` on every page |
| Vercel | Hosting + deploy + cron-relay-via-GitHub-Actions | `vercel.json` |

## 8. Things that look broken but aren't

- **`demos/manifest.json` is `[]`** — that's the expected state when no demos are live. The cleanup workflow truncates it.
- **`<style>` blocks duplicated across 37 pages** — intentional. See [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) for how to keep them in sync.
- **In-memory rate limit "leaks" across cold starts** — by design; we accept some over-limit demos in exchange for not running a KV.
- **Chat widget hard-codes its own colors instead of using `:root`** — by design; widget must render correctly even if the host page didn't define `:root`.
