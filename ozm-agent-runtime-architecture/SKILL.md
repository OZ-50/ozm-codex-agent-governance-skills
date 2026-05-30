---
name: ozm-agent-runtime-architecture
description: Use for OZM-governed agent-native, multi-agent, memory, MCP/tool, control-plane, operator-shell, or agent framework work that needs runtime-real evidence, user-agent parity, tool contracts, state transitions, memory boundaries, and claim ceilings.
---

# OZM Agent Runtime Architecture

OZM owner for agent/framework/memory/tool architecture judgment. It absorbs the normal-path governance from agent-native, framework, memory, and tool-design donor skills while keeping OZM in charge of request role, write-set, truth owner, review, closeout, and claim ceiling.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed agent-native apps, agent frameworks, multi-agent runtimes, MCP/tool layers, memory systems, operator shells, and runtime-real architecture audits. |
| Minimum input | current request role, target runtime slice, owner surfaces, user-facing actions, agent/tool surfaces, state or memory surfaces, and claimed readiness level. |
| Allowed actions | Read owner surfaces, build capability/parity/runtime maps, classify evidence, write candidate records, and name the next OZM gate. |
| Forbidden actions | Do not bypass `ozone-manager`, treat diagrams/prompts/manifests as runtime proof, mutate controller truth from a writer lane, or raise architecture claims without runtime evidence. |
| Output receipt | Agent runtime architecture receipt with loop map, parity matrix, tool contract posture, memory/state posture, evidence class, non-claims, and next gate. |
| Downstream handoff | `ozm-requirement-load`, `ozm-reference-method-grounding`, `ozm-dispatch-freeze`, `ozm-code-writing`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | Holds or lowers claims when architecture is projection-only; raises only to the freshness and runtime seam actually proven. |
| Lineage | Child of `ozone-manager`; absorbs donor governance from agent framework, agent-native, memory, and tool-design skills. |

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-governed agent-native, multi-agent, memory, MCP/tool, control-plane, operator-shell, or agent framework work that needs runtime-real evidence, user-agent parity, tool contracts, state transitions, memory boundaries, and claim ceilings."
  blocks_when:
    - agent capability is claimed without runtime/tool/state proof
    - projection-only architecture is treated as implemented runtime
  required_artifacts:
    - agent_runtime_capability_map
    - tool_contract_table
    - runtime_real_vs_projection_receipt
  downstream_binding:
    - ozm-requirement-load.runtime_truth_map
    - ozm-review-diffgate-acceptance.runtime_real_verdict
  proof_or_script:
    - manual runtime/tool receipt; no dedicated script
  claim_effect:
    - limits agent/runtime claims to projection_only until tool and state transitions are proven
  non_surface_failure_code:
    - ozm-agent-runtime-architecture_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-reference-method-grounding` when the architecture is borrowed from a reference project, paper, framework, runtime, or prior implementation.
- `ozm-external-prerequisite-gate` when the runtime depends on live providers, secrets, hosted agents, MCP servers, browser brokers, queues, or external services.
- `ozm-review-diffgate-acceptance` and `ozm-claim-ceiling` before acceptance, parity, runtime-ready, agent-native, or framework-ready wording.

Do not load standalone `agent-framework-development-governor`, `agent-native-architecture`, `agent-native-audit`, `agent-native-reviewer`, `agent-reference-driven-design`, `memory-systems`, or `tool-design` on the OZM normal path. Their reusable rules are absorbed here; use those donor ids only for explicitly non-OZM standalone workflows or historical/source comparison.

## Core Workflow

1. Classify the request: design, implementation planning, runtime audit, parity review, memory architecture, tool/MCP contract, multi-agent orchestration, reference borrowing, or acceptance review.
2. Freeze the claimed slice: framework-wide, product feature, runtime carrier, tool layer, memory layer, operator shell, or proof harness.
3. Build one canonical loop before widening scope: request entry, controller/policy owner, runtime actor, tool or subagent path, state transition, persistence or receipt, recovery path, and user/operator-visible effect.
4. Build a user-agent parity matrix for product surfaces: user action, visible data, agent tool or primitive, prompt/context availability, verification seam, and gap severity.
5. Build a tool contract map: tool name, owner, input schema, output schema, side effects, permission scope, retry/idempotency posture, error shape, and observation returned to the agent.
6. Build a memory/state posture: semantic, episodic, procedural, correction, controller truth, execution record, scratch, and historical-only surfaces. Name invalidation, freshness, privacy, and retrieval filters.
7. Classify evidence before claims:
   - `contract_only`: docs, prompts, schemas, or manifests only.
   - `projection_only`: demo/harness output without the claimed runtime loop.
   - `runtime_slice_real_but_narrow`: one real loop works through the owner seam.
   - `integration_ready_candidate`: runtime slice plus state/readback/recovery evidence.
   - `accepted_runtime`: reviewed product/runtime evidence consumed by OZM review, closeout, and claim ceiling.
8. If a reference project or paper governs the design, require source-backed method anchors and target-owned adoption decisions. Do not transplant donor architecture when target requirements, runtime, language, security model, or owner surfaces differ.
9. If implementation is requested, hand off to dispatch with the loop node, parity gap, tool contract, memory/state surface, write-set, and proof target. If any field is absent, keep implementation at planned/diagnostic.
10. Before review or closeout, verify that the diff reduced a named runtime/parity/tool/memory gap and did not only add prompts, labels, configs, stubs, or docs.

## Runtime-Real Gates

- A prompt, README, manifest, JSON schema, generated matrix, config flag, mock tool, or debug projection is not runtime proof.
- A switchability claim needs a runtime-consumed switchboard or owner port, not just record-only adapter selection.
- A memory claim needs write/readback, invalidation, and retrieval-filter evidence for the memory class being claimed.
- A tool claim needs observable side effects or readback through the tool owner seam, plus error and permission posture.
- A multi-agent claim needs actual runtime carrier posture: real subagent/tool events, external harness receipts, or a lowered same-thread/text-only ceiling.
- User-facing agent parity claims require both action parity and context parity; agent tools without the data users see are not parity.

## Runtime Parity Matrix

When the task claims agent-native or multi-agent readiness, freeze route triggers and a runtime parity matrix: user action, agent/tool action, state transition, memory/readback, error/recovery path, permission boundary, and proof seam. Missing matrix rows cap the claim at `projection_only` or `contract_only`.

## Output Receipt

Use this compact receipt when the skill changes execution state:

```json
{
  "agent_runtime_architecture_receipt": {
    "slice": "feature | framework | tool_layer | memory_layer | operator_shell | review",
    "claim_ceiling": "contract_only | projection_only | runtime_slice_real_but_narrow | integration_ready_candidate | accepted_runtime",
    "canonical_loop_ref": "...",
    "parity_matrix_ref": "...",
    "tool_contract_map_ref": "...",
    "memory_state_posture_ref": "...",
    "runtime_evidence": ["..."],
    "non_claims": ["..."],
    "blocked_or_next_gate": "..."
  }
}
```

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
