# Sensor Inventory — Aegis-40

*Source: companion to `ic_architecture.md`. Drop-in candidate for FER §8.7 subsection on sensor / detector list.*
*Owner: Azamhon. Last updated: 2026-05-27.*

---

## 1. Conventions

- **Class 1E** = safety-qualified, IEEE 323 / 344 environmental + seismic, IEC 60880 Cat A signal chain.
- **Non-1E** = control / monitoring only, no safety credit.
- **Redundancy n/N** = number of channels / number required to make a decision. e.g. **2/4** means 4 redundant channels with 2-of-4 voting.
- **Diversity** = different sensing principle covering the same variable (defense against common-cause failure).
- All channels include local indication + transmission to RPS/ESFAS or DCS as noted.

---

## 2. Master sensor table

| # | Channel | Variable | Sensor type | Qty | Range | Accuracy | Redundancy | Class | Feeds | Diverse backup |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NF-SR | Source-range neutron flux | Fission chamber (BF₃ option for startup) | 2 | 1 – 1e6 cps | ±10 % | 1/2 | 1E | RPS startup + log power | NF-IR overlap |
| 2 | NF-IR | Intermediate-range neutron flux | Compensated ion chamber | 2 | 1e-8 – 1e-3 A (≈ 1e-5 – 100 % power) | ±5 % | 1/2 | 1E | RPS + log/linear power | NF-PR overlap |
| 3 | NF-PR | Power-range neutron flux | Uncompensated ion chamber (4 axial sections) | 4 | 0 – 125 % rated | ±2 % | **2/4** | 1E | RPS, control, axial offset | Core exit T (T-CE) |
| 4 | T-HL | Hot-leg coolant temperature | RTD (Pt100), triple-element | 4 | 0 – 350 °C | ±0.5 °C | **2/4** | 1E | RPS (OT-ΔT, OP-ΔT), control | T-CE (thermocouples) |
| 5 | T-CL | Cold-leg coolant temperature | RTD (Pt100), triple-element | 4 | 0 – 350 °C | ±0.5 °C | **2/4** | 1E | ΔT calc, control | — |
| 6 | T-CE | Core-exit coolant temperature | Thermocouple K-type (array, distributed) | 8 | 0 – 1200 °C | ±2 °C | array | 1E | Post-accident monitoring, RPS confirmation | T-HL |
| 7 | P-PZR | Pressurizer pressure | Capacitance / piezoresistive transmitter | 4 | 0 – 20 MPa | ±0.1 % FS | **2/4** | 1E | RPS (hi/lo P), control | — |
| 8 | F-LP | Primary loop flow | Elbow tap + venturi (∂P) | 2 per loop | 0 – 110 % rated | ±2 % | **2/4** | 1E | RPS (low flow trip) | F-UFM ultrasonic |
| 9 | F-UFM | Primary loop flow (diverse) | Ultrasonic transit-time | 1 per loop | 0 – 110 % rated | ±1 % | — | non-1E | DCS, calorimetric reference | F-LP |
| 10 | L-SG-NR | SG narrow-range level | Differential pressure | 4/SG | 0 – 100 % NR span | ±3 % | **2/4** | 1E | RPS (low SG level), EFW init | L-SG-WR overlap |
| 11 | L-SG-WR | SG wide-range level | Differential pressure | 2/SG | 0 – 100 % WR span (covers dry-out) | ±5 % | — | non-1E | Post-accident monitoring | L-SG-NR |
| 12 | P-CONT | Containment pressure | Capacitance transmitter, EQ-qualified to LOCA env | 4 | 0 – 0.5 MPa | ±0.5 % FS | **2/3** | 1E | ESFAS (CI), RPS confirm | — |
| 13 | RAD-CONT | Containment radiation | Gamma area monitor + particulate skid | 4 | 1e-6 – 1e3 Sv/h (wide-range) | ±20 % decade | **2/3** | 1E | ESFAS (CI, vent isolation) | RAD-MSL |
| 14 | RAD-MSL | Main steam line radiation | Gamma monitor (one per steam line) | 2 | 1e-6 – 1e2 Sv/h | ±20 % decade | 1/2 | 1E | ESFAS (MSI) | — |
| 15 | RAD-SB | Site boundary radiation | Gamma + particulate + iodine | 4 (cardinal) | 1e-8 – 1e2 Sv/h | ±20 % decade | — | non-1E | Emergency response, post-accident | — |
| 16 | L-PZR | Pressurizer level | Differential pressure | 4 | 0 – 100 % | ±2 % | — | non-1E | DCS (heater / spray control) | — |
| 17 | POS-CRD | Control rod position | Reed switch (digital) + LVDT (analog) | 1/rod, 2 channels | 0 – 100 % | ±1 step | 1E (one channel) | RPS confirmation, control | — |
| 18 | T-FW | Feedwater temperature | RTD | 2/loop | 0 – 250 °C | ±1 °C | — | non-1E | DCS (FW control) | — |
| 19 | F-FW | Feedwater flow | Venturi (∂P) | 2/SG | 0 – 110 % | ±2 % | — | non-1E | DCS (3-element FW control), calorimetric | — |
| 20 | T-CRDM | Control rod drive coil temperature | RTD | 1/drive | 0 – 200 °C | ±2 °C | — | non-1E | DCS (drive fault detection) | — |
| 21 | P-SG | Steam generator pressure | Capacitance transmitter | 4/SG | 0 – 10 MPa | ±0.5 % FS | **2/4** | 1E | ESFAS (MSI on low SG P), DCS | P-PZR cross-check |

