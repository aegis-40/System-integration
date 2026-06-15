# Regulatory Alignment Audit — Aegis-40 vs International Standards

*Owner: Azamhon (3S/I&C). Date: 2026-06-15.*
*Scope: cross-check of every Aegis-40 safety/I&C/layout design document against the four
international standards added to `docs/international_regulations/`.*

## Standards audited

| Repo file | Standard | Role |
|---|---|---|
| `Safety of NPP.pdf` | **IAEA SSR-2/1 (Rev. 1)** — Safety of NPP: Design | Master design-requirements set (82 Requirements) |
| `IAEA.pdf` + `Design of the  Core.pdf` | **IAEA SSG-52** — Design of the Reactor Core | Core-design guidance (peaking, SDM, coefficients) |
| `Safety Requirements SMR.pdf` | **IAEA TECDOC-1936** — Applicability of Design Safety Requirements to SMRs | Graded application of SSR-2/1 to SMRs |
| `NRC spec.pdf` | **NUREG-1431 (Rev. 5)** — Standard Technical Specifications, Westinghouse | Source of the LCO peaking/RPS setpoints |

*(Filenames are scrambled vs content; identities above verified by `pdftotext`. Two copies of SSG-52 are present.)*

## Files cross-checked

`safety/safety_criteria.{yaml,md}`, `safety/trip_signals.md`, `safety/event_tree_{LOHS,SBO}.md`,
`safety/safeguards_nonproliferation.md`, `safety/openmc_rev3_alignment.md`,
`ic/ic_architecture.md`, `ic/sensor_inventory.md`, `ic/fer_8_7_coverage.md`,
`layout/aux_systems.md`, `layout/building_list.md`, `layout/zones.md`,
`docs/FER_Aegis40_8.5-8.7_draft.md`, plus the OpenMC repo `summary_report.txt` / notebook.

---

## 1. Findings — gaps & partials (action required)

*Status below reflects the 2026-06-15 implementation pass that resolved A/B/C and set the path for D.*

| # | Standard clause | Requirement (paraphrase) | Status after implementation |
|---|---|---|---|
| **A** | **SSR-2/1 Req 46 §6.9–6.10** | ≥2 diverse & independent shutdown systems; ≥1 alone subcritical; §6.8 CCF of insertion. | **RESOLVED (design).** Added **EBIS** — passive, diverse, shutdown-only borated-water system, DAS-armed (`trip_signals.md` E6, `ic_architecture.md` §3.6, FER §8.6.2a). Count=2; SBF kept (no operational boron). *Pending:* §6.10 boron-mass sizing (OpenMC). |
| **B** | **SSR-2/1 Req 35** | No radionuclide transport to district-heating / H₂ units, operational + accident. | **RESOLVED (design).** Added cogen interface isolation (`aux_systems.md` §9a): 3 barriers (SG tube + intermediate loop + customer HX), inward ΔP, ESFAS auto-isolation. *Pending:* SOE tritium budget. |
| **C** | **SSR-2/1 Req 13 / 20 §5.27–5.31** | Plant-state categories incl. DEC; "practical elimination" §5.31. | **RESOLVED (framework).** Added FER §8.5.1a (AOO/DBA/DEC-A/DEC-B + deterministic practical-elimination of LBLOCA/rod-ejection/boron-dilution/surge-line). *Pending:* DEC-A sequence analyses. |
| **D** | **NUREG-1431 LCO 3.2.1/3.2.2; SSG-52 §6** | F_Q(Z) ≤ ~2.50; F_ΔH^N ≤ ~1.65. | **FLAGGED + path set.** F_q=3.478, F_ΔH=2.268 exceed; criteria `f_q_total`/`f_delta_h_radial` added. `open_item: peaking_recompute` = pin-aligned re-tally, then de-peak (IFBA + finer Gd zoning + pin enrichment grading) if real. |

**PARTIAL fixes implemented same day:** Req 5 (`occupational_collective_dose` criterion), Req 17 (`hazards_register.md`), Req 65–66 (Remote Shutdown Station, `ic_architecture.md` §4.5 + FER §8.7.5), Req 81–82 (4th monitoring layer / RG 1.97, `aux_systems.md` §4), Req 16/19 (SRP Ch.15 master PIE list, FER §8.6.3), Req 43–44 + 54–58 (`open_item`s with owners).

---

## 2. Coverage — SSR-2/1 design requirements (PASS / PARTIAL / GAP)

