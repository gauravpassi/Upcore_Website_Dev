# Conventions

Rules of the road. When in doubt, default to the existing pattern in the repo over "what would be cleaner."

## 1. File & URL naming

- Page filenames: lowercase, kebab-case (`banking-finance.html`, `nbfc-loans.html`). The filename **is the URL** (minus `.html`, since `cleanUrls: true`).
- Industries pages live under `industries/`. Insights articles live under `insights/`. Generated demo pages live under `demos/` and are owned by the builder + cleanup cron.
- Demo slugs are produced by `generateSlug()` in [`api/build-demo.js`](../api/build-demo.js): `{industry}-{agentName-slugified}-{6-char-rand}`. Do not generate them manually.

## 2. Internal links

- **Always omit `.html`.** `<a href="/about">`, not `<a href="/about.html">`. (`cleanUrls: true` will redirect `.html` URLs, but every redirect is a wasted hop.)
- Use root-absolute paths (`/industries/healthcare`), not relative (`../industries/healthcare.html`). It travels safely if the page is moved.
- If you change a page's URL, add a permanent redirect in [`vercel.json`](../vercel.json) — don't break inbound links.

## 3. Adding a new page (checklist)

1. Copy the closest sibling page (e.g. for a new industry, copy `industries/healthcare.html`).
2. Replace the content. **Keep the `:root` block, font `<link>`, and `<nav>` block untouched** — those are design-system canon.
3. In the nav, set `class="active"` on the link that points to this page.
4. Include the chat widget: `<script src="/chat-widget.js" defer></script>`.
5. Add inbound links from `index.html`, the relevant index page (`industries/index.html` or `insights/index.html`), and any cross-sell pages.
6. Add an entry to [CHANGELOG.md](CHANGELOG.md).

## 4. Adding a new industry to the Demo Builder

1. Extend `INDUSTRY_CONFIG` in [`api/build-demo.js`](../api/build-demo.js) with: `label`, `emoji`, `entityName`, `entityNamePlural`, `defaultAgentName`, `integrations[]`, `metricsTemplate[]`, `statusOptions[]`, `systemPromptContext`.
2. Update the dropdown / industry picker in [`build-your-demo.html`](../build-your-demo.html).
3. Add the industry to Kai's `SYSTEM_PROMPT` industry list in [`api/chat.js`](../api/chat.js) if it's a new vertical.
4. Add the matching marketing page under `industries/` (see §3 above).
5. Smoke-test the builder end-to-end with `vercel dev` and a real Anthropic key.

## 5. Adding a new design token / component

1. Update [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) **first** with the new token/component spec.
2. Add it to the `:root` block in `index.html`.
3. Propagate to every other page's `:root` (search-and-replace + spot-check).
4. Use it. Don't ship a partial rollout.

If a new component is page-specific and won't be reused, document it inline in that page only — don't pollute DESIGN-SYSTEM with one-off styles.

## 6. Editing the nav

This is the highest-risk surface in the repo (recent commits had to repair it). See [DESIGN-SYSTEM.md §4.1](DESIGN-SYSTEM.md#41-nav-most-sensitive--pixel-perfect-across-all-37-pages). Always:

1. Edit `index.html` first.
2. Diff every other page's `<nav>` block against it.
3. Keep `class="active"` correct per page.

## 7. Editing brand copy / messaging

- Site-wide brand voice for the chatbot lives in `SYSTEM_PROMPT` in [`api/chat.js`](../api/chat.js). Update there.
- The "What we build" / "Industries served" / "How it works" lists in `SYSTEM_PROMPT` should match the marketing pages. If you add a product or industry, update both.
- Pricing is intentionally unpublished. Don't add fixed prices to pages.

## 8. Forms & email destinations

- All forms route to FormSubmit.co with target `gaurav@upcoretechnologies.com`. The destination is hard-coded in **four places** (see [ARCHITECTURE.md §7](ARCHITECTURE.md#7-external-services--destinations)). When changing it, change all four.
- Don't introduce a new form-submission service or backend without approval.

## 9. What NOT to do

- ❌ Add React/Vue/Svelte/Next/Astro/etc.
- ❌ Add a bundler (webpack/vite/rollup/esbuild) or a `package.json` with build scripts.
- ❌ Add Tailwind, a CSS framework, or a CSS-in-JS layer.
- ❌ Extract a "shared header" component or shared CSS file.
- ❌ Hand-edit `demos/manifest.json` or any `demos/*.html` file (those are owned by the builder + cleanup cron).
- ❌ Skip the daily cleanup workflow because it "feels redundant" — without it, generated demos accumulate forever.
- ❌ Remove the chat widget from a page silently.
- ❌ Change the Anthropic model in only one of the two API files.
- ❌ Make destructive git operations (force-push, hard reset) without explicit approval.

## 10. Commit style

Recent history shows short, lowercase, type-prefixed messages: `chore: cleanup expired demos [automated]`, `fix: nav CSS damage from previous stripping pass`, `feat: add demo {slug}`. Match that style. The cron commits use `[automated]` — don't reuse that suffix for human commits.

## 11. When you're unsure

Default order:
1. Read the relevant `docs/` file.
2. Look at the closest existing example in the codebase.
3. Ask before introducing a new pattern.
