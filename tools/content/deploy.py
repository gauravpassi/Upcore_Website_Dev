"""Deploy a committed git ref with the Vercel CLI, the way docs/ARCHITECTURE.md section 9 prescribes:
`git archive` the commit into an empty folder (no .git, so Vercel's commit-author check doesn't apply), then
`vercel deploy` from there with the project pinned by VERCEL_ORG_ID / VERCEL_PROJECT_ID.

    python tools/content/deploy.py preview [REF]                 # REF (default HEAD) -> a preview URL on upcore-website-dev
    python tools/content/deploy.py production --confirm-production  # main -> www.upcoretech.com

Production refuses unless: REF is main, the working tree is clean, local main equals origin/main (pushed first),
and --confirm-production is passed. It prints the commits that production has not seen yet (since the last
production deploy recorded in tools/content/deploys.log) so a human can see exactly what goes live.
Needs the Vercel CLI logged in to the gauravpassis-projects team (vercel whoami)."""
import datetime, os, re, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ORG = 'team_u6ZGrna1j8I7c2K3KAHWZiTr'
PROJECTS = {'preview': 'prj_KEIUvNDdxLISCUV9dgz4PsDVGpuC',      # upcore-website-dev
            'production': 'prj_jZXe1p8PuDNEaicVWNWRnUrE5uTa'}   # upcore-ai-workforces = www.upcoretech.com
LOG = os.path.join(ROOT, 'tools', 'content', 'deploys.log')


def git(*args):
    r = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit(f'git {" ".join(args)} failed: {r.stderr.strip()}')
    return r.stdout.strip()


def last_production_sha():
    if not os.path.exists(LOG):
        return None
    shas = [line.split()[2] for line in open(LOG, encoding='utf-8') if line.split()[1:2] == ['production']]
    return shas[-1] if shas else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args or args[0] not in PROJECTS:
        sys.exit(__doc__)
    target = args[0]
    ref = args[1] if len(args) > 1 else ('main' if target == 'production' else 'HEAD')
    sha = git('rev-parse', ref)

    if target == 'production':
        if ref != 'main':
            sys.exit('production deploys only from main')
        if git('status', '--porcelain', '--untracked-files=no'):
            sys.exit('working tree has uncommitted changes; commit or discard them first')
        git('fetch', '--quiet', 'origin', 'main')
        if git('rev-parse', 'origin/main') != sha:
            sys.exit('local main is not what origin/main has; push main to origin first')
        since = last_production_sha()
        span = f'{since}..{sha}' if since else f'-15 {sha}'
        print('Commits going live' + ('' if since else ' (no previous deploy logged; showing the last 15)') + ':')
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
    print(url if target == 'preview' else f'{url}\nLive at https://www.upcoretech.com (aliases update within a minute).')


if __name__ == '__main__':
    main()
