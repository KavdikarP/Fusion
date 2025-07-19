
from google.cloud import aiplatform

aiplatform.init(project="deft-clarity-461011-c7", location="asia-south1")

def generate_sql_from_nl(nl_query):
    model = aiplatform.LanguageModel.from_pretrained("gemini-pro")
    prompt = f"Convert this natural language question into SQL for PostgreSQL: {nl_query}"
    response = model.predict(prompt=prompt, temperature=0)
    return response.text.strip()
