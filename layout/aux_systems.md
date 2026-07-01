# Auxiliary Systems — Aegis-40

*Source document. Drop into FER §8.8 Auxiliary Systems Design.*
*Companion: `layout/zones.md`, `layout/building_list.md`, `layout/block_layout.png`, `layout/flow_arrows.png`.*
*Owner: Azamhon. Last updated: 2026-06-15.*

---

## 0. Scope + how to read this file

FER §8.8 requires that **each** auxiliary system carry six fields:
**purpose · operating principle · layout location · safety function (yes/no) · performance · maintenance**,
plus a flow/instrumentation diagram (A4) and an electrical-supply description (A5).

This file delivers the **list + six-field metadata for all 8 systems** (satisfies §8.8 A1–A3).
A4 (per-system P&IDs) and A5 detailed single-line diagram are **flagged W3** — structure built here, drawings deferred. See §11 coverage.

**Tags:** `[ASSUMED]` = engineering placeholder; `[SIM-PENDING]` = awaits OpenMC/OpenFOAM number; `[ALISHER]`/`[ADILBEK]`/`[SAMIRA]` = teammate input.

**Cross-refs already locked:**
- Sensors / monitoring channels → `ic/sensor_inventory.md`
- Trip + ESF actuations → `safety/trip_signals.md`
- Safety limits (dose, SFP temp, etc.) → `safety/safety_criteria.yaml`
- Building IDs → `layout/building_list.md`

---

## 1. System inventory (the list)

| # | System | FER §8.8 sub-heading | Safety function? | Primary building |
|---|---|---|---|---|
| 1 | HVAC / Ventilation | Ventilation | **Yes** (NI confinement) | RXB, AB, CB, SFB |
| 2 | Fire Protection | Fire protection | **Yes** (defence-in-depth) | site-wide |
| 3 | Radiation Protection + Monitoring | (radiation protection) | **Yes** | site-wide |
| 4 | Emergency Power | electrical (emergency) | **Yes** (1E) | DGB, CB |
| 5 | Normal Electrical Distribution | electrical (on/off-site) | No (non-1E) | EHB, CB |
| 6 | Fuel Handling + Storage | Fuel handling and storage | **Yes** (SFP integrity) | RXB, SFB |
| 7 | Fission-Product Release Control | Fission-product release control | **Yes** | RXB, WMB |
| 8 | Service Systems (compressed air, demin water, SFP cooling) | (compressed air + support) | mixed | AB, SFB |
| 9 | Cogeneration Interface Isolation (TES / SOE) | (cogen interface — Req 35) | **Yes** | TB, EUB |

9 systems: the first eight map 1:1 onto the five FER §8.8 named sub-headings (fission-product release control, ventilation, compressed air, fuel handling/storage, fire protection) **plus** the cross-cutting electrical + radiation-protection systems the section also demands (A1). System 9 (cogeneration interface isolation) is added to satisfy **IAEA SSR-2/1 Req 35** for this cogeneration plant (district heat via TES + hydrogen via SOE).

---

## 2. HVAC / Ventilation

| Field | Detail |
|---|---|
| **Purpose** | Maintain habitability + equipment temperature limits; establish **negative-pressure cascade** so air flows from clean → potentially-contaminated → filtered exhaust, never reverse. |
| **Operating principle** | Once-through (NI radiological zones) and recirculating (CB, clean areas). Zoned pressure gradient: MCR slightly positive (keeps contaminants out); reactor/aux radiological areas slightly negative (confines release). All NI exhaust passes HEPA + activated-charcoal before the off-gas stack. |
| **Layout location** | RXB confinement exhaust + AB radwaste-area exhaust → WMB filter trains → OFFGAS stack (≥ 30 m, `building_list.md` §3.4). CB has its own isolated air-handling with intake radiation monitors. |
| **Safety function** | **Yes.** MCR habitability (operator dose limit), confinement of airborne activity, SFP-area iodine removal. Control-room intake isolation is an ESF actuation — see `safety/trip_signals.md`. |
| **Performance** | MCR ≤ 0.05 Sv 30-day accident dose `[ASSUMED, GDC-19 bound]`; HEPA ≥ 99.97 % @ 0.3 µm; charcoal iodine removal ≥ 99 %; negative-pressure areas ≥ −0.25 in. w.g. relative to atmosphere. |
| **Maintenance** | HEPA/charcoal differential-pressure monitored; filter change on ΔP setpoint or periodic in-place leak test (DOP/freon). Redundant fan trains — maintain one while the other runs. |

