# ActiveInferenceCategoryTheory

*Active Inference & Category Theory* — an [Active Inference Institute](https://www.activeinference.org/) repository for learning about and exploring where Active Inference and Category Theory meet.

## Contents

- [IntroAdventureSyllabus.md](IntroAdventureSyllabus.md) — *Introduction to Category Theory applied to Active Inference, Adventure Mode*: a self-paced, "adventure mode" curriculum for reading and researching active-inference papers that use category-theoretic tools. For those who seek a nonlinear, jump-right-into-the-deep-end experience.
- [docs/](docs/README.md) — documentation index: repository layout, the GNN conformance workflow, and the documentation gate, alongside links to every other document.
- [gnn/](gnn/README.md) — GNN (Generalized Notation Notation) materials for the *Map the model* activity: a small runnable model specification and a walk-through that maps category-theoretic notions onto a generative-model notation, and marks where the mapping runs out. Repositories that consume the notation follow the [GNN downstream adoption guide](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/main/docs/gnn/integration/downstream_adoption.md) (that guide is on GNN `main`; it is not present at the pinned revision in [`.github/gnn-pin.json`](.github/gnn-pin.json)).
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to propose improvements to the curriculum.
- [LICENSE](LICENSE) — CC0 1.0 Universal (public-domain dedication).
- [.aii/config.yaml](.aii/config.yaml) — InstituteOS sidecar metadata for this repository.

## Citation

If you use this repository in your work, please cite it as:

> Active Inference Institute. *Active Inference & Category Theory*. https://github.com/ActiveInferenceInstitute/ActiveInferenceCategoryTheory

Machine-readable citation metadata is available in [CITATION.cff](CITATION.cff).

## Documentation gate

[`run.sh`](run.sh) is the single entry point for every check; each arm is the
exact command CI runs. [`.github/workflows/docs.yml`](.github/workflows/docs.yml)
runs three of them in one job, `docs gate`, on every pull request and on pushes
to `main`: `./run.sh docs` (step `links and metadata`), `./run.sh tests` (step
`gate unit tests (hermetic)`), and `./run.sh gnn` (step
`gnn conformance (pinned)`).

`./run.sh docs` fails, with exit code 1, when a relative Markdown link or image
does not resolve, when a tracked YAML file does not parse, when `CITATION.cff`
lacks `cff-version`, `title` or `license`, or when a tracked Markdown document is
missing from [`docs/documentation-index.md`](docs/documentation-index.md). The
proof that it can fail is run 41720066280, in the job then named
`links and metadata`: the log line `README.md: missing link target:
does-not-exist.md` is followed by `##[error]Process completed with exit code 1.`

Reproduce it locally — the offline arm's only dependency is PyYAML:

```bash
python3 -m pip install pyyaml==6.0.2
./run.sh docs
```

[`docs/run-guide.md`](docs/run-guide.md) lists every arm and
[`docs/arm-runtimes.md`](docs/arm-runtimes.md) holds the measured wall time of
each; [`docs/validation.md`](docs/validation.md) explains what the gate checks.

## Education contract

[`education-contract.json`](education-contract.json) declares adoption of the
[Education workflow contract](https://github.com/ActiveInferenceInstitute/courses/blob/main/docs/workflows/education.md).
[`specs/education/schema.json`](specs/education/schema.json) is the unchanged
canonical schema; [`category-theory.json`](specs/education/category-theory.json)
is a curated transcription of the authored learning plan.

Each teaching section under **Topics and Sections** in the
[syllabus](IntroAdventureSyllabus.md#topics-and-sections) becomes a unit, with its
heading as the title and its opening learning-focus sentence as the objective.
The [GNN scaffold](gnn/map_the_model.template.md) contributes the *Map the Model*
unit, quoting its perception-update and model-writing prompts; its executable
example remains [the learner perception model](gnn/learner_perception_model.md),
not a separate invented learning objective. Unit `source_path` fields and the
bundle's source revision identify the authored material.

Prerequisites and glossary are empty: suggested reading order and optional
external pre-/co-requisites are not internal dependency edges, and the GNN
correspondence table explicitly offers analogies rather than definitions.
The workload outline's “Applying in the variability-retained world” has no
teaching section or objective to transcribe. No topic, stratum, or audience
classification is inferred.

With the lead checkout alongside this repository, validate using its checker
without installing into or writing to the lead:

```bash
python3 -B ../courses/software/scripts/check_education_contract.py \
  specs/education/category-theory.json
python3 -B ../courses/software/scripts/check_education_contract.py
./run.sh docs
./run.sh gnn
```

`gnn` is the member's executable content check; the `tests` arm covers the gate
scripts themselves and asserts nothing about the bundle. Keep bundle wording
aligned with the linked sources when editing the learning plan.
