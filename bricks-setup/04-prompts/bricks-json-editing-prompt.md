# Bricks JSON Editing Prompt

Reusable prompt for asking an AI assistant to modify exported Bricks Builder JSON. Copy everything between the
`---- PROMPT START ----` and `---- PROMPT END ----` markers, fill in the four input blocks, and send.

Works with clipboard JSON (`source: "bricksCopiedElements"`) and template exports. Verified against Bricks 2.3.6 shapes.

---

```
---- PROMPT START ----

You are editing Bricks Builder JSON. Bricks stores a page as a FLAT array of element nodes. Hierarchy lives only in
each node's `parent` and `children` ids. Unknown settings keys are silently ignored, wrong value shapes silently fail,
and global classes have no revision history. Precision matters more than speed.

## Inputs

### Change requested
[Describe the change in plain words. One change per request is safest. Examples:
 "Make the three service cards use the global class gg-card--elevated instead of inline box shadows."
 "Add a fourth card that duplicates the third, change its heading to 'Water Heaters', link to /water-heaters/."
 "Swap the hero background colour to var(--primary-dark) and reduce section padding on mobile_portrait to var(--space-l)."]

### Context
- rem base on this site (what 1rem equals): [16px]
- Class prefix for this client: [gg]
- Bricks version: [2.3.6]
- Breakpoint keys: [tablet_portrait, mobile_landscape, mobile_portrait]
- ACF field names in play, if any: [none]
- Anything else that must not change: [none]

### JSON
[Paste the full exported JSON here.]

## Rules

Editing scope
1. Change only what the request describes. Do not reformat, reorder, relabel, or "improve" anything else.
2. Preserve every existing `id` exactly. Never renumber or regenerate ids that already exist.
3. New elements get new unique 6-character alphanumeric ids that do not collide with any existing id in the file.
4. When adding a node: add its id to the parent's `children` array in the correct position, set its `parent` to that
   parent's id, and include a `children` array (empty if a leaf) and a `settings` object (never an array).
5. When removing a node: remove it from its parent's `children`, and remove every descendant node too.
6. When duplicating a node: deep-copy the subtree, give every copied node a fresh id, and rewrite every internal
   `parent` / `children` reference to the new ids.

Value shapes (silent failure if wrong)
7. Colours are objects: `{"hex": "#1d4ed8"}`, `{"rgb": "rgba(0,0,0,.5)"}`, or `{"raw": "var(--primary)"}`. Never a bare string.
8. Typography keys are CSS property names: `"font-size"`, `"font-weight"`, `"line-height"`, `"text-transform"`. Never camelCase.
9. Spacing (`_margin`, `_padding`) is a per-side object: `{"top": "2rem", "right": "0", "bottom": "2rem", "left": "0"}`.
   Values are strings with units. Bare numbers get `px` appended by Bricks.
10. Box shadow offsets nest under `values`: `{"values": {"offsetX": "0", "offsetY": "4", "blur": "16", "spread": "0"}, "color": {...}}`.
11. Gradients use `"colors": [{"color": {...}, "stop": "0"}, ...]`, never `stops`.
12. Border radius is per-corner: `"_border": {"radius": {"top": "8px", "right": "8px", "bottom": "8px", "left": "8px"}}`.
13. Responsive and state suffixes use colons, breakpoint before pseudo: `_padding:tablet_portrait`, `_background:hover`,
    `_margin:mobile_portrait:hover`. Only the breakpoint keys listed in Context. Only `:hover`, `:active`, `:focus` as pseudos.
14. Custom CSS on an element (`_cssCustom`) uses `%root%` as the element selector. Custom CSS inside a global class uses
    the literal class selector.
15. Do not invent settings keys. If the change needs a key you are not certain exists in Bricks 2.3.6, stop and say so
    instead of guessing.

Global classes
16. Any id placed in an element's `_cssGlobalClasses` array must have a full class object in the top-level `globalClasses`
    array (or `global_classes` in a template export). If the class exists on the site but not in the file, ask for its id.
17. New class names start with the client prefix and follow `{prefix}-{block}__{element}--{modifier}`. No unprefixed names.
18. Never edit the `settings` of an existing global class unless the request explicitly says to. Class edits affect every
    instance site-wide.

Design system
19. Prefer `{"raw": "var(--...)"}` ACSS variables over hex, px, or rem for colour, spacing, radius, and type size.
20. Do not add a `:root` block anywhere in any `_cssCustom` string.
21. Keep one `h1` per page. Do not change heading levels to change size.

## Output

Return exactly these four parts, in order:

1. **Changes made** — a bulleted list in plain words, one bullet per node touched, with the node id and label.
   Example: "`hdg4f2` (Heading: Services H2) — text changed from 'Our Services' to 'Plumbing Services'."
2. **New ids introduced** — list, or "none".
3. **New or modified global classes** — table of id, name, what changed, or "none".
4. **Complete JSON** — the whole file, valid JSON, in one fenced block. Never a partial or a diff. Never truncated.
   If the file is too long to return in one message, say so before starting and propose splitting the request.

## Self-check before answering

Confirm each of these and state "Self-check passed" at the top of the reply, or list the failures:
- [ ] JSON is valid (balanced braces, no trailing commas, no comments).
- [ ] Every `parent` id refers to a node that lists this node in `children` (or is `0` for roots).
- [ ] Every id in every `children` array exists as a node whose `parent` points back.
- [ ] No duplicate ids.
- [ ] Every `_cssGlobalClasses` id exists in the top-level class array.
- [ ] No camelCase typography keys, no bare-string colours, no bare-number spacing.
- [ ] Only the breakpoint and pseudo suffixes allowed above.
- [ ] Nothing outside the requested change was altered.

---- PROMPT END ----
```

---

## Worked example

Request block filled in:

```
### Change requested
On the services grid, the third card (label "Block: Service Card — Sump Pumps") is missing its icon. Duplicate the
icon element from the first card into the third card, placed before the heading, and set its icon to
`ti-droplet` from the Themify library.

### Context
- rem base: 16px
- Class prefix: gg
- Bricks version: 2.3.6
- Breakpoint keys: tablet_portrait, mobile_landscape, mobile_portrait
- ACF field names in play: none
- Must not change: card order, existing classes
```

Expected shape of the reply:

```
Self-check passed

**Changes made**
- `crd3aa` (Block: Service Card — Sump Pumps) — added `icn3aa` as first child.
- `icn3aa` (Icon: Sump Pumps) — new node, copied from `icn1aa`, icon set to Themify `ti-droplet`.

**New ids introduced**
- `icn3aa`

**New or modified global classes**
none

**Complete JSON**
{ ...full file... }
```

---

## Variants

**Batch edits.** If you must send more than one change, number them in the request block and ask for "Changes made"
grouped by number. Still one JSON output.

**Template exports.** Same prompt. Add to Context: "This is a template export; elements live under the `header`,
`content`, or `footer` key, and classes live under `global_classes`."

**Validation only.** Replace the "Change requested" block with "Do not change anything. Run the self-check and report
every failure with the node id." Useful before pasting third-party JSON into a client site.
