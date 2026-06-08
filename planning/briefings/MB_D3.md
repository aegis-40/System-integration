# Meeting Brief — Days 2–3 (I&C System Design)

**Date:** 2026-05-27 → 28 (W1, Days 2–3)
**Owner:** Azamhon (3S Safety / I&C / FOM)
**Audience:** team standup / supervisor
**Duration:** 5–10 min spoken — **full script below**
**Artifacts:** `ic/ic_architecture.md`, `ic/sensor_inventory.md`, `ic/ic_block.mmd`, `ic/ic_block.png`
**Maps to:** FER §8.7 (Instrumentation and Control System Design)

---

## How to use this file

Everything in **>** blocks is spoken verbatim. Bracketed `[...]` are stage directions (what to point at / click). Timing target per section is in the right margin of §0. Total ≈ 8 min + 1–2 min questions.

---

## 0. Timing map

| Section | Content | Time |
|---|---|---|
| 1 | Where we are | 0:30 |
| 2 | What I built (Day 2) | 1:00 |
| 3 | Six design principles | 1:30 |
| 4 | The five layers + DAS | 1:30 |
| 5 | Sensor inventory | 1:00 |
| 6 | **Walk the block diagram** | 2:00 |
| 7 | Decisions + fixes | 0:30 |
| 8 | FER fit + tomorrow | 0:30 |
| | **Total** | **~8:30** |

---

## 1. Where we are (0:30)

> "Day 1 I locked the safety criteria table — the 27 limits the plant must respect. Days 2 and 3 I built the system that *watches* those limits and *acts* when they're approached: the Instrumentation and Control system. This is FER section 8.7. I have three artifacts to show you — an architecture document, a sensor inventory, and a block diagram I'll walk through on screen. The headline: every safety limit from Day 1 now has a sensor that observes it and, where needed, a trip that protects it."

---

## 2. What I built — Day 2 (1:00)

> "The architecture document answers the question the FER asks directly: how do we manage the reactor safely under normal *and* accident conditions. It does that in three parts. First, the design principles — the rules every wire in the plant obeys. Second, the layered architecture — five layers from sensors up to the digital twin. Third, the sensor inventory — twenty measurement channels, each one specified down to type, range, redundancy, and what it feeds.
>
> The single most important idea in the whole document is this: **information flows upward only.** Sensors feed the protection system and the control system. But the control system and the digital twin can *never* reach back down and command a safety action. There is no software path from the non-safety world into the safety world. That one rule is what keeps a cyberattack or a software bug in the control system from ever defeating the reactor trip."

---

## 3. Six design principles (1:30)

> "Six principles, each tied to a standard. I'll go fast.
>
> One — **defense in depth.** The I&C functions are split across five levels so that control and protection never share a failure. Same idea as the physical defense-in-depth from Day 1, applied to electronics.
>
> Two — **redundancy.** Every safety-critical measurement has four independent channels with two-out-of-four voting. That survives one channel failing *and* one channel out for maintenance at the same time.
>
> Three — **diversity.** The same parameter is measured by different sensor technologies. Temperature by resistance detectors *and* thermocouples. Flow by venturi *and* ultrasonic. So a flaw in one technology can't blind us.
>
> Four — **physical separation.** The four channels run in separate cable trays behind rated barriers. A fire or a flood can't take all four.
>
> Five — **single-failure criterion.** No single failure — electrical, mechanical, software, or human — stops a safety function. The two-out-of-four logic delivers this in both directions: it trips when it should, and it doesn't spuriously trip when one channel lies.
>
> Six — and this is the elegant one — **fail-safe, or de-energize-to-trip.** The trip breakers are held *closed by power*. Cut the power, lose the signal, lose instrument air — the rods drop. The safe state is the default state. The FER explicitly demands this: the plant must go safe on loss of power or air. We get it for free from the wiring philosophy."

---

## 4. The five layers plus DAS (1:30)

