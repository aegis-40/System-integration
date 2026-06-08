# safety/ — FER §8.5 Safety Criteria + §8.6 Safety Systems

| File | FER section | Description |
|---|---|---|
| `safety_criteria.yaml` | §8.5 | **Source of truth.** 27 numeric criteria (17 hard / 4 op / 6 target), 7 categories, DiD-mapped. |
| `safety_criteria.md` | §8.5 | Human-facing render of the YAML |
| `trip_signals.md` | §8.6 + §8.7 | 13 RPS trips + 5 ESF actuations + 4 permissives. Links each trip to a `safety_criteria` row. |
| `event_tree_LOHS.md` | §8.6 | First event tree — Loss of Heat Sink, 7 sequences (4 OK / 3 CD). Per-initiator CDF ~1e-8 /ry. |
| `event_tree_LOHS.png` | §8.6 | Rendered for FER drop-in |

**Planned (W2+):** SBO event tree, LOCA event tree, safety systems design narrative for §8.6.
