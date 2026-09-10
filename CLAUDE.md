# CLAUDE.md — wbrooks004/ai

Config and skills for building WordPress sites with Bricks Builder, Automatic.css
(ACSS) 4.x, and ACF Pro. Project skills live in `.claude/skills/`. Reference docs
and starter files live in `bricks-setup/`.

## Bricks Builder JSON

- Any task that reads or writes Bricks JSON: load the `bricks` skill, then read
  `PROJECT.md › Bricks` for site facts. Do not ask for a fact PROJECT.md already
  answers (rem base, versions, class policy, export paths). If there is no
  PROJECT.md, ask for rem base, class prefix, Bricks version, and ACSS version once.
- The site export and ACF export listed in PROJECT.md are ground truth for
  element ids, global class ids and names, ACF field names, and breakpoints.
  Never generate an id that exists in the export. Never reference an ACF field
  that is not in the export.
- Before delivering any Bricks JSON, run the validator
  (`.claude/skills/bricks-json-validate/scripts/bricks_validate.py`) with the
  exports and flags from PROJECT.md, and fix every ERROR. Never deliver JSON that
  has not passed. Paste the validator's last line into the response.
- Where PROJECT.md contradicts a skill's defaults, PROJECT.md wins. Where the
  site's Bricks version differs from the version the skill was verified against
  (2.3.6), confirm setting shapes against Context7 or the Bricks changelog before
  trusting them.

## CSS and HTML

- Any CSS or HTML that will land on an ACSS site, including `_cssCustom` strings
  inside Bricks JSON, follows the `modern-web-standards` skill: ACSS variables
  only, container queries over viewport queries, `light-dark()` via tokens, no
  hex, no px/rem sizes, no `?recipe` tokens in paste output.
- ACSS 3.x and 4.x are not compatible. Confirm which one the site runs before
  applying 4.x rules. `bricks-setup/` was written against 3.x.

## Content

- English only. If source material is in French, reproduce it verbatim, mark it
  `[FR — owner to proofread]`, and do not translate or fix it.
