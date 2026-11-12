# `.github/` — CI and repository automation

Workflows and the pinned metadata that back this repository's automated checks.
There is no application code here; the checks are thin Python scripts, and
[`../run.sh`](../run.sh) is their single entry point.

| Path | Purpose |
| --- | --- |
| [`workflows/docs.yml`](workflows/docs.yml) | The `docs` workflow: one job, `gate` (displayed as `docs gate`), running the offline `links and metadata` step and the network-dependent `gnn conformance (pinned)` step. |
| [`scripts/check_docs.py`](scripts/check_docs.py) | Validates relative Markdown links, tracked YAML, `CITATION.cff` keys, and documentation-index coverage. |
| [`scripts/check_gnn.py`](scripts/check_gnn.py) | Parses and type-checks `gnn/learner_perception_model.md` against the pinned parser. |
| [`scripts/setup_gate.py`](scripts/setup_gate.py) | Installs `requirements-gate.txt` and the parser pinned in `gnn-pin.json`. |
| [`scripts/measure_arms.py`](scripts/measure_arms.py) | Measures each arm and writes the receipts and rendered tables in [`../docs/arm-runtimes.md`](../docs/arm-runtimes.md); `--check` validates the receipts and re-renders without running an arm. |
| [`requirements-gate.txt`](requirements-gate.txt) | The one dependency set both arms share. |
| [`gnn-pin.json`](gnn-pin.json) | The pinned Generalized Notation Notation revision, schema `gnn-importer-pin/v1`: tag `v5.0.3`, commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`, recorded `2026-11-12`. |
| [`dependabot.yml`](dependabot.yml) | Dependabot configuration for GitHub Actions updates. |
| [`GNN.md`](GNN.md) | Pointer to the pinned GNN conformance check: the model source it validates and why that file is not named `*.gnn.md`. |

## Running the gates locally

```bash
./run.sh docs    # links, YAML/CFF metadata, index coverage — offline
./run.sh setup   # one environment for both arms; needs network
./run.sh gnn     # parse + type-check against the pinned parser
```

[`../docs/run-guide.md`](../docs/run-guide.md) lists every arm,
[`../docs/validation.md`](../docs/validation.md) explains the offline checks, and
[`../docs/gnn-materials.md`](../docs/gnn-materials.md) explains the conformance
check.

## Editing rules

- Workflows pin actions by commit SHA; keep the pinned revisions and do not edit
  them as part of a documentation change. The interpreter comes from
  `ActiveInferenceInstitute/.github/.github/actions/setup-python-uv@7159e67315330aac8e414aebae0ad1e999a41448`.
- The workflow holds no copy of a command: it calls `./run.sh` arms, so a change
  to a check belongs in the script and never in the YAML.
- `gnn-pin.json` is a curated pin, not a lockfile; change it only when the GNN
  conformance target intentionally moves, and re-verify the model afterwards.
- Measured numbers live only in [`../docs/arm-runtimes.md`](../docs/arm-runtimes.md);
  regenerate them with `./run.sh measure` instead of typing them into prose.
