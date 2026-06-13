# OpenMC rev_3 ↔ Safety Criteria Alignment Check

*Cross-check of Samira's locked neutronics design (`aegis-40/OpenMC`, rev_3, 2026-06-03, OpenMC 0.15.3) against this repo's W1 safety criteria and locked decisions.*
*Run by Azamhon, 2026-06-08. Source repo cloned to `../aegis-40-OpenMC` (sibling, not vendored).*

---

## 0. Verdict

**Samira's rev_3 core PASSES all 10 of the neutronic/fuel safety gates in `safety_criteria.yaml`.** Six of those gates were `[SIM-PENDING]` placeholders in W1 — they now have real, passing values.

**But:** two of this repo's "locked decisions" are now **factually superseded** by rev_3 (enrichment, burnable absorber), and several `safety_criteria.yaml` notes are stale. These are documentation drift, not safety failures — corrected in §3.

The one big W1 open item — **fuel-assembly count (21 vs 240)** — is **resolved: 21 FAs**.

---

## 1. Gate-by-gate — all PASS

| `safety_criteria.yaml` row | Type | My limit | rev_3 as-run | Verdict |
|---|---|---|---|---|
| `shutdown_margin` | hard | ≥ 1.0 %Δk/k | **12.4 %** | ✅ huge margin |
| `mtc_full_power` | hard | < 0 | **−35.9 pcm/K** | ✅ |
| `dtc_doppler` | hard | < 0 | **−1.84 pcm/K** | ✅ |
| `void_coefficient` | hard | < 0 | **−214 pcm/%void** | ✅ |
| `control_rod_worth_aro` | operating | ≥ 5 000 pcm | **15 226 pcm** | ✅ |
| `max_reactivity_insertion_rate` | hard | ≤ 7.5e-4 Δk/k/s | **1.5e-5** | ✅ (see §4 CRDM) |
| `fuel_burnup_max` | operating | ≤ 62 GWd/MTU | **42.8** | ✅ |
| `fuel_enrichment_max` | hard | ≤ 5.0 wt% | **4.95** | ⚠️ pass but at the edge |
| `cycle_length` | target | ≥ 365 EFPD | **479 EFPD** | ✅ exceeds |
| `k_eff_operating` | operating | ~1.0 (controlled) | BOL excess **+2640 pcm** | ℹ️ held by BA+rods |

**6 rows that were `[SIM-PENDING]` in W1 now have confirmed values:** MTC, DTC, void, ARO worth, shutdown margin, max insertion rate. The safety spine is no longer a table of asserted limits — the margins are demonstrated.

Two watch items even though they pass:
- **Enrichment 4.95 wt% leaves only 0.05 wt% to the 5.0 % LEU ceiling.** A judge will note you sit at the very edge of the commercial-LWR license limit. Defensible (deliberate, to chase burnup) but call it out in the FER rather than let them find it.
- **k_eff BOL = 1.0264** → ~2640 pcm of excess reactivity to hold down at BOL (vs the 722 pcm my old note assumed). Covered with margin: ARO worth 15 226 pcm + cold SDM 12.4 %. Confirms the SBF design closes.

---

## 2. Open items resolved by rev_3

| W1 open item | Status | Resolution |
|---|---|---|
| Fuel-assembly count (21 vs 240) | ✅ **RESOLVED** | **21 FAs, 17×17 square lattice.** 21 is the real full-core count, not a 2D artifact. RXB sized for 21 FA in `layout/building_list.md` is **correct** — your compact reactor building stands. |
| Soluble-boron status | ✅ **CONFIRMED SBF** | Closes the `[OPEN]` in `trip_signals.md` §6. Consequence predicted there came true: rod-worth requirement rose, and rev_3 delivers 15 226 pcm ARO worth. DAS safety-significance argument holds. |
| MTC / DTC / void / ARO worth / SDM | ✅ **QUANTIFIED** | All negative / all above threshold (§1). |
| Cycle length | ✅ | 479 EFPD (~16 months). |
| Decay-heat source for PRHR sizing | ✅ **NEW DATA** | **7.75 MW at shutdown = 6.2 % of 125 MWth** (rigorous full-chain, cross-validates ANS-5.1). This is the number `prhr_capacity` (≥105 % decay heat) and the 72 h grace must reject. Hand to OpenFOAM/TH. |

---

## 3. Misalignments — documentation drift to fix

Two locked decisions in `README.md` + `safety_criteria.yaml` are superseded by Samira's rev_3 design-basis (she relaxed them deliberately, with a supersession note, to chase high burnup / waste-intensity score). **The neutronics owner's locked basis is authoritative — sync to it.**

