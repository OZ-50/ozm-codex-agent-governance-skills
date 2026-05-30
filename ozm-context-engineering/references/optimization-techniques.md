# Optimization Techniques Reference

Use this file when the main skill already selected an optimization family and you need implementation-level guidance.

## Techniques

- KV-cache stabilization:
  keep the prefix stable and move volatile data later
- observation masking:
  elide old verbose outputs while preserving retrievability
- compaction:
  summarize accumulated state before the cliff
- partitioning:
  split across isolated contexts when one window cannot hold the task

## Selection Rule

Choose the cheapest technique that preserves quality. Do not jump to partitioning when masking or compaction would solve the problem.
