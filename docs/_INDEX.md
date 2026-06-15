# docs/ — source documents (read-only)

These are the inputs the project is built against. **Do not edit.** If a value here looks wrong, override it in our own design docs and note the deviation.

| File | What it is | Authority |
|---|---|---|
| `FER_Template.docx` | TEKNOFEST organizers' Final Evaluation Report template — 12 sections under §8, max 120 pages | binding format; Table 1 values are *illustrative*, not prescribed |
| `PER_NUClearly.pdf` | Preliminary Engineering Report — earlier project document containing the original wFOM formula in §5.1 | historical / starting point for FOM design |
| `SMR_booklet.pdf` | IAEA Advances in SMR Technology Developments 2022 — ~80 SMR designs incl. CAREM-25, SMART, NuScale VOYGR | reference data for FOM comparison |
| `tasks_w1.pdf` | Team's Week 1 task list (5 pages, one per scope: OpenFOAM, OpenMC, 3S/I&C/FOM, Energy/TES/SOE, Layout) | supervisor-assigned scope |

### `international_regulations/` — design standards (filenames scrambled vs content; identified by `pdftotext`)

| File | Actual standard | Use |
|---|---|---|
| `Safety of NPP.pdf` | **IAEA SSR-2/1 (Rev. 1)** — Safety of NPP: Design | Master design-requirements set (82 Requirements) |
| `IAEA.pdf` + `Design of the  Core.pdf` | **IAEA SSG-52** — Design of the Reactor Core (duplicate) | Core-design guidance (peaking, SDM, coefficients) |
| `Safety Requirements SMR.pdf` | **IAEA TECDOC-1936** — Applicability of Design Safety Requirements to SMRs | Graded SMR application of SSR-2/1 |
| `NRC spec.pdf` | **NUREG-1431 (Rev. 5)** — STS, Westinghouse | LCO peaking (3.2.1/3.2.2) + RPS setpoints |

Cross-checked in `safety/regulatory_alignment_audit.md` (2026-06-15).
