"""Long-form article layout for the calm guide and comparison pages (2026-10-07):
page hero -> two-column body (sticky contents list that tracks the section being read, article column)
-> FAQ -> CTA, plus a reading-progress line. Styles .ar-*, script "Articles" in js/upcore-v5.js."""
import re
import chrome as C
import calm as K


def words(html):
    return len(re.sub(r'<[^>]+>', ' ', html).split())


def page(trail, eyebrow, h1, lead, sections, meta_line='', aside='', extra='', show_time=True):
    """sections: [(id, h2, html)]; an empty h2 renders an untitled intro. Returns (hero_html, body_html, minutes)."""
    body_words = sum(words(h) for _, _, h in sections)
    mins = max(3, round(body_words / 230))
    toc = ''.join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", h)}</a></li>' for i, h, _ in sections if h)
    secs = ''.join((f'<section class="ar-sec" id="{i}" aria-labelledby="{i}-h"><h2 id="{i}-h" class="ar-h2">{h}</h2>{b}</section>' if h
                    else f'<section class="ar-sec ar-intro" id="{i}" aria-label="Introduction">{b}</section>') for i, h, b in sections)
    meta = f'<p class="ar-meta" data-reveal style="--d:4">{f"<span>{mins} min read</span>" if show_time else ""}{meta_line}</p>'
    hero = K.hero_page(trail, eyebrow, h1, lead, extra=extra + meta, cls='h-hero--article')
    body = f'''<div class="ar-progress" aria-hidden="true"><i></i></div>
<section class="h-sec ar-wrap" aria-label="Article"><div class="wrap ar-grid">
<aside class="ar-side"><nav class="ar-toc" aria-label="On this page" data-toc><p class="h-col">On this page</p><ol>{toc}</ol></nav>{aside}</aside>
<article class="ar-body" data-article>{secs}</article>
</div></section>'''
    return hero, body, mins


def callout(label, html):
    return f'<div class="ar-call"><p class="ar-call-k">{label}</p>{html}</div>'


def table(cols, rows, label, us=None):
    """cols: header labels (first is the row-header column); rows: [(key, v1, v2, ...)]; us: index of the highlighted column (1-based)."""
    head = '<div class="cmp-row cmp-head" role="row"><div role="columnheader"><span class="sr">' + cols[0] + '</span></div>' + ''.join(
        f'<div class="cmp-c{" is-us" if us == j else ""}" role="columnheader">{c}</div>' for j, c in enumerate(cols[1:], 1)) + '</div>'
    body = ''.join(f'<div class="cmp-row" role="row"><div class="cmp-k" role="rowheader">{r[0]}</div>'
                   + ''.join(f'<div class="cmp-c{" is-us" if us == j else ""}" role="cell"><span class="cmp-l">{cols[j]}</span>{v}</div>' for j, v in enumerate(r[1:], 1)) + '</div>'
                   for r in rows)
    n = len(cols) - 1
    return f'<div class="cmp ar-cmp ar-cmp--{n}" role="table" aria-label="{label}">{head}{body}</div>'


def ld_article(key, headline, desc, mins, faq=None, published='2026-10-07'):
    node = {'@type': 'Article', 'headline': headline, 'description': desc, 'url': C.SITE + C.FINAL_URL[key],
            'datePublished': published or '2026-10-07', 'dateModified': '2026-10-07', 'inLanguage': 'en',
            'author': {'@id': C.ORG_ID}, 'publisher': {'@id': C.ORG_ID}, 'timeRequired': f'PT{mins}M',
            'image': C.OG_IMAGE, 'mainEntityOfPage': C.SITE + C.FINAL_URL[key]}
    return [node] + ([K.faq_ld(faq)] if faq else [])
