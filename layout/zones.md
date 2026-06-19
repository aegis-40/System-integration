# Site Zoning — Aegis-40 Three-Island Scheme

*Source document. Drop into FER §8.10 introduction.*
*Companion: `layout/building_list.md`, `layout/block_layout.png` (Day 3), `layout/aux_systems.md` (Day 5).*
*Owner: Azamhon. Last updated: 2026-06-02.*

---

## 1. Why three islands

The Aegis-40 site is partitioned into **three functional islands** separated by physical buffers and security classifications. Each island contains buildings sharing the same hazard class, safety class, and access control. This partition is the basis for every downstream layout decision — building grouping, piping routes, electrical distribution, emergency response zones.

The three-island scheme follows the standard PWR practice (Westinghouse AP1000, KAERI SMART, NuScale VOYGR), adapted for Aegis-40's **cogeneration scope** that adds a non-conventional Industrial Island for thermal energy storage (TES) and hydrogen production (SOE).

The partition is dictated by four constraints:

| Constraint | Source | Implication |
|---|---|---|
| EPZ ≤ 0.5 km radius | `safety/safety_criteria.yaml` row `epz_radius` | Whole site fits within 500 m of reactor centerline |
| SSE 0.3 g foundation | `safety/safety_criteria.yaml` row `sse_design` | Safety-related buildings on Class I foundation; non-safety can use Class II |
| Containment isolation paths | `ic/ic_architecture.md` §3.3 ESFAS | Penetrations consolidated where containment crosses Nuclear Island boundary |
| H₂ explosion stand-off | NFPA 2 + IEC 60079 | Bulk H₂ storage ≥ 100 m from any safety-related occupied building |

---

## 2. Island definitions

### 2.1 Nuclear Island (NI)

**Function:** house the reactor, primary loop, safety systems, control room, fuel, and radwaste — everything whose failure could release radioactivity or whose function is required to prevent a release.

**Buildings (refer to `building_list.md` for full table):**
- Reactor Building (RXB) with containment
- Auxiliary Building (AB)
- Control Building (CB)
- Spent Fuel Building (SFB)
- Diesel Generator Building (DGB)
- Waste Management Building (WMB)

**Class:** Seismic Category I throughout. All buildings on a common engineered fill / mat foundation rated for 0.3 g SSE. Aircraft-impact-resistant outer walls on the RXB (below-grade reactor placement assists).

**Security:** **Protected Area** (NRC 10 CFR 73 / IAEA NSS-13 equivalent). Double-fence + intrusion detection. Limited access via personnel checkpoint.

**Footprint estimate:** ~100 m × 80 m (8 000 m²). Driven by RXB + AB + CB + SFB compact grouping.

### 2.2 Conventional Island (CI)

**Function:** convert thermal energy to electricity, condition it for the grid, dissipate residual heat. Conventional industrial hazards (steam, rotating machinery, high voltage); **no radioactive inventory**.

**Buildings:**
- Turbine Building (TB)
- Electrical / Switchyard (EHB) — main transformers, 33 kV grid interface
- Circulating Water Pump house (CWP) + **seawater intake structure** (breakwater-protected, travelling screens, chlorination) and **discharge/outfall structure** — **once-through Black Sea cooling, NO cooling tower** (C2, 2026-06-13). Intake/outfall are shoreline structures, largely outside the plant-island footprint.
- Service / Workshop Building

**Class:** Seismic Category II. Conventional industrial siting standards. *(Note: the seawater system is the **normal** heat sink only — non-safety-classified. The **safety** ultimate heat sink is the passive IRWST + containment cooling, seawater-independent — see `safety/safety_criteria.yaml` `ultimate_heat_sink`.)*

**Security:** **Vital Area** controlled access — no public, but lower-tier than NI.

**Footprint estimate:** ~80 m × 80 m (6 400 m²) — **smaller than the prior cooling-tower scheme** (the 900 m² MDCT is freed; only the compact CWP house remains on-island). Turbine + switchyard now dominate.

**Separation from NI:** ~20 m physical buffer; main steam + feedwater piping crosses the boundary in a controlled trench.

### 2.3 Industrial Island (II)

**Function:** non-electrical applications of the cogeneration heat — thermal energy storage for district heating, solid-oxide electrolyser hydrogen production, H₂ storage. **This island is the Aegis-40 originality lever** for FER §5.

**Buildings:**
- TES Building — **Thermochemical Energy Storage (TCES), zeolite-13X / water-vapour sorption** (C3 RESOLVED 2026-06-13; supersedes the two-tank sensible Therminol-66 option). ~390 t bed `[ALISHER]` to confirm mass/footprint. For load-following + thermal management.
- SOE Building (high-temperature electrolyser stacks)
- H₂ Storage Yard (compressed gas tanks)

**Class:** Non-safety, but **NFPA 2-classified** for H₂ hazard. ATEX / Zone 2 classification around H₂ handling areas.

**Security:** standard industrial access control. Public excluded for H₂ explosion zone.

**Footprint estimate:** ~60 m × 60 m (3 600 m²), plus a **100 m H₂ stand-off buffer** to the nearest Nuclear Island building.

**Why isolated:** H₂ leak + ignition → deflagration. Distance is the cheapest mitigation. NFPA 2 Table 7.1.16.6.1 gives ≥ 30 m for stationary gaseous H₂ < 5 000 kg, ≥ 60 m for 5 000–15 000 kg. We use 100 m as a **conservative bound** until inventory is sized (Alisher).

---

## 3. Inter-island connections

