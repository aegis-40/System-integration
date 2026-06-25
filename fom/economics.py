#!/usr/bin/env python3
# ============================================================================
# Aegis-40 — Economic evaluation (LCOE / LCOH / LCOH2 + NPV/IRR + sensitivity)
# ----------------------------------------------------------------------------
# Sibling to wfom.py. Where wfom.py RANKS Aegis-40 against competitors, this
# computes the ABSOLUTE economic case for FER §8.12.
#
# DESIGN PHILOSOPHY (read before trusting a number):
#   - "ours"   = computed from the Aegis-40 design (generation, fuel cycle).
#   - "cited"  = literature/market input we cannot derive (capital, O&M, unit
#                fuel prices). Each carries a source + is swept in sensitivity.
#   The capital cost is the dominant, most-uncertain LCOE term and is therefore
#   reported as a BAND, never a single point. This mirrors OECD-NEA/IEA practice.
#
# Run:  python3 fom/economics.py     # writes outputs/economics_report.md
# Pure stdlib (no numpy). Discount/IRR by closed-form + bisection.
# ============================================================================

import math
from datetime import date

# ----------------------------------------------------------------------------
# 1. DESIGN INPUTS  ("ours" — from fom/reactors/aegis40.yaml + safety_criteria)
# ----------------------------------------------------------------------------
P_el_MWe       = 40.0     # net electric
P_th_MWth      = 125.0    # thermal
CF             = 0.95     # capacity factor
LIFE_Y         = 60       # design life
BURNUP_GWd_MTU = 42.8     # rev_3 discharge burnup
ENRICH_PROD    = 0.047    # mass-weighted product assay ~4.7% (zones 4.95/4.70/4.40) [APPROX — confirm zone mass split with Samira]
ENRICH_FEED    = 0.00711  # natural U
ENRICH_TAILS   = 0.0025   # tails assay (typical optimized) [cited assumption]

# Cogeneration (from aegis40.yaml descriptive.cogen)
Q_TH_MWth      = 15.0     # district heat thermal sold
H_TH_HOURS     = 1600     # heating-season hours
M_H2_KG_Y      = 120000.0 # SOE hydrogen

HOURS_Y        = 8760.0
DAYS_Y         = 365.25

# ----------------------------------------------------------------------------
# 2. PRICE INPUTS  (product side — fom/economic_assumptions.yaml; supervisor-pending)
# ----------------------------------------------------------------------------
PRICE_EL_MWh   = 60.0   # electricity $/MWh
PRICE_HEAT_MWh = 50.0   # district heat $/MWh-th
PRICE_H2_KG    = 5.0    # hydrogen $/kg

# ----------------------------------------------------------------------------
# 3. COST INPUTS  ("cited" — LIVE-PULLED June 2026, each with source.
#    These are the inputs we cannot derive from the design.)
# ----------------------------------------------------------------------------
# Capital — overnight $/kWe. Reported as a band; central = NOAK target.
CAPITAL_USD_KWE = {
    "NOAK_target": 3500.0,   # NuScale NOAK ~$2.9k-3.9k/kWe  [INN/IEEFA, INL lit review]
    "FOAK":        5000.0,   # NuScale 12-module FOAK ~$5.0k/kWe [PowerMag/INN]
    "high_FOAK":  10000.0,   # IEA-2025 EU SMR FOAK pessimistic [IEA 2025 via GLOBSEC]
}
CAPITAL_CENTRAL = "NOAK_target"

OM_FIXED_KWE_Y  = 130.0   # fixed O&M $/kWe-yr   [NEA/Lazard ~$120-140]
OM_VAR_MWh      = 4.5     # variable O&M $/MWh   [NEA/Lazard ~$4-4.5]

# Fuel-cycle unit prices (front-end) — market, June 2026
U3O8_USD_LB     = 85.75   # U3O8 spot $/lb       [metalcharts/INN, 23 Jun 2026]
CONVERSION_KGU  = 25.0    # conversion $/kgU     [WNA, escalated]
SWU_USD         = 176.0   # enrichment $/SWU     [UxC 2024-25]
FAB_USD_KGHM    = 300.0   # LEU fabrication $/kgHM [EPRI/INL/WNA]
BACKEND_MWh     = 1.0     # once-through waste fund $/MWh [US NWF 1 mill/kWh precedent]

