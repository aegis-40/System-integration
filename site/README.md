# Aegis-40 — Interactive Layout Viewer

Single-page interactive viewer for the NPP facility layouts. **All plans are drawn natively in the browser as SVG** — no embedded images.

## Open it
Open `site/index.html` in any browser (double-click, or `open site/index.html`). No build step, no dependencies, fully offline.

## Features
- **Four layouts**, switchable via the top tabs (or URL hash `#site` / `#rxb` / `#elev` / `#mcr`):
  1. Site Plot Plan — three islands, 14 buildings to scale, EPZ, H₂ stand-off, piping
  2. Reactor Building — containment, RPV, core, refuel cavity, penetrations
  3. Elevation / Section — below-grade reactor, building heights, grade line
  4. Main Control Room — console layout per the I&C architecture
- **Hover** any building / zone / component → highlight + tooltip + detail panel
- **Pan** (drag) and **zoom** (scroll wheel or the +/−/⊡ buttons)
- **Legend hover** (site view) dims everything except the chosen island

## Tech
Plain HTML + CSS + SVG + vanilla JS, single file. Fonts: Chakra Petch / Manrope / JetBrains Mono.
Every drawing is authored in real-world units inside the SVG `viewBox`; styling and interaction are CSS/JS.

*Source data: `layout/building_list.md`, `layout/zones.md`, rev_3 neutronics. Part of `aegis-40/System-integration`.*
