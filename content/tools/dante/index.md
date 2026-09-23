---
title: DANTE
tool: dante
weight: 40
last_reviewed: 2026-09-23
---

Finds and classifies the conserved protein domains of transposable elements in
nucleotide sequences, by similarity search against the REXdb protein database.
The domains it reports are the starting point for the element-level pipelines,
and on their own they show which lineages are present.

## Output

- A GFF3 file of protein domain positions, with lineage classification
- A FASTA file of the translated domain sequences
- Filtered subsets by domain type or quality
