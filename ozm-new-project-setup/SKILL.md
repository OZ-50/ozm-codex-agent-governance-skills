---
name: ozm-new-project-setup
description: "Use for OZM new-project pre-start setup or audit: TruthDocs surfaces, task/goal loops, Goal/runtime reentry gates, loop output discipline, placement/environment gates, smoke/probe script placement, and bounded run-until-done autonomy."
---

# OZM New Project Setup

Create a governed pre-start package for a new agentic coding project before any source implementation. This skill turns a vague project idea into durable control surfaces, technology decisions, optional UX reference standards, packet sequencing, and verification gates that future coding threads can follow without drifting into shallow MVP work.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM new-project pre-start setup or audit: TruthDocs surfaces, task/goal loops, Goal/runtime reentry gates, loop output discipline, placement/environment gates, smoke/probe script placement, and bounded run-until-done autonomy."
  blocks_when:
    - new project starts without truth docs, environment, or placement posture
    - template defaults overwrite owner intent
  required_artifacts:
    - project_boot_matrix
    - instruction_surface_posture
    - clean_room_entry_receipt
  downstream_binding:
    - ozm-requirement-load.project_truth_surfaces
    - ozm-dispatch-freeze.initial_packet
  proof_or_script:
    - manual project surface audit; no dedicated script
  claim_effect:
    - keeps project at setup_ready only after boot surfaces and first packet are bounded
  non_surface_failure_code:
    - ozm-new-project-setup_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | New OZM-governed project startup, pre-start audit, reusable startup templates, or route repair before implementation. |
| Minimum input | latest user request, project root or intended root, current request role, desired startup/audit/template output. |
| Allowed actions | Read or create planning/control surfaces, classify startup gaps, propose templates, and name the next admissible packet. |
| Forbidden actions | Do not bypass `ozone-manager`, start product implementation, claim runtime proof, mutate controller truth from an execution role, or widen the latest request. |
| Output receipt | Record stage decision, created/updated surfaces, claim ceiling, unresolved gaps, and next authorized gate. |
| Downstream handoff | Hand off to `ozm-requirement-load` and `ozm-dispatch-freeze` before any implementation packet; hand off to preserved specialists only for their domain standards. |
| Claim ceiling effect | Defaults to planning/control-surface wording; may not raise runtime, release, provider, DB, or UI proof without source evidence and receipts. |
| Lineage | Child of `ozone-manager`; not a standalone implementation or acceptance bypass. |

## Required Posture

Use `$ozone-manager` first when available, then use this skill as the project-startup specialist.

Default claim ceiling:

```text
truthdocs_planning_only
```

This skill can create or update planning/control documents and templates. It must not claim runtime, MCP servers, IDE UI, provider adapters, database, tests, or release proof exists until source and receipts exist.

## Workflow

1. Classify the request.
   - `new_project_prestart`: create startup docs and standard templates.
   - `planning_audit`: find gaps in existing startup docs.
   - `standard_template`: produce a reusable standard such as Template A.
   - `route_repair`: add route/index/current-state entries so future agents read the right docs.
   - `implementation_request`: stop and route through OZM requirement load plus dispatch freeze before code.
2. Establish the final objective, non-goals, claim ceiling, and current request role.
3. Create or inspect the control surface set:
   - repo instructions,
   - current-state,
   - file-state manifest,
   - artifact-placement manifest,
   - route index,
   - implementation queue,
   - MainTaskLoop and MainGoalLoop indexes plus 1:1 task/goal files,
   - goal review gate standard,
   - Tasks-Reports write-boundary policy,
   - gap register,
   - source/reference adoption record.
