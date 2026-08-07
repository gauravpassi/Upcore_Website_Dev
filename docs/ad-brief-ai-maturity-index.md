# Ad Campaign & Design Brief — The Upcore AI Maturity Index

**Live page:** https://www.upcoretech.com/lp/ai-maturity-index
**Purpose of this doc:** everything needed to design ads, social creative, and graphics for this landing page — copy, brand assets, colors, fonts, audience, and funnel — in one place.

---

## 1. What this page is

A free, 2-minute, 10-question interactive diagnostic quiz. Visitor answers questions, hits an email gate, gets an instant on-screen score + a branded PDF report, and is offered a 45-minute call. It is an **ad-only landing page** — no site nav distractions in the traffic-facing sense (though the real nav/footer are present for credibility), single goal: start the quiz.

**Target audience:** COO, CEO, CFO, or CHRO at an operationally-complex, growth-stage company running multiple uncoordinated AI pilots across departments. Buyer persona is worried about scattered AI spend with no accountable owner and no way to answer "what did the AI budget actually buy this year" when the board asks.

**What the quiz measures:** AI portfolio coordination maturity across **10 dimensions** — Vision, Ownership, Inventory, Coordination, ROI, Budget, Visibility, Tooling, Adoption, Oversight.

**Funnel:** Ad → this page → quiz (10 Q) → email gate → instant score + PDF download → optional 45-min call booked via Calendly (`ai-strategy-review` event) → dedicated booking page at `/lp/maturity-review` ("AI Portfolio Value Review").

**Relationship to the sibling page:** This is the COO/CFO-facing counterpart to `/lp/governance-index` (the CTO/CISO-facing engineering governance quiz). Same mechanics, different buyer and different measured dimensions — keep visual language consistent with that page's design system, but this one skews slightly more "executive scorecard" than "engineering console."

---

## 2. Brand assets

- **Logo file:** `/upcore-logo.png` — served at `https://www.upcoretech.com/upcore-logo.png` (used at 360×240 native, rendered ~60px tall in nav, ~44px in footer)
- **Favicon set:** `/favicon.ico`, `/favicon-32.png`, `/favicon-192.png`, `/favicon-512.png`, `/apple-touch-icon.png`
- **Company name:** Upcore Technologies (Pvt. Ltd.)
- **Tagline (footer, sitewide):** "Govern Your AI. Then Build With It."
- **Certifications to reference:** ISO 27001 Certified, ISO 9001, CMMI Level 3 Appraised, Nasscom Member
- **Review platforms (real, current ratings):** Clutch — 5.0 rating · DesignRush — 5.0, 16 reviews · Google — 5.0 rating
- **Domain:** upcoretech.com

---

## 3. Design system — colors, type, visual language

### Color palette (hex)
| Token | Hex | Use |
|---|---|---|
| Teal (brand primary) | `#0ABFCC` | CTA buttons, accents, chart fills, links (on dark bg) |
| Teal hover | `#089AAA` | Button hover state |
| Teal text (AA-compliant) | `#077F8C` | Teal-colored text on white (darker for contrast) |
| Ink / near-black | `#0a0a0a` | Headlines, primary text, nav/footer background |
| Body text | `#45515e` | Paragraph text |
| Muted text (AA-compliant) | `#6E7680` | Captions, labels, secondary text |
| Border gray | `#e5e7eb` | Card borders, dividers |
| Card background | `#f7f8fa` | Light gray card fill |
| White | `#ffffff` | Page background, card fill |
| Button ink (on teal) | `#070B10` | Text color on teal buttons |

### Typography
- **Font family:** DM Sans (Google Fonts) — weights 400/500/600/700/800 (this page does **not** use the monospace accent the governance page uses — pure DM Sans throughout, slightly more "executive/clean" than "console/technical")
- **H1:** `clamp(34px, 5.5vw, 52px)`, weight 700, tight letter-spacing (-0.021em), line-height 1.1
- **H2:** `clamp(24px, 3.5vw, 34px)`, weight 700
- **Subhead:** 18px, weight 400, color `#45515e`, max-width 560px
- **Body:** 15.5px

### Visual motifs
- **Background texture (whole page):** a very subtle 72×72px teal grid pattern + a soft radial teal glow at the top center, rgba(10,191,204, .025–.06) — barely-there, adds texture without competing with content. Same treatment as the governance page for brand consistency.
- **Buttons:** fully rounded pill shape (`border-radius: 9999px`), solid teal fill for primary, black outline for secondary/ghost
- **Cards:** 12px border-radius, 1px light-gray border, white or `#f7f8fa` fill, flat/clean, no heavy shadows
- **The "10 Dimensions" radar chart:** a 10-sided radar/spider chart with teal fill + stroke + spokes, axis labels around the perimeter (Vision, Ownership, Inventory, Coordination, ROI, Budget, Visibility, Tooling, Adoption, Oversight). This is the **same radar chart style used in the PDF report** and the quiz's own result screen — reuse this visual for ad graphics, it's the recognizable asset for this campaign.
- **Score/report card visual:** a card showing a big teal score number (e.g. "46/100"), a tier pill badge (e.g. "Emerging"), and horizontal progress bars per dimension — strong visual for ads (shows the deliverable).

