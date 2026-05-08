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
- **The `:root` CSS block and the `<nav>` block are duplicated across all 37 pages and MUST stay in sync.** Recent commits had to repair nav damage from per-page edits. When changing either, propagate to every page in the same commit. Canonical source: `index.html`.
- **`cleanUrls: true`** — internal links omit `.html` (`/about`, not `/about.html`).
- **Anthropic model `claude-haiku-4-5-20251001` is hard-pinned in two places** (`api/chat.js`, `api/build-demo.js`). Bump both together.
- **`demos/manifest.json` is owned by the demo builder + nightly cleanup cron** — don't hand-edit. `[]` is a valid state.
- **All form/booking emails go to `gaurav@upcoretechnologies.com`** via FormSubmit, hard-coded in 4 places. Change all four together.
- **Chat widget (`chat-widget.js`)** is included on every non-demo page. It's a single vanilla-JS IIFE — don't refactor into modules.

## Local development

- Run with `vercel dev` (required for `api/` functions, `cleanUrls`, and redirects to behave like prod).
- No tests, no lint. Save → reload.
- Required env vars: `ANTHROPIC_API_KEY`, `GITHUB_PAT`, `GITHUB_REPO`, `SITE_BASE_URL`. See [docs/ARCHITECTURE.md §5](docs/ARCHITECTURE.md#5-environment-variables).
