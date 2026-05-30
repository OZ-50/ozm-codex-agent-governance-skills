# OZM Script Entrypoints

This directory is the executable helper surface for `ozone-manager`.

| Script | Role |
| --- | --- |
| `ozm_skill_graph.py` | Build, check, and query the deterministic candidate skill graph. Route keywords come from `../references/routing/route-rules.json`. |
| `ozm_eval_suite.py` | Run active OZM hardening evals from `../evals/*.jsonl`. |
| `ozm_guard.py` | Run deterministic governance checks for dispatch, write, audit, closeout, commit, and skill hardening. |
| `ozm_codex_hook.py` | Adapt Codex hook events into OZM guard checks and activation-anchor reminders. |
| `ozm_guard_checks.py` | Shared source-coupling and map-pointer checks used by `ozm_guard.py`. |
| `ozm_skill_health_checks.py` | Skill-maintenance checks used by `ozm_guard.py pre-skill-hardening`. |

Use a resolved Python interpreter path on Windows; do not call these through a bare `python` or `py` command when the WindowsApps launcher shim may be active.