| Connection | Carries | Route | Constraint |
|---|---|---|---|
| NI → CI | Main steam (one line) | Above-ground rack, ~20 m, qualified penetration | Critical piping — feeds FER §8.10 R6 |
| CI → NI | Feedwater (one line) | Above-ground rack | Critical piping |
| CI → grid | Electrical 33 kV | Overhead from EHB | — |
| NI ↔ CI | Auxiliary feedwater (EFW) | Gravity feed from elevated tank in NI | Passive — see `safety/trip_signals.md` E3 |
| NI → II | Process steam / heat | Heat exchanger on NI boundary; secondary loop water to TES | TES side is non-radioactive (interface HX on NI) |
| II → grid | Optional electric tie | (deferred — current scope sells H₂, not electricity from II) | — |
| II output | H₂ truck loading | Surface road to public boundary | NFPA 2 Class 1 area |

All four "critical piping" lines (main steam, feedwater, pressurizer surge, RHR) per FER §8.10 R6 originate inside Nuclear Island; only main steam + feedwater cross to CI.

---

## 4. Site-level dimensions (envelope, with EPZ overlay)

```
              EPZ boundary (radius 500 m)
        ┌─────────────────────────────────────┐
        │                                     │
        │      ┌──────────────┐               │
        │      │ Conventional │               │
        │      │   Island     │               │
        │      │  (80×80 m)   │               │
        │      └───┬──────────┘               │
        │          │ piping rack              │
        │      ┌───┴──────────┐               │
        │      │   Nuclear    │               │
        │      │   Island     │               │
        │      │  (100×80 m)  │               │
        │      └──────────────┘               │
        │                                     │
        │                       100 m buffer  │
        │                          ↓          │
        │                  ┌──────────────┐   │
        │                  │  Industrial  │   │
        │                  │    Island    │   │
        │                  │  (60×60 m)   │   │
        │                  └──────────────┘   │
        │                                     │
        └─────────────────────────────────────┘
```

**Total occupied site:** ~250 m × 300 m, comfortably inside the 500 m EPZ. Remaining EPZ area = exclusion buffer + perimeter road + monitoring stations.

A more accurate block-layout drawing (with internal building positioning) lands as `layout/block_layout.png` on Day 3.

---

## 5. Decisions locked by this document

| ID | Decision | Rationale |
|---|---|---|
| Z1 | Three-island scheme (Nuclear / Conventional / Industrial) | Standard PWR practice extended for cogeneration |
| Z2 | NI is Seismic Cat I throughout, ~100 × 80 m | Driven by RXB + AB + CB grouping + SSE 0.3 g |
| Z3 | CI is Seismic Cat II, ~80 × 80 m | Conventional industrial; turbine + cooling dominate |
| Z4 | II is non-safety with NFPA 2 H₂ classification, ~60 × 60 m | H₂ hazard isolation |
| Z5 | H₂ stand-off = 100 m to nearest NI building | Conservative bound NFPA 2; refine after Alisher sizes inventory |
| Z6 | ~~Closed cooling tower in CI~~ → **RESOLVED 2026-06-13: once-through Black Sea seawater cooling, NO cooling tower** | Team decision — small ~70–82 MWth rejection, negligible thermal-plume impact at the Sinop coastal site (≈1 % of Akkuyu's per-fleet load); CTW footprint freed. **Akkuyu (4×VVER-1200) is the licensed Turkish precedent for once-through seawater.** Text/data recut applied 2026-06-19; graphical recut in progress now that C3 is settled. |
| Z7 | **TB adjacent to the NI boundary; seawater intake/outfall + CWP house at the CI periphery / shoreline** (r2, 2026-06-12; updated 2026-06-19) | NuScale plant-arrangement practice + PFD logic: main-steam/feedwater run must be short (~47 m); condenser circ-water run to the shoreline intake/outfall can be long |
| Z8 | **TCES = thermochemical zeolite-13X / water-vapour sorption** (C3 RESOLVED 2026-06-13) | Non-toxic/non-flammable/non-corrosive proven medium; charge by dehydration off ~280 °C pass-out steam, discharge ~150–200 °C to district heat. Decouples steady reactor output from grid dispatch → **load-following + thermal management without deep reactor maneuvering** (safety upside — see safety review). Supersedes two-tank sensible Therminol-66 |

---

## 6. Open items propagated to next steps

| # | Item | Owner | Resolves |
|---|---|---|---|
| 1 | Final H₂ inventory (kg) | Alisher | Z5 stand-off math (could shrink to 60 m if < 15 000 kg) |
| 2 | TCES bed mass (~390 t?) + height | Alisher | TES Building footprint estimate (currently `[ASSUMED]` 30 × 30 m) |
| 3 | Primary loop pipe NPS + routes | Adilbek | Piping rack sizing between NI and CI |
| 4 | ~~Site type + heat sink~~ → **RESOLVED: coastal Sinop, once-through seawater (Z6); TCES (Z8)** | ✅ team | — graphical recut in progress |
| 5 | Final fuel-assembly count (21 in 2D vs 240 in FER table) | Samira | RXB internal layout (refueling machine span, SFP size) |

---

## 7. References

- FER `docs/FER_Template.docx` §8.10 (facility layout) and §8.8 (auxiliary systems)
- NFPA 2 *Hydrogen Technologies Code* — Tables 7.1.16.6.1 (stand-off), 7.3 (zone classification)
- IEC 60079 — Explosive atmospheres equipment classification
- IAEA SSG-9 — Site evaluation
- NRC RG 1.91 — Evaluation of explosions postulated to occur at nearby facilities
- 10 CFR 73 — Physical protection of plants and materials
- Westinghouse AP1000 DCD Tier 2 Chapter 1 (3-island reference)
- NuScale SMR Standard Plant Design (compact-site reference)

---

*End of zones document. Length ≈ 4 printed pages. Three islands, six locked decisions, five open items.*
