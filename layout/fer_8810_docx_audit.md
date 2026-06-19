# Audit — `docs/FER_Aegis40_8.8-8.10.docx` vs repo design basis

*Run by Azamhon, 2026-06-13. The FER draft (§8.8 aux systems, §8.9 stub, §8.10 layout)
is an **evolved design basis**: it resolves two long-standing opens but contradicts
several locked repo decisions and the team's own PFD. Reconcile before submission —
a judge cross-reading FER sections will catch every one of these.*

**Verdict: 2 resolutions to harvest · 7 conflicts to reconcile · 2 internal
contradictions inside the docx itself.**

> **Update 2026-06-19:** C2 (seawater) and C3 (TCES) are now both team-resolved. Repo text/data reconciled this session (zones, building_list, critical_piping, aux_systems, safety_criteria, fom). The **one-shot graphical recut is unblocked** — Mermaid/SVG/CAD/viewer updated; the **PFD (`docs/aegis40_pfd.drawio.png`) is the one remaining manual redraw** (binary PNG, no source file): drop CT-1 + the two-tank Therminol, add seawater intake/outfall + the TCES bed. C1 (two vs three islands) and C5 (containment concept) remain open.

---

## 1. New decisions the docx makes — harvest into the repo ✅

| # | Docx says | Repo status before | Action |
|---|---|---|---|
| H1 | **Site = Sinop, Turkish Black Sea coast** (multi-criteria optimal, [Kurt 2014]); seawater intake/discharge; coastal-hazard + biofouling design | Open item #6 "site type (inland/coastal)?" — supervisor pending | **RESOLVED — coastal/Sinop.** Update README open items + zones.md. Cascades to H2/C2. |
| H2 | **Critical-piping table with sizes** (§8.10.6): MSL 2×DN250 ~315 °C/5.8 MPa · FWL 2×DN200 ~220 °C/6.5 MPa · DHRS 2×DN100 Cl.1 · ECCS 2×DN80 Cl.1 · TES + SOE branches · **surge line eliminated** (internal to RPV) | R6 blocked "pending Adilbek NPS"; routes drawn `[ASSUMED]` | **R6 UNBLOCKED.** Captured in `layout/critical_piping_table.md`. Line weights on `site_plot_plan` can now be real. Confirm with Adilbek that these DNs are his (or get him to bless them). |

Also new and useful: seismic gap ≥ 75 mm Cat I ↔ Cat II; ≥ 20 m turbine-missile
separation; below-grade steam/FW **tunnel** (vs our surface rack `[ASSUMED]`);
MSIV within 1.5 m of penetration; 2× OTSG (helical-coil) stated explicitly.

---

## 2. Conflicts — docx vs locked repo decisions ⚠️

