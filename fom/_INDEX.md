# fom/ — Figure of Merit (cross-cutting integration)

Implemented 2026-06-15 (focused build of `planning/PLAN.md` §5). Run `python3 fom/wfom.py`.

| File | What it is |
|---|---|
| `README.md` | wFOM definition, absolute-utility property, results, validation methods, caveats |
| `parameters_schema.yaml` | 5 categories × params: normalizers, directions/targets, hard limits, **default weights** |
| `economic_assumptions.yaml` | market prices for specific-revenue (defaults pending supervisor) |
| `reactors/aegis40.yaml` | Aegis-40 rev_3 data (confirmed where from our sims/docs) |
| `reactors/{carem25,smart,nuscale_voygr}.yaml` | reference data — sourced from IAEA SMR booklet (docs/SMR_booklet.pdf), 2026-06-15 |
| `wfom.py` | engine: derive → normalize → wFOM + absolute-utility ranking + validation + TOPSIS + transparency |
| `outputs/wfom_report.md` | generated report |

Also: `reactors/standards.yaml` (absolute international-standard targets), `ahp/category_pairwise.yaml` (AHP weights, CR check).

**Headline (booklet data):** **NuScale > Aegis-40 > CAREM > SMART** — robust under wFOM,
TOPSIS, and AHP weights (CR=0.002). Aegis-40 a solid #2 (→#1 only if Safety dropped).
Absolute-vs-standards (§3b): only NuScale beats the benchmark; Aegis-40 −0.18. Safety
fixed 2026-06-15 (added booklet `seismic_sse` + `primary_circulation`; `n_active` weight
0.35→0.11). As-run peaking trips the hard gate → de-peak target used.

**Open:** AHP weight elicitation, MC sensitivity bands, parameter-uncertainty propagation,
neutral-weight check, and **verifying reference data** (`planning/PLAN.md` §6–7, §1.2).
Cross-refs: `safety/safety_criteria.yaml` (`fom_param` fields), `planning/PLAN.md`.
