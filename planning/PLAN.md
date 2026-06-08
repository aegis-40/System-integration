# Aegis-40 Automated Benchmarking System — Implementation Plan (v2)

**Target executor:** Claude Sonnet (subsequent session).
**Target user:** Aegis-40 team (TEKNOFEST 2026 Nuclear Energy Technologies Design Competition, Detail Design — 40 MWe Modular PWR).
**Source documents:** `NUClearly_PER.pdf` (Preliminary Evaluation Report, Aegis-40), `SMR_booklet_2022-1-154.pdf` (IAEA Advances in Small Modular Reactor Technology Developments, 2022). Plus future OpenMC / OpenFOAM simulation outputs — see `SIMULATION_REQUIREMENTS.md`.
**Repo state:** Greenfield. No code yet.
**Plan owner:** This file. Update it as phases complete; do not delete.

**Revision history:**
- v1: Single-formula wFOM, 5 flat parameters from PER Table 1.
- **v2 (current):** Hierarchical wFOM across 5 categories (Safety, Economic, Safeguards, Sustainability, Efficiency); hybrid normalization (log-ratio + min-max + target-Gaussian); ingests OpenMC/OpenFOAM outputs; richer non-electric economics.

---

## 0. Goal

Build a reproducible, scriptable benchmarking pipeline that:

1. Stores baseline parameters of three reference iPWR designs (CAREM-25, SMART, NuScale VOYGR) and the Aegis-40 design in machine-readable YAML, organized into five engineering categories.
2. Renders a side-by-side benchmark sheet (Markdown + CSV + LaTeX) ready for PER/FER inclusion.
3. Implements a hierarchical Weighted Logarithmic Figure-of-Merit (`wFOM`) with hybrid normalization. Supervisor-approved formula, see §5.
4. Implements a two-level AHP (Analytical Hierarchy Process): (a) 5×5 over categories, (b) 3×3 (or larger) within each category, with Saaty consistency-ratio gates.
5. Ingests OpenMC and OpenFOAM simulation outputs and updates Aegis-40's design parameters automatically (file-watcher or explicit `benchmark ingest`).
6. Runs sensitivity / Monte-Carlo analysis over weights and parameter uncertainties so reported FOM values are reported as ranges, not point values.
7. Exposes a CLI: `benchmark run`, `benchmark wfom`, `benchmark ingest`, `benchmark sensitivity`, `benchmark report`, plus `benchmark add-design <yaml>` so any new candidate can be tested without code changes.

Success criterion: a fresh clone + `make all` regenerates every table, plot, and FOM number deterministically; a fresh OpenMC statepoint dropped in `inputs/openmc/` automatically updates Aegis-40's reactivity and burnup parameters on the next `make all`.

---

## 1. Open questions and resolved decisions

### 1.1 Resolved decisions (locked unless supervisor overrides)

| Decision | Default | Rationale |
|---|---|---|
| SMART thermal power baseline | **365 MWth** | IAEA Booklet 2022 (primary source) over PER Table 3 (likely typo) |
| CAREM-25 grace period baseline | **36 h** | IAEA Booklet PRHRS spec; conservative |
| NuScale grace period baseline | **720 h (cap)** | IAEA says "unlimited"; capped at 30 days for finite ratio. Document as methodology note in FER. |
| wFOM normalization | **Hybrid (3 normalizers, dispatch per parameter)** | log-ratio for monotone continuous, min-max for bounded/ordinal, target-Gaussian for safety limits. See §5. |
| wFOM hierarchy | **Two levels: 5 categories × 2–4 sub-parameters** | Avoids single-formula safety bias of PER v1; transparent for supervisor defense. |
| Category weights `W_c` | Safety 0.35, Economic 0.20, Safeguards 0.15, Sustainability 0.15, Efficiency 0.15 | Reflects nuclear's primary mission while covering competition criteria. Replaceable via AHP. |
| Soluble-boron-free representation | **Ordinal scale 0–3** | 0 = full boron, 1 = boron + rods, 2 = rods + Gd, 3 = full SBF. Min-max normalized. |
| Diversity principles | **Closed checklist** | {gravity, natural circulation, condensation, conduction, evaporation, capillary, pressure suppression}. Count from this list only. |
| Capital cost | **Dropped from Economic v1** | No defensible Aegis-40 number yet. Replaced by Specific Revenue ($/kWe-yr). Add back when LCOE model exists. |
| Non-electric apps metric | **Specific Revenue** | $(electricity + heat sold + H₂ sold) / kWe / year. Heat and H₂ priced from literature. |
| Hard safety constraints | **Pass/fail gate** | MDNBR < 1.3 or PCT > 1204°C → wFOM is `−inf` with explicit error. Safety limits are not tradeable. |

