import psycopg2
import random
import datetime
from faker import Faker

# Database info
DB_HOST = "localhost"
DB_NAME = "cdc-debezium"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def connect_to_db():
    """Connects to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """Creates the 'transactions' table if it doesn't exist."""
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
            transaction_id  VARCHAR(255) PRIMARY KEY,
            user_id         VARCHAR(255),
            timestamp       TIMESTAMP,
            amount          DECIMAL,
            currency        VARCHAR(255),
            city            VARCHAR(255),
            country         VARCHAR(255),
            merchant_name   VARCHAR(255),
            payment_method  VARCHAR(255),
            ip_address      VARCHAR(255),
            voucher_code    VARCHAR(255)
        )
        """)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def generate_fake_transaction():
    """Generates a fake transaction dictionarie."""
    fake = Faker()

    return {
        "transaction_id": fake.uuid4(),
        "user_id": fake.user_name(),
        "timestamp": fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d %H:%M:%S"),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(['USD', 'GBP']),
        'city': fake.city(),
        "country": fake.country(),
        "merchantName": fake.company(),
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer']),
        "ipAddress": fake.ipv4(),
        "voucherCode": random.choice(['', 'DISCOUNT10', '', 'DISCOUNT25'])
    }

def insert_transaction(conn, transaction):
    """Inserts the generated transaction into the database."""
    try:
        cur = conn.cursor()
        cur.execute(
        """
        INSERT INTO transactions(transaction_id, user_id, timestamp, amount, currency, city, country, merchant_name, payment_method, 
        ip_address, voucher_code)
        VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
                transaction["transaction_id"],
                transaction["user_id"],
                transaction["timestamp"],
                transaction["amount"],
                transaction["currency"],
                transaction["city"],
                transaction["country"],
                transaction["merchantName"],
                transaction["paymentMethod"],
                transaction["ipAddress"],
                transaction["voucherCode"]
             )
    )

        conn.commit()
        print("one transaction inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting transactions: {e}")
        conn.rollback()

def main():
    """Main function to orchestrate the process."""
    conn = connect_to_db()
    if conn:
        create_table(conn)
        transaction = generate_fake_transaction()
        insert_transaction(conn, transaction)
        conn.close()

if __name__ == "__main__":
    main()
