# PowerShell Encoding Notes

Use this reference when the task involves PowerShell reads, writes, pipes, redirection, or subprocesses that may emit non-ASCII text.

## Execution routing

Prefer Codex-native execution over external Windows PowerShell hosts.

- First choice: `apply_patch` for repo edits.
- Second choice: the bundled Python writers and validators in `scripts/`.
- Third choice: Codex's built-in shell execution in the current session.

Do not launch `powershell.exe`, `Start-Process powershell`, or similar wrappers for ordinary one-shot file or text tasks. That creates another encoding boundary and makes behavior less predictable.

Allow external Windows PowerShell only when the task genuinely depends on external resident state, such as:

- A Windows PowerShell-specific profile or host configuration
- A module or host integration unavailable in the current Codex shell
- A user request that explicitly requires Windows PowerShell

When that exception applies, keep the external command minimal and continue to enforce explicit encodings at the boundary.

## Session normalization

```powershell
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding
```

Add explicit defaults when a session will write multiple files:

```powershell
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Add-Content:Encoding'] = 'utf8'
$PSDefaultParameterValues['Export-Csv:Encoding'] = 'utf8'
```

Do not rely on shell defaults. Windows PowerShell 5.1 and PowerShell 7+ differ, and redirection can hide those differences.

## Safer write patterns

- Prefer `Get-Content -Raw` when a full file must be preserved as one string.
- Prefer `Set-Content -Encoding utf8` or `Out-File -Encoding utf8`.
- Prefer the bundled `scripts/safe_write_text.py` over bare `>` or `>>`.
- Preserve an existing file's encoding when editing a legacy or non-UTF file.
- If a here-string, patch payload, or command argument is getting large, stop embedding the whole body inline. Write numbered `.part.txt` chunks and assemble them with `scripts/assemble_text_chunks.py`.

Use conservative thresholds instead of exact platform limits:

- Switch away from inline shell literals at about 6000 characters.
- Switch away from single large patch bodies at about 24000 characters.
- Prefer about 12000 characters per chunk file.

Example:

```powershell
python .\scripts\split_text_chunks.py `
  --text-file .\candidate.txt `
  --source-encoding utf-8 `
  --output-dir .\.chunks `
  --prefix out `
  --max-chars 12000

python .\scripts\assemble_text_chunks.py .\out.txt `
  --parts-glob .\.chunks\out-*.part.txt `
  --source-encoding utf-8 `
  --encoding utf-8 `
  --newline lf
```

## Subprocesses

For Python subprocesses that print multilingual text:

```powershell
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
```

For legacy console tools that still read the active code page:

```powershell
chcp 65001
```

Use that only when the tool actually depends on the console code page.

## Common failure signals

- `�` appears after a write or round-trip read.
- `ï»¿` appears inside the file body.
- Chinese text turns into `锟斤拷`.
- Curly quotes turn into `â€™` or `â€œ`.
- A multi-line file collapses into one extremely long line.
- A large patch or command is rejected before the intended tool logic runs.
- The same long command starts working once the embedded body is shortened.

Treat those as blockers and rerun `scripts/text_preflight.py`.

For the last two, check payload size and transport shape before blaming the PowerShell version. In practice they usually indicate inline-length or bridge-transport limits.
