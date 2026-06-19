# Aegis-40 — TCES Adoption + Seawater One-Shot Recut: Execution Record & Engineering Rationale

*Standalone deliverable. Owner: Azamhon (3S / I&C / FOM / layout). Date: 2026-06-19.*
*Executes `planning/NEXT_TCES_recut_prompt.md` Steps 0–3, jointly with the C2 seawater Track-A/B from `planning/seawater_cooling_safety_fom_audit_2026-06-19.md`.*
*Scope: implement two team decisions — (C2) once-through Black Sea seawater cooling and (C3) Thermochemical Energy Storage (TCES) — across safety, layout, FOM, and graphics in one coordinated recut.*

> **Non-proliferation guardrail.** Both changes are balance-of-plant / secondary-side only — no impact on fuel, the once-through fuel cycle, enrichment, the primary boundary, or any fissile stream. Nothing here is structured for or usable for weapons development or for defeating proliferation resistance. Aegis-40 remains once-through, boron-free, self-protecting, with no separated-fissile stream anywhere in the plant.

---

## 0. Result at a glance

| Step | Action | Status |
|---|---|---|
| 0 | Lock TCES working pair | ✅ **Zeolite-13X / water-vapour sorption** locked, with rationale |
| 1 | Text/data reconciliation (kill Therminol + cooling-tower) | ✅ 11 files edited |
| 2 | Safety review of TCES coupling + load-following | ✅ 3 safety files edited; 2 new YAML criteria; UHS conflation fixed |
| 3 | One-shot graphical recut (seawater + TCES) | ✅ Mermaid×2, SVG×2 (+PNG re-render), CAD rebuilt; ⚠ **PFD PNG = 1 manual redraw left** |

**24 files modified + 2 companion docs.** CAD STEP rebuilt (307 site solids), both site PNGs re-rendered, all edited YAML re-parsed clean, `wfom.py` re-run green. The only artifact that could not be auto-updated is the binary PFD (`docs/aegis40_pfd.drawio.png`) — no editable source exists.

---

## 1. Step 0 — TCES working-pair decision (locked)

**Decision: TCES = zeolite-13X / water-vapour adsorption.** Confirms the FER-draft default; the two-tank sensible **Therminol-66** option is superseded.

### 1.1 Engineering rationale

| Criterion | Zeolite-13X / H₂O (CHOSEN) | Salt hydrate (e.g. SrBr₂·6H₂O) | Two-tank Therminol-66 (rejected) |
|---|---|---|---|
| Storage physics | Thermochemical sorption (charge = dehydration, discharge = hydration) | Thermochemical hydration | Sensible only (no reaction) |
| Energy density | ~150 kWh/m³ — moderate | higher (~250+) | low (~60–80) |
| Charge T | ~280 °C pass-out steam (FER draft) | ~80–120 °C | 265/268 °C tanks |
| Discharge T | ~150–200 °C → district heat | ~60–80 °C | ~250 °C |
| Hazard | **Non-toxic, non-flammable, non-corrosive, stable** | deliquescence, corrosion, hydration-rate issues | hot organic fluid (fire, degradation) |
| Loss self-discharge | ~zero (chemical potential held) | low | continuous thermal loss |
| Maturity | proven adsorption medium | developmental | mature but sensible-only |

**Why zeolite-13X wins for Aegis-40:** it is the only candidate that combines (a) **near-zero self-discharge** (chemical, not sensible — heat can be held for long off-peak/on-peak shifts without loss), (b) an **intrinsically low safety hazard** (a benign, non-toxic, non-flammable mineral — important for a nuclear-coupled heat-utilization unit under SSR-2/1 Req 35), and (c) **proven engineering**. The lower energy density vs salt hydrates is acceptable at the ~390 t / 30×30 m building scale already allotted. `[ALISHER]` confirms bed mass/footprint/round-trip η.

### 1.2 Why TCES helps load-following + thermal management — and why that is a *safety* upside

