# solar-opportunity-analysis

Supplementary data analysis for **UTS 36104 AT3 — Solar Energy Expansion Narrative** (Group 17, 2026).

This repository covers **my individual contribution**: sourcing supplementary datasets, joining them to the primary OWID energy dataset, computing market opportunity scores, and producing the analytical outputs that feed into the group's Tableau/Streamlit visualisation.

---

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/<your-username>/solar-opportunity-analysis.git
cd solar-opportunity-analysis

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Obtain the raw OWID energy data (gitignored — too large)
#    Download owid-energy-data.csv from:
#    https://github.com/owid/energy-data
#    and place it at:  raw/owid-energy-data.csv

# 4. Run analysis
python analysis.py
```

---

## Repository Structure

```
solar-opportunity-analysis/
├── .gitignore
├── requirements.txt
├── README.md
├── analysis.py                         ← main analysis script
├── analysis_insights.md                ← 7 written insights
├── stakeholder_candidates.md           ← stakeholder evaluation
├── raw/
│   └── owid-energy-data.csv            ← gitignored (download separately)
├── installed_solar_capacity_owid.csv   ← supplementary input
├── solar_pv_prices_owid.csv            ← supplementary input
├── solar_pv_potential_worldbank.xlsx   ← supplementary input
├── solar_merged_dataset.csv            ← gitignored (large, regenerated)
├── solar_market_opportunity.csv
├── solar_top20_opportunity_markets.csv
├── solar_capacity_utilization.csv
├── solar_price_vs_adoption.csv
└── solar_pv_prices_clean.csv
```

---

## Raw Data — Source Declaration

`raw/owid-energy-data.csv` is a copy of the primary dataset maintained by **Our World in Data**:

> Hannah Ritchie, Pablo Rosado, Max Roser et al. (2023). *Energy*. Published online at OurWorldInData.org. Retrieved from https://github.com/owid/energy-data — Licence: **CC BY 4.0**.

This file is **not committed** to this repository (it is listed in `.gitignore`) because it exceeds GitHub's recommended file-size limit. It can be re-downloaded at any time from the link above. The version used for this analysis was retrieved in April 2026.

---

## Input Files (committed to repo)

| File | Description | Source | Coverage |
|---|---|---|---|
| `installed_solar_capacity_owid.csv` | Cumulative installed solar capacity by country, GW | IRENA (2025) via Our World in Data | 220 countries, 2000–2024 |
| `solar_pv_prices_owid.csv` | Solar PV module cost, USD/W (inflation-adjusted) | IRENA / Nemet / Farmer & Lafond via OWID | Global, 1975–2024 |
| `solar_pv_potential_worldbank.xlsx` | Country-level GHI, PVOUT, LCOE, electricity tariffs | Solargis / World Bank ESMAP (2020) | 209 countries, static (2018-era) |

**Download sources:**
- Installed capacity: https://ourworldindata.org/grapher/installed-solar-pv-capacity.csv?v=1&csvType=full&useColumnShortNames=false
- PV prices: https://ourworldindata.org/grapher/solar-pv-prices.csv?v=1&csvType=full&useColumnShortNames=false
- WB PV potential: https://datacatalogfiles.worldbank.org/ddh-published/0038379/1/DR0046831/solargis_pvpotential_countryranking_2020_data.xlsx

---

## Analysis Script

### `analysis.py`

Run from the **repository root** (after Quick Start steps above):

```bash
python analysis.py
```

**Pipeline:**
1. Load OWID energy data (primary dataset, raw/)
2. Load IRENA installed capacity (supplementary)
3. Load solar PV module prices (supplementary)
4. Load World Bank PV potential (supplementary)
5. Merge all four datasets on `iso_code` + `year`
6. Compute derived metrics: capacity utilisation factor, 5-year CAGR, composite opportunity score
7. Export output CSVs (see below)

---

## Generated Output Files

> These files are regenerated each time `analysis.py` runs. They are committed for reference but can be reproduced from scratch.

| File | Description | Rows |
|---|---|---|
| `solar_merged_dataset.csv` | Full 4-dataset join: OWID energy + IRENA capacity + WB potential | 5,383 |
| `solar_market_opportunity.csv` | 2024 country snapshot with composite opportunity score | 119 |
| `solar_top20_opportunity_markets.csv` | Top 20 opportunity markets ranked | 20 |
| `solar_capacity_utilization.csv` | Capacity utilisation time-series for 10 key countries (2010–2024) | 146 |
| `solar_price_vs_adoption.csv` | Global annual PV price vs solar share (2000–2024) | 25 |
| `solar_pv_prices_clean.csv` | Cleaned annual PV module price (1975–2024) | 50 |

---

## Documentation Files

| File | Description |
|---|---|
| `analysis_insights.md` | 7 key insights derived from the analysis |
| `stakeholder_candidates.md` | Evaluation of 3 candidate stakeholder companies |

---

## Data Joins

```
owid-energy-data.csv          ← primary (iso_code + year)
        │
        ├── JOIN installed_solar_capacity_owid.csv   (iso_code + year)
        │
        ├── JOIN solar_pv_prices_owid.csv            (year, global)
        │
        └── JOIN solar_pv_potential_worldbank.xlsx   (iso_code, static)
                         │
                         └── solar_merged_dataset.csv
