# N02 review: How to review AI-generated code

- **Preview:** https://upcore-website-5fsrfok2j-gauravpassis-projects.vercel.app/learn/how-to-review-ai-generated-code (Vercel Authentication: open while signed in to vercel.com with access to the gauravpassis-projects team)
- **Branch:** `content/how-to-review-ai-generated-code` (backup on the `dev` remote)
- **Title (58 chars):** How to Review AI-Generated Code: Tiered Checklist | Upcore
- **Meta (151 chars):** How to review AI-generated code: how AI-written pull requests fail, what to automate first, a checklist per risk tier and a PR template for AI changes.
- **Primary keyword:** how to review AI-generated code
- **Word count:** about 2,900 in the body, including two copy-paste code blocks (~400 words) and three tables
- **Author / reviewer:** saswata-sengupta / none
- **Drafted:** 2026-11-18

## What the top results miss and how this fills it

The top results on 2026-11-18 were vendor guides (Graphite, CodeRabbit, CodeAnt, Aviator, Verdent), Real Python, thoughtbot and several dev.to checklists.

- They say "focus on where AI is likely to be wrong" without saying where that is. This article has a **failure catalog** (8 patterns) with who catches each one: automation or a person.
- Most checklists are a single flat list applied to every PR. This one has **three risk tiers** with a copy-paste checklist each, plus the GitHub ruleset settings that enforce the high tier.
- None give a **PR template for AI-authored changes**. This one includes one: agent, plan, human-written parts, tier, scope, new dependencies, changed tests.
- Few say when to **send work back to the spec, plan or agent instructions** instead of fixing it in review. This article has a table for that.

## Fact-check list

| Claim | Source | Checked |
|---|---|---|
| 45% of test cases introduced an OWASP Top 10 vulnerability; 80 tasks; 100+ LLMs; July 2025 | https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/ | Fetched 2026-11-18. Quote: "In 45 percent of all test cases, LLMs introduced vulnerabilities classified within the OWASP ... Top 10" |
| XSS (CWE-80) 86%, log injection (CWE-117) 88% | same | Fetched 2026-11-18 |
| Larger models not significantly better on security | same | Fetched 2026-11-18 |
| Nov 2025 update: most providers stayed in the 50-59% range; GPT-5 Mini 72%, GPT-5 70% | https://www.veracode.com/press-release/veracode-research-reveals-openais-gpt-5-models-lead-the-way-in-secure-code-while-wider-industry-progress-stalls/ | Fetched 2026-11-18. The article says "most providers' newer models", matching "remained within the 50-59 percent range" |
| 576,000 samples, 16 LLMs, hallucinated packages at least 5.2% (commercial) and 21.7% (open-source), 205,474 unique names, USENIX Security 2025 | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | Fetched 2026-11-18 (abstract) |
| **As of November 2026:** Copilot code review leaves a "Comment" review by default; doesn't count toward required approvals; approvals off by default, configurable at enterprise/org/repo | https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review | Fetched 2026-11-18 |
| **As of November 2026:** Copilot "not guaranteed to spot all problems"; "Supplement Copilot's feedback with a human review"; doesn't review dependency management files such as package.json | https://docs.github.com/en/copilot/concepts/agents/code-review | Fetched 2026-11-18 |
| Copilot code review reads `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md` | the use-code-review page | Fetched 2026-11-18 |
| Rulesets: require code owner review; require approval of the most recent reviewable push | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets | Fetched 2026-11-18 |
| Upcore: an architect approves the AI-drafted plan before any build; merge limits start strict and loosen as the pipeline proves itself; installed in Jira/Linear, GitHub, CI/CD | live /ai-native-engineering page (built copy in this repo) | Matched to the page wording |

Not used: CodeRabbit's "1.7x more defects" (vendor study measured with its own product) and the Faros AI 98%/91% figures (already the lead stats of N01). The backlog's "CSA 2026 research note" wasn't needed; no CSA figure appears.

Uncited general statements (no figures): the `.github/pull_request_template.md` location, and Stryker, PIT and mutmut as mutation testing tools.

## Questions for the author

1. Which AI failure modes do our reviewers catch most often in real PRs? (A real, anonymized example in the failure catalog would make it much stronger.)
2. What do we automate before a human opens the diff? Does it match the "What to automate" table?
3. What's in the PR template we ask AI-authored changes to carry? Swap in ours if it differs.
4. When do we send a PR back to the spec instead of fixing it in review?
5. Are the tier definitions (which paths count as high risk) close to what we use with clients?

## Things I was unsure about

- **Length.** At about 2,900 words it's above the usual 1,500-2,500 for learn. Most of the overage is the two copy-paste blocks and tables, which are the original asset. If you want it shorter, cut "Where this fits in a governed delivery process" down to its last paragraph, and drop the "Where an AI reviewer fits" custom-instructions paragraph.
- **Overlap with N01** (risk-based merge, still in review). N01 covers scoring and auto-merge policy. This one covers how a person reviews. Both use the Veracode 45% stat. If N01 publishes first, add a link from "Assign the tier from what the change touches" to N01.
- **Links not added yet** (targets unpublished): N01 `/learn/risk-based-merge-ai-pull-requests`, N03 `/learn/ai-code-review-bottleneck`, N10 `/learn/slopsquatting-hallucinated-packages`. Add them when those publish.
- **Wiring.** Cluster A has no JSON articles, so no existing article's `related` list was changed. I added this article second in the /ai-native-engineering "Further reading" list (`reading.py`). The Python-built `/learn/what-is-ai-native-engineering` (build_guide.py) should link to it; I didn't edit that builder. Not the cluster pillar, so `FEATURED` was left alone.
- **Preview check.** The deployment is up but behind Vercel login. I didn't create a share link to read it from outside, so check that it loads when you sign in.

## Approval checklist

1. [ ] Every number traced to its source
2. [ ] Upcore claims match the site
3. [ ] No keyword overlap with an existing URL (checked: none of the content JSON or Python builders target it)
4. [ ] Original asset present (failure catalog, tiered checklist, PR template)
5. [ ] Links resolve (validator: OK)
6. [ ] Author set (saswata-sengupta; no reviewer)
7. [ ] Dates set (published 2026-11-18; PUBLISH.md resets it)
8. [ ] CTA matches the persona (booking, via the AI-Native Engineering aside)
9. [ ] Reads like a practitioner wrote it
10. [ ] Title (58) and meta (151) within length
