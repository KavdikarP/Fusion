import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import psycopg2
import pandas as pd
from fpdf import FPDF
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# ---------- CONFIGURATION ---------

# POSTGRES_CONFIG = {
#     'host': '35.244.42.223',
#     'database': 'nl-report-db',
#     'user': 'postgres',
#     'password': 'test123',
#     'port': '6432'
# }
POSTGRES_CONFIG = {
    'host': 'localhost',
    'database': 'cxo_prism',
    'user': 'local_user',
    'password': 'local_password',
    'port': '5432'
}

PROJECT_ID = 'deft-clarity-461011-c7'
REGION = 'us-central1'
MODEL_NAME = 'gemini-2.5-flash-lite'  # Or latest model available

# ---------- INITIALIZE VERTEX AI ----------
vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel(MODEL_NAME)

# ---------- FUNCTION: GENERATE SQL ----------
def generate_sql(natural_query, table_schema):
    prompt = f"""You are a PostgreSQL SQL expert. Given the table schema below, generate a single-line SQL query that answers the user's question.

Important rules:
- Only write a syntactically correct SELECT query.
- Do NOT use INSERT, UPDATE, DELETE, DROP, or any other modifying statements.
- Do NOT include explanations, markdown, or comments.
- Only return the raw SQL query on a single line, nothing else.

Schema:
{table_schema}

User Question:
{natural_query}"""
    response = model.generate_content([prompt])
    sql_query = response.text.strip()
    if not sql_query.lower().startswith("select"):
        raise Exception("Generated SQL query is invalid or not a SELECT statement.")
    return sql_query

# ---------- FUNCTION: EXECUTE SQL ----------
def run_sql(query):
    engine = create_engine(f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}")
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(query, connection)
        return df
    except SQLAlchemyError as e:
        raise Exception(f"SQLAlchemy Error: {e}")
    finally:
        engine.dispose()

# ---------- FUNCTION: EXPORT PDF ----------
def dataframe_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i in range(len(df)):
        row = ', '.join(str(x) for x in df.iloc[i])
        pdf.cell(200, 10, txt=row, ln=True)
    pdf_path = "/tmp/output.pdf"
    pdf.output(pdf_path)
    return pdf_path

# ---------- STREAMLIT UI ----------
st.title("Natural Language SQL Query App (Vertex AI + Postgres)")

user_question = st.text_input("Ask your question about the database:")

output_format = st.radio("Choose Output Format:", ["Natural Language", "Download PDF"])

if st.button("Run Query"):
    if user_question.strip() == "":
        st.error("Please enter a question.")
    else:
        # Get Table Schema for prompting
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""SELECT table_name, column_name, data_type 
                          FROM information_schema.columns 
                          WHERE table_schema = 'public'""")
        schema_rows = cursor.fetchall()
        conn.close()

        schema_text = ""
        for row in schema_rows:
            schema_text += f"Table: {row[0]} - Column: {row[1]} ({row[2]})\n"

        sql_query = generate_sql(user_question, schema_text)
        st.code(sql_query, language='sql')
        if not sql_query.strip():
            st.error("Generated SQL query is empty or invalid.")
            raise Exception("Generated SQL query is empty or invalid.")
        try:
            df_result = run_sql(sql_query)
            st.success("Query Executed Successfully.")

            if output_format == "Natural Language":
                st.dataframe(df_result)
            else:
                pdf_file_path = dataframe_to_pdf(df_result)
                with open(pdf_file_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="query_result.pdf")

        except Exception as e:
            st.error(f"Error executing SQL: {e}")