The reactor's strength (an integral PWR with negative coefficients and a steady SBF core) is **baseload steadiness**. Forcing it to chase grid load with deep power maneuvers would aggravate xenon transients, MTC swing, and — critically — the **already-flagged peaking** (`f_q_total` 3.478 > 2.50, `open_item: peaking_recompute`).

TCES **decouples** the two: the reactor runs near-baseload; **the storage absorbs the swing.**
- **Off-peak / surplus heat:** divert pass-out steam to *charge* the zeolite bed (dehydration). Reactor stays at power; grid electrical output drops without a deep reactor ramp.
- **Peak demand:** *discharge* the bed (hydration) into the district-heat intermediate loop, freeing turbine steam for electricity.

This is the **thermal-management** claim made concrete, and it is a **safety argument**: the plant follows load **without deep reactor maneuvering**, so the load-following mode does **not** aggravate the peaking/xenon/MTC challenges. Documented in `safety_criteria.yaml` notes and `hazards_register.md`.

---

## 2. Step 1 — Text / data reconciliation (executed)

Every reference to a cooling tower / Therminol two-tank was removed or struck through and replaced with the seawater + TCES design.

| File | Change |
|---|---|
| `layout/zones.md` | CI building list: CTW → CWP house + seawater intake/outfall; CI footprint note (smaller); §2.3 II: TES → TCES zeolite-13X; **new decisions Z8 (TCES) + updated Z6/Z7**; open-items #4 resolved; safety-UHS-≠-normal-sink note added |
| `layout/building_list.md` | CTW row deleted → **CWP (240 m²) + INTK + OUTF** rows; TES row → TCES zeolite-13X (~390 t); CI subtotal recomputed (4 450 → **3 790 m²**); R2 coverage updated; open-items #4/#7 resolved |
| `layout/critical_piping_table.md` | Row 3 → **TCES charging branch** (dehydration steam); Row 8 → seawater once-through finalized (INTK→CWP→condenser→OUTF, ~2–2.5 m³/s, Black Sea 8–25 °C); **new Row 9 CCWS → seawater**; follow-ups updated |
| `layout/aux_systems.md` | §9 SFP cooling sink → seawater (normal) with safety-UHS clarification; §9a cogen intro → TCES zeolite-13X + load-following framing |
| `layout/fer_8810_docx_audit.md` | C3 marked **RESOLVED (TCES)**; C2 text done; verdict update flagging PFD as the remaining manual redraw |
| `layout/fer_8_10_coverage.md` | R2 building list CTW → CWP + seawater |
| `README.md` | Open item #6 (seawater) + new #6b (TCES) marked resolved; Akkuyu realism noted |
| `fom/reactors/aegis40.yaml` | `plant_footprint_m2` 20000 → **19340** (CTW freed); cooling/TCES implications documented as comments (no rating inflation) |
| `fom/parameters_schema.yaml` | `freshwater_consumption` proposed as an **inactive, commented** sustainability param (activation requires competitor data + independent weights) |
| `cad/README.md` | Layout-basis line updated to seawater + TCES |
| `fom/outputs/wfom_report.md` | Regenerated by re-running `wfom.py` |

---

## 3. Step 2 — Safety review of the TCES coupling + load-following (executed)

### 3.1 SSR-2/1 Req 35 (heat-utilization coupling)
The TCES bed sits **downstream of the existing 3-barrier cogen isolation** (`aux_systems.md §9a`: SG tube + non-radioactive intermediate loop held clean-side-high + customer HX, with fail-closed ESFAS isolation). The thermochemical charge/discharge does not add a radionuclide pathway — confirmed; no change to the `cogen_radionuclide_isolation` barrier count.

### 3.2 Load-following transients
Because TCES carries the swing and the reactor stays near-baseload (§1.2), load-following does **not** aggravate `mtc_full_power`, `mdnbr_transient`, or the flagged `f_q_total`/`f_delta_h_radial`. **Caveat carried forward:** do not *certify* load-following until `peaking_recompute` (Samira, due now) resolves whether the peaking breach is real or a mesh artifact.

