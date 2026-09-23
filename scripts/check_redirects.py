#!/usr/bin/env python3
"""Verify the redirect map is in step with the inventory and the built site.

Two modes, because the site is built over several phases:

  default   the redirect map must match the inventory exactly, and every target
            that HAS been built must resolve. Targets not yet written are
            reported as remaining work, not failures.
  --strict  every inventory target must resolve. Required before cut-over
            (phase 4): this is the check that proves no old URL starts 404ing.
"""
import argparse, csv, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'public'


def exists(target):
    rel = target.strip('/')
    return (PUBLIC / rel / 'index.html').exists() if rel else (PUBLIC / 'index.html').exists()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strict', action='store_true',
                    help='require every inventory target to resolve (cut-over gate)')
    args = ap.parse_args()

    if not PUBLIC.exists():
        sys.exit('public/ not built; run hugo first')

    rows = list(csv.DictReader((ROOT / 'migration' / 'inventory.csv').open()))
    shim = ROOT / 'static' / 'redirects.json'
    if not shim.exists():
        sys.exit('static/redirects.json missing; run scripts/build_redirects.py')
    rules = json.loads(shim.read_text())

    problems, pending = [], []

    # The map must always agree with the inventory, in both directions.
    expected = {}
    for r in rows:
        if not r['target_path'] or '?' not in r['old_url']:
            continue
        q = r['old_url'].split('?', 1)[1]
        expected[q] = r['target_path']
    for k, v in expected.items():
        if k not in rules:
            problems.append(f'inventory has {k} -> {v}, redirects.json does not')
        elif rules[k] != v:
            problems.append(f'{k}: inventory says {v}, redirects.json says {rules[k]}')
    for k in rules:
        if k not in expected:
            problems.append(f'redirects.json has stale rule {k}')

    targets = sorted({r['target_path'] for r in rows if r['target_path']})
    for t in targets:
        if not exists(t):
            (problems if args.strict else pending).append(t)

    if problems:
        print(f'{len(problems)} problem(s):', file=sys.stderr)
        for p in problems:
            print(f'  {p}', file=sys.stderr)
        sys.exit(1)

    built = len(targets) - len(pending)
    print(f'redirect map matches inventory: {len(rules)} rules')
    print(f'targets built: {built}/{len(targets)}')
    if pending:
        print(f'remaining to write ({len(pending)}): ' + ', '.join(pending[:6])
              + (' ...' if len(pending) > 6 else ''))
        print('(use --strict before cut-over: then these become failures)')


if __name__ == '__main__':
    main()
