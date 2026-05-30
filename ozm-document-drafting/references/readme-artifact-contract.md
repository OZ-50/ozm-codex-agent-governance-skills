# README Artifact Contract

Use this reference when an OZM-governed draft creates, rewrites, or reviews a README.

## General README Gate

Before writing, record:

- project type and primary reader
- reader first action: install, run, evaluate, integrate, contribute, or maintain
- source refs for commands, entrypoints, config, examples, and support channels
- freshness risk for code symbols, CLI flags, package names, screenshots, badges, and generated examples
- claim ceiling for unverified commands or stale references

GitHub surfaces README files prominently for repository visitors, so OZM treats README text as a navigation and onboarding surface, not a private note.

## Required Coverage

- what the project does
- why it is useful for the target reader
- fastest getting-started path
- basic usage through a real public seam
- configuration or options when they exist
- tests, verification, or examples when the README asks users to trust behavior
- support, maintenance, contribution, or license posture when the repo owns those surfaces

## Ruby Gem / Ankane-Style Preset

Apply this preset only when the request is for a Ruby gem README, Ankane-style README, or equivalent concise gem documentation.

- Preferred order: header, tagline, badges, Installation, Quick Start, Usage, Options if needed, Upgrading if applicable, Contributing, License.
- Use imperative, concise prose.
- Keep examples single-purpose; one code fence per concept.
- Keep options tables compact and avoid placeholder badges without a visible replacement marker.
- Remove HTML comments before closeout.

Do not apply the 15-word sentence rule as a global OZM document policy. It is a style preset, not an evidence or acceptance gate.

## Acceptance

README acceptance requires both document quality and freshness posture:

- Commands, filenames, exported symbols, package names, and config keys are sourced or verified.
- Strong claims have evidence rows or lowered wording.
- Known stale or unverified examples are marked non-claim or blocked.
- Style polish cannot raise the artifact above the active claim ceiling.
