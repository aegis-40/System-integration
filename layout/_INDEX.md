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

**Planned next (W3):**
- Per-system P&IDs (FER §8.8 A4) + formal electrical single-line drawing (A5)
- `critical_piping_table.md` — FER §8.10 R6 (depends on Adilbek pipe NPS)
- 3D / isometric building view (§8.10 R4 upgrade beyond block diagram)
- Weight-distribution table (§8.10 R5) — needs foundation engineer
- `planning/briefings/MB_W2_Layout.md` — end-week briefing script

Cross-refs:
- Reactor footprint + RPV dimensions ← `Aegis-40 2D test/` geometry (Samira)
- TES/SOE space requirements ← Alisher (energy team)
- Piping/flow requirements ← Adilbek (T-H team)
- EPZ → `safety/safety_criteria.yaml` row `epz_radius`
