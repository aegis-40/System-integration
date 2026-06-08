# layout/ — FER §8.10 Facility Layout + §8.8 Auxiliary Systems

**Active scope (opened 2026-06-02).** Working plan: `planning/W2_Layout_Plan.md`.

**Current contents:**

| File | Status | Description |
|---|---|---|
| `zones.md` | ✅ Day 1 | 3-island scheme (Nuclear / Conventional / Industrial), 6 locked decisions Z1–Z6, ASCII site envelope |
| `building_list.md` | ✅ Day 1 | 14 buildings + 5 infrastructure items, footprints first-cut, FER §8.10 R2 coverage ✓ |
| `block_layout.mmd` + `.png` | ✅ Day 2 | Mermaid block-level facility layout · 3 islands color-coded · 6 inter-system connections labeled · mid-week self-review passed (1 fix L6 applied) |
| `flow_arrows.mmd` + `.png` | ✅ Day 3 | Process-flow view: 6 flow types (steam/FW, electrical, district heat, H₂, fuel handling, radwaste) · 6 color-coded streams from RPV |
| `aux_systems.md` | ✅ Day 5 | FER §8.8 auxiliary systems: 8 systems, six-field metadata each (purpose/principle/layout/safety/performance/maintenance) · A1–A3 ✅, A4–A5 △ W3 · consolidated electrical single-line |
| `fer_8_10_coverage.md` | ✅ Audit | Coverage check vs all 11 FER §8.10 R1–R6 + §8.8 A1–A5 requirements (parallels `ic/fer_8_7_coverage.md`) |
| `openmc_rev3_alignment.md`† | ✅ | (in `safety/`) cross-check of Samira's rev_3 vs safety criteria |

**Scaled engineering drawings — `drawings/` (W3, 2026-06-08):**

| File | Status | Description |
|---|---|---|
| `drawings/site_plot_plan.{svg,png}` | ✅ | To-scale site plan (1:333): 3 islands, 14 buildings to footprint, EPZ inset, H₂ stand-off, [ASSUMED] piping. **FER §8.10 R3 + R6.** |
| `drawings/rxb_floor_plan.{svg,png}` | ✅ | Reactor building interior (1:50): containment Ø15 m, RPV Ø2.44 m, 21-FA core [rev_3], refuel cavity, transfer canal, penetrations. **R3.** [CONCEPTUAL] |
| `drawings/site_elevation.{svg,png}` | ✅ | Vertical section (vertical 1:125 true): below-grade reactor, grade line, building heights, off-gas stack. **R3→R4 bridge.** |
| `drawings/mcr_floor_plan.{svg,png}` | ✅ | Control room layout (1:40): consoles, LDP, STA, hardwired safety panel. **FER §8.7 §4.1 + R3.** [CONCEPTUAL] |
| `drawings/render.sh` | ✅ | SVG→PNG @2× via chrome-headless-shell |

Plan: `planning/W3_Drawings_Plan.md`.

**Still planned (post-W3):**
- True 3D / isometric (§8.10 R4 full) — deferred; would install OpenSCAD
- `critical_piping_table.md` with real NPS — FER §8.10 R6, blocked on Adilbek
- Per-system P&IDs (§8.8 A4) + formal electrical single-line (A5)
- Weight-distribution table (§8.10 R5) — blocked on foundation engineer

Cross-refs:
- Reactor footprint + RPV dimensions ← `Aegis-40 2D test/` geometry (Samira)
- TES/SOE space requirements ← Alisher (energy team)
- Piping/flow requirements ← Adilbek (T-H team)
- EPZ → `safety/safety_criteria.yaml` row `epz_radius`
