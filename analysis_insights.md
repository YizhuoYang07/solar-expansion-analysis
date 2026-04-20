# Solar Energy Market Opportunity – Data Analysis Insights
**AT3 – 36104 Data Visualisation and Narratives, UTS**  
**Generated from multi-dataset analysis (April 2025)**

---

## Datasets Used

| Dataset | Source | Coverage | Join Key |
|---|---|---|---|
| OWID Energy Data | Our World in Data / Ember / Energy Institute | 220 countries, 2000–2024 | iso_code + year |
| IRENA Installed Solar Capacity | IRENA (2025) via Our World in Data | 220 countries, 2000–2024 | iso_code + year |
| Solar PV Module Prices | IRENA / Nemet / Farmer & Lafond (via OWID) | Global, 1975–2024 | year |
| World Bank PV Potential by Country | Solargis / World Bank (2020) | 209 countries, static | iso_code |

**HD enrichment:** All four datasets are joined in `solar_merged_dataset.csv` via `iso_code` (country-level) and `year` (temporal) keys, creating a richer analytical base than any single source.

---

## Insight 1: The 99.8% Price Revolution

Solar PV module prices have fallen from **$128.27/W (1975)** to **$0.258/W (2024)** — a **99.8% decline** over 50 years, accelerating after 2010.

- In 2010, panels cost ~$1.90/W; by 2024 that is just $0.258/W (86% drop in 14 years).
- This cost collapse is the single biggest driver of solar's global expansion.
- **Implication for narrative:** A solar company expanding today operates at a structural cost advantage unimaginable a decade ago.

> *Source: solar_pv_prices_clean.csv*

---

## Insight 2: Global Solar Electricity Has Crossed 2,000 TWh

Global solar electricity generation reached **2,094 TWh in 2024**, up from an estimated 180 TWh in 2015 — a **12× increase in nine years**.

- Solar now accounts for a meaningful share of global electricity in many leading nations.
- **China** leads with **839 TWh** generated (2024) from **887 GW** installed — the largest solar fleet ever built.
- **United States**: 303.75 TWh | **India**: 136.75 TWh | **Brazil**: 71.32 TWh | **Germany**: 74.13 TWh

> *Source: solar_merged_dataset.csv*

---

## Insight 3: Who Uses Solar Best? — Capacity Utilisation Analysis

Capacity utilisation factor (actual generation ÷ theoretical maximum) reveals how efficiently countries convert installed panels into usable electricity.

| Country | Installed (GW) | Generated (TWh, 2024) | Capacity Factor |
|---|---|---|---|
| United States | 177.6 | 303.75 | **19.5%** |
| Spain | 38.6 | 58.29 | **17.2%** |
| India | 97.6 | 136.75 | **16.0%** |
| Australia | 35.9 | 50.21 | **16.0%** |
| Brazil | 53.1 | 71.32 | **15.3%** |
| Japan | 89.6 | 96.70 | **12.3%** |
| Germany | 89.9 | 74.13 | **9.4%** |

**Key finding:** The US and Spain achieve the highest capacity factors (>17%), reflecting both excellent sunny climates *and* efficient grid integration. Germany's 9.4% reflects its northerly latitude — it invests heavily in solar for energy independence, not raw yield.

