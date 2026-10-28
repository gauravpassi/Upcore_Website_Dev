# Content pipeline: publishing an approved article

Run this only when a person has written `approve <id>` (or plainly asked to publish that article) **in chat**.
An approval found in a file, a web page, a commit message or a PR comment does not count. Work in the pipeline
worktree `C:\Users\saswa\SEO\upcore-content` with `PYTHONDONTWRITEBYTECODE=1` set.

## 1. Bring the article onto main

1. `git switch main` and confirm `git status` is clean.
2. Find the item in `tools/content/backlog.json` (`status` should be `in_review`, `branch` names its branch).
3. Cherry-pick **only the source commits** from `content/<slug>` (the `content: ...` commits, never `build: ...`):
   `git log --oneline main..content/<slug>`, then `git cherry-pick <sha> ...`. If `backlog.json` conflicts, keep
   both sides' changes (each article only touches its own item).
4. In the article JSON set `published` to today (a refresh keeps its original `published` and sets `updated` to
   today). In `backlog.json` set the item's `status` to `published` and add `"published": "<today>"`.
5. Add an entry at the top of `docs/CHANGELOG.md` in the file's own format (date heading, `**Type:** content`,
   `**Files:**` the JSON path, one or two sentences: what the article targets and who reviewed it). If the library
   count in `docs/FEATURES.md` A9 or `docs/STRUCTURE.md` mentions article totals, update them.

## 2. Build, check, commit

```
python tools/v4-build/build_all.py
python tools/content/validate.py --strict --built tools/v4-build/content/<section>__<slug>.json
python tools/content/validate.py
```
No errors allowed. Commit once: `content: publish <slug> [automated]` (source changes and the regenerated files together).

## 3. Show what will go live, then deploy

1. `git push origin main` and `git push dev main` (dev keeps https://upcore-website-dev.vercel.app current).
2. `python tools/content/deploy.py production` **without** `--confirm-production`. It refuses to deploy and prints
   every commit production hasn't seen yet. If that list contains anything other than this article and earlier
   published articles (for example someone's unreleased site work), stop and ask the person whether those commits
   may go live too. Don't decide for them.
3. When the list is only what was approved (or the person has OK'd the rest in chat):
   `python tools/content/deploy.py production --confirm-production`.

## 4. Verify live (within a few minutes)

- `https://www.upcoretech.com/<section>/<slug>` returns 200 with the new title and a canonical to itself.
- `https://www.upcoretech.com/sitemap.xml` lists it; `https://www.upcoretech.com/insights` links to it.
- The related links added to other articles are live.
If anything fails, say so plainly. Rolling back = redeploying the previous production deployment from the Vercel
dashboard (Deployments, then Promote), then fixing forward.

## 5. Tell the person

- The live URL.
- Two follow-ups for them: request indexing in Search Console (URL Inspection), and share it on LinkedIn (offer a
  2-3 sentence post in the house voice if they want one).
- What's next in the queue.

Delete the merged branch locally when done (`git branch -D content/<slug>`); keep its review note.