**Channel count summary:**
- Class 1E channels in inventory: **14** (#1–#8, #10, #12–#14, #17, #21)
- Non-1E channels: **7** (#9, #11, #15–#16, #18–#20)
- Channels under 2-of-4 voting: **7** (flux PR, T-HL, T-CL, P-PZR, F-LP, L-SG-NR, P-SG); P-CONT + RAD-CONT at 2-of-3

---

## 3. Coverage map — every safety criterion has at least one sensor

Cross-check against `safety/safety_criteria.yaml`:

| Safety criterion ID | Observed by | Trip |
|---|---|---|
| `k_eff_operating` | NF-PR | High flux trip |
| `mtc_full_power`, `dtc_doppler`, `void_coefficient` | NF-PR + T-HL + T-CL (derived) | — (DBE prevention, no trip) |
| `mdnbr_steady`, `mdnbr_transient` | F-LP + T-HL + T-CL + NF-PR (derived) | Low flow + OT-ΔT trip |
| `pct_loca` | T-CE (post-accident) | High outlet T trip |
| `fuel_centerline_temperature` | inferred (fuel model + NF-PR + T-HL) | — |
| `primary_pressure_design` | P-PZR | Hi/Lo pressurizer P trip |
| `containment_pressure` | P-CONT | High containment P → ESFAS CI |
| `sg_pressure_operating` | P-SG (#21) | MSI on low SG P (E5) |
| `operator_grace_period` | NF-SR + T-CE + L-SG-WR (passive monitoring set) | — |
| `cdf`, `lrf` | derived from PRA, not direct | — |
| `dose_site_boundary` | RAD-SB + plume model | — |
| `cycle_length`, `fuel_burnup_max`, `fuel_enrichment_max` | not real-time (operational) | — |

**Coverage complete:** every safety criterion that is observable in real time maps to ≥ 1 channel. The SG-pressure gap found in the first cross-check is now closed by channel #21 (P-SG), added to the master table above and wired to MSI (E5).

---

## 4. Post-accident monitoring (Reg Guide 1.97) subset

Sensors qualified to survive design-basis accident and provide information for ≥ 72 h passive operation:

| Channel | Type A/B/C/D/E | Survival qualified |
|---|---|---|
| T-CE (core exit T) | Type B (diagnose CSF integrity) | Yes |
| P-PZR | Type B | Yes |
| L-SG-WR | Type B (heat sink integrity) | Yes |
| P-CONT | Type C (barrier integrity) | Yes |
| RAD-CONT | Type C | Yes |
| Radiation: containment H₂ (add — see gaps §5) | Type C | Yes (planned) |
| L-PZR (wide-range) — to add | Type B | Planned |

Categories per RG 1.97 Rev 5:
- **Type A** — operator action info,
- **Type B** — CSF status,
- **Type C** — barrier integrity,
- **Type D** — system status,
- **Type E** — release assessment.

---

## 5. Gaps and additions (revisit Day 3)

| # | Gap | Add | Priority |
|---|---|---|---|
| 1 | No containment H₂ monitor (severe accident) | Add catalytic + thermal-conductivity H₂ monitors, RG 1.97 Type C | High |
| 2 | No pressurizer wide-range level (post-acc) | Add L-PZR-WR, dP, Class 1E | Medium |
| 3 | No boric acid concentration sensor | Add online boron meter (low priority — no boration in passive design?) | Low — TBD with Samira |
| 4 | No coolant activity monitor (online failed fuel detection) | Add primary coolant gamma spec | Low |
| 5 | IRWST level | Add 2-channel level for ECCS source | Medium |

---

## 6. Vendor / domestic sourcing note (FER §5.2 originality / domesticity)

Where possible Aegis-40 sensors should source from **domestic suppliers** to meet FER §5.2 ("domestic content"). Candidates by category (placeholder, confirm with team):
- RTDs / thermocouples — local instrumentation industry baseline.
- Pressure / dP transmitters — domestic process-industry suppliers.
- Neutron detectors, fission chambers — typically imported (specialist); flag as imported in §5.2.
- Radiation monitors — mixed (some domestic options).

Build a sourcing matrix once supply chain is mapped by the team.

---

## 7. References

- IEEE 603-2018 — Standard Criteria for Safety Systems
- IEEE 323 — Qualifying Class 1E equipment
- IEEE 344 — Seismic qualification
- NRC RG 1.97 Rev 5 — Post-accident monitoring instrumentation
- IEC 61513 — I&C systems important to safety
- IEC 60880 — Software for Class 1E systems
- IAEA SSG-39 — Design of I&C for NPPs
- ANSI/ISA 18.2 — Alarm management

---

*End of sensor inventory. 20 channels enumerated + 6 gap additions planned. Length ≈ 4 printed pages.*
