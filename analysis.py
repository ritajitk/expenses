#!/usr/bin/env python

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import csv
from datetime import datetime

# Custom date parser
date_parser = lambda x: pd.to_datetime(x, format='%d/%m/%Y')

# Load data and parse dates
def load_data(file):
    df = pd.read_csv(file, parse_dates=['Date'], date_parser=date_parser)
    return df

# Filter by date range
def filter_by_date_range(df, start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]

# Filter by month
def filter_by_month(df, year, month):
    return df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]

# Generate report
def generate_report(df, start_date=None, end_date=None, year=None, month=None):
    if start_date and end_date:
        df_filtered = filter_by_date_range(df, start_date, end_date)
        report_range = f"Report for {start_date} to {end_date}"
    elif year and month:
        df_filtered = filter_by_month(df, year, month)
        report_range = f"Report for {year}-{month:02d}"
    else:
        df_filtered = df
        report_range = "Full Report"

    total_inc = df_filtered[df_filtered['Type'] == 'Income']['Amount'].sum()
    total_exp = df_filtered[df_filtered['Type'] == 'Expense']['Amount'].sum()
    balance = total_inc - total_exp

    # Calculate specific expenses
    exp_credit_card = df_filtered[(df_filtered['Account'] == 'Credit Card') & (df_filtered['Type'] == 'Expense')]['Amount'].sum()
    exp_savings = df_filtered[(df_filtered['Account'] == 'Savings') & (df_filtered['Type'] == 'Expense')]['Amount'].sum()

    print(report_range)
    print(f"Total Income: {total_inc}")
    print(f"Total Expense: {total_exp}")
    print(f"Balance: {balance}")
    print(f"Expense from Credit Card: {exp_credit_card}")
    print(f"Expense from Savings account: {exp_savings}")

    nrows,ncols = df_filtered.shape
    obj2 = df_filtered['Date'].dt.strftime('%Y-%m-%d')

    for i in range(nrows):
        # Convert 'Date' column to string format for display
        df_filtered.loc[i, 'Date'] = obj2[i]

    # Create an interactive table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_filtered.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_filtered[col] for col in df_filtered.columns],
                   fill_color='lavender',
                   align='left'))
    ])

    # Sum expenses by category
    expense_data = df_filtered[df_filtered['Type'] == 'Expense'].groupby(['Category'])['Amount'].sum().reset_index()

    # Create interactive pie chart
    expense_fig = px.pie(expense_data, names='Category', values='Amount', title='Expenses by Category')

    # Save report to HTML
    with open('report.html', 'w') as f:
        # Add the report range as a header
        f.write(f"<h1>{report_range}</h1>")
        f.write(f"<p>Total Income: {total_inc}</p>")
        f.write(f"<p>Total Expense: {total_exp}</p>")
        f.write(f"<p>Balance: {balance}</p>")
        f.write(f"<p>Expense from Credit Card: {exp_credit_card}</p>")
        f.write(f"<p>Expense from Savings account: {exp_savings}</p>")
        f.write(table_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(expense_fig.to_html(full_html=False, include_plotlyjs='cdn'))

def log_transaction(file, date, description, category, amount, t_type, account):
    with open(file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, description, category, amount, t_type, account])

# Example usage
df = load_data('expenses.csv')

# Generate interactive report for a specific date range
generate_report(df, start_date='2024-07-01', end_date='2024-07-10')

# Generate interactive report for a specific month
# generate_report(df, year=2024, month=7)

