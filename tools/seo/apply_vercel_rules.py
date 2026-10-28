"""Adds the 2026-10-28 SEO rules to vercel.json (idempotent; re-run after editing legacy-redirects.json):
1. www.upcoretech.com's Vercel alias upcore-ai-workforces.vercel.app 308s to www (it was indexed as a duplicate site).
2. Every other *.vercel.app host (the upcore-website-dev project and preview deployments) sends X-Robots-Tag: noindex.
   The same vercel.json is deployed to both projects, so the redirect must name the exact production alias.
3. /css/* and /js/* (always requested with a ?v= cache-buster) are cached for 7 days instead of 1 hour.
4. Legacy WordPress URLs from tools/seo/legacy-redirects.json are 301'd to their closest current page.
Run from the repo root: python tools/seo/apply_vercel_rules.py"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
VJ = os.path.join(ROOT, 'vercel.json')
LEGACY = os.path.join(ROOT, 'tools', 'seo', 'legacy-redirects.json')
PROD_ALIAS = 'upcore-ai-workforces.vercel.app'

v = json.load(open(VJ, encoding='utf-8'))

host_redirect = {'source': '/:path*', 'has': [{'type': 'host', 'value': PROD_ALIAS}],
                 'destination': 'https://www.upcoretech.com/:path*', 'permanent': True}
v['redirects'] = [r for r in v['redirects'] if r.get('has') != host_redirect['has']]
v['redirects'].insert(0, host_redirect)

if os.path.exists(LEGACY):
    known = {r['source'] for r in v['redirects']}
    for r in json.load(open(LEGACY, encoding='utf-8'))['redirects']:
        if r['source'] not in known:
            v['redirects'].append({'source': r['source'], 'destination': r['destination'], 'permanent': True})
            known.add(r['source'])

noindex = {'source': '/(.*)', 'has': [{'type': 'host', 'value': '(?<host>.+)\\.vercel\\.app'}],
           'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex'}]}
assets = {'source': '/(css|js)/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=604800, stale-while-revalidate=86400'}]}
v['headers'] = [h for h in v['headers'] if h not in (assets, noindex)] + [assets, noindex]

with open(VJ, 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(v, indent=2, ensure_ascii=False) + '\n')
print(f'vercel.json: {len(v["redirects"])} redirects, {len(v["headers"])} header rules')
