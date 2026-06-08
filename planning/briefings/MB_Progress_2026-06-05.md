# Progress Meeting — Safety Criteria → Facility Layout

**Date:** 2026-06-05
**Owner:** Azamhon
**Scope covered:** 3S Safety · I&C · Facility Layout · Auxiliary Systems
**FER sections:** §8.5 (criteria) · §8.6 (accident I&C bridge) · §8.7 (I&C) · §8.10 (layout) · §8.8 (aux systems)
**Audience:** full team + supervisor
**Purpose:** single walk-through of everything built since the safety criteria table — Week 1 and Week 2.

**Artifacts (all in repo):**
- Safety: `safety/safety_criteria.{yaml,md}` · `safety/trip_signals.md` · `safety/event_tree_LOHS.{md,png}`
- I&C: `ic/ic_architecture.md` · `ic/sensor_inventory.md` · `ic/ic_block.{mmd,png}` · `ic/fer_8_7_coverage.md`
- Layout: `layout/zones.md` · `layout/building_list.md` · `layout/block_layout.{mmd,png}` · `layout/flow_arrows.{mmd,png}` · `layout/aux_systems.md` · `layout/fer_8_10_coverage.md`
- Briefings: `planning/briefings/MB_W1.md` · `MB_W2_Layout.md`

---

## 0. The one-line story

> Every safety limit traces to a sensor that watches it, a trip that protects it, an accident scenario that tests it, an auxiliary system that supports it, and a building that houses it. Two weeks of work built one chain from a number on a page to a place on the ground.

---

## 1. Where this fits

My scope is the **integration tissue** of the design. While the core (Samira/OpenMC) and the thermal-hydraulics (Adilbek/OpenFOAM) and the energy cycle (Alisher/TES-SOE) produce the physics, my job is to:

1. Define the limits the reactor must never cross — **safety**.
2. Build the nervous system that enforces them — **I&C**.
3. Give every system a physical place to stand — **layout + auxiliaries**.

Covered FER chapters: **§8.5, §8.6, §8.7, §8.8, §8.10** — five sections, two weeks.

---

## 2. Status at a glance

| # | Deliverable | FER § | Status |
|---|---|---|---|
| 1 | Safety criteria table (27 limits, 7 categories) | 8.5 | ✅ |
| 2 | Trip signals + ESF actuations | 8.6 | ✅ |
| 3 | Event tree — Loss of Heat Sink (7 sequences) | 8.6 | ✅ |
| 4 | I&C architecture (5 layers + DAS) | 8.7 | ✅ |
| 5 | Sensor inventory (21 channels) | 8.7 | ✅ |
| 6 | I&C block diagram | 8.7 | ✅ |
| 7 | I&C coverage audit (20✓ / 5△ / 0 gaps) | 8.7 | ✅ |
| 8 | Site zoning — 3-island scheme | 8.10 | ✅ |
| 9 | Building list — 14 buildings + 5 infra | 8.10 | ✅ |
| 10 | 2D block layout diagram | 8.10 | ✅ |
| 11 | Process-flow diagram (6 streams) | 8.10 | ✅ |
| 12 | Auxiliary systems (8 systems) | 8.8 | ✅ |
| 13 | Layout + aux coverage audit (7✓ / 8△ / 2✗) | 8.10/8.8 | ✅ |
| — | FOM Python scoring tool | cross-cut | ⏳ not started |

**12 deliverables complete + 2 audits. Two genuine gaps, both deferred with named owners.**

---

## 3. Week 1 — Safety + I&C

### 3.1 Safety criteria (FER §8.5) — the spine

**27 numeric limits across 7 categories**: reactivity, thermal-hydraulics, pressure, decay-heat removal, radiological, seismic, fuel cycle. Each limit is one of three kinds:

- **Hard constraints (17)** — pass/fail. Cross one (e.g. peak clad temp > 1204 °C, MDNBR < 1.3) and the design is rejected; FOM returns −∞. You fix the reactor, not the formula.
- **Operating limits (4)** — trigger a trip, not a design failure.
- **Targets (6)** — EPZ ≤ 0.5 km, 72 h grace, etc. — aspirational, earn score.

Two things make this more than a list: it's **machine-readable** (one YAML feeds the safety chapter, trip logic, *and* the future scoring engine — a number can't disagree with itself), and every row carries a **regulatory citation + IAEA defence-in-depth level** (all 27 mapped across the 5 DiD levels — exactly the §8.6 structure).

### 3.2 Trip signals + event tree (FER §8.6)

- **Trips + ESFAS actuations**: each protective action derived from monitored variables (flux, temp, flow), with setpoint + voting logic. De-energize-to-trip / fail-safe throughout.
- **Event tree — Loss of Heat Sink** chosen as the lead §8.6 accident: it exercises the passive decay-heat removal that is the iPWR unique selling point. 7 sequences including the ATWS branch.

### 3.3 I&C architecture + sensors (FER §8.7)

- **5-layer architecture + diverse actuation system (DAS)**: RPS, ESFAS, DCS, DAS, plant twin. Four divisions, 2-out-of-4 voting, physical separation per IEEE 384.
- **21-channel sensor inventory** — 14 safety-grade Class 1E, accident-qualified set per RG 1.97.
- **Block diagram** (`ic_block.png`) — 5 layers + DAS, one-way signal flow.

### 3.4 Audit (FER §8.7 coverage)

Line-by-line, 25 sub-requirements: **20 ✓ / 5 △ / 0 gaps / 0 hard defects** (after fixing an inverted Purdue-model cybersecurity statement and adding RPS response-time bounds).

---

## 4. Week 2 — Facility Layout + Auxiliary Systems

### 4.1 Three-island scheme (FER §8.10)

Site split into three islands, each separated by **physics, not aesthetics**:

| Island | Houses | Seismic | Separation driver |
|---|---|---|---|
| **Nuclear** | reactor, aux, control room, spent fuel, diesels, radwaste | Cat I (0.3 g SSE) | EPZ + isolation paths |
| **Conventional** | turbine, generator, switchyard, cooling | Cat II | ~20 m buffer; steam/FW in trench |
| **Industrial** | TES, electrolysers, H₂ storage | non-safety, NFPA 2 | **100 m H₂ stand-off** to nearest safety bldg |

Four constraints set every boundary: EPZ ≤ 0.5 km (safety table), 0.3 g SSE, containment isolation paths (I&C), H₂ explosion stand-off (NFPA 2). The Industrial Island is the **Aegis-40 originality lever** — cogeneration of district heat + hydrogen.

### 4.2 Building list (FER §8.10)

**14 buildings + 5 infrastructure items**, each with footprint, height, seismic class, and source. The sizing constraint is the RPV — 2.44 m OD × ~4.8 m (Samira's geometry). Built area ≈ 9 300 m², fits inside the 0.5 km EPZ on a 10 ha plot. Teammate-dependent numbers (TES/SOE, cooling type) tagged, never invented.

### 4.3 Diagrams (FER §8.10)

- `block_layout.png` — 2D block layout, 3 islands, 6 inter-system connections.
- `flow_arrows.png` — 6 process streams (steam/FW, electrical, district heat, H₂, fuel, radwaste). No orphan arrows.

### 4.4 Auxiliary systems (FER §8.8)

**8 systems**, each with the FER-required six fields (purpose · principle · layout · safety function · performance · maintenance): HVAC, fire protection, radiation monitoring, emergency power, normal electrical, fuel handling, fission-product release control, service utilities.

**The power chain is the headline**: grid → onsite generator → 2× emergency diesels → Class 1E batteries → **nothing**. The design ends in "no power needed" because core cooling is passive (gravity feedwater, passive decay-heat removal, 72 h grace). Emergency power keeps *monitoring* alive, not the core — a genuinely different philosophy from a conventional PWR.

### 4.5 Audit (FER §8.10 + §8.8 coverage)

17 sub-requirements: **7 ✓ / 8 △-deferred / 2 ✗ / 0 hard defects.** The two gaps are structural weight + steel-tonnage tables (need a foundation engineer; *not* fabricated). Three minor consistency drifts found and fixed.

---

## 5. Locked decisions (don't re-litigate)

| # | Decision | Why |
|---|---|---|
| 1 | Cladding = Zircaloy-4 | PWR-standard |
| 2 | 3-zone UO₂ at 2.6 / 3.0 / 3.4 wt% | matches Samira's stable OpenMC |
| 3 | Soluble-boron-free | drives Er burnable absorber + ↑ rod worth |
| 4 | Burnable absorber = Er₂O₃ | boron-free needs slow-burning absorber |
| 5 | EFW = gravity-driven, no pumps | genuinely passive; matches 72 h grace |
| 6 | Lead §8.6 accident = Loss of Heat Sink | exercises passive decay-heat removal |
| 7 | Three-island site scheme | standard PWR practice + cogen isolation |
| 8 | Reactor below-grade | seismic + aircraft-impact protection |

---

## 6. Open items + asks

| # | Need | From | Blocks |
|---|---|---|---|
| 1 | Long depletion w/ Er₂O₃ → MTC, void, ARO worth, cycle length | Samira | 5 rows in safety criteria + FOM |
| 2 | **Fuel-assembly count** (2D model = 21, FER example = 240) | Samira | RXB size + spent-fuel pool |
| 3 | First hot-channel MDNBR + PCT | Adilbek/OpenFOAM | hard-constraint normalizers |
| 4 | Critical-piping NPS (steam, FW, surge, RHR) | Adilbek | FER §8.10 R6 piping table |
| 5 | TES/SOE footprint + H₂ inventory | Alisher | industrial-island sizing + stand-off |
| 6 | Site type (inland/coastal) + heat sink | Supervisor | cooling tower vs seawater |
| 7 | 10 supervisor sign-offs from MEETING_BRIEF §4 | Supervisor | final FOM weights |
| 8 | Structural weights + steel tonnage | foundation eng. | FER §8.10 R5 tables |
| 9 | NDK regulator citations | Azamhon | domesticity credit FER §5.2 |

**Three direct asks today** — Samira (fuel count is the biggest unknown), Alisher (industrial footprints), Supervisor (site + heat sink). Until they land I'm proceeding on documented `[ASSUMED]` values, all tagged as obvious swap targets.

---

## 7. What's next

- **W3 layout backlog:** scaled 2D plan, 3D/isometric view (§8.10 R4), critical-piping table (§8.10 R6, needs Adilbek), per-system P&IDs (§8.8 A4), formal electrical single-line (§8.8 A5), structural-weight table (§8.10 R5).
- **FOM Python tool** (`planning/PLAN.md`, 9 phases) — the scoring engine that consumes everyone's numbers. Still unstarted; unblocked once hard-constraint normalizers (items 1–3 above) arrive.

---

## 8. How I know it's right (QA method)

Every deliverable gets a **line-by-line FER coverage audit** — not a tick-box, each requirement graded on whether the answer is *physically coherent*. Two audits run so far (`ic/fer_8_7_coverage.md`, `layout/fer_8_10_coverage.md`), both caught real defects (inverted cybersecurity model; consistency drifts) and both reach **zero hard defects** after fixes. Numbers live in one source (YAML / building list) and are referenced, never re-typed — so no document can disagree with another.

---

*End of progress meeting doc. Detailed weekly scripts: `MB_W1.md`, `MB_W2_Layout.md`. Master status: `README.md`.*
