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
