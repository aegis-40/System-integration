# FER §8.10 (Facility Layout) + §8.8 (Auxiliary Systems) — line-by-line coverage check

*Purpose: confirm every discrete requirement in FER §8.10 + §8.8 has a specific, sensible answer in the W2 layout deliverables. Each row graded on whether the answer is physically/logically coherent — not tick-box.*

*Reviewed: 2026-06-05. Owner: Azamhon. Parallels `ic/fer_8_7_coverage.md`.*

---

## Legend

- ✓ **fully addressed** — answer present, specific, internally consistent
- △ **partially addressed** — answer present but weak/incomplete, or deliberately deferred with structure in place
- ✗ **gap** — requirement unanswered
- 🐞 **defect** — a statement is technically wrong and must be fixed

---

## 1. §8.10 R1 — general layout considering 4 factors

> *"General layout considering constructability, economic efficiency, safety, and operations."*

| Factor | Where | ✓ |
|---|---|---|
| Constructability | `zones.md` §2 (common mat foundation, below-grade RPV), `building_list.md` §2 | ✓ |
| Economic efficiency | `building_list.md` §4 (site/built ratio ~8:1, 10 ha plot with margin) | ✓ |
| Safety | `zones.md` §1 (4 constraints: EPZ, SSE, isolation, H₂ stand-off) | ✓ |
| Operations | three-island access control + `aux_systems.md` electrical/HVAC | ✓ |

**Coherence:** all four FER-named factors explicitly drive a documented decision. ✓

---

## 2. §8.10 R2 — layout description covers required categories

> *"Reactor building, energy conversion, ops/maintenance services, other systems & buildings."*

Already audited in `building_list.md` §5 — all four categories populated (RXB / TB+EHB+CTW / CB+WSB+ADM / AB+SFB+DGB+WMB+TES+SOE+H2S+SEC+METEO+OFFGAS). ✓

---

## 3. §8.10 R3 — 2D plans of main buildings + connections

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 3a | 2D building-level layout | `block_layout.png` (3 islands color-coded) | ✓ |
| 3b | Connections between buildings | `block_layout` 6 labeled inter-system connections + `flow_arrows.png` | ✓ |
| 3c | **True-to-scale 2D plan** | ✅ `drawings/site_plot_plan.png` (1:333) + `rxb_floor_plan.png` (1:50) + `mcr_floor_plan.png` (1:40) | ✓ |

**✓ on 3c (W3, 2026-06-08):** to-scale drawings now exist — site plot plan (all 14 buildings to footprint, EPZ, H₂ stand-off), RXB interior floor plan, and MCR layout. Hand-authored SVG → PNG. Upgrades R3 from △ to ✓.

---

## 4. §8.10 R4 — 3D plans

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 4a | 3D plans of main buildings + connections | `drawings/site_elevation.png` (vertical section) — partial | △ |

**△ partial (W3, 2026-06-08):** a to-scale **vertical section/elevation** (`site_elevation.png`) now shows building heights, the below-grade reactor, and the seismic story — a 2.5D bridge toward R4. **A true axonometric/3D model is still not produced** (user deferred this round; would install OpenSCAD). Don't claim full 3D in the FER yet — claim "elevation + section provided; isometric 3D in progress."

---

## 5. §8.10 R5 — structural-spec tables (weights, steel, etc.)

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 5a | Building footprint + height table | `building_list.md` §3 (all buildings) | ✓ |
| 5b | Seismic class per building | `building_list.md` §3 (Cat I/II/III) | ✓ |
| 5c | **Weight distributions** | not present | ✗ **W3** |
| 5d | Steel / construction-structure specs | not present | ✗ **W3** |

**✗ on 5c/5d:** the FER asks structural-spec tables (weights, steel tonnage) as the *basis for structural specification*. These need a foundation/structural engineer and per-building mass takeoffs we don't have. **Honest gap** — flag in FER as W3+, owner = foundation engineer (`building_list.md` open item #8). Do not fabricate weights.

---

## 6. §8.10 R6 — critical piping shown

> *"Main steam, feedwater, pressurizer lines, RHR — clearly shown within/between structures."*

| # | Line | Where shown | ✓ |
|---|---|---|---|
| 6a | Main steam | `zones.md` §3 + `flow_arrows.png` (NI→CI rack) | △ |
| 6b | Feedwater | `zones.md` §3 + `flow_arrows.png` (CI→NI) | △ |
| 6c | Pressurizer surge | named in `zones.md` §3 (originates inside NI) | △ |
| 6d | RHR | named in `zones.md` §3 | △ |

**△ across the board:** all four lines are *identified* and the two that cross islands (steam, FW) are *routed* on the block/flow diagrams. But there is no **critical-piping table with NPS/diameter** — that waits on Adilbek's pipe sizes (`building_list.md` open item #6, ping sent in `W2_Layout_Plan.md`). **Recommended:** `critical_piping_table.md` structure built now, populated when his data lands. The *intra-building* routing (within RXB) is not yet drawn.

---

## 7. §8.8 A1–A5 — auxiliary systems

Audited in detail in `aux_systems.md` §11. Summary:

| FER §8.8 | Status | Note |
|---|---|---|
| A1 all technical info (vent/elec/fire/rad) | ✓ | aux_systems §2–6 |
| A2 named sub-headings present | ✓ | all 5 FER-named headings + electrical + rad-protection |
| A3 six-field metadata per system | ✓ | 8 systems × purpose/principle/layout/safety/performance/maintenance |
| A4 per-system P&IDs | △ **W3** | structure ready; drawings deferred |
| A5 on/off-site + emergency/UPS electrical | △ **W3** | narrative + ASCII single-line present (§5/§6/§10); formal drawing W3 |

---

