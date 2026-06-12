#!/usr/bin/env python
"""
Aegis-40 NPP — CAD model generator (STEP for Fusion 360 / any CAD).

Outputs:
  cad/aegis40_site.step   — full plant site: 13 buildings (true footprints/heights
                            from layout/building_list.md), island pads, roads,
                            double security fence, critical-pipe runs, trees, terrain.
  cad/aegis40_rxb.step    — reactor-building diorama: soil block w/ excavated pit,
                            below-grade containment + RPV [rev_3], refuel pool,
                            SFB + spent-fuel pool/racks, polar crane. Use Fusion
                            Section Analysis (or hide Soil body) for the cutaway.

Layout basis (r2, 2026-06-12): TB adjacent to NI (short steam/FW run),
CTW at site periphery — NuScale plant-arrangement practice.
Coordinates: site plan metres, X=east, Y=north (plan y flipped), Z=up. STEP in mm.
"""

import math
import random
from build123d import (
    Box, Cylinder, Cone, Compound, Color, Pos, Rot, export_step,
)

M = 1000.0  # m -> mm


def P(x, y, z):
    """site-plan metres (x east, y plan-south) -> world mm, Y flipped to north."""
    return Pos(x * M, -y * M, z * M)


def box(label, color, x, y, w, d, h, z0=0.0):
    """plan-rect (x,y top-left, w,d) extruded z0..z0+h."""
    b = P(x + w / 2, y + d / 2, z0 + h / 2) * Box(w * M, d * M, h * M)
    b.label, b.color = label, Color(*color)
    return b


def cyl(label, color, x, y, r, h, z0=0.0):
    c = P(x, y, z0 + h / 2) * Cylinder(r * M, h * M)
    c.label, c.color = label, Color(*color)
    return c


def hcyl(label, color, x, y, z, length, r, axis="x"):
    """horizontal cylinder centred at (x,y,z)."""
    rot = Rot(0, 90, 0) if axis == "x" else Rot(90, 0, 0)
    c = P(x, y, z) * rot * Cylinder(r * M, length * M)
    c.label, c.color = label, Color(*color)
    return c


# ---------------- palette ----------------
GRASS = (0.62, 0.72, 0.45)
PAD = (0.80, 0.81, 0.78)
ROAD = (0.45, 0.47, 0.48)
WALL_NI = (0.88, 0.90, 0.92)
ROOF_NI = (0.49, 0.59, 0.68)
WALL_CI = (0.91, 0.89, 0.84)
ROOF_CI = (0.71, 0.60, 0.42)
WALL_II = (0.88, 0.92, 0.89)
ROOF_II = (0.44, 0.63, 0.51)
CONC = (0.76, 0.76, 0.74)
STEEL = (0.55, 0.60, 0.65)
FENCE = (0.40, 0.42, 0.44)
TRUNK = (0.42, 0.31, 0.22)
LEAF = (0.30, 0.48, 0.28)
WATER = (0.35, 0.62, 0.72)
YELLOW = (0.88, 0.66, 0.24)
RED = (0.70, 0.25, 0.18)
TEAL = (0.18, 0.43, 0.45)
WHITE = (0.93, 0.93, 0.93)

parts = []


def building(bid, x, y, w, d, h, wall, roof):
    parts.append(box(f"{bid}_walls", wall, x, y, w, d, h))
    parts.append(box(f"{bid}_roof", roof, x + 0.6, y + 0.6, w - 1.2, d - 1.2, 0.5, z0=h))


# ================= TERRAIN =================
parts.append(box("Terrain", GRASS, -50, -45, 400, 300, 2.0, z0=-2.0))
# island pads (Conventional / Nuclear / Industrial)
parts.append(box("Pad_CI", PAD, 20, 10, 80, 80, 0.18))
parts.append(box("Pad_NI", PAD, 20, 110, 100, 80, 0.18))
parts.append(box("Pad_II", PAD, 220, 118, 60, 68, 0.18))

