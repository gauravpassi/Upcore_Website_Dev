"""V5 "Flow" components: open, box-free layouts with motion hooks for js/upcore-v5.js.
Every builder returns plain HTML. Content stays in the DOM (accessible, no-JS readable);
the motion layer only adds behaviour on top."""
import html as H
import json

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def _strip(s):
    return H.unescape(s).replace('←', '<-')


# ------------------------------------------------------------------ hero flowline
def flowline(steps, tickets, title, aria, branch_label='Held for a person', end_label='Released'):
    """steps: [(title, sub, human_bool)]; tickets: [dict(id, title, branch(bool), risk lo|md|hi, out)].
    Rendered by JS as an SVG pipeline the tickets travel along; the <ol> is the accessible fallback."""
    data = {
        'steps': [{'t': _strip(t), 'e': _strip(e), 'h': bool(h)} for t, e, h in steps],
        'tickets': [{'id': t['id'], 'title': _strip(t['title']), 'branch': bool(t.get('branch')), 'risk': t.get('risk', 'lo'), 'out': _strip(t['out'])} for t in tickets],
        'branchLabel': _strip(branch_label), 'endLabel': _strip(end_label),
    }
    items = ''.join(f'<li>{t}<span> &middot; {e}</span>{" (a person decides)" if h else ""}</li>' for t, e, h in steps)
    log = ''.join(f'<li class="r-{t.get("risk", "lo")}"><code>{t["id"]}</code><span>{t["title"]}</span><em>{t["out"]}</em></li>' for t in tickets)
    return f'''<div class="fl" data-flowline='{H.escape(json.dumps(data), quote=True)}'>
<div class="fl-bar wrap"><span class="fl-title"><i class="fl-live" aria-hidden="true"></i>{title} <span>&middot; example run</span></span><button class="fl-toggle run-toggle" type="button" aria-label="Pause animation">Pause</button></div>
<figure class="fl-stage" role="img" aria-label="{H.escape(_strip(aria), quote=True)}"><ol class="fl-fallback">{items}</ol></figure>
<div class="wrap"><ol class="fl-log" aria-hidden="true">{log}</ol></div></div>'''


# ------------------------------------------------------------------ marquee
def marquee(inner_html, dur=48, reverse=False, cls=''):
    """Seamless loop: the content is rendered twice; the second copy is hidden from assistive tech."""
    dup = inner_html.replace('<a ', '<a tabindex="-1" ')
    return (f'<div class="mq{(" " + cls) if cls else ""}" data-marquee style="--dur:{dur}s"{" data-dir=rev" if reverse else ""}>'
            f'<div class="mq-track"><div class="mq-set">{inner_html}</div><div class="mq-set" aria-hidden="true">{dup}</div></div></div>')


# ------------------------------------------------------------------ strike lanes (before -> after)
def strike(rows, c1, c2):
    """rows: [(label, before, after)]. The 'before' text is struck through as the row enters view,
    then the 'after' text writes in beneath it."""
    out = ''.join(
        f'<li class="sk-row" data-reveal style="--d:{i % 2}"><span class="sk-k">{k}</span>'
        f'<p class="sk-was"><span class="sr">{c1}: </span>{a}</p><p class="sk-now"><span class="sr">{c2}: </span>{b}</p></li>'
        for i, (k, a, b) in enumerate(rows))
    return f'<div class="sk"><div class="sk-legend" aria-hidden="true"><span class="was">{c1}</span><span class="now">{c2}</span></div><ol class="sk-list">{out}</ol></div>'


# ------------------------------------------------------------------ timeline (engagement path)
def timeline(steps, start=1):
    """steps: [(title, text)] drawn as nodes on one line; the first node is the entry point."""
    n = len(steps)
    li = ''.join(
        f'<li class="tl-step{" is-first" if i == 0 else ""}" style="--i:{i}"><span class="tl-node" aria-hidden="true"></span>'
        f'<span class="tl-k">Step {i + start:02d}</span><h3 class="t-h3">{t}</h3><p>{p}</p></li>'
        for i, (t, p) in enumerate(steps))
    return f'<div class="tl" data-reveal style="--n:{n}"><span class="tl-line" aria-hidden="true"><i></i></span><ol>{li}</ol></div>'


