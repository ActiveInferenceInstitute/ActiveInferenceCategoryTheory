# Documentation — ActiveInferenceCategoryTheory

Documentation index for **`ActiveInferenceInstitute/ActiveInferenceCategoryTheory`**,
a docs-only curriculum repository. There is no build step, package, or runtime:
every file here is Markdown plus the metadata that the CI gate validates.

Start with [`../README.md`](../README.md) for the repository overview and
[`../IntroAdventureSyllabus.md`](../IntroAdventureSyllabus.md) for the curriculum
itself.

## This folder

- [`repository-layout.md`](repository-layout.md) — what every top-level file and
  folder is for, and which files are source versus generated.
- [`gnn-materials.md`](gnn-materials.md) — the `gnn/` model, the *Map the model*
  walk-through, and how the pinned GNN conformance job verifies them.
- [`validation.md`](validation.md) — the `check_docs.py` gate: what it checks,
  how to run it offline, and how to reproduce a failure.

## Curriculum

- [`../IntroAdventureSyllabus.md`](../IntroAdventureSyllabus.md) — *Introduction
  to Category Theory applied to Active Inference, Adventure Mode*: a self-paced
  curriculum for reading active-inference papers that use category-theoretic
  tools. Sections: Course Information, Topics and Sections (Introduction,
  Foundations, Basic Category Theory, Higher category theory and application,
  Connections, Pathways forward), Other Resources, Encouragement, Thanks.

## GNN materials

- [`../gnn/README.md`](../gnn/README.md) — orientation to the *Map the model*
  activity.
- [`../gnn/map_the_model.template.md`](../gnn/map_the_model.template.md) — the
  walk-through that maps category-theoretic notions onto a GNN specification.
- [`../gnn/learner_perception_model.md`](../gnn/learner_perception_model.md) —
  the two-state perception model the walk-through maps onto.

See [`gnn-materials.md`](gnn-materials.md) for how these are verified.

## Contributing and citation

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — how to propose changes.
- [`../CITATION.cff`](../CITATION.cff) — machine-readable citation metadata.
- [`../LICENSE`](../LICENSE) — CC0 1.0 Universal (public-domain dedication).

## Repository metadata

- [`../AGENTS.md`](../AGENTS.md) — agent guidance and the declared task commands.
- [`../TO-DO.md`](../TO-DO.md) — the documentation review log and open items.
- [`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md) — the
  cross-cutting review record.
- [`../.aii/README.md`](../.aii/README.md) — the InstituteOS sidecar.

## Status

Everything in this repository works offline: there is no install step and no
network call. The only executable check is the documentation gate described in
[`validation.md`](validation.md), which needs PyYAML and nothing else. The GNN
conformance job in CI is the one check that needs network access, because it
installs the pinned GNN parser; it is not required to work on a documentation
change.
