# Bricks JSON — Global Context Layer

Context tells Claude what valid looks like. A validator refuses to let invalid
ship. You need both, and they live in different places.

```
~/.claude/CLAUDE.md                          ← 5 lines: when to load, what to run, what wins
~/.claude/skills/bricks/SKILL.md             ← knowledge (already have it; one line to add)
~/.claude/skills/bricks/scripts/bricks_validate.py   ← enforcement, travels with the skill
<project>/PROJECT.md                         ← site facts the skill cannot know
<project>/exports/                           ← ground truth: site export + ACF export
```

On Windows `~/.claude` is `%USERPROFILE%\.claude` — `C:\Users\William\.claude`.

Scripts live inside the skill folder, not beside it, because the skill is the
thing that knows when to run them and `${CLAUDE_SKILL_DIR}` resolves the path
whether the skill is installed personally, per-project, or as a plugin.

---

## Layer 1 — CLAUDE.md block

Paste into the global `~/.claude/CLAUDE.md`. Keep it this short; the skill
carries the detail.

```markdown
## Bricks Builder JSON

- Any task that reads or writes Bricks JSON: load the `bricks` skill, then read
  `PROJECT.md › Bricks` for site facts. Do not ask for a fact PROJECT.md already
  answers (rem base, versions, class policy, export paths).
- The site export and ACF export listed in PROJECT.md are ground truth for
  element ids, global class ids and names, ACF field names, and breakpoints.
  Never generate an id that exists in the export. Never reference an ACF field
  that is not in the export.
- Before delivering any Bricks JSON, run the skill's validator
  (`${CLAUDE_SKILL_DIR}/scripts/bricks_validate.py`) with the exports and flags
  from PROJECT.md, and fix every ERROR. Never deliver JSON that has not passed.
  Paste the validator's last line into the response.
- Where PROJECT.md contradicts the skill's defaults, PROJECT.md wins. Where the
  site's Bricks version differs from the version the skill was verified against,
  confirm setting shapes against Context7 or the Bricks changelog before trusting
  them.
```

---

## Layer 2 — PROJECT.md block, one per site

The skill's step 0 asks for the rem base on every session. This block answers
it once. Fill it at project init and re-export after any change made inside the
builder.

```markdown
## Bricks

| Fact | Value |
|---|---|
| Bricks version | `2.x.x` — from Bricks › Settings; the JSON `version` field must match |
| Skill verified against | `2.3.6` — if the site is newer, verify shapes before trusting them |
| ACSS version | `4.x` |
| rem base | `16px` — from `html { font-size }`; a 62.5% reset makes it 10px |
| Breakpoints | `tablet_portrait 991 · mobile_landscape 767 · mobile_portrait 478` (or custom) |
| Site export | `exports/site-YYYY-MM-DD.json` — Bricks › Templates › Export, or page export. Ground truth for ids and global classes |
| ACF export | `exports/acf-export-YYYY-MM-DD.json` — ACF › Tools › Export JSON. Ground truth for field names |
| Global class policy | `ride-along` **or** `cssClasses-only` (see below) |
| Color policy | `tokens-only` — `var()` and `color-mix()`; no raw hex |
| Token registry | `claude/DESIGN.md` or `acss-tokens.md` |
| Validator flags | `--no-hex` `--no-global-classes` (match the two policies above) |
| Re-export trigger | any global class, variable, or template edited in the builder UI |

### Global class policy — pick one and name it

**ride-along** — new classes are shipped as full objects in `globalClasses`,
referenced by `_cssGlobalClasses`. The skill's default. Every id must be new
and must not collide with the site export or Bricks skips it silently.

**cssClasses-only** — no `globalClasses` in clipboard JSON at all. BEM names go
in `_cssClasses` as plain strings; the classes are defined once in the site's
registry. Avoids collision entirely. This is the Pride in Turf convention.

These are not compatible in one file. State which the site uses.
```

---

## Layer 3 — Validator

`bricks_validate.py` lives inside the skill; PROJECT.md supplies its
arguments. Full command for a cssClasses-only, tokens-only site:

```bash
python ~/.claude/skills/bricks/scripts/bricks_validate.py bricks-json/section-hero.json \
  --existing exports/site-2026-09-10.json \
  --acf exports/acf-export-2026-09-10.json \
  --no-hex --no-global-classes
```

### Wire it into SKILL.md

Replace the first two items of the skill's **Validation Checklist** with one
line that runs the script. Everything the old items checked by eye, the script
now checks deterministically:

```markdown
- [ ] `python ${CLAUDE_SKILL_DIR}/scripts/bricks_validate.py <file> --existing <site-export> --acf <acf-export> <flags from PROJECT.md>` exits 0 — fix every ERROR before continuing
```

Keep the remaining checklist items (value shapes, breakpoint names, loop
wiring, dynamic tags); the script covers the structural ones but the
value-shape spot-check is still a judgement call.

What it enforces, and at what severity:

| Check | Severity | Why it's deterministic |
|---|---|---|
| Parses; clipboard envelope has `content`, `source`, `version`, or template export has `type` + `header`/`footer`/`content` + `global_classes` | error | Bricks rejects otherwise |
| Ids 6-char alphanumeric, unique | error | Bricks generates these; format is fixed |
| Parent ↔ children agree both ways | error | One-way links render as orphans or vanish |
| No nested `section` | error | Bricks structural rule |
| Responsive suffixes are real breakpoints or pseudo states | error | Unknown suffix is silently ignored |
| `query` present ⇒ `hasLoop: true`, `objectType` set | error | Loop silently does nothing otherwise |
| Every `_cssGlobalClasses` id has an object in `globalClasses` | error | Class silently not applied |
| Em/en dash or curly quote inside `@fallback:'…'` | error | Whole raw tag prints as visible text |
| Element or class id collides with the site export | error | Bricks skips the class; element id conflicts on paste |
| `{acf_*}` tag not in the ACF export | error | Produces broken `src="{"` and collapsed layout |
| Raw hex color (`--no-hex`) | warning → `--strict` promotes | Policy, not structure |
| Any `globalClasses` or `_cssGlobalClasses` (`--no-global-classes`) | warning → `--strict` promotes | Policy, not structure |
| Class *name* already exists with a different id | warning | Ambiguity, not breakage |
| Root element that isn't a section | warning | Legal in some template types |

Exit `0` pass, `1` errors, `2` input unreadable. `--json` for machine output.

**Extend it per site, not globally.** If a site has a recurring convention the
skill doesn't know — the `post_type: [...]` direct syntax vs the bare
`objectType` string that fails, or a required `tag` on every block — add a
site-local check file rather than editing the global tool. The global tool
should only encode what's true of every Bricks site.

---

## Layer 4 — What the validator cannot see

Bricks will accept JSON that passes every check above and still not do what you
meant. Three cases, all only catchable by a round-trip:

1. **Unknown setting keys.** `_fontSize` instead of `_typography.font-size`
   parses, validates, imports, and does nothing. The skill's rule 8 covers the
   intent; only paste-and-look proves it.
2. **Wrong value shape.** A color as a bare string, a shadow without `values`
   nesting. Structurally fine, visually absent.
3. **Version drift.** A shape that worked in 2.3.6 and changed in a later
   release.

For those, the round-trip is the test: paste into a staging page, screenshot,
compare. If you want it automated, the Bricks MCP in your stack can do a
programmatic insert followed by a rendered screenshot — that's the only true
end-to-end validator and it belongs in the delivery SOP, not the prompt.

---

## Read discipline — the half people skip

When Claude reads an existing export (page, template, site), the export is
authority for everything in it. Concretely:

- **Ids** — every element and class id in the export is reserved. New ids come
  from outside that set.
- **Class registry** — if a BEM name already exists as a global class, reference
  the existing id or use `_cssClasses`; never create a second class with the same
  name.
- **Field names** — read from the ACF export, never from memory or from what
  seems plausible.
- **Breakpoints** — if the site has customised them, the export shows the real
  suffixes; the skill's defaults are wrong for that site.
- **Version** — the export's `version` is the site's Bricks version. Use it in
  the JSON you write back.

If Claude is asked to modify an existing section, it should re-emit the whole
section with the same ids so the paste replaces rather than duplicates.

---

## Write discipline

1. Load the skill. Read PROJECT.md. Read the two exports.
2. Generate to a file, never inline: `bricks-json/{type}-{slug}.json`.
3. Run the validator with the site's flags.
4. Fix every error. Decide each warning consciously — don't suppress with
   `--strict` off just to pass.
5. Report: file path, format used, validator's final line, any warnings left
   and why.
6. Round-trip on staging before it goes near production.

---

## Install

Either run the installer (handles Windows and Unix paths, appends the CLAUDE.md
block only if it isn't there, never edits SKILL.md without `--patch-skill`):

```bash
python install_bricks_validator.py            # dry run: shows what it would do
python install_bricks_validator.py --apply    # copies the script, appends CLAUDE.md block
python install_bricks_validator.py --apply --patch-skill   # also rewrites the two checklist lines
```

Or by hand:

```bash
mkdir -p ~/.claude/skills/bricks/scripts
cp bricks_validate.py ~/.claude/skills/bricks/scripts/
# paste the Layer 1 block into ~/.claude/CLAUDE.md
# replace the first two Validation Checklist items in ~/.claude/skills/bricks/SKILL.md (Layer 3)
# paste the Layer 2 block into each Bricks site's PROJECT.md and fill it in
```

Then, in each site repo:

```bash
mkdir -p exports bricks-json
# Bricks › Templates › Export  →  exports/site-YYYY-MM-DD.json
# ACF › Tools › Export JSON   →  exports/acf-export-YYYY-MM-DD.json
```

Re-export both whenever anything changes in the builder UI. Stale exports make
the collision check lie.
