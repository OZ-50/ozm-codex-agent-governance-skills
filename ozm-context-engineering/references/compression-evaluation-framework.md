# Evaluation Framework

Use this file when evaluating whether compression preserved enough working context.

## Probe Categories

- accuracy
- context awareness
- artifact trail
- completeness
- continuity
- instruction following

## Evaluation Rules

- test exact identifiers, not only broad summaries
- probe what the agent must continue working on, not generic facts
- rotate probes to avoid false confidence
- compare compression methods by work continuation quality, not only token reduction

## Failure Signals

- missing file or symbol names
- stale next-step understanding
- broken continuity after compaction
- low re-entry reliability
