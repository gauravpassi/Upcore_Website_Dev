# Content pass (2026-10-28) and statistics to fix

## Content JSON pass: 26 article files edited

**Status:** all 26 article files are edited. Validation passed:
- Every file loads with `json.load`.
- Byte format is unchanged: `indent=1`, `ensure_ascii=False`, CRLF, no trailing newline.
- Key order is unchanged, and `published`, `date_label`, `title`, `path`, `file`, `kind`, `faq`, `stats`, `eyebrow`, `robots` and `lead` are identical to HEAD.
- Section ids and h2s are unchanged.
- All 26 metas are 140–155 characters, with no "…".
- No em dash (U+2014) appears in any added line. `privacy.json` has an old em dash that I did not touch.
- Every new href resolves to an existing `.html` file.
- Every `<a>` is balanced and none are nested.

I did not commit or build anything, and did not touch `privacy.json` or `terms.json`. Others have uncommitted changes to the generator; `build_library.py` now reads optional `author`/`updated` fields. That doesn't conflict with this pass. The edit script is at `C:\Users\saswa\AppData\Local\Temp\claude\C--Users-saswa-SEO\4a437a9e-3cbb-4b63-acb3-3357d2d3e9c5\scratchpad\work\edit.py`.

**Shared conventions:**
- Related kickers are `Service`, `Who we help`, `Guide`, `Playbook`, `Framework` or `Comparison`.
- Titles and descriptions are plain text taken from each target page's own title and meta, with no statistics.
- Service descriptions paraphrase each service page's meta.
- The old related entries ("Platform · April 2, 2025 · 8 min read" descriptions, `/platform` listed twice, misleading titles like "AI Workforce vs. AI Tools" pointing at `/ai-engineering-governance`) are gone.

### Import artifacts fixed
- **H1s:**
  - banking: "…to WhatsApp (And What It Takes to Do It Right)"
  - healthcare: "…More Than You Think, and AI Changes the Equation"
  - logistics: `…"Where Is My Order?" Here's How to Eliminate It`
  - manufacturing: "…3 Months Too Late (And What an AI Agent Changes)"
  - SaaS: "…Warning Signal Problem, and Most Teams Catch It 30 Days Too Late"
- **Leads:** none needed fixing. All 15 insights leads are empty and the learn leads were clean.
- **Body, dashes that had become periods** (now `&ndash;` or a colon):
  - banking: 3
  - ecommerce: 1
  - edtech: 3
  - healthcare: 1
  - logistics: 2
  - manufacturing: 1
  - nbfc: 1
  - real estate: 1
- **Duplicate label:** the extra `<strong>Key Takeaway</strong>` in callouts is removed in choosing-first, government, legal, marketing and roi.
- **Manufacturing, section 3:** the h3 block "The Shift Toward Predictive Detection" was imported three times. I removed the two verbatim copies (2 paragraphs each) and kept the first, which also has the human-in-the-loop paragraph.

### Per file: meta (length) · links added (href "anchor") · related · aside

**Compare: `ai-agents-vs-copilot-financial-services`**
- Meta (144): "Why Microsoft Copilot pilots stall in financial services, and where custom AI agents win on data sovereignty, domain knowledge and auditability."
- Links:
  - `/platform` "Custom AI agents deployed for FS workflows"
  - `/insights/nbfc-kyc-automation` "The KYC agent"
  - `/insights/banking-ai-customer-service` "Customer service agents"
- Related: `/learn/ai-in-banking`, `/insights/banking-ai-customer-service`, `/insights/nbfc-kyc-automation`, `/ai-engineering-governance` (Service)
- Aside: changed from AI Governance to **Business Process Automation** (`/platform`). The page argues for buying custom agents.