4. Add a repo instruction Goal Runtime Reentry Gate:
   - generic continuous-progress wording such as “持续推进”, “自动推进”, “直至完成”, `continue until done`, or standing autonomy activates the OZM agentic coding loop / standing-autonomy contract as current-thread text control, not `create_goal` or native Codex Goal;
   - native Goal mode applies only when the user explicitly asks for native Codex Goal, `/GOAL`, or `create_goal`, or when an active Goal already exists and must be treated as a carrier;
   - after compaction, resume, long wait, handoff, replay, replacement, role switch, or explicit native Goal continuation, future threads must reopen `ozone-manager`, current-phase OZM child skills, mandatory companions, repo instructions, and active owner truth surfaces before tool calls or file mutation;
   - require a compact receipt with `goal_carrier`, `hydration_epoch`, `loaded_child_skills`, `mandatory_companions`, `current_queue_revision`, `current_packet`, `claim_ceiling`, and `next_authorized_action`;
   - if fresh post-compaction hydration cannot be confirmed, the project must stop at `reentry-unbound` / `child_skill_hydration_missing`.
5. Add a repo instruction Agentic Coding Loop Output Discipline:
   - when the project enters an agentic coding loop, standing-autonomy run, explicit native Goal continuation, or file-driven implementation loop, routine progress messages must not explain the process or repeat the plan;
   - ordinary loop progress must output only execution action, result, and current state summary no longer than five lines;
   - OZM stops, user-facing blockers, final closeout, requested plans, requested audits, and error reports may still use the detail required by their gate;
   - this is an output-discipline contract only. It does not waive hydration receipts, dispatch freeze, subagent/review classification, claim ceiling, or closeout.

## Project Surface Map

New-project setup must leave a project surface map: intended root, instruction surfaces, TruthDocs/control docs, active task/goal loop, environment entrypoint, reference/adoption surfaces, smoke/probe script roots, archive/history roots, and first dispatch candidate. Without the map, the project stays at `truthdocs_planning_only`.
6. Apply Standard Template A when the project is a local-first MCP/agent IDE, governed coding runtime, or comparable agentic workbench. Load `references/standard-template-a.md` for the detailed template.
7. Require explicit technology-stack decisions before implementation packets:
   - frontend, desktop shell, backend, database, MCP runtime, provider route, docs app, WASM boundary, test/proof toolchain, environment entry.
8. Use UX/UI sections as applicability-gated references, not as a universal project mandate. If UI/UX, Image-2, UIREF, component atlas, browser proof, visual parity, or user-facing frontend work is in scope, require UX interaction decisions before implementation or image/reference adoption:
   - user-state analysis,
   - visible-copy rules,
   - surface ownership,
   - layer and coordinate contracts,
   - state-machine and event contracts,
   - responsive, resize, and collision rules,
   - keyboard/focus and accessibility,
   - browser/desktop verification states,
   - generated image/UIREF adoption gates.
   If UI/UX is not in scope for the first packets, record `ux_scope=not_applicable_or_deferred` and do not force Template A's workbench surface model into the project structure. If a different UI model is chosen, record adopt/adapt/reject posture and route later visual work to `ozm-ux-ui-expert-suite`.
9. Require a script, smoke/probe, and proof matrix before implementation-ready wording:
   - each planned stable script names owner, inputs, outputs, dependencies, failure classes, tests, and non-claims.
   - ad hoc smoke/probe/inspector/harness scripts default to scratch/Temp placement and can be promoted into source only by explicit controller admission as stable `source_wrapper` records with typed-API boundaries, output contracts, negative cases, and non-claims.
10. Require final-development coverage before broad full-development claims:
   - every final acceptance row maps to an `MTL-*` / `GL-*` owner,
   - broad planned loops split into bounded child packets,
   - final release cannot close from prose, screenshots, harness-only proof, or self-review.
11. Require a standing-autonomy and goal-runtime contract when the user expects run-until-done, all-task automatic advancement, heartbeat/scheduler continuation, or mission-level execution permission:
   - activation source,
   - current-thread versus background carrier posture,
   - one bounded packet per evaluator pass,
   - hard stops,
   - checkpoint cadence,
   - latest-request override,
   - report/controller-update split.
