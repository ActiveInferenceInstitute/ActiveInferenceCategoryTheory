"""Measurement contracts using real, owned subprocess fixtures, not GNN runs."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parents[1]
FIXTURE_HELPER = '''import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(name):
    config = json.loads((HERE / "fixture-config.json").read_text(encoding="utf-8"))
    log = HERE / "fixture-events.jsonl"
    events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
    invocation = sum(event["arm"] == name for event in events)
    with log.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "arm": name, "executable": sys.executable, "prefix": sys.prefix,
            "python_env": os.environ.get("PYTHON"),
        }) + "\\n")
    codes = config.get(name, [0])
    return codes[min(invocation, len(codes) - 1)]
'''


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="category-measure-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.scripts = self.root / ".github" / "scripts"
        (self.scripts / "tests").mkdir(parents=True)
        (self.root / "docs").mkdir()
        shutil.copy2(ROOT / "run.sh", self.root / "run.sh")
        shutil.copyfile(SCRIPTS / "measure_arms.py", self.scripts / "measure_arms.py")
        shutil.copyfile(ROOT / "docs" / "arm-runtimes.md", self.root / "docs" / "arm-runtimes.md")
        (self.scripts / "_category_arm_fixture.py").write_text(FIXTURE_HELPER, encoding="utf-8")
        for name in ("docs", "gnn"):
            (self.scripts / f"check_{name}.py").write_text(
                f"from _category_arm_fixture import run\nraise SystemExit(run({name!r}))\n",
                encoding="utf-8",
            )
        (self.scripts / "tests" / "test_owned_arm.py").write_text(
            "import unittest\nfrom _category_arm_fixture import run\n"
            "class OwnedArm(unittest.TestCase):\n"
            "    def test_fixture_arm(self):\n        self.assertEqual(run('tests'), 0)\n",
            encoding="utf-8",
        )
        self.worker = self.scripts / "fixture_worker.py"
        self.worker.write_text(
            "import sys\nfrom _category_arm_fixture import run\nraise SystemExit(run(sys.argv[1]))\n",
            encoding="utf-8",
        )
        self.config = self.scripts / "fixture-config.json"
        self.log = self.scripts / "fixture-events.jsonl"
        self.config.write_text("{}", encoding="utf-8")
        environment = mock.patch.dict(os.environ, {
            "PYTHON": sys.executable,
            "PYTHONPATH": str(self.scripts),
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        environment.start()
        self.addCleanup(environment.stop)
        spec = importlib.util.spec_from_file_location(
            "measure_owned_fixture", self.scripts / "measure_arms.py",
        )
        assert spec is not None and spec.loader is not None
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        self.original_document = self.gate.DOC.read_bytes()

    def events(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def configure(self, **codes):
        self.config.write_text(json.dumps(codes), encoding="utf-8")

    def main(self, *arguments):
        with mock.patch.object(sys, "argv", ["measure_arms.py", *arguments]), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.gate.main()

    def published_receipt(self):
        text = self.gate.DOC.read_text(encoding="utf-8")
        receipt, error = self.gate.parse_block(text, "receipt")
        self.assertIsNone(error)
        baseline, error = self.gate.parse_block(text, "baseline")
        self.assertIsNone(error)
        self.assertEqual(baseline, self.gate.BASELINE)
        return receipt

    def test_real_all_uses_captured_interpreter_despite_conflicting_environment(self):
        decoys = self.root / "decoy-bin"
        decoys.mkdir()
        marker = self.root / "wrong-interpreter-used"
        for name in ("python", "python3"):
            executable = decoys / name
            executable.write_text(
                '#!/bin/sh\nprintf "wrong interpreter\\n" > "$DECOY_MARKER"\nexit 91\n',
                encoding="utf-8",
            )
            executable.chmod(0o755)
        with mock.patch.dict(os.environ, {
            "PYTHON": str(decoys / "python3"),
            "PATH": str(decoys) + os.pathsep + os.environ.get("PATH", os.defpath),
            "DECOY_MARKER": str(marker),
        }):
            self.assertEqual(self.main(), 0)
        receipt = self.published_receipt()
        self.assertEqual([row["arm"] for row in receipt["arms"]], ["docs", "tests", "gnn", "all"])
        for row in receipt["arms"]:
            self.assertEqual(row["status"], "ok")
            self.assertIsNotNone(row["seconds"])
        events = self.events()
        self.assertEqual([event["arm"] for event in events], ["docs", "tests", "gnn"] * 2)
        for event in events:
            self.assertEqual(event["executable"], sys.executable)
            self.assertEqual(event["prefix"], sys.prefix)
            self.assertEqual(event["python_env"], self.gate.PYTHON)
        self.assertFalse(marker.exists())

    def test_individual_unavailability_skips_aggregate_for_every_arm(self):
        for unavailable in ("docs", "tests", "gnn"):
            with self.subTest(arm=unavailable):
                self.log.unlink(missing_ok=True)
                self.configure(**{unavailable: [2]})
                display = self.gate.ARMS[unavailable][1]
                # Unittest normally returns 1 on test failure. Use a real exit-2
                # fixture process to exercise the measurement contract for it too.
                with mock.patch.dict(self.gate.ARMS, {
                    unavailable: ([self.gate.PYTHON, str(self.worker), unavailable], display),
                }):
                    receipt = self.gate.run_arms()
                rows = {row["arm"]: row for row in receipt["arms"]}
                for name in (unavailable, "all"):
                    self.assertIsNone(rows[name]["seconds"])
                    self.assertNotEqual(rows[name]["status"], "ok")
                self.assertEqual([event["arm"] for event in self.events()], ["docs", "tests", "gnn"])
                self.assertEqual(self.gate.DOC.read_bytes(), self.original_document)

    def test_aggregate_unavailability_is_published_as_unavailable_not_ok(self):
        for unavailable in ("docs", "gnn"):
            with self.subTest(arm=unavailable):
                self.log.unlink(missing_ok=True)
                self.configure(**{unavailable: [0, 2]})
                self.assertEqual(self.main(), 0)
                receipt = self.published_receipt()
                for row in receipt["arms"][:-1]:
                    self.assertEqual(row["status"], "ok")
                    self.assertIsNotNone(row["seconds"])
                aggregate = receipt["arms"][-1]
                self.assertEqual(aggregate["arm"], "all")
                self.assertIsNone(aggregate["seconds"])
                self.assertNotEqual(aggregate["status"], "ok")
                expected = ["docs", "tests", "gnn"] + (
                    ["docs"] if unavailable == "docs" else ["docs", "tests", "gnn"]
                )
                self.assertEqual([event["arm"] for event in self.events()], expected)

    def test_aggregate_failure_aborts_without_overwriting_existing_receipts(self):
        self.configure(gnn=[0, 7])
        with self.assertRaises(SystemExit) as caught:
            self.main()
        self.assertNotIn(caught.exception.code, (None, 0))
        self.assertEqual(self.gate.DOC.read_bytes(), self.original_document)
        self.assertEqual([event["arm"] for event in self.events()], ["docs", "tests", "gnn"] * 2)

    def test_individual_failure_aborts_without_running_later_arms_or_publishing(self):
        self.configure(docs=[7])
        with self.assertRaises(SystemExit) as caught:
            self.main()
        self.assertNotIn(caught.exception.code, (None, 0))
        self.assertEqual(self.gate.DOC.read_bytes(), self.original_document)
        self.assertEqual([event["arm"] for event in self.events()], ["docs"])

    def test_historical_document_check_neither_executes_arms_nor_rewrites_receipts(self):
        with mock.patch.object(
            self.gate.subprocess, "run", side_effect=AssertionError("--check executed an arm"),
        ):
            self.assertEqual(self.main("--check"), 0)
        self.assertEqual(self.gate.DOC.read_bytes(), self.original_document)
        self.assertEqual(self.events(), [])


if __name__ == "__main__":
    unittest.main()
