# Building List — Aegis-40

*Source document. Drop into FER §8.10 building inventory.*
*Companion: `layout/zones.md`, `layout/block_layout.png` (Day 3).*
*Owner: Azamhon. Last updated: 2026-06-02.*

---

## 1. Convention

- All dimensions in metres unless noted.
- **Seismic class:** Cat I = safety-related, qualified to 0.3 g SSE; Cat II = important-to-safety; Cat III = conventional.
- **Power class:** 1E = safety-critical electrical loads; non-1E = balance of plant.
- **Footprints** are **first-cut engineering estimates** based on reference PWR/iPWR designs (NuScale, SMART, AP1000 scaled to 40 MWe) and the Aegis-40 RPV envelope (Ø 2.44 m × ~5 m). Final values await design refinement and teammate inputs (TES/SOE).
- Tags: `[ASSUMED]` = engineering placeholder; `[SAMIRA]` = derived from her geometry; `[ALISHER]` = waiting on her sizing; `[ADILBEK]` = waiting on T-H piping.

---

## 2. Reactor envelope (the constraint that sets everything)

> **⚠ rev_4 re-baseline (2026-06-26):** Samira's neutronics core grew from **21 FA → 37 FA** (7-wide octagon, 12 control-rod clusters; `docs/aegis40_neutronics_FER.ipynb`), and active height **1.90 m → 2.00 m**. The 37-FA core is ~1.76× the 21-FA fuel area, so the **RPV diameter, core-barrel OD, RXB internal dimensions and SFP rack size below are now UNDERSIZED and must be re-derived** for 37 FA + 12 CRA. The values below are the superseded 21-FA envelope, kept until the 37-FA geometry is re-cut. `[REWORK — 37-FA RPV/RXB/SFP sizing]`

From `Aegis-40 2D test/geometry.xml` (**21-FA, superseded — see note above**):

| Component | Value (21-FA, superseded) | rev_4 (37-FA) |
|---|---|---|
| RPV outer diameter | 2.44 m | `[REWORK — larger for 37 FA]` |
| RPV inner diameter | 2.26 m | `[REWORK]` |
| Core barrel OD | 1.94 m | `[REWORK]` |
| Core barrel ID | 1.85 m | `[REWORK]` |
| Active fuel height | ~~1.90 m~~ | **2.00 m** (locked, 37-FA) |
| Modeled total RPV height (heads excluded) | 2.35 m | `[REWORK — +0.10 m active]` |
| Estimated total RPV height incl. heads + plenum `[ASSUMED]` | ~4.8 m | `[REWORK]` |
| Downcomer radial gap | 0.16 m | TBD |
| Heavy-metal loading | — | **9.87 tHM** (37 FA) |

These numbers drive RXB internal dimensions (refueling machine reach, crane clearance, polar crane radius) — **all to be re-derived for the 37-FA core.**

---

## 3. Master building list

### 3.1 Nuclear Island

| ID | Building | Function | Footprint (m²) | Height (m) | Seismic | Power | Source / notes |
|---|---|---|---|---|---|---|---|
| **RXB** | Reactor Building | Houses RPV, primary loop, containment (steel-lined RC), polar crane, refueling pool, IRWST | **25 × 25 = 625** | 30 above grade (+ 15 below) | Cat I | mixed 1E / non-1E | Containment Ø ≈ 15 m × 25 m tall; RPV below grade; head removal via polar crane |
| **AB** | Auxiliary Building | CVCS, sampling, primary makeup, demineralisation, primary radwaste sumps | 25 × 20 = 500 | 15 | Cat I | 1E + non-1E | Penetration interface with RXB consolidated on the AB side |
| **CB** | Control Building | Main Control Room, computer/I&C rooms, RPS/ESFAS divisions A–D in separated rooms, switchgear, battery rooms | 30 × 25 = 750 | 12 | Cat I | 1E primary | MCR per `ic/ic_architecture.md` §4.1; 2/4 voting demands 4 physically separated equipment rooms |
| **SFB** | Spent Fuel Building | Spent fuel pool (water shielded), fuel transfer canal, fuel handling machine, SFP cooling skids | 20 × 15 = 300 | 15 | Cat I | non-1E (SFP cooling) | Pool ≈ 10 × 10 × 10 m holds ≥ full-core offload + 10 cycles |
| **DGB** | Diesel Generator Building | 2× emergency diesel generators (≥ 100 % capacity each), day tanks, control panels | 15 × 10 = 150 | 10 | Cat I | 1E | Per FER Table 1 "Emergency power supplies = 2" |
| **WMB** | Waste Management Building | Liquid radwaste tanks, solid waste compactor, gaseous radwaste hold-up tanks, HEPA + charcoal | 25 × 15 = 375 | 12 | Cat I | non-1E | Tied to AB drains; off-gas stack rises from this building |
| | **NI subtotal** | | **~2 700 m²** | | | | within ~100 × 80 m island envelope (incl. corridors + 20 % circulation) |

