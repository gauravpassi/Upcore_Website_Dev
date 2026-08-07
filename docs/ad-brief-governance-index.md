# Ad Campaign & Design Brief — The Upcore Governance Index

**Live page:** https://www.upcoretech.com/lp/governance-index
**Purpose of this doc:** everything needed to design ads, social creative, and graphics for this landing page — copy, brand assets, colors, fonts, audience, and funnel — in one place.

---

## 1. What this page is

A free, 2-minute, 10-question interactive diagnostic quiz. Visitor answers questions, hits an email gate, gets an instant on-screen score + a branded PDF report, and is offered a 45-minute call. It is an **ad-only landing page** — no site nav distractions in the traffic-facing sense (though the real nav/footer are present for credibility), single goal: start the quiz.

**Target audience:** CTO, VP Engineering, CISO, or technical Founder at a growth-stage B2B SaaS/tech company. Buyer persona is worried about AI-generated code shipping without review — security risk, compliance/audit exposure, investor diligence.

**What the quiz measures:** AI code governance maturity across 5 layers — **Align, Accelerate, Protect, Comply, Optimise** (the "L1–L5" framework, same one used in the main flagship page `/ai-engineering-governance`).

**Funnel:** Ad → this page → quiz (10 Q) → email gate → instant score + PDF download → optional 45-min call booked via Calendly (`ai-governance-review` event).

---

## 2. Brand assets

- **Logo file:** `/upcore-logo.png` — served at `https://www.upcoretech.com/upcore-logo.png` (used at 360×240 native, rendered ~60px tall in nav, ~44px in footer)
- **Favicon set:** `/favicon.ico`, `/favicon-32.png`, `/favicon-192.png`, `/favicon-512.png`, `/apple-touch-icon.png`
- **Wordmark style (used elsewhere on site, not on this specific page anymore):** "UPCORE" in bold uppercase letter-spaced small caps + "upcoretech.com" in muted gray next to it
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
- **Font family:** DM Sans (Google Fonts) — weights 400/500/600/700/800
- **Monospace accent (governance page only):** JetBrains Mono — used for progress counters, badge numbers, layer labels (gives this page a slightly more "technical/console" feel than the maturity page)
- **H1:** `clamp(34px, 5.5vw, 52px)`, weight 700, tight letter-spacing (-0.021em), line-height 1.1
- **H2:** `clamp(24px, 3.5vw, 34px)`, weight 700
- **Subhead:** 18px, weight 400, color `#45515e`, max-width 560px
- **Body:** 15.5px

### Visual motifs
- **Background texture (whole page):** a very subtle 72×72px teal grid pattern + a soft radial teal glow at the top center, rgba(10,191,204, .025–.06) — barely-there, adds texture without competing with content. Reusable for ad backgrounds if you want brand consistency.
- **Buttons:** fully rounded pill shape (`border-radius: 9999px`), solid teal fill for primary, black outline for secondary/ghost
- **Cards:** 12px border-radius, 1px light-gray border, white or `#f7f8fa` fill, no heavy shadows (flat, clean, SaaS-modern aesthetic)
- **The "5 Layers" pentagon diagram:** a 5-sided radar/pentagon shape with teal fill + stroke, each vertex has a numbered badge (L1–L5) with a label below (Align, Accelerate, Protect, Comply, Optimise). This is a **recognizable visual asset unique to governance** — strongly recommend reusing this pentagon motif in ad graphics for this campaign.
- **Score/report card visual:** a card showing a big teal score number (e.g. "48/100"), a tier pill badge (e.g. "Reactive"), and 5 horizontal progress bars — this "sample report" look is a strong visual for ads (shows the deliverable).

---

## 4. Full page copy (verbatim, current live version)

### Eyebrow (small badge above headline)
> Free 2-Minute Diagnostic · AI Code Governance

### Headline (H1)
> **45% of AI-Generated Code Ships With a Security Hole. Is Yours One of Them?**

### Subheadline
> Ten questions, two minutes. Score your AI code governance across the same five layers a Fractional AI Officer runs, and see your gaps before an auditor, a customer, or a diligence team finds them.

### Primary CTA button
> Get My Governance Index Score

### Secondary CTA (link)
> Or skip straight to booking a call

