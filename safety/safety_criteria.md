# Safety Criteria — Aegis-40 (40 MWe / 125 MWth iPWR)

*Source: `safety_criteria.yaml` — single source of truth. This file is auto-renderable from it.*
*Maps to FER §8.5. Cross-referenced from §8.6 (safety systems) and §8.7 (I&C trips).*
*Owner: Azamhon. Last updated: 2026-05-26.*

---

## 1. Reactivity & neutronic safety

| ID | Parameter | Limit | Type | Source | Sensor / chain | Trip |
|---|---|---|---|---|---|---|
| `k_eff_operating` | Operating k-eff | 1.000 ± 50 pcm | operating | IAEA SSR-2/1 Req 46; NRC GDC-26 | Power-range flux 4× | `high_flux_trip` |
| `shutdown_margin` | SDM (stuck-rod) | ≥ 1 % Δk/k | **hard** | NRC SRP 4.3 | Rod position + post-trip flux | — |
| `mtc_full_power` | MTC at full power | < 0 pcm/K | **hard** | NRC GDC-11 | RTD T_avg + flux | — |
| `dtc_doppler` | Doppler coefficient | < 0 pcm/K | **hard** | NRC GDC-11 | Fuel model | — |
| `void_coefficient` | Void coefficient | < 0 pcm/% void | **hard** | NRC GDC-11 | Void model + flux | — |
| `control_rod_worth_aro` | ARO integral worth | ≥ 5 % Δk/k | operating | NRC SRP 4.3 | Diff rod worth | — |
| `max_reactivity_insertion_rate` | Max ρ-insertion rate | ≤ 75 pcm/s | **hard** | ANSI/ANS-58.21 | Rod speed interlock | `high_flux_rate_trip` |

## 2. Thermal-hydraulic safety

| ID | Parameter | Limit | Type | Source | Sensor / chain | Trip |
|---|---|---|---|---|---|---|
| `mdnbr_steady` | MDNBR steady | ≥ 1.3 | **hard** | NUREG-0800 SRP 4.4 | Flow + ΔT + flux | `low_flow_trip` |
| `mdnbr_transient` | MDNBR (AOO) | ≥ 1.3 | **hard** | NUREG-0800 SRP 15.0 | Transient sim | `over_temp_dt_trip` |
| `pct_loca` | PCT LOCA | ≤ 1204 °C | **hard** | 10 CFR 50.46(b)(1) | Core exit TCs + fuel model | `high_outlet_t_trip` |
| `cladding_oxidation` | Clad ECR | ≤ 17 % | **hard** | 10 CFR 50.46(b)(2) | Fuel perf code | — |
| `hydrogen_generation` | Core-wide H₂ (Zr-H₂O) | ≤ 1 % | **hard** | 10 CFR 50.46(b)(3) | Post-LOCA inference | — |
| `fuel_centerline_temperature` | UO₂ centerline T | < 2590 °C | **hard** | NRC SRP 4.2; UO₂ T_melt | Fuel perf model | — |

## 3. Pressure boundary

| ID | Parameter | Limit | Type | Source | Sensor / chain | Trip |
|---|---|---|---|---|---|---|
| `primary_pressure_design` | Primary P (design) | ≤ 17.2 MPa | **hard** | ASME III NB | Pzr P 4× | `high_pressurizer_p_trip` |
| `containment_pressure` | Containment design P | ≤ 0.414 MPa (4.14 bar) | **hard** | FER Tbl 1; IAEA SSR-2/1 Req 56 | Cont P 4× | `high_containment_p_trip` |
| `sg_pressure_operating` | SG operating P | 7.17 MPa ± 0.2 | operating | FER Tbl 1 | SG P | — |

## 4. Decay heat removal & passive safety (iPWR USP)

| ID | Parameter | Limit | Type | Source | Sensor / chain |
|---|---|---|---|---|---|
| `operator_grace_period` | No-action grace | ≥ 72 h (target ∞ → 720 h cap) | target | IAEA SSG-39; NRC SECY-10-0034 | Passive PCCS + IRWST inventory |
| `prhr_capacity` | PRHR vs decay heat | ≥ 1.05 | **hard** | ANS-5.1 + IAEA SSR-2/1 Req 53 | PRHR HX T + flow |
| `sbf_diversity_count` | Safety-by-function principles | ≥ 5 | target | MEETING_BRIEF §4 row 10 | Design-doc audit |

