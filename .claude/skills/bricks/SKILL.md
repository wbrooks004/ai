---
name: bricks
description: Build Bricks Builder (WordPress) sections, pages, templates, and full designs for sites running Automatic.css (ACSS) and ACF Pro. Two deliverables — paste-ready Bricks JSON (verified against Bricks 2.3.6) or paste-ready HTML + CSS for the "HTML & CSS to Bricks" converter. Use for any Bricks task — hero, service grid, card row, FAQ, CTA, pricing, contact form, header/footer, query loops, ACF/dynamic data, faceted filters, conditions, interactions, popups, WooCommerce, custom elements, hooks — and whenever the user says "build me a hero" or "design a services section" for a WordPress site, converts a Figma frame or competitor page into buildable markup, or asks to fix, edit, or validate exported Bricks JSON. Ships a deterministic validator that must pass before any JSON is delivered.
---

# Bricks Builder authoring (JSON and HTML paste)

Generate complete Bricks designs that paste or import cleanly on the first try, on sites where ACSS owns
the design system and global classes have no undo.

## Pick the deliverable

| Deliverable | Use when | Reference |
|---|---|---|
| **Bricks JSON** (default) | Query loops, dynamic data, conditions, interactions, popups, templates, editing an export, or exact control over element settings | This file + [references/json-formats.md](references/json-formats.md) |
| **HTML + CSS paste** | User asks for HTML; converting a Figma frame, competitor page, wireframe, or content brief; a static section on an ACSS site where speed beats precision | [references/html-paste.md](references/html-paste.md) |

Never mix both in one paste. State which one you used in the final response.

## Default Deliverable (JSON path)

Produce an actual `.json` file in the workspace (not inline JSON) unless the user asks otherwise. Use the
project's folder convention if one exists; otherwise `bricks-json/{type}-{slug}.json`. In the final
response state: the file path, which JSON format you used, and the validator's final line.

## Workflow