**`insights/banking-ai-customer-service`**
- Meta (155): "Indian banks are moving customer service to WhatsApp. See how AI agents answer routine queries, escalate sensitive ones and keep the oversight RBI expects."
- Links:
  - `/insights/human-in-the-loop` "appropriate human oversight"
  - `/learn/ai-in-banking` "AI in banking"
  - `/platform` "deploying AI customer service"
  - `/who-we-help/operations-heavy` "expanding service capacity without proportional cost increases"
- Related: `/learn/ai-in-banking`, `/compare/ai-agents-vs-copilot-financial-services`, `/insights/nbfc-kyc-automation`, `/platform`
- Aside: BPA (unchanged)

**`insights/choosing-first-ai-agent`**
- Meta (150): "How to choose your first AI agent: pick a high-volume, low-variance workflow with a clear metric, low error cost and a person to catch the exceptions."
- Links:
  - `/insights/human-in-the-loop` "Human in the loop"
  - `/who-we-help/operations-heavy` "KYC and document collection agents"
  - `/platform` "how Upcore approaches first deployments"
  - `/fractional-ai-officer` "best AI strategy for an organization"
- Related: `/insights/roi-business-case-ai-agents`, `/insights/human-in-the-loop`, `/learn/enterprise-ai-strategy`, `/fractional-ai-officer`
- Aside: BPA (unchanged)

**`insights/ecommerce-cart-recovery-whatsapp`**
- Meta (155): "Cart abandonment is a timing and channel problem. See how a WhatsApp cart recovery agent reaches shoppers inside the 78-minute window, before intent fades."
- Links:
  - `/who-we-help/ecommerce-retail` "ecommerce platforms"
  - `/insights/logistics-wismo-ai-agents` "order updates, tracking information"
  - `/platform` "An AI recovery agent"
- Related: `/insights/logistics-wismo-ai-agents`, `/who-we-help/ecommerce-retail`, `/insights/edtech-enrollment-ai`, `/platform`
- Aside: BPA

**`insights/edtech-enrollment-ai`**
- Meta (150): "EdTech platforms lose qualified leads to slow, generic follow-up. An AI enrollment agent replies in seconds, personalizes and hands off to counselors."
- Links:
  - `/who-we-help/operations-heavy` "speed of first response"
  - `/platform` "An AI enrollment agent"
  - `/insights/human-in-the-loop` "hands off to human counselors"
- Related: `/insights/real-estate-lead-conversion`, `/insights/ecommerce-cart-recovery-whatsapp`, `/who-we-help/operations-heavy`, `/platform`
- Aside: BPA

**`insights/government-ai-citizen-services`**
- Meta (154): "How AI agents on WhatsApp help government bodies answer citizen queries in local languages, track grievances and escalate to officers with an audit trail."
- Links:
  - `/platform` "An AI agent on that same channel"
  - `/who-we-help/operations-heavy` "provides an immediate update"
  - `/insights/human-in-the-loop` "Escalation to a human officer"
- Related: `/insights/banking-ai-customer-service`, `/insights/human-in-the-loop`, `/who-we-help/operations-heavy`, `/platform`
- Aside: BPA

**`insights/healthcare-patient-no-show-ai`**
- Meta (152): "Patient no-shows cost clinics more than an empty slot. An AI appointment agent goes beyond reminders: it confirms, reschedules and fills canceled slots."
- Links:
  - `/platform` "An AI appointment agent"
  - `/learn/ai-data-governance` "data privacy"
  - `/who-we-help/operations-heavy` "appointment scheduling, reminders, and follow-up"
- Related: `/learn/hipaa-compliant-ai`, `/who-we-help/operations-heavy`, `/insights/logistics-wismo-ai-agents`, `/platform`
- Aside: BPA

**`insights/human-in-the-loop`**
- Meta (152): "Human in the loop is how enterprise AI scales. Learn the four oversight layers (automate, notify, approve, escalate) and where each AI decision belongs."
- H1 left as is: it is two grammatical sentences.
- Links:
  - `/insights/manufacturing-ai-quality-control` "an AI quality control system"
  - `/ai-native-engineering` "The QA engineer approved the release"
  - `/platform` "Upcore's approach to human-in-the-loop implementation"