### 1.2 Still open (Sonnet should ask before locking)

1. **Are the category weights (35/20/15/15/15) acceptable, or does the supervisor want to shift?** E.g., 30/30/15/15/10 if economics are weighted heavier in TEKNOFEST scoring.
2. **Specific Revenue inputs** — agreed market prices for the FER baseline:
   - Electricity sale price `p_el` ($/MWh) — proposed default $60.
   - District-heat sale price `p_th` ($/MWh) — proposed default $50.
   - Hydrogen sale price `p_H₂` ($/kg) — proposed default $5.
   These are tunable parameters in `data/economic_assumptions.yaml`.
3. **PCT Gaussian center and α** — proposed: `target = 600°C` (typical PWR steady), `α = 5e-6` (so reaching 1000°C halves the score), with `hard_ceiling = 1204°C`. Confirm with supervisor.
4. **MDNBR Gaussian** — proposed: `target = 2.0`, `α = 4.0` (so MDNBR=1.5 scores ≈0.37), `hard_floor = 1.3`. Confirm.
5. **k_eff Gaussian** — proposed: `target = 1.000`, `α = 1e5` (so 1.005 scores ≈0.78), no hard limits (handled by safety analysis). Confirm.
6. **Aegis-40 TBDs** — RPV dims, footprint, primary pressure, fuel-assembly count, etc. PER doesn't fix them. Stored as `status: tbd`; pipeline reports gaps.

---

## 2. Repository layout

```
teknofest/
├── PLAN.md                          # this file
├── SIMULATION_REQUIREMENTS.md       # what OpenMC and OpenFOAM teams must produce
├── README.md                        # 1-page quickstart, generated last
├── pyproject.toml                   # uv/pip-installable package
├── Makefile                         # `make all`, `make benchmark`, `make wfom`, `make ingest`, `make clean`
├── .gitignore                       # standard Python + outputs/* + inputs/*/*.h5
├── .python-version                  # 3.12
│
├── data/
│   ├── reactors/
│   │   ├── carem25.yaml
│   │   ├── smart.yaml
│   │   ├── nuscale_voygr.yaml
│   │   └── aegis40.yaml
│   ├── ahp/
│   │   ├── category_pairwise.yaml      # 5×5 expert matrix (top-level)
│   │   ├── safety_pairwise.yaml        # within-category matrices
│   │   ├── economic_pairwise.yaml
│   │   ├── safeguards_pairwise.yaml
│   │   ├── sustainability_pairwise.yaml
│   │   ├── efficiency_pairwise.yaml
│   │   └── weights_resolved.yaml       # auto-generated
│   ├── parameters_schema.yaml          # canonical parameter definitions + normalizers
│   └── economic_assumptions.yaml       # market prices, discount rate
│
├── inputs/                            # ingested simulation outputs (gitignored)
│   ├── openmc/
│   │   ├── README.md                  # symlink → SIMULATION_REQUIREMENTS.md §OpenMC
│   │   └── <run-id>/                  # statepoint*.h5, summary.h5, depletion_results.h5
│   └── openfoam/
│       ├── README.md                  # symlink → SIMULATION_REQUIREMENTS.md §OpenFOAM
│       └── <run-id>/                  # postProcessing/, probes/, summary.json
│
├── src/
│   └── benchmark/
│       ├── __init__.py
│       ├── data_models.py           # pydantic v2: Reactor, Parameter, Category, AHPMatrix
│       ├── loader.py                # load + validate YAMLs, raise on schema drift
│       ├── normalizers.py           # log_ratio, min_max, target_gaussian — dispatched
│       ├── benchmark_sheet.py       # build comparative table → CSV/MD/LaTeX
│       ├── ahp.py                   # eigenvector method; CR<0.10 gate; hierarchical
│       ├── wfom.py                  # hierarchical formula; per-category breakdown
│       ├── sensitivity.py           # MC over weights + parameter ±10% uncertainty
│       ├── ingest_openmc.py         # parse statepoint.h5 → update aegis40.yaml
│       ├── ingest_openfoam.py       # parse postProcessing/ → update aegis40.yaml
│       ├── plots.py                 # radar, tornado, sensitivity, category breakdown
│       ├── reports.py               # Markdown report generator (Jinja2)
│       ├── templates/
│       │   └── report.md.j2
│       └── cli.py                   # typer-based CLI
│
├── tests/
│   ├── conftest.py
│   ├── test_loader.py
│   ├── test_normalizers.py          # all 3 normalizers, edge cases (zero, negative, target hit)
│   ├── test_ahp.py                  # Saaty 1980 known answer; CR rejection; hierarchical
│   ├── test_wfom.py                 # identity, monotonicity, sign flip, sum-to-score
│   ├── test_benchmark_sheet.py
│   ├── test_sensitivity.py
│   ├── test_ingest_openmc.py        # mock statepoint.h5 fixture
│   └── test_ingest_openfoam.py      # mock postProcessing/ fixture
│
├── notebooks/
│   ├── 01_baseline_comparison.ipynb
│   ├── 02_wfom_analysis.ipynb
│   ├── 03_sensitivity_studies.ipynb
│   └── 04_simulation_ingest_demo.ipynb
│
├── outputs/                         # gitignored except .gitkeep
│   ├── benchmark_table.csv
│   ├── benchmark_table.md
│   ├── benchmark_table.tex
│   ├── wfom_results.csv
│   ├── wfom_breakdown_<reference>.json     # one per reference reactor
│   ├── sensitivity_summary.csv
│   ├── aegis40_benchmark_report.md
│   └── plots/
│       ├── radar_aegis40_vs_refs.png
│       ├── wfom_tornado.png
│       ├── category_breakdown.png
│       └── sensitivity_distribution.png
│
└── docs/
    ├── methodology.md               # written by user, not by sonnet
    └── parameter_definitions.md     # auto-generated from data/parameters_schema.yaml
```

