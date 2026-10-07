"""/learn/what-is-ai-native-engineering (2026-10-07): the category guide. Definition, AI-assisted vs
AI-native, why it matters, the building blocks, how roles change, what to measure, common mistakes,
how to start, FAQ. Educational and vendor-neutral in tone; links into /ai-native-engineering.
Only one statistic, already cited elsewhere on the site.
Run from the repo root: python tools/v4-build/build_guide.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import article as A

AINE = C.URL['aine']
DEF = A.callout('Definition', '<p><b>AI-native engineering</b> is a way of building software in which AI agents do most of the routine design, coding and testing work, inside a delivery process designed for them: written specs, architecture rules the machine can check, automated checks on every change, limits on what can merge without a person, and a record of every decision. People set the rules, approve plans and handle the changes that need judgment.</p>')

S = []
S.append(('definition', 'The short answer', f'''{DEF}
<p>Most teams now use AI to write code. Far fewer have changed how software gets specified, reviewed and released to match. AI-native engineering is that second step. The question stops being &ldquo;how do we help each developer type faster?&rdquo; and becomes &ldquo;how do we run delivery when much of the first draft is written by a machine?&rdquo;</p>
<p>The answer is not a single tool. It is a process with a small number of parts, each of which makes AI-written work easier to trust: clearer inputs, explicit rules, automated checks, controlled releases and a written trail of what was decided and why.</p>'''))

S.append(('vs-assisted', 'AI-assisted versus AI-native', f'''<p>The difference is where the change happens. AI-assisted engineering adds tools to an unchanged process. AI-native engineering redesigns the process around what the tools do well and the mistakes they tend to make.</p>
{A.table(['Question', 'AI-assisted', 'AI-native'], [
    ('Unit of work', 'A prompt in a developer&rsquo;s editor', 'A written spec with acceptance criteria'),
    ('Architecture rules', 'In senior engineers&rsquo; heads', 'Written down and checked automatically'),
    ('Review', 'People read every AI-written line', 'Automated checks first; people review what is risky'),
    ('Merging', 'Same rules as hand-written code', 'Risk-scored, with limits you set'),
    ('Release', 'Same as before', 'Behind feature flags, watched, then rolled out or back'),
    ('Record', 'Pull-request comments', 'A log of every deviation, why it happened and who decided'),
    ('Who benefits', 'Individual developers', 'The whole team, measurably')], 'AI-assisted and AI-native engineering compared', us=2)}
<p>Neither is wrong. AI assistants are often the right first step. The trouble starts when output rises but the process around it stays the same: review queues grow, architecture drifts and nobody can say what changed or why.</p>'''))

S.append(('why-now', 'Why it matters now', '''<p>When AI writes the first draft, the bottleneck moves. Writing code gets cheaper; reading, checking and trusting it does not. Senior engineers end up reviewing more code they did not write, often without the context of why it was written that way.</p>
<p>Quality is the other pressure. Veracode&rsquo;s 2025 GenAI Code Security Report found that 45% of AI-generated code contained security flaws. Tools built to scan human-written code were not designed for the mistakes models make, such as importing packages that do not exist or quietly inverting a permission check.</p>
<p>Leadership feels it last but hardest: spend on AI tools rises, and nobody can show the board what it changed, what it broke or who approved it. An AI-native process is how you get those answers without slowing teams down.</p>'''))

BLOCKS = [('Specs from a template', 'Every change starts as a short written spec: scope, acceptance criteria, the services it touches, any data changes. It is the input the AI works from and the yardstick it is checked against.'),
          ('Architecture rules the machine can check', 'Your decision records, database schema, API conventions and design system, written so automated checks can compare a spec or a change against them.'),
          ('A plan, approved before the build', 'AI drafts the implementation plan (files, interfaces, migrations, tests) and an architect signs it off. Most expensive mistakes are cheaper to catch here than in a pull request.'),
          ('Build and test in a sandbox', 'Code is written and run in an isolated environment, with tests generated from the acceptance criteria. Tests pass before anyone is asked to look.'),
          ('Automated pull-request checks', 'Architecture rules, security scanning, test coverage and a clear description, checked on every change before a person reviews it.'),
          ('Risk-scored merging', 'Each change gets a risk score based on how far it departs from your rules. Low-risk changes merge on their own; anything above your limit goes to a named approver.'),
          ('Scenario tests and controlled releases', 'Changes run against known-good tasks in staging, then go to a small share of users behind a feature flag and are watched before they are rolled out further.'),
          ('A feedback loop', 'Tickets, decisions and incidents are linked, so the next spec starts with the history of what came before.')]
blocks = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in BLOCKS)
S.append(('building-blocks', 'The building blocks', f'''<p>Different teams name the stages differently, but an AI-native delivery process usually has these parts. Each one either gives the AI better input or makes its output cheaper to trust.</p>
<ol class="ar-steps">{blocks}</ol>
<p>Autonomy is earned, not assumed. Merge limits start strict and loosen only as the process proves itself on the team&rsquo;s own work. <a class="link" href="{AINE}#pipeline">See how we install these stages</a></p>'''))

S.append(('roles', 'How the roles change', '''<p>AI-native engineering does not remove engineers. It changes where their time goes.</p>
<ul class="ar-list"><li><b>Engineers</b> spend less time typing routine code and more time writing and reviewing specs, approving plans and handling the changes that genuinely need judgment.</li>
<li><b>Architects</b> own the rules. Their decisions are written down once and checked on every change, instead of being re-explained in review comments.</li>
<li><b>Engineering managers</b> manage flow: where work waits, which checks fail most and where the merge limits sit.</li>
<li><b>Leadership</b> gets a view it has rarely had: what shipped, what was held, what broke a rule and who decided.</li></ul>'''))

S.append(('measures', 'What to measure', '''<p>Measure the team, not the individual, and compare against your own baseline before any change.</p>
<ul class="ar-list"><li><b>Lead time</b> from spec to production.</li>
<li><b>Review time</b> per change, and how much of it senior engineers carry.</li>
<li><b>Share of changes merged automatically</b>, and how that grows as limits loosen.</li>
<li><b>Change failure rate</b> and time to restore, as in the familiar DORA measures.</li>
<li><b>Rule deviations</b>: how often changes break an architecture rule, and what was decided.</li>
<li><b>Cost per change</b>, including AI tool and token spend.</li></ul>
<p>Lines of code and prompts per developer are poor measures. They reward volume, and volume is the one thing AI already provides.</p>'''))

S.append(('mistakes', 'Common mistakes', '''<ul class="ar-list"><li><b>Buying tools and changing nothing else.</b> Output rises, review queues grow and quality becomes a matter of luck.</li>
<li><b>Letting autonomy run ahead of evidence.</b> Auto-merging before the checks have proved themselves on your codebase.</li>
<li><b>Rules that live in people&rsquo;s heads.</b> If an architecture decision is not written down, no check can enforce it.</li>
<li><b>No record of decisions.</b> When something breaks, nobody can say which change caused it or who approved it.</li>
<li><b>Rolling out everywhere at once.</b> One team and one service first; the lessons transfer.</li></ul>'''))

S.append(('start', 'How to start', f'''<ol class="ar-list ar-list--num"><li><b>Pick one team and one service</b> with a real backlog, not a demo project.</li>
<li><b>Write down the rules</b> that matter most: a handful of architecture decisions, API conventions and the schema.</li>
<li><b>Set strict merge limits</b> so every change is reviewed at first.</li>
<li><b>Agree the measures</b> and capture today&rsquo;s baseline.</li>
<li><b>Run it for a few weeks</b>, then loosen limits only where the evidence supports it.</li></ol>
<p>That is the shape of the pilot we run with clients: one team, one service, measured against your current process before anything wider. <a class="link" href="{AINE}#engagement">How a pilot works</a></p>'''))

FAQ = [('Is AI-native engineering the same as vibe coding?', 'No. Vibe coding usually means prompting until something works and shipping it with little review. AI-native engineering is the opposite discipline: specs, written rules, automated checks, risk-based merge limits and a record of every decision.'),
       ('Do we need new tools?', 'Usually not many. The process runs inside what most teams already use: Jira or Linear, GitHub or GitLab, your CI/CD and the AI assistants you have approved. What changes is how they are connected and what is checked.'),
       ('Will it replace our engineers?', 'It changes their work rather than removing it. Routine code is drafted by AI; engineers write and review specs, approve plans and handle the changes that need judgment.'),
       ('How long does it take to adopt?', 'A first team can usually run a pilot within weeks. Wider rollout depends on how many teams and repositories you have and how quickly the checks earn trust on your own codebase.'),
       ('How is it governed?', f'Through the process itself: rules are written down, every change is checked against them, merge limits are set by people, and every deviation is logged with who decided. For governance of AI use beyond engineering, see <a class="link" href="{C.URL["gov"]}">AI Governance</a>.')]

trail = [(C.URL['home'], 'Home'), (C.URL['insights'], 'Insights'), (None, 'What is AI-native engineering?')]
aside = f'<div class="ar-aside-cta"><p class="h-col">Put it into practice</p><p>See the nine stages we install, and how a pilot works.</p><a class="link" href="{AINE}">AI-Native Engineering</a></div>'
hero, body, mins = A.page(trail, 'Guide', 'What is <span class="hl">AI-native engineering?</span>',
                          'A plain-English guide for CTOs and engineering leaders: what it is, how it differs from giving developers AI assistants, what changes for your teams and how to start.',
                          S, meta_line='<span>Updated October 2026</span>', aside=aside)
faq = K.faq(FAQ, 'Common questions.')
final = K.final('Ready to try it <span class="hl">on one team?</span>',
                'Book a 45-minute discovery call. We&rsquo;ll review your delivery process and outline a pilot on one team, whether or not we work together.',
                f'Or read <a href="{C.URL["cmp-tools"]}">AI-native engineering vs AI coding tools <span aria-hidden="true">&rarr;</span></a>')
page = '\n'.join([hero, body, faq, final])
ld = C.graph('guide-aine', A.ld_article('guide-aine', 'What is AI-native engineering?', 'A plain-English guide to AI-native engineering: definition, how it differs from AI-assisted coding, the building blocks, roles, measures and how to start.', mins, FAQ), crumb='What is AI-native engineering?')
print('guide', C.write('learn/what-is-ai-native-engineering.html', 'guide-aine', 'What Is AI-Native Engineering? A Guide for CTOs | Upcore',
      'AI-native engineering explained: how it differs from AI-assisted coding, the building blocks of a governed AI delivery process, what to measure and how to start.',
      page, active='insights', ld=ld, group='guide', spine=False, main_cls='is-calm'))
