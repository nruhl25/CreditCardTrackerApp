import pandas as pd
import os
import re
import numpy as np
from datetime import datetime, timedelta
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from tools import load_vendorIDs_and_labels, convert_vendorName_to_vendorID

def save_classifier(classifier, vectorizer):
    joblib.dump(classifier, 'model/classifier.pkl')
    joblib.dump(vectorizer, 'model/vectorizer.pkl')
    print("--> model/classifier.pkl and model/vectorizer.pkl have been written.")
    return

def load_classifier():
    if not os.path.exists('model/classifier.pkl'):
        print("--> model/classifier.pkl and model/vectorizer.pkl do not exist. Retraining classifier...")
        return retrain_classifier()
    classifier = joblib.load('model/classifier.pkl')
    vectorizer = joblib.load('model/vectorizer.pkl')
    return classifier, vectorizer

def retrain_classifier():
    '''Re-train classifier every time the user opens up the GUI'''
    X_train, y_train = load_vendorIDs_and_labels()
    vectorizer = CountVectorizer(binary=True)
    X_train_vectors = vectorizer.fit_transform(X_train)
    svm_classifier = svm.SVC(kernel='linear')
    svm_classifier.fit(X_train_vectors, y_train)
    save_classifier(svm_classifier, vectorizer)
    return svm_classifier, vectorizer


def categorize_raw_statement(statement_fn):
    '''This function reads a 'raw statement' and auto-categorizes it'''
    svm_classifier, vectorizer = load_classifier()
    raw_df = pd.read_csv(f"data/RawStatements/{statement_fn}")
    
    # Create a guess auto-category with the ML model
    guessed_dict = {}
    guessed_dict['Transaction_ID'] = []
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

        guessed_dict['Transaction_ID'].append(expense_id)
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
    all_statements_fn.remove(".DS_Store")

    end_date_objects = []
    for statement_fn in all_statements_fn:
        match = re.findall(r'_(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{4}).csv', statement_fn)
        if match:
            end_date_str = match[0][1]
            
            end_date_objects.append(datetime.strptime(end_date_str, "%m-%d-%Y"))
        else:
            print(f"WARNING: data/RawStatements/{statement_fn} is in the wrong format")

    most_recent_index = np.argmax(end_date_objects)
    next_start_date_object = end_date_objects[most_recent_index] + timedelta(days=1)
    next_start_date_str = next_start_date_object.strftime("%m-%d-%Y")
    return next_start_date_str

def categorize_last_raw_statement():
    all_statements_fn = os.listdir("data/RawStatements")
    all_statements_fn.remove(".DS_Store")
    if len(all_statements_fn) == 0:
        print("--> User must put a credit card statement in data/RawStatements...")
        return

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
    print(f"--> Program is auto-classifying {statement_to_classify_fn}.")

    recent_start_date = start_date_objects[most_recent_index]
    recent_end_date = end_date_objects[most_recent_index]
    recent_start_date_str = recent_start_date.strftime("%m-%d-%Y")
    recent_end_date_str = recent_end_date.strftime("%m-%d-%Y")

    # Auto-classify the most recent statement
    auto_classified_df = categorize_raw_statement(statement_to_classify_fn)
    auto_classified_df.to_excel(f"data/CorrectedStatements/TO_BE_CORRECTED_{recent_start_date_str}_{recent_end_date_str}.xlsx", index=False)
    print(f"-->data/CorrectedStatements/TO_BE_CORRECTED_{recent_start_date_str}_{recent_end_date_str}.xlsx has been written and is ready to be edited.")
    return


if __name__ == '__main__':
    categorize_last_raw_statement()