```

This multi-dataset join satisfies the **HD enrichment requirement** of AT3: the merged dataset spans temporal (2000–2024), spatial (220 countries), physical (GHI/PVOUT), economic (GDP, tariffs), and technology (PV prices) dimensions — no single source provides all five.

---

## Data Dictionary

Variable-level definitions for the key analytical outputs. All variables appear in `solar_merged_dataset.csv`; starred (★) variables also appear in `solar_market_opportunity.csv`.

### Identity & Temporal

| Variable | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `iso_code` ★ | string | — | ISO 3166-1 alpha-3 country code (join key) | OWID energy data |
| `country` ★ | string | — | Country or region name | OWID energy data |
| `year` | integer | — | Calendar year (2000–2024) | OWID energy data |

### Solar Generation & Capacity

| Variable | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `solar_electricity` | float | TWh | Total solar electricity generated per year | OWID energy data (IEA/Ember) |
| `solar_share_elec` | float | % | Solar electricity as a share of total electricity generation | OWID energy data |
| `solar_capacity` | float | GW | Cumulative installed solar PV capacity (end-of-year) | IRENA (2025) via OWID |
| `solar_pv_price` | float | USD/W | Solar PV module cost, inflation-adjusted to 2023 USD | IRENA / Nemet / Farmer & Lafond via OWID |

### Physical Potential (static, country-level)

| Variable | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `PVOUT` ★ | float | kWh/kWp/day | Specific PV power output — energy a 1 kWp system produces per day under local irradiance conditions | Solargis / World Bank ESMAP (2020) |
| `GHI` | float | kWh/m²/day | Global Horizontal Irradiance — total solar radiation reaching a horizontal surface per day | Solargis / World Bank ESMAP (2020) |
| `LCOE` | float | USD/kWh | Levelised Cost of Energy for utility-scale solar PV | Solargis / World Bank ESMAP (2020) |
| `ELECTARIFF` | float | USD/kWh | Average local retail electricity tariff | Solargis / World Bank ESMAP (2020) |

### Economic Context

| Variable | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `GDP_per_capita` ★ | float | USD | GDP per capita (current USD) — proxy for market affordability and grid investment capacity | World Bank WDI (2024) via OWID |
| `primary_energy_consumption` | float | TWh | Total primary energy consumption per year — proxy for overall energy demand | OWID energy data (EIA/BP) |

### Derived Metrics

| Variable | Type | Unit | Definition | Calculation |
|---|---|---|---|---|
| `capacity_util_factor` ★ | float | ratio (0–1) | Actual solar electricity generation as a fraction of theoretical maximum capacity output | `solar_electricity / (solar_capacity × 8.760)` (GW → TWh via 8,760 h/yr) |
| `solar_cagr_5yr` ★ | float | decimal (e.g. 0.12 = 12%) | 5-year compound annual growth rate of solar electricity generation | `(solar_electricity_t / solar_electricity_t-5)^(1/5) − 1` |
| `untapped_potential` ★ | float | ratio | Gap between physical resource (normalised PVOUT) and current utilisation (capacity_util_factor) — higher = more room to grow | `norm(PVOUT) − norm(capacity_util_factor)` |

### Normalised Sub-scores (`solar_market_opportunity.csv` only)

All sub-scores are min–max normalised to [0, 1] across the 2024 country snapshot.

| Variable | Type | Unit | Definition | Weight in composite |
|---|---|---|---|---|
| `score_pvout` ★ | float | 0–1 | Normalised PVOUT (physical resource quality) | 25% |
| `score_untapped` ★ | float | 0–1 | Normalised untapped potential | 25% |
| `score_demand` ★ | float | 0–1 | Normalised primary energy consumption (market size) | 20% |
| `score_cagr` ★ | float | 0–1 | Normalised 5-year solar CAGR (growth momentum) | 20% |
| `score_gdp` ★ | float | 0–1 | Normalised GDP per capita (investment readiness) | 10% |
| `opportunity_score` ★ | float | 0–1 | **Composite weighted score** = 0.25 × score_pvout + 0.25 × score_untapped + 0.20 × score_demand + 0.20 × score_cagr + 0.10 × score_gdp | — |

---

## Credits

### Data Sources

| Dataset | Publisher | Licence | Retrieved |
|---|---|---|---|
| [OWID Energy Data](https://github.com/owid/energy-data) — primary dataset covering solar generation, solar share, and energy consumption by country/year | Our World in Data (Ritchie, Rosado, Roser et al., 2023) | CC BY 4.0 | April 2026 |
| [Installed Solar PV Capacity](https://ourworldindata.org/grapher/installed-solar-pv-capacity) — cumulative installed capacity by country/year | IRENA (2025) via Our World in Data | CC BY 4.0 | April 2026 |
| [Solar PV Module Prices](https://ourworldindata.org/grapher/solar-pv-prices) — inflation-adjusted module cost, 1975–2024 | IRENA / Nemet (2009) / Farmer & Lafond (2016) via Our World in Data | CC BY 4.0 | April 2026 |
| [Global Solar Atlas Country Rankings](https://datacatalog.worldbank.org/dataset/solar-photovoltaic-power-potential-country) — PVOUT, GHI, LCOE, electricity tariffs by country | Solargis / World Bank ESMAP (2020) | CC BY 4.0 | April 2026 |

### APA 7th References

Ritchie, H., Rosado, P., & Roser, M. (2023). *Energy*. Our World in Data. https://github.com/owid/energy-data

IRENA. (2025). *Renewable power generation costs in 2024*. International Renewable Energy Agency. https://ourworldindata.org/grapher/installed-solar-pv-capacity

Solargis & World Bank ESMAP. (2020). *Global photovoltaic power potential by country*. World Bank Open Data. https://datacatalog.worldbank.org/dataset/solar-photovoltaic-power-potential-country

### Individual Contribution

This repository represents the **data preparation and analysis** contribution of **Ricki Yang (Yizhuo Yang)** to UTS 36104 AT3, Group 17 (2026). Responsibilities: dataset sourcing, multi-dataset join design, derived metric computation (CAGR, capacity utilisation, composite opportunity score), and CSV output generation for the group's Streamlit dashboard.

Group Streamlit Dashboard: https://solar-expansion.streamlit.app/  
Group GitHub (frontend): https://github.com/prathameshn21/DVN_Assignment3
