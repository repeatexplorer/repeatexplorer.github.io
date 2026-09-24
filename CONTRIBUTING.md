# Contributing

This repository is the repeatexplorer.org website. It is a Hugo site: Markdown
pages, YAML data files and a small theme kept here rather than pulled from
elsewhere.

Tool documentation is **not** here. Installation, parameters and usage belong in
each tool's own repository; the website says what a tool is for and what it
outputs. A correction to a README goes to that repository.

## Reporting something without using git

Open an issue. The templates ask for exactly the fields the change needs, so a
filled-in issue can usually be applied without a second round of questions:

- **Content correction** — something is wrong, out of date or unclear
- **Add a tool** — the fields are the entry in `data/tools.yml`
- **Add or update a workshop** — dates, venue, programme
- **Tool release or change** — a tool changed in a way the site should reflect

Server problems and tool bugs are not website issues; the links at the top of
the issue chooser point to the right place.

## Making the change yourself

    git clone https://github.com/repeatexplorer/repeatexplorer.github.io.git
    cd repeatexplorer.github.io
    conda env create -f environment.yml
    conda activate repeatexplorer-site
    make serve

The site is then at <http://localhost:1313> and reloads as you save.

Before opening a pull request:

    make check

This is what CI runs: a strict build, JSON Schema validation of the data files
and front matter, a redirect-map check, an offline link check and a scan for
insecure links. A pull request cannot merge until it passes, so running it
locally saves a round trip.

One topic per branch and per pull request. Say what changed and why.

## Conventions

**Facts live in `data/`, not in page text.** A tool's repository URL, its
citation, whether it is on the Galaxy server: all of that is in
`data/tools.yml` and rendered by the templates. Writing it into a page means it
will be wrong in one place later.

- `data/tools.yml` — one entry per tool, every field required by
  `schemas/tools.schema.json`
- `data/publications.yml` — references, taken from the DOI record and never
  typed by hand. Authors are stored `Family I.`
- `data/repeat_classes.yml` — the vocabulary behind the class badges
- `data/tool_categories.yml` — how tools are grouped, shared by the home page
  and `/tools/`

**Front matter by page type:**

| Type | Required |
| --- | --- |
| Tool page | `title`, `tool`, `weight` |
| Protocol | `title`, `tools`, `level`, `last_tested` |
| Workshop | `title`, `year`, `layout: workshop`, `start_date`, `end_date` |

A workshop year page must be `_index.md`, not `index.md`, or its subpages are
silently not rendered.

**Writing:** British spelling, sentence-case headings, tool names spelled as in
`tools.yml`. Short sentences, no marketing adjectives. Tool pages carry no
command lines, parameters, installation steps or version numbers, which is why
they do not go stale when a tool is released.

**Images:** in the page bundle they belong to, at most 1600 px wide, with alt
text.

**Links:** never put a query-string URL such as `?page_id=179` in Hugo
`aliases:`. It creates an unreachable directory of that name.
`migration/inventory.csv` is where old URLs are mapped; the redirect files are
generated from it.

**Dates:** `last_reviewed` and `last_tested` are claims that somebody checked
the page against reality. Do not move them without doing so.

## Review

Every pull request is reviewed before merge. `CODEOWNERS` names the reviewer.
Claims about versions, dates and citations are checked against a source rather
than accepted as written.
