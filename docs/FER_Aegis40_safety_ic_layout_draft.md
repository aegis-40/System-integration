# FER Draft — Aegis-40 — Safety, I&C & Layout sections (§8.5–8.8, §8.10)

*Consolidated draft r5, 2026-06-26. Owner: Azamhon (3S / I&C / FOM / layout).*
*r5 re-baselines to the **rev_4 37-FA core** (`docs/aegis40_neutronics_FER.ipynb`): 37 FA, 12.8 MPa, Gd 6 wt%×20, edge-pin + ring de-peaking → Table 8.5-1 + peaking status rewritten; folds in the **OpenFOAM TH results** (`docs/Aegis40_TH_report.docx`: MDNBR 1.56, fuel 734 °C, natural circulation at H_tc 4 m). Neutronic result values are [SIM-PENDING] high-stat. Full plan: `safety/SIMULATION_ANALYSIS_PLAN.md`.*
*Supersedes `docs/FER_Aegis40_8.5-8.7_draft.md` (r2) and the team's `FER_Aegis40_8.8-8.10.docx` for these sections — folds in the 2026-06-19 team decisions (**once-through seawater (C2)**, **TCES zeolite-13X (C3)**, UHS correction).*
*r4 responds to the reviewer audit: **§8.5** event-analysis matrix (8.5.2b) + coastal-hazard analysis (8.5.2c); **§8.6** six simplified event trees (8.6.5: SBLOCA, MSLB, rod-withdrawal/ATWS, SGTR, fuel-handling, marine-intake-blockage); **§8.7** trip-setpoint table (Table 8.7-1) + response-time budget closing the "≤500 ms" TBD (8.7.2a); **§8.8** six-field subsections brought into the report (8.8.1–8.8.8).*

**Covers the sections worked in this scope:** §8.5 Safety Criteria · §8.6 Reactor Safety Systems Design · §8.7 Instrumentation & Control · §8.8 Auxiliary Systems · §8.10 Facility Layout. **Adjacent sections** (§8.1–8.4 core/fuel/cooling, §8.9 energy conversion, §8.11 waste, §8.12 economics) are covered by *notes* at the end — they belong to other team scopes (Samira: core/fuel; Adilbek: thermal-hydraulics/cooling; Alisher: energy/TES/SOE) but are touched here where the safety/layout case depends on them.

**Marker convention** (all must be resolved or accepted before submission):
- ***[SIM-PENDING — …]*** value awaits a scoped-but-unrun simulation
- ***[ANALYSIS-PENDING — …]*** analysis identified, not yet performed
- ***[VERIFY — …]*** claim believed correct but lacking a citable anchor
- ***[DECISION-PENDING — …]*** team decision open; text written against the stated baseline
- ***[ALISHER]/[ADILBEK]/[SAMIRA]*** value owned by a teammate's scope

> **Non-proliferation note.** The Aegis-40 fuel cycle is once-through, boron-free, high-burnup, with **no separated-fissile stream anywhere in the plant**; discharged material is reactor-grade and self-protecting (§8.11 note; `safety/safeguards_nonproliferation.md`). The cogeneration and cooling systems described here are secondary-side / balance-of-plant and have no proliferation relevance.

---

## 8.5 Safety Criteria

### 8.5.1 Criteria framework

The Aegis-40 safety basis is expressed as **34 numeric criteria in eight categories** (reactivity/neutronics, thermal-hydraulics, pressure boundary, decay-heat removal & ultimate heat sink, radiological/site, seismic & external hazards, fuel cycle, cogeneration interface), maintained as a machine-readable single source of truth (`safety/safety_criteria.yaml`) from which the protection-system setpoints (§8.7) and the figure-of-merit hard constraints (§8.12 note) are derived. Each criterion is classified as a **hard constraint** (breach disqualifies the design — pass/fail, never traded), an **operating limit** (breach demands protective action), or a **target** (scored against reference SMRs: CAREM-25, SMART, NuScale VOYGR). Every criterion carries its regulatory source and, where protective action is required, the crediting trip function [SSR-2/1; NUREG-0800].

### 8.5.1a Plant states and design extension conditions

Following IAEA SSR-2/1 Req 13 and Req 20, plant conditions are classified into standard categories, each with its own acceptance criteria:

| Plant state | Definition | Representative Aegis-40 events | Acceptance criterion |
|---|---|---|---|
| Normal operation | within operational limits & conditions | power operation, **TCES-buffered load-follow**, cogen dispatch | OLCs respected |
| Anticipated operational occurrences (AOO) | expected ≥1× in plant life | turbine trip, loss of normal feedwater, uncontrolled rod withdrawal, **loss of seawater intake** | no fuel failure; MDNBR ≥ 1.3 |
| Design basis accidents (DBA) | postulated single faults | small-break LOCA, main-steam-line break | limited fuel damage; dose ≤ 10 CFR 100 |
| **Design extension — DEC-A** (no significant fuel degradation) | multiple-failure / low-frequency | ATWS, station blackout beyond design, total loss of feedwater | core remains coolable; containment intact |
| **Design extension — DEC-B** (severe accident) | core-degradation sequences | postulated core melt | containment integrity preserved; large release **practically eliminated** |

The two analyzed event trees map onto this scheme: **LOHS** spans AOO→DEC-A, and **SBO** is a DEC-A sequence the de-energize-to-actuate design renders benign (§8.6.3). ATWS is the DEC-A sequence closed by the diverse second shutdown system (§8.6.2a). **Note that "loss of normal heat sink" (loss of seawater or condenser) is an AOO/power-conversion event, not a safety challenge** — decay-heat removal is passive and seawater-independent (§8.5.2a, §8.6.2).

**Events removed by "practical elimination" (SSR-2/1 §5.31)** — excluded by physical construction, not by probability:

| Practically eliminated event | Deterministic basis |
|---|---|
| Large-break LOCA | integral RPV — no large-bore primary piping exists (§8.6.1) |
| Control-rod ejection | internal (in-vessel) CRDMs — no ejection path exists (§8.6.1) |
| Boron-dilution accident | soluble-boron-free reactivity control — no dilution pathway (§8.6.1) |
| Pressurizer surge-line break | integral pressurizer in the RPV head — no external surge line (§8.6.1) |

### 8.5.2 Principal criteria and demonstrated margins

Table 8.5-1 presents the principal criteria for the locked core design (**rev_4: OpenMC 37-assembly 7-wide octagonal core, 12 control-rod clusters, 12.8 MPa, 200 cm active, three-zone 4.95/4.70/4.40 wt% + FA-perimeter edge-pin 3.6 wt% + ring zoning for boron-free de-peaking, Gd₂O₃ 6 wt%×20 + Er₂O₃ 0.5 wt%×16, soluble-boron-free**). Neutronic result values (k_eff, coefficients, SDM, peaking, burnup, cycle) are being re-run on this 37-FA core — **medium statistics done, high statistics (STAT_FINAL) running** — so they carry *[SIM-PENDING]* until the high-stat pass lands; the thermal-hydraulic results below are from the completed OpenFOAM study (`docs/Aegis40_TH_report.docx`).

**Table 8.5-1. Principal safety criteria and demonstrated values.**

