# FER Readiness Review — Chapter 8 (§8.5–§8.7) + cross-cutting

*Independent review in the role of a senior nuclear engineer (10+ yr, PWR safety
analysis / I&C licensing). Scope: only the sections this team's System-integration
work feeds (§8.5, §8.6, §8.7; §8.8/§8.10 covered separately by
`layout/fer_8810_docx_audit.md`). Review date 2026-06-13. Companion deliverable:
`docs/FER_Aegis40_8.5-8.7_draft.md` — the drafted text itself.*

---

## Overall verdict

The underlying engineering is **unusually traceable for a student design** — a
machine-readable criteria file, every trip tied to a criterion, every event-tree top
event tied to a trip, and the neutronics cross-checked against the locked core
revision. That spine is FER-ready. The exposure is concentrated in three places:
**(1) thermal-hydraulic hard constraints are still unquantified** (MDNBR, PCT — the
two numbers any reviewer checks first on a PWR), **(2) the accident spectrum has only
two analyzed initiators**, and **(3) several headline claims (72 h vs >100 h grace,
containment concept) are not yet internally consistent**. None of these block
drafting; all of them block *submission*.

---

## §8.5 Safety criteria — verdict: **draft-ready, two holes flagged**

**Strengths**
- 27 criteria with regulatory pedigree per row (10 CFR 50.46, GDC-11, SRP 4.2–4.4,
  SSR-2/1, ASME III). The hard/operating/target taxonomy with "hard = pass/fail,
  never scored" is exactly how a design-certification reviewer thinks.
- Six of ten neutronic gates moved from asserted to **demonstrated** values (rev_3):
  SDM 12.4 %, MTC −35.9 pcm/K, DTC −1.84 pcm/K, void −214 pcm/%void, ARO worth
  15 226 pcm, insertion rate 1.5e-5 Δk/k/s. This is the strongest table in the chapter.

**Gaps (must close before submission)**
- **G1 — MDNBR ≥ 1.3 and PCT ≤ 1204 °C have no demonstrated values.** Hard
  constraints without numbers read as unverified design. Blocked on the OpenFOAM
  hot-channel run; the draft carries `[SIM-PENDING]` markers. *This is the single
  biggest hole in the chapter.*
- **G2 — Boundary dose ≤ 0.25 Sv and EPZ ≤ 0.5 km are asserted, not shown.** The
  source term exists (1.2e17 Bq discharge inventory, rev_3) but no dispersion
  calculation connects it to the dose criterion. A judge will ask "show me."
- **G3 — Enrichment margin.** 4.95 wt% against the 5.0 LEU ceiling leaves 0.05 wt%.
  Defensible (deliberate, burnup-driven) but the FER must state the fabrication
  tolerance argument explicitly (±0.05 wt% enrichment tolerance consumes the entire
  margin — needs a manufacturing-spec statement). Drafted with a `[VERIFY]`.
- Hygiene: the YAML and its MD render drifted once already (enrichment decision
  table; fixed 2026-06-13). Re-render before each submission freeze.

---

## §8.6 Accident analysis — verdict: **strong skeleton, thin spectrum**

**Strengths**
- The **eliminated-events strategy** is the design's best licensing story and is now
  fully claimable: LB-LOCA (integral RPV, no large-bore primary piping), **rod
  ejection (internal CRDMs, confirmed 2026-06-12)**, boron-dilution events (SBF
  core), surge-line break (integral pressurizer). Few competitor designs will argue
  event *elimination* rather than event *mitigation*.
- Two quantified event trees with the right discipline (top events ← trip table ←
  criteria): LOHS at ~1e-8/ry and SBO at ~1e-11/ry, both with explicit
  redundancy/necessity tables. The SBO de-energize-to-actuate argument is the
  signature passive-safety claim and is well substantiated.

**Gaps**
- **G4 — Initiator spectrum.** Two trees ≠ a Chapter 15 analog. Minimum credible set
  for the FER: add **SB-LOCA** (the only LOCA left after LB elimination), **MSLB /
  excess steam demand** (MTC −35.9 pcm/K makes overcooling the *limiting* reactivity
  transient for this core — more limiting than rod withdrawal), and **uncontrolled
  rod withdrawal** (the surviving reactivity AOO). The draft includes a screening
  table with these marked `[ANALYSIS-PENDING]` so the omission is explicit rather
  than silent.
