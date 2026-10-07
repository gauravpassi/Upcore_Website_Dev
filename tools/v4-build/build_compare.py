"""Comparison pages (2026-10-07), honest about when the alternative is the right call:
/compare/ai-native-engineering-vs-ai-coding-tools and /compare/upcore-vs-building-in-house.
No figures or product feature claims beyond what the site already states.
Run from the repo root: python tools/v4-build/build_compare.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import chrome as C
import calm as K
import article as A

AINE = C.URL['aine']
TRAIL = lambda t: [(C.URL['home'], 'Home'), (C.URL['insights'], 'Insights'), (None, t)]


def ul(items):
    return '<ul class="ar-list">' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in items) + '</ul>'


# ------------------------------------------------------------------ 1. vs AI coding tools
S1 = [
    ('short-answer', 'The short answer', A.callout('In one paragraph', '<p>AI coding tools generate code. AI-native engineering is the delivery process that makes that code safe to merge at scale: written specs, architecture rules that are checked automatically, risk-based merge limits, controlled releases and a record of every decision. It is not one or the other. The process runs on the tools you already use.</p>')),
    ('tools-do-well', 'What AI coding tools do well', '<p>Assistants such as GitHub Copilot, Cursor and Claude Code have earned their place. Used well, they:</p>' + ul([
        ('Draft quickly.', 'Boilerplate, tests, migrations and first drafts arrive in seconds.'),
        ('Explain code.', 'Unfamiliar services and legacy modules become easier to read.'),
        ('Handle larger changes.', 'Many now work across several files and can prepare a pull request.'),
        ('Lift individual developers.', 'Especially on routine, well-understood work.')]) + '<p>If your team is small and everyone knows the codebase, that may be all you need for now.</p>'),
    ('where-they-stop', 'Where they stop', '<p>The tools work at the level of a developer and a task. Delivery problems show up at the level of the team and the system:</p>' + ul([
        ('They don&rsquo;t know your unwritten rules.', 'Architecture decisions, API conventions and schema constraints that live in senior engineers&rsquo; heads are invisible to them.'),
        ('They don&rsquo;t decide what is safe to merge.', 'Every AI-written change still needs a person to judge it, so review load lands on your most senior people.'),
        ('They don&rsquo;t keep a record.', 'Why a change was made, which rule it broke and who approved it is scattered across chats and pull-request comments.'),
        ('Leadership sees usage, not outcomes.', 'Seat counts and acceptance rates don&rsquo;t tell you what changed in production or what it cost.')])),
    ('side-by-side', 'Side by side', A.table(['Question', 'AI coding tools alone', 'AI-native engineering'], [
        ('What you get', 'Code suggestions and changes in each developer&rsquo;s editor', 'A delivery process: specs, rules, checks, merge limits, releases and a decision log'),
        ('Who reviews AI-written code', 'Senior engineers, line by line', 'Automated checks first; people review what is risky'),
        ('Your architecture rules', 'Not checked', 'Checked at the spec, the plan and every pull request'),
        ('Merging', 'The same rules as hand-written code', 'Risk-scored, with limits you set and a named approver above them'),
        ('Releases', 'Unchanged', 'Behind feature flags, watched, then rolled out or back'),
        ('What leadership sees', 'Usage statistics', 'What shipped, what was held, which rules were broken and who decided')],
        'AI coding tools alone compared with AI-native engineering', us=2)),
    ('enough', 'When the tools alone are enough', ul([
        ('A small team', 'where everyone knows the codebase and reviews each other&rsquo;s work closely.'),
        ('Low-risk work', 'such as internal tools and prototypes, where a mistake is cheap to fix.'),
        ('Spare senior capacity', 'to review AI-written changes properly, without a queue building up.'),
        ('No audit trail needed', 'from customers, auditors or regulators.')])),
    ('need-more', 'When you need the process as well', ul([
        ('Several teams share services', 'and architecture is starting to drift.'),
        ('Review queues are growing', 'faster than your senior engineers can clear them.'),
        ('You handle regulated data', 'or customers ask who reviewed what and how.'),
        ('The board asks about AI', 'what it costs, what it changed and who is accountable.')])),
    ('fit', 'How they fit together', f'<p>Keep your tools. An AI-native process sits around them: specs in Jira or Linear, checks in GitHub and your CI/CD, merge limits and a decision log on top. The assistants your teams already use keep doing what they do well, with better inputs and a safety net around their output.</p><p><a class="link" href="{AINE}">See the nine stages we install</a> &middot; <a class="link" href="{C.URL["guide-aine"]}">Read the guide to AI-native engineering</a></p>')]
F1 = [('Do we have to replace Copilot, Cursor or Claude Code?', 'No. The process runs inside the tools you already use, including the AI assistants you have approved.'),
      ('Isn&rsquo;t this just code review with extra steps?', 'It moves most of the checking earlier and makes it automatic: a spec before the build, a plan an architect approves, and checks on every change. People then spend their review time on the changes that are genuinely risky.'),
      ('How do we know it is worth it?', 'Start with a pilot on one team and one service, measured against your current process. You see lead time, review time and what was caught before committing further.')]

# ------------------------------------------------------------------ 2. vs building in-house
S2 = [
    ('short-answer', 'The short answer', A.callout('In one paragraph', '<p>Build it yourself if you have a platform team with spare capacity and the patience to tune checks over months. Bring in Upcore if you want the process working on one team within weeks, measured against your own baseline, with someone accountable for keeping it working. You can also combine the two: your team builds alongside ours and owns the process at the end.</p>')),
    ('what-it-takes', 'What building it involves', '<p>An AI-native delivery process is more than a few CI jobs. To build it, your team would need to design and maintain:</p>' + ul([
        ('Spec templates', 'that give AI a usable input and give reviewers a yardstick.'),
        ('Architecture rules as checks,', 'turning decision records, schema and API conventions into something a machine can test.'),
        ('Pull-request checks', 'for rules, security and coverage, tuned so they catch real problems without blocking good work.'),
        ('Risk scoring and merge limits,', 'with named approvers and a way to loosen limits as evidence builds.'),
        ('Scenario tests, feature-flagged releases and monitoring', 'so changes are watched before they reach everyone.'),
        ('A deviation log and a leadership view', 'that someone keeps accurate.'),
        ('Ongoing tuning', 'as your system, your models and your tools change, plus the training and change management for your teams.')])),
    ('side-by-side', 'Side by side', A.table(['Question', 'Build it in-house', 'With Upcore'], [
        ('Time to first results', 'Depends on your platform team&rsquo;s capacity, alongside its roadmap', 'A pilot on one team, scoped on the discovery call'),
        ('Who designs the process', 'Your platform team, learning as it goes', 'A Claude Certified Architect with a tested pipeline design'),
        ('Who maintains the rules', 'Your platform team', 'An embedded architect on retainer, with your team'),
        ('Cost profile', 'Salaries and the opportunity cost of the platform team', 'A one-time implementation fee and a monthly retainer, fixed in a written proposal'),
        ('Where it runs', 'Your tools and repositories', 'Your tools and repositories')],
        'Building in-house compared with Upcore', us=2)),
    ('build', 'When building it yourself is right', ul([
        ('You have a platform team with real spare capacity', 'and leadership support for a long build.'),
        ('Your constraints are unusual,', 'such as fully air-gapped environments or custom tooling an outside team would need months to learn.'),
        ('You want to own every design decision', 'and have the time to make them.')])),
    ('bring-in', 'When bringing in Upcore is right', ul([
        ('You need results this quarter,', 'not after a platform project.'),
        ('Your platform team is fully committed', 'to the product roadmap.'),
        ('You want an outside benchmark', 'measured against your current process before you commit.'),
        ('You want someone accountable', 'for keeping the rules and checks current as your system evolves.')])),
    ('both', 'Doing both', f'<p>The options are not exclusive. In a done-with-you engagement your engineers build alongside ours, the process runs in your own tools and repositories, and your team owns it at the end. <a class="link" href="{AINE}#engagement">How we engage</a></p>')]
F2 = [('Can our team take it over later?', 'Yes. Everything runs in your own tools and repositories, and in a done-with-you engagement your engineers build it alongside ours so they can own it.'),
      ('Is there a platform we have to buy?', 'No. We install the process inside what you already run: Jira or Linear, GitHub, your CI/CD and the AI assistants you have approved.'),
      ('What does it cost?', 'We don&rsquo;t publish a price list. You start with a pilot on one team, then a one-time implementation fee scaled to the teams and repositories in scope, then a monthly retainer. You get a written proposal with a fixed scope and price before any build starts.')]

PAGES = [
    ('cmp-tools', 'compare/ai-native-engineering-vs-ai-coding-tools.html', 'AI-native engineering vs AI coding tools',
     'AI coding tools vs <span class="hl">AI-native engineering.</span>',
     'You may already pay for GitHub Copilot, Cursor or Claude Code. What those tools do well, where they stop, and when you need a delivery process around them.',
     S1, F1, 'AI-Native Engineering vs AI Coding Tools (Copilot, Cursor, Claude Code) | Upcore',
     'What AI coding tools do well, where they stop, and when engineering teams need an AI-native delivery process around them. An honest comparison for CTOs.',
     ('Upcore vs building it in-house', C.URL['cmp-inhouse'])),
    ('cmp-inhouse', 'compare/upcore-vs-building-in-house.html', 'Upcore vs building it in-house',
     'Build it yourself, <span class="hl">or bring in Upcore?</span>',
     'Your platform team could build an AI-native delivery process. What that involves, when it is the right call, and where an outside team saves time.',
     S2, F2, 'Build an AI-Native Delivery Process In-House or with Upcore? | Upcore',
     'What it takes to build an AI-native engineering process in-house, when that is the right call, and when bringing in Upcore saves time. An honest comparison.',
     ('AI-native engineering vs AI coding tools', C.URL['cmp-tools']))]

for key, fname, crumb, h1, lead, secs, faqs, title, meta, other in PAGES:
    aside = f'<div class="ar-aside-cta"><p class="h-col">Also compare</p><a class="link" href="{other[1]}">{other[0]}</a></div>'
    hero, body, mins = A.page(TRAIL(crumb), 'Comparison', h1, lead, secs, meta_line='<span>Updated October 2026</span>', aside=aside)
    faq = K.faq(faqs, 'Common questions.')
    final = K.final('Measure it on <span class="hl">one team first.</span>',
                    'Book a 45-minute discovery call. We&rsquo;ll review your delivery process and outline a pilot on one team, whether or not we work together.',
                    f'Not ready for a call? <a href="{C.URL["guide-aine"]}">Read the guide to AI-native engineering <span aria-hidden="true">&rarr;</span></a>')
    ld = C.graph(key, A.ld_article(key, crumb, meta, mins, faqs), crumb=crumb)
    print(key, C.write(fname, key, title, meta, '\n'.join([hero, body, faq, final]), active='insights', ld=ld, group='comparison', spine=False, main_cls='is-calm'))
