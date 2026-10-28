"""Deploy a committed git ref with the Vercel CLI, the way docs/ARCHITECTURE.md section 9 prescribes:
`git archive` the commit into an empty folder (no .git, so Vercel's commit-author check doesn't apply), then
`vercel deploy` from there with the project pinned by VERCEL_ORG_ID / VERCEL_PROJECT_ID.

    python tools/content/deploy.py preview [REF]                    # REF (default HEAD) -> a preview URL on upcore-website-dev
    python tools/content/deploy.py production --confirm-production  # origin/main -> www.upcoretech.com

Production always deploys exactly what GitHub's main holds (it fetches origin and archives origin/main), so
whatever goes live is pushed first. Without --confirm-production it only prints the commits production has not
seen yet (since the last production deploy recorded in tools/content/deploys.log) so a human can check the list.
Needs the Vercel CLI logged in to the gauravpassis-projects team (vercel whoami)."""
import datetime, os, re, shutil, subprocess, sys, tempfile, urllib.error, urllib.request, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ORG = 'team_u6ZGrna1j8I7c2K3KAHWZiTr'
PROJECTS = {'preview': 'prj_KEIUvNDdxLISCUV9dgz4PsDVGpuC',      # upcore-website-dev
            'production': 'prj_jZXe1p8PuDNEaicVWNWRnUrE5uTa'}   # upcore-ai-workforces = www.upcoretech.com
LOG = os.path.join(ROOT, 'tools', 'content', 'deploys.log')
SITE = 'https://www.upcoretech.com'


def git(*args):
    r = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit(f'git {" ".join(args)} failed: {r.stderr.strip()}')
    return r.stdout.strip()


def last_production_sha():
    """The commit www.upcoretech.com is serving: /build-id.txt (written into every deploy since 2026-10-28),
    else the last production deploy in this checkout's deploys.log, else None."""
    try:
        live = urllib.request.urlopen(SITE + '/build-id.txt', timeout=15).read().decode().strip()
        if re.fullmatch(r'[0-9a-f]{40}', live) and subprocess.run(['git', 'cat-file', '-e', live], cwd=ROOT).returncode == 0:
            return live
    except Exception:  # noqa: BLE001 (older deploys have no build-id.txt)
        pass
    if not os.path.exists(LOG):
        return None
    shas = [line.split()[2] for line in open(LOG, encoding='utf-8') if line.split()[1:2] == ['production']]
    return shas[-1] if shas else None


def probe(url):
    """Preview deployments of upcore-website-dev sit behind Vercel Authentication; say so instead of 'it works'."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    try:
        r = urllib.request.build_opener(NoRedirect).open(url, timeout=30)
        return f'loads (HTTP {r.status})'
    except urllib.error.HTTPError as e:
        loc = e.headers.get('Location', '')
        if e.code in (301, 302, 303, 307, 308) and 'vercel.com' in loc:
            return 'protected by Vercel Authentication: open it while signed in to vercel.com with access to the gauravpassis-projects team'
        return f'HTTP {e.code}'
    except Exception as e:  # noqa: BLE001
        return f'could not check ({e})'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args or args[0] not in PROJECTS:
        sys.exit(__doc__)
    target = args[0]
    if target == 'production':
        if len(args) > 1:
            sys.exit('production always deploys origin/main; push what should go live, then run without a ref')
        git('fetch', '--quiet', 'origin', 'main')
        ref = 'origin/main'
    else:
        ref = args[1] if len(args) > 1 else 'HEAD'
    sha = git('rev-parse', ref)

    if target == 'production':
        since = last_production_sha()
        span = f'{since}..{sha}' if since else f'-15 {sha}'
        print('Commits going live' + (f' (live is {since[:7]})' if since else ' (live commit unknown; showing the last 15)') + ':')
        print(git('log', '--oneline', *span.split()) or '  (none)')
        if '--confirm-production' not in sys.argv:
            sys.exit('\nNot deployed. Re-run with --confirm-production once a human has approved the list above.')

    vercel = shutil.which('vercel')
    if not vercel:
        sys.exit('Vercel CLI not found (npm install -g vercel, then vercel login)')
    tmp = tempfile.mkdtemp(prefix=f'upcore-{target}-')
    try:
        archive = os.path.join(tmp, 'src.zip')
        git('archive', '--format=zip', '-o', archive, sha)
        out = os.path.join(tmp, 'site')
        zipfile.ZipFile(archive).extractall(out)
        with open(os.path.join(out, 'build-id.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(sha + '\n')  # served at /build-id.txt so the next production deploy knows what is live
        env = dict(os.environ, VERCEL_ORG_ID=ORG, VERCEL_PROJECT_ID=PROJECTS[target])
        cmd = [vercel, 'deploy', '--yes', '--cwd', out] + (['--prod'] if target == 'production' else [])
        print(f'Deploying {ref} ({sha[:7]}) to {target}...')
        r = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding='utf-8')
        urls = re.findall(r'https://[^\s]+\.vercel\.app', r.stdout + r.stderr)
        if r.returncode or not urls:
            sys.exit(f'vercel deploy failed (exit {r.returncode}):\n{r.stdout}\n{r.stderr}')
        url = urls[-1]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    stamp = datetime.datetime.now().isoformat(timespec='seconds')
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write(f'{stamp} {target} {sha} {ref} {url}\n')
    if target == 'preview':
        print(url)
        print('Preview check:', probe(url))
    else:
        print(f'{url}\nLive at {SITE} (aliases update within a minute).')


if __name__ == '__main__':
    main()
