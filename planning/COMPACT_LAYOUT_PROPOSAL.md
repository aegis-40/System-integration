# Compact In-Line Layout — Detailed Proposal (for approval)

*Owner: Azamhon (layout). 2026-06-26. **PROPOSAL — not yet locked.** On approval this propagates into `zones.md`, `building_list.md`, the site drawings, CAD and the viewer, and closes open item **C1**.*

---

## 1. Design principles

1. **Single linear process spine** — the modern compact-SMR pattern (NuScale, Rolls-Royce SMR, BWRX-300). One straight steam/process corridor: fuel in at one end, electricity + heat + H₂ out the other.
2. **Descending hazard along the line** — Protected Area (nuclear) → Vital Area (turbine) → non-safety (cogen). Security and seismic class step *down* west-to-east; fences cross the spine cleanly.
3. **Shared structural walls** between adjacent spine buildings — the source of the construction saving.
4. **Flankers, not a campus** — transformers, generators and the remaining aux buildings sit immediately north/south of the spine, on short cable/pipe runs, instead of spread across a site.
5. **Safety separations preserved, not dropped** — seismic gap, H₂ stand-off, fire barriers, security tiers all kept (§4). The saving is geometric.

---

## 2. The spine (west → east)

A ~28 m-deep process band; buildings share walls along it. South face is the straight reference line; the main-steam header runs the length of the spine.

| Order | Building | Footprint (m²) | Seismic | Security | Role |
|---|---|---|---|---|---|
| 1 | **SFB — Storage** (fresh + spent fuel, transfer canal, SFP) | 25 × 18 = 450 | **Cat I** | Protected Area | fuel in/out; SFP grew for the 37-FA core |
| 2 | **RXB — Reactor Building** (RPV ~10 m × Ø3.25 m, **internal IRWST pool**, containment Ø15 m) | 25 × 25 = 625 | **Cat I** | Protected Area | the reactor; transfer canal connects west to SFB |
| — | *seismic gap ≥ 75 mm* (Cat I ↔ Cat II) | — | — | — | structural break |
| 3 | **TB — Turbine Building** (turbine, 40 MWe generator, condenser, FW) | 30 × 20 = 600 | Cat II | Vital Area | steam from RXB → electricity; condenser to seawater |
| 4 | **TCES** (thermochemical zeolite-13X store) | 30 × 30 = 900 | Cat III | non-safety | pass-out steam → district-heat storage / load-following |
| 5 | **SOE** (high-T electrolyser — H₂ *generation*) | 25 × 25 = 625 | Cat III | non-safety | steam → H₂; **production** on-line, **bulk storage** off-line (§4.1) |

**Spine length ≈ 145 m**, depth ≈ 28 m. Main steam: RXB → TB → (header continues) → TCES + SOE — one corridor, one penetration line.

---

## 3. Side buildings (flank the spine on short runs)

**North flank** (Cat I aux, kept inside the Protected Area near the reactor):

| Building | Footprint | Class | Position |
|---|---|---|---|
| **CB — Control Building** (MCR, I&C divisions A–D, switchgear, batteries) | 30 × 25 = 750 | Cat I | north of RXB — shortest 1E cable runs to the reactor |
| **AB — Auxiliary Building** (CVCS, sampling, demin, primary makeup) | 25 × 20 = 500 | Cat I | north of RXB; penetration interface |
| **WMB — Waste Management** (liquid/solid/gas radwaste, HEPA+charcoal, off-gas stack) | 25 × 15 = 375 | Cat I | north of SFB; off-gas stack on its roof |

**South flank** (toward the shoreline; power export + heat rejection):

| Building | Footprint | Class | Position |
|---|---|---|---|
| **DGB — Diesel Generators** (2× EDG, standby) | 15 × 10 = 150 | Cat I | south of RXB/CB, physically + electrically separated from the 1E divisions |
| **Switchyard + Main/Aux Transformers (EHB)** | 50 × 50 yard + 150 bldg | Cat II | south of TB — at the generator output |
| **CWP — Circulating-Water Pumps** | 20 × 12 = 240 | Cat III | south of TB, toward the shoreline intake/outfall |
| **WSB — Workshop / Service / Admin** | 20 × 15 = 300 | Cat III | off-line, SE periphery (non-radiological) |

**Shoreline (south):** seawater intake + outfall structures feed the CWP → TB condenser (short circ-water run, once-through, C2).

---

## 4. Safety separations — preserved

### 4.1 H₂ explosion stand-off — the one tension, solved by a corner offset

H₂ *production* (SOE) is on the spine tail, but **bulk H₂ storage is set back to the SE corner of the site, offset south of the line**, NOT in-line.

- RXB centre ≈ (X 40, Y 14). H₂ storage yard ≈ (X 130, Y −70).
- **RXB → H₂ distance ≈ √(90² + 84²) ≈ 123 m.**
- This **exceeds the 100 m conservative bound** and is far above NFPA 2's ≥60 m (for 5 000–15 000 kg). ✅

So the compact spine keeps its short runs while the H₂ stand-off is **fully satisfied** by offsetting the storage yard to the corner. (Final distance confirmed once Alisher sizes the H₂ inventory; if < 5 000 kg, even less is required.)

### 4.2 Other separations

