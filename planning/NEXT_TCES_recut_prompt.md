# NEXT-STEPS PROMPT — TCES adoption + post-C2/C3 one-shot recut

*Self-prompt. Paste back into a fresh session to execute. Created 2026-06-19 by Azamhon (3S/I&C/FOM/layout).*
*Trigger condition met: team decided **Thermochemical Energy Storage (TCES)** for load-following + thermal management → closes open item **C3 (TES technology)**. Combined with **C2 (once-through seawater, 2026-06-13)**, BOTH gates on the graphical recut are now cleared.*

---

## ROLE
Act as the Aegis-40 3S / I&C / FOM / layout owner. World-class nuclear engineer + safety analyst + non-proliferation expert; deep IAEA SSR-2/1 / SSG-52 / TECDOC-1936 / NUREG-1431 familiarity. Match the repo's existing file conventions (source-doc headers, `[TAG]` status flags, FER-section cross-refs, traceability to `safety/safety_criteria.yaml`).

## NON-PROLIFERATION GUARDRAIL
TCES and seawater cooling are balance-of-plant / secondary-side only. No impact on fuel, fuel cycle, enrichment, primary boundary, or any fissile stream. Keep all output peaceful-use; nothing structured for or usable for weapons development or defeating proliferation resistance. Aegis-40 stays once-through, boron-free, self-protecting, no separated-fissile stream.

## LOCKED DECISIONS (treat as team-final, like C2)
- **C3 = TCES (thermochemical energy storage).** Supersedes the two-tank sensible **Therminol-66** option shown on the current PFD. Purpose: **load-following + thermal management.**
- **C2 = once-through Black Sea seawater cooling, no cooling tower** (2026-06-13).
- FER draft basis for TCES: **zeolite-13X sorption, ~390 t, charge ~280 °C / 15 bar pass-out steam** (`docs/FER_Aegis40_8.8-8.10.docx` §8.10.2/§8.10.3) — confirm or revise the material in Step 0.

---

## STEP 0 — Confirm the TCES working pair (first sub-decision)
Before drawing anything, lock the TCES chemistry. The FER draft assumes **zeolite-13X water sorption**. Decide/confirm vs alternatives and record rationale in `layout/zones.md` (new decision row) + a short note:
- **Zeolite-13X / H₂O** (adsorption): benign, non-toxic, ~180–250 °C discharge, proven, low energy density (~150 kWh/m³). FER-draft default.
- **Salt hydrate** (e.g. SrBr₂·6H₂O, MgSO₄): higher density but hydration-rate / deliquescence / corrosion issues.
- Reject anything with a toxic/proliferation-irrelevant-but-hazardous reagent unless justified.
- Output: `[DECISION]` row + one-paragraph rationale, energy density, charge/discharge T, and the integration point (pass-out steam off the main-steam header, `critical_piping_table.md` Row 3).
- Dependency: **Alisher** owns TES/SOE sizing (mass, footprint, charge/discharge power, round-trip efficiency). Flag `[ALISHER]` where a number is his; proceed on the FER-draft figures as `[ASSUMED]` placeholders so the recut isn't blocked.

---

## STEP 1 — TEXT/DATA updates (do now; no graphics)
Reconcile every file to "TCES (zeolite-13X) + once-through seawater." Remove the Therminol-66 two-tank story wherever it appears.