| # | What's stale | Old (this repo) | rev_3 actual | Action |
|---|---|---|---|---|
| M1 | **Enrichment** | 3-zone 2.6 / 3.0 / 3.4 wt% (decision #2) | **4.95 / 4.70 / 4.40 wt%** (max 4.95) | Update README decision #2, `decisions_locked.enrichment_target`, `fuel_enrichment_max` note |
| M2 | **Burnable absorber** | "Er₂O₃ replacing Gd₂O₃" (decision #4) | **HYBRID: Gd₂O₃ 8 wt% (×32 rods) + Er₂O₃ 0.5 wt% (×16)** — Gd-dominant, Er is slow flat hold-down | Update README decision #4 + `k_eff_operating` note (drop "HIGA Gd burnout" framing) |
| M3 | **SFP "borated" wording** | `aux_systems.md` §7 says borated pool | SBF → SFP criticality credited **unborated**, k_eff(95/95) ≤ 0.95 via burnup credit + rack geometry (Cabrera 2023 method) | Fix `layout/aux_systems.md` §7 |
| M4 | **HM loading** | not stated | rev_3 internally inconsistent: 5.6 t (summary) vs 5.04 t discharge / ~5.3 t fresh (design basis) — Samira flags it herself | Samira's to resolve; affects SFP/cask sizing not core safety |

**Status after sync:** M1, M2, M3 corrected in this commit (see §6). M4 is Samira's.

---

## 4. ~~Still unresolved~~ — **RESOLVED: CRDMs are INTERNAL (in-vessel)** (confirmed 2026-06-12)

Internal/in-vessel CRDMs — the modern iPWR norm, consistent with the evidence already in rev_3 (1.5e-5 Δk/k/s = a rod-*withdrawal* transient; "9 CR clusters" = CCAs).

**Safety consequences, now claimable:**
- **Rod ejection is eliminated by design** — no head-mounted drive housing whose rupture can eject a rod. Claim as a design-basis-event **elimination credit** in FER §8.6 (alongside LB-LOCA elimination from the integral RPV).
- `max_reactivity_insertion_rate` accident basis re-based on **uncontrolled rod withdrawal** (an AOO that exists); rev_3's 1.5e-5 Δk/k/s passes with 50× margin to the 7.5e-4 limit.
- No RG 1.77 / 230 cal/g rod-ejection enthalpy analysis owed.
- RXB internal arrangement: no CRDM gallery above the head → below-grade RPV pit depth stands as drawn.

---

## 5. New rev_3 data to route to other scopes

| Datum | Value | Goes to |
|---|---|---|
| Decay heat @ shutdown | 7.75 MW (6.2 % of 125 MWth) | OpenFOAM/TH → `prhr_capacity`, 72 h grace |
| 3D peaking F_q | 3.48 (F_ΔH 2.27, F_z 1.03) | OpenFOAM → `mdnbr_steady/transient` hot-channel |
| Discharge source term | 1.2e17 Bq (27.8 EBq @ shutdown), HLW, ingestion radiotox 2.18e9 Sv | `dose_site_boundary`, `epz_radius` (needs dispersion analysis to close) |
| Reload scheme | 4-batch, 0.90 CF | waste arisings, SFP/cask sizing |
| Lattice | 21 FA × 17×17, 200 cm active, 20 cm H₂O radial reflector | `layout/building_list.md` RXB internal dims |
| **Proliferation resistance** | discharge Pu is **reactor-grade** (Pu-240 24.6 %, fissile 66 %), self-protecting (19.5 W/kg-Pu, high SF-n), spent U 1.10 % — once-through, no separated stream | **NEW 3S feature** → `safety/safeguards_nonproliferation.md` |

---

## 6. Doc updates applied in this commit

- `README.md` — decisions #2 (enrichment) + #4 (burnable absorber) corrected to rev_3; layout open item #5 (fuel count) marked resolved = 21 FA.
- `safety/safety_criteria.yaml` — `decisions_locked.enrichment_target` updated; `fuel_enrichment_max`, `k_eff_operating` notes corrected; pointer to this report added.
- `layout/aux_systems.md` §7 — SFP wording corrected to unborated / burnup-credit (k_eff ≤ 0.95).

**Not changed:** the limit *values* in `safety_criteria.yaml` (they're regulatory, design-independent). Only notes, statuses, and superseded decisions.

---

## 7. Source files (in `../aegis-40-OpenMC`)

- `docs/competition/design-basis-locked.md` — rev_3 authoritative parameter set
- `openmc_model/results/summary_report.txt` — the 10-gate safety summary
- `openmc_model/sample_inputs/{geometry,materials,settings}.xml` — as-run deck
- `docs/competition/waste/decay-heat-interpretation.md` — 7.75 MW decay heat
- `docs/competition/waste/discharge_source_term.md` — source term / HLW class
- `docs/competition/reference-reactors-comparison.md` — CAREM / Jang precedent + SFP criticality method

---

*End of alignment check. Bottom line: physics passes every gate; sync your enrichment + burnable-absorber decisions to rev_3, resolve CRDM type, and route decay heat + peaking to the T-H team.*
