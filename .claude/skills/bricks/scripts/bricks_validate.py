#!/usr/bin/env python3
"""
bricks_validate.py — deterministic validator for Bricks Builder clipboard JSON and template exports.

Structural failures are ERRORS (exit 1). Convention failures are WARNINGS unless
--strict promotes them. Bricks silently ignores unknown keys and silently skips
colliding global-class IDs, so "Bricks accepted it" is not evidence of
correctness — this script is.

Usage
  python bricks_validate.py section.json
  python bricks_validate.py section.json --existing site-export.json --acf acf-export.json
  python bricks_validate.py section.json --no-hex --no-global-classes --strict
  python bricks_validate.py section.json --breakpoints tablet_portrait,mobile_landscape,mobile_portrait
  python bricks_validate.py section.json --json

Exit codes
  0  valid (warnings may be present)
  1  one or more errors
  2  could not read or parse input
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

# --------------------------------------------------------------------------- #
# Rules and defaults                                                          #
# --------------------------------------------------------------------------- #

ID_RE = re.compile(r"^[a-zA-Z0-9]{6}$")
DEFAULT_BREAKPOINTS = {"tablet_portrait", "mobile_landscape", "mobile_portrait"}
DEFAULT_PSEUDOS = {"hover", "focus", "focus-visible", "active", "visited", "before", "after"}
CLIPBOARD_SOURCE = "bricksCopiedElements"
TEMPLATE_ELEMENT_KEYS = ("content", "header", "footer")   # template exports keep elements under the key matching `type`

# Characters that break Bricks dynamic-tag fallbacks: the whole raw tag prints.
BAD_FALLBACK_CHARS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u2018": "curly single quote",
    "\u2019": "curly single quote",
    "\u201c": "curly double quote",
    "\u201d": "curly double quote",
}
FALLBACK_RE = re.compile(r"@fallback:(['\"])(.*?)\1")
ACF_TAG_RE = re.compile(r"\{acf_([A-Za-z0-9_]+)")
HEX_IN_CSS_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|#[0-9a-fA-F]{8}\b")


# --------------------------------------------------------------------------- #
# Report                                                                      #
# --------------------------------------------------------------------------- #

@dataclass
class Report:
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)
    strict: bool = False

    def error(self, code: str, msg: str, where: str = "") -> None:
        self.errors.append({"code": code, "where": where, "msg": msg})

    def warn(self, code: str, msg: str, where: str = "") -> None:
        target = self.errors if self.strict else self.warnings
        target.append({"code": code, "where": where, "msg": msg})

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> str:
        lines: list[str] = []
        for label, items in (("ERROR", self.errors), ("WARN", self.warnings)):
            for it in items:
                where = f" [{it['where']}]" if it["where"] else ""
                lines.append(f"{label:5} {it['code']:<24}{where}  {it['msg']}")
        summary = f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)"
        lines.append(("PASS  " if self.ok else "FAIL  ") + summary)
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

def load_json(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"cannot read {path}: file not found", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"{path} is not valid JSON: line {e.lineno} col {e.colno}: {e.msg}", file=sys.stderr)
        sys.exit(2)


def walk_strings(obj: Any, path: str = "") -> Iterator[tuple[str, str]]:
    """Yield (json_path, string) for every string value in a nested structure."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


