# Plan — Compact In-Line Layout + Auxiliary-Systems §8.8 Deliverables (P&IDs + Electrical SLD)

*Owner: Azamhon (3S / layout). Created 2026-06-26. Addresses the FER §8.8 requirements that every auxiliary system carry a flow & instrumentation diagram, and that on-site/off-site + emergency/UPS electrical systems be shown with technical specs and drawings — on top of a restructured, SMR-style compact layout.*

---

## 0. Why layout first

The §8.8 requirement is right: an auxiliary system can't be described (its routing, isolation, fire/seismic separation, electrical feed) without knowing **where it sits**. So this plan does the **layout restructure first**, then hangs every P&ID and the electrical single-line off the new arrangement.

---

## 1. The compact in-line layout (the foundation)

### 1.1 Concept

Replace the spread three-island campus with a **single linear process spine** — the modern SMR pattern (NuScale, Rolls-Royce SMR, BWRX-300 all use a tight, near-linear block):

```
        off-site grid (33 kV)
              │
      ┌───────────────┐   ┌──────────────┐   ┌─────────────────────┐
      │ Switchyard +  │   │ EDG / standby│   │ Aux: CB (MCR/I&C),  │   ← SIDE buildings
      │ main Xfmrs    │   │ generators   │   │ AB, WMB, workshops  │     (flank the spine)
      └──────┬────────┘   └──────┬───────┘   └─────────┬───────────┘
             │                   │                     │
   ┌─────────┴────┬──────────────┴────┬────────────────┴─────┬──────────────────────┐
   │  STORAGE     │   REACTOR BLDG    │   TURBINE BLDG       │  TCES  +  H₂ (SOE)    │  ← MAIN SPINE
   │  (fuel/SFB)  │   (RXB + int.     │   (TB: turbine,      │  thermochemical store │    (single line,
   │              │    IRWST pool)    │   condenser, FW)     │  + electrolyser       │     shared walls)
   └──────────────┴───────────────────┴──────────────────────┴──────────┬────────────┘
                                                              ┌──────────┴──────────┐
   seawater intake/outfall (shoreline) ◄── condenser circ    │  H₂ STORAGE YARD    │  ← set BACK from the line
                                                              │  (stand-off offset) │     (explosion stand-off)
                                                              └─────────────────────┘
        ◄─────────────── main-steam / process-heat corridor runs straight down the spine ──────────────►
```

**Flow logic that makes the line natural:** fuel enters at Storage → core in the RXB → steam goes RXB → TB (electricity) → and the same steam header continues TB → TCES/SOE (heat + H₂). It is **one straight steam/process corridor** — shortest pipe runs, one penetration line, shared building walls.

### 1.2 Rationale (economic, as you said)

- **Shorter pipe + cable runs** — main steam/feedwater ~47 m already; a straight spine minimises every run (steam, circ-water, cable trays, HVAC duct).
- **Shared structural walls** between adjacent buildings → less concrete, less steel, smaller footprint.
- **Fewer, combined buildings** — merge AB+WMB (radwaste/aux), CB stays separate for I&C; workshops/admin off-line.
- **One construction front** — a linear site is cheaper to excavate, crane, and sequence than a spread campus.
- "Without sacrificing much" — the safety separations below are *preserved*, not dropped; the savings come from geometry, not from cutting safety.

### 1.3 This resolves C1 (the open island question)

The repo's open **C1** is "three islands vs two (NI + combined Energy/Conventional)." The compact spine **is the two-/merged-island scheme** — one steam corridor, turbine + TCES + SOE on the same line as the reactor. **Recommend: adopt the compact in-line layout as the C1 resolution.** This collapses the Industrial Island into the tail of the spine (with the H₂ stand-off preserved as a setback, §1.4).

### 1.4 Safety constraints that MUST be preserved (the non-negotiables)

| Constraint | Source | How the compact line keeps it |
|---|---|---|
| **H₂ explosion stand-off** | NFPA 2 / IEC 60079 | ⚠ **The tension to manage.** H₂ at the spine tail is separated from the RXB by the whole Turbine Building. RXB→H₂ ≈ TB depth (~30 m) + gaps ≈ 60–80 m — **meets NFPA 2 ≥60 m for 5 000–15 000 kg but is under the old 100 m conservative bound.** Mitigation: keep the **bulk H₂ storage yard set BACK/offset** from the line (not in-line) to recover stand-off; confirm once Alisher sizes H₂ inventory. SOE *production* can be in-line; bulk *storage* is the setback item. |
| **Nuclear Island = Seismic Cat I** | SSE 0.3 g | RXB + SFB + the 1E rooms stay on one Cat-I mat; the TB/TCES end can be Cat II. The line crosses a seismic-class boundary mid-spine — handle with a **seismic gap (≥75 mm)** between Cat I and Cat II blocks (the FER docx already specified this). |
| **Security zones** | 10 CFR 73 / NSS-13 | Protected Area wraps Storage+RXB (+CB/AB); Vital Area the TB; the cogen tail is standard industrial. The line passes through descending security tiers — fence lines cross the spine, not a problem. |
| **Fire separation** | NFPA 805 | 3 h barriers between RPS/ESFAS divisions (in CB) unaffected; the shared-wall spine needs rated fire walls at each building junction. |
| **Internal IRWST pool / passive UHS** | C5 (resolved) | unaffected — it's inside the RXB. |
| **Seawater intake/outfall** | C2 | shoreline, feeds the condenser in the TB (mid-spine) — short circ-water run. |