- Related: `/insights/choosing-first-ai-agent`, `/insights/manufacturing-ai-quality-control`, `/learn/how-ai-agents-work`, `/platform`
- Aside: BPA

**`insights/legal-ai-contract-review`**
- Meta (155): "First-pass contract review is pattern-based work. See how AI contract review flags non-standard clauses and risks, so lawyers spend their time on judgment."
- Links:
  - `/platform` "An AI contract review agent"
  - `/insights/human-in-the-loop` "escalation to a partner"
  - `/who-we-help/professional-services` "Law firms that adopt AI"
- Related: `/who-we-help/professional-services`, `/insights/human-in-the-loop`, `/insights/roi-business-case-ai-agents`, `/platform`
- Aside: BPA

**`insights/logistics-wismo-ai-agents`**
- Meta (154): "WISMO queries flood logistics support. See how AI agents send proactive WhatsApp tracking updates, so customers know where their order is before they ask."
- Links:
  - `/platform` "A full AI communication layer"
  - `/who-we-help/ecommerce-retail` "direct-to-consumer e-commerce deliveries"
  - `/who-we-help/operations-heavy` "The operations team can focus on exceptions"
- Related: `/insights/ecommerce-cart-recovery-whatsapp`, `/who-we-help/ecommerce-retail`, `/who-we-help/operations-heavy`, `/platform`
- Aside: BPA

**`insights/manufacturing-ai-quality-control`**
- Meta (150): "Manufacturing defects surface in the field months after shipment. See how an AI quality control agent spots patterns across shifts and lines in hours."
- Links:
  - `/who-we-help/operations-heavy` "A manufacturing operations team"
  - `/platform` "An AI quality control agent"
  - `/insights/human-in-the-loop` "human-in-the-loop approval gate"
- Related: `/insights/human-in-the-loop`, `/who-we-help/operations-heavy`, `/insights/choosing-first-ai-agent`, `/platform`
- Aside: BPA

**`insights/marketing-ai-execution-vs-strategy`**
- Meta (153): "Marketers lose most of their week to reporting, follow-up and briefs. See how AI agents take over marketing execution so your team can focus on strategy."
- Links:
  - `/platform` "Campaign Report Agent"
  - `/results` "Content Brief Agent" (the real briefing-agent case)
  - `/insights/roi-business-case-ai-agents` "Time saved per week per team member"
- Related: `/insights/roi-business-case-ai-agents`, `/insights/choosing-first-ai-agent`, `/platform`
- No segment link: marketing-agencies redirects to professional-services, which doesn't fit in-house marketing teams.
- Aside: BPA

**`insights/nbfc-kyc-automation`**
- Meta (151): "NBFCs can cut KYC TAT from 7 days to hours without skipping compliance steps: automate the waiting between steps and keep credit decisions with people."
- Links:
  - `/insights/human-in-the-loop` "decision-making steps that require human judgment"
  - `/who-we-help/operations-heavy` "Document collection"
  - `/platform` "an AI orchestration agent"
- Related: `/learn/ai-in-banking`, `/insights/banking-ai-customer-service`, `/insights/human-in-the-loop`, `/platform`
- Aside: BPA

**`insights/real-estate-lead-conversion`**
- Meta (154): "Property buyers decide within 48 hours, but most builders follow up too slowly. See how AI agents respond, personalize and qualify leads before rivals do."
- Links:
  - `/who-we-help/operations-heavy` "A mid-sized residential builder"
  - `/insights/edtech-enrollment-ai` "first meaningful outreach"
  - `/platform` "An AI agent that processes the inquiry"
- Related: `/insights/edtech-enrollment-ai`, `/who-we-help/operations-heavy`, `/insights/roi-business-case-ai-agents`, `/platform`
- Aside: BPA

