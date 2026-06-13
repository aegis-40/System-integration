# Working-file inventory — 3 weeks (2026-05-26 → 2026-06-13)

*Everything produced or worked in the System-integration scope, grouped by FER mapping.
Commit timeline: W1+W2 batch (`1afe439`), rev_3 sync (`3097515`), W3 drawings
(`751bad9`, `1d6ea87`), viewer (`a24b893`, `1f6deda`), safeguards (`c39a455`),
layout r2 + CAD + drawio (`e0d372b`), CRDM/SBO/audit (`b6b1506`).*

## FER §8.5 — Safety criteria (W1)
| File | What |
|---|---|
| `safety/safety_criteria.yaml` | **Source of truth** — 27 criteria (17 hard / 4 operating / 6 target), 7 categories, DiD-mapped, FOM-linked |
| `safety/safety_criteria.md` | Human render of the YAML |
| `safety/openmc_rev3_alignment.md` | rev_3 ↔ criteria cross-check: 10/10 neutronic gates PASS; CRDM=internal resolved (§4) |

## FER §8.6 — Safety systems & accident analysis (W1 + 2026-06-13)
| File | What |
|---|---|
| `safety/trip_signals.md` | 13 RPS trips + 5 ESF actuations + 4 permissives, each tied to a criteria row |
| `safety/event_tree_LOHS.md` + `.png` + `.drawio` | Lead event tree — 7 sequences, CDF ~1e-8/ry |
| `safety/event_tree_SBO.md` + `.drawio` | Second tree — 5 sequences, CDF ~1e-11/ry (de-energize-to-actuate showcase) |

## FER §3S — Safeguards (2026-06-09)
| File | What |
|---|---|
| `safety/safeguards_nonproliferation.md` | Reactor-grade, self-protecting, once-through discharge case |
| `docs/safeguards_attractiveness.md` + `docs/pu_vector.csv` | Samira's source analysis (rev_3 depletion) |

## FER §8.7 — I&C (W1)
| File | What |
|---|---|
| `ic/ic_architecture.md` | 6 principles, 5 layers + DAS, HMI/MCR, cyber, EQ, full standards list |
| `ic/sensor_inventory.md` | 21 channels (14 Class 1E) + 5 planned |
| `ic/ic_block.mmd` + `.png` + `.drawio` | Block diagram (5 layers + DAS + data diode) |
| `ic/fer_8_7_coverage.md` | Line-by-line §8.7 coverage: 20✓ / 5△ / 0✗ |

## FER §8.8 + §8.10 — Layout & aux (W2/W3 + r2)
| File | What |
|---|---|
| `layout/zones.md` | Three-island zoning, decisions Z1–Z7 (Z6→seawater 2026-06-13; Z7 TB-adjacent r2) |
| `layout/building_list.md` | 14 buildings + 5 infra, footprints, seismic class |
| `layout/aux_systems.md` | 8 auxiliary systems, six-field metadata |
| `layout/block_layout.mmd/png`, `flow_arrows.mmd/png` | Schematic block + process-flow diagrams |
| `layout/drawings/` (4 × svg+png + `render.sh`) | Scaled drawings: site plot r2, RXB plan, elevation, MCR |
| `layout/critical_piping_table.md` | R6 table — DNs from FER draft `[FER-DRAFT]` |
| `layout/fer_8_10_coverage.md` | §8.10/§8.8 requirement audit |
| `layout/fer_8810_docx_audit.md` | FER-draft ↔ repo reconciliation (C1–C7; C2 resolved, C3 deliberating, C5 open) |
| `site/index.html` + `site/README.md` | Interactive 5-view layout viewer (classic white) |
| `cad/aegis40_site.step`, `cad/aegis40_rxb.step`, `cad/build_aegis40_cad.py`, `cad/README.md` | Fusion 360 CAD — full site + RXB diorama (§8.10 R4) |

## Inputs / references (docs/)
`FER_Template.docx` · `FER_Aegis40_8.8-8.10.docx` (team draft) · `aegis40_pfd.drawio.png`
(integrated PFD — **needs CT-1 → seawater update**) · `PER_NUClearly.pdf` · `CAREM report.pdf` ·
`IV.5-KenLangdon-NuScale.pdf` · `SMR_booklet.pdf` · `tasks_w1.pdf` · `Aegis-40 2D test/`
(Samira's OpenMC working copy; heavy outputs gitignored) · sibling repo `../aegis-40-OpenMC` (rev_3 basis)

## Process / planning
`planning/`: TASK_PROCESS, W1/W2/W3 plans, PLAN.md (FOM tool, unstarted), MEETING_BRIEF,
SIMULATION_REQUIREMENTS, SESSION_LOG_2026-06-08, briefings/ (MB_D1, MB_D3, MB_W1,
MB_W2_Layout, MB_Progress_2026-06-05), FILES_3WEEKS.md (this file)