0. **Clarify inputs first.** Read `PROJECT.md › Bricks` if it exists; it answers most of these. Otherwise
   ask once, batched, with the default you'll assume if the user says "just go":
   - **rem base** — what `1rem` equals on the target site. Default **16px** (a `html { font-size: 62.5% }`
     reset makes it 10px). All `rem`/`clamp()` math and px→rem conversion depends on it. → [rem base](references/style-settings.md#root-font-size-rem-base)
   - **class prefix** — 2–4 lowercase letters per client (`gg`, `fms`, `ttt`). Default `x-`, flagged for replacement.
   - **ACSS version** — 3.x or 4.x. They are not compatible. The allowlist in [references/acss-conventions.md](references/acss-conventions.md) is 3.x; on 4.x read `../modern-web-standards/references/acss-4-alignment.md` and write variables, not utilities.
   - **exports** — site export and ACF export paths. They are ground truth for ids, class ids and names, field names, breakpoints. → [references/bricks-json-context.md](references/bricks-json-context.md)
   - **reference URL** — if given, fetch it and reference its assets by absolute URL. → [references/external-assets.md](references/external-assets.md)
1. **Pick the format** — clipboard paste vs template import vs programmatic insert → [references/json-formats.md](references/json-formats.md)
2. **Plan structure** — semantic section → container → blocks tree; pick elements from the catalog → [references/elements.md](references/elements.md)
3. **Style with settings** — every `_` style key and its exact value shape → [references/style-settings.md](references/style-settings.md). Colours, sizes, spacing, radius come from ACSS variables as `{"raw": "var(--…)"}`; reusable components get a prefixed BEM global class. → [references/acss-conventions.md](references/acss-conventions.md)
4. **Wire data** — dynamic tags, query loops, filters as needed (see routing table)
5. **Validate** — run the validator (checklist below), fix every ERROR, then deliver

## Format Quick Reference

**Clipboard (paste into builder)** — the default for sections and page content:

```json
{
  "content": [ /* flat array of element nodes */ ],
  "source": "bricksCopiedElements",
  "sourceUrl": "https://example.com",
  "version": "2.3.6",
  "globalClasses": [ /* full class objects referenced by _cssGlobalClasses */ ],
  "globalElements": []
}
```

**Element node** (every entry in `content`):

```json
{
  "id": "abc123",
  "name": "heading",
  "parent": "xyz789",
  "children": [],
  "settings": {},
  "label": "Optional structure-panel label"
}
```

- `id`: unique 6-char alphanumeric. `parent`: parent's id, or `0` for root elements.
- The array is **flat** — hierarchy lives entirely in `parent` + `children` (ids must cross-reference exactly).
- Root elements are usually `section`; never nest a `section` inside anything.

## Task Routing

| Task | Reference |
|------|-----------|
| **HTML + CSS paste path**: rules, output format, handover | [references/html-paste.md](references/html-paste.md) |
| **ACSS allowlist**: confirmed utility classes and variables, BEM + variables pattern, what never to write | [references/acss-conventions.md](references/acss-conventions.md) |
| **ACSS section patterns** (HTML): service grid, hero, FAQ, CTA band, contact form | [references/section-patterns.md](references/section-patterns.md) |
| **Read/write discipline**, PROJECT.md block, what the validator can and cannot see | [references/bricks-json-context.md](references/bricks-json-context.md) |
| ACSS 4.x changes, CSS/HTML feature tiers for custom CSS | `../modern-web-standards/SKILL.md` |
| Format selection, clipboard/template/meta storage, programmatic insert | [references/json-formats.md](references/json-formats.md) |
| Element catalog, per-element settings, nestables | [references/elements.md](references/elements.md) |
| Style keys, value shapes (color/typography/border/shadow/gradient/transform), responsive + hover grammar | [references/style-settings.md](references/style-settings.md) |
| Section/grid/flex recipes, cards, overlays, sticky, full designs (JSON) | [references/layout-recipes.md](references/layout-recipes.md) |
| Dynamic data tags `{post_title}`, args, `{echo:}` | [references/dynamic-data.md](references/dynamic-data.md) |
| ACF (incl. repeaters, groups, flexible content), Meta Box, JetEngine, Pods, CMB2 | [references/acf-providers.md](references/acf-providers.md) |
| Query loops (`hasLoop` + `query`), post/term/user queries | [references/query-loops.md](references/query-loops.md) |
| Faceted filters, AJAX pagination, load more, infinite scroll, live search | [references/query-filters.md](references/query-filters.md) |
| Show/hide conditions (`_conditions`) | [references/conditions.md](references/conditions.md) |
| Interactions, animations, scroll triggers (`_interactions`) | [references/interactions.md](references/interactions.md) |
| Popups (templates, triggers, limits, AJAX) | [references/popups.md](references/popups.md) |
| Template types, conditions, import/export, header/footer/archive/404 | [references/templates.md](references/templates.md) |
| Components, global classes, global variables, color palette | [references/components-classes.md](references/components-classes.md) |
| Theme styles, breakpoints, CSS generation order | [references/theme-styles.md](references/theme-styles.md) |
| Form element, actions, validation | [references/forms.md](references/forms.md) |
| WooCommerce templates and elements | [references/woocommerce.md](references/woocommerce.md) |
| PHP: custom elements with controls | [references/custom-elements.md](references/custom-elements.md) |
| PHP: filters and actions | [references/hooks.md](references/hooks.md) |
| External assets from a reference URL (any image/video/SVG/icon, hotlink vs re-host) | [references/external-assets.md](references/external-assets.md) |
| Asset loading, builder permissions | [references/assets-permissions.md](references/assets-permissions.md) |

Ready-to-paste JSON examples (hero, grids, ACF loops, filtered archive, header/footer, popup…): [patterns/](patterns/) — see [patterns/INDEX.md](patterns/INDEX.md). Note the pattern files use plain hex colours; on an ACSS site swap them for `{"raw": "var(--…)"}` before delivering.

## Non-Negotiable Rules

Bricks JSON structure:

1. **Flat tree integrity** — every `children` id exists as a node whose `parent` points back. No orphans, no duplicates.
2. **Verified value shapes only** — colors are objects (`{"hex": "#222"}` or `{"raw": "var(--x)"}`), typography keys are CSS property names (`"font-size"`, not `fontSize`), box-shadow offsets nest under `values`, gradients use `colors: [{color, stop}]`. When unsure, check style-settings.md — do not guess shapes.
3. **Responsive grammar** — `setting:breakpoint:pseudo` with colons: `_padding:tablet_portrait`, `_background:hover`, `_margin:mobile_portrait:hover`. Default breakpoint keys: `tablet_portrait` (991), `mobile_landscape` (767), `mobile_portrait` (478). Desktop is the bare key. Sites that mapped ACSS breakpoints onto Bricks may use custom keys; the site export shows the real ones.
4. **Units are strings** — `"3rem"`, `"100%"`, `"24px"`. Bare numbers get `px` appended by Bricks.
5. **Real structure, no filler** — semantic `tag` settings on sections/blocks (`header`, `nav`, `article`, `aside`, `footer`), one `h1` per page, descending heading levels.
6. **Global classes ride along** — any id listed in an element's `_cssGlobalClasses` must have its full class object in the top-level `globalClasses` array. (Sites on the `cssClasses-only` policy put BEM names in `_cssClasses` instead and ship no `globalClasses`; PROJECT.md says which.)
7. **Don't invent settings keys** — only keys documented in the references or found in the Bricks source. Unknown keys are silently ignored and waste the user's trust.
8. **Exports are ground truth** — never generate an id that exists in the site export; never reference an ACF field that is not in the ACF export; when editing an existing section, re-emit it whole with the same ids so the paste replaces instead of duplicating.
9. **Reference external assets by absolute `url`, never `id`** — attachment `id`s don't resolve cross-site. Respect licensing. → [references/external-assets.md](references/external-assets.md)

ACSS design system (both deliverables):

10. **Confirm the rem base before using rem** — never assume `1rem = 16px` silently. Convert any px values lifted from a reference using the confirmed base.
11. **No hardcoded design values** — no hex, no px/rem font sizes, no literal spacing. Use `var(--primary)`, `var(--text-l)`, `var(--space-m)`, `var(--radius-m)`, `var(--section-space-m)`, `var(--gutter)`, `var(--grid-3)`. Literal `1px` borders, `0`, `100%`, `auto`, `currentColor`, aspect ratios, and z-index are fine.
12. **Never invent an ACSS class name** — if it is not in [references/acss-conventions.md](references/acss-conventions.md) (and confirmed for the site's ACSS version), write a prefixed BEM class on ACSS variables instead.
13. **Prefix every custom class** — `{prefix}-{block}`, `{prefix}-{block}__{element}`, `{prefix}-{block}--{modifier}`. Never unprefixed `.card`, `.hero`, `.btn`.
14. **Never emit a `:root` block, a redefined ACSS class, or a `?recipe` token** into anything that gets pasted. Custom CSS on an element uses `%root%`; custom CSS in a global class uses the literal class selector.
15. **Never emit `<script>` or `<link>` tags** in an HTML paste. Bricks quarantines them.

## Validation Checklist (run before delivering JSON)

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/bricks_validate.py <file> --existing <site-export> --acf <acf-export> <flags from PROJECT.md>` exits 0 — fix every ERROR before continuing; decide every WARNING consciously
- [ ] `source: "bricksCopiedElements"` + `version` matches the target site's Bricks version (clipboard format)
- [ ] Value shapes match style-settings.md (spot-check colors, typography, spacing); the validator cannot see wrong shapes or unknown keys
- [ ] Responsive keys use the site's breakpoint names (pass `--breakpoints` if custom)
- [ ] Query loops: `hasLoop: true` + `query.objectType` present; filters point at a real query element id via `filterQueryId`
- [ ] Dynamic data tags exist for the stated field provider (`--acf` makes `{acf_*}` checks deterministic)
- [ ] No hex, no px/rem sizes, no `:root`, no `?recipe` in any `_cssCustom` string (`--no-hex` catches hex)
- [ ] Round-trip on staging before production; the validator cannot see version drift

Exit `0` pass, `1` errors, `2` unreadable input. `--json` for machine output. `--strict` promotes warnings.
Paste the validator's last line into the response.

For an HTML paste, the checklist is the **Hard constraints** section of [references/html-paste.md](references/html-paste.md).
