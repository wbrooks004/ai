# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This folder **is a skill for authoring Bricks Builder (WordPress) designs** on sites running Automatic.css (ACSS) and ACF Pro — as paste-ready JSON (sections, full pages, templates, query loops, dynamic data, conditions, interactions, popups) or as paste-ready HTML + CSS for the "HTML & CSS to Bricks" converter. JSON shapes are verified against the Bricks 2.3.6 theme source. A deterministic validator in `scripts/` must pass before any JSON is delivered.

Start at [SKILL.md](SKILL.md) — it routes to per-topic references and ready-to-paste patterns.

## Working in this repo

- **Any Bricks task** (generate a layout, fix pasted JSON, build a template, wire ACF data): follow [SKILL.md](SKILL.md). Its rules — verified value shapes, the `key:breakpoint:pseudo` grammar, flat-tree integrity, the validation checklist — override anything you'd guess from memory.
- **Editing the skill itself**: keep SKILL.md slim (routing + rules); put depth in `references/`. Every settings key or JSON shape added to a reference must be verified against the Bricks theme source (kept locally at `~/Downloads/bricks/` or wherever the user points you), not inferred.
- **Pattern files** (`patterns/*.json`) must pass `python3 scripts/bricks_validate.py patterns/<file>.json` before committing.
- **ACSS 4.x**: `references/acss-conventions.md` and `section-patterns.md` were written against 3.x. The 4.x delta lives in the sibling `modern-web-standards` skill (`../modern-web-standards/references/acss-4-alignment.md`).

## Layout

| Path | Contents |
|------|----------|
| `SKILL.md` | Router + authoring workflow + non-negotiable rules + validation checklist |
| `scripts/bricks_validate.py` | Deterministic validator: structure, id collisions vs site export, ACF field names, breakpoint keys, hex/global-class policy |
| `scripts/install_bricks_validator.py` | Installs the validator into a local `~/.claude/skills/bricks/` and appends the global CLAUDE.md block |
| `references/html-paste.md` | The HTML + CSS paste path: rules, output format, handover |
| `references/acss-conventions.md` | ACSS allowlist (3.x): confirmed utilities and variables, BEM + variables pattern |
| `references/section-patterns.md` | HTML worked examples: service grid, hero, FAQ, CTA band, contact form |
| `references/bricks-json-context.md` | Read/write discipline, PROJECT.md block, what the validator can and cannot see |
| `references/json-formats.md` | Clipboard / template / postmeta formats, option keys, validation script |
| `references/style-settings.md` | Universal `_` settings + exact value shapes (the accuracy backbone) |
| `references/elements.md` | Element catalog incl. nestable structures (`_hidden._cssClasses`) |
| `references/layout-recipes.md` | Composition patterns for real designs |
| `references/query-loops.md`, `query-filters.md` | Loops + faceted filtering |
| `references/dynamic-data.md`, `acf-providers.md` | Tags, args, ACF/Meta Box/etc. |
| `references/conditions.md`, `interactions.md`, `popups.md` | Conditional rendering, animations, popups |
| `references/templates.md`, `components-classes.md`, `theme-styles.md` | Template system, reusables, site-wide styling |
| `references/external-assets.md` | Referencing remote images/video/SVG/icons from a reference URL (hotlink vs re-host) |
| `references/forms.md`, `woocommerce.md`, `hooks.md`, `custom-elements.md`, `assets-permissions.md` | Forms, Woo, PHP extension points |
| `patterns/` | Validated paste/import-ready JSON + INDEX.md (incl. `bem-*.json` class-first examples) |

## Quick facts (full detail in references)

- Element node: `{id, name, parent, children, settings, label?}` in a **flat array**; ids are 6-char alphanumeric.
- Clipboard wrapper: `{content, source: "bricksCopiedElements", sourceUrl, version, globalClasses, globalElements}`.
- Breakpoint/pseudo grammar: `_padding:tablet_portrait`, `_background:hover`, `_margin:mobile_portrait:hover`. Defaults: `tablet_portrait` 991 / `mobile_landscape` 767 / `mobile_portrait` 478.
- Typography keys are CSS property names (`"font-size"`), colors are objects (`{"hex": …}` / `{"raw": "var(--…)"}`), box-shadow offsets nest under `values`, gradients use `colors: [{color, stop}]`.

## WP-CLI

```bash
wp bricks regenerate_assets  # Regenerate CSS files (external-files mode)
```

## Documentation

- Official: https://academy.bricksbuilder.io/
- Developer: https://academy.bricksbuilder.io/collection/developer/
