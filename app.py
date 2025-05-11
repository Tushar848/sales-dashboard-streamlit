import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Dashboard (CSV-based)")

# Load data from your CSV
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    return df

df = load_data()

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')

# KPIs
total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Unique Orders", total_orders)

st.markdown("---")

# Region-wise Sales
st.subheader("Sales by Region")
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
region_sales.plot(kind="bar", ax=ax1, color="skyblue")
ax1.set_ylabel("Sales")
ax1.set_xlabel("Region")
st.pyplot(fig1)

# Category-wise Sales
st.subheader("Sales by Category")
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
category_sales.plot(kind="bar", ax=ax2, color="salmon")
ax2.set_ylabel("Sales")
ax2.set_xlabel("Category")
st.pyplot(fig2)

# Time series
st.subheader("Sales Over Time")
monthly_sales = df.groupby(df['Order Date'].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()

fig3, ax3 = plt.subplots(figsize=(10, 4))
monthly_sales.plot(ax=ax3, color="green")
ax3.set_ylabel("Sales")
ax3.set_xlabel("Month")
ax3.set_title("Monthly Sales Trend")
st.pyplot(fig3)

# Raw data toggle
with st.expander("Show Raw Data"):
    st.dataframe(df)
