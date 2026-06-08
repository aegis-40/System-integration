# W2 Plan — NPP Layout + Auxiliary Systems

**Owner:** Azamhon
**Week:** 2026-W23 (start 2026-06-02)
**Scope assumed:** `docs/tasks_w1.pdf` page 5 (NPP layout / auxiliary systems) — originally Elbek's scope, now taken on.
**FER sections owned by this work:** §8.10 Facility Layout · §8.8 Auxiliary Systems Design.
**Process:** built via `planning/TASK_PROCESS.md` — 7 steps applied.

---

## Step 1 — SPEC: what FER §8.10 + §8.8 demand

### §8.10 Facility Layout — decomposed requirements

| # | Requirement |
|---|---|
| R1 | General layout *considering* constructability, economic efficiency, safety, operations |
| R2 | Layout description covering reactor building, energy conversion, ops/maintenance services, other systems & buildings |
| R3 | **2D plans** of main buildings + connections |
| R4 | **3D plans** of main buildings + connections |
| R5 | Tables with technical specs forming basis for structural specifications (construction structures, steel, connection structures, **weight distributions**, structural requirements) |
| R6 | **Critical piping** clearly shown — main steam, feedwater, pressurizer lines, RHR — within/between structures |

### §8.8 Auxiliary Systems — decomposed requirements

| # | Requirement |
|---|---|
| A1 | Ventilation, electrical, fire safety, radiation protection — all technical info |
| A2 | Each aux system gets its own sub-heading: fission-product release control, ventilation, compressed air, fuel handling/storage, fire protection |
| A3 | Each system: design purpose, operating principles, layout, safety function (if any), performance, maintenance |
| A4 | Flow + instrumentation diagrams per system |
| A5 | On-site + off-site electrical incl. emergency + uninterruptible — graphics, drawings, plans |

**Total: 11 discrete requirements.** Audit at end-of-week will check against this list.

---

## Step 2 — INPUTS

### 2a. Locked inputs (use as-is)

| Source | What I use |
|---|---|
| `Aegis-40 2D test/materials.xml` + `geometry.xml` (Samira) | RPV: 2.44 m OD × ~4.8 m tall incl. heads `[ASSUMED, Samira to confirm]`; modeled height (heads excluded) 2.35 m; core barrel 1.85 m OD; active height 1.90 m (`building_list.md` §2 is the authority for these) |
| `safety/safety_criteria.yaml` row `epz_radius` | EPZ ≤ 0.5 km — defines site boundary |
| `safety/safety_criteria.yaml` row `sse_design` | SSE 0.3 g — drives seismic Cat I siting + foundation |
| `docs/FER_Template.docx` Table 1 | Containment dry, 4.14 bar design; emergency power supplies ×2; ECCS ×3 passive; 240 fuel assemblies (note: Samira uses 21 in 2D) |
| Project basics | 40 MWe + 125 MWth; cogen splits = district heat + H₂ via SOE; process heat 100–260 °C |

### 2b. Pending inputs (pings to send Monday)

| Person | What I need | By | Why |
|---|---|---|---|
| **Adilbek (OpenFOAM / T-H)** | Primary loop pipe NPS + routing constraints; secondary main-steam pipe size; pressurizer surge line | Wed | R6 critical piping plan |
| **Alisher (TES/SOE)** | TES module footprint (m² + height); SOE unit footprint; H₂ storage volume + tank count | Wed | Industrial-island sizing |
| **Samira** | Confirm RPV envelope final dims; confirm number of fuel assemblies (2D model 21, FER table example 240 — what is Aegis target?) | Mon | Reactor building floor plan |
| **Supervisor** | Site assumption (inland Turkey vs coastal); cooling type (closed cooling tower vs open seawater) | Mon | Drives whole site layout |

### 2c. Assumptions until pings resolve (all tagged `[ASSUMED]`)

