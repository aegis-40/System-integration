# safety/ — FER §8.5 Safety Criteria + §8.6 Safety Systems

| File | FER section | Description |
|---|---|---|
| `safety_criteria.yaml` | §8.5 | **Source of truth.** 32 numeric criteria (21 hard / 4 op / 7 target), 8 categories, DiD-mapped. |
| `regulatory_alignment_audit.md` | §8.5 | **2026-06-15 audit + resolutions** vs SSR-2/1, SSG-52, TECDOC-1936, NUREG-1431. A/B/C resolved (EBIS, cogen isolation, DEC framework); D (peaking) flagged + de-peak path. |
| `hazards_register.md` | §8.5/§8.6 | Internal + external hazards register (SSR-2/1 Req 17) — fire/flood/missile/seismic/aircraft + combinations. |
| `safety_criteria.md` | §8.5 | Human-facing render of the YAML |
| `trip_signals.md` | §8.6 + §8.7 | 13 RPS trips + 6 ESF actuations (incl. EBIS diverse shutdown) + 4 permissives. Links each trip to a `safety_criteria` row. |
| `event_tree_LOHS.md` | §8.6 | First event tree — Loss of Heat Sink, 7 sequences (4 OK / 3 CD). Per-initiator CDF ~1e-8 /ry. |
| `event_tree_LOHS.png` | §8.6 | Rendered for FER drop-in |
| `event_tree_LOHS.drawio` | §8.6 | Editable draw.io source of the event tree (diagrams.net) |
| `event_tree_SBO.md` | §8.6 | Second event tree — Station Blackout, 5 sequences (3 OK / 2 CD). CDF ~1e-11 /ry: de-energize-to-actuate makes SBO negligible. |
| `event_tree_SBO.drawio` | §8.6 | Editable draw.io source of the SBO tree |
| `openmc_rev3_alignment.md` | §8.5 | rev_3 neutronics ↔ safety-criteria cross-check — 10/10 gates pass |
| `safeguards_nonproliferation.md` | §3S | Safeguards / non-proliferation case — reactor-grade, self-protecting, once-through discharge |

**Planned (W2+):** ~~SBO event tree~~ ✅ done 2026-06-13 · LOCA event tree (small-break only — LB-LOCA *and* rod ejection both eliminated by design), safety systems design narrative for §8.6.