### Guarantee/reassurance line (under CTAs)
> Free · 10 questions · about 2 minutes · instant PDF. No credit card, no call required.

### Proof bar (3 stat lines, shown as a horizontal row on desktop)
1. 45% of AI-generated code contains an exploitable vulnerability — Veracode, 2025
2. $4.4M global average cost of a data breach — $10.2M in the US (IBM, 2025)
3. 50+ engineering teams scored · FAO engagements from $1,999/month

### Certification badges (shown under proof bar)
ISO 27001 Certified · ISO 9001 · CMMI Level 3 Appraised

### "The 5 Layers You'll Be Scored On" — pentagon diagram labels
L1 Align · L2 Accelerate · L3 Protect · L4 Comply · L5 Optimise

### Sample report card (illustrative numbers shown pre-quiz)
- Score: **48/100** — Tier: **Reactive**
- Align 40% · Accelerate 55% · Protect 30% · Comply 50% · Optimise 65%
- Caption: "Illustrative scoring pattern — your real report is generated from your answers."

### "Why Now" section
**Headline:** 45% of AI-generated code ships with an exploitable vulnerability.
**Body:** That's Veracode's 2025 research across real coding tasks, and CVE-2025-48757 shows what it looks like when one reaches production. IBM puts the global average data breach at $4.4M in its 2025 report — $10.2M in the US. None of this waits for a regulatory deadline: your customers' vendor-security reviews are already asking how AI-written code gets reviewed.

### "Is this you?" (pain-point quotes)
1. "AI-generated code is 30%+ of what ships, and nobody's reviewing it differently than human code."
2. "We raised our Series B and the first diligence question was: how do you govern AI-written code? We didn't have an answer."
3. "Our security team found out about a new AI coding tool from a Slack message, not a review."

**Closing line:** If any of this sounds familiar, the Index shows you which of the five layers is actually exposed — not a sales pitch.

### Testimonials ("What clients say" — 3 cards, anonymized, real & sourced)
1. *"Their ability to simplify difficult AI concepts for both our business and technical teams was particularly impressive."* — Co-Founder, Real Estate — AI Consulting engagement (via DesignRush)
2. *"They stuck to the timetable, completing each milestone on time, with clear, measurable results throughout."* — Client review, Real Estate — AI Consulting engagement (via DesignRush)
3. *"Upcore Technologies delivered a solution using machine learning and NLP that showed significant, measurable improvement."* — Managing Director, Healthcare — Generative AI engagement (via DesignRush)

**Video testimonial:** "Watch a client testimonial" → links to Vimeo (960114218)
**Trust badges:** Clutch — 5.0 rating · DesignRush — 5.0, 16 reviews · Google — 5.0 rating

### "How it works" (4 steps)
1. Answer 10 questions across the 5 layers a Fractional AI Officer governs: Align, Accelerate, Protect, Comply, Optimise.
2. Enter your work email to unlock your Index Score and tier — immediately, on-screen.
3. Download your PDF report instantly — your scores, your weakest layer, and where to start first.
4. Optional 45-minute call to build your Day-30 roadmap, if you want one.

### Footer CTA headline
> Two minutes. Ten questions. Your score.

