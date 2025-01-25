# Functions in this script create "monthly summary table" from all_transactions.csv

import pandas as pd

from tools import load_unique_categories

def calculate_category_totals(transactions_df: pd.DataFrame):
    '''tranactions_df is a subset of the total transactions data frame'''
    # Initialize total_expense_dict, key=categories, values=total expense
    categories = load_unique_categories()
    total_expenses_dict = {}
    for category in categories:
        total_expenses_dict[category] = 0.0

    # Alternative method:
    # my_transactions_df = transactions_df[(transactions_df['Transaction_Date'].dt.month == month) & (transactions_df['Transaction_Date'].dt.year == year)]

    for i, row in transactions_df.iterrows():
        total_expenses_dict[row.Category] += row.Amount

    return total_expenses_dict

def summarize_monthly_transactions():
    '''Main function for reading and summarizing all_transactions.csv'''
    transactions_df = pd.read_csv("data/all_transactions.csv")
    transactions_df['Transaction_Date'] = pd.to_datetime(transactions_df['Transaction_Date'], format='%Y-%m-%d')

    # Create an empty list to store the monthly summaries
    monthly_summary_dicts = []

    # Loop through each unique month and year in the DataFrame
    for (year, month), grouped_df in transactions_df.groupby([transactions_df['Transaction_Date'].dt.year, transactions_df['Transaction_Date'].dt.month]):
        monthly_expenses_dict = calculate_category_totals(grouped_df)

        month_summary = {'Year': year, 'Month': month, **monthly_expenses_dict}
        
        # Append the summary for this month
        monthly_summary_dicts.append(month_summary)

    # Convert the list of monthly summaries into a new DataFrame
    monthly_df = pd.DataFrame(monthly_summary_dicts)

    # Display the result
    monthly_df.to_csv("data/monthly_summary.csv", index=False)
    print("--> data/monthly_summary.csv has been written.")
    return


if __name__ == "__main__":
    summarize_monthly_transactions()
