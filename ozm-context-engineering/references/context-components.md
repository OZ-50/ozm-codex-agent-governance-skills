# Context Components Reference

Use this file when you need the component-level breakdown behind context engineering decisions.

## Core Components

- system instructions
- tool definitions
- conversation history
- retrieved documents
- tool outputs
- summaries or state projections

## Budgeting Rule

Budget each component separately. Do not let any one category silently consume the whole window.

## Placement Rule

Put critical constraints at the edges. Keep stable and volatile content separated.

## Disclosure Rule

Load summaries first, detail later. The point of progressive disclosure is to defer cost, not to rename overloading.
