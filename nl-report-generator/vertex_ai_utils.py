from google.cloud import aiplatform, generative_models

aiplatform.init(project="deft-clarity-461011-c7", location="asia-south1")

model = generative_models.GenerativeModel("gemini-1.5-pro")

def generate_sql_from_nl(nl_query):
    prompt = f"Convert this natural language request into a PostgreSQL SQL query (only SQL, no explanation): {nl_query}"
    response = model.generate_content(
        contents=[prompt],
        generation_config={"temperature": 0}
    )
    return response.text.strip()

