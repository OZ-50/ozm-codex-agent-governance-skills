# Shell Patterns

Use shell inside context-mode workflows for small orchestration steps, not for raw large-output inspection.

## Good Patterns

- save outputs to files
- chain small whitelisted commands around context-mode tools
- prepare paths, filenames, and directories for later analysis

## Keep In Shell

- navigation
- file mutations
- git writes
- process control
- package install
- tiny outputs

## Move To Context-Mode

- logs
- test output
- JSON or CSV analysis
- large git history
- API responses
- browser telemetry

## Avoid

- `cat` on large files
- large `curl` outputs directly into context
- unfiltered `gh` JSON dumps
