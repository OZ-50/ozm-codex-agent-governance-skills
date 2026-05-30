---
name: ozm-wait-block-replay-replacement
description: Use when an OZM-governed lane appears stalled and must be classified honestly as clean wait, nonstart, replay, replacement, blocker, or historical-only without corrupting ownership.
---

# OZM Wait Block Replay Replacement

Lane-state classification skill for governed work. Use it when output is ambiguous, handoff pairs have not landed, or stalled work risks turning into fake progress.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM blocked, waiting, nonstart, replay, replacement, or abandoned-lane handling. |
| Minimum input | lane state, last receipt, wait reason, owner timeout or replacement policy. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when an OZM-governed lane appears stalled and must be classified honestly as clean wait, nonstart, replay, replacement, blocker, or historical-only without corrupting ownership."
  blocks_when:
    - stalled lane is blindly replayed
    - replacement would corrupt owner surface or duplicate writer work
  required_artifacts:
    - lane_state_classification
    - replay_or_replacement_decision
    - ownership_boundary_receipt
  downstream_binding:
    - ozm-dispatch-freeze.replay_admission
    - ozm-record-surface-management.lane_state_record
  proof_or_script:
    - manual lane trace/heartbeat receipt; no dedicated script
  claim_effect:
    - limits lane posture to clean_wait, blocked, nonstart, replay_candidate, or replacement_candidate
  non_surface_failure_code:
    - ozm-wait-block-replay-replacement_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-role-stack-coordination` when stalled work requires a role, lane, or transport refreeze

## Workflow

1. Inspect start signals, source writes, handoff files, and current owner state.
2. Classify the lane as clean wait, real start, nonstart, replay candidate, replacement candidate, blocker, or historical-only.
3. Preserve the original owner boundary while deciding the next action.
4. Use productive controller-side fallback during clean wait without overlapping active writes.
5. Escalate repeated zero-write, stale-path, or severe failed-review behavior instead of replaying forever.
6. When replay has failed repeatedly, downgrade the method to suspect or wrong-direction candidate before replacement.
7. Prefer an autonomous next action when safe: productive controller fallback, replay with new evidence, replacement, downgrade to historical-only, direction search, or diagnostic-only probe before asking for a human decision.

## Clean Wait And File-Bus Controls

- During clean wait, advance only controller-side or disjoint work: acceptance probes, benchmark or judge prep, contract mocks, audit diffs, gap decomposition, wording repair, snapshot inventory, handoff validation, or thread-memory sync.
- Do not touch the active product write-set while another writer owns it.
- File-bus status, heartbeat files, landed handoff pairs, and watcher output are liveness or transport signals only. They never prove acceptance, product truth, or completion.
- Keep polling or heartbeat artifacts in control-layer placement with lifecycle and cleanup posture; do not let them become runtime truth or future baselines.

## Scheduler Transition Rules

Poll `waiting` or `running` lanes only against the frozen status surface, expected outputs, timeout policy, and owner record. Do not infer progress from silence, elapsed time, or plausible chat memory.

Route triggers for this child include stalled lane, clean wait, nonstart, replay candidate, replacement candidate, blocker, historical-only, waiting, blocked, 无启动, 重放, 替换, 等待, and 阻塞. A lane-state receipt must state the exact class and owner boundary before replay or replacement.

Default transitions:

- `waiting` -> `ready` when the dependency, external event, or owner surface becomes true
- `running` -> `review_pending` when expected outputs land
- `running` -> `waiting` with `wait_reason=clean_wait` when start signals exist and the frozen timeout has not elapsed
- `running` -> `nonstart` when no start signal or first artifact appears by the timeout
- `nonstart` -> `replay_candidate` only when a new evidence basis, prompt repair, environment fix, or narrower write-set exists
- `replay_candidate` -> `replacement_candidate` after repeated nonstart, repeated stale-path output, repeated severe review failure, or unchanged automation method failure
- any active lane -> `historical_only` when superseded, archived, or no longer traceable to the current master plan

Use one replay as the default budget unless an owner record freezes a different budget. After the replay budget is exhausted, downgrade the method and search for a replacement direction or blocker classification.

For failed lanes, store a short reflection record: trigger, failed assumption, observed evidence, prevention gate, and next allowed state. Reflections are future hints only; they do not turn stale artifacts into truth.

`clean_wait` is a lane classification and waiting reason, not a separate scheduler queue state. After every transition, update the continuation state and scheduler queue before closeout or replacement dispatch. For long-running file-driven loops, create a new planning-continuity `queue_revision` or explicitly mark the old queue stale and route the next action to requirement load for planner refresh.

## Auxiliary Thread Lease Handling

For auxiliary-thread lanes created by `辅助（<task_root>）下的任务执行`, inspect the frozen claim lock, heartbeat, status surface, expected outputs, timeout policy, and owner record before changing state.

Default transitions:

- `claimed` -> `running` when heartbeat and start signal appear inside the frozen lease
- `claimed` -> `nonstart` when no heartbeat or first artifact appears by the start timeout
- `running` -> `review_pending` when the result pack and expected outputs land
- `running` -> `waiting` with `wait_reason=clean_wait` when the heartbeat is alive and the frozen timeout has not elapsed
- `running` -> `replace` when the lease expires, heartbeat is stale past policy, or output writes outside the frozen write-set
- `replace` -> `ready` for a new auxiliary thread only after the stale claim is downgraded and the controller records takeover reason

A stale lock is not permission to overwrite. It is evidence for wait/replay/replacement classification.

## Blocked Lane State Machine

Classify stalled lanes as `waiting_for_tool`, `waiting_for_user`, `waiting_for_dependency`, `failed_to_start`, `stale`, `replaceable`, `replayable`, or `abandoned`. Replay must preserve the original owner surface; replacement must declare what evidence is inherited versus stale. Every block handling output names lane state, candidate action, and claim ceiling.


## Hard Rules

- Do not treat silence as success.
- Do not turn stale output into live truth.
- Do not run replay or replacement without recording why the prior path was downgraded.
- Do not replay the same automation method after repeated nonstart or severe failed review without a new evidence basis or direction change.
- Do not report a vague blocker when a bounded replay, replacement, diagnostic-only probe, or historical-only downgrade is available.
- Do not keep polling a lane past its frozen timeout without changing the state, lowering the claim ceiling, or recording a clean-wait reason.
- Do not let an auxiliary thread take over a claimed task until the stale lease, heartbeat, and prior result-pack posture have been classified.
- Do not replay, replace, or resume from a lane transition while the continuation queue still reflects the pre-failure priority order.

## Leave With

- the lane classification
- the evidence for that classification
- the method posture when replay/replacement is involved
- the updated scheduler state, wait reason, and replay budget posture when a lane was queued, waiting, running, or replaced
- the updated or stale planning-continuity queue revision when the lane belongs to a long-running file-driven loop
- the auxiliary claim, lease, heartbeat, and takeover posture when an auxiliary thread lane is involved
- the next action: wait, replay, replace, direction-search, block, or downgrade to historical-only
- the exact human-owned blocker only if no safe autonomous next action exists

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
