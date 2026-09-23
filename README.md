# repeatexplorer.org

Source for the RepeatExplorer website: a static site built with Hugo and
deployed to GitHub Pages. No database, no plugins, no server-side code.

## Build it locally

    conda env create -f environment.yml
    conda activate repeatexplorer-site
    make serve

The site is then at <http://localhost:1313>. Edits reload as you save.

## Before committing

    make check

This runs everything CI runs: a strict Hugo build, JSON Schema validation of the
data files and page front matter, a redirect-map consistency check, an offline
link check and a scan for insecure `http://` links.

## Layout

    content/        pages, as Markdown page bundles
    data/           tool metadata, publications, people; the single source for
                    facts that appear on more than one page
    layouts/        the theme, owned by this repo
    assets/css/     one stylesheet
    schemas/        JSON Schema for the data files
    scripts/        redirect generation and the check scripts
    migration/      inventory of old WordPress URLs and where each one now points

## Editing

Facts live in `data/*.yml` and are rendered by templates. To change a tool's
repository URL, its Galaxy availability or its citation, edit `data/tools.yml`;
do not write it into the page text. `CONTRIBUTING.md` covers the conventions for
editors; `CLAUDE.md` holds the rules for agent edits.

## Deployment

Pushing to `main` builds and deploys through
`.github/workflows/deploy-pages.yml`. The same `public/` folder can be served by
any static host; Cloudflare Pages and an institutional nginx are both supported
by the generated redirect files in `static/`.
