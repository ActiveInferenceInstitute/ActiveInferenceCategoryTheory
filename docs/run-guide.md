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
| `measure` | `./run.sh measure` | Refreshes [`arm-runtimes.md`](arm-runtimes.md); `--check` verifies it was not hand-edited. | As above |

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

Row-by-row wall times live in [`arm-runtimes.md`](arm-runtimes.md), which
[`../.github/scripts/measure_arms.py`](../.github/scripts/measure_arms.py)
generates and no one edits by hand. Run `./run.sh measure` after changing an arm;
run `./run.sh measure --check` to confirm the committed file still matches the
generator.

One-time comparison, 2026-11-12, macOS arm64, Python 3.12.16, warm pip cache.
The two-job layout provisioned each job separately: 2.24 s for the
documentation job (`uv venv --seed` 0.39 s, `pyyaml==6.0.2` 1.85 s) and 8.12 s
for the conformance job (`uv venv --seed` 0.03 s, `defusedxml psutil pyyaml`
2.50 s, pinned parser 5.59 s), or 10.36 s across two checkouts and two
interpreters; three repeats landed at 9.33 s, 9.99 s and 10.93 s. The single job
builds one virtual environment and installs one dependency set; the same three
repeats landed at 6.78 s, 7.44 s and 7.71 s, so provisioning fell by roughly
three seconds per run.

The install was also the only place the two jobs disagreed about a version: the
conformance job resolved `pyyaml` to 6.0.3 while the documentation job pinned
6.0.2. One requirements file now serves both arms.

Check time did not move. `docs` measured 0.11 s before and `gnn` 0.30 s; after
the change the same arms measured 0.12 s – 0.59 s and 0.28 s – 0.72 s across
repeated runs, with noise larger than any difference, and running the old
`links,metadata` selection and the new three-check selection in the same
environment differed by less than the noise between runs. The new index check
adds no measurable cost.

## Related

- [`validation.md`](validation.md) — what each offline check does and how to
  reproduce a failure.
- [`gnn-materials.md`](gnn-materials.md) — the pinned revision and the model.
- [`../.github/README.md`](../.github/README.md) — the automation folder guide.