---

## 3. Fire Protection

| Field | Detail |
|---|---|
| **Purpose** | Prevent fire from disabling redundant safety divisions; protect personnel + plant investment. Fire is a credible common-cause failure of I&C divisions — defeated by **separation + suppression**. |
| **Operating principle** | Defence-in-depth: (1) non-combustible construction + 3 h fire barriers between RPS/ESFAS divisions A–D (`ic/ic_architecture.md` 4-division layout); (2) detection (ionisation/photoelectric + thermal); (3) suppression — pre-action sprinkler in most areas, **clean-agent (e.g. Novec/IG-541, no water)** in MCR + I&C + switchgear rooms; (4) manual hose stations + extinguishers. |
| **Layout location** | Fire-water tank + diesel/electric fire pumps in CI service area; ring main loops both NI + CI. Division barriers inside CB enforce the 4-division physical separation that the 2/4 voting logic relies on. |
| **Safety function** | **Yes (defence-in-depth).** Protects safe-shutdown capability; satisfies separation basis of the I&C architecture. No active reactor-trip role, but loss of a division to fire must not defeat 2/4 logic — barriers guarantee that. |
| **Performance** | Fire-water ≥ 2 h at largest-area demand `[ASSUMED]`; barriers 3 h rated; clean-agent design concentration reached ≤ 10 s in I&C rooms. |
| **Maintenance** | Quarterly detector test; pump churn + flow test; barrier-penetration seal inspection after any cable work. |

---

## 4. Radiation Protection + Monitoring

| Field | Detail |
|---|---|
| **Purpose** | Keep worker + public dose ALARA; detect + alarm abnormal radioactivity; provide the radiological data feeding emergency response within the EPZ (`safety/safety_criteria.yaml` `epz_radius` 0.5 km). |
| **Operating principle** | Four monitoring layers per IAEA SSR-2/1 Req 81–82: **area** (fixed gamma monitors in occupied + access-controlled spaces), **process** (in-line monitors on liquid effluent, gaseous effluent stack, primary coolant, SFP, component cooling water — detect leakage), **personnel** (portal monitors, electronic dosimetry, contamination frisking), and **post-accident high-range** (RG 1.97 wide-range containment + effluent monitors, e.g. RAD-CONT to 1e3 Sv/h, `ic/sensor_inventory.md`) so the release path stays instrumented through severe conditions. Stack + liquid-effluent monitors gate all releases against permit limits. Dose-rate zoning map (ALARA, Req 5) overlays `layout/zones.md`. |
| **Layout location** | Sensors per `ic/sensor_inventory.md`; effluent monitors on WMB stack + liquid-discharge line; personnel control point at NI Protected-Area boundary. Health-physics lab + counting room in AB. |
| **Safety function** | **Yes.** High-radiation signals contribute to containment isolation + ventilation isolation actuations (`safety/trip_signals.md`). Effluent monitors enforce release limits. |
| **Performance** | Effluent within 10 CFR 20 / Turkish NDK limits `[verify NDK citation — open item #5 in README]`; area-monitor alarm setpoints zone-specific; sensitivity to detect 1 % failed-fuel iodine in primary coolant `[ASSUMED]`. |
| **Maintenance** | Source-check monitors on schedule; calibrate against traceable standards; redundant stack monitor so release path is never unmonitored during maintenance. |

---

