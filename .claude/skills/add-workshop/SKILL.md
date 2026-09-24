---
name: add-workshop
description: Use when adding a RepeatExplorer workshop to the site or editing one — "add the 2026 workshop", "here is the programme", "attach the slides from 2024", "announce next year's workshop". Covers the year page, the programme schema, slides, and how past and upcoming are decided.
---

# Adding a workshop

One workshop is one branch bundle: `content/workshops/<year>/_index.md`, with
its slides as page resources beside it.

## The two things that must both be right

```yaml
---
title: RepeatExplorer Workshop 2026
year: 2026
layout: workshop          # required
start_date: 2026-05-26    # required
end_date: 2026-05-28      # required
---
```

- The file is `_index.md`, never `index.md`. A leaf bundle turns any subpage
  into a *resource*: it builds without error and the page is simply never
  rendered. That is how `/workshops/2025/venue/` once shipped as a 404.
- `layout: workshop` is required because a branch bundle otherwise renders with
  the section index template, silently dropping the programme and the facts.

`validate_data.py` enforces both, plus `end_date >= start_date` and the start
year matching `year`.

## Past and upcoming decide themselves

There is no "current workshop" flag. The index calls a workshop upcoming only
while its `end_date` is ahead of the build date, so a finished one cannot stay
advertised. Adding a future workshop with correct dates is all that is needed
for it to appear under "Next workshop", and it moves itself to the archive
afterwards.

Never write a `dates:` string. The displayed range is rendered from
`start_date` and `end_date`; a string would be the same fact twice.

## Optional fields

```yaml
venue: Biology Centre CAS, České Budějovice, Czech Republic
lecturers: [Jiří Macas, Petr Novák, Pavel Neumann]
materials_url: https://github.com/repeatexplorer/workshop
program:
  - day: Tuesday (May 26)
    sessions:
      - time: "09:00"
        title: Principles of repeat identification
        speaker: J. Macas
      - time: "13:30 – (18:00)"
        title: Practical training I
        speaker: J. Macas, P. Novák, P. Neumann
        items:
          - introduction to the Galaxy environment
          - setting up clustering analysis
        slides: Macas_repeat_annotation_2026.pdf
```

- `items` is for a session with sub-topics. Without it, a session heading and
  its list collapse into one unreadable title.
- `time` may be empty, but the key must be present in the rendered row; the
  template always emits the cell, because a missing one drops the title into the
  narrow time column.
- `slides` is a file name, linked only if that PDF really is a resource of this
  page or a subpage. A name that matches nothing renders no link rather than a
  dead one.
- Training materials belong in
  <https://github.com/repeatexplorer/workshop>, not here. Set `materials_url`.

## Slides

Put the PDFs in the bundle and give them titles:

```yaml
resources:
  - src: Macas_repeat_annotation_2026.pdf
    title: "Macas – Repeat annotation"
```

Without a title the file name is shown. If a title had to be guessed from the
file name, add `params: {title_from_filename: true}` and the page says so.

Years whose old site had a dedicated slides page keep one
(`2017/presentations/`, `2019/materials/`); everything else attaches to the year
page.

## Converting a programme from elsewhere

`migration/parse_programmes.py` in the working directory above this repository
turns an archived WordPress programme into this schema. It is migration
tooling, not part of the site, and needs the crawled HTML. For a pasted
programme, write the YAML directly; do not invent times or speakers that the
source does not give.

## Check

    make check
