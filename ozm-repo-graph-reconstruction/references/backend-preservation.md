# Backend Preservation And Donor Boundary

Use this reference when deciding whether to use OZM-managed assets, preserved external skills, or manual fallback.

## Default Owner

`ozm-repo-graph-reconstruction` owns:

- graph freshness
- graph artifact schema
- reconstruction bundle schema
- impact-radius admission
- mechanism fidelity
- backend degradation posture
- claim ceiling
- downstream binding into OZM dispatch/write/review

## Archived Restore Backends

`repo-knowledge-graph`:

- archived as a restore-only specialist backend for older Understand-Anything style graph workflow detail
- not the normal OZM route target
- may be restored/read only when OZM-managed scripts are insufficient and the user explicitly asks for donor archaeology or backend-parity comparison

`repo-analysis-deep-reconstruction`:

- archived as a restore-only specialist backend for older `.repo_analysis` bundle repair and deep reconstruction references
- not the normal OZM route target
- may be restored/read only when a reconstruction bundle needs donor-specific archaeology that the OZM bundle contract cannot cover

## OZM-Managed Runtime

`assets/codegraph-runtime/` is the OZM-managed copy of the CodeGraph CLI/MCP runtime source. Use it as a local asset source, not as an always-running service.

Do not claim CodeGraph MCP is available unless a current runtime command, MCP config, or status output proves it.

## Fallback Ladder

1. Fresh CodeGraph MCP or CLI output with source anchors.
2. OZM-managed graph scripts and `.understand-anything` artifacts.
3. Archived backend restore for specialist workflow archaeology, with lowered claim ceiling.
4. Manual `rg`/file read reconstruction with lowered claim ceiling.
5. Blocked: missing repo root, unavailable source, or unsupported analysis question.

## Restore And Archive Posture

The backend skills are not active default-shelf skills after absorption. OZM route rules must target the OZM child first and may list backend aliases only as archived restore targets with fallback to this child.
