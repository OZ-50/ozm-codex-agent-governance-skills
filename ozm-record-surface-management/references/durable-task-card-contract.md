# Durable Task Card Contract

Use this reference when OZM-governed work creates, triages, resolves, imports, or archives durable task cards. It absorbs the reusable workflow from `todo-create`, `todo-triage`, and `todo-resolve`; those donor ids are archive/restore-only history after the 2026-05-28 todo lifecycle absorption.

## Source Classification

| Surface | OZM posture |
| --- | --- |
| Project-approved task-card root | Normal read/write owner for durable task cards. |
| `.context/compound-engineering/todos/` | Legacy donor-compatible import surface. Read before migration or compatibility work; write only when the current project has explicitly kept this as its task-card root. |
| `todos/` | Legacy read-only import surface unless project instructions explicitly make it current owner. |
| Platform in-session plan tools | Temporary execution aid only; not durable task truth. |

Before writing, record `task_card_root`, `authority_class`, `write_owner`, `lifecycle_owner`, and `legacy_import_posture`. If no approved durable root exists, create no task card until `ozm-requirement-load` or project owner surfaces approve one.

## File Identity

Default portable naming:

```text
<task_card_id>-<status>-<priority>-<short-kebab-title>.md
```

Fields:

- `task_card_id`: stable unique id; do not reuse after archive/delete.
- `status`: `pending`, `ready`, `running`, `blocked`, `complete`, `accepted`, or `archived`.
- `priority`: `p1`, `p2`, or `p3`.
- `dependencies`: list of task card ids that must be complete or accepted before admission.
- `tags`: bounded category labels; labels are routing aids, not proof.
- `authority_class`: normally `execution_record` or `derived_navigation`; never silently `controller_truth`.
- `claim_ceiling`: strongest wording this card can support.

Legacy donor files with only `pending`, `ready`, and `complete` map as:

- `pending`: untriaged candidate; not writer-ready.
- `ready`: admitted candidate after triage; still needs dispatch freeze before code writing.
- `complete`: work was reported complete; not accepted until OZM review/closeout consumes fresh evidence.

## Required Sections

Each durable card should contain:

- Problem Statement
- Findings
- Proposed Solutions
- Recommended Action
- Acceptance Criteria
- Work Log
- Dependencies / Blockers
- Evidence And Receipts
- Claim Ceiling / Non-Claims
- Next Consumer

Optional sections: Technical Details, Resources, Notes, Rejected Options, Migration/Compatibility Notes.

## Create Gate

Create a durable task card when the work is cross-session, likely over about 15 minutes, dependency-bearing, needs prioritization, is a residual review finding, or must survive context compression. Do not create one for a trivial immediate fix or a temporary step list.

Creation receipt:

```json
{
  "task_card_event": "create",
  "task_card_id": "...",
  "root": "...",
  "status": "pending|ready",
  "priority": "p1|p2|p3",
  "dependencies": [],
  "authority_class": "execution_record",
  "creation_reason": "...",
  "acceptance_criteria_present": true,
  "claim_ceiling": "candidate_task_card"
}
```

## Triage Gate

Triage is a record decision, not implementation. During triage:

- review problem, findings, proposed solutions, dependencies, and acceptance criteria
- decide `approve`, `defer`, `reject`, or `customize`
- if approving, move `pending` to `ready`, fill Recommended Action, and record dispatch prerequisites
- if rejecting/skipping, archive or delete only candidate task cards; do not delete controller truth, evidence, plans, solution docs, or history surfaces
- do not write product code, lower controller requirements, or mark acceptance during triage

Triage receipt:

```json
{
  "task_card_event": "triage",
  "decision": "approve|defer|reject|customize",
  "from_status": "pending",
  "to_status": "ready|pending|archived",
  "recommended_action_updated": true,
  "dependencies_checked": true,
  "claim_ceiling": "ready_for_dispatch_candidate"
}
```

## Resolve Gate

Resolve only `ready` cards or explicitly selected ready-compatible cards. Skip `pending` cards and report them as not triaged. Sort by dependencies before work; use parallel lanes only after `ozm-role-stack-coordination` and `ozm-dispatch-freeze` prove disjoint write sets and review owners.

Resolution rules:

- a ready card still requires OZM dispatch freeze before writer admission
- a complete card is an execution record, not acceptance proof
- commits, pushes, branch changes, and PR actions require explicit current authorization
- prior-learning or solution documentation is routed through OZM record surfaces, not the old CE compound donor path
- cleanup happens only after evidence, review, closeout, and claim ceiling are recorded

Resolve receipt:

```json
{
  "task_card_event": "resolve",
  "task_card_id": "...",
  "from_status": "ready|running|blocked",
  "to_status": "complete",
  "dispatch_ref": "...",
  "files_changed": [],
  "tests_or_gates": [],
  "evidence_refs": [],
  "pending_cards_skipped": [],
  "claim_ceiling": "complete_pending_review"
}
```

## Cleanup And Archive Gate

Cleanup is safe only when the card is complete or rejected, OZM closeout has recorded consumer state, and no dependent card still needs the body. Prefer archive over deletion when the card contains useful findings, unresolved risks, or cross-session learning.

Never treat a donor cleanup rule as authority to delete `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, controller-truth docs, evidence ledgers, or project history. Those surfaces require their own owner gate.

Cleanup receipt:

```json
{
  "task_card_event": "cleanup",
  "task_card_id": "...",
  "cleanup_action": "archive|delete|retain",
  "reason": "...",
  "dependents_checked": true,
  "restore_path": "...",
  "claim_ceiling": "archived_record_only"
}
```

## Research Basis

This absorption keeps the donor's useful lifecycle discipline while changing ownership:

- LangChain Deep Agents treats todo planning, filesystem context, subagents, and memory as harness capabilities that support long-running agents rather than standalone proof.
- Jira workflow guidance separates work-item status, transition, and resolution; OZM preserves that separation as create/triage/resolve/cleanup receipts.
- GitHub issue label guidance treats labels as categorization for workflow, not evidence of completion; OZM maps priority/tags the same way.
- Recent task-memory and stateful-agent planning papers emphasize persistent task state, dependency tracking, and disruption recovery; OZM binds durable cards to claim ceilings and downstream gates instead of relying on linear chat context.
