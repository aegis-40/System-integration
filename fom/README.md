# fom/ — Weighted Figure of Merit (wFOM)

Focused, runnable implementation of `planning/PLAN.md` §5. Defines the wFOM, scores
Aegis-40 against CAREM-25 / SMART / NuScale VOYGR, and self-validates.

```
python3 fom/wfom.py        # runs everything, writes outputs/wfom_report.md
```

Files: `parameters_schema.yaml` (categories, normalizers, **default weights**),
`economic_assumptions.yaml` (prices), `reactors/*.yaml` (data, with status/source flags),
`wfom.py` (engine), `outputs/wfom_report.md` (generated).

---

## 1. Definition

$$\text{wFOM}(D,R)=\sum_{c}W_c\sum_{i\in c}w_{c,i}\,N_i(x_i^D,x_i^R),\qquad \sum_c W_c=\sum_i w_{c,i}=1$$

5 categories (Safety 0.35, Economic 0.20, Safeguards 0.15, Sustainability 0.15,
Efficiency 0.15). Three normalizers, each a **difference of a per-reactor term** `u_i`:

| Normalizer | `N_i(x^D,x^R)` | `u_i(x)` | Used for |
|---|---|---|---|
| log-ratio | `d·ln(x^D/x^R)` | `d·ln x` | monotone continuous (burnup, revenue…) |
| min-max | `n(x^D)−n(x^R)` | `n(x)∈[0,1]` | ordinal/bounded (SBF, EPZ, diversity) |
| target-Gaussian | `g(x^D)−g(x^R)` | `e^{−α(x−t)²}` | sweet-spot/limits (PCT, MDNBR, peaking, MTC) |

`wFOM>0` ⇒ Aegis-40 better on the weighted aggregate. Hard floors/ceilings (MDNBR≥1.3,
PCT≤1204, peaking≤2.5, MTC<0) are a **pass/fail gate** — violation ⇒ DESIGN_FAILED, not a
tradeable score.

## 2. Key structural property — it's an absolute utility

Since every `N_i = u_i(x^D) − u_i(x^R)`,

$$\text{wFOM}(D,R)=U(D)-U(R),\quad U(X)=\sum_c W_c\sum_i w_{c,i}\,u_i(x^X).$$

So the pairwise score is just the difference of an **absolute utility per reactor** ⇒ the
FOM is exactly **antisymmetric** and **transitive (path-independent)**, and all reactors
can be put on **one ranking scale**. The engine exploits this (report §3) and tests it
(§4). *Caveat:* `U(D)−U(R)` equals the pairwise wFOM only when both are computed on the
**same parameter set** — see §4 below.

## 3. Results (de-peaked Aegis-40, IAEA-booklet data, 2026-06-15)

- **Relative ranking (vs each other):** **NuScale > Aegis-40 > CAREM-25 > SMART.** Aegis-40
  is a robust #2 — same order under wFOM, TOPSIS, and AHP weights; leave-one-category-out
  keeps it #2 (it goes #1 only if Safety is dropped). NuScale leads on Safety (fully passive,
  SSE 0.5 g, 720 h grace) + 12-module footprint economy; Aegis-40 leads on cogen revenue,
  SBF, and efficiency.
- **Absolute scoring vs international-standard targets (§3b):** only **NuScale beats the
  benchmark (+0.23)**; Aegis-40 **−0.18**, SMART −0.46, CAREM −0.48. So against fixed
  targets (not competitors), Aegis-40 is *below* an ideal design — useful gap-finder.
- **Safety is no longer one estimate.** Added booklet-sourced `seismic_sse` and
  `primary_circulation`; `n_active_components` global weight fell 0.35 → 0.11. Safety now
  spreads across grace/SSE/circulation/n_active.
- **AHP weights** (`ahp/category_pairwise.yaml`): CR = 0.002 (<0.10), weights ≈ defaults,
  ranking unchanged.
- An earlier run had Aegis-40 #1; that was a **bad-estimate artifact** (SMART/NuScale
  figures), corrected against the booklet — better data flipped it. Audit data before FER use.
- **As-run Aegis-40 fails the hard gate** (peaking 3.478 > 2.50) — comparison uses the
  post-de-peak target 2.30 (`open_item: peaking_recompute`).

## 4. Validation — how we check it "works"

**Implemented in `wfom.py` (report §4–6):**
1. **Identity** `wFOM(R,R)=0`. ✅
2. **Antisymmetry** `wFOM(A,B)=−wFOM(B,A)`. ✅
3. **Transitivity** `U(A)−U(C)=(A−B)+(B−C)` on a fixed set. ✅
4. **Monotonicity** improving a max-direction param strictly raises wFOM. ✅
5. **Independent method (TOPSIS)** — same data/weights, distance-to-ideal aggregation;
   ranking agrees. ✅
6. **Weight robustness** — leave-one-category-out; Aegis-40 stays #1. ✅

**Why pairwise (§2) and absolute (§3) can disagree (the NuScale case):** the 4-way common
set excludes `grace_period` (SMART's value is unpublished), so the absolute ranking never
sees the metric where NuScale crushes Aegis-40, while the Aegis-vs-NuScale pairwise does.
Both are internally consistent; they answer different questions. **Fix:** fill the data
gaps, or compute absolute U pairwise-consistently.

**Other ways to check (recommended, not yet built):**
- **AHP weight elicitation + CR<0.10** (PLAN §6) — replace the seed weights with a
  consistent expert matrix; report the consistency ratio.
- **Monte-Carlo weight sensitivity** — sample AHP entries, report wFOM 5/50/95-percentile
  ranges so results are bands, not points (PLAN §7.1).
- **Parameter-uncertainty propagation** — sims have error bars; sample ±10 % (±5 % for
  sim-derived) and propagate (PLAN §7.2).
- **Neutral-weight check** — re-run with equal category weights; if Aegis-40 still wins,
  the result isn't an artifact of self-serving weighting (see caveat below).
- **Normalizer-swap** — swap log-ratio↔min-max where both are defensible; check ranking
  stability.
- **Face validity vs reality** — does the ranking match independent reality? NuScale
  (design-certified, most mature) ranking high and our SBF/passive ranking high is a
  sensible sanity check; a wildly counter-intuitive order would flag a bug.
- **Reference-independence** — `wFOM(A,B)−wFOM(A,C)` should track `U(C)−U(B)` once data
  coverage is equal.

## 5. Honesty caveats (must accompany any FER use)

- **Reference data are mostly literature/estimate** (status flags in the YAMLs) — verify
  CAREM/SMART/NuScale figures against the IAEA SMR booklet before publishing.
- **Safety cross-comparison still excludes the sim-only fuel-integrity metrics**
  (PCT/MDNBR/peaking/MTC unpublished for competitors). Mitigated 2026-06-15 by adding
  booklet-sourced `seismic_sse` + `primary_circulation` so Safety no longer rides on the
  single estimated `n_active_components`; the absolute-standards view (§3b) does exercise
  the sim-only metrics for Aegis-40.
- **The metric encodes Aegis-40's own philosophy** (rewards SBF, passive, cogen). Aegis-40
  ranking #1 is partly by construction. Robustness checks (TOPSIS, leave-one-out) mitigate
  but do not remove this — disclose it, and run the neutral-weight check.
- **Weights + prices are defaults pending supervisor** (PLAN §1.2 q1–q2).
