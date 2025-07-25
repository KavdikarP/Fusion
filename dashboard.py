# streamlit_app.py
import streamlit as st
import plotly.express as px
from datetime import datetime
from app import run_sql

# Load data from PostgreSQL
def load_data():
    user_df = run_sql("SELECT * FROM user_details")
    policy_df = run_sql("SELECT * FROM policy_details")
    claim_df = run_sql("SELECT * FROM claim_details")
    return user_df, policy_df, claim_df

# Main App
st.set_page_config(layout="wide")
st.title("📊 Insurance Management Dashboard")

# Load Data
user_df, policy_df, claim_df = load_data()

# Show current date/time
st.markdown(f"**Last Queried On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Summary Metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Policies", len(policy_df))
col2.metric("Active Policies", len(policy_df[policy_df['policy_status'] == 'Active']))
col3.metric("Total Claims", len(claim_df))
col4.metric("Total Premium", f"₹ {policy_df['premium_amount'].sum():,.2f}")

# --- Data Tables ---
st.subheader("📋 User Details")
st.dataframe(user_df)

st.subheader("📋 Policy Details")
st.dataframe(policy_df)

st.subheader("📋 Claim Details")
st.dataframe(claim_df)

# --- Charts ---
st.subheader("📈 Visual Insights")

# Pie Chart: Claim Status
fig_pie = px.pie(claim_df, names='claim_status', title='Claim Status Distribution')
st.plotly_chart(fig_pie, use_container_width=True)

# Bar Graph: Premium by Line of Business
premium_lob = policy_df.groupby('lob')['premium_amount'].sum().reset_index()
fig_bar = px.bar(premium_lob, x='lob', y='premium_amount', color='lob', title='Premium by Line of Business')
st.plotly_chart(fig_bar, use_container_width=True)

# --- Export Buttons ---
st.subheader("⬇️ Export Reports")

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

col5, col6, col7 = st.columns(3)
col5.download_button("Download Users CSV", convert_df(user_df), "users.csv", "text/csv")
col6.download_button("Download Policies CSV", convert_df(policy_df), "policies.csv", "text/csv")
col7.download_button("Download Claims CSV", convert_df(claim_df), "claims.csv", "text/csv")
