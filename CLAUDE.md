# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The repeatexplorer.org website: Hugo, custom theme, no third-party theme and no
npm. It replaces a WordPress install that ran on plain HTTP. The migration design
document lives outside this repo, in the working directory one level up, and is
authoritative for anything not settled here.

## Commands

    conda env create -f environment.yml     # first time
    conda activate repeatexplorer-site

    make serve          # live preview on :1313, drafts visible
    make check          # what CI runs: build, schemas, redirects, links, mixed content
    make check-cutover  # stricter; every old URL must resolve (phase 4 gate)

Run `make check` before every commit. It is fast, and CI should confirm what you
already know rather than be where you find out.

## Core rules

1. Facts about tools, publications and workshops are edited in `data/*.yml`,
   never hard-coded in page text. A tool's repo URL appears once, in `tools.yml`.
2. Never delete or rename a published page without adding an alias and an
   inventory row.
3. Do not edit `layouts/` or `assets/` during a content task. Design changes are
   separate commits.
4. Do not copy README text into tool pages. A tool page answers "is this the
   right tool for my data?"; the README answers "how do I run it?". No command
   lines, no parameters, no installation steps, no version numbers.
5. Images: page bundles only, width <= 1600 px, WebP or optimised PNG/SVG, alt
   text always.
6. British spelling, sentence-case headings, tool names spelled as in `tools.yml`.
7. External claims -- versions, dates, citations -- come from the repo, the DOI
   or the user. Never from memory.

## Redirects: the one thing that is easy to get wrong

The old site had no pretty permalinks. Every page was `?page_id=N` or `?p=N`,
and a static host ignores the query string, so all of them land on `/`.

**Never put a `?` URL in Hugo `aliases:`.** It silently creates an unreachable
directory literally named `?page_id=179`. `scripts/validate_data.py` fails the
build if you try.

Query-string URLs are handled by `static/redirects.json` plus the inline script
in `layouts/_partials/redirect-shim.html`, both generated from
`migration/inventory.csv` by `scripts/build_redirects.py`. Edit the CSV, never
the generated files. `make check` verifies the map still matches the CSV.

`?page_id=179` is linked from the Galaxy server's welcome page, which is a
server template nobody here edits. That redirect is permanent.

## Layout conventions

Hugo 0.166 template lookup, not the older `_default/` scheme:

    layouts/baseof.html          shell
    layouts/home.html            home
    layouts/page.html            single pages
    layouts/section.html         section indexes
    layouts/tools/page.html      tool pages, driven by data/tools.yml
    layouts/workshops/page.html  workshop pages, programme from front matter
    layouts/_partials/           partials (note the underscore)

Deprecated APIs fail the build, because `make check` runs
`hugo --panicOnWarning`. Current traps: use `hugo.Data`, not `site.Data`; use
`site.Language.Locale`, not `.LanguageCode`; `locale` in hugo.toml, not
`languageCode`.

## Workshop pages: branch bundles, not leaf bundles

A workshop year page is `content/workshops/<year>/_index.md` with
`layout: workshop` in its front matter. Both parts are required and
`validate_data.py` enforces them:

- `_index.md` (branch bundle) so the year can carry subpages such as `venue/` or
  `presentations/`. Inside a leaf bundle (`index.md`) a nested page becomes a
  *resource*: it builds without error and is simply never rendered, which is how
  `/workshops/2025/venue/` shipped as a 404.
- `layout: workshop` because a branch bundle otherwise renders with
  `workshops/section.html`, the index template, silently dropping the programme
  and the facts list.

Use this shape for every year, including years that have no subpages yet, so one
can be added without restructuring.

## Past and upcoming workshops

The `/workshops/` index splits the list itself; there is no manual "current"
flag to go stale. `layouts/_partials/workshop-status.html` calls a workshop
upcoming only while its own `end_date` is still ahead of the build date, so a
finished workshop cannot stay advertised as forthcoming. A year page with no
dates falls back to comparing `year`, which fails safe to past.

`start_date` and `end_date` are therefore required on every year page and
`validate_data.py` enforces them, along with end >= start and the start year
matching `year`. The displayed range is rendered by
`layouts/_partials/workshop-dates.html`; do not also write a `dates:` string,
that would be the same fact twice.

When no workshop is upcoming the index says so explicitly. That is the current
state: the most recent was 2025.

## Workshop presentations

Slides are page resources of the workshop they belong to, with their titles in
`resources:` front matter. Years whose old site had a dedicated slides page keep
one (`2017/presentations/`, `2019/materials/`, per the inventory); the rest
attach their PDFs to the year page.

Two things to know before touching them:

- A PDF's upload folder on the old site does not give its year. WordPress filed
  the 2016 slides under `uploads/2014/03/`. Year came from each file's own PDF
  CreationDate.
- The 2014-2016 slides were never linked from any page, so no title survives.
  Theirs are rendered from the filename and carry
  `params.title_from_filename: true`, which makes the page print a line saying
  so. Replace a title with a real one and remove the flag.

Page resources have no size property and `.Content` is text-only, so
`slides.html` gets file sizes from `os.Stat`.

## Content model

| Type | Required front matter | Optional |
| --- | --- | --- |
| Tool page | `title`, `tool` (key into tools.yml), `weight` | `aliases`, `last_reviewed` |
| Protocol | `title`, `tools`, `level`, `last_tested` | `aliases`, `data_url` |
| Workshop | `title`, `year`, `dates`, `venue`, `program` | `materials_url`, `lecturers` |

`last_tested` older than 18 months renders a staleness notice automatically; the
threshold is `protocol_stale_months` in hugo.toml.

## State of the build

Phase 1 (skeleton) is done: the site builds, the checks run, one worked example
of each page type exists. Phases 2 and 3 write the content: 28 redirect targets
are listed in `migration/inventory.csv`, 7 are built.

Deployment is not live yet. `.github/workflows/deploy-pages.yml` will not take
effect until the repository's Pages source is switched from the `gh-pages`
branch to "GitHub Actions" in Settings.
