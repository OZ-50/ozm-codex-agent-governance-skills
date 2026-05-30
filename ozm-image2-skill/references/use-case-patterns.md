# Use-Case Patterns

Load only the relevant section for the current request.

## Chinese Poster Or Social Visual

Use when the user asks for 小红书配图, 公众号封面, 海报, 城市推广图, or Chinese cultural/editorial visuals.

Prompt ingredients:

- vertical or cover canvas with clear title area
- region/cultural subject stated concretely
- illustration/photo/editorial medium
- exact Chinese title and subtitle, if any
- typography style and placement
- clean negative space, no extra pseudo text, no watermark

Template:

```text
Create a <canvas/use> for <subject>. Use <medium/style> with <regional/cultural details>. Composition: <layout and hierarchy>. Text: title "<exact title>" at <placement>, subtitle "<exact subtitle>" at <placement>. Typography: <style>. Avoid extra text, pseudo-characters, watermark, logos, and clutter.
```

## UI Mockup Or App Concept

Use when the user wants an app/web screen, dashboard concept, mobile UI, or design-system panel image.

Prompt ingredients:

- device or frame if desired
- screen purpose and primary user workflow
- key regions: navigation, list/table, cards, chart, controls, empty/loading/error state if needed
- design language: dense operational, editorial, playful, financial, game-like, etc.
- text policy: exact short labels or no tiny unreadable copy

Template:

```text
Create a realistic <mobile/web/dashboard> UI mockup for <product/workflow>. The screen shows <main state>. Layout: <regions>. Controls: <specific controls>. Visual style: <design system tone>. Text must be short, legible, and limited to: "<labels>". No fake brand logos, no watermark, no unreadable placeholder text.
```

OZM note: generated UI images are reference artifacts. They do not replace implemented UI, browser screenshots, or design-system proof.

## Product Or Ad Creative

Use for product shot, packaging, commercial poster, e-commerce visual, or ad creative.

Prompt ingredients:

- product identity without unauthorized real brands unless supplied
- material, finish, scale, label fidelity
- scene, surface, lighting, lens/camera if photoreal
- slogan only when supplied
- no extra logo/text/watermark

Template:

```text
Create a polished product image for <product>. Show <product details> on <surface/scene>. Lighting: <studio/editorial/natural>. Composition: <framing>. If text is present, use only "<exact text>". Preserve label clarity and product geometry. Avoid extra logos, watermark, distorted packaging, and fake claims.
```

## Infographic, Diagram, Or Research Figure

Use for research figures, method diagrams, architecture diagrams, field guides, data explainers, or educational visuals.

Prompt ingredients:

- audience and topic
- layout: flow, grid, comparison, map, exploded view, timeline
- label count and exact labels
- visual hierarchy and color discipline
- no invented data unless the user supplies it

Template:

```text
Create a clear <infographic/diagram/research figure> explaining <topic> for <audience>. Layout: <flow/grid/timeline>. Include exactly these labels: "<label 1>", "<label 2>", "<label 3>". Use clean hierarchy, readable typography, restrained colors, and diagrammatic clarity. Do not invent numeric data, citations, logos, or extra labels.
```

## Character, Illustration, Or Concept Sheet

Use for character art, reference sheets, style boards, game/NPC concepts, comic panels, or illustration sets.

Prompt ingredients:

- character role, silhouette, clothing, props, pose, expression
- sheet layout: single portrait, turnaround, expressions, inventory, panels
- style/medium and rendering level
- identity consistency across panels
- avoid copyrighted characters unless user-authorized

Template:

```text
Create a <single image/reference sheet/panel set> for <character>. Include <pose/layout/panels>. Visual style: <medium>. Key details: <silhouette, clothing, props, palette>. Keep identity consistent across panels. Avoid extra characters, watermark, unrequested logos, and style drift.
```

## Photoreal Or Lifestyle Image

Use for natural photos, editorial scenes, portraits, interiors, fashion, food, or travel.

Prompt ingredients:

- camera/framing/lens only if helpful
- real-world lighting and texture
- restrained retouching
- concrete environment
- no impossible anatomy or over-polished "AI" skin

Template:

```text
Create a photorealistic image of <subject> in <scene>. Camera/framing: <angle/lens/framing>. Lighting: <natural/studio/time of day>. Texture details: <materials/fabric/skin/surface>. Mood: <tone>. Avoid watermark, extra text, plastic skin, distorted anatomy, and unrequested objects.
```

## Multi-Image Edit Or Composite

Use when the user supplies two or more images for style transfer, object insertion, product mockup, virtual try-on, or compositing.

Template:

```text
Image 1 is <target/base>. Image 2 is <source/style/object>. <Image 3...>
Change only <specific target region/change>. Use <source image role> to <transfer/insert/restyle>. Match lighting, perspective, scale, shadows, and material interaction. Preserve <identity/layout/product geometry/background/camera angle>. Avoid changing <critical regions>, adding extra objects, watermark, or text.
```

## Game Assets

For 2D game scenes, characters, spritesheets, sequence-frame animation sheets, VFX sprites, tilemaps, tileable textures, HUD/icons, or item sheets, load `game-asset-patterns.md` instead of using the generic character or texture templates here. The game reference contains stronger rules for projection, frame consistency, silhouette, background removal, tile seams, atlas layout, and conversion from non-image-2 prompt packs.

## Batch Briefs

Use when the user asks for many assets or variants. Make one prompt per distinct asset; do not use one vague umbrella prompt for all assets.

Each item should contain:

- asset id
- intended use
- prompt
- exact text
- size/aspect hint
- invariants/avoid
- validation target