**SBF approved list (count what Aegis-40 uses):** gravity, natural circulation, condensation, conduction, evaporation, capillary, pressure suppression.

## 5. Radiological & site

| ID | Parameter | Limit | Type | Source |
|---|---|---|---|---|
| `epz_radius` | EPZ radius | ≤ 0.5 km | target | FER Tbl 1; NRC RG 1.242 |
| `dose_site_boundary` | Boundary dose (LOCA 0–2 h) | ≤ 0.25 Sv TEDE | **hard** | 10 CFR 100.11 |
| `cdf` | Core damage frequency | < 1e-7 /ry | target | FER Tbl 1; NRC RG 1.174 |
| `lrf` | Large release frequency | < 1e-8 /ry | target | FER Tbl 1; NRC RG 1.174 |

## 6. Seismic / external

| ID | Parameter | Limit | Type | Source |
|---|---|---|---|---|
| `sse_design` | SSE design | ≥ 0.3 g | **hard** | FER Tbl 1; NRC RG 1.60; IAEA SSG-9 |

## 7. Fuel cycle & lifetime

| ID | Parameter | Limit | Type | Source |
|---|---|---|---|---|
| `fuel_burnup_max` | Discharge burnup (peak rod) | ≤ 62 GWd/MTU | operating | NRC SRP 4.2 |
| `fuel_enrichment_max` | Max U-235 enrichment | ≤ 5.0 wt % | **hard** | 10 CFR 50 LEU limit |
| `cycle_length` | Cycle length | ≥ 365 EFPD | target | FER Tbl 1 (12–24 mo reload) |

---

## Defense in depth (IAEA SSR-2/1 Rev 1 §2.13)

| Level | Objective | Aegis-40 features |
|---|---|---|
| 1 | Prevent abnormal operation | Negative MTC/DTC/void · MDNBR margin · HIGA self-regulating Gd₂O₃ absorber |
| 2 | Control abnormal op + detect failures | RPS 2/4 voting · AOO trip envelope · Pzr relief |
| 3 | Control design-basis accidents | Passive ECCS ×3 · PRHR / IRWST · Containment isolation ×3 |
| 4 | Severe-accident management | ≥ 72 h grace · Passive containment cooling ×3 · ≥ 5 diverse SBF principles |
| 5 | Mitigation of radiological release | EPZ ≤ 0.5 km · Boundary dose < 0.25 Sv · CDF < 1e-7, LRF < 1e-8 |

---

## Hard vs operating vs target — convention

- **hard_constraint** — breach ⇒ wFOM = −∞ ⇒ design REJECTED. Fix the design, not the formula.
- **operating_limit** — breach ⇒ scram / trip / corrective action; not a design failure.
- **target** — aspirational; contributes positively to wFOM score against CAREM-25 / SMART / VOYGR references.

Per `MEETING_BRIEF.md` §2.4, hard constraints are pass/fail, never scored.

---

## Decisions locked (2026-05-26)

| # | Item | Decision | Rationale |
|---|---|---|---|
| 1 | Cladding | **Zircaloy-4** | PWR-standard. FER Table 1 Zr-2 was illustrative. |
| 2 | Enrichment | **3-zone UO₂: 2.6/3.0/3.4 wt% U-235** (avg ~3.0 %) | Matches Samira's stable OpenMC. FER Table 1 enrichment was illustrative. |

## Open items still pending

| # | Question | Owner | By | Status |
|---|---|---|---|---|
| 3 | Operating PCT Gaussian center for FOM | OpenFOAM lead | 2026-05-29 | Waiting on OpenFOAM W1 hot-channel run |
| 4 | Containment pressure-suppression yes/no (SBF count) | Elbek / supervisor | When needed | Deferred |

---

*Total: 27 numeric safety criteria across 7 categories (17 hard constraints, 4 operating limits, 6 targets) + 5-level defense-in-depth map. Every row machine-readable in `safety_criteria.yaml`, every row links to a FOM input field, every hard constraint either has a trip or a design-by-construction note.*
