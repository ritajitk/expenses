#!/usr/bin/env python

import pandas as pd
import plotly.express as px
import plotly.io as pio
import io
from flask import Flask, render_template, request

# Load data
def load_data(file):
    df = pd.read_csv(file, parse_dates=['Date'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))
    return df

# Generate report
def generate_report(df, start_date, end_date):
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    total_inc = df_filtered[df_filtered['Type'] == 'Income']['Amount'].sum()
    total_exp = df_filtered[df_filtered['Type'] == 'Expense']['Amount'].sum()
    balance = total_inc - total_exp

    exp_credit_card = df_filtered[(df_filtered['Account'] == 'Credit Card') & (df_filtered['Type'] == 'Expense')]['Amount'].sum()
    exp_savings = df_filtered[(df_filtered['Account'] == 'Savings') & (df_filtered['Type'] == 'Expense')]['Amount'].sum()

    # Create a pie chart
    expense_data = df_filtered[df_filtered['Type'] == 'Expense'].groupby(['Category'])['Amount'].sum().reset_index()
    expense_fig = px.pie(expense_data, names='Category', values='Amount', title='Expenses by Category')

    # Save the figure to a StringIO object and get HTML
    img_str = io.StringIO()
    pio.write_html(expense_fig, file=img_str, auto_open=False)
    img_str.seek(0)
    plot_html = img_str.getvalue()

    return {
        'total_income': total_inc,
        'total_expense': total_exp,
        'balance': balance,
        'exp_credit_card': exp_credit_card,
        'exp_savings': exp_savings,
        'plot_html': plot_html
    }

# Flask application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        df = load_data('expenses.csv')
        report = generate_report(df, start_date, end_date)
        return render_template('report.html', **report)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