---

## 3. Parameter framework — 5 categories × N sub-parameters

Each parameter has these fields in `data/parameters_schema.yaml`:

```yaml
<param_key>:
  category:    safety | economic | safeguards | sustainability | efficiency
  unit:        SI unit string ("h", "MPa", "%", "ordinal", "—")
  description: human-readable
  normalizer:  log_ratio | min_max | target_gaussian
  direction:   max | min                  # only for log_ratio and min_max
  target:      <float>                    # only for target_gaussian
  alpha:       <float>                    # only for target_gaussian
  hard_floor:  <float | null>             # below this → design fails
  hard_ceiling: <float | null>            # above this → design fails
  source:      iaea | per | openmc | openfoam | literature | derived
```

### 3.1 Safety category (W = 0.35)

| key | unit | normalizer | direction / target | sub-weight | source |
|---|---|---|---|---|---|
| `grace_period` | h | log_ratio | max | 0.25 | iaea/per |
| `n_active_components` | count (use 1+N) | log_ratio | min | 0.15 | per/derived |
| `pct` | °C | target_gaussian | target=600, α=5e-6, ceiling=1204 | 0.20 | openfoam |
| `mdnbr` | — | target_gaussian | target=2.0, α=4.0, floor=1.3 | 0.20 | openfoam |
| `peaking_factor_3d` | — | target_gaussian | target=1.5, α=4.0, ceiling=2.5 | 0.10 | openmc |
| `mtc` | pcm/K | target_gaussian | target=−40, α=2e-3, ceiling=0 | 0.10 | openmc |

Note: `mtc` (moderator temperature coefficient) MUST be negative. `hard_ceiling=0` enforces it.

### 3.2 Economic category (W = 0.20)

| key | unit | normalizer | direction | sub-weight | source |
|---|---|---|---|---|---|
| `specific_revenue` | $/kWe-yr | log_ratio | max | 0.40 | derived |
| `footprint_per_mwe` | m²/MWe | log_ratio | min | 0.30 | iaea/per |
| `refuel_cycle` | months | log_ratio | max | 0.20 | iaea/per |
| `cycle_length_efpd` | days | log_ratio | max | 0.10 | openmc |

`specific_revenue` formula (computed in `loader.py` from constituent parameters):
```
R = [P_el · 8760 · CF · p_el + Q_th · h_th · p_th + m_H2 · p_H2] / P_nameplate
```
where prices come from `data/economic_assumptions.yaml`.

