import pandas as pd
import os
import re
import numpy as np
import sys
from datetime import datetime, timedelta

from tools import convert_vendorName_to_vendorID, load_classifier


def categorize_raw_statement(statement_fn):
    '''This function reads a 'raw statement' and auto-categorizes it'''
    svm_classifier, vectorizer = load_classifier()
    raw_df = pd.read_csv(f"data/RawStatements/{statement_fn}")
    
    # Create a guess auto-category with the ML model
    guessed_dict = {}
    guessed_dict['Transaction_Date'] = []
    guessed_dict['Vendor_Name'] = []
    guessed_dict['Inferred_Vendor_ID'] = []
    guessed_dict['Amount'] = []
    guessed_dict['Auto_Category'] = []
    guessed_dict['Category_Fix_USER_ENTERED'] = []

    for expense_id, row in raw_df.iterrows():
        if row.Amount > 0:
            # Credit card payment or re-fund
            continue

        guessed_dict['Transaction_Date'].append(row.Date)
        guessed_dict['Vendor_Name'].append(row.Name.strip())
        X_test = convert_vendorName_to_vendorID(row.Name.lower().strip())
        guessed_dict['Inferred_Vendor_ID'].append(X_test)
        X_test_vector = vectorizer.transform([X_test])
        guessed_dict['Amount'].append(-row.Amount)
        guessed_dict['Auto_Category'].append(svm_classifier.predict(X_test_vector)[0])
        guessed_dict['Category_Fix_USER_ENTERED'].append("None")
    
    guessed_df = pd.DataFrame.from_dict(guessed_dict)
    return guessed_df

def tell_user_next_statement_start():
    '''This function tells the user the start date of the next statement to download'''
    all_statements_fn = os.listdir("data/RawStatements")
    if ".DS_Store" in all_statements_fn:
        all_statements_fn.remove(".DS_Store")

    end_date_objects = []
    for statement_fn in all_statements_fn:
        match = re.findall(r'(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{4}).csv', statement_fn)
        if match:
            end_date_str = match[0][1]
            
            end_date_objects.append(datetime.strptime(end_date_str, "%m-%d-%Y"))
        else:
            print(f"WARNING: data/RawStatements/{statement_fn} is in the wrong format")

    most_recent_index = np.argmax(end_date_objects)
    next_start_date_object = end_date_objects[most_recent_index] + timedelta(days=1)
    next_start_date_str = next_start_date_object.strftime("%m-%d-%Y")
    return next_start_date_str

def sort_statement_fns_by_date(unsorted_statement_fns):
    start_date_objects = []
    end_date_objects = []
    for statement_fn in unsorted_statement_fns:
        match = re.findall(r'(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{4}).csv', statement_fn)
        if match:
            start_date_str = match[0][0]
            end_date_str = match[0][1]
            
            start_date_objects.append(datetime.strptime(start_date_str, "%m-%d-%Y"))
            end_date_objects.append(datetime.strptime(end_date_str, "%m-%d-%Y"))
        else:
            print(f"WARNING: data/RawStatements/{statement_fn} is in the wrong format")

    sorted_indices = np.argsort(start_date_objects)

    sorted_statement_fns = [unsorted_statement_fns[i] for i in sorted_indices]

    return sorted_statement_fns


def categorize_all_raw_statements():
    '''Function to auto-classify all raw statements and write/modify the corresponding corrected statement'''
    all_raw_statements_fn = os.listdir("data/RawStatements")
    if ".DS_Store" in all_raw_statements_fn:
        all_raw_statements_fn.remove(".DS_Store")

    if len(all_raw_statements_fn) == 0:
        print("--> User must put a credit card statement in data/RawStatements...")
        sys.exit()

    # Sort the statement file names by date
    all_raw_statements_fn = sort_statement_fns_by_date(all_raw_statements_fn)

    # Auto-classify all raw statements

    transaction_id = 1  # will increment for each transaction
    counter = 0
    for raw_statement_fn in all_raw_statements_fn:
        counter += 1
        previously_classified = False
        corrected_statement_fn = re.sub('.csv$','.xlsx',raw_statement_fn)

        # Check if the program has already classified this statement, in which case the user might have made modifications
        if corrected_statement_fn in os.listdir("data/CorrectedStatements"):
            previously_classified = True

        auto_classified_df = categorize_raw_statement(raw_statement_fn)

        # Create the index Transaction_ID column
        auto_classified_df['Transaction_ID'] = range(transaction_id, transaction_id + len(auto_classified_df))
        auto_classified_df.set_index('Transaction_ID', inplace=True)

        # User might have made changes... keep their changes
        if previously_classified:
            existing_corrected_df = pd.read_excel(f"data/CorrectedStatements/{corrected_statement_fn}")
            existing_corrected_df.set_index('Transaction_ID', inplace=True)
            # Want to copy over the info that the user could have enter in the "existing_df" into the new auto_classified_df
            auto_classified_df = auto_classified_df.reindex_like(existing_corrected_df)
            cols_to_copy = list(existing_corrected_df.columns)
            auto_classified_df[cols_to_copy] = existing_corrected_df[cols_to_copy]

        auto_classified_df.to_excel(f"data/CorrectedStatements/{corrected_statement_fn}")
        print(f"--> data/CorrectedStatements/{corrected_statement_fn} has been written/updated ({counter}/{len(all_raw_statements_fn)})")
        transaction_id += len(auto_classified_df)

    return

# Below function is not currently used, but could be used in the future
def identify_recent_raw_statement_to_classify():
    '''Function to use when the user wants to classify a specific statement rather than all RawStatemnts.
    Return: file name of raw statement to classify (str)'''
    all_statements_fn = os.listdir("data/RawStatements")
    if ".DS_Store" in all_statements_fn:
        all_statements_fn.remove(".DS_Store")

    if len(all_statements_fn) == 0:
        print("--> User must put a credit card statement in data/RawStatements...")
        sys.exit()
    
    start_date_objects = []
    end_date_objects = []
    for statement_fn in all_statements_fn:
        match = re.findall(r'_(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{4}).csv', statement_fn)
        if match:
            start_date_str = match[0][0]
            end_date_str = match[0][1]
            
            start_date_objects.append(datetime.strptime(start_date_str, "%m-%d-%Y"))
            end_date_objects.append(datetime.strptime(end_date_str, "%m-%d-%Y"))
        else:
            print(f"WARNING: data/RawStatements/{statement_fn} is in the wrong format")

    most_recent_index = np.argmax(end_date_objects)
    statement_to_classify_fn = all_statements_fn[most_recent_index]

    recent_start_date = start_date_objects[most_recent_index]
    recent_end_date = end_date_objects[most_recent_index]
    recent_start_date_str = recent_start_date.strftime("%m-%d-%Y")
    recent_end_date_str = recent_end_date.strftime("%m-%d-%Y")

    return statement_to_classify_fn