**`insights/roi-business-case-ai-agents`**
- Meta (144): "Build a business case for AI agents that your finance team will approve, using three numbers: hours saved, revenue uplift and risk cost avoided."
- Links:
  - `/fractional-ai-officer` "no owner of the outcome"
  - `/insights/nbfc-kyc-automation` "NBFC KYC follow-up"
  - `/insights/real-estate-lead-conversion` "Lead Qualification Agent"
  - `/platform` "Deadline Tracker Agent"
- Related: `/insights/choosing-first-ai-agent`, `/learn/enterprise-ai-strategy`, `/insights/nbfc-kyc-automation`, `/fractional-ai-officer`
- Aside: Fractional AI Officer (unchanged)

**`insights/saas-churn-ai-early-warning`**
- Meta (155): "SaaS churn decisions are made 30 to 60 days before the cancellation email. See how an AI health scoring agent spots the warning signs and alerts your CSMs."
- Links:
  - `/who-we-help/tech-software` "SaaS company"
  - `/platform` "An AI health scoring agent"
  - `/insights/human-in-the-loop` "the handover"
- Related: `/who-we-help/tech-software`, `/insights/human-in-the-loop`, `/insights/roi-business-case-ai-agents`, `/platform`
- Aside: BPA
- The tech-software link is a weak topical match (that page is about engineering delivery). I kept it because the audit asked for it.

**`learn/ai-agent-memory`**
- Meta (152): "How AI agent memory works: episodic, semantic, procedural and working memory, how each is built, and the governance controls regulated enterprises need."
- Links:
  - `/platform` "custom agents"
  - `/ai-engineering-governance` "data governance controls"
- Related: `/learn/how-ai-agents-work`, `/learn/ai-agent-vs-llm`, `/learn/ai-agent-skills`, `/platform`
- Aside: BPA

**`learn/ai-agent-skills`**
- Meta (149): "AI agent skills: tool use, API calls, memory retrieval and form filling, each mapped to an enterprise use case, plus how skills are built and tested."
- Link: `/platform` "how Upcore implements skills"
- Related: `/learn/how-ai-agents-work`, `/learn/ai-agent-memory`, `/learn/ai-agent-vs-llm`, `/platform` (the duplicate `/platform` entry is removed)
- Aside: BPA

**`learn/ai-agent-vs-llm`**
- Meta (151): "AI agent vs LLM: an LLM is a stateless reasoning engine; an agent adds memory, tools, goals and orchestration to take action. Learn when you need each."
- Link: `/platform` "embedded in a system architecture"
- Related: `/learn/how-ai-agents-work`, `/learn/ai-agent-memory`, `/learn/ai-agent-skills`, `/platform`
- Aside: BPA

**`learn/ai-data-governance`**
- Meta (154): "An AI data governance checklist for CTOs and CIOs: five pillars, 15 questions every AI vendor must answer, sector rules and on-premise deployment options."
- Link: `/ai-engineering-governance` "governance-ready AI deployment"
- Related: `/learn/hipaa-compliant-ai`, `/compare/ai-agents-vs-copilot-financial-services`, `/security`, `/ai-engineering-governance`
- Aside: AI Governance

**`learn/ai-in-banking`**
- Meta (155): "AI in banking: front, middle and back office use cases, the compliance limits of generic AI tools, and the architecture that keeps regulated data in-house."
- Links:
  - `/platform` "Purpose-built AI agents"
  - `/insights/banking-ai-customer-service` "24/7 resolution of balance inquiries"
- Related: `/compare/ai-agents-vs-copilot-financial-services`, `/insights/banking-ai-customer-service`, `/insights/nbfc-kyc-automation`, `/platform`
- Aside: BPA

