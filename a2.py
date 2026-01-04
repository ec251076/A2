# app.py
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
# Data loading
# -----------------------------
@st.cache_data
def load_data():
    energy_consumption = pd.read_csv("data/energy_consumption.csv")
    energy_generation = pd.read_csv("data/energy_generation.csv")
    return energy_consumption, energy_generation

consumption_df, generation_df = load_data()


# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("Controls")


min_year = int(consumption_df['year'].min())
max_year = int(consumption_df['year'].max())


year_range = st.sidebar.slider(
"Select year range",
min_year,
max_year,
(min_year, max_year)
)


# Filter data based on user input
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
generation_filtered[generation_filtered['source_type'] == 'Renewable']['generation_mwh'].sum()
/ generation_filtered['generation_mwh'].sum()
) * 100


col1, col2 = st.columns(2)
col1.metric("Total Consumption (MWh)", f"{total_consumption:,.0f}")
col2.metric("Renewable Share (%)", f"{renewable_share:.1f}")


fig = px.line(
consumption_filtered,
x="year",
y="consumption_mwh",
title="Electricity Consumption Over Time"
)
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
title="Yearly Electricity Consumption"
)
st.plotly_chart(fig, use_container_width=True)


st.write("Descriptive statistics")
st.dataframe(consumption_filtered[['consumption_mwh']].describe())


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
barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# Tab 4: Scenario Explorer
# -----------------------------
with tab4:
st.header("Renewable Energy Scenario Explorer")


increase = st.slider(
"Increase renewable generation by (%)",
0,
50,
20
)


scenario_df = generation_filtered.copy()
renewable_mask = scenario_df['source_type'] == 'Renewable'


scenario_df.loc[renewable_mask, 'generation_mwh'] *= (1 + increase / 100)


fig = px.bar(
scenario_df,
x="year",
y="generation_mwh",
color="source_type",
title="Simulated Energy Mix (Illustrative Scenario)",
barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)


st.caption("Scenarios are illustrative and not predictive")


# -----------------------------
# Tab 5: Conclusions
# -----------------------------
with tab5:
st.header("Key Findings and Recommendations")


st.markdown(
"""
**Key findings:**
- Electricity consumption shows identifiable long-term trends.
- Renewable energy represents a growing but still limited share of total generation.


**Recommendations:**
- Continued investment in renewable capacity.
- Use data-driven scenario analysis to support policy decisions.
"""
)
