# synthetic_data_generator.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

# Dates for synthetic CO2 & Water overrides
special_dates = ["2018-01-01", "2018-01-02", "2019-01-01", "2019-01-02"]

# Predefined CO2 emissions for special dates
co2_special = [
    {"Date":"2018-01-01","Source":"Energy","Emissions":800},
    {"Date":"2018-01-01","Source":"Transport","Emissions":400},
    {"Date":"2018-01-01","Source":"Industry","Emissions":127},
    {"Date":"2018-01-02","Source":"Energy","Emissions":810},
    {"Date":"2018-01-02","Source":"Transport","Emissions":395},
    {"Date":"2018-01-02","Source":"Industry","Emissions":123},
    {"Date":"2019-01-01","Source":"Energy","Emissions":780},
    {"Date":"2019-01-01","Source":"Transport","Emissions":420},
    {"Date":"2019-01-01","Source":"Industry","Emissions":88},
    {"Date":"2019-01-02","Source":"Energy","Emissions":790},
    {"Date":"2019-01-02","Source":"Transport","Emissions":415},
    {"Date":"2019-01-02","Source":"Industry","Emissions":83},
]

# Predefined Water usage for special dates
water_special = [
    {"Date":"2018-01-01","Sector":"Residential","Usage":8000},
    {"Date":"2018-01-01","Sector":"Commercial","Usage":5000},
    {"Date":"2018-01-01","Sector":"Industrial","Usage":10000},
    {"Date":"2018-01-02","Sector":"Residential","Usage":8100},
    {"Date":"2018-01-02","Sector":"Commercial","Usage":4950},
    {"Date":"2018-01-02","Sector":"Industrial","Usage":10200},
    {"Date":"2019-01-01","Sector":"Residential","Usage":7900},
    {"Date":"2019-01-01","Sector":"Commercial","Usage":5100},
    {"Date":"2019-01-01","Sector":"Industrial","Usage":9800},
    {"Date":"2019-01-02","Sector":"Residential","Usage":8000},
    {"Date":"2019-01-02","Sector":"Commercial","Usage":5050},
    {"Date":"2019-01-02","Sector":"Industrial","Usage":9900},
]

# -----------------------------
# Energy Consumption (kWh)
# -----------------------------
energy_dates = pd.date_range(start="2018-01-01", end="2019-12-31", freq='D')
sectors = ['Residential', 'Commercial', 'Industrial']

energy_data = []
for date in energy_dates:
    if date.strftime("%Y-%m-%d") in special_dates:
        # Skip special dates (could add realistic values later)
        continue
    for sector in sectors:
        base = {'Residential': 4000, 'Commercial': 6000, 'Industrial': 8000}[sector]
        seasonal = 1 + 0.2*np.sin(2*np.pi*date.timetuple().tm_yday/365)
        value = base * seasonal + np.random.randint(-500, 500)
        energy_data.append([date.strftime("%Y-%m-%d"), sector, max(0, round(value))])

energy_df = pd.DataFrame(energy_data, columns=['Date', 'Sector', 'Consumption'])
energy_df.to_csv(f"{DATA_PATH}/energy_consumption.csv", index=False)
print("Energy consumption data saved.")

# -----------------------------
# Renewable Energy Generation (kWh)
# -----------------------------
sources = ['Solar', 'Wind']
renewable_data = []
for date in energy_dates:
    if date.strftime("%Y-%m-%d") in special_dates:
        continue
    for source in sources:
        if source == 'Solar':
            base = 1000
            seasonal = 1 + 0.5*np.sin(2*np.pi*(date.timetuple().tm_yday-80)/365)
            value = base * seasonal + np.random.randint(-100, 100)
        else:  # Wind
            value = 1500 + np.random.randint(-500, 500)
        renewable_data.append([date.strftime("%Y-%m-%d"), source, max(0, round(value))])

renewable_df = pd.DataFrame(renewable_data, columns=['Date', 'Source', 'Generation'])
renewable_df.to_csv(f"{DATA_PATH}/renewable_generation.csv", index=False)
print("Renewable generation data saved.")

# -----------------------------
# Water Usage (liters)
# -----------------------------
water_data = []
for date in energy_dates:
    if date.strftime("%Y-%m-%d") in special_dates:
        continue
    for sector in sectors:
        base = {'Residential': 8000, 'Commercial': 5000, 'Industrial': 10000}[sector]
        seasonal = 1 + 0.1*np.cos(2*np.pi*date.timetuple().tm_yday/365)
        value = base * seasonal + np.random.randint(-500, 500)
        water_data.append([date.strftime("%Y-%m-%d"), sector, max(0, round(value))])

# Add special dates
water_data.extend([[d['Date'], d['Sector'], d['Usage']] for d in water_special])
water_df = pd.DataFrame(water_data, columns=['Date', 'Sector', 'Usage'])
water_df.to_csv(f"{DATA_PATH}/water_usage.csv", index=False)
print("Water usage data saved.")

# -----------------------------
# CO2 Emissions (tonnes)
# -----------------------------
co2_data = []
for date in energy_dates:
    if date.strftime("%Y-%m-%d") in special_dates:
        continue
    for source in ['Energy', 'Transport', 'Industry']:
        base = {'Energy': 15, 'Transport': 8, 'Industry': 12}[source]
        seasonal = 1 + 0.1*np.sin(2*np.pi*date.timetuple().tm_yday/365)
        value = base * seasonal + np.random.uniform(-2, 2)
        co2_data.append([date.strftime("%Y-%m-%d"), source, round(value, 2)])

# Add special dates
co2_data.extend([[d['Date'], d['Source'], d['Emissions']] for d in co2_special])
co2_df = pd.DataFrame(co2_data, columns=['Date', 'Source', 'Emissions'])
co2_df.to_csv(f"{DATA_PATH}/co2_emissions.csv", index=False)
print("CO2 emissions data saved.")

print("All synthetic datasets generated successfully!")
