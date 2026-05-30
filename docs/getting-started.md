# Getting Started

OZM Skills is a Codex-native governance skill pack. It is useful when a coding-agent workflow needs staged intake, dispatch, writing, review, claim ceilings, reference grounding, and closeout discipline.

## Inspect The Package

```bash
git clone https://github.com/OZ-50/ozm-codex-agent-governance-skills.git
cd ozm-codex-agent-governance-skills
```

Read in this order:

1. `AGENTS.md`
2. `ozone-manager/SKILL.md`
3. the single `ozm-*` child skill that owns the current phase
4. mandatory companion child skills only when the next action needs them

## Optional Checks

Use a local Python interpreter you control:

```bash
<resolved-python> ozone-manager/scripts/ozm_package_scope_check.py --skill-root . --json
<resolved-python> ozone-manager/scripts/prose_security_scan.py --skill-root . --json
```

These checks provide deterministic package evidence only. Passing them does not prove accepted governance behavior, legal completeness, production readiness, or commercial support readiness.

## Claim Language

Prefer scoped wording:

- planned
- draft candidate
- artifact present
- pending controller gate
- verified by scope

Avoid broad wording unless the repository owner has fresh evidence for the exact claim:

- complete
- production-ready
- fully autonomous
- Agent OS
- accepted

