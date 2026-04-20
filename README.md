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
