# GNN materials for the syllabus

[Generalized Notation Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
(GNN) is a plain-text notation for Active Inference generative models: a
specification declares its variables and dimensions, what connects to what, the
parameters, and the equations, in named sections a program can read.

These files support the *Map the model* activity in the
[Connections unit](../IntroAdventureSyllabus.md#connections):

- **[map_the_model.template.md](map_the_model.template.md)** — the exercise: how
  to read a specification, a starting correspondence between category-theoretic
  notions and GNN sections, a hand-worked perception update, and how to run your
  own model.
- **[learner_perception_model.md](learner_perception_model.md)** — a two-state
  perception model of the reader, written in GNN section order. It is the anchor
  you map onto and then argue with.

The walk-through is named with the GNN pipeline's `*.template.md` marker for
non-model Markdown, so `learner_perception_model.md` is the only model source a
directory-level parse picks up (the pipeline's own discovery predicate also
excludes `README.md`). That keeps the verification command below free of
"invalid file" noise from this prose.

The point of the exercise is not that category theory reduces to a matrix
specification. It is the opposite: writing the model down shows exactly which of
your notions survive the translation, and where they do not fit. Section 2 of
the walk-through keeps that boundary explicit.

## Verification

The shipped specification was parsed and type-checked by the GNN implementation
at commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1` (v5.0.3). The repository's
`gnn conformance (pinned)` CI step (`./run.sh gnn`) installs that revision from
[`.github/gnn-pin.json`](../.github/gnn-pin.json), parses
`learner_perception_model.md`, and runs the GNN type checker with `strict=True`; the
job requires the checker to return `True` (a `2` or `False` fails it).

The equivalent full-pipeline check is:

```bash
python src/gnn/main.py --only-steps "3,5" \
  --target-dir path/to/ActiveInferenceCategoryTheory/gnn \
  --output-dir output
```

Result of that manual full-pipeline run (not produced by the CI or `./run.sh gnn`
job), pointed at this directory: step 3 parsed 1 file with 0
failures and serialized 22 formats; step 5 reported the model valid with 0
errors, 0 warnings and 21 parameters. The hand-computed posteriors in the
walk-through were re-checked independently against the parameterization in the
file.

## License

These materials are dedicated to the public domain under
[CC0 1.0](../LICENSE), like the rest of this repository, per
[CONTRIBUTING.md](../CONTRIBUTING.md). The GNN file format belongs to the GNN
project (MIT-licensed); the specification here is original to this repository.
