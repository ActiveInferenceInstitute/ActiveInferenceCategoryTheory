"""Admission for this consumer's legacy GNN pin, before provisioning or imports.

This validates the local record, not an installed parser's source identity.
The intentional legacy contract uses ``revision``, not a migrated ``commit`` key.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SCHEMA = "gnn-importer-pin/v1"
REPOSITORY = "ActiveInferenceInstitute/Generalized_Notation_Notation"


def load_pin(path: Path) -> dict[str, Any]:
    """Return an admitted legacy record, or terminate before any external effect."""
    try:
        pin = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"{path}: cannot read GNN pin: {exc}") from exc
    if not isinstance(pin, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    if pin.get("schema") != SCHEMA:
        raise SystemExit(f"{path}: GNN pin schema must be {SCHEMA!r}")
    if pin.get("repository") != REPOSITORY:
        raise SystemExit(f"{path}: unexpected GNN repository {pin.get('repository')!r}")
    tag = pin.get("tag")
    if not isinstance(tag, str) or not re.fullmatch(r"v?[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise SystemExit(f"{path}: GNN tag {tag!r} must match v?MAJOR.MINOR.PATCH")
    revision = pin.get("revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise SystemExit(f"{path}: GNN revision must be a 40-character lowercase SHA")
    return pin