def walk_dicts(obj: Any, path: str = "") -> Iterator[tuple[str, dict]]:
    """Yield (json_path, dict) for every dict in a nested structure."""
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            yield from walk_dicts(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_dicts(v, f"{path}[{i}]")


def collect_content_lists(export: Any) -> list[list[dict]]:
    """
    Pull every element list out of a Bricks export. Handles clipboard JSON
    ({content:[...]}), template exports ({content|header|footer:[...]}),
    a bare element list, and a list of template objects.
    """
    found: list[list[dict]] = []
    if isinstance(export, list):
        if export and isinstance(export[0], dict) and "id" in export[0] and "name" in export[0]:
            found.append(export)
        else:
            for item in export:
                found.extend(collect_content_lists(item))
    elif isinstance(export, dict):
        for key in ("content", "header", "footer", "data"):
            val = export.get(key)
            if isinstance(val, list):
                found.extend(collect_content_lists(val) or [val])
    return found


def collect_existing(export_paths: list[str]) -> tuple[set[str], dict[str, str], set[str]]:
    """Return (element_ids, global_class_id->name, global_class_names) from site exports."""
    element_ids: set[str] = set()
    class_ids: dict[str, str] = {}
    class_names: set[str] = set()
    for p in export_paths:
        data = load_json(p)
        for lst in collect_content_lists(data):
            for node in lst:
                if isinstance(node, dict) and isinstance(node.get("id"), str):
                    element_ids.add(node["id"])
        for _, d in walk_dicts(data):
            gcs = d.get("globalClasses")
            if isinstance(gcs, list):
                for gc in gcs:
                    if isinstance(gc, dict) and isinstance(gc.get("id"), str):
                        class_ids[gc["id"]] = str(gc.get("name", ""))
                        if gc.get("name"):
                            class_names.add(str(gc["name"]))
    return element_ids, class_ids, class_names


def collect_acf_field_names(acf_export: Any) -> set[str]:
    """Recursively collect every field `name` from an ACF JSON export."""
    names: set[str] = set()

    def rec(fields: Any) -> None:
        if not isinstance(fields, list):
            return
        for f in fields:
            if not isinstance(f, dict):
                continue
            if isinstance(f.get("name"), str) and f["name"]:
                names.add(f["name"])
            rec(f.get("sub_fields"))
            layouts = f.get("layouts")
            if isinstance(layouts, dict):
                for lay in layouts.values():
                    if isinstance(lay, dict):
                        rec(lay.get("sub_fields"))

    groups = acf_export if isinstance(acf_export, list) else [acf_export]
    for g in groups:
        if isinstance(g, dict):
            rec(g.get("fields"))
    return names


# --------------------------------------------------------------------------- #
# Checks                                                                      #
# --------------------------------------------------------------------------- #

def is_template_export(data: Any) -> bool:
    """Bricks › Templates › Export shape: {name, title, type, header|footer|content, global_classes, ...}."""
    return (isinstance(data, dict) and "type" in data and data.get("source") != CLIPBOARD_SOURCE
            and any(isinstance(data.get(k), list) for k in TEMPLATE_ELEMENT_KEYS))


def global_classes_of(data: dict) -> list:
    """Clipboard JSON uses `globalClasses`; template exports use `global_classes`."""
    gcs = data.get("globalClasses")
    if gcs is None:
        gcs = data.get("global_classes")
    return gcs if isinstance(gcs, list) else []


def check_envelope(data: Any, rep: Report) -> list[dict]:
    if not isinstance(data, dict):
        rep.error("ENVELOPE", "top level must be an object with a `content` array")
        return []
    if is_template_export(data):
        content: list = []
        for key in TEMPLATE_ELEMENT_KEYS:
            if isinstance(data.get(key), list):
                content.extend(data[key])
        if not content:
            rep.error("ENVELOPE", "template export has no elements under `content`, `header`, or `footer`")
        if not isinstance(data.get("type"), str) or not data["type"]:
            rep.error("ENVELOPE", "template export `type` must be a non-empty string (header, footer, popup, section, ...)", "type")
        for key in ("global_classes", "globalVariables"):
            if key in data and not isinstance(data[key], list):
                rep.error("ENVELOPE", f"`{key}` must be an array", key)
        return [n for n in content if isinstance(n, dict)]
    content = data.get("content")
    if not isinstance(content, list):
        rep.error("ENVELOPE", "`content` missing or not an array")
        content = []
    if data.get("source") != CLIPBOARD_SOURCE:
        rep.error("ENVELOPE", f"`source` must be \"{CLIPBOARD_SOURCE}\"", "source")
    if not isinstance(data.get("version"), str) or not data["version"]:
        rep.error("ENVELOPE", "`version` must be a non-empty string matching the target site's Bricks version", "version")
    for key in ("globalClasses", "globalElements"):
        if key in data and not isinstance(data[key], list):
            rep.error("ENVELOPE", f"`{key}` must be an array", key)
    return [n for n in content if isinstance(n, dict)] if content else []


def check_tree(nodes: list[dict], rep: Report, root_must_be_section: bool = True) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    for i, n in enumerate(nodes):
        nid = n.get("id")
        where = f"content[{i}]"
        if not isinstance(nid, str) or not ID_RE.match(nid):
            rep.error("ID_FORMAT", f"id must be 6 alphanumeric chars, got {nid!r}", where)
            continue
        if nid in by_id:
            rep.error("ID_DUPLICATE", f"element id {nid} appears more than once", where)
            continue
        by_id[nid] = n
        if not isinstance(n.get("name"), str) or not n["name"]:
            rep.error("NODE_SHAPE", "`name` missing", nid)
        if "settings" in n and not isinstance(n["settings"], dict):
            rep.error("NODE_SHAPE", "`settings` must be an object", nid)
        if "children" in n and not isinstance(n["children"], list):
            rep.error("NODE_SHAPE", "`children` must be an array", nid)

    for nid, n in by_id.items():
        parent = n.get("parent", 0)
        children = n.get("children") or []

        if parent in (0, "0", None):
            if root_must_be_section and n.get("name") != "section":
                rep.warn("ROOT_NOT_SECTION", f"root element is `{n.get('name')}`; root nodes are normally sections", nid)
        else:
            if not isinstance(parent, str) or parent not in by_id:
                rep.error("ORPHAN", f"parent {parent!r} does not exist", nid)
            else:
                if nid not in (by_id[parent].get("children") or []):
                    rep.error("TREE_ONE_WAY", f"parent {parent} does not list {nid} in its children", nid)
                if n.get("name") == "section":
                    rep.error("NESTED_SECTION", "a section can never be nested inside another element", nid)

        seen: set[str] = set()
        for c in children:
            if c in seen:
                rep.error("CHILD_DUPLICATE", f"child {c} listed twice", nid)
            seen.add(c)
            if c not in by_id:
                rep.error("CHILD_MISSING", f"child {c} is not a node in `content`", nid)
            elif by_id[c].get("parent") != nid:
                rep.error("TREE_ONE_WAY", f"child {c} has parent {by_id[c].get('parent')!r}, expected {nid}", nid)
    return by_id


def check_settings(by_id: dict[str, dict], data: dict, rep: Report,
                   breakpoints: set[str], pseudos: set[str]) -> None:
    global_classes = global_classes_of(data)
    gc_ids = {gc.get("id") for gc in global_classes if isinstance(gc, dict)}

    for nid, n in by_id.items():
        s = n.get("settings") or {}
        if not isinstance(s, dict):
            continue

        for key in s:
            if ":" not in key:
                continue
            for seg in key.split(":")[1:]:
                if seg not in breakpoints and seg not in pseudos:
                    rep.error("RESPONSIVE_KEY", f"`{key}`: `{seg}` is not a known breakpoint or pseudo state (Bricks ignores it silently)", nid)

        has_query = "query" in s
        has_loop = s.get("hasLoop") is True
        if has_query and not has_loop:
            rep.error("LOOP_FLAG", "element carries `query` but `hasLoop` is not true", nid)
        if has_loop and not has_query:
            rep.warn("LOOP_NO_QUERY", "`hasLoop: true` without a `query` object", nid)
        if has_query:
            q = s["query"]
            if not isinstance(q, dict) or not q.get("objectType"):
                rep.error("LOOP_SHAPE", "`query.objectType` missing", nid)

        refs = s.get("_cssGlobalClasses")
        if refs is not None:
            if not isinstance(refs, list):
                rep.error("GLOBAL_CLASS_SHAPE", "`_cssGlobalClasses` must be an array of class ids", nid)
            else:
                for r in refs:
                    if r not in gc_ids:
                        rep.error("GLOBAL_CLASS_MISSING", f"references global class {r} but no object with that id is in `globalClasses`", nid)

    for i, gc in enumerate(global_classes):
        if not isinstance(gc, dict):
            rep.error("GLOBAL_CLASS_SHAPE", "entry is not an object", f"globalClasses[{i}]")
            continue
        if not isinstance(gc.get("id"), str) or not ID_RE.match(gc["id"]):
            rep.error("GLOBAL_CLASS_ID", f"global class id must be 6 alphanumeric chars, got {gc.get('id')!r}", f"globalClasses[{i}]")
        if not gc.get("name"):
            rep.error("GLOBAL_CLASS_NAME", "global class has no `name`", f"globalClasses[{i}]")


def check_conventions(data: dict, by_id: dict[str, dict], rep: Report, *,
                      no_hex: bool, no_global_classes: bool,
                      existing_ids: set[str], existing_class_ids: dict[str, str],
                      existing_class_names: set[str], acf_names: set[str] | None) -> None:

    # --- dynamic-tag fallback punctuation (always checked; breaks rendering) ---
    for path, s in walk_strings(data):
        for m in FALLBACK_RE.finditer(s):
            for ch, label in BAD_FALLBACK_CHARS.items():
                if ch in m.group(2):
                    rep.error("FALLBACK_PUNCT", f"{label} inside @fallback — the whole raw tag will print as text", path)

    # --- raw hex ---
    if no_hex:
        for path, d in walk_dicts(data):
            if "hex" in d and isinstance(d["hex"], str):
                rep.warn("RAW_HEX", f"color uses hex {d['hex']} — policy is var() tokens only", path)
        for path, s in walk_strings(data):
            if path.endswith("_cssCustom") and HEX_IN_CSS_RE.search(s):
                rep.warn("RAW_HEX", "hex value inside _cssCustom — policy is var() tokens only", path)

    # --- global class policy ---
    if no_global_classes:
        if global_classes_of(data):
            rep.warn("GLOBAL_CLASS_POLICY", "policy is _cssClasses-only but the global class list is non-empty", "globalClasses")
        for nid, n in by_id.items():
            if (n.get("settings") or {}).get("_cssGlobalClasses"):
                rep.warn("GLOBAL_CLASS_POLICY", "policy is _cssClasses-only but element uses `_cssGlobalClasses`", nid)

    # --- collisions with the live site ---
    for nid in by_id:
        if nid in existing_ids:
            rep.error("ID_COLLISION", f"element id {nid} already exists in the site export", nid)
    for i, gc in enumerate(global_classes_of(data)):
        if not isinstance(gc, dict):
            continue
        gid, gname = gc.get("id"), gc.get("name")
        if gid in existing_class_ids:
            rep.error("CLASS_ID_COLLISION", f"global class id {gid} already exists on the site (Bricks will skip it silently)", f"globalClasses[{i}]")
        elif gname and gname in existing_class_names:
            rep.warn("CLASS_NAME_COLLISION", f"a global class named `{gname}` already exists with a different id", f"globalClasses[{i}]")

    # --- ACF field names ---
    if acf_names is not None:
        seen: set[str] = set()
        for path, s in walk_strings(data):
            for m in ACF_TAG_RE.finditer(s):
                name = m.group(1)
                if name in seen:
                    continue
                seen.add(name)
                if name not in acf_names:
                    rep.error("ACF_UNKNOWN_FIELD", f"{{acf_{name}}} is not a field in the ACF export", path)


# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate Bricks Builder clipboard JSON.")
    ap.add_argument("file", help="clipboard JSON to validate")
    ap.add_argument("--existing", action="append", default=[], metavar="EXPORT",
                    help="site or template export used as ground truth for ids and global classes (repeatable)")
    ap.add_argument("--acf", metavar="ACF_EXPORT", help="ACF field-group export; every {acf_*} tag must resolve to a field in it")
    ap.add_argument("--breakpoints", default=",".join(sorted(DEFAULT_BREAKPOINTS)),
                    help="comma-separated custom breakpoint keys")
    ap.add_argument("--pseudos", default=",".join(sorted(DEFAULT_PSEUDOS)),
                    help="comma-separated allowed pseudo states")
    ap.add_argument("--no-hex", action="store_true", help="flag raw hex colors (token-only policy)")
    ap.add_argument("--no-global-classes", action="store_true",
                    help="flag any globalClasses or _cssGlobalClasses (cssClasses-only policy)")
    ap.add_argument("--strict", action="store_true", help="promote warnings to errors")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    args = ap.parse_args(argv)

    rep = Report(strict=args.strict)
    data = load_json(args.file)

    breakpoints = {b.strip() for b in args.breakpoints.split(",") if b.strip()}
    pseudos = {p.strip() for p in args.pseudos.split(",") if p.strip()}

    nodes = check_envelope(data, rep)
    # popup / section templates legitimately root on a block or container
    root_section = not (is_template_export(data) and data.get("type") in ("popup", "section"))
    by_id = check_tree(nodes, rep, root_must_be_section=root_section) if isinstance(data, dict) else {}
    if isinstance(data, dict):
        check_settings(by_id, data, rep, breakpoints, pseudos)

        existing_ids, existing_class_ids, existing_class_names = collect_existing(args.existing)
        acf_names = collect_acf_field_names(load_json(args.acf)) if args.acf else None

        check_conventions(
            data, by_id, rep,
            no_hex=args.no_hex, no_global_classes=args.no_global_classes,
            existing_ids=existing_ids, existing_class_ids=existing_class_ids,
            existing_class_names=existing_class_names, acf_names=acf_names,
        )

    if args.json:
        print(json.dumps({"ok": rep.ok, "errors": rep.errors, "warnings": rep.warnings}, indent=2))
    else:
        print(rep.render())
    return 0 if rep.ok else 1


if __name__ == "__main__":
    sys.exit(main())