| Criterion | Limit | Value (rev_4, 37-FA) | Margin | Source |
|---|---|---|---|---|
| Shutdown margin (stuck rod) | ≥ 1 % Δk/k | *[SIM-PENDING — 37-FA re-run]* | — | NRC SRP 4.3 |
| Moderator temperature coeff. (HFP) | < 0 | *[SIM-PENDING]* (SBF ⇒ strongly negative by design) | — | GDC-11 |
| Doppler coefficient | < 0 | *[SIM-PENDING]* (UO₂ ⇒ negative by design) | — | GDC-11 |
| Void coefficient | < 0 | *[SIM-PENDING]* (under-moderated ⇒ negative) | — | GDC-11 |
| Control-rod worth (ARO) | ≥ 5 % Δk/k | *[SIM-PENDING — 37-FA, 12 CRA]* | — | SRP 4.3 |
| Max reactivity insertion rate | ≤ 7.5e-4 Δk/k/s | **1.5e-5** (CRDM design input) | ×50 | ANSI/ANS-58.21 |
| F_Q(Z) total peaking | ≤ 2.50 (LCO) | **2.00 design target** (de-peaked) *[SIM-PENDING high-stat]* | +20 % | NUREG-1431 LCO 3.2.1 |
| F_ΔH radial peaking | ≤ 1.65 (LCO) | **1.55 design target** (de-peaked) *[SIM-PENDING high-stat]* | +6 % | NUREG-1431 LCO 3.2.2 |
| MDNBR (steady) | ≥ 1.3 | **1.56** (OpenFOAM, nat-circ design point) | **+20 %** ✅ | SRP 4.4 / 15.0 |
| MDNBR (AOO transient) | ≥ 1.3 | *[SIM-PENDING — OpenFOAM transient F2]* | — | SRP 15.0 |
| Peak fuel centreline (steady) | < 2590 °C | **734 °C** (OpenFOAM) | ≫ margin ✅ | NRC SRP 4.2 |
| Peak clad (steady operating) | — | **349 °C** (OpenFOAM, subcooled-boiling) | — | — |
| PCT (LOCA envelope) | ≤ 1204 °C | *[SIM-PENDING — SBLOCA transient F3]* (operating 349 ≪ 1204) | — | 10 CFR 50.46(b)(1) |
| Cladding oxidation / H₂ generation | ≤ 17 % / ≤ 1 % | *[SIM-PENDING — F3]* | — | 50.46(b)(2,3) |
| Primary design pressure | ≤ 14.1 MPa | 12.8 MPa operating | 110 % per ASME III | ASME III |
| Containment design pressure | ≤ 0.414 MPa | [ANALYSIS-PENDING — P/T response F6] | — | SSR-2/1 Req 56 |
| **Safety ultimate-heat-sink grace** | ≥ 72 h passive, **no seawater/AC** | 72 h by design intent *[F5 transient pending]* | — | SSR-2/1 Req 53 |
| Natural-circulation flow | adequate at design point | **G 542, MDNBR 1.56 at H_tc 4 m** (OpenFOAM) ✅ | — | iPWR design |
| Peak-rod discharge burnup | ≤ 62 GWd/MTU | *[SIM-PENDING — 37-FA depletion]* (rev_3 was 42.8) | — | SRP 4.2 |
| Max enrichment | ≤ 5.0 wt% | **4.95 wt%** (design input) | 0.05 wt% — see note | 10 CFR 50 LEU |
| Cycle length | ≥ 365 EFPD | *[SIM-PENDING — 37-FA depletion]* (rev_3 was 479) | — | competition target |
| SSE | ≥ 0.3 g | 0.3 g design basis | — | RG 1.60; SSG-9 |
| **Coastal external hazard** | protected to site DBFL | [ANALYSIS-PENDING — Sinop surge/tsunami study] | — | SSR-1; SSG-9 |
| Boundary dose (DBA, 0–2 h) | ≤ 0.25 Sv TEDE | [ANALYSIS-PENDING — dispersion O1] | — | 10 CFR 100.11 |
| CDF / LRF | < 1e-7 / < 1e-8 /ry | partial: LOHS ~1e-8 + SBO ~1e-11 (§8.6) | — | RG 1.174 |

**Peaking status (rev_4 — the de-peaking is now in the design).** The rev_3 (21-FA) as-run peaking exceeded the LCOs (F_Q 3.478, F_ΔH 2.268). The rev_4 37-FA design **resolves this at the input level**: (i) the larger 37-assembly core halves the per-pin power (peak linear power 24.6 → 12.8 kW/m); (ii) boron-free de-peaking is built in — FA-perimeter edge-pin de-rate (3.6 wt%), assembly-ring enrichment zoning {4.95/4.70/4.40/4.00}, and Gd ring-zoning; (iii) the tally artifact is removed (pin-by-pin reconstruction; F_Q reported as the separable F_ΔH·F_z). The design-target peaking is **F_Q 2.00 / F_ΔH 1.55**, and the OpenFOAM hot-channel study computed at that peaking gives **MDNBR 1.56 (PASS, +20 %)** with peak fuel only 734 °C. **Remaining:** the OpenMC high-statistics run (STAT_FINAL) must confirm F_Q ≈ 2.0 / F_ΔH ≈ 1.55 on the 37-FA core — the MDNBR PASS is contingent on it (the **F1↔N6 coupling**, `safety/SIMULATION_ANALYSIS_PLAN.md`). The design is no longer gate-failing by construction; it awaits the high-stat confirmation. This is disclosed, not hidden.

**Enrichment margin note.** The 4.95 wt% peak zone deliberately approaches the 5.0 wt% LEU ceiling to maximise discharge burnup. The remaining 0.05 wt% equals a typical fabrication tolerance (±0.05 wt%); the fuel spec therefore requires an asymmetric band (−0.10/+0.00 wt%) **[VERIFY — to be stated in the mechanical/fuel section]**.

### 8.5.2a Heat-sink architecture — two distinct sinks (do not conflate)

Per SSR-2/1 Req 52–53 the design distinguishes:

- **Normal heat sink = the Black Sea, once-through seawater** (condenser + CCWS + TCES rejection). **Non-safety-classified**, graded per TECDOC-1936 because the safety function does not depend on it.
- **Safety ultimate heat sink = the passive IRWST + containment cooling** (atmosphere-coupled), **independent of seawater**, supporting the ≥72 h grace.

Consequently, **loss of the seawater intake** (storm surge, biofouling, jellyfish/algal bloom, debris, ice) or **loss of TCES** is a power-conversion event that does **not** challenge the safety UHS. This corrects an earlier terminology conflation and is enforced by `safety_criteria.yaml` `ultimate_heat_sink`.

### 8.5.2b Postulated-event analysis matrix (AOO / DBA / DEC)

The competition template requires modeling **and results** for AOOs, criticality accidents, DBAs and worst-case scenarios. Table 8.5-2 is the analysis matrix: each postulated event carries its **method**, **acceptance criterion**, and **result status** — where a thermal-hydraulic number awaits a simulation, the row states the **method that will produce it** and the **bounding/interim argument** that holds in the interim, so the safety case is structured and defensible rather than blank. The corresponding event sequences are in §8.6.5.

**Table 8.5-2. Postulated-event analysis status.**

