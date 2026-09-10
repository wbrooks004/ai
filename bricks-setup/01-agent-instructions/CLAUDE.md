# CLAUDE.md — Bricks + ACSS project instructions

You are the build agent for a WordPress site made with **Bricks Builder**, **Automatic.css (ACSS)**, and **ACF Pro**.
Your output is mostly Bricks JSON and small amounts of CSS. It must paste into the builder cleanly on the first try
and must not pollute the site's Class Manager or global variables.

Read this whole file before the first task in a session. When in doubt, follow the stricter rule.

---

## PROJECT (fill in before first use)

```yaml
client_name:        ""            # e.g. "Gagnon Plumbing"
class_prefix:       "x"           # 2–4 lowercase chars, e.g. "gg". Every custom class starts with this.
rem_base_px:        16            # What 1rem equals on the live site. Check html { font-size }.
bricks_version:     "2.3.6"
acss_version:       "3.x"
acss_palette:       [primary, secondary, accent, base, neutral, shade, action]  # names actually enabled in ACSS dashboard
breakpoints_px:     { tablet_portrait: 991, mobile_landscape: 767, mobile_portrait: 478 }
content_language:   "en"          # English only. Flag any French copy for the owner to proofread.
json_output_dir:    "bricks-json/"
css_output_file:    "css/{prefix}-components.css"
```

If `class_prefix` is still `x` or `rem_base_px` is unconfirmed, ask before writing any rem value or any class name.

---

## Stack facts you must respect

- **ACSS owns the design system.** Colours, spacing, type scale, radius, grid, section padding all come from ACSS
  variables. You reference them. You never redefine them and never write a competing `:root` block.
- **Bricks global classes are permanent.** They are not covered by Bricks revisions. A junk class name written once
  stays until someone deletes it by hand. Naming discipline is a safety requirement, not a style preference.
- **ACF Pro** supplies dynamic data. Field names come from the user or the field group export. Never guess a field name.
- **Bricks JSON is a flat tree.** Hierarchy lives in `parent` and `children` ids, not in nesting.

---

## Non-negotiable rules

### Naming and classes
1. Every custom class is `{prefix}-{block}`, `{prefix}-{block}__{element}`, or `{prefix}-{block}--{modifier}`.
   Full system: `02-class-naming/bricks-class-naming-system.md`.
2. Never invent an ACSS utility class. If you cannot confirm it exists on this install, write a prefixed BEM class
   styled with ACSS variables instead.
3. Never write unprefixed generic names (`.card`, `.hero`, `.btn`, `.wrapper`). They collide with ACSS, the theme, or plugins.
4. Global class for anything repeated twice or more. Inline element settings for true one-offs.

### CSS values
5. No hex codes. No px or rem font sizes. No hardcoded spacing. Use `var(--primary)`, `var(--text-l)`, `var(--space-m)`,
   `var(--radius-m)`, `var(--section-space-m)`, `var(--gutter)`, `var(--grid-3)` and friends.
6. Exception: `1px` borders, `0`, `100%`, `auto`, `currentColor`, aspect ratios, and z-index values are fine as literals.
7. Never emit `:root { }` inside anything that gets pasted onto the canvas. Bricks converts it into Global Variables.
8. Custom CSS on an element uses `%root%` as the selector. Custom CSS inside a global class uses the literal class selector.

### JSON
9. Clipboard format only, unless asked for a template export or postmeta insert:
   `{ "content": [], "source": "bricksCopiedElements", "sourceUrl": "", "version": "2.3.6", "globalClasses": [], "globalElements": [] }`.
10. Ids are unique 6-character alphanumerics. Every id in a `children` array exists as a node whose `parent` points back.
11. Every id in any `_cssGlobalClasses` array has its full class object in top-level `globalClasses`.
12. Value shapes are exact. Colours are objects (`{"hex": "#..."}` or `{"raw": "var(--primary)"}`). Typography keys are
    CSS property names (`"font-size"`, never `fontSize`). Box shadow offsets nest under `values`. Spacing is a per-side
    object with string units. Bare numbers get `px` appended by Bricks, so always write the unit.
13. Responsive and state grammar is `key:breakpoint:pseudo` with colons: `_padding:tablet_portrait`,
    `_background:hover`, `_margin:mobile_portrait:hover`. Breakpoint before pseudo. Never the legacy underscore form.
14. Do not invent settings keys. Unknown keys are silently ignored. If a key is not in the Bricks reference, ask or omit.
15. Never nest a `section` inside anything. Root elements are sections. Canonical nesting is section > container > content.

### Structure and SEO
16. Semantic `tag` on layout elements: `header`, `nav`, `main`, `article`, `aside`, `footer`.
17. One `h1` per page. Heading levels descend without skipping. Size comes from a class or ACSS variable, never from
    picking a different heading level.
18. Images get real `alt` text, `loading="lazy"` below the fold, explicit width and height when known.
19. Local SEO pages: write real place names and service names into copy. Use `{acf_*}` or `{post_title}` tokens only
    when the user says the section is a template for programmatic pages.
20. Content is English only. If any source material is in French, reproduce it verbatim, mark it `[FR — owner to proofread]`,
    and do not translate or "fix" it.

---

## Workflow for every build task

1. **Confirm inputs** before writing JSON: rem base, class prefix, ACF field names (if any), reference URL (if any).
   Default to 16px and prefix `x` only if the user says "just go".
2. **Plan the tree** in plain text: section > container > blocks, with element types and labels. Two to six lines.
3. **Decide classes**: list every new global class you will create and why. Zero is a valid answer.
4. **Write the JSON** to `{json_output_dir}/{type}-{slug}.json`. Give every element a `label` so the structure panel documents itself.
5. **Validate** (run, do not eyeball):
   - `python3 -m json.tool file.json` parses.
   - Every parent/children reference resolves; ids unique.
   - Every `_cssGlobalClasses` id exists in `globalClasses`.
   - No hex, no px/rem font sizes, no `:root` in any `_cssCustom` string or CSS file.
   - Every class name starts with `{prefix}-`.
   - Every breakpoint key is one of the configured names.
   - Query loops have `hasLoop: true` and `query.objectType`; filters reference a real `filterQueryId`.
6. **Report** in this order: file path, format used, new global classes created (table), manual steps after paste
   (media to swap, links to wire, ACF fields to bind, interactions to add).

## Workflow for every edit task

Use `04-prompts/bricks-json-editing-prompt.md`. Short version: change only what was asked, preserve every id, keep the
tree flat and valid, return the complete JSON, and list the diff in words.

---

## Where things live

| Thing | Location |
|-------|----------|
| Component CSS for this site | Bricks > Settings > Custom Code > Custom CSS, mirrored in `{css_output_file}` in this repo |
| Starter component CSS | `03-css-framework/bricks-starter.css` |
| Generated section JSON | `{json_output_dir}` |
| ACF field group exports | `acf-json/` (ACF Local JSON) |
| Class naming rules | `02-class-naming/bricks-class-naming-system.md` |

## Things you do not do

- Do not paste HTML with `<script>` or `<link>` tags. Bricks quarantines them into a Code element that needs manual signing.
- Do not use component instances (`cid`) unless the user is already working with Bricks Components.
- Do not reference Bricks palette colour ids (`var(--bricks-color-xxxxxx)`) unless you have the palette export. Use ACSS variables.
- Do not use pseudo suffixes other than `:hover`, `:active`, `:focus` in settings keys. Put `::before` / `::after` styling in `_cssCustom`.
- Do not write to production. Every paste goes to staging or local first. Global class writes have no undo.
