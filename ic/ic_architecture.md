# I&C Architecture — Aegis-40

*Source document. Drop into FER §8.7 (Instrumentation and Control System Design).*
*Companion files: `sensor_inventory.md`, `ic_block.mmd` (Wed), `trip_signals.md` (Thu).*
*Owner: Azamhon. Last updated: 2026-05-27.*

---

## 1. Scope and purpose

This document describes the Aegis-40 Instrumentation & Control (I&C) system: its design principles, architectural layers, sensor inventory, and how monitored variables are logically combined to initiate protective actions. The I&C system fulfils the FER §8.7 requirement to provide the **functions needed to manage processes under normal and accident conditions**, including:

- mitigation of abnormal operating conditions and fault detection,
- prevention or mitigation of design-basis accidents,
- prevention of severe accidents or mitigation of their consequences,
- initiation of systems to mitigate radiological consequences after an accident.

The architecture follows defense-in-depth (IAEA SSR-2/1 Rev 1 §2.13) and applies it to the I&C functions per IAEA SSG-39 and IEC 61513.

---

## 2. Design principles

The I&C system rests on six principles, each traceable to a specific standard. Every architectural decision below cites which principle it satisfies.

### 2.1 Defense in depth (DiD) — IAEA SSG-39, IEC 61513
I&C functions are partitioned across five DiD levels to avoid common-cause failure between control and protection:

| DiD level | I&C function | System |
|---|---|---|
| 1 | Normal operation control | DCS (Distributed Control System) |
| 2 | Operational limitation / anticipatory control | Limitation system (sub-set of DCS, non-safety) |
| 3 | Protection — initiate safety actions on design-basis events | RPS + ESFAS (Class 1E) |
| 4 | Severe accident monitoring + diverse actuation | Diverse Actuation System (DAS) + post-accident monitoring |
| 5 | Emergency response support | Emergency Response Facility I&C |

The Aegis-40 design twins the DCS with a **digital monitoring layer** (non-safety, read-only) for predictive maintenance and condition-based diagnostics. It cannot actuate any safety function.

### 2.2 Redundancy — IEEE 603 §5.1
Safety-critical channels (neutron flux, hot-leg T, primary pressure, primary flow, SG level, containment P) are 4-fold redundant with 2-of-4 voting logic. This survives single failure plus one out-of-service channel and satisfies the **single-failure criterion** under maintenance.

### 2.3 Diversity — IEEE 603 §5.16, NRC SECY-93-087
Same physical parameter is measured by **different sensor technologies** where feasible: RTDs and thermocouples for temperature; ion chambers and fission chambers for neutron flux; venturi and ultrasonic flow meters for primary flow. Diversity guards against common-cause failures in sensor technology, model, or vendor.

### 2.4 Physical separation — IEEE 384, IEEE 603 §5.6
Class 1E channels are physically separated by Class 1E-rated barriers (typically 18 inches or fire-rated wall) and routed through separate cable trays. No Class 1E and non-Class 1E circuit share a tray or penetration unless qualified isolation devices are interposed.

### 2.5 Single-failure criterion — IEEE 603 §5.1
No single failure (mechanical, electrical, environmental, software, or human) shall prevent the safety functions from being performed. The 2-of-4 voting + four redundant trains satisfies this for both:
- **trip** failure: 1 channel failed in safe direction → still trips on 2-of-3
- **trip-prevention** failure: 1 channel failed in unsafe direction → still trips on 2-of-3

### 2.6 Fail-safe — IEC 61513 §5.3.6 ("de-energize-to-trip")
The RPS trip breakers are **normally energized**. Loss of electrical power, instrument air, or signal to the trip system causes immediate scram. Fail-safe extends to ESFAS-actuated passive systems: loss of power causes them to actuate.

This satisfies FER §8.6 explicit requirement: *"safety features must … transition to a safe state when conditions such as loss of system connection, loss of energy (electrical power, instrument air) … are experienced."*

---

## 3. Architecture overview — five layers

