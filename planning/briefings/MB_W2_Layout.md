# Week 2 Report — Facility Layout + Auxiliary Systems

**Week:** 2026-W23 (2026-06-02 → 06-08)
**Owner:** Azamhon
**Scope:** FER §8.10 Facility Layout · §8.8 Auxiliary Systems Design (scope taken on from Elbek)
**Audience:** full team + supervisor review
**Duration:** ~10 min spoken — **complete script below**
**Artifacts (all in repo, `layout/`):**
`zones.md` · `building_list.md` · `block_layout.{mmd,png}` · `flow_arrows.{mmd,png}` · `aux_systems.md` · `fer_8_10_coverage.md`
Plan: `planning/W2_Layout_Plan.md`

---

## How to use this file

`>` blocks = spoken verbatim. `[...]` = stage directions (what to show). Target ≈ 10 min + Q&A.

---

## 0. Timing map

| § | Content | Time |
|---|---|---|
| 1 | What this week's job is | 1:00 |
| 2 | The week in one sentence | 0:30 |
| 3 | The three-island scheme (show zones) | 2:00 |
| 4 | Building list — every box has a number | 1:30 |
| 5 | Block + flow diagrams (on screen) | 1:30 |
| 6 | Auxiliary systems + the power chain | 2:00 |
| 7 | How I know it holds together (audit) | 1:00 |
| 8 | Open items + asks | 0:30 |
| | **Total** | **~10:00** |

---

## 1. What this week's job is (1:00)

> "Last week was the nervous system — safety limits and the I&C that enforces them. This week is the **skeleton**: where everything physically stands. I took on the facility layout and auxiliary systems — FER sections 8.10 and 8.8.
>
> Layout is the integration drawing. Every team's output eventually takes up floor space. The core Samira designs needs a building; the turbine Alisher's energy cycle drives needs a hall; the hydrogen plant needs somewhere it can't blow up the reactor. My job this week was to give each one a defensible place to stand — and to make every distance on the site map trace back to a number, not to aesthetics."

---

## 2. The week in one sentence (0:30)

> "In one sentence: I split the site into three islands separated by physics — radiation, seismic load, and hydrogen explosion distance — gave all fourteen buildings a footprint and a seismic class, and wrote up the eight auxiliary systems that keep them alive. Five deliverables, all complete, audited against seventeen FER sub-requirements."

---

## 3. The three-island scheme (2:00)

> "[show `zones.md` ASCII map or `block_layout.png`] The site is three islands.
>
> **Nuclear Island** — reactor, auxiliary building, control room, spent fuel, diesels, radwaste. Everything whose failure could release radioactivity, or whose job is to prevent one. Seismic Category I throughout, qualified to 0.3 g — that's the safe-shutdown earthquake from my safety table. Reactor sits below grade for seismic and aircraft-impact protection.
>
> **Conventional Island** — turbine, generator, switchyard, cooling. Steam and high voltage, but zero radioactive inventory. Category II. About twenty metres of buffer to the nuclear island, with the steam and feedwater lines crossing in a controlled trench.
>
> **Industrial Island** — this is the Aegis-40 originality lever. Thermal storage for district heat, solid-oxide electrolysers for hydrogen. And it sits **one hundred metres** from the nearest safety building. That number isn't taste — it's NFPA 2, the hydrogen code. A hydrogen leak plus ignition is a deflagration, and distance is the cheapest mitigation there is. When Alisher sizes the hydrogen inventory we may tighten it, but a hundred metres is the conservative bound today.
>
> Four constraints set the whole partition: the half-kilometre emergency planning zone from my safety table, the 0.3 g seismic load, the containment isolation paths from my I&C work, and that hydrogen stand-off. Every island boundary traces to one of them."

---

## 4. Building list — every box has a number (1:30)

> "[show `building_list.md`] Fourteen buildings, five infrastructure items. Each one carries a footprint, a height, a seismic class, and a source.
>
> The constraint that sets everything is the reactor pressure vessel — 2.44 metres outer diameter, about 4.8 metres tall with the heads, straight from Samira's OpenMC geometry file. That drives the reactor building, which drives the crane, which drives the height. The transformer is sized off 40 megawatts electric — fifty MVA covers export plus house load. The spent-fuel pool is sized for a full core offload plus ten cycles.
>
> Where I'm waiting on a teammate, the number is tagged — TES and electrolyser footprints are flagged for Alisher, the cooling tower is an assumption pending the supervisor's heat-sink call. Nothing is invented and left unlabelled. Built area is about 9 300 square metres; the whole site fits comfortably inside the half-kilometre planning zone on a ten-hectare plot."

