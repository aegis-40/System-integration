# Simulation Requirements — OpenMC and OpenFOAM Outputs for Benchmarking

**Purpose:** Define the contract between the simulation team (OpenMC neutronics, OpenFOAM thermal-hydraulics) and the benchmarking pipeline (`benchmark ingest`). Anything listed here is a *required output* — the benchmark tool depends on it. Anything not listed here is optional but welcome.

**Audience:** Aegis-40 simulation engineers writing OpenMC inputs, OpenFOAM cases, and post-processing scripts.

**Companion document:** `PLAN.md` (the benchmarking pipeline this feeds into).

---

## 1. Why this matters

The wFOM (see PLAN.md §5) needs concrete numbers from your simulations. If you don't produce them, the corresponding parameters stay `status: tbd` in `aegis40.yaml` and the wFOM ignores those terms — making the score weaker and less defensible.

Treat this file as your acceptance test. A simulation run is "complete" when it produces every output in §3 (OpenMC) or §4 (OpenFOAM) below in the specified format.

---

## 2. Conventions (apply to both codes)

### 2.1 Run identification

Every simulation run produces a directory under `inputs/openmc/<run-id>/` or `inputs/openfoam/<run-id>/`. The `<run-id>` is a string of the form:

```
<reactor>_<scenario>_<state>_<YYYYMMDD>_<short-git-hash>
```

Examples:
- `aegis40_steady_BOL_20260512_a3f9b2c`
- `aegis40_sbo_transient_MOC_20260601_b1e2d4a`
- `aegis40_steady_EOL_20260720_c5d6e7f`

### 2.2 Mandatory metadata file

Every run directory MUST contain a `metadata.json` at its root:

```json
{
  "reactor_id": "aegis40",
  "scenario": "steady_state | sbo | mslb | loca | depletion_sweep",
  "state": "BOL | MOC | EOL | post-trip",
  "run_date_utc": "2026-05-12T14:32:00Z",
  "code": "openmc | openfoam",
  "code_version": "0.15.2 | v11",
  "geometry_git_hash": "a3f9b2c",
  "input_files": ["materials.xml", "geometry.xml", "settings.xml", "tallies.xml"],
  "operator": "Author Name <email>",
  "notes": "Free-form description"
}
```

Without `metadata.json` the ingest tool refuses to read the run.

### 2.3 Units

All outputs use SI units. Power = W or MW (be explicit). Temperature = K or °C (be explicit). Length = m. Pressure = Pa or MPa (be explicit). Time = s.

### 2.4 Provenance

Every numerical output should carry an associated uncertainty (1-sigma) where computed. Monte Carlo: take from OpenMC's tally `std_dev`. CFD: from solver residual or mesh-convergence study.

---

## 3. OpenMC requirements

### 3.1 Required output files in each run directory

```
inputs/openmc/<run-id>/
├── metadata.json
├── summary.h5                    # geometry summary (auto-generated)
├── statepoint.<batches>.h5       # main result file
├── depletion_results.h5          # for depletion runs only
├── tallies.out                   # tally summary text dump
└── derived.json                  # post-processed scalar parameters (see §3.4)
```

`derived.json` is what the benchmark tool reads first. All scalars listed in §3.3 must appear there. The HDF5 files are for traceability and re-derivation.

### 3.2 Required tallies (declare in `tallies.xml`)

| Tally | Filter | Score | Purpose |
|---|---|---|---|
| `flux_mesh` | RegularMesh (radial × axial, ≥17×20) | flux | Power distribution, peaking factor |
| `power_mesh` | Same RegularMesh | kappa-fission | Power per cell for OpenFOAM coupling |
| `power_assembly` | Cell filter (per fuel assembly) | kappa-fission | Assembly-level power for radial peaking |
| `flux_axial` | RegularMesh axial only (≥20 nodes) | flux | Axial peaking factor |
| `reactivity` | (see §3.3.3) | nu-fission, absorption | k_eff via direct calc; not a tally |
| `temperature_sweep_doppler` | run-time multi-eval | k_eff | Doppler coefficient (see §3.3.4) |
| `temperature_sweep_moderator` | run-time multi-eval | k_eff | MTC (see §3.3.5) |
| `delayed_neutron_fraction` | DelayedGroup | nu-fission | β_eff for kinetics |

