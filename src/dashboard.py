# src/dashboard.py

import sys
import os
import streamlit as st

# -----------------------------
# Fix for ModuleNotFoundError
# -----------------------------
# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# -----------------------------
# Imports from other scripts
# -----------------------------
from src.data_processing import load_all_data
from src.analysis import (
    total_energy,
    total_renewable,
    renewable_percentage,
    total_water,
    total_co2,
    monthly_aggregation,
    latest_values
)
from src.visualizations import plot_line, plot_bar, plot_pie

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Island Dashboard", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
energy_df, renewable_df, water_df, co2_df = load_all_data()

# -----------------------------
# Sidebar Navigation
# -----------------------------
page = st.sidebar.selectbox(
    "Select Page",
    ["Overview", "Energy", "Water", "Environment"]
)

# -----------------------------
# Overview Page
# -----------------------------
if page == "Overview":
    st.title("🏝️ Island Sustainability Overview")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Energy (kWh)", f"{total_energy(energy_df):,}")
    col2.metric("Renewable %", f"{renewable_percentage(energy_df, renewable_df)}%")
    col3.metric("Total Water (L)", f"{total_water(water_df):,}")
    col4.metric("Total CO2 (t)", f"{total_co2(co2_df):.2f}")

    # Monthly energy vs renewable
    energy_month = monthly_aggregation(energy_df, 'Consumption')
    renewable_month = monthly_aggregation(renewable_df, 'Generation')
    merged = energy_month.merge(renewable_month, on='Date')
    fig = plot_line(
        merged,
        x='Date',
        y=['Consumption', 'Generation'],
        title="Monthly Energy vs Renewable Generation"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Energy Page
# -----------------------------
elif page == "Energy":
    st.title("⚡ Energy Dashboard")
    sector = st.multiselect(
        "Select Sector(s)",
        options=energy_df['Sector'].unique(),
        default=energy_df['Sector'].unique()
    )
    filtered_energy = energy_df[energy_df['Sector'].isin(sector)]
    fig = plot_line(
        filtered_energy,
        x='Date',
        y='Consumption',
        color='Sector',
        title="Energy Consumption Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Water Page
# -----------------------------
elif page == "Water":
    st.title("💧 Water Dashboard")
    sector = st.multiselect(
        "Select Sector(s)",
        options=water_df['Sector'].unique(),
        default=water_df['Sector'].unique()
    )
    filtered_water = water_df[water_df['Sector'].isin(sector)]
    fig1 = plot_line(
        filtered_water,
        x='Date',
        y='Usage',
        color='Sector',
        title="Water Usage Over Time"
    )
    st.plotly_chart(fig1, use_container_width=True)

    latest_df, latest_date = latest_values(filtered_water, 'Usage')
    fig2 = plot_pie(
        latest_df,
        names='Sector',
        values='Usage',
        title=f"Water Usage by Sector on {latest_date.date()}"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Environment Page
# -----------------------------
elif page == "Environment":
    st.title("🌱 CO2 Emissions Dashboard")
    source = st.multiselect(
        "Select Source(s)",
        options=co2_df['Source'].unique(),
        default=co2_df['Source'].unique()
    )
    filtered_co2 = co2_df[co2_df['Source'].isin(source)]

    fig1 = plot_line(
        filtered_co2,
        x='Date',
        y='Emissions',
        color='Source',
        title="CO2 Emissions Over Time"
    )
    st.plotly_chart(fig1, use_container_width=True)

    total_emissions = filtered_co2.groupby('Source')['Emissions'].sum().reset_index()
    fig2 = plot_bar(
        total_emissions,
        x='Source',
        y='Emissions',
        title="Total CO2 Emissions by Source"
    )
    st.plotly_chart(fig2, use_container_width=True)

