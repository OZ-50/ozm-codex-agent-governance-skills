# Reconstruction Bundle Contract

Use this reference when OZM-governed work analyzes a reference repository deeply enough to guide implementation.

## Required Artifacts

- `implementation_reconstruction.md`
  - repo identity, question, entrypoints, clusters, runtime loops, state model, important variables, thresholds, unknowns
- `config_dependency_surface.md`
  - dependencies, launch surfaces, environment variables, config files, services, storage, provider seams, overrides
- `effect_surface_report.md`
  - user-visible outcome, UI/API/runtime surfaces, state-to-effect projection, evidence, gaps
- `borrowability_integration_plan.md`
  - adopt now, adapt with redesign, reference only, reject, integration plan, overclaim guards
- `evidence_ledger.json`
  - source anchors, claims, mechanism rows, config sources, runtime paths, effect evidence, borrowability rows, unknowns

## Optional Artifacts

Use when scope demands:

- `major_cluster_map.md`
- `project_remainder_map.md`
- `bundle_readiness_assessment.md`
- `functional_parity_plan.md`
- `mechanism_fidelity_audit.md`
- `code_volume_and_loop_analysis.md`
- `source_backed_gap_ledger.json`

## Readiness Terms

- `analysis_ready_for_runtime_slice`: enough source anchors and mechanism rows exist to plan one bounded local implementation slice.
- `analysis_ready_for_replication`: core runtime mechanisms, config, state, effect, and failure/recovery behavior are extracted with remaining gaps bounded.
- `analysis_ready_for_integration`: borrowability rows, target-owner requirements, and integration constraints are mapped.
- `implementation_core_reproduced`: target code implements the selected mechanism through a real seam.
- `parity_validation_ready`: functional parity tests/proofs are defined and executable.
- `functional_parity_validated`: parity proof has run through accepted target evidence.

Do not collapse analysis readiness into implementation or parity states.

## Evidence Rules

- every major claim needs concrete source anchors
- implementation facts, config facts, runtime-path facts, effect facts, and borrowability judgments stay separate
- borrowability comes after reconstruction
- unknowns stay in the remainder map
- validator success proves shape only, not depth

## Failure Rule

If required artifacts are missing, mostly templated, source-anchor sparse, or concept-compressed, downstream OZM must keep the ceiling below `analysis_ready_for_runtime_slice`.
