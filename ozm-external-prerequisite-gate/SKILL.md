---
name: ozm-external-prerequisite-gate
description: Use when an OZM-governed work packet depends on secrets, providers, browsers, deployments, project environment entrypoints, orchestrators, local runtimes, or remote services and must not be admitted until the prerequisite contract and reachability posture are proven.
---

# OZM External Prerequisite Gate

Prerequisite gate for governed live or remote-integrated work. Use it before admitting any slice that depends on external systems or operator setup.

Do not use this gate merely because the final roadmap, master plan, or eventual product objective contains real deployment, provider, account, or production-integration work. Use it when the current work packet itself depends on that external prerequisite for honest implementation, verification, or claim wording.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM secrets, providers, live targets, local runtimes, wrappers, or environment/tool preflight. |
| Minimum input | prerequisite list, environment entrypoint, tool path, owner permission posture. |
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
    - "Use when an OZM-governed work packet depends on secrets, providers, browsers, deployments, project environment entrypoints, orchestrators, local runtimes, or remote services and must not be admitted until the prerequisite contract and reachability posture are proven."
  blocks_when:
    - live claim depends on unknown secret/provider/account/network state
    - fallback/simulation is treated as real environment proof
  required_artifacts:
    - prerequisite_state_table
    - fallback_boundary
    - external_write_policy
  downstream_binding:
    - ozm-dispatch-freeze.prerequisite_status
    - ozm-claim-ceiling.live_claim_ceiling
  proof_or_script:
    - manual prerequisite probe receipt; scripts/credential_stdout_guard.py for script stdout/env leak scan
  claim_effect:
    - downgrades live/deployed/provider claims to diagnostic, simulated, or blocked when prerequisites are absent
  non_surface_failure_code:
    - ozm-external-prerequisite-gate_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-dispatch-freeze`, `ozm-record-surface-management`, `ozm-closeout-handoff`, and `ozm-claim-ceiling` when this gate writes controller/control surfaces, admits a packet, updates queue/current-state, produces a diagnostic/fallback/live readback report, or uses the result as progress wording

Do not load standalone `agent-browser` or `test-browser` skills merely because a prerequisite is browser-shaped. OZM owns the prerequisite contract and claim ceiling; use the current runtime's browser/test tool or project harness as an evidence carrier only after this gate records target URL, entrypoint class, console/error posture, and whether the result can support product/runtime claims.

## Workflow

1. Confirm whether the current packet is `local-complete-first`, `live-target`, `fallback-live-gap`, or `diagnostic-only`.
2. Freeze the secret or env names, ingress contract, and expected dependency posture only for a `live-target`, `fallback-live-gap`, or `diagnostic-only` packet.
3. Probe reachability and contract fit without leaking raw secrets; check env names, ignored local config, documented setup, and existing receipts before asking the user.
4. Classify the work packet as blocked, placeholder-only, locally mocked, readback-only, degraded-live, fallback-admitted, diagnostic-only, or genuinely ready for live work.
5. Classify unresolved prerequisite uncertainty as repo-readable, diagnostic-reducible, fallback-admittable, or human-owned before asking or guessing.
6. Treat the gate as passed only when the freshest probe actually proves the prerequisite posture being claimed.
7. Admit, degrade, block, or ask the minimum human-owned question based on that prerequisite posture.
8. Keep the resulting receipt separate from later implementation evidence.

## Prerequisite Schema

Each prerequisite row must name id, owner, kind, freshness, primary citation or local manifest, detection method, current state, fallback boundary, external write policy, secret posture, and claim effect. External commands use `references/external-command-posture.schema.json`; scripts that read env or may print credentials should be scanned with `scripts/credential_stdout_guard.py`. Missing or stale prerequisite rows block implementation packets that depend on them; they may support only diagnostic or local-fallback work.

## Control-Surface Admission Companion Gate

External-prerequisite work often looks read-only, but it becomes a cross-stage action as soon as it writes queue, current-state, GL/MTL, Plan/Goal, report, receipt, provider posture, or prerequisite admission records.

Before any such write or admission, freeze:

- `primary_child`: `ozm-external-prerequisite-gate`.
- `admission_posture`: blocked, diagnostic-only, fallback-admitted, degraded-live, or live-ready.
- `control_surfaces_touched`: queue/current-state/GL/MTL/report/Plan/Goal/receipt/index paths.
- `dispatch_companion`: `ozm-dispatch-freeze` loaded or explicit `not_admitting_packet`.
- `record_companion`: `ozm-record-surface-management` loaded or explicit `no_control_surface_write`.
- `closeout_companion`: `ozm-closeout-handoff` loaded before controller consumption, packet stop state, or handoff wording.
- `claim_companion`: `ozm-claim-ceiling` loaded before any `admitted`, `completed`, `passed`, `ready`, `done`, or equivalent positive wording.
- `review_companion`: `ozm-review-diffgate-acceptance` loaded when the prerequisite result affects acceptance, final PASS, or next-packet admission.

If the latest prompt says to load only the current-phase child, keep this gate as primary but still load these companions when their trigger is live. The phrase prevents full-family preload; it is not a waiver for dispatch, record, closeout, or claim ownership.

For diagnostic-only or readback-only packets, the strongest ordinary ceiling is the diagnostic/readback posture. It may justify queue progression or a safer next gate only after dispatch and record-surface owners agree the admission record is current.

## Local-Complete-First Boundary

For long-running agentic coding loops, the default order is:

1. load the current master plan and reference project basis
2. implement all locally realizable functionality in the complete project surface
3. run frontend/browser verification and local tests against the local project
4. record the remaining real-environment gaps as explicit later gates
5. start live provider, production-like environment, or cross-system integration work only when the current packet is admitted as a live-target or fallback-live-gap packet

This boundary prevents real-environment prerequisites from becoming premature blockers. It does not lower the truth rule for live claims: when the admitted target is live, a mock, placeholder, local-only smoke, or readback cannot close that target.

## Project Environment Entry And Orchestrator

When verification depends on local runtimes, WSL, Cargo, Node, browser servers, model/service wrappers, Docker, environment scripts, or project-registered tools, freeze the project environment entry before any command pack, subagent lane, or acceptance proof depends on it.

Record:

- `environment_entrypoint`: owner-approved shell/profile/script, project manifest, wrapper command, or absent.
- `orchestrator_command`: unified gate runner, project wrapper, package script, manual command pack, or absent.
- `loaded_environment_receipt`: command, cwd, shell, env names, version/readback, and redacted proof that the entry was loaded.
- `runtime_tool_posture`: available, missing, misconfigured, unknown, or externally owned.
- `subagent_environment_contract`: how delegated lanes load the same entrypoint, including `audit_receipt_id` or tool-event receipt when used as audit proof; otherwise record `audit-carrier-unavailable` / `not_available_lower_ceiling`.
- `fallback_or_diagnostic_scope`: what can run without the entrypoint and what claim ceiling applies.

If a project defines a canonical environment entrypoint or invocation wrapper, all validation and delegated proof commands should route through it unless the current packet explicitly owns environment repair. Do not rely on manual memory that Cargo, Node, browser, provider, or WSL paths are already present. A missing entrypoint is prerequisite uncertainty, not a product failure, until diagnostic proof says otherwise.

If repeated packets fail with missing tools, ENOENT, wrong shell, stale browser server, unloaded WSL/runtime profile, or subagent-only environment drift, route to dispatch freeze and record-surface management for an official orchestrator or receipt design instead of patching each command separately.

## Session Tool Preflight Cache

When a long-running loop will repeatedly run validation, browser proof, local runtime smokes, subagent audit, or gate orchestration, create a session-scoped preflight receipt before expensive proof work.

Record:

- `preflight_receipt_id`
- `environment_entrypoint_loaded`: command, cwd, shell, and redacted proof.
- `tool_versions`: required Cargo/Rust, Node/npm/pnpm, Python, browser/Playwright/CDP, WSL/Docker, project wrappers, or provider CLIs.
- `orchestrator_availability`: project runner, package script, manual command pack, absent, or control-tooling-needed.
- `browser_server_posture`: not needed, launchable, reused with reset, stale, missing, or blocked.
- `subagent_preflight_contract`: how audit/delegated lanes load the same entrypoint and where they store proof.
- `cache_scope`: session, packet, worktree, repo, or invalid after config/lockfile/environment change.
- `preflight_failures`: missing tool, wrong shell, stale server, quoting/path issue, timeout, permission, or unknown.

If repeated failures show the same missing tool, unloaded profile, stale browser, PowerShell quoting issue, Python/code-health hang, or subagent-only ENOENT, the next packet should be environment/tooling repair or orchestrator creation with a lower product claim ceiling. Do not keep treating the same preflight failure as a fresh product or implementation defect.

## Prerequisite Postures

- `live-ready`: fresh probe proves the real carrier, provider, browser, deployment, or remote service needed by the target.
- `fallback-admitted`: the live prerequisite is missing, but a bounded fallback slice can produce useful implementation or tests without pretending to be live.
- `diagnostic-only`: only safe probes, logs, readbacks, or carrier checks are admitted; no product completion or live behavior claim is allowed.
- `blocked`: progress needs a human-owned secret, external cost decision, account change, destructive operation, legal/security/privacy decision, or un-inferable acceptance criterion.

## Real-Prerequisite Rules

- If the admitted target says real PostgreSQL, sandbox, WSL, provider, browser, OS integration, or remote session, a mock cannot close that target.
- Placeholder, local mock, and readback-only paths may support fallback work only with a lowered claim ceiling.
- Fallback work may be admitted only when the receipt names the non-live posture, scope limit, and proof gap to the real prerequisite.
- Ask the user only for human-owned prerequisites: secret values, account changes, external spend, destructive remote changes, legal/security/privacy decisions, or acceptance criteria.
- For provider/API work, record direct probe status, application-route status, and degradation/fallback posture separately.
- Store secrets only in env, local secret stores, or ignored runtime config; redact or omit secret values in receipts and proof artifacts.
- If live carrier instability is observed, rerun with a bounded retry/timeout plan and classify external instability instead of rewriting product truth.
- If a local environment or orchestrator is required, prove the entrypoint/load path before treating any command failure as product evidence.

## Uncertainty Escalation Rule

Before blocking or asking the user, classify the uncertainty:

- `repo_readable`: existing docs, env samples, ignored config names, scripts, logs, or receipts can answer it
- `diagnostic_reducible`: a safe probe, readback, browser observation, or bounded smoke can reduce it without secrets or cost
- `fallback_admittable`: local-complete-first, mock, degraded, or diagnostic work can proceed with a lowered claim ceiling
- `human_owned`: secret value, account/provider change, external spend, destructive remote action, legal/security/privacy decision, or un-inferable acceptance criterion

Only `human_owned` uncertainty should become a user question or hard block. All other uncertainty should become a read, probe, fallback-admitted packet, diagnostic-only packet, or lowered claim ceiling.

## Prerequisite State Enum And Fallback Ceiling Gate

Classify every external prerequisite as `available`, `unavailable`, `unknown`, `simulated`, `blocked_by_permission`, `blocked_by_cost`, or `blocked_by_network`. Record the detection method, allowed fallback, forbidden external writes, and claim ceiling. Unknown or unavailable prerequisites cannot authorize live-target mutation.


## Hard Rules

- Do not admit a live slice while prerequisite posture is unknown.
- Do not convert an eventual live prerequisite into a default prerequisite for local-complete-first implementation.
- Do not ask for provider setup, accounts, secrets, remote sessions, or production-like services when the current packet can honestly advance local implementation and local verification without them.
- Do not guess live readiness when prerequisite uncertainty is unresolved; classify the uncertainty and either reduce it, fallback-admit it, or block/ask when it is human-owned.
- Do not treat placeholder or mock behavior as live progress.
- Do not block all progress when a bounded fallback or diagnostic-only slice can reduce uncertainty without false live claims.
- Do not ask for a secret, provider action, or browser/session step before checking whether the environment or ignored local config already satisfies the named contract.
- Do not promote a prerequisite from guessed or stale status to live-ready without a fresh probe.
- Do not let writers redefine secret names or external contracts ad hoc.
- Do not write API keys, passwords, tokens, or connection URLs containing secrets into tracked files.
- Do not let validation, browser proof, subagent audit, or local-runtime commands depend on an environment entrypoint that was only remembered in chat and not loaded or recorded in the current command receipt.
- Do not convert a missing runtime wrapper, unloaded project profile, or subagent ENOENT into a product regression without first classifying environment prerequisite posture.
- Do not start a long validation loop with repeated tool commands unless the session preflight cache or a project orchestrator proves the required entrypoints and tools are available, or the claim is explicitly lowered to diagnostic-only.
- Do not let the same missing-tool, wrong-shell, stale-browser, quoting/path, or subagent environment failure repeat across packets without routing to an environment/tooling repair posture.
- Do not write queue/current-state/GL/MTL/report/Plan/Goal/receipt/index control surfaces from this gate without also satisfying the dispatch and record-surface companion posture, or explicitly recording that no admission/control write occurred.
- Do not close or report a diagnostic-only, fallback-admitted, degraded-live, or live-ready prerequisite result as progress without closeout and claim-ceiling companions when that wording affects controller consumption, next-packet admission, or future-thread state.

## Leave With

- the frozen prerequisite contract
- the control-surface admission companion posture when any queue/current-state/GL/MTL/report/receipt/index record was touched
- the environment entrypoint, orchestrator command, and loaded-environment receipt when local tools or runtimes are part of the proof
- the session tool preflight cache when repeated validation, browser proof, subagent audit, or gate orchestration is expected
- the reachability and posture result
- any fallback-admitted or diagnostic-only scope limit
- the uncertainty class and whether it was reduced, fallback-admitted, or human-owned
- the admission or block decision

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
