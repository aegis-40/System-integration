# Aegis-40 — Interactive Layout Viewer

Single-page interactive viewer for the NPP facility layouts. **All plans are drawn natively in the browser as SVG** — no embedded images.

## Open it
Open `site/index.html` in any browser (double-click, or `open site/index.html`). No build step, no dependencies, fully offline.

## Features
- **Five layouts**, switchable via the top tabs (or URL hash `#iso` / `#site` / `#rxb` / `#elev` / `#mcr`):
  0. **Bird’s-eye 3D** — stylised axonometric massing: every building extruded to footprint + height on a ground plane, with leader-line labels (a clean take on a 3D plant render)
  1. Site Plot Plan — three islands, 14 buildings to scale, EPZ, H₂ stand-off, piping
  2. Reactor Building — containment, RPV, core, refuel cavity, penetrations
  3. Elevation / Section — below-grade reactor, building heights, grade line
  4. Main Control Room — console layout per the I&C architecture
- **Hover** any building / zone / component → highlight + tooltip + detail panel
- **Pan** (drag) and **zoom** (scroll wheel or the +/−/⊡ buttons)
- **Legend hover** dims everything except the chosen island

## Style
Classic light "architectural plan" theme — graph-paper grid, tinted building fills, thin precise
linework, scale stamps. Fonts: Spectral (titles) / Archivo (UI) / JetBrains Mono (dimensions).

## Tech
Plain HTML + CSS + SVG + vanilla JS, single file. Every drawing — including the isometric view —
is generated in real-world units inside the SVG `viewBox`; the 3D massing is an axonometric (30°)
projection computed in JS. Styling and interaction are CSS/JS.

*Source data: `layout/building_list.md`, `layout/zones.md`, rev_3 neutronics. Part of `aegis-40/System-integration`.*
