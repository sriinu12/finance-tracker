# analysis.py
# Description: Provides data visualization functions using Matplotlib and Seaborn.

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def create_income_expense_chart(transactions):
    """
    Given a list of transactions (each as a dict with keys: date, amount, category, description),
    create a line chart of monthly income vs expense with a custom title style.
    """
    # Convert the list of transactions to a DataFrame
    df = pd.DataFrame(transactions)
    if df.empty:
        # Create an empty chart if no data is available
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')
        return fig

    # Ensure the 'date' column is a datetime object and extract month information
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)

    # Group data by month. Assume positive amounts represent income and negative amounts represent expenses.
    monthly = df.groupby('month').agg(
        income=pd.NamedAgg(column='amount', aggfunc=lambda x: x[x > 0].sum()),
        expense=pd.NamedAgg(column='amount', aggfunc=lambda x: -x[x < 0].sum())
    ).fillna(0).reset_index()

    # Create a Matplotlib Figure and plot with Seaborn styling
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    sns.lineplot(data=monthly, x='month', y='income', label='Income', ax=ax, marker="o")
    sns.lineplot(data=monthly, x='month', y='expense', label='Expense', ax=ax, marker="o")
    
    # Set a custom title with improved font and color
    ax.set_title("Monthly Income vs Expense", fontdict={'fontsize': 18, 'fontweight': 'bold', 'color': 'navy'})
    
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()
    fig.autofmt_xdate()  # Rotate date labels for better readability

    return fig

def get_chart_canvas(transactions):
    """
    Return a FigureCanvas widget that embeds the chart for the given transactions.
    """
    fig = create_income_expense_chart(transactions)
    canvas = FigureCanvas(fig)
    return canvas
