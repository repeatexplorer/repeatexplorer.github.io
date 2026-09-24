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

Three things fail **silently**, with no error and no output, so check the
rendered HTML rather than trusting the template:

- `where` matches nothing on a data map, though `sort` works on the same map.
  Filter inside the range instead.
- A dynamic tag name (`{{ $h := "h4" }}<{{ $h }}>`) renders nothing at all:
  html/template refuses it. Write each heading level out in full.
- HTML comments in templates are stripped from the output, so they are useless
  for debugging. Use a real element.

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

## The design: badges carry the repeat classes

Two data files drive the look, and neither belongs in a template:

- `data/repeat_classes.yml` is the badge vocabulary. Each tool's `annotates`
  names its classes; `colour` names a `--class-<name>` custom property defined
  in `assets/css/site.css`. Adding a class means adding the property too.
- `data/tool_categories.yml` groups the tools by what you start from, with the
  heading and blurb used on both the home page and `/tools/`.

`validate_data.py` rejects an unknown class and a tool whose category has no
group, either of which would make a tool vanish from a page without an error.

Cards come from `layouts/_partials/tool-cards.html`, shared by both pages, so
they cannot drift. It takes a heading `level`, 4 under the home page's section
heading and 3 on `/tools/`, to keep heading order valid; the CSS styles both.

Hero text is front matter in `content/_index.md` (`tagline`, `lead`), not
markup: rewording the home page should not touch a template. The `h1` there is
the site name itself, so the header bar drops its wordmark on the home page and
keeps it everywhere else, where it is the link home.

The favicon is RE in Space Grotesk Bold, lime ground, dark letters: a bright
mark is findable in a tab strip whichever theme the reader uses. The letters are
outlines, not text, because a favicon cannot rely on a font being installed.
`scripts/make_favicon.py` regenerates the whole set from the woff2; it needs
fontTools and Inkscape, which are one-off asset tools and deliberately not in
environment.yml. Do not hand-edit the files in `static/`.

Fonts are self-hosted in `assets/fonts/`, two variable woff2 files, 48 KB.
Do not replace them with a Google Fonts link: that sends every visitor's IP
address to Google, which this site should not do without consent.

## What the link checker cannot tell you

`lychee` checks status codes. A Galaxy server answers 200 for a shared history
that is not actually accessible, so a dead history link passes every check. The
two protocol histories were removed for exactly this reason. Treat any Galaxy
`/u/<user>/h/<name>` link as unverified unless someone has opened it.

## Content model

| Type | Required front matter | Optional |
| --- | --- | --- |
| Tool page | `title`, `tool` (key into tools.yml), `weight` | `aliases`, `last_reviewed` |
| Protocol | `title`, `tools`, `level`, `last_tested` | `aliases`, `data_url` |
| Workshop | `title`, `year`, `layout: workshop`, `start_date`, `end_date` | `venue`, `lecturers`, `program`, `materials_url`, `resources` |

`last_tested` older than 18 months renders a staleness notice automatically; the
threshold is `protocol_stale_months` in hugo.toml.

## Project skills

`.claude/skills/` holds the procedures for the recurring jobs: `add-tool`,
`add-workshop`, `add-publication` and `site-audit`. Each was written after doing
the task by hand, so it records the traps rather than the ideal. Read the one
that fits before starting, and update it when a procedure changes.

`migrate-page`, `add-news` and `sync-tool` from the design document are
deliberately absent; `.claude/skills/README.md` says why.

## Changes go through a pull request

`main` is protected: a pull request is required, the `check` status must pass,
and a review from `CODEOWNERS` must approve it. Do not commit to `main`.

    git checkout -b <topic>
    # edit, then
    make check
    git commit && git push -u origin <topic>
    gh pr create --fill

Admins are not bound by this (bypassing is allowed, so nobody can be locked
out), which means a direct push would still succeed. Do not use that: the gate
exists so the checks and the review actually happen.

Only `check` is a required status. `build` and `deploy` come from the deploy
workflow, which runs on push to `main` and never on a pull request; requiring
either would leave every pull request waiting forever.

## State of the build

Live at <https://repeatexplorer.github.io/>. Merging to `main` builds, checks
and deploys; the `gh-pages` branch still exists but nothing is served from it.

Phases 1 to 3 are done: skeleton, tools, protocols, workshops, publications,
about and the design. All 26 redirect targets resolve and `make check-cutover`
passes, which is the phase 4 gate. Section 11 is built: `.claude/skills/`,
`CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/` and `CODEOWNERS`.

What is left is the cut-over itself: DNS, the custom domain, and switching
WordPress off. The checklist is `cut-over-checklist.md` in the working
directory above this repository, which is not tracked here.

Known gaps, all of them content rather than code:

- The 2025 workshop page has a programme now, but no venue or lecturers.
- The genome annotation protocol says `Viridiplantae_v3.0`; REXdb now ships
  v4.0. Fix belongs upstream in `kavonrtep/protocols`.
- RepeatExplorer2 and ChIP-Seq Mapper both carry an "All" class badge, which
  reads oddly for ChIP-Seq Mapper.
- The phone layout is written but was never verified in a browser.
