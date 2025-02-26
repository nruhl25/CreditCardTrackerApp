import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.write("## Category Breakdown")

df = pd.read_csv('data/monthly_summary.csv')
df.set_index('Year-Month', inplace=True)
df.index = pd.to_datetime(df.index, yearfirst=True)
categories = list(df.columns.drop(['Year','Month']))

df['Total_Spent'] = df[categories].sum(axis=1)
categories.append("Total_Spent")

##### BARPLOT #####

# TODO: could add another plot showing $ spent at rESTAURANTS AND gROCERIES AND cAFES?

category_to_plot = st.selectbox("Select Category to Plot", categories, index=categories.index("Total_Spent"))

fig, ax = plt.subplots(figsize=(8,6))

ax.bar(df.index, df[category_to_plot], label=category_to_plot, width=30)
ax.set_ylabel("$ Spent")
ax.set_xlabel('Year-Month')
ax.legend()
fig.tight_layout()

st.pyplot(fig)

##### PIE PLOT #####

# TODO: could add radio buttons to select which pie_catogries should be used?


month_to_plot = st.selectbox(label='Select Year-Month to Plot', options=list(df.index.strftime("%Y-%m")), index=len(df.index)-1)

pie_categories = categories.copy()

pie_fig, pie_ax = plt.subplots(figsize=(8,6))
pie_categories.remove('Total_Spent')
pie_ax.pie(df.loc[pd.to_datetime(month_to_plot)][pie_categories], 
    autopct='%1.1f%%',
    pctdistance=0.85,
    labeldistance=1.1,
    shadow=False)
pie_ax.legend(pie_categories, loc='upper right', bbox_to_anchor=(1.3, 0.8))
pie_fig.tight_layout()
st.pyplot(pie_fig)

st.write("### data/monthly_summary.csv")

st.dataframe(df[categories])