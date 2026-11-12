#!/usr/bin/env python3
"""Provision the one environment every gate arm runs in.

Installs the pinned third-party requirements, then the GNN parser at the exact
revision named by ``.github/gnn-pin.json``. The documentation arm needs only the
requirements file; the conformance arm needs the parser as well, so a single
invocation covers both arms.

Network access is required. Nothing here runs during a documentation-only
change: ``./run.sh docs`` uses a Python that already has PyYAML.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / ".github" / "requirements-gate.txt"
PIN = ROOT / ".github" / "gnn-pin.json"


def load_pin(path: Path = PIN) -> dict[str, str]:
    """Read the pin record and refuse a malformed one before it is used."""
    pin = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pin, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    if pin.get("repository") != "ActiveInferenceInstitute/Generalized_Notation_Notation":
        raise SystemExit(f"{path}: unexpected GNN repository {pin.get('repository')!r}")
    tag = pin.get("tag")
    if not isinstance(tag, str) or not re.fullmatch(r"v?\d+\.\d+\.\d+", tag):
        raise SystemExit(f"{path}: GNN tag {tag!r} must match v?MAJOR.MINOR.PATCH")
    revision = pin.get("revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise SystemExit(f"{path}: GNN revision must be a 40-character lowercase SHA")
    return pin


def install(*args: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-q", *args],
        check=True,
    )


def main() -> int:
    install("-r", str(REQUIREMENTS))

    pin = load_pin()
    spec = (
        "generalized-notation-notation @ "
        f"git+https://github.com/{pin['repository']}.git@{pin['revision']}"
    )
    install("--no-deps", spec)
    print(
        json.dumps(
            {"gnn-pin-schema": pin["schema"], "revision": pin["revision"], "result": "installed"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
