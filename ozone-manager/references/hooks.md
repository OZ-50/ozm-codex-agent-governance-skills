# OZM Deterministic Hooks

Use hooks for checks that are mechanical enough to run before a human or model claim. Keep semantic judgment in OZM skills.

## Codex Desktop Built-In Hooks

Codex Desktop/CLI hooks are supported through `hooks.json` or inline `[hooks]` config. The current OZM adapter is:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_codex_hook.py
```

Resolve `<resolved-python>` and `<skills-root>` before installing hooks. These variables are operator-local/local-only hook configuration, not project runtime or deployment truth. Do not configure the hook command as bare `python` or through the WindowsApps Python launcher shim; that shim can hang or leave duplicate launcher processes, causing every tool call to pay hook timeout cost. If an active Codex session already loaded an old command, update `hooks.json`, clear old `ozm_codex_hook.py` shim processes, and restart the Codex session before judging hook latency.

To print local variable values for installation, run:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\resolve_paths.py --shell json
```

Example config:

```powershell
<skills-root>\ozone-manager\references\codex-hooks.example.json
```

Install it as either:

- user-level hook: `<codex-home>\hooks.json` (operator-local configuration path)
- project-level hook: `<repo>\.codex\hooks.json`

The adapter accepts Codex hook JSON on `stdin` and emits Codex hook JSON actions. It blocks high-confidence mechanical errors and otherwise stays advisory:

- `UserPromptSubmit`: when the prompt names OZM/OZoneManager/`ozm-*`, inject the OZM activation anchor and request-role binding reminder.
- `PreToolUse` for `apply_patch`/`Edit`/`Write`: block plan-only/read-only planning edits; block patch text containing likely secrets; run OZM pre-write hygiene on touched patch paths; block guard errors such as writer edits to controller-truth Plan/Goal/contract documents without explicit controller-update posture, version/task/work-unit ids outside planning/control documents, active work-unit filenames, work-unit claim/config/UI/data content, unstable authority names, runtime local absolute path dependencies, hard coupling, and historical runtime dependencies; add model-visible context for warnings.
- `PreToolUse` for `Bash`/`shell_command`: block clearly mutating shell commands only when the current permission mode/request role is plan-only.
- `PostToolUse` for `apply_patch`/`Edit`/`Write`: rerun path hygiene after the edit so newly written files can be scanned; guard errors block normal result processing and force remediation, though they cannot undo side effects.
- `Stop`: for OZM closeout claims that omit guard/validation posture, add a closeout reminder; in `--strict` mode it can continue the turn instead of only warning.

Use strict mode only for repos that have already adopted OZM control-surface discipline:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_codex_hook.py --strict
```

Codex hook limitations matter for OZM:

- `PreToolUse` and `PostToolUse` do not intercept every possible shell/tool path; they are guardrails, not an enforcement boundary.
- `PostToolUse` cannot undo side effects; it can only feed back warnings or block normal result processing.
- hooks from multiple config files can run concurrently, so do not depend on hook ordering for claim ceilings.
- plugin-bundled hooks are disabled by default in this Codex release unless `plugin_hooks` is explicitly enabled.
- a hook success result is candidate mechanical evidence only and never raises OZM acceptance, truth, or claim ceiling by itself.

## Guard Script

Primary script:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_guard.py <mode> --root <project-root>
```

Interpreter resolution is part of the guard contract. Prefer the project environment entrypoint or a recorded operator-local interpreter path. On Windows, bare `python` and `py` can resolve to the WindowsApps launcher shim; if that happens, graph/guard/hook commands may hang and leave duplicate shim processes. Hook examples and OZM command receipts should therefore record the interpreter path used without treating it as portable project truth.

Modes:

- `pre-dispatch`: require file-state and artifact-placement manifests; scan supplied paths when present.
- `pre-write`: scan touched files before an OZM writer/code path continues.
- `pre-audit`: check audit prompt neutrality and candidate-evidence boundary.
- `pre-closeout`: scan touched files, require placement posture, and run the active non-planning surface sweep before closeout.
- `pre-commit`: scan staged or supplied paths for deterministic hygiene issues.
- `pre-skill-hardening`: scan OZM skill-maintenance risks, including missing active eval JSONL files, missing child Governance Contract blocks, over-broad frontmatter, bare Python command examples, route-rule externalization, and archived donor normal-path triggers.

