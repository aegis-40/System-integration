# Aegis-40 Benchmarking System — Meeting Brief

**Project:** TEKNOFEST 2026 Nuclear Energy Technologies Design Competition — Aegis-40 (40 MWe iPWR, Detail Design category).
**Purpose of this brief:** 15-minute review of design decisions for the automated benchmarking system before implementation begins.
**Companion files:** `PLAN.md` (full implementation spec), `SIMULATION_REQUIREMENTS.md` (interface for the OpenMC/OpenFOAM teams).

---

## 1. What we're building (2 min)

A Python tool that automatically scores Aegis-40 against three reference iPWRs (CAREM-25, SMART, NuScale VOYGR) and produces a defensible comparison sheet for the FER. Replaces hand-typed PER tables and ad-hoc spreadsheet math.

Workflow each design iteration:
1. Edit one design parameter (or run OpenMC/OpenFOAM — outputs auto-ingested).
2. Run `make all`.
3. Get fresh benchmark table, wFOM scores, sensitivity ranges, and FER-ready report.

Time per iteration: <2 minutes. Currently: ~2 hours by hand.

---

## 2. The journey of decisions (5 min)

### 2.1 The PER's wFOM was too narrow
PER §5.1 weights: grace 0.40 + passivity 0.30 + PCT margin 0.15 + volume 0.10 + diversity 0.05.
**85 % of weight is safety.** Zero weight on economics, sustainability, safeguards, or efficiency. Judges will ask about them.

### 2.2 Decision: 5 categories × hierarchical wFOM
Restructured into Safety / Economic / Safeguards / Sustainability / Efficiency. Each category has 2–4 sub-parameters. Two-level AHP (5 × 5 across categories + smaller matrices within each). Mathematically identical to the PER formula when one category has weight 1.0 — strict generalization, not a rewrite.

**Default category weights:** Safety 0.35, Economic 0.20, Safeguards 0.15, Sustainability 0.15, Efficiency 0.15.

### 2.3 Decision: hybrid normalization (3 tools, dispatched per parameter)
Single-formula log-ratio fails for binary/bounded/target-centered parameters (SBF flag, k_eff, MDNBR). Single-formula min-max changes everyone's score every time a new reactor is added.

| Tool | Formula | Used for |
|---|---|---|
| Log-ratio | `ln(x_design / x_ref)` | Monotone continuous: grace period, burnup, cycle length, footprint |
| Min-max | `(x − x_min) / (x_max − x_min)` | Bounded/ordinal: SBF complexity score, EPZ class, diversity count |
| Target-Gaussian | `exp(−α (x − x*)²)` | Sweet-spot/safety: k_eff, MTC, MDNBR, PCT, peaking factor |

Each parameter declares its normalizer in the schema. Code dispatches automatically.

### 2.4 Decision: hard constraints are pass/fail, not scored
If MDNBR < 1.3 or PCT > 1204 °C, wFOM = `−∞` and the report flags `DESIGN_FAILED`. Safety limits aren't tradeable — fix the design, not the formula. Matches IAEA SSR-2/1 expectations.

### 2.5 Decision: capital cost dropped, replaced with Specific Revenue
No defensible CAPEX number for Aegis-40 yet. Instead use:
`R = ($_electricity + $_heat_sold + $_H₂_sold) / kWe-year`
Aegis-40 baseline: ~$545/kWe-yr (40 MWe × $60/MWh + 15 MWth district heat + 120 t H₂/yr). Easy to defend, every input is one number you can change.

### 2.6 Decision: simulation outputs auto-ingested
OpenMC produces `derived.json` per run; OpenFOAM produces `derived.json` per run. The benchmark tool reads them and updates `aegis40.yaml` automatically. No manual transcription. Specified in `SIMULATION_REQUIREMENTS.md`.

---

## 3. The formula (1 min — show on screen)

$$
\text{wFOM}(D, R) = \sum_{c} W_c \cdot S_c, \qquad S_c = \sum_{i \in P_c} w_{c,i} \cdot \mathcal{N}_i(x_i^D, x_i^R)
$$

- `W_c` = category weights (sum to 1)
- `w_{c,i}` = sub-weights within category (sum to 1)
- `𝓝_i` = parameter-specific normalizer (one of three tools above)
- Result: 0 = tied with reference, positive = better, `−∞` = constraint violated.