| Event (class) | Analysis method | Acceptance criterion | Result / interim bounding argument |
|---|---|---|---|
| Rod withdrawal (AOO) | OpenMC reactivity + transient | MDNBR ≥ 1.3 | insertion rate 1.5e-5 vs 7.5e-4 limit → **×50 margin (demonstrated)**; flux-rate trip |
| Loss of feedwater / LOHS (AOO→DEC-A) | event tree (done) | core coolable | **CDF ≈1e-8/ry (demonstrated)**, §8.6.3 |
| Station blackout (DEC-A) | event tree (done) | core coolable, 72 h | **CDF ≈1e-11/ry (demonstrated)**, de-energize-to-actuate |
| MSLB / overcooling (DBA) | OpenMC cooldown + OpenFOAM | no return to criticality; MDNBR ≥1.3 | *[SIM-PENDING]* — interim: **SDM 12.4 %** bounds cooldown reactivity; MSI isolates; EBIS backstop (§8.6.5b) |
| SBLOCA (DBA) | OpenFOAM blowdown/reflood | **PCT ≤ 1204 °C**; clad oxidation ≤17 %; H₂ ≤1 % | *[SIM-PENDING]* — interim: integral RPV caps break size; passive gravity SI; small nozzle break only |
| SGTR (DBA) | dose + inventory | offsite dose ≤ 10 CFR 100 | *[ANALYSIS-PENDING]* — interim: SI holds inventory; affected-SG + cogen isolation (§8.6.5d) |
| ATWS (DEC-A) | OpenMC borated-core | coolable; RCS P < limit | *[SIM-PENDING EBIS sizing]* — interim: negative MTC self-limits; DAS+EBIS diverse shutdown (§8.6.2a) |
| Fuel-handling accident | source-term + dispersion | offsite dose ≤ 10 CFR 100 | *[ANALYSIS-PENDING]* — interim: interlocks + pool scrub + HEPA/charcoal (§8.6.5e) |
| Criticality (SFP) | OpenMC storage-rack | k_eff(95/95) ≤ 0.95 unborated | method replicated (Cabrera 2023); fixed-absorber geometry + burnup credit (§8.8.6) |
| Containment response (DBA) | mass-energy → P/T | peak P ≤ 0.414 MPa | *[ANALYSIS-PENDING]* — gated on C5 containment concept |
| Boundary dose (DBA 0–2 h) | atmospheric dispersion | ≤ 0.25 Sv TEDE | *[ANALYSIS-PENDING]* — from rev_3 source term 1.2e17 Bq |
| Coastal external hazard | site flood/surge study | protected to DBFL | *[ANALYSIS-PENDING]* — see §8.5.2c |

**The honest framing for a reviewer:** the demonstrated results (reactivity margins, LOHS/SBO CDF, SFP criticality method) are complete; the pending rows are **simulation-limited, not analysis-undefined** — each names its code and its interim bounding argument. Closing them is the W-phase simulation campaign (priority MSLB→SBLOCA→containment→dose).

### 8.5.2c Coastal external hazards (Sinop)

The coastal Black Sea site introduces design-basis external events not present for an inland plant, screened per SSR-1 / SSG-9 and entered as criterion `coastal_external_hazard`:

| Hazard | Provision | Status |
|---|---|---|
| Extreme sea level / storm surge | safety SSCs on dry-site grade **above the design-basis flood level (DBFL)** | *[ANALYSIS-PENDING — Sinop DBFL study]* |
| Tsunami | Black Sea tsunamigenic potential is low but non-zero; bound by the same dry-site grade + DBFL | *[ANALYSIS-PENDING]* |
| Marine intake blockage (biofouling / jellyfish / algal bloom / debris / ice) | redundant intake bays + travelling screens + chlorination; **CCF of the normal sink only** — safety UHS is seawater-independent (§8.5.2a) | **CARRIED** — bounded by `ultimate_heat_sink`, analyzed §8.6.5f |
| Coastal storm / extreme wind | Seismic Cat-I NI structures bound wind loads | *[ANALYSIS-PENDING — site wind spectrum]* |

The decisive point: the only coastal hazard that could touch core cooling — intake blockage — is **defeated by the passive, seawater-independent safety UHS**, so coastal siting adds external-event screening work but does not weaken the core-cooling safety case. *Realism anchor:* Akkuyu (4×VVER-1200) licenses once-through Mediterranean seawater on the same coast; the breakwater + travelling-screen + chlorination intake-protection scheme is established Turkish practice.

### 8.5.3 Defence in depth

The criteria map onto the five IAEA defence-in-depth levels [SSR-2/1 §2.13]: Level 1 prevention via inherently negative feedback (MTC/DTC/void all negative, demonstrated) and DNB margin; Level 2 control via the reactor protection envelope (§8.7); Level 3 DBA control by passive ECCS, EFW and PRHR (§8.6); Level 4 severe-accident management via the ≥72 h no-operator-action grace and three passive containment-cooling trains; Level 5 mitigation via the site-boundary EPZ (≤0.5 km, *[ANALYSIS-PENDING — dose basis]*).

---

## 8.6 Reactor Safety Systems Design

### 8.6.1 Accident-prevention strategy: elimination before mitigation

Aegis-40 **removes classes of design-basis events by construction**:

1. **Large-break LOCA — eliminated.** The integral RPV contains the core, two helical-coil once-through steam generators and the pressurizer within one pressure boundary; no large-bore primary piping exists. The limiting LOCA reduces to a small break at instrument/injection nozzles.
2. **Rod ejection — eliminated.** CRDMs are **internal (in-vessel)**; no head-mounted housing exists whose rupture could provide an ejection path. The bounding reactivity insertion becomes uncontrolled rod *withdrawal* (AOO); demonstrated insertion rate 1.5e-5 Δk/k/s holds ×50 margin. **[VERIFY — internal-CRDM statement to be anchored in the mechanical design basis with a configuration sketch.]**
3. **Boron-dilution — eliminated.** Soluble-boron-free core; no dilution pathway. Hold-down by hybrid Gd₂O₃/Er₂O₃ burnable absorber + control rods.
4. **Pressurizer surge-line break — eliminated.** Integral pressurizer in the RPV head; no external surge line.

### 8.6.2 Engineered safety features (passive)

All credited ESF are passive and de-energize-to-actuate (§8.7.2):

- **Emergency Feedwater (EFW)** — gravity-driven from an elevated tank; isolation valves fail open; no pumps. Sized for 72 h of decay-heat steaming *[ANALYSIS-PENDING — tank inventory calc]*.
- **Passive Residual Heat Removal (PRHR)** — two 100 % natural-circulation trains, RPV → HX submerged in the IRWST; each removes ≥105 % of decay heat at actuation. Governing decay-heat source **7.75 MW at shutdown (6.2 % of 125 MWth)**, full-chain depletion (rev_3), cross-validated to ANS-5.1.
- **Passive containment cooling** — three trains; condensate return maintains the IRWST as the ≥72 h heat sink. **This — not the seawater system — is the safety ultimate heat sink (§8.5.2a).**
- **Passive safety injection** — gravity feed from IRWST on low pressurizer pressure+level coincidence.
- **Containment:** dry steel-lined, Ø15 m, design pressure 0.414 MPa. **[DECISION-PENDING C5 — a NuScale-style submerged-pool configuration is under team evaluation; this section is written against the dry-containment baseline; containment text, PCC description and Figures 8.6-x revise if the pool concept is adopted.]**

### 8.6.2a Reactor shutdown — two diverse and independent means

IAEA SSR-2/1 Req 46 (§6.9) requires ≥2 diverse, independent shutdown systems, one able alone to hold the core subcritical at its most reactive state (§6.10):

1. **Control rods (primary).** Gravity-drop on de-energization via RPS or DAS; cold stuck-rod SDM 12.4 %.
2. **Emergency Boron Injection System (EBIS) — diverse second system.** Passive, shutdown-only borated-water (gravity head / N₂ accumulator, fail-open isolation), **isolated and dormant in normal operation**, armed only on an ATWS signature by the Diverse Actuation System (§8.7.4). Diverse from the rods in principle (liquid poison vs mechanical insertion) → no shared rod-insertion CCF (§6.8).

