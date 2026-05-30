# Game Asset Patterns

Use this reference for 2D game scenes, characters, spritesheets, sequence-frame animation sheets, VFX sprites, tilesets, tileable textures, HUD/icons, item sheets, and prompt conversion from non-image-2 game-asset sources.

## Reference Weight

For 2D game assets, `0x0funky/agent-sprite-forge` is a high-weight reference because it treats generation as an asset pipeline rather than a single image prompt.

Use this precedence when rules conflict:

1. Current user/project art direction and engine contract.
2. Agent Sprite Forge-style game-asset pipeline rules in this file.
3. Other game prompt donors such as Retro Diffusion, Stable Diffusion, ComfyUI, tilemap tools, and game-asset MCP prompt packs.
4. Generic character, poster, texture, or illustration prompt patterns.

This does not make Agent Sprite Forge a runtime dependency. In OZM image-2 work it donates prompt planning, asset contracts, post-processing posture, and validation gates. Actual generation remains owned by `.system/imagegen`; deterministic slicing, alpha cleanup, GIF export, metadata, and engine wiring require separately admitted project tooling.

## Donor Ideas Absorbed

- Agent Sprite Forge: asset-plan-first prompting, one coherent action family per raw sheet, body/FX separation for controllable heroes, visible-reference handoff, magenta/chroma-key posture, deterministic cleanup/slicing/export, layered map contracts, prop-pack strategy gates, collision/zone metadata, and reference-mockup-not-runtime-output discipline.
- Retro Diffusion style taxonomies: game asset, UI panel, item sheet, character turnaround, isometric, top-down, platformer, skill icon, tile, tileset, small sprite, walking/idle, attack, jump, destroy, subtle motion, and VFX animation.
- Stable Diffusion prompt templates: icons, RPG skill icons, fantasy items, landscape/scene concepts, and high-contrast graphic icon language.
- ComfyUI pixel-art workflows: low-resolution pixel grammar, palette limitation, blocky sharp pixels, downscale/palette cleanup, and avoiding photoreal/high-resolution noise.
- Tilemap generators: swatch -> tile render -> tile variation -> tilemap thinking, inside/outside texture separation, and game-engine tile assembly.
- Game asset MCP tools: character sheet, character variation, pixel art character dimensions, seamless texture, object sheet, transparent background posture, and generated reference views.
- Pose/action systems: sequence prompts should name the action, frame count, direction, pose progression, and neutral starting pose when needed.

These are donor patterns, not image-2 API parameters. Convert them into visual constraints and validation checks.

## Convert Non-Image-2 Prompts To Image-2 Briefs

Do not paste model-specific syntax into image-2 prompts. Convert it as follows:

| Non-image-2 source | Convert to image-2 structure |
| --- | --- |
| `prompt_style`, LoRA, model names, sampler, CFG, seed, steps | Drop as parameters; keep only the visual intent, asset type, style family, palette, perspective, and constraints. |
| positive prompt tags | Convert to natural phrases: subject, projection, silhouette, material, lighting, style, palette, layout. |
| negative prompt tags | Convert to `Avoid:` constraints. Keep only asset-relevant negatives. |
| `tile_x`, `tile_y`, seamless flags | Prompt `seamless/tileable texture with matching edges, no focal object, no borders`; inspect seams after generation. |
| OpenPose / ControlNet / pose text | Convert to `pose/action sequence`, frame order, and preserve body proportions across frames. |
| transparent background flags | Prompt a flat removable chroma-key or plain background; let `.system/imagegen` own actual transparency/removal. |
| `spriteSheet`, `return_spritesheet`, atlas/grid flags | Prompt a contact sheet / sprite atlas with explicit rows, columns, cell padding, consistent baseline, and no overlapping frames. |
| IP-heavy style references | Replace with generic genre language: `MOBA-like`, `dark fantasy RPG`, `retro console`, `arcade platformer`, `anime mobile RPG`, etc. |

Preferred image-2 game brief shape:

```text
Asset type: <2D scene / character sheet / sprite sheet / VFX sheet / tileable texture / HUD icon / item sheet>
Game use: <where it appears in gameplay>
Camera/projection: <side-view / top-down / 3/4 top-down / isometric / orthographic / UI icon>
Canvas/layout: <single asset / grid / rows x columns / tile size / frame count / safe padding>
Subject: <main content>
Style: <pixel art / hand-painted / anime RPG / flat vector-like / painterly fantasy / sci-fi UI>
Palette/materials: <color count, palette family, materials, glow, outline>
Motion or frame plan: <only for spritesheets/VFX>
Background: <transparent-ready chroma key / plain solid / no background scene / gameplay scene>
Invariants: <silhouette, proportions, camera, baseline, palette, item identity>
Avoid: <watermark, text, logos, IP, photoreal noise, cropped objects, frame overlap>
Validation: <what to inspect before using in game>
```

