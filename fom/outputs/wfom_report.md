# Aegis-40 wFOM — analysis report
*Generated 2026-07-01 by fom/wfom.py. Weights: default_pending_supervisor (PLAN §1.2 q1 — supervisor approval pending).*

## 1. Hard-constraint gate (PLAN §5.3)
- aegis40: feasible
- carem25: feasible
- smart: feasible
- nuscale_voygr: feasible

> Aegis-40 peaking is the **rev_4 de-peaked design target F_Q ≈ 2.00** (≤2.50 LCO) — the 37-FA core + edge-pin/ring de-peaking replaces the rev_3 (21-FA) as-run 3.478. The gate now passes; the value awaits OpenMC high-stat confirmation (`open_item: peaking_recompute`; `safety/SIMULATION_ANALYSIS_PLAN.md` F1↔N6).

## 2. Pairwise wFOM — Aegis-40 vs references
wFOM > 0 ⇒ Aegis-40 scores higher on the weighted aggregate. Per-pair renormalization over parameters populated in **both** reactors.

| Reference | wFOM | safety | economic | safeguards | sustainability | efficiency | #params |
|---|---|---|---|---|---|---|---|
| carem25 | **+0.328** | +0.134 | +0.075 | +0.006 | +0.077 | +0.035 | 17 |
| smart | **+0.280** | +0.180 | +0.007 | +0.073 | +0.024 | -0.004 | 16 |
| nuscale_voygr | **-0.385** | -0.389 | -0.069 | +0.044 | +0.030 | +0.000 | 17 |

## 3. Absolute-utility ranking (single scale)
Because every normalizer is a difference of a per-reactor term, an absolute utility U(X) exists and wFOM(D,R)=U(D)−U(R). Ranked on the **16 parameters populated for all four reactors**: burnup, capacity_factor, cycle_length_efpd, design_life, diversity_count, epz_class, footprint_per_mwe, n_active_components, non_electric_revenue_share, primary_circulation, refuel_cycle, sbf_score, seismic_sse, specific_revenue, spent_fuel_per_mwh, thermal_efficiency.

| Rank | Reactor | U (abs. utility) | ΔU vs Aegis-40 |
|---|---|---|---|
| 1 | nuscale_voygr | +0.605 | +0.143 |
| 2 | aegis40 | +0.462 | +0.000 |
| 3 | carem25 | +0.197 | -0.265 |
| 4 | smart | +0.182 | -0.280 |

> Note: the common set has only **n_active_components** from the Safety category (PCT/MDNBR/peaking/MTC are sim-only and unpublished for competitors) — so this ranking under-represents Safety despite its 0.35 weight. The pairwise table (§2) recovers more safety coverage where reference data exists. **This data-availability gap is the single biggest threat to the comparison's validity.**

## 3a. Score transparency — every number

### Raw inputs (what goes in)
| Parameter (cat) | dir | Aegis-40 | CAREM-25 | SMART | NuScale |
|---|---|---|---|---|---|
| specific_revenue (econ) | max | 544 | 473 | 473 | 499 |
| footprint_per_mwe (econ) | min | 484 | 1.2e+03 | 841 | 152 |
| refuel_cycle (econ) | max | 16 | 14 | 30 | 18 |
| cycle_length_efpd (econ) | max | 479 | 390 | 870 | 520 |
| thermal_efficiency (effi) | max | 0.32 | 0.3 | 0.293 | 0.308 |
| burnup (effi) | max | 42.8 | 24 | 54 | 45 |
| capacity_factor (effi) | max | 0.95 | 0.9 | 0.9 | 0.95 |
| sbf_score (safe) | max | 3 | 3 | 0 | 0 |
| diversity_count (safe) | max | 5 | 4 | 3 | 4 |
| epz_class (safe) | max | 1 | 1 | 1 | 2 |
| seismic_sse (safe) | max | 0.3 | 0.25 | 0.3 | 0.5 |
| n_active_components (safe) | min | 2 | 3 | 4 | 1 |
| primary_circulation (safe) | max | 1 | 1 | 0 | 1 |
| non_electric_revenue_share (sust) | max | 0.0827 | 0.05 | 0.05 | 0.05 |
| design_life (sust) | max | 60 | 40 | 60 | 60 |
| spent_fuel_per_mwh (sust) | min | 1.75 | 3.33 | 1.52 | 1.73 |

