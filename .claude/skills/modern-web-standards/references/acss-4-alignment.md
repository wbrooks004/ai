# ACSS 4.x alignment

What Automatic.css 4.x changed, what each change means for the CSS Claude
writes, and which parts of the existing `fms-bricks-html` allowlist
(`references/acss-conventions.md`) it puts in doubt.

Source: docs.automaticcss.com "What's New in ACSS 4.x", "Modern Color Scheme
Workflow", "Website Width & Breakpoints" — all last updated **2026-08-07**.
ACSS 4.x is **not backward compatible** with 3.x; 3.x sites stay on 3.x, new
sites start on 4.x. Confirm which one a site runs before applying any of this.

---

## 1. Variable-first, BEM-first

**Changed.** Most utility class modules were removed. "Some critical utility
classes have been replaced with Recipes which can be expanded inside of any
BEM class."

**Means.** The default styling unit is a namespaced BEM class whose values are
ACSS variables. Utilities are the exception, not the starting point.

**Allowlist impact.** These entries in `acss-conventions.md` were confirmed
against docs retrieved August 2026 but read as v3-era. Treat each as
**unconfirmed for 4.x** until it's found in the site's own 4.x cheat sheet:

| Entry | Concern |
|---|---|
| `.grid--{1-12}` | Likely replaced by the `?flex-grid` / grid recipes |
| `.gap--{size}`, `.grid-gap`, `.container-gap`, `.content-gap` | The `var(--…-gap)` variables are the stable part; the classes may not exist |
| `.text--{size}` | Utility module status unknown |
| `.content-grid--off` | Content Grid behaviour may have changed |
| Size `xxl` anywhere | Renamed to **`2xl`**. All other t-shirt sizes unchanged |
| `.width--{size}` t-shirt form | Now literal: `.width--10` … `.width--90` |

The variables (`--space-m`, `--text-l`, `--primary`, `--radius-m`,
`--content-width`, `--gutter`, `--grid-3`) are the part of that file to keep
trusting. When in doubt, a BEM class on variables gets the same result with
zero risk — that rule from the skill still holds and is now the framework's
own stance.

**Action for Saleem:** paste the 4.x cheat sheet from the ACSS dashboard once,
and `acss-conventions.md` gets re-cut against it. Until then Claude writes
variables, not utilities.

## 2. Recipes use `?`

**Changed.** `?btn`, `?flex-grid` instead of `@btn`. "Expand them in the CSS
input of your builder or in ACSS Custom SCSS."

**Means.** Expansion is an editor-time feature of the ACSS plugin. A `?recipe`
token written into Bricks clipboard JSON (`_cssCustom`) or a paste block does
**not** expand — it ships as literal text.

**Rule.** Never emit a `?recipe` into JSON or HTML paste output. Either write
the CSS the recipe produces, or add a post-paste step: "In the class's CSS
input, type `?btn` and expand."

## 3. Breakpoint-free

**Changed.** Preset breakpoints removed from the framework. "You can still use
media queries and container queries in your development process, but they're
no longer needed in the ACSS framework as fixed presets."

**Means.** ACSS generates no breakpoint utilities and no `@media` scaffolding.
Fluid type, space, and header height are all calculated without breakpoints.
Component responsiveness is the author's job, and the modern answer is
`@container`.

**Bricks still has breakpoints.** The ACSS docs recommend mapping every ACSS
breakpoint name onto Bricks with Custom Breakpoints enabled: rename Bricks's
base → **XL**, tablet portrait → **L**, mobile landscape → **M**, mobile
portrait → **S**, values matching the ACSS Viewport tab. Never make anything
other than the top breakpoint the base.

**Two consequences for the Bricks JSON pipeline:**

- Renaming a breakpoint's label in Bricks does not necessarily change its
  internal key. Confirm from a site export whether responsive suffixes are
  still `tablet_portrait` / `mobile_landscape` / `mobile_portrait` or have
  become custom keys, then set `--breakpoints` on `bricks_validate.py`
  accordingly and record it in `PROJECT.md › Bricks`.
- Any `@media (max-width: 991px)` in custom CSS is now a hardcoded number the
  framework no longer owns. Prefer `@container`; if a viewport query is
  genuinely needed, reference the value the site's Viewport tab actually uses
  and say so in a comment.

**Allowlist impact.** The `@media (max-width: 991px)` example in
`acss-conventions.md` → replace with a container query example.

## 4. Cascade layers

**Changed.** "Implemented CSS Layers: Users now have a lot more control over
framework specificity."

