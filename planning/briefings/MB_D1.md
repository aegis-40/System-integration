# Meeting Brief — Day 1 (3S Safety / I&C / FOM)

**Date:** 2026-05-26 (Mon) — W1, Day 1
**Owner:** Azamhon
**Audience:** team standup / supervisor
**Duration:** 5–10 min spoken
**Companion files:** `W1_Plan.md`, `safety/safety_criteria.yaml`, `safety/safety_criteria.md`

---

## 1. Where I am in the week (30 s)

> "I'm the integration node — safety criteria, I&C, and the FOM rollup that ingests every team's numbers. This week has 6 deliverables. Today I finished the first one: the safety criteria table that anchors FER §8.5. Everything else this week builds on it."

**W1 deliverables (status):**
1. ✅ Safety criteria table (`safety_criteria.yaml` + `.md`) — **done today**
2. ⏳ I&C architecture + sensor inventory — Tue
3. ⏳ I&C block diagram — Wed
4. ⏳ Trip signals + LOHS event tree — Thu
5. ⏳ FOM update template — Fri
6. ⏳ Buffer + supervisor brief — Sat/Sun

---

## 2. What the safety table is (1 min)

> "It's the single source of truth for every safety claim we'll make in the FER. Twenty-seven numeric criteria across seven categories. Every row carries a regulatory citation, a sensor chain that observes it, a trip that protects it where applicable, and a FOM normalizer field that feeds the scoring engine."

**Why it's structured the way it is:**
- **One file → many uses.** Same YAML feeds (a) FER §8.5 narrative, (b) §8.6 fault tree initiators, (c) §8.7 I&C trip setpoints, (d) the FOM scoring engine in `PLAN.md`.
- **Hard / operating / target distinction.** Hard constraints (MDNBR, PCT, dose) make the design pass or fail — they break the FOM with `−∞` if violated. Operating limits (k_eff, SG pressure) cause trips. Targets (EPZ, grace period, CDF) contribute positively to scoring. This three-way split matches `MEETING_BRIEF.md` §2.4.
- **Defense in depth.** Every row tagged with IAEA SSR-2/1 Rev 1 DiD level 1–5. FER §8.6 explicitly asks for this.

---

## 3. What's in the seven categories (2 min)

> "Walk through the categories — call out the load-bearing rows."

1. **Reactivity & neutronic (7 rows)** — k_eff, SDM, MTC/DTC/void coefficients, ARO worth, max reactivity insertion rate.
   *Plug points for Samira's W1 results:* MTC sweep (task 3), void sweep (task 4), shutdown margin (task 14).

2. **Thermal-hydraulic (6 rows)** — MDNBR steady + AOO, PCT LOCA, clad oxidation, H₂ generation, fuel centerline T.
   *Plug points for OpenFOAM W1:* MDNBR steady-state + hot-channel PCT from task 4.

3. **Pressure boundary (3 rows)** — primary design 17.2 MPa, containment 0.414 MPa, SG operating 7.17 MPa.

4. **Decay heat & passive (3 rows)** — grace period ≥ 72 h (target unlimited), PRHR capacity ≥ 1.05× decay heat, SBF diversity ≥ 5 principles. **This is the iPWR competitive lever.**

5. **Radiological & site (4 rows)** — EPZ ≤ 0.5 km, site boundary dose ≤ 0.25 Sv, CDF < 1e-7, LRF < 1e-8.

6. **Seismic (1 row)** — SSE ≥ 0.3 g.

7. **Fuel cycle (3 rows)** — burnup ≤ 62 GWd/MTU, enrichment ≤ 5 %, cycle length ≥ 365 EFPD.

> "Total: 27 criteria. Hard constraints: 17. Operating limits: 4. Targets: 6."

---

## 4. Defense-in-depth map (1 min)

> "Five-level table at the bottom of the criteria doc. For each IAEA DiD level, lists the Aegis-40 features that work at that level. This is the structure judges expect from §8.6."

| Level | Objective | Aegis-40 features |
|---|---|---|
| 1 | Prevent abnormal op | Negative reactivity coefficients · MDNBR margin · HIGA self-regulating Gd₂O₃ |
| 2 | Detect + control failures | RPS 2/4 voting · AOO trip envelope |
| 3 | Design-basis accidents | Passive ECCS ×3 · PRHR/IRWST · Containment isolation ×3 |
| 4 | Severe accidents | ≥ 72 h grace · Passive containment cooling ×3 · ≥ 5 diverse SBF principles |
| 5 | Radiological mitigation | EPZ ≤ 0.5 km · Dose < 0.25 Sv · CDF < 1e-7 |

---

## 5. Two decisions made today (1 min)

> "Resolved two open items rather than waiting on supervisor."

