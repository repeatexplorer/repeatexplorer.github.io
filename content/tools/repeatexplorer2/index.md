---
title: RepeatExplorer2
tool: repeatexplorer2
weight: 10
last_reviewed: 2026-09-23
---

Groups unassembled sequencing reads into clusters by sequence similarity, using
a graph representation. Each cluster corresponds to a repeat family, and the
number of reads it contains estimates that family's share of the genome. No
assembly is needed, and low coverage is sufficient.

## Output

- An HTML report with one entry per cluster
- Cluster graph layouts, whose shape is diagnostic of the repeat type
- Repeat classification based on similarity to known elements and to REXdb
- Estimated genome proportion for each cluster and for each repeat class
