---
title: TideCluster
tool: tidecluster
weight: 70
last_reviewed: 2026-09-23
---

Detects tandem repeat arrays in a genome assembly and groups them into families.
Detection uses TideHunter; the arrays are then clustered by similarity so that
one family is reported once rather than as many separate arrays, and consensus
sequences are reconstructed with TAREAN.

## Output

- A GFF3 file of tandem repeat arrays, labelled by family
- Consensus sequences per family
- An HTML report, with per-family tables
