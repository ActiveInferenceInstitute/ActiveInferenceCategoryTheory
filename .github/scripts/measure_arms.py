#!/usr/bin/env python3
"""Measure every gate arm once and refresh ``docs/arm-runtimes.md``.

``docs/arm-runtimes.md`` is the repository's single home for measured numbers.
The file carries two JSON receipts — the current run and the one-time two-job
baseline — and this script renders all prose and tables from them.

``./run.sh measure`` runs the arms, replaces the current receipt, and rewrites
the document. ``./run.sh measure --check`` runs nothing: it reads the receipts,
validates them, re-renders, and compares byte for byte. Verifying the document
therefore never provisions an environment, installs a package, or touches the
network.

An arm that fails aborts the run without writing anything. An arm that reports
"not installed" (exit code 2, the conformance check's contract) is recorded as
unavailable instead of guessed at.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "arm-runtimes.md"
SCRIPTS = ROOT / ".github" / "scripts"

# Only the check arms are timed. `setup` is provisioning: its wall time is
# dominated by cache and network state, so a single run would report noise as a
# measurement. The baseline receipt records provisioning once, with conditions.
ARMS: dict[str, tuple[list[str], str]] = {
    "docs": ([sys.executable, str(SCRIPTS / "check_docs.py")], "./run.sh docs"),
    "gnn": ([sys.executable, str(SCRIPTS / "check_gnn.py")], "./run.sh gnn"),
}
ALL_COMMAND = "./run.sh all"
RECEIPT_ORDER = [*ARMS, "all"]

# One-time measurement of the two-job layout this repository used before the
# gate was consolidated. That layout no longer exists, so these numbers cannot be
# re-measured; they are recorded here and rendered from here, never retyped into
# prose. Measured 2026-11-12, macOS arm64, Python 3.12.16, warm pip cache.
BASELINE = {
    "measured": "2026-11-12",
    "host": "darwin arm64",
    "python": "3.12.16",
    "conditions": "warm pip cache; one run per arm per layout",
    "rows": [
        {
            "label": "`docs` — links and metadata (plus index coverage after)",
            "before": "0.11 s",
            "after": "0.12 s – 0.59 s",
        },
        {
            "label": "`gnn` — parse and type-check",
            "before": "0.30 s",
            "after": "0.28 s – 0.72 s",
        },
        {
            "label": "provisioning",
            "before": "10.36 s (2.24 s + 8.12 s); repeats 9.33 s, 9.99 s, 10.93 s",
            "after": "6.78 s – 7.71 s; one virtual environment and one install",
        },
    ],
    "note": [
        "The two jobs each created their own virtual environment and installed "
        "their own dependencies: the documentation job 2.24 s "
        "(`uv venv --seed` 0.39 s, `pyyaml==6.0.2` 1.85 s) and the conformance "
        "job 8.12 s (`uv venv --seed` 0.03 s, `defusedxml psutil pyyaml` 2.50 s, "
        "pinned parser 5.59 s), across two checkouts and two interpreters.",
        "They also disagreed about a version: the conformance job resolved PyYAML "
        "to a later patch release than the documentation job pinned.",
        "Check time did not move: repeated runs vary by more than any difference, "
        "and the index check added after the change cost less than run-to-run "
        "noise.",
    ],
}

STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def measure(command: list[str]) -> tuple[float, int]:
    started = time.perf_counter()
    result = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
    elapsed = time.perf_counter() - started
    if result.returncode not in (0, 2):
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"arm failed with exit code {result.returncode}: {' '.join(command)}")
    return round(elapsed, 2), result.returncode


def run_arms() -> dict:
    """Run every arm once and return the receipt that records the result."""
    rows = []
    for name, (command, display) in ARMS.items():
        seconds, code = measure(command)
        if code == 2:
            rows.append(
                {
                    "arm": name,
                    "command": display,
                    "seconds": None,
                    "status": "not installed; run `./run.sh setup`",
                }
            )
        else:
            rows.append({"arm": name, "command": display, "seconds": seconds, "status": "ok"})

    if all(row["seconds"] is not None for row in rows):
        seconds, _ = measure([str(ROOT / "run.sh"), "all"])
        rows.append({"arm": "all", "command": ALL_COMMAND, "seconds": seconds, "status": "ok"})
    else:
        rows.append(
            {
                "arm": "all",
                "command": ALL_COMMAND,
                "seconds": None,
                "status": "not measured; an arm is unavailable",
            }
        )

    return {
        "measured": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": f"{platform.system().lower()} {platform.machine()}",
        "python": platform.python_version(),
        "arms": rows,
    }


def validate_receipt(receipt: dict) -> list[str]:
    errors: list[str] = []
    if not STAMP.match(str(receipt.get("measured", ""))):
        errors.append("receipt: `measured` must be a UTC timestamp")
    for key in ("host", "python"):
        if not isinstance(receipt.get(key), str) or not receipt[key]:
            errors.append(f"receipt: `{key}` must be a non-empty string")
    arms = receipt.get("arms")
    if not isinstance(arms, list):
        return [*errors, "receipt: `arms` must be a list"]
    names = [row.get("arm") for row in arms if isinstance(row, dict)]
    if names != RECEIPT_ORDER:
        errors.append(f"receipt: arms must be {RECEIPT_ORDER} in that order, got {names}")
        return errors
    for row in arms:
        expected = ALL_COMMAND if row["arm"] == "all" else ARMS[row["arm"]][1]
        if row.get("command") != expected:
            errors.append(f"receipt: {row['arm']} command must be {expected!r}")
        seconds = row.get("seconds")
        if seconds is not None and not isinstance(seconds, (int, float)):
            errors.append(f"receipt: {row['arm']} seconds must be a number or null")
        if seconds is not None and seconds < 0:
            errors.append(f"receipt: {row['arm']} seconds must not be negative")
        status = row.get("status")
        if not isinstance(status, str) or not status:
            errors.append(f"receipt: {row['arm']} status must be a non-empty string")
        if seconds is None and status == "ok":
            errors.append(f"receipt: {row['arm']} has no time and no reason")
    return errors


def validate_baseline(baseline: dict) -> list[str]:
    errors: list[str] = []
    if not DATE.match(str(baseline.get("measured", ""))):
        errors.append("baseline: `measured` must be a date")
    rows = baseline.get("rows")
    if not isinstance(rows, list) or not rows:
        return [*errors, "baseline: `rows` must be a non-empty list"]
    for row in rows:
        if not isinstance(row, dict) or not all(
            isinstance(row.get(key), str) and row[key] for key in ("label", "before", "after")
        ):
            errors.append("baseline: every row needs non-empty label, before, and after")
    note = baseline.get("note")
    if not isinstance(note, list) or not note or not all(
        isinstance(part, str) and part for part in note
    ):
        errors.append("baseline: `note` must be a non-empty list of paragraphs")
    return errors


def block(name: str, payload: dict) -> list[str]:
    return [
        f"<!-- {name}:begin -->",
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
        f"<!-- {name}:end -->",
    ]


def render(receipt: dict, baseline: dict) -> str:
    lines = [
        "# Measured arm runtimes",
        "",
        "<!-- generated by .github/scripts/measure_arms.py via `./run.sh measure`; do not hand-edit. -->",
        "<!-- `./run.sh measure --check` re-renders this file from the two receipts below and",
        "     compares byte for byte. It runs no arm, installs nothing, and uses no network. -->",
        "",
        "This file is the repository's single home for measured numbers: prose elsewhere",
        "links here instead of copying a number. Both receipts are written by",
        "[`../.github/scripts/measure_arms.py`](../.github/scripts/measure_arms.py); the",
        "tables and prose below are rendered from them.",
        "",
        "## Current arms",
        "",
        *block("receipt", receipt),
        "",
        "| Arm | Command | Wall time (s) | Status |",
        "| --- | --- | --- | --- |",
    ]
    for row in receipt["arms"]:
        seconds = "—" if row["seconds"] is None else f"{row['seconds']:.2f}"
        lines.append(f"| `{row['arm']}` | `{row['command']}` | {seconds} | {row['status']} |")

    total = sum(
        row["seconds"] or 0.0 for row in receipt["arms"] if row["arm"] in ("docs", "gnn")
    )
    lines += [
        "",
        f"Measured {receipt['measured']} on {receipt['host']}, Python {receipt['python']}: "
        "one run of each arm, no warm-up.",
        "",
        f"The arms above sum to {total:.2f} s, and `./run.sh all` runs `docs` and `gnn`",
        "back to back. `setup` is provisioning, not a check, so it is not timed here.",
        "",
        "`setup` installs",
        "[`../.github/requirements-gate.txt`](../.github/requirements-gate.txt) and the",
        "GNN parser pinned in [`../.github/gnn-pin.json`](../.github/gnn-pin.json); the",
        "`docs` arm never depends on it.",
        "",
        "## Two jobs to one job",
        "",
        *block("baseline", baseline),
        "",
        f"Recorded {baseline['measured']} on {baseline['host']}, Python "
        f"{baseline['python']}, {baseline['conditions']}. The two-job layout no longer",
        "exists, so these numbers cannot be re-measured; the receipt above is the",
        "current record.",
        "",
        "| Comparison | Before (two jobs) | After (one job) |",
        "| --- | --- | --- |",
    ]
    for row in baseline["rows"]:
        lines.append(f"| {row['label']} | {row['before']} | {row['after']} |")
    lines += [""]
    for paragraph in baseline["note"]:
        lines += [paragraph, ""]
    lines += ["See [`run-guide.md`](run-guide.md) for what each arm checks.", ""]
    return "\n".join(lines)


def parse_block(text: str, name: str) -> tuple[dict | None, str | None]:
    begin, end = f"<!-- {name}:begin -->", f"<!-- {name}:end -->"
    if begin not in text or end not in text:
        return None, f"{DOC.relative_to(ROOT)}: missing the {name!r} receipt"
    payload = text.split(begin, 1)[1].split(end, 1)[0]
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return None, f"{DOC.relative_to(ROOT)}: the {name!r} receipt is not JSON: {exc}"
    if not isinstance(data, dict):
        return None, f"{DOC.relative_to(ROOT)}: the {name!r} receipt must be an object"
    return data, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the document against its receipts without running or provisioning anything",
    )
    args = parser.parse_args(argv)

    if not args.check:
        DOC.write_text(render(run_arms(), BASELINE), encoding="utf-8")
        print(f"wrote {DOC.relative_to(ROOT)}")
        return 0

    if not DOC.is_file():
        print(f"{DOC.relative_to(ROOT)}: missing; run ./run.sh measure", file=sys.stderr)
        return 1
    text = DOC.read_text(encoding="utf-8")
    receipt, error = parse_block(text, "receipt")
    baseline, baseline_error = parse_block(text, "baseline")
    errors = [item for item in (error, baseline_error) if item]
    if receipt is not None:
        errors.extend(validate_receipt(receipt))
    if baseline is not None:
        errors.extend(validate_baseline(baseline))
    if errors:
        print(f"{DOC.relative_to(ROOT)}: receipt is not usable:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    if render(receipt, baseline) != text:
        print(
            f"{DOC.relative_to(ROOT)}: prose or tables do not match the receipts; "
            "run ./run.sh measure",
            file=sys.stderr,
        )
        return 1
    print(f"{DOC.relative_to(ROOT)}: matches its receipts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
