# FER Draft — Aegis-40 — §8.12 Economic Evaluation

*Draft r1, 2026-06-25. Owner: Azamhon (FOM scope). Computational engine: `fom/economics.py` → `fom/outputs/economics_report.md`. Companion comparative ranking: `fom/wfom.py`.*

**Marker convention:** *[CITED]* literature/market input not derivable from the design (swept in sensitivity); *[SUPERVISOR-PENDING]* price/weight default; *[VERIFY]*; *[SIM-PENDING]*.

> **Methodology stance.** The Aegis-40 economic case is built on the OECD-NEA/IEA *Levelized Cost of Electricity* framework, with the GIF-EMWG / IAEA G4ECONS code-of-accounts structure. Because Aegis-40 is a paper detailed-design, capital and O&M are **literature-benchmarked, not design-derived** — results are therefore reported as **sensitivity bands**, never single points. The cost terms we *can* compute from the design (generation, fuel cycle) are computed exactly. This separation is stated openly throughout; it is the honest and the professional posture for a design-stage report.

---

## 8.12.1 Methodology and scope

Economic performance is expressed through three layers:

1. **Levelized Cost of Electricity (LCOE)** — the standard international metric [OECD-NEA/IEA *Projected Costs of Generating Electricity*]:

   LCOE = Σₜ (CAPEXₜ + O&Mₜ + Fuelₜ + Backendₜ + Decommₜ)/(1+r)ᵗ ÷ Σₜ Eₜ/(1+r)ᵗ

2. **Cogeneration value** — Aegis-40 sells electricity **plus** district heat (TCES) **plus** hydrogen (SOE). The by-products are valued by the **by-product-credit method** (heat + H₂ revenue netted against the electricity numerator), giving a *cogen-credited LCOE*. A full exergy-based cost allocation (separate LCOH, LCOH₂) is identified as a refinement *[ANALYSIS-PENDING]*.

3. **Financial indicators** — NPV, IRR, simple payback over the 60-year design life, on the project cashflow.

Cost accounting follows the EMWG two-digit code of accounts: overnight capital cost (OCC) → + interest during construction (IDC) → total capital investment; O&M (fixed + variable); fuel cycle (front-end + once-through back-end); decommissioning sinking fund. Discount rate central **7 %**, swept **3 / 7 / 10 %** per OECD-NEA convention.

## 8.12.2 Annual output *(computed from design)*

| Product | Annual | Basis |
|---|---|---|
| Electricity | **332,880 MWh/yr** | 40 MWe × 8760 h × 0.95 CF |
| District heat | 24,000 MWh-th/yr | 15 MWth × 1600 h (heating season) |
| Hydrogen | 120,000 kg/yr | SOE electrolyser |
| Net thermal efficiency | 0.32 | 40 MWe / 125 MWth |

## 8.12.3 Fuel-cycle cost *(design physics + cited market prices)*

The fuel mass throughput is fixed by the reactor physics: at the rev_3 discharge burnup of 42.8 GWd/MTU, the plant burns **≈1,013 kgHM/yr** (= P_th·CF·365.25 / burnup). Enriching to the ~4.7 % mass-weighted product assay at 0.25 % tails requires **7.29 SWU/kg** and **9.65 kg natural U/kg** of fuel (separative-work value function) — i.e. **≈9.8 tU/yr feed and ≈7,400 SWU/yr**. With market unit prices (June 2026):

| Component | Unit price *[CITED]* | $/kgHM | $/yr |
|---|---|---|---|
| Natural U + conversion | $85.75/lb U₃O₈ + $25/kgU | 2,393 | 2.43M |
| Enrichment | $176/SWU | 1,283 | 1.30M |
| Fabrication (LEU) | $300/kgHM | 300 | 0.30M |
| **Front-end total** | | **3,976** | **4.03M** |

Front-end fuel **$12.11/MWh** + once-through back-end **$1/MWh** ⇒ **$13.11/MWh total fuel** — the most design-anchored cost in this evaluation. The boron-free, high-burnup, once-through cycle keeps the back-end minimal (no reprocessing) and is a 3S/non-proliferation strength (§8.11).

## 8.12.4 LCOE — reported as a band *(capital & O&M cited)*

Capital is the dominant, least-certain term, so LCOE is given across three published SMR capital cases. Fixed O&M $130/kWe-yr, variable $4.5/MWh *[CITED — NEA/Lazard]*; IDC over a 3-yr build; decommissioning fund 12 % of capital.

| Capital case *[CITED]* | LCOE @7 % | Cogen-credited LCOE |
|---|---|---|
| **NOAK target — $3,500/kWe** ⭐ | **$70.0/MWh** | $64.6/MWh |
| FOAK — $5,000/kWe | $85.8/MWh | $80.4/MWh |
| High FOAK — $10,000/kWe | $138.4/MWh | $133.0/MWh |

