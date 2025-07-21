import streamlit as st
import pandas as pd
import os
from vertex_ai_utils import generate_sql_from_nl
from db_utils import fetch_sql_results
from report_generator import generate_pdf_report, generate_excel_report, generate_ppt_report

# API Endpoint from Cloud Run
#API_URL = "https://cxo-prism-799196756327.asia-south1.run.app//query"

st.set_page_config(page_title="CXO's Prism")
st.title("CXO's Prism - Insurance AI Reporting Tool")

query_input = st.text_area("Enter your natural language query:")

output_format = st.selectbox("Select Report Format", ["PDF", "Excel", "PowerPoint"])

if st.button("Generate Report"):
    if not query_input.strip():
        st.error("Please enter a query.")
    else:
        st.info("Generating SQL using Vertex AI...")
        sql_query = generate_sql_from_nl(query_input)
        st.code(sql_query)

        st.info("Fetching Data from Database...")
        df = fetch_sql_results(sql_query)

        if df.empty:
            st.warning("No data found for your query.")
        else:
            st.dataframe(df)
            st.success(f"Generating {output_format} report...")

            if output_format == "PDF":
                report_url = generate_pdf_report(df)
            elif output_format == "Excel":
                report_url = generate_excel_report(df)
            else:
                report_url = generate_ppt_report(df)

            st.success("Report generated and uploaded to Cloud Storage.")
            st.markdown(f"[Download {output_format} Report]({report_url})")


