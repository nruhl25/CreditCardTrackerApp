import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def streamlit_app():
    '''Main function for the Streamlit App'''

    st.title('Data Visualization Tool for the CreditCardTrackerApp')

    st.image("cct_init_files/piggybank.png")

    df = pd.read_csv('data/monthly_summary.csv')
    df.set_index('Year-Month', inplace=True)
    df.index = pd.to_datetime(df.index, yearfirst=True)
    categories = list(df.columns.drop(['Year','Month']))

    df['Total_Spent'] = df[categories].sum(axis=1)
    categories.append('Total_Spent')
    st.dataframe(df[categories])

    category_to_plot = st.selectbox('Select Category to Plot', categories, index=categories.index("Total_Spent"))

    fig, ax = plt.subplots(figsize=(8,6))

    ax.plot(df.index, df[category_to_plot], label=category_to_plot)
    ax.set_ylabel("$ Spent")
    ax.set_xlabel('Year-Month')
    ax.legend()
    fig.tight_layout()

    st.pyplot(fig)
    return

if __name__ == '__main__':
    streamlit_app()