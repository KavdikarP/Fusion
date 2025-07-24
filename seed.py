import psycopg2

# Update these if you're using a different DB config
DB_NAME = "cxo_prism"
DB_USER = "local_user"
DB_PASS = "local_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT,
            age INT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS policy (
            policy_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            policy_type TEXT,
            start_date DATE,
            end_date DATE,
            premium NUMERIC,
            sum_insured NUMERIC
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id SERIAL PRIMARY KEY,
            policy_id INT REFERENCES policy(policy_id),
            claim_date DATE,
            claim_amount NUMERIC,
            claim_status TEXT
        );
    """)

def insert_dummy_data(cur):
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()[0] > 0:
        print("Tables already have data. Skipping inserts.")
        return

    cur.execute("""
        INSERT INTO users (name, email, city, age) VALUES
        ('Amit Kumar', 'amit@example.com', 'Mumbai', 34),
        ('Neha Sharma', 'neha@example.com', 'Delhi', 29),
        ('Ravi Mehta', 'ravi@example.com', 'Pune', 42);
    """)

    cur.execute("""
        INSERT INTO policy (user_id, policy_type, start_date, end_date, premium, sum_insured) VALUES
        (1, 'Health', '2023-01-01', '2024-01-01', 10000, 500000),
        (2, 'Motor', '2023-05-15', '2024-05-15', 8000, 300000),
        (3, 'Travel', '2023-12-01', '2024-01-01', 2000, 100000);
    """)

    cur.execute("""
        INSERT INTO claims (policy_id, claim_date, claim_amount, claim_status) VALUES
        (1, '2023-06-10', 20000, 'Approved'),
        (2, '2023-09-20', 15000, 'Rejected'),
        (3, '2023-12-20', 10000, 'Pending');
    """)

def main():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        create_tables(cur)
        insert_dummy_data(cur)
        conn.commit()
        print("✅ Tables created and dummy data inserted.")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