### 3.3 Safeguards / 3S category (W = 0.15)

| key | unit | normalizer | direction / scale | sub-weight | source |
|---|---|---|---|---|---|
| `sbf_score` | ordinal | min_max | max, scale=[0,1,2,3] | 0.40 | per/iaea |
| `epz_class` | ordinal | min_max | max, scale=[0,1,2] | 0.30 | per/iaea |
| `diversity_count` | count | min_max | max, scale=[0..7] | 0.30 | derived |

Scales:
- `sbf_score`: 0 = full soluble boron, 1 = boron + rods, 2 = rods + gadolinia, 3 = fully SBF.
- `epz_class`: 0 = site boundary EPZ, 1 = plant boundary EPZ, 2 = on-vessel EPZ.
- `diversity_count`: count from {gravity, natural circulation, condensation, conduction, evaporation, capillary, pressure suppression}.

### 3.4 Sustainability category (W = 0.15)

| key | unit | normalizer | direction / target | sub-weight | source |
|---|---|---|---|---|---|
| `non_electric_revenue_share` | fraction (0–1) | log_ratio | max | 0.40 | derived |
| `spent_fuel_per_mwh` | g/MWh | log_ratio | min | 0.30 | derived (from burnup) |
| `design_life` | years | log_ratio | max | 0.30 | iaea/per |

`non_electric_revenue_share = (heat_revenue + H2_revenue) / total_revenue`.
`spent_fuel_per_mwh = (1 / burnup) · 24` (MTU/MWh derivation).

### 3.5 Efficiency category (W = 0.15)

| key | unit | normalizer | direction | sub-weight | source |
|---|---|---|---|---|---|
| `thermal_efficiency` | fraction | log_ratio | max | 0.40 | derived (P_el / P_th) |
| `burnup` | GWd/MTU | log_ratio | max | 0.30 | iaea/openmc |
| `capacity_factor` | fraction | log_ratio | max | 0.20 | iaea/per |
| `linear_heat_rate` | kW/m | log_ratio | min | 0.10 | openmc |

---

## 4. Baseline data files

Each reactor YAML follows this structure:

```yaml
id: <slug>
display_name: <Name>
country: <Country>
developer: <Org>
status: <design_status>
source: <citation>

categories:
  safety:
    grace_period: { value: 36, status: confirmed, source: iaea, notes: "..." }
    n_active_components: { value: 4, status: estimate, source: derived }
    pct: { value: null, status: tbd, source: openfoam }
    mdnbr: { value: null, status: tbd, source: openfoam }
    peaking_factor_3d: { value: null, status: tbd, source: openmc }
    mtc: { value: null, status: tbd, source: openmc }
  economic:
    ...
  safeguards:
    ...
  sustainability:
    ...
  efficiency:
    ...

descriptive:
  thermal_power_mwth: 100
  electric_power_mwe: 30
  primary_pressure_mpa: 12.25
  ...
  # raw parameters used for the benchmark sheet (table) but not in wFOM
```

The four reactor YAMLs (CAREM-25, SMART, NuScale VOYGR, Aegis-40) are constructed from the data in PLAN v1 §4 plus the new categorization above.

**Derived parameter computations** (Sonnet must implement in `loader.py` post-validation):

```python
thermal_efficiency  = P_el / P_th
footprint_per_mwe   = plant_footprint / P_el
spent_fuel_per_mwh  = (P_th / P_el) * (1.0 / burnup_GWd_per_MTU) * 24.0   # g_HM/MWh_e
specific_revenue    = (P_el*8760*CF*p_el + Q_th_sold*h_th_sold*p_th + m_H2*p_H2) / P_el
non_electric_revenue_share = (Q_th_sold*h_th_sold*p_th + m_H2*p_H2) / total_revenue
```

For reactors with only electricity (CAREM-25 baseline, SMART desal-only baseline), `non_electric_revenue_share` may be small but nonzero (use desalinated-water value if present; otherwise 0.05 placeholder with a warning).

**Aegis-40 derived inputs from PER §4.1.3:**
- `Q_th_sold = 15` MWth, `h_th_sold = 8 × 200 = 1600` h/yr (winter heating season)
- `m_H2 = 120000` kg/yr
- `P_el = 40` MWe, `P_th = 125` MWth, `CF = 0.95`
- → `R_aegis40 ≈ ($20M + $1.2M + $0.6M) / 40000 kWe ≈ $545/kWe-yr`

