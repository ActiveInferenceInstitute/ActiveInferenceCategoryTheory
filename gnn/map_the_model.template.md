# Map the Model — a GNN scaffold for the Connections unit

This page supports the *Map the model* activity in the
[Connections unit](../IntroAdventureSyllabus.md#connections) of the
adventure-mode syllabus. There, you are asked what kind of Active Inference
model the category-theoretic account arrives at, and to represent it however
you can.

Generalized Notation Notation (GNN) gives you one concrete anchor to push
against: a plain-text way to write a generative model that a machine can parse,
type-check, render and run. Writing your own model in GNN is a cheap way to
find out whether you actually know what states, observations and parameters
your picture has — and where the category-theoretic structure you have been
studying does not fit into a generative model at all.

- Specification file: [learner_perception_model.md](learner_perception_model.md)
- Background: Smékal, J. and Friedman, D. A. (2023) [Generalized Notation
  Notation for Active Inference Models](https://zenodo.org/records/7803328)

This file carries the GNN pipeline's `*.template.md` marker for non-model
Markdown, so pointing the pipeline at this directory parses exactly one model
source, `learner_perception_model.md`.

## 1. Read the specification

Open [learner_perception_model.md](learner_perception_model.md). It declares a
two-state perception model of *yourself* reading this syllabus: a notion is
either **rooted** (connected to what you already know) or **floating** (not yet
attached), and the observation is whether the passage **reads smoothly** or
**reads as noise**.

| Section | What it declares |
|---------|------------------|
| `GNNSection`, `GNNVersionAndFlags` | Which flavour of model this is and which notation version it follows |
| `ModelName`, `ModelAnnotation` | The model's identity and a plain-language reading of it |
| `StateSpaceBlock` | The variables and their dimensions — hidden state `s`, observation `o`, action `u`, and the matrices `A`, `B`, `C`, `D` |
| `Connections` | Which variable bears on which: `D>s`, `s-A`, `A-o`, `s-B`, `B>u`, `u>s` |
| `InitialParameterization` | The actual numbers in `A`, `B`, `C`, `D` |
| `Equations` | The update rule and worked evaluations of it |
| `Time` | `Static` — one observation, no rollout |
| `ActInfOntologyAnnotation` | The Active Inference name of each variable |
| `ModelParameters` | Counts and tensor conventions |

Notice how much of the work is done by `StateSpaceBlock` and `Connections`: the
notation separates *what exists*, *what bears on what*, and *what the numbers
are*. That separation is the part worth carrying back into your sketch.

## 2. Try the mapping

Here is a starting correspondence to argue with, not a theorem. Map the
category-theoretic vocabulary you have collected onto the model, then write in
the last column where it strains.

| Category-theoretic reading | GNN counterpart | Does it hold up? |
|----------------------------|-----------------|------------------|
| Object of a category | A typed variable with a dimension, e.g. `s[2,1,type=float]` (state), `o[2,1,type=int]` (observation) | Types and dimensions are declared, but GNN has no composition law on them |
| Morphism | A connection between variables: `s-A`, `A-o`, `D>s` | Directionality is there; identity and associativity are not stated anywhere |
| Monoidal product | Separate factor blocks in one `StateSpaceBlock` (a model with two agents or two modalities would declare both) | Factors are declared side by side; the tensor structure itself is implicit |
| Bayesian inversion / lens-like interface | The `A` and `D` matrices plus the update rule `q(s) = D[s]A[o,s] / sum_j D[j]A[o,j]` | This is the strongest correspondence: the update *consumes* an observation and *produces* a posterior belief |
| Doctrine, 2-cell, higher structure | Nothing | GNN fixes a first-order generative-model skeleton; it does not encode the higher-categorical layer |

The last row is the interesting one. If your story map has doctrines,
2-morphisms or lenses doing real work, GNN will not hold them, and saying
precisely *why* is a better outcome of this activity than forcing them into a
matrix.

## 3. Do one perception update by hand

With the shipped numbers, `D = (0.4, 0.6)` and `A = ((0.85, 0.25), (0.15, 0.75))`:

1. *Reads smoothly* (`o = 0`): unnormalized belief is
   `(0.4 × 0.85, 0.6 × 0.25) = (0.34, 0.15)`, and `P(o = 0) = 0.49`, so
   `q ≈ (0.6939, 0.3061)`.
2. *Reads as noise* (`o = 1`): unnormalized belief is
   `(0.4 × 0.15, 0.6 × 0.75) = (0.06, 0.45)`, and `P(o = 1) = 0.51`, so
   `q ≈ (0.1176, 0.8824)`.

Then read the second row of `Connections`. Action 0 re-reads the passage and
drifts toward *rooted* with probability 0.85; action 1 moves on and drifts
toward *floating* with probability 0.80. Ask what the category-theoretic account
would say about those two moves as morphisms, and whether "action" there means
what it means here.

## 4. Write your own

Copy the specification file, rename it, and answer for your own model:

1. What are the hidden states, and how many? If a state is not a dimension in a
   space, say so explicitly in `ModelAnnotation`.
2. What is observed, and how does it depend on the hidden state?
3. What is fixed (`A`, `D`) and what is learned over time?
4. Which of your story-map notions appear nowhere in the file? Keep that list;
   it is the honest boundary of the mapping.

Keep the section order and names; GNN reads them by name. `ModelAnnotation` is
the place for the caveats your teacher-self will need in six months.

## 5. Run it

The format is executable. From a clone of the GNN repository, steps 3 and 5
parse and type-check a directory of specifications:

```bash
python src/gnn/main.py --only-steps "3,5" --target-dir path/to/gnn --output-dir output
```

The specification shipped here was checked that way against the GNN v5.0.3
implementation (commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`): pointed at
this directory, step 3 parsed 1 model file and serialized 22 formats with no
parse failures, and step 5 reported the model valid with 0 errors, 0 warnings
and 21 parameters.

## Provenance and license

The model here is original to this repository and, like the rest of it, is
dedicated to the public domain under [CC0 1.0](../LICENSE). The file format
follows the exemplar corpus of the GNN project
([Generalized_Notation_Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)),
which the examples above were verified against; the GNN project is MIT-licensed
and is cited above rather than copied. The model being mapped is St Clere
Smithe's
[*Mathematical Foundations for a Compositional Account of the Bayesian
Brain*](https://arxiv.org/abs/2212.12538), not the specification file here.