# Construction & decommissioning
CONSTRUCT_Y     = 3       # construction years (NOAK modular target) [cited]
DECOMM_FRAC_CAP = 0.12    # decommissioning fund as fraction of overnight capital [IAEA ~9-15%]

DISCOUNT_CENTRAL = 0.07
DISCOUNT_SWEEP   = [0.03, 0.07, 0.10]   # OECD-NEA convention

U3O8_LB_PER_KGU  = 2.59979  # 1 kgU -> kg U3O8 (0.848 U fraction) -> lb

# ----------------------------------------------------------------------------
# 4. CORE CALCS
# ----------------------------------------------------------------------------
def annual_generation():
    """ours: electricity, heat, hydrogen per year."""
    e_el   = P_el_MWe * HOURS_Y * CF          # MWh_el/yr
    e_heat = Q_TH_MWth * H_TH_HOURS           # MWh_th/yr (dispatch-limited, not CF)
    return e_el, e_heat, M_H2_KG_Y

def fuel_throughput_kgHM():
    """ours: heavy-metal mass burned per year from thermal energy / burnup."""
    burn_MWd_kgHM = BURNUP_GWd_MTU * 1000.0 / 1000.0   # GWd/MTU -> MWd/kgHM (=42.8)
    thermal_MWd_y = P_th_MWth * CF * DAYS_Y
    return thermal_MWd_y / burn_MWd_kgHM

def swu_value(x):
    """Separative potential V(x) = (2x-1) ln(x/(1-x))."""
    return (2.0 * x - 1.0) * math.log(x / (1.0 - x))

def swu_per_kg_product():
    xp, xf, xt = ENRICH_PROD, ENRICH_FEED, ENRICH_TAILS
    fp = (xp - xt) / (xf - xt)      # feed / product
    tp = (xp - xf) / (xf - xt)      # tails / product
    swu = swu_value(xp) + tp * swu_value(xt) - fp * swu_value(xf)
    return swu, fp                  # SWU/kgP, kg natU feed / kgP

def fuel_cost_per_year():
    """ours physics + cited unit prices: front-end fuel cost $/yr and $/MWh."""
    kgHM_y = fuel_throughput_kgHM()
    swu_kg, feed_kg = swu_per_kg_product()
    # per kg product
    u_cost   = feed_kg * (U3O8_USD_LB * U3O8_LB_PER_KGU + CONVERSION_KGU)  # $/kgP
    enr_cost = swu_kg * SWU_USD                                            # $/kgP
    fab_cost = FAB_USD_KGHM                                                # $/kgP
    per_kg   = u_cost + enr_cost + fab_cost
    annual   = per_kg * kgHM_y
    e_el, _, _ = annual_generation()
    return {
        "kgHM_y": kgHM_y, "swu_kg": swu_kg, "feed_kg": feed_kg,
        "swu_y": swu_kg * kgHM_y, "feed_tU_y": feed_kg * kgHM_y / 1000.0,
        "u_cost": u_cost, "enr_cost": enr_cost, "fab_cost": fab_cost,
        "per_kg": per_kg, "annual": annual, "per_MWh": annual / e_el,
    }

def crf(r, n):
    """Capital recovery factor (annuity)."""
    return r * (1 + r) ** n / ((1 + r) ** n - 1)

def idc_factor(r, years):
    """Interest-during-construction multiplier on overnight cost.
    Simple even-spend model: capital paid in equal annual tranches, each
    accruing interest to commercial operation date."""
    if years <= 0:
        return 1.0
    tranche = 1.0 / years
    total = sum(tranche * (1 + r) ** (years - t - 0.5) for t in range(years))
    return total   # >1.0

