#!/usr/bin/env python3
"""
install_bricks_validator.py — put the Bricks validator where Claude Code will find it.

Dry run by default. Nothing is written without --apply.

  python install_bricks_validator.py                     # show the plan
  python install_bricks_validator.py --apply             # copy script, append CLAUDE.md block
  python install_bricks_validator.py --apply --patch-skill   # also rewrite SKILL.md checklist lines

Layout it produces (Windows: %USERPROFILE%\\.claude):

  ~/.claude/CLAUDE.md                              ← Bricks block appended once
  ~/.claude/skills/bricks/SKILL.md                 ← two checklist lines replaced (opt-in)
  ~/.claude/skills/bricks/scripts/bricks_validate.py
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUDE_DIR = Path.home() / ".claude"
SKILL_DIR = CLAUDE_DIR / "skills" / "bricks"
SCRIPTS_DIR = SKILL_DIR / "scripts"
SKILL_MD = SKILL_DIR / "SKILL.md"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
VALIDATOR = HERE / "bricks_validate.py"

MARKER = "## Bricks Builder JSON"

CLAUDE_BLOCK = """
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
"""

# The two hand-check items the script replaces. Matched exactly; if the skill
# text has drifted, the patch is skipped and reported rather than guessed at.
OLD_CHECKLIST = (
    "- [ ] JSON parses (`python3 -m json.tool file.json` or equivalent)\n"
    "- [ ] Every `parent`/`children` reference resolves; ids unique, 6-char alphanumeric\n"
)
NEW_CHECKLIST = (
    "- [ ] `python ${CLAUDE_SKILL_DIR}/scripts/bricks_validate.py <file> "
    "--existing <site-export> --acf <acf-export> <flags from PROJECT.md>` exits 0 "
    "— fix every ERROR before continuing\n"
)


def step(label: str, detail: str) -> None:
    print(f"  {label:<8} {detail}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry run)")
    ap.add_argument("--patch-skill", action="store_true", help="also replace the two SKILL.md checklist lines")
    args = ap.parse_args(argv)

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"{mode} — Claude directory: {CLAUDE_DIR}\n")

    if not VALIDATOR.exists():
        print(f"bricks_validate.py not found next to this installer at {VALIDATOR}", file=sys.stderr)
        return 2

    if not SKILL_MD.exists():
        print(f"bricks skill not found at {SKILL_DIR}. Install the skill first, then rerun.", file=sys.stderr)
        return 2

    # 1. validator → skill scripts folder
    dest = SCRIPTS_DIR / "bricks_validate.py"
    if dest.exists() and dest.read_bytes() == VALIDATOR.read_bytes():
        step("skip", f"{dest} already up to date")
    else:
        step("copy", f"{VALIDATOR.name} → {dest}")
        if args.apply:
            SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(VALIDATOR, dest)

    # 2. CLAUDE.md block, appended once
    existing = CLAUDE_MD.read_text(encoding="utf-8") if CLAUDE_MD.exists() else ""
    if MARKER in existing:
        step("skip", f"{CLAUDE_MD} already has the Bricks block")
    else:
        step("append", f"Bricks block → {CLAUDE_MD}")
        if args.apply:
            CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
            sep = "" if not existing or existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
            CLAUDE_MD.write_text(existing + sep + CLAUDE_BLOCK.lstrip("\n"), encoding="utf-8")

    # 3. SKILL.md checklist, opt-in and exact-match only
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    if NEW_CHECKLIST.strip() in skill_text:
        step("skip", f"{SKILL_MD} checklist already patched")
    elif not args.patch_skill:
        step("manual", f"{SKILL_MD}: replace the first two Validation Checklist items with:")
        print("           " + NEW_CHECKLIST.strip())
        print("           (or rerun with --patch-skill)")
    elif OLD_CHECKLIST in skill_text:
        step("patch", f"{SKILL_MD}: two checklist lines → validator line")
        if args.apply:
            SKILL_MD.write_text(skill_text.replace(OLD_CHECKLIST, NEW_CHECKLIST, 1), encoding="utf-8")
    else:
        step("manual", f"{SKILL_MD}: checklist text differs from expected; edit by hand (see Layer 3 in bricks-json-context.md)")

    print()
    if not args.apply:
        print("Nothing written. Rerun with --apply.")
    else:
        print("Done. Verify with:")
        print(f"  python \"{dest}\" --help")
    return 0


if __name__ == "__main__":
    sys.exit(main())