Use `--paths <file...>` when the project is not a Git repo or when the hook owner already knows the touched files. Use `--staged` for Git pre-commit mode. Use `--request-role plan_only` or `--request-role read_only_plan` when a dispatch/write hook is being checked against a no-write planning request. Use `--allow-controller-doc-edits` only for an explicit controller-update packet that is allowed to edit Plan/Goal/master-plan/acceptance/schema/API-contract truth. Use `--json` when another tool will consume the result.

Use `--skip-default-manifests` only for runtime hook adapters that need low-noise path hygiene without requiring project control manifests on every edit. Direct OZM stage checks should normally keep default manifests active.

In `pre-closeout`, supplied paths are not the whole hygiene boundary. The guard also sweeps active non-planning text surfaces under the project root, excluding planning/control docs, execution records, receipts, historical/archive/provenance roots, and ignored/generated cache. This supports closeout's full active naming/path/config/data hygiene gate; it is mechanical evidence only, not proof that the project objective is satisfied.

## What Hooks Should Enforce

Good hook checks:

- likely secrets or private keys in tracked text files
- active files referencing historical/control roots such as `versions`, `completed_versions`, `completed_docs`, or `archive`
- cumulative work-packet or execution logs that contain many historical packets and proof words but no active window, truth-calibration record, or packet-history index
- multiple large project control surfaces such as `master-plan.md`, `current-state.md`, `acceptance-ledger.md`, `gap-register.md`, or packet logs without a compact memory index
- direct writer edits to controller-truth documents such as Plan, Goal, master-plan, roadmap, requirements, acceptance checklist/ledger, schema, API/runtime contract, architecture decision, current-state, or truth calibration unless the guard invocation marks an explicit controller-update packet
- generic root placement under names such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `tmp`, `src`, `docs`, `output`, or `archive`
- active project filenames using date/version/status/run/score/task/work-unit labels outside planning/control documents or historical archive text
- active source, config, tests, maps, deployment docs, authority docs, variables, fields, ids, or values using work-unit, milestone, packet, slice, run, or version ids outside planning/control documents
- active config values, claim ceilings, public HTML/JS render surfaces, persistent seed/fixture rows, and active data content exposing version/task/work-unit ids as current claim/state/product truth
- active `data/` or runtime-state filenames carrying version/status/work-unit/run naming, including ignored local database files that would otherwise survive outside Git review
- active non-planning source/config/data/UI/map/deployment surfaces that carry version/task/work-unit ids or host-local paths even when those files were not dirty or touched in the current packet
- host-local absolute paths in source/config/runtime files without local-only/operator-only governance and a repo-relative/configured/deployment-safe alternative; active docs receive warnings unless the path is explicitly marked local-only/operator-only
- source-level coupling in non-central/non-forwarding scripts: deep relative imports, sibling internal/private imports, `sys.path` parent injection, direct `.codex/skills` or `skills-archive` dependencies, and runtime source dependencies on archive/history/version roots
- active source-map, module-map, source-tree, source-manifest, and `maps/` files that point at historical/control/release roots or local targets missing under the guard root
- missing file-state, artifact-placement, or modification-record manifests
- audit prompts that preload expected outcome conclusions
- dispatch or write hooks attempted while the current request role is plan-only/read-only planning

Bad hook checks:

- deciding whether the final objective is satisfied
- deciding whether a plan is product-correct
- deciding whether a risk story is persuasive
- deciding whether a specialist audit should be approved

## Git Pre-Commit Example

Put this in `.git/hooks/pre-commit` for a Git project:

```sh
#!/bin/sh
"<resolved-python>" "<skills-root>/ozone-manager/scripts/ozm_guard.py" pre-commit --root . --staged
```

This repository may not be a Git repo. If `.git` does not exist, run the guard directly with `--paths`.

## OZM Integration

- `ozm-requirement-load` / `ozm-dispatch-freeze`: run `pre-dispatch` when manifests should exist before writer admission.
- `ozm-dispatch-freeze`: include `--request-role <role>` when the dispatch package records `plan_only`, `read_only_plan`, or execution-request posture.
- `ozm-code-writing`: run `pre-write` before or after code edits when touched files are known; include `--request-role <role>` when the current role could be plan-only/read-only planning.
- `ozm-review-diffgate-acceptance`: run `pre-audit` against the audit prompt before independent audit dispatch.
- `ozm-closeout-handoff`: run `pre-closeout` before positive closeout wording.

Hook output is candidate mechanical evidence only. It can block or downgrade a claim, but it cannot raise the claim ceiling by itself.
