#!/usr/bin/env python3
"""Hermetic regression tests for the conformance gate's outcome contract.

``GNNTypeChecker.validate_gnn_files`` returns ``True`` when every file
validates, ``2`` when files are invalid or none were found, and ``False`` on a
hard failure. Only ``True`` may pass: a truthiness test would accept ``2``.

Each test drives ``.github/scripts/check_gnn.py`` through its own ``main`` with
the three ``gnn`` modules stubbed, so the suite needs neither the pinned parser
nor network access. ``./run.sh tests`` runs it before provisioning.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parents[1]
PIN = ROOT / ".github" / "gnn-pin.json"
STUBBED = ("gnn", "gnn.parsers", "gnn.parsers.basic", "gnn.type_checker")


def load_gate() -> types.ModuleType:
    """Import the gate script as a module without running ``main``."""
    spec = importlib.util.spec_from_file_location(
        "check_gnn_under_test", SCRIPTS / "check_gnn.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
        spec.loader.exec_module(module)
    return module


def stub_parser(outcome: object, calls: list[dict]) -> dict[str, types.ModuleType]:
    """Build the ``gnn`` modules ``check_gnn.main`` imports, reporting ``outcome``."""
    version = json.loads(PIN.read_text(encoding="utf-8"))["tag"].removeprefix("v")

    class Parsed:
        parse_errors: list[str] = []

    class TypeChecker:
        def validate_gnn_files(self, target_dir, output_dir, **kwargs):
            calls.append(dict(kwargs))
            return outcome

    basic = types.ModuleType("gnn.parsers.basic")
    basic.parse_gnn_formal = lambda path: Parsed()
    basic.validate_gnn_syntax = lambda content, **kwargs: (True, [])

    parsers = types.ModuleType("gnn.parsers")
    parsers.basic = basic

    type_checker = types.ModuleType("gnn.type_checker")
    type_checker.GNNTypeChecker = TypeChecker

    gnn = types.ModuleType("gnn")
    gnn.__version__ = version
    gnn.parsers = parsers
    gnn.type_checker = type_checker

    return {
        "gnn": gnn,
        "gnn.parsers": parsers,
        "gnn.parsers.basic": basic,
        "gnn.type_checker": type_checker,
    }


class GateOutcomeTest(unittest.TestCase):
    """One case per outcome the type checker is documented to return."""

    def setUp(self) -> None:
        self.gate = load_gate()
        self.saved = {name: sys.modules.get(name) for name in STUBBED}
        self.calls: list[dict] = []

    def tearDown(self) -> None:
        for name in STUBBED:
            module = self.saved[name]
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    def run_gate(self, outcome: object) -> tuple[int, str, str]:
        sys.modules.update(stub_parser(outcome, self.calls))
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.gate.main()
        return code, stdout.getvalue(), stderr.getvalue()

    def test_true_outcome_passes_and_reports_verified(self) -> None:
        code, out, err = self.run_gate(True)
        self.assertEqual(code, 0, err)
        payload = json.loads(out)
        self.assertEqual(payload["result"], "verified")
        self.assertIs(payload["type-checker-result"], True)
        self.assertEqual(self.calls, [{"strict": True}], "the checker must run in strict mode")

    def test_two_outcome_fails_the_arm(self) -> None:
        code, out, err = self.run_gate(2)
        self.assertEqual(out, "", "a rejected model must not print a verified receipt")
        self.assertEqual(code, 1, err)
        self.assertIn("returned 2", err)
        self.assertIn("only True passes", err)

    def test_false_outcome_fails_the_arm(self) -> None:
        code, out, err = self.run_gate(False)
        self.assertEqual(out, "", "a rejected model must not print a verified receipt")
        self.assertEqual(code, 1, err)
        self.assertIn("returned False", err)


if __name__ == "__main__":
    unittest.main()