# ================= ROADS =================
def road(label, x1, y1, x2, y2, wide=7.0):
    if x1 == x2:  # N-S
        y0, y3 = min(y1, y2), max(y1, y2)
        parts.append(box(label, ROAD, x1 - wide / 2, y0 - wide / 2, wide, (y3 - y0) + wide, 0.22))
    else:         # E-W
        x0, x3 = min(x1, x2), max(x1, x2)
        parts.append(box(label, ROAD, x0 - wide / 2, y1 - wide / 2, (x3 - x0) + wide, wide, 0.22))


# site access spine + inter-island links + perimeter patrol road
road("Road_access_W", -45, 150, 20, 150)
road("Road_NI_spine", 20, 150, 20, 100)
road("Road_NI_CI_gap", 20, 100, 120, 100)
road("Road_to_II", 120, 150, 220, 150)
road("Patrol_S", 10, 198, 130, 198, 5)
road("Patrol_N", 10, 2, 130, 2, 5)
road("Patrol_W", 10, 2, 10, 198, 5)
road("Patrol_E", 130, 2, 130, 198, 5)

# ================= SECURITY FENCES (double, PIDAS-style) =================
def fence(tag, x0, y0, x1, y1, step=12.0, hgt=3.2):
    pts = []
    for x in [x0 + i * step for i in range(int((x1 - x0) / step) + 1)]:
        pts += [(x, y0), (x, y1)]
    for y in [y0 + i * step for i in range(1, int((y1 - y0) / step))]:
        pts += [(x0, y), (x1, y)]
    for i, (px, py) in enumerate(pts):
        parts.append(cyl(f"{tag}_post{i}", FENCE, px, py, 0.07, hgt))
    rails = []
    for z in (1.1, 2.1, 3.1):
        rails.append(box(f"{tag}_railN", FENCE, x0, y0 - 0.04, x1 - x0, 0.08, 0.07, z0=z))
        rails.append(box(f"{tag}_railS", FENCE, x0, y1 - 0.04, x1 - x0, 0.08, 0.07, z0=z))
        rails.append(box(f"{tag}_railW", FENCE, x0 - 0.04, y0, 0.08, y1 - y0, 0.07, z0=z))
        rails.append(box(f"{tag}_railE", FENCE, x1 - 0.04, y0, 0.08, y1 - y0, 0.07, z0=z))
    parts.extend(rails)


fence("Fence_inner", 18, 8, 122, 192)        # protected area (NI+CI)
fence("Fence_outer", 13, 3, 127, 197, step=14)
fence("Fence_II", 218, 116, 282, 188, step=14, hgt=2.4)  # industrial island

# ============ NUCLEAR ISLAND (Seismic Cat I) ============
building("RXB", 55, 135, 25, 25, 30, WALL_NI, ROOF_NI)
parts.append(cyl("RXB_vent", STEEL, 76, 138, 0.8, 4, z0=30))
building("AB", 80, 138, 25, 20, 15, WALL_NI, ROOF_NI)
building("CB", 24, 120, 30, 25, 12, WALL_NI, ROOF_NI)
building("SFB", 34, 150, 20, 15, 15, WALL_NI, ROOF_NI)
building("DGB", 100, 165, 15, 10, 10, WALL_NI, ROOF_NI)
building("WMB", 24, 168, 25, 15, 12, WALL_NI, ROOF_NI)
parts.append(cyl("Offgas_stack", CONC, 46, 170, 1.2, 30))
parts.append(cyl("Offgas_stack_band", RED, 46, 170, 1.25, 1.5, z0=28.5))

