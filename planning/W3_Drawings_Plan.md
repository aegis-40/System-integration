# W3 Plan — Facility Layout Drawings (FER §8.10 R3/R4/R6)

**Owner:** Azamhon · **Started:** 2026-06-08 · **Process:** `planning/TASK_PROCESS.md`
**Builds on:** W2 layout (`layout/zones.md`, `building_list.md`, `block_layout.png`, `flow_arrows.png`, `aux_systems.md`).
**Goal:** turn the W2 *schematic* block diagram into **to-scale engineering drawings** the FER §8.10 demands.

---

## 1. What FER §8.10 still wants (gap from W2 audit)

From `layout/fer_8_10_coverage.md`, the deferred-to-W3 items:

| FER req | Demand | W2 status | This plan |
|---|---|---|---|
| R3 | **2D plans** of main buildings + connections | △ schematic only (block_layout) | ✅ scaled site plot plan + building floor plans |
| R4 | **3D plans** | △ none | ⏸ deferred this round (user decision 2026-06-08) — 2D first |
| R5 | Structural-spec tables (weights, steel) | ✗ gap | ⛔ blocked — needs foundation engineer |
| R6 | **Critical piping** shown | △ named only | ◐ routes drawn `[ASSUMED]`; NPS blocked on Adilbek |

---

## 2. Deliverables this round (4 drawings)

| # | File | View | FER | Data confidence |
|---|---|---|---|---|
| D1 | `layout/drawings/site_plot_plan.{svg,png}` | Scaled site plot plan | R3 + R6 | **High** — footprints from `building_list.md` |
| D2 | `layout/drawings/rxb_floor_plan.{svg,png}` | Reactor building interior | R3 | **Medium** — RPV/containment dims real (rev_3); internal arrangement conceptual |
| D3 | `layout/drawings/site_elevation.{svg,png}` | Vertical section / elevation | R3→R4 bridge | **High** — heights from `building_list.md` |
| D4 | `layout/drawings/mcr_floor_plan.{svg,png}` | Main control room layout | §8.7 §4.1 + R3 | **Medium** — console set from `ic_architecture.md`, arrangement conceptual |

---

## 3. Drawing conventions (apply to all 4)

- **Tool:** hand-authored SVG → PNG via `layout/drawings/render.sh` (chrome-headless-shell @2×). matplotlib is broken in the local env; no inkscape/drawio. SVG = exact-scale, version-controllable, zero-dependency.
- **Units:** metres. Every drawing carries a **scale bar** + **scale ratio** + (site/plan views) a **north arrow**.
- **Colour key by island** (consistent with intent of `block_layout`):
  - Nuclear Island — blue `#cfe8ff` fill / `#1b4965` stroke (Seismic Cat I)
  - Conventional Island — amber `#ffe8b3` fill / `#9a6700` stroke (Cat II)
  - Industrial Island — green `#d8f3dc` fill / `#2d6a4f` stroke (non-safety); H₂ hazard hatched red
- **Tags on the drawing itself:** `[ASSUMED]`, `[SIM-PENDING]`, `[rev_3]`, `[CONCEPTUAL]` so a reviewer sees confidence at a glance.
- **Single source of truth:** every dimension must already exist in `building_list.md` / `safety_criteria.yaml` / rev_3 — no new numbers invented silently.

---

## 4. Per-drawing data + scale