## Agent Sprite Forge Pipeline Rules

Use these rules whenever the requested output is a sprite, animation sheet, prop sheet, map, tilemap, layered scene, side-view stage, or playable prototype art pack.

Asset plan before prompt:

- Classify `asset_type`, `action`, `view`, `sheet`, `frames`, `bundle`, `art_style`, reference role, and expected runtime use before writing the image prompt.
- Pick the smallest useful output. A single idle sheet, a spell bundle, a prop pack, a layered map, and a complete engine atlas are different contracts.
- Decide whether the output is `preview`, `candidate asset`, `reference mockup`, `processed asset`, or `integrated project asset` before making a claim.

Creative source and processing boundary:

- The raw visual asset should come from image generation, not code-drawn placeholder geometry, screenshots, SVG, Canvas, Three.js, or PIL shapes.
- Scripts and local tools may be useful later for chroma-key cleanup, slicing, alignment, GIF/PNG export, placement metadata, collision, and previews, but those are deterministic processing steps, not creative prompt substitutes.
- When a downstream cleanup path exists, prefer a solid flat `#FF00FF` chroma-key background for isolated sprites, props, and sheets. When no cleanup path is admitted, use a plain removable background and keep the claim at candidate art.

Reference handoff:

- If an image reference matters, make the image visible in the conversation context before generation. Do not rely on a filesystem path string as the visual reference.
- State the reference role explicitly: preserve identity, preserve map style, animate the same subject, make a prop matching the map, create an evolution, or derive a scene object.
- Preserve identity markers such as silhouette, palette, face/eyes, costume marks, material language, camera, terrain boundaries, horizon, entrances, and exits.

## Sprite Pipeline Discipline

Use for players, NPCs, monsters, props, summons, projectiles, impacts, spells, FX, and animation sheets.

One action family per raw sheet:

- Do not ask image generation to create unrelated hero actions in one raw atlas just because an engine wants a `4x4`, `5x5`, or custom atlas.
- For controllable heroes, main characters, and high-value player assets, generate one action grid at a time, inspect it, then assemble a delivery atlas only after each action passes.
- A raw `4x4` is valid for canonical four-direction locomotion when every row is the same walk/run action in a different direction. It is not the default for mixed idle/run/attack/jump rows.

Body and effect separation:

- For controllable heroes and fixed-cell runtimes, keep attack/shoot/cast body sheets body-only by default.
- Generate wide slash arcs, muzzle flashes, projectiles, impact bursts, dust clouds, long weapon trails, and detached FX as separate `fx`, `projectile`, or `impact` sheets unless the runtime explicitly supports wider per-action cells and origin metadata.
- Reject or revise a body-action output when a wide FX bounding box makes the body visibly smaller than accepted idle/run scale.

Grid and containment defaults:

- Avoid raw single-row `1x4`, `1x6`, `1x8`, or `1xN` sheets for characters, players, controllable heroes, creatures, NPCs, enemies, summons, or animated props because horizontal drift and cropping are likely.
- Prefer compact multi-row grids for animated bodies: `2x2` for 4 frames, `2x3` for 6 frames, `2x4` for 8 frames, `3x3` for 9 frames, and `3x4` or `4x4` for longer coherent sequences.
- Keep the body centered in each cell, full body inside the central safe area, same scale and outline thickness, stable feet/bottom anchor when visible, and generous removable background margin.
- Nothing should cross cell edges: limbs, weapons, hair, capes, smoke, particles, sparks, tails, wings, or trails.

High-value defaults:

- Standard idle: `2x2`.
- Cast: `2x3`.
- Impact/explosion: `2x2`.
- Top-down four-direction walk: `4x4`, rows down/left/right/up.
- Side-view compact walk/run: `2x2` or `2x3`.
- Boss/large creature idle: `3x3`.
- Spell bundle: separate cast, projectile, and impact assets.
- Hero action bundle: separate idle/run/attack or shoot/jump/body sheets, plus separate projectile, slash, muzzle, dust, and impact assets when needed.

## Map And Scene Pipeline Discipline

Use for top-down RPG maps, monster-taming routes, tower-defense lanes, survivors arenas, tactical boards, side-scroller stages, Metroidvania rooms, parallax backgrounds, tilemaps, and layered scenes.