- **Site type:** inland Turkey, ~10 ha plot, cooling via mechanical-draft cooling tower (most siting-flexible default).
- **Number of modules:** single Aegis-40 module per site (no multi-unit). Multi-unit deferred.
- **Reactor placement:** below-grade — RPV head ~5 m below grade level. Standard SMR trend; better seismic + missile protection.
- **Containment:** dry, steel-lined reinforced concrete; cylindrical ~15 m ID × 25 m tall (inferred from RPV envelope + crane clearance).
- **H₂ separation:** H₂ storage ≥ 100 m from any safety-related building (NFPA 2 / IEC 60079 for explosive atmospheres).
- **Switchyard:** 33 kV interface to grid; one main transformer + one unit-auxiliary transformer.

---

## Step 3 — DECISIONS to lock this week

Lock before drawing anything. Each survives an FER review or doesn't:

| # | Decision | Default | Rationale |
|---|---|---|---|
| L1 | Single-module vs multi-module | **Single** | FER spec is "40 MWe modular PWR" singular. Multi-unit is W4+ if at all. |
| L2 | Reactor below-grade vs above-grade | **Below-grade** | Seismic + aircraft-impact protection; matches NuScale/SMART best practice. |
| L3 | Containment type | **Dry** (steel-lined RC) | Matches FER Table 1; consistent with `safety_criteria.yaml` containment row. |
| L4 | Heat sink | **Closed-cycle cooling tower** (`[ASSUMED]` until supervisor confirms) | Inland-Turkey default; flexible siting |
| L5 | Drawing tool for 2D layout | **Mermaid (block) + a simple scale drawing (draw.io or paper)** | Mermaid for the audit-friendly block diagram, draw.io PNG for FER print |
| L6 | 3D requirement (R4) coverage | **Isometric view in draw.io for W2; full 3D CAD deferred** | W2 ships the concept; W3+ does 3D refinement |
| L7 | Auxiliary buildings grouping | **3-island scheme:** nuclear / conventional / industrial | Standard PWR practice; isolates H₂ + TES from safety zone |

---

## Step 4 — PLAN: day-by-day (this file = the plan)

### Goal of the week
> Ship a defensible **first 2D block layout** + **building list** + **auxiliary systems list** that satisfies FER §8.10 R1–R3 + §8.8 A1–A3, with §8.10 R4–R6 + §8.8 A4–A5 explicitly flagged as W3 follow-up.

### Hard deliverables (5)

| # | File | Status |
|---|---|---|
| 1 | `layout/zones.md` — 3-island zoning rationale | ✅ |
| 2 | `layout/building_list.md` — building/function table | ✅ |
| 3 | `layout/block_layout.{mmd,png}` — 2D block-level facility layout with zones | ✅ |
| 4 | `layout/flow_arrows.{mmd,png}` — major flow arrows (steam, FW, electrical, district heat, H₂, waste/fuel) | ✅ |
| 5 | `layout/aux_systems.md` — auxiliary systems list with design purpose + safety function per FER §8.8 | ✅ |

**Audit done:** `layout/fer_8_10_coverage.md` — 7 ✓ / 8 △ / 2 ✗ (R5 weights+steel, external). 0 hard defects. F1/F2 consistency fixes applied 2026-06-05.

### Stretch deliverables

- `layout/scale_plan_2d.png` — true-to-scale 2D plan in draw.io (R3 quality upgrade)
- `layout/isometric_view.png` — simple isometric for R4
- `layout/critical_piping_table.md` — R6 piping inventory (depends on Adilbek input)
- `layout/fer_8_10_coverage.md` — coverage check parallel to `ic/fer_8_7_coverage.md`

### Day-by-day schedule

