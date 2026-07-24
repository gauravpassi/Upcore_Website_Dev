# Directory Structure

Current as of 2026-05-08. **Update this file whenever you add a new top-level folder, a new file category, or a new asset type.**

## Tree

```
upcore-website/
├── CLAUDE.md                          # Pointer to docs/ — auto-loaded by Claude Code
├── docs/                              # 📖 Source of truth (this folder)
│   ├── README.md                      # Index + working agreement
│   ├── DESIGN-SYSTEM.md               # Colors, fonts, components, do/don't
│   ├── ARCHITECTURE.md                # Stack, functions, demo pipeline, env vars
│   ├── CONVENTIONS.md                 # Naming, link rules, page-add checklists
│   ├── STRUCTURE.md                   # ← this file
│   ├── FEATURES.md                    # Feature inventory + extension guides
│   └── CHANGELOG.md                   # Append-only feature log
│
├── vercel.json                        # Routing, headers, function config
├── .gitignore
├── .vercelignore                      # Excludes *.py (internal one-off maintenance scripts) from the deploy
├── .github/
│   └── workflows/                     # GitHub Actions (daily demo cleanup cron)
│
├── api/                               # 🔌 Vercel serverless functions
│   ├── chat.js                        # /api/chat — Kai chatbot (Anthropic)
│   └── build-demo.js                  # /api/build-demo — demo generator pipeline
│
├── chat-widget.js                     # Global vanilla-JS chat widget (loaded on every page)
│
├── index.html                         # Homepage — CANONICAL :root + nav block
├── about.html                         # About
├── ai-engineering-governance.html     # FLAGSHIP — AI Engineering Governance / Fractional AI Officer
├── platform.html                      # "Four Products. One AI Partner." overview (incl. AI Governance)
├── agent-builder.html                 # Studio — agent builder marketing page
├── fde-engineers.html                 # FLAGSHIP — Forward Deployed Engineers (Studio delivery model)
├── sdlc-agent.html                    # Forge — software-without-a-dev-team page
├── pricing.html                       # FAO pricing + Forge/Studio/FDE add-on pointers
├── build-your-demo.html               # Interactive UI → POSTs to /api/build-demo
├── assessment.html                    # Discovery Call form → FormSubmit
├── contact.html                       # Contact form ⚠️ currently INERT (see FEATURES.md)
│
├── industries/
│   ├── index.html                     # Industries hub
│   ├── banking-finance.html           # 12 vertical pages, one per industry:
│   ├── edtech.html
│   ├── government.html
│   ├── healthcare.html
│   ├── legal-compliance.html
│   ├── logistics.html
│   ├── manufacturing.html
│   ├── marketing-agencies.html
│   ├── nbfc-loans.html
│   ├── real-estate.html
│   ├── retail-d2c.html                # /industries/ecommerce rewrites here
│   ├── saas-technology.html
│   ├── upcore-logo.png                # ⚠️ duplicated copies — see "Anomalies" below
│   └── upcore-logo.svg
│
├── insights/
│   ├── index.html                     # Insights/blog hub
│   ├── ARTICLES-REFERENCE.md          # Editorial metadata (NOT part of source-of-truth set)
│   ├── BATCH-1-SUMMARY.txt            # Editorial batch notes (legacy/reference only)
│   ├── BATCH-2-SUMMARY.txt
│   ├── BATCH-2-COMPLETE.txt
│   └── *.html                         # 16 long-form articles (one per topic/vertical)
│
├── demos/                             # 🤖 Owned by demo builder + cleanup cron
│   ├── manifest.json                  # [{ slug, expires, ... }] — DO NOT hand-edit
│   ├── ecommerce-myagent-ky7o92.html  # ⚠️ stale samples — see "Anomalies"
│   └── manufacturing-myagent-w6ihwp.html
│
├── images/
│   └── accolades/                     # Trust-strip badge SVGs (7 files)
│       ├── clutch.svg
│       ├── cmmi.svg
│       ├── iso27001.svg
│       ├── iso9001.svg
│       ├── nasscom.svg
│       ├── selectedfirms.svg
│       └── upwork.svg
│
└── (root assets)
    ├── upcore-logo.svg                # Primary logo (used in nav across all pages)
    ├── upcore-logo.png                # PNG fallback
    ├── favicon.ico
    ├── favicon-32.png
    ├── favicon-192.png
    ├── favicon-512.png
    └── apple-touch-icon.png
```

## Where new things go

| What you're adding | Where it goes |
|---|---|
| New top-level marketing page | Repo root, `kebab-case.html`. Add link in `index.html` nav. |
| New industry vertical page | `industries/<slug>.html`. Also: link from `industries/index.html`, add to chat `SYSTEM_PROMPT`, optionally extend `INDUSTRY_CONFIG` if demo builder should support it. |
| New insight/blog article | `insights/<slug>.html`. Link from `insights/index.html`. (Optional: update `insights/ARTICLES-REFERENCE.md` for editorial tracking.) |
| New serverless function | `api/<name>.js`. Add `functions[<path>]` config block in `vercel.json`. Document in [ARCHITECTURE.md](ARCHITECTURE.md). |
| New static asset (image/icon) | `images/<category>/`. Don't dump assets in repo root unless they're the favicon set. |
| New trust-strip badge | `images/accolades/<vendor>.svg`. Update marquee on `index.html`. |
| New global JS (rare) | Repo root, like `chat-widget.js`. Push back hard before adding — there's a strong bias toward inline page scripts. |
| New design token / component | Update [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) **first**, then propagate to every page's `:root`. See [CONVENTIONS.md §5](CONVENTIONS.md#5-adding-a-new-design-token--component). |
| New env var | Add to Vercel project settings + document in [ARCHITECTURE.md §5](ARCHITECTURE.md#5-environment-variables). |
| New permanent URL change | Add a redirect in `vercel.json`; never break inbound links silently. |

## Anomalies (current technical debt)

These exist in the working tree and are worth knowing about before you "tidy them up" — verify with the user before touching:

1. **`industries/upcore-logo.png` and `industries/upcore-logo.svg`** are duplicates of the root logos. Likely a leftover from when industry pages used relative paths. Pages currently reference root paths (`/upcore-logo.svg`), so these copies are unused — but confirm before deleting.
2. **`demos/ecommerce-myagent-ky7o92.html` + `demos/manufacturing-myagent-w6ihwp.html`** exist on disk while `demos/manifest.json` is `[]`. Either samples that pre-date the manifest convention, or orphans from a builder run that didn't update the manifest. Cleanup cron won't touch them (it iterates the manifest, not the directory).
3. **No `package.json`** — confirms the no-build-step architecture. If anyone ever needs to add one, that's a significant decision; document it.
4. **~9 one-off Python maintenance scripts at the repo root** (`fix_*.py`, `apply_*.py`, `propagate_design.py`) — used for past bulk find/replace edits across pages. Excluded from the live deploy via `.vercelignore` (2026-07-22, since they were previously publicly downloadable on the static site). No secrets inside them, but don't add new ones without the same exclusion in mind.

## Files explicitly excluded from the source-of-truth set

- `insights/ARTICLES-REFERENCE.md` and `insights/BATCH-*.txt` — these are *editorial* metadata for content authoring, not engineering docs. Don't move them under `docs/` and don't reference them from CLAUDE.md.
- `.claude/` — Claude Code session/worktree state. Auto-managed.