Achieved **without compromising the soluble-boron-free design**: normal coolant stays boron-free (boron-dilution accident stays eliminated, MTC stays strongly negative); boron is solely the dormant emergency reserve — the BWR standby-liquid-control principle. EBIS boron mass/concentration being sized for standalone cold subcriticality *[SIM-PENDING — OpenMC borated-core case]*.

### 8.6.3 Analyzed events — event-tree results

Two initiators analyzed to event-tree depth, chosen to exercise the passive chain end-to-end [WASH-1400; NUREG/CR-6928]; top-event demands map 1:1 onto §8.7 trip/ESF functions.

**Loss of Heat Sink (LOHS)** — loss of main feedwater/condenser (which now includes loss of the once-through seawater intake). Seven sequences (4 safe, 3 core-damage); all CD sequences require ≥2 independent failures; per-initiator CDF ≈ **1e-8/ry** *[PRA-PENDING — generic reliability data]* — an order inside the 1e-7 target (Figure 8.6-1, `event_tree_LOHS`). Critically, the lead safe path is the **passive PRHR/IRWST**, which is **seawater-independent** — loss of the marine intake degrades only the normal (power) sink.

**Station Blackout (SBO)** — LOOP + failure of both standby AC sources (≈1e-5/ry). Every credited function actuates on de-energization (breakers open, rods drop, EFW/PRHR valves fail open, CIVs fail closed) → **loss of power is actuation, not challenge**. No AC, DC, operator action or external water for 72 h; Class 1E batteries (72 h) serve post-accident monitoring only [RG 1.97]. SBO CDF ≈ **1e-11/ry** — four orders below target (Figure 8.6-2, `event_tree_SBO`). ATWS under SBO is backstopped by EBIS (§8.6.2a): mechanical rod-insertion CCF (~1e-6 conditional **[VERIFY — CCF data source]**) is covered by DAS-actuated boron injection, sharing no failure mode with the rods — per 10 CFR 50.62.

**Remaining DBA spectrum — screening status.** PIE list from NUREG-0800 SRP Ch. 15 categories [SSR-2/1 Req 16, 19]. Identified and screened, not yet analyzed to tree depth; priority **MSLB first** then **SBLOCA**:

| Initiator | Why it matters here | Status |
|---|---|---|
| Small-break LOCA | only surviving LOCA class | [ANALYSIS-PENDING — tree planned next] |
| MSLB / excess steam demand | with MTC −35.9 pcm/K, overcooling is the limiting reactivity transient | [ANALYSIS-PENDING] |
| Uncontrolled rod withdrawal | surviving reactivity AOO after ejection elimination | [ANALYSIS-PENDING — bounded by insertion-rate margin] |
| Loss of primary flow / blockage | natural-circulation primary; flow-degradation screening | [ANALYSIS-PENDING — screening] |
| Marine intake blockage (biofouling/debris/ice) | CCF of the *normal* sink; bounded by passive UHS | CARRIED (§8.5.2a) — screening doc'd |
| Fuel-handling accident | SFP/cask operations | [ANALYSIS-PENDING — ties to §8.8.7] |

### 8.6.4 Redundancy and necessity

For each credited system the design demonstrates redundancy (what backs it up) and necessity (what fails without it); the LOHS and SBO sequence tables show **no single failure leads to core damage** — the single-failure criterion is met at the accident-sequence level, not merely the component level (`event_tree_LOHS.md` §6, `event_tree_SBO.md` §6).

### 8.6.5 Postulated-event analysis — simplified event sequences

Beyond the two fully-developed event trees (LOHS, SBO), the remaining SRP-Ch.15 initiators are analyzed here at **simplified sequence-table depth**: each lists the protective functions challenged (top events, mapping 1:1 onto the §8.7 trips/ESF), the success path, the failure consequence, the acceptance criterion, and a qualitative frequency. Quantitative confirmation of the flagged thermal-hydraulic numbers is *[SIM-PENDING — OpenFOAM]*; the **logic and success paths are design-frozen**. Top-event abbreviations: **RT** reactor trip (scram), **SI** passive safety injection (E1), **CI** containment isolation (E2), **EFW** emergency feedwater (E3), **PRHR** passive residual-heat removal (E4), **MSI** main-steam isolation (E5), **EBIS** diverse boration (E6).

**(a) Small-break LOCA (SBLOCA)** — *the only surviving LOCA class; initiator ≈1e-3/ry.*

| Top events (in order) | Success path | Failure → outcome | Acceptance |
|---|---|---|---|
| RT → SI → PRHR → CI | scram on low-pzr-P (trip 10); passive SI from IRWST maintains inventory by gravity; PRHR removes decay heat to IRWST; CI limits release | SI fail (passive, gravity — very low p) → slow uncovery → DEC-A | core stays covered; **PCT ≤ 1204 °C** *[SIM-PENDING]*; dose ≤ 10 CFR 100 |

*Aegis feature:* the integral RPV caps break size — there is no large break, so the limiting LOCA is a small nozzle break with a slow, gravity-injection-mitigated response. CDF contribution low (requires passive-SI + PRHR both to fail).

**(b) Main steam line break (MSLB) / excess steam demand** — *the limiting OVERCOOLING transient; initiator ≈1e-3/ry.*

| Top events | Success path | Failure → outcome | Acceptance |
|---|---|---|---|
| RT → MSI (isolate broken line) → (SDM holds) → SI | scram (low SG P / high containment P); MSI (E5) closes MSIVs, stops the blowdown; cold stuck-rod **SDM 12.4 %** holds the cooldown-induced reactivity subcritical | MSI fail + return-to-power → EBIS borates | no return to criticality; **MDNBR ≥ 1.3**; no fuel failure |

*Aegis feature & the key caveat:* the strongly negative **MTC (−35.9 pcm/K)** that suppresses heat-up transients works *against* us in a cooldown — it inserts positive reactivity. The defense is the large **SDM (12.4 %)** plus MSI. **[SIM-PENDING — confirm SDM bounds the MSLB cooldown reactivity worth; OpenMC cooldown case.]** This is the transient where the boron-free design must be shown robust; EBIS is the backstop.

**(c) Uncontrolled rod withdrawal & ATWS** — *surviving reactivity AOO + its without-scram extension.*

| Case | Top events | Success path | Acceptance |
|---|---|---|---|
| Rod withdrawal (AOO) | RT (flux-rate trip 3 / OPΔT trip 6) | scram before limit; insertion rate **1.5e-5 Δk/k/s** holds **×50** margin to 7.5e-4 limit | MDNBR ≥ 1.3; no fuel failure |
| **ATWS** (rods fail to insert, CCF ~1e-6) | inherent MTC self-limit → DAS detect → EBIS | negative MTC throttles power on heat-up; PORV (trip 9) caps pressure; **DAS** detects ATWS signature; **EBIS** brings cold-subcritical (diverse, no shared CCF) | coolable core; RCS P < limit (per 10 CFR 50.62) |

*Detailed in §8.6.2a. The ATWS path is the design's diverse-shutdown showcase.*

**(d) Steam generator tube rupture (SGTR)** — *primary→secondary leak; radiological focus; initiator ≈1e-3/ry.*

| Top events | Success path | Failure → outcome | Acceptance |
|---|---|---|---|
| RT → SI → isolate affected SG (MSI) → cogen-interface isolation | scram; SI maintains primary inventory; MSI (E5) + affected-SG isolation stop the release path; **cogen interface isolates on SGTR signal** (§8.8.9) | failure to isolate → prolonged release | **offsite dose ≤ 10 CFR 100**; primary inventory maintained |