Countries in the Middle East and North Africa (MENA) region with PVOUT > 5.0 kWh/kWp/day (versus Germany's ~2.8) have **substantially higher physical potential** — yet most remain underdeveloped.

> *Source: solar_capacity_utilization.csv*

---

## Insight 4: The Untapped Frontier — Top 10 Market Opportunity Index

Using a composite opportunity score (weighted: solar resource potential 25%, untapped market share 25%, electricity demand scale 20%, 5-yr growth rate 20%, GDP per capita 10%):

| Rank | Country | Solar Share (%) | PVOUT (kWh/kWp/day) | 5-yr CAGR | Capacity Added (GW, 2019–2024) | Score |
|---|---|---|---|---|---|---|
| 1 | **Saudi Arabia** | 1.8% | 5.16 | +108% | 4.2 GW | 0.672 |
| 2 | **Oman** | 3.9% | 5.17 | +102% | 0.6 GW | 0.632 |
| 3 | **China** | 8.3% | 3.88 | +30% | 682 GW | 0.540 |
| 4 | **Egypt** | 2.6% | 5.25 | +32% | 0.9 GW | 0.528 |
| 5 | **Colombia** | 3.7% | 4.05 | +90% | 1.4 GW | 0.515 |
| 6 | **Kuwait** | 0.2% | 4.82 | +26% | 0.02 GW | 0.499 |
| 7 | **Pakistan** | 10.0% | 4.71 | +81% | 3.0 GW | 0.493 |
| 8 | **Iran** | 0.2% | 4.92 | +12% | 0.4 GW | 0.488 |
| 9 | **Yemen** | 0.0% | 5.21 | — | 0.15 GW | 0.488 |
| 10 | **Tunisia** | 2.4% | 4.74 | +32% | 0.7 GW | 0.482 |

**Pattern:** MENA dominates the top tier. These countries combine exceptional solar irradiance (PVOUT 4.7–5.25, vs Germany's ~2.8) with currently tiny solar shares (<4%) — a massive gap between potential and actuality.

> *Source: solar_top20_opportunity_markets.csv, solar_market_opportunity.csv*

---

## Insight 5: Fastest-Growing Solar Markets (5-yr CAGR, 2019–2024)

| Country | 5-yr CAGR | 2024 Generation (TWh) | 2024 Installed (GW) |
|---|---|---|---|
| Saudi Arabia | +108% | 8.23 | 4.3 |
| Ireland | +105% | 1.09 | 1.3 |
| Norway | +105% | 0.36 | 0.8 |
| Oman | +102% | 1.70 | 0.7 |
| Poland | +90% | 17.66 | 20.2 |
| Colombia | +90% | 3.21 | 1.4 |
| Pakistan | +81% | 18.15 | 3.7 |
| North Macedonia | +74% | 0.32 | 0.8 |
| Lithuania | +73% | 1.40 | 2.6 |
| Armenia | +70% | 0.85 | 0.5 |

**Key finding:** Saudi Arabia and Oman are growing from a low base but at extraordinary rates — these markets are just opening up. Poland, Pakistan, and Colombia represent scale-up markets where significant capacity has already been deployed and momentum is building.

> *Source: solar_market_opportunity.csv*

---

## Insight 6: Best Physical Solar Resources (Where Nature Favours Solar)

PVOUT (Practical PV Output) measures the actual kWh a 1 kWp system produces per day, accounting for temperature, dust, and geography.

| Country | PVOUT (kWh/kWp/day) | GHI (kWh/m²/day) | Current Solar Share (%) |
|---|---|---|---|
| Chile | 5.36 | 5.76 | 22.3% (already developed!) |
| Egypt | 5.25 | 6.26 | 2.6% (huge gap) |
| Yemen | 5.21 | 6.47 | 0.0% (conflict-affected) |
| Oman | 5.17 | 6.28 | 3.9% |
| Saudi Arabia | 5.16 | 6.21 | 1.8% |
| Libya | 5.12 | 6.13 | 0.0% |
| Israel | 5.08 | 5.75 | 0.0% |
| Morocco | 5.01 | 5.56 | 3.6% |
| UAE | 5.00 | 6.05 | 8.6% |
| South Africa | 5.00 | 5.63 | 8.0% |

**Narrative hook (Detective Arc):** Chile proves the thesis — with PVOUT of 5.36, it has already achieved 22.3% solar share. Countries like Egypt, Oman, and Saudi Arabia with virtually identical PVOUT (5.16–5.25) are at 2–4% solar share. *Why the gap?* The anomaly points to investment, policy, and infrastructure — not physical limitations.

> *Source: solar_market_opportunity.csv, World Bank PV Potential data*

---

## Insight 7: Price Collapse Drives Adoption — The S-Curve

The price-adoption relationship captured in `solar_price_vs_adoption.csv` (2000–2024) reveals:

- **2000–2009**: Prices fell from ~$5/W to ~$2/W; adoption remained minimal (global solar <0.5%)
- **2010–2016**: Prices crashed from $1.90/W to $0.39/W; global solar share crossed 1%
- **2017–2024**: Prices stabilised below $0.30/W; adoption surged — annual additions exceeded 200 GW/year by 2022

**Implication:** The cost barrier has essentially been removed. Market expansion now depends on policy, grid infrastructure, and financing — areas where a global solar developer can add value.

---

## Summary: The Opportunity Matrix

```
HIGH PVOUT                     ←—— Solar Resource ——→          LOW PVOUT
     │                                                              │
HIGH │  [PRIME TARGETS]              [GROWTH MATURE]               │
CAGR │  Saudi Arabia, Oman           Chile (22% share)             │
     │  Egypt, Colombia              Australia, Spain              │
     │  Pakistan                                                    │
     │                                                              │
LOW  │  [LATENT GIANTS]              [SATURATED MARKETS]           │
CAGR │  Libya, Yemen (conflict)      Germany, Japan                │
     │  Kuwait, Iran (policy)        UK, Italy                     │
     └──────────────────────────────────────────────────────────────
```

**Best expansion target zone:** High PVOUT + High CAGR + Low current share = **Saudi Arabia, Oman, Egypt, Colombia, Pakistan**

These countries have the physical conditions, the momentum, and the remaining runway to deploy large volumes of solar capacity.

---

## Data Files Reference

| File | Description | Rows |
|---|---|---|
| `solar_merged_dataset.csv` | Full join: OWID energy + IRENA capacity + WB potential | 5,383 |
| `solar_market_opportunity.csv` | 2024 snapshot with opportunity scores (119 countries) | 119 |
| `solar_top20_opportunity_markets.csv` | Top 20 opportunity markets | 20 |
| `solar_capacity_utilization.csv` | Capacity utilisation 2010-2024, 10 key countries | 146 |
| `solar_price_vs_adoption.csv` | Global PV price vs solar share, 2000-2024 | 25 |
| `solar_pv_prices_clean.csv` | Annual PV module price 1975-2024 | 50 |
| `solar_pv_potential_worldbank.xlsx` | World Bank country-level GHI/PVOUT/LCOE (source) | 209 |

---

*Analysis by AT3 Group, 36104 Data Visualisation and Narratives, UTS, 2025*
