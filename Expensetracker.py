import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Tracker")
st.write("Track your daily expenses easily!")

# Initialize expense data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]
)
amount = st.sidebar.number_input(
    "Amount (₹)",
    min_value=0.0,
    step=10.0
)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    if amount > 0:
        st.session_state.expenses.append({
            "Date": date,
            "Category": category,
            "Amount": amount,
            "Description": description
        })
        st.sidebar.success("Expense added! ✅")
    else:
        st.sidebar.error("Please enter an amount.")

# Display expenses
if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    total = df["Amount"].sum()
    count = len(df)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Total Expense", f"₹{total:.2f}")

    with col2:
        st.metric("🧾 Total Entries", count)

    st.subheader("📋 Expense Details")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Category Summary")

    summary = df.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(summary.set_index("Category"))

else:
    st.info("No expenses added yet. Add your first expense from the sidebar 👈")
