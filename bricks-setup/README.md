# Bricks Setup Resources

Four ready-to-use files for building WordPress sites with **Bricks Builder + Automatic.css (ACSS) + ACF Pro**, with an AI agent doing most of the JSON authoring.

| # | File | What it is | Where it goes |
|---|------|------------|---------------|
| 1 | `01-agent-instructions/CLAUDE.md` | Custom instruction file for the agent | Repo root of any Bricks project (rename to `AGENTS.md` for other agents) |
| 2 | `02-class-naming/bricks-class-naming-system.md` | Class naming system | Read once, then link it from the instruction file |
| 3 | `03-css-framework/bricks-starter.css` | Starter CSS framework on top of ACSS variables | Bricks > Settings > Custom Code > Custom CSS (or a child-theme stylesheet) |
| 4 | `04-prompts/bricks-json-editing-prompt.md` | Reusable JSON-editing prompt | Paste into any AI assistant when editing exported Bricks JSON |

## Setup order (one-time per project)

1. Copy `CLAUDE.md` into the project repo root. Fill in the `PROJECT` block at the top (client prefix, rem base, palette names, ACSS version).
2. Paste `bricks-starter.css` into Bricks > Settings > Custom Code > Custom CSS. Replace the `x-` prefix with the client prefix (global find and replace).
3. Keep the naming system open in a tab while auditing the Class Manager.
4. Use the JSON-editing prompt every time you hand the agent an exported section to change.

## Assumptions baked into these files

- Bricks 2.3.6 (JSON shapes verified against that source). Older versions parse the same clipboard format.
- ACSS v3.x. Utility class names are user-configurable, so the files reference **variables** more than classes.
- Default Bricks breakpoints: 991 / 767 / 478. Change the media queries if the project uses custom breakpoints.
- rem base is 16px unless the project says otherwise. Every file asks for confirmation before using rem.

## Related project skills (in `.claude/skills/`)

| Skill | What it does |
|-------|--------------|
| `bricks` | The merged Bricks skill: JSON authoring (verified against 2.3.6), the HTML + CSS paste path with the ACSS allowlist, and the validator (`scripts/bricks_validate.py`) that root `CLAUDE.md` requires to pass before any JSON is delivered. |
| `modern-web-standards` | ACSS 4.x alignment and a dated CSS/HTML feature-tier table. Governs the CSS inside custom classes and `_cssCustom`. Note: the files in this folder were written against ACSS 3.x; 3.x and 4.x are not compatible. |
