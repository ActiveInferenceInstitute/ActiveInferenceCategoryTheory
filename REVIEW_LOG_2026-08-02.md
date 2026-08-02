# REVIEW LOG — 2026-08-02

Docs-deep review pass for ActiveInferenceCategoryTheory (public submodule of ActiveInferenceInstitute).

## Phase 0 — Preflight

- Default branch: main (origin/main via `git symbolic-ref --short refs/remotes/origin/HEAD`).
- HEAD at start: e02d5b5 "add .aii sidecar (100% complete) + CC-BY-4.0 LICENSE (InstituteOS metadata)".
- Working tree clean at start; repo is a git submodule (`.git` is a gitdir pointer file).
- Inventory (all tracked files):
  - README.md (6 lines — minimal)
  - IntroAdventureSyllabus.md (229 lines — the main curriculum document)
  - LICENSE (CC0 1.0 Universal full legal text)
  - .aii/config.yaml (InstituteOS sidecar metadata)
- No docs/ folder, no AGENTS.md/CLAUDE.md, no CI (.github/), no test suite, no existing TODO file.
- Repo history: created 2023-05-12 ("Initial commit"), renamed IntroCTonActInfSyllabus → IntroSyllabus → IntroAdventureSyllabus.

## Phase 1 — Mega-deep docs review: findings

### Accuracy / links (verified by live HTTP checks of all 35 unique external URLs, 2026-08-02)
- 404: https://www.activeinference.org/education/textbook-group — textbook-group sign-up page is gone (checked /education and variants). Replace anchor with the live https://www.activeinference.org/education page.
- 410 Gone, no Wayback snapshot: https://jrlearnstomath.wordpress.com/ — blog no longer online. Reword Encouragement section, drop dead link.
- Tracking fragment on Zenodo link (https://zenodo.org/record/7803328#.ZFo4js5Bzb00): canonicalize to https://zenodo.org/records/7803328 (record verified via extraction; the paper title "Generalized Notation Notation for Active Inference Models" is genuinely the published title — do NOT "fix").
- http://twitter.com/InferenceActive → https:// (bot-blocked 520 via curl but canonical https URL is correct).
- 403s (math.jhu.edu Riehl page, tandfonline, zenodo via curl): bot-blocks on real, canonical resources — left unchanged.
- License consistency: LICENSE file = CC0 1.0 Universal; .aii/config.yaml `license: CC0-1.0` — consistent. (Historical commit message e02d5b5 says "CC-BY-4.0" — cannot rewrite history; noted, no action.)

### Typos / grammar (IntroAdventureSyllabus.md)
- "skteching" → "sketching"; "there wil be" → "there will be"; "intution" → "intuition"; "Kleisi category" → "Kleisli category"; "higher catgory theory" → "higher category theory"; "Modelstream" → "ModelStream" (consistency with line 159); "Github" → "GitHub"; "right and a finite time" → "right, and a finite time"; missing space after "--" (2×) → em dash; "bound,variational" → "bound, variational"; stray ")" in Roman YouTube link; "p. 416-416" → "p. 416"; "co-founded the Topos Institute since" → "since then".

### Formatting / structure
- 5 lines with trailing whitespace (README.md:6, syllabus 19/53/79/119).
- Heading levels inconsistent: 6× H1 in one document; "**Notes**" is bold text, not a heading.
- No table of contents in a 229-line curriculum document (GitHub auto-TOC exists but a compact contents list aids navigation).
- README is a 6-line stub: no repository contents, no license pointer, no citation info, dangling trailing space.

### Metadata
- .aii/config.yaml `artifacts` lists only README.md and LICENSE — the main content document (IntroAdventureSyllabus.md) is missing; no CONTRIBUTING/CITATION artifacts yet.
- No CONTRIBUTING.md (syllabus invites contributions but gives no channel/process doc), no CITATION.cff (GitHub "cite this repository" metadata).

### Not applicable / deferred
- No code, no tests, no CI in this repo — nothing to run; docs-only pass.
- SECURITY.md: not meaningful for a docs-only curriculum repo — deferred with reason.

## Phase 3 — Implementation log

All items implemented and committed on `main` (branch: main):

1. `7041baf` docs: polish IntroAdventureSyllabus — fix typos, dead links, and heading structure
2. `b0ac3e5` docs: expand README with contents, license, and citation info
3. `83f3932` docs: add contributing guide and citation metadata (CONTRIBUTING.md, CITATION.cff)
4. `dc27874` chore: align InstituteOS sidecar artifacts with repository contents (.aii/config.yaml)
5. `6142e53` docs: add review TODO and log for docs-deep pass (TO-DO.md, REVIEW_LOG)

Verification notes:
- The paper title "Generalized Notation Notation for Active Inference Models" was verified on Zenodo — it is the real published title, so the "Notation Notation" text was deliberately left unchanged.
- Replacement links verified: https://www.activeinference.org/education renders (Firecrawl); https://zenodo.org/records/7803328 resolves (Firecrawl; curl is bot-blocked); old textbook-group sign-up URL fails to render → replaced.
- 403s from curl on math.jhu.edu, tandfonline, zenodo are bot-blocks on real resources — left unchanged.
- No code, tests, or CI exist in this repo — nothing to run; docs-only pass.

## Phase 4 — Final verification

- Final sweeps: heading structure (single H1, H2/H3 hierarchy), TOC anchors match GitHub slugs, no trailing whitespace, YAML validity (sidecar via linter, CITATION.cff via ruby YAML parse), leftover-typo grep clean, git status contains only intended files.
- 6 commits total on main (5 feature + 1 log finalize); pushed to origin/main; working tree clean.
