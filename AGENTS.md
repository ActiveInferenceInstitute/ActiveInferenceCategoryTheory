# Agent guide — ActiveInferenceCategoryTheory

Active Inference & Category Theory — an Active Inference Institute repository for learning about and exploring where Active Inference and Category Theory meet.

## Working notes

- Repository: `ActiveInferenceInstitute/ActiveInferenceCategoryTheory` (default branch `main`).
- InstituteOS classification: category `education`, maturity `released`, status `active`.
- License: `CC0-1.0`.
- Keep private content in private repositories; never commit credentials,
  personal data, or unverified claims.
- Read [`README.md`](README.md) first, then the nearest nested `AGENTS.md`.
- Documentation lives in [`docs/`](docs/README.md) (index, repository layout,
  GNN workflow, validation) and in [`gnn/`](gnn/README.md); the curriculum is
  [`IntroAdventureSyllabus.md`](IntroAdventureSyllabus.md).
- Prefer small, verified changes; run the declared tasks before handing work back.

## Tasks

| Task | Command | Working directory |
| --- | --- | --- |
| `inventory` | `git ls-files` | `.` |
| `docs` | `python .github/scripts/check_docs.py` | `.` |

The `docs` gate checks relative Markdown links and images, tracked YAML, and the
`CITATION.cff` metadata fields. Its only dependency is PyYAML
(`python -m pip install pyyaml==6.0.2`); it needs no network and no Lean toolchain.

## InstituteOS sidecar

This repository carries a committed [`.aii/`](.aii/README.md) sidecar with curated
InstituteOS metadata (`aii-sidecar/v1`): category, maturity, ecosystem relations,
key artifacts, provenance, and portable tasks. It is read by
[InstituteOS](https://github.com/ActiveInferenceInstitute/InstituteOS) tooling and
does not affect the project's build or runtime. Regenerating the sidecar docs
rewrites only `.aii/README.md`, `.aii/AGENTS.md`, `.aii/docs/README.md`,
`.aii/docs/AGENTS.md`, and `.aii/docs/INTEGRATION.md`.
