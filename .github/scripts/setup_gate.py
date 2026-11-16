#!/usr/bin/env python3
"""Provision the one environment every gate arm runs in.

Validates ``.github/gnn-pin.json``, then installs the pinned third-party
requirements, then the GNN parser at the exact revision that record names. The
documentation arm needs only the requirements file; the conformance arm needs
the parser as well, so a single invocation covers both arms.

Network access is required. Nothing here runs during a documentation-only
change: ``./run.sh docs`` uses a Python that already has PyYAML.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import gnn_pin_contract

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / ".github" / "requirements-gate.txt"
PIN = ROOT / ".github" / "gnn-pin.json"


def install(*args: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-q", *args],
        check=True,
    )


def main() -> int:
    pin = gnn_pin_contract.load_pin(PIN)
    install("-r", str(REQUIREMENTS))
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
