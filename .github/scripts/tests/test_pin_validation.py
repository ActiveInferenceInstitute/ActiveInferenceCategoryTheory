"""Exercise pin admission without installing or importing a scientific parser."""

from __future__ import annotations

import builtins
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
PIN = SCRIPTS.parents[1] / ".github" / "gnn-pin.json"


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(
        f"{name}_pin_test", SCRIPTS / f"{name}.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
        spec.loader.exec_module(module)
    return module


class PinAdmissionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="category-pin-test-")
        self.addCleanup(directory.cleanup)
        self.pin = Path(directory.name) / "gnn-pin.json"
        self.legacy = json.loads(PIN.read_text(encoding="utf-8"))
        self.setup = load_script("setup_gate")
        self.check = load_script("check_gnn")
        self.setup.PIN = self.pin
        self.check.PIN = self.pin

    def write_pin(self, value):
        self.pin.write_text(json.dumps(value), encoding="utf-8")

    def assert_rejected_before_effects(self):
        original_import = builtins.__import__
        parser_imports = []

        def guarded_import(name, *args, **kwargs):
            if name == "gnn" or name.startswith("gnn."):
                parser_imports.append(name)
                raise AssertionError("invalid pin reached the scientific parser")
            return original_import(name, *args, **kwargs)

        with mock.patch.object(
            self.setup, "install", side_effect=AssertionError("invalid pin reached pip"),
        ) as install, mock.patch("builtins.__import__", side_effect=guarded_import):
            for name, consumer in (("setup", self.setup), ("check", self.check)):
                with self.subTest(consumer=name):
                    with self.assertRaises(SystemExit) as caught:
                        consumer.main()
                    self.assertNotIn(caught.exception.code, (None, 0))
        install.assert_not_called()
        self.assertEqual(parser_imports, [])

    def test_current_legacy_record_is_accepted_without_migration(self):
        self.write_pin(self.legacy)
        self.assertEqual(self.setup.gnn_pin_contract.load_pin(self.pin), self.legacy)
        # The legacy contract deliberately accepts the optional 'v' prefix.
        unprefixed = {**self.legacy, "tag": self.legacy["tag"].removeprefix("v")}
        self.write_pin(unprefixed)
        self.assertEqual(self.check.gnn_pin_contract.load_pin(self.pin), unprefixed)

    def test_missing_required_fields_fail_before_effects(self):
        for field in ("schema", "repository", "tag", "revision"):
            with self.subTest(field=field):
                record = dict(self.legacy)
                del record[field]
                self.write_pin(record)
                self.assert_rejected_before_effects()

    def test_invalid_required_fields_fail_before_effects(self):
        invalid = {
            "schema": (None, False, 1, [], {}, "", "gnn-importer-pin/v2"),
            "repository": (
                None, False, 1, [], {}, "", "another-owner/Generalized_Notation_Notation",
                "https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation",
            ),
            "tag": (
                None, False, 1, [], {}, "", "latest", "v5.0", "v5.0.3-rc1",
                "v5.0.3\n", "v５.０.３",
            ),
            "revision": (
                None, False, 1, [], {}, "", "a" * 39, "a" * 41, "A" * 40,
                "g" * 40, "a" * 40 + "\n",
            ),
        }
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.write_pin({**self.legacy, field: value})
                    self.assert_rejected_before_effects()

    def test_non_object_records_fail_before_effects(self):
        for value in (None, True, 42, "pin", [], [self.legacy]):
            with self.subTest(value=value):
                self.write_pin(value)
                self.assert_rejected_before_effects()

    def test_unreadable_records_fail_before_effects(self):
        for value in (b"", b"{", b"\xff"):
            with self.subTest(value=value):
                self.pin.write_bytes(value)
                self.assert_rejected_before_effects()
        self.pin.unlink()
        self.assert_rejected_before_effects()
        self.pin.mkdir()
        self.assert_rejected_before_effects()


if __name__ == "__main__":
    unittest.main()
