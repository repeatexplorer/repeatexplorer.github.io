---
title: DANTE_LTR
tool: dante_ltr
weight: 50
last_reviewed: 2026-09-23
---

Extends DANTE domain hits into complete LTR retrotransposons: it locates the
long terminal repeats flanking a set of domains and validates the element's
structure. Elements are assigned to lineages, so the annotation distinguishes
families rather than reporting undifferentiated LTR elements.

## Output

- A GFF3 file of complete elements, with their internal features and lineage
- A per-element table of structural details
- A FASTA library of the elements, for use as a repeat library