```
  ┌─────────────────────────────────────────────────────────────┐
  │  LAYER 5 — Digital twin / advisory                           │  non-safety
  │  Soft sensors · Anomaly detection · Predictive maintenance   │  read-only
  ├─────────────────────────────────────────────────────────────┤
  │  LAYER 4 — DCS (Distributed Control System)                  │  non-safety
  │  Control loops · Operator HMI · Alarms · Data historian      │
  ├─────────────────────────────────────────────────────────────┤
  │  LAYER 3 — ESFAS (Engineered Safety Features Actuation)      │  CLASS 1E
  │  Passive SI · Containment isolation · EFW · PRHR/PCCS        │
  ├─────────────────────────────────────────────────────────────┤
  │  LAYER 2 — RPS (Reactor Protection System)                   │  CLASS 1E
  │  2-of-4 voting · Trip breakers · CRD scram                   │
  ├─────────────────────────────────────────────────────────────┤
  │  LAYER 1 — Field instrumentation                             │  CLASS 1E for safety,
  │  Sensors: N, T, P, F, L, radiation · Transmitters · Cabling  │  non-1E for control-only
  └─────────────────────────────────────────────────────────────┘
                          ⇅ signals
                          ⇅ no upward path from L4/L5 to L2/L3
```

**Key rule (FER §8.7 + IEEE 603):** information flows **upward** (sensors → control → operator). The RPS and ESFAS receive sensor signals directly from Layer 1, never from the DCS or digital twin. There is **no software path** from the non-safety layers to the safety layers — actuation can only originate from Layer 2/3 logic.

### 3.1 Layer 1 — Field instrumentation
21 measurement channels (14 Class 1E, 7 non-1E) plus 5 planned additions, covering neutronic, thermal-hydraulic, pressure, level, and radiological variables. Specified in detail in [`sensor_inventory.md`](sensor_inventory.md).

Highlights:
- **Neutron flux** in three overlapping ranges: source (1 – 1e6 cps), intermediate (1e-8 – 1e-3 A), power (0 – 125 %). Continuous coverage from shutdown through 25 % overpower.
- **Temperature**: hot-leg RTDs + core-exit thermocouples (diverse). Cold-leg RTDs for ΔT calculation.
- **Pressure**: pressurizer 4-fold, containment 4-fold.
- **Flow**: venturi primary + ultrasonic backup.
- **Level**: SG narrow-range (control) + wide-range (post-accident).
- **Radiation**: containment + site boundary + main steam line.

### 3.2 Layer 2 — Reactor Protection System (RPS)
Class 1E, hardwired, four redundant divisions A/B/C/D. Each division processes its own sensor signal independently through:
- signal conditioning,
- setpoint comparator,
- bistable trip logic (variable exceeds setpoint),
- voter coincidence (2-of-4 across divisions).

Trip output drives **reactor trip breakers** that interrupt power to the Control Rod Drive Mechanisms (CRDMs). CRDM holding coils de-energize and rods fall by gravity. This is the primary scram path. Trip signals enumerated in `trip_signals.md` (Day 4).

The RPS is implemented in **safety-qualified hardware** (FPGA or qualified PLC per IEC 60880); software development follows IEC 60880 Cat A. The system is real-time deterministic: **scan + voting cycle ≤ 100 ms** per division, **total sensor-threshold-crossing → trip-breaker-open latency ≤ 500 ms**, bounding the time available for the safety analysis to assume protective action.

### 3.3 Layer 3 — Engineered Safety Features Actuation System (ESFAS)
Class 1E, also 4-train. Same sensor inputs as RPS but evaluates a different set of conditions to actuate **passive** safety systems:

