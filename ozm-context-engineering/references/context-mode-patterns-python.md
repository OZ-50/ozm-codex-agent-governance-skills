# Python Patterns

Use Python in context-mode when the task needs richer parsing, CSV handling, structured transforms, or filesystem-heavy analysis.

## Good Patterns

- load saved JSON, CSV, XML, or log files
- aggregate errors, frequencies, or timing stats
- inspect large structured outputs and print only the decision-relevant findings
- compute derived metrics before printing

## Output Rules

- always print the findings you want in context
- prefer compact summaries with exact evidence
- keep raw data on disk unless a tiny excerpt is necessary

## Common Uses

- test output analysis
- dependency or config inspection
- codebase metrics
- large log parsing
- one-shot extraction from saved browser artifacts

## Avoid

- printing full parsed objects
- using Python only to mirror shell output
- reading large files into context without summarizing them