def lcoe(capital_kwe, r, cf=CF, with_cogen_credit=False):
    """$/MWh. Capital+O&M+fuel+backend+decomm, electricity basis.
    with_cogen_credit: subtract heat+H2 revenue from the numerator."""
    e_el = P_el_MWe * HOURS_Y * cf
    e_heat = Q_TH_MWth * H_TH_HOURS
    occ = capital_kwe * P_el_MWe * 1000.0          # $ overnight
    tcic = occ * idc_factor(r, CONSTRUCT_Y)        # + IDC
    decomm = occ * DECOMM_FRAC_CAP                  # fund (undiscounted overnight basis)
    ann_cap = (tcic + decomm) * crf(r, LIFE_Y)      # annualized capital incl. decomm sinking
    ann_om  = OM_FIXED_KWE_Y * P_el_MWe * 1000.0 + OM_VAR_MWh * e_el
    fc = fuel_cost_per_year()
    ann_fuel = fc["annual"] + BACKEND_MWh * e_el
    num = ann_cap + ann_om + ann_fuel
    if with_cogen_credit:
        num -= (e_heat * PRICE_HEAT_MWh + M_H2_KG_Y * PRICE_H2_KG)
    return num / e_el

def npv_irr(capital_kwe, r):
    """NPV at r and IRR from the full cashflow (construction + LIFE_Y operation)."""
    occ = capital_kwe * P_el_MWe * 1000.0
    e_el, e_heat, h2 = annual_generation()
    rev = e_el * PRICE_EL_MWh + e_heat * PRICE_HEAT_MWh + h2 * PRICE_H2_KG
    fc = fuel_cost_per_year()
    op_cost = (OM_FIXED_KWE_Y * P_el_MWe * 1000.0 + OM_VAR_MWh * e_el
               + fc["annual"] + BACKEND_MWh * e_el)
    net_op = rev - op_cost
    decomm = occ * DECOMM_FRAC_CAP

    # cashflow: construction years (capital spend, even), then LIFE_Y operating,
    # decommissioning paid in the final year.
    cf = []
    for t in range(CONSTRUCT_Y):
        cf.append(-occ / CONSTRUCT_Y)
    for t in range(LIFE_Y):
        c = net_op
        if t == LIFE_Y - 1:
            c -= decomm
        cf.append(c)

    def npv_at(rate):
        return sum(c / (1 + rate) ** i for i, c in enumerate(cf))

    npv = npv_at(r)
    # IRR by bisection
    lo, hi = -0.5, 1.0
    irr = None
    if npv_at(lo) * npv_at(hi) < 0:
        for _ in range(200):
            mid = (lo + hi) / 2
            if npv_at(lo) * npv_at(mid) <= 0:
                hi = mid
            else:
                lo = mid
        irr = (lo + hi) / 2
    # simple payback (undiscounted, from commercial operation)
    cum, payback = -occ, None
    for t in range(LIFE_Y):
        cum += net_op
        if cum >= 0:
            payback = t + 1
            break
    return npv, irr, payback, net_op, rev, op_cost

# ----------------------------------------------------------------------------
# 5. REPORT
# ----------------------------------------------------------------------------
def fmt(x, n=1):
    return f"{x:,.{n}f}"

