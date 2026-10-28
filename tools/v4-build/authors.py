"""Bylines for library articles (2026-10-28). Content JSON names people by slug in "author" and "reviewer";
an empty value means the article is credited to Upcore (the Organization). The slugs are the /about anchors
(build_about.py TEAM gives each leadership entry id="<slug>" and the same Person @id), so a byline links to
/about#<slug> and the Article JSON-LD carries a full Person node with the same @id."""
import chrome as C

PEOPLE = {
    'gaurav-passi': {'name': 'Gaurav Passi', 'role': 'Co-Founder & CEO, Claude Certified Architect', 'sameAs': 'https://linkedin.com/in/gauravusa'},
    'shrikant-maniar': {'name': 'Shrikant Maniar', 'role': 'Executive Director', 'sameAs': 'https://www.linkedin.com/in/shrikantmaniar/'},
    'shanker-dhand': {'name': 'Shanker Dhand', 'role': 'Technical Head', 'sameAs': 'https://www.linkedin.com/in/shankerdhand/'},
}


def person_id(slug):
    return C.SITE + '/about#' + slug


def person(slug):
    """Article JSON-LD Person node; a KeyError here means the JSON names someone not in PEOPLE."""
    p = PEOPLE[slug]
    return {'@type': 'Person', '@id': person_id(slug), 'name': p['name'], 'jobTitle': p['role'],
            'url': C.SITE + '/about#' + slug, 'sameAs': [p['sameAs']], 'worksFor': {'@id': C.ORG_ID}}


def link(slug):
    return f'<a href="/about#{slug}">{PEOPLE[slug]["name"]}</a>'