- **G5 — All frequencies are placeholders** (`[PRA-PENDING]`). Acceptable at this
  stage if declared; the draft declares it.
- **G6 — ATWS basis.** With SBF, ATWS mitigation leans entirely on DAS + rod
  diversity; a 10 CFR 50.62-style statement is drafted but the stuck-rod CCF number
  is `[VERIFY]`.
- **G7 — 7.75 MW decay heat** (6.2 % of 125 MWth at t=0) is cited from rev_3 and
  cross-validated against ANS-5.1 — good — but PRHR sizing against it (≥105 %
  criterion) remains an assertion until the T-H run lands.

---

## §8.7 I&C — verdict: **most mature section; close four documentation gaps**

**Strengths**
- Architecture is genuinely licensing-shaped: 4-division 2/4 voting, de-energize-to-
  trip, qualified one-way isolation + data diode, DAS on a diverse platform per
  BTP 7-19, hardwired manual actions per IEEE 603 §5.8, IEC 60880 Cat A software,
  EQ/seismic per IEEE 323/344. The five-layer DiD mapping with "no software path
  from non-safety into Class 1E" is the correct headline.
- The digital-twin layer is a real originality lever and is correctly fenced
  (advisory-only, Category C, diode-isolated).

**Gaps**
- **G8 — Setpoint methodology.** Trip setpoints are listed (118 % flux, 16.5 MPa,
  etc.) but no uncertainty/setpoint calculation method (ISA-67.04 / RG 1.105) is
  referenced. One paragraph fixes it; drafted with `[TBD]` values for total channel
  uncertainty.
- **G9 — Per-channel response time + accuracy table.** The ≤500 ms sensor-to-breaker
  claim exists; the per-channel breakdown does not. Flagged.
- **G10 — FMEA.** Single-failure compliance is argued by architecture; a tabulated
  FMEA (even abbreviated, top 10 failure modes) would close the loop. Flagged.
- **G11 — DAS sufficiency argument.** DAS monitors only flux + pressurizer pressure;
  fine for trip backup, but the FER should state why two variables bound the CCF
  scenarios it covers (drafted, marked for review).

---

## Cross-cutting consistency items (will be caught by a careful judge)

| # | Item | State |
|---|---|---|
| X1 | **72 h vs ">100 h" grace** — criteria say ≥72 h; FER §8.8/§8.10 draft says >100 h | Pick one. Recommendation: claim **72 h** (defensible) and present >100 h as best-estimate upside `[ANALYSIS-PENDING]` |
| X2 | **Containment concept (C5)** — dry Ø15 m + IRWST (all our §8.5/8.6 work) vs pool-type (docx §8.10.4) | Explicitly held open by team. §8.6 draft is written against the **dry** concept with a `[DECISION-PENDING C5]` banner — if pool-type wins, §8.6 containment text + PCC description must be rewritten |
| X3 | **Heat sink** — resolved 2026-06-13 (Black Sea once-through) | PFD still shows CT-1 → **redraw before any FER figure is cut from it**; condenser back-pressure 7 kPa may improve with 15–20 °C seawater — η claim can only get better, no FER risk |
| X4 | TES technology (C3) — under deliberation | §8.9 cannot be finalized until decided; not our section, but §8.10 figures wait on it |
| X5 | "Sinop optimal site [Kurt 2014]" | `[VERIFY citation]` — confirm the actual reference exists and says this |
| X6 | CRDM=internal is currently word-of-mouth | Get one line + sketch into the mechanical design basis so the §8.6 elimination claim has a citable anchor |

---

## What I did NOT review

§8.1–8.4 (core, T-H, mechanical — other scopes), §8.9 (Alisher), §8.11 (waste),
the FOM chapter, and the §8.8/§8.10 draft text itself (already audited separately).

*Bottom line: draft §8.5–8.7 now (done — see companion file), close G1/G2 the moment
OpenFOAM and a dispersion estimate land, add the three screening-level initiators to
§8.6, and resolve X1/X2 before the figures are cut. The traceability spine means
closure is mostly filling declared holes, not restructuring.*
