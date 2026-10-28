# Content pipeline (since 2026-10-28)

An AI writer drafts library articles for www.upcoretech.com from a researched backlog; a person approves each one
before it goes live. Nothing here is served publicly (`.vercelignore` excludes `tools/` and `*.md`).

| File | What it is |
|---|---|
| `backlog.json` | The queue: ~46 new articles plus refreshes, ordered, with keywords, angle, outline, original asset, author questions and fact-checks per item. `status`: `queued`, `drafting`, `in_review`, `published`, `blocked` |
| `WRITER.md` | The procedure the writer follows: pick the next item, research the current search results, write the JSON, build, validate, commit on `content/<slug>`, deploy a preview, write a review note |
| `PUBLISH.md` | The procedure after a person says `approve <id>`: bring it onto `main`, rebuild, push, show what goes live, deploy production, verify |
| `validate.py` | Pre-publish checks: schema, title/meta length, house style (no em dashes, US spelling, banned phrases), allowed HTML, links resolve, sources for figures, FAQs, byline, dates, built page/sitemap/hub. `--strict` for new articles |
| `deploy.py` | `preview [ref]` deploys to the upcore-website-dev project; `production --confirm-production` deploys `main` to www via the git-archive + Vercel CLI method in `docs/ARCHITECTURE.md` §9, after listing every commit that would go live |
| `reviews/` | One review note per drafted article (preview link, fact-check list, author questions, checklist) |

## Schedule

Runs as Claude scheduled tasks on Saswata's PC (they use the Claude subscription there):
- **New articles:** Tuesday and Thursday mornings.
- **Refresh:** Wednesday morning.
- **Pace limit:** the writer pauses while 3 or more articles wait for review.

Each run ends in a Claude session with the preview link and the questions for the author. Reply in that session:
- `approve <id>` publishes it.
- `revise <id>: ...` changes it.
- `skip <id>` sets it aside.

## Who's named on articles

Pipeline articles read "By Saswata Sengupta, Upcore Technologies" and "Drafted with AI assistance. Reviewed by
Saswata Sengupta before publication." (Saswata approves every article). Only people listed in
`tools/v4-build/authors.py` may be named; the leadership on /about is deliberately not named on articles. The 26
articles imported before the pipeline are credited to Upcore until a refresh puts them through the same review.

## Rules the writer can't break

No publishing without a person's approval in chat; no invented client stories, numbers or quotes; every figure
links to its primary source; claims about Upcore only from the live site; one primary keyword per URL. The full list
is in `WRITER.md` §0.