## 5. Emergency Power (Class 1E)

| Field | Detail |
|---|---|
| **Purpose** | Supply safety loads when offsite + normal onsite power are lost (LOOP / SBO). Note Aegis-40's passive safety design (gravity EFW, passive decay-heat removal — locked decision #5 + #6) means emergency power supports **monitoring + active backup**, not primary core cooling. |
| **Operating principle** | Two independent trains: **2× emergency diesel generators** (≥ 100 % safety load each, FER Table 1 "emergency power = 2") + **Class 1E station batteries / UPS** for instantaneous + ride-through power to I&C, MCR, and DC-powered valves. EDGs auto-start on undervoltage / LOOP signal. Inverters give uninterruptible AC to vital I&C buses. |
| **Layout location** | 2× EDG in DGB (Cat I, physically + electrically separated, `building_list.md`); battery + inverter rooms in CB adjacent to switchgear, one set per division. |
| **Safety function** | **Yes — 1E.** Powers RPS/ESFAS, post-accident monitoring (DAS), MCR habitability HVAC, containment isolation valves. Battery sizing covers the gap to passive-system self-sufficiency + the 72 h grace claim. |
| **Performance** | EDG start-to-load ≤ 60 s `[ASSUMED]`; battery duty ≥ 8 h (`W2_Layout_Plan.md` aux list) to ≥ 24 h `[ASSUMED — confirm against 72 h grace]`; redundancy = single-failure-proof (lose one train, the other carries full safety load). |
| **Maintenance** | EDG monthly start + load test; battery service + discharge test; one train maintained while the other remains operable (tech-spec staggered). |

**This is the A5 "emergency + uninterruptible power" deliverable in narrative form.** Single-line diagram → W3.

---

## 6. Normal Electrical Distribution

| Field | Detail |
|---|---|
| **Purpose** | Deliver generated power to grid; supply all normal plant loads (house load) from grid or generator. |
| **Operating principle** | Generator (40 MWe) → main transformer (50 MVA, `building_list.md` EHB) → 33 kV switchyard → grid. House load taken via unit-auxiliary transformer (generator side) with station-service transformer as alternate from the grid side — standard PWR offsite/onsite dual feed. On trip, house load auto-transfers to the offsite (grid) source. |
| **Layout location** | Switchyard + transformer pads in EHB (CI); medium- + low-voltage switchgear in CB; cable routes separated from 1E routes. |
| **Safety function** | **No (non-1E).** But it is the **preferred** power source — the 1E emergency system only acts when this fails. Off-site grid connection is the first defence-in-depth layer. |
| **Performance** | Main transformer 50 MVA covers 40 MWe export + ~5 MW house load `[ASSUMED house load]`; 33 kV grid interface (locked in `building_list.md`). |
| **Maintenance** | Conventional industrial practice; transformer oil + bushing monitoring; switchgear inspection. Non-safety so maintainable without reactor-state restriction. |

**A5 "on-site + off-site electrical" deliverable.** Dual-feed concept here; one-line drawing W3.

---

## 7. Fuel Handling + Storage