---

## 5. wFOM mathematical specification

### 5.1 Top-level formula

$$
\text{wFOM}(D, R) = \sum_{c \in C} W_c \cdot S_c(D, R), \qquad
\sum_c W_c = 1
$$

where `D` is the design, `R` is the reference reactor, `C = {safety, economic, safeguards, sustainability, efficiency}`, `W_c` are the category weights (resolved by AHP, default §1.1), and:

$$
S_c(D, R) = \sum_{i \in P_c} w_{c,i} \cdot \mathcal{N}_i(x_i^D, x_i^R), \qquad
\sum_{i \in P_c} w_{c,i} = 1
$$

`P_c` is the parameter set in category `c`. `w_{c,i}` is the within-category sub-weight (resolved by AHP per category). `𝓝_i` is the parameter-specific normalizer.

### 5.2 The three normalizers

**Log-ratio** (monotone continuous, signed, unbounded):

$$
\mathcal{N}_i^{\text{log}}(x^D, x^R) = d_i \cdot \ln\!\left(\frac{x^D}{x^R}\right), \quad d_i \in \{+1, -1\}
$$

`d_i = +1` if `direction: max`, `d_i = −1` if `direction: min`. Result is `0` when tied, positive when design beats reference.

**Min-max** (bounded, ordinal, or fixed-scale):

$$
N^+(x) = \frac{x - x_{\min}}{x_{\max} - x_{\min}}, \quad N^-(x) = 1 - N^+(x)
$$

$$
\mathcal{N}_i^{\text{minmax}}(x^D, x^R) = N^{+/-}(x^D) - N^{+/-}(x^R)
$$

`N⁺` for `direction: max`, `N⁻` for `direction: min`. Subtraction makes the contribution signed. `x_min`, `x_max` come from the parameter scale defined in the schema.

**Target-Gaussian** (sweet-spot, regulatory limits):

$$
G_i(x) = \exp\!\left(-\alpha_i (x - x_i^*)^2\right) \in (0, 1]
$$

$$
\mathcal{N}_i^{\text{gauss}}(x^D, x^R) = G_i(x^D) - G_i(x^R)
$$

`x_i^*` is the target value, `α_i` controls the falloff.

### 5.3 Hard constraints

If any parameter has `hard_floor` or `hard_ceiling` and the design value violates it:

```
wFOM(D, R) = -inf
status     = "DESIGN_FAILED"
violations = [list of (param, value, limit_type, limit)]
```

Hard constraints are non-negotiable safety limits. `wfom.py` raises a `DesignFailedError` rather than returning a finite score; the report flags it prominently.

### 5.4 Identity property (unit test)

For any reactor `R`: `wFOM(R, R) = 0`, all `S_c(R, R) = 0`, all `𝓝_i(x, x) = 0`. This is non-negotiable; tests must assert it.

### 5.5 Output structure

```python
@dataclass
class ParamContribution:
    key: str
    category: str
    x_design: float
    x_reference: float
    normalizer: str
    raw_value: float          # output of N_i(x^D, x^R)
    sub_weight: float         # w_{c,i}
    contribution: float       # raw_value * sub_weight
    warnings: list[str]

@dataclass
class CategoryScore:
    category: str
    score: float              # S_c
    weight: float             # W_c
    contribution: float       # W_c * S_c
    parameters: list[ParamContribution]

@dataclass
class WFOMResult:
    design: str
    reference: str
    score: float              # total wFOM
    categories: list[CategoryScore]
    failed: bool
    violations: list[dict]
    warnings: list[str]
```

---

## 6. AHP specification (two-level)

### 6.1 Top-level (categories)

A 5×5 Saaty pairwise matrix in `data/ahp/category_pairwise.yaml`. Solve principal eigenvector → priority vector → `W_c`. Saaty CI/CR check with RI(5) = 1.12. Reject if `CR > 0.10`.

### 6.2 Within-category

One pairwise matrix per category in `data/ahp/<category>_pairwise.yaml`. Sizes: Safety 6×6, Economic 4×4, Safeguards 3×3, Sustainability 3×3, Efficiency 4×4. Same eigenvector + CR procedure. RI table: 3→0.58, 4→0.90, 5→1.12, 6→1.24, 7→1.32.