**`learn/ai-workforce-platform`**
- Meta (154): "What an AI workforce platform is: a coordinated team of specialized agents, how it compares with point tools, how it is built and who should evaluate one."
- Links:
  - `/platform` "Upcore's platform deployment methodology"
  - `/who-we-help/operations-heavy` "Your workflows generate more volume than your human teams can handle"
- Related: `/learn/how-ai-agents-work`, `/learn/top-ai-agent-platforms`, `/insights/choosing-first-ai-agent`, `/platform`
- Aside: BPA

**`learn/enterprise-ai-strategy`**
- Meta (152): "An enterprise AI strategy framework: the five decisions to make before you deploy AI, from build vs buy to cloud vs on-premise, and a practical roadmap."
- Links:
  - `/fractional-ai-officer` "a designated programme lead"
  - `/insights/choosing-first-ai-agent` "workflow mapping exercise"
- Related: `/insights/roi-business-case-ai-agents`, `/insights/choosing-first-ai-agent`, `/learn/ai-data-governance`, `/fractional-ai-officer`
- Aside: FAO

**`learn/hipaa-compliant-ai`**
- Meta (152): "What HIPAA-compliant AI requires: where PHI is processed, no training on PHI, audit trails and BAAs, plus questions to ask any AI vendor before signing."
- Links:
  - `/ai-engineering-governance` "evaluate AI vendors against HIPAA requirements"
  - `/insights/healthcare-patient-no-show-ai` "no-show re-booking"
- Related: `/learn/ai-data-governance`, `/insights/healthcare-patient-no-show-ai`, `/security`, `/ai-engineering-governance`
- Aside: AI Governance

**`learn/how-ai-agents-work`**
- Meta (155): "How AI agents work in plain English: perception, reasoning and action layers, how agents differ from chatbots and workflow tools, and how they're deployed."
- Links:
  - `/forward-deployed-engineer` "an integration and systems engineering project"
  - `/insights/human-in-the-loop` "human-in-the-loop policies"
- Related: `/learn/ai-agent-vs-llm`, `/learn/ai-agent-memory`, `/learn/ai-agent-skills`, `/platform`
- Aside: BPA

**`learn/top-ai-agent-platforms`**
- Meta (154): "AI agent platforms compared: AutoGen, LangChain, Vertex AI Agents and Copilot Studio. Where each fits, where each falls short and how to choose your path."
- Links:
  - `/forward-deployed-engineer` "the quality of the implementation team matters more than the quality of the framework"
  - `/platform` "a working agent that runs your business"
- Related: `/learn/how-ai-agents-work`, `/learn/ai-workforce-platform`, `/learn/ai-agent-skills`, `/platform`
- Aside: changed from BPA to **Fractional FDE** (`/forward-deployed-engineer`), per strategy R2.

### Left alone on purpose
- The "₹5 Lakh" H1 on choosing-first-ai-agent; it has no import artifact.
- Typo "the AI follow up" in healthcare section 2.
- Currency symbols that appear lost in import. edtech has "spends 40,000 per month", "approximately 200" and "8,000 weekly"; manufacturing has "recall costs … 200,000 to 500,000". I couldn't tell whether the symbol was ₹ or $.

### Statistics that look unsourced, outdated or wrong (not fixed)

**Learn guides**
- **`learn__hipaa-compliant-ai`**
  - stats "$1.9M Average cost of a healthcare data breach (IBM, 2024)": IBM 2024 puts healthcare at about $9.77M. $1.9M looks mixed up with an HHS penalty figure.
  - body/FAQ "civil monetary penalties up to $1.9 million per violation category per year": the inflation-adjusted annual cap is about $2.1M (2024). Looks outdated.
  - stats "83% Of AI tools used in healthcare fail to meet HIPAA minimum standards": no source.
  - "documentation burden that consumes 30–40% of physician time" and "reduce denial rates by 20–30%": unsourced.
