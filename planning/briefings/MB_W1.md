# Week 1 Report — 3S Safety / I&C / FOM

**Week:** 2026-W22 (2026-05-26 → 05-31)
**Owner:** Azamhon
**Scope:** Safety criteria · Instrumentation & Control · Figure-of-Merit integration
**Audience:** full team + supervisor review
**Duration:** 10–15 min spoken — **complete script below**
**Artifacts (all in repo):**
`safety/safety_criteria.{yaml,md}` · `safety/trip_signals.md` · `safety/event_tree_LOHS.{md,png}`
`ic/ic_architecture.md` · `ic/sensor_inventory.md` · `ic/ic_block.{mmd,png}`
Daily briefs: `MB_D1.md`, `MB_D3.md` · Plan: `W1_Plan.md`

---

## How to use this file

`>` blocks = spoken verbatim. `[...]` = stage directions (what to show). Timing per section in §0. Target ≈ 13 min + 2 min Q&A.

---

## 0. Timing map

| § | Content | Time |
|---|---|---|
| 1 | What my role is | 1:00 |
| 2 | The week in one sentence | 0:30 |
| 3 | Day 1 — Safety criteria | 2:00 |
| 4 | Day 2 — I&C architecture + sensors | 2:00 |
| 5 | Day 3 — Block diagram (on screen) | 2:00 |
| 6 | Day 4 — Trips + event tree (on screen) | 2:30 |
| 7 | The golden thread (traceability) | 1:30 |
| 8 | How I know it's right (QA) | 1:00 |
| 9 | Decisions, open items, asks | 1:00 |
| 10 | FER fit + what's next | 0:30 |
| | **Total** | **~13:00** |

---

## 1. What my role is (1:00)

> "My part of this project is the connective tissue. Three jobs that look separate but are one system. First — **safety**: defining the limits the reactor must never cross. Second — **instrumentation and control**: the nervous system that watches those limits and acts when they're approached. Third — the **Figure of Merit**, the FOM: the scoring framework that pulls every team's numbers — neutronics, thermal-hydraulics, energy conversion, layout — into one comparison against real reference reactors.
>
> So while OpenMC designs the core and OpenFOAM cools it, my job is to take their outputs, prove the design stays safe, show the I&C that enforces it, and roll it all into a single defensible score. I'm the integration node. If their numbers change, my documents update; if my limits are violated, the FOM flags the design as failed. This week I built the backbone of all three, covering FER sections 8.5, 8.6, and 8.7."

---

## 2. The week in one sentence (0:30)

> "In one sentence: I built a chain where every safety limit is traceable to a sensor that watches it, a trip that protects it, an accident scenario that tests it, and a score that rewards it. Six deliverables planned, five complete, the sixth — the FOM template — is next. Let me walk the chain."

---

## 3. Day 1 — Safety criteria (2:00)

> "Day 1 produced the spine: the safety criteria table. **Twenty-seven numeric limits across seven categories** — reactivity, thermal-hydraulics, pressure, decay-heat removal, radiological, seismic, and fuel cycle.
>
> Every limit is one of three kinds. **Hard constraints** — seventeen of them — are pass-fail. Cross one, like peak clad temperature above 1204 degrees or departure-from-nucleate-boiling below 1.3, and the design is rejected outright; the FOM returns minus infinity. You don't tune the formula, you fix the reactor. **Operating limits** — four — trigger a trip but aren't design failures. **Targets** — six — like the emergency planning zone or the seventy-two-hour grace period, are aspirational and earn score.
>
> [optional: show `safety_criteria.md`] Two things make this more than a list. One — it's machine-readable. The same YAML file feeds the safety chapter, the trip logic, and the scoring engine, so a number can never disagree with itself across documents. Two — every row carries a regulatory citation and a defense-in-depth level. I mapped all twenty-seven onto the five IAEA defense-in-depth levels, from 'prevent abnormal operation' down to 'mitigate radiological release.' That five-level map is exactly the structure the FER asks for in section 8.6.
>
> Day 1 also locked two design decisions: cladding is Zircaloy-4, the PWR standard, and enrichment follows Samira's three-zone core at roughly three percent average. The template's example numbers were just that — examples."

---

## 4. Day 2 — I&C architecture and sensors (2:00)

