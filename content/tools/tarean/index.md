---
title: TAREAN
tool: tarean
weight: 20
last_reviewed: 2026-09-23
---

Reconstructs the monomer sequence of satellite repeats from RepeatExplorer2 read
clusters. It resolves the consensus from k-mer frequencies within a cluster
rather than from an assembly, which works even when the array itself cannot be
assembled.

## Output

- Consensus monomer sequences for the satellites found
- A confidence category per satellite, separating well-supported reconstructions
  from tentative ones
- Cluster-level reports and k-mer based diagnostics
