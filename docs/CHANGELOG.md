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

## 2026-08-06 — Diagnose missing saswata@ notification on lp/maturity-review.html (FormSubmit activation gotcha, not a code bug)
**Type:** decision, content
**Files:** `CLAUDE.md`, `docs/CONVENTIONS.md`
User reported saswata@upcoretechnologies.com didn't receive a real production submission from `lp/maturity-review.html`. Re-verified every FormSubmit.co call site sitewide (8 locations, up from the previously-documented 5 — `lp/maturity-review.html`, `lp/lead-magnet-engine.js`, and `insights/index.html`'s newsletter form were added in recent sessions and hadn't been folded into the CLAUDE.md/CONVENTIONS.md count) — all 8 correctly target `gaurav@upcoretechnologies.com` with `_cc: saswata@upcoretechnologies.com`. No code defect found.

Diagnosed as FormSubmit's documented activation behavior instead: a brand-new (recipient, subject) combination's first-ever submission is silently withheld — no error, no bounce — until someone clicks FormSubmit's one-time "Activate your form" confirmation email, and this applies to the CC'd address independently of the primary recipient. `lp/maturity-review.html` only shipped this session, so the reported submission was very likely that page's first-ever real one. Recommended the user check saswata@'s inbox (and spam) for the activation email and confirm it; no further submissions from that page should need it once clicked. Documented the gotcha in both `CLAUDE.md` and `docs/CONVENTIONS.md` §8 as a required post-launch step for any future new FormSubmit-using page: do one real test submission and confirm both inboxes receive it before considering the form done.

## 2026-08-06 — Solutions nav dropdown + homepage cross-link + sitewide consistency audit fixes
**Type:** feature, fix
**Files:** all 71 nav-bearing pages (bulk), `index.html`, `about.html`, `platform.html`, `pricing.html`, `ai-engineering-governance.html`, `ai-adoption-strategy.html`, `docs/DESIGN-SYSTEM.md`, `docs/FEATURES.md`
Adding `ai-adoption-strategy.html` to the flat top-level nav (previous entry) pushed the nav to 8 items and visibly crowded the nav-CTA button on laptop-width viewports (confirmed via measurement: 0px gap at 1150px, well above the 768px mobile breakpoint — a dead zone with no responsive handling between them). Fixed by merging "AI Governance" + "AI Strategy" into a single "Solutions" dropdown (`.nav-dropdown-wrap`/`.nav-dropdown-trigger`/`.nav-dropdown-menu`, hover/focus-within reveal on desktop, flows inline/stacked on mobile — no JS required, pure CSS) — bulk-rolled out via an idempotent PowerShell script across all 71 nav-bearing pages (the 3 `lp/*.html` ad pages correctly excluded, no nav there). `ai-engineering-governance.html` and `ai-adoption-strategy.html` each mark their own Solutions trigger `class="...active"`. Added a small cross-link from `index.html`'s `#fao-section` to `/ai-adoption-strategy` so the new offer has a homepage touchpoint. Full design rationale in `docs/DESIGN-SYSTEM.md` §4.1.

Ran a 4-dimension sitewide consistency audit (pricing/stats arithmetic, nav/footer/CTA sync, copywriting/positioning, design/CSS phantom-class check) via parallel research agents, then fixed every confirmed issue:
- **Pricing arithmetic**: 3 ROI-multiplier claims didn't match their own stated inputs — `pricing.html`'s "~100×" breach-ROI line (real: $4.7M÷$23,988 = 196×, corrected to "~195×"), `ai-engineering-governance.html`'s matching "100x" line (real: $6.5M÷$23,988 = 271×, corrected to "270x"), and `ai-adoption-strategy.html`'s "20–30× less spend" claim (real range against its own $400K–$750K CAIO anchor is 16.7×–31.3×, corrected to "15–30×" — rounded down per this repo's established credibility convention, not up).
- **Broken nav**: 5 `insights/*.html` pages (`choosing-first-ai-agent`, `roi-business-case-ai-agents`, `marketing-ai-execution-vs-strategy`, `legal-ai-contract-review`, `government-ai-citizen-services`) were missing the "Home" nav link entirely — a pre-existing gap from an earlier nav task that never reached these 5 files, surfaced by the audit's exhaustive per-file check. Fixed.
- **Phantom CSS classes**: `.nav-dropdown-trigger` (used sitewide, never defined — added `display:flex;align-items:center` for proper caret alignment, bulk-rolled to all 71 pages) and 4 classes local to the two mirrored flagship pages' shared cost-of-inaction/pricing/case-study sections (`.cong-calc-lbl`, `.ps-row.muted`, `.cs-milestone`, `.cong-left` on `ai-adoption-strategy.html` specifically) — the last four turn out to be pre-existing, previously-documented-as-harmless debt on `ai-engineering-governance.html` (see this file's 2026-07-22 Part 10 audit entry) that got copy-pasted forward onto the new page; now given real (in most cases intentionally empty, matching precedent) CSS definitions on both files so neither shows up as a phantom class again.
- **Positioning gap**: `about.html`'s "FAO Specialists" team card and `platform.html`'s hero line still described the FAO narrowly as a code-governance-only specialist, predating the AI Adoption Strategy offer. Added a 4th "Strategy & Coordination FAO" archetype card to `about.html` (matching the profile already defined on `ai-adoption-strategy.html`), broadened the bio's opening sentence to cover both tracks, and added "or AI Strategy & Adoption" to `platform.html`'s hero sentence. Left `about.html`'s main hero H1/sub untouched — that copy is about the governance→agent-building value chain, a different axis than the two FAO engagement types, and rewriting it wasn't warranted by the finding.

## 2026-08-06 — New AI Adoption Strategy flagship page (Niche 2) + AI Engineering Governance enrichment from Grand Slam Offer docs
**Type:** feature, fix, content
**Files:** `ai-adoption-strategy.html` (new), `ai-engineering-governance.html`, `lp/ai-maturity-index.html`, `sitemap.xml`, footer Solutions column on 8 hub pages
User supplied 5 strategy documents (an `AIGOV_Final_Output_Updated_v3.xlsx` master sheet, two "Grand Slam Offer" drafts for Niche 1/Niche 2, and two LinkedIn/Apollo prospecting playbooks) formalizing the two-niche split the lead-magnet funnels already implement structurally. The offer docs proposed a much higher-ticket pricing model ($5K–$195K, inconsistent even within the same document) — explicitly **rejected**; kept "starting from $1,999/month" everywhere, both niches. The docs' real value was the sharper pain-point framing, the Day-14/30/60/90 (Niche 1) and 3-phase Diagnose/Design/Deploy (Niche 2) program structure, and the hire-cost comparison — not their price tags or 5-bonus dollar-value stacks (explicitly rejected as inconsistent with this site's tone; deliverables folded into program substance instead, no invented dollar figures).

Built **`ai-adoption-strategy.html`** — a new full flagship page for Niche 2 (AI Strategy & Adoption), mirroring `ai-engineering-governance.html`'s section architecture and `<style>` block exactly (added to `docs/DESIGN-SYSTEM.md` §7's `propagate_design.py` SKIP set). 3-phase framework (Diagnose & Decide / Design & De-Risk / Deploy & Prove) instead of governance's 5-layer one. No incidents-equivalent section and no monetized breach-cost stack — no real citable source exists for this niche, so those blocks were skipped rather than fabricated (only the MIT NANDA 95%-pilot-failure stat, already used in the quiz, and the already-approved $400K–$750K CAIO-hire and $500K+ Big-4 figures are reused). All CTAs route into the existing `lp/ai-maturity-index.html` quiz / `lp/maturity-review.html` booking funnel, **not** `#book-governance` (that opens the wrong, Niche-1-framed Calendly modal). No new nav slot — matches the `fde-engineers.html` precedent.

Enriched `ai-engineering-governance.html`: 4 pain cards (was 3, added "No Inventory") each now carry a sharper first-person quote + a solution-title tag; L1 and L4 framework layers gained a capability each (closing real gaps — L1 had nothing about *what AI exists*, L4 had one fewer capability than every other layer); added the previously-missing Day-14 policy-live milestone to the 90-Day Journey, FAQ, and FAQPage JSON-LD; added a new "What exactly are you guaranteeing?" FAQ synthesizing the 4 conditional guarantees with an explicit non-guarantee closing line, and tightened the walk-away CTA copy to specify what's kept vs. owed.

**Companion fix:** `lp/ai-maturity-index.html` (built the same day, earlier in this session) had 3 places quoting "$5K–$30K/mo" — a leftover from before today's pricing decision, and directly in this new page's CTA path. Fixed to "starting from $1,999/month" throughout.

Added `/ai-adoption-strategy` to `sitemap.xml` and the footer Solutions column on 8 hub pages (`index.html`, `ai-engineering-governance.html`, `platform.html`, `pricing.html`, `fde-engineers.html`, `sdlc-agent.html`, `agent-builder.html`, `about.html`) — same rollout scope as the FDE Engineers page, not all 70 pages.

## 2026-08-06 — Fix CTA-mismatch: dedicated booking page for AI Maturity Index funnel + dead Calendly link fix on assessment.html
**Type:** fix, feature
**Files:** `assessment.html`, `lp/maturity-review.html` (new), `lp/ai-maturity-index.html`, `lp/lead-magnet-engine.js`
A CRO audit flagged that the AI Maturity Index quiz's "skip to booking" and post-quiz CTAs both routed to `/assessment` — a page titled "Book an AI Governance Review" with EU AI Act/HIPAA/SOX/GDPR compliance-framework qualifying questions, entirely mismatched to the Maturity Index's own portfolio-value/ROI framing. Per the exact spec supplied by Gaurav: built a dedicated `lp/maturity-review.html` booking page (portfolio-value headline/tiles/copy, a "What's driving this conversation now?" dropdown replacing the compliance-framework dropdown, zero GDPR/HIPAA/SOX/EU AI Act language anywhere) and re-pointed `lp/ai-maturity-index.html`'s `NICHE_CONFIG.bookingHref` to it — a one-line change that cascades to both the hero's pre-quiz "skip to booking" link and the post-quiz Full Result CTA via the shared engine. `/assessment` and the Governance Index funnel are untouched and still route there.

Added score/tier handoff: `lead-magnet-engine.js` gained `_bookingUrl()`, which appends `?tier=&score=` to the booking link once the quiz result is known (pre-quiz links stay plain — no score yet). Both `assessment.html` and `lp/maturity-review.html` read those params on load and show a "we'll pick up from exactly there on the call" personalized line (plus a hidden form field so the value reaches the team-notification email). Verified end-to-end in-browser for both funnels: Governance Index → `/assessment?tier=...&score=...`, Maturity Index → `/lp/maturity-review?tier=...&score=...`.

Added a "What happens on the call" section (4 bullets, adapted per-offer) to both booking pages per Gaurav's priority-2 instruction — cheap, reduces booking hesitation on both CTA paths.

