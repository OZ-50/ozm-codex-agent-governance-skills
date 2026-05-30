# Text I/O Donor Map

Use this reference only when auditing why `encoding-fix` was absorbed or when restoring donor behavior.

## Source Basis

- Microsoft documents that Windows PowerShell and PowerShell 6+ differ in default text output encoding, BOM behavior, append behavior, and no-BOM reads. OZM therefore must avoid implicit redirection when text integrity matters.
- The archived `encoding-fix` donor supplied the practical preflight, safe-write, split, and assemble scripts. OZM keeps those scripts locally so the normal path does not depend on an external donor id.

## Adopted

- Preflight before overwriting existing text.
- Preserve existing encoding, BOM, and newline conventions unless a migration is explicit.
- Prefer `apply_patch` for small repo edits.
- Use safe writer or chunk assembly for generated text and large payloads.
- Treat mojibake markers, replacement characters, embedded BOM, NULs, mixed newlines, and line-collapse risk as blockers.
- Avoid nested Windows PowerShell for ordinary text writes.

## Adapted

- Donor-specific command examples are converted to `<resolved-python>` and `<skills-root>`.
- The donor's standalone skill trigger becomes an OZM child route and claim-ceiling gate.
- Text integrity proof is separated from semantic acceptance.

## Rejected

- Treating `encoding-fix` as an always-on external skill for OZM work.
- Making every small Markdown edit run all scripts when no encoding, newline, size, shell, or multilingual risk exists.
- Using encoding proof to raise code, document, or acceptance claims.

## Restore Posture

The donor may be restored only for explicitly standalone, non-OZM text-write work. OZM-governed work should route to `ozm-text-io-integrity`.