def build_report():
    e_el, e_heat, h2 = annual_generation()
    fc = fuel_cost_per_year()
    L = []
    L.append("# Aegis-40 — Economic evaluation (FER §8.12 working model)")
    L.append(f"*Generated {date.today().isoformat()} by fom/economics.py. "
             f"Discount central {DISCOUNT_CENTRAL:.0%}; prices supervisor-pending defaults.*\n")
    L.append("> **Reliability key:** *ours* = computed from the Aegis-40 design; "
             "*cited* = literature/market input (capital, O&M, unit fuel prices) that "
             "cannot be derived and is swept in sensitivity. Capital is the dominant, "
             "most-uncertain term → reported as a **band**, never a point (OECD-NEA practice).\n")

    # --- generation
    L.append("## 1. Annual output  *(ours)*")
    L.append("| Product | Annual | Basis |")
    L.append("|---|---|---|")
    L.append(f"| Electricity | **{fmt(e_el,0)} MWh/yr** | 40 MWe × 8760 × {CF} |")
    L.append(f"| District heat | {fmt(e_heat,0)} MWh-th/yr | 15 MWth × {H_TH_HOURS} h |")
    L.append(f"| Hydrogen | {fmt(h2,0)} kg/yr | SOE |")
    L.append(f"| Thermal efficiency | {P_el_MWe/P_th_MWth:.3f} | 40/125 |\n")

    # --- fuel
    L.append("## 2. Fuel-cycle cost  *(ours physics + cited unit prices)*")
    L.append(f"Throughput **{fmt(fc['kgHM_y'],0)} kgHM/yr** "
             f"(= P_th·CF·365.25 / burnup {BURNUP_GWd_MTU} GWd/MTU). "
             f"Enrichment to {ENRICH_PROD*100:.2f}% at {ENRICH_TAILS*100:.2f}% tails → "
             f"**{fc['swu_kg']:.2f} SWU/kg** and **{fc['feed_kg']:.2f} kg natU/kg** product.\n")
    L.append("| Component | Unit price (cited) | $/kgHM | Annual $ |")
    L.append("|---|---|---|---|")
    L.append(f"| Natural U + conversion | ${U3O8_USD_LB}/lb U3O8 + ${CONVERSION_KGU}/kgU | {fmt(fc['u_cost'],0)} | {fmt(fc['u_cost']*fc['kgHM_y'],0)} |")
    L.append(f"| Enrichment | ${SWU_USD}/SWU | {fmt(fc['enr_cost'],0)} | {fmt(fc['enr_cost']*fc['kgHM_y'],0)} |")
    L.append(f"| Fabrication | ${FAB_USD_KGHM}/kgHM | {fmt(fc['fab_cost'],0)} | {fmt(fc['fab_cost']*fc['kgHM_y'],0)} |")
    L.append(f"| **Front-end total** | | **{fmt(fc['per_kg'],0)}** | **{fmt(fc['annual'],0)}** |")
    L.append(f"\nFront-end fuel = **${fc['per_MWh']:.2f}/MWh**; "
             f"+ back-end ${BACKEND_MWh:.0f}/MWh (once-through) "
             f"⇒ **${fc['per_MWh']+BACKEND_MWh:.2f}/MWh** total fuel. "
             f"Feed ≈ {fc['feed_tU_y']:.1f} tU/yr, {fmt(fc['swu_y'],0)} SWU/yr.\n")

    # --- LCOE band
    L.append("## 3. LCOE  *(capital + O&M cited → reported as a band)*")
    L.append(f"Annualized via CRF over {LIFE_Y} yr; IDC over {CONSTRUCT_Y}-yr build; "
             f"decommissioning fund {DECOMM_FRAC_CAP:.0%} of capital. "
             f"Fixed O&M ${OM_FIXED_KWE_Y}/kWe-yr, variable ${OM_VAR_MWh}/MWh.\n")
    L.append("| Capital case ($/kWe) | LCOE @7% ($/MWh) | LCOE, cogen-credited ($/MWh) |")
    L.append("|---|---|---|")
    for k, cap in CAPITAL_USD_KWE.items():
        base = lcoe(cap, DISCOUNT_CENTRAL)
        cred = lcoe(cap, DISCOUNT_CENTRAL, with_cogen_credit=True)
        star = " ⭐" if k == CAPITAL_CENTRAL else ""
        L.append(f"| {k} = {fmt(cap,0)}{star} | **{base:.1f}** | {cred:.1f} |")
    L.append(f"\n⭐ central case. Cogen-credited = heat + H₂ revenue netted against the "
             f"electricity numerator (by-product-credit method). "
             f"Compare to electricity price ${PRICE_EL_MWh}/MWh.\n")

    # --- discount sensitivity
    L.append("## 4. Sensitivity — discount rate × capital  *(the headline uncertainty)*")
    L.append("LCOE $/MWh @7% basis. Nuclear is capital-heavy → highly discount-sensitive.\n")
    hdr = "| Capital ($/kWe) | " + " | ".join(f"{r:.0%}" for r in DISCOUNT_SWEEP) + " |"
    L.append(hdr)
    L.append("|" + "---|" * (len(DISCOUNT_SWEEP) + 1))
    for k, cap in CAPITAL_USD_KWE.items():
        row = " | ".join(f"{lcoe(cap, r):.1f}" for r in DISCOUNT_SWEEP)
        L.append(f"| {k} = {fmt(cap,0)} | {row} |")
    L.append("")

    # --- NPV/IRR
    L.append("## 5. Financial indicators  *(inherit capital uncertainty)*")
    L.append(f"Cashflow: {CONSTRUCT_Y}-yr construction + {LIFE_Y}-yr operation; "
             f"revenue = electricity + heat + H₂ at the price assumptions; NPV @7%.\n")
    L.append("| Capital ($/kWe) | NPV @7% ($M) | IRR | Simple payback (yr) |")
    L.append("|---|---|---|---|")
    for k, cap in CAPITAL_USD_KWE.items():
        npv, irr, pb, *_ = npv_irr(cap, DISCOUNT_CENTRAL)
        irr_s = f"{irr*100:.1f}%" if irr is not None else "n/a"
        pb_s = str(pb) if pb else ">life"
        L.append(f"| {k} = {fmt(cap,0)} | {npv/1e6:,.0f} | {irr_s} | {pb_s} |")
    _, _, _, net_op, rev, op = npv_irr(CAPITAL_USD_KWE[CAPITAL_CENTRAL], DISCOUNT_CENTRAL)
    L.append(f"\nAnnual revenue ≈ **${rev/1e6:,.1f}M** "
             f"(elec {e_el*PRICE_EL_MWh/1e6:,.1f} + heat {e_heat*PRICE_HEAT_MWh/1e6:,.1f} "
             f"+ H₂ {h2*PRICE_H2_KG/1e6:,.1f}); operating cost ≈ ${op/1e6:,.1f}M; "
             f"net operating ≈ ${net_op/1e6:,.1f}M/yr.\n")

    # --- caveats
    L.append("## 6. What is computed vs cited (honesty register)")
    L.append("| Element | Status | Note |")
    L.append("|---|---|---|")
    L.append("| Generation, fuel throughput, SWU | **ours** | from design — reliable |")
    L.append("| Fuel-cycle cost | ours physics + cited unit prices | market prices dated June 2026 |")
    L.append("| Revenue | cited prices | supervisor-pending defaults |")
    L.append("| Capital $/kWe | **cited, dominant uncertainty** | literature band; not design-derived |")
    L.append("| O&M | cited | NEA/Lazard benchmark |")
    L.append("| LCOE / NPV / IRR | derived | inherit capital uncertainty → bands |")
    L.append("\n**Open:** mass-weighted enrichment uses ~4.7% pending Samira's zone mass split; "
             "tails assay, construction time, decommissioning fraction are cited assumptions; "
             "prices await supervisor sign-off. See §8.12 draft for the narrative.\n")

    L.append("## 7. Sources (live-pulled June 2026)")
    L.append("- U₃O₈ $85.75/lb — metalcharts.org / Investing News Network Q1-2026")
    L.append("- SWU ~$176 — UxC nuclear fuel price indicators (2024–25)")
    L.append("- Conversion/fabrication — WNA *Economics of Nuclear Power*; EPRI/INL fuel-cycle cost basis")
    L.append("- Capital $/kWe (FOAK 5k / NOAK 3.5k / high 10k) — NuScale (PowerMag/INN/IEEFA); IEA 2025 (GLOBSEC)")
    L.append("- O&M ($130/kWe-yr, $4.5/MWh) — OECD-NEA/IEA Projected Costs; Lazard")
    L.append("- Method — OECD-NEA/IEA LCOE; GIF-EMWG / IAEA G4ECONS code-of-accounts")
    return "\n".join(L)

if __name__ == "__main__":
    import os
    rpt = build_report()
    out = os.path.join(os.path.dirname(__file__), "outputs", "economics_report.md")
    with open(out, "w") as f:
        f.write(rpt + "\n")
    print(rpt)
    print(f"\n[written] {out}")
