# CLAUDE.md — Aegis-40 project context

Context for any future session working in this repo. Read this first.

## What this project is

**Aegis-40** — a TEKNOFEST 2026 *Fuel & Reactor (FER)* detailed-design entry: a **40 MWe / 125 MWth soluble-boron-free natural-circulation integral PWR (iPWR)** with **cogeneration** (district heat + hydrogen), sited at **Sinop on the Turkish Black Sea coast**. The deliverable is the FER report (Chapter 8, §8.1–8.12).

This repo (`aegis-40/System-integration`) holds **one team member's scope**: **3S (Safety · Security · Safeguards), I&C, the Figure of Merit (FOM), and plant layout**. Owner: Azamhon. Other scopes live with teammates (see Ownership).

## Current design baseline — rev_4 (37-FA)

The neutronics core was re-baselined **21-FA → 37-FA** on 2026-06-26. The **simulation-independent design inputs** live in `safety/safety_criteria.yaml` under `design_basis:` (the spine). Key numbers:

- **Core:** 37 fuel assemblies, 7-wide octagon (3-5-7-7-7-5-3), 12 control-rod clusters, 17×17 lattice, 200 cm active, **9.87 tHM**.
- **Primary:** 12.8 MPa, T_avg 283 °C (design pressure 14.1 MPa).
- **Enrichment:** 3-zone 4.95/4.70/4.40 wt% + **edge-pin 3.6 wt% + ring zoning** (boron-free de-peaking), max 4.95 ≤ 5.0 LEU.
- **Burnable absorber:** Gd₂O₃ 6 wt% ×20 rods/FA (ring-zoned) + Er₂O₃ 0.5 wt% ×16.
- **Vessel:** ~10 m × Ø~3.0–3.5 m, NuScale-NPM-class natural-circulation (helical-coil SG in annulus, integral pressurizer, H_tc 4 m).

> **Discipline:** design *inputs* are locked; neutronic *results* (k_eff, coefficients, SDM, peaking, burnup, cycle) are being re-run on the 37-FA core (medium-stat done, high-stat running) and are tagged `[SIM-PENDING]` — never carry the old 21-FA result values as current.

## Locked team decisions

| ID | Decision | Status |
|---|---|---|
| C2 | Once-through Black Sea **seawater cooling** (no cooling tower) | ✅ resolved |
| C3 | **TCES** thermochemical storage (zeolite-13X) for load-following | ✅ resolved |
| C5 | **Internal IRWST pool** inside containment (CAREM-25-style) | ✅ resolved 2026-06-26 |
| — | Site = **Sinop**, Black Sea coast | ✅ |
| C1 | Two- vs three-island scheme | ⏸ open |

**Heat-sink rule (critical, often confused):** the *normal* heat sink is the seawater (non-safety); the *safety* ultimate heat sink is the **passive internal IRWST pool + containment cooling** (seawater-independent, ≥72 h). See `safety_criteria.yaml` `ultimate_heat_sink`.

## File map

- `safety/safety_criteria.yaml` — **the spine**: all numeric criteria + the `design_basis` block. Single source of truth for limits.
- `safety/SIMULATION_ANALYSIS_PLAN.md` — every sim + analysis the safety case needs, by tool, with ownership.
- `safety/{event_tree_LOHS,event_tree_SBO,trip_signals,hazards_register,regulatory_alignment_audit,safeguards_nonproliferation}.md` — safety analyses.
- `safety/openmc_rev3_alignment.md` — **historical** (21-FA), bannered superseded; kept for cross-refs.
- `ic/{ic_architecture,sensor_inventory}.md` + `ic_block.*` — I&C.
- `layout/{zones,building_list,critical_piping_table,aux_systems}.md` + `drawings/*.svg` — layout.
- `fom/` — `wfom.py` (relative ranking), `economics.py` (LCOE/NPV), `reactors/*.yaml`, `outputs/*`.
- `cad/build_aegis40_cad.py` → `*.step` (build123d venv `~/.venvs/cad`); `site/index.html` (viewer).
- `docs/` — **inputs** (read-only): `aegis40_neutronics_FER.ipynb` (Samira's OpenMC), `Aegis40_TH_report.docx` (OpenFOAM T-H), FER template, IAEA/NRC standards (`international_regulations/`), SMR booklet.
- `docs/FER_Aegis40_safety_ic_layout_draft.md` — **the consolidated FER draft** (§8.5–8.8, §8.10), current rev r5.
- `docs/FER_Aegis40_8.12_economics_draft.md` — §8.12 draft.

## Ownership / division of labor

- **Azamhon (this repo)** — 3S, I&C, FOM, layout, FER integration, and all **non-simulation** safety work (cite/bound write-ups, event-tree logic, standalone hand-analyses).
- **Samira** — neutronics OpenMC (`docs/aegis40_neutronics_FER.ipynb` + `docs/README.md` safety deck): high-stat run, N10 EBIS, N11 SFP criticality, N12 MSLB cooldown.
- **T-H contact** — OpenFOAM transients (F2 AOO, F3 SBLOCA, F5 PRHR, F6 containment). Steady-state (F1, MDNBR 1.56) + natural circulation already done (`Aegis40_TH_report.docx`).
- **Alisher** — TES/SOE/energy sizing. **Mechanical/civil teammate** — vessel mechanical design + seismic FEA.

## Conventions

- **Markers:** `[SIM-PENDING]` (awaits a run), `[ANALYSIS-PENDING]`, `[VERIFY]`, `[DECISION-PENDING]`, `[CITE/BOUND]` (substantiated by standard/reference, not run), `[EST]`, `[ALISHER]/[SAMIRA]/[ADILBEK]`.
- **Cite-don't-simulate** is policy for tools outside the team's envelope (dispersion, FRAPCON, PRA, FEA): bound against IAEA/NRC standards + by-similarity to the NRC-reviewed **NuScale NPM** (Aegis-40's core is geometrically the NPM). Always label as bounding/by-reference. See FER §8.5.4 + plan §1.C.1.
- **Non-proliferation guardrail:** once-through, boron-free, self-protecting, no separated-fissile stream. Keep all output peaceful-use.
- **Git:** work on `main` (team convention); commits end with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Push when the user asks.
- Validate YAML after edits (`python3 -c "import yaml; yaml.safe_load(...)"`); re-run `fom/wfom.py` + `fom/economics.py` after touching their inputs; rebuild CAD via the `~/.venvs/cad` python; re-render SVGs via `layout/drawings/render.sh`.
- The **PFD** `docs/aegis40_pfd.drawio.png` is a binary with no source — flag it for manual redraw, don't try to edit it.

## Where safety work stands (resume point)

See `planning/SAFETY_WORK_HANDOFF.md` for the detailed continuation state.