Do not treat playable maps as one image:

- If the user asks for a playable map, level, stage, room, prototype, engine scene, editable map, or collision-aware scene, a single baked image is only a background, reference, or preview artifact.
- Playable output needs explicit runtime structure: tile layers, separate props, platform objects, object placement, collision, zones, exits, spawn hooks, camera bounds, parallax layers, or engine-native scene nodes.
- Use a flat baked image only for title screens, visual novel backgrounds, boss-room concept art, fixed battle backgrounds, decorative backdrops, or when the user explicitly asks for a single flat image.

Mode selection:

- `tile_mode`: editable tile/grid maps for RPGs, monster-taming routes, platformers, tactical maps, and engines that already use tiles.
- `scene_mode`: foundation/base map plus separate props for top-down exploration, tower defense, survivors arenas, and base-map-plus-props workflows.
- `side_scroll_mode`: parallax layers plus separate platform/object/collision data for side-scrollers, runners, brawlers, shooters, and Metroidvania rooms.
- `grid_mode`: rule-heavy board, tactical, factory, automation, terrain-cost, or build-grid scenes.
- `room_chunk_mode`: reusable room/chunk art with exits, sockets, collision, spawn markers, and seam validation.
- `baked_scene_mode`: fixed non-editable visual backgrounds only.

Layer separation:

- Base/foundation layers should contain only stable non-interactive terrain, paths, roads, water, cliffs, low markings, floor patterns, distant scenery, or non-colliding depth.
- Do not bake runtime-controlled objects into the base: tall props, buildings, trees, signs, doors, gates, pickups, chests, hazards, traps, ladders, foreground occluders, actors, enemies, NPCs, bosses, UI, labels, or anything needing collision, y-sort, animation, replacement, reuse, or independent render order.
- If generation bakes runtime objects into the base, demote that image to concept/reference or regenerate a cleaner foundation-only base.

In-world reference mockup:

- For layered maps and side-view stages, generate a sparse in-world reference mockup from the visible base/background before final object production.
- The mockup should preserve camera, framing, dimensions, horizon, terrain boundaries, paths, entrances, exits, and landmarks.
- The mockup must be natural in-world art, not an annotated diagram. Avoid arrows, labels, circles, callouts, legends, highlighted boxes, measurement marks, UI text, or captions.
- Keep the mockup to the most important visible runtime object candidates, usually no more than 9 distinct object types unless the user asks for a larger pass.
- Reference mockups are planning artifacts only. Do not ship them as the final runtime map when separate props, collision, y-sort, editable objects, or engine data are required.

Post-reference object gate:

- After a mockup exists, create an object list from the visible mockup and base: id, type, approximate position, approximate size, render layer, collision role, and asset strategy.
- Generate or define final platforms, terrain chunks, props, hazards, pickups, doors, gates, checkpoints, exits, foreground occluders, and scene objects separately.
- Store placement, collision, zones, scene hooks, camera bounds, exits, and spawns as structured metadata instead of inferring them from pixels.
- Compose a QA preview from the original base/background plus final runtime objects.

Prop strategy gate:

- Use square `2x2`, `3x3`, or `4x4` prop packs only for compact props such as rocks, shrubs, barrels, crates, lamps, small signs, pots, debris, or small ornaments.
- Do not put wide/long, tall/large, collision-bearing, platform, floor, bridge, wall, ladder, gate, door, hazard, road, rail, or tileset/strip pieces into square prop packs.
- Use one-by-one generation for large, important, irregular, animated, identity-sensitive, or collision-aligned props.
- Use platform strips or tileset-like atlases for repeatable floors, platforms, roads, walls, slopes, corners, and terrain pieces.
- If a square pack fails because an object touches an edge, reclassify the object and regenerate with a better strategy; do not pass it by relaxing QC.

Side-scroll and parallax:

- Choose one `stage_canvas` before generation; primary parallax layers, stage reference, and QA preview should share the same aspect and framing.
- Treat parallax layers as scenery only. Walkable floors, platforms, ladders, hazards, pickups, doors, gates, checkpoints, foreground blockers, actors, and UI belong in runtime object layers, not the background.
- If a side-view background contains obvious collidable foreground geometry, reject it as a runtime background or regenerate a cleaner scenery-only layer.

## 2D Scene And Environment

Use for side-scroller backgrounds, top-down maps, isometric maps, battle arenas, parallax layers, overworld scenes, dungeon rooms, and gameplay backdrops.

Key constraints:

- State projection first: side-view, top-down, 3/4 top-down, isometric 45-degree, orthographic platformer, or cinematic concept art.
- Separate playable space from decorative space: readable paths, lanes, platforms, foreground/background layers, collision-friendly silhouettes.
- For parallax, ask for layers as a sheet or separate horizontal bands: far background, midground, gameplay plane, foreground overlays.
- For maps, state grid logic, tile size intent, landmarks, entry/exit points, and whether it is a minimap, tactical map, or visual scene.
- Avoid poster composition when the user needs in-game readability.

Template:

```text
Create a 2D game environment scene for <gameplay use>. Projection: <side-view/top-down/isometric>. The scene shows <biome/location> with <landmarks>. Gameplay readability: clear walkable paths, obstacle silhouettes, foreground/background separation, and uncluttered interaction zones. Style: <pixel/hand-painted/anime/flat>. Palette: <palette>. Lighting: <mood>. Background/layout: <single scene / parallax layer sheet / map view>. Avoid text, logos, watermark, photoreal noise, confusing perspective, and poster-like framing.
```

Validation:

- gameplay path and focal areas are readable
- perspective is consistent
- layers or tile logic can be separated
- no unrequested text/IP/logo appears

## 2D Character And Character Sheet

Use for player/enemy/NPC concepts, pixel characters, portraits, turnarounds, expressions, pose sheets, equipment variants, and multi-view reference sheets.

Key constraints:

- State game role and scale: playable hero, enemy, boss, NPC, summon, companion, UI portrait, overworld sprite.
- Lock the silhouette and identity before costume detail.
- For pixel sprites, name target pixel feel and cell size intent: 16x16, 32x32, 48x48, 64x64, or 96x96 visual target.
- For turnarounds, request front/back/left/right or 8-direction views on a grid with matching proportions.
- For expression/pose sheets, require same face, outfit, palette, and body proportions across all cells.

Template:

```text
Create a 2D game character sheet for <character role>. Layout: <single hero pose / 4-view turnaround / 8-direction view / expression and pose grid>. Character: <silhouette, clothing, weapon, props, personality>. Game style: <pixel art / anime RPG / hand-painted fantasy / sci-fi tactical>. Camera/projection: <front view / 3/4 top-down / side-view>. Keep the same proportions, face, outfit, palette, and silhouette across all cells. Use generous padding and a plain removable background. Avoid extra characters, text, logos, cropped limbs, inconsistent costume details, and IP-specific references.
```

Validation:

- silhouette reads at target scale
- all views look like the same character
- feet/baseline and camera angle are consistent
- no cell overlaps or cropped limbs

## Sequence-Frame Animation And Spritesheets

Use for idle, walk, run, jump, attack, hit reaction, death, cast, interact, crouch, roll, or custom action sheets.

Image-2 can create a candidate spritesheet/contact sheet, but it cannot guarantee production animation. Treat output as candidate art until sliced and tested.

Key constraints:

- Prefer one action per generation.
- State rows/columns, frame count, direction count, and cell padding.
- Use a neutral starting pose for action cycles when possible.
- Keep camera, scale, baseline, silhouette, costume, lighting, and palette constant.
- Describe frame progression in plain language, not model parameters.
- For multi-direction walking, ask for separate rows by direction.

Common layouts:

- idle loop: one row by four frames
- walk cycle: four rows by four frames, rows = down/left/right/up
- run cycle: one row by six or eight frames
- attack: one row by six frames, wind-up -> strike -> follow-through -> recover
- hit/death: one row by six frames, impact -> stagger -> fall -> settle

Template:

```text
Create a 2D game sprite animation sheet for <character>. Action: <idle/walk/run/jump/attack/hit/death/custom>. Layout: <rows by columns>, each cell evenly spaced with clear padding. Frame plan: <describe ordered pose progression>. Camera/projection: <side-view / top-down three-quarter / front-facing>. Keep the same character identity, costume, proportions, outline thickness, palette, lighting, scale, and feet baseline across every frame. Plain removable background. Avoid frame overlap, cropped limbs, extra characters, changing outfit details, motion blur that hides silhouette, text, logos, and watermark.
```

Validation:

- frames can be sliced cleanly
- action reads in order
- character identity does not drift
- baseline and scale are stable
- no frame has missing limbs or extra props unless intended

## VFX Sprite And Effects Sheet

Use for fireballs, slashes, explosions, hit sparks, aura loops, lightning bolts, portals, healing pulses, smoke puffs, dust trails, water splashes, magic circles, and impact decals.

Key constraints:

- State gameplay purpose and blend behavior: projectile, impact, loop, cast, environmental ambience, UI feedback.
- Use a dark, black, white, or chroma-key solid background only when it helps extraction; execution remains owned by `.system/imagegen`.
- Describe motion phases: anticipation, core burst, peak, decay, dissipate.
- Keep shape center, scale envelope, color palette, and cell spacing consistent.
- Avoid full cinematic scenes; VFX sprites need isolated readable effects.

Template:

```text
Create a 2D game VFX sprite sheet for <effect>. Gameplay use: <projectile/impact/cast/loop/decal>. Layout: <rows x columns> with evenly spaced cells. Frame plan: anticipation -> build-up -> peak -> decay -> fade. Visual style: <pixel/hand-painted/anime/mobile RPG>. Palette: <colors>. The effect is isolated, centered, readable at small size, with clear alpha-ready edges on a plain removable background. Avoid characters, environments, text, logos, watermark, cropped effects, noisy particles outside cells, and inconsistent scale between frames.
```

Validation:

- effect remains isolated and extractable
- peak frame is visually readable
- frames progress smoothly
- no unwanted scene/background elements appear

## Tiles, Tilesets, And Tileable Textures

Use for terrain tiles, dungeon tiles, platformer blocks, top-down map surfaces, isometric tiles, object-on-tile assets, seamless textures, and material swatches.

Key constraints:

- For a single texture, prompt seamless/tileable matching edges and no focal object.
- For a tileset, state tile size intent, terrain types, inside/outside transition, corners/edges/center variants, and grid layout.
- For tile objects, request isolated assets with consistent projection and a plain background.
- Treat generated tilesets as candidates; inspect seams and engine slicing before use.

Templates:

```text
Create a seamless 2D game texture tile for <material>. Projection: <flat top-down / side-view platform block / isometric surface>. Style: <pixel/hand-painted/stylized>. The texture must be tileable on all edges, with repeating detail, no central focal object, no border, no text, and no watermark. Keep lighting neutral and material detail readable at small scale.
```

```text
Create a 2D game tileset atlas for <biome/material>. Layout: clean grid of tile variants including center, edges, corners, transition tiles, and small decorative tile objects. Projection: <top-down/isometric/side-view>. Style: <style>. Keep each tile aligned, evenly spaced, and visually compatible. Avoid perspective drift, labels, characters, logos, watermark, and non-grid composition.
```

Validation:

- seams are not obvious
- tile variants share palette/projection
- no border or focal center breaks repetition
- atlas cells can be sliced

## HUD, Icons, Items, And Inventory Sheets

Use for ability icons, inventory items, weapons, consumables, quest objects, UI buttons, HUD panels, status effects, and game logo-like labels when authorized.

Key constraints:

- Prefer strong silhouette, centered object, padding, controlled background.
- For sets, keep same lighting, border, icon scale, material language, and palette.
- Avoid real franchise style names; use generic genre descriptors.
- For text labels, keep text minimal and inspect manually.

Template:

```text
Create a 2D game asset sheet of <item/icon set>. Layout: <grid size> evenly spaced cells. Each cell contains one centered asset with clear silhouette, matching scale, consistent light direction, shared palette, and generous padding. Style: <painted RPG icon / pixel item / sci-fi HUD / flat vector-like UI>. Background: plain removable or simple icon frame. Avoid text, logos, watermarks, IP-specific designs, clutter, cropped assets, and inconsistent perspective.
```

Validation:

- each cell contains one sliceable item/icon
- scale and style match across the set
- silhouettes read at small size
- no unrequested text/IP/logos appear

## Game-Asset Output Checklist

Before claiming a generated game asset is usable:

- classify it as preview, candidate asset, reference sheet, or accepted project asset
- inspect at intended game scale, not only full-size
- confirm background removability or actual alpha after post-processing
- confirm slicing grid, padding, and frame/cell boundaries
- confirm projection consistency
- confirm silhouette readability
- confirm no IP leakage, watermark, or unrequested text
- for spritesheets, test frame order after slicing
- for tiles, test seam and repeat behavior
- for VFX, inspect peak frame, decay, alpha edge, and gameplay readability
- for hero/player action bundles, confirm each action sheet passed separately before any combined engine atlas is accepted
- for playable maps, confirm base/foundation, final objects, placement metadata, collision/zones, and QA preview are separate enough for the runtime
- for layered maps, confirm the dressed/stage reference is not being used as the final runtime map
- for prop packs, confirm every accepted cell matches the requested object and no accepted prop touches a cell edge
- for side-scroll maps, confirm parallax layers and stage preview share the planned canvas or have explicit normalization metadata
