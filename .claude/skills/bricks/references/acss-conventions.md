> **Version note.** Written against ACSS 3.x. On a 4.x site read `../../modern-web-standards/references/acss-4-alignment.md` first: several utility classes below are unconfirmed in 4.x, `xxl` is now `2xl`, and the `@media (max-width)` examples should become `@container` queries. The **variables** listed here remain the trustworthy part.

# ACSS conventions — the allowlist

Everything here is confirmed against Automatic.css documentation (docs.automaticcss.com, retrieved
August 2026). **If a class or variable is not in this file, do not use it** — write a namespaced BEM class
styled with variables from this file instead.

ACSS is user-configurable. Sizes, palettes, and which utilities are generated all depend on the dashboard
settings of the specific site. Treat this file as the *shape* of the system, not a guarantee that every
listed token is enabled on a given install.

## Contents

- [How to verify anything not listed](#how-to-verify-anything-not-listed)
- [Layout and grid](#layout-and-grid)
- [Spacing](#spacing)
- [Typography](#typography)
- [Colour](#colour)
- [The BEM + variables pattern](#the-bem--variables-pattern)
- [Size scale](#size-scale)
- [What never to write](#what-never-to-write)

## How to verify anything not listed

Three options, cheapest first:

1. Ask the user to open the **ACSS cheat sheet** from their ACSS dashboard and paste the relevant section.
2. Ask them to open Bricks' **Class Manager** and search the class name.
3. Skip it. A namespaced BEM class using confirmed variables gets the same visual result with zero risk.

Option 3 is almost always right. Guessing costs more than the utility class saves.

## Layout and grid

| Pattern | Notes |
|---|---|
| `.grid--{1-12}` | Column count, applied to the **parent** container. Children are plain divs that default to full width of their cell |
| `.grid-gap` / `var(--grid-gap)` | Contextual gap between grid items. Preferred over generic `.gap--` on grids |
| `.container-gap` / `var(--container-gap)` | Spacing between multiple containers inside one section |
| `.content-gap` / `var(--content-gap)` | Even spacing between content elements (headings, text, images, buttons) inside a container |
| `.gap--{size}` | Shorthand gap; sets row and column together. Row/column can be set independently with the longer gap utilities |
| `var(--grid-{n})` | Grid template value for use inside a custom class, e.g. `grid-template-columns: var(--grid-3);` |
| `var(--content-width)` | The site's content width |
| `var(--gutter)` | The site's inline padding. Same value as `var(--section-padding-x)`, shorter and preferred |
| `.content-grid--off` | Opts an individual section out of Content Grid, if the site defaults sections to Content Grid |

**Content Grid caveat:** as of ACSS v3.0 a site can default all top-level sections to Content Grid, which
removes the section's inline padding and zeroes column gaps. If a layout comes back with unexpected
full-bleed behaviour, this is the likely cause — ask before working around it.

## Spacing

| Pattern | Notes |
|---|---|
| `var(--space-{size})` | The general-purpose spacing variable. Use for padding and gap inside custom classes |
| `var(--section-space-{size})` | Block padding for section elements. **M is applied to top-level sections by default** — don't restate it |
| `var(--gutter)` | Inline padding / gutter |
| `var(--card-gap)` | Contextual gap for card internals |

There is deliberately no `var(--pad-m)`. Padding uses `var(--space-{size})`.

## Typography

ACSS generates fluid type with `clamp()` from dashboard settings — every heading and body size is
calculated, with no manual breakpoints. Never write a `font-size` in px or rem.

| Pattern | Notes |
|---|---|
| `var(--text-{size})` | Body and UI text size, e.g. `var(--text-s)`, `var(--text-l)` |
| `var(--h1)` … `var(--h6)` | Heading sizes, for when a non-heading element needs heading scale |
| `.text--{size}` | Text size utility |

Prefer letting a semantic heading tag carry its own size. Reach for a size utility only when the visual
hierarchy genuinely differs from the document hierarchy.

## Colour

ACSS has a full colour system with shades and opacity variants generated from palette settings.
Confirmed variable shapes:

| Pattern | Notes |
|---|---|
| `var(--primary)` | Primary palette colour |
| `var(--base)`, `var(--base-dark)`, `var(--base-ultra-light)` | Neutral scale |
| `var(--action)` | Action/interactive colour |
| `var(--text)` | Body text colour |

Palette colour names beyond `primary` / `base` / `action` are site-specific (`secondary`, `accent`, `shade`
and their variants are common but configurable). Confirm before using, or stick to the four above.

**Never write a hex code.** It defeats the palette system, dark mode, and any later rebrand.

## Radius, shadow, and misc

| Pattern | Notes |
|---|---|
| `var(--radius-{size})` | Corner radius |

## The BEM + variables pattern

This is ACSS's own recommendation for reusable components, and it is the default for anything in this
skill that isn't plain layout:

```css
/* One intentional global class. Every value comes from the design system. */
.gg-testimonial-card {
  display: flex;
  flex-direction: column;
  padding: var(--space-m);
  gap: var(--space-m);
  border-radius: var(--radius-m);
  background: var(--base-ultra-light);
}
```

Responsive behaviour goes in a media query on the same custom class, referencing grid variables:

```css
@media (max-width: 991px) {
  .gg-service-grid { grid-template-columns: var(--grid-2); }
}
```

The class is global, so changing it later changes every instance — which is the whole point.

## Size scale

ACSS uses t-shirt sizing across spacing, text, and radius. The generated range depends on dashboard
settings, but the conventional scale is:

`xs` · `s` · `m` · `l` · `xl` · `xxl`

Use `m` as the default and move one step at a time. Jumping from `s` to `xxl` usually means the layout
is wrong, not the token.

## What never to write

| Don't | Because |
|---|---|
| `:root { --anything: … }` | Bricks converts these to Global Variables and they collide with ACSS |
| `.section { … }`, `.container { … }`, `.grid--3 { … }` | Redefining an ACSS class; the converter may write a colliding global class |
| `font-size: 1.25rem`, `#0b5d3a`, `padding: 48px` | Hardcoded values break fluid type, palettes, and contextual spacing |
| `.hero`, `.card`, `.btn` (unprefixed) | Too generic — collides with ACSS, the theme, or a plugin. Prefix it |
| A class you half-remember from ACSS docs | If it isn't in this file, it doesn't exist for your purposes |