---

## 5. Block + flow diagrams (1:30)

> "[show `block_layout.png`] This is the 2D block layout — three islands, colour-coded, with six labelled connections between systems. It's schematic, not yet metric-scale; the scaled drawing and a 3D view are next week.
>
> [show `flow_arrows.png`] And this is the same site as a process-flow view — six streams leaving the reactor: steam and feedwater to the turbine, electricity to the grid, district heat and hydrogen out of the industrial island, fuel handling and radwaste internally. The point of this view is that no arrow is an orphan — every flow starts and ends at a building that exists in the list."

---

## 6. Auxiliary systems + the power chain (2:00)

> "[show `aux_systems.md`] FER 8.8 wants the support systems — eight of them. Ventilation, fire protection, radiation monitoring, emergency power, normal electrical, fuel handling, fission-product release control, and the service utilities. Each one gets the same six fields the FER demands: purpose, operating principle, where it lives, whether it has a safety function, its performance, and how you maintain it.
>
> The one worth saying out loud is **power**, because it ties back to last week's passive-safety decisions. The chain is: grid, then onsite generator, then the two emergency diesels, then the Class 1E batteries — and then **nothing**. The design ends in 'no power needed,' because the core cooling is passive — gravity feedwater, passive decay-heat removal, the seventy-two-hour grace window. So emergency power here isn't keeping the core alive; it's keeping the *monitoring* alive while the passive systems do the work. That's a genuinely different power philosophy from a conventional PWR, and it's a defensible originality point.
>
> Ventilation is the other safety-relevant one — a negative-pressure cascade so air always flows toward the filters, never out a crack, with HEPA and charcoal before the stack. The detailed P&IDs and the formal electrical single-line are flagged for week 3 — the structure's there, the drawings aren't yet."

---

## 7. How I know it holds together (audit) (1:00)

> "[show `fer_8_10_coverage.md`] I ran the same line-by-line audit I did on the I&C work. Seventeen FER sub-requirements across 8.10 and 8.8. Seven fully met, eight partial-or-deliberately-deferred, two genuine gaps — the structural weight and steel-tonnage tables, which need a foundation engineer and per-building mass takeoffs we don't have. I did **not** fabricate weights to fill those.
>
> Zero hard defects — nothing physically wrong, unlike last week where the audit caught an inverted cybersecurity model. I found three minor consistency drifts — a built-area-versus-envelope ambiguity, a 20-centimetre disagreement on vessel height, and a 'borated pool' wording that brushes against our boron-free decision. First two are already fixed. The cross-checks all pass: no orphan buildings, every footprint sourced or tagged, the hundred-metre hydrogen stand-off honoured identically across all four documents."

---

## 8. Open items + asks (0:30)

> "Three asks. **Samira** — confirm the vessel envelope and, critically, the fuel-assembly count; my 2D source shows 21, the FER example shows 240, and that swings the reactor building size hugely. **Alisher** — TES and electrolyser footprints, and the hydrogen inventory so I can tighten the stand-off. **Supervisor** — inland versus coastal site, which decides cooling tower versus seawater. Until those land I've proceeded on documented assumptions, all tagged as obvious swap targets. Week 3 is the scaled 2D plan, a 3D view, and the critical-piping table once Adilbek sends pipe sizes."

---

## 9. FER fit + what's next

- **FER sections answered:** §8.10 R1–R3 ✓, R4–R6 flagged W3; §8.8 A1–A3 ✓, A4–A5 (drawings) flagged W3.
- **Pages in FER:** layout ≈ 6–10 pp.
- **Next week (W3):** scaled 2D plan, isometric/3D, critical-piping table (Adilbek input), per-system P&IDs, structural-weight table (foundation engineer).

---

*End of W2 briefing. Artifacts in `layout/`. Audit: `layout/fer_8_10_coverage.md`. Plan: `planning/W2_Layout_Plan.md`.*
