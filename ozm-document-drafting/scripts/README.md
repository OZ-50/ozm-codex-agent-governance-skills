<!-- Agentic discoverability surface for OZM document-drafting scripts. -->

# OZM Document Drafting Scripts

Public interface:

- `claim_evidence_check.py`: validates one claim/evidence/argument matrix before a strong text claim can be accepted.
- `draft_quality_gate.py`: validates the draft matrix, issue registry, and optional concept map before draft closeout.

Owner contract: these scripts are deterministic structural gates for `ozm-document-drafting`; they do not fetch network sources, rewrite artifacts, or decide prose style.