| Day | Work | Output | Time |
|-----|------|--------|------|
| **Mon** | Steps 1–4 done → this file. Send all 4 pings. Read `Aegis-40 2D test/geometry.xml` for envelope dims. | Plan file + pings sent | 3 h |
| **Tue** | Zone rationale + building list. Reference FER Table 1 safety systems counts. | `layout/zones.md`, `layout/building_list.md` | 4 h |
| **Wed** | Block-level layout diagram (Mermaid). Mid-week self-review. | `layout/block_layout.{mmd,png}` | 4 h |
| **Thu** | Flow arrows diagram + integrate any teammate input received. | `layout/flow_arrows.{mmd,png}` | 3 h |
| **Fri** | Auxiliary systems list + electrical/emergency power narrative. Cross-artifact audit. | `layout/aux_systems.md` + audit findings | 4 h |
| **Sat** | Buffer + apply audit fixes + optional stretch (scale_plan_2d, isometric). | (stretch items) | 3 h |
| **Sun** | Briefing script. | `planning/briefings/MB_W2_Layout.md` | 2 h |

---

## Step 5 — EXECUTE: file conventions

- All deliverables in `layout/` (FER §8.10) — §8.8 aux systems also live here for the week, can move later to `aux/` if it grows.
- Diagrams: Mermaid `.mmd` source + rendered `.png` via the standard pipeline (see `README.md`).
- Cross-reference back to `safety/`, `ic/` whenever a layout decision is constrained by a safety or I&C requirement.
- Every distance, area, weight stated with units. Mark `[ASSUMED]` or `[SIM-PENDING]` per `TASK_PROCESS.md`.

### Building list — preview structure (Day 2 deliverable)

| ID | Building | Function | Footprint (m²) | Height (m) | Seismic | Source |
|---|---|---|---|---|---|---|
| RXB | Reactor Building | Houses RPV + containment | TBD | TBD | Cat I | this work |
| TB | Turbine Building | Steam turbine + generator | TBD | TBD | Cat II | this work |
| AB | Auxiliary Building | Radwaste, CVCS, sampling | TBD | TBD | Cat I | this work |
| CB | Control Building | MCR + switchgear + I&C | TBD | TBD | Cat I | constrained by `ic/ic_architecture.md` §4 |
| SFB | Spent Fuel Building | Wet pool + dry-cask staging | TBD | TBD | Cat I | this work |
| DGB | Diesel Generator Building | 2× emergency diesel | TBD | TBD | Cat I | FER Tbl 1 |
| EHB | Electrical/Switchyard | Main transformers + 33 kV interface | TBD | TBD | Cat II | this work |
| CTW | Cooling Tower | Heat sink | TBD | TBD | Non-safety | [ASSUMED] cooling tower |
| TES | TES Building | Thermal energy storage modules | TBD | TBD | Non-safety | Alisher input |
| SOE | SOE Building | H₂ electrolyser units | TBD | TBD | Non-safety | Alisher input |
| H2S | H₂ Storage yard | Compressed H₂ tanks | TBD | TBD | Non-safety, NFPA 2 zoned | this work |
| WMB | Waste Management Building | Liquid/solid radwaste processing | TBD | TBD | Cat I | this work |

### Auxiliary systems list — preview structure (Day 5 deliverable)

Organized under FER §8.8 sub-headings: each system gets purpose · operating principle · layout location · safety function (yes/no) · performance · maintenance.

1. HVAC — RXB, AB, CB sub-systems
2. Fire protection — detection + suppression + compartmentalization
3. Radiation protection / monitoring — area, process, personnel
4. **Emergency power** — 2× EDG, UPS/batteries (8 h), Class 1E bus
5. Electrical distribution — switchyard, main + unit-aux transformers, station service
6. Fuel handling — refueling machine, transfer canal, SFP cleanup
7. Waste handling — liquid (clean/dirty/chem), solid (compactor), gaseous (HEPA + charcoal)
8. Service systems — compressed air (instrument + service), demin water, SFP cooling

---

## Step 6 — AUDIT: end-week cross-checks

Will run on Fri after deliverables 1–5 are complete. Checks against:

- All 11 FER §8.10 + §8.8 requirements either ✓ or △ with explicit reason
- Every footprint number sourced or `[ASSUMED]`
- Every building tied to a function — no orphan boxes in the diagram
- Cross-references resolve to actual files (e.g. claim of "EPZ 0.5 km" matches `safety/safety_criteria.yaml`)
- Diagram + table + prose tell the same story (no drift)
- H₂ separation distance respected on the diagram (≥ 100 m from RXB)
- Hot/safety/conventional zones clearly distinct

