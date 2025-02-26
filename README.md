# Credit Card Tracker App

The Credit Card Tracker App is a comprehensive tool designed to help users manage and track their credit card expenses efficiently. This application provides features such as expense categorization, spending analysis, and budget management to ensure users have a clear understanding of their financial activities.

## Features

- **Expense Categorization**: Automatically categorize your expenses for better tracking.
- **Spending Analysis**: Generate detailed reports and charts to analyze your spending habits.
- **Budget Management**: Set and monitor budgets to control your spending.

## How to Use

1. **Download and Install**: Download the newest verwsion of executable binary `AppRunner` from the `exec/` folder of this GitHub repository and place it into a folder on your computer that is dedicated to the Credit Card Traker App (eg. `CreditCardTracker/`)
2. **Launch the Application**: Run the `AppRunner` executable to start the application (double click or from the command line)
3. **Track Expenses**: Download your credit card transactions for any range of dates, and place them in the folder `data/RawStatements/`.
    - For ease of use, the app is programmed to read and categorize all raw statements every time it is run. As time goes on, it may take longer to run, but logic could be added to only process a single statement.
    - An example of the "raw statement" file format is given in `data/RawStatements/Credit Card - 08-01-2023_12-31-2023.csv`.
4. **Analyze Spending**: Let the Bag-Of-Words model automatically categorize your credit card statements. You can view and make corrections to the auto-categories in the folder `model/CorrectedStatements/`.

5. **Manage Budgets**: Use the Streamlit dashboard to quickly visualize your data and/or perform your own post-processing of your spending data in `data/all_transactions.csv` and `data/monthly_summary.csv`. Note that these files will be written over and added to the next time you run the app, so be careful to do your post-processing in a file named something slighlty different.

6. **Customize Functionality**: If you want the auto-categorizer to clue-in on specific stores or key phrases when categorizing your expenses, you can modify the text files in `cct_init_files/VendorIDs/`