*Aegis feature:* helical-coil OTSGs; the SGTR signal is also a credited input to the Req-35 cogeneration-interface isolation, so a tube rupture cannot propagate activity to the district-heat/H₂ product.

**(e) Fuel-handling accident** — *assembly drop during refueling/cask ops; initiator ≈1e-4/ry.*

| Barriers (no scram — reactor shut down) | Success path | Acceptance |
|---|---|---|
| handling interlocks → pool water depth → SFB HVAC/filtration | single-failure-proof handling machine + safe-load-path interlocks (no heavy load over irradiated fuel); deep SFP water scrubs iodine; HEPA + charcoal on SFB exhaust | **offsite dose ≤ 10 CFR 100** with margin; small EPZ (≤0.5 km) |

*Aegis feature:* unborated SFP subcriticality is held by fixed-absorber rack geometry + burnup credit (k_eff(95/95) ≤ 0.95), so a drop does not create a criticality concern (§8.8.6).

**(f) Marine intake blockage** — *NEW with once-through seawater; biofouling / jellyfish / algal bloom / debris / ice; credible frequency.*

| Top events | Success path | Failure → outcome | Acceptance |
|---|---|---|---|
| (loss of normal heat sink) → RT → EFW → PRHR | redundant intake bays + travelling screens + chlorination defend the intake; total loss → low SG level (trip 11) scrams → EFW then **PRHR/IRWST** carry decay heat | — | **bounded by LOHS**; core coolable ≥72 h via the **passive, seawater-independent UHS** |

*Aegis feature & the decisive point:* loss of the seawater intake is loss of the **normal** heat sink only — a power-conversion event. The **safety** ultimate heat sink is the passive IRWST/PCC (§8.5.2a), which needs no seawater. So even a *total, permanent* intake blockage degrades only electricity production, never core cooling. This is the single clearest demonstration that the seawater-cooling decision did not weaken the safety case.

**Screening summary.** All six initiators reach a defined safe state through already-credited functions; none introduces a new safety system. Full quantitative event trees for (a)–(d) are prioritized MSLB→SBLOCA→SGTR→ATWS as the OpenFOAM/OpenMC results land; (e)–(f) are bounded by existing analyses (dose limit / LOHS) and need no separate tree.

---

## 8.7 Instrumentation and Control System Design

### 8.7.1 Architecture

Five layers with strict downward non-interference [SSG-39; IEC 61513]: Layer 1 field instrumentation (**21 measurement channels, 14 Class 1E**, +5 planned); Layer 2 Reactor Protection System; Layer 3 ESFAS; Layer 4 Distributed Control System (non-safety); Layer 5 digital twin (advisory, read-only). Signals flow **upward only**: protection layers receive sensor signals directly from Layer 1; **no software path exists from non-safety into Class 1E** — the DCS taps sensor circuits through qualified one-way isolation; the digital twin is fed through a unidirectional data diode [IEEE 603; IEEE 384; 10 CFR 73.54]. Figure 8.7-1 (`ic_block`).

### 8.7.2 Reactor Protection System

Four independent divisions (A–D) with **2-of-4 coincidence voting** satisfy the single-failure criterion in both trip and trip-prevention directions, including one channel out for maintenance [IEEE 603 §5.1]. **De-energize-to-trip**: breakers normally energized; any loss of power/air/signal scrams; rods insert by gravity [IEC 61513 §5.3.6]. Platform: safety-qualified FPGA/PLC, IEC 60880 Category A software (no dynamic memory, no recursion; independent V&V). Deterministic timing: division scan+vote ≤ 100 ms; sensor-threshold-to-breaker ≤ 500 ms (the bound assumed in §8.6) — **allocated in §8.7.2a (Table 8.7-1 + response-time budget)**, closing the prior TBD. Per-channel accuracy is in `ic/sensor_inventory.md`; total channel setpoint uncertainty per ISA-67.04 / RG 1.105 *[remaining: formal uncertainty roll-up once §8.7.7 EQ envelope closes]*.

**Table 8.7-1. Reactor trip setpoints, logic, and total response time.** (Full traceability + ESF actuations E1–E6 in `safety/trip_signals.md`; sensor channels in `ic/sensor_inventory.md`. Setpoints marked *[SIM]* are preliminary, pending OpenMC/OpenFOAM; the **logic, voting, and safe state are design-frozen**.)

| # | Monitored variable | Sensor | Setpoint | Logic | Protective action | TRT | Safe state |
|---|---|---|---|---|---|---|---|
| 1 | Power-range flux (high) | NF-PR | 118 % *[SIM]* | 2/4 | scram | ≤500 ms | rods in |
| 2 | Power-range flux (startup) | NF-PR | 25 % | 2/4 | scram | ≤500 ms | rods in |
| 3 | Intermediate-range flux rate | NF-IR | +5 %/s | 1/2 | scram | ≤500 ms | rods in |
| 4 | Source-range flux | NF-SR | 1e5 cps | 1/2 | scram | ≤500 ms | rods in |
| 5 | OTΔT (DNB protection) | T-HL,T-CL,NF-PR,P-PZR | composite *[SIM]* | 2/4 | scram | ≤500 ms | rods in |
| 6 | OPΔT (LHR/centerline) | T-HL,T-CL | composite *[SIM]* | 2/4 | scram | ≤500 ms | rods in |
| 7 | Core-exit / hot-leg T | T-HL,T-CE | 312 °C *[SIM]* | 2/4 | scram | ≤500 ms | rods in |
| 8 | Primary flow (low) | F-LP | 90 % | 2/4 | scram | ≤500 ms | rods in |
| 9 | Pressurizer P (high) | P-PZR | 16.5 MPa | 2/4 | scram + PORV | ≤500 ms | rods in / PORV open |
| 10 | Pressurizer P (low) | P-PZR | 12.5 MPa | 2/4 | scram + SI | ≤500 ms | rods in / SI |
| 11 | SG level (low) | L-SG-NR | 15 % NR | 2/4 | scram + EFW + PRHR | ≤500 ms | rods in / EFW |
| 12 | Containment P (high) | P-CONT | 0.17 MPa | 2/3 | scram + CI + SI | ≤500 ms | rods in / isolated |
| 13 | Manual | hardwired | operator | 1/2 | scram | — | rods in |

### 8.7.2a Total response time — closing the "≤500 ms" allocation

The §8.6 transients assume protective action completes within **500 ms of threshold crossing**. That bound (previously a TBD) is now closed by the allocation below; every actuated device fails to its safe state on loss of motive power, so the times are upper bounds, not best-estimates [ISA-67.04; RG 1.105].

| Stage | Allocation | Basis |
|---|---|---|
| Sensor + transmitter electrical response | ≤ 150 ms | fast for flux/pressure; RTD thermal lag is carried as a *process* time constant in the T-H model, not in the trip-channel time *[VERIFY — per-channel constants]* |
| Signal conditioning + setpoint comparison | ≤ 50 ms | qualified FPGA/PLC |
| Division scan + 2/4 voting | ≤ 100 ms | deterministic cycle (§8.7.2) |
| Trip-breaker opening + rod release | ≤ 200 ms | undervoltage + shunt breakers |
| **Total response time (threshold → rods released)** | **≤ 500 ms** | the §8.6 analysis bound |

Rod **free-fall insertion** to the dashpot (~2.5 s *[SIM-PENDING — drop-time test/sim]*) is **additional** to this 500 ms and is modeled explicitly in the transient analyses, not folded into the trip response. Total channel uncertainty (setpoint + drift + accuracy) will be tabulated per the ISA-67.04 setpoint methodology with the §8.7.7 accuracy figures.

