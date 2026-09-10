# Bricks Class Naming System

For Bricks Builder sites running ACSS. Goal: every class in the Class Manager is either an ACSS utility or a class you
can identify, find, and delete at a glance. Bricks global classes have no revision history, so naming is the only
undo you get.

---

## 1. The three layers

| Layer | Who owns it | You write it? | Example |
|-------|-------------|---------------|---------|
| **ACSS utilities** | Automatic.css | Yes, but only names you can confirm exist on the install | `grid--3`, `text--l`, `gap--m`, `content-gap` |
| **Project components** | You, per client | Yes, this is the system below | `gg-service-card`, `gg-service-card__icon` |
| **Element inline settings** | Bricks element | Yes, for one-offs only | Padding set directly on a single hero block |

Rule of thumb: layout and spacing come from ACSS utilities. Anything with a name a designer would use ("card",
"testimonial", "eyebrow") becomes a prefixed component class. Anything used exactly once stays inline.

---

## 2. The pattern

```
{prefix}-{block}
{prefix}-{block}__{element}
{prefix}-{block}--{modifier}
{prefix}-{block}__{element}--{modifier}
```

| Part | Rules |
|------|-------|
| `prefix` | 2 to 4 lowercase letters, unique per client. Derived from the business name. Never `acss`, `brx`, `brxe`, `bricks`, `wp`, `x` in production. |
| `block` | Noun, lowercase, hyphen-separated, describes the thing not the look. `service-card`, not `blue-box`. |
| `element` | Child part of the block. Double underscore. One level deep only: `card__title`, never `card__header__title`. |
| `modifier` | Variant or state that changes the look. Double hyphen. `--featured`, `--dark`, `--compact`. |

### Examples for a client prefixed `gg`

| Class | Meaning |
|-------|---------|
| `gg-hero` | Hero section wrapper |
| `gg-hero__media` | Image or video frame inside the hero |
| `gg-hero--overlay` | Hero variant with a dark overlay |
| `gg-service-card` | A service card component |
| `gg-service-card__icon` | Icon slot in the card |
| `gg-service-card--featured` | Highlighted card variant |
| `gg-nap` | Name, address, phone block for local SEO |
| `gg-nap__phone` | Phone link inside it |

### Choosing the prefix

Pick from the business name and check it against the reserved list.

| Business | Prefix |
|----------|--------|
| Gagnon Plumbing | `gg` or `gpl` |
| To The Top SEO | `ttt` |
| Find Me Solutions | `fms` |
| Clinique Mont-Royal | `cmr` |

Reserved, never use: `acss`, `brx`, `brxe`, `bricks`, `wp`, `wc`, `woo`, `acf`, `is`, `has`, `js`, `u`, `l`, `c`, `o`.

---

## 3. State and hook classes (not styled by you)

| Prefix | Purpose | Notes |
|--------|---------|-------|
| `is-` / `has-` | Runtime state toggled by JS or Bricks interactions | `is-open`, `has-video`. Never create as a global class. Apply via interactions or `_attributes`. |
| `js-` | JavaScript hook only, zero styling | `js-toggle-hours`. Keeps behaviour decoupled from styling. |
| `brxe-` | Bricks element classes | Bricks generates these. Never write them, never style them directly in global classes. |

---

## 4. Decision flow: class or not

```
Is it layout, spacing, grid, or text size?
  └─ Yes → ACSS utility (only if confirmed on this install). Done.
  └─ No ↓
Will it appear on the page or site more than once?
  └─ No → inline element settings. Done.
  └─ Yes ↓
Is it a component (has parts, has a name a designer would use)?
  └─ Yes → {prefix}-{block} + __element classes. Global class. Done.
  └─ No → single {prefix}-{block} global class with ACSS variables. Done.
```

---

## 5. Class Manager hygiene

- **Categories**: create one Bricks class category per prefix. Every component class goes in it. ACSS classes stay uncategorised.
- **Audit query**: in Class Manager, search the prefix. Anything not returned by that search and not an ACSS class is a
  candidate for deletion.
- **Never rename in place** after launch. Renaming a global class changes the CSS selector but not any `_cssCustom`
  strings or HTML attributes that reference the old name. Create the new class, migrate, then delete.
- **Unused classes**: Bricks does not warn. Audit quarterly with the search above.

---

## 6. Structure panel labels

Labels are not classes, but the same discipline applies. Label every element in the structure panel so the tree reads
like an outline:

```
Section: Services
  Container
    Block: Section Header
      Heading: Services H2
      Text: Services intro
    Block: Services Grid
      Block: Service Card — Drain Cleaning
```

Format: `{Element type}: {What it is}`. Use the em dash to append the instance name. Labels live in the element's `label`
key in JSON.

---

## 7. IDs

- Do not set `_cssId` for styling. IDs are for anchor targets (`#pricing`, `#contact`) and form field wiring only.
- Anchor IDs: lowercase, hyphenated, no prefix. They appear in URLs.

---

## 8. Forbidden names, with replacements

| Never | Because | Write instead |
|-------|---------|---------------|
| `.card`, `.hero`, `.btn`, `.wrapper`, `.container`, `.section` | Collides with ACSS, theme, or plugins | `.gg-card`, `.gg-hero` |
| `.blue-text`, `.big-heading`, `.mt-40` | Describes the look, not the thing. Breaks on rebrand | `.gg-eyebrow`, ACSS `text--l`, `var(--space-l)` |
| `.card__header__title` | Nested BEM. Unreadable and brittle | `.gg-card__title` |
| `.gg-Card`, `.gg_card`, `.ggCard` | Wrong separators | `.gg-card` |
| `.acss-*`, `.brxe-*` | Reserved namespaces | Any project prefix |
| `.section-padding-fix`, `.temp`, `.test2` | Untraceable intent | Name the component or delete it |

---

## 9. Quick reference card

```
{prefix}-{block}__{element}--{modifier}

prefix   2–4 letters, per client        gg
block    noun, what it is               service-card
element  __ child part, one level       __icon
modifier -- variant or look             --featured
state    is- / has-  (never global)     is-open
hook     js-  (never styled)            js-toggle

ACSS for layout. Prefix for components. Inline for one-offs.
```
