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
