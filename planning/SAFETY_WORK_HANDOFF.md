# Safety Work — Handoff / Resume Point

*Owner: Azamhon (3S). Snapshot 2026-06-26. Use this to pick safety work back up after the auxiliary-systems detour.*
*The live, detailed plan is `safety/SIMULATION_ANALYSIS_PLAN.md`; this is the short "where we are / what's next" overlay.*

## State of play

The safety case (FER §8.5–8.7) is **structurally complete and re-baselined to rev_4 (37-FA)**. Nothing in the FER is blank — every criterion is either demonstrated, in-progress in the team's own tools, or substantiated by reference.

**Done:**
- rev_4 design inputs propagated to `safety_criteria.yaml` (`design_basis`), FER draft r5, FOM.
- OpenFOAM steady-state folded in: **MDNBR 1.56, fuel 734 °C, natural circulation** (`Aegis40_TH_report.docx`).
- FER §8.6.5 — 6 simplified event trees (SBLOCA, MSLB, ATWS, SGTR, fuel-handling, marine-intake).
- FER §8.7 — trip setpoint table + response-time budget (≤500 ms closed).
- FER §8.5.4 — **cite/bound** substantiation (fuel, dose/EPZ, PRA, seismic, decay heat) by standards + NuScale similarity.
- **C5 resolved** — internal IRWST pool (CAREM-style); FER §8.6.2 + containment criteria updated; graphics recut (37-FA vessel + pool).
- Two shutdown systems (rods + EBIS) documented; ATWS path complete.

## What's running elsewhere (fold results in when they land)

| Item | Owner | When it lands, update… |
|---|---|---|
| High-stat OpenMC (k_eff, MTC/DTC/void, SDM, ARO, **peaking F_Q/F_ΔH**, burnup, cycle) | Samira | `safety_criteria.yaml` result notes + FER Table 8.5-1 (replace `[SIM-PENDING]`); **confirm F_Q≈2.0 closes the F1↔N6 coupling** that underwrites MDNBR 1.56 |
| N10 EBIS boron sizing | Samira | `independent_shutdown_systems` §6.10 claim; EBIS tank volume → `building_list.md` |
| N11 SFP-rack criticality | Samira | §8.8.6 fuel-handling; SFP rack design |
| N12 MSLB cooldown | Samira | §8.6.5b MSLB row (return-to-power) |
| OpenFOAM F2/F3/F5/F6 (transient MDNBR, SBLOCA PCT, PRHR grace, containment P/T) | T-H contact | `mdnbr_transient`, `pct_loca`, `prhr_capacity`/`operator_grace_period`, `containment_pressure` |

## What's still OURS to do (3S, non-simulation — pick up here)

1. **B9 — Tritium permeation/carryover budget** (SOE Req 35 interface): mass-transport hand-calc → bound H₂-product + district-heat dose pathway; sizes the permeation-barrier coating + getter. `aux_systems.md §9a` flags it.
2. **B10 — Setpoint-uncertainty roll-up** (ISA-67.04): combine the `sensor_inventory.md` accuracies into total channel uncertainty per trip; closes the §8.7.2 note.
3. **B11 — EDG battery-vs-72h-grace sizing**: confirm the 1E battery duty covers the gap to passive self-sufficiency.
4. **B8 — Coastal DBFL number** (Sinop): needs a site flood/surge study (not a reactor sim) → closes `coastal_external_hazard`.
5. **Containment P/T for the internal-pool concept** — coordinate with the T-H contact (F6) now that C5 is the suppression/condensing-pool case.
6. **DEC-A demonstrations** — quantitative sequence demos to back the §8.5.1a framework (ties to the event-tree completion).

## Watch-outs

- **F1↔N6 coupling:** the MDNBR 1.56 PASS used the *de-peaked design-target* peaking (F_Q 2.00); it is **contingent** on Samira's high-stat confirming it. If high-stat returns higher, MDNBR must be recomputed. This is the single most important open dependency.
- **Path mismatch:** Samira's `docs/README.md` links `docs/competition/SIMULATION_ANALYSIS_PLAN.md`; the file is at `safety/SIMULATION_ANALYSIS_PLAN.md`. Her link needs fixing (her file).
- **PFD redraw** (`docs/aegis40_pfd.drawio.png`) — binary, no source; still shows old cooling/storage/vessel. Manual draw.io job, flagged in `fer_8810_docx_audit.md`.
- **Cite/bound honesty:** every §8.5.4 claim must stay labelled *bounded-by* / *by-similarity*, never as a plant-specific calculation.

## FER draft status

`docs/FER_Aegis40_safety_ic_layout_draft.md` (r5) covers §8.5–8.8, §8.10. Adjacent sections (§8.1–8.4, §8.9, §8.11, §8.12) are notes + the separate §8.12 economics draft. Remaining FER writing: §8.9 (energy conversion, Alisher's data) and full §8.2/8.3 (Samira's core/fuel) when those land.
