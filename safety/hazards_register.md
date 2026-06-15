# Internal & External Hazards Register — Aegis-40

*Source document. Supports FER §8.5/§8.6. Closes the SSR-2/1 Req 17 (internal & external
hazards) coverage gap from the 2026-06-15 regulatory-alignment audit.*
*Owner: Azamhon (3S). Date: 2026-06-15.*

---

## 1. Purpose

IAEA SSR-2/1 **Req 17 (§5.15A–5.22)** requires that internal and external hazards be
identified and that the design protect items important to safety against them, individually
and in credible combinations. This register consolidates the hazard list, screening
outcome, and the Aegis-40 design provision for each — previously scattered across
`zones.md` (seismic, H₂ stand-off), `aux_systems.md` (fire, flooding) and the I&C
separation basis.

Screening key: **CARRIED** = protected/analyzed; **SCREENED OUT** = not credible for this
design (with basis); **PENDING** = provision identified, analysis owed.

---

## 2. Internal hazards

| Hazard | Threat to safety | Aegis-40 provision | Status |
|---|---|---|---|
| Internal fire | CCF of redundant I&C divisions | 3 h fire barriers between RPS/ESFAS divisions A–D; clean-agent suppression in I&C/MCR; detection (`aux_systems.md` §3) | CARRIED |
| Internal flooding | submergence of safety equipment / divisions | division separation + drainage; safety equipment elevated above flood-up level; SFP/IRWST as bounded sources | PENDING — flood-up volume analysis |
| Internal missiles | turbine/pump fragments, pressurized-component failure | turbine oriented so missile trajectory misses NI; rotating equipment guarded; integral RPV reduces high-energy primary components | PENDING — turbine missile strike analysis |
| Pipe whip / jet impingement | secondary-side line rupture damaging safety SSCs | integral RPV eliminates large primary lines (LBLOCA practically eliminated, §8.6.1); secondary lines restrained + separated | CARRIED (primary) / PENDING (secondary restraints) |
| Heavy-load drop | fuel/cask handling over the pool or RPV | single-failure-proof handling machine; safe-load-path interlocks; no heavy load over irradiated fuel | CARRIED |
| Internal explosion (hydrogen) | H₂ in containment post-accident; SOE/TES H₂ on site | core-wide H₂ ≤ 1 % limit (`safety_criteria` `hydrogen_generation`); PARs/igniters [PENDING]; SOE H₂ stand-off (external, §3) | PARTIAL |
| Loss of support systems | loss of cooling/air/power to safety loads | fail-safe valves, passive ESF, 1E power (`aux_systems.md` §5, §9) | CARRIED |

## 3. External hazards

| Hazard | Aegis-40 provision | Status |
|---|---|---|
| Seismic (SSE) | design SSE ≥ 0.3 g; 1E equipment seismically qualified (IEEE 344); `safety_criteria` `sse_design` | CARRIED |
| External flooding / tsunami | site grade + dry-site concept; coastal seawater UHS intake protected [site-dependent] | PENDING — site flood hazard (ties to FER site selection) |
| Extreme wind / tornado / tornado missile | seismic Cat-I structures bound most wind loads; missile-resistant NI exterior | PENDING — tornado-missile spectrum |
| Aircraft hazard | compact, low-profile NI; below-grade/shielded RPV; small target | PENDING — aircraft-impact screening |
| Extreme ambient temperature | UHS + HVAC sized for site temperature extremes | PENDING — site envelope |
| External explosion / toxic gas | site stand-off; MCR habitability isolation (`aux_systems.md` §2) | PENDING — site hazard survey |
| Loss of off-site power (external) | de-energize-to-actuate → SBO benign for ≥72 h (SBO event tree, §8.6.3) | CARRIED |

## 4. Hazard combinations

Per Req 17, credible combinations are considered — notably **seismic + LOOP** (an
earthquake commonly causes grid loss): this is the design-basis case for the passive
chain, and is bounded by the SBO analysis (de-energization = actuation; ≥72 h grace with
no AC/DC/operator action). Seismic + internal fire and external-flood + LOOP are PENDING.

## 5. Aegis-40 screening advantages

The integral, compact, partially-below-grade design intrinsically reduces several hazard
classes: no large-bore primary piping (pipe whip / LBLOCA), small target footprint
(aircraft / external missile), large passive water inventories as benign bounded sources,
and de-energize-to-actuate safety systems (LOOP/SBO). These are the deterministic levers
that turn many Req 17 hazards into low-significance or screened-out items.

## 6. Open analyses (PENDING items above)

| # | Analysis | Owner | Ties to |
|---|---|---|---|
| H1 | Internal flood-up volume + equipment elevation | layout + safety | site grading |
| H2 | Turbine missile strike trajectory | BOP + layout | TB orientation |
| H3 | Secondary pipe-whip restraint layout | mechanical | piping table |
| H4 | Containment H₂ control (PAR/igniter) | safety | severe-accident (DEC-B) |
| H5 | Site external hazards (flood, tornado, aircraft, temp, explosion) | site/licensing | FER site selection |

Most external-hazard items are **site-dependent** and resolve once the FER site is fixed
(currently divergent — see `planning/FER_readiness_review_2026-06-13.md`).