| Field | Detail |
|---|---|
| **Purpose** | Move fuel from delivery → core → spent-fuel pool → dry-cask staging, keeping it cooled + subcritical + shielded at every step. |
| **Operating principle** | Refueling machine over the reactor pool transfers assemblies through a **flooded transfer canal** (water = shield + coolant) to the SFP fuel-handling machine. **Corrected 2026-07-01 (N11):** subcriticality is held by a **flux-trap Boral (B₄C-in-Al) rack + SFP soluble boron + burnup credit** — acceptance **k_adj 0.892 ≤ 0.95 with 2000 ppm SFP boron** (10 CFR 50.68(b); crediting boron + burnup is standard for >4 wt% fuel). The unborated fresh-∞ Boral case (k_inf 1.079) is the defence-in-depth bound, not the credited state. **NOTE: SFP boron is separate from the boron-free reactor coolant — the SBF claim is a reactor-coolant statement and is unaffected.** SFP holds ≥ full-core-offload + multi-cycle capacity. Dry-cask staging for long-term. |
| **Layout location** | Refueling pool in RXB; transfer canal RXB→SFB; SFP + handling machine + cask staging in SFB (`building_list.md`, pool ≈ 10×10×10 m). |
| **Safety function** | **Yes.** Maintain SFP subcriticality + cooling + level (SFP temp/level limits in `safety_criteria.yaml`). Fuel-handling interlocks prevent mishandling / uncovering. |
| **Performance** | SFP capacity ≥ 1 full core + ≥ 10 cycles `[ASSUMED — depends on fuel-assembly count, Samira open item: 21 vs 240]`; rack keff ≤ 0.95 subcritical `[ASSUMED, std SFP criterion]`. |
| **Maintenance** | Fuel-handling machine load-tested before each campaign; SFP cleanup demineraliser resin change; underwater inspection of racks. |

