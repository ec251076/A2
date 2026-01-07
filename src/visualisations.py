# src/visualizations.py

import plotly.express as px

def plot_line(df, x, y, color=None, title="Line Chart"):
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title)
    return fig

def plot_bar(df, x, y, title="Bar Chart"):
    fig = px.bar(df, x=x, y=y, title=title)
    return fig

def plot_pie(df, names, values, title="Pie Chart"):
    fig = px.pie(df, names=names, values=values, title=title)
    return fig
