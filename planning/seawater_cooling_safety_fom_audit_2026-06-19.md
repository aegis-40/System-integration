# Aegis-40 — Seawater Cooling Conversion: Standards Review, Safety-YAML Audit, FOM Defensibility, and Layout Update Map

*Standalone review deliverable. Owner: Azamhon (3S / I&C / FOM). Date: 2026-06-19.*
*Scope: operationalize the team's 2026-06-13 decision to replace closed-cycle cooling towers with a once-through seawater heat-rejection system (Sinop / Black Sea coast).*
*Companions audited: `safety/safety_criteria.yaml`, `fom/*`, `layout/*`, `safety/regulatory_alignment_audit.md`, `docs/international_regulations/*`.*

> **Non-proliferation guardrail (applies to the whole document).** The cooling change is confined to the **balance-of-plant / secondary heat-rejection side**. It does not touch the fuel, the once-through fuel cycle, enrichment, the primary boundary, or any fissile-material stream. Nothing in this analysis is structured for, or usable for, weapons development or for defeating proliferation-resistance measures. The Aegis-40 once-through, boron-free, high-burnup cycle remains self-protecting with **no separated-fissile stream anywhere in the plant** (`safety/safeguards_nonproliferation.md`). Seawater cooling is conventional industrial technology with no proliferation relevance.

---

## 0. Executive summary

| # | Task | Verdict | Key action |
|---|---|---|---|
| 1 | Akkuyu / Türkiye realism check | **Confirmed realistic** | Once-through seawater is the *licensed Turkish precedent* (Akkuyu, 4× VVER-1200). Sinop is **colder** than Akkuyu → our efficiency assumption is conservative. |
| 2 | Standards baseline (`docs/`) | **Re-anchored** | The governing requirement is **SSR-2/1 Req 52–53 (heat transfer to UHS)**. Seawater is the **normal** heat sink (non-safety); the **safety UHS stays passive** (IRWST + passive containment cooling, 72 h+). |
| 3 | `safety_criteria.yaml` audit | **3 structural + 6 technical/compliance findings** | Add a UHS-reliability criterion and a coastal-external-hazard criterion; fix a **UHS terminology conflation** that propagated into two other files; bump `design_id` to rev_3. |
| 4 | FOM defensibility | **Currently indefensible — 6 root causes, all fixable** | Stop silently substituting the de-peaked peaking value; elicit weights independently; propagate data uncertainty; add the water/environmental dimension the cooling change is actually about. |
| 5 | Layout update map | **24 touch-points across 16 files** | Split into **"text/data now"** (TES-independent) vs **"graphical recut batched with the C3 TES decision"** to avoid drawing twice. |

---

## 1. Task 1 — Türkiye / Akkuyu practice & licensing (realism check)

**Question being answered:** is "once-through seawater, no cooling towers, thermal effluent returned to the sea" a realistic, licensable configuration in Türkiye, or an unsupported assumption?

**Answer: it is the established, licensed Turkish precedent.** Akkuyu NPP — Türkiye's first NPP, four Generation III+ **VVER-1200** units on the Mediterranean coast at Büyükeceli (Mersin) — rejects secondary-loop heat to the sea through a **once-through seawater system with no cooling towers.**

### 1.1 What Akkuyu actually does (verified)

| Feature | Akkuyu as built/licensed | Source |
|---|---|---|
| Cooling principle | Once-through seawater on the secondary (non-nuclear) side; **no cooling towers** | WNN, Akkuyu Nükleer |
| Intake capacity | ~**334 m³/s** total (4 units), from coastal ponds behind protective breakwaters; hydraulic design constrained by intake velocity + vortex suppression | Artelia (hydraulic-structures designer) |
| Outfall | Forebay → **12 pressurised culverts**; return to sea via **10 GRP/fiberglass lines Ø2–4 m, ~10 km total** | Artelia; Rosatom |
| Effluent monitoring | **Real-time discharge-water monitoring** (thermal + radiological) | WNN |
| Intake seawater temperature | **30–32 °C in summer** (Mediterranean) → recognised condenser back-pressure / efficiency penalty | Eurasia Review OpEd; thermoeconomic studies |
| Governing environmental impacts | Thermal plume, **entrainment + impingement** of marine organisms, dredging/construction disturbance of shoreline | Akkuyu EIA case studies |
| Licensing | EIA (ÇED) approved 2014; nuclear safety under **NDK** (Nükleer Düzenleme Kurumu, est. 2018, Law No. 7381); thermal/chemical discharge under MoEUCC + the **Water Pollution Control Regulation (Su Kirliliği Kontrolü Yönetmeliği, SKKY)** | NDK; SKKY |

