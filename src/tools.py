import re
import os
import pandas as pd
import joblib
import subprocess

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

def init_working_directory():
    '''Function to initialize the working directory (first time user is running the script)'''
    print("--> Making directories and downloading required files to cct_init_files/")
    subprocess.run(['mkdir', f'data'])
    subprocess.run(['mkdir', f'data/CorrectedStatements', f'data/RawStatements'])
    subprocess.run(['mkdir', 'model'])
    subprocess.run(['gdown','--folder', 'https://drive.google.com/drive/folders/1RdQUjnQV3rb6-pKMM6pYxup7rGO5w4yt?usp=drive_link'])
    print('--> Installation is complete. The GUI should have opened in another tab..')
    return

def get_list_difference(list1, list2):
    return [item for item in list1 if item not in list2]

def load_unique_categories():
    '''Function to load in the recognized categrories'''
    category_labels = os.listdir("cct_init_files/VendorIDs")
    category_labels = [filename.replace(".txt","") for filename in category_labels]
    category_labels.remove(".DS_Store")
    return category_labels

def load_vendorIDs_and_labels():
    '''Function to load in a list of vendorIDs and their labels (data set for model training)'''
    category_labels = load_unique_categories()
    all_vendorIDs = []
    all_labels = []
    for category in category_labels:
        with open(f"cct_init_files/VendorIDs/{category}.txt", "r") as f:
            vendorIDs = f.readlines()
            vendorIDs = [vendor.strip() for vendor in vendorIDs]
        # Append this information to a list
        for vendorID in vendorIDs:
            all_vendorIDs.append(vendorID)
            all_labels.append(category)
    return all_vendorIDs, all_labels

def load_categories_from_all_transactions():
    '''Gets list of categories in all_transactions.csv. These are the categories that were present LAST TIME the use ran the App'''
    all_transactions_df = pd.read_csv("data/all_transactions.csv")
    return list( all_transactions_df.Category.unique() )

def convert_vendorName_to_vendorID(vendor_id):
    '''Function to convert the vendorID in the "raw statement into a vendor name'''
    # remove state abbreviation and city before
    pattern = r'\S+\s+[a-z]{2}$|\b[a-z]{2}$'
    vendor_id = re.sub(pattern, '', vendor_id.lower().strip()).strip()

    # remove the store number
    pattern = r'(^\w+|\b)\d{2,}(^\w+|\b)'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # remove phone number
    pattern = r'\+?\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,4}(?:[\s-]?\d{1,4})?'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # remove llc
    pattern = r'[\s\W]*\b[llc,inc]\b[\s\W]*$'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # replace non-word characters with a space
    pattern = r'[^\w\s]'
    vendor_id = re.sub(pattern, ' ', vendor_id).strip()

    # remove single letters
    pattern = r'\b\w{1}\b'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # remove un-important words (could use nltk)
    pattern = r'\bthe\b|\band\b'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # remove multiple spaces
    pattern = r'\s{2,}'
    vendor_id = re.sub(pattern, ' ', vendor_id).strip()

    # remove website info
    pattern = r'www\.?|\.?com\b|\bweb\b|\bhttps?://\S+'
    vendor_id = re.sub(pattern, '', vendor_id).strip()

    # Remove the word membership
    vendor_id = re.sub(r'\bmembership\b', '', vendor_id).strip()

    return vendor_id

def save_classifier(classifier, vectorizer):
    joblib.dump(classifier, 'model/classifier.pkl')
    joblib.dump(vectorizer, 'model/vectorizer.pkl')
    print("--> model/classifier.pkl and model/vectorizer.pkl have been written.")
    return

def load_classifier():
    if not os.path.exists('model/classifier.pkl'):
        print("--> model/classifier.pkl and model/vectorizer.pkl do not exist. Training classifier...")
        classifier, vectorizer = retrain_classifier()
    else:
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