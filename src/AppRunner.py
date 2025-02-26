# Main script to process credit card statements and run the Streamlit app

import os
import subprocess
import argparse

# Custom python modules / functions
from categorize_raw_statement import categorize_all_raw_statements, tell_user_next_statement_start
from compile_corrected_statements import compile_corrected_statements
from summarize_transactions import summarize_monthly_transactions
from tools import retrain_classifier, init_working_directory

cct_version = '3.5'
src_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Credit Card Tracker')
    args.add_argument('-s', '--streamlit', action='store_true', help="Run  Streamlit app", default=False)
    args = args.parse_args()

    print('\n')
    print(f"**********************************************")
    print(f"********** Credit Card Tracker v{cct_version} **********")
    print(f"**********************************************")
    print('\n')

    # First time user is running the script
    if "cct_init_files" not in os.listdir():
        init_working_directory()

    # Re-train the classifier in-case the user made a change to the VendorID files
    _,_ = retrain_classifier()

    # Re-categorize all of the 'Corrected Statements'
    categorize_all_raw_statements()

    # Compile and summarize all transactions
    compile_corrected_statements()
    summarize_monthly_transactions()

    print('\n')
    print("--------------------------------")
    # Tell user the next Statement start date
    if len(os.listdir('data/RawStatements/'))>0:
        next_statement_date_str = tell_user_next_statement_start()
    else:
        next_statement_date_str = 'any date'
    
    print("--------------------------------")
    print(f"Next RawStatement to download: start date = {next_statement_date_str}")
    print("--------------------------------")

    # Run the streamlit app
    if args.streamlit is True:
        print('\n')
        print("********** Running Streamlit App ************")
        print('\n')
        subprocess.run(f'streamlit run {src_dir}/StreamlitApp.py', shell=True)