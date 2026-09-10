# Feature status — CSS and HTML

Snapshot **2026-09-10**. Tiers follow Baseline: *Widely* = interoperable 30+
months; *Newly* = interoperable, under 30 months; *Limited* = not
interoperable. Dates are the Baseline date, not the first browser ship date.
Re-verify anything near a boundary at webstatus.dev or the monthly web.dev
Baseline digest before it becomes load-bearing.

---

## CSS — Ship (Widely Available)

| Feature | Widely since | Note |
|---|---|---|
| Custom properties, `var()` | long-standing | Foundation of ACSS |
| `clamp()`, `min()`, `max()` | long-standing | ACSS fluid type/space is built on it |
| Grid, flex, `gap` | long-standing | |
| `aspect-ratio` | 2023 | Replaces padding-bottom hacks |
| Logical properties (`inset`, `margin-block`, `padding-inline`…) | 2023 | Default over physical |
| `dvh` / `svh` / `lvh` viewport units | 2025-05 | Use `dvh` for full-height heroes on mobile |
| `@layer` cascade layers | 2024-09 | ACSS 4 is layered — see alignment doc |
| Container queries, size (`@container`, `cqi`) | 2025-08 | Default for component responsiveness |
| `color-mix()` | 2025-11 | ACSS 4's transparency mechanism |
| `:has()` | 2026-06 | Parent/sibling selection without JS |
| CSS nesting | 2026-06 | Keep it shallow |
| `:is()` / `:where()` | long-standing | `:where()` for zero-specificity base styles |
| Subgrid | 2026-03 | Align card internals across a row |
| `contain-intrinsic-size` | 2026-03 | Pair with `content-visibility` |
| `hyphens: auto` | 2026-03 | |
| `image-set()` | 2026-03 | CSS-side `srcset` |
| `display: inline flex` two-value syntax | 2026-01 | Optional clarity |
| `@counter-style` | 2026-03 | |
| `color-scheme` property | 2024 | ACSS sets it on `:root` |
| OKLCH / `oklch()` colours | 2023 | ACSS 4 palette space |
| `inset` shorthand | 2023 | |
| `text-underline-offset`, `text-decoration-thickness` | 2023 | |
| `overscroll-behavior` | 2023 | |
| `scroll-snap` | 2023 | Carousels without JS |
| `accent-color` | 2024 | Native form control tinting |
| `:focus-visible` | 2024 | Only style focus rings with this |

## CSS — Ship with care (Newly Available)

| Feature | Newly since | Widely on | Failure if absent |
|---|---|---|---|
| `light-dark()` | 2024-05 | 2026-11-13 | Whole `var()` fails → colour falls to inherited. ACSS 4 depends on it; accepted |
| `@property` registered custom properties | 2024-07 | 2027-01 | Animation on the property doesn't run; static value fine |
| `@starting-style` | 2024-08 | 2027-02 | Entry animation skipped; element still appears |
| `transition-behavior: allow-discrete` | 2024-08 | 2027-02 | Exit animation skipped |
| Relative color syntax `oklch(from var(--x) l c h / 0.5)` | 2024-07 | 2027-01 | Colour fails → prefer `color-mix()` (Ship) where either works |
| `text-wrap: balance` | 2024-05 | 2026-11 | Cosmetic |
| `text-wrap: pretty` | partial | — | Cosmetic; Safari 26+; treat as Enhance |
| `content-visibility: auto` | 2025-09 | 2028-03 | No rendering skip; page still correct |
| `abs()` / `sign()` | 2025-06 | 2027-12 | Rare need |
| `@scope` | 2025-12 | 2028-06 | Rules inside are ignored → do not use for base styling yet |
| `:open` pseudo-class | 2026 | — | Style with `[open]` + `:popover-open` instead until Widely |
| `field-sizing: content` | 2026 (Firefox 152) | — | Textarea doesn't auto-grow; fine |
| `sibling-index()` / `sibling-count()` | 2026 | — | Staggers collapse to same delay; fine |
| `shape()` for `clip-path` | 2026-02 | — | Shape not applied → element unclipped; avoid for hero masks |
| `contrast-color()` | 2026-04 | — | Falls back to declared colour; set one |
| `width: stretch` | 2025 | — | Use `100%` fallback |
| `<details name>` exclusive accordions | 2024-09 | 2027-03 | Multiple panels can open at once |