12. Record rejected routes explicitly, especially MVP-first, ungoverned provider calls, image-only proof, UI/UX template over-application, background execution without a carrier, repeated explanatory loop narration that dilutes execution focus, unsupported independent audit, and docs that are too thin to drive future agents.
    - For startup checks without tool events, set audit_carrier=same-thread-review.
13. Update navigation surfaces whenever adding a new owner document.
14. Close with exact files changed, claim ceiling, unresolved gaps, and next admissible packet.

## Standard Template A

Load `references/standard-template-a.md` when:

- creating a project startup pack from scratch;
- auditing whether a plan is too thin for agentic coding loops;
- standardizing Tauri + React + Rust + PostgreSQL + MCP + provider governance;
- writing UX interaction templates for a PanGu-like or workbench-style IDE when UI/UX is in scope;
- adding Image-2, UIREF, component-atlas, or deep-research automation governance;
- defining environment dependency routes and script/smoke placement matrices;
- defining MainTaskLoop/MainGoalLoop, Tasks-Reports, final coverage, audit declaration, or standing-autonomy/goal-runtime contracts.

Use Template A as a strong default for comparable local-first governed workbenches, not a universal mandate. Apply its common control-surface, task/goal, placement, environment, script, and autonomy rules broadly; apply its UI/UX structure only when the project has user-facing UI/UX scope or when the owner explicitly adopts that model. If a project chooses a different stack or UX model, record the deviation, reason, owner, and claim-ceiling effect instead of silently drifting.

## Hard Gates

Reject or downgrade:

- MVP-grade or thin planning that lacks owner docs, task order, acceptance, verification, or script contracts.
- Technology stack prose without exact package/runtime boundaries.
- UX references based only on attractive images or brand pages instead of source/evidence and interaction states.
- UI/UX workbench structure applied as a hidden default when the current project has no admitted UI/UX scope or has selected a different UI model.
- Generated Image-2 outputs treated as implementation proof.
- Provider or deep-research automation without fake-provider tests, secret refs, cost/rate policy, and retention posture.
- Environment/tool lookup that bypasses the project environment entrypoint.
- Ad hoc smoke/probe/inspector/harness scripts persisted under source roots or stable script directories without explicit `source_wrapper` admission.
- Future-agent read routes that require bulk-loading the entire doc corpus.
- Main task and goal loops that are not 1:1 or lack a blocking review gate.
- Ordinary development threads that can mutate controller truth outside a selected task report.
- Final full-development claims without acceptance-row-to-task/goal coverage and child packetization for broad loops.
- Standing authorization treated as background execution, queue advancement, controller-truth mutation, independent review, or permission to bypass bounded packet gates.

## Output Shape

For a new project startup package, produce or update:

- control-surface map,
- technology-stack contract,
- UX interaction contract when UI/UX is in scope or explicitly adopted,
- provider/deep-research route contract when relevant,
- environment dependency route,
- implementation packet ladder,
- task/goal loop and review-gate standard,
- standing-autonomy/goal-runtime contract, repo-instruction reentry gate, and routine loop output discipline when run-until-done behavior is desired,
- core script matrix with smoke/probe scratch-vs-`source_wrapper` placement,
- gap register,
- current-state and route-index entries,
- acceptance checklist.

For an audit, lead with P0/P1/P2 gaps, then name exact documents or templates to add.

For a template-only request, output the reusable template and state how future threads should read it.

## Project Boot Matrix And Clean-Room Gate

New project setup must capture repo structure, package manager, install command, test command, lint command, environment entrypoint, secrets posture, deployment posture, docs, CI, and owner surfaces. Without install/test command or first closeout resume/verify instructions, claim only setup candidate.


## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
- `references/template-a-ui-ux-reference.md` only when Template A UI/UX, Image-2, UIREF, component atlas, browser proof, visual parity, or user-facing frontend detail is admitted for the project.
