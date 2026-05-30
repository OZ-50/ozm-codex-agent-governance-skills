# Template A UI/UX Reference

This file contains the applicability-gated UI/UX, visible-copy, Image-2, UIREF, and atlas portions of Standard Template A. Load it only when the new project has admitted UI/UX, Image-2, UIREF, component atlas, browser proof, visual parity, or user-facing frontend work.

## 6. UX Interaction Standard

Use this section when the project has admitted UI/UX, Image-2, UIREF, component atlas, browser proof, visual parity, or user-facing frontend work. It is a reference structure for comparable workbench-style products, not a universal architecture mandate. If UI/UX is absent or deferred, record `ux_scope=not_applicable_or_deferred` and do not force workbench surfaces into the project. If another UI model is selected, record adopt/adapt/reject posture and route later visual work to the OZM UX owner.

Run user-use and state analysis before UI styling. UX planning is insufficient unless it names the user's repeated work loop, each admitted surface owner, the surface's layout contribution, its state machine, event handlers, layer order, motion rules, copy source, and verification evidence.

UX artifact floor:

| Artifact | Required Contents |
| --- | --- |
| `TruthDocs/ux-user-state-model.md` | primary users, repeated work loops, decision points, interruptions, recovery moments, fatigue risks |
| `TruthDocs/ux-surface-inventory.md` | all permanent, temporary, floating, docked, modal, tooltip, and diagnostic surfaces |
| `TruthDocs/ux-interaction-contract.md` | state machines, events, keyboard routes, pointer behavior, drag/resize rules |
| `TruthDocs/ux-layer-coordinate-contract.md` | coordinate bases, z-index tokens, collision rules, scroll owners, safe areas |
| `TruthDocs/ux-copy-contract.md` | copy classes, visible labels, redaction rules, locale posture, forbidden leakage |
| `TruthDocs/ux-reference-adoption.md` | source-read reference behavior, adopted/rejected UIREF elements, image/reference limits |
| `TruthDocs/ux-verification-matrix.md` | screenshots, DOM checks, accessibility checks, resize checks, focus/keyboard proof |

User work-loop template:

| Field | Required Answer |
| --- | --- |
| primary loop | what the user repeatedly does for 30-120 minutes |
| scan target | what they must recognize in under 3 seconds |
| switch target | which panes, modes, tools, or records they switch between |
| interruption | notification, blocker, provider wait, review request, error, conflict |
| recovery | how the user returns to the prior task without losing context |
| confidence signal | what tells the user the action is safe, pending, blocked, or complete |
| fatigue control | density, contrast, motion, and noise constraints for long sessions |
| novice path | how first-run users avoid dead ends without tutorial prose in the main UI |
| expert path | keyboard, command palette, recent objects, pinned panes, bulk actions |

Surface contract template:

| Field | Required Definition |
| --- | --- |
| `surface_id` | stable id such as `top-hub`, `left-rail`, `left-overlay`, `canvas`, `right-companion`, `global-dock` |
| user job | one sentence: what user question this surface answers |
| owner | frontend component/module or future owner doc |
| permanence | permanent, transient, modal, floating, docked, tooltip, toast |
| layout contribution | fixed track, flex pane, absolute overlay, fixed viewport layer, portal |
| coordinate basis | viewport, shell, rail, canvas, right companion, anchor element |
| scroll owner | none, self, parent, virtual list, canvas viewport |
| input model | pointer, keyboard, command palette, touch, drag, resize |
| state set | exact states from the state-machine table below |
| copy source | copy catalog keys, not ad hoc debug strings |
| accessibility | role, label, focus entry, focus return, keyboard equivalent |
| collision rule | how it behaves near rail, splitter, dock, popover, tooltip, and viewport edge |
| persistence | whether width, tab, selection, scroll, and position survive restart |
| proof | screenshot states, DOM assertions, keyboard checks, visual regression target |

Reference UX model for a governed IDE/workbench:

