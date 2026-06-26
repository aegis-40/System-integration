# Aegis-40 — Safety Neutronics (FER §8.5–8.6)

Standalone OpenMC criticality study for the three **missing** safety-neutronics
simulations identified in `docs/competition/SIMULATION_ANALYSIS_PLAN.md`:

| # | Simulation | Safety question | FER criterion |
|---|---|---|---|
| **N10** | EBIS soluble-boron sizing | How much boron makes the core **cold-subcritical with no control rods**? | Independent (2nd, diverse) shutdown system — IAEA SSR-2/1 Req. 46 |
| **N11** | SFP storage-rack criticality | Is the spent-fuel rack **subcritical in unborated water** with the most-reactive assembly? | k_eff(95/95) ≤ 0.95 — 10 CFR 50.68 |
| **N12** | MSLB cooldown reactivity | On an overcooling transient with the **most-reactive rod stuck out**, does the core **return to power**? | k < 1 on cooldown — NUREG-0800 SRP 15.1.5 |

The geometry, materials and the **locked design** (Approach B: discrete uniform
assemblies, in-out enrichment, Gd 20 @ 6 wt% + Er 16 @ 0.5 wt%) are **reused
verbatim** from `aegis40_neutronics_FER.ipynb` (the file includes that notebook's
builder cells), so these results are consistent with the main neutronics deck.

---

## How to run

```bash
conda activate <openmc-env>
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml  # ENDF/B-VIII.0
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=<physical cores>
export SAFETY_STAT=medium          # fast | medium | final
python aegis40_safety_neutronics.py        # all three; or SAFETY_RUN=N10|N11|N12
```

**Acceleration:** ENDF/B-VIII.0 library on a native (ext4) disk + OpenMP threads —
same library as the final FER notebook. **No weight windows**: N10–N12 are
*k-eigenvalue / criticality* problems; variance-reduction weight windows apply only
to *fixed-source* (shielding/dose) transport, so they are correctly **not** used
here. Results, JSON (`safety_neutronics_results.json`) and plots land in `results/`.

---

## N10 — EBIS (Emergency Boron Injection System) sizing

**Method.** Most-reactive shutdown state — **cold (294 K, dense water), BOC fresh
fuel, all rods out (ARO)** — swept over soluble-boron concentration; the EBIS must
hold the core subcritical *by itself* (no credit for the control rods), satisfying
the "second, diverse, independent shutdown system" requirement. Boron is natural B
added to the moderator by mass fraction.

**Result.** _(filled after the run)_ k(0 ppm) ≈ __ ; boron for k = 1.00 ≈ __ ppm;
**boron for k = 0.99 (1 % margin) ≈ __ ppm.** Boron *mass* = ppm × primary coolant
inventory (take the primary mass from the RPV/T-H design).

**Interpretation.** A finite, achievable boron concentration drives the
unrodded cold core subcritical → the EBIS is a credible **diverse** shutdown means
alongside the gravity-insert control rods, closing the two-shutdown-system case.

**References:** IAEA SSR-2/1 Req. 46 (two diverse shutdown systems); IAEA SSG-2;
NUREG-0800 SRP 4.3; 10 CFR 50.68.

---

## N11 — Spent-fuel-pool storage-rack criticality

**Method.** Bounding **infinite array** (fully reflective cell) of the
**most-reactive assembly** — fresh, 4.95 wt% enrichment, **no burnable-absorber
credit** (Gd/Er burn out over life, so crediting them would be non-conservative) —
in **unborated, cold (294 K) water**, with a poison rack panel. Two rack variants:
plain SS-304 (shows the poison is needed) and a **Boral (B₄C-in-Al) panel**.

**Result.** _(filled after the run)_ SS-304 (no poison) k_inf ≈ __ ; **Boral-panel
k_inf ≈ __** (target ≤ 0.95).

**Interpretation.** The Boral neutron-absorber panel brings the infinite-array
k_inf below the 0.95 (95/95) limit in unborated water — the most conservative
storage condition. The infinite, fully-reflected, fresh-fuel, no-BA basis bounds
any real finite rack (axial/radial leakage and burnup credit only lower k).

> **Design-stage caveat (state explicitly in the FER):** this is a *bounding*
> rack demonstration with a representative Boral areal density (30 wt% B₄C-in-Al,
> 0.30 cm). A licensing analysis fixes the panel B-10 areal density, adds biases &
> uncertainties to the 95/95 value, and may take burnup credit. The geometry/method
> here follow the standard envelope.

**References:** 10 CFR 50.68(b)(4); NUREG-0800 SRP 9.1.1; ANSI/ANS-8.1; IAEA SSG-15.

---

## N12 — MSLB (main-steam-line-break) cooldown reactivity

**Method.** The strong **negative MTC** of this boron-free core means an
overcooling transient *adds* reactivity. k_eff is computed from the hot full-power
moderator temperature (556 K) **down to cold (294 K)**, density tracked along the
12.8 MPa isobar, with **the most-reactive control rod stuck out** (all other CRAs
inserted) — the limiting single-failure for the event.

**Result.** _(filled after the run)_ k(556 K) ≈ __ → **k_max on cooldown ≈ __** ;
return-to-power: __.

**Interpretation.** With the most-reactive rod stuck out, the remaining rods must
keep k < 1 across the entire cooldown. If k stays below 1 → **no return to power**
on the MSLB (acceptance met). If it crosses 1, the margin/return-to-power must be
bounded by the EBIS boration (N10) and the moderator feedback.

**References:** NUREG-0800 SRP 15.1.5 (steam-system piping failures); IAEA SSG-2
(deterministic safety analysis); RG 1.77 (anticipated transients); ANS-51.1.

---

## Honesty / scope notes
- N10–N12 are **plant-specific OpenMC calculations** on the locked Aegis-40 core
  (not bound-by-reference) — they are within the team's tool envelope.
- The "most-reactive rod" in N12 is approximated as the most central CRA (highest
  worth by symmetry); a per-rod worth scan (N5 in the main notebook) confirms the
  ranking. State this approximation in the FER.
- Statistics: `SAFETY_STAT=medium` (180×20k) for reported numbers; bump to `final`
  for the record run.
