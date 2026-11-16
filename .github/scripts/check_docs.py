#!/usr/bin/env python3
"""Validate documentation links, metadata, and index coverage for this repository.

Three checks, selectable with ``--only`` and all of which can fail:

1. ``links`` — every relative Markdown link or image resolves inside the
   repository to a tracked file or a directory with tracked descendants.
2. ``metadata`` — every tracked YAML file (including CITATION.cff) parses as
   YAML, and CITATION.cff carries the required Citation File Format keys.
3. ``index`` — every tracked Markdown document is reachable from the flat
   index at ``docs/documentation-index.md``.

External URLs are not fetched: the gate is about the repository's own links,
and a network probe would make the verdict depend on third-party availability.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
CFF_REQUIRED = ("cff-version", "title", "license")
INDEX_DOC = Path("docs/documentation-index.md")
MARKDOWN_SUFFIXES = {".md", ".markdown"}
CHECKS = ("links", "metadata", "index")


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [ROOT / name for name in result.stdout.decode("utf-8").split("\0") if name]


def link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    parts = target.split()
    return parts[0] if parts else ""


def _relative_target(raw: str) -> str | None:
    target = link_target(raw)
    if not target or target.startswith("#") or SCHEME.match(target):
        return None
    # An encoded '#' belongs to a filename, not to the URI fragment.
    base = target.split("#", 1)[0]
    return unquote(base) if base else None


def _tracked_inventory(files: list[Path], root: Path) -> tuple[set[Path], set[Path]]:
    tracked = {root / path.relative_to(ROOT) for path in files}
    directories = {
        parent for path in tracked for parent in path.parents
        if parent.is_relative_to(root)
    }
    return tracked, directories


def _resolve_tracked_target(
    path: Path, root: Path, tracked: set[Path], directories: set[Path],
) -> Path:
    """Admit the resolved target and every symlink dependency in its path."""
    try:
        resolved = path.resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise ValueError("missing link target") from exc
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError("cannot resolve link target") from exc
    if not resolved.is_relative_to(root):
        raise ValueError("link escapes repository")
    for component in (path, *path.parents):
        if component == root:
            break
        if component.is_symlink():
            # Resolving only the final filename would admit untracked aliases.
            if component.parent.resolve(strict=True) / component.name not in tracked:
                raise ValueError("link depends on an untracked symlink")
            _resolve_tracked_target(
                component.parent / component.readlink(), root, tracked, directories,
            )
    if resolved.is_file() and resolved in tracked:
        return resolved
    if resolved.is_dir() and resolved in directories:
        return resolved
    raise ValueError("untracked link target")


def relative_targets(path: Path) -> list[str]:
    """Return the in-repository target of every relative link in one file."""
    text = path.read_text(encoding="utf-8")
    targets = INLINE_LINK.findall(text) + REFERENCE_LINK.findall(text)
    return [raw for raw in targets if _relative_target(raw) is not None]


def check_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    resolved_root = ROOT.resolve()
    tracked, directories = _tracked_inventory(files, resolved_root)
    for path in files:
        if path.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue
        source = resolved_root / path.relative_to(ROOT)
        try:
            _resolve_tracked_target(source, resolved_root, tracked, directories)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot inspect document: {exc}")
            continue
        for raw in relative_targets(source):
            base = _relative_target(raw)
            assert base is not None
            try:
                _resolve_tracked_target(
                    source.parent / base, resolved_root, tracked, directories,
                )
            except ValueError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc}: {raw}")
    return errors


def check_yaml(files: list[Path]) -> list[str]:
    import yaml

    errors: list[str] = []
    for path in files:
        is_yaml = path.suffix.lower() in {".yml", ".yaml"}
        is_cff = path.name == "CITATION.cff"
        if not (is_yaml or is_cff):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report the parser message
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
            continue
        if is_cff:
            for key in CFF_REQUIRED:
                if not isinstance(data, dict) or key not in data:
                    errors.append(f"{path.relative_to(ROOT)}: missing required CFF key: {key}")
    return errors


def check_index(files: list[Path]) -> list[str]:
    index = ROOT / INDEX_DOC
    if not index.is_file():
        return [f"{INDEX_DOC}: missing documentation index"]
    resolved_root = ROOT.resolve()
    tracked, directories = _tracked_inventory(files, resolved_root)
    index = resolved_root / INDEX_DOC
    try:
        resolved_index = _resolve_tracked_target(index, resolved_root, tracked, directories)
    except ValueError as exc:
        return [f"{INDEX_DOC}: cannot inspect documentation index: {exc}"]
    listed = set()
    for raw in relative_targets(index):
        try:
            base = _relative_target(raw)
            assert base is not None
            listed.add(_resolve_tracked_target(
                index.parent / base, resolved_root, tracked, directories,
            ))
        except ValueError:
            # Invalid links cannot satisfy coverage; the links arm reports them.
            continue
    errors: list[str] = []
    for path in files:
        if path.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue
        try:
            resolved = _resolve_tracked_target(
                resolved_root / path.relative_to(ROOT), resolved_root, tracked, directories,
            )
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot inspect document: {exc}")
            continue
        if resolved == resolved_index:
            continue
        if resolved not in listed:
            errors.append(
                f"{path.relative_to(ROOT)}: not listed in {INDEX_DOC}"
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--only",
        default=",".join(CHECKS),
        help=f"comma-separated subset of: {', '.join(CHECKS)} (default: all)",
    )
    args = parser.parse_args(argv)
    selected = [name.strip() for name in args.only.split(",") if name.strip()]
    unknown = [name for name in selected if name not in CHECKS]
    if unknown:
        parser.error(f"unknown check(s) {unknown}; choose from {list(CHECKS)}")

    files = tracked_files()
    runners = {"links": check_links, "metadata": check_yaml, "index": check_index}
    if "metadata" in selected:
        try:
            import yaml  # noqa: F401 - preflight for the documented dependency
        except ImportError:
            print(
                "the metadata check needs PyYAML: python3 -m pip install pyyaml==6.0.2",
                file=sys.stderr,
            )
            return 2
    errors: list[str] = []
    for name in selected:
        errors.extend(runners[name](files))

    if errors:
        print(f"{len(errors)} documentation check(s) failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"checked {len(files)} tracked files: "
        f"{', '.join(selected)} ok"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