### 3.3 Required scalar parameters

These go into `derived.json` and will be ingested into `aegis40.yaml`. Every value carries `value`, `uncertainty`, `unit`, and `source` (the tally name + statepoint hash).

#### 3.3.1 `k_eff`
- BOL, MOC, EOL — three values, one per state.
- Source: combined collision-tracklength-absorption estimator.
- Statistical uncertainty: ≤ 100 pcm (1σ). Use enough particles per batch.
- Schema: `{value: 1.0023, uncertainty: 0.0008, unit: "—", state: "BOL"}`

#### 3.3.2 `cycle_length_efpd`
- Computed from depletion: time at which `k_eff` drops below 1.000 + reactivity reserve.
- Source: depletion sweep.
- Schema: `{value: 547, uncertainty: 12, unit: "days"}`

#### 3.3.3 `peaking_factor_3d`
- Maximum cell power / average cell power across the active core mesh.
- Source: `power_mesh` tally.
- Required: report at BOL, MOC, EOL.
- Schema: `{value: 1.42, uncertainty: 0.02, unit: "—", state: "BOL"}`

#### 3.3.4 `doppler_coefficient`
- Δρ/ΔT for fuel temperature, where ρ is reactivity in pcm.
- Method: run two simulations at fuel temperatures `T_ref ± 50 K` (typically 600 K and 700 K), compute `(ρ_high − ρ_low) / ΔT`.
- Required: must be NEGATIVE (hard constraint).
- Schema: `{value: -3.2, uncertainty: 0.4, unit: "pcm/K"}`

#### 3.3.5 `moderator_temperature_coefficient` (MTC)
- Δρ/ΔT for moderator temperature.
- Method: same dual-evaluation as Doppler but for water density at moderator temperatures (typically 560 K and 580 K).
- Required: must be NEGATIVE (hard constraint, captured by `hard_ceiling: 0` in schema).
- Schema: `{value: -45.0, uncertainty: 5.0, unit: "pcm/K"}`

#### 3.3.6 `scram_worth`
- Total reactivity worth of all control rods inserted, in pcm.
- Method: `k_eff` with rods out − `k_eff` with rods in.
- Required: report shutdown margin = scram_worth − maximum stuck-rod worth − reactivity reserve.
- Schema: `{value: 12500, uncertainty: 200, unit: "pcm", shutdown_margin: 4500}`

#### 3.3.7 `linear_heat_rate_max`
- Maximum linear heat rate in the core, kW/m.
- Method: `power_assembly` tally / (rod count × active fuel length) for the hottest assembly.
- Schema: `{value: 18.5, uncertainty: 0.3, unit: "kW/m", state: "BOL"}`

#### 3.3.8 `discharge_burnup`
- Average burnup of fuel discharged at end of cycle.
- Source: depletion summary.
- Schema: `{value: 45.2, uncertainty: 0.5, unit: "GWd/MTU"}`

#### 3.3.9 `delayed_neutron_fraction` (β_eff)
- Effective delayed neutron fraction.
- Source: prompt-vs-total nu-fission tally ratio.
- Used by transient analysis but reported here.
- Schema: `{value: 0.00665, uncertainty: 0.00005, unit: "—"}`

### 3.4 `derived.json` schema

