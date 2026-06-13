# Critical Piping Table — FER §8.10 R6

*Owner: Azamhon · 2026-06-13. Sizes harvested from the FER draft Table 8.10-2
(`docs/FER_Aegis40_8.8-8.10.docx`) — closes the R6 gap that was blocked on pipe NPS.
Status tag `[FER-DRAFT]` = stated in the draft, pending Adilbek's hydraulic
confirmation; routing per layout r2 (TB adjacent to NI, zones.md Z7).*

| # | Line | Size | Design T/P | Route | Code class | Layout drivers | Status |
|---|---|---|---|---|---|---|---|
| 1 | Main steam (MSL) | **2 × DN250** | ~315 °C / 5.8 MPa | RXB → TB, below-grade tunnel, ~47 m | ASME III Cl. 2 | MSIVs inside RXB ≤1.5 m of penetration; whip restraints ≤3 m; redundant trains ≥3 m apart; common corridor feeds turbine + TES + SOE take-offs | `[FER-DRAFT]` |
| 2 | Main feedwater (FWL) | **2 × DN200** | ~220 °C / 6.5 MPa | TB → RXB, co-routed with MSL | ASME III Cl. 2 | MFIVs at RXB boundary; thermal sleeve at RPV nozzle; RC dividing wall from MSL in tunnel | `[FER-DRAFT]` |
| 3 | TES charging branch | branch off MSL header | ~280 °C / 1.5 MPa | steam header → TES (pass-out, peak hours) | ASME B31.1 | isolation valves at TES inlet; short run within island | `[FER-DRAFT]` |
| 4 | SOE steam branch | branch off header | deaerator-inlet steam | header → SOE (off-peak) | ASME B31.1 | isolation + flow control; H₂ side separated per NFPA 2 | `[FER-DRAFT]` |
| 5 | Decay heat removal (DHRS/PRHR) | **2 × DN100** | 343 °C / 15.5 MPa | intra-RXB: RPV ↔ DHRS HX in pool/IRWST | ASME III Cl. 1 | fully passive, no active valves, **no containment penetration** | `[FER-DRAFT]` |
| 6 | Passive ECCS injection | **2 × DN80** | 15.5 MPa design | intra-RXB: IRWST → RPV | ASME III Cl. 1 | gravity-driven; no pump penetrations | `[FER-DRAFT]` |
| 7 | Pressurizer surge line | — | — | — | — | **ELIMINATED** — integral pressurizer internal to RPV upper head | by design |
| 8 | Condenser circ water | TBD (large-bore, ~82 MWth @ ΔT≈8–10 K → ~2–2.5 m³/s seawater) | ~20–30 °C / low P | seawater intake → TB condenser → discharge (once-through, **C2 resolved 2026-06-13**) | B31.1 | route + sizing with intake/discharge structures; biofouling + thermal-discharge limits at Sinop | ◐ size TBD |

**Penetration note (draft §8.10.6):** MSL + FWL exit the RXB through dedicated,
missile-protected, double-walled penetrations with annular leak-off monitoring;
pipe-whip zones confirmed not to impact safety SSCs.

**Follow-ups:**
1. Adilbek: confirm/own the DN values (flow-velocity check at 26 kg/s steam per PFD).
2. Swap `[ASSUMED]` line weights on `site_plot_plan.svg` + viewer for the real 2×DN250 / 2×DN200 once confirmed.
3. Row 8 waits on the heat-sink decision (audit C2).
