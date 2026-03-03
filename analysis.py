from __future__ import annotations

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def _build_monthly_summary(transactions: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(transactions)
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expense", "net"])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expense", "net"])

    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("month")["amount"]
        .agg(
            income=lambda x: x[x > 0].sum(),
            expense=lambda x: -x[x < 0].sum(),
            net="sum",
        )
        .fillna(0)
        .reset_index()
    )
    monthly["month"] = monthly["month"].astype(str)
    return monthly


def create_income_expense_chart(transactions: list[dict]) -> Figure:
    """Create a polished monthly income vs expense trend chart."""
    monthly = _build_monthly_summary(transactions)

    fig = Figure(figsize=(8, 4.5))
    fig.patch.set_facecolor("#fffaf4")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#fffdf9")

    if monthly.empty:
        ax.text(
            0.5,
            0.5,
            "No transactions yet",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=13,
            color="#7a6651",
        )
        ax.set_xticks([])
        ax.set_yticks([])
        return fig

    sns.lineplot(
        data=monthly,
        x="month",
        y="income",
        label="Income",
        ax=ax,
        marker="o",
        color="#1b9aaa",
        linewidth=2.5,
    )
    sns.lineplot(
        data=monthly,
        x="month",
        y="expense",
        label="Expense",
        ax=ax,
        marker="o",
        color="#e76f51",
        linewidth=2.5,
    )

    ax.fill_between(monthly["month"], monthly["income"], alpha=0.08, color="#1b9aaa")
    ax.fill_between(monthly["month"], monthly["expense"], alpha=0.08, color="#e76f51")

    ax.set_title("Monthly Income vs Expense", fontsize=15, fontweight="bold", color="#2f2a24")
    ax.set_xlabel("Month", color="#4e463d")
    ax.set_ylabel("Amount", color="#4e463d")
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.legend(frameon=False)
    fig.autofmt_xdate(rotation=25)
    fig.tight_layout()
    return fig


def get_chart_canvas(transactions: list[dict]) -> FigureCanvas:
    """Return a FigureCanvas that renders the trend chart."""
    return FigureCanvas(create_income_expense_chart(transactions))
