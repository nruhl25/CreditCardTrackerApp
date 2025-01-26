# Credit Card Tracker App

The Credit Card Tracker App is a comprehensive tool designed to help users manage and track their credit card expenses efficiently. This application provides features such as expense categorization, spending analysis, and budget management to ensure users have a clear understanding of their financial activities.

## Features

- **Expense Categorization**: Automatically categorize your expenses for better tracking.
- **Spending Analysis**: Generate detailed reports and charts to analyze your spending habits.
- **Budget Management**: Set and monitor budgets to control your spending.
- **Alerts and Notifications**: Receive alerts for due payments and budget limits.

## How to Use

1. **Download and Install**: Download the newest verwsion of executable binary `AppRunner` from the `executables/` folder of this GitHub repository and place it into a folder on your computer that is dedicated to the Credit Card Traker App (eg. `CreditCardTracker/`)
2. **Launch the Application**: Run the `AppRunner` executable to start the application.
3. **Track Expenses**: Download your credit card transactions for any range of dates, and place them in the folder `model/RawStatements/`. These files should have a file name of the following format: Credit_Card_08-01-2023_12-31-2023.csv.
    - For ease of use, the app is programmed to read the _most recently_ dated credit card statement in the folder. Only add one file at a time before you have the app categorize the raw statement.
    - An example of the "raw statement file format is given in `data/RawStatements/Credit Card - 08-01-2023_12-31-2023.csv`.
4. **Analyze Spending**: Let the Bag-Of-Words model automatically categorize your credit card statements. You can view and make corrections to the auto-categories in the folder `model/CorrectedStatements/`. Feel free to remove "TO_BE_CORRECTED" from the file names once they have been corrected.
    - An exemple of the "to-be corrected" excel file format is given in `data/CorrectedStatements/TO_BE_CORRECTED_08-01-2023_12-31-2023.csv`
5. **Manage Budgets**: Perform your own post-processing of your spending data in `data/all_transactions.csv` and `data/monthly_summary.csv`. Note that these files will be written over and added to the next time you run the app, so be careful to do your post-processing in a file named something slighlty different.
    - It was decided to re-process everything and re-write the file every time, but this could be changed in future versions.
6. **Customize Functionality**: If you want the auto-categorizer to clue-in on stores or key phrases when categorizing your expenses, you can modify the text files in `cct_init_files/VendorIDs/`

#### In the future, I may consider making a Data App that uses the `Streamlit` library. You can make the Streamlit App an executable with a Python library called `Nativifier`, or you can deploy the app via a GitHub repository.