| Req | Topic | Status | Where / note |
|---|---|---|---|
| 4 | Fundamental safety functions | PASS | reactivity control, heat removal, confinement — `safety_criteria`, FER §8.6 |
| 5 | Radiation protection in design | RESOLVED (criterion) | `occupational_collective_dose` ≤0.5 person-Sv/yr added; ALARA features noted; collective-dose estimate [ANALYSIS-PENDING] |
| 7 | Defence in depth (5 levels) | PASS | `safety_criteria.yaml` DiD map; FER §8.5.3 |
| 8 | Safety/security/safeguards interfaces (3S) | PASS | `safeguards_nonproliferation.md`; I&C cyber §5 |
| 13 | Categories of plant states | RESOLVED | FER §8.5.1a plant-states table (Finding C) |
| 14–15 | Design basis / design limits | PASS | `safety_criteria` is the design-limit spine |
| 16 | Postulated initiating events | PARTIAL | master PIE list = SRP Ch.15 categories (FER §8.6.3); MSLB→SBLOCA analyses pending |
| 17 | Internal & external hazards | RESOLVED (register) | `hazards_register.md` — internal+external+combinations; site-dependent items PENDING |
| 19 | Design basis accidents | PARTIAL | event-tree spectrum incomplete (declared); prioritized MSLB/SBLOCA |
| 20 | Design extension conditions | RESOLVED (framework) | FER §8.5.1a DEC-A/-B + practical-elimination (Finding C) |
| 22 | Safety classification | PASS | Class 1E partition, `ic_architecture` §2; SSG-30 cited |
| 24 | Common cause failure | PASS | DAS platform diversity, `ic_architecture` §3.6 |
| 25 | Single failure criterion | PASS | 2/4 voting both directions; sequence-level in FER §8.6.4 |
| 26 | Fail-safe design | PASS | de-energize-to-trip / -actuate, `trip_signals` §1 |
| 35 | Cogeneration | RESOLVED (design) | `aux_systems.md` §9a interface isolation (Finding B); tritium budget pending |
| 43–44 | Fuel performance / core structural | PARTIAL | `open_item: fuel_core_structural` — owner assigned (mechanical/fuel) |
| 45 | Control of the core (power distribution) | FLAGGED | peaking criteria added + de-peak path (Finding D) |
| 46 | Reactor shutdown | RESOLVED (design) | EBIS = diverse system #2 (Finding A); §6.10 sizing pending |
| 47–49 | RCS design / overpressure / inventory | PASS | integral RPV, Pzr P limits + relief, SI |
| 51–53 | Residual heat removal / ECCS / ultimate heat sink | PASS | PRHR/IRWST; UHS = seawater (C2 resolved) |
| 54–58 | Containment & isolation | PARTIAL | `open_item: containment_pt_analysis` — resolve C5 then run P/T |
| 59–64 | Instrumentation / protection / control / separation | PASS | `ic_architecture` — strong; one-way isolation, DAS, computer-based per IEC 60880 |
| 65–66 | Control room / supplementary CR | RESOLVED | Remote Shutdown Station, `ic_architecture` §4.5 + FER §8.7.5 |
| 68 | Loss of off-site power | PASS | SBO event tree; de-energization = actuation |
| 80 | Fuel handling & storage | PASS | SFP in `aux_systems`; storage-criticality (OpenMC) |
| 81–82 | Radiation protection / monitoring | RESOLVED (improved) | 4th post-accident high-range layer (RG 1.97) added, `aux_systems` §4 |

---

## 3. SSG-52 (reactor core) — spot check

| Topic | SSG-52 | Aegis-40 | Status |
|---|---|---|---|
| Negative reactivity coefficients | recommended over operating range | MTC −35.9, DTC −1.84, void −214 pcm | PASS |
| Shutdown margin w/ most-reactive rod stuck | required | SDM 12.4 % | PASS |
| Power-distribution / peaking control | §6 | F_q/F_ΔH exceed limits | GAP (Finding D) |
| Control of reactivity during cycle (SBF) | burnable absorber acceptable | hybrid Gd+Er | PASS |
| Reactor shutdown systems | aligns to SSR-2/1 Req 46 | one system | GAP (Finding A) |

## 4. TECDOC-1936 (SMR applicability) — relevance

TECDOC-1936 is the lever for Findings A & C: it endorses a **graded / risk-informed**
application of SSR-2/1 to SMRs (single-failure for passive systems, EPZ sizing by source
term, control-room staffing, "practical elimination"). It is the correct vehicle to either
(a) justify a single highly-reliable diverse-actuated shutdown system, or (b) frame the
eliminated events as practically eliminated. Cite it explicitly when closing A and C.

## 5. NUREG-1431 — setpoint traceability

Source of the LCO numbers now in `safety_criteria` (F_Q 3.2.1, F_ΔH 3.2.2). Next pass:
reconcile `trip_signals.md` setpoints (OTΔT/OPΔT, P-permissives) against NUREG-1431
Section 3.3 RPS Instrumentation once OpenFOAM closes the DNB correlation.

---

## 6. Net effect on the design (after 2026-06-15 implementation)

Five new criteria added (4 hard + 1 target → 32 total: 21 hard / 4 op / 7 target).
Findings A, B resolved by design (EBIS shutdown system #2; cogen interface isolation),
C resolved by framework (DEC + practical elimination). Of the new hard constraints, only
the **peaking pair (D)** still shows FAIL on as-run inputs — and that is plausibly a
RegularMesh tally artifact pending a pin-aligned re-tally; a de-peak path (IFBA + Gd
zoning + enrichment grading) is set if it proves real.

PARTIALs cleared: Req 5, 13, 17, 20, 65–66, 81–82. Remaining PARTIAL/PENDING (with owners,
tracked as `open_items`): peaking re-tally (`peaking_recompute`), EBIS boron sizing
(`shutdown_second_system`), SOE tritium budget (`cogen_isolation_design`), DEC-A analyses
(`dec_plant_states`), fuel/core structural (`fuel_core_structural`), containment P/T after
C5 (`containment_pt_analysis`), and the SRP Ch.15 event-tree completion (FER §8.6.3).

**Net:** no concept-fatal finding. The single remaining hard FAIL (peaking) is on the
W-freeze critical path because it also gates MDNBR and LOCA PCT — resolve the re-tally
first.
