---
name: modern-web-standards
description: Current HTML and CSS practice for sites built on Automatic.css 4.x — which CSS and HTML features are safe to ship today, which need a fallback, which to refuse, and how ACSS 4's variable-first, breakpoint-free, cascade-layered architecture changes what "good CSS" means. Use whenever writing, reviewing, refactoring or auditing HTML/CSS, custom classes, `_cssCustom` in Bricks JSON, or `<style>` blocks for paste — even when the user only says "make it responsive", "add dark mode", "style this card", or "is this CSS any good". Pair with the `bricks` and `fms-bricks-html` skills; this one governs the CSS inside the classes they create.
---

# Modern web standards — ACSS 4.x sites

Status snapshot: **2026-09-10**. Baseline moves monthly. When a feature's tier
decides the answer, check `references/feature-status.md` and, if the feature is
near a boundary, re-verify at webstatus.dev before shipping.

## The four tiers

Every feature is one of these. The tier decides how it's used, not whether it's
"modern".

| Tier | Meaning | How to use it |
|---|---|---|
| **Ship** | Baseline Widely Available — interoperable 30+ months | Use freely. No fallback, no `@supports`. |
| **Ship with care** | Baseline Newly Available — works in current browsers, not yet 30 months | Use when the failure mode is cosmetic. Provide a fallback or `@supports` when it's structural. |
| **Enhance only** | Not Baseline — missing or partial in at least one engine | Only inside `@supports` or as pure enhancement. Never load-bearing for layout, navigation, or forms. |
| **Refuse** | Chromium-only or experimental | Do not emit. Say why, and give the Ship-tier alternative. |

Default target for a client service-business site is **Ship**, with **Ship with
care** allowed where ACSS 4 itself already depends on the feature (see below).
State the target once at the top of any CSS you deliver.

## What ACSS 4 already decided for you

ACSS 4.x is variable-first and BEM-first, breakpoint-free, cascade-layered,
OKLCH-based, and uses `color-scheme` + `light-dark()` for dark mode. That fixes
several answers:

- **Color** — `var(--primary)` and friends already resolve for light and dark.
  Never write `@media (prefers-color-scheme)`. Force a subtree with
  `.scheme--light` / `.scheme--dark`. Transparency is `color-mix()` or relative
  color syntax on a token, never a hex with alpha.
- **Responsiveness** — components respond to their container, not the viewport.
  `@container` for components; `@media` only for page-level chrome. Bricks
  still has breakpoints; map their names to ACSS's (XL / L / M / S) and keep
  the values identical in both places.
- **Type and space** — every size is a fluid ACSS variable. A `px` or `rem`
  font-size or padding in custom CSS is a defect.
- **Specificity** — ACSS ships in `@layer`. Unlayered author CSS beats every
  layered rule. That means custom classes win by default; if a rule *should* be
  overridable by ACSS, it has to sit in a layer below ACSS's. Confirm the
  site's layer order before relying on either direction.
- **Reuse** — recipes (`?btn`, `?flex-grid`) expand only in the builder's CSS
  input or ACSS Custom SCSS. Never emit a `?recipe` token into Bricks JSON or
  a paste block; write the CSS it expands to, or leave a post-paste step.

Full mapping and what changed from v3: `references/acss-4-alignment.md`.

## Writing CSS

Order of preference for any styling need:

1. An ACSS **variable** on a namespaced BEM class
2. An ACSS **recipe**, expanded where recipes expand
3. A confirmed ACSS **utility** — only if it's in the site's 4.x cheat sheet,
   not the v3-era list
4. Custom CSS, Ship-tier only, on the same BEM class

Inside custom CSS:

- Logical properties (`margin-block`, `inset-inline`, `padding-inline`) not
  physical ones
- `gap` not margins between siblings
- `aspect-ratio` not padding-hacks
- `clamp()` only for values ACSS doesn't already make fluid
- Nesting is Ship-tier; use it, keep it two levels deep
- `:has()`, `:is()`, `:where()` are Ship-tier; `:where()` to keep specificity
  flat on base styles
- Subgrid for aligning card internals across a grid row
- `@starting-style` + `transition-behavior: allow-discrete` for
  enter/exit animation on `display: none` elements — Ship with care
- `text-wrap: balance` on headings, `text-wrap: pretty` on body — both
  cosmetic, both safe to include without a fallback
- Never: floats for layout, clearfix, `!important` to beat ACSS, vendor
  prefixes, `-webkit-` hacks, `@media (max-width)` on a component

## Writing HTML

- Landmarks: one `<main>`, one `<h1>`, `<header>` / `<nav>` / `<footer>`,
  `<section>` only when it has a heading, `<article>` for self-contained items
- Disclosure: `<details name="group">` for exclusive accordions (Ship with
  care); no JS accordion scripts
- Overlays: `<dialog>` for modals (Ship). `popover` attribute for menus,
  tooltips, toasts (Ship with care). Wire buttons with `commandfor` /
  `command` (Ship with care, Dec 2025) — for a public site add
  `popovertarget` or a 4-line JS fallback for the previous Safari
- Images: `width` and `height` always; `loading="lazy"` below the fold;
  `fetchpriority="high"` on the LCP image only; `decoding="async"`;
  `<picture>` / `srcset` + `sizes` for art direction and density; real `alt`
- Forms: `autocomplete` tokens, `inputmode`, `enterkeyhint`; `<label>` on
  every control; `field-sizing: content` on textareas (Ship with care)
- `<search>` around site search (Ship). `inert` on backgrounded content (Ship)
- No inline event handlers. No `<div>` buttons. No `<br>` for spacing.

## Reviewing existing CSS or HTML

Report by tier: what's fine, what has a modern replacement, what will break.
Use the legacy → modern table in `references/feature-status.md`. Flag, in this
order: hardcoded colors and sizes; viewport media queries on components;
`prefers-color-scheme` queries; JS doing what `<dialog>`, `popover`,
`<details>` or anchor-free CSS now does; missing image dimensions; `!important`.

## Output contract

For any delivered CSS or HTML:

1. First line: `/* target: Ship | Ship with care | Enhance */` and the reason
   if not Ship
2. Only namespaced BEM classes; only ACSS variables for colour, size, space,
   radius, shadow
3. Anything above Ship-tier wrapped in `@supports` or annotated as
   progressive enhancement with its degraded behaviour stated
4. Nothing from the Refuse tier, ever, with the alternative named
5. If a v3-era utility class was avoided because it's unconfirmed in 4.x, say
   so once

## References

- `references/feature-status.md` — the dated tier table for CSS and HTML,
  plus legacy → modern replacements
- `references/acss-4-alignment.md` — what ACSS 4 changed from 3.x and what
  that means for custom CSS, Bricks breakpoints, and the existing
  `acss-conventions.md` allowlist
