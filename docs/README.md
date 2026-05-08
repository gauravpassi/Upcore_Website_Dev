# Upcore Website — Source of Truth

This folder is the **single source of truth** for how this website is built, styled, and operated. Everything here overrides assumptions, tribal knowledge, and "what looks right" based on a single file.

## Read order (start here)

| File | Read when |
|---|---|
| [STRUCTURE.md](STRUCTURE.md) | Getting oriented; deciding where a new file should live; understanding the directory layout. |
| [FEATURES.md](FEATURES.md) | Auditing what already exists; planning a new feature; finding which files participate in a given user-facing capability. |
| [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) | Touching anything visual: colors, fonts, nav, buttons, cards, spacing, gradients. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Working on serverless functions, the demo builder pipeline, the chat widget, deploys, env vars. |
| [CONVENTIONS.md](CONVENTIONS.md) | Adding/renaming a page, writing internal links, adding a vertical, deciding *how* something is done. |
| [CHANGELOG.md](CHANGELOG.md) | After shipping a feature or learning a non-obvious fact. **Append, don't overwrite.** |

> **For a brand-new session:** read [STRUCTURE.md](STRUCTURE.md) and [FEATURES.md](FEATURES.md) first to get oriented, then jump to whichever of the others fits the task.

## Working agreement

1. **Before changes** — skim the relevant doc above. If you're about to violate something it says, raise it; don't silently override.
2. **After changes** — if you introduced a new pattern, component, page type, env var, API endpoint, or design token, **update the relevant doc in the same change**. Add a one-line entry to [CHANGELOG.md](CHANGELOG.md) too.
3. **When docs and code disagree** — the code is currently winning, but the gap is a bug. Fix the doc (or the code) instead of leaving the contradiction.
4. **Don't fork the design system into a new file.** New components extend [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md).
5. **New feature shipped?** Add it to [FEATURES.md](FEATURES.md) under the right section (A/B/C/D) and add a [CHANGELOG.md](CHANGELOG.md) entry. New file/folder type? Update [STRUCTURE.md](STRUCTURE.md). Same change, not later.

## What lives where

- **Project root `CLAUDE.md`** — short pointer to this folder + the must-knows that future Claude Code sessions need before they touch anything. Don't duplicate the long-form content here into CLAUDE.md.
- **`docs/`** (this folder) — long-form truth.
- **`insights/ARTICLES-REFERENCE.md` and `insights/BATCH-*.txt`** — editorial/content metadata only. Not part of this source-of-truth set; do not move them here.