> **The one real design tension is the H₂ stand-off.** Everything else the compact line preserves cleanly. Flag it, set the H₂ yard back, close it when the inventory number lands.

### 1.5 Files to update for the layout restructure

`layout/zones.md` (island scheme → compact spine; close C1), `layout/building_list.md` (adjacencies + shared-wall footprint savings), `layout/drawings/site_plot_plan.svg` + `site_elevation.svg` (re-cut to the line), `cad/build_aegis40_cad.py` (re-position the building solids), `site/index.html` (viewer), `layout/fer_8810_docx_audit.md` (mark C1 resolved).

---

## 2. Auxiliary-systems P&ID program (FER §8.8 A4)

### 2.1 The requirement

> *Every auxiliary system must be supported by a flow & instrumentation diagram, carrying its design purpose, operating principle, layout, safety function (if any), performance characteristics and maintenance requirements.*

The **six-field narrative already exists** for all 9 systems (`layout/aux_systems.md` §2–§9a + FER §8.8.1–8.8.8). What's missing is the **A4 graphic — a flow/instrumentation diagram per system**. That is the deliverable here.

### 2.2 The nine systems → one P&ID each

| # | System | P&ID shows (flow + instrumentation) | Safety fn | Priority |
|---|---|---|---|---|
| 1 | HVAC / Ventilation | supply/exhaust trains, negative-pressure cascade, HEPA+charcoal, stack, dampers + radiation monitors (ESF isolation) | Yes | high (confinement) |
| 2 | Fire Protection | fire-water ring main, pumps (diesel+electric), pre-action vs clean-agent zones, detection | Yes (DiD) | med |
| 3 | Radiation Protection + Monitoring | area/process/effluent/post-accident monitors, stack + liquid-discharge + **seawater-discharge** monitors | Yes | high |
| 4 | **Emergency Power (1E)** | covered by the electrical SLD (§3) — cross-reference | Yes (1E) | **see §3** |
| 5 | Normal Electrical | covered by the electrical SLD (§3) | No | **see §3** |
| 6 | Fuel Handling + Storage | refuel pool → transfer canal → SFP, handling machine, SFP cooling loop + level/temp/criticality instr | Yes | high |
| 7 | Fission-Product Release Control | containment isolation valves, gaseous decay-hold-up + HEPA/charcoal, liquid radwaste → monitored discharge | Yes (top) | high |
| 8 | Service Systems (air · demin · SFP cooling) | instrument/service air compressors+dryers, demin plant, SFP cooling skids → CCWS → seawater | Mixed | med |
| 9 | **Cogen Interface Isolation (Req 35)** | reactor steam → interface HX → **non-radioactive intermediate loop (clean-side-high ΔP)** → customer HX → TCES/SOE; fail-closed ESFAS valves, activity + ΔP monitors, tritium monitor | Yes | high (originality) |

**9 P&IDs**, or **8** if Emergency Power (4) folds into the §3 electrical SLD. Each P&ID is a one-page `.drawio` with a **title block** carrying the six fields (purpose / principle / layout location / safety function / performance / maintenance) so the diagram *is* the §8.8 deliverable, not just a flow sketch.

### 2.3 Convention

- Standard P&ID symbology: ISA-5.1 (instrument bubbles, valve symbols, line types), simplified for FER readability.
- Colour key consistent with the repo (blue=water/steam, yellow=electrical, orange=heat, green=H₂, red=radioactive) — same as `layout/flow_arrows.mmd`.
- Each instrument bubble tags to a channel in `ic/sensor_inventory.md`; each ESF valve tags to `safety/trip_signals.md`.

---

## 3. Electrical systems — single-line diagram + specs (FER §8.8 A5)

### 3.1 The requirement

> *On-site and off-site electrical systems supplying safety-significant SSCs, including emergency and uninterruptible power, must be introduced with technical specifications + graphics/drawings/plans.*

There is an **ASCII single-line** in `aux_systems.md §10` and narrative in §5–§6. The A5 deliverable is a **formal single-line diagram (SLD)** + a **technical-spec table**.

### 3.2 SLD content (the `.drawio`)