### 1.2 What this means for Aegis-40 (the realism transfer)

1. **The configuration is licensable in Türkiye.** Once-through seawater with sea-return thermal effluent is exactly what the national regulator and EIA process have already accepted for a 4×3200 MWth fleet. Our single 125 MWth unit is a small, conventional case by comparison.
2. **Our heat load is ~1 % of Akkuyu's.** Aegis-40 rejects roughly **70–82 MWth** to the condenser (125 MWth − 40 MWe − ~15 MWth cogen draw-off). Akkuyu rejects on the order of **8 000 MWth** across four units. The Aegis-40 thermal plume is therefore **negligible** at the site scale — this is a genuinely defensible environmental claim, not hand-waving.
3. **Sinop/Black Sea is colder than Akkuyu/Mediterranean → our efficiency assumption is conservative.** Akkuyu's summer intake reaches 30–32 °C and *still* licenses once-through. Black Sea surface water at Sinop runs roughly **8 °C (winter) to ~25 °C (summer)**. Colder cooling water lowers condenser back-pressure, so the Aegis-40 cycle-efficiency claim **can only improve** versus a cooling-tower baseline — consistent with `planning/FER_readiness_review_2026-06-13.md` item X3.
4. **The intake is the new safety-relevant external interface.** Akkuyu uses breakwaters, coastal ponds, intake-velocity limits, and vortex suppression precisely because a coastal intake imports external hazards: **storm surge, marine debris/biofouling, jellyfish/algal blooms, oil slicks, ice.** These must enter the Aegis-40 hazards register (see §3) — but note (critically) that for Aegis-40 they threaten only the *normal* heat sink, not the *safety* heat sink (§2).

### 1.3 Regulatory framing to adopt

- **Nuclear safety:** NDK, applying IAEA SSR-2/1 (the `docs/` master set). The seawater system is **secondary-side, non-safety-classified** (justified in §2.2).
- **Environmental discharge:** SKKY governs the thermal/chemical effluent. Cooling systems are licensed for **a maximum discharge temperature and a maximum ΔT (rise above ambient at the mixing-zone boundary).** *Adopt as a design assumption a conservative receiving-water rise (commonly ≤ ~1–2 °C beyond the mixing zone for sensitive coastal waters) and tag it `[VERIFY-SKKY]` against the exact current SKKY clause before any FER environmental claim.* The exact numerical SKKY limit could not be machine-verified in this pass and must be confirmed from the official regulation text.

