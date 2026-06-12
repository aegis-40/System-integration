# CAD models — Aegis-40 (Fusion 360 / STEP)

3D solid models of the plant, generated parametrically by `build_aegis40_cad.py`
(build123d / OpenCascade). STEP AP214 — opens natively in Fusion 360, FreeCAD,
SolidWorks, etc. All parts are named and coloured.

| File | Contents |
|---|---|
| `aegis40_site.step` | **Plant site** (317 solids): all 13 buildings at true footprints + heights from `layout/building_list.md`, island pads, access/patrol roads, double PIDAS-style security fence + industrial-island fence, mech-draft cooling tower (6 fan cells), switchyard gantries + transformers, TES hot/cold tanks, H₂ tank yard, off-gas stack, critical pipe runs `[ASSUMED]`, terrain + trees. |
| `aegis40_rxb.step` | **Reactor-building diorama** (31 solids): soil block with excavated pit, RC pit liner + basemat, below-grade containment shell Ø15 m, RPV Ø2.44 m with 21-FA core band [rev_3], IRWST annulus, refuelling pool, bio-shield slab, RXB superstructure + polar crane, SFB annex with spent-fuel pool/racks + transfer canal. |

**Layout basis (r2, 2026-06-12):** TB adjacent to NI (shortest main-steam/feedwater
run, ~47 m), CTW at the site periphery — NuScale plant-arrangement practice
(IV.5-KenLangdon-NuScale.pdf, slide 15).

## Fusion 360 import

1. **File → Open → Open from my computer…** → pick the `.step` — or upload via the
   Data Panel (preserves the named browser tree).
2. Site model: orbit freely; every building is a named body (RXB_walls, CTW_fan_…,
   Fence_inner_…, Tree…).
3. RXB model: for the NuScale-style cutaway use **Inspect → Section Analysis** on
   the XZ plane through origin — or just hide the `Soil` and `Grass` bodies.
4. Units: model is in **mm** (1 m = 1000 mm). RXB footprint = 25 000 mm.

## Regenerate

```bash
~/.venvs/cad/bin/python build_aegis40_cad.py   # venv with `pip install build123d`
```

Edit dimensions/positions at the top of the script — single source of truth is
still `layout/building_list.md`; keep them in sync.