> "Now the architecture itself. Five layers, bottom to top.
>
> **Layer 1 — field instrumentation.** The sensors. Neutron flux, temperatures, pressures, flow, level, radiation.
>
> **Layer 2 — the Reactor Protection System, the RPS.** Class 1E, hardwired, four divisions. It compares each measurement to a setpoint and, on a two-out-of-four vote, drops the control rods. This is the scram path.
>
> **Layer 3 — the ESFAS**, the Engineered Safety Features Actuation System. Same four-channel logic, but instead of scramming it fires the *passive* safety systems — safety injection, containment isolation, emergency feedwater, passive residual heat removal.
>
> **Layer 4 — the DCS**, the Distributed Control System. Non-safety. This is what runs the plant day to day — rod positioning, pressurizer control, feedwater, turbine, and the cogeneration steam split to district heat and hydrogen.
>
> **Layer 5 — the digital twin.** Advisory only, read-only. It mirrors every sensor into a live model of the plant, runs soft sensors for things we can't measure directly like margin-to-boiling, flags anomalies before alarms trip, and predicts maintenance. It cannot touch a single valve. This layer is our originality lever for FER section 5 — modern operator decision support without compromising the safety qualification underneath.
>
> And sitting beside all of that — the **Diverse Actuation System, the DAS.** It's a deliberate paranoia device. Suppose a software bug is hiding in all four RPS divisions at once — a common-cause failure. The DAS is built on a *different* platform by a *different* team, watches the two most important signals — neutron flux and pressurizer pressure — and provides a completely independent backup path to trip the reactor. The regulators require it for digital protection systems, and I added it after review on Day 3 because the first draft had it in the diagram but never described."

---

## 5. Sensor inventory (1:00)

> "The inventory is twenty-one channels. Fourteen are safety-grade Class 1E, seven are control-only. Seven of them run the two-out-of-four voting.
>
> A few highlights. Neutron flux is covered in three overlapping ranges — source, intermediate, and power — so we have continuous coverage from cold shutdown all the way through twenty-five percent overpower, with no blind gap. Temperature is measured two ways for diversity. Core-exit thermocouples are qualified to survive an accident and keep reporting for the seventy-two-hour passive grace period.
>
> The key discipline point: I cross-checked the inventory against Day 1. **Every safety criterion now has at least one sensor that observes it.** That cross-check caught a gap — we had no steam-generator pressure transmitter — so I added it as channel twenty-one. The inventory also lists five more planned additions, including a containment hydrogen monitor for severe-accident monitoring."

---

## 6. Walk the block diagram (2:00)

> "Let me put the block diagram up. [display `ic/ic_block.png`] One reading rule first: **signals flow downward in this drawing, and the red boxes are safety-grade Class 1E.** Blue is non-safety control. Grey is the advisory twin. Yellow is the physical plant.
>
> [point top] At the **top** are the seven sensor groups — flux, temperature, pressure, flow, level, radiation, and steam-generator pressure.
>
> [point to BUS node] They feed into this one node — the **safety signal distribution bus**. I drew it this way on purpose. Each sensor actually feeds four independent divisions, so the honest picture is twenty-eight wires. That's unreadable. The bus node says 'hardwired, four divisions A through D' and lets the diagram breathe.
>
> [point to red CLASS 1E cluster] From the bus, signals fan into the **Class 1E block** — three things live here. The **RPS**: four divisions, the two-out-of-four voter, and the trip breakers. The **ESFAS**: its own voter firing the passive safety features. And the **DAS** off to the side — the diverse backup I mentioned.
>
> [trace TB → CRD → RX] Follow the protection path: voter trips the breakers, the breakers *interrupt power* to the control rod drives, and the rods fall into the core by gravity. De-energize to trip — the safe direction is the no-power direction.
>
> [point left side] Now the **non-safety side**. Notice the sensors also feed left — but only through this **qualified isolation** node, a one-way device, into the DCS. And they feed the digital twin only through a **data diode** — physically one-way, no return path. That's the upward-only rule made visible. The twin's output goes to the operator screen as *advisory only* — see the dashed line — never to a control loop.
>
> [point far right MANUAL box] This red box is the **hardwired manual controls**. Even with digital I&C everywhere, the operator's scram button and the manual safety actuations are hardwired straight to the breakers — independent of any computer. If every processor in the plant froze, the operator can still trip the reactor by hand.
>
> [trace DAS dashed lines] And these dashed 'diverse backup' lines from the DAS to the rods and the safety features — that's the anti-common-cause path. If the whole RPS is compromised, the DAS still gets us to safe shutdown.
>
> So in one picture: sensors at top, protection in the red middle, control and twin isolated on the sides, plant at the bottom, and a human with a hardwired button who can always override. That's the whole I&C story, and it directly answers the FER requirement to show *how protective actions are derived from monitored variables and logically combined*."