1. **Cladding: Zircaloy-4** (not Zr-2 as in FER template).
   - Zr-4 is PWR-standard, Zr-2 is BWR. Matches Samira's OpenMC model. Confirmed FER template values are **illustrative format examples** only.

2. **Enrichment: 3-zone UO₂ at 2.6/3.0/3.4 wt% U-235.**
   - Matches Samira's stable model. FER's 3.81 % was illustrative, not prescribed.

> "Both decisions logged in `safety_criteria.yaml` under `decisions_locked`."

---

## 6. Two questions still open (1 min)

> "Two items I can't close today. Both have specific unblockers."

1. **PCT operating envelope (FOM Gaussian center)** — *blocked on OpenFOAM W1 hot-channel run (their task 4).* Once they give a steady-state PCT, I set the Gaussian center to ~that value or slightly below. Until then the row has a 600 °C placeholder per `MEETING_BRIEF.md` §4 row 5. **Cost of delay: zero — only affects normalizer constant, not safety claim.**

2. **Containment pressure-suppression yes/no** — affects SBF diversity count (target ≥ 5). Deferred until layout/Elbek confirms containment type details. **Cost of delay: ±1 on diversity count — Aegis-40 likely scores 4–5 either way.**

> "Neither blocks the rest of W1."

---

## 7. What I need from the team this week (1 min)

> "Five asks. All non-blocking for me today but feed the FOM template by Friday."

| Person | What | By | Why |
|---|---|---|---|
| Samira | DTC, MTC at full power, void coefficient, SDM estimate | Wed | Fills 4 rows + FOM inputs |
| Samira | When will full-cycle depletion run? | Mon | Sets burnup + cycle-length targets |
| OpenFOAM lead | First hot-channel MDNBR + PCT | Fri | Two hard constraints currently TBD |
| Alisher (TES/SOE) | MWe split, district heat MWth, H₂ kg/yr | Wed | FOM economic + sustainability rows |
| Elbek (layout) | Footprint, EPZ assumption | Fri | FOM layout row |
| Supervisor | 10 sign-offs from `MEETING_BRIEF.md` §4 | When you can | Final FOM weights — defaults work until then |

---

## 8. Reproducibility & FER fit (30 s)

> "Why this is FER-ready, not throwaway."

- Every row machine-readable in `safety_criteria.yaml` → goes into Digital Appendix (FER requires it).
- Every row has a regulatory citation → meets FER §8.5 ("national/international standards") and §8.1 ("list of reference regulatory documents").
- Defense-in-depth map → meets FER §8.6 IAEA SSR-2/1 expectation.
- Same file feeds the wFOM engine in `PLAN.md` → same numbers in safety chapter, FOM scoring, and final tables. No transcription errors.

---

## 9. Tomorrow (30 s)

> "Day 2 = I&C architecture. Sensor inventory table — 13 channels mapped to RPS/ESFAS/DCS/digital-twin layers. Trip mapping comes Thursday."

Day 3 = block diagram. Day 4 = trip signals + LOHS event tree. Day 5 = FOM template. Sat/Sun = buffer + supervisor brief.

---

## Speaker timing target

| Section | Time |
|---|---|
| 1. Where I am | 0:30 |
| 2. What the table is | 1:00 |
| 3. Seven categories | 2:00 |
| 4. DiD map | 1:00 |
| 5. Decisions made | 1:00 |
| 6. Open questions | 1:00 |
| 7. Asks of team | 1:00 |
| 8. FER fit | 0:30 |
| 9. Tomorrow | 0:30 |
| **Total** | **~8:30** |

Buffer for questions: 1:30.

---

## Backup slides — likely questions

**Q: "Why 27 rows, why not fewer?"**
A: Each row maps to either a 10 CFR / IAEA citation or an FER Table 1 row. Pruning means losing a citation. Hard-constraint count (14) matches IAEA SSR-2/1 hard limits set.

**Q: "Why YAML, not just a table?"**
A: Same data feeds three places — FER narrative, FOM engine, I&C trip linker. One file, three renderings. Avoids three copies drifting.

**Q: "What if a row's number is wrong?"**
A: Change one place. The `.md` regenerates, FOM re-scores, trip setpoints recompute. No find-and-replace across docs.

**Q: "What's the riskiest row?"**
A: `passive_decay_heat_removal_grace_h`. Aegis-40 selling point — but until we run a long-transient sim showing ≥ 72 h with no operator action, it's a claim, not a number. PRHR capacity row is the bound that proves it.

**Q: "How do you handle uncertainty?"**
A: Not in this file. Sensitivity module in `PLAN.md` propagates ±10 % parameter perturbations into wFOM 5–95 % bands. This file holds central values + regulatory limits.
