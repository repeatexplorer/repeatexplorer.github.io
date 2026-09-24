---
name: add-tool
description: Use when adding a tool to the RepeatExplorer website, or changing what an existing tool page says — "add CARP to the site", "put DANTE_TIR on the website", "this tool is now on Galaxy". Covers the data entry, the page bundle and the checks. Not for editing a tool's README, which lives in its own repository.
---

# Adding a tool

A tool is one entry in `data/tools.yml` and one page bundle. The entry drives
the badges, the cards, the index order and the citation; the page carries only
prose. Get the entry right first.

## 1. Gather facts from the repository, not from memory

- **What it does and what it outputs** — the one-line summary in the toolkit
  table at <https://github.com/kavonrtep>, then the README's own Output section.
- **Galaxy availability** — the `galaxy` tag in that toolkit table, confirmed
  against `kavonrtep/galaxy_packages`, which holds the Tool Shed wrappers.
- **Citation** — the README's citation section. A DOI there goes through the
  `add-publication` skill first; never type a reference by hand.

If the README says "TODO: add citation", the tool has no paper. Leave `cite`
empty; the template renders no citation block and that is correct.

## 2. Add the entry

Every field in `schemas/tools.schema.json` is required, so the build fails on a
missing one rather than shipping a half-entry:

```yaml
carp:
  name: CARP
  category: assembly          # must be a key in data/tool_categories.yml
  summary: One line, under 200 characters, no marketing
  repo: https://github.com/kavonrtep/CARP
  galaxy: ["carp"]            # empty list when not on the server
  cli: true                   # false for data, or for a Galaxy-only tool
  annotates: [ltr, tandem]    # keys in data/repeat_classes.yml
  inputs: [genome assembly]
  depends_on: [dante]         # other keys in tools.yml
  protocols: []               # slugs under content/protocols/
  cite: []                    # keys in data/publications.yml
  status: active
```

`annotates` decides the class badges. If the tool does not fit the existing
vocabulary, do not invent a colour: add the class to `data/repeat_classes.yml`
**and** a `--class-<name>` custom property in `assets/css/site.css`, or use
`protein_domains` / `reference` / `all_repeats`.

## 3. Add the page

`content/tools/<key with underscores as hyphens>/index.md`:

```markdown
---
title: CARP
tool: carp
weight: 80        # decides position in the index; leave gaps of 10
last_reviewed: 2026-09-24
---

One or two paragraphs: what it does, and what it is for.

## Output

- One bullet per artefact, naming the format
```

A tool with an entry but no page **disappears from both the home page and
`/tools/`** without any error, because both build their cards from pages.
`validate_data.py` fails on this, which is the only reason it is caught.

Keep the page short. No command lines, no parameters, no installation, no
version numbers: the box already links the repository for that, and a page
without versions does not go stale when the tool is released.

## 4. Check

    make check

That validates the schema, the cross-references and the links, and rebuilds.
Then look at `/tools/` and the tool's own page before committing.