### 3.3 TCES material hazards — new register row
Added to `safety/hazards_register.md`: bed over-temperature / vessel over-pressure / dust / loss-of-charge. Zeolite-13X is **non-toxic, non-flammable, non-corrosive** → intrinsically low hazard; bed isolated, charge-steam relief + temperature/pressure interlocks; **loss-of-charge is a power-conversion event, not a safety event.**

### 3.4 Heat-sink terminology correction (the highest-value safety finding)
The seawater audit identified a **UHS conflation** that had propagated into two files. Both are now corrected, and the distinction is locked into the spine YAML:

- **Normal heat sink = once-through seawater** (power operation, **non-safety-classified**, TECDOC-1936 graded). Also serves CCWS and TCES.
- **Safety ultimate heat sink = passive IRWST + containment cooling** (atmosphere-coupled, **seawater-independent**, ≥72 h grace).

Implemented:
- `safety/safety_criteria.yaml` — **2 new hard-constraint criteria**: `ultimate_heat_sink` (Req 53; asserts seawater/TCES loss does not challenge the safety sink) and `coastal_external_hazard` (SSR-1/SSG-9; tsunami/surge/marine-blockage as design-basis). Plus structural fixes: `design_id` rev_0 → **rev_3-safety_r1**; `cycle_length` DiD `0` → `null`; `tolerance` documented in the schema header. **34 criteria total, parses clean.**
- `safety/regulatory_alignment_audit.md` — Req 51–53 row corrected (was wrongly "UHS = seawater").
- `safety/hazards_register.md` — external-flooding row reworded; **new marine-intake-blockage row** (CCF of the normal sink only, bounded by `ultimate_heat_sink`).

---

## 4. Step 3 — One-shot graphical recut (executed, minus the PFD)

Both C2 (seawater) and C3 (TCES) being settled unblocked the single recut the team deferred to avoid drawing twice.

| Artifact | Change | Verified |
|---|---|---|
| `layout/block_layout.mmd` | CTW node → CWP (seawater); TES → TCES zeolite-13X; **new SEA node** + intake/return arrows; class lists updated | source edited ✅ (PNG re-render needs mermaid CLI — not installed) |
| `layout/flow_arrows.mmd` | Condenser → **Black Sea once-through** (intake + warm return); TES → TCES bed; surplus-steam charge arrow | source edited ✅ (PNG pending mermaid) |
| `layout/drawings/site_plot_plan.svg` | CTW block → CWP house + shoreline SEA intake/outfall; "circ water → sea"; "process steam → TCES bed"; legend + header note | **PNG re-rendered ✅** |
| `layout/drawings/site_elevation.svg` | CTW (20 m) → CWP house (10 m); TES → "TCES" | **PNG re-rendered ✅** |
| `site/index.html` (web viewer) | CTW entry → CWP (seawater); TES → TCES zeolite-13X; elevation + plan-pipe annotations | source edited ✅ |
| `cad/build_aegis40_cad.py` → `aegis40_site.step` | Cooling-tower solids removed → CWP house + shoreline intake/screen-house; two-tank Therminol → TCES sorption bed | **STEP rebuilt ✅ (307 solids)** |
| `docs/aegis40_pfd.drawio.png` | drop CT-1 + two-tank Therminol; add seawater intake/outfall + TCES bed | ⚠ **manual — binary PNG, no source** |

The re-rendered plot plan was visually confirmed: CWP, SEA intake/outfall, "circ water → sea", "process steam → TCES bed", and updated legend all present.

---

## 5. FOM treatment — deliberately conservative

Per this project's own FOM-defensibility findings (`seawater_cooling_safety_fom_audit_2026-06-19.md §4`), I **did not hand-tune weights or invent competitor data** to make the cooling/TCES change look favourable — that would repeat the very root causes (F1 self-referential weighting, F3 data asymmetry) flagged as making the FOM indefensible.