## CSS — Enhance only (Limited / partial)

| Feature | Status 2026-09 | Use |
|---|---|---|
| **Anchor positioning** (`anchor-name`, `position-anchor`, `anchor()`, `position-try-fallbacks`) | Not Baseline. Chrome 125+, Safari 26, Firefox shipped 2026 but MDN and OddBird still list it non-Baseline; ~81% support (Comeau, Jul 2026). Level 2 Chromium-only. In Interop 2026. | Tooltips and popover placement inside `@supports (anchor-name: --x)` with a static-position fallback. Never for navigation menus on a client site yet |
| Scroll-driven animations (`animation-timeline: scroll()`) | Expected Baseline 2026; not confirmed | Decorative only, inside `@supports` |
| Cross-document view transitions | Chrome 134, Safari 18.2; Firefox pending | Enhancement only |
| `text-box: trim` | Chrome 133, Safari 18.2; Firefox pending | Enhancement only |
| Customizable `<select>` (`appearance: base-select`) | Chromium only | Enhancement only; native select must stay usable |
| CSS Grid Lanes (`display: grid-lanes`, masonry) | Safari 26.4; others flagged | Do not ship |
| Scroll-state container queries | Chromium only | Do not ship |
| `::scroll-button()`, `::scroll-marker` | Chromium only | Do not ship |
| `corner-shape` | Chromium only | Do not ship |
| `interpolate-size` / `calc-size()` | Chromium only | Do not ship |

## CSS — Refuse (Chromium-only or experimental)

| Feature | Why | Alternative |
|---|---|---|
| `if()` inline conditional | Chrome 137+ only; Firefox and Safari absent, vendor positions unknown | Style queries via `@container style()` are also limited; use class toggles or `light-dark()` |
| `@function` custom functions | Chrome 139+ only | Custom properties + `calc()`; Sass functions if a build step exists |
| `@mixin` / `@apply` | Chrome 146 expected only | BEM class composition |
| Advanced typed `attr()` | Chromium only | Custom property set on the element |
| CSS gap decorations | Chrome 147 expected | Pseudo-element borders |

---

## HTML — Ship

| Feature | Note |
|---|---|
| `<dialog>` + `showModal()` | Modals. Widely since 2024-09 |
| `<details>` / `<summary>` | Disclosure |
| `<search>` | Wrap site search |
| `inert` | Backgrounded content behind a modal |
| `loading="lazy"` on `<img>` / `<iframe>` | Never on the LCP image |
| `decoding="async"` | Every non-critical image |
| `fetchpriority="high"` | LCP image and nothing else |
| `<picture>`, `srcset`, `sizes` | Art direction and density |
| `width` / `height` on every `<img>` | CLS |
| `autocomplete`, `inputmode`, `enterkeyhint` | Every form field |
| `<link rel="modulepreload">` | Widely 2026-03 |
| `dirname` on inputs | Widely 2026-02 |

## HTML — Ship with care

| Feature | Newly since | Fallback |
|---|---|---|
| `popover` attribute | 2025-01 | Element renders in-flow; add `hidden` until opened by JS |
| `commandfor` / `command` invokers | 2025-12 (Safari 26.2) | Keep `popovertarget` on popovers; 4-line `click → showModal()` shim for dialogs |
| `<details name="…">` | 2024-09 | Panels don't auto-close each other |
| `closedby="any"` on `<dialog>` | 2025 | Backdrop click doesn't close; ESC still does |

## HTML — Enhance only

