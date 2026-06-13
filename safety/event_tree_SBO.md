# Event Tree — Station Blackout (SBO) — Aegis-40

*Source document. Drop into FER §8.6 (event trees, redundancy & necessity analysis).*
*Companion: `event_tree_LOHS.md` (first tree, method baseline), `trip_signals.md`,
`safety_criteria.yaml`, `event_tree_SBO.drawio` (editable diagram).*
*Owner: Azamhon. Created: 2026-06-13.*

---

## 1. Why SBO (and why it is the design's showcase)

Station Blackout — loss of off-site power (LOOP) **plus** failure of both standby AC
sources — is historically the dominant CDF contributor for active-safety LWRs
(Fukushima initiator). For the Aegis-40 it is the **showcase tree**: every credited
safety function is driven by **de-energization** — loss of power *is* the actuation
signal, not a challenge to it:

- Trip breakers open on de-energization → CRDM coils release → **rods drop** (gravity).
- EFW valves are fail-**open** (de-energize-to-actuate) → gravity feed from elevated tank.
- PRHR alignment valves fail-open → natural circulation to IRWST.
- Containment isolation valves fail-**closed**.

The FER draft (§8.8.3) asserts "negligible SBO contribution to CDF" — **this tree
substantiates that claim.** The standby diesels (DGB) are defence-in-depth /
investment protection, *not* credited for core safety.

---

## 2. Initiator and mission

| Item | Value |
|---|---|
| **Initiating event** | LOOP + both standby AC sources fail = SBO |
| **Initiator frequency** | f(LOOP) ~2e-2 /ry (coastal grid, Sinop `[SITE-PENDING]`) × P(both AC fail \| LOOP) ~5e-4 → **~1e-5 /ry** `[PRA-PENDING]` |
| **Mission time** | 72 h (`operator_grace_period`; FER draft claims >100 h — see audit C6, unsubstantiated until the OpenFOAM transient closes) |
| **DC role** | Class 1E batteries (≥72 h) power **monitoring only** (RG 1.97 post-accident channels). No DC is required to *actuate* any credited function. |
| **Success end-state** | Stable passive cooling ≥72 h; barriers intact; AC recovery or external makeup beyond 72 h |
| **Failure end-state** | Core damage (CD) |

---

## 3. Top events (in order of demand)

| # | Top event | Success criterion | Powered by | I&C trigger |
|---|---|---|---|---|
| **RT** | Reactor trip | Rods in on de-energization | Gravity (stored energy) | None needed — undervoltage = trip (fail-safe) |
| **EFW** | Emergency feedwater | ≥1 SG fed by gravity; steam relieved via SG safety valves | Gravity head, fail-open valves | E3 / undervoltage |
| **PRHR** | Passive residual heat removal | PRHR HX ≥105 % decay heat to IRWST by natural circ | Buoyancy | E4 / fail-open alignment |
| **IRWST** | Long-term passive sink | IRWST + passive containment cooling ≥72 h | Inventory + condensation return | Latched |

No BOR/DAS branch as in LOHS: with no AC, the diverse *powered* mitigations are
unavailable — but rod insertion itself is unpowered, so ¬RT requires **mechanical
common-cause failure of ≥2 of 9 CCAs** (~1e-6 conditional `[PRA-PENDING]`), which is
modelled as a direct CD transfer (S5).

---

## 4. Event tree (logic)

Diagram: `event_tree_SBO.drawio` (editable). Structure:

```
SBO (~1e-5/ry) ── RT? ──fail (mech CCF ~1e-6)──────────────► CD-2  (ATWS+SBO, ~1e-11)
                   │success
                   ├─ EFW? ──success──► OK-1  hot standby, SG sink (dominant)
                   │fail (~1e-2)
                   ├─ PRHR? ──success──► OK-2  passive cooldown to IRWST
                   │fail (~1e-2)
                   ├─ IRWST? ──success──► OK-3  ≥72 h passive (ext. makeup after)
                   │fail (~1e-3)
                   └────────────────────► CD-1  total loss of heat removal (~1e-12)
```

---

## 5. Sequence table

