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

Every check is an arm of [`run.sh`](run.sh); the workflow calls the same arms and
holds no copy of a command. See [`docs/run-guide.md`](docs/run-guide.md).

| Task | Command | Working directory | Network |
| --- | --- | --- | --- |
| `inventory` | `git ls-files` | `.` | No |
| `docs` | `./run.sh docs` | `.` | No |
| `links` | `./run.sh links` | `.` | No |
| `metadata` | `./run.sh metadata` | `.` | No |
| `index` | `./run.sh index` | `.` | No |
| `tests` | `./run.sh tests` | `.` | No |
| `gnn` | `./run.sh setup && ./run.sh gnn` | `.` | Yes |
| `measure` | `./run.sh measure` | `.` | Yes |

The `docs` arm checks relative Markdown links and images, tracked YAML, the
`CITATION.cff` metadata fields, and that every tracked Markdown document appears
in [`docs/documentation-index.md`](docs/documentation-index.md). Its only
dependency is PyYAML (`python3 -m pip install pyyaml==6.0.2`); it needs no
network and no Lean toolchain. The `tests` arm runs the gate scripts' unit tests
with the GNN parser stubbed, so it needs only the standard library. The `gnn` arm
installs the parser pinned in
[`.github/gnn-pin.json`](.github/gnn-pin.json) and type-checks
`gnn/learner_perception_model.md`. The `measure` arm regenerates
[`docs/arm-runtimes.md`](docs/arm-runtimes.md), the only home for measured
numbers.

## InstituteOS sidecar

This repository carries a committed [`.aii/`](.aii/README.md) sidecar with curated
InstituteOS metadata (`aii-sidecar/v1`): category, maturity, ecosystem relations,
key artifacts, provenance, and portable tasks. It is read by
[InstituteOS](https://github.com/ActiveInferenceInstitute/InstituteOS) tooling and
does not affect the project's build or runtime. Regenerating the sidecar docs
rewrites only `.aii/README.md`, `.aii/AGENTS.md`, `.aii/docs/README.md`,
`.aii/docs/AGENTS.md`, and `.aii/docs/INTEGRATION.md`.
