---
title: RepeatExplorer2
tool: repeatexplorer2
weight: 10
last_reviewed: 2026-09-23
---

## What it is for

Most plant genomes consist largely of repeated sequences, and assembling them is
hard. RepeatExplorer2 takes a different route: it works directly on unassembled
sequencing reads, at coverage far below what an assembly needs, and groups reads
into clusters by their similarity to one another. Each cluster corresponds to a
repeat family, and the number of reads in it estimates how much of the genome
that family occupies.

## When to use it

Use it when you want to know which repeats a genome contains and in what
proportions, and you do not have an assembly. A few hundred thousand reads,
around 0.1 to 1 percent genome coverage, is usually enough. If you already have
an assembly, the assembly-based tools annotate repeats in place instead.
