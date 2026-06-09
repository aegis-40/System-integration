# Safeguards & Non-Proliferation — discharge-material attractiveness (FER 3S)

*The third "S" of 3S (Safety · Security · **Safeguards**). Frames the proliferation-resistance case for the Aegis-40 once-through SBF fuel cycle.*
*Owner: Azamhon (3S). Source analysis: `docs/safeguards_attractiveness.md` + `docs/pu_vector.csv` — discharge inventory from Samira's rev_3 OpenMC depletion (42.8 GWd/t, whole 21-FA core). Last updated: 2026-06-09.*

> **Headline:** the high-burnup, boron-free, **once-through** cycle makes the discharged material **strongly proliferation-resistant by design** — reactor-grade degraded Pu, self-protecting radiation/heat fields, non-usable spent uranium, and **no separated-fissile stream anywhere in the plant.** This is a genuine 3S design feature, not an afterthought.

---

## 1. Why this is a design feature, not a footnote

Aegis-40 makes three design choices that each *raise* proliferation resistance, and they compound:

| Design choice | Effect on attractiveness |
|---|---|
| **High discharge burnup (42.8 GWd/t)** | Degrades the Pu vector — burns Pu-239 down, breeds Pu-240/241/242 up. *More* degraded than a typical 33 GWd/t LWR. |
| **Soluble-boron-free (SBF)** | No chemistry path that could be repurposed; reactivity held by integral Gd+Er, not separable streams. |
| **Once-through cycle (no reprocessing)** | **Decisive.** There is never a separated-Pu stream to divert — the only Pu exists locked inside intact, intensely radioactive spent-fuel assemblies. |

---

## 2. Plutonium vector — reactor-grade, degraded

From `docs/pu_vector.csv` (whole-core discharge, 55.3 kg Pu):

| Isotope | wt % of Pu |
|---|---|
| Pu-238 | 2.72 |
| Pu-239 | **52.29** |
| Pu-240 | **24.62** |
| Pu-241 | 13.91 |
| Pu-242 | 6.45 |

- **Grade: REACTOR-GRADE.** Pu-240 = 24.6 wt% (weapons-grade is <7 %; reactor-grade is >19 %).
- Fissile fraction (Pu-239 + Pu-241) = **66.2 %** vs >93 % Pu-239 alone for weapons-grade.
- High burnup is what pushes Pu-239 down to 52 % — a deliberate consequence of the fuel-efficiency design point.

## 3. Intrinsic self-protection barriers

| Barrier | Value | Significance |
|---|---|---|
| Decay heat | **19.5 W/kg-Pu** (1,076 W total) | ≫ the ~2 W/kg self-protection level — heat alone degrades a device |
| Spontaneous-fission neutrons (Pu metal) | **4.33 × 10⁵ n/s/kg-Pu** | high predetonation background (Pu-240/238/242) — defeats a reliable yield |
| SF neutrons incl. Cm-244 | 5.40 × 10⁷ n/s/kg | Cm-244 dominates the spent-fuel handling radiation field |

## 4. Spent uranium — non-usable

- Discharge U-235 = **1.10 wt%** — far below the 20 % LEU/HEU line and the ~90 % weapons line. Recovered uranium is **not a usable enrichment.**

## 5. Significant-quantity (SQ) accounting — IAEA, 8 kg Pu/SQ

- Whole-core Pu 55.3 kg = **6.9 SQ**, but embedded in intact assemblies.
- Per discharge batch (¼ core) 13.8 kg = **1.7 SQ** — inside self-protecting, intensely radioactive spent fuel.
- Minor actinides (kg): Np-237 3.34, Am-241 0.37, Am-243 0.71, Cm-244 0.27 — of safeguards interest **only after reprocessing**, which the cycle does not include.

## 6. Proliferation-resistance summary (FER drop-in)

- **Intrinsic (raised by high burnup):** reactor-grade degraded Pu (Pu-239 52 %, Pu-240 25 %, fissile 66 %); 19 W/kg-Pu decay heat; high SF-neutron background; spent U at 1.10 % U-235.
- **Extrinsic (decisive):** Pu is locked inside self-protecting, intensely radioactive **intact spent-fuel assemblies** (whole-assembly dose ≫ the 1 Gy/h self-protecting threshold), under IAEA safeguards, in a **once-through** cycle — **no separated-fissile stream to divert.**
- **Net:** high burnup + SBF + once-through compound the standard spent-fuel proliferation resistance; the design introduces no reprocessing or separated-fissile streams.

---

## 7. Where this connects in the FER + this repo

| Hook | Where |
|---|---|
| 3S Safeguards narrative | this file → FER 3S / §5 originality (domestic, non-proliferating cycle) |
| Discharge source term + decay heat | [[reference-aegis40-files]]; `safety/openmc_rev3_alignment.md` §5 |
| Spent-fuel pool criticality (unborated, k≤0.95) | `layout/aux_systems.md` §7 |
| ISFSI / dry-cask staging | `layout/building_list.md` (SFB) |
| Source analysis (NEU-produced) | `docs/safeguards_attractiveness.md`, `docs/pu_vector.csv` (Samira's OpenMC back-end) |

## 8. Open / next

- Optional **burnup-trajectory plot** (Pu-239 fraction vs burnup) needs the per-step Pu vector from the depletion `.h5` — flagged in the source doc.
- Pull the three plots (`pu_vector.png`, `self_protection.png`, `snm_inventory.png`) into the FER figure set when assembling §3S.
- Cite: Wu et al., *Int. J. Energy Res.* (2020) — proliferation-resistance barriers; IAEA Safeguards Glossary (significant quantities).

*Cross-refs: `safety/safety_criteria.yaml`, `safety/openmc_rev3_alignment.md`, `layout/aux_systems.md`.*
