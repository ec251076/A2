# src/data_processing.py

import pandas as pd
import os

def load_csv(file_path):
    df = pd.read_csv(file_path)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    return df

def clean_energy(df):
    """Clean energy dataframe."""
    df = df.dropna()
    df['Consumption'] = df['Consumption'].clip(lower=0)
    return df

def clean_renewable(df):
    """Clean renewable generation dataframe."""
    df = df.dropna()
    df['Generation'] = df['Generation'].clip(lower=0)
    return df

def clean_water(df):
    """Clean water usage dataframe."""
    df = df.dropna()
    df['Usage'] = df['Usage'].clip(lower=0)
    return df

def clean_co2(df):
    """Clean CO2 emissions dataframe."""
    df = df.dropna()
    df['Emissions'] = df['Emissions'].clip(lower=0)
    return df

def load_all_data():
    """Load and clean all datasets."""
    from src.utils import DATA_PATH
    energy = clean_energy(load_csv(f"{DATA_PATH}/energy_consumption.csv"))
    renewable = clean_renewable(load_csv(f"{DATA_PATH}/renewable_generation.csv"))
    water = clean_water(load_csv(f"{DATA_PATH}/water_usage.csv"))
    co2 = clean_co2(load_csv(f"{DATA_PATH}/co2_emissions.csv"))
    return energy, renewable, water, co2
