# Building List — Aegis-40

*Source document. Drop into FER §8.10 building inventory.*
*Companion: `layout/zones.md`, `planning/COMPACT_LAYOUT_PROPOSAL.md`.*
*Owner: Azamhon. Last updated: 2026-06-26.*

> **Arrangement (2026-06-26, C1 resolved):** these buildings are now arranged in a **compact in-line spine** — SFB → RXB → TB → TCES → SOE, with CB/AB/WMB on the north flank and DGB/switchyard/CWP/WSB on the south, bulk H₂ offset to the SE corner. Footprints below are unchanged; only the *arrangement* changed (shared spine walls save ~6–8 % built area). Positions + the building schedule with adjacencies are in `planning/COMPACT_LAYOUT_PROPOSAL.md` (zones.md Z9).

---

## 1. Convention

- All dimensions in metres unless noted.
- **Seismic class:** Cat I = safety-related, qualified to 0.3 g SSE; Cat II = important-to-safety; Cat III = conventional.
- **Power class:** 1E = safety-critical electrical loads; non-1E = balance of plant.
- **Footprints** are **first-cut engineering estimates** based on reference PWR/iPWR designs (NuScale, SMART, AP1000 scaled to 40 MWe) and the Aegis-40 RPV envelope (Ø 2.44 m × ~5 m). Final values await design refinement and teammate inputs (TES/SOE).
- Tags: `[ASSUMED]` = engineering placeholder; `[SAMIRA]` = derived from her geometry; `[ALISHER]` = waiting on her sizing; `[ADILBEK]` = waiting on T-H piping.

---

## 2. Reactor envelope (the constraint that sets everything)

> **rev_4 re-baseline (2026-06-26):** the core is now **37 FA, 7-wide octagon, 12 CRA** (`docs/aegis40_neutronics_FER.ipynb`), and the thermal-hydraulic study (`docs/Aegis40_TH_report.docx`) fixes the integral-vessel arrangement: a **~10 m tall, ~Ø3.0–3.5 m NuScale-class natural-circulation vessel** (helical-coil SG in the annulus around a central riser, integral pressurizer on top). The envelope below is **re-derived for 37 FA**; values tagged `[EST]` are first-cut engineering estimates pending the mechanical vessel design (wall thickness, seismic) which is the mechanical teammate's scope.

**Core size (from the locked lattice):** 37 FA × 21.6038 cm pitch → active-core **equivalent diameter ≈ 1.50 m** (≈ 1.51 m across the 7-wide flats); + 20 cm radial water reflector each side → **≈ 1.9 m** reflected-core diameter; **9 768 fuel pins**, **9.87 tHM**.

| Component | rev_4 (37-FA) | Basis |
|---|---|---|
| Active fuel height | **2.00 m** | locked geometry |
| Active-core equivalent diameter | **~1.50 m** | 37 FA × 0.216 m pitch |
| Reflected-core diameter (+20 cm reflector) | **~1.9 m** | locked reflector |
| RPV inner diameter | **~2.7–3.0 m** `[EST]` | reflected core + downcomer + riser/SG annulus |
| RPV outer diameter | **~3.0–3.5 m** `[EST]` | TH report (NuScale-class) |
| RPV total height | **~10 m** | TH report elevation budget (vs ~17.7 m NuScale — shorter riser) |
| Heavy-metal loading | **9.87 tHM** | 37 FA |

**Integral-vessel elevation budget** (delivers natural-circulation H_tc ≈ 4 m; core mid 1.9 m → SG mid 5.9 m), from the TH report:

| Elevation [m] | Component |
|---|---|
| 0.0 – 0.9 | lower plenum / core inlet |
| 0.9 – 2.9 | **core** (2.0 m active; mid-plane 1.9 m) |
| 2.9 – 4.4 | outlet plenum + riser (chimney) |
| 4.4 – 7.4 | **steam generator** (helical coil in annulus; mid 5.9 m; ~1 250 m², 467 kg/s) |
| 7.4 – 7.9 | upper plenum |
| 7.9 – 9.9 | integral pressurizer |

These drive RXB internal dimensions (refuel-pool depth, crane lift height, polar-crane radius) and the SFP size — updated in §3.1 below. **Binding RXB dimension is now vessel HEIGHT (~10 m, was ~4.8 m), not diameter** (Ø3.25 m ≪ containment).

---

## 3. Master building list

### 3.1 Nuclear Island

| ID | Building | Function | Footprint (m²) | Height (m) | Seismic | Power | Source / notes |
|---|---|---|---|---|---|---|---|
| **RXB** | Reactor Building | Houses the ~10 m integral RPV, **internal IRWST pool (CAREM-style, in-containment)**, primary loop, containment, polar crane, refueling pool | **25 × 25 = 625** `[re-check]` | **~36 above grade (+ ~12 below)** `[EST]` | Cat I | mixed 1E / non-1E | rev_4: vessel **~10 m × Ø~3.25 m** (was ~4.8 × 2.44). Internal height re-derived for the taller vessel + head-lift + fuel withdrawal + crane: **vessel 10 m + ~12 m refuel/crane above**. Footprint Ø15 m containment still ≫ vessel → plan unchanged; the change is vertical. Internal IRWST = the passive safety UHS (no external ECCS penetration) |
| **AB** | Auxiliary Building | CVCS, sampling, primary makeup, demineralisation, primary radwaste sumps | 25 × 20 = 500 | 15 | Cat I | 1E + non-1E | Penetration interface with RXB consolidated on the AB side |
| **CB** | Control Building | Main Control Room, computer/I&C rooms, RPS/ESFAS divisions A–D in separated rooms, switchgear, battery rooms | 30 × 25 = 750 | 12 | Cat I | 1E primary | MCR per `ic/ic_architecture.md` §4.1; 2/4 voting demands 4 physically separated equipment rooms |
| **SFB** | Spent Fuel Building | Spent fuel pool (water shielded), fuel transfer canal, fuel handling machine, SFP cooling skids | **~25 × 18 = 450** `[EST]` | 15 | Cat I | non-1E (SFP cooling) | rev_4: 37-FA core is **~1.76× the 21-FA** → full-core offload + multi-cycle storage scales up; pool **~13 × 13 × 10 m** (or denser racks). SFP cooling duty also scales with the larger core decay heat |
| **DGB** | Diesel Generator Building | 2× emergency diesel generators (≥ 100 % capacity each), day tanks, control panels | 15 × 10 = 150 | 10 | Cat I | 1E | Per FER Table 1 "Emergency power supplies = 2" |
| **WMB** | Waste Management Building | Liquid radwaste tanks, solid waste compactor, gaseous radwaste hold-up tanks, HEPA + charcoal | 25 × 15 = 375 | 12 | Cat I | non-1E | Tied to AB drains; off-gas stack rises from this building |
| | **NI subtotal** | | **~2 850 m²** `[EST]` | | | | rev_4: SFB +150 m² for the 37-FA pool; within ~100 × 80 m island envelope (incl. corridors + 20 % circulation) |

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
- Aegis-40 RPV envelope from `docs/aegis40_neutronics_FER.ipynb` (rev_4 37-FA) + `docs/Aegis40_TH_report.docx` (vessel elevation budget)
- NuScale Power Plant Design — six-module / single-module compact siting
- KAERI SMART reference plant — single-module iPWR layout
- AP1000 DCD Tier 2 §1.2 — building/island grouping reference

---

*End of building list. 14 named buildings + 5 site-infrastructure items, footprints first-cut, 9 open items flagged.*
