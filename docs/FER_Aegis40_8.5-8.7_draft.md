# FER Draft — Aegis-40 — §8.5 Safety Criteria · §8.6 Safety Systems & Accident Analysis · §8.7 Instrumentation & Control

*Draft r1, 2026-06-13. Companion to the team's `FER_Aegis40_8.8-8.10.docx` (§8.8–8.10);
together these cover all System-integration sections of Chapter 8. Sections not worked
in this scope (§8.1–8.4, §8.9, §8.11) are intentionally absent.*

*Marker convention — these are explicit and must all be resolved or accepted before
submission:*
- ***[SIM-PENDING — …]*** *value awaits a simulation that is scoped but not yet run*
- ***[ANALYSIS-PENDING — …]*** *analysis identified, not yet performed*
- ***[VERIFY — …]*** *claim believed correct but lacking a citable anchor*
- ***[DECISION-PENDING — …]*** *team decision still open; text written against the stated baseline*

---

## 8.5 Safety Criteria

### 8.5.1 Criteria framework

The Aegis-40 safety basis is expressed as **27 numeric criteria in seven categories**
(reactivity/neutronics, thermal-hydraulics, pressure boundary, decay-heat removal,
radiological/site, seismic, fuel cycle), maintained as a machine-readable single
source of truth (`safety_criteria.yaml`) from which the protection-system setpoints
(§8.7) and the figure-of-merit hard constraints are derived. Each criterion is
classified as a **hard constraint** (breach disqualifies the design — pass/fail,
never traded), an **operating limit** (breach demands protective action), or a
**target** (scored against reference SMRs: CAREM-25, SMART, NuScale VOYGR). Every
criterion carries its regulatory source and, where protective action is required,
the crediting trip function [SSR-2/1; NUREG-0800].

### 8.5.2 Principal criteria and demonstrated margins

Table 8.5-1 presents the principal criteria with the values demonstrated by the
locked core design (OpenMC rev_3, 21-assembly 17×17 core, three-zone 4.95/4.70/4.40
wt% U-235, hybrid Gd₂O₃+Er₂O₃ burnable absorber, soluble-boron-free).

**Table 8.5-1. Principal safety criteria and demonstrated values.**

| Criterion | Limit | Demonstrated (rev_3) | Margin | Source |
|---|---|---|---|---|
| Shutdown margin (stuck rod) | ≥ 1 % Δk/k | **12.4 %** | ×12 | NRC SRP 4.3 |
| Moderator temperature coeff. (HFP) | < 0 | **−35.9 pcm/K** | strongly negative | GDC-11 |
| Doppler coefficient | < 0 | **−1.84 pcm/K** | negative | GDC-11 |
| Void coefficient | < 0 | **−214 pcm/%void** | strongly negative | GDC-11 |
| Control-rod worth (ARO) | ≥ 5 % Δk/k | **15 226 pcm** | ×3 | SRP 4.3 |
| Max reactivity insertion rate | ≤ 7.5e-4 Δk/k/s | **1.5e-5** | ×50 | ANSI/ANS-58.21 |
| MDNBR (steady / AOO) | ≥ 1.3 | **[SIM-PENDING — OpenFOAM hot-channel run; F_q = 3.48, F_ΔH = 2.27 handed to T-H]** | — | SRP 4.4 / 15.0 |
| PCT (LOCA envelope) | ≤ 1204 °C | **[SIM-PENDING — same run]** | — | 10 CFR 50.46(b)(1) |
| Cladding oxidation / H₂ generation | ≤ 17 % / ≤ 1 % | [SIM-PENDING] | — | 50.46(b)(2,3) |
| Primary design pressure | ≤ 17.2 MPa | 15.5 MPa operating | design per ASME III NB | ASME III |
| Containment design pressure | ≤ 0.414 MPa | [ANALYSIS-PENDING — containment P/T response] | — | SSR-2/1 Req 56 |
| Peak-rod discharge burnup | ≤ 62 GWd/MTU | **42.8 GWd/MTU** | 31 % | SRP 4.2 |
| Max enrichment | ≤ 5.0 wt% | **4.95 wt%** | 0.05 wt% — see note | 10 CFR 50 LEU |
| Cycle length | ≥ 365 EFPD | **479 EFPD** | +31 % | competition target |
| SSE | ≥ 0.3 g | 0.3 g design basis | — | RG 1.60; SSG-9 |
| Boundary dose (DBA, 0–2 h) | ≤ 0.25 Sv TEDE | [ANALYSIS-PENDING — atmospheric dispersion from the rev_3 source term, 1.2e17 Bq] | — | 10 CFR 100.11 |
| CDF / LRF | < 1e-7 / < 1e-8 /ry | partial: LOHS ~1e-8 + SBO ~1e-11 (§8.6) | — | RG 1.174 |
| Operator grace period | ≥ 72 h | 72 h by design intent; **[ANALYSIS-PENDING — IRWST inventory boil-off transient. The >100 h figure used elsewhere in this report is a best-estimate upside and shall not be cited as the licensing basis until that analysis closes]** | — | SECY-10-0034 |

