#!/usr/bin/env python3
"""Parse and type-check the repository's GNN model against the pinned parser.

Exit codes carry meaning, and the measurement producer relies on them:

0  the pinned parser is installed, the model parses, and the type checker
   accepts it.
1  the check ran and failed (version drift, parse error, syntax error, or a
   type-checker rejection).
2  the pinned parser is not installed; run ``./run.sh setup`` first.

The model source is ``gnn/learner_perception_model.md``. That file is not named
``*.gnn.md``; ``.github/GNN.md`` records why.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / ".github" / "gnn-pin.json"
MODEL = ROOT / "gnn" / "learner_perception_model.md"


def main() -> int:
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

    pin = json.loads(PIN.read_text(encoding="utf-8"))
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
    valid, errors = validate_gnn_syntax(MODEL.read_text(encoding="utf-8"))
    if not valid:
        print(f"{MODEL.name} syntax errors: {errors!r}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="category-theory-gnn-") as output_dir:
        model_dir = Path(output_dir) / "models"
        model_dir.mkdir()
        shutil.copy(MODEL, model_dir / MODEL.name)
        if not GNNTypeChecker().validate_gnn_files(model_dir, Path(output_dir)):
            print("GNN type checker rejected the learner perception model", file=sys.stderr)
            return 1

    print(json.dumps({"gnn-version": __version__, "result": "verified"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
