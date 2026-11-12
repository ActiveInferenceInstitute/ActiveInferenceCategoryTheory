#!/usr/bin/env python3
"""Parse and type-check the repository's GNN model against the pinned parser.

Exit codes carry meaning, and the measurement producer relies on them:

0  the pinned parser is installed, the model parses, and the type checker
   accepts it.
1  the check ran and failed (version drift, parse error, syntax error, or a
   type-checker outcome other than ``True``, or a malformed pin record).
2  the pinned parser is not installed; run ``./run.sh setup`` first.

``GNNTypeChecker.validate_gnn_files`` returns ``True`` when every file validates,
``2`` when files are invalid or none were found, and ``False`` on a hard failure.
Only ``True`` passes: a bare truthiness test would accept ``2``.

The model source is ``gnn/learner_perception_model.md``. That file is not named
``*.gnn.md``; ``.github/GNN.md`` records why.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / ".github" / "gnn-pin.json"
MODEL = ROOT / "gnn" / "learner_perception_model.md"


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


def main() -> int:
    pin = load_pin()
    try:
        from gnn import __version__
        from gnn.parsers.basic import parse_gnn_formal, validate_gnn_syntax
        from gnn.type_checker import GNNTypeChecker
    except ImportError as exc:
        print(
            f"the pinned GNN parser is not installed ({exc}); run ./run.sh setup",
            file=sys.stderr,
        )
        return 2

    expected_version = pin["tag"].removeprefix("v")
    if __version__ != expected_version:
        print(
            f"installed GNN {__version__!r} does not match {pin['tag']!r}",
            file=sys.stderr,
        )
        return 1

    parsed = parse_gnn_formal(MODEL)
    if parsed is None or getattr(parsed, "parse_errors", None):
        print(f"{MODEL.name} did not parse cleanly", file=sys.stderr)
        return 1
    valid, errors = validate_gnn_syntax(MODEL.read_text(encoding="utf-8"), is_content=True)
    if not valid:
        print(f"{MODEL.name} syntax errors: {errors!r}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="category-theory-gnn-") as output_dir:
        model_dir = Path(output_dir) / "models"
        model_dir.mkdir()
        shutil.copy(MODEL, model_dir / MODEL.name)
        # Contract: True = every file valid; 2 = invalid files or no files found;
        # False = hard failure. strict=True makes type/consistency problems errors.
        outcome = GNNTypeChecker().validate_gnn_files(model_dir, Path(output_dir), strict=True)
        if outcome is not True:
            print(
                f"GNN type checker did not accept the learner perception model "
                f"(returned {outcome!r}; only True passes)",
                file=sys.stderr,
            )
            return 1

    print(
        json.dumps(
            {"gnn-version": __version__, "result": "verified", "type-checker-result": outcome},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
