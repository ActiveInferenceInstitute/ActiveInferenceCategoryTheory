# TO-DO — ActiveInferenceCategoryTheory docs-deep review

Last reviewed: 2026-11-12

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
- [x] ✓ Close the GNN checker fail-open in `.github/scripts/check_gnn.py`: `GNNTypeChecker.validate_gnn_files` returns `True` (all files valid), `2` (invalid files or no files found) or `False` (hard failure), and the old truthiness test let `2` pass. The job now calls it with `strict=True`, requires `is True`, prints the returned value as `type-checker-result`, and passes `is_content=True` to `validate_gnn_syntax`. `check_gnn.py` and `setup_gate.py` also validate the pin record (repository, tag shape, 40-hex revision) before use. The 22-format, 0-warning, 21-parameter counts come from the manual full-pipeline command, not from this job.
- [ ] Re-verify the GNN references in `gnn/` when the pinned revision moves: the specification was parsed and type-checked against GNN v5.0.3 (commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`), and the walk-through quotes that run's counts.
- [ ] Re-check the hand-computed posteriors in `gnn/map_the_model.template.md` if the parameterization in `gnn/learner_perception_model.md` changes.

### 2026-11-11 — modular `docs/` tree

- [x] ✓ Add `docs/README.md` as the documentation index and `docs/repository-layout.md`,
      `docs/gnn-materials.md`, and `docs/validation.md` as one-topic pages; add a
      `.github/README.md` folder guide. Link the index from `README.md` and name the docs
      locations in `AGENTS.md`.
- [ ] Keep the GNN conformance description in `docs/gnn-materials.md` in step with the
      pinned revision and CI job when either changes.

### 2026-11-12 — one gate entry point, one CI job, generated measurements

- [x] ✓ Add `run.sh` as the single entry point with separately runnable arms
      (`docs`, `links`, `metadata`, `index`, `gnn`, `setup`, `all`, `measure`);
      split the GNN conformance heredoc out of the workflow into
      `.github/scripts/check_gnn.py` and provisioning into
      `.github/scripts/setup_gate.py`.
- [x] ✓ Collapse the two CI jobs into one (`gate`, displayed `docs gate`): one
      checkout, one `setup-python-uv` interpreter, one virtual environment, and
      one install from `.github/requirements-gate.txt`, which also stops the
      conformance job from resolving `pyyaml` 6.0.3 while the documentation job
      pinned 6.0.2.
- [x] ✓ Add `docs/documentation-index.md` (flat index, enforced by the new
      `index` arm), `docs/run-guide.md` (arms and what CI runs), and
      `docs/arm-runtimes.md` (generated by `./run.sh measure`).

### 2026-11-12 — canonical GNN pin, shared interpreter, Education contract

- [x] ✓ Replace the pin heredoc with the canonical GNN importer pin
      `.github/gnn-pin.json` (schema `gnn-importer-pin/v1`, tag `v5.0.3`,
      revision `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`); `./run.sh gnn` now
      asserts the installed `gnn.__version__` equals the pin's tag before it
      parses the model — commit `1a279e5`, PR #9.
- [x] ✓ Take the interpreter from the shared `setup-python-uv` composite action
      instead of provisioning it inline in the workflow — commit `d59fb80`,
      PR #8.
- [x] ✓ Adopt the Education workflow contract: `education-contract.json`, the
      unchanged canonical `specs/education/schema.json`, and
      `specs/education/category-theory.json` (7 units transcribed from the
      syllabus sections and the GNN *Map the model* activity), with the
      adoption rationale and the deliberate empty `prerequisite_edges` and
      `glossary` recorded in `README.md` — commit `3efaf8f`, PR #12.
- [ ] `specs/education/category-theory.json` has no validator in this
      repository: `./run.sh` has no `education` arm and CI never reads the
      bundle, so `README.md` instead asks the reader to run
      `../courses/software/scripts/check_education_contract.py` from a sibling
      checkout that is not vendored here. Owner: the `courses` lead repository
      (or InstituteOS) must publish a pinned checker; only then can an
      `education` arm and a `gate` step be added.
- [ ] The pin trails the estate cutover: this repository pins `v5.0.3`
      (`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`) while the cutover pin is
      `v5.1.0` (`75c834bd8519dc7b5adc4d24f16bf393cfd1ecdf`, as recorded in the
      sibling `AEOS/.github/gnn-pin.json`). Bumping is a maintainer edit to
      `.github/gnn-pin.json` plus a local `./run.sh setup && ./run.sh gnn`,
      because GitHub Actions is billing-locked org-wide; the parse counts,
      serialized-format count, and parameter total quoted in `gnn/README.md`,
      `gnn/map_the_model.template.md`, `docs/gnn-materials.md`,
      `.github/GNN.md`, `.github/README.md`, and `.aii/config.yaml` must be
      re-measured against the new parser in the same change.
- [ ] `specs/` and `education-contract.json` are absent from the tables in
      `docs/repository-layout.md` and from `docs/README.md`; the `index` arm
      covers Markdown only, so it does not report the gap. Owner: documentation
      maintainer, in the next layout edit.

### 2026-11-12 — regression test for the checker contract, pin validated first

- [x] ✓ Add `./run.sh tests` (CI step `gate unit tests (hermetic)`):
      `.github/scripts/tests/test_check_gnn.py` drives `check_gnn.py` through all
      three documented type-checker outcomes with the `gnn` modules stubbed, so
      `True` must pass, and `2` or `False` must fail the arm. It needs no wheel
      and no network, and every case fails against the pre-fix truthiness test.
- [x] ✓ `setup_gate.py` now validates `.github/gnn-pin.json` before it installs
      anything; previously a malformed pin record surfaced as a `pip` failure
      traceback. `docs/gnn-materials.md` states the actual order for both
      scripts.

## Open / deferred

- SECURITY.md — deferred: not meaningful for a docs-only curriculum repository (no code, no security-contact surface).
- Unit tests cover the gate scripts, not the content: `./run.sh tests` is
  hermetic and stubs the parser. Everything else is checked by the arms of
  [`run.sh`](run.sh) (`docs`, `links`, `metadata`, `index`, `gnn`), run by
  `.github/workflows/docs.yml` as one job; the offline arms need PyYAML and no
  network.
- Historical commit e02d5b5 message says "CC-BY-4.0" while the LICENSE is CC0 1.0 Universal — history cannot be rewritten; current files are consistent (LICENSE = CC0, sidecar `license: CC0-1.0`).
