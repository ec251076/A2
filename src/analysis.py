# src/analysis.py

import pandas as pd

def total_energy(energy_df):
    return energy_df['Consumption'].sum()

def total_renewable(renewable_df):
    return renewable_df['Generation'].sum()

def renewable_percentage(energy_df, renewable_df):
    return round(total_renewable(renewable_df) / total_energy(energy_df) * 100, 2)

def total_water(water_df):
    return water_df['Usage'].sum()

def total_co2(co2_df):
    return co2_df['Emissions'].sum()

def monthly_aggregation(df, value_col):
    """Aggregate daily data to monthly sums."""
    df_month = df.groupby(df['Date'].dt.to_period("M"))[value_col].sum().reset_index()
    df_month['Date'] = df_month['Date'].dt.to_timestamp()
    return df_month

def latest_values(df, value_col):
    """Return the latest values for a given column."""
    latest_date = df['Date'].max()
    latest_df = df[df['Date'] == latest_date][['Sector', value_col]] if 'Sector' in df.columns else df[df['Date'] == latest_date]
    return latest_df, latest_date