| Separation | Kept how |
|---|---|
| Seismic Cat I ↔ Cat II | ≥ 75 mm seismic gap between RXB and TB (mid-spine structural break) |
| Security tiers | Protected-Area fence wraps SFB+RXB+CB+ARB+DGB; Vital-Area fence the TB; cogen tail standard industrial — fences cross the spine between blocks |
| Fire | 3 h rated fire walls at every shared-wall junction; RPS/ESFAS division barriers inside CB unchanged |
| Internal IRWST / passive UHS | inside RXB — unaffected |
| Turbine-missile orientation | TB long axis along the spine → missile trajectory misses the RXB (≥ 20 m + Cat-I RXB wall) |

---

## 5. Plan view (schematic, north up)

```
                                   N ▲
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │                                NORTH FLANK                                     │
  │     ┌───────────────┐      ┌───────────────────┐                              │
  │     │ ARB           │      │ CB  (MCR / I&C     │                              │
  │     │ aux + radwaste│      │ div A–D)  Cat I    │                              │
  │     │ Cat I  + stack│      └─────────┬─────────┘                              │
  │     └──────┬────────┘                │                                        │
  │ ═══════════╪═════════════════════════╪═══ Protected-Area fence ══╗            │
  │     ┌──────┴───────┬─────────────────┴──┐ ║ ┌────────┬──────────┬──────────┐  │
  │  W  │  STORAGE     │     REACTOR         │ ║ │TURBINE │  TCES    │  SOE     │ E│
  │     │  SFB  Cat I  │  RXB Cat I          │ ║ │ TB     │  Cat III │  (H₂     │  │
  │     │  (SFP)       │  + internal IRWST   │ ║ │ Cat II │  zeolite │  gen)    │  │
  │     └──────────────┴─────────────────────┘ ║ └───┬────┴──────────┴──────────┘  │
  │       └─ transfer canal ─┘      seismic gap ╝   Vital Area     non-safety     │
  │                                  ≥75 mm                                       │
  │              ┌──────┐            ┌───────────────┐                            │
  │              │ DGB  │            │ Switchyard +  │              ┌───────────┐ │
  │              │ EDG  │            │ Main Xfmrs    │   ┌──────┐   │ H₂ STORAGE│ │
  │              │ Cat I│            │ (50 MVA)      │   │ WSB  │   │ YARD      │ │
  │              └──────┘            └──────┬────────┘   └──────┘   │ (set back)│ │
  │   ┌── CWP ──┐                          │                       └───────────┘ │
  │   │seawater │   ◄═══ intake / outfall (shoreline) ═══►       ~123 m to RXB ↗  │
  │   └─────────┘                   SOUTH FLANK                                   │
  └──────────────────────────────────────────────────────────────────────────────┘
        ◄──────────── main-steam / process-heat corridor along the spine ────────────►
```

## 6. Elevation (along the spine, schematic)

```
   m │              ┌──RXB──┐                                          stack
  30 │              │ 30 m  │                                            │
     │   ┌─SFB─┐    │  +    │   ┌─TB─┐    ┌─TCES─┐  ┌SOE┐               │
  15 │   │15 m │    │ poolO │   │15 m│    │ 12 m │  │10m│               │
   0 ═══─┴─────┴────┤───────├───┴────┴────┴──────┴──┴───┴═══ GRADE ═════╧═══
     │   below-grade│ RPV   │  (TB on grade)
 -12 │   reactor    │~10 m  │
     │   cavity     │internal IRWST pool
```

---

## 7. Site envelope + the construction saving

| | Old 3-island | Compact spine |
|---|---|---|
| Arrangement | 3 separated islands across a campus | 1 linear spine + flankers |
| Site envelope | ~250 × 300 m | **~160 × 120 m** (much tighter) |
| Built area | ~8 800 m² | **~8 200 m²** (≈6–8 % saved via shared spine walls; AB + WMB kept separate per team) |
| Pipe/cable runs | island-to-island | spine-adjacent (shortest) |
| Construction | 3 fronts, spread excavation | **1 linear front** — cheaper to crane, sequence, grade |

Still comfortably inside the 500 m EPZ; the tighter envelope *helps* the small-EPZ story.

---

## 8. What this changes + C1 resolution

- **Closes C1** — the spine *is* the merged single-steam-corridor scheme (NI + combined Energy/Conventional), the FER docx's "two-island" option. The Industrial Island dissolves into the spine tail; the H₂ stand-off survives as the corner offset (§4.1).
- **AB + WMB kept separate** (team decision 2026-06-26) — saving comes from the linear packing + shared spine walls, not from merging buildings.
- **Files to update on approval:** `zones.md` (island scheme → spine; new decision row; close C1), `building_list.md` (adjacencies, ARB merge, shared-wall footprints), `layout/drawings/site_plot_plan.svg` + `site_elevation.svg`, `cad/build_aegis40_cad.py`, `site/index.html`, `fer_8810_docx_audit.md` (C1 resolved).

## 9. Open items (don't block the lock-in)

- **H₂ inventory (Alisher)** → final stand-off distance (123 m is the proposed bound; shrinks if inventory is small).
- **House-load MW** → aux-transformer rating.
- **Exact survey coordinates** → for the formal GA drawing (these are schematic representative positions).

---

## ❓ Approval requested

Before I lock this into the authoritative layout files + drawings, please confirm:
1. **Building order on the spine:** SFB → RXB → TB → TCES → SOE — OK?
2. **Merge AB + WMB into one ARB building** — OK, or keep them separate?
3. **H₂ bulk storage set back to the SE corner** (~123 m from RXB) — OK?
4. **Adopt this as the C1 resolution** (compact merged scheme) — OK?

Tell me which to adjust; otherwise I'll propagate it and close C1.