### 6.3 Seed matrices

Sonnet writes seed matrices that approximately reproduce the default weights in §1.1 and §3. Verify weights within ±0.03 of intended; tune until CR < 0.10 and weight target met.

### 6.4 Override flag

`benchmark wfom --use-default-weights` skips AHP and uses the §1.1 / §3 defaults directly. For sanity-checking AHP output.

---

## 7. Sensitivity analysis

Three studies, all driven by `sensitivity.py`:

### 7.1 Weight sensitivity (Monte Carlo over both AHP levels)
Sample each pairwise entry uniformly from `{a−1, a, a+1}` clamped to Saaty 1–9 scale, with reciprocal mirror. Reject samples that fail CR<0.10. N=10,000 valid samples. Report wFOM 5/50/95-percentile per (design, reference) pair.

### 7.2 Parameter uncertainty
Sample each `log_ratio` and `min_max` parameter from `Normal(value, 0.10·value)`. Sample each `target_gaussian` parameter from `Normal(value, 0.05·value)` (tighter — these are usually simulation-derived). Integer parameters use Poisson. N=10,000.

### 7.3 Tornado plot
One-at-a-time ±20% perturbation per parameter; rank by absolute change in wFOM. Output `outputs/plots/wfom_tornado.png`.

### 7.4 Category breakdown plot
Stacked bar: wFOM split into category contributions for each (design, reference) pair. Identifies dominant categories.

---

## 8. Phase-by-phase execution

### Phase 1 — Bootstrap (~30 min)
1. `uv init` (preferred) — pyproject.toml with deps: `pydantic>=2`, `pyyaml`, `numpy`, `pandas`, `scipy`, `matplotlib`, `typer`, `rich`, `tabulate`, `jinja2`, `h5py` (for OpenMC ingest), `openmc` (optional, for full statepoint API). Dev deps: `pytest`, `pytest-cov`, `ruff`, `pyright`.
2. Create directory tree from §2. Empty `__init__.py`s. `.gitignore` (Python defaults + `outputs/` + `inputs/*/` except READMEs).
3. `git init && git add -A && git commit -m "bootstrap: project skeleton"`.
4. Makefile: `install`, `test`, `lint`, `benchmark`, `wfom`, `ingest`, `sensitivity`, `report`, `all`, `clean`.
**Done when:** `make install && make test` exits 0 (no tests yet).

### Phase 2 — Data layer (~60 min)
1. Write `data/parameters_schema.yaml` from §3 (full parameter dictionary with normalizers).
2. Write `data/economic_assumptions.yaml`:
   ```yaml
   prices:
     electricity_usd_per_mwh: 60
     district_heat_usd_per_mwh: 50
     hydrogen_usd_per_kg: 5
     desalinated_water_usd_per_m3: 1.0
   reference_year: 2026
   discount_rate: 0.07
   ```
3. Write the four reactor YAMLs in the categorized structure of §4.
4. Implement `data_models.py` (pydantic v2: Reactor, Category, Parameter, AHPMatrix, EconomicAssumptions).
5. Implement `loader.py`: validate YAML, compute derived parameters (`thermal_efficiency`, `footprint_per_mwe`, `spent_fuel_per_mwh`, `specific_revenue`, `non_electric_revenue_share`), raise on schema drift.
6. Implement `normalizers.py`: three pure functions + dispatch.
7. Tests: `test_loader.py` round-trips all four YAMLs; `test_normalizers.py` covers identity (N(x,x)=0), monotonicity, hard constraints, edge cases (negative `mtc`, zero in min direction).
**Done when:** `make test` passes ≥12 tests.

