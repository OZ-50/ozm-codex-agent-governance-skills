# CodeGraph Embedded Runtime Policy

The bundled `assets/codegraph-runtime` tree is a preserved backend asset, not a normal OZM skill execution path.

Default posture:

- Do not run asset scripts from ordinary `ozm-code-writing` packets.
- Do not run `local-install.sh`, `patch-tree-sitter-dart.js`, or `release.sh` without explicit operator approval and an `external_command_posture` receipt.
- Treat `npm link`, `npm install -g`, native rebuilds, `git tag`, `git push`, and `gh release create` as global or remote side effects.
- If the asset runtime is not installed or approved, repo graph claims are capped at `repo_graph_runtime_packaged_but_not_installed`.
- Asset test success proves only backend asset viability. It does not prove target repo graph freshness, impact radius, or implementation acceptance.

Required receipts before asset execution:

- `asset-runtime-manifest.json` hash match.
- External prerequisite posture for network, credentials, global writes, and approval mode.
- CodeGraph freshness or reconstruction bundle target.
- Claim ceiling that separates packaged asset, installed runtime, fresh graph, and graph-backed write admission.
