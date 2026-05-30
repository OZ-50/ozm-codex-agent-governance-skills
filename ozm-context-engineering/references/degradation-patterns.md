# Degradation Patterns Reference

Use this file when the main skill already identified context degradation and you need a tighter pattern diagnosis.

## Pattern Map

- lost in the middle:
  fix with placement and summarization
- poisoning:
  fix with validation, freshness checks, and contradiction detection
- distraction:
  fix with curation and masking
- confusion:
  fix with task separation and clearer objective boundaries
- clash:
  fix with explicit precedence and conflict resolution

## Detection Signals

- rising irrelevance as context grows
- missed instructions that were present earlier
- unstable answers after contradictory retrieval
- tool misuse after long histories

## Response Rule

Do not apply mitigation blindly. First identify whether the problem is placement, noise, stale truth, or task mixing.