- **`learn__ai-in-banking`**
  - stats "$487B Projected AI cost savings in banking by 2030 (McKinsey)": doesn't match known McKinsey figures (about $1T annual value; $447B is an Autonomous NEXT/Business Insider number). The FAQ calls it "cost savings and revenue uplift", which is inconsistent.
  - "73% Of bank CIOs name compliance as their #1 AI concern": no source.
  - AML workload "60–80%", cost per interaction "60–80%", fraud "20–40%", "10x the volume", "70–85% of inbound queries" and "4–6 FTE, payback <6 months": all unsourced.
- **`learn__ai-data-governance`**
  - "62% Of AI projects blocked by data governance concerns": no source (strategy R3).
  - EU AI Act "phased compliance timelines through 2026" in the body vs "2026–2027" in the FAQ. Obligations run to August 2027.
- **`learn__enterprise-ai-strategy`**
  - "85% Of AI projects never reach production": often misattributed (R10).
  - "18 mo average time to first meaningful AI ROI" and "3x more likely to scale": unsourced.
- **`learn__ai-workforce-platform`**
  - "6–8" tools and "40% average utilisation", while the body says "below 50%": unsourced and inconsistent.
  - Body pricing "$80,000 to $300,000 for initial deployment … maintenance 15–25%" and "$100,000 deployment pays back in 6–8 months": unpublished Upcore pricing. This conflicts with the guardrail (only the FAO price is published) and with the segment pages ("We don't publish a price list").
- **`learn__ai-agent-skills`** "100% Of enterprise workflows require at least 3 agent skills" and **`learn__ai-agent-memory`** "100% Of context-dependent decisions require memory": unsourced or circular.
- **"30 days" stats** in skills, data-governance and ai-in-banking ("Upcore deployment time"): the site's wording is "first agent live within 30 days of design sign-off". Align the qualifier.

**Compare page (`compare__ai-agents-vs-copilot-financial-services`)**
- "RBI's Master Direction on outsourcing … explicitly requires that data … be stored and processed within India, on infrastructure that the regulated entity controls": overstated. RBI's localisation mandate covers payment-system data.
- "RBI's 2023 guidelines on cloud adoption … explicit regulatory approval for certain data categories": needs verifying.
- "Basel III's requirements for model risk management": model risk management is mainly SR 11-7 / PRA SS1/23.
- "Dozens of Copilot pilots in FS have quietly ended": unsourced.
- Copilot "$30 per user per month" needs an "as of" date.

**Insights**
- **`insights__banking-ai-customer-service`**
  - "India has 500 million WhatsApp users": no year or source.
  - Open rates "85–95%" vs email "15–25%" and SMS "30–40%": unsourced; SMS is usually cited much higher.
  - "A survey of mid-sized Indian banks found … 62% reached out first on WhatsApp", "35–40% now come via WhatsApp" and the query-mix percentages: unsourced.
  - Internal conflict: "85%" automatable vs the "Automate" tier at "50–60%".
  - "According to RBI guidelines, AI can be deployed … as long as…": presents rules RBI hasn't issued in that form.
- **`insights__ecommerce-cart-recovery-whatsapp`**
  - "68%… within two hours", "78%… within 78 minutes", "2.3x", 1.7x/2.8x/3.1x and "35% lower at 90 minutes": all unsourced.
  - "What Upcore's Clients See": a "25% to 40%" recovery lift is an Upcore claim not on /results. The math is also off: 12% plus 25–40% gives 15–16.8%, not "17% to 19%".
- **`insights__edtech-enrollment-ai`**
  - Response-time study "34% / 19% / 4%": unsourced.
  - The callout says "3-4x the rate of a response an hour later", but 34% vs 19% is about 1.8x.
  - The ad-spend math doesn't add up, and currency symbols are missing.
  - H1 says "60%" don't convert; the body says "the other 80% are lost".
