import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 Personal Expense Tracker")
st.write("Track your daily expenses easily!")

# Store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar
st.sidebar.header("➕ Add Expense")

with st.sidebar.form("expense_form"):

    expense_name = st.text_input(
        "Expense Name",
        placeholder="e.g. Food, Shopping"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Shopping", "Travel", "Bills", "Education", "Other"]
    )

    date = st.date_input("Date")

    add_expense = st.form_submit_button("Add Expense")

    if add_expense:

        if expense_name and amount > 0:

            st.session_state.expenses.append({
                "Expense": expense_name,
                "Amount": amount,
                "Category": category,
                "Date": date
            })

            st.success("Expense added successfully! ✅")

        else:
            st.error("Please enter expense name and amount.")


# Main area
if len(st.session_state.expenses) == 0:

    st.info(
        "No expenses added yet. Add your first expense from the sidebar 👉"
    )

else:

    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.expenses)

    # Total expense
    total = df["Amount"].sum()

    st.subheader("📊 Expense Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Expense", f"₹{total:.2f}")
    col2.metric("🧾 Total Entries", len(df))
    col3.metric("📅 Categories", df["Category"].nunique())

    st.divider()

    # Expense table
    st.subheader("📋 Your Expenses")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Category summary
    st.subheader("📈 Category-wise Expenses")

    category_total = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_total)

    # Delete all expenses
    if st.button("🗑️ Delete All Expenses"):

        st.session_state.expenses = []

        st.rerun()