---

## 4. Full page copy (verbatim, current live version)

### Eyebrow (small badge above headline)
> Free 2-Minute Diagnostic · AI Portfolio Coordination

### Headline (H1)
> **You're Paying for a Dozen AI Tools. Is Any of It Actually Working — or Just Expensive Theater?**

### Subheadline
> Ten questions, two minutes. Score your company's AI coordination across 10 dimensions and see exactly which pilots deserve next quarter's budget — and which ones to quietly kill.

### Primary CTA button
> Get My Maturity Index Score

### Secondary CTA (link)
> Or skip straight to booking a call

### Guarantee/reassurance line (under CTAs)
> Free · 10 questions · about 2 minutes · instant PDF. No credit card, no call required.

### Proof bar (3 stat lines, shown as a horizontal row on desktop)
1. 95% of enterprise generative AI pilots fail to deliver measurable ROI — MIT NANDA, 2025
2. Starting from $1,999/month vs. $400K–$750K+ for a full-time Chief AI Officer hire
3. 50+ enterprise teams scored

### Certification badges (shown under proof bar)
ISO 27001 Certified · ISO 9001 · CMMI Level 3 Appraised

### "The 10 Dimensions You'll Be Scored On" — radar chart labels
Vision · Ownership · Inventory · Coordination · ROI · Budget · Visibility · Tooling · Adoption · Oversight

### Sample report card (illustrative numbers shown pre-quiz)
- Score: **46/100** — Tier: **Emerging**
- Vision 40% · Ownership 30% · Coordination 45% · ROI 25% · Adoption 65%
- Caption: "Illustrative scoring pattern — your real report is generated from your answers."

### "Why Now" section
**Headline:** 95% of enterprise generative AI pilots fail to deliver measurable ROI.
**Body:** That's MIT's NANDA initiative research, 2025 — widely reported since. It's not a reason to stop experimenting. It's the reason scattered pilots rarely turn into the few that matter without someone coordinating them across departments.
**Healthcare-specific extra line (shown only to healthcare-tagged traffic via UTM):** CMS-0057-F's prior-authorization compliance deadline lands January 1, 2027 — a dated trigger, not a someday one.

### "Is this you?" (pain-point quotes)
1. "We have AI pilots running in half a dozen departments, and I couldn't tell you which two are actually worth scaling."
2. "Every department picked its own AI tool. Nobody's comparing notes, and nobody owns the ROI number."
3. "The board asked what we're getting for our AI spend this year. I didn't have a real answer."

**Closing line:** If any of this sounds familiar, the Index tells you exactly where your coordination gaps are — not a sales pitch.

### Testimonials ("What clients say" — 3 cards, anonymized, real & sourced)
1. *"They spent a large amount of time understanding every aspect of our vision — critical in shaping the project's direction."* — Managing Director, Retail — App Development engagement (via DesignRush)
2. *"Upcore was adaptable, offering regular updates and fielding inquiries quickly — a genuinely collaborative process."* — Founder & CEO, Retail — App Development engagement (via DesignRush)
3. *"Upcore Technologies delivered a solution using machine learning and NLP that showed significant, measurable improvement."* — Managing Director, Healthcare — Generative AI engagement (via DesignRush)

**Video testimonial:** "Watch a client testimonial" → links to Vimeo (960114218)
**Trust badges:** Clutch — 5.0 rating · DesignRush — 5.0, 16 reviews · Google — 5.0 rating

### "How it works" (4 steps)
1. Work through the same 10 dimensions we score in a paid diagnostic engagement.
2. Enter your work email to unlock your Maturity Index Score and tier — immediately, on-screen.
3. Download your PDF report instantly — your scores, your weakest dimension, and where to start first.
4. Optional 45-minute call to walk through your 90-Day Plan, if you want one.

### Footer CTA headline
> Two minutes. Ten questions. Your score.

### FAQ (5 questions)
1. **Is this actually free?** — Yes — the Index, your on-screen score, and the PDF report are free, no credit card, no obligation. The only ask afterward is whether you want a 45-minute call, and there's no pressure either way.
2. **We already have a CIO / IT leader.** — This isn't about IT infrastructure — it's about coordinating AI initiatives across departments (ops, finance, HR, customer-facing teams) that a CIO typically isn't chartered to own end-to-end. Most companies that take this Index still don't have anyone accountable for AI ROI across the whole business, CIO or not.
3. **We're not ready for a Chief AI Officer.** — Good — this isn't a pitch to hire one. It's a 90-day engagement under a fractional model, starting from $1,999/month against a $400K–$750K+ full-time hire. If your Index score comes back Orchestrated, we'll say so directly rather than oversell.
4. **We're still experimenting — it's early days.** — That's exactly the stage this is built for. MIT's NANDA research found 95% of enterprise AI pilots fail to show measurable ROI — mostly not from bad tools, but from nobody coordinating across departments early enough. The Index tells you which of your current experiments are worth doubling down on before more budget sinks into the wrong ones.
5. **Can 10 questions really tell you anything about a company our size?** — Not everything — and we're not claiming to. The Index is a fast signal across the same 10 dimensions a full Diagnostic engagement runs on, built to show you your biggest coordination gap, not replace an actual portfolio review. Think of it as the first data point, not the final word.

