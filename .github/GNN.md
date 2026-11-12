# GNN conformance

The conformance check is the `./run.sh gnn` arm of [`../run.sh`](../run.sh), run
in CI as the step `gnn conformance (pinned)` inside the `gate` job of
`.github/workflows/docs.yml`. It reads `.github/gnn-pin.json` — schema
`gnn-importer-pin/v1` — which pins
`ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.0.3`
(`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`, recorded `2026-11-12`).

The check asserts the installed `gnn.__version__` matches the pin's `tag`, then
parses and type-checks the repository's model declaration,
`gnn/learner_perception_model.md`. That file is not named `.gnn.md`; this pointer
records the existing bespoke validation, not a claim that a second canonical
model exists.

Provision the parser with `./run.sh setup` before running the arm locally; without
it the arm exits with code 2 instead of reporting a model failure. See
[`../docs/gnn-materials.md`](../docs/gnn-materials.md) for the full description.
