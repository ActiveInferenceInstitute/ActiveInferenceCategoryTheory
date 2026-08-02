# TO-DO — ActiveInferenceCategoryTheory docs-deep review

Last reviewed: 2026-08-02

Findings from the docs-deep review pass, scoped by severity:

- **Minor** = typo, broken link, formatting issue.
- **Medium** = stale section rewrite, doc restructure, added missing guide.
- **Major** = large doc-system overhaul / cross-cutting refactor.

## Minor

- [x] ✓ Fix typos in IntroAdventureSyllabus.md: "skteching", "there wil", "intution", "Kleisi", "catgory", "Modelstream"→"ModelStream", "Github"→"GitHub", missing comma after "right", missing space after "--" (2×), "bound,variational" (`IntroAdventureSyllabus.md`)
- [x] ✓ Fix "p. 416-416" → "p. 416" and "co-founded the Topos Institute since" → "since then" (`IntroAdventureSyllabus.md`)
- [x] ✓ Remove stray ")" in the Roman "Course: Category Theory" YouTube link (`IntroAdventureSyllabus.md`)
- [x] ✓ Replace dead links: Zenodo tracking fragment → canonical `https://zenodo.org/records/7803328`; twitter http→https; textbook-group sign-up 404 → live Institute education page; jrlearnstomath blog (410, never archived) → reworded, link dropped (`IntroAdventureSyllabus.md`)
- [x] ✓ Remove trailing whitespace on 5 lines (README.md, IntroAdventureSyllabus.md lines 19/53/79/119)

## Medium

- [x] ✓ Expand README from a 6-line stub: repository contents, license clarity (CC0 1.0), citation line, cross-links (`README.md`)
- [x] ✓ Normalize heading hierarchy (single H1; Course Information / Topics and Sections / Other Resources / Encouragement / Thanks as H2; subsections H3; "**Notes**" → "### Notes") and add a compact contents list (`IntroAdventureSyllabus.md`)
- [x] ✓ Add CONTRIBUTING.md: contribution channels (issues/PRs, Discord, X), verification guidelines, CC0 dedication note — grounded in the syllabus's own invitation (`CONTRIBUTING.md`)
- [x] ✓ Add CITATION.cff with Institute attribution, CC0-1.0 license, release date from repo history (2023-05-12) (`CITATION.cff`)
- [x] ✓ Align InstituteOS sidecar: add IntroAdventureSyllabus.md / CONTRIBUTING.md / CITATION.cff to `artifacts`, bump `meta.updated` to 2026-08-02 (`.aii/config.yaml`)

## Major

- [x] ✓ Cross-cutting documentation-system pass: verified every external link in the repo (35 unique URLs, live HTTP checks), made all docs mutually consistent (README ↔ syllabus ↔ CONTRIBUTING ↔ CITATION.cff ↔ LICENSE ↔ sidecar), and added a review TODO/log convention for future passes (see `REVIEW_LOG_2026-08-02.md`)

## Open / deferred

- SECURITY.md — deferred: not meaningful for a docs-only curriculum repository (no code, no security-contact surface).
- No test suite / CI to run — repo contains documentation only; nothing to execute.
- Historical commit e02d5b5 message says "CC-BY-4.0" while the LICENSE is CC0 1.0 Universal — history cannot be rewritten; current files are consistent (LICENSE = CC0, sidecar `license: CC0-1.0`).
