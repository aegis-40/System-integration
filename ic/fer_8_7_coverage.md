# FER §8.7 (and §8.6 I&C-relevant) — line-by-line coverage check

*Purpose: confirm every discrete requirement in FER §8.7 has a specific, sensible answer in our I&C deliverables. Not a tick-box exercise — each row is graded on whether the answer is physically/logically coherent, not just present.*

*Reviewed: 2026-06-02. Owner: Azamhon.*

---

## Legend

- ✓ **fully addressed** — answer present, specific, internally consistent
- △ **partially addressed** — answer present but weak, incomplete, or contradictory
- ✗ **gap** — requirement is unanswered
- 🐞 **defect** — a statement is technically wrong and must be fixed

---

## 1. §8.7 opening — scope statement

> *"Information on the design of the Nuclear Instrumentation and Control (I&C) system, which includes the functions needed to manage the processes required to provide adequate safety under normal conditions and accident conditions in modular reactors, must be presented in this section."*

| Where | Quality | Notes |
|---|---|---|
| `ic_architecture.md` §1 (Scope and purpose) | ✓ | Opens with explicit FER scope language, lists all four functions, names the operating envelope (normal + accident). |

---

## 2. §8.7 — four required I&C functions

> *"These functions include the data and triggers necessary for: (a) mitigation of abnormal operating conditions and fault detection; (b) prevention or mitigation of accidents within design limits and their consequences; (c) prevention of severe accidents or mitigation of their consequences; (d) initiation of systems to mitigate radiological consequences in the event of an accident."*

| # | Function | Data source | Trigger source | Where | ✓ |
|---|---|---|---|---|---|
| 2a | Abnormal op + fault detection | All sensors (`sensor_inventory.md`) | DCS alarms + RPS bistables (`ic_architecture.md` §3.2, §3.4) | ic_architecture.md §1, §3.2, §3.4; DiD level 2 in §2.1 | ✓ |
| 2b | DBA prevention/mitigation within design limits | Safety-grade sensors (14 Class 1E) | RPS trips + ESFAS (`trip_signals.md` §2, §3) | ic_architecture.md §3.2/§3.3; trip_signals.md §2/§3 | ✓ |
| 2c | Severe-accident prevention/mitigation | Same + accident-qualified sensors (`sensor_inventory.md` §4 RG 1.97 set) | DAS + passive ESF latching (`ic_architecture.md` §3.6) | ic_architecture.md §3.6; sensor_inventory.md §4; event_tree_LOHS.md ATWS branch | ✓ |
| 2d | Radiological release mitigation initiation | RAD-CONT, RAD-MSL, RAD-SB | ESFAS (CI, MSI) — `trip_signals.md` E2/E5 | ic_architecture.md §3.3; trip_signals.md §3; safety_criteria.yaml `dose_site_boundary` | ✓ |

**Coherence check:** every function names *both* a data path *and* a trigger path, as the FER explicitly requires ("data **and** triggers"). The four functions also map cleanly to IAEA DiD levels 2/3/4/5 — coherent with safety chapter.

---

## 3. §8.7 — architecture, components, diagrams

> *"The instrumentation and control system architecture of the reactor, main components, subsystems and block, logic and flow diagrams showing the connections between them must be described in this section."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 3a | Architecture description | `ic_architecture.md` §3 (5 layers + DAS) | ✓ |
| 3b | Main components | §3.1–§3.6 enumerated by layer | ✓ |
| 3c | Subsystems | RPS, ESFAS, DCS, DAS, twin — each its own subsection | ✓ |
| 3d | **Block diagram** | `ic_block.mmd` / `ic_block.png` | ✓ |
| 3e | **Logic diagram** | `ic_architecture.md` §7 + `trip_signals.md` §2 (logic encoded as variable→setpoint→voting→actuation table) | △ |
| 3f | **Flow diagram** | Signal flow shown in block diagram (sensor→bus→logic→breaker→CRD); no separate data-flow diagram | △ |
| 3g | Connections between components | Block diagram arrows + cross-reference table in `ic_architecture.md` §9 | ✓ |

**△ on 3e/3f:** the FER literally asks for three diagram types. We have a strong block diagram but the *logic* is rendered as a table, not a schematic, and there's no dedicated *flow* diagram. **Recommended fix:** add one simplified logic schematic — the OTΔT composite trip is the natural candidate (it's the most complex logic) — and consider a small signal-flow diagram showing how a flux reading reaches a trip breaker. ~2 hours of work.

---

## 4. §8.7 — sensors and instruments