| Surface | Standard Template A |
| --- | --- |
| top hub | fixed compact global status and commands |
| left primary rail | narrow icon-first rail, stable width, tooltip-backed |
| left secondary overlay | floating popover/overlay by default; consumes zero layout width |
| center canvas | primary work area, independent scroll owner |
| center/right splitter | visible draggable and keyboard-resizable boundary |
| right companion | contextual claim/receipt/provider/help/audit pane, resizable/collapsible |
| center-bottom local tray | local workspace tray; if present, its left edge must be explicitly tied to rail or canvas boundary |
| bottom global dock | small floating object shelf, not a footer, console, banner, or permanent bottom panel |
| floating windows | bounded helper surfaces with drag/resize/escape behavior |
| tooltip/tip layer | non-occluding, timed, focus-compatible |

Detailed surface defaults:

| Surface | Layout And Interaction Contract |
| --- | --- |
| top hub | Fixed shell row, about 56-72px high. Owns global status, global commands, profile/notification affordances, and route-level mode switch. It must not absorb local canvas tools or debug readouts. Overflow uses icon menu or command palette, not wrapping rows. |
| left primary rail | Fixed shell column, about 48-64px wide. Icon-first, one active item, hover/focus tooltip, keyboard roving index, visible disabled state, no text pills. Active indication must be readable without relying only on color. |
| left secondary overlay | Portal or absolute overlay anchored to the rail and top hub. It contributes zero layout width, must not move the canvas, splitter, right companion, center-bottom tray, or global dock. It closes through outside click, Escape, rail toggle, or selection when configured. |
| center canvas | Primary work owner. It owns selection, zoom/pan when applicable, local scroll, empty state, loading state, and object focus. It must remain usable when the left overlay is open. |
| center/right splitter | Boundary owner between canvas and right companion. Hit zone can be wider than the visible line. Must support pointer drag, keyboard resize, double-click reset if admitted, and min/max bounds. |
| right companion | Contextual inspector/audit/helper pane. Resizable, collapsible, and independently scrollable. It must not own global navigation or provider acceptance. Sections have collapse state, loading, empty, error, and stale-data states. |
| center-bottom local tray | Local to the canvas/work area. Its anchor must be named as `canvas-left`, `rail-right`, or another explicit coordinate. It must not be indented by a temporary left overlay. It must not pretend to be the global dock. |
| bottom global dock | Fixed/floating viewport layer centered on the chosen basis, usually the full viewport unless a project-specific contract says otherwise. It is a compact object shelf, not a footer/banner/log console. Hover/focus expansion must not reflow the shell. |
| floating window | Portal/floating layer with drag handle, bounds, resize handles if admitted, focus management, close/restore, and saved or reset position policy. It must not hide critical blockers without an alternate route. |
| modal dialog | Highest blocking interaction layer. Requires focus trap, labeled title, Escape/close policy, explicit destructive confirmation, and focus return. |
| popover/menu | Anchored transient layer with collision handling, outside-click policy, Escape close, and keyboard navigation. |
| tooltip | Non-interactive hint layer by default. Requires delay, collision handling, reduced-motion compatibility, and pointer-event safety. |
| toast/status | Temporary status surface. Requires severity, timeout, action link policy, and log/receipt linkage when the message matters later. |

Interaction inventory required before admitted UI implementation:

| Interaction | Required Definition |
| --- | --- |
| primary rail item | icon, selected state, tooltip, keyboard focus, disabled state |
| secondary left surface | overlay anchor, open/close triggers, outside click, escape behavior, z-index, zero layout contribution |
| top hub command | icon/text policy, active state, notification state, overflow behavior |
| right companion section | collapse behavior, resizing bounds, scroll owner, empty/error/loading states |
| center canvas node/list/table | selection model, drag affordance, keyboard alternative, zoom/pan if applicable |
| splitter | pointer drag, keyboard resize, min/max pane constraints, persistence |
| bottom global dock | viewport-centered or explicitly anchored basis, hover/focus expansion, collision rule |
| center-bottom local tray | anchor basis, overlap rule with rail/overlay, resize rule, scroll owner |
| floating window | drag handle, resize handles, focus trap when modal, escape/close, restore position |
| modal/popover | modality level, dismissal, focus return, portal root |
| toast/status | severity, timeout, action, log linkage |
| command palette | scope, filtering, keyboard shortcuts, provider/action eligibility labels |

State-machine template:

| State | Required UX Rule |
| --- | --- |
| `default` | visible affordance and stable size |
| `hover` | subtle visual feedback; must not be the only discoverability path |
| `focus-visible` | keyboard-visible ring or equivalent, no layout shift |
| `active/pressed` | immediate feedback for command execution or drag start |
| `current` | user's location in nav/workflow |
| `selected` | object selection distinct from current route |
| `expanded` | content revealed with named scroll owner and close path |
| `collapsed` | compact representation still exposes restore affordance |
| `loading` | skeleton/spinner/progress chosen by expected duration |
| `empty` | next safe action, not feature explanation prose |
| `error` | recoverable message, retry/copy/report action, redacted details |
| `warning/stale` | non-blocking risk with source/time when relevant |
| `disabled` | reason available through tooltip/status when not obvious |
| `dragging` | cursor, ghost/preview, drop target, cancel route |
| `resizing` | live or throttled preview, min/max, snap/reset if admitted |
| `overflow` | scroll, menu, truncation, or collapse strategy |
| `offline/unavailable` | degraded posture and blocked actions |
| `read-only` | explains why editing controls are unavailable |
| `modal-blocked` | background inertness and focus trap |

Event contract template:

| Event | Required Definition |
| --- | --- |
| click/press | command, selection, toggle, open, or navigation; avoid mixed meanings |
| double click | admitted only when needed; provide single-click/keyboard alternative |
| hover | preview or hint only; no hover-only critical action |
| focus | tab order, roving focus, focus restoration, visible indicator |
| keyboard | shortcuts, Escape behavior, arrow navigation, Enter/Space activation |
| drag | start threshold, preview, legal targets, cancellation, accessibility fallback |
| resize | pointer handle, keyboard path, persistence, min/max, collision behavior |
| scroll | owner, virtualization, sticky headers, scroll restoration |
| outside click | which transient surfaces close and which stay pinned |
| context menu | scope, keyboard invocation, destructive action placement |
| route change | state persistence, stale selection cleanup, focus target |
| notification | severity, badge count, toast, right companion entry, or receipt log |

Layer contract:

1. Base shell grid owns permanent layout.
2. Secondary overlay is absolute/floating and must not move splitters or compress panes.
3. Dock is fixed/floating and must not become a layout row.
4. Floating windows and tooltips have explicit z-index and hit-test rules.
5. Coordinate bases must be named: viewport, shell, canvas, rail, companion, or owning anchor.

Z-index and pointer-safety template:

| Layer Token | Owner | Pointer Rule |
| --- | --- | --- |
| `z-base` | shell grid, permanent panes | normal hit testing |
| `z-rail` | primary rail and top hub | above base, below transient overlays |
| `z-left-overlay` | secondary rail overlay | blocks only its own bounds; outside click closes when configured |
| `z-right-companion` | companion pane | normal pane hit testing |
| `z-global-dock` | bottom global dock | fixed hitbox; expansion must not steal unrelated pointer events |
| `z-popover` | menus and popovers | anchored, outside click/Escape policy |
| `z-floating-window` | floating tools | movable, focus-managed, bounded |
| `z-tooltip` | tooltips | pointer-events none unless explicitly interactive |
| `z-toast` | status toasts | does not cover primary command zones when avoidable |
| `z-modal` | modal dialogs | background inert, focus trapped |

Coordinate and collision rules:

- Choose a named basis for every fixed or absolute surface before design generation.
- A temporary overlay must not create grid columns, flex tracks, pane margins, or resized splitters.
- The bottom global dock keeps its declared basis while overlays open and close.
- Local trays remain tied to the canvas/work area and do not inherit the left overlay's temporary width.
- Splitter hit zones must remain reachable when overlays, docks, or floating windows are present.
- Tooltip/popover collision behavior must be tested at all four viewport edges and near the dock.

Motion contract:

| Motion | Default Rule |
| --- | --- |
| overlay enter/exit | 120-180ms opacity/translate; reduced-motion uses instant or opacity-only |
| dock expand/collapse | 120-180ms transform/width; no shell reflow |
| pane resize | direct pointer response; avoid delayed animation while dragging |
| splitter reset | optional 120ms transition after pointer release |
| tooltip | 400-700ms show delay, fast hide, no motion-only meaning |
| toast | 150-220ms enter, timed exit only for non-critical messages |
| modal | short fade/scale or instant under reduced motion |
| canvas pan/zoom | performance-budgeted; preserve reduced-motion fallback |

