# a2.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Isle of Man Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# Data loading function with upload
# -----------------------------
@st.cache_data
def load_data(consumption_file, generation_file):
    consumption_df = pd.read_csv(consumption_file)
    generation_df = pd.read_csv(generation_file)

    # Clean column names
    consumption_df.columns = consumption_df.columns.str.strip().str.lower()
    generation_df.columns = generation_df.columns.str.strip().str.lower()

    # Ensure 'year' column exists
    if "year" not in consumption_df.columns:
        if "date" in consumption_df.columns:
            consumption_df["date"] = pd.to_datetime(consumption_df["date"])
            consumption_df["year"] = consumption_df["date"].dt.year
        elif "period" in consumption_df.columns:
            consumption_df["year"] = consumption_df["period"].astype(int)
        else:
            st.error("No 'year' or 'date' column found in consumption data")
            st.stop()

    if "year" not in generation_df.columns and "date" in generation_df.columns:
        generation_df["date"] = pd.to_datetime(generation_df["date"])
        generation_df["year"] = generation_df["date"].dt.year

    return consumption_df, generation_df

# -----------------------------
# File upload section
# -----------------------------
st.sidebar.title("Upload CSV Files")

consumption_file = st.sidebar.file_uploader(
    "Upload consumption CSV",
    type=["csv"]
)

generation_file = st.sidebar.file_uploader(
    "Upload generation CSV",
    type=["csv"]
)

if consumption_file and generation_file:
    # Load data after upload
    consumption_df, generation_df = load_data(consumption_file, generation_file)
else:
    st.warning("Please upload both consumption and generation CSV files to continue.")
    st.stop()

# -----------------------------
# Sidebar controls
# -----------------------------
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
    (consumption_df["year"] >= year_range[0]) &
    (consumption_df["year"] <= year_range[1])
]
generation_filtered = generation_df[
    (generation_df["year"] >= year_range[0]) &
    (generation_df["year"] <= year_range[1])
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
    total_generation = generation_filtered['generation_mwh'].sum()
    renewable_generation = generation_filtered[
        generation_filtered['source_type'].str.lower() == 'renewable'
    ]['generation_mwh'].sum()

    renewable_share = (renewable_generation / total_generation * 100) if total_generation > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Consumption (MWh)", f"{total_consumption:,.0f}")
    col2.metric("Renewable Share (%)", f"{renewable_share:.1f}")

    fig = px.line(
        consumption_filtered,
        x="year",
        y="consumption_mwh",
        markers=True,
        title="Electricity Consumption Over Time",
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
        barmode="stack",
        title="Renewable vs Non-Renewable Energy Generation",
        labels={"year": "Year", "generation_mwh": "Generation (MWh)", "source_type": "Energy Source"},
        hover_data={"generation_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white", legend_title_text="Energy Source")
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
        barmode="stack",
        title="Simulated Energy Mix (Illustrative Scenario)",
        labels={"year": "Year", "generation_mwh": "Generation (MWh)", "source_type": "Energy Source"},
        hover_data={"generation_mwh": ":,.0f"}
    )
    fig.update_layout(template="plotly_white", legend_title_text="Energy Source")
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