### 8.7.3 ESFAS

Same 4-division/2-of-4 structure; actuations **latching** (deliberate operator reset). Functions: passive safety injection (low pzr P + level), containment isolation (high containment P or radiation), EFW (low SG level / loss of normal FW), PRHR/PCC alignment (low SG level + EFW unavailable, or high core-exit T post-scram), main-steam isolation (high MSL radiation or containment P), and **cogeneration-interface isolation** (fail-closed on high intermediate-loop/product activity or SGTR — see §8.8.9, Req 35). All actuated devices move to safe state on loss of motive power.

### 8.7.4 Diverse Actuation System

Class 1E but **platform-diverse** (different technology and team from RPS) covering postulated CCF of all four RPS divisions [SECY-93-087; BTP 7-19; SSG-39 §6]. Monitors power-range flux and pressurizer pressure through fixed hardware-biased logic, setpoints staggered beyond the RPS envelope; diverse paths to trip breakers, SI/PRHR, and **EBIS (§8.6.2a)** on an ATWS signature (high flux/temperature with no rod insertion confirmed). *Sufficiency: monitored variables bound the high-consequence CCF families (overpower, loss-of-coolant/overpressure); [VERIFY — defend variable sufficiency against the §8.6.3 screened-initiator list once those close].* The DAS is the **sole actuation path for EBIS**, which carries the ATWS burden in this boron-free core.

### 8.7.5 Control room, control philosophy and human factors

Two-operator MCR per NUREG-0700: reactor-operator + BOP consoles, STA read-only station, 4×80″ overview wall (plant mimic, SPDS, critical safety functions). Alarm management per ISA 18.2 (≤10 alarms / 10-min window under DBA transients). Computer-based procedures with paper backup. **Hardwired, software-independent manual actions** — reactor trip, SI, CI, EFW, MSIV closure — per IEEE 603 §5.8. A **Remote Shutdown Station**, physically/electrically separated (separate fire area, independent 1E division), provides post-accident monitoring (RG 1.97) + diverse manual trip/ESF (incl. EBIS) to reach and hold safe shutdown if the MCR is uninhabitable [SSR-2/1 Req 65–66]; its scope is minimal because the plant is passively safe for ≥72 h without operator action.

**Load-following control philosophy (originality).** Plant load-following is achieved primarily through the **TCES buffer (§8.9 note)**, not through deep reactor power maneuvering: the reactor is held near baseload while the thermochemical store absorbs the dispatch swing (charge = divert surplus steam to dehydrate the zeolite bed; discharge = hydrate to district heat). This keeps the reactor in the regime where its negative feedbacks and power distribution are best-characterized, and **does not aggravate the peaking/xenon/MTC challenges** — a control-side safety benefit. The DCS coordinates turbine-throttle, TCES charge/discharge valving, and the cogen-interface isolation interlocks.

### 8.7.6 Digital twin (advisory) — originality feature

A non-safety digital twin mirrors all Layer 1 signals through the data diode and provides soft sensors (MDNBR, fuel-centreline estimates), anomaly detection and predictive maintenance. Category C software; cannot actuate any device; presents alongside (never in place of) qualified indications. Enables condition-based maintenance and reduced-staffing operation without touching the Layer 1–3 safety qualification — cf. NuScale's ISV-validated reduced-staffing precedent [NUREG-0711].

### 8.7.7 Qualification

Class 1E: environmental qualification per IEEE 323 (150 °C, 0.5 MPa, 100 % steam, 1 MGy lifetime, jet impingement where exposed) *[VERIFY — envelope to confirm against the containment P/T analysis]*; seismic per IEEE 344 at SSE 0.3 g; cybersecurity per 10 CFR 73.54 / RG 5.71 (Purdue-model segmentation, no wireless in safety areas, no remote access to Class 1E, signed firmware, write-once audit logs).

---

## 8.8 Auxiliary Systems Design

Nine auxiliary systems are presented below as **separate subsections, each with the six template-required fields** (purpose · operating principle · layout · safety function · performance · maintenance). Per-system P&IDs (A4) and the formal single-line (A5) are the drawing-pass deliverable (W3); the narrative (A1–A3) is complete here. Source detail: `layout/aux_systems.md`.

**8.8.1 HVAC / Ventilation.** *Purpose:* habitability + equipment-temperature limits + a negative-pressure cascade (clean→contaminated→filtered). *Principle:* once-through in radiological zones, recirculating in clean areas; MCR slightly positive, radiological areas negative; all NI exhaust via HEPA + charcoal to the stack. *Layout:* RXB/AB exhaust → WMB filter trains → off-gas stack; CB isolated air-handling. *Safety function:* **yes** — MCR habitability + airborne confinement; intake isolation is an ESF actuation. *Performance:* HEPA ≥99.97 %@0.3 µm, charcoal iodine ≥99 %, areas ≥ −0.25 in.w.g. *Maintenance:* ΔP-monitored filters, redundant fan trains.

**8.8.2 Fire Protection.** *Purpose:* prevent fire from disabling redundant safety divisions. *Principle:* non-combustible construction + 3 h barriers between RPS/ESFAS divisions A–D; detection; pre-action sprinkler + **clean-agent in MCR/I&C/switchgear**; manual backup. *Layout:* fire-water tank + pumps in CI; ring mains in NI + CI; division barriers in CB. *Safety function:* **yes (DiD)** — protects the 2/4 separation basis. *Performance:* fire-water ≥2 h, barriers 3 h, clean-agent ≤10 s in I&C rooms. *Maintenance:* quarterly detector test, pump flow test, penetration-seal inspection.

**8.8.3 Radiation Protection + Monitoring.** *Purpose:* worker/public dose ALARA; detect + alarm; feed EPZ response. *Principle:* four monitoring layers (area / process / personnel / post-accident high-range RG 1.97). *Layout:* effluent monitors on WMB stack + liquid-discharge line + **seawater discharge**; HP lab in AB. *Safety function:* **yes** — high-radiation signals drive CI + ventilation isolation; effluent monitors gate all releases. *Performance:* effluent within 10 CFR 20 / Turkish NDK limits *[VERIFY-NDK]*; wide-range to 1e3 Sv/h. *Maintenance:* source-checks, redundant stack monitor.

**8.8.4 Emergency Power (Class 1E).** *Purpose:* supply safety loads on LOOP/SBO. *Principle:* 2× EDG (≥100 % each) + 1E batteries/UPS; EDGs auto-start on undervoltage. *Layout:* EDGs in DGB (separated), batteries/inverters in CB per division. *Safety function:* **yes (1E)** — powers RPS/ESFAS/DAS, post-accident monitoring, CIVs; note core cooling is **passive**, so power supports monitoring + active backup, not primary cooling. *Performance:* start-to-load ≤60 s; battery duty sized to the 72 h grace *[ANALYSIS-PENDING — battery-vs-grace]*. *Maintenance:* monthly EDG load test, staggered.

**8.8.5 Normal Electrical Distribution.** *Purpose:* deliver generation to grid + supply house load. *Principle:* generator → 50 MVA main Xfmr → 33 kV; dual offsite/onsite feed, auto-transfer on trip. *Layout:* switchyard in EHB (CI), switchgear in CB, routes separated from 1E. *Safety function:* **no (non-1E)** — but the preferred/first-DiD power source. *Performance:* 50 MVA covers 40 MWe + house load. *Maintenance:* conventional, no reactor-state restriction.

