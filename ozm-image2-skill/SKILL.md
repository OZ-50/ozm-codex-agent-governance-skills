---
name: ozm-image2-skill
description: "Craft and audit GPT Image 2 / image-2 prompts and visual briefs under OZM governance. Use for prompt-only planning, image-2 brief refinement, and project asset prompt evidence posture; actual generation remains owned by imagegen."
---

# OZM GPT Image 2 Skill

Prompt-craft and reference-case routing for GPT Image 2 work; use `image-2` only when naming the model string. This skill improves the brief before generation; it does not replace `.system/imagegen`, invent API calls, or own generated-image verification.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Craft and audit GPT Image 2 / image-2 prompts and visual briefs under OZM governance. Use for prompt-only planning, image-2 brief refinement, and project asset prompt evidence posture; actual generation remains owned by imagegen."
  blocks_when:
    - prompt craft is claimed as generated/integrated asset
    - game asset lacks style, sequence, or integration boundary
  required_artifacts:
    - image2_prompt_brief
    - asset_provenance
    - visual_qa_receipt
  downstream_binding:
    - image_generation.prompt_input
    - ozm-review-diffgate-acceptance.visual_claim_boundary
  proof_or_script:
    - manual prompt/asset QA; image generation tool result when available
  claim_effect:
    - separates prompt_ready, asset_generated, asset_reviewed, and integrated claims
  non_surface_failure_code:
    - ozm-image2-skill_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed GPT Image 2 prompt craft or visual brief governance, especially image-2 prompt-only or project asset evidence posture. |
| Minimum input | image request, target use, visible text, invariants, generation/editing owner. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## OZM / Imagegen Interop

- OZM owns requirement role, artifact placement, truth owner, claim ceiling, and whether a generated asset may affect project evidence.
- This skill owns prompt shape, reference-case adaptation, text/typography constraints, and edit invariants.
- `.system/imagegen` owns actual generation/editing mode, built-in tool versus CLI fallback, save-path policy, transparency workaround, and output inspection.
- Prompt-gallery cases are inspiration and pattern evidence only. They are not proof that a new output will match.
- UI mockup images are ideation/reference artifacts unless implemented and verified in the product.

## Donor Absorption

Adopted:

- `wuyoscar/gpt_image_2_skill`: classify request first, search a gallery/category only when helpful, load craft guidance for dense text, UI, diagrams, edits, and multi-panel consistency.
- `longyunfeigu/awesome-gpt-image-2-skill`: case-index style matching for vague Chinese-context prompts, especially poster, portrait, character, UI, infographic, and social-cover requests.
- `dshark3y/gpt-image-2-skill`: parameter honesty, size/quality discipline, edit invariants, and the rule that scripts/tooling own API details.
- non-image-2 game-asset donors: prompt-style taxonomies, pixel-art constraints, tileset/atlas thinking, pose/action sequencing, transparent-sprite posture, and asset-specific validation gates.
- `0x0funky/agent-sprite-forge` as a high-weight 2D game-asset reference: asset-plan-first prompting, one-action-per-raw-sheet discipline, body/FX separation, deterministic post-processing posture, layered map contracts, prop strategy gates, collision/zone metadata, and the rule that reference mockups are not runtime deliverables.

Rejected:

- CLI-first execution as a default path. Codex already has `.system/imagegen`, and that remains the normal tool owner.
- Copying long donor galleries into this skill. Load donor repos only for archaeology or explicit prompt-case lookup.
- Treating community prompt cases as contracts, evaluation proof, or guaranteed image behavior.
- Adding unsupported parameters or downgrading model/tool path from memory.

## Workflow

