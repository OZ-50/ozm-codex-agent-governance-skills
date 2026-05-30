---
name: ozm-text-io-integrity
description: Use for OZM-governed text file writes, generated reports, skill files, Markdown/JSON/YAML/config edits, Windows or PowerShell encoding boundaries, mojibake, newline drift, BOM handling, oversized inline payloads, chunked writes, and safe text preflight before positive claims.
---

# OZM Text I/O Integrity

Text-write integrity skill for OZM work. Use it when the work writes or repairs text where encoding, newline style, shell transport, payload size, or generated-file growth can corrupt the control surface or source artifact.

This child absorbs the common-case workflow from `encoding-fix`. The old donor id is historical. OZM owns request role, write authority, proof class, and claim ceiling.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-governed text file writes, generated reports, skill files, Markdown/JSON/YAML/config edits, Windows or PowerShell encoding boundaries, mojibake, newline drift, BOM handling, oversized inline payloads, chunked writes, and safe text preflight before positive claims."
  blocks_when:
    - generated text write lacks encoding/newline/readback posture
    - oversized payload is written without chunk/manifest boundary
  required_artifacts:
    - text_preflight_report
    - chunk_manifest
    - round_trip_hash_receipt
  downstream_binding:
    - ozm-record-surface-management.text_write_receipt
    - ozm-closeout-handoff.artifact_integrity
  proof_or_script:
    - scripts/text_preflight.py and hash/readback receipt
  claim_effect:
    - separates written, readback_verified, and content_integrity_verified
  non_surface_failure_code:
    - ozm-text-io-integrity_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed text writes, generated text, Markdown/JSON/YAML/config edits, multilingual files, Windows/PowerShell shell I/O, mojibake, newline/BOM drift, oversized inline payloads, or chunk assembly. |
| Minimum input | target path, existing/new file posture, intended authority class, write method, size risk, encoding/newline expectation, and rollback or re-run path. |
| Allowed actions | Inspect text conventions, choose safe write transport, run preflight/safe-write/chunk scripts, record warnings, and lower claims when integrity proof is missing. |
| Forbidden actions | Do not rely on implicit shell redirection, nested PowerShell hosts, unbounded here-strings, or whole-file replacement when convention/size risk is unclassified. |
| Output receipt | Record target, encoding, BOM posture, newline style, warnings, write method, max-size guard, post-write preflight, and claim effect. |
| Downstream handoff | Hand off to the active OZM owner, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling` when text integrity affects acceptance. |
| Claim ceiling effect | May hold or lower claims to `text_integrity_unverified`, `encoding_risk`, `newline_risk`, `oversized_transport_risk`, or `safe_write_verified`. |
| Lineage | Child of `ozone-manager`; portable OZM rewrite of the archived `encoding-fix` donor. |

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.

- `references/powershell-encoding.md` for PowerShell-specific encoding behavior.
- `references/text-io-donor-map.md` for donor absorption, source basis, and preserve/reject decisions.

## Workflow

1. Classify the write: existing file edit, new file, generated report, shell capture, chunk assembly, or repair after corruption.
2. For existing files, run preflight before overwrite and preserve encoding, BOM posture, and newline style unless the packet explicitly owns a migration.
3. For new files, choose `utf-8` without BOM and repo-consistent newlines unless a consumer requires another convention.
4. Select the safest transport: `apply_patch` for small repo edits, OZM safe-writer scripts for generated text, chunk split/assembly for oversized payloads, and explicit encodings for shell captures.
5. Stop using one giant inline command when a command literal is likely above 6000 characters, an `apply_patch` is likely above 24000 characters, or one hunk is likely above 150 changed lines.
6. Avoid nested `powershell.exe`, `cmd /c powershell`, or detached PowerShell wrappers for ordinary text work. Change transport shape before changing shells.
7. Re-run preflight after writing. Treat replacement characters, embedded BOMs, NULs, mixed newlines, mojibake markers, unexpected encoding, or sudden size/line-length jumps as blockers unless explicitly accepted with lowered wording.
8. Before positive closeout, leave a text integrity receipt or state why the touched files did not need this gate.

## Scripted Checks

Use the bundled scripts through a resolved interpreter, not bare `python` on Windows:

```powershell
& '<resolved-python>' <skills-root>\ozm-text-io-integrity\scripts\text_preflight.py <path> --json
& '<resolved-python>' <skills-root>\ozm-text-io-integrity\scripts\safe_write_text.py <path> --stdin --encoding utf-8 --newline lf
& '<resolved-python>' <skills-root>\ozm-text-io-integrity\scripts\split_text_chunks.py --text-file <candidate> --output-dir <chunks> --prefix <name>
& '<resolved-python>' <skills-root>\ozm-text-io-integrity\scripts\assemble_text_chunks.py <target> --parts-glob <chunks>\*.part.txt --preserve-existing
```

Script pass is text-integrity proof only. It does not prove semantic correctness, authority, acceptance, or product readiness.

## Round-Trip Hash And Chunk Manifest Gate

Large or multilingual writes require preflight before writing and readback after writing. If chunking is used, keep a chunk manifest with assembly order, expected hash, actual hash, encoding, newline policy, and fixture coverage for mixed Chinese/English, code fences, tables, and frontmatter. Without readback hash, claim only candidate write completion.

Schema detail lives in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.

## Companion Trigger Gate

Treat this child as mandatory companion for OZM-governed document drafting, skill hardening, report generation, Markdown/JSON/YAML/config edits, large Chinese/English text writes, PowerShell shell capture, chunked payload assembly, or any generated text that affects controller truth or future-agent reload.

The receipt must state `stdout_data_class`, write transport, encoding/BOM/newline posture, preflight result, post-write readback hash, and whether semantic review is still pending. A text preflight pass proves transport integrity only; it does not prove the artifact is accepted, current truth, or safe for product/runtime claims.


## Hard Rules

- Do not write through implicit `>` or `>>` when encoding or append behavior matters.
- Do not assume PowerShell 5.1 and PowerShell 7 use the same default encoding.
- Do not convert line endings as a side effect of unrelated work.
- Do not preserve mojibake because it already exists unless the current packet explicitly marks it historical-only or non-authoritative.
- Do not make a control-surface, skill, prompt, JSON, YAML, or multilingual document closeout claim after a write that skipped preflight despite visible encoding risk.
- Do not let a safe-write script pass raise claims above the active OZM owner ceiling.

## Leave With

- target files and authority class
- preflight and post-write findings
- write method and size guard
- encoding, BOM, and newline posture
- accepted warnings or blockers
- claim ceiling effect