**8.8.6 Fuel Handling + Storage.** *Purpose:* move/keep fuel cooled, subcritical, shielded. *Principle:* refuelling machine → flooded transfer canal → SFP machine; **unborated SFP** — subcriticality by fixed-absorber rack geometry + burnup credit. *Layout:* refuelling pool in RXB; SFP + cask staging in SFB. *Safety function:* **yes** — SFP subcriticality/cooling/level + handling interlocks. *Performance:* **k_eff(95/95) ≤ 0.95 unborated** (consistent with the boron-free core); SFP ≥ full core + ≥10 cycles. *Maintenance:* machine load-test per campaign, rack inspection.

**8.8.7 Fission-Product Release Control.** *Purpose:* keep fission products out of the environment across the three-barrier chain. *Principle:* containment isolation on high radiation/pressure; leak-tight containment; gaseous decay hold-up + HEPA/charcoal; liquid radwaste treatment before monitored discharge. *Layout:* isolation valves at RXB boundary; radwaste trains + stack in WMB. *Safety function:* **yes (top-tier)** — the §8.6 release-mitigation path. *Performance:* containment leak rate ≤ design *[SIM-PENDING source term]*; dose within `safety_criteria` limits. *Maintenance:* ILRT, isolation-valve stroke test.

**8.8.8 Service Systems (compressed air · demin water · SFP cooling).** *Purpose:* support utilities. *Principle:* oil-free instrument air (valves fail-safe on loss); demin makeup; SFP cooling skids reject to component-cooling water → **once-through seawater (normal sink)**. *Layout:* compressors/demin in AB, SFP skids in SFB. *Safety function:* **mixed** — instrument air fail-safe; SFP cooling important-to-safety but large pool inertia gives long grace; **safety UHS stays passive/seawater-independent (§8.5.2a)**. *Performance:* air dew point ≤ −40 °C; SFP ≤50 °C normal/≤80 °C max. *Maintenance:* redundant skids, resin regeneration.

**8.8.9 Cogeneration interface isolation (Req 35)**

Aegis-40 exports heat to a **Thermochemical Energy Storage (TCES, zeolite-13X)** district-heating network and steam to a **Solid-Oxide Electrolysis (SOE)** hydrogen plant. IAEA SSR-2/1 **Req 35** requires that no process transport radionuclides to the heat/H₂ user in operational **or** accident states. Provision: a **non-radioactive intermediate loop** between the reactor secondary steam and both customer circuits (reactor steam never contacts district-heat water or SOE feed), held at **higher pressure** than the reactor-side stream at each interface HX so any leak flows **inward** (clean→reactor). Result: **≥3 independent barriers** — (1) SG tube wall, (2) intermediate-loop boundary, (3) customer-side HX wall (`cogen_radionuclide_isolation` ≥2 ✅). Accident-condition isolation: fail-closed ESFAS valves on high intermediate-loop/product activity, SGTR signal, or containment isolation (§8.7.3). The TCES bed and SOE sit downstream of this barrier set. **Tritium** is the governing nuclide at the SOE high-T (~800 °C) interface → permeation-barrier coatings + H₂-product tritium monitor + intermediate-loop getter *[ANALYSIS-PENDING — tritium permeation/carryover budget; Alisher + safety]*.

### 8.8.10 Electrical-supply summary (A5)

Defence-in-depth power chain: **grid (33 kV) → onsite generator → 2× EDG → 1E batteries → passive (no power needed)**. The passive core-cooling decision is what lets the chain end in "no power needed" within the 72 h grace. Single-line drawing → W3 (`aux_systems.md §10`).

---

## 8.10 Facility Layout Design

### 8.10.1 Three-island scheme

The site is partitioned into three functional islands by hazard class, safety class and access control [AP1000 DCD Ch.1; NuScale; KAERI SMART], extended for the cogeneration scope:

- **Nuclear Island (NI)** — RXB, AB, CB, SFB, DGB, WMB. Seismic Cat I throughout on a common 0.3 g SSE mat; Protected Area (10 CFR 73 / NSS-13). ~100 × 80 m.
- **Conventional Island (CI)** — TB, EHB/switchyard, **Circulating-Water Pump house (CWP) + seawater intake/outfall (once-through, no cooling tower)**, WSB. Seismic Cat II; Vital Area. ~80 × 80 m (smaller than the prior cooling-tower scheme — the 900 m² MDCT is freed).
- **Industrial Island (II)** — **TCES (zeolite-13X)**, SOE, H₂ storage. Non-safety, NFPA 2 H₂ classification; **100 m H₂ stand-off** to the nearest NI building. ~60 × 60 m.

Driving constraints: EPZ ≤ 0.5 km, SSE 0.3 g, consolidated containment penetrations, H₂ explosion stand-off (NFPA 2 / IEC 60079). Layout r2: **TB adjacent to NI** (shortest main-steam/feedwater run ~47 m); seawater intake/outfall + CWP at the CI periphery/shoreline (the circ-water run can be long). Decisions Z1–Z8 in `layout/zones.md`.

### 8.10.2 Building inventory and cooling configuration

Full table in `layout/building_list.md` (14 named buildings + site infrastructure). Cooling is **once-through Black Sea seawater (C2)**: condenser circ-water and CCWS reject to the sea via a breakwater-protected **intake structure** (trash racks + redundant travelling screens + chlorination), the **CWP house** (240 m² on-island), and a **discharge/outfall structure**. Heat rejected ≈ **70–82 MWth** at ΔT ≈ 8–10 K (~2–2.5 m³/s); plume is negligible at site scale (~1 % of the per-fleet Akkuyu load). Thermal discharge under the Turkish Water Pollution Control Regulation (SKKY) *[VERIFY-SKKY — confirm the max-T / ΔT clause]*. **This is the normal heat sink only; the safety UHS is the passive IRWST (§8.5.2a, §8.6.2).** *Realism is anchored to Akkuyu NPP (4× VVER-1200, Mediterranean) — the licensed Turkish once-through precedent; the colder Black Sea at Sinop makes the Aegis-40 condenser back-pressure / efficiency case conservative.*

### 8.10.3 Energy-storage building (TCES)

The TES building houses a **thermochemical zeolite-13X / water-vapour sorption bed (~390 t [ALISHER])**: charge by dehydration off ~280 °C pass-out steam, discharge by hydration delivering ~150–200 °C to the district-heat intermediate loop. Chosen over two-tank sensible Therminol-66 (C3) for near-zero self-discharge, intrinsically low hazard (non-toxic, non-flammable, non-corrosive — favourable under Req 35), and proven engineering. Enables the load-following/thermal-management role (§8.7.5, §8.9 note).

### 8.10.4 Critical piping (R6)

Full table in `layout/critical_piping_table.md`. Main steam **2×DN250** (~315 °C/5.8 MPa) and feedwater **2×DN200** co-routed RXB↔TB in a below-grade tunnel (~47 m), MSIVs ≤1.5 m inside the penetration, whip restraints, RC division wall. DHRS/PRHR **2×DN100** and passive ECCS **2×DN80** are intra-RXB, fully passive, **no containment penetration**. Pressurizer surge line **eliminated** (integral pressurizer). **TCES charge branch** off the MSL header; **condenser circ-water** intake→CWP→condenser→outfall (seawater once-through); **CCWS** rejection to seawater. Sizes `[FER-DRAFT]` pending Adilbek's hydraulic confirmation.

### 8.10.5 Site dimensions and coverage

Built area ~9 000 m² across the three islands; total occupied site ~250 × 300 m, comfortably inside the 500 m EPZ. The CAD model (`cad/aegis40_site.step`) is the spatial single-source-of-truth under Git; drawings `site_plot_plan` / `site_elevation` and the interactive viewer (`site/index.html`) are regenerated from the same basis. All four FER §8.10 R2 categories (reactor building / energy conversion / O&M services / other systems) are populated (`layout/fer_8_10_coverage.md`).