> "Day 2 built the nervous system. Two documents — an architecture and a sensor inventory.
>
> The architecture rests on six principles, each tied to a standard: defense in depth, redundancy, diversity, physical separation, the single-failure criterion, and fail-safe. The one to remember is **fail-safe, de-energize-to-trip**. The trip breakers are held closed by power. Lose power, lose air, lose signal — the rods drop. The safe state is the default. The accident we fear most, a blackout, *becomes* the protective action instead of defeating it.
>
> The system has **five layers**. Sensors at the bottom. Above them the Reactor Protection System — Class 1E, four divisions, two-out-of-four voting, dropping the rods. Then the ESFAS, firing the passive safety features. Then the non-safety control system that runs the plant day-to-day, including the cogeneration steam split to district heat and hydrogen. And on top, a **digital twin** — advisory only, read-only — that runs soft sensors and anomaly detection. The iron rule: information flows *upward only*. The control system and the twin can never command a safety action. There is no software path from the non-safety world into the safety world.
>
> Beside all of it sits the **Diverse Actuation System** — a deliberately different platform that backs up the protection system against a common-cause software failure.
>
> The inventory itself is **twenty-one channels**, fourteen safety-grade. Neutron flux in three overlapping ranges with no blind gap, temperature measured two ways for diversity, accident-qualified sensors for the seventy-two-hour passive phase. I cross-checked it against Day 1 — every observable safety limit has a sensor. That check caught a missing steam-generator pressure transmitter, which I added."

---

## 5. Day 3 — The block diagram (2:00)

> "Day 3 turned the architecture into a single picture. [display `ic/ic_block.png`]
>
> Reading rule: red is safety-grade Class 1E, blue is non-safety control, grey is the advisory twin, yellow is the physical plant.
>
> [point top] Sensors at the top — flux, temperature, pressure, flow, level, radiation, steam-generator pressure.
>
> [point BUS] They feed this distribution bus. I drew it as one node on purpose — the honest picture is each sensor feeding four independent divisions, twenty-eight wires, unreadable. The bus says 'four divisions A through D' and keeps it legible.
>
> [point red cluster] Into the Class 1E block: the protection system with its voter and trip breakers, the ESFAS, and the diverse actuation system.
>
> [trace down to plant] Follow the protection path — the voter trips the breakers, the breakers *cut power* to the rod drives, and the rods fall by gravity into the core.
>
> [point left] The control system and the twin only receive sensor data through **one-way devices** — a qualified isolator into control, a physical data diode into the twin. That dashed advisory line to the operator screen is the only thing the twin can do — inform, never command.
>
> [point right] And this hardwired manual box: even with digital I&C everywhere, the operator's scram button is wired straight to the breakers, independent of every computer. If all the software froze, a human can still trip the reactor by hand.
>
> That one diagram answers the FER's explicit demand: show how protective actions are derived from monitored variables and logically combined."

---

## 6. Day 4 — Trips and the first event tree (2:30)

> "Day 4 closed the loop with two documents: the trip table and the first event tree.
>
> The **trip table** specifies thirteen reactor trips and five engineered-safety actuations. Each trip names its variable, its setpoint, its voting logic, its sensor channel, and — critically — the exact safety limit from Day 1 that it protects. High flux protects criticality. Low flow protects departure-from-nucleate-boiling. High pressure protects the vessel. I also added the permissives — the interlocks that block low-power trips during startup but can never block a trip that guards an active safety limit. The setpoints are flagged preliminary, because the final numbers come from OpenMC and OpenFOAM — but the logic is frozen.
>
> Then the **event tree**. [display `safety/event_tree_LOHS.png`] I chose Loss of Heat Sink, not the textbook Station Blackout, because it directly exercises our passive decay-heat removal — the thing that makes an integral PWR worth building.
>
> [trace top line] Read it left to right. The initiator: loss of feedwater. First question — does the reactor trip? Yes. Next — is emergency feedwater available? If yes, we're at stable hot standby, the green box. If not, does passive residual heat removal engage? If yes, passive cooldown to the in-containment tank — still safe. If that fails too, the tank plus passive containment cooling carry us past seventy-two hours.
>
> [point CD boxes] Only when *three independent systems fail in series* do we reach core damage — the red boxes. The bottom branch is the unlikely case where the reactor fails to trip at all, an ATWS, backed up by the diverse actuation system.
>
> [point sequence table region] The key result: every core-damage path requires at least two independent failures. No single failure causes core damage. The per-initiator core-damage frequency comes out around one-in-a-hundred-million per year — an order of magnitude below our plant target, leaving budget for the other initiators we'll add in week two. That redundancy-and-necessity analysis is, again, exactly what FER section 8.6 requires."

---

## 7. The golden thread (1:30)

