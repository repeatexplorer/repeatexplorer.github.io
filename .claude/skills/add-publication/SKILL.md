---
name: add-publication
description: Use when adding or correcting a reference on the RepeatExplorer site — "add the new DANTE paper", "this tool has a citation now", "add the Zenodo record". Fetches the record from the DOI so nothing is typed by hand.
---

# Adding a publication

Every field in `data/publications.yml` comes from the DOI record. Nothing in
that file is typed from memory, a PDF or a README's own formatting.

## 1. Fetch the record

```bash
curl -sSL -H "Accept: application/vnd.citationstyles.csl+json" \
     "https://doi.org/10.1093/nargab/lqae113" | python3 -m json.tool
```

## 2. Write the entry

```yaml
dante2024:
  authors:
    - Novák P.
    - Hoštáková N.
  year: 2024
  title: "DANTE and DANTE_LTR: lineage-centric annotation pipelines ..."
  journal: "NAR Genomics and Bioinformatics"
  volume: "6"
  pages: "113"
  doi: 10.1093/nargab/lqae113
```

**Authors must be `Family I.`** Short citations take the first token of the
first author, so a literal name breaks them: a Zenodo record gave
`Petr Novak`, and the tools page rendered "Petr 2023" instead of "Novák 2023".
`validate_data.py` now rejects any author that does not end in a period.

Keep the key short and stable: it is referenced from `tools.yml` and from page
front matter. Year suffixes are fine (`dante2024`), the DOI is not.

## 3. Wire it up

Add the key to the tool's `cite` list in `data/tools.yml`, or to a page's
`cite:` front matter. An unused entry still shows on `/publications/`; a key
that names nothing fails the build.

Where a tool has both a paper and a Zenodo record, cite both, as REXdb does.

## 4. Check

    make check

Then look at `/publications/` and the tool page: the same reference partial
renders in both, so if one is wrong both are.
