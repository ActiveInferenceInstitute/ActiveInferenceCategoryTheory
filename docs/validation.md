# Documentation gate

This repository has no runtime, so its only executable check is the documentation
gate. It runs in CI on every pull request and on pushes to `main`, and it is the
repository's declared `docs` task (see [`../AGENTS.md`](../AGENTS.md)).

## What it runs

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) has two jobs:

| Job | What it does | Needs network |
| --- | --- | --- |
| `links and metadata` | Runs [`check_docs.py`](../.github/scripts/check_docs.py). | No |
| `gnn conformance (pinned)` | Installs the pinned GNN parser and type-checks the model. | Yes |

See [`gnn-materials.md`](gnn-materials.md) for the conformance job.

## What `check_docs.py` checks

[`.github/scripts/check_docs.py`](../.github/scripts/check_docs.py) fails, with
exit code 1, on any of three conditions:

1. A relative Markdown link or image target does not resolve to a path inside the
   repository that exists at the checked-out commit. Links may not escape the
   repository; fragments (`#...`) and absolute URLs are ignored.
2. A tracked YAML file (including [`CITATION.cff`](../CITATION.cff)) does not
   parse as YAML.
3. `CITATION.cff` lacks any of the required Citation File Format keys
   `cff-version`, `title`, or `license`.

External URLs are not fetched: the verdict must not depend on third-party
availability.

## Run it locally

The gate's only dependency is PyYAML, and it needs no network:

```bash
python -m pip install pyyaml==6.0.2
python .github/scripts/check_docs.py
```

A passing run prints `checked N tracked files: relative links resolve; YAML
parses`.

## Failure proof

The gate is known to be able to fail. CI run 41720066280, job
`links and metadata`, logs `README.md: missing link target: does-not-exist.md`
followed by `##[error]Process completed with exit code 1`. The root
[`README.md`](../README.md#documentation-gate) records the same reproduction.