### Weighted contribution to the ranking (centered on field mean)
Cell = `gw·(uᵢ − mean)`. **+** helps, **−** hurts. Column sum = U − mean(U). `gw` = global weight of the parameter.
| Parameter | gw | Aegis-40 | CAREM-25 | SMART | NuScale |
|---|---|---|---|---|---|
| specific_revenue | 0.080 | +0.007 | -0.004 | -0.004 | +0.000 |
| footprint_per_mwe | 0.060 | +0.005 | -0.050 | -0.029 | +0.074 |
| refuel_cycle | 0.040 | -0.006 | -0.011 | +0.019 | -0.001 |
| cycle_length_efpd | 0.020 | -0.002 | -0.006 | +0.010 | -0.001 |
| thermal_efficiency | 0.067 | +0.003 | -0.001 | -0.003 | +0.001 |
| burnup | 0.050 | +0.004 | -0.025 | +0.015 | +0.006 |
| capacity_factor | 0.033 | +0.001 | -0.001 | -0.001 | +0.001 |
| sbf_score | 0.060 | +0.030 | +0.030 | -0.030 | -0.030 |
| diversity_count | 0.045 | +0.006 | +0.000 | -0.006 | +0.000 |
| epz_class | 0.045 | -0.006 | -0.006 | -0.006 | +0.017 |
| seismic_sse | 0.135 | -0.011 | -0.036 | -0.011 | +0.058 |
| n_active_components | 0.113 | +0.011 | -0.034 | -0.067 | +0.090 |
| primary_circulation | 0.102 | +0.025 | +0.025 | -0.076 | +0.025 |
| non_electric_revenue_share | 0.060 | +0.023 | -0.008 | -0.008 | -0.008 |
| design_life | 0.045 | +0.005 | -0.014 | +0.005 | +0.005 |
| spent_fuel_per_mwh | 0.045 | +0.005 | -0.023 | +0.012 | +0.006 |
| **category subtotals:** | | | | | |
| _safety_ | 0.350 | +0.026 | -0.045 | -0.154 | +0.173 |
| _economic_ | 0.200 | +0.003 | -0.072 | -0.004 | +0.072 |
| _safeguards_ | 0.150 | +0.031 | +0.024 | -0.042 | -0.013 |
| _sustainability_ | 0.150 | +0.033 | -0.045 | +0.009 | +0.003 |
| _efficiency_ | 0.150 | +0.008 | -0.027 | +0.012 | +0.008 |
| **U − mean(U)** | 1.000 | **+0.100** | **-0.164** | **-0.179** | **+0.243** |

## 3b. Absolute scoring vs international-standard targets
Each reactor scored against a fixed benchmark of regulatory limits + good-design targets (`reactors/standards.yaml`) instead of against each other. **wFOM > 0 ⇒ beats the benchmark.** Reactor-independent, so it answers "is it good?" not just "better than X?"

| Reactor | wFOM vs standards | #params |
|---|---|---|
| aegis40 | **-0.196** | 21 |
| carem25 | **-0.481** | 17 |
| smart | **-0.462** | 16 |
| nuscale_voygr | **+0.231** | 17 |
> Aegis-40 uses the de-peaked variant; with as-run peaking it is DESIGN_FAILED (§1). Aegis-40 sees more safety parameters here (it has PCT-less but MTC/peaking) than competitors do.

## 3c. AHP category weights + consistency check
Principal-eigenvector weights from `ahp/category_pairwise.yaml`. **Consistency ratio CR = 0.0021** (must be < 0.10 — PASS).

| Category | AHP weight | default weight |
|---|---|---|
| safety | 0.395 | 0.350 |
| economic | 0.234 | 0.200 |
| safeguards | 0.124 | 0.150 |
| sustainability | 0.124 | 0.150 |
| efficiency | 0.124 | 0.150 |

→ ranking with AHP weights: nuscale_voygr > aegis40 > carem25 > smart
→ ranking with default weights: nuscale_voygr > aegis40 > carem25 > smart  (SAME)

## 4. Validation suite
| Property | Pass | Value |
|---|---|---|
| identity  wFOM(R,R)=0 | ✅ | 0.00e+00 |
| antisymmetry  wFOM(A,B)=−wFOM(B,A) | ✅ | +0.280/-0.280 |
| transitivity  U(A)−U(C)=(A−B)+(B−C) | ✅ | -0.143=-0.143 |
| monotonicity  ↑burnup ⇒ ↑wFOM | ✅ | +0.328→+0.333 |

## 5. Independent cross-check — TOPSIS
Same data + global weights, different aggregation (distance-to-ideal). If the ranking agrees with wFOM, the result is method-robust.

| Reactor | TOPSIS closeness | wFOM rank | TOPSIS rank |
|---|---|---|---|
| nuscale_voygr | 0.695 | 1 | 1 |
| aegis40 | 0.644 | 2 | 2 |
| carem25 | 0.469 | 3 | 3 |
| smart | 0.248 | 4 | 4 |

→ wFOM order: nuscale_voygr > aegis40 > carem25 > smart
→ TOPSIS order: nuscale_voygr > aegis40 > carem25 > smart  (AGREE)

## 6. Weight robustness — leave-one-category-out
Drop each category, re-rank on the common set. If Aegis-40's rank holds, the result doesn't hinge on one category.

| Dropped category | Ranking (best→worst) | Aegis-40 rank |
|---|---|---|
| (none) | nuscale_voygr > aegis40 > carem25 > smart | 2 |
| −safety | aegis40 > nuscale_voygr > smart > carem25 | 1 |
| −economic | nuscale_voygr > aegis40 > carem25 > smart | 2 |
| −safeguards | nuscale_voygr > aegis40 > smart > carem25 | 2 |
| −sustainability | nuscale_voygr > aegis40 > carem25 > smart | 2 |
| −efficiency | nuscale_voygr > aegis40 > carem25 > smart | 2 |

