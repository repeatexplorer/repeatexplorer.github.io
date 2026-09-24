# Project skills

Procedures for the recurring jobs on this site. Each was written after doing
the task by hand at least once, as the design document asks, so they describe
what actually worked rather than what ought to.

| Skill | For |
| --- | --- |
| `add-tool` | A tool joins the site, or its entry changes |
| `add-workshop` | A workshop is added or edited |
| `add-publication` | A reference is added, always from its DOI |
| `site-audit` | Periodic health check; reports, changes nothing |

Three skills proposed in section 11 of the design document are deliberately
absent:

- **migrate-page** was phase 1 only. The migration is done: every URL in
  `migration/inventory.csv` has an outcome and resolves.
- **add-news** has nothing to attach to. There is no `/news/` section, because
  the old site had no news worth migrating.
- **sync-tool** is folded into `site-audit`, which runs
  `scripts/sync_tool_docs.py`. Splitting it out would mean two skills sharing
  one script and one judgement call.
