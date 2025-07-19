from sqlalchemy import create_engine
import pandas as pd

def get_db_engine():
    db_user = "report_user"
    db_pass = "test123"
    db_host = "35.244.42.223"
    db_name = "reporting_db"
    
    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(db_url)
    return engine

def run_sql_and_fetch(sql_query):
    engine = get_db_engine()
    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn)
    return df
