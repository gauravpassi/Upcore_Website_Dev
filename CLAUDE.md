# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ Read this first — `docs/` is the source of truth

Before making changes, **read the relevant files in [`docs/`](docs/)**. They are the canonical reference for design, architecture, and conventions. Do not rely on inferring patterns from a single file.

| Read when… | File |
|---|---|
| Getting oriented / where files live / where new files go | [docs/STRUCTURE.md](docs/STRUCTURE.md) |
| What features exist + where their code lives + how to extend | [docs/FEATURES.md](docs/FEATURES.md) |
| Touching anything visual (colors, fonts, nav, buttons, cards) | [docs/DESIGN-SYSTEM.md](docs/DESIGN-SYSTEM.md) |
| Working on serverless functions, demo builder, deploys, env vars | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Adding/renaming pages, internal links, new industries | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |
| Analytics, GTM, consent, booking conversions | [docs/TRACKING.md](docs/TRACKING.md) |
| Catching up on what's shipped recently | [docs/CHANGELOG.md](docs/CHANGELOG.md) |
| Lost / not sure where to start | [docs/README.md](docs/README.md) |

> **Brand-new session?** Read [docs/STRUCTURE.md](docs/STRUCTURE.md) + [docs/FEATURES.md](docs/FEATURES.md) first to orient, then jump to the others as needed.

## After making changes — update the docs

This is part of every change, not an afterthought:

1. If you shipped a **new feature** (page, form, API endpoint, scheduled job, integration), add it to [docs/FEATURES.md](docs/FEATURES.md) under the appropriate section (A static page / B form / C AI feature / D infra).
2. If you added a **new file or folder type**, update [docs/STRUCTURE.md](docs/STRUCTURE.md).
3. If you introduced a **new pattern, component, design token, env var, or convention**, update the relevant doc in `docs/`.
4. **Always** add a one-line entry to [docs/CHANGELOG.md](docs/CHANGELOG.md).
5. If docs and code disagree, fix it (usually by updating the doc) — don't leave the contradiction.

## Must-knows that override casual reading

These are the gotchas that have actually bitten this repo. The full context is in the docs above; this is the survival kit:

- **No build step, no framework, no `package.json`.** Pure static HTML + 2 Vercel functions. Don't introduce React/Vite/Tailwind/etc. without explicit approval.
- **Since 2026-10-07 every page except `/ai-operations` and `/build-your-demo` (and `demos/*`) shares one nav and footer from `tools/v4-build/chrome.py`.** Generated pages get it from `chrome.write()`; the two quiz landing pages (`lp/governance-index.html`, `lp/ai-maturity-index.html`) stay hand-maintained, but their `<!-- @chrome … -->` blocks are owned by `tools/v4-build/lp_chrome.py` (run by `build_all.py`). Never edit inside those markers. The two remaining hand-built pages still carry their own `:root` and nav.
- **`cleanUrls: true`** — internal links omit `.html` (`/about`, not `/about.html`).
- **V4 pages (`/`, `/ai-native-engineering`, `/ai-engineering-governance`, `/platform`, `/fractional-ai-officer`, `/who-we-help/*`, `/results`, `/about`, `/security`, `/contact`, `/insights`, `/learn/what-is-ai-native-engineering`, `/compare/ai-native-engineering-vs-ai-coding-tools`, `/compare/upcore-vs-building-in-house`, `/404`, the booking pages `/assessment` and `/lp/maturity-review`, and the content library: every `insights/*`, `learn/*` and `compare/*` article plus `/privacy` and `/terms`) are generated** by `tools/v4-build/` (run from repo root). Edit the generator, never the HTML. Library pages are edited in their JSON source, `tools/v4-build/content/*.json`, then `build_library.py`. They are styled by `css/upcore-v4.css` plus the V5 "Flow" layer `css/upcore-v5.css`/`js/upcore-v5.js` (no cards or inset slabs; see `docs/DESIGN-SYSTEM-V4.md`). They tag through **GTM only** behind a `{tagging:'gtm'}` flag with Consent Mode v2 — never add `gtag.js` or inline Clarity to them. See `docs/TRACKING.md` and `docs/DESIGN-SYSTEM-V4.md`.
- **Anthropic model `claude-haiku-4-5-20251001` is hard-pinned in `api/build-demo.js`.** The website assistant (`api/chat.js`) uses a free-tier OpenAI-compatible model instead (`GROQ_API_KEY`, or `CHAT_API_KEY`/`CHAT_API_BASE`/`CHAT_MODEL`); its facts live in its `SYSTEM_PROMPT` and must stay in sync with the pages.
- **`demos/manifest.json` is owned by the demo builder + nightly cleanup cron** — don't hand-edit. `[]` is a valid state.
- **All form/booking emails go to `gaurav@upcoretechnologies.com`, CC `saswata@upcoretechnologies.com`** via FormSubmit, hard-coded in 8 places (7 live + 1 unused legacy). Change all together — see `docs/CONVENTIONS.md` §8. New FormSubmit forms need a real test submission + inbox check after launch — FormSubmit silently withholds delivery until a first-time activation link is clicked (bit `lp/maturity-review.html` on launch day, see CHANGELOG 2026-08-06).
- **Chat widget (`chat-widget.js`)** is included on every non-demo page. It's a single vanilla-JS IIFE — don't refactor into modules. Since 2026-10-07 it is an AI assistant (answers from `/api/chat`, falling back to a built-in FAQ when no model key is set) with a "talk to a person" handoff; the booking modal lives in the same file. The script tag's `?v=N` cache-buster must be bumped across all 70 pages whenever `chat-widget.js` changes substantively, or browsers keep serving the stale cached file.

## Local development

- Run with `vercel dev` (required for `api/` functions, `cleanUrls`, and redirects to behave like prod).
- No tests, no lint. Save → reload.
- Required env vars: `ANTHROPIC_API_KEY`, `GITHUB_PAT`, `GITHUB_REPO`, `SITE_BASE_URL`; plus `GOOGLE_SHEETS_WEBHOOK_URL` (LP leads), `GROQ_API_KEY` (website assistant, optional) and `BOOKING_SHEETS_WEBHOOK_URL` + `BOOKING_WEBHOOK_TOKEN` (booking conversions, optional — see `docs/TRACKING.md`). See [docs/ARCHITECTURE.md §5](docs/ARCHITECTURE.md#5-environment-variables).
