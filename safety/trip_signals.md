# Reactor Trip & ESF Actuation Signals — Aegis-40

*Source document. Drop into FER §8.6 (protective actions) + §8.7 (logic combination of monitored variables).*
*Companion: `safety_criteria.yaml` (limits each trip protects), `ic/sensor_inventory.md` (sensor channels), `ic/ic_block.mmd` (logic paths).*
*Owner: Azamhon. Last updated: 2026-06-15.*

> **Setpoint status:** all setpoints below are **preliminary engineering values**. Final values depend on OpenMC (flux, reactivity, peaking) and OpenFOAM (DNB, hot-channel T, flow). Each row tagged `[SIM-PENDING]` where a simulation result will replace the placeholder. The *logic, voting, and actuated devices* are design-frozen; only the *numbers* move.

---

## 1. Convention

- **Voting** `m/n` = m-of-n coincidence across redundant divisions (e.g. 2/4).
- **Fail-safe** = behavior on loss of power/signal/air. All RPS trips are **de-energize-to-trip** (loss → trip). ESF actuations are de-energize-to-actuate where the safety function is fail-to-safe.
- **Permissive** = an interlock that enables or blocks a trip depending on plant state (prevents spurious trips at low power / during startup). Defined in §4.
- **Basis limit** = the row ID in `safety_criteria.yaml` this trip protects.

---

## 2. Reactor trip signals (RPS → control rod scram)

