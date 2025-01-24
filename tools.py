import re
import os

def load_unique_categories():
    '''Function to load in the recognized categrories'''
    category_labels = os.listdir("cct_init_files/VendorIDs")
    category_labels = [filename.replace(".txt","") for filename in category_labels]
    category_labels.remove(".DS_Store")
    return category_labels

def load_vendorIDs_and_labels():
    '''Function to load in a list of vendorIDs and their labels'''
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