1. Classify the request as `generate`, `edit`, `multi-reference edit`, `inpaint-like edit`, `prompt-only`, `batch brief`, or `reference-case search`.
2. Classify the asset type: poster/social cover, UI mockup, product/ad, infographic/diagram, character/illustration, photoreal/lifestyle, logo/brand exploration, 2D game scene, game character, spritesheet/sequence frame, VFX sprite, tile/texture asset, HUD/icon/item sheet, or research figure.
3. Extract invariants: subject, use location, exact visible text, aspect/format, input image roles, style references, must-keep elements, must-avoid elements, project destination, and whether this is preview-only.
4. Ask at most one blocking question only when exact text, target format, edit target, legal/identity boundary, or project save destination is required.
5. Load `references/prompt-craft.md` when the prompt is vague, text-heavy, layout-sensitive, edit-sensitive, or expected to be reused.
6. Load `references/use-case-patterns.md` when a concrete asset type needs a compact template or donor-inspired pattern.
7. Load `references/game-asset-patterns.md` for game scenes, characters, spritesheets, sequence-frame animation sheets, VFX sprites, tilemaps, tileable textures, HUD/icons, inventory items, or when converting Stable Diffusion / ComfyUI / Retro Diffusion / MCP game-asset prompts into image-2 brief structure.
8. For 2D game assets, treat Agent Sprite Forge-style rules in `references/game-asset-patterns.md` as higher-weight than generic image prompt patterns unless the user/project gives a stricter art pipeline.
9. Build the prompt as a production brief. Prefer dense natural language for simple creative generations; use labeled sections for complex UI, diagrams, game-asset sheets, batch prompts, or multi-image edits.
10. For edits, label every input image by role and repeat invariants: what changes, what remains, what must not be altered.
11. For Chinese or exact text, quote the exact text, specify placement and typography, avoid decorative fake text, and keep text short enough to inspect.
12. Hand the final prompt to `.system/imagegen` for generation/editing when the user wants an image, or output the prompt spec when the user asks only for prompts.
13. After generation, inspect output against subject, text, composition, style, invariants, avoid list, and game-asset constraints such as frame consistency, silhouette readability, tile seams, background removability, atlas layout, map layering, and runtime metadata readiness.

## Output Shape

For prompt-only work, return:

- `Reference posture`: donor/pattern used, adapted, rejected, or not needed
- `Prompt`: final prompt ready for imagegen
- `Imagegen posture`: built-in generation/editing path unless the user explicitly requested CLI/API
- `Exact text`: quoted visible text, or `none`
- `Invariants`: must keep / must avoid
- `Validation checklist`: what to inspect after generation

For generation work, use the normal `imagegen` skill/tool after preparing the prompt, then report the final prompt and resulting path or preview according to `.system/imagegen`.

## Image Provenance And Visual QA Gate

Separate prompt craft, source image, generated image, edited image, visual QA, and integration claim. Prompt packages do not prove generated asset quality; generated or edited assets do not prove in-product integration. Visual parity or asset-ready wording requires inspection receipt and source constraints.

Use the Image Asset Provenance fields in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.

Prompt audits should also record negative prompt intent, style boundary, asset consumer, iteration criteria, source-image roles, and generated-asset proof posture. If the work only produces a prompt, the ceiling is `prompt_ready`; `asset_generated`, `asset_reviewed`, and `integrated` require an actual image tool result, file/provenance receipt, QA inspection, and product/runtime consumer evidence respectively.


## Hard Rules

- Do not call an image CLI/API or write one-off SDK scripts from this skill. Use `.system/imagegen` for execution.
- Do not silently switch tool path, model, transparency mode, output format, or project save policy.
- Do not copy a donor prompt verbatim unless the user asks for that exact prompt/case and the source context is acceptable; adapt the structure instead.
- Do not add real brands, celebrities, copyrighted characters, personal identity claims, or political endorsements unless the user supplied and authorized them.
- Do not promise exact text rendering. Treat text accuracy as something to inspect and iterate.
- Do not treat generated images, prompt cases, screenshots, gallery labels, or style tags as product proof.
- Do not let a prompt broaden project scope. When a generated asset belongs to a governed project, keep the final objective, placement, and claim ceiling explicit.
- Do not use generic negative prompts as a substitute for positive composition and invariant instructions.
- Do not paste Stable Diffusion, ComfyUI, Retro Diffusion, LoRA, CFG, seed, sampler, `prompt_style`, or MCP parameter blocks into image-2 prompts. Convert their useful intent into natural visual constraints, layout, invariants, and avoid lists.
- Do not promise production-ready animation, tileset, or transparent sprite output from a generated image alone. Generated sheets are candidate art until inspected, sliced, post-processed, and tested in the target game context.
- Do not treat an Agent Sprite Forge-style request as permission to run its donor scripts or install donor skills unless the user explicitly asks for that execution path. In this skill, Agent Sprite Forge is a high-weight prompt/planning reference; `.system/imagegen` and admitted project tooling still own generation and processing.

## Reference Map

- `references/trigger-scope.md`: full trigger/use-case list kept out of frontmatter to avoid broad image/UI/game false positives.
- `references/prompt-craft.md`: prompt structure, text handling, edit invariants, iteration gates, and validation checklist.
- `references/use-case-patterns.md`: compact patterns for posters, Chinese social visuals, UI mockups, products, diagrams, characters, research figures, and batch briefs.
- `references/game-asset-patterns.md`: 2D game scene, character, sprite, sequence-frame, VFX, tile/texture, HUD/icon, item-sheet, and non-image-2 prompt conversion patterns.

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