**Independently discovered, unrelated to the reported issue:** `assessment.html`'s post-submission Calendly widget pointed to `calendly.com/gaurav-upcore/governance-review` — confirmed via direct request to return **HTTP 404**, an unreplaced placeholder the code's own comment warned about. This means the site's primary lead form's Calendly step has never let a visitor actually book a real slot after submitting. Fixed to the known-working `calendly.com/saswata-upcoretechnologies/30min` link (confirmed 200 OK, already used correctly elsewhere via `chat-widget.js`'s `#book-governance` modal).

`lp/lead-magnet-engine.js?v=2` → `?v=3` on both landing pages (cache-buster bump, required per this repo's established gotcha — see 2026-08-05 entries below).

**Not done this pass (deprioritized by Gaurav as priority-4 polish):** hero scarcity line + FAQ #4 on the Maturity Index page — blocked on exact copy, not yet supplied.

## 2026-08-05 — Bump lead-magnet-engine.js cache-buster (client-side notification fix wasn't loading)
**Type:** fix
**Files:** `lp/governance-index.html`, `lp/ai-maturity-index.html`
The previous entry's client-side notification fix was live in the deployed file but not actually reaching visitors: `lead-magnet-engine.js?v=1` had never been bumped despite several substantive edits to that file across this session (jitter fix, GA4 events, Typeform redesign, this notification fix) — browsers/Vercel's CDN kept serving the stale cached copy. Confirmed directly on the live production page: `typeof engine._sendTeamNotification` was `undefined` even after the new code was deployed, because the cached script simply didn't have that method yet. Same cache-buster discipline `CLAUDE.md` already documents for `chat-widget.js` applies here too — now noted for this file as well. Bumped `?v=1` → `?v=2` on both pages.

## 2026-08-05 — Real fix: move lead-magnet team notification to client-side (Cloudflare blocks Vercel server-side)
**Type:** fix
**Files:** `api/lead-magnet-submit.js`, `lp/lead-magnet-engine.js`
The Referer-header fix (previous entry) turned out to be necessary but not sufficient. Added a temporary `_debug` field to the API response and re-tested — the real error was `FormSubmit error 403: <!DOCTYPE html>...<title>Just a moment...</title>...`, Cloudflare's bot-detection interstitial challenge (Cloudflare fronts FormSubmit.co). **Cloudflare returns this 403 challenge to Vercel's serverless outbound IPs regardless of headers** — it's not solvable from a Node.js `fetch()` call, only from an actual browser. Confirmed directly: the identical FormSubmit payload sent from a real browser tab succeeds every time; the same payload sent server-side from Vercel gets challenged every time.

**Fix:** removed `sendTeamNotification` from `api/lead-magnet-submit.js` entirely (it can never work from a serverless function against this specific FormSubmit/Cloudflare combination) and moved it to `lp/lead-magnet-engine.js` as `_sendTeamNotification`, fired client-side from `_onSubmitResult` — the same working pattern already used by `contact.html` and `chat-widget.js`. It builds the email from `apiResult`'s server-verified `tier`/`overallScore`/`dims`/`weakestDim` (added `weakestDim` to the API response), not the client's own locally-computed score, so the notification content is still authoritative even though the request now originates from the browser. Removed the temporary `_debug` field and the now-unused `NOTIFY_TO`/`NOTIFY_CC`/`SITE_URL` constants from the API file.

Verified end-to-end in-browser against the live production API: submitted the full 10-question flow twice, confirmed via `performance.getEntriesByType('resource')` that the client-side FormSubmit call fires and completes with no errors both times.

**Known pre-existing risk, not fixed in this pass:** `api/build-demo.js`'s demo-lead notification and prospect-confirmation emails use the identical server-side FormSubmit pattern and almost certainly hit the same Cloudflare block — the Referer-header fix applied to that file (previous entry) is necessary but likely still insufficient, same as it was here. Moving it client-side would need a larger refactor of the demo-builder flow (the notification currently fires from inside the same function that generates and commits the demo HTML) — flagged as follow-up work, not addressed now since the user's immediate report was specifically about the lead-magnet pages.

## 2026-08-05 — Fix silent FormSubmit failures on server-side (Vercel function) calls
**Type:** fix
**Files:** `api/lead-magnet-submit.js`, `api/build-demo.js`
User reported not receiving the lead-magnet "assessment complete" summary emails. Root-caused by testing FormSubmit.co directly: it requires a `Referer`/`Origin` header identifying a real website, and rejects requests without one — but returns **HTTP 200 with an HTML error page** ("Unable to submit form... Make sure you open this page through a web server") instead of a proper error status. Browser-side `fetch()` calls (contact.html, chat-widget.js, assessment.html's native form POST) send this header automatically, so those have always worked. Server-side calls from Vercel serverless functions do **not** send a Referer automatically — so `api/lead-magnet-submit.js`'s team notification, and (pre-existing, unrelated to this session's work) `api/build-demo.js`'s lead notification + prospect confirmation email, were silently failing every time despite the code's own `if (!res.ok)` check reporting success (`res.ok` was `true` — FormSubmit's 200 status hid the failure).

Fixed by explicitly setting `Referer`/`Origin: https://www.upcoretech.com` on every server-side FormSubmit call in both files, and hardening the success check to also scan the response body for `"Unable to submit form"` (belt-and-suspenders — catches this failure mode even if FormSubmit ever changes its status-code behavior). Verified the fix directly: the same POST to FormSubmit.co returns FormSubmit's actual "Thanks!" confirmation page with the header set, vs. the silent error page without it.

**Pre-existing bug, not introduced this session:** `api/build-demo.js`'s demo-lead team notifications and prospect confirmation emails have had this same silent-failure bug since that feature was built — worth mentioning in case past demo leads were never actually delivered by email (the demo itself and `demos/manifest.json` entry were never affected, only the email step).

## 2026-08-05 — Audit all forms send to both team inboxes; fix fake newsletter form
**Type:** fix
**Files:** `insights/index.html`
Sitewide audit per user request: every form submission (and the new lead-magnet assessment-complete notifications) should reach both `gaurav@upcoretechnologies.com` and `saswata@upcoretechnologies.com`. Checked every FormSubmit.co call site: `assessment.html`'s main form (`_cc` hidden input), `contact.html`, `chat-widget.js` (`LEAD_EMAIL`/`LEAD_CC`), `api/build-demo.js` (`NOTIFY_TO`/`NOTIFY_CC`), and `api/lead-magnet-submit.js` (`NOTIFY_TO`/`NOTIFY_CC`, already sending the full score + tier + per-dimension breakdown + weakest area, built earlier this session) — all already correctly send to both addresses (one as primary, one as `_cc`). No changes needed there.

Found one real bug while auditing: `insights/index.html`'s newsletter signup form (`handleNewsletter()`) was completely fake — it called `e.preventDefault()`, showed a "✓ You're subscribed!" success message, and never sent the email anywhere. Fixed to actually POST to FormSubmit.co (`gaurav@upcoretechnologies.com`, cc `saswata@upcoretechnologies.com`), matching the async fetch pattern already used in `contact.html`. Verified live in-browser — the fix works and the browser sandbox actually has network access to formsubmit.co (unlike Google's ad-tech domains, which are blocked), so a real one-off test submission (`test@example.com`) was sent to both inboxes during verification.

## 2026-08-05 — Fix "Book a Governance Review" buttons pointing to /assessment instead of Calendly
**Type:** fix
**Files:** `about.html`, `ai-engineering-governance.html`, `index.html`, `pricing.html`, `platform.html`, `privacy.html`, `terms.html`
Sitewide audit per user request: every "Book a Governance Review" button should open the Calendly popup (`href="#book-governance"`, caught by `chat-widget.js`'s delegated click listener), not navigate to `/assessment`. Nav CTAs were already consistent (65+ instances, all correct) — the inconsistency was in 10 body/hero/final-CTA buttons across 5 pages that had drifted to `/assessment` at various points: `about.html` (hero, cta_final), `ai-engineering-governance.html` (journey, cta), `index.html` (hero, cta), `pricing.html` (hero, cta), `platform.html` (tab-governance secondary CTA, cta_final — the last one spans multiple lines with an inline SVG icon, easy to miss with a naive single-line search). All 10 switched to `href="#book-governance"`. Verified via `grep` that zero `data-gtm-cta="book-a-governance-review"` buttons still point to `/assessment` anywhere in the repo, and confirmed live in-browser that clicking a fixed button opens the Calendly iframe modal.

Also fixed two stale content references found during the same audit, left over from this session's earlier Google Calendar → Calendly switch: `privacy.html`'s "Calendar bookings" section still described the flow as "Google Calendar Appointments"; `terms.html`'s third-party-links list still named "Google Calendar" instead of "Calendly". Both corrected to describe the actual current integration.

**Not fixed in this pass, flagged separately:** `privacy.html`'s "AI chat with Kai" section still describes messages as being sent to Anthropic — stale since `chat-widget.js` was revamped into a client-side FAQ menu earlier this session with no AI backend call. Out of scope for this button audit; spun off as its own task.

## 2026-08-05 — Wire real Google Ads conversion labels for Assessment Complete
**Type:** feature
**Files:** `lp/lead-magnet-engine.js`, `lp/governance-index.html`, `lp/ai-maturity-index.html`
User created two separate Google Ads conversion actions (their choice, over one shared action — lets each niche's ad campaign optimize independently) and supplied both labels. Set `googleAdsConversionLabel`/`Value`/`Currency` on both `NICHE_CONFIG` objects: Governance Index → `AW-16546427858/ozjeCPjqqNwcENLn-dE9`, AI Maturity Index → `AW-16546427858/Aa1UCPvqqNwcENLn-dE9`, both `value:1.0, currency:'INR'` (matching the snippets Google Ads generated). Also added `value`/`currency` to the `gtag('event','conversion',...)` call in the engine (previously only `send_to`). Verified both fire correctly in-browser with the right label/value/currency at the `assessment_complete` moment. No more manual step pending — the lead-magnet conversion tracking is fully live.

## 2026-08-05 — Lead-magnet pages: GA4 events + Google Ads "Assessment Complete" conversion, ad-landing-page copy fix
**Type:** feature, fix
**Files:** `lp/lead-magnet-engine.js` (`pushEvent`, `_submitContact`), `lp/governance-index.html` + `lp/ai-maturity-index.html` (`events.assessmentComplete`, `googleAdsConversionLabel`, howItWorks copy)
User's ask: treat both pages as **ad landing pages** and add "assessment complete" as a Google Ads conversion with properly-named GA4 custom events. Two changes:

1. **`pushEvent()` now fires directly via `gtag('event', name, params)`, not just `dataLayer.push`.** Both pages already load `gtag.js` straight for GA4, so this lands events in GA4 Realtime immediately — no GTM trigger/tag configuration needed to see them. `dataLayer.push` is kept alongside for anyone who later wants GTM-based triggers too. Full event list documented in `docs/FEATURES.md` B4 — 8 events per niche (`index_*`/`maturity_*`), covering the whole funnel from quiz start through call-booked.
2. **New `{prefix}_assessment_complete` event** fires at the exact moment the email-gate form is submitted (same instant as the existing `email_captured`, distinctly named so it's unambiguous which event to mark as the GA4 key event / conversion). A `googleAdsConversionLabel` field was added to both `NICHE_CONFIG` objects (currently `null`) — once set to a real `AW-16546427858/<label>` string (from a new conversion action the user needs to create in Google Ads), the same moment also fires `gtag('event','conversion',{send_to:...})`, matching the exact pattern already used by `assessment.html` and `chat-widget.js`'s Calendly conversion. Left as a documented placeholder rather than fabricated — verified the code path is fully wired and doesn't error when the label is unset (skips the Ads ping, GA4 event still fires).

Also fixed a real copy bug found while auditing these pages as ad landing pages: the "How it works" step 3 on both pages still said "Get a full PDF report emailed" — stale from before the Phase A simplification to immediate in-browser download (no email delivery at all). Now says "Download your full PDF report instantly."

Checked mobile responsiveness of the new Typeform-style quiz (most ad-click traffic is mobile) — hero CTA is above the fold with no scroll needed, quiz question/options render cleanly at 375px width, no overflow.

**Manual step still needed:** create a Google Ads conversion action named something like "Assessment Complete" (one shared or two per-niche — user's call), then set `googleAdsConversionLabel` on the relevant `NICHE_CONFIG`(s) to the resulting `AW-16546427858/<label>` string.

## 2026-08-05 — Fix jittery quiz re-render on every option click
**Type:** fix
**Files:** `lp/lead-magnet-engine.js`
User reported the quiz "gitters a lot" after clicking each option. Cause: selecting a single-select option calls `_render()` immediately (to show the highlighted state) before the 280ms delayed advance to the next question — both that intermediate re-render and the real navigation rebuilt the same `.lm-quiz-anim` element, so the slide-in entrance animation played twice in quick succession on every click (same root cause would've hit multiselect toggling too). Fixed by tracking a `_lastQuizRenderKey` (`'q'+qIndex` or `'insight'+qIndex`) and only attaching the `lm-quiz-anim` class when that key actually changes — re-renders for the same question (selection highlight, multiselect toggle) skip the animation; real navigation (next question, back, insight interrupt) still plays it. Verified via direct class-presence checks before/after a click.

## 2026-08-05 — Lead-magnet quiz rebuilt as Typeform-style one-question-at-a-time flow
**Type:** fix
**Files:** `lp/lead-magnet-engine.js` (quiz rendering rewrite), `lp/governance-index.html` + `lp/ai-maturity-index.html` (quiz CSS + dropped now-unused `progressStyle`/`screensPerView` config fields)
User feedback on the shipped quiz UI: **"Design wise terrible, make it more interactive questionnaire, beautiful design, more like typeform questionnaire."** Replaced the old grouped-screens-with-a-scan-log-or-Continue-button flow with a proper one-question-at-a-time experience on both niches: thin animated progress bar + "N / total" counter at the top, a `←` back button (re-shows the previous answer, editable), a category eyebrow label above each question, numbered option rows (1–9) with a hover micro-shift and a fade/slide-in transition between questions. Keyboard navigation added — press 1–9 to select (single-select auto-advances after a brief highlight, matching the click behavior), Enter confirms a multiselect question and continues, Backspace goes to the previous question. Insight interrupts (previously a small card stacked below the question) are now their own centered full-screen interstitial, shown at the same trigger point as before (right after the specific question that earns them is answered) via a new `state.pendingInsight` + `_dismissInsight()` mechanism, so their exact timing is unchanged.

Internally this replaced screen-grouped rendering (`state.screenIndex` + `config.screens[i].questions.forEach`) with a flat question list (`allQuestions(config)` — already existed for scoring, now reused for the UI) driven by `state.qIndex`; `_findScreenForQuestion()` looks up a question's parent screen only for its category label and insight-interrupt config. `config.progressStyle` and `config.screensPerView` are no longer read by the engine and were removed from both pages' `NICHE_CONFIG` objects as dead config. One side effect, not a regression: `ai-maturity-index.html`'s 2-questions-per-screen grouping is gone — every question is now its own screen on both niches, which is the correct Typeform-style behavior the user asked for, not an accidental loss of the original design (the original 2-per-screen grouping was itself the layout being replaced).

Verified end-to-end in-browser on both pages: full 10-question click-through, keyboard-only click-through (number keys + Enter + Backspace), the multiselect question (doesn't auto-advance, Enter/Continue confirms), and both niches' insight interrupts firing at the correct question.

## 2026-08-05 — Lead-magnet backend: drop Vercel KV, Sheet-computed peer stats + FormSubmit team notification + branded PDF
**Type:** feature, fix
**Files:** `api/lead-magnet-submit.js`, `lp/lead-magnet-engine.js` (`_generatePdf` + branding helpers), Apps Script source (given to user, not committed)
User doesn't have a Vercel Pro plan, so Vercel KV isn't usable — corrected with **"dont overcomplicate stuff... using existing api used in our website."** Two changes:

1. **Peer-benchmark storage moved from Vercel KV into the Google Sheet itself.** The Apps Script webhook (`doPost`) now reads the sheet's own rows for the matching niche, computes `count`/`avgOverall`/`avgByDim`, and returns that aggregate in its response — `api/lead-magnet-submit.js` just relays it (gated at the same 30-response honest-FOMO threshold as before). No database, no KV, one less moving part, works on any Google account for free.
2. **Team notification via FormSubmit.co** — the same service already used by `assessment.html`/`contact.html`/`chat-widget.js`/`api/build-demo.js`, so no new API key. Fires alongside the sheet write (`Promise.allSettled`, one failing doesn't block the other) with the lead's tier, score, dimension breakdown, and UTM data, matching the existing lead-notification pattern.

Also upgraded the client-side PDF report (`_generatePdf` in `lead-magnet-engine.js`) from plain text-and-bars to an actually branded report: teal header band on every page, a score card with a colored tier badge and peer-comparison callout on the cover, per-dimension bars with a peer-average tick marker on the breakdown page, and a dark CTA box with the booking link on the closing page. Caught and fixed one real bug while visually verifying the generated PDF (decoded and rendered the actual output, not just checked for exceptions): the `60/100` score text overlapped itself on the cover page because `doc.getTextWidth()` was called *after* the font size had already been changed for the `/100` suffix, so it measured the wrong glyph width — fixed by capturing the width immediately after drawing the number, before changing font size.

Sent the user an updated Apps Script file with setup + redeploy instructions (Apps Script Web Apps require "New version" under Manage Deployments to pick up code changes — editing alone isn't enough).

## 2026-08-05 — Lead-magnet backend (Phase B): Google Sheets CRM + Vercel KV peer-benchmark, not Apollo
**Type:** feature
**Files:** `api/lead-magnet-submit.js` (new), `vercel.json` (functions entry), `lp/governance-index.html` + `lp/ai-maturity-index.html` (`config.api.submit` wired to the real endpoint), `docs/ARCHITECTURE.md` (env vars + external services)
User corrected the CRM choice for Phase B: **"no apollo crm just a google sheet crm."** `api/lead-magnet-submit.js` now recomputes the score server-side (never trusts a client-submitted score — trivially spoofable), POSTs one row per lead to a Google Sheet via a Google Apps Script Web App webhook (`GOOGLE_SHEETS_WEBHOOK_URL`), and updates a per-niche peer-benchmark aggregate in Vercel KV (`KV_REST_API_URL`/`KV_REST_API_TOKEN`, raw REST `fetch()` pipeline calls — no `@vercel/kv` package, matches the repo's zero-npm-deps rule). No `APOLLO_API_KEY`, no custom-field-ID lookup, no service-account auth — the Apps Script webhook needs nothing more than a URL. The Apps Script source (`doPost` handler) is account-specific and was handed to the user directly rather than committed to this repo.

Both landing pages' `NICHE_CONFIG.api.submit` now points at `/api/lead-magnet-submit` (previously an empty object / Phase A stub). Verified client-side wiring end-to-end under the static preview server (which has no `/api/*` routing, so the POST correctly 404s): the engine's existing fetch-failure fallback in `_submitContact` still degrades gracefully to a client-only score with `peer.sufficientData:false`, so a CRM/KV outage in production never blocks a visitor from seeing their result and downloading the PDF. Full live backend verification (a real Apps Script Web App + a real Vercel KV instance) still needs `vercel dev` with real env vars — not testable in this environment.

**Known gap, not a regression:** the original spec's CIO/CTO title-based cross-routing rule (route a Niche-2 submission to the Niche-1 offer if the contact is a CIO/CTO) was never implemented — the built email-gate form only collects firstName/email/company, no title field. Flagged in `docs/FEATURES.md` B4 rather than silently dropped.

Remaining: Phase C (GTM event QA, UTM/gclid persistence QA, soft-disqualify QA, LCP check) is still open. Manual prerequisites before this can be tested live: user creates a Google Sheet + deploys the given Apps Script as a Web App and sets `GOOGLE_SHEETS_WEBHOOK_URL` in Vercel; a Vercel KV store is attached to the project (auto-populates the two `KV_REST_API_*` vars).

## 2026-08-05 — Two ad-only lead-magnet landing pages: Governance Index + AI Maturity Index (Phase A)
**Type:** feature
**Files:** `lp/lead-magnet-engine.js` (new), `lp/governance-index.html` (new), `lp/ai-maturity-index.html` (new), `robots.txt` (`Disallow: /lp/`)
Phase A of the approved lead-magnet plan (see `docs/` plan history / PART 13): two net-new, isolated, paid-traffic-only landing pages, each a 10-question scored quiz gated behind an email, with an immediate client-side PDF download (jsPDF via CDN `<script>`, no transactional email service — matches the "don't overcomplicate" simplification). `/assessment` and its funnel are untouched. Both pages are `noindex,nofollow`, have no `<nav>` and no chat-widget (a deliberate, documented exception — paid landing pages shouldn't have a competing interactive element), and share one mechanical engine (`lead-magnet-engine.js`, same precedent tier as `chat-widget.js`/`cta-tracking.js`) driving two content-owning pages: `governance-index.html` (dark "developer console" skin, 5-axis radar chart, chip-style auto-advancing progress) and `ai-maturity-index.html` (light "executive scorecard" skin, 4-stage maturity curve + 10-axis radar, screen-style progress with an explicit Continue button, 2 questions/screen). Backend (`api/lead-magnet-submit.js`, Apollo CRM write, Vercel KV peer-benchmarking) is Phase B, not yet built — the email-gate submit currently uses a documented client-only stub (`console.warn('[lead-magnet] Phase A stub...')`) so the full UX is reviewable before real credentials exist.

Found and fixed two real bugs in the engine while verifying both pages end-to-end in-browser: (1) `_answerQuestion` auto-advanced the whole screen after the *first* answered question even when a screen has two questions (both pages' screens are 2-questions-per-screen) — silently left the second question unanswered/scored-as-0. Fixed by only auto-advancing once every question on the current screen is answered. (2) The `Continue` button (used on `screensPerView>1` screens, i.e. `ai-maturity-index.html`) was permanently disabled — `el()`'s attribute setter called `setAttribute('disabled', null)` to mean "not disabled," but `setAttribute` with any value, including the string `"null"`, still makes a boolean HTML attribute present. Fixed by skipping `setAttribute` entirely for `null`/`false`/`undefined` attr values in the shared `el()` helper. Verified via live click-through of both full flows (all 10 questions, insight interrupts, soft-disqualify option, email gate, full result, PDF download with no console errors) after each fix.

Remaining for Phase A: none — this closes it. Phase B (`api/lead-magnet-submit.js`, Apollo, Vercel KV) and Phase C (GTM event QA, UTM persistence QA, LCP check) are still open per the plan.

## 2026-07-29 — Full-site SEO deep audit: GSC verification, structured data, CLS, hreflang
**Type:** fix
**Files:** all 70 non-demo HTML pages (logo `width`/`height`), `index.html` (5 accolade SVG dims), `pricing.html`/`privacy.html`/`security.html`/`terms.html` (hreflang tags)
Ran a deeper sweep beyond the earlier same-day audit, checking things not yet verified: Google Search Console (confirmed connected via a domain-level DNS TXT record, `google-site-verification=bZ7oRsO8...` — no meta-tag/file-based verification in the codebase, DNS is the sole method and it's the most robust of the three); live production checks against `upcoretech.com` (robots.txt and sitemap.xml both match the repo and return 200; live `<head>` confirmed charset/viewport genuinely first now); JSON-LD validity across all 70 pages (0 parse errors; the 13 pages that looked "unknown-type" turned out to correctly use the valid `@graph` pattern bundling Article+FAQPage, not a real issue); zero hardcoded `http://` links (no mixed-content risk); zero relative `og:image` URLs.

Two real, fixable findings from this pass: (1) 145 `<img>` tags (the site logo, repeated across all 70 pages, plus 5 homepage accolade SVGs) had no `width`/`height` attributes — a Core Web Vitals (CLS) risk since the browser can't reserve layout space before the image loads. Fixed by adding each image's real native dimensions (logo: 360×240 from the source PNG; SVGs: their own `viewBox` dimensions) — CSS still controls final rendered size (`.nav-logo img{height:60px;width:auto}` etc.), the HTML attributes just let the browser compute the correct aspect ratio immediately. (2) 4 pages (`pricing.html`, `privacy.html`, `security.html`, `terms.html`) had a canonical tag but no self-referencing `hreflang` tags, unlike the other 66 pages — added the same `en` + `x-default` pair for consistency.

Confirmed as correct/intentional, not issues: `build-your-demo.html`'s `noindex,nofollow` (matches its `robots.txt` disallow), `privacy.html`/`terms.html`'s `noindex,follow` (standard for legal boilerplate).

## 2026-07-29 — Fix remaining SEO audit findings: title/description lengths, sitemap
**Type:** fix
**Files:** 12 pages (`<title>` trims), `fde-engineers.html` (meta description trim), `sitemap.xml` (+`/security`)
Closed out the minor findings from the same-day SEO audit. Trimmed 12 titles from 61–71 chars down to 42–58 chars (decoded/entity-aware count), preserving the core keyword and `| Upcore` suffix on each — e.g. `security.html` dropped the redundant "Technologies" (67→54 chars), `learn/ai-workforce-platform.html` dropped the "Buyer's Guide 2025" qualifier (63→42 chars). Re-checked `index.html`'s meta description with entities decoded and found it was actually already fine at 158 displayed chars (the earlier audit's 162 count included the raw `&amp;` source length, not the 1-char rendered `&`) — left it untouched. `fde-engineers.html`'s description was genuinely over even decoded (182 chars) — trimmed to 154 by dropping "in your workflow" and "to ship AI" while keeping the $2,499/month anchor and the OpenAI/Anthropic/Databricks social proof. Added `/security` to `sitemap.xml` (priority 0.6, since it's real content with search value, unlike `/privacy`/`/terms`/`/build-your-demo` which stay correctly excluded). Verified: 0 titles or descriptions outside the 30–60/70–160 decoded-character guidelines sitewide, 0 new duplicate titles/descriptions/H1s introduced, diff touches exactly the 14 intended files.

## 2026-07-29 — SEO audit + fix: restore meta charset/viewport to top of <head>
**Type:** fix
**Files:** all 70 non-demo HTML pages (2-line move each)
Ran a full technical + on-page SEO audit specifically checking for regressions from the recent GTM/GA4/Clarity/Ads/CTA-tagging changes. Found one real issue: adding those tracking scripts pushed `<meta charset>` and the viewport meta tag down to byte offset ~1160 in every page — past the 1024-byte window browsers use for early encoding detection, and no longer the first element in `<head>` as the HTML spec recommends. Moved both back to be the literal first two lines inside `<head>`, before the GTM/GA4/Clarity/Ads block, on all 70 pages (max offset now 47 bytes). Verified via `git diff --numstat` that every page's diff is a clean 2-added/2-removed move, no content lost.

Full audit results — everything else came back clean: 0 duplicate titles/descriptions/H1s across all 70 pages, exactly one `<h1>` per page, canonical tags present everywhere, all image `alt` text present, zero broken internal links (verified against `vercel.json` redirects/rewrites), sitemap.xml's 66 URLs all map to real pages (the 4 pages correctly excluded — `/build-your-demo` per robots.txt, `/privacy`, `/terms`, and `/security` — are reasonable omissions, `/security` being the only one worth reconsidering later as a content page with real search value). Minor, non-blocking opportunities noted but not fixed: 12 titles run 61–71 chars (vs. the ~60 guideline) and `fde-engineers.html`'s meta description is 186 chars (vs. ~160) — cosmetic SERP-truncation risk, not indexation-breaking. `privacy.html`/`terms.html` lack Open Graph tags and JSON-LD (reasonable for legal boilerplate pages).

## 2026-07-29 — Switch booking widget to Calendly; wire up primary Google Ads conversion
**Type:** feature | infra | decision
**Files:** `chat-widget.js` (bottom IIFE + cache-buster bump), all 70 non-demo HTML pages (`chat-widget.js?v=10` → `?v=11`), `docs/FEATURES.md`, `docs/ARCHITECTURE.md`
User clarified the conversion hierarchy from the previous entry: the assessment.html form submission should be the *secondary* conversion, and the *primary* should be "click Book a Governance Review anywhere, then successfully book a meeting." Google Calendar's public appointment-scheduling embed (used until now for the "Book a Governance Review" modal, sitewide via `a[href="#book-governance"]`) doesn't expose any postMessage/callback signal when a visitor actually finishes booking a slot inside the iframe — cross-origin, no completion event — so there was no way to distinguish "opened the modal" from "actually booked." Flagged this constraint and asked the user to choose between firing on click (inaccurate — overstates conversions), switching to a booking tool with a real completion signal, or dropping the calendar-modal tracking entirely; user chose to switch. Replaced the Google Calendar iframe with Calendly (`https://calendly.com/saswata-upcoretechnologies/30min`, same modal chrome, same trigger mechanism) and added a `window.addEventListener('message', ...)` listener (checking `e.origin === 'https://calendly.com'` first) that fires `gtag('event', 'conversion', {send_to: 'AW-16546427858/_Q5SCO7LodgcENLn-dE9'})` only on Calendly's genuine `calendly.event_scheduled` event — i.e. an actually-completed booking, not a click. The assessment.html conversion (`AW-16546427858/CN8BCPra5LsZENLn-dE9`) is untouched and stays wired exactly as before; the user still needs to mark it Secondary and the new one Primary in the Google Ads dashboard itself (not something settable from code). Bumped `chat-widget.js?v=` from 10 to 11 across all 70 pages since the change is substantive.

## 2026-07-29 — Add Google Ads conversion tracking
**Type:** infra
**Files:** all 70 non-demo HTML pages (1-line `gtag('config', ...)` addition each), `assessment.html` (conversion event), `docs/FEATURES.md`
Per Google Ads' own "already installed a Google tag" instructions (the site already has `gtag.js` loaded for GA4), added `gtag('config', 'AW-16546427858')` right after the existing `gtag('config', 'G-TVRF5M70ES')` call on all 70 pages — reusing the existing loader script rather than installing a second, duplicate `gtag.js` tag (which Google explicitly warns against). Skipped the AMP-specific instructions entirely since this site isn't built with AMP. Installed the Lead conversion event (`AW-16546427858/CN8BCPra5LsZENLn-dE9`) on `assessment.html` only, scoped inside the existing `if(window.location.search.includes('submitted=true'))` block that already shows the post-submit success message (the target of the FormSubmit `_next` redirect) — this fires the conversion exactly once per real completed Discovery Call booking, never on a normal page load, since Google's literal snippet (unconditional, dropped anywhere in `<head>`) would have fired on every visit to whatever page it was placed on. Verified in-browser: zero conversion events on a plain `assessment.html` visit, exactly one correctly-shaped event (`{event:'conversion', send_to:'AW-16546427858/CN8BCPra5LsZENLn-dE9'}`) on `assessment.html?submitted=true`.

## 2026-07-29 — Tag every primary/secondary CTA for GTM/GA4 click tracking
**Type:** feature | infra
**Files:** `cta-tracking.js` (new), all 70 non-demo HTML pages (293 CTA `<a>` tags + 1 new `<script>` tag each), `docs/FEATURES.md`, `docs/STRUCTURE.md`
Wrote a one-off HTML-aware Python script (`html.parser`-based, no external deps) to find every genuine primary/secondary CTA sitewide — deliberately excluding card links, footer badges, and "back" navigation by using a curated allow-list of button classes (`btn-teal`/`btn-fill`/`btn-primary`/`nav-cta`/`btn-p`/`btn-cta`/etc. = primary; `btn-ghost`/`btn-o`/etc. = secondary) rather than a blanket selector. Found and tagged 293 CTAs across 70 pages with three attributes: `data-gtm-cta` (slugified from the button's own visible text, e.g. "Book a Governance Review →" → `book-a-governance-review` — deliberately reusable across pages so identical copy rolls up together in reporting, with per-page segmentation left to GA4's own `page_path`), `data-gtm-cta-type` (`primary`/`secondary`), and `data-gtm-cta-section` (nearest ancestor element's `id` when present — preferred over any closer heuristic match — else a fallback: `nav`, `footer`, `hero`, `cta_final`, `other`). Caught and fixed two real classification bugs during review before applying: (1) broadening CTA-block detection to match any class containing "cta" (not just the exact token `cta-section`) initially caused agent-builder.html's 10 distinct per-industry-panel secondary CTAs to collapse into one generic label, fixed by making explicit `id`-based markers always take priority over heuristic class-based ones regardless of nesting depth; (2) the original fallback label "top" was actively misleading (it was firing on final-page CTA blocks wrapped in unlabeled `<div>`s, not literal page-top content) — renamed to "other" for honesty. Added [`cta-tracking.js`](../cta-tracking.js), a single vanilla-JS IIFE (same pattern as `chat-widget.js`) that listens for clicks on any `[data-gtm-cta]` element and pushes `{event:'cta_click', cta_id, cta_type, cta_section, cta_text, cta_url, page_path}` to `window.dataLayer`; wired in via `<script src="/cta-tracking.js?v=1" defer>` immediately after the `chat-widget.js` tag on every page. Verified in-browser: clicking a tagged CTA produces the exact expected dataLayer entry, no console errors. Configuring the GTM Custom Event trigger and the GA4 Event tag to actually surface this in GTM/GA4 reporting is a manual step in the GTM web UI — not something committable to this repo.

## 2026-07-29 — Add Google Tag Manager sitewide
**Type:** infra
**Files:** all 70 non-demo HTML pages (new head `<script>` + body `<noscript>` blocks), `docs/ARCHITECTURE.md`
Installed GTM (container `GTM-MH5PB32L`) per Google's standard two-part snippet: the loader script as the very first thing in `<head>` — above the existing GA4/Clarity blocks, per Google's own placement guidance — and the `<noscript><iframe>` fallback immediately after the opening `<body>` tag. Same one-off Python-script approach as the GA4/Clarity rollouts (LF/CRLF- and BOM-safe, verified `<head>`/`<body>` each occur exactly once per file first). Verified every diff is a clean 11-line pure insertion (7 head + 4 body lines), 0 deletions, across all 70 files. Demo pages excluded, matching the existing analytics-script convention.

## 2026-07-29 — Add Microsoft Clarity sitewide
**Type:** infra
**Files:** all 70 non-demo HTML pages (new `<script>` block in `<head>`), `docs/ARCHITECTURE.md`
Inserted Microsoft Clarity's tracking snippet (project ID `xtvhi9nvqa`) immediately after the GA4 `gtag.js` block on every page, via a small one-off Python script that matched the exact post-GA4 anchor per file (handling both LF and CRLF line endings and preserving each file's original BOM state, so the diff is a clean 8-line pure insertion on every file — verified via `git diff --numstat`). Demo pages (`demos/*.html`) intentionally excluded, matching the existing GA4/analytics-script convention for auto-generated pages.

## 2026-07-29 — Replace GA4 measurement ID sitewide
**Type:** infra
**Files:** all 70 non-demo HTML pages (`gtag.js` script `src` + `gtag('config', ...)` call)
Swapped the Google Analytics 4 property from `G-T4WFSX3C90` to `G-TVRF5M70ES` per the exact snippet from Google's "Install manually" setup screen, bulk-replaced across every page (2 occurrences per file — the loader script tag and the config call). Verified zero remaining references to the old ID anywhere in the repo, including demo pages.

## 2026-07-24 — Revamp chat widget: one-click FAQ + email lead capture
**Type:** feature | decision
**Files:** `chat-widget.js`, all 70 non-demo HTML pages (cache-buster bump only), `docs/FEATURES.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/STRUCTURE.md`, `CLAUDE.md`
Rebuilt Kai from a live Anthropic-backed conversation into a self-contained client-side FAQ menu, per explicit request: "common questions and answers should be answered in one click and custom questions will be submitted on our mail as a lead form." Added a `CATEGORIES`/`FAQ` data structure (6 categories, 12 questions grounded in real site content — FAO, FDE, Studio pricing, industries, security) rendered as one-click chips; a "📂 Browse All Topics" card grid (redesigned with hover-lift `.uc-topic-card`s, gradient header, fade-in message animation) drills into any category. Anything typed into the free-text input is no longer sent to the Anthropic API — it starts a short name → email capture, then POSTs directly to FormSubmit (`gaurav@upcoretechnologies.com`, cc'd to a second inbox), mirroring `assessment.html`/`contact.html`'s existing pattern, and shows a "Message Sent" confirmation instead of an AI-generated reply. Verified end-to-end in-browser: one-click answers, category drill-down, the "Book a Governance Review" chip re-opening the existing calendar modal, invalid-email rejection, and the exact FormSubmit payload on successful submission. `api/chat.js` (the old Anthropic backend, `SYSTEM_PROMPT`, `[BOOK_APPOINTMENT:{...}]` marker) is no longer called by the widget — left in place as unused legacy rather than deleted, and documented as such everywhere it was previously referenced as load-bearing. Bumped the `chat-widget.js?v=` cache-buster from 9 to 10 across all 70 pages in the same commit (required — browsers cache the script by exact URL, so skipping this would leave visitors on the old AI-chat version).

## 2026-07-24 — Build FDE Engineers flagship page + integrate sitewide
**Type:** feature | content
**Files:** `fde-engineers.html` (new), `about.html`, `agent-builder.html`, `pricing.html`, `sitemap.xml`, `docs/FEATURES.md`, `docs/STRUCTURE.md`
After the 2026-07-22 revert, researched the "Forward Deployed Engineer" (FDE) concept properly via web search before rebuilding: confirmed Palantir originated the role and that OpenAI, Anthropic, Cohere, Databricks, and Scale AI now run their own versions of it; sourced real failure-rate stats (RAND 2025: 80% of AI projects fail to deliver value; Gartner June 2025: 40%+ of agentic pilots canceled by 2027; S&P Global 2025: $7.2M average sunk cost per abandoned large-enterprise AI initiative) and real FDE compensation data ($180K–$550K+ depending on seniority/company) to ground every claim on the new page — no fabricated stats or named-company incidents (used anonymized "Failure Patterns" instead). Built `fde-engineers.html` mirroring `ai-engineering-governance.html`'s exact section architecture and CSS component library (hero delivery-log widget labeled "— Example" per the site's static-mockup convention, 5-stage Discover/Build/Integrate/Deploy/Iterate framework accordion, price-stack + econ-cards economics, anonymized client-outcome composites). One clean retainer price sitewide: starting from $2,499/month — deliberately avoided the dual-tier $799/$2,499 confusion from the reverted 2026-07-22 attempt. Integrated with exactly one link each from `about.html` (3rd team card, "The FDE Engineers"), `agent-builder.html` (new `.fde-callout` box in the Investment section), and `pricing.html` (3rd `.addon-card` + footer Solutions link) — scoped to agent-building pages only, no homepage/nav changes, per the confirmed integration-scope decision. Added `/fde-engineers` to `sitemap.xml` and documented the new page in `docs/FEATURES.md` (A4b) and `docs/STRUCTURE.md`.

## 2026-07-22 — Revert all "FDE Engineers" content
**Type:** content | decision
**Files:** `about.html`, `agent-builder.html`, `platform.html`, `index.html`, `industries/index.html`, `pricing.html`
User asked to revert the FDE (Forward Deployed Engineer) concept sitewide and reconsider how/whether to integrate it properly later, rather than iterating further on today's rollout. Removed: the FDE team-card on `about.html` (back to 2 cards: Gaurav Passi, The FAO Specialists), the FDE bullet on `agent-builder.html`'s Phase 2 card and its Investment section mention, the FDE mentions on `platform.html`'s hero and Studio tab, the `.fde-badge` and its usage on `index.html`, the FDE mention on `industries/index.html`'s hero, and the entire FDE pricing plan on `pricing.html` (price-anchor section, what's-included grid, JSON-LD Product schema, 2 FAQ entries, the dedicated FAQ question, and the now-unused `.src-note` CSS rule). Preserved everything unrelated that was bundled in the same prior commits: the site-wide nav "Home" link, Gaurav's "Co-Founder & CEO" title, the `industries/index.html` duplicate "View suite" button fix and stale "14 Industry Workforces" count fix, and the Team section's stacked full-width card layout (kept since it's a genuine improvement independent of how many cards it holds). Verified zero remaining "FDE"/"Forward Deployed Engineer"/"$2,499" references sitewide, and pricing.html's tag balance/JSON-LD/phantom-class checks all pass post-revert.

## 2026-07-22 — Add "Home" to nav site-wide
**Type:** content
**Files:** all 69 pages
Nav previously had no way back to the homepage except clicking the logo. Added `<li><a href="/">Home</a></li>` as the first nav item across all 69 pages via a verified bulk script (confirmed present on every page afterward, correct item count, no duplicates). `index.html` itself marks Home as `class="active"`, matching the existing active-state convention for other nav items.

## 2026-07-22 — Add FDE Engineers pricing plan; fix about.html team-card issues
**Type:** feature | fix | content
**Files:** `pricing.html`, `about.html`, `agent-builder.html`
(1) Gaurav Passi's title corrected from "Founder & CEO" to "Co-Founder & CEO". (2) Removed the "Explore Studio →" link from the FDE Engineers team-card (no replacement requested). (3) "Meet Your FAO →" now links to `/ai-engineering-governance#solution` (scrolls to the FAO intro) instead of `/assessment`; added a secondary "Book a Governance Review →" button matching the nav CTA, plus `margin-top` on `.team-links` for breathing room above the button row. (4) Built a full FDE Engineers pricing plan on `pricing.html`, mirroring the FAO plan's structure: a price-anchor comparison (Full-Time Integration Engineer $15,000+/mo vs. Agency/Contract Dev Shop $8,000+/mo vs. FDE Engineers by Upcore $2,499+/mo — "65–80% less spend", conservatively rounded down from the actual 69–83% range for credibility), a 5-stage "what's included" grid (Discovery & Workflow Mapping → Custom Agent Build → Systems Integration → Channel Deployment → Governed by Your FAO) plus an "Always included: Named FDE, Dedicated" card, a new JSON-LD Product schema (name "FDE Engineers by Upcore", price 2499), and 2 FAQ updates clarifying the $799 one-off Studio project rate vs. the $2,499/month dedicated retainer are two different things, not a contradiction. Cross-linked from the existing Studio add-on card and from `agent-builder.html`'s Investment section. Added the missing `.src-note` CSS rule the new section referenced (verified zero phantom classes in the new content before committing).

## 2026-07-22 — Make FDE mentions genuinely prominent (homepage badge + 2 more page heroes)
**Type:** content
**Files:** `index.html`, `platform.html`, `industries/index.html`
User re-emphasized wanting FDE visibility to "ride the hype" — the earlier additions (subhead sentences) were too easy to miss while scanning. (1) `index.html`: added a distinct `.fde-badge` pill ("🛠 Built & deployed by Forward Deployed Engineers (FDEs)") directly under the Agent Add-Ons H2, above the subhead — a scannable visual element, not just body text. (2) `platform.html`: added an FDE mention to the top-level hero paragraph (visible immediately, before any tab is clicked — previously FDE only appeared inside the Studio tab's content). (3) `industries/index.html`: added an FDE mention to the hero intro paragraph (previously zero FDE mentions on this page despite it being the primary agent-suite discovery page); also fixed a stale "12 Industry Workforces" eyebrow badge that should have read "14" since the hub grew to 14 cards earlier today.

## 2026-07-22 — Redesign Team section as stacked cards; fix duplicate "View suite" button
**Type:** fix
**Files:** `about.html`, `industries/index.html`
User reported the Team section still "looks terrible" after the earlier grid rebalance (2-col + full-width row). Root cause was more fundamental than alignment: mixing a half-width card format with a full-width one in the same grid reads as visually inconsistent regardless of alignment fixes. Redesigned `.team-grid` from a grid to a simple vertical flex stack — every card is now full-width, one per row, in logical order (Gaurav Passi → The FAO Specialists → The FDE Engineers). Added `max-width:680px` to `.team-bio` so paragraph text doesn't stretch into unreadably long lines now that cards are much wider; `.fao-archetypes` (already changed to a 3-column row) still uses the full card width. Removed the now-dead `.team-grid{grid-template-columns:1fr}` mobile override and the `.team-card-wide` class, both no longer needed.

Also fixed a duplicate-button bug on `industries/index.html`: every hub card already had a hardcoded `<a class="hub-view-link">View suite →</a>`, but a JS block (from a past "make cards clickable" fix) was also dynamically creating and appending a second one to every card via `document.createElement`/`appendChild`. Removed the dynamic link creation, kept the click-anywhere-on-card listener. Also added the 2 industries added earlier today (Software & Technology (SDLC), Compliance & Governance) to the `HUB_URLS` map, which had silently excluded them from the click-anywhere behavior (their hardcoded links still worked, just not the whole-card click target).

## 2026-07-22 — Fix Team section layout, expand FDE mentions to homepage + pricing
**Type:** fix | content
**Files:** `about.html`, `index.html`, `pricing.html`
User feedback: the 3-card Team section (added same day) looked bad, and FDE needed more visibility site-wide to "ride the hype." (1) Layout fix: `.team-grid` was `repeat(auto-fit,minmax(280px,1fr))` with default `stretch` alignment — since "The FAO Specialists" card (long bio + 3 stacked archetype blocks) was far taller than the other two, the shorter Gaurav Passi and FDE Engineers cards were stretching to match it, leaving large dead whitespace. Restructured to a 2-column grid with `align-items:start` (Gaurav Passi + The FDE Engineers side by side, similar content length) and gave "The FAO Specialists" a `.team-card-wide` (`grid-column:1/-1`) full-width row of its own, since it has the most content depth. Also changed `.fao-archetypes` from a stacked column to a 3-column row (collapsing to 1 column ≤768px) so the now-full-width card doesn't just get taller — it uses the width. (2) Added FDE mentions to `index.html`'s "Agent Add-Ons" section intro and `pricing.html`'s Studio add-on card, both naming "a dedicated Forward Deployed Engineer (FDE)" as who does the build/deploy work — extending the 3-page FDE rollout from earlier today to the two most-trafficked pages.

## 2026-07-22 — Add "FDE Engineers" (Forward Deployed Engineers) role
**Type:** content
**Files:** `about.html`, `agent-builder.html`, `platform.html`
The site named exactly one delivery role (the FAO, for governance) but never credited who actually builds/integrates/deploys Studio's custom agents — that work was described entirely in passive voice ("Custom agent built...", "Upcore configures, tests, and deploys..."). Added a new "The FDE Engineers" team-card on `about.html` (3rd card alongside Gaurav Passi and The FAO Specialists — `.team-grid` CSS changed from a fixed `1fr 1fr` to `repeat(auto-fit,minmax(280px,1fr))` to fit cleanly), named the role as the first bullet in `agent-builder.html`'s Phase 2 "Build & Deploy" card, and updated `platform.html`'s Studio tab description to say "delivered by a dedicated Forward Deployed Engineer (FDE)". Deliberately did NOT touch `sdlc-agent.html` (Forge) — that page's entire pitch is "zero team overhead, no dev team," so naming an FDE role there would contradict its own positioning.

## 2026-07-22 — Fix "Book a Governance Review" CTA on agent (non-governance) sections
**Type:** content
**Files:** `platform.html`, `agent-builder.html`
User feedback: agent product sections (Forge, Studio, AI Workforce) shouldn't use the governance-specific CTA label — booking a "Governance Review" doesn't fit a visitor evaluating an agent product. Changed `platform.html`'s Forge/Studio/AI Workforce tab CTAs (3 instances) and `agent-builder.html`'s hero-secondary + final CTA (2 instances) to "Book a Live Demo", matching `sdlc-agent.html`'s own already-established pattern. Left untouched: the site-wide nav CTA, `platform.html`'s whole-platform hero/bottom CTAs (cover all products, not agent-specific), and the AI Governance tab's own CTA (correctly governance-focused). Also fixed a footer-sync bug found along the way: both files' footer link had drifted to "Book a Governance Review" when the canonical (`index.html`) footer says "Book a Discovery Call" — corrected both to match.

## 2026-07-22 — Pre-live audit Sprint B12: exclude *.py scripts from deploy + doc staleness cleanup
**Type:** infra | fix
**Files:** `.vercelignore` (new), `docs/STRUCTURE.md`, `docs/FEATURES.md`
9 internal one-off Python maintenance scripts (`fix_*.py`, `apply_*.py`, `propagate_design.py`) sit at the repo root with no exclusion from the Vercel static deploy — likely publicly downloadable (e.g. `/fix_cta_buttons.py`) despite containing no secrets. Added `.vercelignore` to exclude `*.py`. While touching `docs/STRUCTURE.md`, also fixed a stale claim (`contact.html` form documented as "inert"/fake since 2026-05 — it was actually fixed to a real FormSubmit `fetch()` call at some point and the docs were never updated) — corrected in both `STRUCTURE.md`'s anomalies list and `FEATURES.md`'s B2 entry + Known Gaps section, per `CLAUDE.md`'s "if docs and code disagree, fix it" rule.

## 2026-07-22 — Pre-live audit Sprint B11: fix 10 broken Related Articles modules
**Type:** fix
**Files:** 10 `insights/*.html` article pages
The `.related-card h4`/`.related-card p` CSS selector only matched 6 of 16 article pages' actual markup. 5 pages used `<div class="title">`/`<div class="meta">` instead of `<h4>`/`<p>` (completely unstyled - no font hierarchy at all): `choosing-first-ai-agent.html`, `government-ai-citizen-services.html`, `legal-ai-contract-review.html`, `marketing-ai-execution-vs-strategy.html`, `roi-business-case-ai-agents.html`. 5 more used `<h3>` instead of `<h4>` (renders at default oversized browser heading size instead of the intended 14px/600): `banking-ai-customer-service.html`, `healthcare-patient-no-show-ai.html`, `logistics-wismo-ai-agents.html`, `real-estate-lead-conversion.html`, `saas-churn-ai-early-warning.html`. Fixed via a scoped script (matched only within each page's `related-grid` block, verified not to touch legitimate `<h3>` article subheadings elsewhere on the same pages).

## 2026-07-22 — Pre-live audit Sprint B9-B10: formalize amber/violet tokens, correct button-color doc
**Type:** decision
**Files:** `index.html`, `docs/DESIGN-SYSTEM.md`
(B9) Amber (`--amber`/`--amber-bright`) and violet (`--violet`) were used repeatedly in the Risk Monitor and FAO Explorer widgets for RAG severity coding but never declared in `:root`, contradicting the doc's "no amber token" rule (a leftover from the 2025-07 MiniMax redesign). Added both to `:root`, replaced every hardcoded solid hex occurrence with `var()`, and updated `DESIGN-SYSTEM.md` to document them as risk-status-only colors (not general branding — teal remains the only brand accent). (B10) `DESIGN-SYSTEM.md` documented the primary CTA (`.btn-fill`) as a black pill, but every page's actual `.btn-fill` is teal (`#0ABFCC`), 100% consistently — updated the doc to match reality rather than repaint every button. Also fixed a stale comment calling `--ink` an "alias for button fill" (it isn't, teal is) and added a doc note about the recurring "button uses an undefined class" bug pattern to help prevent it next time.

## 2026-07-22 — Pre-live audit Sprint B7-B8: footer certs sitewide, orphan industry pages linked into hub
**Type:** content | decision
**Files:** all 69 pages (footer), `industries/index.html`
(B7) `docs/DESIGN-SYSTEM.md` documents a footer certification strip (CMMI Level 3 · ISO 27001 · ISO 9001 · Nasscom Member) as standard, but only `index.html` actually rendered it. Rolled out the same `.footer-certs` block + CSS to all other 68 pages via a verified bulk script (confirmed HTML+CSS present on all 69 files afterward, zero corruption). (B8) `industries/compliance-governance.html` and `industries/tech-sdlc.html` existed but weren't linked from the 12-card hub, nav, or footer — added both as new cards on `industries/index.html` (now 14 cards total), updated the page's "12 Industry Workforces" stat and meta description to 14. The footer's "Industries" column is an intentionally curated 5-6 link sample ending in "View All →" on every page (never exhaustive) — left as-is, since the hub-card fix already makes both pages discoverable.

## 2026-07-22 — Pre-live audit Sprint B1-B6: pricing math, sitemap, SEO tags, product-story contradictions, copy artifacts, CTA labels
**Type:** fix | content
**Files:** `pricing.html`, `ai-engineering-governance.html`, `sitemap.xml`, `agent-builder.html`, `platform.html`, `index.html`, `about.html`
(B1) Pricing-savings copy ("70-80% less spend") was stale math left over from the old $4,000 price point — corrected to "80-90%" to match the current $1,999 floor, consistently across both pages. (B2) `sitemap.xml` was missing `/pricing` entirely and had a literal `` `n `` (unescaped PowerShell newline artifact) corrupting all 64 entries — regenerated cleanly with 65 URLs and realistic `lastmod` dates for recently-touched pages. (B3) Trimmed `agent-builder.html`'s title (67→50 chars) and meta description (183→139 chars) and `platform.html`'s title (69→47 chars) to fit SEO guidelines. (B4) Fixed 3 product-story contradictions that had regressed from earlier fixes: `platform.html` calling Studio "no-code" (contradicts its own corrected "managed deployment service" framing, fixed in 4 places including JSON-LD), `index.html`'s hero reintroducing an unverifiable "certified" FAO claim (also found + fixed in `ai-engineering-governance.html`'s FAQ, both visible text and JSON-LD twin), and `platform.html`'s "Compliance Autopilot" claim (softened to "Compliance framework mapping" elsewhere already, missed in one diagram). (B5) Fixed 79 instances across `agent-builder.html` (53), `platform.html` (17), and `about.html` (9) where a past "remove all em dashes" commit had replaced "—" with ". " mid-sentence, producing fragments like "...your business. deployed in 48 hours." — restored proper em dashes via a verified regex pass (each match manually reviewed for false positives before applying). (B6) Standardized `pricing.html`'s "Get a Quote" CTA and `platform.html`'s "Book a Demo" CTA to "Book a Governance Review", matching the site's dominant CTA label (note: `sdlc-agent.html`'s "Book a Live Demo" is an intentional, previously-documented exception — not touched).

## 2026-07-22 — Pre-live audit Sprint A: 3 launch-blocking bugs fixed
**Type:** fix
**Files:** `agent-builder.html`, `assessment.html`, `ai-engineering-governance.html`
(1) `agent-builder.html`'s hero CTA + 2 other primary buttons used `class="btn btn-fill"`, but neither class was ever defined in this page's stylesheet — same phantom-class bug already fixed twice this session elsewhere. Swapped to `.btn-hero-primary`/`.btn-primary`. (2) `assessment.html`'s submit handler referenced two nonexistent element IDs (`industry`, `confirm-email` — leftover from a past field-reduction edit), throwing a JS error on every submission that silently skipped the button loading state and the prospect confirmation email. Removed the dead references. (3) `ai-engineering-governance.html`'s hero dashboard said "— Live" with an animated pulsing dot and "LIVE" status badges over static hardcoded numbers, unlike `index.html`'s equivalent widget (already fixed to say "— Example" with a static dot). Matched the same treatment here.

## 2026-07-20 — Agent pricing anchor: "Starting at $799" for Forge/Studio
**Type:** content
**Files:** `pricing.html`, `sdlc-agent.html`, `agent-builder.html`
Added a public starting price for agent services (Forge, Studio) — previously both were quote-only with no number shown anywhere. "$799" now appears on pricing.html's two add-on cards + FAQ, and as the headline stat on each page's Investment section. Governance pricing ($1,999/mo) is unaffected — this anchor is agents-only. (Initially shipped as $149, corrected same-day to $799.)

## 2026-07-20 — Pricing floor $1,999/mo, Forge/Studio Investment sections, homepage/governance de-dupe
**Type:** content | decision
**Files:** `pricing.html`, `ai-engineering-governance.html`, `sdlc-agent.html`, `agent-builder.html`, `index.html`
FAO headline price changed from "under $4,000/month" to "starting from $1,999/month" everywhere (pricing.html hero/meta/JSON-LD/FAQ, governance page price-stack/cost-of-not-governing/econ-card). ROI multiplier on the governance page rounded from a literal ~271x (at the new lower price) down to a credible "100x" to match pricing.html. Added a labeled "Investment" section (no public numbers — quote-based, links to /pricing) to sdlc-agent.html and agent-builder.html, since neither had any pricing signal before. Homepage Problem-section H2 changed from a verbatim duplicate of the governance page's headline to distinct phrasing; FAO Explorer widget's 5 accordion rows trimmed from 3-bullet capability lists to 1-line summaries each, plus a "See the full framework →" link to the governance page — reduces homepage/governance content overlap while keeping the widget's live-log interactivity.

## 2026-07-20 — Homepage UI cleanup: clutter cuts, visual alignment, responsive fixes
**Type:** refactor
**Files:** index.html
Tier 1 cuts: removed ~80 lines dead CSS (prob-layout, products, old steps-grid, who-we-govern blocks); removed hero-metrics strip, fao-price-stack, persona-cta, cta-reversal, Nasscom/Upwork cert badges, bridge body+CTA, #who-we-govern section; CISO quote updated to be non-literal. Tier 2 visual: border-radius standardised across all cards/pills/panels (12/14→16px, 6→8px, 3→9999px); persona-card and tl-card ::before gradient top-bars replaced with border-top:3px solid teal; body line-height 1.6→1.75, hero-sub 16→17px, fao-desc 14→16px/opacity bump, fao-h2 + cta-title clamps standardised; #how-we-work bg bg→bg2, #cta bg bg3→bg; #fao-section #070B10→#0a0a0a. Tier 3 responsive: tl-grid 2-col at 1024px, addon-cards 2-col at 1024px/1-col at 600px, section padding 64px on mobile.

## 2026-07-20 — Sprint 8: External audit consistency fixes
**Type:** content fix
**Files:** ai-engineering-governance.html, index.html, agent-builder.html, about.html, platform.html, industries/index.html, all 69 pages (nav bulk)
A1: Dashboard widget layer names aligned to brand names (Accelerate/Protect/Comply/Optimise) — were using operational names (Code Review/Dependency Check/CI/CD Gate/Production Monitor). A2: index.html L1 capability bullets updated to match governance page (Spec & Goals Engine → AI risk inventory etc.). A3: $3.2B stat standardised to "In annual enterprise AI spend — zero team-level visibility or attribution" on both pages. A4: 45% vulnerability stat attribution fixed — index.html now cites Veracode 2025 (not Gartner). A5: "90-day proof of concept" reframed as "90-day engagement with a Day-30 walk-away checkpoint" with month-to-month continuation copy. A6: agent-builder.html "Deploy Time" label → "Agent Build Time"; index.html Day-90 milestone → "Full AI Workforce Operational"; OG meta updated to "First agent live within 30 days". A7: Amazon incident anonymized to "Fortune 10 Retailer" with source updated to Stack Overflow Blog · Developer Survey 2025. Sprint B: All major CTAs on 6 flagship pages unified — "Book a Governance Review →" pointing to /assessment; secondary distraction buttons removed. Sprint C: Nav "Services" → "AI Agents" (href stays /platform) and "Pricing" link added across 69 pages via PowerShell. Sprint D: about.html "Why We Started" rewritten governance-first — leads with the governance accountability gap, not agent tools. Sprint E: industries/index.html — teal "Governed by Default" callout strip added above industry card grid with link to /ai-engineering-governance.

## 2026-07-15 — Audit batch: M8, M13, M18, M19, M20 + sitewide minors
**Type:** content fix
**Files:** about.html, industries/index.html, sdlc-agent.html, compare/ai-workforce-vs-ai-tools.html, insights/index.html, all 66 pages (footer)
M8: Removed India-specific financial terms (NBFC, DPD bucket) from about.html origin story — replaced with international equivalents (specialist lending portfolios, delinquency schedules, Days Past Due schedules). M13: Added "View suite →" links to all 12 industry hub cards in industries/index.html using PowerShell targeted replacement — all 12 confirmed via grep. M18: Fixed Forge contradiction — "1× Train. Use Forever." → "Train once. Refine as you grow." and "Continuous retraining" → "Refinement" in sdlc-agent.html. M19: Compare page meta description updated — "6–8 AI SaaS subscriptions" → "10–14 disconnected AI tools" to match hero stat and body copy. M20: insights/index.html OG/Twitter titles and `<title>` tag updated from "India's Industries" to "AI Governance & Industry Strategy Insights". Minor: Facebook and Instagram social links removed from footer of 66 pages (sitewide PowerShell). Copyright year already 2026 sitewide — no change needed.

## 2026-07-14 — Sprint 5: C6 (case studies), M4 (FAO archetypes), M3 (72h qualification)
**Type:** content
**Files:** ai-engineering-governance.html, about.html
C6: Added "Client Outcomes" section to ai-engineering-governance.html (between Economics and Engagement Model) with 3 anonymized scenarios — Series B Fintech/SOX, Enterprise SaaS UK/EU AI Act, Healthtech US/HIPAA. Each card shows Day 30 and Day 90 outcome metrics. Clearly labeled as anonymized composites. M4: Expanded the FAO Specialists team card on about.html with 3 specialist archetype sub-cards (Engineering-Native, Compliance-Led, Security-First) — describes the type of person without fabricating identities. M3: Added enterprise procurement caveat to the FAQ "How fast can you start?" answer on ai-engineering-governance.html and a one-sentence qualifier to the "72 hours is not a marketing claim" belief in about.html.

## 2026-07-14 — C9 + M11: template contradiction resolved, fake "Live" labels removed
**Type:** content fix
**Files:** about.html, platform.html, index.html
C9 fix: "60+ Agent Templates" (about.html stats strip + Studio card) changed to "60+ Agent Specialities" — matches agent-builder.html which already used correct wording. platform.html "No templates. No adapters." reworded to avoid directly contradicting the specialities count while keeping the custom-build message intact. M11 fix: "FAO Risk Monitor — Live" → "FAO Risk Monitor — Example"; "FAO Governance Explorer — Active" → "FAO Governance Explorer — Interactive Demo"; pulsing green dot removed from rm-live-dot (animation:none, color changed from green to teal). A developer inspecting the DOM no longer sees a marketing mockup claiming to be a live system.

## 2026-07-14 — Sprint 4: credibility hardening (team, jurisdiction, AI-certified reframe)
**Type:** content + trust
**Files:** about.html, security.html, ai-engineering-governance.html, index.html, platform.html, pricing.html
Four credibility fixes: (1) about.html team section added — Gaurav Passi founder card + FAO Specialists profile card, closes audit finding M7; (2) security.html new "Contracting Entity & Jurisdiction" section with factual Q&A on GDPR/SCCs, HIPAA BAA, SOX scope, EU AI Act extraterritoriality for the Indian Pvt. Ltd. entity — closes audit finding M9; (3) "AI-certified" removed from all body copy and LD+JSON, replaced with "AI governance specialist" or "specialist in AI engineering governance" — closes C7; (4) "Compliance Autopilot" implausible claim (M5) softened to "Compliance Framework Mapping" with an honest description of what the FAO actually does.

## 2026-07-14 — /pricing page + sitewide footer link
**Type:** feature
**Files:** pricing.html (new), all 67 pages (footer bulk replace)
Audit finding C5 closed: no pricing information anywhere on site. New `/pricing` page: hero with `<$4,000/month` anchor, price-stack visual (vs $20K FTE vs $10K contractor), what's included (all 6 FAO deliverables per layer), Done-For-You vs. Done-With-You engagement model comparison, Forge/Studio add-on cards, 5 FAQ items, and a "Get a Quote" CTA linking to /assessment. Sitewide footer update: Pricing link added to Company column on all 67 pages (one PowerShell pass — all used `&amp;` entity variant).

## 2026-07-14 — Assessment page overhaul: governance focus + Calendly embed
**Type:** content + feature
**Files:** assessment.html
Sprint 3 conversion fix. Changes: title/meta → "Book an AI Governance Review"; left panel → governance-focused (risk mapping, compliance gap, Day-30 roadmap, honest fit); form reduced from 9 fields to 7 (4 required) — removed phone, industry, team size; added "AI tools in use" and "compliance framework" governance-specific dropdowns; textarea now optional; success screen now shows Calendly embed for immediate booking (URL: calendly.com/gaurav-upcore/governance-review — update if different); honeypot field added; FormSubmit.co disclosed in privacy note.

## 2026-07-14 — FAO "who is it?" profile strip on governance page
**Type:** content
**Files:** ai-engineering-governance.html
Audit finding C10: "FAO = person or system — never answered." Added 4-card profile strip inside the Engagement Model section: Who (a real person), Background (8+ yrs AI engineering + compliance), Time commitment (8-12 hrs/week), Selection (named before you sign, met in discovery call). Closes the biggest ambiguity buyers had about the core product.

## 2026-07-14 — Studio framing: no-code builder → managed deployment service
**Type:** content fix
**Files:** agent-builder.html
Audit finding C8: page titled "No-Code AI Agent Builder" implied a DIY SaaS product; reality is a services engagement. Fixes: title/OG/Twitter → "Managed AI Agent Deployment", LD+JSON type SoftwareApplication → Service, hero eyebrow "Agent Builder" → "Managed Deployment", "Instant Kill Switch" → "Instant Pause Control" (less alarming), ₹2,000 rupee example removed (international buyers).

## 2026-07-14 — Security & Trust page + ISO 27001 badge links
**Type:** feature
**Files:** security.html (new), all 67 HTML pages (footer + ISO 27001 badge), index.html (cert-item), agent-builder.html, ai-engineering-governance.html, platform.html, sdlc-agent.html
Created `/security` page addressing 6 key CISO questions: ISO 27001 status, code handling, LLM provider disclosure, BAA availability, SOC 2 audit, on-premise option. Linked ISO 27001 badges sitewide to `/security`. Added "Security & Trust" link to footer Resources column on all 67 pages. Page is honest about what's available on-request vs. included.

## 2026-07-14 — Full customer audit + Sprint 1-2 fixes
**Type:** fix
**Files:** all 67 HTML, industries/index.html, agent-builder.html, ai-engineering-governance.html
3-agent audit surfaced 10 critical and 20 major conversion blockers. Implemented: mobile nav hamburger drawer (all pages), industry hub cards now clickable with "View suite →" links (JS + href), hero CTA scrolls to grid not assessment form, "60+ Agent Templates" changed to "Agent Specialities" removing contradiction with platform.html "No templates", Upwork badge removed from all footers, "Fortune 50 AppSec Benchmarks" fabricated citation removed, L1 hero dashboard label changed from "Prompt Audit" → "Align" for consistency, "Top AI Company 2025" updated to 2026, hero hook quote gets Clutch link for verifiability.

## 2026-07-14 — Messaging & structure overhaul: FAO primary, agents secondary
**Type:** content + feature
**Files:** All 67 `.html` files (nav, footer, v=9 cache-bust), `ai-engineering-governance.html`, `platform.html`, `index.html`, `sdlc-agent.html`, `agent-builder.html`
8-change overhaul to make FAO hierarchy explicit site-wide:
1. Nav "Products" → "Services" (all 67 pages); Upcore Studio footer link fixed to `/agent-builder` (64 pages).
2. `<$4K/month` price-stack visual added above economics table (governance page) and in FAO section (homepage) — "Fractional. Not Expensive." with full-time/contractor strikethrough.
3. New "Cost of Not Governing" section on governance page (between incidents and The Gap): $4.7M breach + $1.2M compliance + $600K productivity = ~$6.5M annual exposure vs <$48K/yr FAO. 135× return framing.
4. Token optimisation mini-dashboard added inside L5 Optimise accordion panel on governance page — static dark widget showing AI spend by team (Frontend/Backend/Data/Mobile) with bar charts and delta indicators.
5. `platform.html` reframed: title "AI Services", hero "Governed First. Built to Last.", 4 Products stat removed, Tab 1 visually featured with "Start here" framing, contradictory "We're not a platform" line replaced.
6. "Governed Delivery" trust badge added below hero CTAs on both `sdlc-agent.html` and `agent-builder.html` — teal callout linking back to `/ai-engineering-governance`.
7. Tab labels in platform.html updated (SDLC Agent → Forge (SDLC Agent) for clarity).
8. `chat-widget.js` bumped v=8 → v=9 across all 67 pages.

---

## 2026-07-13 — Governance calendar: align with official Google Scheduling Button embed pattern
**Type:** fix
**Files:** `chat-widget.js`, all `.html` files (67, `?v=6`)
Rewrote governance calendar IIFE to mirror the official Google Calendar embed pattern (`window.addEventListener('load', …)` + dual-signal guard). The hidden-div + synchronous `.click()` approach is preserved (user activation context maintained; popup blockers don't fire). Both signals — `script.onload` and `window.load` — must arrive before `schedulingButton.load()` is called, ensuring the API is ready. Handles the edge case where `window.load` fires before our deferred script registers the listener. Cache-busted to v=6.

---

## 2026-07-07 — Privacy Policy and Terms & Conditions pages + footer links
**Type:** feature
**Files:** `privacy.html`, `terms.html`, all `.html` files (65 updated)
Added `/privacy` and `/terms` pages. Privacy Policy covers India DPDP Act 2023 (primary), GDPR (EU visitors), CCPA (California); documents all six third-party processors (Anthropic, Google Analytics/GTM/Fonts/Calendar, FormSubmit, Vercel), cookie table, retention schedule, B2B client data handling, and data subject rights. Terms covers website use, AI chat disclaimer (Kai), IP, limitation of liability, B2B services clause, and governing law (India, courts of Chandigarh). Both pages use sticky TOC sidebar (desktop), same nav/footer/design system. Both `noindex` to avoid thin-content SEO noise. Footer-copy updated with Privacy Policy and T&C links across all 65 existing pages.

---

## 2026-07-03 — Governance CTAs open calendar modal; other CTAs stay on /assessment
**Type:** feature
**Files:** `chat-widget.js`, all `.html` files
AI-governance CTAs ("Book a Governance Review", "Start Your 72-Hour Onboarding") now open an inline iframe modal with the Google Calendar booking page — no external redirect. All other CTAs ("Book a Discovery Call", "Free AI Assessment", etc.) continue to link to /assessment. Modal built lazily on first click, closes on ×, backdrop click, or Escape. Added ?v=2 cache-bust to chat-widget.js script tag across all 65 pages so the new modal code loads immediately.

---

## 2026-07-03 — No em dashes, calendar CTAs, bigger logo (site-wide)
**Type:** fix
**Files:** all `.html` files (67+)
Removed all em dashes site-wide (replaced with ` - ` inline or `- ` for attributions). Changed all `href="/assessment"` CTA links (319 instances) to point directly to the Google Calendar booking link. Enlarged nav logo from 48px to 60px height across all pages.

---

## 2026-07-03 — Homepage design improvements — proof stats, Bridge CTA, connectors, addon icons
**Type:** feature
**Files:** `index.html`
Added 3-column crisis proof stats block to Problem section (45% exploitable / $4.7M breach cost / 0 named owners). Added "Book a Governance Review →" CTA with reassurance copy to Bridge section. Added teal `→` step connectors to How It Works cards (desktop only, inside top-right of each non-last card). Added emoji icons to agent add-on cards. Converted Gauntlet section to light theme (`var(--bg2)`) and added AIGOV Gauntlet section between FAO and Bridge.

---

## 2026-07-03 — FAO section redesign — dark theme, outcome bullets, 2-col layout
**Type:** fix
**Files:** `index.html`
Replaced the white "cutout" FAO section with a full dark `#070B10` treatment. Moved eyebrow + H2 inside the layout grid column (eliminated standalone section-title above the grid). Removed the generic 2×2 stat card grid and replaced with 4 outcome-specific bullet rows (fao-wins). Updated left-column CTA to "Book a Governance Review →" (primary, /assessment) and "See the Framework →" (ghost). New description copy focuses on the concrete problem: AI-generated code shipping unreviewed. Section is visually cohesive with the FAO Explorer accordion and ribbon already in place.

---

## 2026-07-03 — UI/UX audit quick wins — CTA standardization + design system fixes
**Type:** fix
**Files:** `index.html`, `about.html`, `contact.html`, `ai-engineering-governance.html`, 61 subdirectory pages
Implemented all 8 quick wins from the PART 4 UI/UX audit: (1) nav CTA standardized to "Book a Governance Review" across all 65 pages; (2) index.html hero primary CTA now "Book a Governance Review →" → /assessment; secondary becomes "See the Framework →"; (3) auto-expands first framework layer (Align) on governance page load; (4) removed banned `.grad-text` CSS and fixed `font-weight:900→700` in about.html; (5) added "See X Suite →" links to all 3 industry addon cards; (6) de-risking copy already present under governance page CTAs; (7) added attribution to hero hook quote — CTO, Series B Fintech; (8) added "–73% risk exposure" outcome label to ribbon SVG chart at Day 90 endpoint.

---

## 2026-07-03 — FAO section proper redesign — two-column accordion layout (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the 3-dark-block "Governance Intelligence Dashboard" (score ring + 3-pane command widget) with the site's canonical two-column layout. Left: prose + 5 layer pills + 4 stat cards (`var(--bg2)` light style, matching site) + CTAs. Right: `.fao-explorer` dark accordion with 5 expandable rows (L1–L5), each revealing capability bullets + timestamped log entry + compliance tags; L3 pre-opens on load; L2 amber REVIEW state; L3 red SCANNING/alert state. Pills on hover highlight matching accordion row via teal outline. Ribbon below unchanged (4 stats + SVG risk-decline chart). Removed all score-ring, layer-bar, and packet-animation JS; replaced with `toggleLayer()` accordion function + DOMContentLoaded pre-open + new pill hover. Zero console errors.

---

## 2026-07-03 — FAO "Governance Intelligence Dashboard" full redesign (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the entire FAO section with a 3-layer visual dashboard. (1) Intro row: text/pills/CTAs left + dark governance score ring card right (CSS `@property` conic-gradient, animates to 94/100 on scroll, with 3 mini progress bars). (2) Full-width 3-pane dark command widget: layer coverage bars with IntersectionObserver fill animation; SVG architecture diagram with 5 nodes (L3 pulsing red via SMIL `<animate>`, 3 animated packets via `@keyframes`, scan sweep line); auto-scrolling live activity feed (CSS `feed-scroll` animation, 12 entries × 2 duplicated sets for seamless loop). (3) Dark ribbon: 4 stats (72h / Day 30 / 19 / 5, two count-up on scroll) + SVG risk-decline curve (stroke-dashoffset draw on scroll). Subtle teal dot-grid `::before` on section background. Zero console errors; all brand tokens preserved.

---

## 2026-07-03 — FAO section visual framework redesign (homepage)
**Type:** feature
**Files:** `index.html`
Replaced the plain 3-stat card in the FAO section right column with a dark "FAO Governance Pipeline" widget — 5 connected layer nodes (L1–L5) with status badges, L3 Protect in active SCANNING state. Replaced 4 text bullets on the left with a 2×2 teal stat grid (5 / 72h / Day 30 / 19). Added vanilla JS: hovering a layer pill highlights the matching pipeline node. No new hex values; reuses `#0a0a0a` and `blink` keyframe from existing tokens.

---

## 2026-07-02 — CTA button standardization: all primary buttons now black pill site-wide
**Type:** fix
**Files:** 14 `learn/*.html`, `compare/*.html`, `solutions/*.html` pages (btn-p size); 12 `industries/*.html` (btn-ghost border-radius)
Primary CTA buttons were inconsistent across 5 class families (btn-fill, btn-p, btn-cta, btn-teal, btn-primary) with 3 distinct visual treatments: black pill on main pages, teal squircle on industry/insights, undersized pill on learn/compare/solutions. Industry+insights pages were already fixed in a prior pass. This pass normalizes: (1) `.btn-p` in 14 learn/compare/solutions pages from `padding:11px 24px; font-size:14px` → `padding:12px 26px; font-size:15px`. (2) `.btn-ghost` on all 12 standard industry pages from `border-radius:8px; padding:13px 28px` → `border-radius:9999px; padding:12px 26px` so secondary pills match the primary. Canonical standard: `background:#0a0a0a · color:#fff · padding:12px 26px · border-radius:9999px · font-size:15px · font-weight:600`. Script: `fix_cta_buttons.py`.

---

## 2026-07-02 — Full-site consistency audit: governance cross-links, content fixes, CTA standardization
**Type:** fix | content
**Files:** `about.html`, `platform.html`, `sdlc-agent.html`, `assessment.html`, `contact.html`, `kw/manufacturing-ai-agents.html`, `kw/index.html`, `platform/ai-agent-builder.html`, `platform/custom-ai-agents.html`, `platform/30-day-deployment.html`, `platform/on-premise-deployment.html`, `insights/banking-ai-customer-service.html`, `learn/enterprise-ai-strategy.html`, `learn/ai-data-governance.html`, all 12 `industries/*.html` pages
Multi-pass site-wide consistency audit. Key changes: (1) **about.html** — governance-first hero H1, added FAO as 4th product card in 2×2 grid, stats updated ("48hrs"→"72h", "3 Core Products"→"4 Products"), hero CTA "Work With Us"→"Book a Discovery Call", meta/schema updated. (2) **platform.html** — hero H1 updated to governance framing, Studio tab now has booking CTA. (3) **Governance cross-links** — teal callout box added before CTA on all 12 industry pages and 3 platform sub-pages; Decision 5 in enterprise-ai-strategy.html and ai-data-governance.html both now link to /ai-engineering-governance. (4) **CTA fixes** — manufacturing KW page CTAs changed /contact→/assessment; assessment.html button "Schedule My Assessment"→"Book My Discovery Call"; success message "You're on the list!"→"Request received."; placeholder names Rahul/Sharma→Alex/Smith; Studio Templates CTA label fixed. (5) **SEO** — banking article canonical URL changed from upcore.tech/insights/banking/ to upcoretech.com/insights/; ai-agent-builder meta description completed. (6) **Content fixes** — "48 hours"→"72 hours" throughout about.html; sdlc-agent "0 Developers Needed"→"0 Dev Handover Cycles"; sdlc schema offers.url /contact→/assessment; artefacts→artifacts in on-premise and ai-data-governance; contact response time inconsistency fixed; kw/index.html planning stats removed. (7) **Copyright** — 41 files updated 2025→2026.

---

## 2026-07-01 — Full design overhaul: MiniMax white-canvas system (65 pages)
**Type:** feature | fix
**Files:** all 65 HTML pages, `apply_minimax.py` (new), `fix_flagships.py` (new), `docs/DESIGN-SYSTEM.md`
Flipped the entire site from dark charcoal to a MiniMax-adapted white-canvas system. Key changes: (1) **Colors**: `--bg:#ffffff`, `--txt:#0a0a0a`, `--border:#e5e7eb` — fully light. (2) **Font**: Poppins → DM Sans (weights 300/400/500/600/700). (3) **Nav**: dark-glass `rgba(7,11,16,0.97)` → white `#ffffff`; CTA teal/8px → black `#0a0a0a`/9999px pill. (4) **Buttons**: `.btn-fill` teal → black, `.btn-ghost` white-alpha → ink outline, all `8px` → `9999px` pill. (5) **Cards**: `10px` → `16px`, `rgba(0,0,0,.06)` shadow hover, teal left-borders removed. (6) **Badges/pills**: `6px` → `9999px` site-wide. (7) **Footer**: kept dark `#0a0a0a`; text forced to `rgba(255,255,255,…)` since `--txt` is now dark. (8) **Hero strong**: `color:#fff` → `color:var(--txt)` on 3 flagship pages (was invisible on white bg). `apply_minimax.py` handles 60 template pages idempotently; `fix_flagships.py` patches the 5 uniquely-formatted flagship pages. Both scripts re-runnable safely.

---

## 2026-07-01 — Design system enforcement: upcore-design.md + apply_design_system.py
**Type:** fix | infra
**Files:** `upcore-design.md` (new), `apply_design_system.py` (new), 45+ HTML pages, `industries/index.html`, `kw/index.html`, `platform/custom-ai-agents.html`, `platform/on-premise-deployment.html`, `kw/real-estate-ai-workforce.html`, `docs/DESIGN-SYSTEM.md`
Defined a comprehensive 15-section design system in `upcore-design.md` (single source of truth) and enforced it site-wide. `apply_design_system.py` patched 42 content pages (kw/, learn/, industries/, compare/, solutions/) in one pass. Key changes: badge border-radius 20px/100px → 6px; button gradient fills → solid `var(--teal)`; button border-radius 100px → 8px; card border-radius 16-20px → 10px; card hover teal glow → `border-color:var(--bh)`; gradient `::before` top-bars removed → left-border accent; stat number gradient text → `color:var(--teal)`; hero radial-gradient + grid overlay removed; teal box-shadows removed. Manual patches: `industries/index.html` (unique `.eyebrow`/`.hub-card`/`.btn-primary` template), `kw/index.html` (unique `.hub-badge`/`.hub-stat-num`/`.res-card` template), `platform/custom-ai-agents.html` (`.step-num`), `platform/on-premise-deployment.html` (`.arch-card::before`), `kw/real-estate-ai-workforce.html` (`.case-metric-num`). Final state: 0 gradient fills on buttons, 0 pill badges, 0 teal glow shadows on any content page.

---

## 2026-07-01 — Full site visual redesign: Palantir/Anduril aesthetic (charcoal-neutral system)
**Type:** feature | fix
**Files:** all 65 HTML pages, `docs/DESIGN-SYSTEM.md`, `propagate_design.py`, `fix_all.py`
Overhauled the entire site from "AI slop" navy/teal-glow to a Palantir/Anduril-inspired charcoal-neutral dark mode. Changes propagated to all 65 HTML files via Python scripts with zero manual per-page edits. Key changes: (1) **Color system**: backgrounds shifted from blue-navy (`#07101e`) to charcoal-neutral (`#070B10`); borders switched from teal-alpha to white-alpha (`rgba(255,255,255,0.07)`); amber governance accent added (`--amber`/`--amber2`); text lightened to warm `#E2E8F0`. (2) **Typography**: gradient text (`.grad-text`) banned on all H1/H2 — replaced with `font-weight:300` H1 + `<strong>` for emphasis; 14 `grad-text` instances removed across secondary pages. (3) **Nav**: 7 links → 5 links (`AI Governance`, `Products`, `Industries`, `Resources`, `About`); `backdrop-filter:blur` removed; height 72px → 64px; CTA changed from gradient to solid teal. (4) **Buttons**: 6+ old classes collapsed to 3 — `.btn.btn-fill`, `.btn.btn-ghost`, `.btn.btn-amber`. (5) **Cards**: border-radius 20px → 10px; teal glow shadows removed; gradient top-bars removed; left-border accent adopted for semantic cards. (6) **Insights articles**: all 15 article files had no `:root` block — injected canonical tokens + `ARTICLE_BASE_CSS`. (7) **Footer**: tagline updated to "Govern Your AI. Then Build With It." across all pages. Final audit: ALL CLEAR — 0 issues across 65 files.

---

## 2026-07-01 — Pivot: AI Engineering Governance (Fractional AI Officer) as new flagship
**Type:** feature | content | decision
**Files:** `ai-engineering-governance.html` (new), `index.html`, `platform.html`, `api/chat.js`, `chat-widget.js`, `sitemap.xml`, `vercel.json`, all ~65 non-demo pages (nav), `sdlc-agent.html`, `industries/compliance-governance.html`, `learn/ai-data-governance.html`
Positioned **AI Engineering Governance** — delivered via a **Fractional AI Officer (FAO)** — as Upcore's new flagship offering, added *alongside* the kept agent-building business (softer pivot, all existing SEO pages retained). Source of truth = the FAO decks (V8b latest). What shipped: (1) New flagship page `/ai-engineering-governance` (built from `sdlc-agent.html` shell) — crisis stats, documented incidents (Moltbook, CVE-2025-48757, Amazon), the-gap two-column, the FAO solution, 5-layer/19-capability framework, hire-vs-Big4-vs-FAO economics, 90-day journey, FAQ; Service + FAQPage JSON-LD. (2) Homepage: FAO added as first product card in `#products` + crisis stat panel, hero "New" announcement link, title/meta/OG rewritten, Organization `knowsAbout` expanded. (3) Nav: added top-level **AI Governance** link (before Industries) — propagated to all ~65 non-demo pages via script, in sync per DESIGN-SYSTEM rule. (4) `platform.html`: added AI Governance as first product tab ("Four Products"), retitled. (5) Kai (`api/chat.js` SYSTEM_PROMPT): AIGOV/FAO added as lead offering with CTO/CISO/CFO framing; `chat-widget.js` suggested prompt added. (6) SEO: sitemap entry (0.9); redirects `/fractional-ai-officer`, `/aigov`, `/ai-governance` → `/ai-engineering-governance`. (7) Funnel-in cross-links from Forge + compliance-governance + ai-data-governance. Note: "AIGOV" is internal shorthand; market-facing names are "AI Engineering Governance" + "Fractional AI Officer". Stats carry deck sources (Gartner/Veracode/IBM/GitClear 2025, CVE-2025-48757). All pricing kept unpublished per convention.

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
