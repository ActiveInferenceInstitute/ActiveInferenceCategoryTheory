# GNN materials and conformance

The [`gnn/`](../gnn/README.md) folder supports the *Map the model* activity in
the [Connections unit](../IntroAdventureSyllabus.md#connections) of the syllabus.
It holds exactly one GNN model source plus a walk-through:

| File | Role |
| --- | --- |
| [`gnn/README.md`](../gnn/README.md) | Orientation to the activity and the verification result. |
| [`gnn/learner_perception_model.md`](../gnn/learner_perception_model.md) | The model: a two-state perception model of the reader, written in GNN section order. |
| [`gnn/map_the_model.template.md`](../gnn/map_the_model.template.md) | The exercise: a starting category-theory-to-GNN correspondence, a hand-worked perception update, and how to run your own model. |

[`../.github/GNN.md`](../.github/GNN.md) is the pointer that records what the
conformance step parses and why the model is not named `*.gnn.md`.

## The pin

The upstream parser is pinned in [`../.github/gnn-pin.json`](../.github/gnn-pin.json),
a curated pin rather than a lockfile. Its schema is `gnn-importer-pin/v1` and it
records:

| Field | Value |
| --- | --- |
| `repository` | `ActiveInferenceInstitute/Generalized_Notation_Notation` |
| `tag` | `v5.0.3` |
| `revision` | `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1` |
| `recorded` | `2026-11-12` |

`./run.sh setup` installs exactly that revision; `./run.sh gnn` then asserts the
imported `gnn.__version__` matches `tag`, parses
`gnn/learner_perception_model.md`, checks its syntax, and runs the GNN type
checker. In CI both commands are steps of the `gate` job, the second named
`gnn conformance (pinned)`.

Change the pin only when the conformance target intentionally moves, and
re-verify the model afterwards: [`../.github/README.md`](../.github/README.md)
records that editing rule.

## Why the walk-through is named `*.template.md`

The GNN pipeline's directory discovery treats `*.template.md` as non-model
Markdown (and also excludes `README.md`). Naming the walk-through
`map_the_model.template.md` means that pointing the pipeline at `gnn/` parses
exactly one model source, `learner_perception_model.md`, with no "invalid file"
noise from the prose. Do not rename it to a bare `*.md` unless you also adjust
the pipeline invocation.

## Run the check locally

```bash
./run.sh setup   # installs the pinned parser; needs network
./run.sh gnn     # parse + type-check; prints {"gnn-version": ..., "result": "verified"}
```

Without `setup`, the arm exits with code 2 and says the parser is missing, so a
missing environment is never reported as a model failure. CI is the only place
the check runs automatically; a documentation-only change does not require it.

To run the upstream pipeline directly from a clone of the GNN repository, steps
3 and 5 parse and type-check a directory of specifications:

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
