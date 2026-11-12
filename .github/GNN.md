# GNN conformance

`gnn conformance (pinned)` is defined in `.github/workflows/docs.yml` and reads
`.github/gnn-pin.json`, which pins
`ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.0.3`
(`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`).

The job installs the pinned parser and parses and type-checks the repository's
model declaration, `gnn/learner_perception_model.md`. That file is not named
`.gnn.md`; this pointer records the existing bespoke validation, not a claim
that a second canonical model exists.