### Phase 2.5 — Simulation ingestion (~60 min) **NEW**
1. Implement `ingest_openmc.py`: open `inputs/openmc/<run-id>/statepoint.h5` via `openmc.StatePoint`, extract `k_eff`, peaking factor, MTC, Doppler, max LHR, cycle-length proxy from depletion. See `SIMULATION_REQUIREMENTS.md §OpenMC` for required tallies.
2. Implement `ingest_openfoam.py`: parse `inputs/openfoam/<run-id>/postProcessing/` and `summary.json`, extract MDNBR, PCT, mass flow, pressure drop, outlet temp. See `SIMULATION_REQUIREMENTS.md §OpenFOAM`.
3. Both ingest scripts merge into `data/reactors/aegis40.yaml` (or a chosen design ID via `--target` flag), updating values and setting `status: confirmed`, `source: openmc/openfoam`, `notes: "ingested from <run-id> on <date>"`.
4. Idempotent: re-running the same ingest produces the same YAML (no churn).
5. CLI: `benchmark ingest --simulation openmc --run-id <id> --target aegis40`.
6. Tests: mock statepoint.h5 (using `openmc.StatePoint` programmatically) and mock OpenFOAM `postProcessing/` with known values; assert YAML updates correctly.
**Done when:** `make ingest` works on a synthetic test fixture and updates the YAML.

### Phase 3 — Benchmark sheet (~30 min)
1. Implement `benchmark_sheet.py`: build DataFrame, rows = parameters from schema (organized by category), cols = the four reactors. Render values as `value unit` with `[tbd]` / `[target]` markers.
2. CLI: `benchmark run` writes `outputs/benchmark_table.{csv,md,tex}`.
3. The Markdown should reproduce PER Table 3 visually plus the new category-organized layout.
4. Test: snapshot the Markdown output.
**Done when:** `make benchmark` produces three files.

### Phase 4 — AHP (two-level) (~60 min)
1. Implement `ahp.py` per §6: solve principal eigenvector, compute λ_max, CI, CR; reject if CR>0.10.
2. Write all six pairwise YAMLs (1 top-level + 5 within-category) with seed values that produce the default weights of §1.1 and §3.
3. CLI: `benchmark ahp` solves all matrices and writes `data/ahp/weights_resolved.yaml` with `category_weights:` and `param_weights: {category: {param: weight}}`.
4. Tests: Saaty 1980 textbook example (4×4); deliberately inconsistent matrix → rejection; Aegis-40 seed matrices produce default weights ±0.03.
**Done when:** `make test` includes ≥4 AHP tests; weights file exists.

### Phase 5 — Hierarchical wFOM (~60 min)
1. Implement `wfom.py` per §5: load weights from `weights_resolved.yaml` (or defaults via flag); for each reference reactor, compute `S_c` per category, then total wFOM. Apply hard-constraint check first.
2. Output `WFOMResult` dataclass; serialize to JSON breakdown.
3. CLI: `benchmark wfom --design aegis40 --reference {carem25|smart|nuscale_voygr|all} [--use-default-weights]`.
4. Outputs: `outputs/wfom_results.csv` (all design×reference pairs), `outputs/wfom_breakdown_<ref>.json` (full hierarchy).
5. Tests: identity (`wFOM(R,R)=0`), monotonicity (improving a max-direction param strictly increases wFOM), sign-flip on direction change, hard-constraint rejection, sum-of-contributions = score, category-sums = total.
**Done when:** `make wfom` produces outputs; ≥8 wFOM tests pass.

### Phase 6 — Sensitivity (~45 min)
1. Implement `sensitivity.py` per §7.
2. CLI: `benchmark sensitivity --study {weight,parameter,tornado,category} --n 10000 --reference carem25`.
3. Implement `plots.py` for radar, tornado, sensitivity histogram, category breakdown.
4. Outputs: `sensitivity_summary.csv` + 4 PNGs.
5. Tests: smoke at N=100.
**Done when:** `make sensitivity` produces all artifacts.

### Phase 7 — Report generator (~30 min)
1. Jinja2 template `report.md.j2`: benchmark table, category-by-category wFOM breakdown for each reference, sensitivity percentiles, hard-constraint check, data-quality flags (TBD count, capped values, source conflicts), AHP CR values, normalizer choices.
2. CLI: `benchmark report` writes `outputs/aegis40_benchmark_report.md`.
3. Should be paste-ready into FER.
**Done when:** `make report` produces a self-contained ≥3-page Markdown file.

### Phase 8 — Notebooks + README (~30 min)
1. Four notebooks per §2 layout — thin wrappers, no logic.
2. `README.md`: 1-page quickstart + CLI command list + pointer to PLAN.md and SIMULATION_REQUIREMENTS.md.
**Done when:** `make all` runs end-to-end on a clean clone in <3 minutes.

