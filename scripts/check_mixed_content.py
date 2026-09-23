#!/usr/bin/env python3
"""Fail on http:// links in the built site.

The old site was http-only and its text is full of http:// URLs; any that
survive conversion become mixed content or dead links on an https site.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'public'
# http:// is legitimate inside these: XML namespaces and schema identifiers.
ALLOW = re.compile(r'http://(www\.w3\.org|purl\.org|schema\.org|wordpress\.org|'
                   r'localhost|127\.0\.0\.1)')

def main():
    hits = []
    for f in PUBLIC.rglob('*.html'):
        for n, line in enumerate(f.read_text(errors='replace').splitlines(), 1):
            for m in re.finditer(r'http://[^\s"\'<>)]+', line):
                if not ALLOW.match(m.group()):
                    hits.append(f'{f.relative_to(PUBLIC)}:{n}: {m.group()[:90]}')
    if hits:
        print(f'{len(hits)} insecure link(s):', file=sys.stderr)
        for h in hits[:40]:
            print(f'  {h}', file=sys.stderr)
        sys.exit(1)
    print('no http:// links in output')

if __name__ == '__main__':
    main()
