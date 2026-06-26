# Aegis-40 — Economic evaluation (FER §8.12 working model)
*Generated 2026-06-26 by fom/economics.py. Discount central 7%; prices supervisor-pending defaults.*

> **Reliability key:** *ours* = computed from the Aegis-40 design; *cited* = literature/market input (capital, O&M, unit fuel prices) that cannot be derived and is swept in sensitivity. Capital is the dominant, most-uncertain term → reported as a **band**, never a point (OECD-NEA practice).

## 1. Annual output  *(ours)*
| Product | Annual | Basis |
|---|---|---|
| Electricity | **332,880 MWh/yr** | 40 MWe × 8760 × 0.95 |
| District heat | 24,000 MWh-th/yr | 15 MWth × 1600 h |
| Hydrogen | 120,000 kg/yr | SOE |
| Thermal efficiency | 0.320 | 40/125 |

## 2. Fuel-cycle cost  *(ours physics + cited unit prices)*
Throughput **1,013 kgHM/yr** (= P_th·CF·365.25 / burnup 42.8 GWd/MTU). Enrichment to 4.70% at 0.25% tails → **7.29 SWU/kg** and **9.65 kg natU/kg** product.

| Component | Unit price (cited) | $/kgHM | Annual $ |
|---|---|---|---|
| Natural U + conversion | $85.75/lb U3O8 + $25.0/kgU | 2,393 | 2,425,335 |
| Enrichment | $176.0/SWU | 1,283 | 1,300,326 |
| Fabrication | $300.0/kgHM | 300 | 304,019 |
| **Front-end total** | | **3,976** | **4,029,681** |

Front-end fuel = **$12.11/MWh**; + back-end $1/MWh (once-through) ⇒ **$13.11/MWh** total fuel. Feed ≈ 9.8 tU/yr, 7,388 SWU/yr.

## 3. LCOE  *(capital + O&M cited → reported as a band)*
Annualized via CRF over 60 yr; IDC over 3-yr build; decommissioning fund 12% of capital. Fixed O&M $130.0/kWe-yr, variable $4.5/MWh.

| Capital case ($/kWe) | LCOE @7% ($/MWh) | LCOE, cogen-credited ($/MWh) |
|---|---|---|
| NOAK_target = 3,500 ⭐ | **70.0** | 64.6 |
| FOAK = 5,000 | **85.8** | 80.4 |
| high_FOAK = 10,000 | **138.4** | 133.0 |

⭐ central case. Cogen-credited = heat + H₂ revenue netted against the electricity numerator (by-product-credit method). Compare to electricity price $60.0/MWh.

## 4. Sensitivity — discount rate × capital  *(the headline uncertainty)*
LCOE $/MWh @7% basis. Nuclear is capital-heavy → highly discount-sensitive.

| Capital ($/kWe) | 3% | 7% | 10% |
|---|---|---|---|
| NOAK_target = 3,500 | 50.9 | 70.0 | 87.1 |
| FOAK = 5,000 | 58.5 | 85.8 | 110.2 |
| high_FOAK = 10,000 | 83.8 | 138.4 | 187.2 |

## 5. Financial indicators  *(inherit capital uncertainty)*
Cashflow: 3-yr construction + 60-yr operation; revenue = electricity + heat + H₂ at the price assumptions; NPV @7%.

| Capital ($/kWe) | NPV @7% ($M) | IRR | Simple payback (yr) |
|---|---|---|---|
| NOAK_target = 3,500 | 0 | 7.0% | 14 |
| FOAK = 5,000 | -56 | n/a | 19 |
| high_FOAK = 10,000 | -244 | n/a | 38 |

Annual revenue ≈ **$21.8M** (elec 20.0 + heat 1.2 + H₂ 0.6); operating cost ≈ $11.1M; net operating ≈ $10.7M/yr.

## 6. What is computed vs cited (honesty register)
| Element | Status | Note |
|---|---|---|
| Generation, fuel throughput, SWU | **ours** | from design — reliable |
| Fuel-cycle cost | ours physics + cited unit prices | market prices dated June 2026 |
| Revenue | cited prices | supervisor-pending defaults |
| Capital $/kWe | **cited, dominant uncertainty** | literature band; not design-derived |
| O&M | cited | NEA/Lazard benchmark |
| LCOE / NPV / IRR | derived | inherit capital uncertainty → bands |

**Open:** mass-weighted enrichment uses ~4.7% pending Samira's zone mass split; tails assay, construction time, decommissioning fraction are cited assumptions; prices await supervisor sign-off. See §8.12 draft for the narrative.

## 7. Sources (live-pulled June 2026)
- U₃O₈ $85.75/lb — metalcharts.org / Investing News Network Q1-2026
- SWU ~$176 — UxC nuclear fuel price indicators (2024–25)
- Conversion/fabrication — WNA *Economics of Nuclear Power*; EPRI/INL fuel-cycle cost basis
- Capital $/kWe (FOAK 5k / NOAK 3.5k / high 10k) — NuScale (PowerMag/INN/IEEFA); IEA 2025 (GLOBSEC)
- O&M ($130/kWe-yr, $4.5/MWh) — OECD-NEA/IEA Projected Costs; Lazard
- Method — OECD-NEA/IEA LCOE; GIF-EMWG / IAEA G4ECONS code-of-accounts