Output: `layout/fer_8_10_coverage.md` analogous to `ic/fer_8_7_coverage.md`.

---

## Step 7 — BRIEF: end-week scripted briefing

`planning/briefings/MB_W2_Layout.md` — 10-min script targeting team + supervisor.

Headline narrative will be:
> "Layout is the integration drawing. Every team's output ends up taking floor space; my job this week was to give each one a defensible place to stand. Reactor and safety systems in one island; turbine and electrical in another; TES, SOE, and hydrogen in a third — with a separation distance dictated by hydrogen explosion physics, not by aesthetics. Each block traces back to a number — RPV from Samira, TES from Alisher, EPZ from my safety table."

---

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Teammate input doesn't arrive in time | Use `[ASSUMED]` defaults from standard SMR practice; flag in deliverable so it's an obvious swap target |
| 3D plan (R4) requires real CAD beyond Mermaid | Ship isometric draw.io view for W2; promise CAD-level for W3+ |
| Critical piping (R6) needs Adilbek's pipe sizes | Build the *table structure* with TBD; populate when his data lands |
| H₂ exclusion-zone math complicated | Use NFPA 2 simple distance rule (100 m for bulk H₂ near occupied building); refine in W3 |
| Site assumption flipping (coastal vs inland) would force redo | Lock as `[ASSUMED]` with explicit dependency; supervisor decision blocks at most the cooling block, not the whole layout |
| FER 120-page budget | Layout will be ~6–10 pp in FER; compress diagrams |

---

## Coordination — pings to send Monday

```
TO: Adilbek (OpenFOAM / T-H)
Need by Wed: primary loop pipe diameters (hot leg, cold leg, surge line), 
main steam pipe diameter, FW pipe diameter, any routing constraints from 
your CFD work. Drives FER §8.10 R6 critical piping. Reply even rough 
ballpark — will tag preliminary.

TO: Alisher (TES / SOE)
Need by Wed: TES module footprint (m²) and stacking height; SOE unit 
footprint per electrolyser stack; H₂ daily production target (kg/day); 
H₂ storage form (tube trailer vs stationary tank vs salt cavern). 
Drives industrial-island sizing.

TO: Samira (OpenMC)
Need by Mon: confirm RPV envelope I'm reading from your materials.xml 
(~2.44 m OD × ~3 m tall active region — does that include head/lower 
plenum?). Also: number of fuel assemblies in your *target* design — 
your 2D model uses 21 fuel positions; FER Table 1 example shows 240. 
Big number drives RXB size.

TO: Supervisor
Need by Mon: (1) site assumption — inland Turkey vs coastal? (2) heat 
sink type — closed cooling tower (siting flexible) vs open seawater 
(coastal only, cheaper). Locks decisions L4 + much of the conventional 
island layout. If undecided, fine — I'll proceed with closed cooling 
tower as documented [ASSUMED] and revisit when you decide.
```

---

## EOW self-check

- [ ] All 5 hard deliverables present and named per `_INDEX.md`
- [ ] All 11 FER §8.10 + §8.8 requirements graded ✓/△/✗ in coverage doc
- [ ] Every building has function + footprint + seismic class
- [ ] Block diagram renders cleanly to PNG (use the standard pipeline)
- [ ] Flow arrows diagram shows all 6 flow types (steam, FW, electrical, heat, H₂, waste/fuel)
- [ ] Aux systems list covers all 8 categories with §8.8 metadata (purpose/principle/layout/safety/performance/maintenance)
- [ ] No diagram or table cites a number not also stated in another doc — single source of truth
- [ ] `_INDEX.md` in `layout/` updated with the new files
- [ ] Locked decisions L1–L7 visible (this file + `README.md` table)
- [ ] Briefing script written

---

*End of W2 layout plan. Process per `planning/TASK_PROCESS.md`.*
