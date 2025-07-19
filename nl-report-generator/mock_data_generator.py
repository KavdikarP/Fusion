import pandas as pd
import random
import uuid
from faker import Faker
from sqlalchemy import create_engine

fake = Faker()

def get_db_engine():
    db_user = "report_user"
    db_pass = "test123"
    db_host = "35.244.42.223"
    db_name = "reporting_db"
    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(db_url)
    return engine

def generate_mock_data():
    users = []
    policies = []
    claims = []

    for _ in range(100):
        user_id = str(uuid.uuid4())
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address().replace("\n", ", ")
        city = fake.city()
        state = fake.state()
        country = fake.country()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=75)
        customer_since = fake.date_between(start_date='-5y', end_date='today')

        users.append([user_id, name, email, phone, address, city, state, country, dob, customer_since])

        for _ in range(random.randint(1, 3)):
            policy_id = str(uuid.uuid4())
            policy_number = fake.bothify(text='POL-#####')
            policy_type = random.choice(["Motor", "Health", "Travel", "Property"])
            start_date = fake.date_between(start_date='-2y', end_date='today')
            end_date = fake.date_between(start_date=start_date, end_date='+1y')
            premium_amount = round(random.uniform(3000, 50000), 2)
            sum_insured = premium_amount * 10
            policy_status = random.choice(["Active", "Expired", "Cancelled"])
            created_at = start_date

            policies.append([policy_id, policy_number, user_id, policy_type, start_date, end_date, premium_amount, sum_insured, policy_status, created_at])

            for _ in range(random.randint(0, 2)):
                claim_id = str(uuid.uuid4())
                claim_number = fake.bothify(text='CLM-#####')
                claim_type = random.choice(["Accident", "Theft", "Damage", "Medical"])
                claim_amount = round(random.uniform(1000, 20000), 2)
                claim_status = random.choice(["Filed", "Approved", "Rejected", "Settled"])
                claim_date = fake.date_between(start_date=start_date, end_date=end_date)
                settlement_amount = claim_amount if claim_status in ["Approved", "Settled"] else 0
                settled_on = claim_date if claim_status in ["Approved", "Settled"] else None

                claims.append([claim_id, policy_id, claim_number, claim_type, claim_amount, claim_status, claim_date, settlement_amount, settled_on])

    return users, policies, claims

def insert_mock_data():
    engine = get_db_engine()
    users, policies, claims = generate_mock_data()

    users_df = pd.DataFrame(users, columns=["user_id", "name", "email", "phone_number", "address", "city", "state", "country", "date_of_birth", "customer_since"])
    policies_df = pd.DataFrame(policies, columns=["policy_id", "policy_number", "user_id", "policy_type", "start_date", "end_date", "premium_amount", "sum_insured", "policy_status", "created_at"])
    claims_df = pd.DataFrame(claims, columns=["claim_id", "policy_id", "claim_number", "claim_type", "claim_amount", "claim_status", "claim_date", "settlement_amount", "settled_on"])

    users_df.to_sql('user_master', engine, if_exists='append', index=False)
    policies_df.to_sql('policy_master', engine, if_exists='append', index=False)
    claims_df.to_sql('claim_master', engine, if_exists='append', index=False)

if __name__ == "__main__":
    insert_mock_data()