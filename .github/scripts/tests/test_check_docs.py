"""Link admission against real temporary Git indexes and filesystem targets.

Only owned temporary repositories are initialized or staged. No commits, remote
operations, user Git configuration, or fsmonitor daemons are needed.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]


class TrackedLinkTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="category-links-test-")
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        self.root = self.base / "repo"
        self.root.mkdir()
        template = self.base / "empty-git-template"
        template.mkdir()
        # A caller's GIT_DIR/INDEX_FILE/config must never redirect fixture writes
        # into a real repository or start optional user-configured services.
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update({
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.fsmonitor",
            "GIT_CONFIG_VALUE_0": "false",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        })
        patch = mock.patch.dict(os.environ, environment, clear=True)
        patch.start()
        self.addCleanup(patch.stop)
        self.git("init", "--quiet", f"--template={template}")
        spec = importlib.util.spec_from_file_location("check_docs_link_test", SCRIPTS / "check_docs.py")
        assert spec is not None and spec.loader is not None
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        self.gate.ROOT = self.root
        self.source = self.write("README.md", "# Fixture\n")

    def git(self, *arguments):
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments], check=True,
            capture_output=True, text=True,
        )

    def write(self, relative, content="fixture", *, tracked=True):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if tracked:
            self.git("add", "--", str(relative))
        return path

    def symlink(self, relative, target, *, tracked=True, directory=False):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target, target_is_directory=directory)
        if tracked:
            self.git("add", "--", str(relative))
        return path

    def link(self, target):
        self.source.write_text(f"# Fixture\n\n[asset]({target})\n", encoding="utf-8")

    def errors(self):
        return self.gate.check_links(self.gate.tracked_files())

    def assert_link_error(self, reason):
        errors = self.errors()
        self.assertTrue(any("README.md" in error and reason in error for error in errors), errors)

    def test_existing_file_requires_membership_in_the_real_index(self):
        self.write("asset.bin", tracked=False)
        self.link("asset.bin")
        self.assert_link_error("untracked")
        self.git("add", "--", "asset.bin")
        self.assertEqual(self.errors(), [])

    def test_ignored_existing_file_is_not_a_portable_link_target(self):
        self.write(".gitignore", "ignored/\n")
        self.write("ignored/asset.bin", tracked=False)
        self.link("ignored/asset.bin")
        self.assert_link_error("untracked")

    def test_directory_requires_a_tracked_descendant(self):
        (self.root / "assets").mkdir()
        self.link("assets/")
        self.assert_link_error("untracked")
        self.write("assets/nested/asset.bin", tracked=False)
        self.assert_link_error("untracked")
        self.git("add", "--", "assets/nested/asset.bin")
        self.assertEqual(self.errors(), [])
        self.link(".")
        self.assertEqual(self.errors(), [])

    def test_missing_tracked_target_still_fails(self):
        target = self.write("asset.bin")
        self.link("asset.bin")
        target.unlink()
        self.assert_link_error("missing")

    def test_encoded_filenames_are_decoded_after_removing_fragments(self):
        self.write("assets/a b.bin")
        self.write("assets/part#one.bin")
        for target in ("assets/a%20b.bin", "assets/part%23one.bin#preview"):
            with self.subTest(target=target):
                self.link(target)
                self.assertEqual(self.errors(), [])

    def test_encoded_and_absolute_escapes_fail_for_inline_and_reference_links(self):
        outside = self.base / "outside.bin"
        outside.write_text("outside", encoding="utf-8")
        for target in ("%2e%2e/outside.bin", str(outside), "%2f" + str(outside).lstrip("/")):
            for reference in (False, True):
                with self.subTest(target=target, reference=reference):
                    if reference:
                        self.source.write_text(f"[asset][outside]\n\n[outside]: {target}\n", encoding="utf-8")
                    else:
                        self.link(target)
                    self.assert_link_error("escapes")

    def test_tracked_symlink_chain_to_tracked_file_is_accepted(self):
        self.write("asset.bin")
        self.symlink("second.bin", "asset.bin")
        self.symlink("first.bin", "second.bin")
        self.link("first.bin")
        self.assertEqual(self.errors(), [])

    def test_untracked_alias_and_intermediate_symlink_are_rejected(self):
        self.write("asset.bin")
        self.symlink("untracked.bin", "asset.bin", tracked=False)
        self.link("untracked.bin")
        self.assert_link_error("untracked")
        self.symlink("tracked.bin", "untracked.bin")
        self.link("tracked.bin")
        self.assert_link_error("untracked")

    def test_tracked_symlink_cannot_make_an_untracked_target_portable(self):
        self.write("untracked.bin", tracked=False)
        self.symlink("tracked.bin", "untracked.bin")
        self.link("tracked.bin")
        self.assert_link_error("untracked")

    def test_directory_alias_and_nested_file_alias_keep_their_tracked_identity(self):
        self.write("asset.bin")
        self.symlink("assets/inner.bin", "../asset.bin")
        self.symlink("alias", "assets", directory=True)
        for target in ("alias/", "alias/inner.bin"):
            with self.subTest(target=target):
                self.link(target)
                self.assertEqual(self.errors(), [])
        self.symlink("untracked-alias", "assets", tracked=False, directory=True)
        self.link("untracked-alias/inner.bin")
        self.assert_link_error("untracked")

    def test_outside_file_and_directory_symlinks_fail(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "asset.bin").write_text("outside", encoding="utf-8")
        self.symlink("escape.bin", "../outside/asset.bin")
        self.symlink("escape-dir", "../outside", directory=True)
        for target in ("escape.bin", "escape-dir/asset.bin"):
            with self.subTest(target=target):
                self.link(target)
                self.assert_link_error("escapes")

    def test_symlink_escape_then_reentry_is_not_a_portable_target(self):
        (self.base / "outside").mkdir()
        self.write("asset.bin")
        self.symlink("bridge", "../outside", directory=True)
        self.link("bridge/../repo/asset.bin")
        self.assert_link_error("escapes")

    def test_dangling_and_looping_symlinks_fail(self):
        self.symlink("dangling.bin", "missing.bin")
        self.symlink("loop-a.bin", "loop-b.bin")
        self.symlink("loop-b.bin", "loop-a.bin")
        self.link("dangling.bin")
        self.assert_link_error("missing")
        self.link("loop-a.bin")
        self.assert_link_error("resolve")

    def test_outside_markdown_source_is_rejected_before_reading_its_content(self):
        outside = self.base / "outside.md"
        outside.write_text("[secret](private-target)\n", encoding="utf-8")
        self.symlink("outside-source.md", "../outside.md")
        original_read = Path.read_text

        def read_inside_only(path, *args, **kwargs):
            if not path.resolve().is_relative_to(self.root):
                raise AssertionError("read outside Markdown content")
            return original_read(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read_inside_only):
            errors = self.errors()
        self.assertTrue(any("outside-source.md" in error and "escapes" in error for error in errors), errors)

    def test_untracked_alias_cannot_satisfy_index_coverage(self):
        self.symlink("alias.md", "README.md", tracked=False)
        self.write(self.gate.INDEX_DOC, "[root](../alias.md)\n")
        files = self.gate.tracked_files()
        errors = self.gate.check_index(files)
        self.assertTrue(any("README.md" in error for error in errors), errors)
        self.git("add", "--", "alias.md")
        self.assertEqual(self.gate.check_index(self.gate.tracked_files()), [])

    def test_links_and_index_entrypoint_uses_the_live_index(self):
        self.write(self.gate.INDEX_DOC, "[root](../README.md)\n")
        self.write("asset.bin", tracked=False)
        self.link("asset.bin")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.gate.main(["--only", "links,index"]), 1)
            self.git("add", "--", "asset.bin")
            self.assertEqual(self.gate.main(["--only", "links,index"]), 0)


if __name__ == "__main__":
    unittest.main()