# ============ CONVENTIONAL ISLAND (Cat II) — r2 arrangement ============
building("TB", 50, 68, 30, 20, 15, WALL_CI, ROOF_CI)      # adjacent to NI
building("WSB", 24, 58, 20, 15, 8, WALL_CI, ROOF_CI)
# Cooling tower (peripheral): basin + plenum + 6 mech-draft fan cells
parts.append(box("CTW_basin", CONC, 22, 12, 30, 30, 2.0))
parts.append(box("CTW_plenum", CONC, 23, 13, 28, 28, 6.0, z0=2.0))
for i in range(3):
    for j in range(2):
        fx, fy = 27 + 0.5 + i * 9.5, 19 + j * 13 - 1.5
        parts.append(cyl(f"CTW_fanring_{i}{j}", STEEL, fx + 1.5, fy + 2.5, 3.6, 2.6, z0=8.0))
        parts.append(cyl(f"CTW_fan_{i}{j}", (0.25, 0.28, 0.30), fx + 1.5, fy + 2.5, 2.9, 0.4, z0=10.0))
# Switchyard: gravel pad, control building, gantries, transformers
parts.append(box("EHB_pad", (0.70, 0.69, 0.66), 56, 14, 40, 28, 0.25))
building("EHB_ctrl", 58, 16, 10, 8, 6, WALL_CI, ROOF_CI)
for i in range(3):
    gx = 66 + i * 9
    parts.append(cyl(f"EHB_gantryA{i}", STEEL, gx, 22, 0.25, 9))
    parts.append(cyl(f"EHB_gantryB{i}", STEEL, gx, 36, 0.25, 9))
    parts.append(box(f"EHB_beam{i}", STEEL, gx - 0.3, 22, 0.6, 14, 0.6, z0=8.6))
parts.append(box("EHB_trafo1", (0.35, 0.38, 0.42), 59, 30, 4, 3.2, 4.2, z0=0.25))
parts.append(box("EHB_trafo2", (0.35, 0.38, 0.42), 59, 35, 4, 3.2, 4.2, z0=0.25))

# ============ INDUSTRIAL ISLAND ============
parts.append(box("TES_slab", CONC, 224, 124, 30, 30, 0.4))
parts.append(cyl("TES_tank_hot", RED, 232, 132, 6, 14, z0=0.4))
parts.append(cyl("TES_tank_cold", TEAL, 246, 145, 6, 14, z0=0.4))
parts.append(box("TES_skid", STEEL, 228, 146, 8, 6, 4, z0=0.4))
building("SOE", 224, 156, 25, 25, 10, WALL_II, ROOF_II)
parts.append(box("H2_pad", CONC, 256, 140, 20, 30, 0.3))
for i in range(4):
    parts.append(hcyl(f"H2_tank{i}", WHITE, 266, 145 + i * 6.5, 2.3, 14, 1.9, axis="x"))
    parts.append(box(f"H2_saddleA{i}", STEEL, 261, 144.2 + i * 6.5, 1.2, 1.6, 1.4, z0=0.3))
    parts.append(box(f"H2_saddleB{i}", STEEL, 270, 144.2 + i * 6.5, 1.2, 1.6, 1.4, z0=0.3))

# ============ CRITICAL PIPE RUNS [ASSUMED] ============
parts.append(hcyl("Pipe_main_steam", RED, 62, 111.5, 1.6, 47, 0.35, axis="y"))
parts.append(hcyl("Pipe_feedwater", (0.20, 0.42, 0.62), 70, 111.5, 1.6, 47, 0.30, axis="y"))
parts.append(hcyl("Pipe_circwater_A", TEAL, 43.5, 73, 1.2, 13, 0.55, axis="x"))
parts.append(hcyl("Pipe_circwater_B", TEAL, 37, 57.5, 1.2, 31, 0.55, axis="y"))
parts.append(hcyl("Pipe_process_steam", (0.45, 0.30, 0.55), 164.5, 144, 1.8, 119, 0.25, axis="x"))

# ============ ENVIRONMENT: trees outside the fences ============
rng = random.Random(40)
n_t = 0
while n_t < 46:
    tx, ty = rng.uniform(-45, 345), rng.uniform(-40, 250)
    if 5 <= tx <= 135 and -5 <= ty <= 205:   # protected area + patrol
        continue
    if 210 <= tx <= 290 and 108 <= ty <= 196:  # industrial island
        continue
    if 144 <= ty <= 156 and -45 <= tx <= 225:  # access road corridor
        continue
    s = rng.uniform(0.7, 1.5)
    parts.append(cyl(f"Tree{n_t}_trunk", TRUNK, tx, ty, 0.25 * s, 2.2 * s))
    cone = P(tx, ty, 2.2 * s + 2.6 * s) * Cone(2.1 * s * M, 0.15 * M, 5.2 * s * M)
    cone.label, cone.color = f"Tree{n_t}_crown", Color(*LEAF)
    parts.append(cone)
    n_t += 1

