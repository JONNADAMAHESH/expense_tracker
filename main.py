import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Streamlit page config
st.set_page_config(page_title="Smart Expense Tracker", layout="centered")

# Initialize expenses in session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# Function to load default CSV
def load_default_csv():
    default_path = "C://Users//jonna//Downloads//expenses.csv"
    if os.path.exists(default_path):
        try:
            st.session_state.expenses = pd.read_csv(default_path)
            st.success("Expenses loaded from default file!")
        except Exception as e:
            st.warning(f"Failed to load default file: {e}")

# Function to add an expense
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]],
                               columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

# File uploader to allow manual loading
def manual_file_upload():
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)
        st.success("Expenses loaded from uploaded file!")

# Save expenses to CSV
def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved to 'expenses.csv'")

# Visualize expenses by category
def visualize_expenses():
    if st.session_state.expenses.empty:
        st.warning("No expenses to visualize!")
        return

    fig, ax = plt.subplots()
    sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', estimator=sum, ci=None, ax=ax)
    ax.set_title("Total Expenses by Category")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Load default CSV when app starts
load_default_csv()

# UI
st.title("Smart Expense Tracker")

with st.sidebar:
    st.subheader("Add New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")

    if st.button("Add Expense"):
        add_expense(date, category, amount, description)
        st.success("Expense added!")

    st.markdown("---")
    st.subheader("File Operations")
    if st.button("Save to CSV"):
        save_expenses()
    manual_file_upload()

# Main content
st.subheader("Current Expenses")
st.dataframe(st.session_state.expenses, use_container_width=True)

st.subheader("Expense Visualization")
if st.button("Show Chart"):
    visualize_expenses()