| ESFAS function | Initiating condition | Actuates |
|---|---|---|
| Safety Injection (SI) | Low pressurizer P + low pressurizer level | Passive SI tanks (gravity feed) |
| Containment Isolation (CI) | High containment P OR high containment radiation | All non-essential containment penetrations close |
| Emergency Feedwater (EFW) | Low SG level OR loss of normal FW | Gravity-driven feedwater from elevated tank (passive — isolation valves open, no pumps) |
| PRHR / PCCS | Low SG level + EFW unavailable OR high core exit T post-scram | Passive Residual Heat Removal HX aligned to IRWST |
| Main Steam Isolation (MSI) | High steam line radiation OR high containment P | MSIVs close |
| Emergency Boron Injection (EBIS) | ATWS signature (high flux/T + no rod insertion) — **DAS only** | Passive borated-water injection (shutdown system #2) |

ESFAS uses the same 2-of-4 voting model as RPS. Actuation is **latching** — once initiated, operator must consciously reset; not auto-cleared by signal recovery.

### 3.4 Layer 4 — Distributed Control System (DCS)
Non-safety. Closed control loops for plant operation in the design envelope:

- **Reactor power control:** modulates control rod position (gray rods for fine control + black rods for coarse). Uses T_avg and flux as process variables.
- **Pressurizer P + level control:** heaters / sprays + charging / letdown.
- **Feedwater control:** three-element control (SG level, steam flow, FW flow).
- **Turbine control:** load-following + frequency response.
- **Cogeneration extraction control:** steam diversion to TES (district heat) and SOE (H₂) per dispatch.

The DCS communicates with the RPS / ESFAS through **qualified one-way isolation devices** (fiber optic with no reverse channel, or analog isolators). The DCS receives sensor data via dedicated taps off the RPS sensor circuits **downstream** of the safety bistable — so a DCS fault cannot corrupt the RPS signal.

### 3.5 Layer 5 — Digital twin / advisory monitoring
Non-safety, advisory only. Mirrors all Layer 1 signals into a real-time digital twin of the plant. Functions:

- **Soft sensors:** infer unobservable quantities (fuel centerline T, MDNBR, hot channel factor) from observable signals + physics model. Used by operators for situational awareness.
- **Anomaly detection:** machine-learning model flags out-of-pattern signal behavior before alarm thresholds trip.
- **Predictive maintenance:** identifies degrading sensors, pumps, valves before failure.
- **Post-event reconstruction:** stores high-frequency data for forensic analysis.

The digital twin **cannot actuate any device** and **does not feed the DCS control loops**. It is a parallel observer. Outputs are displayed to the operator as advisory information on the HMI alongside (not in place of) the qualified instrumentation.

This layer is a **TEKNOFEST originality lever** for FER §5 (originality / innovation): the digital twin enables condition-based maintenance and operator decision support without compromising safety qualification of the underlying I&C.

### 3.6 Diverse Actuation System (DAS)
Class 1E but **technologically diverse** from the RPS/ESFAS — implemented on a different platform (e.g. FPGA where RPS uses qualified PLC, or vice-versa), by a different design team, to defeat **common-cause software failure** (CCF) of the primary protection system. Required by NRC SECY-93-087 / BTP 7-19 and IAEA SSG-39 §6 for digital protection systems.

The DAS independently monitors a reduced set of the most safety-significant variables — power-range neutron flux, pressurizer pressure, and core-exit temperature with control-rod-bottom confirmation (see `sensor_inventory.md`) — and provides a **diverse backup** path to:
- trip the reactor (independent signal to the trip breakers), and
- actuate the key passive ESF functions (SI, PRHR), and
- **actuate the Emergency Boron Injection System (EBIS)** — shutdown system #2 — on an ATWS signature (high flux/temperature **with no rod insertion confirmed**). EBIS is the diverse, independent second means of shutdown required by IAEA SSR-2/1 Req 46 §6.9 in this soluble-boron-free core; the DAS is its sole actuation path (see `safety/trip_signals.md` E6).

The DAS is **not** part of the layered DiD control hierarchy (Layers 1–5); it is a parallel safety-grade subsystem whose sole purpose is to cover a postulated CCF that disables all four RPS divisions simultaneously. It uses simpler, fixed, hardware-biased logic to minimize shared failure modes with the RPS software. Its actuation thresholds are set slightly beyond the RPS setpoints so the RPS acts first under normal demand, with the DAS as backstop.

---

## 4. Human-Machine Interface (HMI) and Main Control Room

### 4.1 MCR layout principles (FER §8.7 explicit requirement)
Two-operator minimum. Ergonomic layout per NUREG-0700 (HFE design guidelines):

- **Primary console:** reactor operator. Touch-screen + hardwired switches for safety-significant actions (manual scram, ESFAS actuation, MSIV close).
- **Secondary console:** turbine / balance-of-plant operator.
- **Shift Technical Advisor (STA) station:** read-only mirror with diagnostic tools.
- **Large overview display panel:** 4 × 80" screens showing plant mimic, alarm overview, safety parameter display system (SPDS), critical safety functions (CSFs).
- **Sit-stand work surfaces;** indirect lighting; sound-treated walls; emergency lighting on uninterruptible power.

### 4.2 Alarm philosophy — ISA 18.2
Three-tier alarm hierarchy:
1. **Emergency (red, audible):** operator action required within 10 min.
2. **High (amber, audible):** operator action required within 30 min.
3. **Diagnostic (yellow, silent):** advisory only.

Cap on simultaneous alarms: **≤ 10 in any 10-minute window** under design-basis transients. Alarm rationalization done before commissioning.

### 4.3 Soft procedures + paper backup
Critical Safety Function trees, EOPs, and AOPs available as:
- **Computer-based procedures** with step interlocks and plant-data-aware prompts;
- **Paper backup** in MCR cabinet for any single-point software failure.

### 4.4 Hardwired safety controls
Despite digital I&C throughout, the following operator actions remain **hardwired** (non-software):
- Manual reactor trip,
- Manual ESFAS actuation (SI, CI, EFW, PRHR),
- Manual MSIV closure.

Per IEEE 603 §5.8, manual initiation must be independent of computer health.

### 4.5 Supplementary control room / Remote Shutdown Station (RSS)

Per IAEA SSR-2/1 Req 65–66, a **Remote Shutdown Station** is provided, physically and
electrically separated from the MCR (different fire area, independent cabling and 1E power
division), able to bring the plant to and maintain **safe shutdown** if the MCR becomes
uninhabitable (fire, smoke, toxic gas, sabotage). Because Aegis-40 is passively safe for
≥72 h with no operator action (§8.6), the RSS scope is deliberately minimal:

- **Post-accident monitoring** of the critical safety-function variables (neutron flux,
  core-exit T, pressurizer P, SG/IRWST level, containment P/radiation) per RG 1.97;
- **Diverse manual reactor trip** and **manual ESF actuation** (SI, EFW/PRHR alignment,
  containment isolation, **EBIS**) on hardwired controls independent of the MCR;
- confirmation of shutdown-system status (rod-bottom + EBIS).

The RSS does not need full control capability — it only has to confirm the passive systems
have actuated and provide a diverse manual backstop. It shares no cabling, HVAC, or power
division with the MCR so that a single MCR-disabling event cannot also disable it.

---

## 5. Secure communication and cybersecurity

Per FER §8.7 ("secure communication protocols") and 10 CFR 73.54:

- **Network segmentation:** Purdue Model zones, numbered bottom-up. RPS / ESFAS at **Level 0/1** (safety-critical, physically and electrically isolated); DCS at **Level 2/3** (site operations); corporate IT at **Level 4/5** (business / enterprise). **Unidirectional data diodes** carry signals only upward (Level 1 → 2, Level 3 → 4); no command path runs downward into safety.
- **No wireless** in safety-related areas.
- **No remote login** to RPS / ESFAS — onsite physical access only.
- **Firmware integrity:** cryptographic signature verification on safety-system firmware updates; updates performed only in cold shutdown.
- **Audit logging:** all DCS/HMI actions logged to write-once media.
- **Periodic vulnerability assessment** + cyber-incident response plan per NRC RG 5.71.

---

## 6. Equipment qualification

### 6.1 Environmental qualification (EQ) — IEEE 323
Class 1E sensors and cabling rated for the worst-case environment they could see post-accident:
- temperature up to 150 °C, pressure up to 0.5 MPa, 100 % steam, radiation up to 1 MGy lifetime,
- LOCA jet impingement where exposed.

### 6.2 Seismic qualification — IEEE 344
Class 1E I&C qualified to SSE (0.3 g per `safety_criteria.yaml`). Demonstrated by tri-axial shake-table test or analysis per IEEE 344.

### 6.3 Software qualification — IEC 60880, IEEE 7-4.3.2
- RPS / ESFAS software: **IEC 60880 Category A** — formal V&V, independent verification, no use of features deemed unsuitable (dynamic memory allocation, recursion, dynamic linking).
- DCS software: **IEC 62138 Category B**.
- Digital twin software: **Category C** (informational only).

---

## 7. Connections to monitored variables — protective action derivation

FER §8.7 requires explicit demonstration of "how the parameters required to initiate reactor protective actions are derived from monitored variables such as neutron flux, temperature and flow, and how they are logically combined."

This is illustrated by the block diagram (`ic_block.mmd`, Day 3) and the trip signal logic table (`trip_signals.md`, Day 4). Summary mapping:

| Monitored variable | Derived parameter | Protective action |
|---|---|---|
| Neutron flux (power range) | Flux > 118 % rated | Reactor trip |
| Neutron flux (power range) | dΦ/dt > 5 %/s | Reactor trip |
| T_hot, T_cold, flux, P | Overtemperature ΔT composite | Reactor trip |
| T_hot, T_cold | Overpower ΔT composite | Reactor trip |
| Primary flow | Flow < 90 % rated | Reactor trip |
| Pressurizer P | P > 16.5 MPa | Reactor trip + PORV |
| Pressurizer P | P < 12.5 MPa | Reactor trip + SI |
| SG level | Level < 15 % NR | Reactor trip + EFW + PRHR |
| Containment P | P > 0.17 MPa | Reactor trip + CI |
| Containment radiation | Activity > 100 × bkg | CI + ventilation isolation |

Each derived parameter is computed by **identical algorithms in all four RPS divisions**; the 2-of-4 voter compares the four independent bistable outputs.

---

## 8. Standards and codes — complete reference list

**General I&C:**
- IAEA SSG-39 — Design of I&C systems for NPPs
- IAEA SSG-30 — Safety Classification of SSCs
- IEC 61513 — I&C systems important to safety, general requirements
- IEEE 603 — Standard Criteria for Safety Systems
- IEEE 7-4.3.2 — Digital computers in safety systems

**Software for safety systems:**
- IEC 60880 — Category A (RPS, ESFAS)
- IEC 62138 — Category B / C (DCS, advisory)
- NRC RG 1.152 — Criteria for safety-related digital computers

**Sensor / equipment qualification:**
- IEEE 323 — Environmental qualification
- IEEE 344 — Seismic qualification
- IEEE 384 — Independence and physical separation

**Human factors:**
- NUREG-0700 — HFE design guideline
- NUREG-0711 — HFE program review model
- ISA 18.2 — Alarm management

**Cybersecurity:**
- 10 CFR 73.54 — Cyber security for nuclear facilities
- NRC RG 5.71 — Cyber security program

**Regulatory baseline:**
- 10 CFR 50 Appendix A — General Design Criteria 13, 19, 20, 21, 22, 23, 24
- IAEA SSR-2/1 Rev 1 Requirement 59 — Protection system

---

## 9. Cross-references inside Aegis-40 documents

| This document references | Where it lives |
|---|---|
| Sensor channel inventory | `ic/sensor_inventory.md` (Day 2 — adjacent) |
| Trip setpoints + voting logic | `safety/trip_signals.md` (Day 4) |
| Block diagram | `ic/ic_block.mmd` + PNG (Day 3) |
| Safety limits trips protect | `safety/safety_criteria.yaml` |
| Event tree showing I&C in LOHS | `safety/event_tree_LOHS.md` (Day 4) |
| FOM I&C-relevant parameters | `fom/fom_inputs.yaml` (Day 5) |
| Standards / IAEA citation list | This document §8 |

---

*End of I&C architecture document. Drop-in candidate for FER §8.7. Length expected ≈ 8 printed pages in Arial 12 / 1.15 line spacing.*