---

## 4. Decisions needing supervisor sign-off (3 min)

| # | Item | Proposed default | What we need from you |
|---|---|---|---|
| 1 | Category weights | 35 / 20 / 15 / 15 / 15 | Approve, or shift toward economics if competition rubric demands |
| 2 | Electricity sale price `p_el` | $60 / MWh | Confirm or override |
| 3 | District heat sale price `p_th` | $50 / MWh | Confirm |
| 4 | Hydrogen sale price `p_H₂` | $5 / kg | Confirm |
| 5 | PCT Gaussian center / α | 600 °C / 5e-6, hard ceiling 1204 °C | Confirm |
| 6 | MDNBR Gaussian center / floor | target 2.0 / floor 1.3 | Confirm |
| 7 | k_eff Gaussian | target 1.000, α 1e5 | Confirm |
| 8 | SMART thermal power baseline | 365 MWth (IAEA), not 540 (PER table) | Sign off on correction |
| 9 | NuScale grace period cap | 720 h (30 d) for "unlimited" claim | Confirm methodology note |
| 10 | Closed list of "diversity principles" | gravity, natural circ., condensation, conduction, evaporation, capillary, pressure suppression | Approve list |

---

## 5. Timeline (2 min)

| Phase | Duration | Outcome |
|---|---|---|
| 1. Bootstrap | 30 min | Repo, deps, Makefile |
| 2. Data layer | 60 min | Schema, 4 reactor YAMLs, normalizers |
| 2.5. Sim ingestion | 60 min | OpenMC + OpenFOAM ingest pipelines |
| 3. Benchmark sheet | 30 min | CSV/MD/LaTeX comparison table |
| 4. AHP engine (2-level) | 60 min | Weights with consistency checks |
| 5. Hierarchical wFOM | 60 min | The core scoring engine |
| 6. Sensitivity | 45 min | Monte Carlo, tornado plots |
| 7. Report generator | 30 min | FER-ready Markdown |
| 8. Notebooks + README | 30 min | User-facing docs |
| 9. Polish | 30 min | Lint, types, coverage ≥80% |

**Total:** ~7 hours of automated execution. One uninterrupted afternoon.

---

## 6. Risks and mitigations (1 min)

| Risk | Mitigation |
|---|---|
| OpenMC/OpenFOAM team produces outputs in wrong format | `SIMULATION_REQUIREMENTS.md` is the contract; share it now |
| AHP pairwise matrices fail consistency (CR > 0.10) | Code rejects them; team must redo elicitation. Better than ignoring |
| Aegis-40 TBD parameters delay scoring | Pipeline reports gaps in FER; partial wFOM still defensible |
| Supervisor disagrees with category weights | One YAML edit, re-run; no code change needed |

---

## 7. Asks from this meeting (1 min)

1. Sign off on the 10 items in §4.
2. Approve `SIMULATION_REQUIREMENTS.md` distribution to the OpenMC/OpenFOAM teammates so their first runs produce ingest-compatible outputs.
3. Greenlight Sonnet execution of the 9-phase plan.

---

## 8. Backup slides — questions you may get

**"Why not just use the PER formula as-is?"**
PER §5.1 itself flags weights as "preliminary engineering judgment" and promises "Final weighting will be determined through formal AHP pairwise comparison." We're delivering on that.

**"Is the log-ratio defensible vs simple linear scoring?"**
Log-ratio is symmetric (2× better = 2× worse), scale-invariant, dimensionless, and matches the PER's published formula. It's the standard approach in Saaty-style multi-criteria analysis when ratios make physical sense.

**"What if a competing team uses a different formula?"**
Our wFOM produces signed scores against named references (CAREM-25, etc.) — every number is auditable to a specific IAEA page. Other teams can re-derive ours; we cannot re-derive theirs. Reproducibility is our moat.

**"How do you handle uncertainty?"**
Every parameter carries its own uncertainty (Monte Carlo from OpenMC, residual-based from OpenFOAM). The sensitivity module propagates ±10 % parameter perturbation into wFOM 5–95 percentile bands. Reported FOM is a range, not a point.

End of brief.
