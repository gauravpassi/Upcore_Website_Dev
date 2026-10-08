"""Rebuild every generated page. Run after changing chrome.py, the cache-buster V, or shared parts.
Also refreshes the content library (content/*.json), the two booking pages and the site chrome on the
two quiz landing pages (lp_chrome.py). Run from the repo root: python tools/v4-build/build_all.py"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDERS = ['build_home.py', 'build_aine.py', 'build_gov.py', 'build_bpa.py', 'build_fao.py', 'build_fde.py', 'segments.py',
            'build_results.py', 'build_about.py', 'build_security.py', 'build_contact.py', 'build_booking.py', 'build_404.py',
            'build_guide.py', 'build_compare.py', 'build_library.py', 'build_insights.py', 'lp_chrome.py']

env = dict(os.environ, PYTHONIOENCODING='utf-8')
failed = []
for b in BUILDERS:
    r = subprocess.run([sys.executable, os.path.join(HERE, b)], env=env, capture_output=True, text=True, encoding='utf-8')
    print(f'{b:22} {"ok" if r.returncode == 0 else "FAILED"}  {r.stdout.strip().replace(chr(10), " | ")}')
    if r.returncode:
        failed.append(b)
        print(r.stderr)
sys.exit(1 if failed else 0)
