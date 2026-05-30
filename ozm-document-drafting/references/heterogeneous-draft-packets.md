# Heterogeneous Draft Packets

Use this reference when a long draft should adapt during writing instead of following a fixed read-plan-write-review sequence.

## Packet Shape

```json
{
  "packet_id": "DRAFT-P3",
  "task_type": "retrieval | reasoning | composition | revision | verification",
  "input_surfaces": [],
  "output_surface": "",
  "section_scope": [],
  "reason_for_task_type": "",
  "done_condition": "",
  "next_allowed_types": []
}
```

## Task Types

- `retrieval`: source gap, unknown-unknown, citation, file read, or paper/web search.
- `reasoning`: compare evidence, resolve tension, choose argument order, derive section contract.
- `composition`: write or rewrite prose from ready claim/evidence rows.
- `revision`: apply registered reader/editor issues to a known section.
- `verification`: check claim/evidence, issue closure, section depth, or closeout readiness.

Do not continue composition when evidence or reasoning gaps are still blocking the section's claim ceiling.