**Enrichment margin note.** The 4.95 wt% peak zone deliberately approaches the 5.0
wt% LEU ceiling to maximise discharge burnup (waste-intensity score). The remaining
0.05 wt% equals a typical fabrication enrichment tolerance (±0.05 wt%); the
fuel-specification therefore requires the tolerance band to be asymmetric (−0.10/+0.00
wt%) **[VERIFY — fabrication-spec statement to be added to the mechanical/fuel
section]**.

### 8.5.3 Defence in depth

The criteria map onto the five IAEA defence-in-depth levels [SSR-2/1 §2.13]:
Level 1 prevention through inherently negative feedback (MTC/DTC/void all negative,
demonstrated) and DNB margin; Level 2 control via the reactor protection envelope
(§8.7); Level 3 design-basis-accident control by passive ECCS, EFW and PRHR (§8.6);
Level 4 severe-accident management via the ≥72 h no-operator-action grace and three
passive containment-cooling trains; Level 5 mitigation via the site-boundary EPZ
(≤0.5 km, *[ANALYSIS-PENDING — dose basis, see Table 8.5-1]*).

---

## 8.6 Safety Systems and Accident Analysis

### 8.6.1 Accident-prevention strategy: elimination before mitigation

The Aegis-40 systematically **removes classes of design-basis events by
construction** rather than mitigating them:

1. **Large-break LOCA — eliminated.** The integral RPV contains the core, two
   helical-coil once-through steam generators and the pressurizer within one pressure
   boundary; no large-bore primary piping exists. The limiting LOCA reduces to a
   small-break at instrument/injection nozzles.
2. **Rod ejection — eliminated.** Control-rod drive mechanisms are **internal
   (in-vessel)**; no head-mounted drive housing exists whose rupture could provide an
   ejection path. The bounding reactivity insertion becomes uncontrolled rod
   *withdrawal* (an AOO), against which the demonstrated insertion rate of 1.5e-5
   Δk/k/s holds a ×50 margin to the 7.5e-4 Δk/k/s limit. **[VERIFY — internal-CRDM
   statement to be anchored in the mechanical design basis with a configuration
   sketch; presently recorded from the core-design lead, 2026-06-12.]**
3. **Boron-dilution events — eliminated.** The core is soluble-boron-free; no
   dilution pathway exists. Reactivity hold-down is by hybrid Gd₂O₃/Er₂O₃ burnable
   absorber plus control rods (ARO worth 15 226 pcm vs BOL excess ~2 640 pcm).
4. **Pressurizer surge-line break — eliminated.** The pressurizer is integral to the
   RPV upper head; there is no external surge line.

### 8.6.2 Engineered safety features (passive)

All credited ESF are passive and de-energize-to-actuate (§8.7.2):

- **Emergency Feedwater (EFW)** — gravity-driven from an elevated tank; isolation
  valves fail open; no pumps. Sized for 72 h of decay-heat steaming
  *[ANALYSIS-PENDING — tank inventory calc]*.
- **Passive Residual Heat Removal (PRHR)** — two 100 % natural-circulation trains
  from the RPV to heat exchangers submerged in the In-containment Refuelling Water
  Storage Tank (IRWST); each train removes ≥105 % of decay heat at actuation. The
  governing decay-heat source is **7.75 MW at shutdown (6.2 % of 125 MWth)**,
  computed by full-chain depletion (rev_3) and cross-validated against ANS-5.1.
- **Passive containment cooling** — three trains; condensate return maintains the
  IRWST as the ≥72 h heat sink.
- **Passive safety injection** — gravity feed from IRWST on low pressurizer
  pressure+level coincidence.
- Containment: dry steel-lined, Ø15 m, design pressure 0.414 MPa. **[DECISION-PENDING
  C5 — a NuScale-style submerged-pool configuration is under team evaluation
  (`layout/fer_8810_docx_audit.md`); this section is written against the dry-containment
  baseline and the containment text, PCC description and Figures 8.6-x must be revised
  if the pool concept is adopted.]**

### 8.6.3 Analyzed events — event-tree results

