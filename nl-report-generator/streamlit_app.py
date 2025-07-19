import streamlit as st
import requests

# API Endpoint from Cloud Run
API_URL = "https://YOUR_CLOUD_RUN_URL/query"

st.title("Natural Language Report Generator 📊")

# User Input
nl_query = st.text_area("Enter your natural language query:", height=150)
file_format = st.selectbox("Select Output Format:", ["Excel", "PDF", "PPT"])

if st.button("Generate Report"):
    if not nl_query.strip():
        st.error("Please enter a query.")
    else:
        with st.spinner("Generating your report..."):
            payload = {
                "query": nl_query,
                "format": file_format.lower()
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    download_url = data.get("file_url")
                    sql_used = data.get("sql_used")
                    st.success("Report generated successfully!")
                    st.write(f"**SQL Query Generated:** `{sql_used}`")
                    st.markdown(f"[Download your {file_format} report]({download_url})", unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Request failed: {e}")
