import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('superstore_clean.csv')

st.title("📊 Sales Dashboard")

# KPI Section
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", int(df['sales'].sum()))
col2.metric("Total Profit", int(df['profit'].sum()))
col3.metric("Total Quantity", int(df['quantity'].sum()))

# -------------------------------
# 💬 Interactive Chatbox (Sidebar)
# -------------------------------
st.sidebar.header("💬 Ask Business Questions")

# Function to answer questions
def answer_question(q, df):
    q = q.lower()

    if "total sales" in q:
        return f"Total Sales: ${df['sales'].sum():,.2f}"

    elif "total profit" in q:
        return f"Total Profit: ${df['profit'].sum():,.2f}"

    elif "best region" in q:
        best = df.groupby('region')['profit'].sum().idxmax()
        return f"Most profitable region is: {best}"

    elif "lowest profit region" in q:
        worst = df.groupby('region')['profit'].sum().idxmin()
        return f"Least profitable region is: {worst}"

    elif "top category" in q:
        top = df.groupby('category')['sales'].sum().idxmax()
        return f"Top selling category is: {top}"

    elif "most discount" in q:
        region = df.groupby('region')['discount'].mean().idxmax()
        return f"Region with highest discount: {region}"

    elif "profit per item" in q:
        avg = df['profit_per_item'].mean()
        return f"Average profit per item is: ${avg:.2f}"

    else:
        return "Sorry, I don't understand. Try another question!"

# -------------------------------
# 🧠 Suggested Questions (Buttons)
# -------------------------------
st.sidebar.markdown("### 💡 Try these questions:")

questions = [
    "What is total sales?",
    "What is total profit?",
    "Which is the best region?",
    "Which region has lowest profit?",
    "What is the top category?",
    "Which region gives most discount?",
    "What is profit per item?"
]

# Store selected question
selected_q = None

for q in questions:
    if st.sidebar.button(q):
        selected_q = q

# Manual input (optional)
user_question = st.sidebar.text_input("Or type your own question:")

# Decide which question to answer
final_question = selected_q if selected_q else user_question

# Show answer
if final_question:
    response = answer_question(final_question, df)
    st.sidebar.write("📊 Answer:")
    st.sidebar.success(response)

# Region Sales
st.subheader("🌍 Sales by Region")
region_sales = df.groupby('region')['sales'].sum()
st.bar_chart(region_sales)

# Category Profit
st.subheader("🏷️ Profit by Category")
category_profit = df.groupby('category')['profit'].sum()
st.bar_chart(category_profit)

# Discount Impact
st.subheader("💰 Discount vs Profit")
st.scatter_chart(df[['discount', 'profit']])

# Profit per Item
st.subheader("📦 Profit per Item by Category")
ppi = df.groupby('category')['profit_per_item'].mean()
st.bar_chart(ppi)

# Filter (Interactive)
st.subheader("🔍 Filter by Region")
selected_region = st.selectbox("Select Region", df['region'].unique())

filtered_df = df[df['region'] == selected_region]
st.write(filtered_df.head())

st.write(df.head())