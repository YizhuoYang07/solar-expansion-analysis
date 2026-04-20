"""
Solar Energy Market Opportunity Analysis
AT3 – 36104 Data Visualisation and Narratives, UTS

Script location : data_management/processed/analysis.py
Run from repo root:
    .venv/bin/python data_management/processed/analysis.py

Datasets used:
  1. OWID energy-data          – data_management/raw/energy-data/owid-energy-data.csv
  2. IRENA installed capacity  – data_management/processed/installed_solar_capacity_owid.csv
  3. Solar PV module prices    – data_management/processed/solar_pv_prices_owid.csv
  4. World Bank PV potential   – data_management/processed/solar_pv_potential_worldbank.xlsx

Outputs written to data_management/processed/:
  - solar_merged_dataset.csv
  - solar_market_opportunity.csv
  - solar_top20_opportunity_markets.csv
  - solar_capacity_utilization.csv
  - solar_price_vs_adoption.csv
  - solar_pv_prices_clean.csv
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# ── Paths ────────────────────────────────────────────────────────────────────
# Script lives at: <repo_root>/analysis.py  (this folder IS the git repo root)
HERE        = os.path.dirname(os.path.abspath(__file__))   # repo root

ENERGY_CSV  = os.path.join(HERE, "raw", "owid-energy-data.csv")
CAP_CSV     = os.path.join(HERE, "installed_solar_capacity_owid.csv")
PRICE_CSV   = os.path.join(HERE, "solar_pv_prices_owid.csv")
WB_XLSX     = os.path.join(HERE, "solar_pv_potential_worldbank.xlsx")
OUT         = HERE


# ════════════════════════════════════════════════════════════════════════════
# 1.  LOAD & CLEAN OWID ENERGY DATA
# ════════════════════════════════════════════════════════════════════════════
print("Loading OWID energy data …")
energy = pd.read_csv(ENERGY_CSV, low_memory=False)

# Keep only real countries (3-char ISO codes, no aggregates)
energy = energy[energy["iso_code"].str.len() == 3].copy()

# Solar columns of interest
solar_cols = [
    "country", "iso_code", "year",
    "population", "gdp",
    "electricity_demand",       # TWh
    "electricity_generation",   # TWh
    "solar_consumption",        # TWh – primary energy equivalent
    "solar_elec_per_capita",    # kWh per person
    "solar_electricity",        # TWh generated
    "solar_share_elec",         # % of electricity from solar
    "solar_share_energy",       # % of primary energy from solar
]
energy = energy[solar_cols].copy()

# Fill solar NaN with 0 (no solar data = no meaningful generation)
for c in ["solar_consumption", "solar_elec_per_capita",
          "solar_electricity", "solar_share_elec", "solar_share_energy"]:
    energy[c] = energy[c].fillna(0)

# Filter year range 2000–2024 (overlap with IRENA capacity data)
energy = energy[(energy["year"] >= 2000) & (energy["year"] <= 2024)]
print(f"  → {len(energy):,} rows, {energy['iso_code'].nunique()} countries")


# ════════════════════════════════════════════════════════════════════════════
# 2.  LOAD IRENA INSTALLED CAPACITY
# ════════════════════════════════════════════════════════════════════════════
print("Loading IRENA installed solar capacity …")
cap = pd.read_csv(CAP_CSV)
cap.rename(columns={
    "Entity":    "country",
    "Code":      "iso_code",
    "Year":      "year",
    "Solar":     "installed_capacity_gw",   # GW
}, inplace=True)
cap = cap[cap["iso_code"].str.len() == 3].copy()
print(f"  → {len(cap):,} rows, {cap['iso_code'].nunique()} countries")


# ════════════════════════════════════════════════════════════════════════════
# 3.  LOAD SOLAR PV PRICES
# ════════════════════════════════════════════════════════════════════════════
print("Loading solar PV module prices …")
prices = pd.read_csv(PRICE_CSV)
prices.rename(columns={
    "Solar PV module cost": "pv_module_cost_usd_per_w",
}, inplace=True)
prices = prices[["Year", "pv_module_cost_usd_per_w"]].copy()
prices.rename(columns={"Year": "year"}, inplace=True)
print(f"  → {len(prices)} annual price observations (global)")


# ════════════════════════════════════════════════════════════════════════════
# 4.  LOAD WORLD BANK PV POTENTIAL (country-level GHI / PVOUT / LCOE)
# ════════════════════════════════════════════════════════════════════════════
print("Loading World Bank PV potential data …")
wb_raw = pd.read_excel(
    WB_XLSX,
    sheet_name="Country indicators",
    header=1,      # row index 1 is the actual header
    usecols=[0, 1, 9, 10, 11, 12, 17, 20],
)
wb_raw.columns = [
    "iso_code", "wb_country",
    "gdp_per_capita_2018",
    "ghi_kwh_m2_day",          # Global Horizontal Irradiation
    "pvout_kwh_kwp_day",       # Practical PV Power Output
    "lcoe_usd_kwh_2018",       # Levelised Cost of Electricity
    "rural_elec_access_pct",   # % rural population with electricity
    "elec_tariff_cent_kwh",    # Electricity tariff for SMEs (US cents/kWh)
]
# Drop non-country rows (empty iso_code)
wb_raw = wb_raw.dropna(subset=["iso_code"])
wb_raw["iso_code"] = wb_raw["iso_code"].astype(str).str.strip()
wb_raw = wb_raw[wb_raw["iso_code"].str.len() == 3].copy()

# Replace '#N/A' strings / coerce numeric columns only (preserve iso_code)
numeric_cols = [c for c in wb_raw.columns if c != "iso_code"]
for c in numeric_cols:
    wb_raw[c] = pd.to_numeric(wb_raw[c], errors="coerce")

print(f"  → {len(wb_raw)} countries with PV potential data")


# ════════════════════════════════════════════════════════════════════════════
# 5.  MERGE: energy × installed capacity (on iso_code + year)
# ════════════════════════════════════════════════════════════════════════════
print("Merging datasets …")
merged = energy.merge(
    cap[["iso_code", "year", "installed_capacity_gw"]],
    on=["iso_code", "year"],
    how="left",
)
merged["installed_capacity_gw"] = merged["installed_capacity_gw"].fillna(0)

# Merge World Bank potential (static, join on iso_code only)
merged = merged.merge(
    wb_raw.drop(columns=["wb_country", "gdp_per_capita_2018"]),
    on="iso_code",
    how="left",
)

# Save full merged dataset
merged.to_csv(os.path.join(OUT, "solar_merged_dataset.csv"), index=False)
print(f"  → Merged dataset: {len(merged):,} rows")


# ════════════════════════════════════════════════════════════════════════════
# 6.  DERIVED METRICS
# ════════════════════════════════════════════════════════════════════════════

# 6a. Capacity utilisation factor (generation / installed capacity)
#     solar_electricity is TWh; installed_capacity_gw × 8.76 = max possible TWh
#     (GW × 8760 h = GWh → ÷ 1000 = TWh → shortcut: GW × 8.76 = TWh)
merged["max_possible_twh"] = merged["installed_capacity_gw"] * 8.760
merged["capacity_util_factor"] = np.where(
    merged["max_possible_twh"] > 0,
    merged["solar_electricity"] / merged["max_possible_twh"],
    np.nan,
)

# 6b. Theoretical ceiling: if 1% of land captured at average PVOUT
#     (used only for illustration; primary opportunity metric is penetration rate)
#     penetration_rate = actual solar share of electricity / max solar share
#     We use PVOUT as a proxy for potential:
#       potential_annual_twh_per_gw = pvout_kwh_kwp_day * 365 / 1000  [TWh/GWp]
merged["pvout_twh_per_gwp_year"] = merged["pvout_kwh_kwp_day"] * 365 / 1000

# 6c. CAGR of solar electricity 2019→2024 (5-year window)
solar_2019 = (
    merged[merged["year"] == 2019][["iso_code", "solar_electricity"]]
    .rename(columns={"solar_electricity": "solar_2019"})
)
solar_2024 = (
    merged[merged["year"] == 2024][["iso_code", "solar_electricity"]]
    .rename(columns={"solar_electricity": "solar_2024"})
)
cagr_df = solar_2019.merge(solar_2024, on="iso_code")
cagr_df["solar_cagr_5yr"] = np.where(
    (cagr_df["solar_2019"] > 0.001) & (cagr_df["solar_2024"] > 0.001),
    (cagr_df["solar_2024"] / cagr_df["solar_2019"]) ** (1 / 5) - 1,
    np.nan,
)


# ════════════════════════════════════════════════════════════════════════════
# 7.  MARKET OPPORTUNITY SNAPSHOT (2024 latest year)
# ════════════════════════════════════════════════════════════════════════════
snap = merged[merged["year"] == 2024].copy()
snap = snap.merge(cagr_df[["iso_code", "solar_cagr_5yr", "solar_2019", "solar_2024"]], on="iso_code", how="left")

# Absolute installed capacity added 2019-2024
cap_2019 = (
    cap[cap["year"] == 2019][["iso_code", "installed_capacity_gw"]]
    .rename(columns={"installed_capacity_gw": "cap_2019_gw"})
)
cap_2024 = (
    cap[cap["year"] == 2024][["iso_code", "installed_capacity_gw"]]
    .rename(columns={"installed_capacity_gw": "cap_2024_gw"})
)
cap_growth = cap_2019.merge(cap_2024, on="iso_code")
cap_growth["cap_added_gw_5yr"] = cap_growth["cap_2024_gw"] - cap_growth["cap_2019_gw"]
snap = snap.merge(cap_growth, on="iso_code", how="left")

# Market opportunity score (composite):
#   High PVOUT  → good natural conditions (normalised 0–1)
#   Low solar_share_elec → untapped market
#   High GDP per capita → ability to pay / invest
#   High electricity demand → large addressable market
#   High CAGR → momentum

def minmax(s):
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng > 0 else s * 0

# Diagnostics
print(f"  → 2024 snapshot rows: {len(snap)}")
print(f"  → With PVOUT: {snap['pvout_kwh_kwp_day'].notna().sum()}")
print(f"  → With CAGR: {snap['solar_cagr_5yr'].notna().sum()}")
print(f"  → With electricity_demand: {snap['electricity_demand'].notna().sum()}")

# Relax filter: CAGR optional (fill with 0 for countries with no prior solar)
snap["solar_cagr_5yr"] = snap["solar_cagr_5yr"].fillna(0)
snap["electricity_demand"] = snap["electricity_demand"].fillna(snap["electricity_demand"].median())
snap_clean = snap.dropna(subset=["pvout_kwh_kwp_day", "solar_share_elec"]).copy()

snap_clean["score_pvout"]      = minmax(snap_clean["pvout_kwh_kwp_day"])
snap_clean["score_untapped"]   = minmax(100 - snap_clean["solar_share_elec"].clip(0, 100))
snap_clean["score_demand"]     = minmax(snap_clean["electricity_demand"].clip(0))
snap_clean["score_cagr"]       = minmax(snap_clean["solar_cagr_5yr"].clip(0, 2))
snap_clean["score_gdp"]        = minmax(
    snap_clean["gdp"].fillna(0).clip(0) / snap_clean["population"].replace(0, np.nan)
)

snap_clean["opportunity_score"] = (
    0.25 * snap_clean["score_pvout"]
    + 0.25 * snap_clean["score_untapped"]
    + 0.20 * snap_clean["score_demand"]
    + 0.20 * snap_clean["score_cagr"]
    + 0.10 * snap_clean["score_gdp"]
)

output_cols = [
    "country", "iso_code",
    "solar_share_elec", "solar_electricity",
    "installed_capacity_gw", "capacity_util_factor",
    "ghi_kwh_m2_day", "pvout_kwh_kwp_day", "lcoe_usd_kwh_2018",
    "elec_tariff_cent_kwh", "rural_elec_access_pct",
    "electricity_demand", "solar_cagr_5yr",
    "cap_2019_gw", "cap_2024_gw", "cap_added_gw_5yr",
    "opportunity_score",
]
opp = snap_clean[output_cols].sort_values("opportunity_score", ascending=False)
opp.to_csv(os.path.join(OUT, "solar_market_opportunity.csv"), index=False)

top20 = opp.head(20)
top20.to_csv(os.path.join(OUT, "solar_top20_opportunity_markets.csv"), index=False)
print(f"  → Market opportunity table: {len(opp)} countries")


# ════════════════════════════════════════════════════════════════════════════
# 8.  CAPACITY UTILISATION TIME-SERIES (2010-2024, top emitters/producers)
# ════════════════════════════════════════════════════════════════════════════
focus_countries = ["CHN", "USA", "IND", "DEU", "JPN", "AUS", "BRA", "ESP", "ITA", "GBR"]
util_ts = merged[
    (merged["iso_code"].isin(focus_countries)) &
    (merged["year"] >= 2010) &
    (merged["capacity_util_factor"].notna()) &
    (merged["capacity_util_factor"] > 0)
][["country", "iso_code", "year", "installed_capacity_gw",
   "solar_electricity", "capacity_util_factor"]].copy()
util_ts.to_csv(os.path.join(OUT, "solar_capacity_utilization.csv"), index=False)
print(f"  → Capacity utilization time-series: {len(util_ts)} rows")


# ════════════════════════════════════════════════════════════════════════════
# 9.  PV PRICE VS. GLOBAL ADOPTION (annual, world totals)
# ════════════════════════════════════════════════════════════════════════════
world_solar = (
    energy[energy["iso_code"] == "WLD"]   # OWID world aggregate
    [["year", "solar_electricity", "solar_share_elec"]]
    .copy()
)
if world_solar.empty:
    # Fallback: sum all countries
    world_solar = (
        energy.groupby("year")[["solar_electricity"]].sum().reset_index()
    )
    world_solar["solar_share_elec"] = np.nan

price_adoption = prices.merge(world_solar, on="year", how="inner")
price_adoption.to_csv(os.path.join(OUT, "solar_price_vs_adoption.csv"), index=False)

prices.to_csv(os.path.join(OUT, "solar_pv_prices_clean.csv"), index=False)
print(f"  → Price vs adoption: {len(price_adoption)} rows")


# ════════════════════════════════════════════════════════════════════════════
# 10.  PRINT SUMMARY STATISTICS
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("KEY SUMMARY STATISTICS")
print("="*60)

# Global solar electricity 2024
world_gen_2024 = energy[
    (energy["year"] == 2024)
]["solar_electricity"].sum()
print(f"\nGlobal solar electricity generated (2024): {world_gen_2024:,.0f} TWh")

# Price drop
p_1975 = prices.loc[prices["year"] == 1975, "pv_module_cost_usd_per_w"].values[0]
p_2024 = prices.loc[prices["year"] == 2024, "pv_module_cost_usd_per_w"].values[0]
print(f"PV module price 1975: ${p_1975:.2f}/W  →  2024: ${p_2024:.4f}/W  "
      f"({(1 - p_2024/p_1975)*100:.1f}% decline)")

# Top 10 opportunity markets
print("\nTop 10 Solar Expansion Opportunity Markets:")
print(top20[["country", "solar_share_elec", "pvout_kwh_kwp_day",
             "solar_cagr_5yr", "cap_added_gw_5yr",
             "opportunity_score"]].head(10).to_string(index=False))

# Fastest growing 2019-2024
print("\nTop 10 Fastest-Growing Solar Markets (5-yr CAGR, 2019-2024):")
fast = opp.dropna(subset=["solar_cagr_5yr"]).nlargest(10, "solar_cagr_5yr")[
    ["country", "solar_cagr_5yr", "solar_electricity", "installed_capacity_gw"]
]
fast["solar_cagr_5yr_%"] = (fast["solar_cagr_5yr"] * 100).round(1)
print(fast[["country", "solar_cagr_5yr_%", "solar_electricity", "installed_capacity_gw"]].to_string(index=False))

# Highest PVOUT countries (best natural conditions)
print("\nTop 10 Countries by Solar Resource (PVOUT, kWh/kWp/day):")
pvout_top = opp.nlargest(10, "pvout_kwh_kwp_day")[
    ["country", "pvout_kwh_kwp_day", "ghi_kwh_m2_day",
     "solar_share_elec", "solar_cagr_5yr"]
]
print(pvout_top.to_string(index=False))

# Capacity utilization comparison (2024)
print("\nCapacity Utilization Factor – Selected Countries (2024):")
util_2024 = merged[
    (merged["year"] == 2024) &
    (merged["iso_code"].isin(focus_countries)) &
    (merged["capacity_util_factor"].notna())
][["country", "installed_capacity_gw", "solar_electricity", "capacity_util_factor"]]
print(util_2024.sort_values("capacity_util_factor", ascending=False).to_string(index=False))

print("\n" + "="*60)
print("All output files written to:", OUT)
print("="*60)