```json
{
  "run_id": "aegis40_steady_BOL_20260512_a3f9b2c",
  "code": "openmc",
  "k_eff": {
    "BOL": {"value": 1.0023, "uncertainty": 0.0008, "unit": "—"},
    "MOC": {"value": 1.0001, "uncertainty": 0.0009, "unit": "—"},
    "EOL": {"value": 0.9985, "uncertainty": 0.0009, "unit": "—"}
  },
  "cycle_length_efpd": {"value": 547, "uncertainty": 12, "unit": "days"},
  "peaking_factor_3d": {"value": 1.42, "uncertainty": 0.02, "unit": "—", "state": "BOL"},
  "doppler_coefficient": {"value": -3.2, "uncertainty": 0.4, "unit": "pcm/K"},
  "moderator_temperature_coefficient": {"value": -45.0, "uncertainty": 5.0, "unit": "pcm/K"},
  "scram_worth": {"value": 12500, "uncertainty": 200, "unit": "pcm"},
  "shutdown_margin": {"value": 4500, "unit": "pcm"},
  "linear_heat_rate_max": {"value": 18.5, "uncertainty": 0.3, "unit": "kW/m"},
  "discharge_burnup": {"value": 45.2, "uncertainty": 0.5, "unit": "GWd/MTU"},
  "delayed_neutron_fraction": {"value": 0.00665, "uncertainty": 0.00005, "unit": "—"},
  "coupling_outputs": {
    "power_distribution_path": "tallies.out#power_mesh",
    "axial_power_shape_path": "tallies.out#flux_axial"
  }
}
```

### 3.5 OpenMC quality gates (don't ship a run that fails these)

- Particles per batch ≥ 100,000 for criticality runs; ≥ 10,000 active batches.
- Inactive batches ≥ 50; verify Shannon entropy converged.
- Statistical uncertainty on `k_eff` ≤ 100 pcm (1σ).
- Cross-section library: ENDF/B-VIII.0 (PER §4.1.1 spec). Other libs are acceptable for sensitivity studies but mark them in metadata.
- Doppler/MTC: ΔT large enough that signal exceeds 3σ.

### 3.6 Coupling output for OpenFOAM

OpenMC must emit a per-cell power density file for the OpenFOAM team to consume:

```
inputs/openmc/<run-id>/coupling/power_density.csv
```

Columns: `cell_id, x_m, y_m, z_m, power_density_W_per_m3, uncertainty`.

This becomes the volumetric heat source in OpenFOAM. The benchmark itself doesn't read this, but it's the same run directory so keep them together.

---

## 4. OpenFOAM requirements

### 4.1 Required output structure

```
inputs/openfoam/<run-id>/
├── metadata.json
├── case_summary.txt              # log: solver, schemes, BCs, mesh size
├── postProcessing/
│   ├── probes/T/              # temperature probes
│   ├── probes/p/              # pressure probes
│   ├── probes/U/              # velocity probes
│   ├── surfaceFieldValue/clad_max/  # maximum clad temperature over time
│   ├── volFieldValue/MDNBR/   # minimum DNBR over the domain
│   ├── volFieldValue/mass_flow/
│   └── pressure_drop/
├── derived.json                  # post-processed scalars (see §4.3)
└── coupling/
    └── temperature_field.csv     # for OpenMC feedback
```

### 4.2 Required fields and probes

| Output | Format | Frequency | Purpose |
|---|---|---|---|
| Temperature `T` | volume field | every write | clad/coolant temperature distribution |
| Pressure `p` | volume field | every write | natural circulation driving pressure |
| Velocity `U` | volume field | every write | mass flow, mixing |
| Density `rho` | volume field | every write | natural circulation buoyancy |
| Probe T at clad surface | time series | per timestep | PCT tracking |
| Probe T at hot-channel exit | time series | per timestep | outlet T extreme |
| Surface integral mass flow at core inlet | time series | per timestep | natural circulation flow rate |
| Pressure drop core inlet to outlet | time series | per timestep | driving head |
| MDNBR field | volume scalar | every write | DNB safety margin |

### 4.3 Required scalar parameters in `derived.json`

#### 4.3.1 `pct` (Peak Cladding Temperature)
- Maximum clad surface temperature anywhere in the simulated domain over the simulated time window.
- Steady-state: scalar value at converged solution.
- Transient (SBO, MSLB, LOCA): peak value during transient + time-of-peak.
- Schema: `{value: 642.5, unit: "°C", scenario: "steady_state", time_s: null}` or `{value: 1180, unit: "°C", scenario: "sbo", time_s: 14400}`

