---
title: ChIP-Seq Mapper
tool: chipseq_mapper
weight: 30
last_reviewed: 2026-09-23
---

Maps ChIP and input reads onto RepeatExplorer2 clusters and compares their
abundance in each. Repeats bound by the protein under study are enriched in the
ChIP sample relative to the input, which identifies them without needing an
assembled reference. It has been used to find centromeric repeats through CENH3
ChIP-seq.

## Output

- Per-cluster ratio of ChIP to input read counts
- A ranking of clusters by enrichment, identifying the associated repeats