| Feature | Status |
|---|---|
| `popover="hint"`, `interestfor` | Chromium only |
| `hidden="until-found"` | Not interoperable |
| `<selectedcontent>` | Chromium only |

---

## Legacy → modern replacements

Use when reviewing existing code. Left column is a defect on an ACSS 4 site.

| Legacy | Modern | Tier |
|---|---|---|
| `@media (max-width: 991px)` on a component | `@container (inline-size < 40rem)` | Ship |
| `@media (prefers-color-scheme: dark)` | `light-dark()` via ACSS tokens; `.scheme--dark` to force | Ship with care (ACSS-accepted) |
| `rgba(11, 93, 58, 0.4)` | `color-mix(in oklch, var(--primary), transparent 60%)` | Ship |
| `font-size: 18px` / `1.125rem` | `var(--text-m)` | Ship |
| `padding: 24px` | `var(--space-m)` | Ship |
| `margin-left`, `padding-right` | `margin-inline-start`, `padding-inline-end` | Ship |
| `height: 100vh` hero | `min-height: 100dvh` | Ship |
| Padding-bottom % aspect hack | `aspect-ratio: 16 / 9` | Ship |
| `.clearfix`, floats for layout | Grid / flex | Ship |
| Sibling margins for spacing | `gap` | Ship |
| `-webkit-` prefixes on standard properties | Drop them | Ship |
| `!important` to beat framework CSS | Fix the layer or specificity | Ship |
| JS accordion | `<details name="faq">` | Ship with care |
| JS modal + focus trap + body-scroll lock | `<dialog>` + `showModal()` | Ship |
| JS dropdown / tooltip show-hide | `popover` (+ anchor positioning as enhancement) | Ship with care |
| JS to open a dialog on click | `<button commandfor="id" command="show-modal">` | Ship with care |
| JS "is open" class toggling | `:open` (Newly) or `[open]` / `:popover-open` (Ship) | mixed |
| JS textarea auto-grow | `field-sizing: content` | Ship with care |
| `opacity` + `visibility` fade-in from `display:none` | `@starting-style` + `allow-discrete` | Ship with care |
| Nested grid alignment hacks | `subgrid` | Ship |
| `outline: none` on focus | Style `:focus-visible` instead | Ship |
| Uneven heading line breaks | `text-wrap: balance` | Ship with care |
| Manual `srcset` in CSS backgrounds | `image-set()` | Ship |

---

## Sources (retrieved 2026-09-10)

- web.dev Baseline digests: Jan 2026 (`display` two-value widely), Feb 2026
  (`shape()` newly; `dirname` widely; Interop 2026 launched), Mar 2026
  (subgrid, `contain-intrinsic-size`, `hyphens`, `image-set()`,
  `modulepreload` widely), Apr 2026 (`contrast-color()` newly), May 2026
- web-features explorer: `light-dark` (newly 2024-05-13, widely 2026-11-13),
  `@property` (newly 2024-07-09, widely 2027-01-09), `@scope` (newly
  2025-12-12), `abs()`/`sign()` (newly 2025-06-26), `if()` and `@function`
  (Limited; Firefox and Safari absent)
- MDN `position-anchor` (2026-05-11): "not Baseline because it does not work
  in some of the most widely-used browsers"
- OddBird, Winging It 31 (2026-04-16): anchor positioning "isn't baseline yet"
- Josh Comeau, Getting Started with Anchor Positioning (2026-07-07): ~81%
  support, level 2 Chromium-only, in Interop 2026
- MDN `CommandEvent` / `HTMLButtonElement.command`: Baseline 2025 Newly, Dec 2025
- pawelgrzybek.com (2026-01-27): invoker browser versions — Chrome 135, Edge
  135, Firefox 144, Safari 26.2
- State of CSS 2025: `:has()` most-used and most-loved; subgrid second most
  loved
- modern-css.com What's New (2026): secondary aggregator used only to
  cross-check the Enhance and Refuse tiers