### Phase 9 — Polish (~30 min)
1. `ruff check --fix && ruff format`.
2. Type hints + `pyright`. Resolve all errors.
3. Coverage ≥80% on `wfom.py`, `ahp.py`, `normalizers.py`.
4. Final commit per phase (~10 commits total).
**Done when:** lint clean, types clean, coverage met.

---

## 9. Verification gate

```bash
make install
make lint
make test
make all
ls -la outputs/ outputs/plots/ data/ahp/

python -c "import yaml; w=yaml.safe_load(open('data/ahp/weights_resolved.yaml')); \
  assert abs(sum(w['category_weights'].values()) - 1.0) < 1e-6; \
  print('category weights OK:', w['category_weights'])"

python -m benchmark.cli wfom --design aegis40 --reference carem25
python -m benchmark.cli wfom --design aegis40 --reference all
python -m benchmark.cli wfom --design aegis40 --reference carem25 --use-default-weights
python -m benchmark.cli sensitivity --study tornado --n 1000

# Identity check
python -c "from benchmark.wfom import compute_wfom; \
  from benchmark.loader import load_reactor; \
  r = load_reactor('carem25'); \
  result = compute_wfom(r, r); \
  assert abs(result.score) < 1e-12, f'identity broken: {result.score}'; \
  print('identity OK')"
```

Expected: every command exits 0; `wfom --all` returns 3 finite numbers (or DESIGN_FAILED with named violations); the AHP and default-weights wFOMs agree within 5%; identity property holds exactly.

---

## 10. Out-of-scope

- OpenMC / OpenFOAM model construction. The benchmark **ingests** their outputs; producing them is a separate workstream documented in `SIMULATION_REQUIREMENTS.md`.
- Digital Twin GP surrogate (PER §4.1.4). Different system.
- Web UI / dashboard. CLI + Markdown reports only.
- Database / persistent state. Filesystem + YAML.
- LCOE / full economic model. Specific Revenue is the v2 economic metric; LCOE is a v3 upgrade.
- Live cost data feeds. Prices are static in `economic_assumptions.yaml`.

---

## 11. Notes for the user (Aegis-40 team)

1. **Fill TBD entries in `aegis40.yaml`** as your sims produce results. Better: use `benchmark ingest` so the YAML updates automatically. See `SIMULATION_REQUIREMENTS.md` for what your OpenMC/OpenFOAM models must output.
2. **Re-run `make all` after each design iteration.** wFOM evolution across iterations is exactly the quantitative progress story PER §5.1 promises.
3. **Pairwise matrices are seeds, not gospel.** When the team does formal AHP elicitation, replace them. CR<0.10 enforcement refuses sloppy updates.
4. **Hard constraints are non-negotiable.** If MDNBR drops below 1.3 or PCT exceeds 1204°C, wFOM returns DESIGN_FAILED. Fix the design, not the formula.
5. **NuScale grace-period cap (720 h)** is a methodology choice. Document it explicitly in FER.
6. **SMART 540 vs 365 MWth:** decide explicitly. We default to 365 (IAEA).
7. **Adding new candidates** (Aegis-40 v2, Aegis-50, etc.): drop a YAML into `data/reactors/`. Pipeline picks it up automatically.
8. **Supervisor-facing summary:** see §1.1 for all locked decisions; §1.2 for ones still needing approval.

---

## 12. Hand-off checklist

When Sonnet finishes:

- [ ] All 9 phases complete; `make all` green.
- [ ] `outputs/benchmark_table.md` reproduces PER Table 3 + new category structure.
- [ ] `outputs/wfom_results.csv` reports `wFOM(aegis40, carem25)`, `wFOM(aegis40, smart)`, `wFOM(aegis40, nuscale_voygr)` with category breakdown.
- [ ] `outputs/sensitivity_summary.csv` shows wFOM 5–95% range per reference.
- [ ] `outputs/aegis40_benchmark_report.md` is paste-ready into FER.
- [ ] `data/ahp/weights_resolved.yaml` exists, all matrices have CR<0.10.
- [ ] Hard-constraint test passes (deliberately bad PCT triggers DESIGN_FAILED).
- [ ] Identity property test passes (`wFOM(R,R)=0` to machine precision).
- [ ] `benchmark ingest` works against synthetic OpenMC/OpenFOAM fixtures.
- [ ] One git commit per phase (~10 total) with conventional-commit messages.
- [ ] PLAN.md and SIMULATION_REQUIREMENTS.md left intact.

End of plan v2.
