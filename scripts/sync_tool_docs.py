#!/usr/bin/env python3
"""Flag tool pages that may be out of date with their repository.

For each tool in data/tools.yml, compares the page's `last_reviewed` with the
repository's most recent push and latest release. It does not read the page or
the README: it only says which pages are worth a human look, which is what the
design document asks for. Nothing is copied from a repository into a page.

Network access is required. Without it, the script says so and exits 0, so it
never fails a build for being offline.
"""
import argparse, datetime, json, pathlib, re, sys, urllib.error, urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = 'https://api.github.com/repos/'


def gh(path):
    req = urllib.request.Request(API + path,
                                 headers={'Accept': 'application/vnd.github+json',
                                          'User-Agent': 'repeatexplorer-site/1.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def last_reviewed(slug):
    p = ROOT / 'content' / 'tools' / slug / 'index.md'
    if not p.exists():
        return None
    m = re.search(r'^last_reviewed:\s*(\d{4}-\d{2}-\d{2})', p.read_text(), re.M)
    return datetime.date.fromisoformat(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quiet', action='store_true', help='print only pages needing review')
    args = ap.parse_args()

    tools = yaml.safe_load((ROOT / 'data' / 'tools.yml').read_text())
    stale, checked = [], 0

    for key, tool in tools.items():
        slug = key.replace('_', '-')
        repo = tool['repo'].replace('https://github.com/', '').rstrip('/')
        reviewed = last_reviewed(slug)
        try:
            meta = gh(repo)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f'cannot reach GitHub ({e}); nothing checked', file=sys.stderr)
            return 0
        except urllib.error.HTTPError as e:
            print(f'  {key}: repo {repo} returned HTTP {e.code}')
            continue
        checked += 1
        pushed = datetime.date.fromisoformat(meta['pushed_at'][:10])
        try:
            rel = gh(f'{repo}/releases/latest')
            release = f"{rel['tag_name']} ({rel['published_at'][:10]})"
            rel_date = datetime.date.fromisoformat(rel['published_at'][:10])
        except Exception:
            release, rel_date = '-', None

        newer = reviewed is None or pushed > reviewed or (rel_date and rel_date > reviewed)
        if newer:
            stale.append(key)
        if newer or not args.quiet:
            mark = 'REVIEW' if newer else 'ok'
            print(f'  {mark:6s} {key:16s} reviewed {reviewed or "never"}  '
                  f'pushed {pushed}  release {release}')

    print(f'\n{checked} tools checked, {len(stale)} worth a look: {", ".join(stale) or "none"}')
    print('A newer push does not mean the page is wrong. The page describes what '
          'the tool is for, which changes far less often than the code.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