---

## 7. Decisions and fixes (0:30)

> "Three things I corrected after a self-review of the two days.
>
> One — I'd written 'auxiliary feedwater pumps, passive' — which is a contradiction, pumps aren't passive. Renamed to **Emergency Feedwater**, gravity-driven from an elevated tank, no pumps. Consistent everywhere now.
>
> Two — the DAS existed in the diagram but had no description. **Now fully written up** with its standards basis.
>
> Three — the architecture text said thirteen channels, the inventory listed twenty. **Reconciled to twenty.** Small things, but in a safety document an internal contradiction is the first thing a reviewer pounces on."

---

## 8. FER fit and tomorrow (0:30)

> "Why this is FER-ready. The architecture document maps one-to-one onto the section 8.7 checklist — architecture, sensors, HMI ergonomics, redundancy, diversity, separation, secure communications. The block diagram satisfies the explicit requirement for a diagram showing how trips derive from monitored variables. And every standard is cited.
>
> Tomorrow, Day 4, I close the loop: the **trip signals table** — exact setpoints and voting for each trip — and the **first event tree**, loss of heat sink, showing the I&C and the safety systems working together through an accident. Both build directly on what's on this screen.
>
> One ask: I still need confirmation on whether the design uses soluble boron, because that decides how much shutdown margin the rods alone must provide — and that flows straight into the trip logic I'm writing tomorrow. That's it."

---

## Backup — likely questions

**Q: "Why a digital twin if it can't do anything?"**
> "Decision support and predictive maintenance without touching safety qualification. It tells the operator *why* a parameter is drifting before the alarm. It's an advisory copilot, not a controller — and keeping it advisory is exactly what lets us use modern machine learning without a multi-year safety-software licensing burden."

**Q: "Isn't four channels expensive for a small reactor?"**
> "Two-out-of-four is the standard for safety-grade PWR protection. We could argue two-out-of-three for some channels to cut cost, but four buys us trip-on-failure *and* no-spurious-trip while a channel is out for maintenance. For an iPWR selling on safety, that margin is the product."

**Q: "What's the weakest part right now?"**
> "The setpoints. The diagram shows *that* a trip happens; tomorrow's table fixes *at what value*. Those numbers need OpenMC and OpenFOAM results to be final — today they're engineering placeholders."

**Q: "Why de-energize-to-trip and not energize?"**
> "Because the failure we fear most is loss of power in an accident. If the trip needs power to fire, a blackout disables your protection exactly when you need it. De-energize-to-trip inverts that: the blackout *is* the trip."

**Q: "Are these domestic components?"**
> "Mixed. Resistance detectors, pressure transmitters — domestic suppliers exist. Neutron detectors and fission chambers are specialist, likely imported. I've flagged a sourcing matrix as a to-do for the domesticity section, 5.2."

---

*End of briefing. Companion artifacts in `ic/`. Next: `MB_D4` after trip signals + event tree.*