⭐ central. These sit squarely in the published SMR LCOE range ($80–150/MWh FOAK; lower at NOAK) and bracket the electricity price assumption ($60/MWh). **The NOAK case approaches competitiveness; the FOAK case does not** — the standard, honest SMR finding: the economics depend on reaching nth-of-a-kind series production.

## 8.12.5 Sensitivity — the headline result

LCOE ($/MWh) across discount rate × capital. Nuclear is capital-heavy, hence strongly discount-sensitive:

| Capital ($/kWe) | 3 % | 7 % | 10 % |
|---|---|---|---|
| NOAK $3,500 | 50.9 | 70.0 | 87.1 |
| FOAK $5,000 | 58.5 | 85.8 | 110.2 |
| High $10,000 | 83.8 | 138.4 | 187.2 |

The spread (≈$51 to $187/MWh) is dominated by **capital cost and financing**, not by anything in the reactor physics — the message a reviewer should take is that Aegis-40's competitiveness is a *deployment/financing* question (achieve NOAK capital, secure low-cost capital), not a design-physics question.

## 8.12.6 Financial indicators *(inherit capital uncertainty)*

Cashflow: 3-yr construction + 60-yr operation; revenue = electricity + heat + H₂ at the price assumptions; NPV @7 %.

| Capital ($/kWe) | NPV @7 % | IRR | Payback |
|---|---|---|---|
| NOAK $3,500 | ≈ $0M | 7.0 % | 14 yr |
| FOAK $5,000 | −$56M | n/a | 19 yr |
| High $10,000 | −$244M | n/a | 38 yr |

Annual revenue **≈$21.8M** (electricity 20.0 + heat 1.2 + H₂ 0.6); operating cost ≈$11.1M; **net operating ≈$10.7M/yr**. At the central NOAK capital and the $60/MWh price assumption the project is **near break-even (NPV≈0, IRR≈7 %)** — i.e. marginal at default prices, and value-positive if either NOAK capital is bettered, electricity/H₂ prices rise, or low-cost financing is secured. The cogeneration revenue (heat + H₂ ≈ $1.8M/yr, ~8 % of revenue) is the lever that moves it from sub-market to competitive.

## 8.12.7 SMR-specific economic argument

Aegis-40, being 40 MWe, **forgoes economy of scale** (higher $/kWe than a GW-class LWR). The recognized counter-levers, each reflected above:
- **Economy of multiples** — factory/series production drives FOAK→NOAK (the $5,000→$3,500/kWe move).
- **Shorter construction** → lower IDC.
- **Smaller EPZ (≤0.5 km)** → siting/land savings.
- **Modular cash-flow** → lower financing risk.
- **Cogeneration revenue stacking** — the §8.12.6 by-product credit.

## 8.12.8 Comparative position

The comparative figure of merit (`fom/wfom.py`) ranks Aegis-40 a robust **#2 of four** (NuScale > Aegis-40 > CAREM-25 > SMART), stable across weighting schemes, TOPSIS, and leave-one-out. The absolute LCOE here and the relative wFOM are complementary: LCOE answers "is it affordable?", wFOM answers "is it competitive on the weighted attributes?". Both carry the same disclosed caveats (cited capital, supervisor-pending prices).

## 8.12.9 Open items (close before submission)

| # | Item | Type | Owner |
|---|---|---|---|
| E1 | Overnight capital $/kWe — narrow the band toward an Aegis-specific estimate (code-of-accounts or scaled reference) | [CITED] dominant | FOM + supervisor |
| E2 | O&M benchmark for a 40 MWe reduced-staffing plant | [CITED] | FOM |
| E3 | Mass-weighted enrichment (zone mass split) → exact SWU/fuel cost | [SIM-PENDING] | Samira |
| E4 | Market prices (electricity/heat/H₂) sign-off | [SUPERVISOR-PENDING] | supervisor |
| E5 | Exergy-based cost allocation → separate LCOH, LCOH₂ | [ANALYSIS-PENDING] | FOM |
| E6 | Construction time, tails assay, decommissioning fraction | [CITED] assumptions | FOM |

## 8.12.10 References

OECD-NEA/IEA *Projected Costs of Generating Electricity* (LCOE method + discount convention); GIF-EMWG *Cost Estimating Guidelines* / IAEA **G4ECONS** (code of accounts); IAEA SMR booklet (`docs/SMR_booklet.pdf`); WNA *Economics of Nuclear Power* + *Nuclear Fuel Cycle*; EPRI/INL fuel-cycle cost basis. Market data (June 2026): U₃O₈ $85.75/lb [metalcharts/INN], SWU ~$176 [UxC], capital $/kWe [NuScale via PowerMag/INN/IEEFA; IEA 2025 via GLOBSEC], O&M [NEA/Lazard].

---
*End of §8.12 draft r1. Engine: `fom/economics.py` (re-run to regenerate `fom/outputs/economics_report.md`). All cited inputs carry sources; results are bands by design.*