**Open dependency:** SFP size + rack design both ride on the unresolved fuel-assembly count (`building_list.md` open item #5).

---

## 8. Fission-Product Release Control

| Field | Detail |
|---|---|
| **Purpose** | The FER §8.8 first-named sub-heading. Provide the **barriers + cleanup** that keep fission products out of the environment across the three-barrier chain (fuel cladding → primary boundary → containment). |
| **Operating principle** | (1) Containment isolation — automatic valve closure of penetrations on high-radiation / high-pressure (ESFAS, `safety/trip_signals.md`); (2) containment as the leak-tight pressure boundary (dry, steel-lined RC, 4.14 bar design, FER Table 1); (3) gaseous-radwaste treatment — decay hold-up tanks + HEPA + charcoal before stack; (4) liquid-radwaste treatment before monitored discharge. |
| **Layout location** | Isolation valves at RXB containment boundary; gaseous + liquid radwaste trains in WMB; off-gas stack on WMB. |
| **Safety function** | **Yes — top-tier.** This *is* the §8.6-accident mitigation path for any release sequence. Directly tied to dose acceptance criteria in `safety_criteria.yaml`. |
| **Performance** | Containment leak rate ≤ design `[SIM-PENDING source-term]`; gaseous decay hold-up sized so noble-gas activity decays below release limit before discharge `[ASSUMED]`; dose at EPZ boundary within limits (`safety_criteria.yaml`). |
| **Maintenance** | Containment integrated leak-rate test (ILRT) per interval; isolation-valve stroke test; radwaste filter change on ΔP. |

---

## 9. Service Systems (compressed air · demin water · SFP cooling)

| Field | Detail |
|---|---|
| **Purpose** | Support utilities every other system needs: instrument + service air, demineralised water makeup, and active SFP heat removal. |
| **Operating principle** | **Instrument air** — oil-free compressors + dryers feed air-operated valves/dampers (fail-safe on loss of air — valves go to safe position). **Service air** — general plant use. **Demin water** — ion-exchange plant supplies primary makeup, SFP makeup, steam-cycle makeup. **SFP cooling** — pump + heat-exchanger skids reject SFP decay heat to component-cooling water → **once-through seawater (the NORMAL heat sink, non-safety)**. Note: the **safety** ultimate heat sink is the passive IRWST/containment cooling (seawater-independent); the large SFP thermal inertia gives long grace if active SFP cooling is lost (`safety/safety_criteria.yaml` `ultimate_heat_sink`). |
| **Layout location** | Compressors + air receivers + demin plant in AB; SFP cooling skids in SFB. |
| **Safety function** | **Mixed.** Instrument air: non-1E but valves fail-safe (so loss is bounded). SFP cooling: important-to-safety (loss → SFP heat-up; but large pool thermal inertia gives long grace, monitored by `safety_criteria.yaml` SFP-temp limit). Demin water: non-safety. |
| **Performance** | Instrument-air dew point ≤ −40 °C `[ASSUMED]`; SFP cooling sized to hold pool ≤ 50 °C normal / ≤ 80 °C max `[ASSUMED — set against safety_criteria SFP row]`. |
| **Maintenance** | Compressor + dryer service; demin resin regeneration; SFP-cooling redundant skid (maintain one, run the other). |

---

## 9a. Cogeneration Interface Isolation (SSR-2/1 Req 35)

Aegis-40 is a **cogeneration plant**: it exports heat to a **Thermochemical Energy
Storage (TCES, zeolite-13X)** district-heating network and steam to a Solid-Oxide
Electrolysis (SOE) hydrogen plant. The TCES bed (C3 resolved 2026-06-13) is charged by
dehydration off surplus pass-out steam and discharged by hydration to the district-heat
intermediate loop, decoupling steady reactor output from grid dispatch (load-following).
IAEA SSR-2/1 **Req 35** requires that such heat-utilization couplings be
designed so that **no process can transport radionuclides from the nuclear plant to the
district-heating or hydrogen unit in operational states OR accident conditions**. This
system provides that barrier set.

| Field | Detail |
|---|---|
| **Purpose** | Deliver heat/steam to TES (district heating) and SOE (H₂) while guaranteeing no radionuclide pathway to the public product, in normal and accident conditions (Req 35). |
| **Operating principle** | **Non-radioactive intermediate loop** interposed between the reactor secondary steam and *both* customer circuits — reactor steam never contacts district-heat water or SOE feed. Heat crosses two interface heat exchangers (reactor-side HX → intermediate loop → customer-side HX). The clean intermediate loop is held at **higher pressure** than the reactor-side stream at the interface HX, so any HX tube leak flows **inward** (clean → reactor), never outward. Result: ≥3 independent barriers between primary coolant and the public product — (1) SG tube wall, (2) intermediate-loop boundary, (3) customer-side HX wall. |
| **Layout location** | Reactor-side interface HX in the Turbine Building (TB); intermediate-loop pumps + customer-side HX in the Energy-Utilization Building (EUB, TES/SOE island per `zones.md` Z-energy). Cogen island is the hydrogen-stand-off zone, already separated for explosion physics. |
| **Safety function** | **Yes.** Auto-isolation of the cogen interface is credited for Req 35: fail-closed isolation valves on both interface HX close on (a) high activity in the intermediate loop or a product stream, (b) steam-generator-tube-rupture signal, or (c) containment isolation — tied into ESFAS / `safety/trip_signals.md`. Isolation removes the export path without affecting reactor safety systems (cogen is not a reactor safety function — only its isolation is). |
| **Performance** | ≥3 independent barriers (criterion `cogen_radionuclide_isolation` ≥2 ✅). Intermediate-loop + product-stream activity ≤ background; interface ΔP maintained clean-side-high with continuous monitoring. **Tritium** is the governing nuclide — at SOE temperatures (~800 °C) it permeates metal readily: mitigate with oxide/alumina **permeation-barrier coatings** on the high-temperature SOE interface HX, tritium monitoring on the H₂ product, and a getter/cleanup on the intermediate loop `[ANALYSIS-PENDING — tritium permeation + carryover budget for the SOE high-T interface]`. District-heat side is lower-temperature and bounded by the intermediate loop + ΔP. |
| **Maintenance** | Periodic interface-HX leak test (eddy-current / pressure-decay); isolation-valve stroke test; intermediate-loop + product activity-monitor source-check; permeation-barrier integrity inspection on the SOE HX. |

**Barrier-count check (Req 35):** SG tube + intermediate-loop boundary + customer HX = **3 ≥ 2** → `cogen_radionuclide_isolation` satisfied by design. Accident-condition isolation (the second half of Req 35) is the ESFAS-actuated fail-closed valving above.

---

## 10. Electrical supply summary (FER §8.8 A5 consolidated)

Drawn together so the reviewer sees one electrical story:

```
  GRID (33 kV) ──► Switchyard (EHB) ──► Main Xfmr 50 MVA ──► GENERATOR (40 MWe)
       │                                      │
       │ (offsite feed)                       │ (onsite normal feed via UAT)
       ▼                                      ▼
  Station-Service Xfmr ───────► PLANT NORMAL BUSES (non-1E)  [§6]
                                      │
                            (on loss of normal + offsite)
                                      ▼
   ┌────────────── CLASS 1E BUSES ──────────────┐            [§5]
   │  2× EDG (DGB)        1E Batteries/UPS (CB)  │
   │  (auto-start LOOP)   (instant + ride-thru)  │
   └─────────────────────────────────────────────┘
        powers: RPS · ESFAS · DAS · MCR HVAC · isolation valves
```

Defence-in-depth power layers: **grid → onsite generator → EDG → battery → passive (no power needed)**. The passive core-cooling decision (#5, #6) is what lets the chain end in "no power needed" within the 72 h grace window.

---

## 11. FER §8.8 coverage check

| FER §8.8 req | Demand | Status | Where |
|---|---|---|---|
| A1 | Ventilation, electrical, fire, radiation protection — all technical info | ✅ | §2, §3, §4, §5, §6 |
| A2 | Each named sub-heading present (fission-product control, ventilation, compressed air, fuel handling/storage, fire protection) | ✅ | §8, §2, §9, §7, §3 |
| A3 | Each system: purpose · principle · layout · safety function · performance · maintenance | ✅ | six-field table, all 8 systems |
| A4 | Flow + instrumentation diagram per system | △ **W3** | structure ready; P&IDs deferred to W3 (CAD-level) |
| A5 | On-site + off-site electrical incl. emergency + uninterruptible — graphics/drawings/plans | △ **W3** | narrative + ASCII single-line in §5, §6, §10; formal drawing deferred |

**3 of 5 fully ✅; 2 (A4, A5 drawings) △ deferred to W3 with structure in place. 0 gaps.**

---

## 12. Open items propagated

| # | Item | Affects | Owner |
|---|---|---|---|
| 1 | Battery duty 8 h vs 24 h vs 72 h-grace alignment | §5 performance | Azamhon + safety |
| 2 | SFP rack type given boron-free core (decision #3) — fixed absorber vs borated | §7 | Samira + safety |
| 3 | Fuel-assembly count (21 vs 240) → SFP size | §7 | Samira |
| 4 | NDK effluent-limit citation | §4 performance | Azamhon (README open item #5) |
| 5 | Source term for containment leak / gaseous hold-up sizing | §8 performance | OpenMC/safety `[SIM-PENDING]` |
| 6 | Per-system P&IDs (A4) + formal single-line (A5) | §11 | Azamhon, W3 |
| 7 | House-load MW for transformer sizing | §6 | T-H / BOP |
| 8 | Tritium permeation/carryover budget for the SOE high-T interface (Req 35) | §9a performance | Alisher (TES/SOE) + safety |

---

## 13. References

- FER `docs/FER_Template.docx` §8.8 (auxiliary systems design)
- `ic/ic_architecture.md` — 4-division I&C separation (fire-barrier basis)
- `ic/sensor_inventory.md` — radiation + process monitoring channels
- `safety/trip_signals.md` — containment + ventilation isolation actuations
- `safety/safety_criteria.yaml` — SFP, dose, EPZ limits
- `layout/building_list.md` — building IDs + DGB/EHB/WMB/SFB sizing
- FER Table 1 — emergency power supplies = 2; containment dry 4.14 bar
- NFPA 805 (fire), GDC-19 (MCR habitability), 10 CFR 20 (effluent) — `[verify against Turkish NDK equivalents]`

---

*End of auxiliary systems list. 9 systems (incl. cogeneration interface isolation, SSR-2/1 Req 35), full six-field metadata each, §8.8 A1–A3 ✅, A4–A5 △ (W3). 8 open items flagged.*