# ------------------------------------------------------------------ index rows
def index_rows(items, cls=''):
    """items: [dict(href, k, title, text, more, extra)] -> large typographic rows with a hover sweep."""
    rows = ''
    for i, it in enumerate(items):
        tag = 'a' if it.get('href') else 'div'
        href = f' href="{it["href"]}"' if it.get('href') else ''
        extra = it.get('extra', '')
        more = f'<span class="ix-go">{it["more"]} {ARROW}</span>' if it.get('more') else ''
        rows += (f'<li data-reveal style="--d:{i % 4}"><{tag} class="ix-row"{href}><span class="ix-n">{i + 1:02d}</span>'
                 f'<span class="ix-k">{it.get("k", "")}</span><span class="ix-t">{it["title"]}</span>'
                 f'<span class="ix-p">{it.get("text", "")}{extra}</span>{more}</{tag}></li>')
    return f'<ol class="ix{(" " + cls) if cls else ""}">{rows}</ol>'


# ------------------------------------------------------------------ outcome rows (workflows)
def outcome_rows(items):
    """items: [(title, text, outcome)] -> numbered rows; the outcome reads as the result column."""
    rows = ''.join(
        f'<li class="oc-row" data-reveal style="--d:{i % 3}"><span class="oc-n">{i + 1:02d}</span><h3 class="t-h3">{t}</h3><p>{p}</p><span class="oc-out">{o}</span></li>'
        for i, (t, p, o) in enumerate(items))
    return f'<ol class="oc">{rows}</ol>'


# ------------------------------------------------------------------ quote carousel
def quote_carousel(quotes, links_html):
    """quotes: [(text, who, source, url)]. All quotes stay in the DOM; JS crossfades between them."""
    items = ''
    for i, (q, w, s, u) in enumerate(quotes):
        src = f' <a href="{u}" target="_blank" rel="noopener">{s}<span class="sr"> (opens in a new tab)</span></a>' if s else ''
        items += (f'<figure class="qc-item{" is-on" if i == 0 else ""}" id="qc-{i}"><blockquote><p>{q}</p></blockquote>'
                  f'<figcaption><span>{w}</span>{src}</figcaption></figure>')
    dots = ''.join(f'<button type="button" class="qc-dot{" is-on" if i == 0 else ""}" aria-controls="qc-{i}" aria-label="Show quote {i + 1} of {len(quotes)}"><i></i></button>' for i in range(len(quotes)))
    return f'<div class="qc" data-quotes><span class="qc-mark" aria-hidden="true">&ldquo;</span><div class="qc-stage">{items}</div><div class="qc-nav">{dots}</div>{links_html}</div>'


# ------------------------------------------------------------------ CTA flow lines
def cta_lines():
    paths = [
        'M-50 120 C 300 60, 520 300, 760 240 S 1180 120, 1500 220',
        'M-50 260 C 260 200, 560 420, 820 330 S 1200 210, 1500 300',
        'M-50 420 C 320 380, 600 520, 860 430 S 1220 330, 1500 400',
        'M-50 560 C 280 520, 620 600, 900 520 S 1240 460, 1500 520',
        'M-50 40 C 340 0, 580 180, 800 150 S 1160 40, 1500 120',
        'M-50 640 C 360 610, 640 660, 940 600 S 1260 560, 1500 620',
    ]
    ps = ''.join(f'<path class="cl cl-{i}" d="{d}"/><path class="cl-run cl-{i}" d="{d}" pathLength="1000"/>' for i, d in enumerate(paths))
    return f'<svg class="cta-lines" viewBox="0 0 1440 680" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{ps}</svg>'
