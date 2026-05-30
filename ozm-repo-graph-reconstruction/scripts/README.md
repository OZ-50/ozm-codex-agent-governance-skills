# OZM Repo Graph Scripts

Stable entrypoints:

- `run_understand.py`: builds or refreshes `.understand-anything/knowledge-graph.json` and optional embeddings.
- `build_js_ts_graph.py`: creates the lighter JS/TS graph artifact for targeted projects.
- `build_diff_overlay.py`: creates a one-hop changed-file impact overlay from a graph.
- `explain_graph_component.py`: explains a graph node, file, or symbol with source preview and relationships.
- `search_graph.py`: searches graph nodes and embeddings.
- `init_reconstruction_bundle.py`: creates the `.repo_analysis` reconstruction bundle skeleton.
- `validate_reconstruction_bundle.py`: validates reconstruction bundle readiness and mechanism-fidelity evidence.

Support libraries:

- `repo_graph_runtime_lib.py`: graph construction, scanning, review, and JSON helpers.
- `graph_query_lib.py`: graph loading, indexing, changed-file detection, and path normalization.
- `embedding_search_lib.py`: local embedding/search helpers.

OZM ownership:

- `ozm-repo-graph-reconstruction/SKILL.md` owns when these scripts may be used.
- Script output is navigation or candidate evidence until graph freshness, impact radius, reconstruction bundle readiness, mechanism fidelity, and claim ceiling are recorded.