**Means.** ACSS's rules sit in named `@layer`s. Per the cascade spec, any
**unlayered** author style beats **every** layered style regardless of
specificity. So:

- Custom BEM CSS written unlayered will always override ACSS. Good for
  intentional overrides; dangerous when a class was only meant to add to ACSS
  defaults and now silently replaces them.
- If a custom rule should be overridable by ACSS utilities or theme styles, it
  must be placed in a layer that ACSS's layer order ranks below its own.
- `!important` inverts layer order — never use it against ACSS.

**Unknown.** The exact layer names and their order weren't in the pages
retrieved. Before writing `@layer` declarations of your own, open the
generated CSS or the ACSS docs' layers page and record the order in
`PROJECT.md › Bricks`.

## 5. OKLCH palette

**Changed.** New color system in OKLCH for perceptual accuracy.

**Means.** Colour math should stay in the same space: `color-mix(in oklch, …)`
and `oklch(from var(--primary) …)`. Mixing in `srgb` against an OKLCH palette
produces muddier midpoints. Never a hex, never an `rgb()` — that was already
the rule; OKLCH makes the reason concrete.

## 6. `color-scheme` + `light-dark()` dark mode

**Changed.** "Alt" colours removed. ACSS outputs every palette variable as
`light-dark(light-value, dark-value)`, sets `color-scheme` on `:root` from the
Website Scheme setting, and provides `.scheme--light` / `.scheme--dark` to
force a subtree.

**Means.**
- `var(--primary)` is already correct in both schemes. Components never need
  to know the scheme.
- `@media (prefers-color-scheme: dark)` in custom CSS is wrong on an ACSS 4
  site — it fights the framework's mechanism and ignores `.scheme--*` forcing.
- A light card on a dark section: add `.scheme--light` to the card. Nothing
  else.
- Native form controls and scrollbars follow `color-scheme` automatically;
  don't restyle them for dark mode.
- Baseline note: `light-dark()` is Newly Available (May 2024), Widely on
  2026-11-13. ACSS chose it; the site inherits that target.

## 7. Transparency tokens removed

**Changed.** The predefined transparency token library is gone in favour of
`color-mix()` and relative color syntax.

**Means.** Two forms, pick by tier:

```css
/* Ship — color-mix() is Widely Available (2025-11) */
background: color-mix(in oklch, var(--primary), transparent 60%);

/* Ship with care — relative color syntax Widely on 2027-01 */
background: oklch(from var(--primary) l c h / 0.4);
```

Default to `color-mix()`. Any `var(--primary-trans-40)`-style token from v3
memory is a v3-ism and will not resolve.

## 8. Naming and width changes

- **2XL** replaces **XXL**. Everything else in the t-shirt scale is unchanged.
  `--space-2xl`, not `--space-xxl`.
- Width classes are literal 10-point values: `.width--60`. No t-shirt widths.

## 9. Effects, surfaces, overlays, forms

- Transition, sticky, and selection styling live under **Effects** (Additional
  Styling). Selection colours follow `color-scheme`.
- Surfaces and overlays are separate systems now — five custom slots each.
  Don't assume a v3 overlay class name.
- Form styling was refactored per third-party form system. Styling for WS
  Form Pro comes from ACSS's WS Form integration, not from `forms.md` in the
  `bricks` skill (which covers Bricks's native form).

---

## What this means for the three skills together

| Skill | Governs | Adjusted by ACSS 4 |
|---|---|---|
| `bricks` | JSON structure, element catalog, value shapes | Breakpoint keys may be custom after ACSS mapping; `xxl` → `2xl` in any variable references |
| `fms-bricks-html` | Paste markup, class naming, allowlist | Utility entries unconfirmed until re-cut; `@media` example replaced; recipes never emitted |
| `modern-web-standards` | The CSS inside custom classes | Container queries default; `light-dark()` accepted; `@layer` awareness; OKLCH mixing |

---

## PROJECT.md additions for ACSS 4 sites

Add to the existing `## Bricks` block:

```markdown
| ACSS version | `4.x` — confirm; 3.x sites follow the old allowlist |
| ACSS cheat sheet | `exports/acss-cheatsheet-YYYY-MM-DD.txt` — pasted from the dashboard; source of truth for surviving utilities |
| ACSS layer order | `<record from generated CSS>` |
| Website scheme | `light dark` / `light` / `dark` — from Color Scheme Setup |
| Bricks breakpoint keys | `tablet_portrait, mobile_landscape, mobile_portrait` or the custom keys after ACSS mapping — feeds `bricks_validate.py --breakpoints` |
```
