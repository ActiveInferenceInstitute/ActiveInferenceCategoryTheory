# `.github/` — CI and repository automation

Workflows and the pinned metadata that back this repository's automated checks.
There is no application code here; the only script is the documentation gate.

| Path | Purpose |
| --- | --- |
| [`workflows/docs.yml`](workflows/docs.yml) | The `docs` workflow: the offline `links and metadata` gate and the network-dependent `gnn conformance (pinned)` job. |
| [`scripts/check_docs.py`](scripts/check_docs.py) | Validates relative Markdown links, tracked YAML, and `CITATION.cff` keys. |
| [`gnn-pin.json`](gnn-pin.json) | The pinned Generalized Notation Notation revision (`v5.0.3`, commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`) used by the conformance job. |
| [`dependabot.yml`](dependabot.yml) | Dependabot configuration for GitHub Actions updates. |

## Running the gate locally

```bash
python -m pip install pyyaml==6.0.2
python .github/scripts/check_docs.py
```

See [`../docs/validation.md`](../docs/validation.md) for what the gate checks and
[`../docs/gnn-materials.md`](../docs/gnn-materials.md) for the conformance job.

## Editing rules

- Workflows pin actions by commit SHA; keep the pinned revisions and do not edit
  them as part of a documentation change.
- `gnn-pin.json` is a curated pin, not a lockfile; change it only when the GNN
  conformance target intentionally moves, and re-verify the model afterwards.
