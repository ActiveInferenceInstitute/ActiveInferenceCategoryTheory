# Documentation gate

This repository has no runtime, so its only executable checks are the arms of
[`../run.sh`](../run.sh). CI runs three of them on every pull request and on
pushes to `main`; they are also the repository's declared `docs`, `tests`, and
`gnn` tasks (see [`../AGENTS.md`](../AGENTS.md)). [`run-guide.md`](run-guide.md)
is the authoritative list of every arm.

## Where it runs

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) defines one job,
`gate`, displayed as `docs gate`, with three check steps:

| Step | Arm | What it does | Needs network |
| --- | --- | --- | --- |
| `links and metadata` | `./run.sh docs` | [`check_docs.py`](../.github/scripts/check_docs.py): links, YAML and CFF metadata, documentation-index coverage. | No |
| `gate unit tests (hermetic)` | `./run.sh tests` | [`tests/test_check_gnn.py`](../.github/scripts/tests/test_check_gnn.py): asserts `True` passes and `2` or `False` fails, with the parser stubbed. | No |
| `gnn conformance (pinned)` | `./run.sh gnn` | [`check_gnn.py`](../.github/scripts/check_gnn.py): parses and type-checks the model against the pinned parser. | Yes, to install |

The steps share one checkout, one interpreter, and one environment: the job
creates it with `uv venv --seed` and provisions it with `./run.sh setup`, which
installs [`../.github/requirements-gate.txt`](../.github/requirements-gate.txt)
and the parser pinned in [`../.github/gnn-pin.json`](../.github/gnn-pin.json).
The interpreter comes from the composite action
`ActiveInferenceInstitute/.github/.github/actions/setup-python-uv@7159e67315330aac8e414aebae0ad1e999a41448`,
used with `python-version: "3.12"` and `enable-cache: "false"`.

See [`gnn-materials.md`](gnn-materials.md) for the conformance step.

## What `check_docs.py` checks

It fails, with exit code 1, on any of four conditions:

1. A relative Markdown link or image target does not resolve to a path inside the
   repository that exists at the checked-out commit. Links may not escape the
   repository; fragments (`#...`) and absolute URLs are ignored.
2. A tracked YAML file (including [`CITATION.cff`](../CITATION.cff)) does not
   parse as YAML.
3. `CITATION.cff` lacks any of the required Citation File Format keys
   `cff-version`, `title`, or `license`.
4. A tracked Markdown document is absent from
   [`documentation-index.md`](documentation-index.md). The index file itself is
   exempt.

The checks are separately runnable with `./run.sh links`, `./run.sh metadata`, and
`./run.sh index`; `./run.sh docs` runs all three in one process. External URLs
are not fetched: the verdict must not depend on third-party availability.

## Run it locally

The gate's only dependency is PyYAML, and it needs no network:

```bash
python3 -m pip install pyyaml==6.0.2
./run.sh docs
```

A passing run prints `checked N tracked files: links, metadata, index ok`.

If PyYAML is missing, the `metadata` check exits with code 2 and prints the install
line above instead of reporting a YAML error, so a missing dependency is never
mistaken for invalid metadata.

The gate's own unit tests need only the standard library:

```bash
./run.sh tests
```

They stub the `gnn` parser, so they run without the environment that
`./run.sh setup` provisions and without network access.

## Failure proof

The gate is known to be able to fail. CI run 41720066280, in the job then named
`links and metadata`, logs `README.md: missing link target: does-not-exist.md`
followed by `##[error]Process completed with exit code 1`. That job was merged
into `gate`; the step keeps the name `links and metadata`. The root
[`README.md`](../README.md#documentation-gate) records the same reproduction.
