# Critical Piping Table — FER §8.10 R6

*Owner: Azamhon · 2026-06-13. Sizes harvested from the FER draft Table 8.10-2
(`docs/FER_Aegis40_8.8-8.10.docx`) — closes the R6 gap that was blocked on pipe NPS.
Status tag `[FER-DRAFT]` = stated in the draft, pending Adilbek's hydraulic
confirmation; routing per layout r2 (TB adjacent to NI, zones.md Z7).*

| # | Line | Size | Design T/P | Route | Code class | Layout drivers | Status |
|---|---|---|---|---|---|---|---|
| 1 | Main steam (MSL) | **2 × DN250** | ~315 °C / 5.8 MPa | RXB → TB, below-grade tunnel, ~47 m | ASME III Cl. 2 | MSIVs inside RXB ≤1.5 m of penetration; whip restraints ≤3 m; redundant trains ≥3 m apart; common corridor feeds turbine + TES + SOE take-offs | `[FER-DRAFT]` |
| 2 | Main feedwater (FWL) | **2 × DN200** | ~220 °C / 6.5 MPa | TB → RXB, co-routed with MSL | ASME III Cl. 2 | MFIVs at RXB boundary; thermal sleeve at RPV nozzle; RC dividing wall from MSL in tunnel | `[FER-DRAFT]` |
| 3 | TCES charging branch | branch off MSL header | ~280 °C / 1.5 MPa | steam header → **TCES zeolite-13X bed** (dehydration/charge, off-peak surplus heat) | ASME B31.1 | isolation valves at bed inlet (Req 35 set); short run within energy island; charge diverts surplus reactor heat so the reactor stays near-baseload (load-following) | `[FER-DRAFT]` (TCES, C3 resolved) |
| 4 | SOE steam branch | branch off header | deaerator-inlet steam | header → SOE (off-peak) | ASME B31.1 | isolation + flow control; H₂ side separated per NFPA 2 | `[FER-DRAFT]` |
| 5 | Decay heat removal (DHRS/PRHR) | **2 × DN100** | 343 °C / 15.5 MPa | intra-RXB: RPV ↔ DHRS HX in pool/IRWST | ASME III Cl. 1 | fully passive, no active valves, **no containment penetration** | `[FER-DRAFT]` |
| 6 | Passive ECCS injection | **2 × DN80** | 15.5 MPa design | intra-RXB: IRWST → RPV | ASME III Cl. 1 | gravity-driven; no pump penetrations | `[FER-DRAFT]` |
| 7 | Pressurizer surge line | — | — | — | — | **ELIMINATED** — integral pressurizer internal to RPV upper head | by design |
| 8 | Condenser circ water (once-through seawater) | large-bore, ~70–82 MWth @ ΔT≈8–10 K → **~2–2.5 m³/s seawater** | ~8–25 °C (Black Sea, Sinop) / low P | **seawater intake (INTK) → CWP → TB condenser → outfall (OUTF)**, once-through (**C2 resolved 2026-06-13**) | B31.1 | INTK/OUTF shoreline structures; CWP house on-island; biofouling/chlorination; thermal-discharge ΔT under Turkish SKKY `[VERIFY-SKKY]`; NORMAL sink only (safety UHS independent) | ◐ velocity/NPS with Adilbek |
| 9 | Component cooling water (CCWS) final rejection | per CCWS duty | low | CCWS HX → **seawater** (once-through), normal sink | B31.1 | non-safety final rejection; SFP/aux loads have passive long-term grace independent of CCWS | ◐ `[ADILBEK]` |

**Penetration note (draft §8.10.6):** MSL + FWL exit the RXB through dedicated,
missile-protected, double-walled penetrations with annular leak-off monitoring;
pipe-whip zones confirmed not to impact safety SSCs.

**Follow-ups:**
1. Adilbek: confirm/own the DN values (flow-velocity check at 26 kg/s steam per PFD) + the seawater circ-water NPS (rows 8–9).
2. Swap `[ASSUMED]` line weights on `site_plot_plan.svg` + viewer for the real 2×DN250 / 2×DN200 once confirmed.
3. ~~Row 8 waits on the heat-sink decision (audit C2).~~ **C2 resolved — once-through seawater; rows 8–9 reflect it.** Row 3 reflects C3 (TCES).
