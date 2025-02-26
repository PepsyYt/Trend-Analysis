import os
from datetime import datetime
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()

class User:
    def __init__(self, id=None, email=None, password=None, full_name=None):
        self.id = id
        self.email = email
        self.password = password
        self.full_name = full_name

    @staticmethod
    def create(email, password, full_name):
        if not email or not password:
            raise ValueError("Email and password are required")

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Check if email already exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone() is not None:
                raise ValueError("Email already registered")

            password_hash = generate_password_hash(password)

            cur.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s) RETURNING id",
                (email, password_hash, full_name)
            )
            user_id = cur.fetchone()[0]
            conn.commit()

            return User(id=user_id, email=email, full_name=full_name)
        except psycopg2.Error as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_email(email):
        if not email:
            return None

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id, email, password_hash, full_name FROM users WHERE email = %s",
                (email,)
            )
            user_data = cur.fetchone()

            if user_data:
                return User(
                    id=user_data[0],
                    email=user_data[1],
                    password=user_data[2],
                    full_name=user_data[3]
                )
            return None
        finally:
            cur.close()
            conn.close()

    def verify_password(self, password):
        return check_password_hash(self.password, password)