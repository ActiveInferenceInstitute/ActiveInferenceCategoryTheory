# Documentation index

Flat index of every long-lived document in
`ActiveInferenceInstitute/ActiveInferenceCategoryTheory`. The hub is
[`README.md`](README.md); this page is the exhaustive list. Every tracked
Markdown file must appear here — the `index` arm of [`../run.sh`](../run.sh)
fails otherwise, so add a row when you add a document.

Start reading at [`../README.md`](../README.md) for the overview and
[`../IntroAdventureSyllabus.md`](../IntroAdventureSyllabus.md) for the curriculum.

## Entry points and orientation

| Document | Purpose | Kind |
| --- | --- | --- |
| [`../README.md`](../README.md) | Repository overview, contents, citation, documentation gate. | source |
| [`../IntroAdventureSyllabus.md`](../IntroAdventureSyllabus.md) | The curriculum: readings, sections, exercises. | source |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to propose changes; license dedication. | source |
| [`../AGENTS.md`](../AGENTS.md) | Agent guidance and the declared task commands. | source |
| [`../TO-DO.md`](../TO-DO.md) | Documentation review log and open items. | source |
| [`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md) | Record of the cross-cutting documentation review. | source |

## Operational documentation

| Document | Purpose | Kind |
| --- | --- | --- |
| [`validation.md`](validation.md) | What the documentation gate checks and how to reproduce a failure. | source |
| [`repository-layout.md`](repository-layout.md) | What every top-level file and folder is for. | source |
| [`gnn-materials.md`](gnn-materials.md) | The GNN model, the walk-through, and the pinned conformance check. | source |

## GNN materials

| Document | Purpose | Kind |
| --- | --- | --- |
| [`../gnn/README.md`](../gnn/README.md) | Orientation to the *Map the model* activity. | source |
| [`../gnn/learner_perception_model.md`](../gnn/learner_perception_model.md) | The model specification validated by the conformance arm. | source |
| [`../gnn/map_the_model.template.md`](../gnn/map_the_model.template.md) | The exercise that maps category theory onto a GNN specification. | source |

## CI and automation

| Document | Purpose | Kind |
| --- | --- | --- |
| [`../.github/README.md`](../.github/README.md) | The `.github/` folder guide: workflow, scripts, pin, Dependabot. | source |
| [`../.github/GNN.md`](../.github/GNN.md) | Pointer recording what the conformance step parses and why. | source |

## Metadata and legal

| Document | Purpose | Kind |
| --- | --- | --- |
| [`../CITATION.cff`](../CITATION.cff) | Citation File Format metadata validated by the gate. | metadata |
| [`../LICENSE`](../LICENSE) | CC0 1.0 Universal public-domain dedication. | legal |
| [`../.aii/README.md`](../.aii/README.md) | InstituteOS sidecar overview (`aii-sidecar/v1`). | generated |
| [`../.aii/AGENTS.md`](../.aii/AGENTS.md) | Agent notes for the sidecar. | generated |
| [`../.aii/docs/README.md`](../.aii/docs/README.md) | Sidecar documentation hub. | generated |
| [`../.aii/docs/AGENTS.md`](../.aii/docs/AGENTS.md) | Sidecar documentation agent notes. | generated |
| [`../.aii/docs/INTEGRATION.md`](../.aii/docs/INTEGRATION.md) | How InstituteOS consumes the sidecar. | generated |

"Generated" means a script owns the file: the `.aii/` documents come from
InstituteOS tooling. Edit the producer, not the output; see
[`repository-layout.md`](repository-layout.md).
