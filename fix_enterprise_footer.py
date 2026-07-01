"""
Enterprise footer quality pass — all 65 pages:
1. Fix var(--txt) / var(--txt2) / var(--txt3) leaking into dark footer CSS
2. Make social buttons circular (border-radius:50%)
3. Replace duplicate italic tagline in footer-bottom with certification strip
"""
import glob, re

files = [f for f in glob.glob('**/*.html', recursive=True) if 'demos' not in f]
updated = []

for f in sorted(files):
    content = orig = open(f, encoding='utf-8').read()

    # ── 1. footer-review-btn: color:var(--txt) → white ───────────────────────
    # Single-line format (compare/, industries/ unique)
    content = content.replace(
        '.footer-review-btn:hover{color:var(--txt);',
        '.footer-review-btn:hover{color:rgba(255,255,255,.85);'
    )
    # Multi-line format (index.html, ai-engineering-governance.html)
    content = re.sub(
        r'(\.footer-review-btn:hover\s*\{[^}]*)color:\s*var\(--txt\)',
        r'\1color:rgba(255,255,255,.85)',
        content, flags=re.DOTALL
    )

    # ── 2. footer-review-btn: color:var(--txt3) → white-alpha ────────────────
    # Single-line (compare/, industries/ unique, learn/)
    content = re.sub(
        r'(\.footer-review-btn\{[^}]*);color:var\(--txt3\)',
        r'\1;color:rgba(255,255,255,.45)',
        content
    )

    # ── 3. footer-soc-btn: color:var(--txt2) → white-alpha ───────────────────
    # Single-line format
    content = re.sub(
        r'(\.footer-soc-btn\{[^}]*);color:var\(--txt2\)',
        r'\1;color:rgba(255,255,255,.55)',
        content
    )
    # Multi-line format (index.html)
    content = re.sub(
        r'(\.footer-soc-btn\s*\{[^}]*)color:\s*var\(--txt2\)',
        r'\1color:rgba(255,255,255,.55)',
        content, flags=re.DOTALL
    )

    # ── 4. footer-soc-btn: circular (border-radius → 50%) ────────────────────
    # Single-line 10px
    content = re.sub(
        r'(\.footer-soc-btn\{[^}]*);border-radius:10px',
        r'\1;border-radius:50%',
        content
    )
    # Single-line 8px (some template variants)
    content = re.sub(
        r'(\.footer-soc-btn\{[^}]*);border-radius:8px',
        r'\1;border-radius:50%',
        content
    )
    # Multi-line format (index.html)
    content = re.sub(
        r'(\.footer-soc-btn\s*\{[^}]*)border-radius:\s*8px',
        r'\1border-radius:50%',
        content, flags=re.DOTALL
    )

    # ── 5. footer-links on special pages: var(--txt3) → white-alpha ──────────
    # about.html, contact.html have .footer-links a{...color:var(--txt3);}
    content = re.sub(
        r'(\.footer-links\s+a\{[^}]*)color:var\(--txt3\)',
        r'\1color:rgba(255,255,255,.52)',
        content
    )

    # ── 6. Replace italic tagline in footer-bottom with certifications ─────────
    # Old: <span class="footer-copy" style="font-style:italic;color:var(--txt3);">Govern Your AI. Then Build With It.</span>
    content = content.replace(
        '<span class="footer-copy" style="font-style:italic;color:var(--txt3);">Govern Your AI. Then Build With It.</span>',
        '<span class="footer-copy" style="color:rgba(255,255,255,.2);letter-spacing:.3px;">CMMI Level&nbsp;3 &nbsp;&middot;&nbsp; ISO&nbsp;27001 &nbsp;&middot;&nbsp; ISO&nbsp;9001</span>'
    )

    if content != orig:
        open(f, 'w', encoding='utf-8').write(content)
        updated.append(f)

print(f'Updated {len(updated)} files')
for f in updated:
    print(f'  {f}')

# ── Verification ──────────────────────────────────────────────────────────────
print()
print('Verification:')
remaining = []
for f in files:
    content = open(f, encoding='utf-8').read()
    lines = content.split('\n')
    for i, line in enumerate(lines):
        in_footer = any(cls in line for cls in [
            'footer-soc-btn', 'footer-review-btn', 'footer-links', 'footer-tagline', 'footer-copy'
        ])
        if in_footer and ('var(--txt)' in line or 'var(--txt2)' in line or 'var(--txt3)' in line):
            remaining.append(f'{f}:{i+1}: {line.strip()[:80]}')

if not remaining:
    print('  ALL CLEAR — no dark text tokens in footer CSS')
else:
    print(f'  {len(remaining)} remaining issues:')
    for r in remaining[:20]:
        print(f'    {r}')