| # | Topic | Docx (§) | Repo (locked) | Who should win / action |
|---|---|---|---|---|
| C1 | **Island scheme** | **Two islands**: NI + combined "Energy/Conventional Island" (turbine + TES + SOE on one steam corridor) (§8.10.2) | **Three islands** (README #7, zones.md Z1, all drawings/viewer/CAD) | Real design choice, not drift. Docx logic is strong (one steam corridor, fewer penetrations) and *compatible* with r2 (TB adjacent to NI). But it dissolves the II-as-separate-island story incl. the 100 m H₂ stand-off framing. **Team decision needed** — if E-CI wins, zones.md/viewer/CAD/drawings all re-cut. |
| C2 | **Heat sink** — ✅ **RESOLVED 2026-06-13 (team): Black Sea once-through, no cooling tower** | Condenser circ-water → **Black Sea once-through** (§8.10.2); CCWS → seawater (§8.8.9) | ~~CTW `[ASSUMED]` (Z6)~~ → Z6 updated. **PFD still shows CT-1 + CWP — must be redrawn** (drop CT-1, add seawater intake/discharge + CWP). Layout/viewer/CAD recut deferred to the post-C3 one-shot. | Docx wins. Rationale: 82 MWth rejection is small → negligible thermal-plume impact; better cycle η; CTW footprint freed. |
| C3 | **TES technology** — ✅ **RESOLVED 2026-06-13 (team): Thermochemical Energy Storage (TCES), zeolite-13X** | **Thermochemical** zeolite-13X sorption, ~390 t, charge ~280 °C/15 bar pass-out steam (§8.10.3, §8.10.2) | ~~Two-tank sensible Therminol-66 (TK-C/TK-H, IHX E-2, boiler E-3)~~ → **superseded** | **FER text/data reconciled 2026-06-19** (zones Z8, building_list, critical_piping Row 3, aux_systems §9a). **PFD must drop the two-tank Therminol and show the TCES bed** — part of the now-unblocked one-shot recut (C2+C3 both settled). |
| C4 | **SFP boration** | "**borated-water pool**" (SFPB bullet, §8.10.3); "below-grade **borated**-water pool" for RPV (§8.10.4) | **Unborated** SFP, burnup credit + rack geometry, k_eff(95/95) ≤ 0.95 (`aux_systems.md` §7, M3 fix; SBF story) | Repo wins — boration contradicts the SBF originality claim **and the docx's own §8.8.10** ("not dissolved boron"). Strip "borated" from §8.10.3/8.10.4. |
| C5 | **Containment concept** — ⏸ **explicitly held OPEN (team, 2026-06-13)** | RPV submerged in a **steel-lined water pool** as UHS, NuScale-style; "pool as ultimate heat sink for **>100 h**" (§8.10.4) | **Dry steel-lined containment Ø15 m + IRWST annulus** (viewer, CAD, rxb drawings); 72 h grace (`operator_grace_period`) | Architecture-level divergence: pool-type vs dry changes containment pressure analysis, IRWST role, RXB sections, CAD diorama. FER text must stay concept-neutral or carry a `[DECISION-PENDING]` marker until closed. |
| C6 | **Grace period** | "> 100 h passive cooling" (§8.10.4, §8.8.3 cites §8.5) | `safety_criteria.yaml` `operator_grace_period` = **72 h** | Don't claim two numbers. Either re-baseline the criterion to 100 h **with analysis** (OpenFOAM transient pending!) or pull the docx back to 72 h. Currently 100 h is unsubstantiated. |
| C7 | **Elevations** | RPV-pool level **El. −12.0 m** (§8.10.4) | Pit −15.5/−16 m, RPV head ≈ −5 m (zones.md, CAD, elevation drawing) | Minor but visible in drawings. Pick one datum set; propagate to GA-003/004 + CAD. |

Lesser deltas: building set/names — docx has RB/SFPB/**ARB** (aux+radwaste merged)/**ECB**
(electrical+control merged)/TGB/TESB/SOEU, **no DGB, no WSB, no CTW**; repo has 13
buildings incl. DGB+WMB+CB separate. Cycle "18-month" (§8.8.10) vs rev_3 **479 EFPD**
(~17.5 cal-months @ 0.90 CF — defensible as "≈18-month", say it that way). RPV
"dimensionally referenced to NuScale VOYGR" — fine as reference, but rev_3 geometry
(Ø2.44 m) is the binding number. "two helical-coil OTSGs" vs PFD's single OTSG block —
PFD should show 2×50 % if that's real.

---

## 3. Internal contradictions *inside* the docx 🐞

| # | Where | Contradiction |
|---|---|---|
| I1 | §8.10.3/§8.10.4 vs §8.8.10 | "Borated-water pool" vs "criticality safety relies on fixed geometry and absorber rack materials, **not dissolved boron**" — same document, both can't hold. |
| I2 | §8.10.2 (sea-cooled condenser) vs team PFD CT-1 | FER figures will be generated from the PFD; if §8.10 text says "condenser end toward the sea" while Figure 8.9-x shows a mech-draft tower, judges will flag it. |

---

## 4. Good alignment — no action

- §8.8 aux systems structure matches `layout/aux_systems.md` 8-system set (HVAC, air,
  power, sampling, rad monitoring, comms, lighting, lifting, cooling/demin/drain, fuel
  handling, fire, RP) with SSG-62 anchoring — stronger citations than repo version.
- Reduced CVCS / SBF originality story consistent (§8.8.9 ↔ aux_systems §1).
- Fail-safe positions (CIV closed, passive-DHR open) match `trip_signals.md`.
- "SBO contribution to CDF negligible because passive functions need no AC" (§8.8.3) —
  **now demonstrated** by `safety/event_tree_SBO.md` (this session).
- §8.10.5 declares the CAD model the spatial SSOT under Git — `cad/` now provides it;
  drawing list AE-40-GA-001…006 maps onto our existing drawings + two gaps
  (below-grade plan GA-003 as standalone, steam-distribution GA-005).
- 4-batch / ~5–6 assemblies per outage consistent with rev_3 21-FA core.

---

## 5. Recommended sync order

1. **C2 + C3 first** (heat sink, TES tech) — they decide the PFD, §8.9, and half of
   §8.10; team call with Alisher + supervisor.
2. **C1** (two vs three islands) — after C2 (no CTW → CI shrinks → E-CI merge gets easy).
3. **C5 + C7** (pool vs dry containment + datum) — gates all RXB drawings/CAD rework.
4. **C4, C6, I1** — text-level fixes, 30 min once decided.
5. Re-cut viewer/CAD/drawings once, after 1–3 settle. Don't chase each decision with
   a separate redraw.

*Sources: `/tmp` text extraction of the docx; repo cross-refs as cited per row.*
