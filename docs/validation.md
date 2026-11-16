# Documentation gate

The repository's executable checks are Python/Bash arms of
[`run.sh`](../run.sh), not an application runtime. CI runs `docs`, `tests`, and
`gnn` on pull requests and pushes to `main`; see
[`AGENTS.md`](../AGENTS.md) and the authoritative [run guide](run-guide.md).

## Where it runs

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) defines one job,
`gate`, displayed as `docs gate`, with three check steps:

| Step | Arm | What it does | Needs network |
| --- | --- | --- | --- |
| `links and metadata` | `./run.sh docs` | [`check_docs.py`](../.github/scripts/check_docs.py): links, YAML and CFF metadata, documentation-index coverage. | No |
| `gate unit tests (hermetic)` | `./run.sh tests` | Offline contracts for pin admission, tracked links, measurement outcomes, and literal GNN conformance results. | No |
| `gnn conformance (pinned)` | `./run.sh gnn` | [`check_gnn.py`](../.github/scripts/check_gnn.py): parses and type-checks the model against the already provisioned parser. | No |

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

1. A relative Markdown link or image target does not resolve inside the repository
   to a tracked file or a directory with tracked descendants. Symlink dependencies
   must also be admitted. Fragments and external URLs are not fetched.
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

## Tracked-target admission

Untracked aliases do not make untracked content portable. Missing, escaping,
dangling, or looping paths fail. URL fragments are removed before percent
decoding so encoded filename characters remain filename content. These are
offline source checks, not scientific or external-link qualification.