### 3.2 Conventional Island

| ID | Building | Function | Footprint (m²) | Height (m) | Seismic | Power | Source / notes |
|---|---|---|---|---|---|---|---|
| **TB** | Turbine Building | Steam turbine + generator (40 MWe), condenser, condensate + FW pumps, lube oil | 30 × 20 = 600 | 15 | Cat II | non-1E | 40 MWe is small — single condensing turbine; saturated steam at 7.17 MPa |
| **EHB** | Electrical / Switchyard Building | Main transformer + unit-aux transformer pads; station service transformer; 33 kV switchyard interface | 50 × 50 = 2 500 (yard) + 15 × 10 = 150 (building) | 8 (building) | Cat II | non-1E | Main transformer 50 MVA — covers 40 MWe + house load |
| **CWP** | Circulating Water Pump house | Seawater circ-water pumps for the condenser (once-through) + travelling-screen wash | 20 × 12 = 240 | 10 | Cat III | non-1E | **Replaces CTW** (C2, once-through Black Sea seawater). Compact on-island; intake/outfall are shoreline structures below |
| **INTK** | Seawater intake structure | Breakwater-protected intake forebay, trash racks + redundant travelling screens, chlorination/biofouling control | shoreline (off-island) | — | Cat III | non-1E | Akkuyu-pattern; protects against marine debris/biofouling/jellyfish (CCF of the NORMAL sink only — `safety/safety_criteria.yaml` `coastal_external_hazard`) |
| **OUTF** | Discharge / outfall structure | Returns condenser circ-water to sea via forebay + culverts; thermal-discharge monitoring | shoreline (off-island) | — | Cat III | non-1E | Thermal/ΔT discharge under Turkish SKKY `[VERIFY-SKKY]`; ~70–82 MWth → negligible plume |
| **WSB** | Workshop / Service Building | Maintenance shops, warehouse, hot-tool storage, gas cylinders | 20 × 15 = 300 | 8 | Cat III | non-1E | Combined with admin in this estimate |
| | **CI subtotal** | | **~3 790 m² (incl. switchyard; CTW 900 m² freed, CWP 240 m² added)** | | | | within ~80 × 80 m envelope; intake/outfall off-island shoreline |

### 3.3 Industrial Island

| ID | Building | Function | Footprint (m²) | Height (m) | Seismic | Power | Source / notes |
|---|---|---|---|---|---|---|---|
| **TES** | Thermochemical Energy Storage (TCES) Building | **Zeolite-13X / water-vapour sorption** bed (~390 t `[ALISHER]`), charge (dehydration) / discharge (hydration) HX | 30 × 30 = 900 `[ALISHER]` | 12 | Cat III | non-1E | C3 RESOLVED: TCES, not sensible Therminol-66. Load-following + thermal management. `[ALISHER]` confirms bed mass/footprint |
| **SOE** | Solid-Oxide Electrolyser Building | High-temperature electrolyser stacks, water purification, H₂ separation + purification | 25 × 25 = 625 `[ALISHER]` | 10 | Cat III | non-1E | NFPA 2 Class 1 around stack exhaust |
| **H2S** | H₂ Storage Yard | Compressed gas tanks (350 bar typical), distribution manifold | 20 × 30 = 600 | 6 | Cat III | non-1E | NFPA 2 stand-off ≥ 100 m from NI buildings (see `zones.md` §2.3) |
| | **II subtotal** | | **~2 125 m²** | | | | within ~60 × 60 m envelope, plus 100 m buffer to NI |