Two initiators are analyzed to event-tree depth, chosen to exercise the passive chain
end-to-end. Methodology follows standard PRA practice [WASH-1400; NUREG/CR-6928];
top-event demands map one-to-one onto the trip/ESF functions of §8.7.

**Loss of Heat Sink (LOHS)** — loss of main feedwater/condenser, the lead transient
for a plant whose selling point is passive decay-heat removal. Seven sequences (4
safe, 3 core-damage); all CD sequences require ≥2 independent failures; per-initiator
CDF ≈ **1e-8/ry** *[PRA-PENDING — generic reliability data; component-specific data
to replace]* — an order of magnitude inside the 1e-7 plant target (Figure 8.6-1,
`event_tree_LOHS`).

**Station Blackout (SBO)** — LOOP plus failure of both standby AC sources
(initiator ≈1e-5/ry). Because every credited function actuates on de-energization —
trip breakers open, rods drop by gravity, EFW/PRHR valves fail open, containment
isolation valves fail closed — **loss of power constitutes actuation, not
challenge**. No AC, no DC, no operator action and no external water are required for
72 h; Class 1E batteries (72 h) serve post-accident monitoring only [RG 1.97]. The
standby diesels are defence-in-depth, not credited. SBO CDF ≈ **1e-11/ry** — four
orders below target, quantitatively substantiating the "negligible SBO" claim of
§8.8.3 (Figure 8.6-2, `event_tree_SBO`). ATWS under SBO is bounded by mechanical
common-cause failure of rod insertion (~1e-6 conditional **[VERIFY — CCF data
source]**), consistent with the intent of 10 CFR 50.62 given rod/DAS diversity.

**Remaining design-basis spectrum — screening status.** The following initiators are
identified and screened but not yet analyzed to event-tree depth; this is a declared
gap, not an oversight:

| Initiator | Why it matters here | Status |
|---|---|---|
| Small-break LOCA | only surviving LOCA class | [ANALYSIS-PENDING — tree planned next] |
| Main steam line break / excess steam demand | with MTC −35.9 pcm/K, **overcooling is the limiting reactivity transient** for this core | [ANALYSIS-PENDING] |
| Uncontrolled rod withdrawal | surviving reactivity AOO after ejection elimination | [ANALYSIS-PENDING — bounded by insertion-rate margin] |
| Loss of primary flow | natural-circulation primary; no pump-trip initiator exists, but flow-degradation (blockage) screening required | [ANALYSIS-PENDING — screening] |
| Fuel-handling accident | SFP/cask operations | [ANALYSIS-PENDING — ties to §8.8.10] |

### 8.6.4 Redundancy and necessity

For each credited system the design demonstrates both redundancy (what backs it up)
and necessity (what fails without it); the LOHS and SBO sequence tables show that
**no single failure leads to core damage** — the single-failure criterion is met at
the accident-sequence level, not merely the component level. The full tabulation is
in the event-tree analyses (`event_tree_LOHS.md` §6, `event_tree_SBO.md` §6).

---

## 8.7 Instrumentation and Control

### 8.7.1 Architecture

The I&C system is organised in five layers with strict downward non-interference
[SSG-39; IEC 61513]: Layer 1 field instrumentation (21 measurement channels, 14
Class 1E); Layer 2 Reactor Protection System; Layer 3 ESFAS; Layer 4 Distributed
Control System (non-safety); Layer 5 digital twin (advisory, read-only). Signals flow
upward only: the protection layers receive sensor signals directly from Layer 1, and
**no software path exists from the non-safety layers into Class 1E** — the DCS taps
sensor circuits through qualified one-way isolation, and the digital twin is fed
through a unidirectional data diode [IEEE 603; IEEE 384; 10 CFR 73.54]. Figure 8.7-1
(`ic_block`) shows the architecture.

### 8.7.2 Reactor Protection System

Four independent divisions (A–D) with **2-of-4 coincidence voting** satisfy the
single-failure criterion in both the trip and trip-prevention directions, including
one channel out for maintenance [IEEE 603 §5.1]. The RPS is **de-energize-to-trip**:
trip breakers are normally energized and any loss of power, air or signal produces a
scram; rods insert by gravity [IEC 61513 §5.3.6]. Platform: safety-qualified FPGA/PLC
with IEC 60880 Category A software (no dynamic memory, no recursion; independent
V&V). Deterministic timing: division scan+vote ≤ 100 ms; sensor-threshold-to-breaker
≤ 500 ms, the bound assumed in the §8.6 analyses. *[TBD — per-channel response-time
and accuracy table; total channel uncertainty per ISA-67.04 / RG 1.105 setpoint
methodology to be tabulated.]*

