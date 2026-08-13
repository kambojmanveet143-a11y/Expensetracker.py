import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# CSV File
# -----------------------------
FILE = "expenses.csv"

# Create CSV if it doesn't exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
    df.to_csv(FILE, index=False)

# Load expenses
df = pd.read_csv(FILE)

# -----------------------------
# Title
# -----------------------------
st.title("💰 Personal Expense Tracker")
st.write("Track your daily expenses and understand where your money goes.")

st.divider()

# -----------------------------
# SIDEBAR - ADD EXPENSE
# -----------------------------
st.sidebar.header("➕ Add New Expense")

expense_date = st.sidebar.date_input(
    "Date",
    date.today()
)

amount = st.sidebar.number_input(
    "Amount (₹)",
    min_value=0.0,
    step=10.0
)

category = st.sidebar.selectbox(
    "Category",
    [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Education",
        "Entertainment",
        "Health",
        "Other"
    ]
)

description = st.sidebar.text_input(
    "Description"
)

add_expense = st.sidebar.button(
    "Add Expense"
)

# -----------------------------
# SAVE EXPENSE
# -----------------------------
if add_expense:

    if amount <= 0:
        st.sidebar.error("Please enter a valid amount.")

    else:
        new_expense = pd.DataFrame({
            "Date": [expense_date],
            "Amount": [amount],
            "Category": [category],
            "Description": [description]
        })

        df = pd.concat(
            [df, new_expense],
            ignore_index=True
        )

        df.to_csv(FILE, index=False)

        st.sidebar.success("Expense added successfully! 🎉")
        st.rerun()

# -----------------------------
# TOTAL AMOUNT
# -----------------------------
if len(df) > 0:
    total_amount = df["Amount"].sum()
else:
    total_amount = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Spent",
        f"₹{total_amount:,.2f}"
    )

with col2:
    st.metric(
        "🧾 Total Expenses",
        len(df)
    )

with col3:
    if len(df) > 0:
        average = df["Amount"].mean()
    else:
        average = 0

    st.metric(
        "📊 Average Expense",
        f"₹{average:,.2f}"
    )

st.divider()

# -----------------------------
# SPENDING BY CATEGORY
# -----------------------------
st.subheader("📊 Spending by Category")

if len(df) > 0:

    category_data = df.groupby(
        "Category"
