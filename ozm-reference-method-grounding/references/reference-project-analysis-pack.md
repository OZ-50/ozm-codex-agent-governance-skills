# Reference Project Analysis Pack

Use this when a project, framework, engine, product, prior implementation, or local sibling is named as a reference.

## Source Classification

Classify each source before deriving work:

- `authoritative_requirement`: owner-designated source that defines target behavior.
- `implementation_donor`: source implementation that may shape target structure after portability review.
- `method_donor`: source method or algorithm that may be adopted or adapted.
- `benchmark`: source used for comparison, not direct adoption.
- `design_inspiration`: visual or UX inspiration only.
- `historical_sibling`: related history that informs risk but is not current truth.
- `background_only`: context that cannot govern execution.

Only `authoritative_requirement`, `implementation_donor`, and `method_donor` can affect execution depth without explicit owner promotion.

## Runtime Capability Structure

Build a source-first map with evidence pointers:

- entrypoints and runtime carriers
- state authority and ownership
- state transitions
- algorithms, policies, scoring rules, or method primitives
- scheduling, workers, queues, ticks, or async loops
- persistence and readback
- provider, external, environment, or data seams
- UI/API execution seams
- negative, recovery, security, and performance behavior
- verification seams and existing test/proof surfaces
- owner-truth and configuration surfaces

## Target Truth Map

Do not copy donor architecture by default. Synthesize target truth from:

- target owner requirements
- explicit non-goals
- local runtime shape
- language/framework constraints
- deployment or environment constraints
- portability and anti-transplant constraints
- multi-reference common, variant, incompatible, and architecture-bound nodes

The target truth map, not a union of donor maps, owns later packet admission.

## Unavailable Sources

If a reference cannot be read deeply enough, record:

- missing surface
- attempted access
- uncertainty
- safe lower claim
- whether the reference remains background-only or can be revisited later