> "Now step back, because this is the point of the whole week. [if slides: show a one-line chain]
>
> Take one limit — departure from nucleate boiling, must stay above 1.3, or the fuel burns. Follow it through the week's documents:
>
> It's **row `mdnbr_steady`** in the safety table, tagged hard constraint, citing the NRC standard review plan.
> It's **observed** by the primary-flow and temperature sensors, channels eight, four, and five in the inventory.
> It's **protected** by the low-flow trip, two-out-of-four, in the trip table.
> It's **tested** in the event tree — loss of flow is one of the demands on the protection system.
> And it's **scored** by a target-Gaussian normalizer that rewards margin above 1.3, feeding the FOM.
>
> Five documents, one limit, no contradictions. That traceability — limit to sensor to trip to scenario to score — is the deliverable. Any judge can pick any safety claim we make and follow it back to an IAEA or NRC page. Other teams can re-derive our numbers. We could not re-derive theirs. That reproducibility is our moat."

---

## 8. How I know it's right (1:00)

> "I didn't just write these and hope. After Day 3 I ran a senior-level self-review and caught real defects — a contradiction where I'd called feedwater 'passive pumps' when pumps aren't passive, a subsystem drawn but never described, and a channel count that disagreed between two documents. Fixed all of them.
>
> Then after Day 4 I ran a full cross-artifact audit — machine-checked that every sensor reference resolves, every trip links to a real limit, every pressure and temperature setpoint sits in the right order, and the event-tree end-states match the sequence table. That audit caught three more: a fuel limit not linked to its trip, the steam-generator pressure channel only half-wired, and — the subtle one — a core-damage-frequency budget where a single accident was consuming the entire plant target. All three corrected.
>
> The reason I'm listing this: in a safety submission, an internal contradiction is the first thing a reviewer attacks. These documents have been adversarially checked against themselves before anyone else sees them."

---

## 9. Decisions, open items, and asks (1:00)

> "Decisions locked this week: Zircaloy-4 cladding, three-zone enrichment per Samira's model, Loss of Heat Sink as the lead accident, emergency feedwater is gravity-driven and genuinely passive.
>
> Open items I'm carrying:
> — The **soluble-boron question**. Samira's materials show pure water, no boron. If we're boron-free, the rods alone carry all the shutdown margin and the diverse actuation system gets more weight. This decides part of the event tree, so I need it confirmed.
> — **Final setpoints** wait on OpenMC and OpenFOAM results.
> — And a process point: everything cites US and IAEA standards right now. For this competition we should add the Turkish regulator, NDK, as the primary basis — that's free credit on the domesticity score.
>
> My asks: Samira, the reactivity coefficients and the boron answer. OpenFOAM, the first hot-channel result for departure-from-nucleate-boiling. Energy and layout teams, your output numbers for the FOM. Supervisor, the ten sign-offs that set the final scoring weights."

---

## 10. FER fit and what's next (0:30)

> "Where this lands in the report: Day 1 is section 8.5, Day 4's event tree is section 8.6, Days 2 and 3 are section 8.7. All drop-in ready, all cited.
>
> Next: the FOM template — the single file every team writes their numbers into, with a validator that screams when a value is missing. That's the piece that turns five separate workstreams into one score. After that, week two: a second event tree, the safety-systems design detail, and plugging in the first real simulation numbers as they land. That's the week. Questions?"

---

## Backup — likely questions

**Q: "Five documents is a lot — is this over-engineered for a student competition?"**
> "The volume is in the working files; the FER drop-in is compressed to about fifteen pages across three sections. The structure is what wins — most teams keep numbers in three places that drift apart. Ours can't."

**Q: "What's the single weakest point right now?"**
> "Setpoints and reliability data — both flagged preliminary, both waiting on simulation and PRA data. The *logic* is frozen; the *numbers* will firm up. I'd rather show honest placeholders than invented precision."

**Q: "Why Loss of Heat Sink and not Station Blackout?"**
> "Both matter; LOHS is first because it exercises passive decay-heat removal, which is the integral-PWR's whole pitch. SBO is the second tree, week two."

**Q: "How does the digital twin help if it can't control anything?"**
> "Decision support and predictive maintenance without touching safety qualification. It tells the operator *why* a parameter is drifting before the alarm trips. Keeping it advisory is exactly what lets us use modern machine learning without years of safety-software licensing."

**Q: "What happens to all this when the design changes?"**
> "That's the point of the machine-readable spine. Change a number in one YAML file and the safety chapter, the trip setpoints, and the FOM score all update from it. One edit, no transcription, no drift."

**Q: "Is the core-damage frequency credible?"**
> "It's preliminary — reliability data is pending. But the *structure* is sound: every core-damage path needs at least two independent failures, and no single initiator consumes the plant budget. The number will move; the architecture won't."

---

*End of Week 1 report. Companion daily briefs: `MB_D1.md`, `MB_D3.md`. Next: FOM template + `MB_W2`.*