### 3.4 Site infrastructure

| ID | Item | Function | Notes |
|---|---|---|---|
| ADM | Administration Building | Offices, training, locker rooms, security HQ | ~30 × 20 m, Cat III, outside Protected Area boundary |
| SEC | Security perimeter | Double fence, intrusion detection, lighting, vehicle barriers | Encloses Protected Area (NI + CI) |
| ROADS | Internal roads + heavy haul route | Reactor module delivery, refueling cask transport | Heavy-haul road from H2S to public boundary for H₂ trucks |
| METEO | Meteorological tower | Atmospheric dispersion monitoring | ≥ 100 m from any major building |
| OFFGAS | Off-gas stack | Releases monitored gaseous effluent | Mounted on WMB; ≥ 30 m above grade |

---

## 4. Footprint summary

| Island | Footprint (m²) | Share |
|---|---|---|
| Nuclear | ~2 700 | 29 % |
| Conventional (incl. switchyard) | ~4 450 | 47 % |
| Industrial | ~2 125 | 23 % |
| **Built total** | **~9 275** | 100 % |
| **Site envelope** (with circulation, buffers, EPZ) | ~75 000 (= 250 × 300 m) | — |
| Site / built ratio | ~8 : 1 | typical for SMR |

Conservative: a 10 ha (100 × 100 m × 10 ≈ 100 000 m²) inland plot accommodates the design with comfortable margin inside the EPZ.

> **Built area ≠ island envelope.** The footprints above are *building* areas. The island envelopes in `zones.md` (NI ~8 000 m², CI ~6 400 m², II ~3 600 m²) are larger because they include internal circulation, separation buffers, and access corridors around the buildings. Both are correct measures of different things.

---

## 5. Coverage check against FER §8.10 R2

> *"include the reactor building, energy conversion systems, operation and maintenance services, and other systems and buildings"*

| FER-required category | Covered by |
|---|---|
| Reactor building | RXB |
| Energy conversion systems | TB + EHB + CWP (seawater intake/outfall) |
| Operation and maintenance services | CB + WSB + ADM |
| Other systems and buildings | AB + SFB + DGB + WMB + TES + SOE + H2S + SEC + METEO + OFFGAS |

✓ All four §8.10 R2 categories populated.

---

## 6. Open items (forward to building diagram + W3)

| # | Item | Affects | Owner |
|---|---|---|---|
| 1 | TES building footprint final number | TES row | Alisher |
| 2 | SOE building footprint final number | SOE row | Alisher |
| 3 | H₂ inventory + storage form (tube trailer / stationary tanks / underground) | H2S row + stand-off Z5 | Alisher |
| 4 | ~~Heat sink choice (MDCT vs seawater)~~ → **RESOLVED: once-through seawater** (CWP/INTK/OUTF rows) | ✅ team | — |
| 5 | Fuel-assembly count (21 vs 240) | RXB internal + SFB pool size | Samira |
| 6 | Critical piping NPS | Piping rack between NI and CI | Adilbek |
| 7 | ~~Site selection (inland / coastal)~~ → **RESOLVED: coastal Sinop** | ✅ team | — |
| 8 | Weight distributions for R5 | Whole table | foundation engineer (W3+) |
| 9 | RPV total height including heads | RXB above-grade envelope | Samira |

---

## 7. References

- FER `docs/FER_Template.docx` §8.10 (facility layout) — building inventory + structural-spec requirements
- Aegis-40 RPV envelope from `Aegis-40 2D test/geometry.xml`
- NuScale Power Plant Design — six-module / single-module compact siting
- KAERI SMART reference plant — single-module iPWR layout
- AP1000 DCD Tier 2 §1.2 — building/island grouping reference

---

*End of building list. 14 named buildings + 5 site-infrastructure items, footprints first-cut, 9 open items flagged.*
