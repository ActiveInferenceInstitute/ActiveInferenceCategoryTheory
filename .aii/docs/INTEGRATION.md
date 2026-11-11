# InstituteOS integration — ActiveInferenceCategoryTheory

## Identity

| Field | Value |
| --- | --- |
| Repository | `ActiveInferenceInstitute/ActiveInferenceCategoryTheory` |
| Affiliation | `institute` |
| Category | `education` |
| Status | `active` |
| Maturity | `released` |
| Steward | Active Inference Institute |
| Default branch | `main` |
| Current release | — |
| License | `CC0-1.0` |
| Citation | Active Inference Institute — ActiveInferenceCategoryTheory. |

## Federation

| Setting | Value |
| --- | --- |
| Dashboard mode | `repos` |
| Analytics | `true` |
| Dashboard | `true` |
| Sync policy | `pull` |
| Registries | — |
| Tags | active-inference, category-theory, education, curriculum |

## Ecosystem relations

| Repository | Relation | Note |
| --- | --- | --- |
| `ActiveInferenceInstitute/InstituteOS` | `referenced-by` | Federated via the InstituteOS .aii manifest. |
| `ActiveInferenceInstitute/Active_Inference_Ontology` | `references` | Uses Active Inference Ontology terms. |
| `ActiveInferenceInstitute/Generalized_Notation_Notation` | `references` | Uses Generalized Notation Notation (GNN) for model specifications. |

## Key artifacts

| Path | Kind | Description |
| --- | --- | --- |
| `README.md` | `doc` | Repository overview. |
| `IntroAdventureSyllabus.md` | `doc` | Adventure-mode curriculum for category theory applied to active inference. |
| `gnn/README.md` | `doc` | GNN materials for the Map the model activity. |
| `gnn/map_the_model.template.md` | `doc` | Walk-through mapping category-theoretic notions onto a GNN model specification. |
| `gnn/learner_perception_model.md` | `doc` | Two-state GNN perception model of the reader, parsed and type-checked against GNN v5.0.3. |
| `CONTRIBUTING.md` | `doc` | Contribution guide. |
| `CITATION.cff` | `citation` | Machine-readable citation metadata. |
| `LICENSE` | `doc` | License. |
| `AGENTS.md` | `doc` | Agent guidance. |

## Portable tasks

| Task | Command | Working directory | Description |
| --- | --- | --- | --- |
| `inventory` | `git ls-files` | `.` | List tracked files. |

## Validation

```bash
python -m aii_platform.aii_sidecar.validate <repo> --completeness
python -m aii_platform.aii_sidecar docs <repo> --overwrite
python -m aii_platform.aii_sidecar.run <repo> --list
```

The sidecar is valid when `validate` prints `OK` and reports no missing artifact,
manifest, link, or declared-doc path. Completeness is a curation target, not a
runtime requirement.

## Data boundary

This sidecar carries metadata only. It does not grant execution permission, does not
replace the repository's own documentation, and must not be used to move private
content into a public repository. Task execution is limited to trusted checkouts.
