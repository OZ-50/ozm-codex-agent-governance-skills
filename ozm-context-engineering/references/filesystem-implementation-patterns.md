# Implementation Patterns

Use this file when you need concrete filesystem-context patterns beyond the main skill.

## Recommended Surfaces

- scratch directory for intermediate work
- structured current plan file
- per-agent workspaces for concurrent tasks
- persisted logs or terminal output
- stable artifact directories for retrieval

## Pattern Rules

- store large outputs on disk, not in prompt context
- keep file formats structured and grep-friendly
- isolate concurrent writers
- prefer references plus summaries over inline dumps

## Retrieval Rules

- discover with listing or glob
- narrow with grep or structured search
- read only the needed section
- validate paths before use

## Failure Rules

- stale paths must be rediscovered
- broad globs create context waste
- unstructured scratch pads decay quickly
