import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# ---------- CONFIG ---------- #
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ---------- DATA LOADING ---------- #
@st.cache_data

def load_data():
    conn = psycopg2.connect(
    database="sales_db",
    user="postgres",
    password="Salunkhe@123",
    host="localhost",
    port="5432"
)


    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Revenue'] = df['Sales']
    return df

df = load_data()

# ---------- SIDEBAR ---------- #
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

df_filtered = df[df['Region'].isin(regions) & df['Category'].isin(categories)]

# ---------- KPI SECTION ---------- #
st.title("📊 Sales Dashboard")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.2f}")
col2.metric("Avg Order Value", f"${df_filtered['Revenue'].mean():,.2f}")
col3.metric("Total Orders", df_filtered.shape[0])

# ---------- VISUALIZATIONS ---------- #
st.markdown("### 📈 Monthly Revenue")
monthly_sales = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M')).sum(numeric_only=True)
monthly_sales.index = monthly_sales.index.astype(str)
st.line_chart(monthly_sales['Revenue'])

st.markdown("### 🛍️ Top 10 Products by Revenue")
top_products = df_filtered.groupby('Product Name').sum(numeric_only=True).sort_values(by='Revenue', ascending=False).head(10)
st.bar_chart(top_products['Revenue'])

st.markdown("### 🌍 Revenue by Region")
region_sales = df_filtered.groupby('Region')['Revenue'].sum()
fig, ax = plt.subplots()
ax.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# ---------- EXPORT DATA ---------- #
st.markdown("### 💾 Download Filtered Data")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_filtered)
st.download_button("Download CSV", csv, "filtered_sales_data.csv", "text/csv")