#### 4.3.2 `mdnbr` (Minimum Departure from Nucleate Boiling Ratio)
- Minimum value of DNBR across the entire simulated domain.
- Method: W-3 correlation (or Bowring, or Groeneveld) computed cell-by-cell, take minimum.
- Required: must be ≥ 1.3 (hard constraint).
- Schema: `{value: 2.45, unit: "—", correlation: "W-3", limit: 1.3, scenario: "steady_state"}`

#### 4.3.3 `mass_flow_rate`
- Steady-state mass flow rate through the core, kg/s.
- For natural circulation: this is the achieved flow at the design power.
- Schema: `{value: 542, uncertainty: 8, unit: "kg/s"}`

#### 4.3.4 `pressure_drop_core`
- Static pressure drop from core inlet to outlet, Pa.
- For natural circulation, lower is better (less driving head needed).
- Schema: `{value: 14500, unit: "Pa"}`

#### 4.3.5 `outlet_temperature`
- Bulk-average coolant temperature at core outlet, °C.
- Schema: `{value: 326, uncertainty: 1, unit: "°C"}`

#### 4.3.6 `void_fraction_max` (only for boiling cases)
- Maximum void fraction in the core. Should be near zero for sub-cooled normal operation.
- Schema: `{value: 0.001, unit: "—", model: "Euler-Euler"}`

#### 4.3.7 `chf_ratio_min` (Critical Heat Flux margin)
- Minimum CHF / actual heat flux ratio.
- Schema: `{value: 1.85, unit: "—", correlation: "Groeneveld"}`

#### 4.3.8 `mixing_factor` (engineering hot-channel factor)
- Hot-channel temperature rise / average temperature rise.
- Schema: `{value: 1.18, unit: "—"}`

### 4.4 `derived.json` schema (OpenFOAM)

```json
{
  "run_id": "aegis40_steady_BOL_20260512_a3f9b2c",
  "code": "openfoam",
  "scenario": "steady_state",
  "pct": {"value": 642.5, "unit": "°C", "scenario": "steady_state", "time_s": null},
  "mdnbr": {"value": 2.45, "unit": "—", "correlation": "W-3", "limit": 1.3},
  "mass_flow_rate": {"value": 542, "uncertainty": 8, "unit": "kg/s"},
  "pressure_drop_core": {"value": 14500, "unit": "Pa"},
  "outlet_temperature": {"value": 326, "uncertainty": 1, "unit": "°C"},
  "void_fraction_max": {"value": 0.001, "unit": "—", "model": "Euler-Euler"},
  "chf_ratio_min": {"value": 1.85, "unit": "—", "correlation": "Groeneveld"},
  "mixing_factor": {"value": 1.18, "unit": "—"},
  "convergence": {
    "residual_continuity": 1e-6,
    "residual_momentum": 1e-5,
    "residual_energy": 1e-7,
    "iterations": 12500
  }
}
```

### 4.5 OpenFOAM quality gates

- Mesh independence: at least 3 mesh densities, report PCT and MDNBR change <2% from medium to fine.
- Boundary-layer resolution: y+ < 1 on cladding surfaces (k-ω SST requirement).
- Turbulence model: k-ω SST (PER §4.1.2 spec).
- Solver: `buoyantSimpleFoam` for steady, `buoyantPimpleFoam` for transient (PER §4.1.2). For 2-phase: `foamForNuclear` Euler-Euler solver.
- Convergence: continuity residual < 1e-6, energy residual < 1e-7, all monitor probes flat over last 1000 iterations.
- Conjugate heat transfer enabled at fuel/clad/coolant interfaces.

### 4.6 Coupling output for OpenMC

Emit a temperature field that OpenMC can read for the next iteration:

```
inputs/openfoam/<run-id>/coupling/temperature_field.csv
```

Columns: `cell_id, x_m, y_m, z_m, temperature_K, density_kg_per_m3`.