Principal trip derivations (full logic in `trip_signals.md`): high flux >118 %;
flux rate >5 %/s; overtemperature-ΔT and overpower-ΔT composites from T_hot/T_cold/
flux/pressure; low flow <90 %; pressurizer pressure >16.5 / <12.5 MPa; SG level
<15 % NR; containment pressure >0.17 MPa; containment radiation >100× background.

### 8.7.3 ESFAS

Same 4-division/2-of-4 structure; actuations are **latching** (deliberate operator
reset required). Functions: passive safety injection (low pzr P + level), containment
isolation (high containment P or radiation), EFW (low SG level or loss of normal FW),
PRHR/PCC alignment (low SG level + EFW unavailable, or high core-exit T post-scram),
main-steam isolation (high MSL radiation or containment P). All actuated devices move
to their safe state on loss of motive power (§8.6.2).

### 8.7.4 Diverse Actuation System

A Class 1E but **platform-diverse** system (different technology and design team from
the RPS) covers postulated common-cause failure of all four RPS divisions
[SECY-93-087; BTP 7-19; SSG-39 §6]. It monitors power-range flux and pressurizer
pressure through fixed, hardware-biased logic, with setpoints staggered beyond the
RPS envelope, and provides diverse paths to the trip breakers and to SI/PRHR
actuation. *Sufficiency rationale: the two monitored variables bound the
high-consequence CCF scenarios (overpower and loss-of-coolant/overpressure families);
[VERIFY — defend two-variable sufficiency against the screened initiator list of
§8.6.3 once those analyses close].* In the soluble-boron-free core, DAS rod-insertion
diversity carries the ATWS burden (§8.6.3).

### 8.7.5 Control room and human factors

Two-operator MCR per NUREG-0700: reactor-operator and BOP consoles, STA read-only
station, 4×80″ overview wall (plant mimic, SPDS, critical safety functions). Alarm
management per ISA 18.2 (three tiers; ≤10 alarms in any 10-minute window under
design-basis transients). Computer-based procedures with paper backup. **Hardwired,
software-independent manual actions** — reactor trip, SI, CI, EFW, MSIV closure — per
IEEE 603 §5.8. MCR habitability HVAC per §8.8.1.

### 8.7.6 Digital twin (advisory) — originality feature

A non-safety digital twin mirrors all Layer 1 signals through the data diode and
provides soft sensors (MDNBR, fuel centreline temperature estimates), anomaly
detection and predictive maintenance. It is Category C software, cannot actuate any
device, and presents alongside (never in place of) qualified indications. This
enables condition-based maintenance and reduced-staffing operation without touching
the safety qualification of Layers 1–3 — cf. NuScale's ISV-validated reduced-staffing
precedent [NUREG-0711 program].

### 8.7.7 Qualification

Class 1E equipment: environmental qualification per IEEE 323 (150 °C, 0.5 MPa, 100 %
steam, 1 MGy lifetime, jet impingement where exposed) *[VERIFY — environment envelope
to be confirmed against the containment P/T analysis when it closes]*; seismic per
IEEE 344 at SSE 0.3 g; cybersecurity program per 10 CFR 73.54 / RG 5.71 (Purdue-model
segmentation, no wireless in safety areas, no remote access to Class 1E, signed
firmware, write-once audit logs).

### References (§8.5–8.7)

IAEA SSR-2/1 Rev 1; IAEA SSG-2 Rev 1 (deterministic safety analysis); SSG-9; SSG-30;
SSG-39; 10 CFR 50 App. A (GDC 11, 13, 17, 19–24, 26); 10 CFR 50.46; 10 CFR 50.62;
10 CFR 50.63 + RG 1.155; 10 CFR 73.54 + RG 5.71; 10 CFR 100.11; NUREG-0800 SRP
Ch. 4, 7, 15; NUREG-0700/0711; NUREG/CR-6890; NUREG/CR-6928; WASH-1400; RG 1.60,
RG 1.97 Rev 5, RG 1.105, RG 1.152, RG 1.174, RG 1.242; IEEE 603, 7-4.3.2, 323, 344,
384; IEC 61513, 60880, 62138; ISA 18.2, ISA-67.04; ANSI/ANS-58.21; ANS-5.1;
ASME III; SECY-93-087, SECY-10-0034; BTP 7-19.

---

*End of draft r1. Open markers: 6× [SIM/ANALYSIS-PENDING], 5× [VERIFY], 1×
[DECISION-PENDING C5], 2× [TBD]. Review companion:
`planning/FER_readiness_review_2026-06-13.md` (gaps G1–G11, consistency X1–X6).*