> *"The sensors, detectors and instruments to be used to collect data in the system, as well as the software and hardware required for real-time processing of data, must be explained."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 4a | Sensors / detectors / instruments | `sensor_inventory.md` §2 master table (21 channels) | ✓ |
| 4b | Hardware for real-time processing | `ic_architecture.md` §3.2 (FPGA / qualified PLC), §6 EQ | ✓ |
| 4c | Software for real-time processing | `ic_architecture.md` §6.3 (IEC 60880 Cat A for RPS, Cat B for DCS) | ✓ |
| 4d | **Real-time performance characterized** | Not quantified anywhere — no scan-cycle time or response-time target stated | ✗ |

**✗ on 4d:** "real-time" is a property — bounded latency. We name the hardware (FPGA, PLC) and the software category (IEC 60880 Cat A) but never state the RPS response-time target (typical 50–100 ms from sensor threshold crossing to trip-breaker actuation). **Recommended fix:** add one sentence in `ic_architecture.md` §3.2: *"RPS scan + voting + actuation cycle ≤ 100 ms; total signal-to-rod-release ≤ 500 ms."* No design impact, closes the gap.

---

## 5. §8.7 — HMI and secure communications

> *"The design of Human-Machine Interfaces (HMI) and secure communication protocols must be specified."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 5a | HMI design | `ic_architecture.md` §4.1–§4.4 (NUREG-0700, ISA 18.2, soft procedures, hardwired manual) | ✓ |
| 5b | Secure communication protocols | `ic_architecture.md` §5 | △ 🐞 |

**🐞 in 5b — Purdue model levels stated backwards.** Current text says *"RPS/ESFAS = Level 4 isolated; DCS = Level 3; corporate IT = Level 1/2."* The Purdue Model numbering runs **bottom-up**: Level 0 = physical process, Level 1 = basic control / safety, Level 2 = area supervisory, Level 3 = site operations, Level 4 = business planning, Level 5 = enterprise IT. Safety-critical systems live at the **bottom** (Level 0/1), not the top. Our assignment is inverted. **Mandatory fix.** Correct mapping: *"RPS/ESFAS = Level 0/1 (safety-critical, isolated); DCS = Level 2/3; corporate IT = Level 4/5; unidirectional data diodes upward only."*

---

## 6. §8.7 — design criteria and principles

> *"The general design criteria and principles of the instrumentation and control system must be explained, taking into account factors such as critical parameters to be monitored and controlled, safety and operational requirements, redundancy, diversity and physical separation."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 6a | General design criteria | `ic_architecture.md` §2 (six numbered principles) | ✓ |
| 6b | Critical parameters **monitored** | `sensor_inventory.md` §2 + `safety_criteria.yaml` sensor_chain fields | ✓ |
| 6c | Critical parameters **controlled** | `ic_architecture.md` §3.4 enumerates control loops (rod position, pressurizer P/L, FW, turbine, cogen) | △ |
| 6d | Safety requirements | `ic_architecture.md` §2 (single-failure, fail-safe) + `safety_criteria.yaml` | ✓ |
| 6e | Operational requirements | `ic_architecture.md` §3.4 control loops; cogen extraction control mentioned | △ |
| 6f | Redundancy | `ic_architecture.md` §2.2 (4 div, 2/4 voting) | ✓ |
| 6g | Diversity | `ic_architecture.md` §2.3 (RTD vs TC, venturi vs ultrasonic, DAS diverse platform) | ✓ |
| 6h | Physical separation | `ic_architecture.md` §2.4 (IEEE 384, separate trays, rated barriers) | ✓ |

**△ on 6c and 6e:** controlled variables are *mentioned* but not listed as a dedicated table parallel to the sensor inventory. **Recommended fix:** add a small "controlled variables" table in `ic_architecture.md` §3.4 showing each control loop's process variable, manipulated variable, setpoint range, and control mode (PI, PID, three-element). Aligns with the FER's specific demand to list things "monitored **and** controlled."

---

## 7. §8.7 — main control room ergonomics

> *"It must be demonstrated that the main control room panel is designed ergonomically."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 7a | Ergonomic MCR | `ic_architecture.md` §4.1 (NUREG-0700, two-operator console, large overview display panel, sit-stand surfaces, indirect lighting, sound treatment, emergency lighting, STA station) | ✓ |

**Coherence check:** §4.1 names a credible HFE basis (NUREG-0700) and gives concrete design features. Doesn't claim a specific operator-workload study — fine for FER conceptual design level.

---

## 8. §8.6 — protective action derivation (the I&C bridge)

> *"How the parameters required to initiate reactor protective actions are derived from monitored variables such as neutron flux, temperature and flow, and how they are logically combined, must be demonstrated with schematic diagrams."*