**Sources:**
- [Akkuyu 1 construction and components — World Nuclear News](https://www.world-nuclear-news.org/Articles/Akkuyu-1-construction-and-components)
- [Akkuyu to have real-time discharge water monitoring system — World Nuclear News](https://www.world-nuclear-news.org/articles/akkuyu-to-have-real-time-discharge-water-monitoring-system)
- [Start-up work under way for Akkuyu pumping station — World Nuclear News](https://www.world-nuclear-news.org/articles/start-up-work-under-way-for-akkuyu-pumping-station)
- [Sea water intakes and outfalls — Akkuyu NPP — Artelia](https://www.laboratory.arteliagroup.com/7119-akkuyu-power-plant-water-intakes-outfalls.htm)
- [How the NPP works — Akkuyu Nükleer A.Ş.](https://akkuyu.com/en/how-it-works)
- [Akkuyu NPP and the Cooling Water Temperature Issue — Eurasia Review](https://www.eurasiareview.com/09102023-akkuyu-nuclear-power-plant-and-the-cooling-water-temperature-issue-oped/)
- [Thermoeconomic analysis and environmental impact assessment of the Akkuyu NPP — Springer](https://link.springer.com/article/10.1007/s10973-024-13237-x)
- [Turkish Regulations — water pollution control framework (DEU)](https://web.deu.edu.tr/atiksu/ana52/ani4152.html)

---

## 2. Task 1 — Standards baseline from `docs/international_regulations/`

The `docs/` master set (identified in `docs/_INDEX.md`) is: **SSR-2/1 Rev 1** (Safety of NPP: Design), **SSG-52** (Core), **TECDOC-1936** (SMR applicability), **NUREG-1431 Rev 5** (STS). The requirements that the cooling change actually touches:

| Requirement | What it demands | Bearing on the seawater change |
|---|---|---|
| **SSR-2/1 Req 52** — removal of residual heat from the core | Reliable means to transfer residual heat under all operational states + DBA | Seawater path is *not* credited for this in Aegis-40 — passive PRHR/IRWST is. **Confirms seawater can be non-safety.** |
| **SSR-2/1 Req 53** — heat transfer to an ultimate heat sink | A UHS + the systems transferring heat to it, with reliability commensurate with safety function | **The pivotal requirement.** The *safety* UHS must be the passive sink (IRWST + atmosphere); seawater is the *normal-operation* sink only. The YAML must say this explicitly (§3). |
| **SSR-2/1 Req 17 / 18** — internal & external hazards, CCF | Design against site-credible hazards and common-cause failure | Coastal intake imports new external CCF candidates (surge, biofouling, debris, ice). Must be screened — but they do **not** propagate to the safety UHS because that sink is seawater-independent. |
| **SSR-1 / SSG-9** — site evaluation, external natural hazards | Tsunami, storm surge, extreme sea level, marine biological events | New design-basis external events for a coastal site; currently only `[PENDING]` in `safety/hazards_register.md`. |
| **TECDOC-1936** — graded SMR application | Apply SSR-2/1 with grading appropriate to the SMR's hazard | Justifies **non-safety classification of the seawater system**: because decay-heat removal is passive and seawater-independent, loss of seawater is a *power-conversion* event, not a *safety* event → graded down. |
| **SSR-2/1 Req 35** — non-electrical / heat-utilization couplings | No radionuclide transport to heat/H₂ users | Already resolved (`aux_systems.md §9a`); unaffected by the heat-sink change. |
| **NUREG-1431 LCO 3.2.1/3.2.2** — core peaking | Core power-distribution limits | **Independent of heat-sink choice** — peaking findings (§3) stand regardless of cooling. |

**The single most important standards conclusion:** under SSR-2/1 Req 53, Aegis-40 has **two distinct heat sinks that must not be conflated** —

- **Normal heat sink = the Black Sea (once-through seawater).** Power operation, non-safety-classified, removes the ~70–82 MWth condenser duty.
- **Safety ultimate heat sink = the IRWST + passive containment cooling (and ultimately the atmosphere).** Decay-heat removal, safety-classified, **independent of seawater**, supports the 72 h+ grace claim (`event_tree_LOHS.md`, `safety_criteria.yaml` `prhr_capacity` / `operator_grace_period`).

This separation is *the* defensibility argument for the whole change: **switching the normal heat sink to seawater does not degrade the safety case, because the safety UHS was never the heat sink being switched.** Two existing files currently violate this distinction (§3, findings T2/T3) and must be corrected.

---

## 3. Task 2 — Audit of `safety/safety_criteria.yaml`

Audited against the §2 standards. The file is well-structured and traceable; findings below are ordered structural → technical → compliance. Severity: 🔴 must-fix before FER, 🟡 should-fix, 🟢 housekeeping.

### 3.1 Structural findings

| ID | Sev | Finding | Fix |
|---|---|---|---|
| **S1** | 🟡 | `design_id: aegis40-rev_0` (line 24) contradicts the rev_3 core basis cited throughout the notes (k_eff 1.0264, 4.95/4.70/4.40 wt%, 479 EFPD). The spine document is labelled with a superseded revision. | Bump `design_id` to track rev_3 (e.g. `aegis40-rev_3-safety_r1`). |
| **S2** | 🟢 | `cycle_length` carries `defense_in_depth_level: 0` (line 502). The header (line 20) defines the DiD scale as **1..5**; 0 is out of range. | Set to `null` (cycle length is an economic target, not a DiD feature), not 0. |
| **S3** | 🟢 | The `tolerance` field is used (`k_eff_operating`, `sg_pressure_operating`) but is **not declared** in the schema header (lines 4–21). | Add `tolerance` to the schema legend so the field is self-documenting. |

### 3.2 Technical findings

| ID | Sev | Finding | Fix |
|---|---|---|---|
| **T1** | 🔴 | **Two hard-constraints are currently breached.** `f_q_total` = 3.478 > 2.50 LCO and `f_delta_h_radial` = 2.268 > 1.65 LCO (rev_3 as-run, both flagged in the notes). By the file's own semantics (`hard_constraint → breach ⇒ design REJECTED`), Aegis-40 is formally in a **DESIGN_REJECTED** state pending `open_item: peaking_recompute`. This is correctly *documented* but must not be silently bypassed downstream — see FOM finding F2. | Keep the FLAG; gate the design as provisional until the pin-aligned re-tally closes `peaking_recompute` (due 2026-06-19, now). Do **not** treat the de-peak target as achieved. |
| **T2** | 🔴 | **No ultimate-heat-sink reliability criterion exists**, despite SSR-2/1 Req 53 being directly engaged by the cooling change. The file has `prhr_capacity` and `operator_grace_period` but no row that *names the safety UHS and asserts its seawater-independence*. | **Add criterion** `ultimate_heat_sink` (below). |
| **T3** | 🔴 | **UHS terminology conflation propagated into other files.** `safety/regulatory_alignment_audit.md:66` states "UHS = seawater (C2 resolved)" and `safety/hazards_register.md:40` calls it "coastal seawater UHS intake." This **contradicts** the passive-IRWST 72 h safety case in `event_tree_LOHS.md`. Per §2, seawater is the *normal* sink, not the *safety* UHS. | Correct both lines: "normal heat sink = seawater (non-safety); **safety UHS = IRWST + passive containment cooling**, seawater-independent." |
| **T4** | 🟡 | **No coastal external-hazard criterion** even though the site is now coastal (Sinop). `hazards_register.md` lists tsunami/flooding as `PENDING`, but there is no design-basis criterion row (SSR-1/SSG-9). | **Add criterion** `coastal_external_hazard` (below) for design-basis extreme sea level / storm surge / tsunami, and a marine-intake-blockage screen for the normal sink. |
| **T5** | 🟡 | `shutdown_margin` hard limit = **0.01 Δk/k (1 %)** (line 53). Typical PWR Tech-Spec SDM is **~1.3–1.77 %**; 1 % is permissive for a hard floor. The as-run cold SDM (12.4 %) clears either, so this is about defensibility of the *limit*, not the design. | Justify the 1 % choice against NRC SRP 4.3 / SSG-52, or raise to ≥ 1.3 %. |
| **T6** | 🟡 | Several rows are sourced to **"FER Template Table 1"** (`containment_pressure`, `sg_pressure_operating`, `epz_radius`, `cdf`, `lrf`, `sse_design`). `docs/_INDEX.md` marks Table 1 values as **illustrative, not prescribed**. Hard-constraints should not rest on illustrative numbers. | Re-source to analysis (`open_item: containment_pt_analysis` already covers containment P); mark the rest `[ILLUSTRATIVE-SOURCE — confirm by analysis]`. |

### 3.3 Compliance scorecard (vs §2 standards)

| Standard | Status in YAML | Note |
|---|---|---|
| SSR-2/1 Req 46 (shutdown systems ≥2) | ✅ Resolved | EBIS adopted; sizing pending (`shutdown_second_system`). |
| SSR-2/1 Req 35 (cogen isolation) | ✅ Resolved | 3 barriers; tritium budget pending. |
| SSR-2/1 Req 52 (residual-heat removal) | ✅ Covered | `prhr_capacity`. |
| **SSR-2/1 Req 53 (UHS)** | **⚠ GAP** | No UHS-reliability row; terminology conflated (T2/T3). **Add `ultimate_heat_sink`.** |
| **SSR-1 / SSG-9 (coastal hazards)** | **⚠ GAP** | Not a criterion (T4). **Add `coastal_external_hazard`.** |
| NUREG-1431 LCO 3.2.1/3.2.2 (peaking) | ⚠ Breached | T1 — design-level, not a file error. |
| Thermal-discharge environmental limit | ◻ Out of nuclear-safety scope | Belongs in an environmental/discharge doc or the layout file; tag `[VERIFY-SKKY]` (§1.3). |

### 3.4 Proposed new YAML criteria (drop-in, schema-conformant)

```yaml
  - id: ultimate_heat_sink
    parameter: "Safety ultimate heat sink — availability & seawater-independence"
    limit_value: 72            # h of passive heat removal with no operator action, no AC, no seawater
    unit: "h"
    direction: ">="
    type: hard_constraint
    source: "IAEA SSR-2/1 Rev 1 Req 53 (heat transfer to UHS); TECDOC-1936 (graded SMR)"
    normalizer: log_ratio
    fom_param: derived_safety.uhs_passive_grace_h
    sensor_chain: ["IRWST level + temperature", "containment pressure", "PCCS pool level"]
    setpoint_link: null
    defense_in_depth_level: 4
    notes: >
      The SAFETY UHS is the IRWST + passive containment cooling (atmosphere-coupled),
      NOT the once-through seawater system. Seawater is the NORMAL (power-operation,
      non-safety-classified) heat sink only. This row asserts that loss of the seawater
      intake (storm surge / biofouling / debris / ice) is a power-conversion event that
      does NOT challenge the safety UHS — decay heat removal is passive and
      seawater-independent for >=72 h (target unlimited). Corrects the UHS conflation in
      regulatory_alignment_audit.md and hazards_register.md (2026-06-19 seawater audit).

  - id: coastal_external_hazard
    parameter: "Design-basis extreme sea level / storm surge / tsunami protection"
    limit_value: null          # site-specific DBFL grade once Sinop hazard study lands
    unit: "m (DBFL grade)"
    direction: ">="
    type: hard_constraint
    source: "IAEA SSR-1; SSG-9 (site evaluation); SSR-2/1 Req 17/18 (external hazards, CCF)"
    normalizer: min_max
    normalizer_params: {min: 0, max: 1}
    fom_param: derived_safety.coastal_hazard_protected
    sensor_chain: ["site flood-hazard study", "intake forebay level", "trash-rack dP"]
    setpoint_link: null
    defense_in_depth_level: 4
    notes: >
      Coastal Sinop site introduces extreme-sea-level, storm-surge and tsunami as
      design-basis external events, plus marine intake blockage (biofouling, jellyfish/
      algal bloom, debris, ice) as a CCF candidate for the NORMAL heat sink. Safety SSCs
      on dry-site grade above DBFL; intake protected by breakwater + redundant
      travelling screens (Akkuyu practice). [ANALYSIS-PENDING — Sinop coastal hazard study].
```

---

## 4. Task 3 — FOM defensibility (why it fails, how to fix it)

The FOM (`fom/wfom.py`, `fom/parameters_schema.yaml`, README) is mathematically clean — antisymmetric, transitive, AHP CR = 0.002, TOPSIS cross-checked. **Its indefensibility is not in the math; it is in the inputs, the gate-handling, and the framing.** The README's own "Honesty caveats" already name most of this; below each is turned into a *concrete, actionable fix* with engineering/safety justification.

### 4.1 Root causes of indefensibility

| ID | Root cause | Why it makes the result indefensible | Concrete fix (with justification) |
|---|---|---|---|
| **F1** | **Self-referential weighting.** Weights reward Aegis-40's own design philosophy (SBF, passive, cogen); README admits "ranking #1 partly by construction." | A reviewer can dismiss the whole result as constructed to win. The weights are the single biggest lever and are author-chosen. | Elicit the AHP pairwise matrix from an **independent panel / the supervisor**, not the design author; keep CR < 0.10 (already achievable). **Always report the neutral equal-weight result alongside** — if Aegis-40 holds rank under equal weights, the conclusion is not a weighting artifact. Publish the weight-sensitivity band, not a point. |
| **F2** | **Comparing a design that fails its own hard gate.** `wfom.py` substitutes the **de-peak target 2.30** for the as-run **3.478** that trips the gate (README §3 + report §1 both admit this). | This compares a *hypothetical, not-yet-achieved* de-peaked Aegis-40 against *as-built* competitors. That is not a like-for-like comparison and is the most attackable single move in the FOM. | **Never silently swap.** Report Aegis-40 as **DESIGN_PROVISIONAL** until `peaking_recompute` closes. Show **both** rows explicitly: "as-run (FAILS gate)" and "post-de-peak target (provisional, contingent on Samira's pin-aligned re-tally)." Tie the provisional flag to `safety_criteria.yaml` T1. |
| **F3** | **Confidence asymmetry in the data.** Aegis-40 inputs are sim-derived/precise; competitor inputs are literature **estimates** (status flags in the YAMLs). | Mixing high- and low-confidence numbers as if equal hides that the ranking could flip on a single soft competitor figure — which already happened once (README §3: "an earlier run had Aegis-40 #1… a bad-estimate artifact"). | **Propagate parameter uncertainty:** sample ±10 % on literature values, ±5 % on sim values, report wFOM as **5/50/95-percentile bands**. Cite every competitor value to the **IAEA SMR booklet** (`docs/SMR_booklet.pdf`) with a page reference, or mark it `[ESTIMATE]` and exclude from headline claims. |
| **F4** | **Pairwise vs absolute inconsistency** (the NuScale case — README §4). Different parameter coverage gives different answers. | Two internally-consistent methods disagreeing, unexplained, reads as instability. | Compute the absolute utility **U on a single common parameter set**, or always disclose both with the coverage caveat stated inline. Fill the `grace_period` gap for SMART so the common set is complete. |
| **F5** | **Normalizer tuning is unjustified.** `target_gaussian` α values (e.g. `pct` α = 5e-6, `mtc` α = 2e-3, `peaking` α = 4) are free parameters that set how steeply score decays — currently chosen by hand. | α silently controls how much a parameter can swing the result; arbitrary α = arbitrary outcome. | **Derive each α from the physical tolerance band**: set α so the Gaussian drops to 0.5 *at the regulatory limit / LCO* (e.g. `peaking` g = 0.5 at F_q = 2.50; `mtc` g = 0.5 at 0 pcm/K). Document the derivation per row. Run a **normalizer-swap** robustness pass (log-ratio ↔ min-max where both defensible). |
| **F6** | **The FOM is blind to the dimension this design change is about.** There is **no water-use / thermal-discharge / environmental parameter.** | The headline decision of this whole task — switch to once-through seawater — has real trade-offs the current FOM literally cannot score. A FOM that can't see the design's marquee change is not defensible *as a decision tool*. | **Add the environmental dimension** (§4.3). This both closes a coverage gap and ties the FOM directly to the cooling decision. |

### 4.2 What is already defensible (keep it)

The **parameter limits are well-anchored to standards** — this is the FOM's strength and should be foregrounded:

- `peaking_factor_3d` ceiling 2.5 ← NUREG-1431 LCO 3.2.1 · `mdnbr` floor 1.3 ← NUREG-0800 SRP 4.4 (W-3 95/95) · `pct` ceiling 1204 °C ← 10 CFR 50.46(b)(1) · `mtc` ceiling 0 ← GDC-11 / SSR-2/1 Req 46 · `grace_period` ← SSG-39 · `seismic_sse` ← RG 1.60 / SSG-9.

The hard gate (pass/fail on these) is the right design and should stay. The defensibility work is entirely on **weights (F1), gate-honesty (F2), data (F3), method-reconciliation (F4), normalizer derivation (F5), and coverage (F6)** — not on the limits.

### 4.3 Cooling-change impact on FOM inputs (concrete, do now)

The seawater conversion changes three existing inputs and motivates one new parameter:

| Parameter | Current (`fom/reactors/aegis40.yaml`) | Change | Justification |
|---|---|---|---|
| `plant_footprint_m2` | 20000 (→ footprint_per_mwe 500) | **Reduce** by the freed CTW building (~900 m²) net of the shoreline intake/discharge + CWP house (mostly outside the plant island). Net: modest improvement. | CTW deleted from `building_list.md`; intake/outfall are shoreline structures, not plant-island footprint. |
| `thermal_efficiency` (derived) | from P_el/P_th | **Nudge up** with cold Black Sea intake (8–25 °C vs cooling-tower approach temp) → lower condenser back-pressure. | §1.2(3); `FER_readiness_review_2026-06-13.md` X3 ("η claim can only get better"). Confirm magnitude with the cycle/OpenFOAM number before publishing. |
| `refuel_cycle` / others | — | No change | Heat-sink-independent. |
| **NEW** `freshwater_consumption` (sustainability) | — | **Add.** Once-through seawater ≈ **0 freshwater makeup**; evaporative cooling towers consume ~2–3 % of circulating flow. | Strong, defensible sustainability differentiator; competitor cooling type is booklet-sourceable. Direction = min, log-ratio. |
| **NEW (optional)** `thermal_discharge_marine_load` (environmental, honesty MINUS) | — | Consider adding so the FOM stays honest about the once-through trade-off (plume/entrainment), not just the water-saving upside. | Keeps F6 fix balanced; can be a small-weight min-direction min_max ordinal. |

> **Net FOM effect of the cooling change:** marginally favourable to Aegis-40 (smaller footprint, better η, near-zero freshwater) **but only meaningful once F1–F5 are fixed** — otherwise it just adds another author-tuned number to an already-contested metric.

### 4.4 Minimal defensible-FOM checklist (for the FER)

1. ☐ Independent/supervisor AHP weights, CR < 0.10, **+ equal-weight neutral run reported**.
2. ☐ Aegis-40 shown **as-run (FAILS gate) and de-peak-target (provisional)** — no silent swap.
3. ☐ Every competitor value cited to `docs/SMR_booklet.pdf` or marked `[ESTIMATE]`.
4. ☐ Uncertainty propagation → wFOM reported as **percentile bands**.
5. ☐ α values **derived from limits**, documented per parameter.
6. ☐ Environmental/water dimension added (`freshwater_consumption` at minimum).
7. ☐ Pairwise vs absolute reconciled or jointly disclosed.

---

## 5. Task 4 — Layout & system-file update map

The team flagged a **single graphical recut after the C3 (TES technology) decision settles** to avoid drawing twice (`fer_8810_docx_audit.md` C2/C3; C3 is still under deliberation — zeolite-13X vs two-tank Therminol-66). Accordingly the work splits cleanly:

- **Track A — text/data updates: do now** (TES-independent; unblocks the FER text and the FOM/safety files).
- **Track B — graphical recut: batch with the C3 TES resolution** (PFD, SVGs, CAD/STEP, web viewer, Mermaid sources — all redrawn once).

### 5.1 Track A — do now (text, tables, YAML)

| # | File | Current state | Required change | Pri |
|---|---|---|---|---|
| A1 | `layout/zones.md` | §2.2 CI still lists "Cooling Tower (CTW) … closed-cycle"; §4 ASCII + Z3 say "turbine + cooling tower dominate"; Z6 notes the decision | Replace CTW with **Seawater Intake Structure + Discharge/Outfall + Circulating Water Pump (CWP) house**; recompute CI footprint; add the **safety-UHS ≠ seawater** note (§2) | 🔴 |
| A2 | `layout/building_list.md` | CTW row (line 58, 900 m² MDCT `[ASSUMED]`); §5 R2 coverage "TB+EHB+**CTW**"; CI subtotal | Delete CTW; **add CWP house + Intake Structure + Discharge Structure** rows (with screens/biofouling notes); update R2 coverage + CI subtotal | 🔴 |
| A3 | `layout/critical_piping_table.md` | Row 8 condenser circ-water "◐ size TBD"; CCWS not shown | Finalize **seawater once-through** (intake → condenser → outfall); confirm ~2–2.5 m³/s with Adilbek; add **CCWS-to-seawater** path; biofouling + `[VERIFY-SKKY]` thermal-discharge note | 🟡 |
| A4 | `layout/aux_systems.md` | §9 SFP cooling "→ component cooling water → ultimate heat sink"; §0 cross-refs | Clarify **CCWS final sink = seawater (normal, non-safety)**; keep SFP long-term grace on pool inertia; align "ultimate heat sink" wording with §2 | 🟡 |
| A5 | `safety/safety_criteria.yaml` | No UHS / coastal-hazard rows; rev_0 id; DiD 0 | Apply §3 fixes: add `ultimate_heat_sink` + `coastal_external_hazard`; bump `design_id`; fix S2/S3 | 🔴 |
| A6 | `safety/regulatory_alignment_audit.md` | Line 66 "UHS = seawater (C2 resolved)" | Correct to "normal sink = seawater; **safety UHS = IRWST + passive PCC**" (finding T3) | 🔴 |
| A7 | `safety/hazards_register.md` | Line 40 "coastal seawater UHS intake"; tsunami `PENDING` | Reword seawater as **normal** sink; promote coastal hazards (surge/tsunami/biofouling-blockage) to **design-basis external events** (T4) | 🟡 |
| A8 | `layout/fer_8_10_coverage.md` | R2 coverage references "TB+EHB+**CTW**" | Update building list to seawater structures | 🟢 |
| A9 | `fom/reactors/aegis40.yaml` | `plant_footprint_m2: 20000`; no water param | Reduce footprint (CTW removed), nudge `thermal_efficiency` input, **add `freshwater_consumption`** (§4.3) | 🟡 |
| A10 | `fom/parameters_schema.yaml` | No environmental/water dimension | Add `freshwater_consumption` (sustainability, min, log-ratio) **+ matching values for competitors**; optional `thermal_discharge_marine_load` | 🟡 |
| A11 | `README.md` | Line 109 open item "update PFD + layout recut after C3" | Mark Track-A done; keep Track-B pending C3 | 🟢 |
| A12 | `layout/fer_8810_docx_audit.md` | C2: "PFD still shows CT-1 — must be redrawn" | Note Track-A text done; PFD/graphics deferred to the C3 batch | 🟢 |

### 5.2 Track B — batch with the C3 TES decision (graphics)

| # | Artifact | Change | Tool |
|---|---|---|---|
| B1 | `docs/aegis40_pfd.drawio.png` (+ drawio source) | **The headline redraw.** Drop CT-1 + cooling-tower CWP loop; add seawater **intake → condenser → outfall**; CCWS to seawater. Blocks all FER §8.10 figures cut from the PFD. | draw.io |
| B2 | `layout/drawings/site_plot_plan.svg` + `.png` | Remove CTW block; add shoreline **intake + discharge + CWP house**; re-render | `layout/drawings/render.sh` |
| B3 | `layout/drawings/site_elevation.svg` + `.png` | Replace cooling-tower elevation with intake/discharge + CWP | render.sh |
| B4 | `layout/block_layout.mmd` + `.png` | Drop CT node; add intake/outfall + CWP; re-render | Mermaid |
| B5 | `layout/flow_arrows.mmd` + `.png` | Re-route condenser heat-rejection arrow CTW → sea | Mermaid |
| B6 | `cad/build_aegis40_cad.py` → `cad/aegis40_site.step` | Remove CTW solid; add intake/discharge + CWP house; rebuild STEP | build123d venv `~/.venvs/cad` |
| B7 | `site/index.html` | Drop CTW from the site viewer; add seawater structures | native SVG |

**Why Track B waits:** C3 (TES technology) directly changes the same PFD, §8.9, and the site/CAD diorama. Redrawing graphics now and again after C3 wastes effort; the text/data in Track A is C3-independent and unblocks the FER prose immediately. Trigger Track B the moment C3 closes.

### 5.3 New / changed physical scope introduced by the change

| Element | Was | Becomes | Notes |
|---|---|---|---|
| Heat-rejection structure | Mechanical-draft cooling tower (CTW, 900 m², Cat III) | **Seawater intake** (breakwater-protected, travelling screens, biofouling/chlorination) + **outfall/discharge** + **CWP house** | Akkuyu-pattern; mostly shoreline, not plant-island footprint |
| Component cooling water (CCWS) ultimate rejection | To CTW | To **seawater** (normal, non-safety) | `aux_systems.md §9`; SFP/CCWS long-term grace still on passive margins |
| New external hazards | — | Storm surge, tsunami, marine biofouling/debris/ice intake blockage | New design-basis screening (§3 `coastal_external_hazard`) |
| Effluent permitting | Plume from CT drift (water vapour) | **Thermal discharge to sea** under SKKY (max T + ΔT, real-time monitoring per Akkuyu) | `[VERIFY-SKKY]` |
| Freshwater consumption | ~2–3 % of circ flow evaporated | **≈ 0** | Sustainability gain (FOM A9/A10) |

---

## 6. Consolidated action list

**Immediate (this week, TES-independent):**
1. 🔴 `safety_criteria.yaml` — add `ultimate_heat_sink` + `coastal_external_hazard`; fix S1/S2/S3 (A5).
2. 🔴 Fix the UHS conflation in `regulatory_alignment_audit.md:66` and `hazards_register.md:40` (A6/A7).
3. 🔴 `zones.md` + `building_list.md` — swap CTW → seawater structures in text (A1/A2).
4. 🟡 FOM: stop the silent de-peak swap; report as-run + provisional (F2). Add `freshwater_consumption` (A9/A10).
5. 🟡 Tag the thermal-discharge limit `[VERIFY-SKKY]` and confirm the exact SKKY clause.

**Contingent on `peaking_recompute` (due now):** resolve whether F_q/F_ΔH are real or a mesh artifact; this gates both the safety design state (T1) and the FOM headline (F2).

**Batch with C3 (TES decision):** the full graphical recut — PFD, SVGs, CAD/STEP, viewer, Mermaid (Track B).

**For FER-grade FOM:** work the §4.4 seven-point checklist; the limits are already defensible, the weights/data/gate-handling are not.

---

## 7. Verification notes / limits of this pass

- Akkuyu cooling configuration, intake/outfall design, and the colder-Sinop efficiency argument are **web-verified** (§1 sources).
- The **exact SKKY thermal-discharge numerical limit was not machine-verifiable** in this pass — flagged `[VERIFY-SKKY]`, do not publish a number in the FER without confirming the regulation text.
- Safety-YAML findings are against the `docs/` standards as identified in `docs/_INDEX.md`; the peaking breach (T1) is a pre-existing, already-documented design issue surfaced here for FOM consistency, not a new discovery.
- No file was modified by this deliverable — it is a review document. The §5 update map is the proposed edit set for sign-off.

*End of review. 5 tasks, 9 YAML findings, 6 FOM root causes, 24 layout touch-points across 16 files.*