Responsive and scaling rules:

| Condition | Required Behavior |
| --- | --- |
| desktop default | all permanent workbench regions visible unless user collapsed them |
| narrow desktop | right companion can collapse before the canvas loses its minimum usable width |
| tablet/narrow viewport | left secondary overlay becomes modal or full-height sheet only if recorded |
| high text scaling | labels wrap/truncate with tooltip or detail route; buttons do not clip text |
| high DPI | icon stroke and hit target remain readable |
| reduced motion | all animated state changes remain understandable |
| low contrast risk | color-only signals gain shape, icon, label, or pattern |

Default geometry floor:

| Token | Floor |
| --- | --- |
| top hub | about 56-72px |
| rail width | about 48-64px |
| rail button | about 44x44px |
| dock item | about 44-48px |
| compact action height | about 34-36px |
| right companion | about 300-380px default |
| dense shell body | about 14px |
| readable body | about 16px |
| compact metadata | 11-12px only for short metadata |

Record any deviation as a project-specific UX decision.

UX verification matrix before implementation-ready UI claims:

| Proof Target | Required Scenario |
| --- | --- |
| shell default | top hub, left rail, canvas, splitter, right companion, and global dock visible without overlap |
| left overlay open | canvas/right companion keep layout; overlay floats above without consuming layout width |
| dock interaction | dock stays on its declared basis, expands on hover/focus, and does not become a footer |
| center-bottom tray | tray anchor matches its contract and is not pushed by left overlay |
| splitter | pointer resize, keyboard resize, min/max, and persistence checked |
| right companion | collapse/restore, scroll, empty/loading/error states checked |
| popover/tooltip | edge collision, focus route, Escape/outside click, pointer safety checked |
| floating window | drag, resize, focus, close, restore, and viewport bounds checked |
| keyboard pass | tab order, roving focus, command palette, Escape behavior checked |
| copy audit | no raw enum/debug/provider/secret/backend strings visible in normal UI |
| responsive pass | desktop and narrow viewport screenshots or DOM assertions checked |
| accessibility pass | labels, roles, contrast, focus, reduced motion checked |

## 7. Visible Copy And User-State Rules

Before UI implementation, define:

- user task states,
- allowed visible copy classes,
- diagnostics disclosure levels,
- locale plan,
- forbidden frontend leakage,
- copy catalog ownership.

Default forbidden visible UI content:

- raw backend enum names;
- debug params;
- provider payloads;
- API keys or secret refs;
- full file paths unless in an explicit technical surface;
- SQL strings;
- stack traces;
- hidden prompts;
- implementation notes like "this feature does X" in normal UI;
- generated fake prose in UI reference images.

Default allowed normal UI:

- state,
- blocker,
- next safe action,
- claim ceiling label,
- provider posture label,
- redacted diagnostics entry point.

## 8. Image-2, UIREF, And Atlas Rules

Generated images are candidate references, not product proof.

Before an image can influence source, require a `UIREF` mapping:

| Field | Required |
| --- | --- |
| image path | stable project artifact path |
| prompt/source | prompt or reference source |
| adopted elements | exact zones/components/states |
| rejected elements | drift, fake text, bad geometry |
| evidence ids | source/UX ids when reference-derived |
| geometry requirements | proportions, bounds, scroll owners |
| display methods | grid, fixed, absolute overlay, portal, scroll |
| interaction requirements | click, keyboard, drag alternatives, focus |
| motion requirements | duration, easing, reduced-motion |
| token requirements | colors, type, control sizes |
| copy requirements | catalog keys only |
| proof required | DOM, browser, desktop, a11y tests |

For component atlases or texture sheets:

- one sheet class per sheet;
- no full-screen UI reconstruction;
- manifest required before calling it an atlas;
- padding/gutters/alpha/9-slice strategy required;
- state matrix required;
- ordinary controls remain component/token/vector-first.