| # | File | Change |
|---|---|---|
| 1 | `layout/zones.md` | Add C3 `[DECISION]` row (TCES); confirm TES Building in the energy/industrial island; drop "`molten salt [ASSUMED]`" wording → "zeolite-13X TCES". Carry the seawater Track-A edits from `seawater_cooling_safety_fom_audit_2026-06-19.md` §5.1 if not yet applied. |
| 2 | `layout/building_list.md` | TES Building row → TCES (zeolite-13X), footprint from ~390 t bed `[ALISHER]`; charge/discharge HX. Apply seawater Track-A (CTW→intake/outfall/CWP). |
| 3 | `layout/critical_piping_table.md` | Row 3 (TES charging branch) → pass-out steam ~280 °C/15 bar to the **TCES reactor/sorption bed**, not a sensible-heat tank; isolation per Req 35. |
| 4 | `layout/aux_systems.md` | §9a cogen interface: confirm the non-radioactive intermediate loop feeds the TCES bed; thermochemical charge/discharge is downstream of the 3-barrier isolation — no new radionuclide path. |
| 5 | `fom/reactors/aegis40.yaml` + `fom/parameters_schema.yaml` | Load-following raises usable **capacity_factor / dispatchability** and **non_electric_revenue_share**; reflect TCES round-trip η in the cogen revenue. Keep the FOM-defensibility fixes from the seawater audit §4 in mind (don't hand-tune to win). |
| 6 | FER §8.9 (energy storage) + §8.10 | Make the prose say TCES consistently; delete two-tank Therminol references; add the load-following/thermal-management narrative (FER §5 originality lever). |
| 7 | `layout/fer_8810_docx_audit.md` | Mark C3 RESOLVED (TCES); note PFD/§8.9/§8.10 now reconcilable. |
| 8 | `README.md` | Close the C3 open item; note the recut is now unblocked. |

---

## STEP 2 — SAFETY review of the TCES coupling + load-following
1. **SSR-2/1 Req 35** — TCES is a heat-utilization unit: confirm the existing 3-barrier isolation (`aux_systems.md §9a`) still bounds it; no radionuclide transport to the TCES bed or district-heat product in normal **or** accident states.
2. **Load-following reactivity/thermal transients** — load-follow maneuvering exercises MTC / xenon / power-distribution. Check against `safety/safety_criteria.yaml`: `mtc_full_power`, `f_q_total`/`f_delta_h_radial` (already breached — see `peaking_recompute`), `mdnbr_transient`. Confirm TCES *reduces* reactor power-ramp demand (the thermal-management claim) rather than adding transients — that's the safety upside; document it.
3. **TCES material hazards** — add to `safety/hazards_register.md`: bed over-temperature, steam/pressure in the sorption vessel, dust (zeolite), loss-of-charge. Zeolite-13X is non-toxic/non-flammable → low hazard; state it.
4. **Heat-sink clarity** — keep the `seawater_cooling_safety_fom_audit_2026-06-19.md` distinction: TCES + seawater are both **normal-operation** systems; the **safety UHS stays passive (IRWST + PCC)**. Apply the new `ultimate_heat_sink` / `coastal_external_hazard` YAML rows from that audit if not yet committed.

---

## STEP 3 — GRAPHICAL RECUT (the one-shot — now unblocked by C2+C3)
Redraw once, with seawater cooling AND TCES, per `seawater_cooling_safety_fom_audit_2026-06-19.md` §5.2 Track B:

| Artifact | Change | Tool |
|---|---|---|
| `docs/aegis40_pfd.drawio.png` (+ drawio source) | **Headline.** Drop CT-1 + tower loop → seawater intake/condenser/outfall. Drop two-tank Therminol (TK-C/TK-H, IHX E-2, boiler E-3) → **TCES zeolite bed** with charge (steam→bed) / discharge (bed→district heat) paths off the main-steam header. | draw.io |
| `layout/drawings/site_plot_plan.svg` + `.png` | CTW→seawater structures; TES block = TCES | render.sh |
| `layout/drawings/site_elevation.svg` + `.png` | Same | render.sh |
| `layout/block_layout.mmd` + `.png` | Drop CT + Therminol nodes; add intake/outfall + TCES | Mermaid |
| `layout/flow_arrows.mmd` + `.png` | Re-route heat-rejection → sea; add TCES charge/discharge arrows | Mermaid |
| `cad/build_aegis40_cad.py` → `cad/aegis40_site.step` | Remove CTW solid; TES building = TCES envelope; rebuild STEP | build123d venv `~/.venvs/cad` |
| `site/index.html` | Drop CTW; TES = TCES; add seawater structures | native SVG |

---

## DONE CRITERIA
- [ ] TCES working pair locked (Step 0) with rationale + `[ALISHER]` sizing flags.
- [ ] Zero "Therminol" / "two-tank" / "cooling tower" / "CTW" references remain except as struck-through decision history (`grep -riE "therminol|two-tank|cooling tower|CTW" --include=*.md --include=*.yaml --include=*.mmd` clean).
- [ ] FER §8.9/§8.10 + PFD tell the same TCES + seawater story.
- [ ] Safety: Req 35 still bounded; load-following transients checked vs `safety_criteria.yaml`; TCES hazards in register; safety-UHS-≠-normal-sink distinction preserved.
- [ ] One-shot graphical recut complete; PNGs re-rendered; STEP rebuilt.
- [ ] README + `fer_8810_docx_audit.md` mark C3 resolved.

## OPEN DEPENDENCIES
- `[ALISHER]` — TCES bed mass, footprint, charge/discharge power, round-trip η, district-heat dispatch profile.
- `peaking_recompute` (Samira, due now) — gates whether load-following transient checks pass; do not certify load-follow until F_q/F_ΔH resolved.
- `[VERIFY-SKKY]` — seawater thermal-discharge limit (from the seawater audit).
- C5 (containment dry vs submerged pool) — still open; keep PFD/CAD containment concept-neutral if unresolved at recut time.

---
*End of self-prompt. Companion: `planning/seawater_cooling_safety_fom_audit_2026-06-19.md` (C2 side of the same recut).*