site = Compound(label="Aegis40_Site", children=parts)
export_step(site, "aegis40_site.step")
print(f"site: {len(parts)} solids -> aegis40_site.step")

# ======================================================================
# RXB DIORAMA — below-grade reactor, true rev_3 dims
# ======================================================================
rp = []
GRADE = 0.0
PIT_W, PIT_DEPTH = 20.0, 16.0          # excavation
# soil block 90 x 56, 20 deep, with pit + SFP excavations cut
soil = Pos(0, 0, -10 * M) * Box(90 * M, 56 * M, 20 * M)
soil -= Pos(0, 0, -PIT_DEPTH / 2 * M) * Box(PIT_W * M, PIT_W * M, PIT_DEPTH * M + 2)
soil -= Pos(-22 * M, 0, -6.5 * M) * Box(16 * M, 14 * M, 13.0 * M + 2)
soil.label, soil.color = "Soil", Color(0.48, 0.39, 0.29)
rp.append(soil)
grass = Pos(0, 0, 0.15 * M) * Box(90 * M, 56 * M, 0.3 * M)
grass -= Pos(0, 0, 0.15 * M) * Box((PIT_W + 4) * M, (PIT_W + 4) * M, 0.4 * M)
grass -= Pos(-22 * M, 0, 0.15 * M) * Box(20 * M, 18 * M, 0.4 * M)
grass.label, grass.color = "Grass", Color(*GRASS)
rp.append(grass)

def rbox(label, color, cx, cy, w, d, h, zc):
    b = Pos(cx * M, cy * M, zc * M) * Box(w * M, d * M, h * M)
    b.label, b.color = label, Color(*color)
    return b

def rcyl(label, color, cx, cy, r, h, zc):
    c = Pos(cx * M, cy * M, zc * M) * Cylinder(r * M, h * M)
    c.label, c.color = label, Color(*color)
    return c

# reinforced-concrete pit liner + basemat
liner = Pos(0, 0, -8 * M) * Box(PIT_W * M, PIT_W * M, 16 * M)
liner -= Pos(0, 0, -8 * M + 1) * Box((PIT_W - 2.4) * M, (PIT_W - 2.4) * M, 16 * M + 4)
liner.label, liner.color = "Pit_liner", Color(*CONC)
rp.append(liner)
rp.append(rbox("Basemat", CONC, 0, 0, PIT_W + 4, PIT_W + 4, 2.0, -17.0))

# containment: steel shell Ø15 m, -15.5 .. -1  (RPV head ~5 m below grade)
cont = Pos(0, 0, -8.25 * M) * Cylinder(7.5 * M, 14.5 * M)
cont -= Pos(0, 0, -8.25 * M) * Cylinder(7.1 * M, 14.5 * M + 4)
cont.label, cont.color = "Containment_shell", Color(*STEEL)
rp.append(cont)
# IRWST annulus water (lower containment)
irwst = Pos(0, 0, -13 * M) * Cylinder(7.0 * M, 5.0 * M)
irwst -= Pos(0, 0, -13 * M) * Cylinder(2.6 * M, 5.2 * M)
irwst.label, irwst.color = "IRWST_water", Color(*WATER)
rp.append(irwst)
# RPV Ø2.44, integral iPWR ~10.5 m tall, head at -5
rp.append(rcyl("RPV", (0.62, 0.66, 0.70), 0, 0, 1.22, 10.5, -10.25))
rp.append(rcyl("RPV_core_region", RED, 0, 0, 1.05, 2.0, -13.5))   # 21-FA core band
rp.append(rcyl("CRDM_nozzles", STEEL, 0, 0, 0.7, 0.8, -4.6))
# refuelling pool above containment (flooded during outage)
rp.append(rbox("Refuel_pool_water", WATER, 0, 0, 9, 9, 3.5, -2.8))
# biological shield slab at grade over pit (with hatch gap)
bio = Pos(0, 0, -0.5 * M) * Box((PIT_W - 2.4) * M, (PIT_W - 2.4) * M, 1.0 * M)
bio -= Pos(4 * M, 4 * M, -0.5 * M) * Box(5 * M, 5 * M, 1.2 * M)
bio.label, bio.color = "Bio_shield_slab", Color(*CONC)
rp.append(bio)

