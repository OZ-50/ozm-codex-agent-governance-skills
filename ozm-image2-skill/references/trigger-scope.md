# OZM GPT Image 2 Trigger Scope

Use this reference only when deciding whether `ozm-image2-skill` is the correct OZM child or when auditing a missed/false-positive GPT Image 2 route.

## In-Scope Triggers

- explicit GPT Image 2, `image-2`, `gpt-image-2`, or image-2 prompt craft
- prompt-only visual brief refinement for a governed project
- adapting prompt-gallery or donor prompt cases into an image-2 brief
- translating non-image-2 game-asset prompts into image-2 natural-language constraints
- planning GPT Image 2 assets where artifact placement, claim ceiling, or project evidence matters
- exact-text Chinese posters, social covers, product shots, infographics, character sheets, multi-image edits, or batch visual briefs when the user asks for image-2 prompt structure
- 2D game scenes, characters, spritesheets, sequence-frame animation sheets, VFX sprites, tileable textures, HUD/icons, item sheets, and Agent Sprite Forge-style 2D sprite/map prompt planning

## Out-Of-Scope First Routes

- actual raster generation or editing: use `.system/imagegen` after the prompt is prepared
- general frontend UI implementation: use `ozm-ux-ui-expert-suite`; `ui-ux-pro-max:data-backend` is optional search/data support only after the OZM UI suite is selected
- ordinary image generation with no image-2 prompt planning or OZM evidence posture: use `imagegen`
- game runtime asset slicing, atlas packing, metadata writing, or post-processing: use the admitted project tooling or implementation lane

## False-Positive Guard

Do not trigger this skill from generic words such as image, UI, game, asset, prompt, skill, graph, route, or design unless the request also asks for image-2/GPT Image 2 prompt craft, a reusable visual brief, or OZM-governed asset prompt evidence.