---

## 5. Coupling iteration (OpenMC ↔ OpenFOAM)

PER §4.1 calls for iterative neutronics/TH coupling. Workflow:

1. OpenMC run #1 with assumed temperatures → produces `power_density.csv`.
2. OpenFOAM run #1 with that power source → produces `temperature_field.csv`.
3. OpenMC run #2 with updated temperatures → produces new power.
4. Repeat until k_eff and PCT change <0.1% between iterations.

Each iteration is its own `<run-id>`. Tag them with `coupling_iteration: 1, 2, ...` in `metadata.json`. The benchmark ingest takes the last (converged) iteration as the design point.

---

## 6. Scenario list (what to simulate)

For the FER, the following scenarios should each produce a complete OpenFOAM run with full `derived.json`:

| ID | Description | Required by |
|---|---|---|
| `steady_state_BOL` | Full power, beginning of life | wFOM baseline |
| `steady_state_MOC` | Full power, middle of cycle | depletion check |
| `steady_state_EOL` | Full power, end of cycle | depletion check |
| `sbo` | Station Black-Out | grace period validation |
| `mslb` | Main Steam Line Break | safety case (PER §4.1.2 cites Zhang 2025) |
| `loca_small` | Small-Break LOCA | ECCS validation |
| `load_follow_50pct` | 50% power transient | I&C / Digital Twin training |

OpenMC scenarios: BOL, MOC, EOL depletion sweep + scram-worth eval at each. Total 4 OpenMC runs minimum.

---

## 7. Naming convention summary

```
<reactor>_<scenario>_<state>_<YYYYMMDD>_<git-hash>

reactor:  aegis40 | aegis40v2 | ...
scenario: steady | sbo | mslb | loca_small | loca_large | load_follow | depletion
state:    BOL | MOC | EOL | post-trip | transient
```

Both codes use the same convention so a single `<run-id>` may exist in both `inputs/openmc/` and `inputs/openfoam/` for a coupled iteration.

---

## 8. Quickref — what the benchmark ingests

| Parameter in `aegis40.yaml` | Comes from | Code | Required scenario |
|---|---|---|---|
| `pct` | `derived.json` | OpenFOAM | steady_state_BOL (peak across BOL/MOC/EOL) |
| `mdnbr` | `derived.json` | OpenFOAM | steady_state_BOL |
| `peaking_factor_3d` | `derived.json` | OpenMC | BOL |
| `mtc` | `derived.json` | OpenMC | BOL |
| `cycle_length_efpd` | `derived.json` | OpenMC | depletion |
| `linear_heat_rate` | `derived.json` | OpenMC | BOL |
| `burnup` | `derived.json` | OpenMC | depletion (EOL) |

(Doppler, scram_worth, β_eff, mass_flow, outlet_T, etc. are tracked in YAML as descriptive fields but don't currently feed wFOM. They appear in the report and may join wFOM in a future revision.)

---

## 9. What to do if a parameter can't be produced

If a simulation can't compute a required output (e.g., MDNBR not yet implemented as a post-processor), the team should:

1. Set the value to `null` in `derived.json` with a `pending: true` flag.
2. Add a note to `metadata.json` explaining the gap.
3. Plan when it will be available.

The benchmark tool treats `null` as `status: tbd` and reports the gap in the FER report. Better to ship a partial `derived.json` than to delay.

---

## 10. File checklist for a complete run

OpenMC:
- [ ] `metadata.json`
- [ ] `summary.h5`
- [ ] `statepoint.<batches>.h5`
- [ ] `depletion_results.h5` (if depletion)
- [ ] `tallies.out`
- [ ] `derived.json`
- [ ] `coupling/power_density.csv` (if coupled run)

OpenFOAM:
- [ ] `metadata.json`
- [ ] `case_summary.txt`
- [ ] `postProcessing/` populated
- [ ] `derived.json`
- [ ] `coupling/temperature_field.csv` (if coupled run)

End of simulation requirements.
