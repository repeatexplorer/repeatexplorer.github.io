---
title: CARP
tool: carp
weight: 80
last_reviewed: 2026-09-23
---

Comprehensive Annotation of Repeats Pipeline. Runs the annotation tools over a
genome assembly and merges their results into one annotation in which each
position is assigned to a single repeat, resolving the overlaps that arise when
the tools are run separately.

## Output

- A unified, non-overlapping GFF3 annotation of the genome
- Per-class GFF3 files and repeat density tracks
- An interactive HTML report
