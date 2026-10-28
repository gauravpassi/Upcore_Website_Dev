"""Bylines for library articles (2026-10-28). Content JSON names people by slug in "author" and "reviewer";
an empty value means the article is credited to Upcore (the Organization). Only people who have agreed to be
named may be listed here (decided 2026-10-28: Saswata Sengupta; the leadership on /about is not named on
articles). A byline reads "By <name>, Upcore Technologies" and links to /about; the Article JSON-LD carries a
Person node with the same @id on every article."""
import chrome as C

PEOPLE = {
    'saswata-sengupta': {'name': 'Saswata Sengupta', 'role': '', 'sameAs': ''},
}
AFFILIATION = 'Upcore Technologies'


def person_id(slug):
    return C.SITE + '/#person-' + slug


def person(slug):
    """Article JSON-LD Person node; a KeyError here means the JSON names someone not in PEOPLE."""
    p = PEOPLE[slug]
    node = {'@type': 'Person', '@id': person_id(slug), 'name': p['name'], 'url': C.SITE + '/about', 'worksFor': {'@id': C.ORG_ID}}
    if p.get('role'):
        node['jobTitle'] = p['role']
    if p.get('sameAs'):
        node['sameAs'] = [p['sameAs']]
    return node


def link(slug):
    return f'<a href="/about">{PEOPLE[slug]["name"]}</a>, {AFFILIATION}'
