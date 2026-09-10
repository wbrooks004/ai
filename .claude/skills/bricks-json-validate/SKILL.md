---
name: bricks-json-validate
description: Deterministic validator for Bricks Builder clipboard JSON, plus the read/write discipline that keeps Claude honest about site exports. Use before delivering ANY Bricks JSON (sections, templates, edits to exported JSON) and whenever reading an existing Bricks or ACF export. Pairs with the `bricks` skill (which knows the shapes) — this skill enforces structure, id collisions, ACF field names, breakpoint keys, and colour/class policy, and refuses to let invalid JSON ship.
---

# Bricks JSON validation

Context tells Claude what valid looks like. This validator refuses to let invalid
ship. Both are required; "Bricks accepted the paste" is not evidence of correctness,
because Bricks silently ignores unknown keys and silently skips colliding class ids.

## Run it

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/bricks_validate.py <file.json> \
  --existing <site-export.json> \
  --acf <acf-export.json> \
  <flags from PROJECT.md>            # e.g. --no-hex --no-global-classes --strict
```

- Exit `0` pass, `1` errors, `2` input unreadable. `--json` for machine output.
- `--breakpoints a,b,c` when the site has custom Bricks breakpoint keys.
- Fix every ERROR. Decide each WARNING consciously; never suppress to pass.
- Paste the validator's last line into the delivery report.

## Read discipline

The site export and ACF export are ground truth. Every id in them is reserved.
Every ACF field name comes from the export, never from memory. If a BEM class name
already exists as a global class, reference the existing id or use `_cssClasses`;
never create a second class with the same name. When editing an existing section,
re-emit it whole with the same ids so the paste replaces instead of duplicating.

## Write discipline

1. Load the `bricks` skill. Read `PROJECT.md › Bricks`. Read the two exports.
2. Generate to a file, never inline: `bricks-json/{type}-{slug}.json`.
3. Run the validator with the site's flags.
4. Fix errors; decide warnings.
5. Report: file path, format used, validator's final line, warnings left and why.
6. Round-trip on staging before production. The validator cannot see unknown
   setting keys, wrong value shapes, or version drift; only a paste can.

## References

- `references/bricks-json-context.md` — the four-layer model (global CLAUDE.md
  block, per-site PROJECT.md block, validator, what it cannot see), the full
  check table, and install notes for `~/.claude` on a local machine.
- `scripts/install_bricks_validator.py` — installs the validator into a local
  `~/.claude/skills/bricks/scripts/` and appends the CLAUDE.md block. Dry run
  by default; `--apply` to write; `--patch-skill` to rewrite the checklist.