| # | Requirement | Where | ✓ |
|---|---|---|---|
| 8a | Derivation explained | `ic_architecture.md` §7 (monitored-variable → derived-parameter → action table) | ✓ |
| 8b | Logical combination shown | `trip_signals.md` §2 (per-trip variable, setpoint, voting) | ✓ |
| 8c | **Schematic diagram** of derivation | `ic_block.png` block diagram | △ |

**△ on 8c:** the §8.6 request is for a *schematic* showing the logical combination, not just a tabular description. The block diagram shows architecture; it does *not* show, for example, *"OTΔT trip = f(Thot − Tcold, P, axial offset, flux) > setpoint"* as a logic schematic. **Recommended fix:** the same OTΔT logic schematic flagged under §8.7 item 3e also closes this — kill two birds.

---

## 9. §8.6 related — automatic actuation + fail-safe + reactivity envelope

These §8.6 sentences are formally outside §8.7 but are answered by the I&C deliverables, so they belong in this coverage map.

| Requirement | Where | ✓ |
|---|---|---|
| Auto-actuation of appropriate systems on accident detection | `trip_signals.md` §3 ESFAS (E1–E5, all latching auto-init) | ✓ |
| Transition to safe state on loss of power/signal/air | `ic_architecture.md` §2.6 (de-energize-to-trip principle) | ✓ |
| Reactivity-control trip envelope | `trip_signals.md` Trip 3 (high flux rate) + Trip 1/2 (high flux) | ✓ |

---

## 10. Coverage summary

| Status | Count |
|---|---|
| ✓ fully addressed | **20** |
| △ partially addressed | **5** |
| ✗ gap | **0** |
| 🐞 defect to fix | **0** |
| **Total requirements** | **25** |

*Updated 2026-06-02 after F1 + F2 applied.*

---

## 11. Fix list (recommended actions, prioritized)

| # | Severity | Item | File | Effort |
|---|---|---|---|---|
| F1 | ✓ DONE | Purdue model levels corrected to bottom-up (RPS = Level 0/1, IT = Level 4/5) — `ic_architecture.md` §5 | applied 2026-06-02 | — |
| F2 | ✓ DONE | RPS scan ≤ 100 ms / signal-to-rod-release ≤ 500 ms added to §3.2 | applied 2026-06-02 | — |
| F3 | △ enhance | Add OTΔT logic schematic (handles both FER §8.7 item 3e *and* §8.6 item 8c) | new `ic/ic_logic_otdt.mmd` | 1 h |
| F4 | △ enhance | Add a "controlled variables" table parallel to the sensor inventory | `ic_architecture.md` §3.4 | 30 min |
| F5 | △ enhance | Optional: a small data-flow diagram (sensor → bistable → vote → breaker) for the "flow diagram" leg | new `ic/ic_signal_flow.mmd` | 1 h |

**F1 must be fixed** — it's technically wrong and any reviewer with OT-cybersecurity background will spot it. F2 closes the only real gap. F3 doubles up for FER §8.7 and §8.6. F4 and F5 are quality polish.

---

## 12. Sense-check — does the answer set hold together?

A few coherence cross-checks beyond the requirement-by-requirement view:

- **No circular dependencies.** RPS doesn't read from DCS; DCS doesn't read from twin; twin doesn't read from anywhere safety. Tree flows one way. ✓
- **No orphan components.** Every layer in the block diagram is described in `ic_architecture.md` (after DAS was added in §3.6) and references a sensor or function. ✓
- **No double-counting of redundancy claims.** "Four divisions + 2/4 voting" is stated once in §2.2 and applied consistently in §3.2 and `trip_signals.md`. No drift. ✓
- **HMI hardwired manual ≠ software-dependent.** §4.4 explicitly carves out manual scram/SI/CI/EFW/MSIV as non-software. Consistent with the IEEE 603 §5.8 citation. ✓
- **Cyber-security argument** (after F1 fix): one-way data diodes upward only; no remote login to safety; firmware updates only in cold shutdown; matches NRC RG 5.71. ✓
- **Sensor → trip → safety-limit closure.** Verified in the W1 audit (every hard limit either has a trip or a documented design-protection note). ✓

The architecture is *internally consistent*. The five remaining items in §11 are presentation/completeness fixes, not structural problems.

---

*End of coverage check. Cross-references: `ic_architecture.md`, `ic_block.png`, `sensor_inventory.md`, `safety/trip_signals.md`, `safety/safety_criteria.yaml`, FER `Final_Template.docx` §8.6 + §8.7.*
