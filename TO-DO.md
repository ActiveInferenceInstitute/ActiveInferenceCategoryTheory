# TO-DO — ActiveInferenceCategoryTheory docs-deep review

Last reviewed: 2026-11-11

Findings from the docs-deep review pass and the 2026-11-11 completeness pass,
scoped by severity:

- **Minor** = typo, broken link, formatting issue.
- **Medium** = stale section rewrite, doc restructure, added missing guide.
- **Major** = large doc-system overhaul / cross-cutting refactor.

## Minor

- [x] ✓ Fix typos in IntroAdventureSyllabus.md: "skteching", "there wil", "intution", "Kleisi", "catgory", "Modelstream"→"ModelStream", "Github"→"GitHub", missing comma after "right", missing space after "--" (2×), "bound,variational" (`IntroAdventureSyllabus.md`) — commit `7041baf`
- [x] ✓ Fix "p. 416-416" → "p. 416" and "co-founded the Topos Institute since" → "since then" (`IntroAdventureSyllabus.md`) — commit `7041baf`
- [x] ✓ Remove stray ")" in the Roman "Course: Category Theory" YouTube link (`IntroAdventureSyllabus.md`) — commit `7041baf`
- [x] ✓ Replace dead links: Zenodo tracking fragment → canonical `https://zenodo.org/records/7803328`; twitter http→https; textbook-group sign-up 404 → live Institute education page; jrlearnstomath blog (410, never archived) → reworded, link dropped (`IntroAdventureSyllabus.md`) — commit `7041baf`
- [x] ✓ Remove trailing whitespace on 5 lines (README.md, IntroAdventureSyllabus.md lines 19/53/79/119) — commits `7041baf`, `b0ac3e5`

## Medium

- [x] ✓ Expand README from a 6-line stub: repository contents, license clarity (CC0 1.0), citation line, cross-links (`README.md`) — commit `b0ac3e5`
- [x] ✓ Normalize heading hierarchy (single H1; Course Information / Topics and Sections / Other Resources / Encouragement / Thanks as H2; subsections H3; "**Notes**" → "### Notes") and add a compact contents list (`IntroAdventureSyllabus.md`) — commit `7041baf`
- [x] ✓ Add CONTRIBUTING.md: contribution channels (issues/PRs, Discord, X), verification guidelines, CC0 dedication note — grounded in the syllabus's own invitation (`CONTRIBUTING.md`) — commit `83f3932`
- [x] ✓ Add CITATION.cff with Institute attribution, CC0-1.0 license, release date from repo history (2023-05-12) (`CITATION.cff`) — commit `83f3932`
- [x] ✓ Align InstituteOS sidecar: add IntroAdventureSyllabus.md / CONTRIBUTING.md / CITATION.cff to `artifacts`, bump `meta.updated` to 2026-08-02 (`.aii/config.yaml`) — commit `dc27874`

## Major

- [x] ✓ Cross-cutting documentation-system pass: verified every external link in the repo (35 unique URLs, live HTTP checks), made all docs mutually consistent (README ↔ syllabus ↔ CONTRIBUTING ↔ CITATION.cff ↔ LICENSE ↔ sidecar), and added a review TODO/log convention for future passes (see `REVIEW_LOG_2026-08-02.md`) — commits `7041baf`…`6142e53`

## Additions

### 2026-11-01 — GNN materials for the Connections unit

- [x] ✓ Add `gnn/` (README, walk-through, model specification) and link it as item 4 of the *Map the model* activity in `IntroAdventureSyllabus.md`; list it in `README.md` and align the InstituteOS sidecar artifacts and `meta.updated`.
- [x] ✓ Rename the walk-through to `gnn/map_the_model.template.md` (the GNN pipeline's `*.template.md` marker for non-model Markdown) after a directory-level run picked it up as a model and reported it invalid; a repeat run pointed at `gnn/` parses exactly one model source with no errors.
- [ ] Re-verify the GNN references in `gnn/` when the pinned revision moves: the specification was parsed and type-checked against GNN v5.0.3 (commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`), and the walk-through quotes that run's counts.
- [ ] Re-check the hand-computed posteriors in `gnn/map_the_model.template.md` if the parameterization in `gnn/learner_perception_model.md` changes.

### 2026-11-11 — modular `docs/` tree

- [x] ✓ Add `docs/README.md` as the documentation index and `docs/repository-layout.md`,
      `docs/gnn-materials.md`, and `docs/validation.md` as one-topic pages; add a
      `.github/README.md` folder guide. Link the index from `README.md` and name the docs
      locations in `AGENTS.md`.
- [ ] Keep the GNN conformance description in `docs/gnn-materials.md` in step with the
      pinned revision and CI job when either changes.

## Open / deferred

- SECURITY.md — deferred: not meaningful for a docs-only curriculum repository (no code, no security-contact surface).
- No unit-test suite — the repo is documentation only. The docs gate
  (`.github/scripts/check_docs.py`, run by `.github/workflows/docs.yml`) is the
  only executable check; it needs PyYAML and no network.
- Historical commit e02d5b5 message says "CC-BY-4.0" while the LICENSE is CC0 1.0 Universal — history cannot be rewritten; current files are consistent (LICENSE = CC0, sidecar `license: CC0-1.0`).
