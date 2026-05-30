# RFMC Capsule Contract

Each capsule should include these surfaces unless the extraction ceiling is explicitly lower:

- `RFMC.md`: asset summary, type, status, claim ceiling, fit, quick adoption path, and non-claims.
- `provenance.md`: source project, source paths, evidence refs, authoring context, license/security notes.
- `interface.md`: public API, integration contract, inputs, outputs, extension points, and unsupported cases.
- `dependencies.md`: packages, runtime, services, data, secrets posture, environment prerequisites.
- `variability.md`: configurable points, assumptions, project-specific cleanup, and non-goals.
- `portability-smoke.md`: smoke target, steps, observed result, and next proof gate.

## RFMC Index Row

```json
{
  "asset_id": "stable-domain-id",
  "type": "function | module | component | pattern | template | adapter | example | incubating | deprecated",
  "path": "relative/or/configured/path",
  "status": "extraction_candidate | prototype_extracted | portability_smoked | adopted | deprecated",
  "claim_ceiling": "same as status or lower",
  "source_project": "project name",
  "source_refs": ["path#symbol-or-section"],
  "evidence_refs": ["receipt/test/review/doc"],
  "dependencies": ["runtime/package/service"],
  "portability_smoke": "missing | planned | run_failed | run_passed",
  "lifecycle": "active | incubating | deprecated",
  "updated_at": "YYYY-MM-DD"
}
```

## Source Proof

Every reusable capsule needs source proof before it can be advertised as reusable:

- source project or repository
- source file and symbol or section refs
- accepted behavior receipt, test, screenshot, or review evidence
- known stale or unverified assumptions
- license, security, and dependency notes

If source proof is missing, the capsule ceiling is `extraction_candidate`.

## Reuse Boundary

State what is portable, what must be adapted, and what must not be copied:

- public interface and intended consumer
- supported inputs, outputs, and failure modes
- project-specific names, brands, routes, storage, or providers to remove
- target environment prerequisites
- non-goals and unsupported cases

## Deprojectization Checklist

- names and brands
- routes and URLs
- environment variables and config
- credentials/secrets posture
- storage paths and schema assumptions
- UI copy and locale assumptions
- service/provider dependencies
- test fixtures and sample data
- target-project integration steps

## Acceptance Receipt

Close an RFMC extraction with a receipt containing:

- capsule path and index row id
- source proof refs
- deprojectization result
- portability smoke status
- remaining non-claims
- next adoption gate
