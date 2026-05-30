# Instruction Surface Contract

## Minimal Root Surface

A root `AGENTS.md` should usually answer:

- what this repository is
- which global or repo-local workflow applies
- what files or docs an agent should read first
- canonical commands or environment entrypoints
- what not to touch without explicit authorization
- how directory-scoped instruction files override or narrow root guidance

## Compatibility Shim

- Prefer `AGENTS.md` as the substantive Codex-facing file.
- Let `CLAUDE.md` point to `AGENTS.md` only when Claude Code compatibility is required.
- Do not duplicate the same rules in both files unless the owner explicitly requires parallel maintenance.
- If no tool needs the shim, do not create one for symmetry.

## Allowed Surfaces

- root `AGENTS.md`
- root `CLAUDE.md` compatibility shim
- directory-scoped `AGENTS.md` or `CLAUDE.md`
- linked project docs referenced by those instruction files
- global/workspace instruction surfaces only when explicitly in scope

## Forbidden Drift

- archived or absorbed skill ids in normal startup guidance
- plan-only or read-only guidance that turns into writer admission
- project-local assumptions promoted to global defaults
- stale paths, ports, commands, model names, or environment entrypoints
- duplicated rules across shims that can diverge
- secrets, tokens, credentials, or machine-private values

## Validation

- Reread changed instruction files.
- Search active instruction surfaces for removed stale ids or paths.
- Confirm no instruction claims authority over unrelated roots.
- Confirm plan-only/read-only posture did not become writer admission.
- Confirm missing lower-level instruction files are recorded as absent rather than blockers.

## Output Receipt

This is the Closeout Receipt for instruction-surface work.

```json
{
  "instruction_surfaces": [
    {"path": "AGENTS.md", "class": "repo_root_authority", "posture": "created | updated | unchanged | absent"}
  ],
  "edit_posture": {
    "owner": "project or user",
    "allowed_root": "repo root",
    "no_edit_surfaces": []
  },
  "stale_references_removed": [],
  "stale_references_remaining": [],
  "compatibility_shim": "none | points_to_agents | duplicated_by_owner_request",
  "validation": "passed | warning | blocked",
  "claim_effect": "navigation_control_only"
}
```