### FAQ (5 questions)
1. **Is this actually free?** — Yes — the Index, your on-screen score, and the PDF report are free, no credit card, no obligation. The only ask afterward is whether you want a 45-minute call, and there's no pressure either way.
2. **Can't we just build this ourselves?** — Some teams do — usually by hiring a dedicated AI governance lead ($180K–$250K+ fully loaded) or spending 3–6 engineering months building policy, scanning, and audit tooling in-house. The FAO gets the same outcome in 72 hours at a fraction of that cost, month-to-month, with a 30-day exit clause.
3. **We're not regulated / this isn't material yet.** — If your Index comes back Structured or Governed, we'll tell you that directly — the report doesn't oversell risk that isn't there. But if you're selling to enterprise customers, their vendor-security reviews don't wait for a regulatory deadline, and the EU AI Act's high-risk obligations (now due December 2, 2027 after this year's delay) are still real, just less imminent than a lot of teams assume.
4. **Won't this slow our engineering team down?** — The FAO runs alongside your existing PR workflow, not a separate approval queue. It works as guardrails, not a second review board — and your Index result shows exactly where the current gaps are before anything changes.
5. **Can 10 questions really assess something this complex?** — No — and we don't pretend they can. The Index is a fast diagnostic signal across the same 5 layers a full engagement governs against, built to show you where to look first. The full picture — actual code, actual policy, actual audit trails — is what the 45-minute call and a real engagement are for.

### Post-quiz teaser screen (after all 10 answered, before email)
> "Your customers' vendor-security reviews already ask how AI-written code gets reviewed. This is that answer, scored."

### Full result screen CTAs (after email gate)
- Primary: "Walk me through my Day-30 roadmap"
- Lighter-touch (for already-strong scorers): "Get a second opinion on my lowest layers"

### PDF report closing pitch (page 2 of the downloadable PDF)
> In 45 minutes, a Fractional AI Officer candidate walks this report layer by layer, maps your actual AI risk surface, and hands you a concrete Day-30 roadmap. No pitch, no pressure. If you engage, the FAO embeds in 72 hours from $1,999/month, and if the Day-30 report doesn't justify continuing, you walk away.

---

## 5. The 10 quiz questions (for reference / context on what "governance" means here)

| # | Layer | Question |
|---|---|---|
| 1 | Align | Do you have a written AI usage policy, and is it enforced? |
| 2 | Align | Who owns AI policy decisions at your company today? |
| 3 | Accelerate | How does AI-generated code get identified in your PR process? |
| 4 | Accelerate | Do you know which AI tools each engineer is using right now? |
| 5 | Protect | How do you scan for vulnerabilities in AI-generated code? |
| 6 | Protect | If an AI coding tool introduced a vulnerability last quarter, would you know? |
| 7 | Comply | Could you produce a full audit trail of AI-assisted code changes today? |
| 8 | Comply | Which of these does your company have to answer to today? (EU AI Act, GDPR, HIPAA, SOC 2, SOX, ISO 42001) |
| 9 | Optimise | Do you track AI tool spend below the whole-company level? |
| 10 | Optimise | Can you currently quantify ROI from AI coding tools? |

**Mid-quiz insight interrupt (shown after Q6):** "Veracode's 2025 research found AI-generated code introduces at least one exploitable vulnerability in 45% of coding tasks. If you answered 'Never' to scanning, that's not a hypothetical."

**Tier outcomes:** Ungoverned (0–25) · Reactive (26–50) · Structured (51–75) · Governed (76–100)

---

## 6. Key facts & stats safe to use in ads (all verified, sourced)

- **45%** of AI-generated code contains an exploitable vulnerability — *Veracode, 2025*
- **$4.4M** global average cost of a data breach; **$10.2M** in the US — *IBM Cost of a Data Breach Report, 2025*
- Starting from **$1,999/month** for the Fractional AI Officer (FAO) engagement — vs. **$180K–$250K+** fully-loaded cost of hiring a dedicated AI governance lead
- **72 hours** — time to embed an FAO and start governing
- **Day 30** — first risk report / walk-away checkpoint (no lock-in)
- **5.0 rating** on Clutch, DesignRush (16 reviews), and Google
- ISO 27001, ISO 9001 certified · CMMI Level 3 Appraised

**Do not use:** any number not listed above. No fabricated client names, logos, or testimonials — only the anonymized/sourced ones listed in §4.

---

## 7. CTA / funnel destinations (for tracking/UTMs)

- Quiz start → in-page (no URL change)
- "Skip to booking a call" / nav CTA → `/assessment`
- Calendly event used downstream: `calendly.com/saswata-upcoretechnologies/ai-governance-review` (45 min)
- Google Ads conversion action: "Governance Index — Assessment Complete"

---

## 8. Tone & voice notes for copywriters/designers

- Direct, second-person, no fluff. Short sentences. Confident but not hypey.
- Never say "AI-certified" or use unverifiable superlatives.
- Every stat must be sourced — this brand has been through multiple fact-check passes specifically to avoid fabricated claims; don't reintroduce any.
- Visual identity should feel like a **security/dev-tooling product** (console, monospace accents, precise data visualization) — closer to a Vercel/Linear/Datadog aesthetic than a generic corporate SaaS page.
