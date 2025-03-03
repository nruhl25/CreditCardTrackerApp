import streamlit as st
import pandas as pd
import os

# Custom python modules / functions
from categorize_raw_statement import categorize_all_raw_statements, tell_user_next_statement_start
from compile_corrected_statements import compile_corrected_statements
from summarize_transactions import summarize_monthly_transactions
from tools import retrain_classifier, init_working_directory

st.set_page_config(page_title="CreditCardTrackerApp", page_icon=":credit_card:", layout="wide")

cct_version = '3.7'

#### HELPER FUNCTIONS BELOW ####

def run_autocategorization():
    global next_statement_date_str
    # Re-train the classifier in case the user made a change to the VendorID files
    my_bar = st.progress(1./3., "Re-training classifier...")
    _,_ = retrain_classifier()
    my_bar.progress(2./3., "Auto-categorizing RawStatements...")
    categorize_all_raw_statements()

    if len(os.listdir('data/RawStatements/'))>0:
        next_statement_date_str = tell_user_next_statement_start()
    else:
        next_statement_date_str = 'any date'

    my_bar.progress(3./3., "Finished auto-categorizing RawStatements! You can now correct the statements in the CorrectedStatements folder")
    return

def run_compile_and_summarize():
    # Compile and summarize all transactions
    my_bar = st.progress(1./3., "Compiling corrected statements...")
    compile_corrected_statements()
    my_bar.progress(2./3., "Summarizing transactions...")
    summarize_monthly_transactions()
    my_bar.progress(3./3., "Finished summarizing CorrectedStatements! You can now view the data visualization tabs")
    st.balloons()
    return

#### PAGE LAYOUT AND FUNCTIONALITY BELOW ####

st.title(f'Credit Card Travker v{cct_version} :credit_card:')

# Tell user the next statement to download
if len(os.listdir('data/RawStatements/'))>0:
    next_statement_date_str = tell_user_next_statement_start()
else:
    next_statement_date_str = 'any date'

# First time user is running the script
if "cct_init_files" not in os.listdir():
    init_working_directory()

if len(os.listdir('data/RawStatements/'))>0:
    next_statement_date_str = tell_user_next_statement_start()
else:
    next_statement_date_str = 'any date'

st.write(f"#### Next RawStatement to download: start date = {next_statement_date_str}")

st.button("Auto-categorize RawStatements", on_click=run_autocategorization)

st.button("Compile and summarize CorrectedStatements", on_click=run_compile_and_summarize)

st.image("cct_init_files/piggybank.png")