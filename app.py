import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for PDF parsing
import openpyxl
import tempfile
import os
import json
from google.cloud import storage
import vertexai
from vertexai import generative_models, init

PROJECT_ID = 'deft-clarity-461011-c7'
REGION = 'us-central1'
MODEL_NAME = 'gemini-2.5-pro'  # Or latest model available

# ---------- INITIALIZE VERTEX AI ----------
init(project=PROJECT_ID, location=REGION)

# Initialize the best available Gemini model (stable, accurate, consistent)
gemini_model = generative_models.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "temperature": 0.0,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048
    }
)


# Set up your GCS bucket name
GCS_BUCKET_NAME = "cxo-prism"

def upload_to_gcs(local_path, gcs_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    return f"gs://{GCS_BUCKET_NAME}/{gcs_path}"

st.set_page_config(page_title="Document Comparison QC Tool", layout="wide")
st.title("📑 GenAI Document Comparison QC Tool")

st.markdown("Upload your **Quotation** (PDF or Excel) and **Policy Schedule** (PDF) to compare them and generate a QC report.")

col1, col2 = st.columns(2)

with col1:
    quote_file = st.file_uploader("Upload Quotation (PDF/Excel)", type=["pdf", "xlsx"])

with col2:
    policy_file = st.file_uploader("Upload Policy Schedule (PDF)", type=["pdf"])

st.markdown("### 🔧 Field Mapping Configuration")
default_fields = ["Sum Insured", "Premium", "Deductible", "Endorsements", "Exclusions"]
field_mappings = st.text_area(
    "Enter parameters to compare (comma-separated):",
    value=", ".join(default_fields)
)

fields_to_compare = [f.strip() for f in field_mappings.split(",") if f.strip()]
def clean_text(text):
    return " ".join(text.split())

if st.button("Generate QC Report"):
    if not quote_file or not policy_file:
        st.error("Please upload both the Quotation and Policy Schedule files.")
    else:
        with st.spinner("Extracting and comparing documents using Gemini..."):
            def extract_text_from_pdf(file):
                text = ""
                with fitz.open(stream=file.read(), filetype="pdf") as doc:
                    for page in doc:
                        text += page.get_text()
                return text

            #def extract_text_from_excel(file):
            def extract_text_from_excel(file, max_rows=50):
                dfs = pd.read_excel(file, sheet_name=None)
                text = ""
                for sheet, df in dfs.items():
                    df = df.head(max_rows)
                    text += f"\n--- Sheet: {sheet} ---\n"
                    text += df.to_string()
                return text

            if quote_file.name.endswith(".pdf"):
                quote_text = extract_text_from_pdf(quote_file)
            else:
                quote_text = extract_text_from_excel(quote_file)

            policy_text = extract_text_from_pdf(policy_file)
            quote_text = clean_text(quote_text[:20000])
            policy_text = clean_text(policy_text[:20000])


            # Gemini prompt with strict JSON output requirement
            prompt = f"""
            You are a commercial insurance underwriter. Your job is to perform accurate comparisons.
            Use only the information provided in the documents below. Do not assume or hallucinate values.

            Documents:
            1. Quotation:
            {quote_text}

            2. Policy Schedule:
            {policy_text}

            Compare the following fields: {', '.join(fields_to_compare)}.

            Output a valid JSON array where each element has the following keys:
              - parameter (string)
              - quotation_value (string)
              - policy_value (string)
              - match_status ("Match", "Not Match", or "Missing")
              - comments (string)

            Ensure the format is consistent for every item and no extra text is added.
            """

            response = gemini_model.generate_content(prompt)
            response_text = response.text

            try:
                response_text = response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content.parts else ""

                if not response_text.strip():
                    st.error("⚠️ Gemini did not return any output. The input may be too long or blocked by safety filters.")
                    st.stop()
                data = json.loads(response_text)
                df = pd.DataFrame(data)

                # Add score summary at the top
                total = len(df)
                matches = df['match_status'].str.lower().eq('match').sum()
                not_matches = df['match_status'].str.lower().eq('not match').sum()
                missing = df['match_status'].str.lower().eq('missing').sum()
                match_score = round((matches / total) * 100, 2) if total else 0

                st.markdown(f"### ✅ Match Summary")
                st.markdown(f"- **Total Fields Compared**: {total}")
                st.markdown(f"- ✅ **Matched**: {matches}")
                st.markdown(f"- ❌ **Not Matched**: {not_matches}")
                st.markdown(f"- ⚠️ **Missing**: {missing}")
                st.markdown(f"- 🧮 **Match Score**: {match_score}%")

                st.dataframe(df)
                temp_dir = tempfile.mkdtemp()
                output_path = os.path.join(temp_dir, "qc_report.xlsx")
                df.to_excel(output_path, index=False)

                 # Upload to GCS with timestamped version
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                base_q = quote_file.name.split('.')[0]
                base_p = policy_file.name.split('.')[0]
                gcs_path = f"reports/qc_report_{base_q}_{base_p}_{timestamp}.xlsx"
                gcs_url = upload_to_gcs(output_path, gcs_path)

                st.success(f"✅ Report saved to GCS: {gcs_url}")
                with open(output_path, "rb") as f:
                    st.download_button("Download QC Report (Excel)", f, file_name="QC_Report.xlsx")
            except Exception as e:
                st.warning("Could not parse JSON. Showing raw output as fallback:")
                st.markdown(str(response))
                st.error(str(e))
