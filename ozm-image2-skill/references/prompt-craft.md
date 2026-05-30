# Prompt Craft

Use this file when an image-2 request needs more than a simple one-line prompt.

## Prompt Shape

A reliable prompt answers these questions in order:

1. Intended use: poster, UI mockup, product ad, concept sheet, infographic, research figure, preview asset, or project asset.
2. Canvas and composition: aspect, framing, subject placement, negative space, panel count, hierarchy.
3. Subject and scene: what appears, where it is, what it is doing, relevant scale.
4. Visual grammar: medium, realism level, rendering style, material, texture, camera/lens if useful.
5. Lighting and mood: natural, studio, editorial, cinematic, flat diagrammatic, clinical, playful, etc.
6. Text: exact visible text in quotes, typography, placement, density, and language.
7. Invariants: must preserve identity, layout, product geometry, brand elements, labels, camera angle, or existing image regions.
8. Avoid list: no watermark, no extra text, no fake UI labels, no distorted hands, no unrequested logos, no style drift.

Use labeled sections for complex prompts. Use dense prose for simple creative images.

## Request Classification

- `generate`: no edit target; create a new raster image.
- `edit`: change an existing image while preserving parts of it.
- `multi-reference edit`: combine, transfer, or restyle using multiple input images.
- `prompt-only`: user wants a reusable prompt, not immediate generation.
- `batch brief`: user needs several prompt variants or assets.
- `reference-case search`: user asks for gallery/case ideas or a style borrowed from a known example.

## Exact Text

For posters, infographics, UI mockups, covers, and ads:

- Put the exact text in quotes.
- Keep visible text short when possible.
- Specify text hierarchy: title, subtitle, badge, labels, captions.
- Specify placement and typography: top title, bottom caption, centered badge, large sans-serif, handwritten, calligraphy, etc.
- Add `no extra text, no pseudo-letters, no watermark` when text fidelity matters.
- Use higher-quality generation in the execution skill for dense text, diagrams, or Chinese labels.

If the user has not supplied required text, ask once instead of inventing slogans.

## Edit Invariants

For any edit or multi-reference request, write the prompt with this structure:

```text
Image roles: Image 1 is <target>; Image 2 is <style/source/object>.
Change only: <specific intended change>.
Preserve: <identity/geometry/layout/background/camera/labels>.
Match: <lighting/perspective/scale/shadows/materials>.
Avoid: <unwanted changes>.
```

Repeat the preserve list in every iteration. If identity, product label, or UI layout matters, avoid broad language such as "make it better" without a constrained change.

## Reference-Case Adaptation

Use donor/gallery prompts as skeletons:

- keep the style DNA: composition, medium, lighting, materials, typography grammar, and constraints
- replace the subject and purpose with the user's actual request
- keep usage-specific aspect cues only when they still apply
- preserve source attribution in the chat summary when the user asked for a named case
- avoid copying long prompt text unless the user requested that exact case

Do not treat a prompt case as evidence that the model will render the same quality, text, or layout.

## Iteration Gate

After generation, inspect:

- Does the subject match?
- Is exact text correct and legible?
- Is composition suitable for the intended canvas?
- Did edits preserve the invariant regions?
- Did any unrequested logos, watermarks, text, people, or extra UI appear?
- Is the asset usable at the target size and destination?

Iterate with one change at a time:

```text
Keep <successful parts>. Change only <one issue>. Preserve <critical invariants>. Avoid <observed failure>.
```

## OZM Project-Bound Assets

When the output belongs to a project:

- state whether it is preview, reference, candidate asset, or accepted asset
- do not raise project proof from the generated image alone
- save final assets through `.system/imagegen` policy
- record the prompt and output path in the owning project surface if requested or if the project workflow requires it
