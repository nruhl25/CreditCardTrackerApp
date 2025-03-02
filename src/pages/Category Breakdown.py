import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.write("# Category Breakdown :money_with_wings:")

df = pd.read_csv('data/monthly_summary.csv')
df.set_index('Year-Month', inplace=True)
df.index = pd.to_datetime(df.index, yearfirst=True)
categories = list(df.columns.drop(['Year','Month']))

df['Total_Spent'] = df[categories].sum(axis=1)
categories.append("Total_Spent")

##### BARPLOT #####

st.write("### Bar chart of monthly expenses")

default_colors = px.colors.qualitative.Plotly

categories_chosen = st.multiselect(f"Select categories to plot", categories, default=["Total_Spent"])

bar_plot = go.Figure()
for i, category in enumerate(categories_chosen):
    avg_spent = df[category].mean()
    bar_plot.add_trace(go.Bar(x=df.index, y=df[category], name=category, marker_color=default_colors[i]) )
    bar_plot.add_trace(go.Scatter(x=df.index, y=[avg_spent]*len(df.index), mode='lines', name=f"Avg = ${avg_spent:.0f}", line_color=default_colors[i]) )

bar_plot.update_layout(xaxis_title="Year-Month", yaxis_title="$ Spent", showlegend=True)

st.plotly_chart(bar_plot)

##### PIE PLOTS #####
st.write("### Pie charts of monthly expenses")
col1, col2 = st.columns(2)
pie_categories = categories.copy()
pie_categories.remove('Total_Spent')

with col1:
    st.write("### Monthly expenses (single month)")

    month_year_to_plot = st.selectbox(label='Select the Year-Month to plot', options=list(df.index.strftime("%Y-%m")), index=len(df.index)-1)

    pie_df = df[pie_categories].loc[pd.to_datetime(month_year_to_plot)]

    plotly_pie = px.pie(pie_df, names=pie_categories, values=pd.to_datetime(month_year_to_plot))
    st.plotly_chart(plotly_pie)

with col2:
    st.write("### Monthly expenses (year average)")
    year_to_plot = st.selectbox(label='Select the Year to plot', options=list(df['Year'].unique()), index=len(df['Year'].unique())-1)

    pie_year_df = df[df['Year'] == year_to_plot]
    avg_pie_series = pie_year_df[pie_categories].mean(axis=0)

    plotly_pie_year = px.pie(avg_pie_series, values=avg_pie_series.values, names=avg_pie_series.index)
    st.plotly_chart(plotly_pie_year)

st.write("### All year-averaged pie charts")

show_all_years = st.checkbox("Show all year-averaged pie charts", value=False)

if show_all_years:
    n_years = len(df['Year'].unique())
    n_cols = 2
    n_rows = int(np.ceil(n_years/n_cols))
    specs = [[{"type": "domain"} for _ in range(n_cols)] for _ in range(n_rows)]

    subplot_titles = [f"{year}" for year in df['Year'].unique()]
    if len(subplot_titles) % n_cols != 0:
        subplot_titles.append("")

    pie_subfig = make_subplots(rows=n_rows, cols=n_cols, specs=specs,
                            subplot_titles=subplot_titles)
    for i, year in enumerate(df['Year'].unique()):
        pie_year_df = df[df['Year'] == year]
        avg_pie_series = pie_year_df[pie_categories].mean(axis=0)
        pie_subfig.add_trace(go.Pie(labels=avg_pie_series.index, values=avg_pie_series.values), row=i//n_cols+1, col=i%n_cols+1)

    # Set layout to make subplots fit well
    pie_subfig.update_layout(
        height=900,  # Adjust height
        width=1000,  # Adjust width
        margin=dict(l=10, r=10, t=50, b=10),  # Reduce margins
    )

    st.plotly_chart(pie_subfig, use_container_width=True)