# RXB superstructure 25x25x30 above grade (hollow shell, open over pit)
shell = Pos(0, 0, 15 * M) * Box(25 * M, 25 * M, 30 * M)
shell -= Pos(0, 0, 14.6 * M) * Box(23.4 * M, 23.4 * M, 30 * M)
shell -= Pos(0, -12.5 * M, 6 * M) * Box(8 * M, 3 * M, 9 * M)   # equipment hatch opening
shell.label, shell.color = "RXB_shell", Color(*WALL_NI)
rp.append(shell)
rp.append(rbox("RXB_roof", ROOF_NI, 0, 0, 25, 25, 0.6, 30.3))

# polar crane: rails + bridge + trolley + hook
rp.append(rbox("Crane_rail_W", STEEL, -11.2, 0, 0.8, 23.4, 0.8, 24.0))
rp.append(rbox("Crane_rail_E", STEEL, 11.2, 0, 0.8, 23.4, 0.8, 24.0))
rp.append(rbox("Crane_bridge_A", YELLOW, 0, -1.2, 23.2, 1.4, 1.6, 25.2))
rp.append(rbox("Crane_bridge_B", YELLOW, 0, 1.2, 23.2, 1.4, 1.6, 25.2))
rp.append(rbox("Crane_trolley", YELLOW, 2, 0, 3.4, 4.0, 1.8, 26.2))
rp.append(rcyl("Crane_cable", (0.2, 0.2, 0.2), 2, 0, 0.06, 18, 16.2))
rp.append(rbox("Crane_block", YELLOW, 2, 0, 1.2, 1.2, 1.4, 7.0))

# SFB annex (west): shell + spent-fuel pool + racks + transfer canal
sfb = Pos(-22 * M, 0, 7.5 * M) * Box(20 * M, 15 * M, 15 * M)
sfb -= Pos(-22 * M, 0, 7.2 * M) * Box(18.6 * M, 13.6 * M, 15 * M)
sfb.label, sfb.color = "SFB_shell", Color(*WALL_NI)
rp.append(sfb)
rp.append(rbox("SFB_roof", ROOF_NI, -22, 0, 20, 15, 0.5, 15.3))
pool = Pos(-22 * M, 0, -6 * M) * Box(13 * M, 11 * M, 12 * M)
pool -= Pos(-22 * M, 0, -6 * M + 1) * Box(11.4 * M, 9.4 * M, 12 * M + 4)
pool.label, pool.color = "SFP_liner", Color(*CONC)
rp.append(pool)
rp.append(rbox("SFP_water", WATER, -22, 0, 11.4, 9.4, 10.8, -6.4))
for i in range(3):
    for j in range(2):
        rp.append(rbox(f"SFP_rack{i}{j}", (0.30, 0.50, 0.34),
                       -25.5 + i * 3.5, -2.2 + j * 4.4, 2.8, 3.6, 4.2, -9.5))
canal = Pos(-13.5 * M, 0, -5 * M) * Box(7 * M, 3 * M, 2.4 * M)
canal.label, canal.color = "Transfer_canal_water", Color(*WATER)
rp.append(canal)

rxb = Compound(label="Aegis40_RXB", children=rp)
export_step(rxb, "aegis40_rxb.step")
print(f"rxb: {len(rp)} solids -> aegis40_rxb.step")