> **Figure status.** The site plan, elevation, CAD STEP and viewer are updated to seawater + TCES (2026-06-19). **The process-flow diagram `docs/aegis40_pfd.drawio.png` is the one remaining manual redraw** (binary PNG, no source): it must drop CT-1 + the two-tank Therminol and add the seawater intake/outfall + the TCES bed before any FER figure is cut from it. Containment concept on all figures stays **concept-neutral** pending C5.

---

## Notes on adjacent sections (other team scopes)

These are **not** in this scope but are summarized so the reviewer sees the whole story and the safety/layout dependencies are explicit.

- **§8.1 General description / Table 1** — 40 MWe / 125 MWth integral PWR, **37-FA 17×17 core (rev_4)**, 12.8 MPa, 60 y life, cogen (district heat + H₂). Codes/standards anchored on IAEA SSR-2/1, SSG-52, TECDOC-1936 + NRC SRP/NUREG-1431. *Owner: team lead; safety criteria here feed Table 1.*
- **§8.2 Core Design** *(Samira)* — **rev_4 OpenMC: 37-FA 7-wide octagonal core, 12 CRA, Gd 6 wt%×20 + Er 0.5 wt%×16, edge-pin + ring de-peaking, 12.8 MPa.** Neutronic results (k_eff, coefficients, SDM, peaking, burnup, cycle) re-running at high statistics (medium done). **Governing item: high-stat confirmation of F_Q ≈ 2.0 / F_ΔH ≈ 1.55** — feeds the OpenFOAM MDNBR (1.56) PASS.
- **§8.3 Fuel & Material** *(Samira / mechanical)* — Zircaloy-4 clad; fuel-performance + core-structural demonstration owed (`open_item: fuel_core_structural`). Asymmetric enrichment tolerance to be stated (§8.5.2).
- **§8.4 Cooling Circuit** *(Adilbek)* — primary natural circulation; secondary saturated steam 7.17 MPa; **the seawater once-through condenser/CCWS described in §8.10.2 is the secondary-side terminus** — final NPS/velocity and condenser back-pressure with cold Black Sea intake are his to confirm (efficiency can only improve vs a cooling-tower baseline).
- **§8.9 Energy Conversion & Integrated Systems** *(Alisher)* — turbine/generator + the **TCES + SOE cogeneration** plant. TCES technology is now locked (zeolite-13X, §8.10.3); the load-following control philosophy is in §8.7.5; the Req 35 isolation is §8.8.9. Outstanding: TCES bed sizing/round-trip η + the SOE tritium budget.
- **§8.11 Nuclear Waste Management** — once-through, no reprocessing; reactor-grade self-protecting spent fuel; SFP (unborated, burnup-credit) + dry-cask staging. Strong 3S/non-proliferation feature (`safety/safeguards_nonproliferation.md`).
- **§8.12 Economic Evaluation** *(FOM)* — wFOM ranks Aegis-40 a robust #2 (NuScale > **Aegis-40** > CAREM-25 > SMART); the once-through seawater change marginally improves footprint/efficiency/freshwater. The FOM's defensibility caveats (independent weights, peaking-gate honesty, data sourcing) are tracked in `planning/seawater_cooling_safety_fom_audit_2026-06-19.md §4`.

---

## Consolidated open-items register (must close or accept before submission)

| ID | Item | Section | Owner | Gates |
|---|---|---|---|---|
| O1 | **Peaking re-tally** F_Q/F_ΔH real vs mesh artifact | 8.5.2 | Samira (now) | MDNBR, LOCA PCT, FOM headline, load-follow certification |
| O2 | OpenFOAM hot-channel MDNBR + PCT | 8.5.2 | OpenFOAM | 2 hard-constraint normalizers |
| O3 | Containment P/T response (after C5) | 8.5/8.6 | layout+safety | containment design-P criterion; IEEE 323 envelope |
| O4 | C5 dry vs submerged-pool containment | 8.6.2 | team | RXB drawings, CAD, figures |
| O5 | EBIS boron mass/concentration sizing | 8.6.2a | Samira+3S | §6.10 standalone-subcriticality claim |
| O6 | DEC-A sequence demonstrations (MSLB, SBLOCA trees) | 8.6.3 | 3S | DBA spectrum completion |
| O7 | Tritium permeation/carryover budget (SOE Req 35) | 8.8.9 | Alisher+3S | cogen dose pathway |
| O8 | Sinop coastal hazard study (surge/tsunami) | 8.5.2/8.10 | site/licensing | coastal_external_hazard criterion |
| O9 | SKKY thermal-discharge ΔT limit | 8.10.2 | 3S | environmental discharge claim |
| O10 | **PFD redraw** (seawater + TCES) | 8.10.5 | 3S | all FER figures cut from the PFD |
| O11 | Boundary-dose dispersion + EPZ basis | 8.5.3 | safety | EPZ ≤0.5 km claim |
| O12 | RPS response-time/accuracy table; setpoint uncertainty | 8.7.2 | I&C | setpoint methodology (RG 1.105) |
| O13 | Internal-CRDM configuration sketch | 8.6.1 | mechanical | practical-elimination anchor |

**Marker tally:** ~10× [SIM/ANALYSIS-PENDING], 4× [VERIFY], 1× [DECISION-PENDING C5], 1× [VERIFY-SKKY], 2× [TBD]. Companion gap review: `planning/FER_readiness_review_2026-06-13.md`.

---

## References (§8.5–8.8, §8.10)

IAEA SSR-1; SSR-2/1 Rev 1 (Req 5, 13, 16, 17, 19, 20, 35, 45, 46, 52, 53, 56, 65–66, 81–82, §2.13, §5.31, §6.8–6.10); SSG-2 Rev 1; SSG-9; SSG-30; SSG-39; SSG-52; TECDOC-1936. NUREG-0700/0711; NUREG-0800 SRP Ch. 4, 7, 15; NUREG-1431 Rev 5 (LCO 3.2.1/3.2.2); NUREG/CR-6890; NUREG/CR-6928; WASH-1400. 10 CFR 50 App. A (GDC 10, 11, 13, 17, 19–24, 26); 10 CFR 50.46; 50.62; 50.63; 100.11; 73 / 73.54. RG 1.60, 1.97 Rev 5, 1.105, 1.152, 1.155, 1.174, 1.242, 5.71. IEEE 323, 344, 384, 603, 7-4.3.2; IEC 61513, 60880, 60079, 62138; ISA 18.2, ISA-67.04; ANSI/ANS-58.21; ANS-5.1; ASME III; NFPA 2; SECY-93-087, SECY-10-0034; BTP 7-19. Turkish: NDK (Nükleer Düzenleme Kurumu); Su Kirliliği Kontrolü Yönetmeliği (SKKY). Akkuyu NPP (once-through seawater precedent).

---

*End of consolidated draft r3 (2026-06-19). Folds in the seawater (C2) + TCES (C3) decisions and the UHS terminology correction. Source documents: `safety/safety_criteria.yaml`, `safety/{event_tree_LOHS,event_tree_SBO,hazards_register,trip_signals,regulatory_alignment_audit,safeguards_nonproliferation}.md`, `ic/{ic_architecture,sensor_inventory}.md`, `layout/{aux_systems,zones,building_list,critical_piping_table,fer_8_10_coverage}.md`. Supersedes `FER_Aegis40_8.5-8.7_draft.md`.*
