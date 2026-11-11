# GNN materials and conformance

The [`gnn/`](../gnn/README.md) folder supports the *Map the model* activity in
the [Connections unit](../IntroAdventureSyllabus.md#connections) of the syllabus.
It holds exactly one GNN model source plus a walk-through:

| File | Role |
| --- | --- |
| [`gnn/README.md`](../gnn/README.md) | Orientation to the activity and the verification result. |
| [`gnn/learner_perception_model.md`](../gnn/learner_perception_model.md) | The model: a two-state perception model of the reader, written in GNN section order. |
| [`gnn/map_the_model.template.md`](../gnn/map_the_model.template.md) | The exercise: a starting category-theory-to-GNN correspondence, a hand-worked perception update, and how to run your own model. |

## Why the walk-through is named `*.template.md`

The GNN pipeline's directory discovery treats `*.template.md` as non-model
Markdown (and also excludes `README.md`). Naming the walk-through
`map_the_model.template.md` means that pointing the pipeline at `gnn/` parses
exactly one model source, `learner_perception_model.md`, with no "invalid file"
noise from the prose. Do not rename it to a bare `*.md` unless you also adjust
the pipeline invocation.

## The pinned revision

The upstream parser is pinned in [`../.github/gnn-pin.json`](../.github/gnn-pin.json)
to `ActiveInferenceInstitute/Generalized_Notation_Notation` v5.0.3, commit
`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`. The `gnn conformance (pinned)` job in
[`../.github/workflows/docs.yml`](../.github/workflows/docs.yml) installs that
exact revision, asserts the imported `gnn.__version__` matches the pin, parses
`learner_perception_model.md`, checks its syntax, and runs the GNN type checker.

CI is the only check here that needs network access (it installs the pinned
parser). A documentation-only change does not require it to run locally.

## Reproduce the check locally

From a clone of the GNN repository, steps 3 and 5 parse and type-check a
directory of specifications:

```bash
python src/gnn/main.py --only-steps "3,5" --target-dir path/to/gnn --output-dir output
```

Pointed at `gnn/`, that run parsed one model file and serialized 22 formats with
no parse failures, and reported the model valid with 0 errors, 0 warnings, and 21
parameters. The walk-through quotes those counts, and its hand-computed
posteriors were checked independently against the parameterization in
`learner_perception_model.md`.

## License

These materials are dedicated to the public domain under
[CC0 1.0](../LICENSE), like the rest of the repository, per
[CONTRIBUTING.md](../CONTRIBUTING.md). The GNN file format belongs to the GNN
project (MIT-licensed); the specification here is original to this repository.