- **`insights__government-ai-citizen-services`**
  - "call centre … ₹3–5 crore per month" for 50,000 queries a month looks implausibly high.
  - "roughly 35% of India's rural population has never accessed the internet": the only source given is "recent surveys".
  - "85% of Indians already use" WhatsApp contradicts the article's own 500M users (about 35% of the population).
  - "chatbot reached 5 crore users": needs verifying.
- **`insights__healthcare-patient-no-show-ai`**
  - "20-30% / 25%" no-show rates: unsourced.
  - "A no-show prevented is worth 3x a new appointment": unsourced.
  - "300+ vs 150" appointments per receptionist: unsourced.
- **`insights__human-in-the-loop`**
  - The opening manufacturing case ("98% accuracy", "15% below the pre-AI baseline") reads like a real case but has no source.
  - The 80/20 split and "85% vs 95% quality": unsourced (strategy R4).
- **`insights__legal-ai-contract-review`**
  - Time split is 40/30/20/10, then "That's 70% of the work that is systematically automatable"; 40+30+20 is 90%. The callout says "the 30% … that requires experience".
  - "150 → 250 contracts" (+67%) conflicts with "processes 200% of the contracts".
  - "₹25-40L per year fully loaded": unsourced.
  - "Upcore's contract review agent / legal AI is trained on Indian contracts": a product claim not on the site.
- **`insights__logistics-wismo-ai-agents`**
  - H1 and meta say "35%"; the body uses "20%".
  - 500–800 support hours a day is about 60–100+ FTE, not "30–50 full-time support agents".
  - "3% of shipments": unsourced.
- **`insights__manufacturing-ai-quality-control`**
  - Recall cost "200,000 to 500,000" (no currency, no source).
  - "200 to 400 hours" of engineering time per corrective-action (CAPA) cycle: unsourced.
  - "margin is 3 to 5 percent … 2% vs 0.5% defect rate": unsourced.
- **`insights__marketing-ai-execution-vs-strategy`**
  - H1 says "60%" on execution; the body breakdown adds to 75% (20+15+25+15).
  - "₹25–50L vs ₹3–5L" and "15–25% higher conversion": unsourced.
  - "an hour to five minutes" for briefs vs the real /results case (70% faster).
- **`insights__nbfc-kyc-automation`**
  - "The Credit Information Companies (Regulation) Act requires human judgment in credit assessments": CICRA regulates credit bureaus and doesn't say this.
  - The headline "7 days to 4 hours" vs the body's "16 to 18-hour process in most cases".
- **`insights__real-estate-lead-conversion`**
  - "Lose 70%": the body's own numbers (350 qualified, 40–60 booked) give 83–89% lost.
  - "460-unit loss into a 220-unit loss": going from 8% to 18–20% of 500 leaves about 400 lost.
  - "200+ crore in additional revenue per month": 50–60 extra units at ₹60–80L is about ₹30–48 crore.
  - "60-70% of the conversion" and "top 10% of builders": unsourced.
- **`insights__roi-business-case-ai-agents`**
  - "500 leads × 1% improvement × ₹60L = ₹30L": that is ₹3 crore.
  - "25 deals × ₹60L = ₹15L per month": that is ₹15 crore.
  - "ROI: 155x": ₹8.17 crore / ₹8L is about 102x.
  - "₹67,500 per week" × 52 is about ₹35L, not "₹27L".
  - All figures are in INR only (strategy R6).
- **`insights__saas-churn-ai-early-warning`**
  - "A 5% improvement in retention has more NPV impact than a 25% improvement in acquisition": a garbled version of the Bain/Reichheld "5% retention lifts profit 25–95%" claim.
  - The "30–60 days" decision window is unsourced.
- **`insights__choosing-first-ai-agent`**
  - "The 48-Hour Proof of Concept" and "48-hour setup" conflict with the site's standard ("first agent live within 30 days of design sign-off"; pilot duration agreed on the discovery call).
  - The ₹50L, ₹5L and ₹2 crore figures aren't labeled as illustrative.