### D1 — Site plot plan
- **Source:** `building_list.md` §3 footprints; `zones.md` §4 envelope; `safety_criteria.yaml` `epz_radius` (0.5 km).
- **Scale:** ~3 px/m for the ~250 × 300 m developed area (legible buildings). EPZ (R = 500 m) shown via annotated boundary arc + a small locator inset (full circle can't share scale with 25 m buildings).
- **Contents:** 3 island envelopes; all 14 buildings to footprint; H₂ 100 m stand-off ring; `[ASSUMED]` piping routes (main steam, FW, surge, RHR) NI↔CI; north arrow; scale bar.
- **R6 note:** piping shown as routes tagged `[ASSUMED]`; line weights notional until Adilbek gives NPS.

### D2 — RXB floor plan
- **Source:** rev_3 (`openmc_rev3_alignment.md`): RPV Ø 2.44 m, 21 FA core; `building_list.md`: RXB 25×25 m, containment Ø ≈ 15 m.
- **Scale:** ~20 px/m (building is only 25 m → needs a large scale to show RPV).
- **Contents:** RXB outer wall 25×25; containment circle Ø 15 m; RPV Ø 2.44 m centred; refuel pool + transfer canal to SFB; polar crane swing radius; consolidated penetration zone (AB side); equipment hatch. **Tag `[CONCEPTUAL]`** — internal arrangement is illustrative, not a stress-analysed layout.

### D3 — Site elevation / section
- **Source:** `building_list.md` heights; `zones.md` below-grade decision (RPV head ~5 m below grade).
- **Scale:** ~3 px/m horizontal matched, vertical exaggeration noted if used.
- **Contents:** grade line; below-grade reactor cavity (+15 m below per RXB row); RXB 30 m above grade; containment; CB 12 m; TB 15 m; CTW 20 m; off-gas stack ≥30 m. Shows the seismic/below-grade story.

### D4 — MCR floor plan
- **Source:** `ic/ic_architecture.md` §4.1.
- **Scale:** ~25 px/m.
- **Contents:** primary (reactor-operator) console, secondary (BOP) console, STA station, 4×80" overview display panel wall, large overview display, paper-procedure cabinet, entry/egress. Tag `[CONCEPTUAL]` arrangement.

---

## 5. Steps remaining (checklist)

- [x] Probe tooling, set up `render.sh`, verify SVG→PNG
- [x] This plan doc
- [x] D1 site plot plan
- [x] D2 RXB floor plan
- [x] D3 site elevation
- [x] D4 MCR floor plan
- [x] Update `layout/_INDEX.md` + coverage delta in `fer_8_10_coverage.md` (R3 △→✓, R4 partial)
- [x] Commit + push to System-integration

**Still blocked after this round (not in scope here):**
- R4 true 3D — deferred (would install OpenSCAD)
- R5 weights/steel — needs foundation engineer
- R6 exact pipe NPS — needs Adilbek (routes drawn `[ASSUMED]` meanwhile)
- RXB internal arrangement validation — needs Samira final RPV height + mechanical (CRDM type)

---

## Next steps — updated 2026-06-09

**Done since W3:**
- ✅ Interactive web layout viewer `site/index.html` — classic-white, 5 native-SVG views incl. a bird's-eye **3D axonometric massing** (covers R4 at "stylised 3D" level, beyond the elevation). Hosted-ready (GitHub Pages one step away).
- ✅ **3S Safeguards / non-proliferation** deliverable `safety/safeguards_nonproliferation.md` — reactor-grade, self-protecting, once-through discharge from rev_3 depletion. Closes the third "S".

**Next, in priority order:**
1. **CRDM type** from Samira (still the #1 open) → unlocks rod-ejection accident basis + RXB internal validation.
2. **Adilbek pipe NPS** → `critical_piping_table.md` (R6) + swap `[ASSUMED]` routes on `site_plot_plan` and the viewer.
3. **Alisher TES/SOE footprint + H₂ inventory** → finalise Industrial-Island sizing + maybe shrink the 100 m stand-off.
4. **FOM scoring tool** (`planning/PLAN.md`, 9 phases) — still unstarted; unblocked once hard-constraint normalizers (MDNBR/PCT from OpenFOAM) land.
5. Optional FER polish: pull safeguards plots (pu_vector / self_protection / snm) into the §3S figure set; push the viewer's iso view further (shadows/trees/roads) if a showcase image is wanted; deploy the viewer to GitHub Pages.
6. **Supervisor:** site type (inland/coastal) + heat sink; 10 sign-offs from `MEETING_BRIEF` §4.

*Photoreal 3D render (NuScale-style) intentionally NOT pursued — 3D-viz pipeline, not an FER-scoring task. The SVG iso massing is the in-repo answer.*

---

*End of W3 drawings plan.*