## 8. Cross-artifact audit (W2 plan Step 6 checks)

Beyond requirement-by-requirement — does the deliverable set hold together?

| Check | Result |
|---|---|
| Every building tied to a function — no orphan boxes | ✓ all 14 buildings in `building_list.md` have a function; block diagram boxes all appear in the list |
| Every footprint sourced or `[ASSUMED]` | ✓ tags present; TES/SOE flagged `[ALISHER]`, CTW `[ASSUMED]` |
| Cross-references resolve to real files | ✓ `epz_radius`, `sse_design` exist in `safety/safety_criteria.yaml`; `ic_architecture.md` §4 MCR ref valid |
| Diagram + table + prose tell same story | ✓ 3 islands + same building IDs across `zones.md`, `building_list.md`, `block_layout`, `aux_systems.md` |
| H₂ stand-off ≥ 100 m respected on diagram | ✓ `zones.md` §4 ASCII + Z5 + `building_list.md` H2S note all state 100 m |
| Hot/safety/conventional zones distinct | ✓ Seismic Cat I (NI) / II (CI) / III (II) cleanly separated |
| Single source of truth — no number cited in only one doc | △ see defect D1 below |

---

## 9. Defects + inconsistencies found

| ID | Severity | Finding | Fix |
|---|---|---|---|
| **D1** | △ minor | Footprint totals: `building_list.md` §4 gives NI ~2 700 m² *built*, but `zones.md` §2.1 gives NI envelope ~8 000 m² (100×80). These measure different things (built area vs island envelope) but a reviewer could read them as contradictory. | Add one clarifying line in `building_list.md` §4: "built area ≠ island envelope; envelope includes circulation + separation." **Recommend apply.** |
| **D2** | △ minor | RPV height: `building_list.md` lists "~4.8 m incl. heads `[ASSUMED]`" but `W2_Layout_Plan.md` §2a says "~5 m". Cosmetic ~0.2 m drift. | Harmonize to "~4.8 m `[ASSUMED, Samira to confirm]`" — `building_list.md` is the authority. Minor. |
| **D3** | △ watch | SFP "borated" wording in `aux_systems.md` §7 conflicts with boron-free core decision #3. | Already self-flagged inline in `aux_systems.md` §7 with a note to confirm rack type (fixed absorber vs soluble). Resolve with Samira/safety. |

**No 🐞 hard defects** (nothing physically wrong like the inverted-Purdue error caught in the I&C audit). D1–D3 are consistency polish.

---

## 10. Coverage summary

| Status | Count |
|---|---|
| ✓ fully addressed | **7** |
| △ partial / deferred-with-structure | **8** |
| ✗ gap | **2** (R5 weights, R5 steel specs) |
| 🐞 hard defect | **0** |
| **Total requirements** | **11 §8.10 + §8.8 lines (R1–R6, A1–A5 = 17 sub-items)** |

W2 goal was R1–R3 + A1–A3 fully, R4–R6 + A4–A5 flagged. **Achieved:** R1 ✓, R2 ✓, R3 ✓(△ scale), A1 ✓, A2 ✓, A3 ✓. Deferred items all carry a named owner + week, none silent.

---

## 11. Fix list (prioritized)

| # | Severity | Item | File | Effort |
|---|---|---|---|---|
| F1 | ✓ DONE | D1 — clarified built-area vs envelope | `building_list.md` §4 | applied 2026-06-05 |
| F2 | ✓ DONE | D2 — harmonized RPV height to 4.8 m | `W2_Layout_Plan.md` §2a | applied 2026-06-05 |
| F3 | △ W3 | Critical-piping table (R6) — structure now, NPS when Adilbek replies | new `critical_piping_table.md` | 1 h + input |
| F4 | △ W3 | Scaled 2D plan (R3 upgrade) | `scale_plan_2d.png` draw.io | 2 h |
| F5 | △ W3 | Isometric / 3D (R4) | `isometric_view.png` | 2 h |
| F6 | ✗ W3+ | Weight + steel structural tables (R5) | needs foundation engineer | external |
| F7 | △ W3 | Per-system P&IDs (A4) + formal single-line (A5) | new diagrams | 3 h |

**No mandatory-now fixes.** F1/F2 are 7-minute consistency cleanups. F3–F7 are the W3 backlog, all already tracked in `_INDEX.md` "Planned next (W3)".

---

## 12. Sense-check — does the layout hold together?

- **Physics-driven separation, not aesthetic.** H₂ 100 m stand-off = NFPA 2; NI seismic Cat I = SSE 0.3 g; EPZ 500 m = `safety_criteria.yaml`. Every buffer traces to a number. ✓
- **No orphan flows.** Every arrow in `flow_arrows.png` originates/terminates at a building in `building_list.md`. ✓
- **Power chain ends in "no power needed."** `aux_systems.md` §10 defence-in-depth (grid→gen→EDG→battery→passive) consistent with locked passive-cooling decisions #5/#6 + 72 h grace. ✓
- **Every building traces to a number.** RPV←Samira geometry.xml, TES/SOE←Alisher (flagged pending), EPZ←my safety table, transformer←40 MWe. ✓
- **Honest about what's missing.** R4 (3D), R5 (weights), R6 (pipe NPS), A4/A5 (drawings) all explicitly deferred with owner + week — no silent gaps, no fabricated data. ✓

The layout is *internally consistent*. Remaining items are CAD-level drawings + teammate inputs, not structural problems with the concept.

---

*End of coverage check. Cross-refs: `zones.md`, `building_list.md`, `block_layout.png`, `flow_arrows.png`, `aux_systems.md`, `safety/safety_criteria.yaml`, `ic/ic_architecture.md`, FER `docs/FER_Template.docx` §8.8 + §8.10.*
