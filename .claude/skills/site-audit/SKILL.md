---
name: site-audit
description: Use for a periodic health check of the RepeatExplorer site — "audit the site", "is anything stale", "check the links", "are the tool pages still current", or before a release or cut-over. Reports what needs a human decision rather than changing anything.
---

# Site audit

Run the checks, then read the results. This skill changes nothing on its own.

## 1. The blocking checks

    make check

Build with `--panicOnWarning`, schema validation of the data files and front
matter, redirect map against `migration/inventory.csv`, offline link check,
and a scan for insecure links. All of this runs in CI too.

Before a cut-over, also:

    make check-cutover

which additionally requires every inventory target to resolve.

## 2. External links

    lychee --no-progress public/

Not part of `make check`: other people's servers fail intermittently and should
not block a commit.

Judge the output rather than trusting it:

- **403 is usually bot-blocking**, not a dead link. Publishers do this.
- **A 200 does not mean a link works.** A Galaxy server answers 200 for a shared
  history that is not accessible; two protocol links were removed for exactly
  this. Treat any `/u/<user>/h/<name>` link as unverified unless someone opened
  it.
- `w3lamc.umbr.cas.cz` serves no HTTPS at all. Those links are `http://` on
  purpose and are allowlisted in `scripts/check_mixed_content.py`.

## 3. Tool pages against their repositories

    python3 scripts/sync_tool_docs.py

Compares each tool's `last_reviewed` with its repository's latest push and
release. A newer push does **not** mean the page is wrong: the page says what a
tool is for and what it outputs, which changes far less often than the code.
Read the page, and if it still holds, just move `last_reviewed` forward.

## 4. Stale protocols

Protocols carry `last_tested`. Past `protocol_stale_months` in `hugo.toml`
(18 months) the page shows a notice by itself. Re-testing means running the
protocol on the Galaxy server, which is a human job; do not move the date
without doing it.

Known: the genome annotation protocol names REXdb `Viridiplantae_v3.0` while
the current release is v4.0. The fix belongs upstream in
`kavonrtep/protocols`, which is where that page comes from.

## 5. Things no check covers

- **The phone layout.** Nothing in CI renders the site. Open it at about 400px.
- **Orphaned images.** A page bundle keeps its own images, so a deleted page
  takes them with it; a renamed one does not.
- **Wording that has quietly become false.** "No workshop is currently
  announced" is generated from dates and cannot go stale, but prose such as the
  Galaxy server page's quota paragraph can.

## 6. Report

Say what needs a decision and what you changed, separately. Do not move
`last_reviewed` or `last_tested` dates as part of an audit: that is the claim
the audit exists to test.
