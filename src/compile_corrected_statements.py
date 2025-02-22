import os
import pandas as pd
import sys

from tools import load_unique_categories, load_classifier

def compile_corrected_statements():
    '''This function compiles all .xlsx files in CorrectedStatements/, applies the user-entered corrections, and write a file data/all_transactions.csv'''
    corrected_df_list = []
    corrected_statements = os.listdir("data/CorrectedStatements")
    if ".DS_Store" in corrected_statements:
        corrected_statements.remove(".DS_Store")

    if len(corrected_statements) == 0:
        print("data/CorrectedStatements is empty. You must download and categorize a credit card statement...")
        return

    for statement_fn in corrected_statements:
        if "TO_BE_CORRECTED" in statement_fn:
            print(f"--> WARNING: User may not have corrected data/CorrectedStatements/{statement_fn}. Proceeding using the auto-categories...")
        corrected_df = pd.read_excel(f"data/CorrectedStatements/{statement_fn}")
        corrected_df_list.append(corrected_df)

    all_corrected_dfs = pd.concat(corrected_df_list)

    category_with_fix_list = []
    all_corrected_dfs.Category_Fix_USER_ENTERED = all_corrected_dfs.Category_Fix_USER_ENTERED.astype(str)
    for transaction_id, row in all_corrected_dfs.iterrows():
        if row.Category_Fix_USER_ENTERED == "nan":
            category_with_fix_list.append(row.Auto_Category)
        else:
            category_with_fix_list.append(row.Category_Fix_USER_ENTERED)
            recognized_categories = load_unique_categories()
            if row.Category_Fix_USER_ENTERED not in recognized_categories:
                print(f"WARNING: User-entered category is not a recognized VendorID. Please initialize this category by creating the file: cct_init_files/VendorIDs/{row.Category_Fix_USER_ENTERED}.txt")
                print("--> Exiting the program...")
                sys.exit()
    
    all_corrected_dfs = all_corrected_dfs[["Transaction_Date", "Vendor_Name", "Amount"]]
    all_corrected_dfs["Category"] = category_with_fix_list

    all_corrected_dfs.to_csv("data/all_transactions.csv")
    return

# Not currently used, but keeping for reference
def reclassify_corrected_statement(statement_fn):
    ''' User has modified their classifier, and all "Corrected Statements need to be re-classified. This function modifies the "Auto-Category" '''
    new_auto_categories = []
    corrected_statement_df = pd.read_excel(f"data/CorrectedStatements/{statement_fn}")
    svm_classifier, vectorizer = load_classifier()
    for index, row in corrected_statement_df.iterrows():
        X_test = row.Inferred_Vendor_ID
        X_test_vector = vectorizer.transform([X_test])
        new_auto_categories.append(svm_classifier.predict(X_test_vector)[0])
    corrected_statement_df["Auto_Category"] = new_auto_categories
    corrected_statement_df.to_excel(f"data/CorrectedStatements/{statement_fn}")
    print(f"--> data/CorrectedStatements/{statement_fn} has been re-classified")
    return