What I *did* change:
- **Factual:** `plant_footprint_m2` 20000 → 19340 (CTW genuinely freed). This flows through `footprint_per_mwe` → economic score. Re-ran `wfom.py`: ranking unchanged (**NuScale > Aegis-40 > CAREM-25 > SMART**); Aegis-40 absolute utility 0.460 → 0.462.
- **Documented, not activated:** `freshwater_consumption` added as a commented, inactive parameter (once-through ≈ 0 makeup vs ~2–3 % evaporative-tower loss). Activation is gated on competitor data from the IAEA booklet + independent weight elicitation.
- **Not inflated:** thermal-efficiency rating and capacity factor held at 40 MWe/125 MWth and 0.95 — the cold-seawater η benefit is real but stays unclaimed until the cycle number is confirmed.

Aegis-40 still **fails its own hard gate** (peaking 3.478 > 2.50); the report continues to flag DESIGN_FAILED and uses the de-peak target only with that disclosure.

---

## 6. Verification performed

- `safety/safety_criteria.yaml`, `fom/reactors/aegis40.yaml`, `fom/parameters_schema.yaml` — **re-parsed with PyYAML, all clean** (34 safety criteria; both new UHS rows present).
- `fom/wfom.py` — **re-run green**, report regenerated; footprint change propagated, ranking stable.
- `cad/build_aegis40_cad.py` — **rebuilt** `aegis40_site.step` (307 solids) + `aegis40_rxb.step` via the build123d venv with no errors.
- `site_plot_plan.png`, `site_elevation.png` — **re-rendered** @2x and the plot plan visually inspected.
- Repo-wide grep sweep — no live cooling-tower / Therminol / molten-salt references remain in the design files (only intentional decision-history strike-throughs and "freed-CTW" explanations).

---

## 7. What remains (carried open items)

| # | Item | Owner | Why blocked |
|---|---|---|---|
| 1 | **PFD redraw** (`docs/aegis40_pfd.drawio.png`) — drop CT-1 + two-tank Therminol, add seawater intake/outfall + TCES bed | Azamhon | binary PNG, no editable source; manual draw.io session. **Blocks FER figures cut from the PFD.** |
| 2 | Mermaid PNG re-render (`block_layout.png`, `flow_arrows.png`) | Azamhon | `mmdc` not installed in this environment; sources are updated and correct |
| 3 | TCES bed mass / footprint / round-trip η / dispatch profile | `[ALISHER]` | his TES/SOE scope; placeholders used |
| 4 | `peaking_recompute` (F_q/F_ΔH real vs mesh artifact) | Samira (due now) | gates load-following certification + the FOM headline |
| 5 | `[VERIFY-SKKY]` seawater thermal-discharge ΔT limit | Azamhon | exact Turkish SKKY clause not machine-verified |
| 6 | C1 (two vs three islands), C5 (dry vs submerged-pool containment) | team / supervisor | independent of C2/C3; keep CAD/PFD containment concept-neutral |
| 7 | Activate `freshwater_consumption` in FOM | Azamhon | needs competitor data + independent weights |

---

## 8. Decision log (lock these)

1. **C3 = TCES, zeolite-13X / water-vapour sorption** (supersedes two-tank Therminol-66). Rationale §1.
2. **TCES is the primary load-following mechanism** — reactor stays near-baseload; storage carries the swing → safety upside, no aggravation of peaking/xenon/MTC.
3. **Normal heat sink = seawater (non-safety); safety UHS = passive IRWST/PCC (seawater-independent).** Now enforced by `safety_criteria.yaml` `ultimate_heat_sink`.
4. **No FOM weight self-tuning** for the cooling/TCES change; only the factual footprint update applied.

*End of execution record. 24 files changed, 2 new criteria, CAD + PNGs rebuilt, 1 manual PFD redraw outstanding. Companions: `NEXT_TCES_recut_prompt.md`, `seawater_cooling_safety_fom_audit_2026-06-19.md`.*