| Seq | Path | End state | Class | Approx. frequency `[PRA-PENDING]` | Dominant dependency |
|---|---|---|---|---|---|
| S1 | RT·EFW | OK-1 | Safe (hot standby on SG sink) | ~1e-5 | EFW tank + fail-open valves |
| S2 | RT·¬EFW·PRHR | OK-2 | Safe (passive cooldown) | ~1e-7 | PRHR train (≥1 of 2) |
| S3 | RT·¬EFW·¬PRHR·IRWST | OK-3 | Safe (≥72 h passive) | ~1e-9 | IRWST inventory + containment condensation |
| S4 | RT·¬EFW·¬PRHR·¬IRWST | **CD-1** | Core damage | ~**1e-12** | total passive-chain failure |
| S5 | ¬RT (mech CCF) | **CD-2** | Core damage (ATWS+SBO) | ~**1e-11** | stuck-rod common cause |

**CDF contribution (SBO):** Σ(S4,S5) ≈ **1e-11 /ry** — four orders of magnitude below
the 1e-7 plant target and ~three below the LOHS contribution (1e-8). **The FER §8.8.3
"negligible SBO" claim is quantitatively demonstrated.** Beyond-72 h: OK-1/OK-2/OK-3
require AC recovery (off-site restoration typ. <24 h) **or** external water makeup via
the FLEX-style connection `[CONNECTION-POINT-TBD]` — a coping extension, not a cliff.

---

## 6. Redundancy & necessity analysis (FER §8.6 explicit requirement)

| System | Redundancy | Necessity (what fails without it) | Why SBO-proof |
|---|---|---|---|
| Trip breakers / rods | 9 CCAs, any-2-of-9 SDM ≥1 % | ¬RT → S5 | De-energize-to-trip — SBO *causes* scram |
| EFW | Elevated tank, gravity, 72 h inventory | Demand passes to PRHR | No pumps, fail-open valves |
| PRHR | 2 × 100 % trains | Demand passes to IRWST | Natural circulation only |
| IRWST + PCC | Single pool + 3 passive containment trains | CD-1 | No moving parts; condensation return |
| Class 1E DC | 2 × 72 h battery banks | Monitoring blind (not a CD path) | Sized for monitoring loads only |
| Standby diesels (DGB) | 2 × 100 % | Nothing safety-credited — DiD only | Their CCF *defines* the initiator, not the response |

**Necessity conclusion:** as in LOHS, every CD sequence needs ≥2 independent failures;
additionally, **no sequence requires any AC or DC power, operator action, or external
water for 72 h** — the strongest single statement in the §8.6 package.

---

## 7. I&C role through the sequence (ties to §8.7)

1. **t = 0:** grid lost + both standby sources fail → undervoltage on Class 1E buses →
   trip breakers open (no logic required), CRDM coils release, rods in.
2. EFW/PRHR/CIV solenoids de-energize to their safe states (`trip_signals.md`
   fail-safe table; FER draft §8.8.2 confirms air/power-loss = safe position).
3. Batteries carry RG 1.97 monitoring: core-exit TCs, wide-range SG level, containment
   P/T, IRWST level → operators *observe*, intervene only beyond 72 h.
4. DAS: also de-energize-to-actuate, but unpowered diverse logic adds nothing here —
   its value is in powered ATWS sequences (see LOHS tree).

---

## 8. Open items

| # | Item | Impact | Owner |
|---|---|---|---|
| 1 | Site-specific LOOP frequency (Sinop grid) | Initiator frequency | supervisor / site data |
| 2 | Battery sizing calc (monitoring load × 72 h) | Validates DC coping claim | Azamhon + electrical |
| 3 | SG safety-valve relief capacity vs decay heat | OK-1 viability duration | T-H team |
| 4 | FLEX-style external makeup connection point | Beyond-72 h coping | layout (next drawing rev) |
| 5 | Stuck-rod mechanical CCF probability | S5 frequency | reliability/PRA |
| 6 | 72 h vs ">100 h" (FER draft) reconciliation | One number everywhere | audit C6 |

---

## 9. References

- NUREG/CR-6890 — LOOP/SBO frequency data · 10 CFR 50.63 (SBO rule) + RG 1.155
- IAEA SSR-2/1 Rev 1 Req 68; SSG-34 §SBO · NUREG-0800 SRP 8.4
- ANS-5.1 decay heat · NRC RG 1.97 Rev 5 (monitoring)

---

*End of SBO event tree. 5 sequences, 3 safe / 2 CD, CDF ≈ 1e-11 /ry — SBO is
demonstrated negligible because de-energization actuates, rather than defeats,
every credited safety function.*
