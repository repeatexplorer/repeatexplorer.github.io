#!/usr/bin/env python3
"""Schema-check data/*.yml and the front matter that references it.

Catches the failure modes that a Hugo build alone does not: a tool entry with a
missing repo URL, a `cite` key with no publication, a tool page whose `tool:`
names nothing, a protocol whose `last_tested` is unparseable.
"""
import datetime, json, pathlib, re, sys
import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


def load_yaml(path):
    if not path.exists():
        err(path.name, 'missing')
        return {}
    return yaml.safe_load(path.read_text()) or {}


def front_matter(path):
    text = path.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        err(path.relative_to(ROOT), 'no YAML front matter')
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(path.relative_to(ROOT), f'unparseable front matter: {e}')
        return {}


def check_schema(data, schema_path, label):
    schema = json.loads(schema_path.read_text())
    for e in sorted(Draft202012Validator(schema).iter_errors(data), key=str):
        loc = '/'.join(str(p) for p in e.path) or '(root)'
        err(label, f'{loc}: {e.message}')


def main():
    tools = load_yaml(ROOT / 'data' / 'tools.yml')
    pubs = load_yaml(ROOT / 'data' / 'publications.yml') or {}

    check_schema(tools, ROOT / 'schemas' / 'tools.schema.json', 'data/tools.yml')
    check_schema(pubs, ROOT / 'schemas' / 'publications.schema.json', 'data/publications.yml')

    # cross-references inside the data files
    for key, tool in (tools or {}).items():
        for dep in tool.get('depends_on', []):
            if dep not in tools:
                err('data/tools.yml', f'{key}.depends_on: {dep!r} is not a tool key')
        for c in tool.get('cite', []):
            if c not in pubs:
                err('data/tools.yml', f'{key}.cite: {c!r} is not in publications.yml')
        # the index lists tool pages, so a tool without one is invisible
        slug = key.replace('_', '-')
        if not (ROOT / 'content' / 'tools' / slug / 'index.md').exists():
            err('data/tools.yml', f'{key}: no content/tools/{slug}/index.md, so the '
                                  f'tool will not appear in the tools index')
        for slug in tool.get('protocols', []):
            if not (ROOT / 'content' / 'protocols' / slug).exists():
                err('data/tools.yml', f'{key}.protocols: no content/protocols/{slug}/')

    # front matter
    for md in (ROOT / 'content').rglob('*.md'):
        rel = md.relative_to(ROOT)
        fm = front_matter(md)
        if not fm:
            continue
        if not fm.get('title'):
            err(rel, 'missing title')
        for a in fm.get('aliases', []):
            if '?' in a:
                err(rel, f'alias {a!r} contains a query string; path aliases '
                         f'cannot match one. Use migration/inventory.csv instead.')
        if 'tools/' in str(rel) and md.name == 'index.md':
            t = fm.get('tool')
            if not t:
                err(rel, 'tool page has no `tool:` key')
            elif t not in tools:
                err(rel, f'tool: {t!r} is not in data/tools.yml')
        for field in ('last_tested', 'last_reviewed'):
            if field in fm and not isinstance(fm[field], (datetime.date, datetime.datetime)):
                err(rel, f'{field} must be a date (YYYY-MM-DD), got {fm[field]!r}')
        if 'workshops/' in str(rel) and fm.get('year') is not None:
            if not isinstance(fm['year'], int):
                err(rel, f'year must be an integer, got {fm["year"]!r}')
            # A workshop year page must be a branch bundle so it can carry
            # subpages (venue/, presentations/). A leaf bundle silently turns
            # its children into resources: they build, but no page is rendered.
            if md.name != '_index.md':
                err(rel, 'workshop year pages must be _index.md (branch bundle), '
                         'not index.md, or subpages will not be rendered')
            if fm.get('layout') != 'workshop':
                err(rel, 'workshop year pages need `layout: workshop`, otherwise '
                         'Hugo renders them with the section index template')
            # past/upcoming is derived from end_date, never from a manual flag,
            # so a finished workshop cannot be left advertised as forthcoming.
            for f in ('start_date', 'end_date'):
                v = fm.get(f)
                if v is None:
                    err(rel, f'workshop year pages need {f} (YYYY-MM-DD); '
                             f'the index derives past/upcoming from end_date')
                elif not isinstance(v, (datetime.date, datetime.datetime)):
                    err(rel, f'{f} must be a date, got {v!r}')
            s_, e_ = fm.get('start_date'), fm.get('end_date')
            if isinstance(s_, datetime.date) and isinstance(e_, datetime.date):
                if e_ < s_:
                    err(rel, f'end_date {e_} precedes start_date {s_}')
                if s_.year != fm['year']:
                    err(rel, f'start_date {s_} does not fall in year {fm["year"]}')

    if errors:
        print(f'{len(errors)} problem(s):', file=sys.stderr)
        for e in errors:
            print(f'  {e}', file=sys.stderr)
        sys.exit(1)
    print('data and front matter OK')


if __name__ == '__main__':
    main()
