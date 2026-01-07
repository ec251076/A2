# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Isle of Man Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).parent
CONSUMPTION_FILE = BASE_DIR / "consumption.csv"
GENERATION_FILE = BASE_DIR / "generation.csv"

# -----------------------------
# Data loading function
# -----------------------------
@st.cache_data
def load_data():
    consumption_df = pd.read_csv(CONSUMPTION_FILE)
    generation_df = pd.read_csv(GENERATION_FILE)
    # Clean column names immediately
    consumption_df.columns = consumption_df.columns.str.strip().str.lower()
    generation_df.columns = generation_df.columns.str.strip().str.lower()
    # Ensure 'year' exists
    if "year" not in consumption_df.columns:
        if "date" in consumption_df.columns:
            consumption_df["date"] = pd.to_datetime(consumption_df["date"])
            consumption_df["year"] = consumption_df["date"].dt.year
        elif "period" in consumption_df.columns:
            consumption_df["year"] = consumption_df["period"].astype(int)
        else:
            st.error("No 'year' or 'date' column found in consumption data")
            st.stop()
    if "year" not in generation_df.columns:
        if "date" in generation_df.columns:
            generation_df["date"] = pd.to_datetime(generation_df["date"])
            generation_df["year"] = generation_df["date"].dt.year
    return consumption_df, generation_df

# -----------------------------
# Load data
# -----------------------------
consumption_df, generation_df = load_data()

st.write("Columns:", consumption_df.columns.tolist())
st.write(consumption_df.head(3))

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("Controls")
min_year = int(consumption_df["year"].min())
max_year = int(consumption_df["year"].max())

year_range = st.sidebar.slider(
    "Select year range",
    min_year,
    max_year,
    (min_year, max_year)
)

# Filter data
consumption_filtered = consumption_df[
    (consumption_df['year'] >= year_range[0]) &
    (consumption_df['year'] <= year_range[1])
]
generation_filtered = generation_df[
    (generation_df['year'] >= year_range[0]) &
    (generation_df['year'] <= year_range[1])
]

# -----------------------------
# Tabs layout
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Consumption Trends",
    "Energy Mix",
    "Scenario Explorer",
    "Conclusions"
])

# -----------------------------
# Tab 1: Overview
# -----------------------------
with tab1:
    st.header("Energy Overview")
    
    total_consumption = consumption_filtered['consumption_mwh'].sum()
    renewable_share = (
        generation_filtered[generation_filtered['source_type'].str.lower() == 'renewable']['generation_mwh'].sum()
        / generation_filtered['generation_mwh'].sum()
    ) * 100 if generation_filtered['generation_mwh'].sum() > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Consumption (MWh)", f"{total_consumption:,.0f}")
    col2.metric("Renewable Share (%)", f"{renewable_share:.1f}")

    fig = px.line(
        consumption_filtered,
        x="year",
        y="consumption_mwh",
        title="Electricity Consumption Over Time",
        markers=True,
        labels={"year": "Year", "consumption_mwh": "Consumption (MWh)"},
        hover_data={"year": True, "consumption_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 2: Consumption Trends
# -----------------------------
with tab2:
    st.header("Electricity Consumption Trends")
    fig = px.line(
        consumption_filtered,
        x="year",
        y="consumption_mwh",
        markers=True,
        title="Yearly Electricity Consumption",
        labels={"year": "Year", "consumption_mwh": "Consumption (MWh)"},
        hover_data={"year": True, "consumption_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.write("Descriptive statistics")
    st.dataframe(consumption_filtered[['consumption_mwh']].describe().style.format("{:,.0f}"))

# -----------------------------
# Tab 3: Energy Mix
# -----------------------------
with tab3:
    st.header("Energy Generation Mix")
    fig = px.bar(
        generation_filtered,
        x="year",
        y="generation_mwh",
        color="source_type",
        title="Renewable vs Non-Renewable Energy Generation",
        barmode="stack",
        labels={"year": "Year", "generation_mwh": "Generation (MWh)", "source_type": "Energy Source"},
        hover_data={"generation_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white", legend_title_text='Energy Source')
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tab 4: Scenario Explorer
# -----------------------------
with tab4:
    st.header("Renewable Energy Scenario Explorer")
    increase = st.slider(
        "Increase renewable generation by (%)",
        0, 50, 20
    )
    scenario_df = generation_filtered.copy()
    renewable_mask = scenario_df['source_type'].str.lower() == 'renewable'
    scenario_df.loc[renewable_mask, 'generation_mwh'] *= (1 + increase / 100)
    fig = px.bar(
        scenario_df,
        x="year",
        y="generation_mwh",
        color="source_type",
        title="Simulated Energy Mix (Illustrative Scenario)",
        barmode="stack",
        labels={"year": "Year", "generation_mwh": "Generation (MWh)", "source_type": "Energy Source"},
        hover_data={"generation_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white", legend_title_text='Energy Source')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Scenarios are illustrative and not predictive")

# -----------------------------
# Tab 5: Conclusions
# -----------------------------
with tab5:
    st.header("Key Findings and Recommendations")
    st.markdown("""
    **Key findings:**
    - Electricity consumption shows identifiable long-term trends.
    - Renewable energy represents a growing but still limited share of total generation.

    **Recommendations:**
    - Continued investment in renewable capacity.
    - Use data-driven scenario analysis to support policy decisions.
    """)