```
 OFF-SITE GRID 33 kV ──┬── Main Xfmr (50 MVA) ── GENERATOR (40 MWe gross)
                       │                              │
            Station-Service Xfmr            Unit-Aux Xfmr (UAT)
                       │                              │
                 ┌─────┴───────── PLANT NORMAL BUSES (non-1E) ─────────┐
                 │                                                      │
        (on loss of normal + off-site → auto-transfer)                 │
                 ▼                                                      ▼
   ┌──────────────── CLASS 1E BUSES (Div A/B/C/D) ───────────────┐   house loads
   │  2× EDG (auto-start LOOP)      1E Batteries / UPS (inverters)│
   │  ≥100% safety load each       instantaneous + ride-through  │
   └───────────────┬──────────────────────────┬─────────────────┘
            powers: RPS · ESFAS · DAS · MCR HVAC · containment-isolation valves · post-accident monitoring
            (passive core cooling needs NO power → chain can end here within the 72 h grace)
```

### 3.3 Technical-spec table (accompanies the SLD)

| Element | Spec (to populate) | Basis |
|---|---|---|
| Off-site feed | 33 kV, dual independent lines `[VERIFY grid]` | first DiD layer |
| Main transformer | 50 MVA | 40 MWe + house load |
| Unit-aux / station-service Xfmr | ~6–8 MVA `[EST house load]` | dual on/off-site feed |
| 2× EDG | ≥100% 1E load each, start-to-load ≤60 s | FER Table 1 "emergency power = 2" |
| 1E batteries / UPS | duty **8 h vs 24 h vs 72 h** — close `[open item §5]` | ride-through to passive self-sufficiency |
| Inverters | uninterruptible AC to vital I&C buses | IEEE 308 / 1E |
| Voltage levels | 33 kV / MV / 480 V / 120 V vital | standard |

Standards: IEEE 308 (1E power), IEEE 387 (diesel-generators), IEEE 484/485 (batteries), RG 1.6/1.9/1.32, 10 CFR 50 GDC 17.

### 3.4 Deliverables for A5

1. **`electrical_sld.drawio`** — the single-line above, drawn properly (Div A–D colour-separated, 1E vs non-1E shading).
2. **Spec table** — into `aux_systems.md §10` + FER §8.8.10.
3. Close the **battery-duty open item** (B11 in the safety plan) so the UPS spec is real.

---

## 4. Yes — draw.io, and how

**I can author `.drawio` files directly** — they are mxGraph XML (same format as `safety/event_tree_LOHS.drawio`, `ic/ic_block.drawio` already in the repo). Workflow:

- I write the `.drawio` (editable XML) → you open/refine in draw.io desktop or app.diagrams.net.
- **Rendering to PNG:** there's no `drawio` CLI in this environment, so the committed `.drawio.png` companions are exported from the draw.io app (File → Export → PNG). For anything that needs an *immediately rendered* image, I can instead author a **native SVG** (renderable here via `layout/drawings/render.sh`) — so the plan is: **`.drawio` for editable engineering diagrams** (P&IDs, SLD), with an **SVG twin** where we want a committed rendered image without the export step.
- Location: P&IDs in `layout/drawings/pid/`, the SLD in `layout/drawings/electrical_sld.drawio`.

---

## 5. Sequence (recommended order)

| Phase | Work | Output |
|---|---|---|
| **P0** | Lock the compact in-line layout — update `zones.md` + `building_list.md`, resolve C1, flag the H₂ setback | text/data baseline |
| **P1** | Re-cut the **site plan + elevation** (SVG) + CAD + viewer to the compact line | figures |
| **P2** | **Electrical SLD** (`.drawio` + spec table) — A5, single highest-value diagram; close battery duty | A5 done |
| **P3** | **Aux P&IDs** — author the 9 (or 8) `.drawio` P&IDs with six-field title blocks; start with the safety-significant ones (HVAC, fuel handling, fission-product control, cogen isolation, rad monitoring) | A4 done |
| **P4** | Cross-link every P&ID instrument to `sensor_inventory.md` + every ESF valve to `trip_signals.md`; fold into FER §8.8 | integration |

## 6. Open dependencies

- **C1 decision** — recommend the team formally adopt the compact line (this plan is the basis).
- **H₂ inventory (Alisher)** — sets the stand-off → fixes the H₂-yard setback distance.
- **House-load MW** — sizes the UAT/station-service transformer.
- **Battery duty (8/24/72 h)** — B11 in `SAFETY_WORK_HANDOFF.md`; sizes the UPS.
- **Per-system performance numbers** — some still `[ASSUMED]` in `aux_systems.md` (HEPA %, air dew point, etc.) — fine for the FER if labelled.

---

*Net: 1 layout restructure (resolves C1) + 1 electrical SLD (A5) + 8–9 P&IDs (A4), all authorable as `.drawio` (with SVG twins where a rendered image is wanted). Recommend starting at P0→P2 so the electrical A5 — the more rigid requirement — lands first.*
