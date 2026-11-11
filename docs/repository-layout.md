# Repository layout

`ActiveInferenceInstitute/ActiveInferenceCategoryTheory` is a documentation-only
repository: it ships a curriculum and its supporting metadata, with no package,
no build, and no runtime. This page maps the tracked tree.

## Top level

| Path | Kind | Purpose |
| --- | --- | --- |
| [`README.md`](../README.md) | source | Repository overview, contents, citation, and the documentation gate. |
| [`IntroAdventureSyllabus.md`](../IntroAdventureSyllabus.md) | source | The curriculum: readings, videos, sections, and exercises. |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | source | How to propose changes; license dedication. |
| [`CITATION.cff`](../CITATION.cff) | metadata | Citation File Format record validated by the gate. |
| [`LICENSE`](../LICENSE) | legal | CC0 1.0 Universal public-domain dedication. |
| [`AGENTS.md`](../AGENTS.md) | source | Agent guidance and declared task commands. |
| [`TO-DO.md`](../TO-DO.md) | source | Documentation review log and open items. |
| [`REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md) | source | Record of the cross-cutting documentation review. |
| [`docs/`](README.md) | source | This documentation tree. |

## Folders

| Path | Purpose |
| --- | --- |
| [`gnn/`](../gnn/README.md) | GNN materials for the *Map the model* activity: the model specification and the walk-through. See [`gnn-materials.md`](gnn-materials.md). |
| [`.github/`](../.github/README.md) | Workflows, the pinned GNN revision, Dependabot, and the documentation gate. |
| `.aii/` | InstituteOS sidecar: curated institutional metadata (`aii-sidecar/v1`). See [`.aii/README.md`](../.aii/README.md). |

## Source versus generated

Nothing in the tree is generated: every Markdown, YAML, and CFF file is
hand-maintained and reviewed. The `gnn/learner_perception_model.md`
specification is hand-written but is *validated* against the pinned GNN parser in
CI; it is not rendered from code. There is no `output/`, `dist/`, or `build/`
directory, and no dependency lockfile.

## Conventions

- One H1 per document; use H2 and H3 for structure.
- Every relative Markdown link must resolve inside the repository — the
  [documentation gate](validation.md) enforces this.
- Keep the "adventure mode" voice of the syllabus when editing curriculum text.
- Prefer plain Markdown and avoid trailing whitespace.
