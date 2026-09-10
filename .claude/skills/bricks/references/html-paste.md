# HTML + CSS paste path

The second deliverable this skill produces: a single block of HTML (with an optional inline `<style>`)
that the user pastes directly onto the Bricks canvas. Bricks' native **HTML & CSS to Bricks** converter
turns it into real Bricks elements, global classes, and global variables. This is not a code
deliverable. It is an intermediate format whose only job is to survive that conversion cleanly.

Use this path when the user asks for HTML, is converting a Figma frame / competitor page / wireframe /
content brief, or wants a static section fast on an ACSS site. Use the JSON path (SKILL.md) when the
section needs query loops, dynamic data, conditions, interactions, popups, templates, or exact control
over element settings. Never mix both in one paste.

Two consequences shape everything below:

1. **The converter creates global classes from the classes in the markup.** Sloppy class naming writes
   permanent junk into the site's Class Manager, and global classes are *not* covered by Bricks revisions.
   There is no undo.
2. **The site already has a design system.** ACSS owns hundreds of classes and variables. The markup's job
   is to *reference* that system, never to restate or compete with it.

## Before writing markup

Work from what the conversation and `PROJECT.md` already contain. Ask only when the answer would change
the structure, and batch the questions at the top with the default you'll assume if the user says "just go":

1. Which site/client is this for? → default: use a generic `x-` class prefix and flag it for replacement.
2. Is this a one-off section or a repeating pattern (service card, location page hero)? → default: one-off,
   utility-class-led.
3. Any content supplied, or is placeholder copy fine? → default: write realistic placeholder copy for the
   client's actual industry, never lorem ipsum.
4. ACSS 3.x or 4.x? → the allowlist in `acss-conventions.md` is 3.x. On 4.x, utilities are unconfirmed;
   write BEM classes on variables (see `../../modern-web-standards/references/acss-4-alignment.md`).

Do **not** ask which ACSS classes exist. Instead follow the naming rule below, which is designed so that
you never need to know.

## The one rule that prevents damage

**Never invent an ACSS class name.** If a class is not in `acss-conventions.md`, do not write it.

That leaves two legitimate sources of styling, and every element uses one of them:

| Situation | Use | Why |
|---|---|---|
| Layout, spacing, grid, text size — things ACSS demonstrably has utilities for | ACSS utility classes from the allowlist | They already exist on the site; the converter matches them instead of creating new ones |
| A reusable component (card, quote form, testimonial, nav block) | A namespaced BEM class styled with ACSS **variables** | This is ACSS's own recommended pattern, and it means the one new global class the converter creates is intentional and findable |
| Anything you're unsure about | Namespaced BEM class + ACSS variables | The safe default. A named custom class is a known cost; a guessed utility class is silent breakage |

Namespace every custom class with a short client prefix: `gg-hero__media`, `cm-quote__field`,
`pit-service-card__icon`. When the user later opens the Class Manager, every class you created is
identifiable at a glance and removable in one pass.

## Hard constraints

- **Never emit a `:root` block.** Bricks converts `:root` variables into Bricks Global Variables, which
  collides head-on with ACSS's variable set and is not revision-protected.
- **Never redefine an ACSS class.** No `.section { padding-block: 5rem; }`. If the default is wrong, use a
  different ACSS size modifier or set the value on a custom class.
- **Never emit `<script>` or external `<link>` tags.** Bricks quarantines them into a Code element that must
  be manually reviewed and signed. If interactivity is needed, describe it in the handoff notes and let the
  user build it with Bricks interactions.
- **Never hardcode a colour, font size, or spacing value.** Use `var(--primary)`, `var(--text-l)`,
  `var(--space-m)`. A hex code in the output is a bug: it breaks the site's dark mode, palette shifts, and
  fluid type.
- **Never emit an ACSS `?recipe` token.** Recipes expand only in the builder's CSS input. In a paste they
  ship as literal text. Write the CSS the recipe produces, or add a post-paste step.
- **Custom CSS goes in one `<style>` block at the top of the paste**, containing only namespaced classes.

## Structure conventions

- Semantic HTML: `<section>`, `<header>`, `<nav>`, `<article>`, `<figure>`, `<h1>`–`<h4>` in order.
  The converter maps standard tags to native Bricks elements, so semantics you write are semantics you keep.
- One `<h1>` per page. Section headings are `<h2>`. Never skip a level to get a size; size comes from a
  text utility class or variable.
- The canonical nesting is `section > container > content`. ACSS applies section spacing and gutters at that
  level; breaking the pattern means fighting the framework.
- Images: real `alt` text describing the image, `loading="lazy"` on everything below the fold, explicit
  `width`/`height` when known. Use a descriptive placeholder `src` path; the user swaps in media after paste.
- Local SEO context: where a section names a service area, write the real place names into the copy rather
  than a `{{city}}` token, unless the user has said the section is a template for programmatic pages.

## Output format

Return exactly this structure, in this order:

```
## What this builds
One or two lines. What the section is and any assumption you made.

## Paste into Bricks
[one fenced html block — the complete paste, <style> first if custom classes exist]

## New global classes this creates
| Class | Purpose |
|---|---|
(only custom classes — do not list ACSS utilities, which already exist)

## After pasting
1. Numbered manual steps: media to swap, links to wire, interactions to add,
   dynamic data or ACF fields to bind, anything the converter can't do.
```

Keep the HTML in **one** fenced block. Splitting it across blocks makes the user paste twice and produces
two disconnected element trees.

## Handing it over

State these once, briefly, the first time in a conversation:

- Set `Bricks > Settings > Builder > HTML & CSS to Bricks` to **"Enabled (confirm on paste)"** so nothing
  converts silently.
- Paste onto a staging or local copy first. Global class writes have no revision history.
- The converter needs the "Create global classes" permission on the acting user.

After the user reports back, expect structure to be close and styling to need a pass; the site's existing
theme styles and plugin CSS interact with the pasted rules. Offer to adjust the markup rather than telling
them to fix it in the builder. Regenerating is cheaper than hand-editing converted elements.

## Worked examples

`section-patterns.md` has the full output format for a service grid, plus hero, FAQ, CTA band, and
contact form markup. Adapt the shapes; do not copy verbatim.