| # | Trip ID | Monitored variable | Setpoint | Voting | Sensor (inventory) | Basis limit | Permissive | Also actuates |
|---|---|---|---|---|---|---|---|---|
| 1 | `high_flux_trip` | Power-range neutron flux | 118 % rated `[SIM-PENDING]` | 2/4 | NF-PR (#3) | `k_eff_operating` | Blocked < P-10 | — |
| 2 | `high_flux_trip_lo` | Power-range flux (low setpoint, startup) | 25 % rated | 2/4 | NF-PR (#3) | `k_eff_operating` | Enabled < P-10, auto-removed > P-10 | — |
| 3 | `high_flux_rate_trip` | Intermediate-range flux rate | +5 % rated/s (≈ +0.5 decade/s) | 1/2 | NF-IR (#2) | `max_reactivity_insertion_rate` | Blocked > P-6 | — |
| 4 | `source_range_trip` | Source-range flux | 1e5 cps | 1/2 | NF-SR (#1) | shutdown integrity | Blocked > P-6 | — |
| 5 | `over_temp_dt_trip` | OTΔT composite (Thot−Tcold, f(flux, P, axial)) | composite `[SIM-PENDING]` | 2/4 | T-HL (#4), T-CL (#5), NF-PR, P-PZR | `mdnbr_transient` | — | — |
| 6 | `over_power_dt_trip` | OPΔT composite (Thot−Tcold, f(rate)) | composite `[SIM-PENDING]` | 2/4 | T-HL (#4), T-CL (#5) | `fuel_centerline_temperature` | — | — |
| 7 | `high_outlet_t_trip` | Core exit / hot-leg temperature | 312 °C `[SIM-PENDING]` | 2/4 | T-HL (#4), T-CE (#6) | `pct_loca` | — | — |
| 8 | `low_flow_trip` | Primary loop flow | 90 % rated | 2/4 per loop | F-LP (#8) | `mdnbr_steady` | Blocked < P-7 | — |
| 9 | `high_pressurizer_p_trip` | Pressurizer pressure (high) | 16.5 MPa | 2/4 | P-PZR (#7) | `primary_pressure_design` | — | PORV open |
| 10 | `low_pressurizer_p_trip` | Pressurizer pressure (low) | 12.5 MPa | 2/4 | P-PZR (#7) | `primary_pressure_design` | Blocked < P-7 (startup) | Safety Injection (SI) |
| 11 | `low_sg_level_trip` | SG narrow-range level | 15 % NR | 2/4 per SG | L-SG-NR (#10) | heat-sink integrity | — | EFW start, PRHR align |
| 12 | `high_containment_p_trip` | Containment pressure | 0.17 MPa | 2/3 | P-CONT (#12) | `containment_pressure` | — | Containment Isolation (CI), SI |
| 13 | `manual_scram` | Operator action | — | 1/2 (two switches) | hardwired | all | none | — |

**Notes:**
- Trips 1–2: dual-setpoint flux. Low setpoint (25 %) active during startup, automatically swapped for the 118 % setpoint above permissive P-10. Prevents overpower during low-power physics testing.
- Trip 5 (OTΔT) is the primary **DNB protection** trip — composite function of ΔT, pressure, axial offset, and flux. The setpoint is a *line* in the T-P plane, not a single number; full form derived once OpenFOAM gives the DNB correlation margin.
- Trip 6 (OPΔT) protects the **linear heat rate / centerline** limit — guards against power peaking.
- Trips 9/10: pressurizer pressure has both high and low trips; high also lifts the PORV, low also fires SI (small-break LOCA signature).

---

## 3. ESF actuation signals (ESFAS → passive safety features)

| # | ESF function | Initiating condition | Voting | Sensor | Actuates | Latching |
|---|---|---|---|---|---|---|
| E1 | Safety Injection (SI) | Low pressurizer P < 12.5 MPa **OR** low pressurizer level + high containment P | 2/4 | P-PZR (#7), L-PZR, P-CONT (#12) | Passive SI tanks (gravity/accumulator) | Yes |
| E2 | Containment Isolation (CI) | High containment P > 0.17 MPa **OR** high containment radiation | 2/3 | P-CONT (#12), RAD-CONT (#13) | Close all non-essential containment penetrations | Yes |
| E3 | Emergency Feedwater (EFW) | Low SG level < 15 % **OR** loss of normal feedwater | 2/4 | L-SG-NR (#10) | Gravity feed from elevated tank (no pumps) | Yes |
| E4 | PRHR / PCCS | Low SG level + EFW unavailable **OR** high core-exit T post-scram | 2/4 | L-SG-NR (#10), T-CE (#6) | Passive Residual Heat Removal HX → IRWST | Yes |
| E5 | Main Steam Isolation (MSI) | Low SG pressure (steam-line-break signature) **OR** high steam-line radiation **OR** high containment P | 2/4 (P-SG), 2/3 (RAD/P-CONT) | P-SG (#21), RAD-MSL (#14), P-CONT (#12) | Close MSIVs | Yes |
| E6 | **Emergency Boron Injection (EBIS)** — diverse shutdown system #2 (`ebis_actuation`) | **ATWS signature**: high flux/high core-exit T **AND** no rod insertion confirmed (rod-bottom not reached after trip demand) — issued by the **DAS** | 2/4 (flux/T) + rod-position confirm | NF-PR (#3), T-CE (#6), CRD rod-bottom switches | Passive borated-water injection (gravity/N₂ accumulator; fail-open isolation valves) | Yes |

**Latching:** every ESF actuation is latching — once initiated it stays actuated until the operator consciously resets. It does **not** auto-clear when the initiating signal recovers. This prevents a flickering signal from cycling a safety system.

---

## 4. Permissives and interlocks

Permissives prevent spurious trips during startup/low-power and are auto-managed by the RPS.

| Permissive | Derived from | Threshold | Effect |
|---|---|---|---|
| P-6 | Intermediate-range flux | ≈ 1e-10 A (above source range) | Above: block source-range + flux-rate trips, allow rod withdrawal |
| P-7 | Power-range flux **OR** turbine first-stage P | 10 % power | Below: block low-flow and low-pressurizer-P trips (no DNB risk at low power) |
| P-8 | Power-range flux | 48 % power | Above: low-flow trip on single-loop loss enabled |
| P-10 | Power-range flux | 10 % power | Above: swap low (25 %) flux setpoint → high (118 %); block intermediate-range trip |

**Design rule:** permissives may only *block low-power trips that have no safety basis at that state*. They can never block a trip that protects an active design-basis limit. All permissive logic is itself Class 1E and 2/4-voted.

---

## 5. Trip → safety-limit traceability (closes the loop with Day 1)

Every reactor trip maps back to a `safety_criteria.yaml` row. Reverse check — every *hard* limit that is trip-protectable has a trip:

| `safety_criteria.yaml` row | Type | Protected by |
|---|---|---|
| `k_eff_operating` | operating | Trips 1, 2 (high flux) |
| `max_reactivity_insertion_rate` | hard | Trip 3 (flux rate) |
| `mdnbr_steady` | hard | Trip 8 (low flow) |
| `mdnbr_transient` | hard | Trip 5 (OTΔT) |
| `pct_loca` | hard | Trip 7 (high outlet T) + E1 (SI) |
| `fuel_centerline_temperature` | hard | Trip 6 (OPΔT) |
| `primary_pressure_design` | hard | Trips 9, 10 (pressurizer P) |
| `containment_pressure` | hard | Trip 12 + E2 (CI) |
| `shutdown_margin` | hard | **design** (rod worth) — see §6 |
| `independent_shutdown_systems` | hard | **design**: #1 rods + #2 EBIS (E6) — see §6 |
| `mtc/dtc/void` | hard | **inherent** (physics, no trip) — DBE *prevention* |
| `prhr_capacity` | hard | E4 (PRHR) |

Limits with **no trip** are protected by design or inherent physics, not by an action — documented so a reviewer sees the omission is deliberate, not a gap.

---

## 6. Soluble-boron status `[RESOLVED 2026-06-15]` + the two shutdown systems

Aegis-40 is **soluble-boron-free for reactivity control** — the normal-operation coolant carries no boron (Samira's `materials.xml` = pure-water moderator), so boron-dilution accidents stay eliminated and the MTC stays strongly negative. SDM in normal operation comes from rods + fixed Gd/Er burnable absorber.

To satisfy **SSR-2/1 Req 46 §6.9 (two diverse and independent shutdown systems)**, Aegis-40 provides:

1. **Shutdown system #1 — control rods.** Gravity-drop on de-energization (RPS or DAS path). Cold stuck-rod SDM = 12.4 %. Protects `shutdown_margin`, `independent_shutdown_systems`.
2. **Shutdown system #2 — Emergency Boron Injection System (EBIS)** (`ebis_actuation`, ESF E6). A **passive, diverse, shutdown-only** borated-water system, **isolated and dormant in normal operation**, armed only on an ATWS signature by the **DAS**. Diverse from #1 in physical principle (chemical poison vs mechanical insertion) → does **not** share the rod-insertion common-cause failure mode (§6.8). Sized so it ALONE holds the core cold-subcritical at the most-reactive condition (§6.10) — `[SIM-PENDING — OpenMC borated-core case, Samira]`.

This is the diverse second shutdown system; the DAS provides diverse *actuation* of **both** #1 (rods) and #2 (EBIS). The LOHS event-tree ATWS branch now credits EBIS as the diverse-shutdown success path. See `safety/safety_criteria.yaml` `independent_shutdown_systems` + `open_item: shutdown_second_system`.

---

## 7. References

- IEEE 603 — Safety system criteria (voting, single failure)
- IEC 61513 — I&C systems important to safety
- NUREG-0800 SRP 7.2 — Reactor trip system
- NUREG-0800 SRP 7.3 — ESFAS
- 10 CFR 50 App A GDC-20/21/22/23/25 — protection system requirements
- IAEA SSR-2/1 Rev 1 Req 59, 67 — protection + actuation systems
- Westinghouse permissive scheme (P-6…P-10) as reference architecture

---

*End of trip signals. 13 reactor trips + 6 ESF actuations (incl. EBIS diverse shutdown) + 4 permissives, all traced to Day-1 limits. Length ≈ 3 printed pages.*