### Post-quiz teaser screen (after all 10 answered, before email)
> "Your board will ask what the AI spend bought this year. This is the shape of that answer."

### Full result screen CTAs (after email gate)
- Primary: "Get my 90-Day Plan walkthrough"
- Lighter-touch (for already-strong scorers): "Get a second opinion on my lowest dimensions"

### PDF report closing pitch (page 2 of the downloadable PDF)
> In 45 minutes, we walk this report dimension by dimension, identify which of your current pilots are worth funding and which to stop, and draft the first version of your 90-Day Plan. No pitch, no pressure. If you engage, it starts from $1,999/month against $400K–$750K+ for a full-time Chief AI Officer hire — and if the Day-30 findings don't justify continuing, you walk away.

---

## 5. The 10 quiz questions (for reference / context on what "coordination" means here)

| # | Dimension | Question |
|---|---|---|
| 1 | Vision | How would you describe your company's AI strategy today? |
| 2 | Ownership | Who owns AI adoption across your company today? |
| 3 | Inventory | Do you have a single, current inventory of every AI pilot running across departments? |
| 4 | Coordination | When two departments both start using AI for similar tasks, does anyone coordinate? |
| 5 | ROI | Can you currently quantify ROI from your AI initiatives? |
| 6 | Budget | Is there a dedicated budget for AI transformation, separate from individual department experiments? |
| 7 | Visibility | How does AI adoption get reported upward — to your board, investors, or exec team? |
| 8 | Tooling | Do you have visibility into which AI tools each department is using? |
| 9 | Adoption | When your company rolls out an AI tool, what typically happens? |
| 10 | Oversight | If asked today, could you say who's responsible for AI risk and compliance across departments? |

**Mid-quiz insight interrupt (shown after Q5):** "MIT's NANDA initiative research (2025) found 95% of enterprise generative AI pilots fail to deliver measurable ROI. If you answered anything but 'full quantified ROI,' you're in that majority — and so is almost everyone else who takes this Index."

**Tier outcomes:** Fragmented (0–25) · Emerging (26–50) · Aligning (51–75) · Orchestrated (76–100)

---

## 6. Key facts & stats safe to use in ads (all verified, sourced)

- **95%** of enterprise generative AI pilots fail to deliver measurable ROI — *MIT NANDA Initiative, 2025*
- Starting from **$1,999/month** for the Fractional AI Officer (FAO) engagement — vs. **$400K–$750K+** fully-loaded cost of a full-time Chief AI Officer hire
- **90-day** engagement structure with a Day-30 walk-away checkpoint (no lock-in)
- **5.0 rating** on Clutch, DesignRush (16 reviews), and Google
- ISO 27001, ISO 9001 certified · CMMI Level 3 Appraised
- Healthcare-specific (only for healthcare-tagged ad traffic): CMS-0057-F prior-authorization compliance deadline — **January 1, 2027**

**Do not use:** any number not listed above. No fabricated client names, logos, or testimonials — only the anonymized/sourced ones listed in §4.

---

## 7. CTA / funnel destinations (for tracking/UTMs)

- Quiz start → in-page (no URL change)
- "Skip to booking a call" / nav CTA → `/lp/maturity-review` (dedicated "AI Portfolio Value Review" booking page — NOT the same booking page as the governance quiz)
- Calendly event used downstream: `calendly.com/saswata-upcoretechnologies/ai-strategy-review` (45 min) — this page has its **own** Calendly event, distinct from governance's `ai-governance-review`
- **robots.txt note:** `/lp/` is disallowed under the generic `User-agent: *` block (deliberate — keeps these pages out of search). Google's AdsBot ignores that wildcard block and crawls `/lp/` fine, so ads still get approved — but Google also can't read the page to auto-generate assets for you. Supply all headlines/descriptions/images manually in Google Ads and turn off automatically-created assets / final URL expansion for these campaigns.
- Google Ads conversion action: "AI Maturity Index — Assessment Complete"
- Healthcare-segment traffic detection: UTM params containing `healthtech` or `healthcare` trigger an extra compliance-deadline line in the "Why Now" section

---

## 8. Tone & voice notes for copywriters/designers

- Direct, second-person, no fluff. Short sentences. Confident but not hypey.
- Buyer language should sound like COO/CFO/CEO concerns: budget, board accountability, ROI, ownership — NOT engineering/security jargon (that's the governance page's territory).
- Never say "AI-certified" or use unverifiable superlatives.
- Every stat must be sourced — this brand has been through multiple fact-check passes specifically to avoid fabricated claims; don't reintroduce any.
- Visual identity should feel like an **executive scorecard/portfolio dashboard** — closer to a boardroom reporting tool aesthetic than a dev-console aesthetic (that distinction is deliberate vs. the governance page).
