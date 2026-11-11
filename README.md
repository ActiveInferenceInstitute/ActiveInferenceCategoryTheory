# ActiveInferenceCategoryTheory

*Active Inference & Category Theory* — an [Active Inference Institute](https://www.activeinference.org/) repository for learning about and exploring where Active Inference and Category Theory meet.

## Contents

- [IntroAdventureSyllabus.md](IntroAdventureSyllabus.md) — *Introduction to Category Theory applied to Active Inference, Adventure Mode*: a self-paced, "adventure mode" curriculum for reading and researching active-inference papers that use category-theoretic tools. For those who seek a nonlinear, jump-right-into-the-deep-end experience.
- [docs/](docs/README.md) — documentation index: repository layout, the GNN conformance workflow, and the documentation gate, alongside links to every other document.
- [gnn/](gnn/README.md) — GNN (Generalized Notation Notation) materials for the *Map the model* activity: a small runnable model specification and a walk-through that maps category-theoretic notions onto a generative-model notation, and marks where the mapping runs out. Repositories that consume the notation follow the [GNN downstream adoption guide](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/main/docs/gnn/integration/downstream_adoption.md).
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to propose improvements to the curriculum.
- [LICENSE](LICENSE) — CC0 1.0 Universal (public-domain dedication).
- [.aii/config.yaml](.aii/config.yaml) — InstituteOS sidecar metadata for this repository.

## Citation

If you use this repository in your work, please cite it as:

> Active Inference Institute. *Active Inference & Category Theory*. https://github.com/ActiveInferenceInstitute/ActiveInferenceCategoryTheory

Machine-readable citation metadata is available in [CITATION.cff](CITATION.cff).

## Documentation gate

[`.github/workflows/docs.yml`](.github/workflows/docs.yml) runs
[`.github/scripts/check_docs.py`](.github/scripts/check_docs.py) on every pull
request and on pushes to `main`. The gate fails, with exit code 1, when a
relative Markdown link or image does not resolve, when a tracked YAML file does
not parse, or when `CITATION.cff` lacks `cff-version`, `title` or `license`.
The proof that it can fail is run 41720066280, job `links and metadata`: the log
line `README.md: missing link target: does-not-exist.md` is followed by
`##[error]Process completed with exit code 1.`

Reproduce it locally — the gate's only dependency is PyYAML:

```bash
python -m pip install pyyaml==6.0.2
python .github/scripts/check_docs.py
```
