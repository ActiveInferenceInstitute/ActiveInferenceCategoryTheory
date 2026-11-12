# Run guide

[`../run.sh`](../run.sh) is the single entry point for every check in this
repository. Each arm it exposes is the exact command CI runs; the workflow in
[`../.github/workflows/docs.yml`](../.github/workflows/docs.yml) invokes
`./run.sh` and holds no second copy of a command.

There are no `lint`, `type`, or `test` arms. The repository ships documentation
and metadata, with one Python gate script as its entire executable surface, so a
separate linter or test suite would have nothing of its own to check.

## Arms

| Arm | Command | Checks | Network |
| --- | --- | --- | --- |
| `docs` | `./run.sh docs` | All three offline checks below, in one pass. | No |
| `links` | `./run.sh links` | Every relative Markdown link and image target resolves inside the repository. | No |
| `metadata` | `./run.sh metadata` | Every tracked YAML file and `CITATION.cff` parses; the required CFF keys exist. | No |
| `index` | `./run.sh index` | Every tracked Markdown document appears in [`documentation-index.md`](documentation-index.md). | No |
| `gnn` | `./run.sh gnn` | `gnn/learner_perception_model.md` parses and type-checks against the pinned parser. | Only to install |
| `setup` | `./run.sh setup` | Installs [`../.github/requirements-gate.txt`](../.github/requirements-gate.txt) and the parser pinned in [`../.github/gnn-pin.json`](../.github/gnn-pin.json). | Yes |
| `all` | `./run.sh all` | `docs`, then `gnn`. | As above |
| `measure` | `./run.sh measure` | Refreshes the current receipt in [`arm-runtimes.md`](arm-runtimes.md); `--check` validates the receipts and re-renders without running anything. | Refresh only |

The offline arms need one wheel, `pyyaml==6.0.2`, and nothing else. The
conformance arm exits with code 2 and a pointer to `./run.sh setup` when the
pinned parser is missing, so a missing environment is never mistaken for a failed
model.

`./run.sh` runs `python3` from `PATH`; set `PYTHON=/path/to/python` to override it.

## What CI runs

`.github/workflows/docs.yml` defines one job, `gate` (display name `docs gate`),
with one checkout, one `setup-python-uv` interpreter, one virtual environment,
and one install for both checks. Its steps are `./run.sh setup`, then
`./run.sh docs` under the step name `links and metadata`, then `./run.sh gnn`
under the step name `gnn conformance (pinned)`.

The conformance step keeps its historical step name, so log searches for
`gnn conformance (pinned)` still find it; the job that contains it is `gate`.
Earlier revisions of the workflow ran two jobs, `links-and-metadata` and
`gnn-conformance`, and each paid for its own checkout, interpreter, virtual
environment, and dependency install.

## Measurement

Every measured number — each arm's wall time and the one-time two-job baseline —
lives in [`arm-runtimes.md`](arm-runtimes.md). That file carries two JSON receipts
and is rendered from them by
[`../.github/scripts/measure_arms.py`](../.github/scripts/measure_arms.py); prose
here and elsewhere links to it instead of repeating a number.

`./run.sh measure` refreshes the current receipt by running the arms.
`./run.sh measure --check` runs nothing: it validates both receipts, re-renders
the document, and compares byte for byte, so verification needs no environment,
no install, and no network. The baseline receipt records the two-job layout this
repository used before the gate was consolidated; that layout no longer exists,
so its numbers cannot be re-measured.

## Related

- [`validation.md`](validation.md) — what each offline check does and how to
  reproduce a failure.
- [`gnn-materials.md`](gnn-materials.md) — the pinned revision and the model.
- [`../.github/README.md`](../.github/README.md) — the automation folder guide.
