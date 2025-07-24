-- Drop tables if they exist
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS customers;

-- Table: customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: policies
CREATE TABLE policies (
    policy_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    policy_number VARCHAR(50) UNIQUE NOT NULL,
    policy_type VARCHAR(50),
    coverage_amount NUMERIC(15, 2),
    premium_amount NUMERIC(15, 2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    CONSTRAINT fk_customer
        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- Table: claims
CREATE TABLE claims (
    claim_id SERIAL PRIMARY KEY,
    policy_id INTEGER NOT NULL,
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    claim_amount NUMERIC(15, 2),
    claim_reason TEXT,
    claim_date DATE,
    status VARCHAR(20) DEFAULT 'Pending',
    CONSTRAINT fk_policy
        FOREIGN KEY(policy_id)
        REFERENCES policies(policy_id)
        ON DELETE CASCADE
);

-- Sample Customers
INSERT INTO customers (name, email, phone, city, state, zip_code)
VALUES 
('John Doe', 'john.doe@example.com', '9999999999', 'Mumbai', 'Maharashtra', '400001'),
('Jane Smith', 'jane.smith@example.com', '8888888888', 'Delhi', 'Delhi', '110001'),
('Ravi Kumar', 'ravi.kumar@example.com', '7777777777', 'Bangalore', 'Karnataka', '560001');

-- Sample Policies
INSERT INTO policies (customer_id, policy_number, policy_type, coverage_amount, premium_amount, start_date, end_date, status)
VALUES
(1, 'POL001', 'Health', 500000, 12000, '2025-01-01', '2026-01-01', 'Active'),
(2, 'POL002', 'Vehicle', 800000, 15000, '2025-02-01', '2026-02-01', 'Active'),
(3, 'POL003', 'Life', 1000000, 20000, '2025-03-01', '2030-03-01', 'Active');

-- Sample Claims
INSERT INTO claims (policy_id, claim_number, claim_amount, claim_reason, claim_date, status)
VALUES
(1, 'CLM001', 25000, 'Hospitalization due to accident', '2025-05-10', 'Approved'),
(2, 'CLM002', 50000, 'Vehicle accident', '2025-06-15', 'Pending'),
(3, 'CLM003', 100000, 'Critical illness claim', '2025-07-01', 'Approved');
